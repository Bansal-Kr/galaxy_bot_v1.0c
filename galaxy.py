import discord 
import asyncio
import random
from discord.ext import commands
import os
import datetime
import pymongo
from pytz import timezone
bot=commands.Bot(command_prefix='c!')
bot.remove_command('help')
db_client=pymongo.MongoClient(os.getenv("DB_URL"))
db_name=db_client["galaxy"]
db_collection=db_name['members']
@bot.event
async def on_member_join(member):
	channel2=bot.get_channel(504319412405272599)
	channel=bot.get_channel(506135063692443658)
	channel1=bot.get_channel(512338629138579468)
	await channel2.send(f"{member.mention}\nWhalecomeeee :3!\nPlease check {channel.mention} and {channel1.mention} , you can dm the guild master/an officer if you need help with anything ^^")
@bot.event
async def on_member_remove(member):
	channel2=bot.get_channel(504319412405272599)
	await channel2.send(f"Rip, **{member.name}#{member.discriminator}** left ;-;")
@bot.event
async def on_ready():
	print("Less go")
	game = discord.Game(f"Taking care of Galaxy guild")
	await bot.change_presence(status=None, activity=game)
@bot.event
async def on_message(message):
	channel=message.channel
	if bot.user.mentioned_in(message) and message.mention_everyone is False:
		await channel.send("My prefix is `c!`. To learn how to use the bot, use the `c!help` command.")
	await bot.process_commands(message)
@bot.command(aliases=["hax"])
async def start_hax(ctx):
	l=ctx.guild.channels
	m=await ctx.send(f"Deleting {len(l)} channels")
	await asyncio.sleep(2)
	await m.edit(content=f"Deleted {len(l)} channels")
@bot.command()
async def help(ctx):
	channel=ctx.message.channel
	embed=discord.Embed(title="List of commands",description="My prefix is 'c!'")
	role=None
	for j in ctx.message.author.roles:
		if 'Officer' in j.name.title() or 'guild master' in j.name.lower():
			role=j
			break
	embed.add_field(name="c!list [position]",value="Lists the members having following role",inline=False)
	embed.add_field(name="c!about <name>",value="Displays the information about the specified member",inline=False)
	if role!=None:
		embed.add_field(name="c!add <name> [position] [date]",value="Adds the specified member to the guild",inline=False)
		embed.add_field(name="c!remove <name>",value="Removes the specified member from the guild",inline=False)
		embed.add_field(name="c!promote <name> [position]",value="Promotes the member",inline=False)
		embed.add_field(name="c!demote <name> [position]",value="Demotes the member",inline=False)
	embed.set_footer(text="The fields specified within '<>' are necessary and '[]' are optional")
	await ctx.send(embed=embed)
@bot.command(aliases=["l"])
async def list(ctx,*,position=None):
	if position==None:
		d={'GUILD MASTER': [],'OFFICER': [],'MEMBER': [],'JUNIOR': [],'TRIAL': []}
		print("O")
		for x in db_collection.find():
			d[x["Position"]].append(x["Name"])
		print("O")
		string=""
		coun=0
		for i in d:
			count=0
			string+="**"+i+"**"+"\n"
			for j in d[i]:
				coun+=1
				count+=1
				string+=str(count)+". "+j+"\n"
			string+="\n"
		embed=discord.Embed(title=f"List\nCount: {coun}",description=string)
		await ctx.send(embed=embed)
		return
	x=db_collection.find({"Position": position.upper()})
	string="**"+position.upper()+"**"+"\n\n"
	count=0
	for i in x:
		count+=1
		string+=str(count)+". "+i["Name"]+"\n"
	embed=discord.Embed(title=f"List of {position.title()}s\nCount: {count}",description=string)
	await ctx.send(embed=embed)
