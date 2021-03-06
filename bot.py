import os
import asyncio
import json
import os
import random
import discord
from discord.ext import commands, tasks
import datetime
from discord.utils import get
from itertools import cycle
from PIL import Image, ImageFont, ImageDraw
import gspread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Screenshot import *
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta, date
import urllib.parse
import urllib.request
from googletrans import Translator, constants
import python_weather
from instagram_web_api import Client, ClientCompatPatch, ClientError, ClientLoginError
import instaloader
from GoogleNews import GoogleNews
from PyDictionary import PyDictionary
from pytrivia import Category, Diffculty, Type, Trivia

os.system('pip install googletrans==3.1.0a0')

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
ss = Screenshot_Clipping.Screenshot()

intents = discord.Intents(messages=True,
                          guilds=True,
                          reactions=True,
                          members=True,
                          presences=True)
bot_prefix = '.'
bot = commands.Bot(command_prefix=bot_prefix,
                   intents=intents,
                   case_insensitive=True)
bot.remove_command('help')

gc = gspread.service_account('adept-comfort-330218-f1e157e04890.json')
sh = gc.open("nsborobotNames")
worksheet = sh.worksheet("Sheet1")

sh2 = gc.open("nsborobotGenshin")
worksheet2 = sh2.worksheet("Sheet1")

sh3 = gc.open("classes")
worksheet3 = sh3.worksheet("Sheet1")

sh4 = gc.open("nsborobotHomework")
worksheet4 = sh4.worksheet("Sheet1")

num_names = 150
list_names = worksheet.get_all_values()
list_names = sorted(list_names, key=lambda x: x[1].lower())
list_UIDs = worksheet2.get_all_values()
list_classes = worksheet3.get_all_values()
list_hw = worksheet4.get_all_values()

mainshop = [{
    "name":
        "basta_bible",
    "price":
        100,
    "description":
        "Religion",
    "use":
        "You pray for days and days on end, Basta will always be our God"
}, {
    "name": "pc",
    "price": 500,
    "description": "Gaming",
    "use": "You play the FoRtNiTe on your PC"
}, {
    "name": "laptop",
    "price": 300,
    "description": "Work",
    "use": "Your MacBook cooks an egg after running helloworld"
}, {
    "name": "cool_bot",
    "price": 69420,
    "description": "not cool",
    "use": "studymode was definitely not copied"
}, {
    "name":
        "indentured_servant",
    "price":
        10,
    "description":
        "hardworking and strong",
    "use":
        "hey! human rights boi. the servant works very hard so you get 100 coins owner"
}, {
    "name":
        "basta_blessings",
    "price":
        1000,
    "description":
        "gives you luck",
    "use":
        "Basta blesses you kindness and happiness, have a wonderful day!!"
}, {
    "name": "kyt_vote",
    "price": 20,
    "description": "vote KYT for president ",
    "use": "You voted for KYT, his campaign never stops!"
}, {
    "name": "froggy",
    "price": 999,
    "description": "Froggy monta la bicicleta",
    "use": "Froggy monta la bicicleta ???? ????"
}, {
    "name": "steven_prayer",
    "price": 200,
    "description": "Religion",
    "use": "steven blesses you with his cheese, aka 1000 coins"
}, {
    "name": "fortnite",
    "price": 6969,
    "description": "this is not a fortnite server",
    "use": "you play fortnite while Dan default dances on you"
}, {
    "name":
        "calculator",
    "price":
        99,
    "description":
        "get your sweet ti-84 plus ce",
    "use":
        "you download pokemon on your ti-84+ce, smh such a waste of money"
}, {
    "name": "stock",
    "price": 349028,
    "description": "a share of NSBORO bot",
    "use": "you cannot use this, check the price using .stock"
}, {
    "name":
        "minecraft",
    "price":
        50,
    "description":
        "minecraft is epic",
    "use":
        "You create a survival world.....you get blown up by a creeper"
}]

periods = [
    "period 1", "period 2", "period 3", "period 4", "period 5", "period 6",
    "period 7"
]


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(".help"))
    getNews.start()
    get_covid_data.start()
    getInstagram.start()
    print("The NSBORO Bot is up and running.")


@tasks.loop(hours=23)
async def get_covid_data():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(
        "https://www.nsboro.k12.ma.us/site/default.aspx?PageType=3&DomainID=4&ModuleInstanceID=438&ViewID=6446EE88-D30C-497E-9316-3F8874B3E108&RenderLoc=0&FlexDataID=6091&PageID=1&Comments=true"
    )
    driver.maximize_window()

    button = driver.find_element_by_link_text(
        "NSBORO Weekly COVID-19 Dashboard")
    print(button)
    button.click()

    p = driver.current_window_handle

    chwd = driver.window_handles

    for w in chwd:
        if (w != p):
            driver.switch_to.window(w)

    driver.set_window_size(1920, 2000)

    a = ActionChains(driver)
    a.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('[').key_up(
        Keys.CONTROL).key_up(Keys.ALT).perform()

    driver.save_screenshot("ss.png")


@tasks.loop(hours=15)
async def getInstagram():
    username = os.environ['username']
    password = os.environ['password']

    L = instaloader.Instaloader()
    L.login(username, password)

    # gonkgram
    profile = instaloader.Profile.from_username(L.context, 'gonkgram')
    for post in profile.get_posts():
        f = open('gonkgram_oldpost.txt', 'r')
        old_file_name = f.readline()
        filename = L.format_filename(post, target=profile.username)
        if old_file_name.strip() in filename or old_file_name == filename or filename in old_file_name:
            print("nothing new on gonkgram")
            return
        else:
            dir = './/gonkgram//'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
            L.download_post(post, target=profile.username)
            caption_file = filename + '.txt'
            break
    f = open(f".//gonkgram//{caption_file}")
    captions = f.readlines()
    caption = ""
    for cap in captions:
        caption += cap
    file = open("gonkgram_oldpost.txt", "w")
    file.close()
    f = open('gonkgram_oldpost.txt', 'w')
    f.write(filename.strip())
    channel = bot.get_channel(685975002683539569)
    await channel.send(caption)
    path = ".//gonkgram//"
    text_files = [k for k in os.listdir(path) if k.endswith('.jpg')]
    for thing in text_files:
        await channel.send(file=discord.File(f".//gonkgram//{thing}"))

    # gonk2024
    profile = instaloader.Profile.from_username(L.context, 'gonk2024')
    for post in profile.get_posts():
        f = open('gonk2024_oldpost.txt', 'r')
        old_file_name = f.readline()
        filename = L.format_filename(post, target=profile.username)
        if old_file_name.strip() in filename or old_file_name == filename or filename in old_file_name:
            print("nothing new on gonk2024")
            return
        else:
            dir = './/gonk2024//'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
            L.download_post(post, target=profile.username)
            caption_file = filename + '.txt'
            break
    f = open(f".//gonk2024//{caption_file}")
    captions = f.readlines()
    caption = ""
    for cap in captions:
        caption += cap
    file = open("gonk2024_oldpost.txt", "w")
    file.close()
    f = open('gonk2024_oldpost.txt', 'w')
    f.write(filename.strip())
    channel = bot.get_channel(685975002683539569)
    await channel.send(caption)
    path = ".//gonk2024//"
    text_files = [k for k in os.listdir(path) if k.endswith('.jpg')]
    for thing in text_files:
        await channel.send(file=discord.File(f".//gonk2024//{thing}"))


@tasks.loop(hours=24)
async def getNews():
    channel = bot.get_channel(906915291668299786)
    topics = ['news', 'Massachusetts', "COVID-19"]
    for i in topics:
        googlenews = GoogleNews(lang='en', region='US', period="1d")
        if i == 'news':
            title = 'Miscellaneous'
        else:
            title = i
        googlenews.search(i)
        titles = googlenews.get_texts()
        links = googlenews.get_links()
        em = discord.Embed(
            title=f"{title} News",
            description=f"```Recent news about {title}```",
            color=discord.Color.blue())
        for j in range(5):
            em.add_field(name=titles[j], value=links[j])
        await channel.send(embed=em)


@bot.event
async def on_member_join(member):
    channel = await member.create_dm()
    await channel.send(f"""***WELCOME TO THE NSBORO DISCORD SERVER***
You may chat and discuss about anything related to school or have any conversations with classmates.

Please read the rules in the welcome channel and react to the check mark at the bottom to gain access to the rest of 
the server. You may also get your school, graduation year, and class roles in #??????roles . Feel free to use the 
specific channel for your class to ask questions and learn with your classmates. 

Invite your NSBORO friends!

PERMANENT INVITE LINK:  https://discord.gg/Ksb296M

For any inquiries about the server, DM @charlestang06#0754  or @True#7190""")

    await ctx.send(
        f"""Welcome {member.mention} to the NSBORO Discord Server!""")


@bot.event
async def on_message(message):
    id = bot.get_guild(685973564121284692)

    if message.content.lower().find("froggy") != -1:
        emoji = '????'
        await message.add_reaction(emoji)

    if message.content.lower().find("charly") != -1:
        emoji = '<:charlespog:703737266211782768>'
        await message.add_reaction(emoji)

    if message.content.lower().find("basta") != -1:
        emoji = '<:basta:722590619683258479>'
        await message.add_reaction(emoji)

    if message.content.lower().find("kyt") != -1:
        emoji = ':<:kevin:699703167834652733>'
        emoji_2 = '<:emoji_25:699610131784269885>'
        await message.add_reaction(emoji)
        await message.add_reaction(emoji_2)

    bad_words = [
        "nigger", "nigga", "slut", "scum", "cunt", "whore", "retard",
        "retarded", "fag", "faggot"
    ]

    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("Wash your mouth with soap plz")

    valid_users = [
        "charlestang06#0754", "True#7190", "Froggy#4022", "ey#8969",
        "loplkc#7489"
    ]

    user = message.author
    role = discord.utils.get(user.roles, name="studymode")
    if message.content.find(".studymode off") != -1:
        pass
    elif role in message.author.roles:
        channel = await user.create_dm()
        await channel.send(
            f"""Noob go do your work \".studymode off\" to turn this off""")
        await message.channel.purge(limit=1)
        await message.channel.send("do your hw")

    await bot.process_commands(message)


