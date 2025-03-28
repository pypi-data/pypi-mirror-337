import xfox
import discord
from Amisynth.utils import buttons

# Contador de fila global
row_counter = 0  

@xfox.addfunc(xfox.funcs)
async def addButton(new_row: str, button_id: str, label: str, style: str, *args, **kwargs):
    """Crea múltiples botones interactivos y devuelve una lista de objetos de botones creados."""
    ctx = kwargs["ctx_command"]
    global row_counter  # Para modificar el contador de fila

    # Estilos disponibles
    estilos = {
        "primary": discord.ButtonStyle.primary,
        "cecondary": discord.ButtonStyle.secondary,
        "success": discord.ButtonStyle.success,
        "danger": discord.ButtonStyle.danger,
        "link": discord.ButtonStyle.link
    }
    
    button_style = estilos.get(style, discord.ButtonStyle.primary)

    # Definir valores predeterminados
    disabled = False
    emoji = None
    message_id = None

    if len(args) > 0:
        disabled = args[0].lower() == "true"
    if len(args) > 1:
        emoji = args[1]
    if len(args) > 2:
        message_id = args[2]  # No se está usando en la creación del botón, revisar si es necesario

    # Validar si es un botón de tipo enlace
    custom_id = button_id if button_style != discord.ButtonStyle.link else None
    url = button_id if button_style == discord.ButtonStyle.link else None

    # Lógica para manejar la fila (row)
    if new_row.lower() == "true":
        row_counter += 1  # Aumenta la fila si se indica "true"
    elif new_row.lower() == "re":
        row_counter = 0  # Reinicia la fila si se indica "re"

    button = discord.ui.Button(
        label=label,
        custom_id=custom_id,
        style=button_style,
        emoji=emoji,
        disabled=disabled,
        url=url,
        row=row_counter
    )

    if message_id:
        message_id = int(message_id)  # Convertir a número
        channel = ctx.channel  # Obtener el canal
        message = await channel.fetch_message(message_id)  # Obtener el mensaje
        if message.components:
            view = discord.ui.View.from_message(message)  # Recuperar los botones existentes
        else:
            view = discord.ui.View()  # Crear una nueva vista si no hay botones

        view.add_item(button)  # Agregar el botón sin eliminar los anteriores
        await message.edit(view=view)  # Editar el mensaje con la nueva vista
        return ""
    
    buttons.append(button)
    return ""