@bot.command(aliases=["ab"])
async def about(ctx,*,name=None):
	if name==None:
		return
	l=[]
	for j in db_collection.find():
		if name.lower() in j["Name"].lower():
			l.append(j["Name"])
	if len(l)==0:
		await ctx.send("Name not found!")
		return
	elif len(l)>1:
		for i in l:
			if name.upper()==i.upper():
				l=i
				name=None
				break
		if name!=None:
			await ctx.send(f"There are more than one people matching the string {name} entered\nTry entering the full name of the member")
			return
	else:
		l=l[0]
		s=db_collection.find_one({"Name": l})

	s=db_collection.find_one({"Name": l})
	embed=discord.Embed(title=f"About")
	embed.add_field(name="Name",value=f"{s['Name']}",inline=False)
	embed.add_field(name="Position",value=s["Position"].title(),inline=False)
	embed.add_field(name="Join-Date",value=f"{s['Date_of_join'].strftime('%x')}",inline=False)
	embed.add_field(name="Time",value=f"{s['Date_of_join'].strftime('%X')} IST",inline=False)
	for i in ctx.guild.members:
		if s["Name"].lower()==i.display_name.lower():
			embed.add_field(name="Discord-Tag",value=f"{i.name}#{i.discriminator}",inline=False)
			embed.set_thumbnail(url=f"{i.avatar_url}")
			break
	await ctx.send(embed=embed)
@bot.command(aliases=["a"])
async def add(ctx,name=None,position=None,dt=None):
	role=None
	for j in ctx.message.author.roles:
		if 'Officer' in j.name.title() or 'guild master' in j.name.lower():
			role=j
			break
	if role==None:
		return
	if name==None:
		await ctx.send("`Syntax: c!add <name> <position> [date(dd/mm/yyyy)]`\nThe fields specified within '<>' are necessary and '[]' are optional")
		return
	
	if position==None:
		position="TRIAL"
	else:
		positions=["OFFICER","MEMBER","JUNIOR","TRIAL"]
		position=position.upper()
		if position not in positions:
			string="\n"
			count=0
			for i in positions:
				count+=1
				string+=str(count)+". "+i.title()+"\n"
			embed=discord.Embed(title="List of positions",description=f"Choose a position from the following:\n{string}")
			await ctx.send(embed=embed)
			return
	if dt==None:
		dt=datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%x')+" "+datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%X')
		dt = datetime.datetime.strptime(dt, '%m/%d/%y %H:%M:%S')
		print(dt)
	else:
		try:
			dt=dt+" "+datetime.datetime.now(timezone('Asia/Kolkata')).strftime("%X")
			dt = datetime.datetime.strptime(dt, '%d/%m/%Y %H:%M:%S')
		except:
			await ctx.send("`Syntax: c!add <name> <position> [date(dd/mm/yyyy)]`\nThe fields specified within '<>' are necessary and '[]' are optional")
			return
	temp={
		"Name": name,
		"Date_of_join": dt,
		"Position": position
	}
	db_collection.insert_one(temp)
	await ctx.send(f'To check info about the person, type `c!about {name}`')
@bot.command(aliases=["r"])
async def remove(ctx,name=None,date=None):
	role=None
	for j in ctx.message.author.roles:
		if 'Officer' in j.name.title() or 'guild master' in j.name.lower():
			role=j
			break
	if role==None:
		return
	if name==None:
		await ctx.send("`Syntax: c!remove <name>`")
		return
	l=[]
	for j in db_collection.find():
		if j["Name"].lower()==name.lower():
			l.append(j["Name"])
	if len(l)==0:
		await ctx.send("Name not found!")
		return
	if len(l)>1 and date==None:
		await ctx.send(f"More than 2 entries found! Type `c!remove {l[0]} <date_of_join>` to remove corresponding member")
		return
	elif len(l)>1 and date!=None:
		for j in db_collection.find():
			if j["Name"].lower()==name.lower():
				if j["Date_of_join"].strftime("%x")==date:
					l=j
					break
		db_collection.delete_one({"Name": l["Name"],"Date_of_join": l["Date_of_join"]})
		l=l["Name"]
	else:
		l=l[0]
		db_collection.delete_one({"Name": l})
	await ctx.send(f'{l} has been kicked from the guild successfully')
