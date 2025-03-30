import xfox
import discord
import datetime

@xfox.addfunc(xfox.funcs, name="sendEmbedMessage")
async def etc(channel_id=None, 
              content="",
              title=None, 
              title_url=None, 
              description=None,
              color=None,
              author=None, 
              author_icon=None, 
              author_url=None,
              footer=None, 
              footer_icon=None,
              image=None,
              thumbnail=None,
              timestamp=None,
              retorna_id=None,
              *args, **kwargs):
    
    ctx = None
    channel = None

    # Si el comando proviene de un comando (ctx_command)
    if "ctx_command" in kwargs:
        ctx = kwargs["ctx_command"]
        if channel_id:
            try:
                channel = ctx.bot.get_channel(int(channel_id))
            except ValueError:
                print(f"[DEBUG ERROR] channel_id '{channel_id}' no es un número válido.")
                return
    
    # Si el comando proviene de un evento (ctx_message_env, ctx_slash_env, etc.)
    else:
        event_keys = [
            "ctx_message_env", "ctx_slash_env", "ctx_reaction_env",
            "ctx_reaction_remove_env", "ctx_interaction_env",
            "ctx_message_edit_env", "ctx_message_delete_env"
        ]

        for key in event_keys:
            if key in kwargs:
                ctx = kwargs[key]._state._get_client()
                break  # Usa el primer contexto válido encontrado

        if ctx and channel_id:
            try:
                channel = ctx.get_channel(int(channel_id))
            except ValueError:
                print(f"[DEBUG ERROR] channel_id '{channel_id}' no es un número válido.")
                raise ValueError(f":x: El argumento channel_id '{channel_id}' no es un número o canal válido.")
    



    embed = discord.Embed()

    # Validaciones y asignaciones correctas
    if title:
        embed.title = title
    if title_url:
        embed.url = title_url
    if description:
        embed.description = description
    
    if color:
        try:
            embed.color = int(color, 16)  # Convierte el color a entero base 16
        except ValueError:
            pass  # Si el color no es válido, lo ignora

    if author: 
        embed.set_author(
            name=author,
            url=author_url if author_url else "",
            icon_url=author_icon if author_icon else ""
        )
    if footer:
        embed.set_footer(
            text=footer,
            icon_url=footer_icon if footer_icon else ""
        )

    if image:
        embed.set_image(url=image)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if timestamp:
        if timestamp == "true":
            embed.timestamp = datetime.datetime.utcnow()
        elif timestamp != "false":
            print(f"[DEBUG TIMESTAMP] Error no válido el argumento `'timestamp': {timestamp}` en la función `$sendEmbedMessage[{timestamp}]`")
            raise ValueError(f":x: Error no válido el argumento `'timestamp': {timestamp}` en la función `$sendEmbedMessage[]`, usa true/false")

    # Agregar fields desde *args
    args_list = list(args)
    for i in range(0, len(args_list), 3):
        try:
            name = args_list[i]
            value = args_list[i + 1]
            inline = args_list[i + 2] if i + 2 < len(args_list) else "true"

            # Convertir inline a booleano
            inline = True if inline.lower() == "true" else False

            embed.add_field(name=name, value=value, inline=inline)
        except IndexError:
            missing_index = i + (3 - len(args_list) % 3)
            missing_parts = ["nombre", "valor", "inline"][len(args_list) % 3:]
            print(f"[DEBUG FIELD ERROR] Error al agregar field en `$sendEmbedMessage`. "
                  f"[DEBUG FIELD ERROR] Se esperaba un grupo de 3 argumentos (nombre, valor, inline opcional), "
                  f"[DEBUG FIELD ERROR] Se encontraron {len(args_list) % 3}. Faltan: {', '.join(missing_parts)}.")
            raise ValueError(f":x: Error al agregar field en `$sendEmbedMessage`. "
                             f"Faltan los siguientes valores en un field: {', '.join(missing_parts)}.")


    # Validar el canal antes de enviar
    if channel_id:
        
        if channel:
            message = await channel.send(content, embed=embed)
    else:
        message = await ctx.send(content, embed=embed)

    if retorna_id:
        if retorna_id == "true":
            return message.id
        elif retorna_id != "false":
            print(f"[DEBUG RETORNAR_ID ERROR] Error no válido el argumento `'retornar_id': {retorna_id}` en la función `$sendEmbedMessage[{retorna_id}]`")
            raise ValueError(f":x: Error no válido el argumento `'retornar_id': {retorna_id}` en la función `$sendEmbedMessage[]`, usa true/false")

    print("[DEBUG AMYSINTH ERROR] Contacta con Soporte: https://discord.gg/NyGuP3e5")
    return ""
