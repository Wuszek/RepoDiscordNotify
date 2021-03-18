# !/usr/bin/python
import os
import time
import sys
import getopt
import re
import subprocess
from datetime import datetime

# repo = "../Dockerfiles/"  # set repository path relative to script location
counter = 0


def clone(repo, branch):
    dir_name = re.search(r"(([^\/]+).{4})$", repo).group(2)

    if os.path.isdir('../' + dir_name):
        actual_branch = os.popen('cd ../' + dir_name + '; git branch').read()[2:]
        filtered_branch = os.linesep.join([s for s in actual_branch.splitlines() if s])
        # print(filtered_branch)

        if filtered_branch == branch:
            print("Repository already cloned with selected branch.")
        else:
            print("Repository cloned, but with wrong branch. Removing old, cloning proper one.")
            os.popen('cd ../; rm -rf ' + dir_name + '; git clone --single-branch --branch ' + branch + " " + repo).read()
    else:
        os.popen('cd ../; git clone --single-branch --branch ' + branch + ' ' + repo).read()
        # subprocess.Popen("cd ../ \n git clone --single-branch --branch {branch} {repo}")

    return dir_name


def pull(repo):
    dir_name = re.search(r"(([^\/]+).{4})$", repo).group(2)
    os.popen('cd ../' + dir_name + '; git pull').read()
    time.sleep(1)
    return


def job(repo):
    dir_name = re.search(r"(([^\/]+).{4})$", repo).group(2)
    file = open("commit.txt", "r+")
    previous_checked1 = file.read()
    previous_checked = os.linesep.join([s for s in previous_checked1.splitlines() if s])

    time.sleep(1)
    count = 0

    while True:
        output = os.popen('cd ../' + dir_name + '; git log -1 --skip ' + str(count) + ' --pretty=format:%s').read()
        commit_hash = os.popen('cd ../' + dir_name + '; git log -1 --skip ' + str(count) + ' --pretty=format:%H').read()

        # print("Last commit: " + previous_checked)
        # print("Now checked: " + output)

        if previous_checked == output:
            print("No new updates.")
            latest_commit = os.popen('cd ../' + dir_name + '; git log -1 --pretty=format:%s').read()
            file.seek(0)
            file.truncate()
            file.write(latest_commit)
            time.sleep(1)
            print("-----------------------------------------------")
            file.close()
            print("Sleeping for 1min now, because no new commits were pushed.")
            print("-----------------------------------------------")
            time.sleep(10)  # set break after no new commits found to 60s
            # quit("All done")  # use this with while True loop to run script once
            break

        else:
            print("New commit!")
            apo = '"'
            command = "./discord.sh " + "--username OpenVisualCloud " + "--avatar " + apo \
                      + "https://avatars3.githubusercontent.com/u/46843401?s=90&v=4" + apo \
                      + " --text " + apo + "🐳 NEW COMMIT: " + "**" + output + "**" \
                      + "\\n" + "path: <https://github.com/OpenVisualCloud/Dockerfiles/commit/" \
                      + commit_hash + ">" + apo
            os.popen(command)
            count = count + 1  # to move to next new commit
            time.sleep(1)
            print("-----------------------------------------------")


def usage():
    print("python3 main.py --repo <link_to_repo> --branch <branch_to_be_observed>")
    print("--repo: Link to clone repo, with .git at the end")
    print("--branch: Branch name, that will be cloned")
    print("e.g.")
    print("python3 main.py --repo https://github.com/OpenVisualCloud/Dockerfiles.git --branch v21.3")
    sys.exit()


def getarguments(argv):
    repo = None
    branch = None
    short_opts = 'hr:b:'
    long_opts = ["help", "repo=", "branch="]
    try:
        opts, _ = getopt.getopt(argv, short_opts, long_opts)
        if not opts:
            print("Error: No options supplied")
            usage()
    except getopt.GetoptError:
        print(f"Error in options {opts}")
        usage()

    for opt, arg in opts:
        if opt in ("-r", "--repo"):
            repo = arg
        elif opt in ("-b", "--branch"):
            branch = arg
        elif opt in ("-h", "--help"):
            usage()
        else:
            print(f"Unsupported option {opt}")
            usage()
    return repo, branch


# while True: # use this loop, to run script forever (or once - find new commits and quit when no new updates found)
# while counter < 1:  # set how many times script should run its loop
if __name__ == '__main__':
    repo, branch = getarguments(sys.argv[1:])
    now = datetime.now()
    loop_time = now.strftime("%d/%m/%Y, %H:%M:%S")
    # sys.stdout = open('log.txt', 'a+')
    # print("Next loop started: " + loop_time)
    clone(repo, branch)

    while True:
        pull(repo)
        job(repo)

    # pull()
    # job()
    # sys.stdout.close()
    # counter += 1
    exit()
