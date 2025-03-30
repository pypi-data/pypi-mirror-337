import xfox
import discord

@xfox.addfunc(xfox.funcs)
async def mentioned(nombre: str = None, *args, **kwargs):
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

    # Obtener menciones dependiendo del tipo de contexto
    mentions = []
    
    if hasattr(ctx, "message") and hasattr(ctx.message, "mentions"):
        mentions = ctx.message.mentions  # Contextos con mensaje
    
    elif hasattr(ctx, "mentions"):  
        mentions = ctx.mentions  # En caso de slash commands u otros eventos que tengan menciones

    elif hasattr(ctx, "interaction") and hasattr(ctx.interaction, "message"):
        mentions = ctx.interaction.message.mentions  # Interacción con mensaje de respuesta


    if not mentions:
        print("[DEBUG MENTIONED]: No se econtraron menciones")
        return ""

    # Si no se proporciona un índice o selector, devolver el primero
    if nombre is None:
        return str(mentions[0].id)

    # Si el argumento es un número, obtener la mención en ese índice
    if nombre.isdigit():  
        indice = int(nombre) - 1  # Convertir a índice basado en 1
        if 0 <= indice < len(mentions):
            return str(mentions[indice].id)
        else:
            print("[DEBUG MENTIONED]: No hay suficiente cantidad de usuarios mencionados.")
            return ""

    # Mayor y menor ID de usuario
    if nombre == ">":
        return str(max(mentions, key=lambda user: user.id).id)  # Mayor ID
    
    if nombre == "<":
        return str(min(mentions, key=lambda user: user.id).id)  # Menor ID
    print(f"[DEBUG MENTIONED]: Parametro no valido: {nombre}")
    raise ValueError(f":x: No pusiste el parametro adecuado: `{nombre}`, en `$mentioned[{nombre}]`")
