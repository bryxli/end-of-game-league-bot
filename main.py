import discord
from riotwatcher import LolWatcher
from discord.ext import commands
import asyncio
from datetime import datetime
import json

channelid = 0
client = commands.Bot(command_prefix='$')
client.remove_command('help')
watcher = LolWatcher('<RIOT-API-TOKEN>')
latest = watcher.data_dragon.versions_for_region('na1')['n']['champion']
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']
users = []
userHistory = {}
setup = False


@client.event
async def status_task():
    channel = client.get_channel(channelid)
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("System Time: ", current_time)
        try:
            for i in users:
                me = watcher.summoner.by_name('na1', i)
                my_matches = watcher.match.matchlist_by_account('na1', me['accountId'])
                last_match = my_matches['matches'][0]
                match_detail = watcher.match.by_id('na1', last_match['gameId'])
                if match_detail != userHistory.get(i):
                    userHistory[i] = match_detail
                    participants_row = {}
                    complete = False
                    for row1 in match_detail['participants']:
                        for row2 in match_detail['participantIdentities']:
                            if row1['participantId'] == row2['participantId']:
                                if ((watcher.summoner.by_id('na1', row2['player']['summonerId'])[
                                         'name'].lower() == i.lower())):
                                    participants_row['champion'] = champ_dict[str(row1['championId'])]
                                    participants_row['kills'] = row1['stats']['kills']
                                    participants_row['deaths'] = row1['stats']['deaths']
                                    participants_row['assists'] = row1['stats']['assists']
                                    winloss = 'won'
                                    if not row1['stats']['win']:
                                        winloss = 'lost'
                                    addition = (participants_row['kills'] + participants_row["assists"])
                                    addition = float(addition)
                                    divide = float(participants_row['deaths'])
                                    try:
                                        kda = addition / divide
                                        kda = round(kda, 2)
                                    except ZeroDivisionError:
                                        kda = 'perfect'
                                    await channel.send(i + ' just ' + winloss + 'a game on ' + participants_row[
                                        'champion'] + ' with a ' + str(kda) + ' KDA.')
                                    complete = True
                                    break
                        if complete:
                            break
        except Exception as ex:
            print(str(ex))
        await asyncio.sleep(60)  # every minute


@client.command()
async def lolname(ctx, arg):
    check = True
    for i in users:
        if i == arg:
            check = False
    if check:
        users.append(arg)
    await ctx.channel.send(arg + ' has been added to the user list.')


@client.command()
async def loldel(ctx, arg):
    check = False
    i = 0
    while check is False and i < len(users):
        if users[i] == arg:
            check = True
        i = i + 1
    if check:
        users.remove(arg)
        userHistory.pop(arg, 'null')
    await ctx.channel.send(arg + ' has been removed from the user list.')


@client.command()
async def loldelall(ctx):
    users.clear()
    userHistory.clear()
    await ctx.channel.send("User list cleared.")


@client.command()
async def lolprint(ctx):
    user_list = ''
    for i in users:
        user_list += (i + ' ')
    await ctx.channel.send(user_list)


@client.command()
async def lolhelp(ctx):
    await ctx.channel.send(
        'List of commands:\n$lolsetup <CHANNEL ID> - run bot setup.\n$lolname <SUMMONER NAME> - adds a user to the '
        'list.\n$loldel <SUMMONER NAME> - deletes a user from the list.\n$loldelall - clears the user list.\n$lolprint '
        '- print all users on the list.\n$lolsave - save names of all users to \\data.json.\n$lolimport - imports user '
        'list from \\data.json.')


@client.command()
async def lolsave(ctx):
    data = json.dumps(users)
    with open('data.json', 'w') as f:
        json.dump(data, f)
    await ctx.channel.send('Player names successfully saved to \\data.json.')


@client.command()
async def lolimport(ctx):
    global users
    with open('data.json') as f:
        data = json.load(f)
    users = json.loads(data)
    await ctx.channel.send('User list successfully imported from \\data.json.')


@client.command()
async def lolsetup(ctx, arg):
    global channelid, setup, users
    print(setup)
    if not setup:
        channelid = int(arg)
        await ctx.channel.send('I will now display stats in ' + client.get_channel(channelid).name + '.')
        with open('data.json') as f:
            data = json.load(f)
        users = json.loads(data)
        setup = True
        client.loop.create_task(status_task())
        print("SETUP COMPLETE")
    else:
        await ctx.channel.send('I am already set up in ' + client.get_channel(
            channelid).name + '. Please kick me and add me back to redo setup.')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='$lolhelp'))


client.run('DISCORD-API-TOKEN')
