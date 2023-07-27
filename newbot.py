import discord
import wavelink
from discord.ext import commands
from wavelink.ext import spotify

TOKEN = None
with open('TOKEN.txt', 'r') as file:
    data = file.readline().replace('\n', '')
    TOKEN = data[6:]

class Bot(commands.Bot):

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(intents=intents, command_prefix='?')

    async def on_ready(self) -> None:
        print(f'Logged in {self.user} | {self.user.id}')

    async def setup_hook(self) -> None:
        sc = spotify.SpotifyClient(
            client_id='CLIENT_ID',
            client_secret='CLIENT_SECRET'
        )

        node: wavelink.Node = wavelink.Node(uri='https://eu-lavalink.lexnet.cc:443', password='lexn3tl@val!nk', secure=True)
        await wavelink.NodePool.connect(client=self, nodes=[node], spotify=sc)


bot = Bot()


@bot.command()
@commands.is_owner()
async def play(ctx: commands.Context, *, search: str) -> None:

    try:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    except discord.ClientException:
        vc: wavelink.Player = ctx.voice_client

    vc.autoplay = True

    track: spotify.SpotifyTrack = await spotify.SpotifyTrack.search(search)

    if not vc.is_playing():
        await vc.play(track, populate=True)
    else:
        await vc.queue.put_wait(track)

bot.run(TOKEN)
