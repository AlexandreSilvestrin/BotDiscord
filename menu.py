import discord
from discord.ext import commands
from discord import FFmpegPCMAudio


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.musica = None
        self.value = None
        self.listM = None
        self.index = None

    def pegarmusica(self, music, lista):
        self.listM = lista
        self.musica = music
        self.index = self.listM.index(self.musica)
        print(f"{self.index, self.musica, self.listM}")

    def proxima(self, music, lista, index):
        tamanho = len(self.listM)-1
        if index+1 > tamanho:
            index = 0
            music = lista[index]
            print(f"var {index, music,lista }")
            print(f"self {self.index, self.musica, self.listM}")
            return music, lista, index
        else:
            index +=1
            music = lista[index]
            print(f"var {index, music, lista}")
            print(f"self {self.index, self.musica, self.listM}")
            return music, lista, index

    def voltar(self, music, lista, index):
        tamanho = len(self.listM)-1
        if index-1 < 0:
            index = tamanho
            music = lista[index]
            print(f"var {index, music,lista }")
            print(f"self {self.index, self.musica, self.listM}")
            return music, lista, index
        else:
            index -= 1
            music = lista[index]
            print(f"var {index, music, lista}")
            print(f"self {self.index, self.musica, self.listM}")
            return music, lista, index

    def tocarMusica(self, voice,music):
        source = FFmpegPCMAudio(music)
        voice.play(source)


    @discord.ui.button(label="PAUSE", style=discord.ButtonStyle.red)
    async def menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice = interaction.guild.voice_client
        if voice.is_paused():
            embed = discord.Embed(color=discord.Color.green())
            embed.set_author(name=f"{interaction.user}")
            embed.add_field(name="PLAY", value=f"Tocando: {self.musica}")
            await interaction.response.edit_message(embed=embed)
            voice.resume()
        else:
            embed = discord.Embed(color=discord.Color.red())
            embed.set_author(name=f"{interaction.user}")
            embed.add_field(name="PAUSADO", value=f"Ultima musica tocada: {self.musica}")
            await interaction.response.edit_message(embed=embed)
            voice.pause()

    @discord.ui.button(label="PLAY", style=discord.ButtonStyle.green)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=f"{interaction.user}")
        embed.add_field(name="PLAY", value=f"Tocando {self.musica}")
        voice = interaction.guild.voice_client
        voice.pause()
        Menu.tocarMusica(self, voice=voice, music= self.musica)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="palmas", style=discord.ButtonStyle.blurple)
    async def palmas(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name=f"{interaction.user}")
        embed.add_field(name="SAINDO", value=f"Ultima musica tocada: {self.musica}")
        if interaction.guild.voice_client:
            source = FFmpegPCMAudio("palmas.m4a")
            voice = interaction.guild.voice_client
            voice.pause()
            voice.play(source)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"erro no play")

    @discord.ui.button(label="VOLTAR", style=discord.ButtonStyle.blurple)
    async def volt(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.musica, self.listM, self.index = Menu.voltar(self, self.musica, self.listM, self.index)
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=f"{interaction.user}")
        embed.add_field(name="PLAY", value=f"tocando {self.musica}")
        if interaction.guild.voice_client:
            voice = interaction.guild.voice_client
            voice.pause()
            Menu.tocarMusica(self, voice=voice, music= self.musica)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"erro no play")

    @discord.ui.button(label="PROXIMA", style=discord.ButtonStyle.blurple)
    async def prox(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.musica, self.listM, self.index = Menu.proxima(self, self.musica, self.listM, self.index)
        embed = discord.Embed(color=discord.Color.green())
        embed.set_author(name=f"{interaction.user}")
        embed.add_field(name="PLAY", value=f"tocando {self.musica}")
        if interaction.guild.voice_client:
            voice = interaction.guild.voice_client
            voice.pause()
            Menu.tocarMusica(self, voice=voice, music= self.musica)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"erro no play")
