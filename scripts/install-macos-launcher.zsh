#!/bin/zsh

set -euo pipefail

script_dir="${0:A:h}"
repo_root="${script_dir:h}"
applescript_source="$repo_root/macos/AI Writer.applescript"
command_source="$repo_root/macos/AI Writer.command"
applications_dir="${AI_WRITER_APPLICATIONS_DIR:-$HOME/Applications}"
app_path="$applications_dir/AI Writer.app"
command_path="$applications_dir/AI Writer.command"
legacy_desktop_command="$HOME/Desktop/AI Writer.command"
writer_path="$HOME/.local/bin/ai-writer"
timestamp="$(date +%Y%m%d-%H%M%S)"
backup_dir="$HOME/.local/share/ai-handy-writer/backups/$timestamp-$$/macos-launcher"
temporary_dir=""
update_desktop_command=false

cleanup() {
  if [[ -n "$temporary_dir" && -d "$temporary_dir" ]]; then
    /usr/bin/find "$temporary_dir" -depth -delete
  fi
}

trap cleanup EXIT

if [[ "$(uname -s)" != "Darwin" ]]; then
  print -u2 -r -- "The AI Writer launcher requires macOS."
  exit 1
fi

if [[ ! -x /usr/bin/osacompile ]]; then
  print -u2 -r -- "Required command not found: /usr/bin/osacompile"
  exit 1
fi

if [[ ! -x "$writer_path" ]]; then
  print -u2 -r -- "AI Handy Writer is not installed at $writer_path."
  print -u2 -r -- "Run scripts/install.sh first."
  exit 1
fi

for source_file in "$applescript_source" "$command_source"; do
  if [[ ! -f "$source_file" ]]; then
    print -u2 -r -- "Launcher source not found: $source_file"
    exit 1
  fi
done

temporary_dir="$(mktemp -d "${TMPDIR:-/tmp}/ai-handy-writer-launcher.XXXXXX")"
temporary_app="$temporary_dir/AI Writer.app"

/usr/bin/osacompile -o "$temporary_app" "$applescript_source"
app_info="$temporary_app/Contents/Info.plist"
if /usr/bin/plutil -extract CFBundleIdentifier raw "$app_info" >/dev/null 2>&1; then
  /usr/bin/plutil -replace CFBundleIdentifier -string "com.aihandywriter.launcher" "$app_info"
else
  /usr/bin/plutil -insert CFBundleIdentifier -string "com.aihandywriter.launcher" "$app_info"
fi
/usr/bin/plutil -replace NSAppleEventsUsageDescription -string \
  "AI Writer opens Terminal and starts the installed ai-writer command." "$app_info"
/usr/bin/codesign --force --deep --sign - "$temporary_app"
mkdir -p "$applications_dir"

for installed_item in "$app_path" "$command_path"; do
  if [[ -e "$installed_item" ]]; then
    mkdir -p "$backup_dir"
    mv "$installed_item" "$backup_dir/"
  fi
done

if [[ -e "$legacy_desktop_command" ]]; then
  mkdir -p "$backup_dir"
  mv "$legacy_desktop_command" "$backup_dir/AI Writer Desktop.command"
  update_desktop_command=true
fi

mv "$temporary_app" "$app_path"
cp "$command_source" "$command_path"
chmod 0755 "$command_path"

if $update_desktop_command; then
  cp "$command_source" "$legacy_desktop_command"
  chmod 0755 "$legacy_desktop_command"
fi

print -r -- "Installed macOS app: $app_path"
print -r -- "Installed command fallback: $command_path"
if [[ -d "$backup_dir" ]]; then
  print -r -- "Archived the previous launcher under: $backup_dir"
fi
if $update_desktop_command; then
  print -r -- "Updated legacy desktop command: $legacy_desktop_command"
fi
print -r -- "Open the app once and allow it to control Terminal when macOS asks."
print -r -- "Assign a global hotkey in Shortcuts by creating an Open App shortcut for AI Writer."
