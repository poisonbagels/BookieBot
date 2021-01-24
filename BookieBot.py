# BookieBot.py
import os
import json
import discord
import asyncio
from discord.ext import commands
from itertools import islice

from dotenv import load_dotenv

load_dotenv()

TOKEN = 'NzY4OTYxMjA3OTQ3NjI0NDQ4.X5IE7g.LJ8ilWQw0jKeNkl9rF381xdS74k'

client = discord.Client()
bot = commands.Bot('$')

global betting
global betteam
global betamount
global userliandri
global author
global user
global numredbets
global numbluebets

betting = 0
betteam = 'not specified'
betamount = 0
userliandri = 0
numredbets = 0
numbluebets = 0

with open('bank.txt') as f:
    bank = json.load(f)

# bank = {'user': []}

winners = []
losers = []
currentbets = []


# returns a users current liandri
def findmoney(json_object, name):
    for entry in json_object['user']:
        if name == entry['name']:
            return entry['Liandri']


def findtargetmoney(json_object, name):
    for entry in json_object['user']:
        if name == entry['username']:
            return entry['Liandri']

        if name == entry['mentionname']:
            return entry['Liandri']

        namenoex = name.replace('!', '')

        if namenoex == entry['mentionname']:
            return entry['Liandri']


def findtargetname(json_object, name):
    for entry in json_object['user']:
        if name == entry['username']:
            return entry['username']

        if name == entry['mentionname']:
            return entry['username']

        namenoex = name.replace('!', '')

        if namenoex == entry['mentionname']:
            return entry['username']


def findcurrentbet(json_object, name):
    for entry in json_object['user']:
        if name == entry['name']:
            return entry['Current Bet']


def findmentionname(json_object, name):
    for entry in json_object['user']:
        if name == entry['username']:
            return entry['mentionname']

        if name == entry['mentionname']:
            return entry['mentionname']

        namenoex = name.replace('!', '')

        if namenoex == entry['mentionname']:
            return entry['mentionname']


def updatecurrentbet(json_object, name, money):
    for entry in json_object['user']:
        if name == entry['name']:
            entry['Current Bet'] = money
            with open('bank.txt', 'w') as outfile:
                json.dump(bank, outfile)


def updatecurrentteam(json_object, name, team):
    for entry in json_object['user']:
        if name == entry['name']:
            entry['Current team'] = team
            with open('bank.txt', 'w') as outfile:
                json.dump(bank, outfile)


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def sortbymoney():
    sorted_list = dict(bank)

    sorted_list['user'] = sorted(bank['user'], key=lambda x: x['Liandri'], reverse=True)

    # n_items = take(x, sorted_list.['user']())

    print(sorted_list)

    return sorted_list


def addtargetmoney(target, amount):
    print('target =' + target)

    for entry in bank['user']:

        print(entry['name'])
        if entry['username'] == target:
            currentmoney = entry['Liandri']
            print('HEY!')
            entry['Liandri'] = currentmoney + int(amount)

    with open('bank.txt', 'w') as outfile:
        json.dump(bank, outfile)


def subtracttargetmoney(target, amount):
    print('target =' + target)

    for entry in bank['user']:

        print(entry['name'])
        if entry['username'] == target:
            currentmoney = entry['Liandri']
            print('HEY!')
            entry['Liandri'] = currentmoney - int(amount)

    with open('bank.txt', 'w') as outfile:
        json.dump(bank, outfile)


