# !/usr/bin/python
import os
import time


def pull():
    os.popen('cd ../Test2/; git config pull.rebase false; git pull') #change your local repo directory
    time.sleep(2)
    return


def job():
    file = open("commit.txt", "r+")
    previous_checked = file.read()
    print("Previously: " + previous_checked)

    output = os.popen('cd ../Test2/; git log -1 --pretty=%B').read() #change your local repo directory
    output_oneline = os.linesep.join([s for s in output.splitlines() if s])

    print("New check: " + output_oneline)

    time.sleep(2)

    if previous_checked != output_oneline:
        print("New commit!")
        apo = '"'
        command = "./discord.sh " + "--username OpenVisualCloud " + "--avatar " + apo \
                  + "https://avatars3.githubusercontent.com/u/46843401?s=90&v=4" + apo \
                  + " --text " + apo + "🐳 NEW COMMIT: " + "**" + output_oneline + "**" \
                  + " -path: <https://github.com/OpenVisualCloud/Dockerfiles/commits/v2.0>" + apo
        # + " --title " + apo + "Check more here" + apo\
        # + " --url " + apo + "https://github.com/OpenVisualCloud/Dockerfiles/commits/v2.0" + apo
        os.popen(command)
        print(command)

        file.seek(0)
        file.truncate()
        file.write(output_oneline)
        file.close()

        time.sleep(2)
        # quit("Znalazłem update i spadam.")
        print("-----------------------------------------------")

    else:
        print("No new updates.")
        file.close()
        time.sleep(2)
        # quit("Nic sie nie dzieje, wiec spadam.")
        print("-----------------------------------------------")

    return


while True:
    pull()
    job()
    time.sleep(15)  # wait 15 seconds
