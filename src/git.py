"""Simple GIT API.

The purpose of this library is to keep using git in Python instead of using
os.system or subprocess. There are not too much features implemented. However it
is already enough for what we need it.

"""

import os

class Git:
    """Simple GIT API.

    :param path: path of the git repository
    :param type: str
    """

    def __init__(self, path):
        """Constructor"""
        self._path = path
        if path[-1] == '/':
            self._path = path[:-1]
        self._add = False

    def is_git_repo(self):
        """Check if the current directory is a git repository

        :rtype: bool
        :return: True if the current directory is a git repository, False\
        otherwise
        """
        return os.path.isdir(".git")

    def init(self):
        """Initialize a git repository in the current directory

        If the directory is alread a git repository, it does nothing
        """
        if self.is_git_repo():
            print("Already a git directory")
        else:
            os.system("git init")
            os.system('git config --global user.email ""')
            os.system('git config --global user.name "Tux"')

    def get_all_branches(self):
        """Gives the list of all branches of the repository

        :rtype: list
        :return: list of all branches
        """
        heads = "{}/.git/refs/heads".format(self._path)
        return os.listdir(heads)

    def checkout(self, name):
        """Move to another branch

        :param name: name of the destination branch
        :param type: str
        :raises: NameError if the destination branch is unknown
        """
        if name in self.get_all_branches():
            os.system("git checkout {}".format(name))
        else:
            raise NameError("Unkown git branch: {}".format(name))

    def create_branch(self, name):
        """Create a new branch. If the branch already exists, it just moves to the
        existing branch

        :param name: name of the new branch
        :param type: str
        """
        if name in self.get_all_branches():
            self.git_checkout(name)
        else:
            os.system("git checkout -b {}".format(name))

    def add(self, *files, force=False):
        """Add files

        :param files: files to add
        :type files: string or list of strings
        :param force: force the addition
        :param type: bool
        """
        files_str = " ".join(files)
        force_flag = ""
        if force:
            force_flag = "-f"
        os.system("git add {} {}".format(force_flag, files_str))
        self._add = True

    def commit(self, msg):
        """Commit

        :param msg: message
        :param type: str
        """
        if self._add:
            os.system("git commit -m \"{}\"".format(msg))
            self._add = False
        else:
            print("Nothing to commit")

    def branch_diff(self, branch1, branch2, stat=False, output_fn=None):
        """Diff of two branches

        :param branch1: first branch
        :param type: str
        :param branch2: second branch
        :param type: str
        :param stat: True to add git's --stat parameter; False otherwise
        :param type: bool
        :param output_fn: filename to write the result in. If None, result will\
        be printed in stdout
        :param type: str
        """
        output_redir_cmd = ""
        stat_flag = ""
        if output_fn is not None:
            output_redir_cmd = ">> {}".format(output_fn)
        if stat:
            stat_flag = "--stat"
        if branch1 not in self.get_all_branches():
            raise NameError("Unkown git branch: {}".format(name))
        if branch2 not in self.get_all_branches():
            raise NameError("Unkown git branch: {}".format(name))
        os.system("git diff {} {}..{} {}"\
                  .format(stat_flag, branch1, branch2, output_redir_cmd))

    def __check_git_config(self):
        """Check the configuration of the current git repository.
        If username and email are not defined, it will ask it.
        """
        git_config_ret = os.system("git config user.name")
        if git_config_ret != 0:
            print("*** Please tell me who you are.")
            print("Set your account's default identity.")
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            config_cmd = 'git config --global user.email "{}"\
                          git config --global user.name "{}"'.format(email, name)
            print("Done.")
