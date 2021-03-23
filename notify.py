# !/usr/bin/python
import argparse
import os
import re
import sys
import time
from datetime import datetime

import requests

counter = 0  # Counter if you want to run script with finite number of loops. Leave it 0!


def get_files():
    if os.path.isfile('discord.sh'):
        print("File 'discord.sh' already exists. Proceeding...")
    else:
        filename = "discord.sh"
        url = 'https://raw.githubusercontent.com/ChaoticWeg/discord.sh/master/discord.sh'
        f = requests.get(url)
        open(filename, 'wb').write(f.content)
        os.popen('chmod +x discord.sh').read()
        print("File 'discord.sh' downloaded. Proceeding...")
    if os.path.isfile('.webhook'):
        print(".webhook file fund! Proceeding...")
    else:
        exit("No .webhook file. Create one with webhook url inside.")
    return


def test():
    command = f'./discord.sh \
                            --username "NotificationBot" \
                            --avatar "https://i.imgur.com/12jyR5Q.png" \
                            --text "Commit appear: **test value** \\n path: <test values>"'
    os.popen(command)
    return


def clone(repo, branch, dir_name):
    if not os.popen(f'git ls-remote --heads {repo} {branch}').read():
        exit("Given branch does not exist in remote.")
    print("Valid repository url. Proceeding...")
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

    latest_commit_hash = os.popen('cd ../' + dir_name + '; git log -1 --pretty=format:%H').read()
    if os.path.isfile(".commit"):
        file = open(".commit", "r+")
        saved_name = [line.split() for line in file]
        if saved_name[0][0] == dir_name:
            print(f".commit file exists. Good dir name: {saved_name[0][0]}")
            file.close()
        else:
            print(f'WRONG! Dir name: {saved_name[0][0], saved_name[0][1]}')
            file.seek(0)
            file.truncate()
            print(dir_name, latest_commit_hash, file=file)
            print(f'Filled with {dir_name, latest_commit_hash}')
            file.close()
    else:
        file = open(".commit", "w+")
        print(dir_name, latest_commit_hash, file=file)
        file.close()
        print(f".commit file created and filled: {dir_name, latest_commit_hash}")
    print("-----------------------------------------------")
    return


def pull(dir_name):
    os.popen('cd ../' + dir_name + '; git pull').read()
    return


def job(dir_name, sleep_time):
    file = open(".commit", "r+")
    previous_checked = [line.split() for line in file]
    print(f'Hash from file: {previous_checked[0][1]}')
    count = 0

    while True:
        commit_name = os.popen('cd ../' + dir_name + '; git log -1 --skip ' + str(count) + ' --pretty=format:%s').read()
        commit_hash = os.popen('cd ../' + dir_name + '; git log -1 --skip ' + str(count) + ' --pretty=format:%H').read()
        commit_link = f"{repo[:-4]}/commit/"

        if previous_checked[0][1] == commit_hash:
            print(f"No new updates. Sleeping for {sleep_time}s now.")
            actual_commit_hash = os.popen('cd ../' + dir_name + '; git log -1 --pretty=format:%H').read()
            file.seek(0)
            file.truncate()
            print(dir_name, actual_commit_hash, file=file)
            print("-----------------------------------------------")
            time.sleep(sleep_time)  # Set sleep time if no new commits found
            break

        else:
            print("New commit! -> " + commit_name)
            # EXAMPLE DISCORD BOT MESSAGE
            command = f'./discord.sh \
                        --username "NotificationBot" \
                        --avatar "https://i.imgur.com/12jyR5Q.png" \
                        --text "Commit appear: **{commit_name}** \\n path: <{commit_link}{commit_hash}>"'
            # DOCKERFILES DISCORD BOT MESSAGE
            # command = f'./discord.sh \
            #             --username "OpenVisualCloud" \
            #             --avatar "https://avatars3.githubusercontent.com/u/46843401?s=90&v=4" \
            #             --text "🐳 NEW COMMIT: **{commit_name}** \\n path: <{commit_link}{commit_hash}>"'

            os.popen(command)
            count = count + 1  # to move to next new commit
            print("-----------------------------------------------")


def argument_parse(argv):
    print("\n→ " + datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
    parser = argparse.ArgumentParser \
        (usage="python3 notify.py [--help] --repo <link> [--branch <name>] [--time <sec>] [--loop <num>]", \
         description="Repo_Discord_Notify tool - get pinged, whenever new commit appears!", \
         epilog="© 2021, wiktor.kobiela, Repo_Discord_Notify - feel free to contribute", prog="Repo_Discord_Notify", \
         add_help=False, formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=120, width=250))

    def git_repo_regex(arg_value, pat=re.compile(
        r"^(([A-Za-z0-9]+@|http(|s)\:\/\/)|(http(|s)\:\/\/[A-Za-z0-9]+@))([A-Za-z0-9.]+(:\d+)?)(?::|\/)([\d\/\w.-]+?)(\.git){1}$")):
        if not pat.match(arg_value):
            raise argparse.ArgumentTypeError("Invalid repository url.")
        return arg_value

    def positive_int(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive int value." % value)
        return ivalue

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    helpful = parser.add_argument_group('helpful arguments')

    required.add_argument('-r', '--repo', action='store', dest="repo", help="repository link to cloned repo,\
                        with .git at the end", type=git_repo_regex, required=True, metavar="<link>")

    optional.add_argument('-b', '--branch', action='store', dest="branch", help="branch name, that will be cloned - \
                        default is master", default="master", metavar="<name>")
    optional.add_argument('-t', '--time', action='store', dest="time", help="idle time between next pull&check - \
                          default is 10s", type=positive_int, default=10, metavar="<sec>")
    optional.add_argument('-l', '--loop', action='store', dest="loop", help="number of loops that script should make - \
                          default is infinite", default=0, type=positive_int, metavar="<num>")

    helpful.add_argument('-v', '--version', action='version', version='%(prog)s alpha 21.3')
    helpful.add_argument('-h', '--help', action='help', help='show this help message and exit')
    helpful.add_argument('-c', '--check', action='store_true', dest="check", help="add this to your command, to \
                         send test message before script start", default=False)

    args = parser.parse_args()
    return args.repo, args.branch, args.time, args.loop, args.check


def looping(loop, counter):
    if loop == 0:
        while True:
            pull(dir_name)
            job(dir_name, sleep_time)
    else:
        while counter < loop:
            pull(dir_name)
            job(dir_name, sleep_time)
            counter += 1
    return


if __name__ == '__main__':
    # sys.stdout = open('log.txt', 'a+')  # Comment this, to enable live logging in terminal
    repo, branch, sleep_time, loop, check = argument_parse(sys.argv[1:])
    print('-----------------------Settings--------------------------')
    print(f'Repo: {repo}\nBranch: {branch}\nIdle time: {sleep_time}s\nLoops: {"Inf" if loop == 0 else loop}')
    print('---------------------------------------------------------')
    dir_name = re.search(r"(([^/]+).{4})$", repo).group(2)
    get_files()
    if check: test()
    clone(repo, branch, dir_name)
    looping(loop, counter)
    # sys.stdout.close()  # Comment this, to enable live logging in terminal
    exit("Finished my job. Bye")
