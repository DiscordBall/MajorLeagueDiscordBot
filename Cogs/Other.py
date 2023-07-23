import configparser
import random
import requests
import Utils
from discord.ext import commands

# Set up config reader
config = configparser.ConfigParser()
config.read('config.ini')


class Other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Bot commands
    @commands.command(brief='Baseball reference player search',
                      description='Search for a player on Baseball Reference.')
    async def bbref(self, ctx, *, player_name: str):
        base_url = 'https://www.baseball-reference.com/search/search.fcgi?search='
        await ctx.send(f"https://www.baseball-reference.com/search/search.fcgi?search={player_name.replace(' ', '+')}")

    @commands.command(brief='Flip a coin',
                      description='Flip a coin.',
                      aliases=['coin', 'flip'])
    async def coin_flip(self, ctx):
        await ctx.send(random.choice(['Heads', 'Tails']))

    @commands.command(brief='Dad jokes',
                      description='Tells a dad joke.',
                      aliases=['joke', 'dadjoke'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def dad_joke(self, ctx):
        r = requests.get('https://icanhazdadjoke.com', headers={"Accept": "text/plain"})
        await ctx.send(r.text)

    @commands.command(brief='Ask the magic eight ball',
                      description='Ask the magic eight ball a question.',
                      aliases=['magic8ball', '8ball'])
    async def magic_8_ball(self, ctx, *, text: str = None):
        response = ''
        if text:
            response += f'> *{text}*\n'
        response += random.choice(Utils.magic_8_ball)
        await ctx.send(response)

    @commands.command(brief='Random number generator',
                      description='I... Do we really need to explain this one? Here, of all places?',
                      aliases=['rand'])
    async def random(self, ctx):
        await ctx.send(random.randint(1, 1000))

    @commands.command(brief='Roll some dice',
                      description='Roll a d20, or specify the number and type of dice using 1d20 notation.')
    async def roll(self, ctx, die: str = None, *, prompt: str = None):
        if not die:
            die = ['1', '20']
        else:
            if 'd' not in die:
                return
            die = die.split('d')
            if '0' in die:
                return
            if not len(die) == 2:
                return
        rolls = []
        for i in range(int(die[0])):
            rolls.append(random.randint(1, int(die[1])))
        if not prompt:
            prompt = 'Result'
        await ctx.send(f'{ctx.author.mention} 🎲\n**{prompt}:** {die[0]}d{die[1]}: {rolls}\n**Total:** {sum(rolls)}')

    @commands.command(brief='Pls ignore',
                      description='Dottie forgot to comment this out before deploying code :)')
    async def test(self, ctx):
        await ctx.send('Hello world')


# Add cog to discord bot
async def setup(bot):
    await bot.add_cog(Other(bot))
