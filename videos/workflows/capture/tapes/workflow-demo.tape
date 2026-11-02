Output "../assets/workflows-raw.mp4"
Output "../assets/workflows-terminal.txt"
Source tapes/settings.tape

Type "# Release readiness: real checks, human review, reusable report"
Enter
Sleep 2s
Type "copilot --experimental --disable-builtin-mcps --allow-all-tools --no-remote"
Sleep 600ms
Enter
Sleep 9s
Screenshot "../assets/01-launched.png"

Type "Run the book-release-check dynamic workflow."
Sleep 1s
Enter
Sleep 22s
Screenshot "../assets/02-checkpoint.png"

Type "/workflows"
Sleep 700ms
Enter
Sleep 6s
Screenshot "../assets/03-workflows.png"
Enter
Sleep 3s
Screenshot "../assets/04-run-details.png"

Type "r"
Sleep 2s
Screenshot "../assets/05-resumed.png"
Sleep 12s
Down 2
Sleep 3s
Screenshot "../assets/06-result.png"
Down
Sleep 4s
Screenshot "../assets/07-saved-report.png"
Tab
Sleep 4s
Screenshot "../assets/08-completed-overview.png"
Ctrl+C
Sleep 500ms
Ctrl+C
Sleep 1s
