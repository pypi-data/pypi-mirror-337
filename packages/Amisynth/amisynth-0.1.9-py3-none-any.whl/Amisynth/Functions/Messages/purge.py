import xfox
import discord

@xfox.addfunc(xfox.funcs, name="clear")
async def clear_func(amount: int, user_id: str = None, remove_pinned: bool = False, *args, **kwargs):
    ctx = (kwargs.get("ctx_command") or kwargs.get("ctx_message_env") or kwargs.get("ctx_slash_env") or 
           kwargs.get("ctx_reaction_env") or kwargs.get("ctx_reaction_remove_env") or kwargs.get("ctx_interaction_env") or 
           (kwargs.get("ctx_message_edit_env", (None,))[0]) or kwargs.get("ctx_message_delete_env") or kwargs.get("ctx_bulk_message_delete_env"))
    
    if not ctx or not hasattr(ctx, 'channel'):
        return
    
    def check(msg):
        if user_id and str(msg.author.id) != user_id:
            return False
        if not remove_pinned and msg.pinned:
            return False
        return True
    
    await ctx.channel.purge(limit=amount, check=check)
    return ""
