on run
	set writerCommand to "exec /bin/zsh -lic " & quoted form of "exec \"$HOME/.local/bin/ai-writer\""

	tell application "Terminal"
		do script writerCommand
		activate
	end tell
end run
