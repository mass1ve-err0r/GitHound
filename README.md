# GitHound
> A GitHub v3-API compliant watchdog | Python 3.6+

This is just a simple Bot for basic commit monitoring & pulling infos.

Does _not_ feature a databse, so once it goes offline you will have to re-setup your repos. Howerver, setting up a DB just for this would be easy as well and it can also be integrated into your existing database!

## Triggers & Usage
#### _(!) Some commands have mandatory arguments, those are noted with `<>` and optional with `[]` (!)_
#### _=> The prefix is currently set to '?', this can ofc be changed_
- addRepo \<repoOwner\> \<repoName\>
	- Add a repository to the watchlist
- deleteRepo \<repoName\> \<1 or 0\>
	- Delete a repository from the watchlist
- listRepos
	- lists all the currently monitor-able repositories in the watchlist, starting with index 0
- getCommits \<RepoIndexInWatchlist\> \<AmountOfCommits\>
	- Gets the designated amount of commits off a repo (latest -> oldest)
		- Fallbacks to the max length if specified amount exceeds commits in total

## Deployment
Just fork the project or download the project, replace the entire `environ.get('TOKEN')` String in `Bot.py` with your Discord Bot Token and your ready to deploy it anywhere and just run it!

If you'd like to setup env-vars, then just set `TOKEN=<YourToken>` and you're ready!

#### => Special Note for starting with PM2:
if the regular `pm2 start Bot.py` does _not_ work, specify the interpreter as well. So do it like this:

`pm2 start Bot.py --interpreter python3`
## Credits
- Rapptz - DiscordPy
- Some Pigeon for flying by and stealing my bread
