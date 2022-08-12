import discord
from discord import FFmpegPCMAudio
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='?', intents=intents)


@client.event
async def on_ready():
    print('BORA LA')
    print('-------')


# use pra testar se esta funcionando
@client.command()
async def teste(ctx):
    await ctx.send('Iae, estou funcinando')


# pesquisa na pasta do arquivo se tem algum audio com o nome e o formato (exemplo: ?p musica.mp3 )
# obs: nao testei outros formatos de audio alem de mp3 e m4a.
@client.command(pass_context=True)
async def p(ctx, args):
    try:
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            await ctx.send('Conectado')
            source = FFmpegPCMAudio(args)
            voice.play(source)
        else:
            await ctx.send(f'Voce nao esta em um canal de voz')
    except:
        await ctx.send('ja estou na call')
# ele nao toca outra musica se nao for desconectado da call com o comando ?sair antes


# desconecta o bot da call onde esta
@client.command(pass_context=True)
async def sair(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send('Flw')
    else:
        await ctx.channel.send(f'Eu nao estou em um canal de voz')

# coloque o codigo do seu bot como parametro
client.run('CODIGO AQUI')