@bot.event
async def on_member_leave(member):
    channel = await member.create_dm()
    await channel.send(
        "Sorry to see you go"
    )
    await member.channel.send(
        f"""{member.nick} betrayed the NSBORO Discord Server since they simped too hard"""
    )


@bot.command()
async def ping(ctx):
    await ctx.send(f"pong. '{round(bot.latency * 1000)}ms")


@bot.command()
async def rules(ctx):
    await ctx.author.send("""RULES
1) Do not shame, bully, harass, attack, threaten, or intentionally provoke other people.
2) No edgy memes, spam (unless in off-topic), large unnecessary spacing, shit-posting, spam pings, or porn.
3) DDOS,  DoX Threats or hacking threats will result in a ban.
4) Please try to keep things on topic, if @Staff  asks you to change channels please do so.
5) Keep a maximum of one Music Bot at a time in each Voice Channel (Octave and Groovy)
6) Keep subject-related conversations or questions to each designated channel
7) Moderators have final say in all situations
8) To change your color, choose your color in the roles channel , if you want a specific hex code, DM any of the Staff for a color role
9) You may invite any students in NSBORO or are former NSBORO students""")


@bot.command()
@commands.has_role('Staff')
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await ctx.send(f"""{member.nick} has been muted""")
    await member.add_roles(role)


@bot.command()
@commands.has_role('Staff')
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await ctx.send(f"""{member.nick} has been unmuted""")
    await member.remove_roles(role)


@bot.command()
@commands.has_role('Staff')
async def purge(ctx, limit: int):
    if limit > 10:
        limit = 10
    await ctx.channel.purge(limit=limit)
    await ctx.send(f"""Purged {limit} messages""")
    await ctx.message.delete()


@bot.command()
@commands.has_role('Staff')
async def warn(ctx, member: discord.Member):
    await ctx.send(
        f"""{member.nick} has been warned. be aware of the mute""")


@bot.command()
@commands.has_role('Staff')
async def tempmute(ctx, member: discord.Member, mute_time: int):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(
        f"""{member.nick} has been temporarily muted for {mute_time} seconds"""
    )
    await asyncio.sleep(mute_time)
    await member.remove_roles(role)
    await ctx.send(
        f"""{member.nick} has been unmuted after {mute_time} seconds""")


@bot.command()
@commands.has_role('Admin')
async def kick(ctx, member: discord.Member, arg):
    await member.kick()
    await ctx.send(f"""{member.nick} was kicked because of {arg}""")


@bot.command()
@commands.has_role('Admin')
async def ban(ctx, member: discord.Member, arg=None):
    valid_users = [
        "charlestang06#0754", "True#7190", "Froggy#4022", "ey#8969",
        "loplkc#7489"
    ]
    if member not in valid_users:
        await member.ban()
        await ctx.send(
            f"""{member.nick} was banned from the NSBORO server because of {arg}"""
        )


@bot.command()
@commands.has_role('Admin')
async def unban(ctx, member: discord.Member, arg=None):
    await member.unban()
    await ctx.send(
        f"""{member.nick} was unbanned from the NSBORO server because of {arg}"""
    )


@bot.command()
@commands.has_role('Staff')
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{user.name} has been giving a role called: {role.name}")


@bot.command()
@commands.has_role('Staff')
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"The role {role.name} was removed from {user.name}")


@bot.command()
@commands.has_role('Staff')
async def addrole(ctx, arg):
    guild = ctx.guild
    await guild.create_role(name=str(arg))
    await ctx.send(f"The {arg} role was created")


@bot.command()
async def basta(ctx):
    random_number = random.randint(1, 7)
    image = f".//pics//Basta{random_number}.png"
    await ctx.send(file=discord.File(image))


@bot.command()
async def spam(ctx, user: discord.Member, *, arg):
    person = bot.get_user(user.id)
    for x in range(5):
        await person.send(arg)


@bot.command()
async def setname(ctx, *, arg):
    user = ctx.author
    if arg == None:
        ctx.send("You need to input your name!")
        return
    name = str(arg)
    list_names = worksheet.get_all_values()
    user_id = str(user.id)
    for i in range(len(list_names)):
        if list_names[i][0] == user_id:
            await ctx.send(
                f"Your name has already been set to {list_names[i][1]}, ask Charles to change it"
            )
            return
    list_names.append([user_id, name])
    list_names = sorted(list_names, key=lambda x: x[1].lower())
    worksheet.update(f'A1:B{len(list_names)}', list_names)
    await ctx.send(f"Your name has sucessfully been set to {name}")

    # sending namelist in member channel
    if bot.get_channel(789896145781391370) == None:
        pass
    else:
        channel = bot.get_channel(789896145781391370)
        await channel.purge(limit=10)
        em = discord.Embed(
            title="Name List",
            description="```List of IRL Names for students on the NSBORO Server.```",
            color=discord.Color.orange())
        em2 = discord.Embed(title="Name List Part 2",
                            description="```Part 2 of list of IRL Names for students on the NSBORO Server.```",
                            color=discord.Color.orange())
        em3 = discord.Embed(title="Name List Part 3",
                            description="```Part 3 of list of IRL Names for students on the NSBORO Server.```",
                            color=discord.Color.orange())
        em4 = discord.Embed(title="Name List Part 4",
                            description="```Part 4 of list of IRL Names for students on the NSBORO Server.```",
                            color=discord.Color.orange())
        em5 = discord.Embed(title="Name List Part 5",
                            description="```Part 5 of list of IRL Names for students on the NSBORO Server.```",
                            color=discord.Color.orange())

        counter = 1

        for x in list_names:
            user = bot.get_user(int(x[0]))
            if user == None: continue
            if counter <= 25:
                em.add_field(name=f"{user}", value=x[1])
            elif counter > 25 and counter <= 50:
                em2.add_field(name=f"{user}", value=x[1])
            elif counter > 50 and counter <= 75:
                em3.add_field(name=f"{user}", value=x[1])
            elif counter > 75 and counter <= 100:
                em4.add_field(name=f"{user}", value=x[1])
            elif counter > 100 <= 125:
                em5.add_field(name=f"{user}", value=x[1])
            counter += 1

        await channel.send(embed=em)
        await channel.send(embed=em2)
        await channel.send(embed=em3)
        await channel.send(embed=em4)
        await channel.send(embed=em5)


@bot.command()
async def getname(ctx, user: discord.User):
    user_id = str(user.id)
    list_names = worksheet.get_all_values()
    for i in range(len(list_names)):
        if user_id == list_names[i][0]:
            await ctx.send(f"{user.name} IRL name is {list_names[i][1]}")
            return
    await ctx.send(f"{user.name} IRL name has not been set")


@bot.command()
@commands.has_role('Staff')
async def changename(ctx, user: discord.User, *, arg):
    user_id = str(user.id)
    list_names = worksheet.get_all_values()

    ifFound = True
    for i in range(len(list_names)):
        if user_id == list_names[i][0]:
            list_names[i][1] = arg
            worksheet.update(f'A1:B{len(list_names)}', list_names)
            await ctx.send(
                f"{user.name} IRL name has been updated to {list_names[i][1]}")
            ifFound = False
    if ifFound == True:
        list_names.append([user_id, arg])
        list_names = sorted(list_names, key=lambda x: x[1].lower())
        worksheet.update(f'A1:B{len(list_names)}', list_names)
        await ctx.send(f"{user.name} IRL name has been set to {arg}")

        # sending namelist in member channel
        if bot.get_channel(789896145781391370) == None:
            pass
        else:
            channel = bot.get_channel(789896145781391370)
            await channel.purge(limit=10)
            em = discord.Embed(
                title="Name List",
                description="```List of IRL Names for students on the NSBORO Server.```",
                color=discord.Color.orange())
            em2 = discord.Embed(title="Name List Part 2",
                                description="```Part 2 of list of IRL Names for students on the NSBORO Server.```",
                                color=discord.Color.orange())
            em3 = discord.Embed(title="Name List Part 3",
                                description="```Part 3 of list of IRL Names for students on the NSBORO Server.```",
                                color=discord.Color.orange())
            em4 = discord.Embed(title="Name List Part 4",
                                description="```Part 4 of list of IRL Names for students on the NSBORO Server.```",
                                color=discord.Color.orange())
            em5 = discord.Embed(title="Name List Part 5",
                                description="```Part 5 of list of IRL Names for students on the NSBORO Server.```",
                                color=discord.Color.orange())

            counter = 1

            for x in list_names:
                user = bot.get_user(int(x[0]))
                if user == None: continue
                if counter <= 25:
                    em.add_field(name=f"{user}", value=x[1])
                elif counter > 25 and counter <= 50:
                    em2.add_field(name=f"{user}", value=x[1])
                elif counter > 50 and counter <= 75:
                    em3.add_field(name=f"{user}", value=x[1])
                elif counter > 75 and counter <= 100:
                    em4.add_field(name=f"{user}", value=x[1])
                elif counter > 100 <= 125:
                    em5.add_field(name=f"{user}", value=x[1])
                counter += 1

            await channel.send(embed=em)
            await channel.send(embed=em2)
            await channel.send(embed=em3)
            await channel.send(embed=em4)
            await channel.send(embed=em5)


@bot.command()
@commands.has_role('Staff')
async def namelist(ctx):
    list_names = worksheet.get_all_values()
    list_names = sorted(list_names, key=lambda x: x[1].lower())
    em = discord.Embed(
        title="Name List",
        description="```List of IRL Names for students on the NSBORO Server.```",
        color=discord.Color.orange())
    em2 = discord.Embed(title="Name List Part 2",
                        description="```Part 2 of list of IRL Names for students on the NSBORO Server.```",
                        color=discord.Color.orange())
    em3 = discord.Embed(title="Name List Part 3",
                        description="```Part 3 of list of IRL Names for students on the NSBORO Server.```",
                        color=discord.Color.orange())
    em4 = discord.Embed(title="Name List Part 4",
                        description="```Part 4 of list of IRL Names for students on the NSBORO Server.```",
                        color=discord.Color.orange())
    em5 = discord.Embed(title="Name List Part 5",
                        description="```Part 5 of list of IRL Names for students on the NSBORO Server.```",
                        color=discord.Color.orange())

    counter = 1
    for x in list_names:
        user = bot.get_user(int(x[0]))
        if user == None: continue
        if counter <= 25:
            em.add_field(name=f"{user}", value=x[1])
        elif counter > 25 and counter <= 50:
            em2.add_field(name=f"{user}", value=x[1])
        elif counter > 50 and counter <= 75:
            em3.add_field(name=f"{user}", value=x[1])
        elif counter > 75 and counter <= 100:
            em4.add_field(name=f"{user}", value=x[1])
        elif counter > 100 <= 125:
            em5.add_field(name=f"{user}", value=x[1])
        counter += 1

    await ctx.send(embed=em)
    await ctx.send(embed=em2)
    await ctx.send(embed=em3)
    await ctx.send(embed=em4)
    await ctx.send(embed=em5)


