import discord
import datetime
from discord import Embed
from discord.ext import commands
from voting_open import VotingOpen


client = commands.Bot(command_prefix='b:')
client.remove_command('help')


def check_error(string):
    msg = ""
    for letter in range(0,5):
        msg += string[letter]
    if msg == "ERROR":
        return True



@client.event
async def on_ready():
    print("bot is ready")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


@client.command()
@commands.has_role('Bartender')
async def start(ctx, *, theme):
    global voting_session
    voting_session = VotingOpen(theme)
    embed = discord.Embed(
        colour = 16580705
    )
    embed.set_author(name=theme)
    await ctx.send(embed=embed)


@client.command(aliases=['add'])
async def add_contendr(ctx, contendr):
    msg = voting_session.add_contender(contendr, ctx.author.name, ctx.author.id)
    if check_error(msg) == True:
        await ctx.send(msg)
    else:
        embed = discord.Embed(
            colour = 16580705
        )
        embed.set_author(name=msg)
        await ctx.send(embed=embed)


@client.command()
async def votelist(ctx):
    embed = discord.Embed(
        colour = 16580705
    )
    embed.set_author(name="Voting List")
    for key in voting_session.contenders.keys():
        embed.add_field(name=voting_session.contenders[key][0], value="By %s with: %s votes."%(voting_session.contenders[key][1], voting_session.contenders[key][2]), inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['vote'])
async def vote_ctdr(ctx, *, contendr):
    msg = voting_session.vote_contender(contendr, ctx.author.name, ctx.author.id)
    if check_error(msg) == True:
        await ctx.send(msg)
    else:
        embed = discord.Embed(
            colour = 16580705
        )
        embed.set_author(name=msg)
        await ctx.send(embed=embed)


@client.command(aliases=['voteid'])
async def vote_id(ctx, member=discord.Member):
    msg = voting_session.vote_id(member.id, ctx.author.name, ctx.author.id)
    if check_error(msg) == True:
        await ctx.send(msg)
    else:
        embed = discord.Embed(
            colour = 16580705
        )
        embed.set_author(name=msg)
        await ctx.send(embed=embed)


@client.command()
@commands.has_role('Bartender')
async def change(ctx):
    msg = voting_session.change_fase()
    if check_error(msg) == True:
        await ctx.send(msg)
    else:
        embed = discord.Embed(
            colour = 16580705
        )
        embed.set_author(name=msg)
        await ctx.send(embed=embed)


@client.command(aliases=['delcontender'])
@commands.has_role('Bartender')
async def test1(ctx, id):
    # msg = voting_session.del_contender(member.id)
    # embed = discord.Embed(
    #     colour = 16580705
    # )
    # embed.set_author(name=msg)
    # await ctx.send(id)
    print(id)


@client.command()
@commands.has_role('Bartender')
async def recover(ctx):
    msg = voting_session.recover_themes()
    embed = discord.Embed(
        colour = 16580705
    )
    embed.set_author(name=msg)
    await ctx.send(embed=embed)


@client.command()
@commands.has_role('Bartender')
async def test(ctx):
    global voting_session
    voting_session = VotingOpen("anime test")
    voting_session.recover_themes()
    voting_session.change_fase()
    await ctx.send(voting_session.contenders)


client.run('**')