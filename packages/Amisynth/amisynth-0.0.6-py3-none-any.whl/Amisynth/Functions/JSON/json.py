import xfox
from Amisynth.utils import json_storage
import asyncio
@xfox.addfunc(xfox.funcs)
async def json(*args, **kwargs):
    try:
        data = json_storage  # Asegúrate de que json_storage es un diccionario
        for clave in args:
            if isinstance(data, dict) and clave in data:
                data = data[clave]
            else:
                raise ValueError("Error: Clave no encontrada en el JSON almacenado")
        return data
    except Exception as e:
        return f"Error inesperado: {str(e)}"

