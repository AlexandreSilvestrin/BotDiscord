import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.ui import view
from discord import components
from discord import app_commands
from menu import Menu

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


def listmusicas():
    musicas = ['bones.mp3', 'lonely.mp3', 'living.mp3', 'palmas.m4a','Animals.mp3', 'Whatever It Takes.mp3', 'Enemy.mp3']
    return musicas


def tocaraudio(voice, musica):
    source = FFmpegPCMAudio(musica)
    voice.play(source, after=lambda x=None: tocaraudio(voice=voice))


@bot.event
async def on_ready():
    print('BORA LA')
    print('-------')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="iaee")
async def iae(interaction: discord.Interaction):
    await interaction.response.send_message(f"Iae {interaction.user.mention} estou funcinando", delete_after=10)


@bot.tree.command(name='tocar')
@app_commands.describe(nome_da_musica="musica")
async def tocar(interaction: discord.Interaction, nome_da_musica: str):
    global musica
    musica = nome_da_musica
    view = Menu()
    try:
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            if not interaction.guild.voice_client:
                print("entrou no if")
                voice = await channel.connect()
                tocaraudio(voice, nome_da_musica)
                view.pegarmusica(music=musica, lista=listmusicas())
                embed = discord.Embed(color=discord.Color.green())
                embed.set_author(name=f"{interaction.user}")
                embed.add_field(name="PLAY", value=f"Tocando: {nome_da_musica}")
                await interaction.response.send_message(embed=embed, view=view, delete_after=300)
            else:
                voice = interaction.guild.voice_client
                voice.pause()
                tocaraudio(voice, nome_da_musica)
                view.pegarmusica(music=musica, lista=listmusicas())
                embed = discord.Embed(color=discord.Color.green())
                embed.set_author(name=f"{interaction.user}")
                embed.add_field(name="PLAY", value=f"Tocando: {nome_da_musica}")
                await interaction.response.send_message(embed=embed, view=view, delete_after=300)
        else:
            await interaction.response.send_message(f"nao esta no canal de voz", delete_after=10)
    except Exception as e:
        print(e)
        await interaction.response.send_message(f"errin", delete_after=10)


@tocar.autocomplete('nome_da_musica')
async def musica_pc(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    musicas = listmusicas()
    return [app_commands.Choice(name=nome_da_musica, value=nome_da_musica) for nome_da_musica in musicas if
            current.lower() in nome_da_musica.lower()]


@bot.tree.command(name="sair")
async def sair(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message(f"flw", delete_after=10)
    else:
        await interaction.response.send_message(f"Nao estou na call", delete_after=10)


# coloque o codigo do seu bot como parametro
token2 = 'MTA0MjkwOTAwMTk3MDYxNDQ0NA.GQSsYK.M-0iMq28NJLCt7TvrP5nZn5c1vx3ANf9k8yAm4'
token = 'OTYxNDUwOTgxNjE3NDM4NzUw.Gas6aY.xOHZ2pLCdU1Yz0kN_3gCn3ppbKi8UKHXMYhFaI'
bot.run(token)
