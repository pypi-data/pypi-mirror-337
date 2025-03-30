import xfox
import discord

@xfox.addfunc(xfox.funcs, name="mentionedRoles")
async def mentioned_roles(nombre: str = None, *args, **kwargs):
    # Obtener el contexto disponible
    ctx = (
        kwargs.get("ctx_command") or
        kwargs.get("ctx_slash_env") or
        kwargs.get("ctx_message_env") or
        kwargs.get("ctx_reaction_env") or
        kwargs.get("ctx_reaction_remove_env") or
        kwargs.get("ctx_interaction_env") or
        kwargs.get("ctx_message_edit_env") or
        kwargs.get("ctx_message_delete_env")
    )

    if not ctx:
        return "Error: No hay contexto válido."

    # Obtener menciones de roles dependiendo del tipo de contexto
    mentioned_roles = []
    
    if hasattr(ctx, "message") and hasattr(ctx.message, "role_mentions"):
        mentioned_roles = ctx.message.role_mentions  # Contextos con mensaje
    
    elif hasattr(ctx, "role_mentions"):
        mentioned_roles = ctx.role_mentions  # Para otros contextos con menciones de roles
    
    elif hasattr(ctx, "interaction") and hasattr(ctx.interaction, "message"):
        mentioned_roles = ctx.interaction.message.role_mentions  # Interacción con mensaje de respuesta
    
    if not mentioned_roles:
        print("[DEBUG MENTIONED_ROLES]: No se encontraron menciones de roles")
        return ""

    # Si no se proporciona un índice o selector, devolver el primer rol mencionado
    if nombre is None:
        return str(mentioned_roles[0].id)

    # Si el argumento es un número, obtener la mención en ese índice
    if nombre.isdigit():  
        indice = int(nombre) - 1  # Convertir a índice basado en 1
        if 0 <= indice < len(mentioned_roles):
            return str(mentioned_roles[indice].id)
        else:
            print("[DEBUG MENTIONED_ROLES]: No hay suficiente cantidad de roles mencionados.")
            return ""

    # Mayor y menor ID de rol
    if nombre == ">":
        return str(max(mentioned_roles, key=lambda role: role.id).id)  # Mayor ID
    
    if nombre == "<":
        return str(min(mentioned_roles, key=lambda role: role.id).id)  # Menor ID
    
    print(f"[DEBUG MENTIONED_ROLES]: Parámetro no válido: {nombre}")
    raise ValueError(f":x: No pusiste el parámetro adecuado: `{nombre}`, en `$mentionedRoles[{nombre}]`")
