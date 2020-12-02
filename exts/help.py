import discord
from discord.ext import commands
from fuzzywuzzy.process import extractOne


class EmbedHelp(commands.HelpCommand):
    def command_not_found(self, string):
        suggestion = extractOne(string, self.context.bot.commands)
        return f"Command {string} not found, did you mean {suggestion[0]}?"

    async def send_bot_help(self, mapping):
        dest = self.get_destination()
        embed = discord.Embed(color=0x301baa)
        embed.add_field(name="Commands", value="\u200B", inline=False)
        sorted_cogs = sorted(mapping, key=lambda c: c.qualified_name if c else 'No category')
        for cog in sorted_cogs:
            cmds = await self.filter_commands(mapping[cog])
            if cmds:
                name = cog.qualified_name if cog else 'No category'
                value = '\n'.join([f"**· {cmd}** {cmd.short_doc}" for cmd in cmds])
                embed.add_field(name=name, value=value)

        await dest.send(embed=embed)

    async def send_cog_help(self, cog):
        dest = self.get_destination()
        cmds = await self.filter_commands(cog.get_commands())
        if cmds:
            embed = discord.Embed(
                color=0x301baa,
                title=cog.qualified_name,
                description=cog.description
            )
            embed.add_field(
                name='Commands',
                value='\n'.join([f"**· {cmd}** {cmd.short_doc}" for cmd in cmds])
            )

            await dest.send(embed=embed)

        else:
            await dest.send(f'No data for {cog.qualified_name}')

    async def send_group_help(self, group):
        dest = self.get_destination()
        embed = discord.Embed(
            color=0x301baa,
            title=f"{self.get_command_signature(group)}",
            description=group.help
        )

        cmds = await self.filter_commands(group.commands)
        if cmds:
            embed.add_field(
                name="Commands",
                value='\n'.join([f"**· {cmd}** {cmd.short_doc}" for cmd in cmds])
            )

        else:
            embed.add_field(
                name="Commands",
                value="<No visible commands>"
            )

        if not group.hidden:
            embed.description += f"\n\n[**Documentation link**](https://docs.byterbot.com/#{group.cog.qualified_name.lower()}.{group})"

        await dest.send(embed=embed)

    async def send_command_help(self, command):
        dest = self.get_destination()
        embed = discord.Embed(
            color=0x301baa,
            title=f"{self.get_command_signature(command)}",
            description=command.help
        )

        if not command.hidden:
            embed.description += f"\n\n[**Documentation link**](https://docs.byterbot.com/#{command.cog.qualified_name.lower()}.{command})"

        await dest.send(embed=embed)


def setup(bot):
    bot.help_command = EmbedHelp()
