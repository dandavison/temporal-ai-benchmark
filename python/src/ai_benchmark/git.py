import subprocess
import sys


def assert_workspace_clean():
    if output := subprocess.check_output(["git", "status", "--porcelain"]).strip():
        print(output.decode(), file=sys.stderr)
        raise Exception("Workspace is not clean")


def stash_changes():
    subprocess.check_output(["git", "stash", "save"])


def checkout(ref: str, path: str):
    subprocess.check_output(["git", "checkout", ref, path])
