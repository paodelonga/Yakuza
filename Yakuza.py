import io, os, sys, discord, datetime, platform
from discord.ext import commands
from configparser import ConfigParser
from pydeezer import Deezer, Downloader
from discord.ext.commands.errors import *
from pydeezer.constants import track_formats
from discord.ext.commands import has_permissions

#reading config
Config = ConfigParser()
[Config.read(file) for file in os.listdir() if file.endswith('.ini')]

ConverTime = datetime.datetime.strptime

# Clear console
def clear():
	if "linux" in str(platform.system()).lower():
		os.system("clear")
	elif "windows" in str(platform.system()).lower():
		os.system("cls")
	else:
		os.system("clear")
clear()


# Discord Authentication
try:
	discordIntents = discord.Intents.default()
	discordIntents.members = True
	discordClient = commands.Bot(command_prefix = Config['Discord']['Prefix'],
		case_insensitive = True,
		intents = discordIntents)
	discordClient.remove_command('help')
	
	@discordClient.event
	async def on_ready():
		await discordClient.change_presence(
			activity = discord.Activity(
			type = discord.ActivityType.listening,
			name = 'o som das navalhas rasgando a pele'))
		print(f"[Discord] - Login\n"
			f".USER: {discordClient.user.name}\n"
			f".TAG: {discordClient.user}\n.ID: {discordClient.user.id}\n")
except Exception as discordClientException:
	print(f"[Discord]\n[Exception] :: {discordClientException}")
	sys.exit()

# Deezer Authentication
try:
	deezerClient = Deezer(arl=Config['Deezer']['Token'])
	print(f"[Deezer] - Login\n.USER: {deezerClient.user['name']}\n.ID: {deezerClient.user['id']}\n\n")
except Exception as deezerClientException:
	print(f"[Deezer]\n[Exception] :: {deezerClientException}")
	sys.exit()


# Get information
@discordClient.group(case_insensitive=True)
async def Get(ctx):
	...

@Get.command()
async def Role(ctx, role: discord.Role):
	await ctx.message.delete()
	await ctx.send(f'{ctx.author.mention} Requerido com sucesso!')


@Get.command()
async def Members(ctx, role: discord.Role):
	membersEmbedDescription = (f"Membros inclusos em {role}\n")
	Count = 0
	for M in role.members:
		Count += 1
		membersEmbedDescription += str(
			f"Name: `{M.name}`\n"
			f"TAG: `{M.name}#{M.discriminator}`\n"
			f"Discriminador: `{M.discriminator}`\n"
			f"ID: `{M.id}`\n"
			f"IsBot: `{M.bot}`\n\n")
	membersEmbedDescription += str(f"\n\nQuantidade de Membros: {Count}")
	membersEmbed = discord.Embed(titule = "Listagem de Membros", description=membersEmbedDescription)
	membersEmbed.timestamp = ctx.message.created_at
	membersEmbed.set_footer(text = f"Prefix {Config['Discord']['Prefix']} | {Config['App']['defaultPowered']}")
	await ctx.message.delete()
	await ctx.send(f'{ctx.author.mention} Requerido com sucesso!', embed=membersEmbed)


@Get.command()
async def ID(ctx, role: discord.Role):
	await ctx.message.delete()
	await ctx.send(f'{ctx.author.mention} Requerido com sucesso!')


@Get.command()
async def User(ctx, user: discord.User):
	await ctx.message.delete()
	await ctx.send(f'{ctx.author.mention} Requerido com sucesso!')


