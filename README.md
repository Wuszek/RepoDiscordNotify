## Commits checking script with Discord bot

Discord bot integrated with simple python script which checks for new commits in given repo/branch and informs you with Discord message.

### Built With
   - [discord.sh](https://github.com/ChaoticWeg/discord.sh) - bash integration for Discord webhooks
   - python 

### How to use
1. Clone repository
   ```
   git clone https://git.kobiela.click/wiktor.kobiela/Repo_discord_notifier.git
   ```
2. Create file .webhook with your channel webhook link inside
3. Start script. You can check available option by:
   ```
    python3 notify.py --help
   ====================================== DISPLAYING HELP ======================================
   python3 notify.py --repo <link_to_repository> --branch <branch_to_be_observed>
   --repo: Link to cloned repo, with .git at the end.
   --branch: Branch name, that will be cloned. Default is master.
   In code: setup sleep timer and Discord Bot message.
   e.g. of usage:
   python3 notify.py --repo https://github.com/OpenVisualCloud/Dockerfiles.git --branch v21.3
   =============================================================================================
   ```
4. To start script, run in shell/screen:
   ```
   python3 notify.py --repo <link_to_repo.git> --branch <branch_to_observe>
   ```
   a. or other scheduler e.g. this one on Synology (it allows to run script at a given time, with preset number of loops in notify.py)
   ```
   cd /volume/path/to/script
   python3 notify.py --repo <link_to_repo.git> --branch <branch_to_observe>
   ```
###Script at the beginning will:
   * Check, if given repo link is correct. If no branch given, default is master
   * Download discord.sh script and make it executable
   * Check, if given repository is on disk in ```cd ../```
      * If not, download repository
      * If yes but wrong branch, delete repo folder and download again with correct one
      * If yes, leave it alone
   * Create file ```commit.txt```, save there ```last-1``` commit name
      * It will send you notify about latest commit, just to check if bot works, then it will overrite ```commit.txt``` 
        with latest commit name 
   * Will generate commit link using repo path and commit hash  
   * Will save its logs to ```log.txt``` file

### Additional setup:
   * Interval of checking for new commits (default is 10s)
   * If script should run constantly, or make a few rounds (e.g. 120 loops, with interval of 1 minute, to check for new commits between 7am and 9am) 
   * Your Discord message, bot name, avatar etc.  

