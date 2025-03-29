import discord
import xfox
from Amisynth.utils import mensaje_id_global


@xfox.addfunc(xfox.funcs)
async def sendMessage(texto, retornar_id="false", canal_id=None, *args, **kwargs): 
    global mensaje_id_global  # Usar la variable global
    
    # Obtener el contexto adecuado
    ctx_message_env = kwargs.get("ctx_message_env")
    ctx_command = kwargs.get("ctx_command")
    ctx_slash_env = kwargs.get("ctx_slash_env")
    ctx_join_member_env = kwargs.get("ctx_join_member_env")
    ctx_remove_member_env = kwargs.get("ctx_remove_member_env")


    # Determinar el canal correcto
    canal = None

    if ctx_command and canal_id:
        canal = ctx_command.bot.get_channel(int(canal_id))  # Obtener canal por ID
    elif ctx_message_env:
        canal = ctx_message_env.guild.get_channel(int(canal_id))
    elif ctx_slash_env:
        canal = ctx_slash_env.guild.get_channel(int(canal_id))
    elif ctx_join_member_env:
        canal = ctx_join_member_env.guild.get_channel(int(canal_id))
    elif ctx_remove_member_env:
        canal = ctx_remove_member_env.guild.get_channel(int(canal_id))

    # Verificar si el canal es válido antes de enviar el mensaje
    if isinstance(canal, discord.TextChannel):
        mensaje = await canal.send(texto)
        if str(retornar_id).lower() == "true":
            mensaje_id_global = mensaje.id  # Guardar el ID del mensaje en la variable global
            return mensaje.id
        
        return ""
    
    print(f"No se encontró un canal válido para enviar el mensaje. Canal ID: {canal_id}")
    return None  # Indicar que falló el envío
