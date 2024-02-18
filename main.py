#TODO !search before having a dragon\, typo for "I wasn't a dodge" and for "inventory hero"
import asyncio
import random
import sqlite3
from discord.ext import commands
import discord
import json
from discord.ext.commands import MissingPermissions


f = open('config.json')
datac = json.load(f)
token = datac['token']
gameChannel = datac['channel']
db = sqlite3.connect('database.sqlite')
cursor = db.cursor()


TOKEN = token

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!",intents=intents)
client.remove_command('help')
colors = [1752220,1146986,3066993,2067276,3447003,2123412,10181046,7419530,15277667,11342935,15844367,12745742,15105570,11027200,15158332,10038562,9807270,9936031,8359053,12370112,3426654,2899536,16776960]
color = random.choice(colors)

invites = {}
l0 = 0
l1 = 50
l2 = 100
l3 = 200
l4 = 350
l5 = 550
l6 = 800
l7 = 1100
l8 = 1450
l9 = 1850
l10 = 2300
l11 = 2800
l12 = 3350
l13 = 3950
l14 = 4600
l15 = 5300
l16 = 6050
l17 = 6850
l18 = 7700
l19 = 8600
l20 = 9550
mature = 10550
allLevels = [0,50,100,200,350,550,800,1100,1450,1850,2300,2800,3350,3950,4600,5300,6050,6850,7700,8600,9550,10550]

blackberryXP = 5
blueberryXP = 3
blackcurrantXP = 1
raspberryXP = 1

#on ready
@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name = "over the Dragons"))



@client.command(brief="Hatching your own dragon.",usage="!hatch <dragonName>",aliases=["Hatch",'HATCH'])
async def hatch(ctx,name=None):
    if int(ctx.channel.id) == int(gameChannel):
        mention = ctx.message.author.mention
        if name is not None:
            cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{ctx.message.author.id}'")
            playerCheck = cursor.fetchone()
            if playerCheck is None:
                cursor.execute(f"SELECT userID FROM users WHERE dragonName = '{name}'")
                dragonCheck = cursor.fetchone()
                if dragonCheck is None:
                    cursor.execute(f"INSERT INTO users (userID, dragonName,dragonXP, Dcash,damage,armor,dexterity,health,inteligence,pointsLeft,level) VALUES ('{ctx.message.author.id}','{name}','0','0','1','1','1','1','1','1','0')")
                    db.commit()
                    cursor.execute(f"INSERT INTO inventory (userID, blackberry, blueberry, blackcurrant,raspberry) VALUES ('{ctx.message.author.id}','0','0','0','0')")
                    db.commit()
                    cursor.execute(f"INSERT INTO fightsRanking (userID, wins, losses,ratio) VALUES ('{ctx.message.author.id}','0','0','0')")
                    db.commit()
                    embed = discord.Embed(description=f"Congrats {ctx.message.author.mention} you got your dragon, `{name}`!\n\n"
                                                      f"» You can use your dragon to fight in dungeons using `!dungeon`\n"
                                                      f"» You can use your dragon to fight against other players using `!fight @user <amount>`\n"
                                                      f"» Don't forget to use the food from your inventory to grow up your dragon using `!feed <itemName> <amount>`\n",color=color)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f"{mention} please pick another name, `{name}` is taken.",color=15158332)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description = f"{mention} You already have your dragon hatched. Use `!dragon` to check its stats.", color = 15158332)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"{mention} you have to put a name to your dragon, please use `!hatch <name>`",color=15158332)
            await ctx.send(embed=embed)


@client.command(brief="Information about each stats and how it works",aliases=['Stats','STATS'])
async def stats(ctx):
    embed = discord.Embed(description="All stats and their use.",color=color)
    embed.add_field(name="Damage Bonus",value="This status increase the damage your dragon deals in fights.")
    embed.add_field(name="Armor Bonus", value="This status decrease the damage your dragon receives in fights.")
    embed.add_field(name="Dexterity Bonus",value="This status increase the chance to dodge enemies attack.")
    embed.add_field(name="Health Bonus", value="This status increase the health of your dragon in fights.")
    embed.add_field(name="Intelligence Bonus", value="This status increase the amount of healing you get from items in fights.")
    embed.add_field(name="To be continued...",
                    value="More advanced stats might come in the near future.")
    await ctx.send(embed=embed)

@client.command(brief="Check the stats of your dragon.",aliases=['Dragon','DRAGON'])
async def dragon(ctx):
    if int(ctx.channel.id) == int(gameChannel):
        global allLevels
        cursor.execute(f"SELECT dragonXP FROM users WHERE userID = '{ctx.message.author.id}'")
        dragonXP = cursor.fetchone()
        cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{ctx.message.author.id}'")
        dragonName = cursor.fetchone()



        if dragonXP is None:
            embed = discord.Embed(
                description=f"{ctx.message.author.mention} you do not have a dragon, please use `!hatch <name>` to get it.", color=15158332)
            await ctx.send(embed=embed)
        else:

            cursor.execute(f"SELECT damage FROM users WHERE userID = '{ctx.message.author.id}'")
            dmg = cursor.fetchone()[0]

            cursor.execute(f"SELECT armor FROM users WHERE userID = '{ctx.message.author.id}'")
            armor = cursor.fetchone()[0]

            cursor.execute(f"SELECT dexterity FROM users WHERE userID = '{ctx.message.author.id}'")
            dex = cursor.fetchone()[0]

            cursor.execute(f"SELECT health FROM users WHERE userID = '{ctx.message.author.id}'")
            health = cursor.fetchone()[0]

            cursor.execute(f"SELECT inteligence FROM users WHERE userID = '{ctx.message.author.id}'")
            intelligence = cursor.fetchone()[0]

            cursor.execute(f"SELECT pointsLeft FROM users WHERE userID = '{ctx.message.author.id}'")
            pointsLeft = cursor.fetchone()[0]

            x = 0
            dragonLevel = 0
            nextLevel = 0
            previousLevel = 0
            while x < 1:
                for level in allLevels:
                    if level <= int(dragonXP[0]):
                        x+=1
                        dragonLevel = allLevels.index(level)
                        nextLevel = allLevels[dragonLevel+1]
                        previousLevel = allLevels[dragonLevel]
                    else:
                        pass

            percentage = ((dragonXP[0] - previousLevel) * 100 ) /(nextLevel-previousLevel)
            points = round(percentage/10)
            progress = f"{points*'🔵'}{(10-points)*'🔘'} | "
            textProgress = f"{dragonXP[0]}/{nextLevel}"
            print(points)

            embed = discord.Embed(title = f"{dragonName[0]}",description=f"{ctx.message.author.mention}'s Dragon",color=color)
            embed.add_field(name="Level",value=dragonLevel)
            embed.add_field(name="XP",value=dragonXP[0])
            embed.add_field(name="Progress", value=f"{textProgress}")
            embed.add_field(name="Progress Bar",value=f"{progress} {round(percentage)}%",inline=False)
            embed.add_field(name="Advanced Stats",value=f"**Damage Bonus** (damage): `{dmg}`\n"
                                                        f"**Armor Bonus** (armor): `{armor}`\n"
                                                        f"**Dexterity Bonus** (dex): `{dex}`\n"
                                                        f"**Health Bonnus** (health): `{health}`\n"
                                                        f"**Intelligence Bonus** (int): `{intelligence}`\n"
                                                        f"**Points Left**: `{pointsLeft}`\n\n"
                                                        f"**In case you have points left, add them by using** \n`!addpoints <damage/armor/dex/health/int> <amount>`\n"
                                                        f"**Type `!stats` in order to get the information about each status**",inline=False)
            file = discord.File("tmbnail.png", filename="tmbnail.png")
            embed.set_thumbnail(url="attachment://tmbnail.png")
            await ctx.send(file=file,embed=embed)


