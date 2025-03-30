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

    # Convertir SequenceProxy a lista antes de concatenar
    members_list = (
        (list(ctx_command.guild.members) if ctx_command else []) +
        (list(ctx_message_env.guild.members) if ctx_message_env else []) +
        (list(ctx_join_member_env.guild.members) if ctx_join_member_env else []) +
        (list(ctx_leave_member_env.guild.members) if ctx_leave_member_env else [])
    )

    # Si se proporciona un user_id, intentar buscar al usuario por ID
    if user_id:
        user = discord.utils.get(members_list, id=int(user_id))
        return f"{user.name}" if user else ""  # Retorna el nombre o una cadena vacía

    # Si no se proporciona user_id, obtener el username desde los contextos
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

    return username_info[0] if username_info else ""  # Retorna el nombre o vacío si no se encontró