@Get.command()
async def InRole(ctx, Source: discord.Role, Compare: discord.Role):
	SourceRole = {} 
	CompareRole = {}
	OutCompare = []
	Out = False

	if Source.id != Compare.id:
		SC = 0
		for Member in Source.members:
			SC = SC +1
			SourceRole.update(
				{SC:{
					"ID": Member.id,
					"Name": Member.name
					}
				})

		CC = 0
		for Member in Compare.members:
			CC = CC +1
			CompareRole.update(
				{CC:{
					"ID": Member.id,
					"Name": Member.name
					}
				})

		for User in SourceRole:
			if SourceRole[User]['ID'] not in [CompareRole[x]['ID'] for x in CompareRole]:
				OutCompare.append(SourceRole[User]['ID'])
				Out = True

		if Out == True:
			inroleEmbedDescription = (f'Membros de {Source.mention} que não estão em {Compare.mention}\n')
			for User in SourceRole:
				if SourceRole[User]['ID'] in OutCompare:
					inroleEmbedDescription += str(f"Name: `{SourceRole[User]['Name']}`\nID: `{SourceRole[User]['ID']}`\n\n")

			inroleEmbed = discord.Embed(
				title = 'Comparação de Cargos.',
				description = inroleEmbedDescription)

			inroleEmbed.set_footer(text = f"Prefix {Config['Discord']['Prefix']} | {Config['App']['defaultPowered']}")
			inroleEmbed.timestamp = ctx.message.created_at

			await ctx.message.delete()
			await ctx.send(f'{ctx.author.mention} Verificação completa!', embed=inroleEmbed)


		elif Out == False:
			inroleEmbedDescription = (f'Todos os membros de {Source.mention} estão em {Compare.mention}')
			inroleEmbed = discord.Embed(
				title = 'Comparação de Cargos.',
				description = inroleEmbedDescription)

			inroleEmbed.set_footer(text = f"Prefix {Config['Discord']['Prefix']} | {Config['App']['defaultPowered']}")
			inroleEmbed.timestamp = ctx.message.created_at

			await ctx.message.delete()
			await ctx.send(f'{ctx.author.mention} Tudo certo!', embed=inroleEmbed)


	elif Source.id == Compare.id:
		inroleEmbedDescription = (
			'Os cargos a serem comparados não devem ser os mesmos!\n\n'
			f'Os cargos a serem comparados foram os mesmos.\nRole: {Source.mention}\n'
			'**Use:**\n'
			f"`{Config['Discord']['Prefix']}Get InRole <SourceID> <CompareID>`\n\n"
			'`SourceID`: ID do Cargo Base.\n`CompareID`: ID do Comparando')

		inroleEmbed = discord.Embed(
			title='Comparação de Cargos.',
			description = inroleEmbedDescription)

		inroleEmbed.set_footer(text = f"Prefix {Config['Discord']['Prefix']} | {Config['App']['defaultPowered']}")
		inroleEmbed.timestamp = ctx.message.created_at

		await ctx.message.delete()
		await ctx.send(f'{ctx.author.mention} Você usou o comando de forma errada!', embed=inroleEmbed)

@InRole.error
async def error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		inroleEmbedDescription = (
			'Os cargos a serem comparados devem ser passados logo depois do comando!'
			'**Use:**\n'
			f"`{Config['Discord']['Prefix']}Get InRole <SourceID> <CompareID>`\n\n"
			'`SourceID`: ID do Cargo Base.\n`CompareID`: ID do Comparando')

		inroleEmbed = discord.Embed(
			title='Comparação de Cargos.',
			description = inroleEmbedDescription)

		inroleEmbed.set_footer(text = f"Prefix: {Config['Discord']['Prefix']} | {Config['App']['defaultPowered']}")
		inroleEmbed.timestamp = ctx.message.created_at

		await ctx.message.delete()
		await ctx.send(f'{ctx.author.mention} Você usou o comando de forma errada!',embed=inroleEmbed)


@Get.command(aliases = ['cmds', 'comandos', 'commands', ''])
async def ajuda(ctx):
	getEmbedDescription = (
		'**SubComandos disponíveis:**\n'
		f"> {Config['Discord']['Prefix']}Get ID: Role ID.\n"
		f"> {Config['Discord']['Prefix']}Get User: Roles of a User.\n"
		f"> {Config['Discord']['Prefix']}Get Role: Role Name.\n"
		f"> {Config['Discord']['Prefix']}Get InRole: Compare Users Between Roles.\n"
		f"> {Config['Discord']['Prefix']}Get Member: Info About a Member.\n"
		f"> {Config['Discord']['Prefix']}Get Members: Members in a Role.\n")

	getEmbed = discord.Embed(description = getEmbedDescription)
	getEmbed.set_footer(text = f"Prefix {Config['Discord']['Prefix']}  | {Config['App']['defaultPowered']}")
	getEmbed.timestamp = ctx.message.created_at
	await ctx.message.delete()
	await ctx.send(f'{ctx.author.mention} Requerido com sucesso!',embed=getEmbed)


@discordClient.command(case_insensitive=True, aliases=['m','song','s', 'MusicSearch', 'search'])
async def track(ctx, *, track: str):
	Search = deezerClient.search_tracks(track)
	Tracks = {}
	Songs = ""
	N = 0

	for Track in Search:
		N += 1
		Tracks.update({N: {
			"artist": {"name": Track['artist']['name']},
			"song_title": Track['title'],
			"n": N,
			"id": Track['id'],
			"url": Track['link'],
			'short_title': Track['title_short'],
			'mp3_preview': Track['preview'],
			'duration': Track['duration']}})

	Nb = len(Track)-5
	for s in Tracks:
		Songs += str(f"**{Tracks[s]['n']}.** [{Tracks[s]['artist']['name']} - {Tracks[s]['song_title']}]({Tracks[s]['url']}) - [`{ConverTime(str(Tracks[s]['duration']), '%M%S')}`]\n")
	Songs += str(f"\nRequested by: {ctx.author.mention}")

	musicEmbed = discord.Embed(
		title="DeezMusic Searching...",
		description=Songs)

	musicEmbed.timestamp = ctx.message.created_at
	musicEmbed.set_footer(text = f"Prefix {Config['Discord']['Prefix']}  | {Config['App']['defaultPowered']}")

	await ctx.message.delete()
	await ctx.send(ctx.author.mention, embed=musicEmbed)