def updatemoney(message, json_object, winteam):
    for entry in json_object['user']:

        currentbet = entry['Current Bet']
        currentmoney = entry['Liandri']

        if winteam == 'none':
            entry['Current Bet'] = 0
            entry['Current Team'] = 'none'

            with open('bank.txt', 'w') as outfile:
                json.dump(bank, outfile)

        else:
            # check for tie. pays out half
            if winteam == entry['Current team'] and winteam == 'tie' and entry['Current Bet'] > 0:

                winners.append(
                    str(entry['mentionname']) + '(' + str((entry['Liandri']) + entry['Current Bet']) + '=' + str(
                        entry['Liandri']) + '+' + str(entry['Current Bet']) + ')')

                entry['Liandri'] = currentmoney + (currentbet / 2)

                entry['Current Bet'] = 0
                entry['Current Team'] = 'none'

            else:

                if winteam == entry['Current team'] and entry['Current Bet'] > 0:

                    winners.append(
                        str(entry['mentionname']) + '(' + str((entry['Liandri']) + entry['Current Bet']) + '=' + str(
                            entry['Liandri']) + '+' + str(entry['Current Bet']) + ')')

                    entry['Liandri'] = currentmoney + currentbet

                    entry['Current Bet'] = 0
                    entry['Current Team'] = 'none'

                    print(entry)

                    with open('bank.txt', 'w') as outfile:
                        json.dump(bank, outfile)

                elif entry['Current Bet'] > 0:

                    losers.append(
                        str(entry['mentionname']) + '(' + str((entry['Liandri']) - entry['Current Bet']) + '=' + str(
                            entry['Liandri']) + '-' + str(entry['Current Bet']) + ')')
                    entry['Liandri'] = currentmoney - currentbet
                    entry['Current Bet'] = 0
                    entry['Current Team'] = 'none'
                    print(entry)

                    with open('bank.txt', 'w') as outfile:
                        json.dump(bank, outfile)

        print(entry)


def giveallx(amount):
    for entry in bank['user']:
        print(type(amount))
        currentmoney = entry['Liandri']

        amount = int(amount)

        entry['Liandri'] = currentmoney + amount

        with open('bank.txt', 'w') as outfile:
            json.dump(bank, outfile)


def givewelfare():
    for entry in bank['user']:

        if entry['Liandri'] == 0:
            entry['Liandri'] = 25

    with open('bank.txt', 'w') as outfile:
        json.dump(bank, outfile)


# Gives LLiandri to user if they haven't already claimed it that week
# TODO - Make this actually weekly
#
#

@bot.command()
async def register(message):
    global bank
    author = message.author
    user = author.mention
    username = message.author.display_name

    people = json.dumps(bank)
    authorstring = str(author)

    if authorstring in people:
        response = 'You are already registered' + ' ' + user
        await message.channel.send(response)

    else:
        # adds money to bank
        bank['user'].append({
            'name': str(author),
            'username': str(username),
            'mentionname': user,
            'Liandri': 100,
            'Current Bet': 0,
            'Current team': 'none'
        })

        print(bank)
        with open('bank.txt', 'w') as outfile:
            json.dump(bank, outfile)

        response = 'You have received 100 Liandri' + ' ' + user
        await message.channel.send(response)


@bot.command()
async def weekly(message):

    author = message.author
    user = author.mention

    response = 'This command is outdated and you should receive 100 Liandri every Sunday.'

    await message.channel.send(response)

    response = 'Use $register to register for betting' + ' ' + user

    await message.channel.send(response)


#
# Checks Lirandri for self
#

@bot.command()
async def liandri(message):
    author = message.author
    user = author.mention

    userliandri = findmoney(bank, str(author))

    if userliandri:
        response = 'You currently have ' + str(userliandri) + ' Liandri ' + user
        await message.channel.send(response)
    elif userliandri == 0:
        response = 'You have used all of your liandri for this week ' + user
        await message.channel.send(response)
    else:
        response = 'You have not registered your discord account $register' + user
        await message.channel.send(response)


@bot.command()
async def currentbet(message):
    author = message.author
    user = author.mention

    userbet = findcurrentbet(bank, str(author))

    if userbet:
        response = 'Your current bet is ' + str(userbet) + ' Liandri ' + user
        await message.channel.send(response)
    elif userliandri == 0:
        response = 'You do not have a current bet ' + user
        await message.channel.send(response)
    else:
        response = 'You do not have a current bet ' + user
        await message.channel.send(response)


