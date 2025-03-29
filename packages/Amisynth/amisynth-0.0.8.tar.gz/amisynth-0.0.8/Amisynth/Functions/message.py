import xfox

@xfox.addfunc(xfox.funcs)
async def message(num, *args, **kwargs):
    # Filtrar kwargs para ignorar 'ctx_slash_env'
    filtered_kwargs = {k: v for k, v in kwargs.items() if k != "ctx_slash_env"}

    # Obtener el contexto adecuado
    ctx_message_env = kwargs.get("ctx_message_env")
    ctx_command = kwargs.get("ctx_command")

    if ctx_message_env:
        message_content = ctx_message_env.content  # Mensaje del evento
        palabras = message_content.split()  # Obtener palabras
    elif ctx_command and ctx_command.message:
        message_content = ctx_command.message.content  # Mensaje del comando
        palabras = message_content.split()[1:]  # Excluir el nombre del comando
    else:
        palabras = []

    # Si el número es "-1", devolver todo el contenido después del comando
    if num == "-1":
        return " ".join(palabras)  # Devuelve todos los argumentos como un solo string

    # Intentar convertir num a un índice
    try:
        index = int(num) - 1  # Ajuste para que 1 sea el primer elemento
        if 0 <= index < len(palabras):
            palabra = palabras[index]
        else:
            palabra = ""
    except ValueError:
        # Si num no es un número, usarlo como clave de kwargs
        return filtered_kwargs.get(num, "")

    # Si hay argumentos extra, buscar en kwargs si la palabra no existe
    if args:
        for clave in args:
            if clave in filtered_kwargs:
                return palabra if palabra else filtered_kwargs[clave]
    
    return palabra
