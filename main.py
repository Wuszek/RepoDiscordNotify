# !/usr/bin/python
import os
import time
import sys
import getopt
import re
from datetime import datetime

counter = 0


def clone(repo, branch, dir_name):
    if os.path.isdir('../' + dir_name):
        actual_branch = os.popen('cd ../' + dir_name + '; git branch').read()[2:]
        filtered_branch = os.linesep.join([s for s in actual_branch.splitlines() if s])

        if filtered_branch == branch:
            print("Repository already cloned with selected branch.")
        else:
            print("Repository cloned, but with wrong branch. Removing old, cloning proper one.")
            os.popen('cd ../; rm -rf ' + dir_name + '; git clone \
                     --single-branch --branch ' + branch + " " + repo).read()
    else:
        os.popen('cd ../; git clone --single-branch --branch ' + branch + ' ' + repo).read()

    # take second latest commit and create commit.txt file. Just to make sure, that script would catch next
    # newer commit and send message using Discord bot
    latest_commit_to_file = os.popen('cd ../' + dir_name + '; git log -1 --skip 1 --pretty=format:%s').read()
    file = open("commit.txt", "w")
    file.write(latest_commit_to_file)
    file.close()

    return


def pull(dir_name):
    os.popen('cd ../' + dir_name + '; git pull').read()
    time.sleep(1)
    return


def job(dir_name):
    file = open("commit.txt", "r+")
    previous_checked1 = file.read()
    previous_checked = os.linesep.join([s for s in previous_checked1.splitlines() if s])

    time.sleep(1)
    count = 0

    while True:
        output = os.popen('cd ../' + dir_name + '; git log -1 --skip ' + str(count) + ' --pretty=format:%s').read()
        commit_hash = os.popen('cd ../' + dir_name + '; git log -1 --skip ' + str(count) + ' --pretty=format:%H').read()
        sleep_time = 10
        # print("Last commit: " + previous_checked)
        # print("Now checked: " + output)

        if previous_checked == output:
            print(f"No new updates. Sleeping for {sleep_time}s now.")
            latest_commit = os.popen('cd ../' + dir_name + '; git log -1 --pretty=format:%s').read()
            file.seek(0)
            file.truncate()
            file.write(latest_commit)
            file.close()
            print("-----------------------------------------------")
            time.sleep(sleep_time)  # set break after no new commits found to 60s
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
    print("====================================== DISPLAYING HELP ======================================")
    print("python3 main.py --repo <link_to_repository> --branch <branch_to_be_observed (default master)>")
    print("--repo: Link to clone repo, with .git at the end")
    print("--branch: Branch name, that will be cloned")
    print("e.g.")
    print("python3 main.py --repo https://github.com/OpenVisualCloud/Dockerfiles.git --branch v21.3")
    print("=============================================================================================\n")
    sys.exit()


def getarguments(argv):
    global opts
    repo = None
    branch = "master"
    short_opts = 'hr:b:'
    long_opts = ["help", "repo=", "branch="]
    try:
        opts, _ = getopt.getopt(argv, short_opts, long_opts)
        if not opts:
            print("Error: No options supplied")
            usage()
    except getopt.GetoptError:
        print(f"Error in options or options not specified.\n")
        usage()

    for opt, arg in opts:
        if opt in ("-r", "--repo"):
            repo = arg
        elif opt in ("-b", "--branch"):
            branch = arg
            if re.match(r"/^(([A-Za-z0-9]+@|http(|s)\:\/\/)|(http(|s)\:\/\/[A-Za-z0-9]+@))([A-Za-z0-9.]\
                        +(:\d+)?)(?::|\/)([\d\/\w.-]+?)(\.git){1}$/i", branch):
                print("Valid git repository url. Continuing...")
            else:
                print("Invalid git repository url.\n")
                usage()
        elif opt in ("-h", "--help"):
            usage()
        else:
            print(f"Unsupported option {opt}")
            usage()
    return repo, branch


if __name__ == '__main__':
    repo, branch = getarguments(sys.argv[1:])
    dir_name = re.search(r"(([^/]+).{4})$", repo).group(2)

    now = datetime.now()
    loop_time = now.strftime("%d/%m/%Y, %H:%M:%S")
    # sys.stdout = open('log.txt', 'a+')
    print("Program started: " + loop_time)
    clone(repo, branch, dir_name)
    while True:  # or while counter < given number of loops
        pull(dir_name)
        job(dir_name)
        # counter += 1
    # sys.stdout.close()
    # exit()
