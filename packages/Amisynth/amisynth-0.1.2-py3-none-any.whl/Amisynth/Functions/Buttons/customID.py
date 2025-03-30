import xfox
import discord

@xfox.addfunc(xfox.funcs)
async def customID(*args, **kwargs):
    if "ctx_interaction_env" in kwargs:
        interaction = kwargs["ctx_interaction_env"]
        return interaction.data.get("custom_id")
    
    return ""
