
import logging
import subprocess

logger = logging.getLogger("updater")

def currentVersion():
    gitTag = runCommand("git", "describe", "--tags", "--exact-match")
    tag = gitTag.stdout.strip()
    if gitTag.returncode != 0 or not tag:
        return None
    gitBranch = runCommand("git", "branch", "--show-current")
    if gitBranch.stdout.strip():
        return None
    return tag

def latestVersion():
    _ = runCommand("git", "fetch", "--tags")
    gitVersion = runCommand("git tag --sort=-creatordate | head -n 1", shell=True)
    return gitVersion.stdout.strip()

def updateToVersion(version: str):
    _ = runCommand("git", "checkout", f"tags/{version}")


def runCommand(*args, shell=False):
    logger.debug(f"\"{' '.join(args)}\"")
    return subprocess.run(args, shell=shell, capture_output=True, text=True)