@bot.command()
async def getUID(ctx, user: discord.User):
    user_id = str(user.id)
    list_UIDs = worksheet2.get_all_values()
    for i in range(len(list_UIDs)):
        if user_id == list_UIDs[i][0]:
            await ctx.send(f"{user.name} genshin UID is {list_UIDs[i][1]}")
            return
    await ctx.send(f"{user.name} genshin UID name has not been set")


@bot.command()
async def setUID(ctx, arg):
    user = ctx.author
    if arg == None:
        ctx.send("You need to input your UID!")
        return
    uid = str(arg)
    list_UIDs = worksheet2.get_all_values()
    user_id = str(user.id)
    for i in range(len(list_UIDs)):
        if list_UIDs[i][0] == user_id:
            await ctx.send(
                f"Your UID has already been set to {list_UIDs[i][1]}, ask Charles to change it"
            )
            return
    list_UIDs.append([user_id, uid])
    worksheet2.update(f'A1:B{len(list_UIDs)}', list_UIDs)
    await ctx.send(f"Your name has sucessfully been set to {uid}")


@bot.command()
async def stats(ctx):
    member_count = len(ctx.guild.members)  # includes bots
    true_member_count = len([m for m in ctx.guild.members if not m.bot])  # doesn't include bots
    await ctx.send(f"""NSBORO Discord Server Stats: \n {true_member_count} students""")


@bot.command()
async def studymode(ctx, arg):
    if arg == 'on':
        user = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name="studymode")
        if role in ctx.author.roles:
            await ctx.send("You are already on studymode")
        else:
            await user.add_roles(role)
            await ctx.send(f"""studymode is turned on for {user.mention}""")
    elif arg == 'off':
        user = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name="studymode")
        if role in ctx.author.roles:
            await user.remove_roles(role)
            await ctx.send(f"""studymode is turned off for {user.mention}""")
        else:
            await ctx.send("You are not on studymode")
    else:
        await ctx.send(
            "The studymode commands accepts arguments **[on]/[off]**")


@bot.command()
async def color(ctx, arg, arg2=None):
    user = ctx.author
    guild = ctx.guild
    if arg2 == None:
        if get(ctx.guild.roles, name=str(arg)):
            await user.add_roles(get(ctx.guild.roles, name=str(arg)))
            await ctx.send(f"{user.name} has been given a role called: {arg}")
        else:
            if len(arg) == 6:
                await guild.create_role(name=str(arg),
                                        color=discord.Color(int(arg, 16)))
                await ctx.send(f"The {arg} role was created")
                await user.add_roles(get(ctx.guild.roles, name=str(arg)))
                await ctx.send(
                    f"{user.name} has been given a role called: {arg}")
            else:
                await ctx.send(
                    f"{str(arg)} is not a HEX code, please try the command again with a hex code"
                )
    elif arg2.lower() == 'remove':
        if len(arg) == 6:
            await user.remove_roles(get(ctx.guild.roles, name=str(arg)))
            await ctx.send(f"{arg} was removed from {user.name}")
        else:
            await ctx.send(
                f"{str(arg)} is not a HEX code, please try the command again with a hex code"
            )


@bot.command()
async def invite(ctx):
    await ctx.send("https://discord.gg/Ksb296M")


@bot.command()
async def report(ctx, *, arg):
    if bot.get_channel(771888680083652628) == None:
        return
    else:
        channel = bot.get_channel(771888680083652628)
        author = ctx.message.author
        await channel.send(f"""{author.name} reported {arg}""")
    user = bot.get_user(530569044185579521)
    await user.send(f"""{author.name} reported {arg}""")


@bot.command()
@commands.has_role('Staff')
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"""Set the slowmode delay in this channel to {seconds} seconds!""")


