import discord, time, datetime, re
import json
import psycopg2

TOKEN = 'ODE1MTM3Mzk5MTU1NzIwMTky.YDoB3A._IASkIm8_bBtt6FSe38oDCVYR0k'
postgres = 'postgres://lkqrjjtnsmdaor:ed80e278bbaf164b2f53b7f2c9173c448313ca793b7c57ec1bb0a9ec2d53bbc6@ec2-54-205-183-19.compute-1.amazonaws.com:5432/dc3lcj8g41q7p2'
pattern = re.compile(r"(<:.+:\d+>)")
client = discord.Client()

with open('emotes.json') as f:
	data = json.load(f)

conn = psycopg2.connect(postgres, sslmode='require')
cur = conn.cursor()
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, emote text, uses smallint);")
cur.close()
conn.close()

@client.event
async def on_ready():
    print(f'{client.user} is connected')
    
    
@client.event
async def on_reaction_add(reaction, user):
	print(f'Got reaction: {reaction.emoji}')
	if reaction.emoji not in data['emotes']:
		print(f'Adding {emote} to dictionary')
		data['emotes'][reaction.emoji] = 0
	print(f'Adding 1 to {emote}')
	data['emotes'][reaction.emoji] += 1
	with open('emotes.json', 'w') as f:
		json.dump(data, f)


@client.event
async def on_message(message):
	print(f'Got message: {message.content}')
	for emote in re.findall(pattern, message.content):
		if emote not in data['emotes']:
			print(f'Adding {emote} to dictionary')
			data['emotes'][emote] = 0
		print(f'Adding 1 to {emote}')
		data['emotes'][emote] += 1

		with open('emotes.json', 'w') as f:
			json.dump(data, f)



try:
	client.run(TOKEN)
except:
	with open('emotes.json', 'w') as f:
		json.dump(data, f)




