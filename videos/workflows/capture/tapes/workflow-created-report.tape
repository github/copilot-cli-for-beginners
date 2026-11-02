Output "../assets/report-focused-raw.mp4"
Output "../assets/report-focused-terminal.txt"
Source tapes/settings.tape
Type "sed -n '1,7p;/## Two untested behaviors/,$p' release-report.md | fold -s -w 112"
Sleep 800ms
Enter
Sleep 14s
Screenshot "../assets/report-focused.png"
