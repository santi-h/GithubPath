import sublime
import sublime_plugin
import os
import subprocess
import re
import webbrowser

class GithubPathCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    current_file = self.view.file_name()
    if current_file is None:
      return

    check_path = os.path.dirname(current_file)
    git_dir_path = None
    repo_file_path = [os.path.basename(current_file)]
    while (len(check_path) > 1) and (git_dir_path is None):
      dirs = [possible_dir for possible_dir in os.listdir(check_path) if os.path.isdir(os.path.join(check_path, possible_dir))]
      if '.git' in dirs:
        git_dir_path = check_path
      else:
        repo_file_path.insert(0, os.path.basename(check_path))

      check_path = os.path.dirname(check_path)

    if git_dir_path is None:
      sublime.message_dialog('Not a git repo')
      return

    repo_file_path = os.path.join(*repo_file_path)

    remotes = output_from_command('git', '--git-dir', git_dir_path + '/.git', 'remote', '-v')
    print(remotes)
    match = re.search(r'github\.com(?::|\/)([\w\-]+)\/([\w\-]+)\.git \(fetch\)', remotes)
    owner = None
    repo = None
    if match is not None:
      owner = str(match.group(1))
      repo = str(match.group(2))

    if owner is None or repo is None:
      sublime.message_dialog('No github remote found')
      return

    sha = output_from_command('git', '--git-dir', git_dir_path + '/.git', 'rev-parse', 'master')
    selection = self.view.sel()[0]
    line_start = 'L' + str(self.view.rowcol(selection.begin())[0] + 1)
    line_end = 'L' + str(self.view.rowcol(selection.end())[0] + 1)
    line_range = [line_start]
    if line_start != line_end:
      line_range.append(line_end)

    url = "https://github.com/{owner}/{repo}/blob/{sha}/{repo_file_path}#{line_number}".format(
      owner = owner,
      repo = repo,
      sha = sha,
      repo_file_path = repo_file_path,
      line_number = '-'.join(line_range)
    )
    sublime.set_clipboard(url)
    webbrowser.open(url)

def output_from_command(*cmd):
  return subprocess.check_output(cmd, stderr = subprocess.STDOUT).decode("utf-8").strip()
