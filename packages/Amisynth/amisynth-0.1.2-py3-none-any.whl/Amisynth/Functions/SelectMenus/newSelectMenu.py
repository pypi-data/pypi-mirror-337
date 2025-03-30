import xfox
import discord
from Amisynth.utils import buttons, menu_options

@xfox.addfunc(xfox.funcs)
async def newSelectMenu(placeholder: str, min_val: int, max_val: int, menu_id: str, *args, **kwargs):
    """Crea un menú de selección interactivo con opciones."""
    if "ctx_command" in kwargs:
        ctx=kwargs["ctx_command"]
    if "ctx_join_member_env" in kwargs:
        ctx=kwargs["ctx_join_member_env"]
    if "ctx_remove_member_env" in kwargs:
        ctx=kwargs["ctx_remove_member_env"]
    if "ctx_message_edit_env" in kwargs:
        ctx=kwargs["ctx_message_edit_env"]
    if "ctx_message_delete_env" in kwargs:
        ctx=kwargs["ctx_message_delete_env"]
    if "ctx_message_env" in kwargs:
        ctx=kwargs["ctx_message_env"]
 
    # Extraer valores opcionales
    message_id = None
    if len(args) > 0:
        message_id = args[0]  # ID del mensaje al que se vinculará el menú

    # Obtener las opciones del menú por su ID desde menu_options
    options = menu_options.get(menu_id, [])

    # Crear el menú de selección
    select_menu = discord.ui.Select(
        placeholder=placeholder if placeholder else "Seleccione una opción",
        min_values=min_val,
        max_values=max_val,
        options=options,
        custom_id=menu_id
    )

    if message_id:
        message_id = int(message_id)  # Convertir a número

        for channel in ctx.guild.text_channels:
            try:
                message = await channel.fetch_message(message_id)  # Obtener el mensaje
                if message.components:
                    view = discord.ui.View.from_message(message)  # Recuperar los botones existentes
                else:
                    view = discord.ui.View()  # Crear una nueva vista si no hay botones
                    view.add_item(select_menu)  # Agregar el botón sin eliminar los anteriores
                    await message.edit(view=view)  # Editar el mensaje con la nueva vista
                    return ""
            except discord.NotFound:
                continue  # Si el mensaje no se encuentra, continuar con el siguiente canal
            except discord.Forbidden:
                continue  # Si no tienes permisos para ver el canal, continuar con el siguiente canal
            except discord.HTTPException as e:
                continue  # Manejar errores HTTP y continuar con el siguiente canal
    
    buttons.append(select_menu)
    return ""