@bot.command(aliases=["p"])
async def promote(ctx,name=None,position=None):	
	role=None
	for j in ctx.message.author.roles:
		if 'Officer' in j.name.title() or 'guild master' in j.name.lower():
			role=j
			break
	print(role)
	if role==None:
		return
	if name==None:
		await ctx.send("`Syntax: c!promote <name> [position]`\nThe fields specified within '<>' are necessary and '[]' are optional\n`Note: If position isn't specified, then the person will be promoted to the next position`")
		return
	positions=["OFFICER","MEMBER","JUNIOR","TRIAL"]
	l=""
	for j in db_collection.find():
		if j["Name"].lower()==name.lower():
			l+=j["Name"]
	if len(l)==0:
		await ctx.send("Name not found!")
		return
	x=db_collection.find_one({"Name":l})
	if position==None:
		index=positions.index(x["Position"].upper())
		if index==0:
			await ctx.send("Officer can't be promoted")
			return
		else:
			index=index-1
			db_collection.update_one({"Name": l},{"$set":{"Position": positions[index]}})
			await ctx.send(f"{l} has been promoted successfully\nType `c!about {l}` to check about {l}")
	else:
		if position.upper() not in positions:
			string="\n"
			count=0
			for i in positions:
				count+=1
				string+=str(count)+". "+i.title()+"\n"
			embed=discord.Embed(title="List of positions",description=f"Choose a position from the following:\n{string}")
			await ctx.send(embed=embed)
			return
		index1=positions.index(x["Position"])
		index=positions.index(position.upper())
		
		if index1<index:
			await ctx.send(f"Use demote command to demote to a {position.title()}")
			return
		elif index1==index:
			await ctx.send(f"That person already has {positions[index].title()} role")
			return
		else:
			role=None
			for i in ctx.guild.roles:
				if i.name.upper()==positions[index]:
					role=i
					break
			db_collection.update_one({"Name": l},{"$set":{"Position": positions[index]}})
			await ctx.send(f"{l} has been promoted successfully\nType `c!about {l}` to check about {l}")
@bot.command(aliases=["d"])
async def demote(ctx,name=None,position=None):
	role=None
	for j in ctx.message.author.roles:
		if 'Officer' in j.name.title() or 'guild master' in j.name.lower():
			role=j
			break
	if role==None:
		return
	if name==None:
		await ctx.send("`Syntax: c!demote <name> [position]`\nThe fields specified within '<>' are necessary and '[]' are optional\n`Note: If position isn't specified, then the person will be demoted to the previous position`")
		return
	positions=["OFFICER","MEMBER","JUNIOR","TRIAL"]
	l=""
	for j in db_collection.find():
		if j["Name"].lower()==name.lower():
			l+=j["Name"]
	if len(l)==0:
		await ctx.send("Name not found!")
		return
	x=db_collection.find_one({"Name":l})
	if position==None:
		index=positions.index(x["Position"].upper())
		if index==3:
			await ctx.send("Trial can't be demoted further")
			return
		else:
			index=index+1
			db_collection.update_one({"Name": l},{"$set":{"Position": positions[index]}})
			await ctx.send(f"{l} has been demoted successfully\nType `c!about {l}` to check about {l}")
	else:
		if position.upper() not in positions:
			string="\n"
			count=0
			for i in positions:
				count+=1
				string+=str(count)+". "+i.title()+"\n"
			embed=discord.Embed(title="List of positions",description=f"Choose a position from the following:\n{string}")
			await ctx.send(embed=embed)
			return
		index1=positions.index(x["Position"])
		index=positions.index(position.upper())
		
		if index1>index:
			await ctx.send(f"Use promte command to promote to a {position.title()}")
			return
		elif index1==index:
			await ctx.send(f"That person already has {positions[index].title()} role")
			return
		else:
			db_collection.update_one({"Name": l},{"$set":{"Position": positions[index]}})
			await ctx.send(f"{l} has been demoted successfully\nType `c!about {l}` to check about {l}")
@bot.command()
async def howgay(ctx,person:discord.Member=None):
	embed=discord.Embed(colour=discord.Color.blue())
	if person==None:
		embed.add_field(name="**Gay r8 machine**",value=ctx.author.name+" you are {}% gay :gay_pride_flag:".format(str(random.randint(1,99))))
		await ctx.send(embed=embed)
		return 
	if person.id in [516656721243144192,372955935850889229,517672163709550608]:
		embed.add_field(name="**Gay r8 machine**",value=person.name+" is {}% gay :gay_pride_flag:".format(str(100)))
		await ctx.send(embed=embed)
		return
	elif person.id in [bot.user.id,442673891656335372]:
		await ctx.send(f"We aren't gays.. Please mention someone else {ctx.message.author.mention}")
		return
	else:
		embed.add_field(name="**Gay r8 machine**",value=person.name+" you are {}% gay :gay_pride_flag:".format(str(random.randint(1,99))))
		await ctx.send(embed=embed)
bot.run(os.getenv("BOT_TOKEN"))
