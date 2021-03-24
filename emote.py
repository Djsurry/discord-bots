import discord, time, datetime, re
import json



TOKEN = 'ODE1MTM3Mzk5MTU1NzIwMTky.YDoB3A._IASkIm8_bBtt6FSe38oDCVYR0k'

pattern = re.compile(r"<:.+:\d+>")
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
		data['emotes'][reaction.emoji] = 0
	data['emotes'][reaction.emoji] += 1
@client.event
async def on_message(message):
	print(f'Got message: {message.content}')
	m = pattern.search(message.content)
	if not m:
		return
	if m.group(0) not in data['emotes']:
		data['emotes'][m.group(0)] = 0
	data['emotes'][m.group(0)] += 1
	with open('emotes.json', 'w') as f:
		json.dump(data, f)

    

try:
	client.run(TOKEN)
except:
	with open('emotes.json', 'w') as f:
		json.dump(data, f)




