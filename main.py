import discord
import os 
from discord.ext import commands
import random
from discord import app_commands
import json
import asyncio
from keep_alive import keep_alive
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

anowns_counter = "anowns_count.json"
conf_counter = "conf_count.json"
ask_counter = "ask_count.json"
load_dotenv()

DC_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

description = "Hi I am Eggy your friendly neighborhood programmer!"
bot = commands.Bot(command_prefix='!', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try: 
      synced = await bot.tree.sync()
      print(f"Synced {len(synced)} command(s)")
    except Exception as e:
      print(e)

emoji_channel_id = 1152491024493596674 
emoji_channel = bot.get_channel(emoji_channel_id)

if emoji_channel is not None:
    print(f'Emoji reactions will be monitored in #{emoji_channel.name}')

@bot.command()
async def send_verification_message(ctx):
    if ctx.channel.name == 'verify': 
      
        verification_message = """
        Welcome to the BSIT 2-2N Discord Server! 🎉

To ensure a positive and productive community for our BSIT 2-2N block section, we have a few rules in place:

1. **Respect:** Treat every member of our BSIT 2-2N community with respect and kindness. Harassment, hate speech, and any form of discrimination will not be tolerated.

2. **No Spam:** Please refrain from excessive self-promotion, spamming, or flooding the channels.

3. **Stay On Topic:** Keep discussions relevant to our academic and social interests as BSIT 2-2N students. If you have unrelated questions or topics, use the appropriate channels or create a new one if necessary.

4. **No NSFW Content:** This is a professional and academic environment. Posting explicit, NSFW, or offensive content is strictly prohibited.

5. **No Unauthorized Invites:** Do not invite or share the server link with individuals who are not part of our BSIT 2-2N block section.

6. **Use Channels Wisely:** Please use the designated channels for their intended purposes. If you're unsure, ask a moderator or fellow BSIT 2-2N member.

7. **Be Helpful:** If a fellow BSIT 2-2N student has a question or needs assistance, be polite and offer your help if you can.

8. **No Spoilers:** Respect others' enjoyment of movies, books, or shows by not posting spoilers without proper warnings.

9. **Follow Discord's Terms of Service:** Ensure that your actions on this server comply with Discord's terms and policies.

By reacting with the 👍 emoji below, you agree to abide by these rules and become a valued member of our BSIT 2-2N community. If you have any questions or concerns, feel free to reach out to our friendly moderators. Let's make this server a great place for all BSIT 2-2N students to connect and learn together! 🌟
        """
        message = await ctx.send(verification_message)
        await message.add_reaction('👍')
        await ctx.message.delete()

def get_random_welcome_message():
    welcome_messages = [
        "Welcome to the 2Nighters Server [username] woop woop!",
        "Wazzup wazzup, wazz buzzing [username] welcomee!!",
        "Sheesh, welcome na welcome ka here [username]!",
        "Wala ng intro intro, lezz give it up for [username]!",
        "Nandito na si [username], magbabagsakan in 5..4..3..2..1..",
        "Holabels to the server [username], enjoii kaa here hehe",
        "Boogsh, may nightowl na dumating, koo koo [username]",
        "Uy, HAHA hello [username] welcome welcome!",
        "Hala korean si [username], annyeongahasayo kaen tayo ramyeon?, welcomesayo",
        "Uyy si aighdough [username] andito na!",
        "Welcome aboard [username] di na kami mabobored coz ur here na eh...",
        "Si idol [username] pala ito eh, tugs tugs!!",
        "Wala na, batak yang si [username] mag-code 😏",
        "Oy [username] patingin naman code mo... ibahin ko variables.",
      "Hello bebeloves ko [username] mwuah mwuah"
    ]

    return random.choice(welcome_messages)
  
welcomed_users = {}
async def send_welcome_message(member):
    welcome_channel = bot.get_channel(1152515598128005190)

    if welcome_channel is not None:
        random_message = get_random_welcome_message()
        customized_message = random_message.replace('[username]', member.mention)
        await welcome_channel.send(customized_message)
        
def read_counter_conf():
  try:
      with open(conf_counter, "r") as file:
        data = json.load(file)
        return data.get("conf_count", 0)
  except FileNotFoundError:
      return 0

def update_counter_conf(counter):
  data = {"conf_count": counter}
  with open(conf_counter, "w") as file:
    json.dump(data, file)

@bot.tree.command(name="sikret", description="Send a sikret message through eggy")
@app_commands.describe(content="Ano sikret mo?", attachment="Pasend image")
async def sikret(interaction: discord.Interaction, content: str = None, attachment: discord.Attachment = None):
  
  anon_channel_id = 1152510600195358741
  
  anonymous_channel = bot.get_channel(anon_channel_id)

  counter = read_counter_conf()

  if not interaction.channel_id == anon_channel_id:
    return

  emb = discord.Embed(color=discord.Color.random())
  if anonymous_channel is not None:
    counter += 1
    emb.title = f"Bulong kay eggy #{counter}"
    
    if content:
      emb.description = content
    
    if attachment:
      emb.set_image(url=attachment.url)
    
    await anonymous_channel.send(embed=emb)
    update_counter_conf(counter)
    await interaction.response.send_message("Message sent successfuly", ephemeral=True)

@bot.command()
async def send_roles(ctx):
    await ctx.send("React to the messages below to set your preferred pronouns, programming language, and zodiac sign.")
    # Send the Pronoun Roles Message
    pronoun_roles_message = await ctx.send("React with one of the following emojis to set your pronouns:\n"
                                           "👨 - He/Him\n"
                                           "👩 - She/Her\n"
                                           "🧑‍🤝‍🧑 - They/Them\n"
                                           "🤐 - Prefer Not to Say")

    # Add reactions for pronouns
    await pronoun_roles_message.add_reaction('👨')  # He/Him
    await pronoun_roles_message.add_reaction('👩')  # She/Her
    await pronoun_roles_message.add_reaction('🧑‍🤝‍🧑')  # They/Them
    await pronoun_roles_message.add_reaction('🤐')  # Prefer Not to Say

    # Send the Programming Languages Roles Message
    programming_languages_message = await ctx.send("React with one of the following emojis to set your preferred programming language:\n"
                                                   "🅰️ - C/C++\n"
                                                   "🅱️ - Python\n"
                                                   "🆎 - JavaScript\n"
                                                   "🅾️ - Java\n"
                                                   "🆑 - C#\n"
                                                   "💻 - Other")

    # Add reactions for programming languages
    await programming_languages_message.add_reaction('🅰️')  # C/C++
    await programming_languages_message.add_reaction('🅱️')  # Python
    await programming_languages_message.add_reaction('🆎')  # JavaScript
    await programming_languages_message.add_reaction('🅾️')  # Java
    await programming_languages_message.add_reaction('🆑')  # C#
    await programming_languages_message.add_reaction('💻')  # Other

    # Send the Zodiac Signs Roles Message
    zodiac_roles_message = await ctx.send("React with one of the following emojis to set your preferred zodiac sign:\n"
                                          "♈ - Aries\n"
                                          "♉ - Taurus\n"
                                          "♊ - Gemini\n"
                                          "♋ - Cancer\n"
                                          "♌ - Leo\n"
                                          "♍ - Virgo\n"
                                          "♎ - Libra\n"
                                          "♏ - Scorpio\n"
                                          "♐ - Sagittarius\n"
                                          "♑ - Capricorn\n"
                                          "♒ - Aquarius\n"
                                          "♓ - Pisces")

    # Add reactions for zodiac signs
    await zodiac_roles_message.add_reaction('♈')  # Aries
    await zodiac_roles_message.add_reaction('♉')  # Taurus
    await zodiac_roles_message.add_reaction('♊')  # Gemini
    await zodiac_roles_message.add_reaction('♋')  # Cancer
    await zodiac_roles_message.add_reaction('♌')  # Leo
    await zodiac_roles_message.add_reaction('♍')  # Virgo
    await zodiac_roles_message.add_reaction('♎')  # Libra
    await zodiac_roles_message.add_reaction('♏')  # Scorpio
    await zodiac_roles_message.add_reaction('♐')  # Sagittarius
    await zodiac_roles_message.add_reaction('♑')  # Capricorn
    await zodiac_roles_message.add_reaction('♒')  # Aquarius
    await zodiac_roles_message.add_reaction('♓')  # Pisces

    
  # Send the Games Roles Message
    games_roles_message = await ctx.send("React with one of the following emojis to set your preferred game:\n"
                                         "🎮 - Genshin Impact\n"
                                         "📱 - Honkai Star Rail\n"
                                         "🚀 - Farlight 84\n"
                                         "🏹 - League of Legends\n"
                                         "🔫 - Valorant\n"
                                         "🕹️ - Mobile Legends")

    # Add reactions for games
    await games_roles_message.add_reaction('🎮')
    await games_roles_message.add_reaction('📱')
    await games_roles_message.add_reaction('🚀') 
    await games_roles_message.add_reaction('🏹') 
    await games_roles_message.add_reaction('🔫') 
    await games_roles_message.add_reaction('🕹️') 
  


emoji_to_role = {
  discord.PartialEmoji(name='👍'): 'NightOwls',
    discord.PartialEmoji(name='♈'): 'Aries',              # Aries Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♉'): 'Taurus',             # Taurus Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♊'): 'Gemini',             # Gemini Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♋'): 'Cancer',             # Cancer Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♌'): 'Leo',                # Leo Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♍'): 'Virgo',              # Virgo Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♎'): 'Libra',              # Libra Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♏'): 'Scorpio',            # Scorpio Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♐'): 'Sagittarius',        # Sagittarius Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♑'): 'Capricorn',          # Capricorn Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♒'): 'Aquarius',           # Aquarius Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='♓'): 'Pisces',             # Pisces Emoji for Zodiac Signs Roles
    discord.PartialEmoji(name='🎮'): 'Genshin Impact',    # Video Game Emoji for Genshin Impact
    discord.PartialEmoji(name='📱'): 'Honkai Star Rail', # Mobile Phone Emoji for Honkai Impact 3rd
    discord.PartialEmoji(name='🚀'): 'Farlight 84',       # Rocket Emoji for Farlight 84
    discord.PartialEmoji(name='🏹'): 'League of Legends', # Bow and Arrow Emoji for League of Legends
    discord.PartialEmoji(name='🔫'): 'Valorant',          # Gun Emoji for Valorant
    discord.PartialEmoji(name='🕹️'): 'Mobile Legends',  # Joystick Emoji for Mobile Legends
    discord.PartialEmoji(name='🅰️'): 'C/C++',            # A Emoji for C/C++
    discord.PartialEmoji(name='🅱️'): 'Python',           # B Emoji for Python
    discord.PartialEmoji(name='🆎'): 'JavaScript',        # AB Emoji for JavaScript
    discord.PartialEmoji(name='🅾️'): 'Java',             # O Emoji for Java
    discord.PartialEmoji(name='🆑'): 'C#',               # CL Emoji for C#
    discord.PartialEmoji(name='💻'): 'Other',             # Computer Emoji for Other programming languages
    discord.PartialEmoji(name='👨'): 'He/Him',            # Man Emoji for He/Him pronouns
    discord.PartialEmoji(name='👩'): 'She/Her',           # Woman Emoji for She/Her pronouns
    discord.PartialEmoji(name='🧑‍🤝‍🧑'): 'They/Them',    # People Holding Hands Emoji for They/Them pronouns
    discord.PartialEmoji(name='🤐'): 'Prefer Not to Say', # Zipper-Mouth Face Emoji for Prefer Not to Say
}

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    role_name = None
  
    verify_channel_id = 1152491024493596674
    if payload.channel_id == verify_channel_id and str(payload.emoji) == '👍':
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member:
            role_name = 'NightOwls'
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.add_roles(role)
                print(f"Added role '{role_name}' to {member.name}")
                await send_welcome_message(member)  # Send welcome message
            else:
                print(f"Role not found: {role_name}")
        else:
            print(f"Member not found: {payload.user_id}")
  
    # Message 1: Gender Roles
    gender_role_message_id = 1152559667663355954
    if payload.message_id == gender_role_message_id:
        try:
            role_name = emoji_to_role[payload.emoji]
        except KeyError:
            print(f"Emoji not found in dictionary: {payload.emoji}")
            return

        # Handle gender role assignment using role_name

    # Message 2: Games Roles
    
    games_role_message_id = 1152559718217297972
    if payload.message_id == games_role_message_id:
        try:
            role_name = emoji_to_role[payload.emoji]
        except KeyError:
            print(f"Emoji not found in dictionary: {payload.emoji}")
            return

        # Handle games role assignment using role_name

    # Message 3: Zodiac Roles
    
    zodiac_role_message_id = 1152559691277291623
    if payload.message_id == zodiac_role_message_id:
        try:
            role_name = emoji_to_role[payload.emoji]
        except KeyError:
            print(f"Emoji not found in dictionary: {payload.emoji}")
            return

        # Handle zodiac role assignment using role_name

    # Message 4: Programming Languages Roles
    
    programming_languages_message_id = 1152559677595459675
    if payload.message_id == programming_languages_message_id:
        try:
            role_name = emoji_to_role[payload.emoji]
        except KeyError:
            print(f"Emoji not found in dictionary: {payload.emoji}")
            return

        # Handle programming language role assignment using role_name

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    role = discord.utils.get(guild.roles, name=role_name)

    if role is None:
        print(f"Role not found - Role: {role_name}")
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        print(f"Member not found: {payload.user_id}")
        return

    try:
        await member.add_roles(role)
        print(f"Added role '{role_name}' to {member.name}")
    except discord.HTTPException:
        print(f"Failed to add role for {member.name}")

@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    # Message 1: Gender Roles
    role_name = None

    verify_channel_id = 1152491024493596674
    if payload.channel_id == verify_channel_id and str(payload.emoji) == '👍':
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member:
            role_name = 'NightOwls'
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await member.remove_roles(role)
                print(f"Removed role '{role_name}' from {member.name}")
            else:
                print(f"Role not found: {role_name}")
        else:
            print(f"Member not found: {payload.user_id}")
          
    gender_role_message_id = 1152559667663355954
    if payload.message_id == gender_role_message_id:
        try:
            role_name = emoji_to_role[payload.emoji]
        except KeyError:
            print(f"Emoji not found in dictionary: {payload.emoji}")
            return

        # Handle removal of gender role using role_name

    # Message 2: Games Roles
    
    games_role_message_id = 1152559718217297972
    if payload.message_id == games_role_message_id:
        try:
            role_name = emoji_to_role[payload.emoji]
        except KeyError:
            print(f"Emoji not found in dictionary: {payload.emoji}")
            return

        # Handle removal of games role using role_name

    # Message 3: Zodiac Roles
    
    zodiac_role_message_id = 1152559691277291623
    if payload.message_id == zodiac_role_message_id:
        try:
            role_name = emoji_to_role[payload.emoji]
        except KeyError:
            print(f"Emoji not found in dictionary: {payload.emoji}")
            return

        # Handle removal of zodiac role using role_name

    # Message 4: Programming Languages Roles
    
    programming_languages_message_id = 1152559677595459675
    if payload.message_id == programming_languages_message_id:
        try:
            role_name = emoji_to_role[payload.emoji]
        except KeyError:
            print(f"Emoji not found in dictionary: {payload.emoji}")
            return

        # Handle removal of programming language role using role_name

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    role = discord.utils.get(guild.roles, name=role_name)

    if role is None:
        print(f"Role not found - Role: {role_name}")
        return

    member = guild.get_member(payload.user_id)
    if member is None:
        print(f"Member not found: {payload.user_id}")
        return

    try:
        await member.remove_roles(role)
        print(f"Removed role '{role_name}' from {member.name}")
    except discord.HTTPException:
        print(f"Failed to remove role for {member.name}")


def read_counter_anowns():
  try:
      with open(anowns_counter, "r") as file:
        data = json.load(file)
        return data.get("anowns_count", 0)
  except FileNotFoundError:
      return 0

def update_counter_anowns(counter):
  data = {"anowns_count": counter}
  with open(anowns_counter, "w") as file:
    json.dump(data, file)

@bot.tree.command(name="anowns", description="Announcement")
@app_commands.describe(content1="Send announcement", attachment="Add image")
async def anowns(
  interaction: discord.Interaction, 
  content1: str, content2: str = None, content3: str = None, content4: str = None, content5: str = None, link: str = None, attachment: discord.Attachment = None):
    anowns_channel_id = 1152508222352138240
    announcement_channel = bot.get_channel(anowns_channel_id)
    role_mention = f"<@&{1152492901809520711}>"

    if not interaction.channel_id == anowns_channel_id:
      return
  
    counter = read_counter_anowns()
    counter += 1
    emb = discord.Embed(color=discord.Color.green())
    emb.title = f"Announcement #{counter}"
    emb.add_field(name='\u200B', value=f"{role_mention}\n\n{content1}\n", inline=False)
    if content2 is not None:
        emb.add_field(name='\u200B', value=f"\n{content2}\n", inline=False)
    if content3 is not None:
        emb.add_field(name='\u200B', value=f"\n{content3}\n", inline=False)
    if content4 is not None:
        emb.add_field(name='\u200B', value=f"\n{content3}\n", inline=False)
    if content5 is not None:
        emb.add_field(name='\u200B', value=f"\n{content3}\n", inline=False)
    if link is not None:
        emb.add_field(name='\u200B', value=f"\n{link}\n{link}\n{link}", inline=False)
    emb.set_footer(text="BSIT 2-2N announcement")

    if attachment:
      emb.set_image(url=attachment.url)
    
    if not interaction.channel_id == anowns_channel_id:
        print("Debug: Interaction not in announcement channel") 
        return

    try:
        await announcement_channel.send(embed=emb)
        await interaction.response.send_message("Announcement sent successfully", ephemeral=True)
        print("Debug: Announcement sent successfully")

        update_counter_anowns(counter)
    except Exception as e:
        print(f"Debug: Error sending announcement - {e}")

def read_counter_ask():
  try:
      with open(ask_counter, "r") as file:
        data = json.load(file)
        return data.get("ask_count", 0)
  except FileNotFoundError:
      return 0

def update_counter_ask(counter):
  data = {"ask_count": counter}
  with open(ask_counter, "w") as file:
    json.dump(data, file)
    
@bot.tree.command(name="askhelp", description="Ask for help")
@app_commands.describe(content="Ask a question", attachment="Add image for context")
async def askHelp(interaction: discord.Interaction, content: str = None, attachment: discord.Attachment = None):
  emb = discord.Embed(color=discord.Color.random())

  ask_channel_id = 1152510737865003038
  
  ask_channel = bot.get_channel(ask_channel_id)

  counter = read_counter_ask()

  if not interaction.channel_id == ask_channel_id:
    return

  emb = discord.Embed(color=discord.Color.random())
  if ask_channel is not None:
    counter += 1
    emb.title = f"Question #{counter}"
    
    if content:
      emb.description = content
    
    if attachment:
      emb.set_image(url=attachment.url)
    
    await ask_channel.send(embed=emb)
    update_counter_ask(counter)
    await interaction.response.send_message("Message sent successfuly", ephemeral=True)
  
@bot.command(name="upfile", description="Upload a file")
async def upfile(ctx, content: str = None):
    upfile_channel_id = 1152562166222823474
    acadfiles_channel = bot.get_channel(upfile_channel_id)

    if ctx.channel.id != upfile_channel_id:
        await ctx.send("You can only use this command in the designated channel.")
        return

    # Check for attachments
    if not ctx.message.attachments:
        await ctx.send("Please attach a file to upload.", ephemeral=True)  # Visible only to the sender
        return

    # Handle file upload
    for attachment in ctx.message.attachments:
        # Mention the user who sent the file in the content
        user_mention = f"<@{ctx.author.id}>"
        user_name = user_mention if content is None else f"From: {user_mention} \nwith message: {content} \nthank you! - eggy"
        await acadfiles_channel.send(content=user_name, file=await attachment.to_file())

    # Delete the user's command message
    await ctx.message.delete()

    # Send "File uploaded successfully!" as an ephemeral message (only visible to the sender)
    response = await ctx.send("File uploaded successfully!", ephemeral=True)

    # Remove the response message and the "File uploaded successfully!" message after a brief delay
    await asyncio.sleep(2)  # Adjust the delay time as needed
    await ctx.channel.delete_messages([ctx.message, response])

keep_alive()

try:
  bot.run(DC_TOKEN)
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  os.system('kill 1')
  os.system("restarter.py")