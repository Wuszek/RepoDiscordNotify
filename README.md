## Commits checking script with Discord bot

Discord bot integrated with simple python script which checks for new commits in given repo/branch and informs you with Discord message.

### Built With
   - [discord.sh](https://github.com/ChaoticWeg/discord.sh) - bash integration for Discord webhooks
   - python3

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
    usage: python3 notify.py [--help] --repo <link> [--branch <branch>] [--time <sec>] [--loops <num>]
    
    Repo_Discord_Notify tool - get pinged, whenever new commit appears!
    
    required arguments:
      -r <link>, --repo <link>    repository link to cloned repo, with .git at the end
    
    optional arguments:
      -b <name>, --branch <name>  branch name, that will be cloned - default is master
      -t <time>, --time <time>    idle time between next pull&check - default is 10s
      -l <quan>, --loop <quan>    number of loops that script should make - default is infinite (0)
    
    helpful arguments:
      -v, --version               show program's version number and exit
      -h, --help                  show this help message and exit
    
    © 2021, wiktor.kobiela, Repo_Discord_Notify - feel free to contribute
   ```
4. To start script, run in shell/screen:
   ```
   python3 notify.py --repo <link_to_repo.git> --branch <branch_to_observe> --time <idle_time> --loop <loops_num>
   e.g:
   python3 notify.py --repo https://git.kobiela.click/wiktor.kobiela/Test.git --branch master --time 100 --loops 10
   ```
   a. or other scheduler e.g. this one on Synology (it allows running script at a given time, with preset number of loops in notify.py)
   ```
   cd /volume/path/to/script
   python3 notify.py --repo <link_to_repo.git> --branch <branch_to_observe> --time <idle_time> --loop <loops_num>
   ```
### Script at the beginning will:
   * Check, if given repo link is correct. 
   * Check, if given branch actually exists on remote, default is 'master'  
   * Check if discord.sh script exists, if no download and make it executable  
      * Check for .webhook file
   * Check, if given repository is on disk in ```cd ../```
      * If not, download repository
      * If yes but wrong branch, delete repo folder and download again with correct one
      * If yes, leave it alone
   * Save ```last-1``` commit hash in global variable
      * It will send you notify about the latest commit, just to check if bot works, then it will override variable 
        with the latest commit hash
   * Run forever or finite number of loops, if said so     
   * Will generate commit link using repo path and commit hash  
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