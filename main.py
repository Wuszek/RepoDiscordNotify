# !/usr/bin/python
import os
import time
import sys
from datetime import datetime

repo = "../Dockerfiles/"  # set repository path relative to script location
counter = 0


def pull():
    os.popen('cd ' + repo + '; git pull')
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
            print("Sleeping for 1min now, because no new commits were pushed.")
            print("-----------------------------------------------")
            time.sleep(60)  # set break after no new commits found to 60s
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


# while True: # use this loop, to run script forever (or once - find new commits and quit when no new updates found)
while counter < 1:  # set how many times script should run its loop
    now = datetime.now()
    loop_time = now.strftime("%d/%m/%Y, %H:%M:%S")

    sys.stdout = open('log.txt', 'a+')
    print("Next loop started: " + loop_time)
    pull()
    job()
    sys.stdout.close()
    counter += 1
