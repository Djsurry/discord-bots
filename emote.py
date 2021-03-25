import discord, time, datetime, re
import json
import psycopg2

TOKEN = 'ODE1MTM3Mzk5MTU1NzIwMTky.YDoB3A._IASkIm8_bBtt6FSe38oDCVYR0k'
postgres = 'postgres://lkqrjjtnsmdaor:ed80e278bbaf164b2f53b7f2c9173c448313ca793b7c57ec1bb0a9ec2d53bbc6@ec2-54-205-183-19.compute-1.amazonaws.com:5432/dc3lcj8g41q7p2'
pattern = re.compile(r"(<:.+:\d{15,20}>)")
client = discord.Client()


def insert(emote):
	conn = psycopg2.connect(postgres, sslmode='require')
	cur = conn.cursor()
	cur.execute("INSERT INTO emotes (emote, uses) VALUES (%s, %s);", (emote, 1))
	conn.commit()
	cur.close()
	conn.close()

def add(emote):
	conn = psycopg2.connect(postgres, sslmode='require')
	cur = conn.cursor()
	cur.execute("SELECT uses FROM emotes WHERE emote = %s;", (emote,))
	uses = cur.fetchone()[0]
	cur.execute("UPDATE emotes SET uses = %s WHERE emote = %s;", (uses + 1, emote))
	conn.commit()
	cur.close()
	conn.close()

def exists(emote):
	conn = psycopg2.connect(postgres, sslmode='require')
	cur = conn.cursor()
	cur.execute("SELECT * FROM emotes WHERE emote = %s;", (emote,))
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
	print(f'Got reaction: {reaction.emoji}')
	if exists(reaction.emoji):
		print(f'Adding 1 to {reaction.emoji}')
		add(reaction.emoji)
	else:
		print(f'Adding {reaction.emoji} to db')
		insert(reaction.emoji)


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




