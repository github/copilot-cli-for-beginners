# 07-putting-it-together: Idea to merged PR: plan, implement, test a new feature
# Auto-generated from demos.json - Real copilot execution

Output full-review-demo.gif

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
Type "I need to add a 'list unread' command to the book app that shows only books where read is False. What files need to change?"
Sleep 2s
Enter

# Wait for response
Sleep 25s

# Prompt 2 - Select python-reviewer agent
Type "/agent"
Sleep 1s
Enter

# Wait for agent picker
Sleep 3s
Down 3
Sleep 1s
Enter

# Wait for agent to load
Sleep 3s

# Prompt 3
Type "@samples/book-app-project/books.py Design a get_unread_books method. What is the best approach?"
Sleep 2s
Enter

# Wait for response
Sleep 30s

# Prompt 4 - Select pytest-helper agent
Type "/agent"
Sleep 1s
Enter

# Wait for agent picker
Sleep 3s
Down 2
Sleep 1s
Enter

# Wait for agent to load
Sleep 3s

# Prompt 5
Type "@samples/book-app-project/tests/test_books.py Design test cases for filtering unread books."
Sleep 2s
Enter

# Wait for response
Sleep 30s

# Prompt 6
Type "Add a get_unread_books method to BookCollection in books.py. Add a 'list unread' command option in book_app.py. Update the help text in the show_help function."
Sleep 2s
Enter

# Wait for response
Sleep 30s

# Prompt 7
Type "Generate comprehensive tests for the new feature"
Sleep 2s
Enter

# Wait for response
Sleep 35s

# Prompt 8
Type "/review"
Sleep 2s
Enter

# Wait for response
Sleep 25s

# Prompt 9
Type "Create a pull request titled 'Feature: Add list unread books command'"
Sleep 2s
Enter

# Wait for response
Sleep 25s

# Exit cleanly
Ctrl+C
Sleep 2s