@bot.command()
@commands.has_role("Active Members")
async def give(message, amount, target):
    author = message.author
    user = author.mention

    userbet = findcurrentbet(bank, str(author))

    targetmention = str(findmentionname(bank, target))

    print(userbet)
    print(author)
    print(user)

    if betting == 1:

        response = "You cannot give liandri while betting is open."
        await message.channel.send(response)

    elif userbet > 0:

        response = "You cannot give after you have placed a bet."
        await message.channel.send(response)

    else:

        if int(amount) < 0:

            response = "You cannot steal another user's liandri."
            await message.channel.send(response)

        else:

            userliandri = findmoney(bank, str(author))

            if userliandri < int(amount):

                response = "You do not have enough liandri for this transaction."
                await message.channel.send(response)

            elif (int(userliandri)) - (int(amount)) < 25:

                response = "You cannot give liandri to bring your total below 25."
                await message.channel.send(response)

            else:

                targetliandri = findtargetmoney(bank, str(target))

                convertedtarget = findtargetname(bank, str(target))

                converteduser = findtargetname(bank, str(user))

                addtargetmoney(convertedtarget, amount)

                subtracttargetmoney(converteduser, amount)

                print(userliandri)
                print(targetliandri)

                response = user + ' has given ' + str(targetmention) + ' ' + amount + ' liandri'
                await message.channel.send(response)


#
# opens betting
#
#

@bot.command()
@commands.has_permissions(manage_messages=True)
async def openbets(message):
    global betting

    if betting == 0:

        betting = 1
        response = 'Bets are open for the next 10 minutes!'
        await message.channel.send(response)

        await asyncio.sleep(480)
        #test below
        #await asyncio.sleep(8)

        if betting == 0:
            return

        response = 'Bets close in 2 minutes!!'
        await message.channel.send(response)

        #uncomment
        await asyncio.sleep(120)

        if betting == 0:
            return

        response = 'Bets are closed!'
        await message.channel.send(response)

        betting = 0

        currentbets[:] = []
        currentredbets = []
        currentbluebets = []

        for x in bank['user']:
            if x['Current Bet'] > 0 and x['Current team'] == 'red':

                currentredbets.append(str(x['mentionname']) + '(' + str(x['Current Bet']) + ')')

            elif x['Current Bet'] > 0 and x['Current team'] == 'blue':

                currentbluebets.append(str(x['mentionname']) + '(' + str(x['Current Bet']) + ')')

        redbigbetstring = currentredbets

        betredstring = str(redbigbetstring).replace(',', ':heavy_dollar_sign:')
        betredstring = betredstring.replace('[', '')
        betredstring = betredstring.replace(']', '')
        betredstring = betredstring.replace("'", '')

        bluebigbetstring = currentbluebets

        betbluestring = str(bluebigbetstring).replace(',', ':heavy_dollar_sign:')
        betbluestring = betbluestring.replace('[', '')
        betbluestring = betbluestring.replace(']', '')
        betbluestring = betbluestring.replace("'", '')

        numredbets = len(currentredbets)

        numbluebets = len(currentbluebets)

        response = '**[' +str(numredbets) + ']** **Current red bets:** ' + betredstring
        await message.channel.send(response)

        response = '**[' +str(numbluebets) + ']** **Current blue bets:** ' + betbluestring

        await message.channel.send(response)

    else:
        response = 'Bets are already open.'
        await message.channel.send(response)


# Closes betting and applies winnings or losses

@bot.command()
@commands.has_permissions(manage_messages=True)
async def closebets(message):
    global betting
    betting = 0
    response = 'Bets are closed!'
    await message.channel.send(response)


@bot.command()
async def bet(message, arg, team):
    global betting
    global numredbets
    global numbluebets

    author = message.author
    user = author.mention

    untuple_str = str(arg)
    betamount = int(untuple_str)

    userliandri = findmoney(bank, str(author))

    betteam = team

    if userliandri is None:

        response = 'You have not registered $register.'
        await message.channel.send(response)

    else:
        if betteam == 'red' or team == 'blue' or team == 'tie':

            if betting == 1 and userliandri >= betamount:
                author = message.author
                user = author.mention
                response = user + ' has placed a ' + str(betamount) + ' Liandri bet for ' + betteam
                updatecurrentbet(bank, str(author), betamount)
                updatecurrentteam(bank, str(author), betteam)
                print(bank)
                await message.channel.send(response)

            elif betting == 1 and userliandri < betamount:
                response = 'You do not have enough Liandri for this bet.'
                await message.channel.send(response)

            elif betting == 1 and userliandri == 0:
                response = user + "You are bankrupt until Sunday."
                await message.channel.send(response)

            else:
                response = 'Betting is not open.'
                await message.channel.send(response)
        else:
            response = betteam + ' is not a valid team'
            await message.channel.send(response)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def winner(message, winteam):
    global winners
    global losers
    updatemoney(message, bank, winteam)

    winnerstring = str(winners).replace(',', ':small_red_triangle:')
    winnerstring = winnerstring.replace('[', '')
    winnerstring = winnerstring.replace(']', '')
    winnerstring = winnerstring.replace("'", '')

    response = '**Winners:** ' + winnerstring
    await message.channel.send(response)

    loserstring = str(losers).replace(',', ':small_red_triangle_down:')
    loserstring = loserstring.replace('[', '')
    loserstring = loserstring.replace(']', '')
    loserstring = loserstring.replace("'", '')

    response = '**Losers:** ' + loserstring
    await message.channel.send(response)

    currentbets[:] = []
    winners[:] = []
    losers[:] = []

    givewelfare()


