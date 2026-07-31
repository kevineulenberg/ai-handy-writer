#!/bin/zsh

set -euo pipefail

script_dir="${0:A:h}"
repo_root="${script_dir:h}"
timestamp="$(date +%Y%m%d-%H%M%S)"

codex_skill_dir="$HOME/.codex/skills/ai-handy-writer"
pi_skill_dir="$HOME/.pi/agent/skills/ai-handy-writer"
config_dir="$HOME/.config/ai-handy-writer"
launcher_dir="$HOME/.local/bin"
codex_profile="$HOME/.codex/ai-handy-writer.config.toml"
codex_notify="$config_dir/copy_codex_turn_to_clipboard.py"
backup_root="$HOME/.local/share/ai-handy-writer/backups/$timestamp"

if [[ "$(uname -s)" != "Darwin" || ! -x /usr/bin/pbcopy ]]; then
  print -u2 -r -- "AI Handy Writer requires macOS and /usr/bin/pbcopy."
  exit 1
fi

for required_command in codex pi; do
  if ! command -v "$required_command" >/dev/null 2>&1; then
    print -u2 -r -- "Required command not found: $required_command"
    exit 1
  fi
done

archive_legacy_dir() {
  local source_dir="$1"
  local label="$2"

  if [[ ! -d "$source_dir" ]]; then
    return
  fi

  mkdir -p "$backup_root"
  mv "$source_dir" "$backup_root/$label"
  print -r -- "Archived $source_dir to $backup_root/$label"
}

archive_legacy_dir "$HOME/.codex/skills/write-skill" "codex-write-skill"
archive_legacy_dir "$HOME/.pi/agent/skills/write-skill" "pi-write-skill"

mkdir -p "$codex_skill_dir" "$pi_skill_dir" "$config_dir" "$launcher_dir"

cp "$repo_root/SKILL.md" "$codex_skill_dir/SKILL.md"
cp "$repo_root/SKILL.md" "$pi_skill_dir/SKILL.md"
cp "$repo_root/README.md" "$pi_skill_dir/README.md"
cp "$repo_root/INSTALL.md" "$pi_skill_dir/INSTALL.md"

cp "$repo_root/bin/ai-writer" "$launcher_dir/ai-writer"
chmod 0755 "$launcher_dir/ai-writer"
ln -sfn "ai-writer" "$launcher_dir/ai-handy-writer"
cp "$repo_root/scripts/copy_codex_turn_to_clipboard.py" "$codex_notify"
chmod 0755 "$codex_notify"

if [[ ! -f "$config_dir/config.zsh" ]]; then
  cp "$repo_root/config/config.zsh" "$config_dir/config.zsh"
  print -r -- "Installed editable defaults at $config_dir/config.zsh"
else
  print -r -- "Kept existing editable defaults at $config_dir/config.zsh"
fi

if ! grep -q '^AI_WRITER_CODEX_SERVICE_TIER=' "$config_dir/config.zsh"; then
  print -r -- 'AI_WRITER_CODEX_SERVICE_TIER="fast"' >> "$config_dir/config.zsh"
  print -r -- "Added Codex service-tier default to $config_dir/config.zsh"
fi

skill_file="$codex_skill_dir/SKILL.md"
escaped_skill_file="${skill_file//\\/\\\\}"
escaped_skill_file="${escaped_skill_file//&/\\&}"
escaped_codex_notify="${codex_notify//\\/\\\\}"
escaped_codex_notify="${escaped_codex_notify//&/\\&}"

sed "s|__AI_HANDY_WRITER_CODEX_SKILL_FILE__|$escaped_skill_file|g" \
  "$repo_root/config/ai-handy-writer.config.toml.in" |
  sed "s|__AI_HANDY_WRITER_CODEX_NOTIFY__|$escaped_codex_notify|g" > "$codex_profile.tmp"
mv "$codex_profile.tmp" "$codex_profile"

print -r -- "Installed Codex skill: $codex_skill_dir"
print -r -- "Installed Pi skill: $pi_skill_dir"
print -r -- "Installed Codex profile: $codex_profile"
print -r -- "Installed launcher: $launcher_dir/ai-writer"
print -r -- "Run 'ai-writer --help' after removing any older ai-writer shell function."