@bot.command()
async def bal(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    await open_account(member)
    user = member
    users = await get_bank_data()
    bank_amt = users[str(user.id)]["bank"]
    em = discord.Embed(title=f"{member.name}'s bank ")
    em.add_field(name="Bank balance (coins)", value=bank_amt)
    await ctx.send(embed=em)


@bot.command()
async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        pass
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["bank"] = 0
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


@bot.command()
async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users


@bot.command()
async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(101)
    await ctx.send(f"Basta blesses you {earnings} coins")
    users[str(user.id)]["bank"] += earnings
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@bot.command()
async def pray(ctx, arg=None):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    if arg == None:
        earnings = random.randrange(500)
        await ctx.send(f"Charles gives thy peasant {earnings} coins")
    elif arg.lower() == 'basta':
        earnings = random.randrange(1000)
        await ctx.send(f"Basta blesses you {earnings} coins")
    elif arg.lower() == 'steven':
        earnings = random.randrange(2000)
        await ctx.send(f"Steven blesses you {earnings} coins")
    else:
        await ctx.send("Noob you can only pray to basta or steven")
    users[str(user.id)]["bank"] += earnings
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@bot.command()
async def lottery(ctx, arg):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    amt = int(arg) * 100
    random_user_number = random.randint(0, 25)
    random_bot_number = random.randint(0, 25)
    if random_user_number == random_bot_number:
        await ctx.send(
            f"You won the lottery for {amt}! The lottery number was {random_bot_number}. You drew {random_user_number}"
        )
        users[str(user.id)]["bank"] += amt
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
    else:
        users[str(user.id)]["bank"] -= int(arg)
        await ctx.send(
            f"so sad you didn't win the lottery. The lottery number was {random_bot_number}. You drew {random_user_number}. You wasted {int(arg)} coins"
        )
        with open("mainbank.json", "w") as f:
            json.dump(users, f)


@bot.command()
async def give(ctx, member: discord.Member, arg):
    amt = arg
    user = ctx.author
    receiver = member
    await open_account(member)
    await open_account(discord.Member)
    users = await get_bank_data()
    if users[str(user.id)]["bank"] - int(amt) < 0:
        await ctx.send("Noob you are broke and cannot give that much")
    else:
        users[str(user.id)]["bank"] -= int(amt)
        users[str(receiver.id)]["bank"] += int(amt)
        await ctx.send(f"You generoused {amt} to {member.name}")
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@bot.command()
async def rob(ctx, member: discord.Member):
    user = ctx.author
    person = member
    if member == ctx.author:
        await ctx.send(f"Noob you can't rob yourself")
    else:
        await open_account(member)
        await open_account(user)
        users = await get_bank_data()
        probability = random.randint(1, 6)
        happened = random.randint(1, 6)
        if probability == happened:
            amt = random.randint(0, int(users[str(person.id)]["bank"] / 8))
            users[str(person.id)]["bank"] -= amt
            users[str(user.id)]["bank"] += amt
            await ctx.send(f"You stole {amt} from {member.name}")
        else:
            amt_2 = random.randint(1, int(users[str(user.id)]["bank"] / 12))
            users[str(person.id)]["bank"] += amt_2
            users[str(user.id)]["bank"] -= amt_2
            await ctx.send(
                f"You failed to steal from {member.name}. You paid {amt_2} to {member.name}"
            )

        with open("mainbank.json", "w") as f:
            json.dump(users, f)


@bot.command()
async def fight(ctx, member: discord.Member):
    statements = [f"{ctx.author} beat {member} into pulp",
                  f"{ctx.author} used Self Destruct! It was not very effective...",
                  f"{ctx.author} was too much for {member}",
                  f"{member} was ended by {ctx.author}",
                  f"{member} was mauled by {ctx.author}'s hydroflask",
                  f"{ctx.author}'s mixtape was too fire for {member}",
                  f"{ctx.author} vaporized {member} using their unlimited stupidity",
                  f"{member} fainted due to {ctx.author}'s lack of braincells",
                  f"{member} was betrayed by {ctx.author}"
                  ]
    await ctx.send(statements[random.randint(0, 8)])


@bot.command()
async def kill(ctx, member: discord.Member):
    statements = [
        f"{ctx.author} obliterated {member} in fortnite",
        f"{ctx.author} juiced the insides of {member} out",
        f"{ctx.author} rhone moaned {member} while trying to throb",
        f"{ctx.author} succed {member}'s ducc",
        f"{ctx.author} let dan absolutely destroy {member}'s ducc",
        f"{member} was smited by God",
        f"{member} was eviscerated by a tree",
        f"{member} was pricked to death",
        f"{member} stared at the Sun for too long",
        f"{ctx.author} was stabbed in the chest, but took it out and killed {member}",
        f"{member} thinks about suicide, however, they call 800-273-8255 and get help from a professional",
        f"{member} was slaughtered by hungry puppies in a bucket.",
        f"{member} listened to death metal at max volume",
        f"{member} was assassinated while on a date with {ctx.author}",
        f"{member} tried to defuse a bomb. It wasn't the red wire",
        f"{member} challenged Goku to a duel",
        f"{member} was Haydened",
        f"{ctx.author} figured out what the liquefy tool in Photoshop was. {member} was their first test subject",
        f"{ctx.author} used {member} as a shield in a gunfight",
        f"{member} went on https://reddit.com/r/rule34fallguys"
    ]
    await ctx.send(statements[random.randint(0, len(statements) - 1)])


@bot.command()
async def KYT(ctx):
    user = bot.get_user(535314077329784854)
    await ctx.send(f"{user.mention} ping!")
    await user.send("Kevin Yao is the coolest class president ever")
    await user.send(file=discord.File('.//pics//KYT1.jpeg'))
    await user.send(file=discord.File('.//pics//KYT2.jpg'))


@bot.command()
async def androne(ctx, *, arg=None):
    if arg == None:
        await ctx.send(file=discord.File('.//pics//Androne.png'))
    else:
        user = bot.get_user(541427575818551297)
        await ctx.send(file=discord.File('.//pics//Androne.png'))
        await user.send(f"AndroneZ for Treasurer! Your supporters said {arg}")
        await ctx.send(f"{arg} sent to Androne")


@bot.command()
async def tax(ctx, member: discord.Member):
    user = ctx.author
    await open_account(member)
    await open_account(user)
    users = await get_bank_data()
    if int(users[str(member.id)]["bank"]) > 10000:
        taxed = int(.1 * int(users[str(member.id)]["bank"]))
        users[str(member.id)]["bank"] -= taxed
        await ctx.send(
            f"omar says eat the rich so {member} got heavily taxed {taxed} coins"
        )
    elif int(users[str(member.id)]["bank"]) < 10000:
        await ctx.send(f"{member} is a peasant and is too broke to be taxed")
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@bot.command()
@commands.has_role('Admin')
async def punish(ctx, member: discord.Member):
    user = ctx.author
    await open_account(member)
    users = await get_bank_data()
    smited = int(.5 * int(users[str(member.id)]["bank"]))
    amt = users[str(member.id)]["bank"]
    users[str(member.id)]["bank"] -= smited
    await ctx.send(
        f"{member.mention} was punished by charly, his wealth got cut by half")
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@bot.command()
@commands.has_role('Admin')
async def reset(ctx, member: discord.Member):
    user = ctx.author
    await open_account(member)
    users = await get_bank_data()
    users[str(member.id)]["bank"] = 69
    index = 0
    for x in users[str(member.id)]["bag"]:
        if users[str(member.id)]["bag"][index]["amount"] > 1000:
            users[str(member.id)]["bag"][index]["amount"] = 1000
        index += 1
    await ctx.send(f"{member.name}'s wealth was eaten by omar")
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@bot.command()
async def slots(ctx, arg):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    if arg == None:
        await ctx.send("Please enter the amount")
        return
    amt = int(arg)
    if amt > int(users[str(user.id)]["bank"]):
        await ctx.send("You don't have that much money you broke peasant!")
        return
    if amt < 0:
        await ctx.send("Amount must be positive nerd")
    final = []
    for i in range(3):
        a = random.choice([
            '<:basta:722590619683258479>', '<:basta2:771810393014272051>',
            '<:rhone:695277725300162579>', '<:charlespog:703737266211782768>',
            '<:emoji_25:699610131784269885>', '<:mazzu:707006025970221137>',
            '<:andrewbeeheart:772280878298300416>',
            '<:sansduck:692377832965406732>',
            '<:andrewmurder:772471054114750495>',
            '<:pogomega:766465414636109848>'
        ])
        final.append(a)
    await ctx.send(str(final))
    if final[0] == final[1] == final[2]:
        users[str(user.id)]["bank"] += 5 * amt
        await ctx.send(f"You matched three slots! You earned {str(5 * amt)}!")
    elif final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        users[str(user.id)]["bank"] += 3 * amt
        await ctx.send(f"You matched two slots! You earned {str(3 * amt)}!")
    else:
        users[str(user.id)]["bank"] -= amt
        await ctx.send(
            f"You did not match any slots! You lost {str(amt)} coins!")
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@bot.command()
async def shop(ctx):
    em = discord.Embed(title="NSBORO Discord Bot Shop", description="```All items you can buy from the shop```")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        description = item["description"]
        em.add_field(name=name, value=f"""${price} | {description}""")

    await ctx.send(embed=em)


@bot.command()
async def buy(ctx, item, amount=1):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    item = item.lower()

    for each in mainshop:
        name = each["name"].lower()
        if name == item:
            price = each["price"]
            bal = users[str(user.id)]["bank"]
            cost = price * amount
            if bal < cost:
                await ctx.send(
                    f"You're a broke peasant, get more money before buying this"
                )
                break
            elif bal >= cost:
                users[str(user.id)]["bank"] -= cost
                await ctx.send(
                    f"You purchased {amount} {name} for {cost} coins")
                try:
                    index = 0
                    t = None
                    for thing in users[str(user.id)]["bag"]:
                        n = thing["item"]
                        if n == name:
                            old_amt = thing["amount"]
                            new_amt = old_amt + amount
                            users[str(
                                user.id)]["bag"][index]["amount"] = new_amt
                            t = 1
                            break
                        index += 1
                    if t == None:
                        obj = {"item": name, "amount": amount}
                        users[str(user.id)]["bag"].append(obj)
                except:
                    obj = {"item": name, "amount": amount}
                    users[str(user.id)]["bag"] = [obj]
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@bot.command()
async def sell(ctx, item, amount=1):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    item = item.lower()
    for each in mainshop:
        name = each["name"].lower()
        if name == item:
            price = each["price"]
            bal = users[str(user.id)]["bank"]
            cost = price * amount
            index = 0
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item:
                    old_amt = int(thing["amount"])
                    new_amt = old_amt - amount
                    if new_amt < 0:
                        await ctx.send(
                            "You cannot sell more than you have")
                        break
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    users[str(user.id)]["bank"] += cost
                    await ctx.send(
                        f"You sold {amount} {item} and earned {cost} coins")
                index += 1
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@bot.command()
async def bag(ctx, member: discord.Member = None):
    if member == None:
        user = ctx.author
        await open_account(user)
        users = await get_bank_data()
        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []
        em = discord.Embed(
            title=f"{ctx.author}'s Bag",
            description=
            "```Your bag contains items you buy from the NSBORO bot shop```")
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            em.add_field(name=name, value=amount)
        await ctx.send(embed=em)
    else:
        await open_account(member)
        user = member
        users = await get_bank_data()
        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []
        em = discord.Embed(
            title=f"{member}'s Bag",
            description=
            "Your bag contains items you buy from the NSBORO bot shop")
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            em.add_field(name=name, value=amount)
        await ctx.send(embed=em)


@bot.command()
async def use(ctx, item):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    item = item.lower()
    index = 0
    try:
        for x in users[str(user.id)]["bag"]:
            n = x["item"]
            if n == item:
                for each in mainshop:
                    name = each["name"].lower()
                    if name == item:
                        if int(users[str(
                                user.id)]["bag"][index]["amount"]) == 0:
                            await ctx.send(
                                "Noob you cannot use more than you have")
                            break
                        if name == 'stock':
                            await ctx.send(each["use"])
                            break
                        users[str(user.id)]["bag"][index]["amount"] -= 1
                        await ctx.send(each["use"])
                        if name == 'indentured_servant':
                            users[str(user.id)]["bank"] += 100
                        if name == 'steven_prayer':
                            users[str(user.id)]["bank"] += 1000
                        with open("mainbank.json", "w") as f:
                            json.dump(users, f)
                        break
            index += 1
    except:
        await ctx.send("Noob you do not have this item")


@bot.command()
async def stock(ctx):
    for x in mainshop:
        name = x["name"]
        if name == 'stock':
            await ctx.send(f"The stock is trading at ${x['price']} per share")


@bot.command()
async def panda(ctx):
    random_number = random.randint(1, 7)
    if random_number == 1:
        await ctx.send(file=discord.File('.//pics//panda1.png'))
    if random_number == 2:
        await ctx.send(file=discord.File('.//pics//panda2.png'))
    if random_number == 3:
        await ctx.send(file=discord.File('.//pics//panda3.png'))
    if random_number == 4:
        await ctx.send(file=discord.File('.//pics//panda4.png'))
    if random_number == 5:
        await ctx.send(file=discord.File('.//pics//panda5.png'))
    if random_number == 6:
        await ctx.send(file=discord.File('.//pics//panda6.png'))
    if random_number == 7:
        await ctx.send(file=discord.File('.//pics//panda7.png'))


@bot.command()
async def schedule(ctx, arg1, arg2, arg3, arg4, arg5, arg6, arg7):
    new_schedule = periods[:]

    # assign
    new_schedule[0] = arg1
    new_schedule[1] = arg2
    new_schedule[2] = arg3
    new_schedule[3] = arg4
    new_schedule[4] = arg5
    new_schedule[5] = arg6
    new_schedule[6] = arg7
    # image stuff
    im1 = Image.open("schedule template.PNG")

    im2 = im1.copy()

    image_editable = ImageDraw.Draw(im2)

    # txtfont = ImageFont.truetype("arial.ttf", 25)
    txtfont = ImageFont.truetype("DejaVuSansMono-Bold.ttf", 16)

    # period 1
    image_editable.text((100, 100),
                        new_schedule[0] + "\n8:00-9:00 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((325, 180),
                        new_schedule[0] + "\n8:50-9:30 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((540, 100),
                        new_schedule[0] + "\n8:00-9:00 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((750, 180),
                        new_schedule[0] + "\n8:50-9:30 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((970, 83),
                        new_schedule[0] + "\n8:00-8:45 AM", (255, 255, 255),
                        font=txtfont)

    # period 2
    image_editable.text((100, 215),
                        new_schedule[1] + "\n9:05-10:00 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((325, 85),
                        new_schedule[1] + "\n8:00-8:45 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((540, 215),
                        new_schedule[1] + "\n9:05-10:00 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((750, 85),
                        new_schedule[1] + "\n8:00-8:45 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((970, 175),
                        new_schedule[1] + "\n8:50-9:30 AM", (255, 255, 255),
                        font=txtfont)

    # period 3
    image_editable.text((100, 325),
                        new_schedule[2] + "\n10:05-10:45 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((325, 775),
                        new_schedule[2] + "\n1:50-2:30 PM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((540, 688),
                        new_schedule[2] + "\n1:05-1:45 PM", (255, 255, 255),
                        font=txtfont)
    image_editable.text(
        (750, 510),
        new_schedule[2] +
        "\n11:35 AM-1:00 PM\n1: 11:35-12:00 PM \n2: 12:05-12:30 PM \n3: 12:35-1:00 PM",
        (255, 255, 255),
        font=txtfont)
    image_editable.text((970, 400),
                        new_schedule[2] + "\n10:30-11:30 AM", (255, 255, 255),
                        font=txtfont)

    # period 4
    image_editable.text((100, 420),
                        new_schedule[3] + "\n10:50-11:30 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((325, 275),
                        new_schedule[3] + "\n9:35-10:25 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((540, 775),
                        new_schedule[3] + "\n1:50-2:30 PM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((750, 688),
                        new_schedule[3] + "\n1:05-1:45 PM", (255, 255, 255),
                        font=txtfont)
    image_editable.text(
        (970, 510),
        new_schedule[3] +
        "\n11:35 AM-1:00 PM\n1: 11:35-12:00 PM \n2: 12:05-12:30 PM \n3: 12:35-1:00 PM",
        (255, 255, 255),
        font=txtfont)

    # period 5 + lunch
    image_editable.text(
        (100, 510),
        new_schedule[4] +
        "\n11:35 AM-1:00 PM\n1: 11:35-12:00 PM \n2: 12:05-12:30 PM \n3: 12:35-1:00 PM",
        (255, 255, 255),
        font=txtfont)
    image_editable.text((325, 390),
                        new_schedule[4] + "\n10:30-11:30 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((540, 325),
                        new_schedule[4] + "\n10:05-10:45 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((750, 775),
                        new_schedule[4] + "\n1:50-2:30 PM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((970, 688),
                        new_schedule[4] + "\n1:05-1:45 PM", (255, 255, 255),
                        font=txtfont)

    # period 6
    image_editable.text((100, 688),
                        new_schedule[5] + "\n1:05-1:45 PM", (255, 255, 255),
                        font=txtfont)
    image_editable.text(
        (315, 510),
        new_schedule[5] +
        "\n11:35 AM-1:00 PM\n1: 11:35-12:00 PM \n2: 12:05-12:30 PM \n3: 12:35-1:00 PM",
        (255, 255, 255),
        font=txtfont)
    image_editable.text((540, 420),
                        new_schedule[5] + "\n10:50-11:30 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((750, 275),
                        new_schedule[5] + "\n9:35-10:30 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((970, 775),
                        new_schedule[5] + "\n1:50-2:30 PM", (255, 255, 255),
                        font=txtfont)

    # period 7
    image_editable.text((100, 775),
                        new_schedule[6] + "\n1:50-2:30 PM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((325, 688),
                        new_schedule[6] + "\n1:05-1:45 PM", (255, 255, 255),
                        font=txtfont)
    image_editable.text(
        (540, 510),
        new_schedule[6] +
        "\n11:35 AM-1:00 PM\n1: 11:35-12:00 PM \n2: 12:05-12:30 PM \n3: 12:35-1:00 PM",
        (255, 255, 255),
        font=txtfont)
    image_editable.text((750, 390),
                        new_schedule[6] + "\n10:35-11:30 AM", (255, 255, 255),
                        font=txtfont)
    image_editable.text((970, 275),
                        new_schedule[6] + "\n9:35-10:25 AM", (255, 255, 255),
                        font=txtfont)

    im2 = im2.save(f".//schedules//{ctx.author.id}.png")
    await ctx.send(file=discord.File(f".//schedules//{ctx.author.id}.png"))

    user_id = str(ctx.author.id)
    list_classes = worksheet3.get_all_values()
    ifFound = False
    for i in range(len(list_classes)):
        if user_id == list_classes[i][0]:
            list_classes[i][1:] = [arg1, arg2, arg3, arg4, arg5, arg6, arg7]
            worksheet3.update(f'A1:H{len(list_classes)}', list_classes)
            await ctx.send(f"{ctx.author.name} schedule has been updated")
            ifFound = True
    if ifFound == False:
        list_classes.append(
            [user_id, arg1, arg2, arg3, arg4, arg5, arg6, arg7])
        worksheet3.update(f'A1:H{len(list_classes)}', list_classes)
        await ctx.send(f"{ctx.author.name}'s schedule has been set")


@bot.command()
async def viewschedule(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    userID = user.id

    try:
        f = open(f".//schedules/{userID}.png")
        await ctx.send(file=discord.File(f".//schedules/{userID}.png"))
    except IOError:
        await ctx.send(
            f"{user.mention} did not create a schedule yet, use .schedule or .help schedule to learn more about the command"
        )


@bot.command()
async def clubs(ctx):
    em = discord.Embed(title="ARHS Clubs on NSBORO Bot",
                       description="Some clubs at gonk that are pretty cool",
                       color=discord.Color.orange())

    em.add_field(
        name="Programming Club",
        value=
        "Thursdays after school @ D111 (Forhan) \n https://discord.gg/HEzFX8VD7F \n https://nsboro.instructure.com/enroll/WP3LEW"
    )

    em.add_field(
        name="Asia Club",
        value=
        "Wednesdays after school @ H207 (Frantz) \n https://discord.gg/DRX6jw8g2T"
    )

    em.add_field(
        name="Varsity Math Team",
        value="Tuesdays @ 7:10am @ \n Email Mrs.Dore edore@nsboro.k12.ma.us")

    await ctx.send(embed=em)


@bot.command()
@commands.has_role('Staff')
async def announce(ctx, *, arg):
    channel = bot.get_channel(685975002683539569)
    msg = await channel.send(arg)
    await msg.publish()


@bot.command()
async def covid(ctx):
    await ctx.send(file=discord.File(".//ss.png"))


@bot.group(invoke_without_command=True)
async def getclass(ctx, user: discord.Member = None):
    list_classes = worksheet3.get_all_values()
    if user == None:
        user = ctx.author
    userID = user.id

    ifFound = False

    for i in range(len(list_classes)):
        if list_classes[i][0] == str(user.id):
            classes = list_classes[i][1:]
            ifFound = True
            break

    if ifFound == False:
        await ctx.send(
            f"{user.mention} has not set their schedule yet using .schedule")
    else:
        periods = [[1, 2, 3, 4, 5, 6, 7], [2, 1, 4, 5, 6, 7, 3],
                   [1, 2, 5, 6, 7, 3, 4], [2, 1, 6, 7, 2, 3, 4, 5],
                   [1, 2, 7, 3, 4, 5, 6]]

        timeEnd = [[540, 600, 645, 690, 780, 825, 870],
                   [525, 570, 625, 690, 780, 825, 870],
                   [540, 600, 645, 690, 780, 825, 870],
                   [525, 570, 630, 690, 780, 825, 870],
                   [525, 570, 625, 690, 780, 825, 870]]

        now = datetime.now().time()
        currentDay = datetime.today().weekday()
        if currentDay in [5, 6]:
            await ctx.send("Today is a weekend")
            return
        hour = int(now.strftime("%H")) - 4 - 1
        if hour < 0:
            hour = 24 - hour
        currentMin = hour * 60 + int(now.strftime("%M"))
        currentPeriod = f"Not in school"

        for i in range(len(timeEnd[currentDay])):
            if currentMin < timeEnd[currentDay][i] and currentMin > 480:
                currentPeriod = classes[periods[currentDay][i] - 1]
                break

        em = discord.Embed(title=f"{user.name} Class",
                           description=currentPeriod,
                           color=discord.Color.orange())

        await ctx.send(embed=em)


@getclass.command()
async def next(ctx, user: discord.Member = None):
    list_classes = worksheet3.get_all_values()
    if user == None:
        user = ctx.author
    userID = user.id

    ifFound = False

    for i in range(len(list_classes)):
        if list_classes[i][0] == str(user.id):
            classes = list_classes[i][1:]
            ifFound = True
            break

    if ifFound == False:
        await ctx.send(
            f"{user.mention} has not set their schedule yet using .schedule")
    else:
        periods = [[1, 2, 3, 4, 5, 6, 7], [2, 1, 4, 5, 6, 7, 3],
                   [1, 2, 5, 6, 7, 3, 4], [2, 1, 6, 7, 2, 3, 4, 5],
                   [1, 2, 7, 3, 4, 5, 6]]

        timeEnd = [[540, 600, 645, 690, 780, 825, 870],
                   [525, 570, 625, 690, 780, 825, 870],
                   [540, 600, 645, 690, 780, 825, 870],
                   [525, 570, 630, 690, 780, 825, 870],
                   [525, 570, 625, 690, 780, 825, 870]]

        now = datetime.now().time()
        currentDay = datetime.today().weekday()
        if currentDay in [5, 6]:
            await ctx.send("Today is a weekend")
            return
        hour = int(now.strftime("%H")) - 4 - 1
        if hour < 0:
            hour = 24 - hour
        currentMin = hour * 60 + int(now.strftime("%M"))
        currentPeriod = f"Not in school"

        for i in range(len(timeEnd[currentDay])):
            if currentMin < timeEnd[currentDay][i] and currentMin > 480:
                if i == 6:
                    currentPeriod = "Done with school after this period!"
                else:
                    currentPeriod = classes[periods[currentDay][i + 1] - 1]
                    break

        em = discord.Embed(title=f"{user.name} Next Class",
                           description=currentPeriod,
                           color=discord.Color.orange())

        await ctx.send(embed=em)


@bot.group(invoke_without_command=True)
async def period(ctx):
    periods = [[1, 2, 3, 4, 5, 6, 7], [2, 1, 4, 5, 6, 7, 3],
               [1, 2, 5, 6, 7, 3, 4], [2, 1, 6, 7, 2, 3, 4, 5],
               [1, 2, 7, 3, 4, 5, 6]]

    timeEnd = [[540, 600, 645, 690, 780, 825, 870],
               [525, 570, 625, 690, 780, 825, 870],
               [540, 600, 645, 690, 780, 825, 870],
               [525, 570, 630, 690, 780, 825, 870],
               [525, 570, 625, 690, 780, 825, 870]]

    now = datetime.now().time()
    currentDay = datetime.today().weekday()
    if currentDay in [5, 6]:
        await ctx.send("Today is a weekend")
        return
    hour = int(now.strftime("%H")) - 4 - 1
    if hour < 0:
        hour = 24 - hour
    currentMin = hour * 60 + int(now.strftime("%M"))
    currentPeriod = f"Not in school"

    for i in range(len(timeEnd[currentDay])):
        if currentMin < timeEnd[currentDay][i] and currentMin > 480:
            currentPeriod = str(periods[currentDay][i])
            break

    em = discord.Embed(title="Period",
                       description=currentPeriod,
                       color=discord.Color.orange())

    await ctx.send(embed=em)


@period.command()
async def next(ctx):
    periods = [[1, 2, 3, 4, 5, 6, 7], [2, 1, 4, 5, 6, 7, 3],
               [1, 2, 5, 6, 7, 3, 4], [2, 1, 6, 7, 2, 3, 4, 5],
               [1, 2, 7, 3, 4, 5, 6]]

    timeEnd = [[540, 600, 645, 690, 780, 825, 870],
               [525, 570, 625, 690, 780, 825, 870],
               [540, 600, 645, 690, 780, 825, 870],
               [525, 570, 630, 690, 780, 825, 870],
               [525, 570, 625, 690, 780, 825, 870]]

    now = datetime.now().time()
    currentDay = datetime.today().weekday()
    if currentDay in [5, 6]:
        await ctx.send("Today is a weekend")
        return
    hour = int(now.strftime("%H")) - 4 - 1
    if hour < 0:
        hour = 24 - hour
    currentMin = hour * 60 + int(now.strftime("%M"))
    currentPeriod = f"Not in school"

    for i in range(len(timeEnd[currentDay])):
        if currentMin < timeEnd[currentDay][i] and currentMin > 480:
            if i == 6:
                currentPeriod = "Done with school after this period!"
            else:
                currentPeriod = str(periods[currentDay][i + 1])
            break

    em = discord.Embed(title="Period",
                       description=currentPeriod,
                       color=discord.Color.orange())

    await ctx.send(embed=em)


@bot.group(invoke_without_command=True)
async def hw(ctx):
    list_hw = worksheet4.get_all_values()
    em = discord.Embed(
        title=f"{ctx.author}'s Homework",
        description=f"```{ctx.author}'s homework for the day of {date.today()}```",
        color=discord.Color.orange())
    found = False
    for i in range(len(list_hw)):
        if list_hw[i][0] == str(ctx.author.id):
            found = True
            if len(list_hw[i]) <= 1:
                await ctx.send("You have nothing to do!")
                return
            else:
                for j in range(1, len(list_hw[i][1:]) + 1):
                    if list_hw[i][j] == '':
                        continue
                    em.add_field(name=f"Task {j}", value=list_hw[i][j])
            break
    if found == False:
        await ctx.send("You have no homework to do!")
    else:
        await ctx.send(embed=em)


@hw.command()
async def add(ctx, *, args):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    list_hw = worksheet4.get_all_values()
    found = False
    found2 = False
    for i in range(len(list_hw)):
        if list_hw[i][0] == str(ctx.author.id):
            found = True
            if i >= 26:
                await ctx.send("You have exceeded the number of total tasks")
                return
            for j in range(1, len(list_hw[i])):
                if list_hw[i][j] == '':
                    list_hw[i][j] = args
                    found2 = True
                    break
            if found2 == False:
                list_hw[i].append(args)
            await ctx.send(f"Task: `{args}` added to your homework list")
            break
    if found == False:
        list_hw.append([str(ctx.author.id), args])
        await ctx.send(f"Task: {args} added to your homework list")
    worksheet4.update(f'A1:{alphabet[len(list_hw[0]) - 1].upper()}{len(list_hw)}', list_hw)


@hw.command()
async def remove(ctx, arg):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    list_hw = worksheet4.get_all_values()
    arg = int(arg)
    found = False
    if arg == 0:
        await ctx.send("Task 0 is not a thing!")
        return
    for i in range(len(list_hw)):
        if list_hw[i][0] == str(ctx.author.id):
            found = True
            if len(list_hw[i]) <= arg:
                await ctx.send("You do not have that many tasks!")
                return
            await ctx.send(f"Task: `{list_hw[i][arg]}` removed from your homework list")
            list_hw[i].pop(arg)
            runningMax = 0
            for person in list_hw:
                runningMax = max(runningMax, len(person))
            worksheet4.clear()
            worksheet4.update(f'A1:{alphabet[len(list_hw[0]) - 1].upper()}{len(list_hw)}', list_hw)

    if found == False:
        await ctx.send(f"You do not have any homework!")


@hw.command()
async def change(ctx, arg1, *, arg2):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    list_hw = worksheet4.get_all_values()
    arg1 = int(arg1)
    found = False
    if arg1 == 0:
        await ctx.send("Task 0 is not a thing!")
        return
    for i in range(len(list_hw)):
        if list_hw[i][0] == str(ctx.author.id):
            found = True
            if len(list_hw[i]) <= arg1:
                await ctx.send("You do not have that many tasks!")
                return
            await ctx.send(f"Task: `{list_hw[i][arg1]}` changed to `{arg2}` on your homework list")
            list_hw[i][arg1] = arg2
            worksheet4.clear()
            worksheet4.update(f'A1:{alphabet[len(list_hw[0]) - 1].upper()}{len(list_hw)}', list_hw)
    if found == False:
        await ctx.send(f"You do not have any homework!")


@hw.command()
async def clear(ctx):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    list_hw = worksheet4.get_all_values()
    for i in range(len(list_hw)):
        if list_hw[i][0] == str(ctx.author.id):
            found = True
            list_hw[i] = [str(ctx.author.id)]
            runningMax = 0
            for person in list_hw:
                runningMax = max(runningMax, len(person))
            worksheet4.clear()
            worksheet4.update(f'A1:{alphabet[runningMax - 1].upper()}{len(list_hw)}', list_hw)
            await ctx.send("All homework marked as done!")

    if found == False:
        await ctx.send(f"You don't have any homework!")


@bot.group(invoke_without_command=True)
async def translate(ctx, toLang, *, args):
    translator = Translator()
    translation = translator.translate(args, dest=toLang)
    em = discord.Embed(
        title="NSBORO Bot Translater",
        description=f"{translation.origin} ({translation.src})",
        color=0xe91e63
    )
    em.add_field(name="**Translation**", value=f"{translation.text} ({translation.dest})")
    await ctx.send(embed=em)


@translate.command()
async def codes(ctx):
    em = discord.Embed(
        title="NSBORO Bot Translater Language Codes Pt. 1",
        description="```Language Codes for Supported Languages```",
        color=0xe91e63
    )
    em2 = discord.Embed(
        title="NSBORO Bot Translater Language Codes Pt. 2",
        description="```Language Codes for Supported Languages```",
        color=0xe91e63
    )
    em3 = discord.Embed(
        title="NSBORO Bot Translater Language Codes Pt. 3",
        description="```Language Codes for Supported Languages```",
        color=0xe91e63
    )
    em4 = discord.Embed(
        title="NSBORO Bot Translater Language Codes Pt. 4",
        description="```Language Codes for Supported Languages```",
        color=0xe91e63
    )

    LANGUAGES = {
        'af': 'afrikaans',
        'sq': 'albanian',
        'am': 'amharic',
        'ar': 'arabic',
        'hy': 'armenian',
        'az': 'azerbaijani',
        'eu': 'basque',
        'be': 'belarusian',
        'bn': 'bengali',
        'bs': 'bosnian',
        'bg': 'bulgarian',
        'ca': 'catalan',
        'ceb': 'cebuano',
        'ny': 'chichewa',
        'zh-cn': 'chinese (simplified)',
        'zh-tw': 'chinese (traditional)',
        'co': 'corsican',
        'hr': 'croatian',
        'cs': 'czech',
        'da': 'danish',
        'nl': 'dutch',
        'en': 'english',
        'eo': 'esperanto',
        'et': 'estonian',
        'tl': 'filipino',
        'fi': 'finnish',
        'fr': 'french',
        'fy': 'frisian',
        'gl': 'galician',
        'ka': 'georgian',
        'de': 'german',
        'el': 'greek',
        'gu': 'gujarati',
        'ht': 'haitian creole',
        'ha': 'hausa',
        'haw': 'hawaiian',
        'iw': 'hebrew',
        'he': 'hebrew',
        'hi': 'hindi',
        'hmn': 'hmong',
        'hu': 'hungarian',
        'is': 'icelandic',
        'ig': 'igbo',
        'id': 'indonesian',
        'ga': 'irish',
        'it': 'italian',
        'ja': 'japanese',
        'jw': 'javanese',
        'kn': 'kannada',
        'kk': 'kazakh',
        'km': 'khmer',
        'ko': 'korean',
        'ku': 'kurdish (kurmanji)',
        'ky': 'kyrgyz',
        'lo': 'lao',
        'la': 'latin',
        'lv': 'latvian',
        'lt': 'lithuanian',
        'lb': 'luxembourgish',
        'mk': 'macedonian',
        'mg': 'malagasy',
        'ms': 'malay',
        'ml': 'malayalam',
        'mt': 'maltese',
        'mi': 'maori',
        'mr': 'marathi',
        'mn': 'mongolian',
        'my': 'myanmar (burmese)',
        'ne': 'nepali',
        'no': 'norwegian',
        'or': 'odia',
        'ps': 'pashto',
        'fa': 'persian',
        'pl': 'polish',
        'pt': 'portuguese',
        'pa': 'punjabi',
        'ro': 'romanian',
        'ru': 'russian',
        'sm': 'samoan',
        'gd': 'scots gaelic',
        'sr': 'serbian',
        'st': 'sesotho',
        'sn': 'shona',
        'sd': 'sindhi',
        'si': 'sinhala',
        'sk': 'slovak',
        'sl': 'slovenian',
        'so': 'somali',
        'es': 'spanish',
        'su': 'sundanese',
        'sw': 'swahili',
        'sv': 'swedish',
        'tg': 'tajik',
        'ta': 'tamil',
        'te': 'telugu',
        'th': 'thai',
        'tr': 'turkish',
        'uk': 'ukrainian',
        'ur': 'urdu',
        'ug': 'uyghur',
        'uz': 'uzbek',
        'vi': 'vietnamese',
        'cy': 'welsh',
        'xh': 'xhosa',
        'yi': 'yiddish',
        'yo': 'yoruba',
        'zu': 'zulu',
    }
    counter = 0
    for key in LANGUAGES:
        counter += 1
        if counter > 25 and counter <= 50:
            em.add_field(name=f"**{LANGUAGES[key]}**", value=key)
        elif counter > 50 and counter <= 75:
            em2.add_field(name=f"**{LANGUAGES[key]}**", value=key)
        elif counter > 75 and counter <= 100:
            em3.add_field(name=f"**{LANGUAGES[key]}**", value=key)
        elif counter > 100 and counter <= 125:
            em4.add_field(name=f"**{LANGUAGES[key]}**", value=key)

    await ctx.send(embed=em)
    await ctx.send(embed=em2)
    await ctx.send(embed=em3)
    await ctx.send(embed=em4)


@bot.group(invoke_without_command=True)
async def therapy(ctx):
    em = discord.Embed(
        title=f"Mental Health Commands",
        description=f"```These provide helpful tips and strategies to keep your mind healthy and relaxed!```",
        color=discord.Color.orange())
    em.add_field(name="`.therapy breathe`", value="Generates a breathing GIF!")
    em.add_field(name="`.therapy hotlines`", value="Provides hotlines")
    em.add_field(name="`.therapy motivation`", value="Generates a motivational message!")
    em.add_field(name="`.therapy relax`", value="Generates a relaxing image!")
    em.add_field(name="`.therapy vent`", value="Vent in dms! Everything will be kept private.")

    await ctx.send(embed=em)


@therapy.command()
async def breathe(ctx):
    links = ["https://i.pinimg.com/originals/1d/7a/6d/1d7a6df38bd0b1aab9d6c3b7c3d00779.gif",
             "https://i.pinimg.com/originals/92/1d/d9/921dd92426d71b810df0edf61a9abffe.gif",
             "https://www.mondaycampaigns.org/wp-content/uploads/2020/04/destress-monday-breathing-gif-circle-white-border.gif",
             "https://smho-smso.ca/wp-content/uploads/2020/06/Four-square-breathing-EN.gif",
             "https://cdn.discordapp.com/attachments/760988796249833472/837030298876379166/image0.gif",
             "https://cdn.discordapp.com/attachments/760988796249833472/837031005327458324/image0.gif",
             "https://cdn.doyou.com/wp/2016/12/giphy.gif",
             "https://media4.giphy.com/media/TH5hwgzAUx0ZOWOsh6/giphy.gif",
             "https://cdn.discordapp.com/attachments/760988796249833472/837030525981032569/image0.gif"]

    em = discord.Embed(
        title=f"Follow along with the GIF below!",
        description="",
        color=discord.Color.blue())
    em.set_image(url=links[random.randrange(0, len(links))])
    em.set_footer(text="Everything will be okay <3")

    await ctx.send(embed=em)


@therapy.command()
async def hotlines(ctx):
    em = discord.Embed(
        title=f"Hotlines",
        description="Crisis and Suicide Hotlines",
        color=discord.Color.blue())
    em.add_field(name="**General Crisis Line:**", value="> Text SUPPORT to 741-741")
    em.add_field(name="**National Suicide Prevention Lifeline:**", value="> 1-800-273-8255")
    em.add_field(name="**Online Chat:**", value="> https://suicidepreventionlifeline.org/chat/")
    await ctx.send(embed=em)


@therapy.command()
async def motivation(ctx):
    quotes = ["You're completely valid!", "You???re a true gift to the people in your life.", "You are loved!",
              "Today will be a good day. Keep that in your head.",
              "Sometimes when things are falling apart, they may actually be falling into the right place.",
              "The world would be a better place if more people were like you!",
              "Everything will be okay, I promise.", "Believe in yourself! Never give up!",
              "It may seem like there's no hope, but things will get better eventually.", ]
    em = discord.Embed(
        title=f"Motivation",
        description=f"```{quotes[random.randrange(0, len(quotes))]}```",
        color=discord.Color.blue())
    await ctx.send(embed=em)


@therapy.command()
async def relax(ctx):
    links = ["https://thumbs.gfycat.com/ObedientEmptyGazelle-max-1mb.gif",
             "https://64.media.tumblr.com/d01cd181bf81abc9ac6fc6f64e854371/291858a8d8307206-b2/s1280x1920/b7b903829cfcb292d026ae1e3fc46c426cc186ca.gif",
             "https://i.pinimg.com/originals/41/ff/e2/41ffe25dce45496f8078aa4777913695.gif",
             "https://i.imgur.com/BzbvfCf.gif",
             "https://i.pinimg.com/originals/3c/31/c8/3c31c8503d9e31400e96d4b90b93c141.gif",
             "https://i.pinimg.com/originals/b1/e7/84/b1e784b9edb0272216441fc1774d8ed4.gif",
             "https://i0.wp.com/i.redd.it/y1ewvqjf3gt21.png",
             "https://cdn.statically.io/img/nextshark.com/wp-content/uploads/2018/01/tumblr_ozth0ga3EL1qze3hdo1_r1_500.gif?quality=80&f=auto",
             "https://cdn.discordapp.com/attachments/815851587615326228/874943404587511878/download.gif",
             "https://i.pinimg.com/originals/34/d7/a3/34d7a3bbe7ab056f213e66c7182dd57e.gif",
             "https://64.media.tumblr.com/29a8712aafa887fe4c8d32b726adb647/tumblr_osiz5xMRBW1vg9wr5o1_1280.gif",
             "https://i.imgur.com/UmppnUD.gif"]
    motivations = ["it'll be alright <3", "everything will be okay <3", "take a deep breath and relax <3",
                   "you have nothing to worry about <3"]

    em = discord.Embed(
        title=motivations[random.randrange(0, len(motivations))],
        description="",
        color=discord.Color.blue())
    em.set_image(url=links[random.randrange(0, len(links))])
    await ctx.send(embed=em)


@therapy.command()
async def vent(ctx):
    person = bot.get_user(ctx.author.id)
    await person.send("Vent here, no one is listening!")


@bot.group(invoke_without_command=True)
async def weather(ctx, *, args):
    client = python_weather.Client(format=python_weather.IMPERIAL)
    weather = await client.find(args)
    em = discord.Embed(
        title=f"Weather of {args}",
        description=f"```As of {date.today()}```",
        color=discord.Color.blue())
    em.add_field(name="Temperature",
                 value=str(weather.current.sky_text) + ": " + str(weather.current.temperature) + "?? F")
    for forecast in weather.forecasts:
        em.add_field(name=str(forecast.date)[0:10], value=f"{str(forecast.sky_text)}: {str(forecast.temperature)}?? F")
    await client.close()
    await ctx.send(embed=em)


@bot.command()
async def news(ctx, *, topic=""):
    title = topic
    if topic == "":
        topic = "news"
        title = "Miscellaneous"
    googlenews = GoogleNews()
    googlenews = GoogleNews(lang='en', region='US', period="7d")
    googlenews.search(topic)
    titles = googlenews.get_texts()
    links = googlenews.get_links()
    em = discord.Embed(
        title=f"{title} News",
        description=f"```Recent news about {title}```",
        color=discord.Color.blue())
    for i in range(5):
        em.add_field(name=titles[i], value=links[i])
    await ctx.send(embed=em)

@bot.command()
async def trivia(ctx):
    my_api = Trivia(True)
    response = my_api.request(1, None, None, Type.Multiple_Choice)

    all_answers = [response['results'][0]['correct_answer']] + response['results'][0]['incorrect_answers']
    random.shuffle(all_answers)
    correct_answer = response['results'][0]['correct_answer']
    val_str = ""
    for i in range(len(all_answers)):
        val_str += f"{i + 1}. {all_answers[i]} \n"
    em = discord.Embed(
        title=response['results'][0]['question'],
        description=f"Category: {response['results'][0]['category']}, " + f"Difficulty: {response['results'][0]['difficulty'].capitalize()} \n \n {val_str}",
        color=discord.Color.blue())
    em.set_footer(text="Say the number of the correct answer")

    await ctx.send(embed=em)
    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    possibles = [str(i) for i in range(1, 5)]
    if msg.content not in possibles:
        await ctx.send("Input a valid number!")
    elif all_answers[int(msg.content) - 1] == correct_answer:
        await ctx.send(":white_check_mark: You were right!")
    else:
        await ctx.send(f":x: Incorrect! The correct answer was **{correct_answer}**")

@bot.command()
async def definition(ctx, arg):
    dictionary = PyDictionary()
    result = "```"
    for key in dictionary.meaning(arg).keys():
        result += key + ": \n"
        counter = 1
        for definition_ in dictionary.meaning(arg)[key]:
            result += f"{counter}. {definition_} \n"
            counter += 1
    result += "```"
    await ctx.send(result)


@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(
        title=".help on NSBORO Bot",
        description=
        "```Some useful commands for this bot. The bot prefix is \".\". Use .help [command] for more information on each command.```",
        color=discord.Color.orange())
    em.add_field(
        name="General",
        value=
        "color, setname, getname, stats, rules, studymode, invite, report, schedule, viewschedule, getUID, setUID, clubs, covid, period, getclass, hw, translate"
    )
    em.add_field(
        name="Moderation",
        value=
        "mute, unmute, warn, purge, tempmute, kick, ban, giverole, removerole, addrole, slowmode, changename"
    )
    em.add_field(
        name="Currency",
        value=
        "bal, beg, pray, give, rob, lottery, slots, shop, buy, sell, use, stock"
    )
    em.add_field(name="Miscellaneous", value="fight, kill, basta, kyt")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def color(ctx):
    em = discord.Embed(
        title="Color",
        description=
        "```Gives [HEX Code] as a color role. Please do not include the # in the Hex Code when running the command. Before changing roles to another color, please include \"remove\" in [arg], else leave it blank.```"
    )
    em.add_field(name="**Syntax**", value=".color [HEX Code] [arg]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def stats(ctx):
    em = discord.Embed(
        title="Stats",
        description="```Returns the number of users on the NSBORO Server```")
    em.add_field(name="**Syntax**", value=".stats")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def ping(ctx):
    em = discord.Embed(title="Ping", description="```Returns latency```")
    em.add_field(name="**Syntax**", value=".ping")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def rules(ctx):
    em = discord.Embed(title="Rules",
                       description="```Returns NSBORO server rules```")
    em.add_field(name="**Syntax**", value=".rules")
    await ctx.send(embed=em)


@help.command()
async def studymode(ctx):
    em = discord.Embed(
        title="Studymode",
        description=
        "```Turns studymode [on/off]]. Studymode will remind you to keep working on your work, so whenever you send a message onto the NSBORO server, the NSBORO bot will remind you to keep working```"
    )
    em.add_field(name="**Syntax**", value=".studymode [on/off]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def invite(ctx):
    em = discord.Embed(title="Invite",
                       description="```Returns the NSBORO server invite```")
    em.add_field(name="**Syntax**", value=".invite")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def report(ctx):
    em = discord.Embed(
        title="Report",
        description="```Reports [arg]] to the Moderators and Admins```")
    em.add_field(name="**Syntax**", value=".report [arg]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def mute(ctx):
    em = discord.Embed(
        title="Mute",
        description="```Any Mods/Admins can use this command to mute [user]```")
    em.add_field(name="**Syntax**", value=".mute [user]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def unmute(ctx):
    em = discord.Embed(
        title="Unmute",
        description="```Any Mods/Admins can use this command to unmute [user]```")
    em.add_field(name="**Syntax**", value=".unmute [user]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def warn(ctx):
    em = discord.Embed(
        title="Warn",
        description="```Any Mods/Admins can use this command to warn [user]```")
    em.add_field(name="**Syntax**", value=".warn [user]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def purge(ctx):
    em = discord.Embed(
        title="Purge",
        description=
        "```Any Mods/Admins can use this command to clear [arg] number of messages in that channel```"
    )
    em.add_field(name="**Syntax**", value=".purge [arg]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def tempmute(ctx):
    em = discord.Embed(
        title="Tempmute",
        description=
        "```Any Mods/Admins can use this command to tempmute [user] for [arg] seconds```"
    )
    em.add_field(name="**Syntax**", value=".tempmute [user] [arg]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def kick(ctx):
    em = discord.Embed(
        title="Kick",
        description="```Any Admins can use this command to kick [user]```")
    em.add_field(name="**Syntax**", value=".kick [user]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def ban(ctx):
    em = discord.Embed(
        title="Ban",
        description="```Any Admins can use this command to ban [user]```")
    em.add_field(name="**Syntax**", value=".ban [user]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def unban(ctx):
    em = discord.Embed(
        title="Ban",
        description="```Any Admins can use this command to unban [user]```")
    em.add_field(name="**Syntax**", value=".unban [user]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def giverole(ctx):
    em = discord.Embed(
        title="Giverole",
        description=
        "```Any Mods/Admin can use this command to give [role] to [user]```")
    em.add_field(name="**Syntax**", value=".giverole [user] [role]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def removerole(ctx):
    em = discord.Embed(
        title="Removerole",
        description=
        "```Any Mods/Admin can use this command to remove [role] from [user]```")
    em.add_field(name="**Syntax**", value=".removerole [user] [role]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def addrole(ctx):
    em = discord.Embed(
        title="Addrole",
        description=
        "```Any Mods/Admin can use this command to add [arg] role to the server```")
    em.add_field(name="**Syntax**", value=".addrole [arg]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def slowmode(ctx):
    em = discord.Embed(
        title="Slowmode",
        description=
        "```Any Mods/Admin can use this command to set [arg] second slowmode to the channel```"
    )
    em.add_field(name="**Syntax**", value=".slowmode [arg]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def bal(ctx):
    em = discord.Embed(
        title="Bal",
        description=
        "```You can use this to check the balance of [user]. If [user] is left empty, then it is defauled to check your own balance```"
    )
    em.add_field(name="**Syntax**", value=".bal [user]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def beg(ctx):
    em = discord.Embed(
        title="Beg",
        description="```Beg for coins, where the currency is stored in your bank```")
    em.add_field(name="**Syntax**", value=".beg")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def pray(ctx):
    em = discord.Embed(title="Pray",
                       description="```Pray to either basta or steven for coins```")
    em.add_field(name="**Syntax**", value=".pray [basta/steven]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def lottery(ctx):
    em = discord.Embed(
        title="Lottery",
        description=
        "```Enter the lottery with [arg] coins, you have a 1/10 chance of winning 100x the amount entered```"
    )
    em.add_field(name="**Syntax**", value=".lottery [arg]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def give(ctx):
    em = discord.Embed(title="Give",
                       description="```You can give [arg] coins to [user]```")
    em.add_field(name="**Syntax**", value=".give [user] [arg]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def rob(ctx):
    em = discord.Embed(
        title="Rob",
        description=
        "```You attempt to rob [user]. If successful, you will take a part of their money. If you fail, you must pay them money.```"
    )
    em.add_field(name="**Syntax**", value=".rob [user]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def slots(ctx):
    em = discord.Embed(
        title="Slots",
        description=
        "```Bet [arg] coins in a game of slots! Same 2 slots will reward you 3x the amount entered. Same 3 slots will reward you 5x the amount entered.```"
    )
    em.add_field(name="**Syntax**", value=".slots [arg]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def shop(ctx):
    em = discord.Embed(
        title="Shop",
        description=
        "```It will open the NSBORO bot shop where you can buy miscellaneous items with your coins```"
    )
    em.add_field(name="**Syntax**", value=".shop")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def bag(ctx):
    em = discord.Embed(
        title="Bag",
        description="```It will open your inventory containing items you bought```")
    em.add_field(name="**Syntax**", value=".bag")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def buy(ctx):
    em = discord.Embed(
        title="Buy",
        description=
        "```Buys [qty] [item]s from the shop with your coins. Leaving [qty] blank will default the amount to one```"
    )
    em.add_field(name="**Syntax**", value=".buy [item] [qty]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def sell(ctx):
    em = discord.Embed(
        title="Shop",
        description=
        "```Sells [qty] [item]s from your bag with your coins. Leaving [qty] blank will default the amount to one```"
    )
    em.add_field(name="**Syntax**", value=".sell [item] [qty]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def use(ctx):
    em = discord.Embed(
        title="Shop",
        description=
        "```Uses 1 [item] from your bag. Various items will do various things.```")
    em.add_field(name="**Syntax**", value=".use [item]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def fight(ctx):
    em = discord.Embed(title="Fight", description="```Fights [user]```")
    em.add_field(name="**Syntax**", value=".fight [user]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def kill(ctx):
    em = discord.Embed(title="Kill", description="```Kills [user]```")
    em.add_field(name="**Syntax**", value=".kill [user]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def basta(ctx):
    em = discord.Embed(title="Basta",
                       description="```Returns a random image of Basta god```")
    em.add_field(name="**Syntax**", value=".basta")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def kyt(ctx):
    em = discord.Embed(
        title="KYT",
        description="```Send President Kevin Yao your prayers and thanks```")
    em.add_field(name="**Syntax**", value=".kyt")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def stock(ctx):
    em = discord.Embed(
        title="Stock",
        description="```Returns the current price of the NSBORO bot stock```")
    em.add_field(name="**Syntax**", value=".stock")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def setname(ctx):
    em = discord.Embed(title="Setname",
                       description="```Sets your IRL name using this command```")
    em.add_field(name="**Syntax**", value=".setname [FirstName LastName]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def getname(ctx):
    em = discord.Embed(title="Getname",
                       description="```Gets the mentioned user's IRL name```")
    em.add_field(name="**Syntax**", value=".getname @user")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def changename(ctx):
    em = discord.Embed(
        title="Changename",
        description="```Changes the mentioned user's IRL name (for Staff only)```")
    em.add_field(name="**Syntax**",
                 value=".changename @user [FirstName LastName]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def schedule(ctx):
    em = discord.Embed(
        title="Schedule",
        description=
        "```Creates a schedule (School Year 2021-2022). Keep each class name to one word without spaces. Once initially created, you can update your schedule with the same command, or you can .viewschedule to get your schedule```"
    )
    em.add_field(
        name="**Syntax**",
        value=
        ".schedule [first_class] [second_class] [third_class] [fourth_class] [fifth class] [sixth class] [seventh class] **NO SPACES IN CLASS NAMES**"
    )
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def covid(ctx):
    em = discord.Embed(
        title="Covid",
        description="```Sends the weekly COVID-19 data of NSBORO schools.```")
    em.add_field(name="**Syntax**", value=".covid")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def viewschedule(ctx):
    em = discord.Embed(
        title="Viewschedule",
        description="```Sends your or another person's saved schedule.```")
    em.add_field(name="**Syntax**", value=".viewschedule [optional: @person]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def getclass(ctx):
    em = discord.Embed(
        title="Getclass",
        description="```Gets you or another person's current or next class```")
    em.add_field(name="**Syntax**",
                 value=".getclass [optional: next] [optional: @person]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def period(ctx):
    em = discord.Embed(title="Period",
                       description="```Sends the current or next period number```")
    em.add_field(name="**Syntax**", value=".period [optional: next]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def hw(ctx):
    em = discord.Embed(title="HW",
                       description="```Sends a list of all homework/tasks. Can be updated with .hw add/remove/clear```")
    em.add_field(name="**Syntax**", value=".hw [optional: add/remove/clear]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def translate(ctx):
    em = discord.Embed(title="Translate", description="```Translates one language into another```")
    em.add_field(name="**Syntax**",
                 value=".translate [optional: codes] [language code to be translated into (ex. es) [words]")
    em.add_field(name="**Common Language Codes**",
                 value="Spanish - es \nFrench - fr\n Chinese - zh-CN \n English - en \nJapanese - ja \nArabic - ar \nRussian - ru")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def therapy(ctx):
    em = discord.Embed(title="Therapy", description="```Personal therapy for irene```")
    em.add_field(name="**Syntax**",
                 value=".therapy")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def weather(ctx):
    em = discord.Embed(title="Weather", description="```Sends the weather```")
    em.add_field(name="**Syntax**",
                 value=".weather [place]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


@help.command()
async def definition(ctx):
    em = discord.Embed(title="Definition", description="```Sends the definition of a word```")
    em.add_field(name="**Syntax**", value=".definition [word]")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)

@help.command()
async def trivia(ctx):
    em = discord.Embed(title="Trivia", description="```Sends a random trivia question!```")
    em.add_field(name="**Syntax**", value=".trivia")
    em.set_thumbnail(url="https://i.imgur.com/VfNZlg1.jpg")
    await ctx.send(embed=em)


my_secret = os.environ['serverkey']
bot.run(my_secret)
