import xfox
import discord

@xfox.addfunc(xfox.funcs)
async def channelNames(separator:str, guild_id=None, *args, **kwargs):
    # Obtenemos los diferentes contextos desde kwargs
    ctx_command = kwargs.get("ctx_command")
    ctx_slash_env = kwargs.get("ctx_slash_env")
    ctx_message_env = kwargs.get("ctx_message_env")
    ctx_reaction_env = kwargs.get("ctx_reaction_env")  # Contexto de reacciones
    ctx_reaction_remove_env = kwargs.get("ctx_reaction_remove_env")  # Contexto de eliminación de reacciones
    ctx_interaction_env = kwargs.get("ctx_interaction_env")
    ctx_message_edit_env = kwargs.get("ctx_message_edit_env")
    ctx_message_delete_env = kwargs.get("ctx_message_delete_env")
    ctx_join_member_env = kwargs.get("ctx_join_member_env")
    ctx_leave_member_env = kwargs.get("ctx_leave_member_env")

    # Validar el separador para evitar problemas
    separator = separator.strip()  # Eliminamos espacios en blanco antes y después


    # Si se pasa un guild_id, intentamos obtener el servidor por ID
    if guild_id:
        guild = discord.utils.get(ctx_command.bot.guilds, id=int(guild_id))
    else:
        # Si no se pasa guild_id, intentamos obtener el servidor del contexto
        guild = ctx_command.guild if ctx_command else None

        # Si no conseguimos el guild en ctx_command, intentamos en otros contextos
        if not guild:
            if ctx_slash_env:
                guild = ctx_slash_env.guild
            elif ctx_message_env:
                guild = ctx_message_env.guild
            elif ctx_interaction_env:
                guild = ctx_interaction_env.guild
            elif ctx_message_edit_env:
                guild = ctx_message_edit_env.guild
            elif ctx_message_delete_env:
                guild = ctx_message_delete_env.guild
            elif ctx_join_member_env:
                guild = ctx_join_member_env.guild
            elif ctx_leave_member_env:
                guild = ctx_leave_member_env.guild
            elif ctx_reaction_env:
                guild = ctx_reaction_env.guild  # Usamos ctx_reaction_env para obtener el guild
            elif ctx_reaction_remove_env:
                guild = ctx_reaction_remove_env.guild  # Usamos ctx_reaction_remove_env para obtener el guild

    # Si encontramos el servidor, devolvemos los nombres de los canales como texto
    if guild:
        # Filtramos los canales y solo incluimos los canales que no sean de tipo 'CategoryChannel'
        channel_names = [channel.name for channel in guild.channels if not isinstance(channel, discord.CategoryChannel)]

        # Si encontramos canales, los unimos en un string usando el separator
        if channel_names:
            return separator.join(channel_names)
        else:
            print("No hay canales")
            return ""
    else:
        print("No se pudo obtener el servidor.")
        return "No se pudo obtener el servidor."
