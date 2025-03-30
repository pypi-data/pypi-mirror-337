import xfox
import discord

@xfox.addfunc(xfox.funcs)
async def channelID(nombre: str = None, *args, **kwargs):
    ctx_command = kwargs.get("ctx_command")
    ctx_slash_env = kwargs.get("ctx_slash_env")
    ctx_message_env = kwargs.get("ctx_message_env")
    ctx_reaction_env = kwargs.get("ctx_reaction_env")
    ctx_reaction_remove_env = kwargs.get("ctx_reaction_remove_env")
    ctx_interaction_env = kwargs.get("ctx_interaction_env")
    ctx_message_edit_env = kwargs.get("ctx_message_edit_env")
    ctx_message_delete_env = kwargs.get("ctx_message_delete_env")

    # Obtener el servidor (guild) desde cualquier contexto disponible
    guild = (
        ctx_command.guild if ctx_command else
        ctx_message_env.guild if ctx_message_env else
        ctx_slash_env.guild if ctx_slash_env else
        ctx_reaction_env.message.guild if ctx_reaction_env else
        ctx_reaction_remove_env.message.guild if ctx_reaction_remove_env else
        ctx_interaction_env.guild if ctx_interaction_env else
        ctx_message_edit_env[0].guild if ctx_message_edit_env else
        ctx_message_delete_env.guild if ctx_message_delete_env else None
    )

    # Si no hay servidor, retornar vacío
    if not guild:
        return ""

    # Si se proporciona un nombre de canal, buscarlo por nombre
    if nombre:
        channel = discord.utils.get(guild.channels, name=nombre)
        return str(channel.id) if channel else ""

    # Obtener el ID del canal actual según el contexto disponible
    channel_id = (
        ctx_command.channel.id if ctx_command else
        ctx_message_env.channel.id if ctx_message_env else
        ctx_slash_env.channel_id if ctx_slash_env else
        ctx_reaction_env.message.channel.id if ctx_reaction_env else
        ctx_reaction_remove_env.message.channel.id if ctx_reaction_remove_env else
        ctx_interaction_env.channel.id if ctx_interaction_env and ctx_interaction_env.channel else
        ctx_message_edit_env[0].channel.id if ctx_message_edit_env else 
        ctx_message_delete_env.channel.id if ctx_message_delete_env else None
    )

    return str(channel_id) if channel_id else ""
