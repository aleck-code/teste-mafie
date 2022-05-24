"""
MIT License
Copyright (c) 2021 NamNam#0090 & OTTWAW team
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
from discord.ext import commands
import asyncio
import json


with open('./config.json', 'r') as f:
    config = json.load(f)


class testy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="testy", aliases=config['aliases']['testy'])
    @commands.guild_only()
    @commands.cooldown(1, int(config["cooldown"]), commands.BucketType.user)
    async def testy_command(self, ctx):
        channel = self.client.get_channel(int(config['testy_channel']))  # id channel
        answers = []
        embed = discord.Embed(
            description=ctx.author.id,
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        )
        m = "Ai 60 de secunde sa raspunzi la fiecare intrebare"
        if config['language'] == "ar":
            m = "لديك 3 دقائق للإجابة على كل سؤال"
        await ctx.author.send(
            embed=discord.Embed(
                description=m,
                color=0xf7072b))
        await ctx.message.add_reaction('✅')

        def check(m):
            return m.author == ctx.author and m.author == ctx.author and str(m.channel.type) == "private"
        nam = 0
        for i in config['questions']:
            nam += 1
            await ctx.author.send(embed=discord.Embed(
                    description=i,
                    color=0x69442f).set_author(name=f"{nam}/{len(config['questions'])}"))
            try:
                msg = await self.client.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                m = 'Ti-a expirat timpul'
                if config['language'] == "ar":
                    m = "لقد تجاوزت الوقت المحدد للإرسال"
                await ctx.author.send(embed=discord.Embed(
                    description=m,
                    color=0x69442f))
                return
            else:
                answers.append(msg.content)

        for kay, value in enumerate(config["questions"]):
            embed.add_field(
                name=f"{kay} - {value}:",
                value=answers[kay],
                inline=False
            )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        m = "Reactioneaza ✅ pentru a trimite testul\nsau ❎ pentru a anula testul"
        if config['language'] == "ar":
            m = "اضغط ✅ لارسال تقديمك\nاضغط ❌ للغاء تقديمك"
        message = await ctx.author.send(embed=discord.Embed(
            description=m,
            color=discord.Color.green()
        ))
        await message.add_reaction("✅")
        await message.add_reaction("❎")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❎"]

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

            if str(reaction.emoji) == "✅":
                await channel.send(embed=embed)
                m = "✅ Testul tau a fost trimis cu succes"
                if config['language'] == "ar":
                    m = "✅ تم ارسال تقديمك في نجاح"
                await message.edit(embed=discord.Embed(
                    description=m,
                    color=discord.Color.green()
                ))
            elif str(reaction.emoji) == "❎":
                m = "❌ Testul tau a fost anulat"
                if config['language'] == "ar":
                    m = "❌ تم الغاء تقديمك"
                await message.edit(embed=discord.Embed(
                    description=m,
                    color=discord.Color.red()
                ))
                pass
            else:
                await message.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.delete()

    @testy_command.error
    async def testy_error(self, ctx, error):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                description="❌ Te rugam sa iti deschizi DM-ul inainte de a reaplica in 24 de ore",
                color=0x69442f
            ))
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            await ctx.send(embed=discord.Embed(
                description="❌ Se pare ca ai raspuns gresit. Reaplica din nou in {}".format(
                    "%d hour, %02d minutes, %02d seconds" % (h, m, s)),
                color=0x69442f
            ))
        else:
            pass

    @commands.command(name="accepta", aliases=config['aliases']['accepta'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def a_command(self, ctx, member: discord.Member):
        m = "✅ I-ai acceptat testul"
        if config['language'] == "ar":
            m = "✅ تم القبول بنجاح"
        await ctx.send(embed=discord.Embed(
            description=m,
            color=0x69442f
        ))
        await member.add_roles(discord.utils.get(member.guild.roles, name=config['role']))
        m = "✅ Testul tau a fost acceptat"
        if config['language'] == "ar":
            m = "✅ تم قبولك بنجاح"
        await member.send(embed=discord.Embed(
            description=m,
            color=0x69442f
        ))

    @commands.has_permissions(administrator=True)
    @a_command.error
    async def a_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description="{}a <member or DI>".format(self.client.command_prefix),
                color=0x69442f
            ))
        if isinstance(error, commands.MissingPermissions):
            pass

    @commands.command(name='respinge', aliases=config['aliases']['respinge'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def respinge_command(self, ctx, member: discord.Member, *, reason):
        m = f"❌ L-ai respins pe {member.mention}"
        if config['language'] == "ar":
            m = f"✅ تم رفض {member.mention}"
        await ctx.send(embed=discord.Embed(
            description=m,
            color=0x69442f
        ))
        m = f"⬇️ Motivul respingerii\n{reason}\nDaca ai ceva impotriva, contacteaza-l pe {ctx.author}"
        if config['language'] == "ar":
            m = f"❌ للاسف لقد تم رفضك للأسف بسبب:\n{reason}\nإذا كان لديك أي اعتراضات ، يرجى التواصل مع {ctx.author}"
        await member.send(embed=discord.Embed(
            description=m,
            color=0x69442f
        ))

    @commands.has_permissions(administrator=True)
    @respinge_command.error
    async def respinge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description="{}respinge <member or DI>".format(self.client.command_prefix),
                color=0x69442f
            ))
        if isinstance(error, commands.MissingPermissions):
            pass


def setup(client):
    client.add_cog(testy(client))
# Copyright (c) 2021 NamNam#0090 & OTTWAW team