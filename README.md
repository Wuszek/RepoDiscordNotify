## Commits checking script with Discord bot

Discord bot integrated with simple python script which checks for new commits in given repo/branch and informs you with Discord message.

### Built With
   - [discord.sh](https://github.com/ChaoticWeg/discord.sh) - bash integration for Discord webhooks
   - python3

### Requirements
Script requires wget, curl and jq to work properly. Just run:
```pip3 install -r requirements.txt```
to install all packages.

### How to use
1. Clone repository
   ```
   git clone https://git.kobiela.click/wiktor.kobiela/Repo_Discord_Notify.git
   ```
2. Create a file ```.webhook``` with your channel webhook link inside
3. Start script. You can check available options by:
   ```
    python3 notify.py --help

    → 20/03/2021, 18:01:29
    usage: python3 notify.py [--help] --repo <link> [--branch <name>] [--time <sec>] [--loop <num>] [--check]
    
    Repo_Discord_Notify tool - get pinged, whenever new commit appears!
    
    required arguments:
      -r <link>, --repo <link>    repository link to cloned repo, with .git at the end
    
    optional arguments:
      -b <name>, --branch <name>  branch name, that will be cloned - default is master
      -t <sec>, --time <sec>    idle time between next pull&check - default is 10s
      -l <num>, --loop <num>    number of loops that script should make - default is infinite (0)
    
    helpful arguments:
      -c, --check                 add this to your command, to send test discord message before script starts
      -v, --version               show program's version number and exit
      -h, --help                  show this help message and exit
    
    © 2021, wiktor.kobiela, Repo_Discord_Notify - feel free to contribute
   ```
4. To start script, run in shell/screen:
   ```
   python3 notify.py --repo <link_to_repo.git> --branch <branch_to_observe> --time <idle_time> --loop <loops_num>
   e.g:
   python3 notify.py --repo https://git.kobiela.click/wiktor.kobiela/Test.git --branch master --time 100 --loop 10
   ```
   a. or other scheduler e.g. this one on Synology (it allows running script at a given time, with preset number of loops in notify.py)
   ```
   cd /volume/path/to/script
   python3 notify.py --repo <link_to_repo.git> --branch <branch_to_observe> --time <idle_time> --loop <loops_num>
   ```
### Script at the beginning will:
   * With ```argument_parse()``` function:
       * Parse all given arguments
       * Check, if given link is valid repository link
       * Check, if time and loop arguments are positive ints
   * With ```get_files()``` function:
       * Check, if ```discord.sh``` script is downloaded (if not, download and make it executable)
       * Check, if ```.webhook``` file exists. If not, exit program.
   * With ```test()``` function (if flag ```--check``` given):
       * Send test message, to verify that ```.webhook``` and Discord connection works fine
   * With ```clone()``` function:
       * Check, if given branch exists on remote
       * Check if repository is already downloaded, and with which branch
            * If not, download repository
            * If yes but wrong branch, delete repo folder and download again with correct one
            * If yes, leave it alone
   * With ```commit_check()``` function:
       ```.commit``` file contains ('repo_name', 'branch_name', 'commit_hash')
       * Check if ```.commit``` file exists, if not create it and fill with data
       * If exists, check for repo_name and branch_name, if the same as given in commnad
            * If the same, move forward (and check for new commits from this place)
            * If not the same, clear file and fill with new data
   * With ```job()``` function:
      * Run forever on in loops
      * Check for new commits (from last commit hash from ```.commit``` file)
            * If new commit, send Discord notification (generate commit link using repo path and commit hash)
      * If no new commits, wait given time until next loop
   * Will save its logs to ```log.txt``` file, if said so

### Sample discord message

#### Code

```
command = f'./discord.sh \
          --username "NotificationBot" \
          --avatar "https://i.imgur.com/12jyR5Q.png" \
          --text "Commit appear: **{commit_name}** \\n path: <{commit_link}{commit_hash}>"'
```
#### Looks

![alt text](https://i.imgur.com/mFnKPBW.png)

#### How to create more complex messages

```
./discord.sh \
  --webhook-url="$WEBHOOK" \
  --username "NotificationBot" \
  --avatar "https://i.imgur.com/12jyR5Q.png" \
  --text "Check out this embed!" \
  --title "New Notification!" \
  --description "This is a description\nPretty cool huh?" \
  --color "0xFFFFFF" \
  --url "https://github.com/ChaoticWeg/discord.sh" \
  --author "discord.sh" \
  --author-url "https://github.com/ChaoticWeg/discord.sh" \
  --author-icon "https://i.imgur.com/12jyR5Q.png" \
  --image "https://i.imgur.com/12jyR5Q.png" \
  --thumbnail "https://i.imgur.com/12jyR5Q.png" \
  --footer "discord.sh" \
  --footer-icon "https://i.imgur.com/12jyR5Q.png" \
  --timestamp
  ```

More information and source [HERE](https://github.com/ChaoticWeg/discord.sh#3-using-the-script).

### Additional setup
   * Your Discord message, bot name, avatar etc.  

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Licence

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)