@client.command(brief = "Enter dungeon and fight monsters to get food used to level up your dragon.",aliases=['Dungeon','DUNGEON'])
@commands.cooldown(1, 1200, commands.BucketType.user)
async def dungeon(ctx):
    if int(ctx.channel.id) == int(gameChannel):
        cursor.execute(f"SELECT dragonXP FROM users WHERE userID = '{ctx.message.author.id}'")
        dragonCheck = cursor.fetchone()
        cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{ctx.message.author.id}'")
        dragonName = cursor.fetchone()
        battleQuotes = [f"What a nice dodge made by **{dragonName[0]}**","Monsters are not holding back for sure.",
                        "The fight is not over yet!",f"Keep going **{dragonName[0]}**, you got this!",
                        "This fight will be decided pretty soon",f"**{dragonName[0]}** seems exhausted already",
                        "That's an unfortunate miss...",f"**{dragonName[0]}**, GET UP! PLEASE!",
                        "That hit could have ended the fight","There is no way back, we must win."]
        dungeonType = random.choice(range(0,3))
        bosses = random.choice(range(1,4))
        if dungeonType == 0:
            prc = random.choice(range(75,95))
            embed = discord.Embed(description=f"{ctx.message.author.mention} you entered in a dungeon with your dragon **{dragonName[0]}**\n\n"
                                              f"You found **{bosses} monsters**, but they seem to be weak.\n"
                                              f"You should not worry about it, you have a chance of `{prc}%` to finish the dungeon.\n\n"
                                              f"*{dragonName[0]} getting closer to the first monster.*\n\n")
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(2)
            embed.add_field(name="ohh..",value=random.choice(battleQuotes))
            await msg.edit(embed=embed)
            if prc > 85:
                await asyncio.sleep(2)
                embed.add_field(name="cmon..", value=random.choice(battleQuotes),inline=False)
                await msg.edit(embed=embed)
            s = list(round(prc)*'1'+((100-round(prc)) * '0'))
            result = random.choice(s)
            await asyncio.sleep(2)
            if result == "1":
                blackberry = random.choice(range(0,2))
                blueberry = random.choice(range(0,3))
                blackcurrant = random.choice(range(0,4))
                raspberry = random.choice(range(0,5))
                dCash = random.choice(range(0,50))
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n", color=color)
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n", color=color)
                await msg.edit(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n", color=color)
                await msg.edit(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n"
                                f"- Raspberries: {raspberry}\n"
                                f"- Dcash: {dCash}", color=color)
                await msg.edit(embed=embed)
                cursor.execute(f"UPDATE inventory SET blackberry = blackberry + '{blackberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET blueberry = blueberry + '{blueberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET blackcurrant = blackcurrant + '{blackcurrant}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET raspberry = raspberry + '{raspberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE users SET Dcash = Dcash + '{dCash}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()


            elif result == "0":
                embed = discord.Embed(description=f"Bad news... I know this was an easy fight but **{dragonName[0]}** didn't offer enough respect to these monsters\n\n"
                                                  f"The good part is that you both escaped from the dungeon safely and you can get your revenge in about 1h.\n"
                                                  f"Don't blame **{dragonName[0]}**, there are so many things to be learned.\n\n"
                                                  f"Don't forget to feed **{dragonName[0]}**, getting stronger!",color=15158332)
                await ctx.send(embed=embed)

        elif dungeonType == 1:
            prc = random.choice(range(50, 75))
            embed = discord.Embed(
                description=f"{ctx.message.author.mention} you entered in a dungeon with your dragon **{dragonName[0]}**\n\n"
                            f"You found **{bosses} monsters**, they don't seem to be intimidated by us.\n"
                            f"We should be careful, you have a chance of `{prc}%` to finish the dungeon.\n\n"
                            f"*{dragonName[0]} slowly getting closer to the first monster.*\n\n")
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(2)
            embed.add_field(name="pfuu..", value=random.choice(battleQuotes))
            await msg.edit(embed=embed)
            if prc > 60:
                await asyncio.sleep(2)
                embed.add_field(name="holy..", value=random.choice(battleQuotes), inline=False)
                await msg.edit(embed=embed)
            s = list(round(prc) * '1' + ((100 - round(prc)) * '0'))
            result = random.choice(s)
            await asyncio.sleep(2)
            if result == "1":
                blackberry = random.choice(range(0, 3))
                blueberry = random.choice(range(0, 5))
                blackcurrant = random.choice(range(0, 7))
                raspberry = random.choice(range(0, 10))
                dCash = random.choice(range(0,75))
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n", color=color)
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n", color=color)
                await msg.edit(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n", color=color)
                await msg.edit(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                 f"- Blackcurrants: {blackcurrant}\n"
                                f"- Raspberries: {raspberry}\n"
                                f"- Dcash: {dCash}", color=color)
                await msg.edit(embed=embed)
                cursor.execute(
                    f"UPDATE inventory SET blackberry = blackberry + '{blackberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET blueberry = blueberry + '{blueberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET blackcurrant = blackcurrant + '{blackcurrant}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET raspberry = raspberry + '{raspberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE users SET Dcash = Dcash + '{dCash}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()


            elif result == "0":
                embed = discord.Embed(
                    description=f"NOOOOOOO.... **{dragonName[0]}** please get up...\n\n"
                                f"The good part is that you both escaped from the dungeon safely and you can get your revenge in about 1h.\n"
                                f"**{dragonName[0]}** really needs some rest after this lose..\n\n"
                                f"Don't forget to feed **{dragonName[0]}**, getting stronger!", color=15158332)
                await ctx.send(embed=embed)

        elif dungeonType == 2:
            prc = random.choice(range(25, 50))
            embed = discord.Embed(
                description=f"{ctx.message.author.mention} you entered in a dungeon with your dragon **{dragonName[0]}**\n\n"
                            f"You found **{bosses} monsters**, they are bigger and look stronger than us.\n"
                            f"Play it safe, you only have a chance of `{prc}%` to finish the dungeon.\n\n"
                            f"*{dragonName[0]} slowly getting closer to the first monster.*\n\n")
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(2)
            embed.add_field(name="hmm..", value=random.choice(battleQuotes))
            await msg.edit(embed=embed)
            if prc > 60:
                await asyncio.sleep(2)
                embed.add_field(name="errrm..", value=random.choice(battleQuotes), inline=False)
                await msg.edit(embed=embed)
            s = list(round(prc) * '1' + ((100 - round(prc)) * '0'))
            result = random.choice(s)
            await asyncio.sleep(2)
            if result == "1":
                blackberry = random.choice(range(0, 5))
                blueberry = random.choice(range(0, 8))
                blackcurrant = random.choice(range(0, 10))
                raspberry = random.choice(range(0, 15))
                dCash = random.choice(range(0,100))
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n", color=color)
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n", color=color)
                await msg.edit(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n", color=color)
                await msg.edit(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n"
                                f"- Raspberries: {raspberry}\n"
                                f"- Dcash: {dCash}", color=color)
                await msg.edit(embed=embed)
                cursor.execute(
                    f"UPDATE inventory SET blackberry = blackberry + '{blackberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET blueberry = blueberry + '{blueberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET blackcurrant = blackcurrant + '{blackcurrant}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET raspberry = raspberry + '{raspberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE users SET Dcash = Dcash + '{dCash}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()


            elif result == "0":
                embed = discord.Embed(
                    description=f"To be honest, this was quite expected. **{dragonName[0]}** is way smaller and has a lot to learn...\n\n"
                                f"The good part is that you both escaped from the dungeon safely and you can get your revenge in about 1h.\n"
                                f"**{dragonName[0]}** really needs some rest after this lose..\n\n"
                                f"Don't forget to feed **{dragonName[0]}**, getting stronger!", color=15158332)
                await ctx.send(embed=embed)


        elif dungeonType == 3:
            prc = random.choice(range(1, 25))
            embed = discord.Embed(
                description=f"{ctx.message.author.mention} you entered in a dungeon with your dragon **{dragonName[0]}**\n\n"
                            f"You found **{bosses} monsters**, from what we can see, they are the strongest monsters out there.\n"
                            f"BE CAREFUL! Seems like you only have a chance of `{prc}%` to finish the dungeon.\n\n"
                            f"*{dragonName[0]} slowly and slightly scared, getting closer to the first monster.*\n\n")
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(2)
            embed.add_field(name="outch..", value=random.choice(battleQuotes))
            await msg.edit(embed=embed)
            if prc > 60:
                await asyncio.sleep(2)
                embed.add_field(name="let's goooo..", value=random.choice(battleQuotes), inline=False)
                await msg.edit(embed=embed)
            s = list(round(prc) * '1' + ((100 - round(prc)) * '0'))
            result = random.choice(s)
            await asyncio.sleep(2)
            if result == "1":
                blackberry = random.choice(range(0, 5))
                blueberry = random.choice(range(0, 10))
                blackcurrant = random.choice(range(0, 15))
                raspberry = random.choice(range(0, 20))
                dCash = random.choice(range(0,150))
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n", color=color)
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n", color=color)
                await msg.edit(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n", color=color)
                await msg.edit(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"What an easy fight this was, **{dragonName[0]}** seems so happy with this win.\n\n"
                                f"He's picking up now the goods from the ground.\n"
                                f"Remember to give him a round of applause.\n\n"
                                f"Don't forget to feed **{dragonName[0]}** with the goods collected, getting stronger!\n\n"
                                f"**{dragonName[0]}** collected as following:\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n"
                                f"- Raspberries: {raspberry}\n"
                                f"- Dcash: {dCash}", color=color)
                await msg.edit(embed=embed)
                cursor.execute(
                    f"UPDATE inventory SET blackberry = blackberry + '{blackberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET blueberry = blueberry + '{blueberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET blackcurrant = blackcurrant + '{blackcurrant}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET raspberry = raspberry + '{raspberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE users SET Dcash = Dcash + '{dCash}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()


            elif result == "0":
                embed = discord.Embed(
                    description=f"This was an easy fight... unfortunately, for them. **{dragonName[0]}** had very low chances...\n\n"
                                f"The good part is that you both escaped from the dungeon safely and you can get your revenge in about 1h.\n"
                                f"**{dragonName[0]}** really needs some rest after this lose..\n\n"
                                f"Don't forget to feed **{dragonName[0]}**, getting stronger!", color=15158332)
                await ctx.send(embed=embed)


@dungeon.error
async def dungeon_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(description=f"{ctx.message.author.mention} you can enter in dungeon again in `{round(error.retry_after/60)} minutes`.", color=15158332)
        await ctx.send(embed=em)


@client.command(brief = "Check your inventory.",aliases=['Inventory','INVENTORY'])
async def inventory(ctx):
    if int(ctx.channel.id) == int(gameChannel):
        cursor.execute(f"SELECT userID FROM inventory WHERE userID = '{ctx.message.author.id}'")
        check = cursor.fetchone()
        if check is None:
            em = discord.Embed(
                description=f"{ctx.message.author.mention} you have to hatch your dragon first, do it using `!hatch <name>`.",
                color=15158332)
            await ctx.send(embed=em)
        else:
            cursor.execute(f"SELECT blackberry FROM inventory WHERE userID = '{ctx.message.author.id}'")
            blackberry = cursor.fetchone()[0]
            cursor.execute(f"SELECT blueberry FROM inventory WHERE userID = '{ctx.message.author.id}'")
            blueberry = cursor.fetchone()[0]
            cursor.execute(f"SELECT blackcurrant FROM inventory WHERE userID = '{ctx.message.author.id}'")
            blackcurrant = cursor.fetchone()[0]
            cursor.execute(f"SELECT raspberry FROM inventory WHERE userID = '{ctx.message.author.id}'")
            raspberry = cursor.fetchone()[0]
            cursor.execute(F"SELECT Dcash FROM users WHERE userID = '{ctx.message.author.id}'")
            Dcash = cursor.fetchone()[0]
            embed = discord.Embed(description=f"{ctx.message.author.mention}'s Inventory\n\n"
                                              f"• **Dcash**: `{Dcash}` -> *Buy items from other players*\n"
                                              f"• **Blackberry**: `{blackberry}`  -> *5XP or 20HP*\n"
                                              f"• **Blueberry**: `{blueberry}` -> *3XP or 15HP*\n"
                                              f"• **Blackcurrant**: `{blackcurrant}` -> *1XP or 10HP*\n"
                                              f"• **Raspberry**: `{raspberry}` -> *1XP or 5HP*\n\n"
                                              f"You can always use the items to level up your dragon using `!feed <item> <amount>`\n"
                                              f"You can use the items in fights in order to heal your dragon using `!heal <item>` while in an active fight.\n"
                                              f"Or You can sell them to Market for Dcash using `!sell <item> <amount>`",color=color)
            await ctx.send(embed=embed)


@client.command(brief = "Feed your dragon with the items you own in your inventory and gain XP.",aliases=['Feed','FEED'])
async def feed(ctx,item,amount:int):
    if int(ctx.channel.id) == int(gameChannel):
        if type(amount) is not int:
            em = discord.Embed(
                description=f"{ctx.message.author.mention} amount must be a rounded number.",
                color=15158332)
            await ctx.send(embed=em)
        else:
            item = item.lower()
            cursor.execute(f"SELECT userID FROM inventory WHERE userID = '{ctx.message.author.id}'")
            check = cursor.fetchone()
            if check is None:
                em = discord.Embed(
                    description=f"{ctx.message.author.mention} you have to hatch your dragon first, do it using `!hatch <name>`.",
                    color=15158332)
                await ctx.send(embed=em)
            else:
                cursor.execute(f"SELECT {item} FROM inventory WHERE userID = '{ctx.message.author.id}'")
                checkItem = cursor.fetchone()[0]
                if checkItem >= amount:
                    if item == "blackberry":
                        XP = 5
                        itm = "blackberry"
                    elif item == "blueberry":
                        XP = 3
                        itm = "blueberry"
                    elif item == "blackcurrant":
                        XP = 1
                        itm = "blackcurrant"
                    elif item == "raspberry":
                        XP = 1
                        itm = "raspberry"
                    XP = XP * amount
                    cursor.execute(f"UPDATE users SET dragonXP = dragonXP + '{XP}' WHERE userID = '{ctx.message.author.id}'")
                    db.commit()
                    cursor.execute(f"UPDATE inventory SET {itm} = {itm} - '{amount}' WHERE userID = '{ctx.message.author.id}'")
                    db.commit()
                    x=0
                    dragonLevel = 0
                    nextLevel = 0
                    previousLevel = 0

                    cursor.execute(f"SELECT dragonXP FROM users WHERE userID = '{ctx.message.author.id}'")
                    dragonXP = cursor.fetchone()

                    while x < 1:
                        for level in allLevels:
                            if level <= int(dragonXP[0]):
                                x += 1
                                dragonLevel = allLevels.index(level)
                                nextLevel = allLevels[dragonLevel + 1]
                                previousLevel = allLevels[dragonLevel]
                            else:
                                pass

                    cursor.execute(f"SELECT level FROM users WHERE userID = '{ctx.message.author.id}'")
                    currentlevel = cursor.fetchone()[0]

                    if int(dragonLevel) != int(currentlevel):
                        cursor.execute(f"UPDATE users SET level = '{dragonLevel}' WHERE userID = '{ctx.message.author.id}'")
                        db.commit()
                        embed=discord.Embed(description=f"Congrats {ctx.message.author.mention}!\nYour dragon leveled up to {dragonLevel} and received 2 status points.\n"
                                                        f"You can see them and how to use them by running `!dragon` and follow the instructions from the bottom.\n\n"
                                                        f"Your dragon overall stats increased by 1 point.",color=color)

                        leveldif = int(dragonLevel) - int(currentlevel)
                        pointsLeftGiven = int(leveldif) * 2
                        cursor.execute(f"UPDATE users SET pointsLeft = pointsLeft + '{pointsLeftGiven}' WHERE userID = '{ctx.message.author.id}'")
                        db.commit()

                        cursor.execute(
                            f"UPDATE users SET damage = damage + '{leveldif}' WHERE userID = '{ctx.message.author.id}'")
                        db.commit()
                        cursor.execute(
                            f"UPDATE users SET armor = armor + '{leveldif}' WHERE userID = '{ctx.message.author.id}'")
                        db.commit()
                        cursor.execute(
                            f"UPDATE users SET dexterity = dexterity + '{leveldif}' WHERE userID = '{ctx.message.author.id}'")
                        db.commit()
                        cursor.execute(
                            f"UPDATE users SET health = health + '{leveldif}' WHERE userID = '{ctx.message.author.id}'")
                        db.commit()
                        cursor.execute(
                            f"UPDATE users SET inteligence = inteligence + '{leveldif}' WHERE userID = '{ctx.message.author.id}'")
                        db.commit()

                        await ctx.send(embed=embed)

                    em = discord.Embed(
                        description=f"{ctx.message.author.mention} you successfully fed your dragon.\n"
                                    f"Your dragon experience increased with **{XP} XP**.",color=15158332)

                    await ctx.send(embed=em)
                    await dragon(ctx)
                else:
                    em = discord.Embed(
                        description=f"{ctx.message.author.mention} seems like you do not have enough {item}.",
                        color=15158332)
                    await ctx.send(embed=em)


@client.command(brief="Randomly taking a look around your for potential goodies or Dcash",aliases=['Search','SEARCH'])
@commands.cooldown(1, 1200, commands.BucketType.user)
async def search(ctx):
    if int(ctx.channel.id) == int(gameChannel):
        cursor.execute(f"SELECT userID FROM inventory WHERE userID = '{ctx.message.author.id}'")
        check = cursor.fetchone()
        if check is None:
            em = discord.Embed(
                description=f"{ctx.message.author.mention} you have to hatch your dragon first, do it using `!hatch <name>`.",
                color=15158332)
            await ctx.send(embed=em)
        else:
            chances = [1,1,1,1,1,1,1,1,1,0]
            result = random.choice(chances)
            if result == 1:
                blackberry = random.choice(range(0, 1))
                blueberry = random.choice(range(0, 3))
                blackcurrant = random.choice(range(0, 5))
                raspberry = random.choice(range(0, 5))
                dCash = random.choice(range(0, 25))

                embed = discord.Embed(
                    description=f"Hmm, let's take a look around this area, I have a feeling that we might get something...\n\n", color=color)
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(
                    description=f"Hmm, let's take a look around this area, I have a feeling that we might get something...\n\n"
                                f"- Blackberries: {blackberry}\n", color=color)
                await msg.edit(embed=embed)
                embed = discord.Embed(
                    description=f"Hmm, let's take a look around this area, I have a feeling that we might get something...\n\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n", color=color)
                await msg.edit(embed=embed)
                embed = discord.Embed(
                    description=f"Hmm, let's take a look around this area, I have a feeling that we might get something...\n\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n", color=color)
                await msg.edit(embed=embed)
                embed = discord.Embed(
                    description=f"Hmm, let's take a look around this area, I have a feeling that we might get something...\n\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n"
                                f"- Raspberries: {raspberry}\n", color=color)
                await msg.edit(embed=embed)
                embed = discord.Embed(
                    description=f"Hmm, let's take a look around this area, I have a feeling that we might get something...\n\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n"
                                f"- Raspberries: {raspberry}\n"
                                f"- Dcash: {dCash}", color=color)
                await msg.edit(embed=embed)
                embed = discord.Embed(
                    description=f"Hmm, let's take a look around this area, I have a feeling that we might get something...\n\n"
                                f"- Blackberries: {blackberry}\n"
                                f"- Blueberries: {blueberry}\n"
                                f"- Blackcurrants: {blackcurrant}\n"
                                f"- Raspberries: {raspberry}\n"
                                f"- Dcash: {dCash}\n"
                                f"All the items added in the inventory. Use `!inventory` to check your amount.", color=color)
                await msg.edit(embed=embed)

                cursor.execute(
                    f"UPDATE inventory SET blackberry = blackberry + '{blackberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET blueberry = blueberry + '{blueberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET blackcurrant = blackcurrant + '{blackcurrant}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE inventory SET raspberry = raspberry + '{raspberry}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(
                    f"UPDATE users SET Dcash = Dcash + '{dCash}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
            else:
                em = discord.Embed(
                    description=f"Hmm, let's take a look around this area, I have a feeling that we might get something...\n\n",
                    color=15158332)
                msg = await ctx.send(embed=em)
                await asyncio.sleep(1)
                em = discord.Embed(
                    description=f"Hmm, let's take a look around this area, I have a feeling that we might get something...\n\n"
                                f"uffff.. I really didn't find anything. How unfortunate this is.",
                    color=15158332)
                await msg.edit(embed=em)

@search.error
async def search_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(description=f"{ctx.message.author.mention} you can search again in `{round(error.retry_after/60)} minutes`.", color=15158332)
        await ctx.send(embed=em)


@client.command(brief="Showing top 10 highest level dragons from the server",aliases=['Leaderboard','LEADERBOARD'])
async def leaderboard(ctx):
    if int(ctx.channel.id) == int(gameChannel):
        cursor.execute(f"SELECT dragonXP FROM users ORDER BY dragonXP DESC")
        allUsers = cursor.fetchall()
        cursor.execute(f"SELECT dragonName FROM users ORDER BY dragonXP DESC")
        allDragonS = cursor.fetchall()
        cursor.execute(f"SELECT userID FROM users ORDER BY dragonXP DESC")
        allUsersIDD = cursor.fetchall()
        allXPs = []
        allDragonNames =[]
        allUsersIDs =[]
        for user in allUsers:
            allXPs.append(user[0])
        for dragonName in allDragonS:
            allDragonNames.append(dragonName[0])
        for userID in allUsersIDD:
            member = await client.fetch_user(userID[0])
            allUsersIDs.append(member.name)
        noUsers = len(allUsers)
        embed = discord.Embed(description="Leaderboard | Top10",color=color)
        x = 0
        while x < noUsers and x < 10:
            embed.add_field(name=f"#{int(x)+1}",value=f"Owner: **{allUsersIDs[x]}**\n"
                                                      f"Dragon: **{allDragonNames[x]}**\n"
                                                      f"XP: **{allXPs[x]}**")
            x+=1
        file = discord.File("leaderboard.png", filename="leaderboard.png")
        embed.set_thumbnail(url="attachment://leaderboard.png")
        await ctx.send(file=file, embed=embed)


@client.command(brief="Player vs Player fights for Dcash",aliases=['Fight','FIGHT'])
async def fight(ctx,member:discord.Member, amount):
    cursor.execute(f"SELECT firstUserID FROM activeFights WHERE firstUserID = '{ctx.message.author.id}'")
    check1 = cursor.fetchone()
    cursor.execute(f"SELECT secondUserID FROM activeFights WHERE secondUserID = '{ctx.message.author.id}'")
    check2 = cursor.fetchone()
    cursor.execute(f"SELECT firstUserID FROM activeFights WHERE firstUserID = '{member.id}'")
    check3 = cursor.fetchone()
    cursor.execute(f"SELECT secondUserID FROM activeFights WHERE secondUserID = '{member.id}'")
    check4 = cursor.fetchone()
    if check1 is None and check2 is None and check3 is None and check4 is None:
        if int(ctx.channel.id) == int(gameChannel):
            cursor.execute(f"SELECT firstUserID FROM fightsQ WHERE firstUserID = '{ctx.message.author.id}' AND secondUserID ='{member.id}'")
            checkActive = cursor.fetchone()
            if checkActive is None:
                cursor.execute(f"SELECT Dcash FROM users WHERE userID = '{ctx.message.author.id}'")
                checkCash = cursor.fetchone()
                if checkCash is None:
                    em = discord.Embed(
                        description=f"{ctx.message.author.mention} you have to hatch your dragon first, do it using `!hatch <name>`.",
                        color=15158332)
                    await ctx.send(embed=em)
                else:

                    if int(checkCash[0]) < int(amount):
                        em = discord.Embed(
                            description=f"{ctx.message.author.mention} you don't have enough Dcash.",
                            color=15158332)
                        await ctx.send(embed=em)
                    else:
                        cursor.execute(f"SELECT Dcash FROM users WHERE userID = '{member.id}'")
                        checkMember = cursor.fetchone()
                        if checkMember is None:
                            em = discord.Embed(
                                description=f"{ctx.message.author.mention} the member you provoked does not have a dragon yet.",
                                color=15158332)
                            await ctx.send(embed=em)
                        else:
                            cursor.execute(f"INSERT INTO fightsQ (firstUserID,secondUserID,amount) VALUES ('{ctx.message.author.id}','{member.id}','{amount}')")
                            db.commit()
                            cursor.execute(
                                f"UPDATE users SET Dcash = Dcash - '{amount}' WHERE userID = '{ctx.message.author.id}'")
                            db.commit()
                            em = discord.Embed(
                                description=f"{ctx.message.author.mention} provoked {member.mention} in a 1v1 duel. Use `!accept @user`",
                                color=color)
                            await ctx.send(embed=em)
            else:
                em = discord.Embed(
                    description=f"{ctx.message.author.mention} you already provoked {member.mention}. Wait for his reply.",
                    color=15158332)
                await ctx.send(embed=em)
    else:
        em = discord.Embed(
            description=f"{ctx.message.author.mention} you or {member.mention} are already in a fight, finish that before starting new one.",
            color=15158332)
        await ctx.send(embed=em)

@client.command(brief = "Accepts a fight that the user started",aliases=['Accept','ACCEPT'])
async def accept(ctx,member:discord.Member):
    if int(ctx.channel.id) == int(gameChannel):

        cursor.execute(f"SELECT firstUserID FROM fightsQ WHERE secondUserID = '{ctx.message.author.id}'")
        checkFight = cursor.fetchone()
        cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{ctx.message.author.id}'")
        firstDragon = cursor.fetchone()[0]
        cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{member.id}'")
        secondDragon = cursor.fetchone()[0]
        if checkFight is None:
            em = discord.Embed(
                description=f"{ctx.message.author.mention} the respective user did not provoke you. You can provoke him using `!fight @user <amountDcash>`",
                color=15158332)
            await ctx.send(embed=em)
        else:
            cursor.execute(f"SELECT amount FROM fightsQ WHERE secondUserID = '{ctx.message.author.id}'")
            amount = cursor.fetchone()[0]
            cursor.execute(f"SELECT Dcash FROM users WHERE userID = '{ctx.message.author.id}'")
            amountowned = cursor.fetchone()[0]
            if int(amount) > int(amountowned):
                em = discord.Embed(
                    description=f"{ctx.message.author.mention} you don't have enough Dcash to accept the fight.",
                    color=15158332)
                await ctx.send(embed=em)
            else:
                category = discord.utils.get(ctx.guild.categories,name="Dragon Active Fights")
                if category is None:
                    category = await ctx.guild.create_category('Dragon Active Fights')
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.message.author: discord.PermissionOverwrite(read_messages=True),
                    member:discord.PermissionOverwrite(read_messages=True)
                }
                channel = await ctx.guild.create_text_channel(f"{ctx.message.author.name} vs {member.name}",overwrites=overwrites,category=category)


                cursor.execute(f"SELECT health FROM users WHERE userID = '{ctx.message.author.id}'")
                healthone = cursor.fetchone()[0]
                cursor.execute(f"SELECT health FROM users WHERE userID = '{member.id}'")
                healthtwo = cursor.fetchone()[0]
                cursor.execute(f"UPDATE users SET Dcash = Dcash - '{amount}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()

                firstHP = int(healthone) + 100
                secondHP = int(healthtwo) + 100
                cursor.execute(f"INSERT INTO activeFights (firstUserID,secondUserID, channelID, firstHP, secondHP, turn,def1,def2,amount,firstDef,secondDef) VALUES ('{ctx.message.author.id}','{member.id}','{channel.id}','{firstHP}','{secondHP}','{ctx.message.author.id}','0','0','{amount}','0','0')")
                db.commit()
                cursor.execute(f"DELETE FROM fightsQ WHERE firstUserID = '{member.id}' AND secondUserID = '{ctx.message.author.id}' ")
                db.commit()
                await channel.send(f"{ctx.message.author.mention} and {member.mention}")
                embed = discord.Embed(title = f"{ctx.message.author.name} vs {member.name}",description="Welcome to the ARENA\n\n"
                                                                                                        f"**{ctx.message.author.mention}** along with **{firstDragon}**\n"
                                                                                                        f"**{member.mention}** along with **{secondDragon}**\n"
                                                                                                        "The rules are simple, do your best to defeat the opponent.\n"
                                                                                                        "Possible Actions:\n"
                                                                                                        "- `!attack` > Using attack to decrease opponent HP\n"
                                                                                                        "- `!defend` > Using defend, you have a chance to dodge the next attack\n"
                                                                                                        "- `!heal <item>` > Using heal to increase your current HP\n\n"
                                                                                                        f"{ctx.message.author.mention} has the first turn.\n"
                                                                                                        f"FIGHT!")
                await channel.send(embed=embed)
                embedMention = discord.Embed(description=f"Hi {ctx.message.author.mention},\n\n"
                                                  f"Your fight against {member.id} started\n"
                                                         f"Please go to {channel.mention} and follow the instructions.\n\n"
                                                         f"GOOD LUCK!",color=color)
                await ctx.message.author.send(embed=embedMention)
                embedMember = discord.Embed(description=f"Hi {member.mention},\n\n"
                                                         f"Your fight against {ctx.message.author.id} started\n"
                                                         f"Please go to {channel.mention} and follow the instructions.\n\n"
                                                         f"GOOD LUCK!", color=color)
                await member.send(embed=embedMember)


@client.command(brief="While in active fight, use this to attack the enemy dragon",aliases=['Attack','ATTACK'])
async def attack(ctx):
    cursor.execute(f"SELECT turn FROM activeFights WHERE channelID = '{ctx.channel.id}'")
    checkTurn = cursor.fetchone()
    cursor.execute(f"SELECT firstUserID FROM activeFights WHERe channelID = '{ctx.channel.id}'")
    first = cursor.fetchone()[0]
    cursor.execute(f"SELECT secondUserID FROM activeFights WHERe channelID = '{ctx.channel.id}'")
    second = cursor.fetchone()[0]
    if int(first) == (checkTurn[0]):
        cursor.execute(f"SELECT secondUserID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
        enemy = cursor.fetchone()
    else:
        cursor.execute(f"SELECT firstUserID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
        enemy = cursor.fetchone()
    cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{ctx.message.author.id}'")
    firstDragon = cursor.fetchone()[0]
    cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{enemy[0]}'")
    secondDragon = cursor.fetchone()[0]
    enemyMember = await client.fetch_user(enemy[0])
    category = discord.utils.get(ctx.guild.categories, name="Dragon Active Fights")
    if ctx.message.channel.category == category:
        if int(checkTurn[0]) != int(ctx.message.author.id):
            em = discord.Embed(
                description=f"{ctx.message.author.mention} doesn't seem to be your turn. Wait for the opponent.",
                color=15158332)
            await ctx.send(embed=em)
        else:
            cursor.execute(f"SELECT firstDef FROM activeFights WHERE channelID = '{ctx.channel.id}'")
            firstDef = cursor.fetchone()[0]
            cursor.execute(f"SELECT secondDef FROM activeFights WHERE channelID = '{ctx.channel.id}'")
            secondDef = cursor.fetchone()[0]

            cursor.execute(f"SELECT damage FROM users WHERE userID = '{first}'")
            firstdmg = cursor.fetchone()[0]
            cursor.execute(f"SELECT armor FROM users WHERE userID = '{first}'")
            firstarmor = cursor.fetchone()[0]
            cursor.execute(f"SELECT dexterity FROM users WHERE userID = '{first}'")
            firstdex = cursor.fetchone()[0]
            cursor.execute(f"SELECT health FROM users WHERE userID = '{first}'")
            firsthealth = cursor.fetchone()[0]
            cursor.execute(f"SELECT inteligence FROM users WHERE userID = '{first}'")
            firstintelligence = cursor.fetchone()[0]

            cursor.execute(f"SELECT damage FROM users WHERE userID = '{second}'")
            seconddmg = cursor.fetchone()[0]
            cursor.execute(f"SELECT armor FROM users WHERE userID = '{second}'")
            secondarmor = cursor.fetchone()[0]
            cursor.execute(f"SELECT dexterity FROM users WHERE userID = '{second}'")
            seconddex = cursor.fetchone()[0]
            cursor.execute(f"SELECT health FROM users WHERE userID = '{second}'")
            secondhealth = cursor.fetchone()[0]
            cursor.execute(f"SELECT inteligence FROM users WHERE userID = '{second}'")
            secondintelligence = cursor.fetchone()[0]
            dodgeReason = "ahh, it wasn't"

            if int(first) == int(ctx.message.author.id):
                if int(secondDef) == 1:
                    chances = [range(0,1),range(0,1),range(10,15)]
                    attpower = random.choice(random.choice(chances))
                    if attpower != 1 and attpower != 0:
                        if seconddex > 0:
                            dexOptions = list(seconddex*"0")
                            NonDexOptions = list((100-seconddex)*"1")
                            chancesWithDex = list(dexOptions+NonDexOptions)
                            finalChances = random.choice(chancesWithDex)
                            if finalChances == 0:
                                attpower=0
                                dodgeReason = "Indeed, a dodge due to **enemy's dexterity**."
                            else:
                                attpower = (attpower + firstdmg) - secondarmor

                    elif attpower == 0 or attpower == 1:
                        cursor.execute(F"UPDATE activeFights SET secondDef = '0' WHERE channelID = '{ctx.channel.id}'")
                        db.commit()
                        dodgeReason = "Indeed, a Dodge due to enemy's earlier **defense play**."
                else:
                    attpower = random.choice(range(10, 15))
                    attpower = (attpower + firstdmg) - secondarmor
                    if seconddex > 0:
                        dexOptions = list(seconddex * "0")
                        NonDexOptions = list((100 - seconddex) * "1")
                        chancesWithDex = list(dexOptions + NonDexOptions)
                        finalChances = random.choice(chancesWithDex)
                        if int(finalChances) == 0:
                            attpower = 0
                            dodgeReason = "Indeed, a Dodge due to **enemy's dexterity**."
                        else:
                            attpower = (attpower + firstdmg) - secondarmor
            elif int(second) == int(ctx.message.author.id):
                if int(firstDef) == 1:
                    chances = [range(0, 1),range(0, 1), range(10, 15)]
                    attpower = random.choice(random.choice(chances))
                    if attpower != 1 and attpower != 0:
                        if firstdex > 0:
                            dexOptions = list(firstdex*"0")
                            NonDexOptions = list((100-firstdex)*"1")
                            chancesWithDex = list(dexOptions+NonDexOptions)
                            finalChances = random.choice(chancesWithDex)
                            if finalChances == 0:
                                attpower=0
                                dodgeReason = "Indeed, a Dodge due to **enemy's dexterity**."
                            else:
                                attpower = (attpower + seconddmg) - firstarmor

                    if attpower == 0 or attpower == 1:
                        cursor.execute(F"UPDATE activeFights SET firstDef = '0' WHERE channelID = '{ctx.channel.id}'")
                        db.commit()
                        dodgeReason = "Indeed, a Dodge due to enemy's earlier **defense play**."
                else:
                    attpower = random.choice(range(10, 15))
                    attpower = (attpower + seconddmg) - firstarmor
                    if firstdex > 0:
                        dexOptions = list(firstdex * "0")
                        NonDexOptions = list((100 - firstdex) * "1")
                        chancesWithDex = list(dexOptions + NonDexOptions)
                        finalChances = random.choice(chancesWithDex)
                        if int(finalChances) == 0:
                            attpower = 0
                            dodgeReason = "Indeed, a Dodge due to **enemy's dexterity**."
                        else:
                            attpower = (attpower + seconddmg) - firstarmor
            else:
                attpower = random.choice(range(10, 15))
                attpower = (attpower + seconddmg) - firstarmor
                if seconddex > 0:
                    dexOptions = list(seconddex * "0")
                    NonDexOptions = list((100 - seconddex) * "1")
                    chancesWithDex = list(dexOptions + NonDexOptions)
                    finalChances = random.choice(chancesWithDex)
                    if int(finalChances) == 0:
                        attpower = 0
                        dodgeReason = "**Indeed, a Dodge due to enemy's dexterity**."
                    else:
                        attpower = (attpower + seconddmg) - firstarmor
            if attpower < 0:
                attpower = 0
            if int(first) == int(ctx.message.author.id):
                cursor.execute(f"UPDATE activeFights SET secondHP = secondHP - '{attpower}' WHERE channelID = '{ctx.channel.id}'")
                db.commit()
            else:
                cursor.execute(
                    f"UPDATE activeFights SET firstHP = firstHP - '{attpower}' WHERE channelID = '{ctx.channel.id}'")
                db.commit()
            cursor.execute(f"SELECT firstHP FROM activeFights WHERE channelID = '{ctx.channel.id}'")
            firstHP = cursor.fetchone()[0]
            cursor.execute(f"SELECT secondHP FROM activeFights WHERE channelID = '{ctx.channel.id}'")
            secondHP = cursor.fetchone()[0]
            cursor.execute(f"UPDATE activeFights SET turn = '{enemy[0]}' WHERE channelID = '{ctx.channel.id}'")
            db.commit()
            if firstHP <= 0:
                cursor.execute(f"SELECT amount FROM activeFights WHERE channelID = '{ctx.channel.id}'")
                amount = cursor.fetchone()[0]
                cursor.execute(f"UPDATE users SET Dcash = Dcash + '{amount}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(f"UPDATE users SET Dcash = Dcash + '{amount}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(f"DELETE FROM activeFights WHERE channelID = '{ctx.channel.id}'")
                db.commit()
                cursor.execute(f"UPDATE fightsRanking SET wins = wins + 1 WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(f"UPDATE fightsRanking SET losses = losses + 1 WHERE userID = '{first}'")
                db.commit()
                cursor.execute(f"SELECT wins FROM fightsRanking WHERE userID = '{ctx.message.author.id}'")
                secondWins = cursor.fetchone()[0]
                cursor.execute(f"SELECT losses FROM fightsRanking WHERE userID = '{ctx.message.author.id}'")
                secondlosses = cursor.fetchone()[0]
                cursor.execute(f"SELECT wins FROM fightsRanking WHERE userID = '{first}'")
                firstWins = cursor.fetchone()[0]
                cursor.execute(f"SELECT losses FROM fightsRanking WHERE userID = '{first}'")
                firstlosses = cursor.fetchone()[0]
                secondRatio = int(secondWins) - int(secondlosses)
                firstRatio = int(firstWins) - int(firstlosses)
                cursor.execute(f"UPDATE fightsRanking SET ratio = {firstRatio} WHERE userID = '{first}'")
                db.commit()
                cursor.execute(f"UPDATE fightsRanking SET ratio = {secondRatio} WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                embed = discord.Embed(description="WHAT A FINAL HIT!\n\n"
                                                  f"**{secondDragon}** takes {firstDragon} down, making {ctx.message.author.mention} the winner!\n"
                                                  f"The bet `{amount} Dcash` also goes to {ctx.message.author.mention}\n\n"
                                                  f"Channel will be deleted in 10 seconds.")
                await ctx.send(embed=embed)
                await asyncio.sleep(10)
                await ctx.channel.delete()
            elif secondHP <= 0:
                cursor.execute(f"SELECT amount FROM activeFights WHERE channelID = '{ctx.channel.id}'")
                amount = cursor.fetchone()[0]
                cursor.execute(f"UPDATE users SET Dcash = Dcash + '{amount}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(f"UPDATE users SET Dcash = Dcash + '{amount}' WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(f"DELETE FROM activeFights WHERE channelID = '{ctx.channel.id}'")
                db.commit()
                cursor.execute(f"UPDATE fightsRanking SET wins = wins + 1 WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                cursor.execute(f"UPDATE fightsRanking SET losses = losses + 1 WHERE userID = '{second}'")
                db.commit()
                cursor.execute(f"SELECT wins FROM fightsRanking WHERE userID = '{ctx.message.author.id}'")
                firstWins = cursor.fetchone()[0]
                cursor.execute(f"SELECT losses FROM fightsRanking WHERE userID = '{ctx.message.author.id}'")
                firstlosses = cursor.fetchone()[0]
                cursor.execute(f"SELECT wins FROM fightsRanking WHERE userID = '{second}'")
                secondWins = cursor.fetchone()[0]
                cursor.execute(f"SELECT losses FROM fightsRanking WHERE userID = '{second}'")
                secondlosses = cursor.fetchone()[0]
                secondRatio = int(secondWins) - int(secondlosses)
                firstRatio = int(firstWins) - int(firstlosses)
                cursor.execute(f"UPDATE fightsRanking SET ratio = {firstRatio} WHERE userID = '{second}'")
                db.commit()
                cursor.execute(
                    f"UPDATE fightsRanking SET ratio = {secondRatio} WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                embed = discord.Embed(description="WHAT A FINAL HIT!\n\n"
                                                  f"**{firstDragon}** takes {secondDragon} down, making {ctx.message.author.mention} the winner!\n"
                                                  f"The bet `{amount} Dcash` also goes to {ctx.message.author.mention}\n\n"
                                                  f"Channel will be deleted in 10 seconds.")
                await ctx.send(embed=embed)
                await asyncio.sleep(10)
                await ctx.channel.delete()
            else:
                if ctx.message.author.id == first:
                    embed = discord.Embed(description=f"{ctx.message.author.mention} used `attack` with **{attpower}** damage.\n\n"
                                                      f"Was that a dodge???\n"
                                                      f"{dodgeReason}\n\n"
                                                      f"{firstDragon} : {firstHP}HP\n"
                                                      f"{secondDragon} : {secondHP}HP\n"
                                                      f"{enemyMember.mention} is your turn.",color=color)
                else:
                    embed = discord.Embed(
                        description=f"{ctx.message.author.mention} used `attack` with **{attpower}** damage.\n\n"
                                    f"Was that a dodge???\n"
                                    f"{dodgeReason}\n\n"
                                    f"{secondDragon} : {firstHP}HP\n"
                                    f"{firstDragon} : {secondHP}HP\n"
                                    f"{enemyMember.mention} is your turn.", color=color)
                await ctx.send(embed=embed)


@client.command(brief="Gives you a chance to dodge the next opponent attack",aliases=['Defend','DEFEND'])
async def defend(ctx):
    cursor.execute(f"SELECT turn FROM activeFights WHERE channelID = '{ctx.channel.id}'")
    checkTurn = cursor.fetchone()
    cursor.execute(f"SELECT firstUserID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
    first = cursor.fetchone()[0]
    cursor.execute(f"SELECT secondUserID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
    second = cursor.fetchone()[0]
    if int(first) == (checkTurn[0]):
        cursor.execute(f"SELECT secondUserID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
        enemy = cursor.fetchone()
    else:
        cursor.execute(f"SELECT firstUserID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
        enemy = cursor.fetchone()
    cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{first}'")
    firstDragon = cursor.fetchone()[0]
    cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{second}'")
    secondDragon = cursor.fetchone()[0]
    enemyMember = await client.fetch_user(enemy[0])
    category = discord.utils.get(ctx.guild.categories, name="Dragon Active Fights")
    if ctx.message.channel.category == category:
        if int(checkTurn[0]) != int(ctx.message.author.id):
            em = discord.Embed(
                description=f"{ctx.message.author.mention} doesn't seem to be your turn. Wait for the opponent.",
                color=15158332)
            await ctx.send(embed=em)
        else:
            attpower = random.choice(range(1, 20))
            if int(first) == int(ctx.message.author.id):
                cursor.execute(
                    f"UPDATE activeFights SET firstDef = '1' WHERE channelID = '{ctx.channel.id}'")
                db.commit()
            else:
                cursor.execute(
                    f"UPDATE activeFights SET secondDef = '1' WHERE channelID = '{ctx.channel.id}'")
                db.commit()
            cursor.execute(f"SELECT firstHP FROM activeFights WHERE channelID = '{ctx.channel.id}'")
            firstHP = cursor.fetchone()[0]
            cursor.execute(f"SELECT secondHP FROM activeFights WHERE channelID = '{ctx.channel.id}'")
            secondHP = cursor.fetchone()[0]
            cursor.execute(f"SELECT firstUserID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
            firstPlayer = cursor.fetchone()[0]
            firstMember = await client.fetch_user(int(firstPlayer))
            cursor.execute(f"SELECT secondUserID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
            secondPlayer = cursor.fetchone()[0]
            secondMember = await client.fetch_user(int(secondPlayer))
            cursor.execute(f"UPDATE activeFights SET turn = '{enemy[0]}' WHERE channelID = '{ctx.channel.id}'")
            db.commit()

            embed = discord.Embed(
                description=f"{ctx.message.author.mention} used `defend`. Giving him a chance to dodge the future attacks.\n\n"
                            f"{secondDragon} : {secondHP}HP\n"
                            f"{firstDragon} : {firstHP}HP\n"
                            f"{enemyMember.mention} is your turn.", color=color)
            await ctx.send(embed=embed)


@client.command(brief="Use an item from inventory to heal up",aliases=['Heal','HEAL'])
async def heal(ctx,item):
    item = item.lower()
    cursor.execute(f"SELECT {item} FROM inventory WHERE userID = '{ctx.message.author.id}'")
    checkItem = cursor.fetchone()
    if int(checkItem[0]) < 1:
        em = discord.Embed(
            description=f"{ctx.message.author.mention} you don't have {item} in your inventory.",
            color=15158332)
        await ctx.send(embed=em)
    else:
        cursor.execute(f"SELECT turn FROM activeFights WHERE channelID = '{ctx.channel.id}'")
        checkTurn = cursor.fetchone()
        cursor.execute(f"SELECT firstUserID FROM activeFights WHERe channelID = '{ctx.channel.id}'")
        first = cursor.fetchone()[0]
        cursor.execute(f"SELECT secondUserID FROM activeFights WHERe channelID = '{ctx.channel.id}'")
        second = cursor.fetchone()[0]
        if int(first) == (checkTurn[0]):
            cursor.execute(f"SELECT secondUserID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
            enemy = cursor.fetchone()
        else:
            cursor.execute(f"SELECT firstUserID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
            enemy = cursor.fetchone()
        cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{first}'")
        firstDragon = cursor.fetchone()[0]
        cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{second}'")
        secondDragon = cursor.fetchone()[0]
        enemyMember = await client.fetch_user(enemy[0])
        category = discord.utils.get(ctx.guild.categories, name="Dragon Active Fights")
        if ctx.message.channel.category == category:
            if int(checkTurn[0]) != int(ctx.message.author.id):
                em = discord.Embed(
                    description=f"{ctx.message.author.mention} doesn't seem to be your turn. Wait for the opponent.",
                    color=15158332)
                await ctx.send(embed=em)
            else:
                cursor.execute(f"SELECT inteligence FROM users WHERE userID = '{ctx.message.author.id}'")
                intelligence = cursor.fetchone()
                if item == "blackberry":
                    attpower = 20 + int(intelligence[0])
                elif item == "blueberry":
                    attpower = 15 + int(intelligence[0])
                elif item == "blackcurrant":
                    attpower = 10 + int(intelligence[0])
                elif item == "raspberry":
                    attpower = 5 + int(intelligence[0])
                if int(first) == int(ctx.message.author.id):
                    cursor.execute(f"UPDATE activeFights SET firstHP = firstHP + '{attpower}' WHERE channelID = '{ctx.channel.id}'")
                    db.commit()
                else:
                    cursor.execute(
                        f"UPDATE activeFights SET secondHP = secondHP + '{attpower}' WHERE channelID = '{ctx.channel.id}'")
                    db.commit()
                cursor.execute(f"SELECT firstHP FROM activeFights WHERE channelID = '{ctx.channel.id}'")
                firstHP = cursor.fetchone()[0]
                cursor.execute(f"SELECT secondHP FROM activeFights WHERE channelID = '{ctx.channel.id}'")
                secondHP = cursor.fetchone()[0]
                cursor.execute(f"UPDATE activeFights SET turn = '{enemy[0]}' WHERE channelID = '{ctx.channel.id}'")
                db.commit()
                cursor.execute(f"UPDATE inventory SET {item} = {item} - 1 WHERE userID = '{ctx.message.author.id}'")
                db.commit()
                if ctx.message.author.id == first:
                    embed = discord.Embed(description=f"{ctx.message.author.mention} healed with **{item}** for **{attpower}**.\n\n"
                                                      f"{secondDragon} : {secondHP}HP\n"
                                                      f"{firstDragon} : {firstHP}HP\n"
                                                      f"{enemyMember.mention} is your turn.",color=color)
                else:
                    embed = discord.Embed(
                        description=f"{ctx.message.author.mention} healed with **{item}** for **{attpower}**.\n\n"
                                    f"{secondDragon} : {secondHP}HP\n"
                                    f"{firstDragon} : {firstHP}HP\n"
                                    f"{enemyMember.mention} is your turn.", color=color)
                await ctx.send(embed=embed)


@client.command(brief="Check market price for items.",aliases=['Market','MARKET'])
async def market(ctx):
    if int(ctx.channel.id) == int(gameChannel):
        cursor.execute(f"SELECT blackberry FROM marketPrices WHERE way = 'SELL'")
        sblackberryPrice = cursor.fetchone()[0]
        cursor.execute(f"SELECT blueberry FROM marketPrices WHERE way = 'SELL'")
        sblueberryPrice = cursor.fetchone()[0]
        cursor.execute(f"SELECT blackcurrant FROM marketPrices WHERE way = 'SELL'")
        sblackcurrantPrice = cursor.fetchone()[0]
        cursor.execute(f"SELECT raspberry FROM marketPrices WHERE way = 'SELL'")
        sraspberryPrice = cursor.fetchone()[0]

        cursor.execute(f"SELECT blackberry FROM marketPrices WHERE way = 'BUY'")
        bblackberryPrice = cursor.fetchone()[0]
        cursor.execute(f"SELECT blueberry FROM marketPrices WHERE way = 'BUY'")
        bblueberryPrice = cursor.fetchone()[0]
        cursor.execute(f"SELECT blackcurrant FROM marketPrices WHERE way = 'BUY'")
        bblackcurrantPrice = cursor.fetchone()[0]
        cursor.execute(f"SELECT raspberry FROM marketPrices WHERE way = 'BUY'")
        braspberryPrice = cursor.fetchone()[0]

        embed = discord.Embed(description="WELCOME TO THE MARKET\n"
                                          "Please take a look over our offers:\n\n"
                                          "**WE SELL**\n"
                                          f"- **Blackberry**: `{sblackberryPrice}` Dcash\n"
                                          f"- **Blueberry**: `{sblueberryPrice}` Dcash\n"
                                          f"- **Blackcurrant**: `{sblackcurrantPrice}` Dcash\n"
                                          f"- **Raspberry**: `{sraspberryPrice}` Dcash\n\n"
                                          "**WE BUY**\n"
                                          f"- **Blackberry**: `{bblackberryPrice}` Dcash\n"
                                          f"- **Blueberry**: `{bblueberryPrice}` Dcash\n"
                                          f"- **Blackcurrant**: `{bblackcurrantPrice}` Dcash\n"
                                          f"- **Raspberry**: `{braspberryPrice}` Dcash\n\n"
                                          f"If you want to buy something, you can do it using `!buy <item> <amount>`\n"
                                          f"If you want to sell something, you can od it using  `!sell <item> <amount>`\n"
                                          f"After that items/cash will be available right away in your inventory.",color=color)
        await ctx.send(embed=embed)

@client.command(brief="Admin only command set market price.",aliases=['Setprice','SETPRICE'])
@commands.has_permissions(administrator=True)
async def setprice(ctx,item=None,way=None,price=None):
    item = item.lower()
    way = way.upper()
    cursor.execute(f"SELECT {item} FROM marketPrices")
    checkItem = cursor.fetchone()
    if checkItem is None or way is None or price is None:
        em = discord.Embed(
            description=f"The item {item} either does not exist, or you use the command in a wrong way\n"
                        f"Please use `!setprice <item> <sell/buy> <price>`.\n"
                        f"e.g.: `!setprice raspberry sell 10`",
            color=15158332)
        await ctx.send(embed=em)
    else:
        cursor.execute(f"SELECT {item} FROM marketPrices WHERE way = '{way}'")
        oldPrice = cursor.fetchone()[0]
        cursor.execute(f"UPDATE marketPrices SET {item} = '{price}' WHERE way = '{way}'")
        db.commit()
        embed = discord.Embed(description= "MARKET PRICE UPDATE!\n\n"
                                           f"The price for **{item}** for **{way}** changed to `{price}` Dcash from `{oldPrice}` Dcash",color=color)
        await ctx.send(embed=embed)

@setprice.error
async def setprice_error(ctx, error):
    if isinstance(error, MissingPermissions):
        print(f"{ctx.message.author} tried to run command !setprice")


@client.command(brief="Add your attributes points to your dragon and make it stronger.",aliases=['Addpoinnts','ADDPOINTS','AddPoints'])
async def addpoints(ctx,attributeInput=None,amount:int=0):
    if int(ctx.channel.id) == int(gameChannel):
        if attributeInput is None or amount == 0:
            em = discord.Embed(description=f"Please specify the attribute (**damage/armor/dex/health/int**) and the amount.\n"
                                           f"e.g.: `!addpoints int 2`",
                               color=15158332)
            await ctx.send(embed=em)


        else:
            attributeInput = attributeInput.lower()
            print(attributeInput)
            if attributeInput == "damage" or attributeInput == "dmg":
                attribute = "damage"
            elif attributeInput == "armor":
                attribute = "armor"
            elif attributeInput == "dex" or attributeInput == "dexterity":
                attribute = "dexterity"
            elif attributeInput == "health":
                attribute = "health"
            elif attributeInput == "int" or attributeInput == "intelligence":
                attribute = "inteligence"
            else:
                attribute = "none"

            cursor.execute(f"SELECT {attribute} FROM users WHERE userID = '{ctx.message.author.id}'")
            checkAttr = cursor.fetchone()
            if checkAttr is None:
                em = discord.Embed(description=f"Please specify the attribute (damage/armor/dex/health/int)",
                                   color=15158332)
                await ctx.send(embed=em)
            else:
                cursor.execute(f"SELECT pointsLeft FROM users WHERE userID = '{ctx.message.author.id}'")
                leftPoints = cursor.fetchone()[0]
                if int(leftPoints < amount):
                    em = discord.Embed(description=f"You only have {leftPoints} points left.",
                                       color=15158332)
                    await ctx.send(embed=em)
                else:
                    cursor.execute(f"UPDATE users SET {attribute}={attribute} +  '{amount}' WHERE userID = '{ctx.message.author.id}'")
                    db.commit()
                    cursor.execute(f"UPDATE users SET pointsLeft = pointsLeft - '{amount}' WHERE userID = '{ctx.message.author.id}'")
                    db.commit()
                    embed = discord.Embed(description=f"{ctx.message.author.mention}, you added {amount} points into {attribute} for your dragon.",color=color)
                    await ctx.send(embed=embed)


@client.command(brief="Duels Ranking based on win/lose ratio.",aliases=['Ranking','RANKING'])
async def ranking(ctx):
    if int(ctx.channel.id) == int(gameChannel):
        cursor.execute(f"SELECT userID FROM fightsRanking  ORDER BY ratio DESC LIMIT 10")
        allUsers = cursor.fetchall()
        noUsers = len(allUsers)
        embed = discord.Embed(description="Duel Ranking | Top10", color=color)
        x = 1
        for user in allUsers:
            x += 1
            member = await client.fetch_user(int(user[0]))
            cursor.execute(f"SELECT dragonName FROM users WHERE userID = '{int(user[0])}'")
            dragonName = cursor.fetchone()
            cursor.execute(f"SELECT wins FROM fightsRanking WHERE userID = '{int(user[0])}'")
            wins = cursor.fetchone()
            cursor.execute(f"SELECT losses FROM fightsRanking WHERE userID = '{int(user[0])}'")
            losses = cursor.fetchone()
            ratio = int(wins[0])-int(losses[0])
            embed.add_field(name=f"#{int(x)-1}", value=f"Player: **{member.mention}**\n"
                                                         f"Dragon: **{dragonName[0]}**\n"
                                                         f"Wins: **{wins[0]}** "
                                                         f"Losses: **{losses[0]}**\n"
                                                         f"Ratio: **{ratio}** ")
        file = discord.File("leaderboard.png", filename="leaderboard.png")
        embed.set_thumbnail(url="attachment://leaderboard.png")
        await ctx.send(file=file, embed=embed)


@client.command(brief="Sells items for Dcash",aliases=['Sell','SELL'])
async def sell(ctx,item=None,amount=0):
    if int(ctx.channel.id) == int(gameChannel):
        if item is None or amount == 0:
            em = discord.Embed(
                description=f"The item **{item}** either does not exist, or you use the command in a wrong way\n"
                            f"Please use `!sell <item> <amount>`.\n"
                            f"e.g.: `!sell raspberry 5`",
                color=15158332)
            await ctx.send(embed=em)
        else:
            cursor.execute(f"SELECT firstUserID FROM activeFights WHERE firstUserID = '{ctx.message.author.id}'")
            check1 = cursor.fetchone()
            cursor.execute(f"SELECT secondUserID FROM activeFights WHERE secondUserID = '{ctx.message.author.id}'")
            check2 = cursor.fetchone()
            if check1 is None and check2 is None:
                item = item.lower()
                cursor.execute(f"SELECT {item} FROM inventory WHERE userID = '{ctx.message.author.id}'")
                itemCheck = cursor.fetchone()
                if itemCheck is None:
                    em = discord.Embed(
                        description=f"{item} does not exist.", color=15158332)
                    await ctx.send(embed=em)
                else:
                    if int(itemCheck[0]) < amount:
                        em = discord.Embed(
                            description=f"You do not have **{amount} {item}** in your inventory. ",color=15158332)
                        await ctx.send(embed=em)
                    else:
                        cursor.execute(f"SELECT {item} FROM marketPrices WHERE way = 'BUY'")
                        price = cursor.fetchone()[0]
                        cursor.execute(f"UPDATE inventory SET {item} = {item}-'{amount}' WHERE userID = '{ctx.message.author.id}'")
                        db.commit()
                        totalPrice = int(price) * amount
                        cursor.execute(f"UPDATE users SET Dcash = Dcash + {totalPrice} WHERE userID = '{ctx.message.author.id}'")
                        db.commit()
                        em = discord.Embed(
                            description=f"{ctx.message.author.mention} sold **{amount} {item}** for **{totalPrice}** Dcash",
                            color=15158332)
                        await ctx.send(embed=em)
            else:
                em = discord.Embed(
                    description=f"{ctx.message.author.mention} you can't sell while in a fight.",
                    color=15158332)
                await ctx.send(embed=em)


@client.command(brief="Buy items with Dcash",aliases=['Buy','BUY'])
async def buy(ctx,item=None,amount=0):
    if int(ctx.channel.id) == int(gameChannel):
        if item is None or amount == 0:
            em = discord.Embed(
                description=f"The item {item} either does not exist, or you use the command in a wrong way\n"
                            f"Please use `!buy <item> <amount>`.\n"
                            f"e.g.: `!buy raspberry 5`",
                color=15158332)
            await ctx.send(embed=em)
        else:
            cursor.execute(f"SELECT firstUserID FROM activeFights WHERE firstUserID = '{ctx.message.author.id}'")
            check1 = cursor.fetchone()
            cursor.execute(f"SELECT secondUserID FROM activeFights WHERE secondUserID = '{ctx.message.author.id}'")
            check2 = cursor.fetchone()
            if check1 is None and check2 is None:
                item = item.lower()
                cursor.execute(f"SELECT {item} FROM marketPrices")
                itemCheck = cursor.fetchone()
                if itemCheck is None:
                    em = discord.Embed(
                        description=f"{item} does not exist.", color=15158332)
                    await ctx.send(embed=em)
                else:
                    cursor.execute(f"SELECT {item} FROM marketPrices WHERE way = 'SELL'")
                    price = cursor.fetchone()[0]
                    totalPrice = int(price) * amount
                    cursor.execute(f"SELECT Dcash FROM users WHERE userID = '{ctx.message.author.id}'")
                    cash = cursor.fetchone()[0]
                    if totalPrice > int(cash):
                        em = discord.Embed(
                            description=f"You do not **{totalPrice} Dcash** to pay for **{amount} {item}**.", color=15158332)
                        await ctx.send(embed=em)
                    else:
                        cursor.execute(f"UPDATE users SET Dcash = Dcash - {totalPrice} WHERE userID = '{ctx.message.author.id}'")
                        db.commit()
                        cursor.execute(
                            f"UPDATE inventory SET {item} = {item} + '{amount}' WHERE userID = '{ctx.message.author.id}'")
                        db.commit()
                        em = discord.Embed(
                            description=f"{ctx.message.author.mention} bought **{amount} {item}** for **{totalPrice} Dcash**",
                            color=15158332)
                        await ctx.send(embed=em)
            else:
                em = discord.Embed(
                    description=f"{ctx.message.author.mention} you can't buy while in a fight.",
                    color=15158332)
                await ctx.send(embed=em)

@client.command(brief="Trade with other players items for items.",aliases=['Trade','TRADE'])
async def trade(ctx,member:discord.Member=None,itemGive=None,amountGive=None,itemGet=None,amountGet=None):
    if member is None or itemGive is None or amountGive is None or itemGet is None or amountGet is None:
        em = discord.Embed(
            description=f"The item **{itemGive}** either does not exist, or you use the command in a wrong way\n"
                        f"Please use `!trade @user <itemToGive> <amountToGive> <itemToGet> <amountToGet>`.\n"
                        f"e.g.: `!buy @TagSomeone raspberry 5 blackberry 1`",
            color=15158332)
        await ctx.send(embed=em)
    else:
        cursor.execute(f"SELECT {itemGive} FROM inventory WHERE userID = '{ctx.message.author.id}'")
        checkItem = cursor.fetchone()
        if int(checkItem[0]) < int(amountGive):
            em = discord.Embed(
                description=f"You do not have {amountGive} {itemGive}to trade.",color=15158332)
            await ctx.send(embed=em)
        else:
            cursor.execute(f"SELECT {itemGet} FROM inventory WHERE userID = '{member.id}'")
            checkGet = cursor.fetchone()
            if checkGet is None:
                em = discord.Embed(
                    description=f"User either does not exist, not having a dragon yet or you use the command in a wrong way\n"
                                f"Please use `!trade @user <itemToGive> <amountToGive> <itemToGet> <amountToGet>`.\n"
                                f"e.g.: `!trade @TagSomeone raspberry 5 blackberry 1`",
                    color=15158332)
                await ctx.send(embed=em)
            else:
                if int(checkGet[0]) < int(amountGet):
                    em = discord.Embed(
                        description=f"User do not have {amountGet} {itemGet}to trade.", color=15158332)
                    await ctx.send(embed=em)
                else:
                    cursor.execute(f"INSERT INTO openTrades (firstUserID, secondUserID, itemToGive, amountToGive, itemToGet, amountToGet)"
                                   f"VALUES ('{ctx.message.author.id}','{member.id}','{itemGive}','{amountGive}','{itemGet}','{amountGet}')")
                    db.commit()
                    em = discord.Embed(
                        description=f"{ctx.message.author.mention} wants to trade with {member.mention}, **{amountGive} {itemGive}** for **{amountGet} {itemGet}**.",
                        color=color)
                    await ctx.send(embed=em)

@trade.error
async def trade_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        em = discord.Embed(
            description=f"User either does not exist, or you use the command in a wrong way\n"
                        f"Please use `!trade @user <itemToGive> <amountToGive> <itemToGet> <amountToGet>`.\n"
                        f"e.g.: `!trade @TagSomeone raspberry 5 blackberry 1`",
            color=15158332)
        await ctx.send(embed=em)
    elif isinstance(error, commands.BadArgument):
        em = discord.Embed(
            description=f"User either does not exist, or you use the command in a wrong way\n"
                        f"Please use `!trade @user <itemToGive> <amountToGive> <itemToGet> <amountToGet>`.\n"
                        f"e.g.: `!trade @TagSomeone raspberry 5 blackberry 1`",
            color=15158332)
        await ctx.send(embed=em)

@client.command(brief="Accept and active trade with other player",aliases=['Accepttrade','ACCEPTTRADE','AcceptTrade'])
async def accepttrade(ctx,member:discord.Member=None):
    if member is None:
        em = discord.Embed(
            description=f"User either does not exist, or you use the command in a wrong way\n"
                        f"Please use `!accepttrade @user`.\n",
            color=15158332)
        await ctx.send(embed=em)
    else:
        cursor.execute(f"SELECT firstUserID FROM openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
        check = cursor.fetchone()
        if check is None:
            em = discord.Embed(
                description=f"No active trade with this user",color=15158332)
            await ctx.send(embed=em)
        else:
            cursor.execute(f"SELECT itemToGive from openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
            itemToGive = cursor.fetchone()
            cursor.execute(
                f"SELECT amountToGive from openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
            amountToGive = cursor.fetchone()

            cursor.execute(
                f"SELECT itemToGet from openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
            itemToGet = cursor.fetchone()
            cursor.execute(
                f"SELECT amountToGet from openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
            amountToGet = cursor.fetchone()

            cursor.execute(f"UPDATE inventory SET {itemToGive[0]} = {itemToGive[0]} - '{amountToGive[0]}' WHERE userID = '{member.id}'")
            db.commit()
            cursor.execute(
                f"UPDATE inventory SET {itemToGet[0]} = {itemToGet[0]} + '{amountToGet[0]}' WHERE userID = '{member.id}'")
            db.commit()

            cursor.execute(
                f"UPDATE inventory SET {itemToGive[0]} = {itemToGive[0]} + '{amountToGive[0]}' WHERE userID = '{ctx.message.author.id}'")
            db.commit()
            cursor.execute(
                f"UPDATE inventory SET {itemToGet[0]} = {itemToGet[0]} - '{amountToGet[0]}' WHERE userID = '{ctx.message.author.id}'")
            db.commit()

            cursor.execute(f"DELETE FROM openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
            db.commit()

            em = discord.Embed(
                description=f"{ctx.message.author.mention} accepts the trade with {member.mention}."
                            f"{member.mention} gives **{amountToGive[0]} {itemToGive[0]}** to {ctx.message.author.mention} for **{amountToGet[0]} {itemToGet[0]}**",
                color=color)
            await ctx.send(embed=em)

@client.command(brief="Checks if you have an active trade with particular user.",aliases=['Checktrade','CHECKTRADE','CheckTrade'])
async def checktrade(ctx,member:discord.Member=None):
    if member is None:
        em = discord.Embed(
            description=f"User either does not exist, or you use the command in a wrong way\n"
                        f"Please use `!accepttrade @user`.\n",
            color=15158332)
        await ctx.send(embed=em)
    else:
        cursor.execute(f"SELECT firstUserID FROM openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
        check = cursor.fetchone()
        if check is None:
            em = discord.Embed(
                description=f"No active trade with this user", color=15158332)
            await ctx.send(embed=em)
        else:
            cursor.execute(
                f"SELECT itemToGive from openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
            itemToGive = cursor.fetchone()
            cursor.execute(
                f"SELECT amountToGive from openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
            amountToGive = cursor.fetchone()

            cursor.execute(
                f"SELECT itemToGet from openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
            itemToGet = cursor.fetchone()
            cursor.execute(
                f"SELECT amountToGet from openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
            amountToGet = cursor.fetchone()

            em = discord.Embed(
                description=f"{ctx.message.author.mention} you have an active trade with {member.mention}.\n"
                            f"You get **{amountToGet[0]} {itemToGet[0]}** for **{amountToGive[0]} {itemToGive[0]}** ",color=color)
            await ctx.send(embed=em)

@checktrade.error
async def trade_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        em = discord.Embed(
            description=f"User either does not exist, or you use the command in a wrong way\n"
                        f"Please use `!checktrade @member.\n",color=15158332)
        await ctx.send(embed=em)

@client.command(brief="Refuse a trade",aliases=['Refusetrade','REFUSETRADE','RefuseTrade'])
async def refusetrade(ctx,member:discord.Member=None):
    if member is None:
        em = discord.Embed(
            description=f"User either does not exist, or you use the command in a wrong way\n"
                        f"Please use `!accepttrade @user`.\n",
            color=15158332)
        await ctx.send(embed=em)
    else:
        cursor.execute(
            f"SELECT firstUserID FROM openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
        check = cursor.fetchone()
        if check is None:
            em = discord.Embed(
                description=f"No active trade with this user", color=15158332)
            await ctx.send(embed=em)
        else:
            cursor.execute(f"DELETE FROM openTrades WHERE firstUserID = '{member.id}' AND secondUserID ='{ctx.message.author.id}'")
            db.commit()
            em = discord.Embed(
                description=f"{ctx.message.author.mention} rejected {member.mention}'s trade.\n",
                color=color)
            await ctx.send(embed=em)

@refusetrade.error
async def refuse_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        em = discord.Embed(
            description=f"User either does not exist, or you use the command in a wrong way\n"
                        f"Please use `!checktrade @member.\n", color=15158332)
        await ctx.send(embed=em)

@client.command(brief="List all members you have an active trade with",aliases=['Checkalltrades','CHECKALLTRADES'])
async def checkalltrades(ctx):
    cursor.execute(f"SELECT * FROM openTrades WHERE secondUserID = '{ctx.message.author.id}' ")
    allUsers = cursor.fetchall()
    allNames = []
    if allUsers is None:
        em = discord.Embed(
            description=f"You don't have any open trades.", color=15158332)
        await ctx.send(embed=em)
    else:
        for user in allUsers:
            member = await client.fetch_user(int(user[0]))
            allNames.append(member.name)
        embed = discord.Embed(description="This is the list with all members you have an active trade with.\n"
                                                  "You can either accept `!accepttrade @user` or refuse `!refusetrade @user` the trade.\n\n"
                                                  f"List: {allNames}",color=color)
        await ctx.message.author.send(embed=embed)

@client.command(brief="Admin only, force end an active fight",aliases=['Endfight','ENDFIGHT'])
@commands.has_permissions(administrator=True)
async def endfight(ctx):
    cursor.execute(f"SELECT channelID FROM activeFights WHERE channelID = '{ctx.channel.id}'")
    checkFight = cursor.fetchone()
    if checkFight is None:
        pass
    else:
        cursor.execute(f"DELETE FROM activeFights WHERE channelID = '{ctx.channel.id}'")
        db.commit()
        await ctx.channel.delete()


@endfight.error
async def endfight_error(ctx, error):
    if isinstance(error, MissingPermissions):
        print(f"{ctx.message.author} tried to run command !endfight")



@client.command(brief="Admin only, gives cash",aliases=['Givecash','GIVECASH'])
@commands.has_permissions(administrator=True)
async def givecash(ctx,member:discord.Member=None,amount=0):
    if member is None:
        em = discord.Embed(
            description=f"User does not exist",
            color=15158332)
        await ctx.send(embed=em)
    else:
        cursor.execute(f"SELECT Dcash FROM users WHERE userID = '{member.id}'")
        check = cursor.fetchone()
        if check is None:
            em = discord.Embed(
                description=f"User does not exist or is not having a dragon yet.",
                color=15158332)
            await ctx.send(embed=em)
        else:
            if type(amount) is not int:
                em = discord.Embed(
                    description=f"Amount parameter has to be number.",
                    color=15158332)
                await ctx.send(embed=em)
            else:
                if amount == 0:
                    em = discord.Embed(
                        description=f"Don't forget to specify the amount.",
                        color=15158332)
                    await ctx.send(embed=em)
                else:
                    cursor.execute(f"UPDATE users SET Dcash = Dcash + '{amount}' WHERE userID = '{member.id}'")
                    db.commit()
                    em = discord.Embed(
                        description=f"{ctx.message.author.mention} gave {member.mention} **{amount} Dcash**",
                        color=color)
                    await ctx.send(embed=em)

@givecash.error
async def givecash_error(ctx, error):
    if isinstance(error, MissingPermissions):
        print(f"{ctx.message.author} tried to run command !givecash")
    elif isinstance(error, commands.MemberNotFound):
        em = discord.Embed(
            description=f"User does not exist",
            color=15158332)
        await ctx.send(embed=em)



@client.command(brief="Admin only, gives items",aliases=['Giveitem','GIVEITEM'])
@commands.has_permissions(administrator=True)
async def giveitem(ctx,member:discord.Member=None,item=None,amount=0):
    if member is None:
        em = discord.Embed(
            description=f"User does not exist",
            color=15158332)
        await ctx.send(embed=em)
    else:
        cursor.execute(f"SELECT {item} FROM inventory WHERE userID = '{member.id}'")
        check = cursor.fetchone()
        if check is None:
            em = discord.Embed(
                description=f"User does not exist or is not having a dragon yet.",
                color=15158332)
            await ctx.send(embed=em)
        else:
            if type(amount) is not int:
                em = discord.Embed(
                    description=f"Amount parameter has to be number.",
                    color=15158332)
                await ctx.send(embed=em)
            else:
                if amount == 0:
                    em = discord.Embed(
                        description=f"Don't forget to specify the amount.",
                        color=15158332)
                    await ctx.send(embed=em)
                else:
                    cursor.execute(f"UPDATE inventory SET {item} = {item} + '{amount}' WHERE userID = '{member.id}'")
                    db.commit()
                    em = discord.Embed(
                        description=f"{ctx.message.author.mention} gave {member.mention} **{amount} {item}**",
                        color=color)
                    await ctx.send(embed=em)

@giveitem.error
async def giveitem_error(ctx, error):
    if isinstance(error, MissingPermissions):
        print(f"{ctx.message.author} tried to run command !giveitem")
    elif isinstance(error, commands.MemberNotFound):
        em = discord.Embed(
            description=f"User does not exist",
            color=15158332)
        await ctx.send(embed=em)



@client.command(brief="Shows this message",aliases=['Help','HELP'])
async def help(ctx):
    embed = discord.Embed(description="**COMMANDS LIST**\n\n\n"
                                      "**General Users Commands**\n"
                                      "`!hatch <name>`  Get your Dragon\n"
                                      "`!dragon`  Shows your dragon stats\n"
                                      "`!addpoints <attribute> <amount>`  Add your stat points\n"
                                      "`!stats`  Check stats description\n"
                                      "`!inventory`  Shows your inventory\n"
                                      "`!feed <item> <amount>`  Feeds your dragon for XP\n"
                                      "`!help`  Shows this message\n"
                                      "`!leaderboard`  Top 10 Dragons based on level\n"
                                      "`!ranking`  Top 10 Dragons based on PVP win/lose situation\n"
                                      "`!patch`  Check latest patch notes\n\n"
                                      "**Exchange Users Commands**\n"
                                      "`!market`  Check market prices\n"
                                      "`!buy <item> <amount>`  Buy items from Market\n"
                                      "`!sell <item> <amount>`  Sell items on Market\n"
                                      "`!trade @user <itemToGive> <amountToGive> <itemToGet> <amountToGet>`  Trade with @user\n"
                                      "`!accepttrade @user`  Accept the trade with @user\n"
                                      "`!checktrade @user`  Check the trade with @user again.\n"
                                      "`!refusetrade @user`  Refuse the trade with @user\n"
                                      "`!checkalltrades`  Get a list with all users requested trade with you\n"
                                      "`!uncheck newgame`  Restart the game (REMOVES EVERYTHING, BE CAREFUL)\n"
                                      "**Activities Users Commands**\n"
                                      "`!search`  Randomly search for items around you every 20 minutes\n"
                                      "`!dungeon`  Enter a dungeon at your risk every 20 minutes\n"
                                      "`!fight @user <amount>`  Provoke @user at duel\n"
                                      "`!accept @user`  Accept @user duel request\n\n"
                                      "**During Fight Users Commands**\n"
                                      "`!attack`  Attack enemy dragon\n"
                                      "`!defend`  Gives a high chance to dodge one of the next attacks\n"
                                      "`!heal <item>`  Use items to heal your dragon\n\n"
                                      "**Admin Only Commands**\n"
                                      "`!endfight`  Ends a fight if command run in a fight channel\n"
                                      "`!setprice <item> <SELL/BUY> <price>`  Change Market prices\n"
                                      "`!givecash @user <amount>`  Gives <amount> cash to @user\n"
                                      "`!giveitem @user <item> <amount>`  Gives <amount> of <items> to @user\n",color=color)


    await ctx.channel.send(embed=embed)


@client.command(aliasses=['Unhatch','UNHATCH'])
async def unhatch(ctx,confirmation=None):
    if confirmation is None:
        em = discord.Embed(
            description=f"{ctx.message.author.mention} You are about to:\n"
                        f"- DELETE YOUR DRAGON AND ITS STATS\n"
                        f"- LOSE ALL ITEMS FROM INVENTORY\n"
                        f"- LOSE ALL ITEMS YOU INVESTED IN DRAGON\n"
                        f"- GET REMOVED FROM RANKINGS AND LEADERBOARDS\n"
                        f"If you really want to unhatch your dragon you have to type the confirmation word: `newgame`\n"
                        f"e.g.: `!unhatch newgame`",
            color=15158332)
        await ctx.send(embed=em)
    elif confirmation == "newgame":
        cursor.execute(f"DELETE FROM users WHERE userID = '{ctx.message.author.id}'")
        db.commit()
        cursor.execute(f"DELETE FROM openTrades WHERE firstUserID = '{ctx.message.author.id}'")
        db.commit()
        cursor.execute(f"DELETE FROM openTrades WHERE secondUserID = '{ctx.message.author.id}'")
        db.commit()
        cursor.execute(f"DELETE FROM inventory WHERE UserID = '{ctx.message.author.id}'")
        db.commit()
        cursor.execute(f"DELETE FROM fightsRanking WHERE UserID = '{ctx.message.author.id}'")
        db.commit()
        cursor.execute(f"DELETE FROM fightsQ WHERE firstUserID = '{ctx.message.author.id}'")
        db.commit()
        cursor.execute(f"DELETE FROM fightsQ WHERE secondUserID = '{ctx.message.author.id}'")
        db.commit()
        cursor.execute(f"DELETE FROM activeFights WHERE firstUserID = '{ctx.message.author.id}'")
        db.commit()
        cursor.execute(f"DELETE FROM activeFights WHERE secondUserID = '{ctx.message.author.id}'")
        db.commit()

        em = discord.Embed(
            description=f"{ctx.message.author.mention} is about to start a new journey.\n"
                        f"Please use `!hatch <name>` to enjoy your new dragon.",
            color=color)
        await ctx.send(embed=em)
    elif confirmation != "newgame":
        em = discord.Embed(
            description=f"{ctx.message.author.mention} You are about to:\n"
                        f"- DELETE YOUR DRAGON AND ITS STATS\n"
                        f"- LOSE ALL ITEMS FROM INVENTORY\n"
                        f"- LOSE ALL ITEMS YOU INVESTED IN DRAGON\n"
                        f"- GET REMOVED FROM RANKINGS AND LEADERBOARDS\n"
                        f"If you really want to unhatch your dragon you have to type the confirmation word: `newgame`\n"
                        f"`e.g.: !unhatch newgame`",
            color=15158332)
        await ctx.send(embed=em)

@client.command(aliases=['Patch','PATCH'])
async def patch(ctx):
    embed = discord.Embed(description="**Dragoonz Game Patch Notes**\n"
                                      "*Current Version: 1.3*",color=color)
    embed.add_field(name = "version Alpha 1.0",value="Alpha | First Release")
    embed.add_field(name=" version Alpha 1.1",value="**Bug Fixes**\n"
                                     "- Negative numbers in inventory | bug fixed\n"
                                     "- HP reverse sometimes in fights | bug fixed\n"
                                     "**Adjustments**\n"
                                              "- 1v1 fights can be one at once per member\n"
                                              "**New Implementations**\n"
                                              "- Bot DM users when 1v1 fight starts\n"
                                              "- Added !patch command to keep track of the patch notes",inline=False)
    embed.add_field(name=" version Alpha 1.2", value="**Bug Fixes**\n"
                                                     "- Fights not ending | bug fixed\n"
                                                     "- Market prices not correctly counted (didn't affect so far) | bug fixed\n"
                                                     "- Massive leveling up not giving specific stats points | bug fixed\n"
                                                     "- Ranking started from 2 to 11 instead of 1 to 10 | bug fixed\n"
                                                     "**Adjustments**\n"
                                                     "- People can't buy/sell during a fight.\n",
                    inline=False)
    embed.add_field(name=" version Alpha 1.3", value="**Bug Fixes**\n"
                                                     "- Typo issues | bug fixed\n"
                                                     "- Bet on fights were wrongly addressed sometimes | bug fixed\n"
                                                     "**Upcoming Implementations**\n"
                                                     "- We will add more quests/tasks to get resources from.\n"
                                                     "**New Implementations**\n"
                                                     "- !unhatch command which wipes all your data",
                    inline=False)
    embed.add_field(name="Found a bug?",value="If you find a potential bug, please use the bugs channel below to report it. Thanks!")
    await ctx.send(embed=embed)



client.run(TOKEN)
print(client.user.name)