# Remember the BAN
@discordClient.command(aliases = ['kdban', 'bankd', 'relembre', 'lembre'])
async def remember(ctx):
	rememberEmbed = discord.Embed()
	rememberEmbed.set_author(name="Remember, Remember", icon_url="https://media.discordapp.net/attachments/931416681509703691/933183478453919865/carlos.gif?width=65&height=65")
	rememberEmbed.set_image(url="https://cdn.discordapp.com/attachments/933182302580789298/933871646522089512/BANIDO.png")
	rememberEmbed.timestamp = ctx.message.created_at

	await ctx.message.delete()
	await ctx.send(embed=rememberEmbed)


# Yakuza
@discordClient.command(aliases = ['sobre','clan','servidor'])
async def yakuza(ctx):
	await ctx.send(f'Yakuza, mexeu morreu!')

# Embed
@discordClient.command(aliases=['embedtest','testembed','embtest','emb'])
async def embed(ctx):
	embed = discord.Embed(
		title = 'Yakuza™',
		description = ' A Yakuza é um clan criado por <@511678205795631125>',
		colour = 8421504)

	embed.set_author(name = 'Yakuza™', icon_url = 'https://static.wikia.nocookie.net/minecraft/images/6/69/GoldenAppleNew.png/revision/latest/scale-to-width-down/160?cb=20190908183714')
	embed.set_thumbnail(url = 'https://c.tenor.com/f1pKX_I2Cs0AAAAC/steve-minecraft.gif')
	embed.set_image(url = 'https://cdn.discordapp.com/attachments/879114476106960918/932750874445488139/Captura_de_tela_de_2022-01-13_22-03-13.png')
	embed.set_footer(text = 'Powered by @KDespinho®')
	await ctx.message.delete()
	await ctx.send(ctx.author.mention, embed = embed)


"""
@discordClient.group(case_insensitive=True)
async def Set(ctx):
	...
"""

"""
# Set log channel
@Set.command(aliases=['lChannel','lCh','logch','DebugChannel'])
async def logChannel(ctx, channel: discord.TextChannel):
	Config['Discord']['logChannel'] = str(channel.id)
	with open('config.ini', 'w') as f:
		Config.write(f)

	SetChannelEmbedDescription = (
		f"Canal de log definido para {channel.mention}")
	SetChannelEmbed = discord.Embed(title='Canal de Erros', description=SetChannelEmbedDescription)
	SetChannelEmbed.timestamp = ctx.message.created_at
	SetChannelEmbed.set_footer(text = f"Prefix {Config['Discord']['Prefix']}  | {Config['App']['defaultPowered']}")
	await ctx.send(ctx.author.mention, embed=SetChannelEmbed)
"""


"""
# Search on Deezer.
@discordClient.command(aliases = ['SearchArtist', 'DeezerArtist', 'FindArtist', 'AboutArtist', 'fArt', 'dArt', 'sArt'])
async def artist(ctx, *, resposta):
	search = deezerClient.search_artists(resposta)

	artistEmbed = discord.Embed(description=search)
	artistEmbed.timestamp = ctx.message.created_at
	artistEmbed.set_footer(text = f"Prefix {Config['Discord']['Prefix']}  | {Config['App']['defaultPowered']}")
	await ctx.send(f"{ctx.author.mention}", embed = artistEmbed)
"""

"""
@Get.command()
async def logChannel(ctx):
	logChannelEmbedDescription = (
		f"LogChannel definido para {discordClient.get_channel(str(Config['Discord']['logChannel']))}")
	logChannelEmbed = discord.Embed(title='Canal de Erros',description=logChannelEmbedDescription)
	logChannelEmbed.timestamp = ctx.message.created_at
	logChannelEmbed.set_footer(text = f"Prefix {Config['Discord']['Prefix']}  | {Config['App']['defaultPowered']}")
	await ctx.send(ctx.author.mention, embed=logChannelEmbed)
"""

"""
@discordClient.event
async def on_error(error):
	channel = discordClient.get_channel(Config['Discord']['logChannel'])
	errorEmbed = discord.Embed(description=error)
	errorEmbed.set_footer(text = f"Prefix {Config['Discord']['Prefix']}  | {Config['App']['defaultPowered']}")
	send = await channel.message.send(embed=errorEmbed)
	errorEmbed.timestamp = send.created_at
	send
"""
discordClient.run(Config['Discord']['Token'])
