import xfox
import discord
from Amisynth.utils import context_keys
@xfox.addfunc(xfox.funcs, name="mentionedChannels")
async def mentioned_channels(nombre: str = None, *args, **kwargs):
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

    # Obtener menciones de canales dependiendo del tipo de contexto
    mentioned_channels = []
    
    if hasattr(ctx, "message") and hasattr(ctx.message, "channel_mentions"):
        mentioned_channels = ctx.message.channel_mentions  # Contextos con mensaje
    
    elif hasattr(ctx, "channel_mentions"):
        mentioned_channels = ctx.channel_mentions  # Para otros contextos con menciones de canales
    
    elif hasattr(ctx, "interaction") and hasattr(ctx.interaction, "message"):
        mentioned_channels = ctx.interaction.message.channel_mentions  # Interacción con mensaje de respuesta
    
    if not mentioned_channels:
        print("[DEBUG MENTIONED_CHANNELS]: No se encontraron menciones de canales")
        return ""

    # Si no se proporciona un índice o selector, devolver el primer canal mencionado
    if nombre is None:
        return str(mentioned_channels[0].id)

    # Si el argumento es un número, obtener la mención en ese índice
    if nombre.isdigit():  
        indice = int(nombre) - 1  # Convertir a índice basado en 1
        if 0 <= indice < len(mentioned_channels):
            return str(mentioned_channels[indice].id)
        else:
            print("[DEBUG MENTIONED_CHANNELS]: No hay suficiente cantidad de canales mencionados.")
            return ""

    # Mayor y menor ID de canal
    if nombre == ">":
        return str(max(mentioned_channels, key=lambda channel: channel.id).id)  # Mayor ID
    
    if nombre == "<":
        return str(min(mentioned_channels, key=lambda channel: channel.id).id)  # Menor ID
    
    print(f"[DEBUG MENTIONED_CHANNELS]: Parámetro no válido: {nombre}")
    raise ValueError(f":x: No pusiste el parámetro adecuado: `{nombre}`, en `$mentionedChannels[{nombre}]`")
