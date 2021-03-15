# !/usr/bin/python
import os
import time


def pull():
    os.popen('cd ../Dockerfiles/; git pull')
    return


def job():

    file = open("commit.txt", "r+")
    previous_checked = file.read()
    print("Previously: " + previous_checked)

    output = os.popen('cd ../Dockerfiles/; git log -1 --pretty=%B').read()
    output_oneline = os.linesep.join([s for s in output.splitlines() if s])

    print("New check: " + output_oneline)

    file.seek(0)
    file.truncate()
    file.write(output_oneline)
    file.close()


    time.sleep(0)

    if previous_checked != output_oneline:
        print("New commit!")
        apo = '"'
        command = "./discord.sh " + "--username Docker " + "--avatar " + apo\
                  + "https://avatars3.githubusercontent.com/u/46843401?s=90&v=4" + apo\
                  + " --text " + apo + "New commit! " + output_oneline + apo\
                  + " --title " + apo + "Check more here" + apo\
                  + " --url " + apo + "https://github.com/OpenVisualCloud/Dockerfiles/commits/v2.0" + apo
        os.popen(command)
        print(command)

        file.seek(0)
        file.truncate()
        file.write(output_oneline)
        file.close()

        time.sleep(2)
        quit("Znalazłem update i spadam.")

    else:
        print("No new updates.")
        file.close()
        time.sleep(2)
        quit("Nic sie nie dzieje, wiec spadam.")
    quit()
    return


# while True:
#     pull()
#     job()
#     time.sleep(1)  # wait one second

