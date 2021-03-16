## Commits check bot

Discord bot integrated with simple python script which checks for new commits in given repo/branch and informs you with Discord message.

### Built With
   - [discord.sh](https://github.com/ChaoticWeg/discord.sh) - bash integration for Discord webhooks
   - python 

### How to use
1. Clone repository
2. Create file .webhook with your channel webhook link inside
3. Clone repository you want to watch next to folder with Script/bot (if you want to watch other branch then master, clone repo with this branch only)
   ```
   git clone --single-branch -branch link
   ```
4. In file commit.txt insert last commit name (commit from which you want to start watching)
5. Setup script:
   1. Path to watched repo
   2. Interval of checking for new commits
   3. If script should run constantly, or make a few round (e.g. 120 loops, with interval of 1 minute, to check for new commits between 7am and 9am) 
   4. Your Discord message, bot name, avatar etc.  
6. Run script using screen/shell 
```
python3 main.py
```
or other scheduler e.g. this one on Synology (it allows to run script at a given time, with preset number of loops in main.py)
```
cd /volume/path/to/script
python3 main.py
```
  
7. Script generates log in log.txt file.

In progess