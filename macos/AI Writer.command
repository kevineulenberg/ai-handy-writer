#!/bin/zsh

writer_path="$HOME/.local/bin/ai-writer"

if [[ ! -x "$writer_path" ]]; then
  print -u2 -r -- "AI Handy Writer is not installed at $writer_path."
  print -u2 -r -- "Run scripts/install.sh from the repository first."
  exec /bin/zsh -l
fi

cd "$HOME" || exit 1
exec /bin/zsh -lic 'exec "$HOME/.local/bin/ai-writer"'
