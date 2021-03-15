# !/usr/bin/python
import os
import time


def pull():
    os.popen('cd ../Dockerfiles/; git pull')  # change your local repo directory
    time.sleep(2)
    return


def job():
    file = open("commit.txt", "r+")
    previous_checked1 = file.read()
    previous_checked = os.linesep.join([s for s in previous_checked1.splitlines() if s])

    time.sleep(2)
    same = 0
    count = 0

    while same != 1:
        output = os.popen('cd ../Dockerfiles/; git log -1 --skip ' + str(count) + ' --pretty=format:%s').read()
        hash = os.popen('cd ../Dockerfiles/; git log -1 --skip ' + str(count) + ' --pretty=format:%H').read()

        print(hash)
        print("From file: " + previous_checked)
        print("New check: " + output)

        if previous_checked == output:
            print("No new updates.")
            latest_commit = os.popen('cd ../Dockerfiles/; git log -1 --pretty=format:%s').read()
            file.seek(0)
            file.truncate()
            file.write(latest_commit)
            time.sleep(2)
            print("-----------------------------------------------")
            file.close()
            same = 1
            quit("All done")

        else:
            print("New commit!")
            apo = '"'
            command = "./discord.sh " + "--username OpenVisualCloud " + "--avatar " + apo \
                      + "https://avatars3.githubusercontent.com/u/46843401?s=90&v=4" + apo \
                      + " --text " + apo + "🐳 NEW COMMIT: " + "**" + output + "**" \
                      + "\\n" + "path: <https://github.com/OpenVisualCloud/Dockerfiles/commit/" + hash + ">" + apo
            os.popen(command)
            print(command)
            count = count + 1
            print(count)
            time.sleep(2)
            print("-----------------------------------------------")

    return


if __name__ == '__main__':
    pull()
    job()
