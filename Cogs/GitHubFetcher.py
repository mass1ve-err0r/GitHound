from asyncio import get_event_loop
from requests import get
from datetime import datetime
from discord import Embed, Colour
from discord.ext import commands


class GitHubFetcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("yeet")
        self.baseURL = "https://api.github.com/repos/"
        self.targetURL = []

    @commands.command(name='addRepo')
    @commands.has_role('RepoManager')
    @commands.guild_only()
    async def addRepo(self, ctx, repoOwner: str = None, repoName: str = None):
        timeNow = datetime.now()
        if repoOwner is None or repoName is None:
            errorEmbed = Embed(title='Repo Error', color=Colour(0xCA2167), timestamp=timeNow)
            errorEmbed.add_field(name='**Details**', value='A field was missing!', inline=False)
            await ctx.send(embed=errorEmbed)
            return
        self.targetURL.append(self.baseURL + repoOwner + "/" + repoName + "/commits")
        successEmbed = Embed(title='Setup Success', color=Colour(0x21CA95), timestamp=timeNow)
        successEmbed.add_field(name='**Status**', value='Successfully added repo to list', inline=False)
        successEmbed.add_field(name='**Repository**', value="https://github.com/"+repoOwner+"/"+repoName, inline=False)
        await ctx.send(embed=successEmbed)
        return

    @commands.command(name='deleteRepo')
    @commands.has_role('RepoManager')
    @commands.guild_only()
    async def deleteRepo(self, ctx, repoName: str, really: int = 0):
        timeNow = datetime.now()
        if really == 0:
            errorEmbed = Embed(title='Repo Error', color=Colour(0xCA2167), timestamp=timeNow)
            errorEmbed.add_field(name='**Details**', value='Confirmation was missing!', inline=False)
            await ctx.send(embed=errorEmbed)
            return
        else:
            for i in self.targetURL:
                urlBits = i.split('/')
                if urlBits[5] == repoName:
                    self.targetURL.remove(repoName)
                    successEmbed = Embed(title='Deletion Success', color=Colour(0x21CA95), timestamp=timeNow)
                    successEmbed.add_field(name='**Status**', value='Successfully removed repo from list!', inline=False)
                    await ctx.send(embed=successEmbed)
                    return

    @commands.command(name='listRepos')
    @commands.has_role('RepoManager')
    @commands.guild_only()
    async def listRepos(self, ctx):
        timeNow = datetime.now()
        repoEmbed = Embed(title='Currently Monitored Repositories', color=Colour(0x21CA95), timestamp=timeNow)
        for i in self.targetURL:
            urlBits = i.split('/')
            listString = "User: " + urlBits[4] + "\nRepo: " + urlBits[5]
            repoEmbed.add_field(name='**Entry #' + str(self.targetURL.index(i)) + "**", value=listString, inline=False)
        await ctx.send(embed=repoEmbed)
        return

    @commands.command(name='getCommits')
    @commands.has_role('RepoManager')
    @commands.guild_only()
    async def getCommits(self, ctx, repoNum: int, commitAmount: int):
        timeNow = datetime.now()
        target = self.targetURL[repoNum]
        commits = await self.createCommitDictArray(target, commitAmount)
        if not commits:
            errorEmbed = Embed(title='Fetching Error', color=Colour(0xCA2167), timestamp=timeNow)
            errorEmbed.add_field(name='**Details**', value='Malformed URL ! (Repo doesnt exist or is private?)', inline=False)
            await ctx.send(embed=errorEmbed)
            return
        for commitDict in commits:
            commitEmbed = Embed(title='Commit Details', color=Colour(0x21CA95), timestamp=timeNow)
            commitEmbed.add_field(name='**Author**', value=commitDict['author'], inline=False)
            commitEmbed.add_field(name='**E-Mail**', value=commitDict['email'], inline=False)
            commitEmbed.add_field(name='**Message**', value=commitDict['message'], inline=False)
            commitEmbed.add_field(name='**Link**', value=commitDict['url'], inline=False)
            commitEmbed.add_field(name='**Date**', value=commitDict['date'], inline=False)
            commitEmbed.set_footer(text='Git Hound')
            await ctx.send(embed=commitEmbed)
        return

    async def createCommitDictArray(self, url, amount):
        retArray = []
        loop = get_event_loop()
        future1 = loop.run_in_executor(None, get, url)
        response_data = await future1
        data_json = response_data.json()
        maxRange = len(data_json) if (len(data_json) < amount) else amount
        try:
            for commit in data_json:
                if maxRange == 0:
                    break
                else:
                    maxRange -= 1
                cAuthor = commit['commit']['author']['name']
                cEmail = commit['commit']['author']['email']
                cDateRAW = commit['commit']['author']['date']
                cDate = datetime.strptime(cDateRAW, "%Y-%m-%dT%H:%M:%SZ").strftime('%d-%m-%Y at %H:%M')
                cMessage = commit['commit']['message']
                cURL = commit['html_url']
                commitDict = {
                    "author": cAuthor,
                    "email": cEmail,
                    "date": cDate,
                    "message": cMessage,
                    "url": cURL
                }
                retArray.append(commitDict)
            return retArray
        except Exception as e:
            return []

    @addRepo.error
    @deleteRepo.error
    @listRepos.error
    @getCommits.error
    async def common_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            embedx = Embed(title="Command Invocation Error", colour=Colour(0x000001))
            embedx.add_field(name="dmesg", value="Argument number mismatch! Please check your command.")
            await ctx.send(embed=embedx, delete_after=5)
        elif isinstance(error, commands.MissingRole):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            return
        else:
            embedx = Embed(title="Command Error", colour=Colour(0x000001))
            embedx.add_field(name="dmesg", value="Unknown error, contact Bot Administrator!")
            await ctx.send(embed=embedx, delete_after=5)


def setup(bot):
    bot.add_cog(GitHubFetcher(bot))
