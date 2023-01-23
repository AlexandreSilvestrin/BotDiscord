import time
import discord
from discord import app_commands, FFmpegPCMAudio

token_bot = 'Seu token aqui'


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.musica = None
        self.value = None
        self.listM = None
        self.index = None
        self.embed = None
        self.msgID = None
        self.inte = None

    def pegarmusica(self, music, lista):
        self.listM = lista
        self.musica = music
        self.index = self.listM.index(self.musica)

    def proxima(self, lista, index, voice):
        tamanho = len(self.listM) - 1
        if index + 1 > tamanho:
            index = 0
            music = lista[index]
        else:
            index += 1
            music = lista[index]
        self.musica, self.listM, self.index = music, lista, index
        voice.pause()
        self.tocarMusica(voice, self.musica)

    async def voltar(self, lista, index, voice):
        tamanho = len(self.listM) - 1
        if index - 1 < 0:
            index = tamanho
            music = lista[index]
            self.musica, self.listM, self.index = music, lista, index
            voice.pause()
            self.tocarMusica(voice, self.musica)
        else:
            index -= 1
            music = lista[index]
            self.musica, self.listM, self.index = music, lista, index
            voice.pause()
            self.tocarMusica(voice, self.musica)

    def criaEmbed(self, cor, descricao, musica):
        if cor == 'verde':
            self.embed = discord.Embed(color=discord.Color.green(), title=self.musica)
        elif cor == 'vermelho':
            self.embed = discord.Embed(color=discord.Color.red(), title=self.musica)
        elif cor == 'gold':
            self.embed = discord.Embed(color=discord.Color.gold(), title=musica)
            self.embed.add_field(name=descricao, value='tetste', inline=True)
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/556189304997543938/1064355905753325568/image.png")
        return self.embed

    async def verificar(self, botao, voice, interaction=None):
        if botao == 'play':
            if interaction.guild.voice_client:
                if voice.is_paused():
                    voice.resume()
                else:
                    voice.pause()
                    self.tocarMusica(voice, self.musica)
            self.criaEmbed(cor='verde', descricao='Tocando', musica=self.musica)
        elif botao == 'pause':
            if voice.is_paused():
                self.criaEmbed(cor='verde', descricao='Tocando', musica=self.musica)
                voice.resume()
            else:
                self.criaEmbed(cor='vermelho', descricao='Pausado', musica=self.musica)
                voice.pause()
        elif botao == 'voltar':
            await self.voltar(self.listM, self.index, voice)
            if interaction.guild.voice_client:
                self.criaEmbed(cor='verde', descricao='Tocando', musica=self.musica)
        elif botao == 'proxima':
            self.proxima(self.listM, self.index, voice)
            if interaction.guild.voice_client:
                self.criaEmbed(cor='verde', descricao='Tocando', musica=self.musica)
        elif botao == 'palmas':
            if interaction.guild.voice_client:
                voice.pause()
                self.criaEmbed(cor='gold', descricao='Tocando', musica='palmas.m4a')
                self.tocarMusica(voice, 'palmas.m4a')

    def tocarMusica(self, voice, music):
        source = FFmpegPCMAudio('Musicas/'+music)
        voice.play(source, after=lambda x: Menu.proxima(self, self.listM, self.index, voice))

    @discord.ui.button(emoji='⏯')
    async def playPause(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.verificar(interaction=interaction, botao='pause', voice=interaction.guild.voice_client)
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(emoji='🔁')
    async def recomecar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.verificar(interaction=interaction, botao='play', voice=interaction.guild.voice_client)
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.grey, label='palmas')
    async def palmas(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.verificar(interaction=interaction, botao='palmas', voice=interaction.guild.voice_client)
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(emoji='⏮')
    async def volt(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.verificar(interaction=interaction, botao='voltar', voice=interaction.guild.voice_client)
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(emoji='⏭')
    async def prox(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.verificar(interaction=interaction, botao='proxima', voice=interaction.guild.voice_client)
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.grey, label='Atualizar')
    async def att(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.criaEmbed(cor='verde', descricao='Tocando', musica=self.musica)
        await interaction.response.edit_message(embed=self.embed)


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False  # Nós usamos isso para o bot não sincronizar os comandos mais de uma vez

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # Checar se os comandos slash foram sincronizados
            await tree.sync()  # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
            self.synced = True
        print(f"Entramos como {self.user}.")


aclient = client()
tree = app_commands.CommandTree(aclient)


def listmusicas():
    musicas = ['Lista com nome das musicas aqui']

    return musicas


@tree.command(name='tocar', description='Setup')
@app_commands.describe(nome_musica="musica")
async def tocar(interaction: discord.Interaction, nome_musica: str):
    if interaction.user.voice:
        menu = Menu()
        menu.pegarmusica(music=nome_musica, lista=listmusicas())
        channel = interaction.user.voice.channel
        embed = menu.criaEmbed(cor='verde', descricao='Tocando', musica=nome_musica)
        if not interaction.guild.voice_client:
            voice = await channel.connect()
            menu.tocarMusica(voice, nome_musica)
            await interaction.response.send_message(view=menu, embed=embed)
        else:
            voice = interaction.guild.voice_client
            voice.pause()
            menu.tocarMusica(voice, nome_musica)
            await interaction.response.edit_message(embed=embed)
    else:
        await interaction.response.send_message('Voce nao esta conectado em nenhuma call', delete_after=10, ephemeral=True)


@tocar.autocomplete('nome_musica')
async def musica_pc(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    musicas = listmusicas()
    return [app_commands.Choice(name=nome_musica, value=nome_musica) for nome_musica in musicas[:14] if current.lower() in nome_musica.lower()]


aclient.run(token_bot)
