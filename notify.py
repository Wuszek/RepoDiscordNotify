# !/usr/bin/python
import argparse
import os
import re
import sys
import time
from datetime import datetime

import requests

counter = 0  # Counter if you want to run script with finite number of loops. Leave it 0!
latest_commit_hash = ""

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
        print(".webhook file fund!")
    else:
        exit("No .webhook file. Create one with webhook url inside.")
    return


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

    # Take second latest commit hash and write it down. Just to make sure, that script would catch next
    # newer commit and send message using Discord bot
    global latest_commit_hash
    latest_commit_hash = os.popen('cd ../' + dir_name + '; git log -1 --skip 1 --pretty=format:%H').read()
    return


def pull(dir_name):
    os.popen('cd ../' + dir_name + '; git pull').read()
    return


def job(dir_name, sleep_time):
    global latest_commit_hash
    count = 0

    while True:
        commit_name = os.popen('cd ../' + dir_name + '; git log -1 --skip ' + str(count) + ' --pretty=format:%s').read()
        commit_hash = os.popen('cd ../' + dir_name + '; git log -1 --skip ' + str(count) + ' --pretty=format:%H').read()
        commit_link = f"{repo[:-4]}/commit/"
        # sleep_time = 10  # Sleep timer in seconds. Change to customize repo refresh rate

        if latest_commit_hash == commit_hash:
            print(f"No new updates. Sleeping for {sleep_time}s now.")
            actual_commit_hash = os.popen('cd ../' + dir_name + '; git log -1 --pretty=format:%H').read()
            latest_commit_hash = actual_commit_hash
            print("-----------------------------------------------")
            time.sleep(sleep_time)  # Set sleep time after no new commits found to ?seconds
            break

        else:
            print("New commit! -> " + commit_name)
            # EXAMPLE DISCORD BOT MESSAGE
            # command = f'./discord.sh \
            #             --username "NotificationBot" \
            #             --avatar "https://i.imgur.com/12jyR5Q.png" \
            #             --text "Hello, world!"'
            # DOCKERFILES DISCORD BOT MESSAGE
            command = f'./discord.sh \
                        --username "OpenVisualCloud" \
                        --avatar "https://avatars3.githubusercontent.com/u/46843401?s=90&v=4" \
                        --text "🐳 NEW COMMIT: **{commit_name}** \\n path: <{commit_link}{commit_hash}>"'

            os.popen(command)
            count = count + 1  # to move to next new commit
            # time.sleep(1)
            print("-----------------------------------------------")


def argument_parse(argv):
    parser = argparse.ArgumentParser\
    (usage="python3 notify.py [--help] --repo <link_to_repository> [--branch <branch_to_be_observed>]", \
    description="Repo_Discord_Notify tool - get pinged, whenever new commit appears!", \
    epilog="© 2021, wiktor.kobiela, Repo_Discord_Notify - feel free to contribute", prog="Repo_Discord_Notify", \
    add_help=True, formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=100, width=250))

    def git_repo_regex(arg_value, pat=re.compile(r"^(([A-Za-z0-9]+@|http(|s)\:\/\/)|(http(|s)\:\/\/[A-Za-z0-9]+@))([A-Za-z0-9.]+(:\d+)?)(?::|\/)([\d\/\w.-]+?)(\.git){1}$")):
        if not pat.match(arg_value):
            raise argparse.ArgumentTypeError("Invalid repository link.")
        print("Valid git repository url. Proceeding...")
        return arg_value

    def positive_int(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive int value." % value)
        return ivalue

    parser.add_argument('-r', '--repo', action='store', dest="repo", help="repository link to cloned repo,\
                        with .git at the end", type=git_repo_regex, required=True)
    parser.add_argument('-b', '--branch', action='store', dest="branch", help="branch name, that will be cloned - \
                        default is master", default="master")
    parser.add_argument('-t', '--time', action='store', dest="time", help="idle time between next pull&check - default \
                        is 10s", type=positive_int, default=10)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s alpha')

    args = parser.parse_args()
    return args.repo, args.branch, args.time


if __name__ == '__main__':
    loop_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    # sys.stdout = open('log.txt', 'a+')  # Comment this, to enable live logging in terminal
    repo, branch, sleep_time = argument_parse(sys.argv[1:])
    print(f'Setup idle time: {sleep_time}')
    print("Program started: " + loop_time)
    dir_name = re.search(r"(([^/]+).{4})$", repo).group(2)
    get_files()
    clone(repo, branch, dir_name)
    while True:  # Or while counter < given_number, to get finite number of loops
        pull(dir_name)
        job(dir_name, sleep_time)
      # counter += 1
    # sys.stdout.close()  # Comment this, to enable live logging in terminal
    # exit()  # Uncomment, if using finite number of loops
