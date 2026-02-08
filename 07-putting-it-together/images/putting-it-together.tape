# 07-putting-it-together: Copilot creates high-level plan... demo
# Auto-generated from demos.json - Real copilot execution

Output putting-it-together-demo.gif

Set FontSize 18
Set Width 1000
Set Height 600
Set Theme "Dracula"
Set Padding 20
Set BorderRadius 8
Set Margin 10
Set MarginFill "#282a36"

# Human typing speed
Set TypingSpeed 60ms

# Launch copilot
Type "copilot"
Enter

# Wait for copilot to start
Sleep 5s

# Execute the prompt
Type "Generate commit message for: $(git diff --staged)"
Sleep 2s
Enter

# Wait for response
Sleep 25s

# Exit cleanly
Ctrl+C
Sleep 2s
