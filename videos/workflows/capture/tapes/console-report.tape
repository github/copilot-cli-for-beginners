Output "../assets/report-raw.mp4"
Output "../assets/report-terminal.txt"
Source tapes/settings.tape
Type "# The workflow saved this report in the project"
Enter
Sleep 2s
Type "fold -s -w 112 release-report.md"
Sleep 700ms
Enter
Sleep 12s
Screenshot "../assets/09-report.png"
