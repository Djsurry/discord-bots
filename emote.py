import discord, time, datetime, re, asyncio
import json
import sqlite3, os

TOKEN = os.environ['DISCORD_BOT']
pattern = re.compile(r"(<:[^:]+:\d+>)")
client = discord.Client()


def insert(emote):
	conn = sqlite3.connect('../db/emotes.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO emotes (emote, uses) VALUES (?, ?);", (emote, 1))
	conn.commit()
	cur.close()
	conn.close()

def add(emote):
	conn = sqlite3.connect('../db/emotes.db')
	cur = conn.cursor()
	cur.execute("SELECT uses FROM emotes WHERE emote = ?;", (emote,))
	uses = cur.fetchone()[0]
	cur.execute("UPDATE emotes SET uses = ? WHERE emote = ?;", (uses + 1, emote))
	conn.commit()
	cur.close()
	conn.close()

def exists(emote):
	conn = sqlite3.connect('../db/emotes.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM emotes WHERE emote = ?;", (emote,))
	if cur.fetchone() is None:
		cur.close()
		conn.close()
		return False
	else:
		cur.close()
		conn.close()
		return True
	
@client.event
async def on_ready():
    print(f'{client.user} is connected')
    
    
@client.event
async def on_reaction_add(reaction, user):
	print(f'Got reaction: {str(reaction.emoji)}')
	if exists(str(reaction.emoji)):
		print(f'Adding 1 to {str(reaction.emoji)}')
		add(str(reaction.emoji))
	else:
		print(f'Adding {str(reaction.emoji)} to db')
		insert(str(reaction.emoji))

	if str(reaction.emoji) == "<:Gulag:815302593348632626>":
		message = reaction.message
		print(f'Got vote for {message.author.nick}')
		gulags = 0
		for r in message.reactions:
			if str(reaction.emoji) == "<:Gulag:815302593348632626>":
				gulags += 1
		if gulags > 4 and message.author.id != 242030668228460555:
			await message.author.add_roles(discord.Object(550485684129890336))
			await message.author.remove_roles(discord.Object(482339033717145620))


@client.event
async def on_message(message):
	print(f'Got message: {message.content}')
	for emote in re.findall(pattern, message.content):
		print(emote)
		if exists(emote):
			print(f'Adding 1 to {emote}')
			add(emote)
		else:
			print(f'Adding {emote} to db')
			insert(emote)




try:
	client.run(TOKEN)
except:
	with open('emotes.json', 'w') as f:
		json.dump(data, f)




