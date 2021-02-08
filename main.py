import discord
import os
from keep_alive import keep_alive
from riotwatcher import LolWatcher
from discord.ext import commands
import asyncio

channelid = 0
client = commands.Bot(command_prefix='$')
client.remove_command('help')
api_key = os.getenv('api_key')
watcher = LolWatcher(api_key)
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
    for i in users:
      me = watcher.summoner.by_name('na1', i)
      my_matches = watcher.match.matchlist_by_account('na1' ,me['accountId'])
      last_match = my_matches['matches'][0]
      match_detail = watcher.match.by_id('na1', last_match['gameId'])
      if(match_detail != userHistory.get(i)):
        userHistory[i] = match_detail;
        participants_row = {}
        sum = 0
        kda = 0
        for row in match_detail['participants']:
          for row2 in match_detail['participantIdentities']:
            if(row['participantId'] == row2['participantId']):
              if((watcher.summoner.by_id('na1',row2['player']['summonerId'])['name'].lower() == i.lower())):
                participants_row['champion'] = champ_dict[str(row['championId'])]         
                participants_row['kills'] = row['stats']['kills']
                participants_row['deaths'] = row['stats']['deaths']
                participants_row['assists'] = row['stats']['assists']
                winloss = 'won'
                if(row['stats']['win'] == False):
                  winloss = 'lost'
                sum = (participants_row['kills']+participants_row["assists"])
                sum = float(sum)
                divide = float(participants_row['deaths'])
                try:
                  kda = sum/divide
                  kda = round(kda, 2)
                except:
                  kda = 'perfect'
                await channel.send(i + ' just ' + winloss + 'a game on ' + participants_row['champion'] + ' with a ' + str(kda) + ' KDA.')
                break

    await asyncio.sleep(60) #every minute
    
@client.command()
async def lolname(ctx, arg):
  check = True
  for i in users:
    if(i == arg):
      check = False
  if(check):  
    users.append(arg)
  await ctx.channel.send(arg+' has been added to the user list.')

@client.command()
async def loldel(ctx, arg):
  users.remove(arg)
  userHistory.pop(arg,'null')
  await ctx.channel.send(arg+' has been removed from the user list.')

@client.command()
async def lolprint(ctx):
  userList = ''
  for i in users:
    userList += (i+' ')
  await ctx.channel.send(userList)

@client.command()
async def lolhelp(ctx):
  await ctx.channel.send('List of commands:\n$lolsetup <CHANNEL ID> - run bot setup.\n$lolname <SUMMONER NAME> - adds a user to the list.\n$loldel <SUMMONER NAME> - deletes a user from the list.\n$lolprint - print all users on the list.')

@client.command()
async def lolsetup(ctx, arg):
  global channelid, setup
  if(not(setup)):
    channelid = int(arg)
    await ctx.channel.send('I will now display stats in ' + client.get_channel(channelid).name + '.')
    setup = True
    client.loop.create_task(status_task())
    print("SETUP COMPLETE")
  else:
    await ctx.channel.send('I am already set up in ' + client.get_channel(channelid).name + '. Please kick me and add me back to redo setup.')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name='$lolhelp'))

keep_alive()
client.run(os.getenv('TOKEN'))
