import xfox
import discord

@xfox.addfunc(xfox.funcs)
async def username(user_id: str = None, *args, **kwargs):
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

    # Si se proporciona un user_id, intentar buscar al usuario por ID
    if user_id:
        user = discord.utils.get(
            (ctx_command.guild.members if ctx_command else []) +
            (ctx_message_env.guild.members if ctx_message_env else []) +
            (ctx_join_member_env.guild.members if ctx_join_member_env else []) +
            (ctx_leave_member_env.guild.members if ctx_leave_member_env else []),
            id=int(user_id)
        )
        if user:
            return user.name
        else:
            return ""  # Retorna vacío si no se encuentra el usuario con el ID proporcionado

    # Si no se proporciona user_id, usar el contexto disponible para obtener el username y user_id
    username_info = (
        (ctx_command.author.name, ctx_command.author.id) if ctx_command else
        (ctx_message_env.author.name, ctx_message_env.author.id) if ctx_message_env else
        (ctx_slash_env.user.name, ctx_slash_env.user.id) if ctx_slash_env else
        (ctx_reaction_env.message.author.name, ctx_reaction_env.message.author.id) if ctx_reaction_env else
        (ctx_reaction_remove_env.message.author.name, ctx_reaction_remove_env.message.author.id) if ctx_reaction_remove_env else
        (ctx_interaction_env.user.name, ctx_interaction_env.user.id) if ctx_interaction_env else
        (ctx_message_edit_env[0].author.name, ctx_message_edit_env[0].author.id) if ctx_message_edit_env else
        (ctx_message_delete_env.author.name, ctx_message_delete_env.author.id) if ctx_message_delete_env else
        (ctx_join_member_env.member.name, ctx_join_member_env.member.id) if ctx_join_member_env else
        (ctx_leave_member_env.member.name, ctx_leave_member_env.member.id) if ctx_leave_member_env else None
    )

    # Si se encontró la información del username y user_id, retornarla
    if username_info:
        username, user_id = username_info
        return username
    else:
        return ""  # Retorna vacío si no se encuentra la información