@bot.command()
async def bets(message):

    currentbets[:] = []
    currentredbets = []
    currentbluebets = []

    for x in bank['user']:

        if x['Current Bet'] > 0 and x['Current team'] == 'red':

            currentredbets.append(str(x['username']) + '(' + str(x['Current Bet']) + ')')

        elif x['Current Bet'] > 0 and x['Current team'] == 'blue':

            currentbluebets.append(str(x['username']) + '(' + str(x['Current Bet']) + ')')

    redbigbetstring = currentredbets

    print(len(currentredbets))

    betredstring = str(redbigbetstring).replace(',', ':heavy_dollar_sign:')
    betredstring = betredstring.replace('[', '')
    betredstring = betredstring.replace(']', '')
    betredstring = betredstring.replace("'", '')

    bluebigbetstring = currentbluebets

    betbluestring = str(bluebigbetstring).replace(',', ':heavy_dollar_sign:')
    betbluestring = betbluestring.replace('[', '')
    betbluestring = betbluestring.replace(']', '')
    betbluestring = betbluestring.replace("'", '')

    numredbets = len(currentredbets)

    numbluebets = len(currentbluebets)

    response = '**[' +str(numredbets) + ']** **Current red bets:** ' + betredstring
    await message.channel.send(response)

    response = '**[' + str(numbluebets) + ']** **Current blue bets:** ' + betbluestring
    await message.channel.send(response)


@bot.command()
async def standings(message, totalnum):

    sortedarray = []
    sorted = sortbymoney()

    for x in sorted['user']:
        sortedarray.append(str(x['username']) + '(' + str(x['Liandri']) + ')')

    redbigbetstring = sortedarray

    betredstring = str(redbigbetstring).replace(',', ':heavy_dollar_sign:')
    betredstring = betredstring.replace('[', '')
    betredstring = betredstring.replace(']', '')
    betredstring = betredstring.replace("'", '')

    print(totalnum)
    print(type(totalnum))

    poop = int(totalnum)

    test = betredstring.split(":heavy_dollar_sign:")[:poop]

    test = str(test).replace(',', ':heavy_dollar_sign:')
    test = test.replace('[', '')
    test = test.replace(']', '')
    test = test.replace("'", '')

    print(betredstring)
    print(test)
    response = '**Liandri Totals:** ' + str(test)
    await message.channel.send(response)


@bot.command()
@commands.has_permissions(administrator=True)
async def giveall(message, totalnum):

    giveallx(totalnum)

    response = '+ ' + str(totalnum) + ' for all users'

    await message.channel.send(response)


@bot.command()
async def welfare(message):

    givewelfare()

    response = 'This command is now automatically applied when you are bankrupt and is not necessary'

    await message.channel.send(response)


global channel_ut4
global channel_garden
id_user_pugbot = 141723331471605760
id_chan_ut4 = 192460940409700352
id_chan_garden = 493208320916717578
str_puglive = 'Teams have been selected:'


@client.event
async def on_ready():

    global channel_ut4
    channel_ut4 = client.get_channel(id_chan_ut4)
    global channel_garden
    channel_garden = client.get_channel(id_chan_garden)


@client.event
async def on_message(message):

    if message.content.startswith(
            str_puglive) and message.author.id == id_user_pugbot and message.channel == channel_garden:
        await channel_ut4.send(message.content)
        await channel_ut4.send("$openbets")


bot.run(TOKEN)
