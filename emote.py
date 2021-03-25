import discord, time, datetime, re
import json



TOKEN = 'ODE1MTM3Mzk5MTU1NzIwMTky.YDoB3A._IASkIm8_bBtt6FSe38oDCVYR0k'

pattern = re.compile(r"(<:.+:\d+>)")
client = discord.Client()

with open('emotes.json') as f:
	data = json.load(f)


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




