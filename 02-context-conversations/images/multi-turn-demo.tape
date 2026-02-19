# 02-context-conversations: Multi-turn conversation building on previous context
# Auto-generated from demos.json - Real copilot execution

Output multi-turn-demo.gif

Set FontSize 18
Set Width 1000
Set Height 600
Set Theme "Dracula"
Set Padding 20
Set BorderRadius 8
Set Margin 10
Set MarginFill "#282a36"
Set Framerate 10

# Human typing speed
Set TypingSpeed 60ms

# Launch copilot
Type "copilot"
Enter

# Wait for copilot to start
Sleep 5s

# Prompt 1
Type "@samples/book-app-project/ Give me an overview of this project"
Sleep 2s
Enter

# Wait for response
Sleep 25s

# Prompt 2
Type "What are the main code quality issues?"
Sleep 2s
Enter

# Wait for response
Sleep 25s

# Prompt 3
Type "Which issue should I fix first and show me how?"
Sleep 2s
Enter

# Wait for response
Sleep 45s

# Exit cleanly
Ctrl+C
Sleep 2s
