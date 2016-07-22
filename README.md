# GithubPath
Plug in for sublime to open current file in Github's website. **NO SETUP, GITHUB TOKEN, OR PASSWORD REQUIRED**.

![alt text](https://github.com/santi-h/GithubPath/blob/master/GithubPath.gif?raw=true)

# Usage
- Right click on the current file and select "Open in Github"
- The link is already sent to your clipboard

# Why?
A lot of times I find myself searching for a file in a repo through the web browser with the intention to point someone else to a particular line or block of code.

Searching for a file and selecting lines of code is a lot easier to do in sublime than it is in the web browser.

With this plugin I can just find the file in sublime, use a keyboard shortut to get the link in github, and just paste the link in the email/message I'm trying to send.

# Behind the scenes
It obtains the required values and opens the following link
```
https://github.com/XXXXXXX/XXXXXX/blob/XXXXXXXXXXXX/XXXX/XXX/XXX#XXXX-XXXX
                  |^^^^^^^|^^^^^^|    |^^^^^^^^^^^^|^^^^^^^^^^^^|^^^^ ^^^^
                  | owner | repo |    | master sha |  file path | line or range
```

The values are obtained the following way:
- **owner** and **repo**: it runs `git remote -v` and searches for a github remote
- **master sha**: it runs `git rev-parse master` to get the sha of your local `master`
- **file path**: relative to your `.git` folder
- **line or range**: the current position of the cursor or the selection

# Pro tip
Add a keyboard shortcut like this to your user key bindings file:
```python
# "Default (OSX).sublime-keymap"
[
  # ...
  { "keys": ["super+shift+8"], "command": "github_path" },
  # ...
]
```
