import xfox
import discord

@xfox.addfunc(xfox.funcs)
async def categorysNames(separator:str, guild_id=None, *args, **kwargs):
    # Obtenemos los diferentes contextos desde kwargs
    ctx_command = kwargs.get("ctx_command")
    ctx_slash_env = kwargs.get("ctx_slash_env")
    ctx_message_env = kwargs.get("ctx_message_env")
    ctx_reaction_env = kwargs.get("ctx_reaction_env")
    ctx_reaction_remove_env = kwargs.get("ctx_reaction_remove_env")
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

    # Si encontramos el servidor, devolvemos los nombres de las categorías como texto
    if guild:
        # Filtramos las categorías (solo los canales de tipo 'CategoryChannel')
        category_names = [category.name for category in guild.categories]

        # Si encontramos categorías, las unimos en un string usando el separator
        if category_names:
            return separator.join(category_names)
        else:
            print("[DEBUG CATEGORYSNAMES] No se encontraron categorías en este servidor.")
            return ""
    else:
        print("[DEBUG CATEGORYSNAMES] No se pudo obtener el servidor.")
        return ""
