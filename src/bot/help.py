from discord.ext import commands

from src.bot.embed_generator import EmbedGenerator


class Help(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = EmbedGenerator.get_help_embed(
            f'Use ``{self.clean_prefix}help [command]`` for more info on a ' +
            'command')
        for cog, bot_commands in mapping.items():
            command_signatures = [self.get_command_signature(c)
                                  for c in bot_commands if not c.hidden]
            if command_signatures:
                cog_name = getattr(cog, 'qualified_name', 'Other')
                embed.add_field(name=cog_name,
                                value='\n'.join(command_signatures),
                                inline=True)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = EmbedGenerator.get_help_embed('')
        embed.add_field(name=f'``{self.get_command_signature(command)}``',
                        value=command.description)

        channel = self.get_destination()
        await channel.send(embed=embed)
