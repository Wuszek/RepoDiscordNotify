# !/usr/bin/python
import os
import time
import sys
from datetime import datetime

repo = "../Test2/"  # repository path relative to script location
counter = 0


def pull():
    os.popen('cd ' + repo + '; git pull')  # change your local repo directory
    time.sleep(1)
    return


def job():
    file = open("commit.txt", "r+")
    previous_checked1 = file.read()
    previous_checked = os.linesep.join([s for s in previous_checked1.splitlines() if s])

    time.sleep(1)
    count = 0

    while True:
        output = os.popen('cd ' + repo + '; git log -1 --skip ' + str(count) + ' --pretty=format:%s').read()
        commit_hash = os.popen('cd ' + repo + '; git log -1 --skip ' + str(count) + ' --pretty=format:%H').read()
        # commit_date = os.popen('cd ' + repo + '; git log -1 --skip ' + str(count) + ' --pretty="format:%ar"').read()

        # print(commit_hash)
        print("Last commit: " + previous_checked)
        print("Now checked: " + output)

        if previous_checked == output:
            print("No new updates.")
            latest_commit = os.popen('cd ' + repo + '; git log -1 --pretty=format:%s').read()
            file.seek(0)
            file.truncate()
            file.write(latest_commit)
            time.sleep(1)
            print("-----------------------------------------------")
            file.close()
            # quit("All done")
            print("Sleeping for 1min now \n")
            print("-----------------------------------------------")
            time.sleep(60)  # set break after no new commits to 60s
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
            # print(command)
            count = count + 1
            # print(count)
            time.sleep(2)
            print("-----------------------------------------------")


# if __name__ == '__main__':  # change main with while, to run script in loop
# while True:
while counter < 10:  # set counter
    now = datetime.now()
    loop_time = now.strftime("%d/%m/%Y, %H:%M:%S")

    sys.stdout = open('log.txt', 'a+')
    print("Next loop started: " + loop_time)
    pull()
    job()
    sys.stdout.close()
    counter += 1
