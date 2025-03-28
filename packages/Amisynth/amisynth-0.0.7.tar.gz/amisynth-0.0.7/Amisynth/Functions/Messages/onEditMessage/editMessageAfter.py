import xfox

@xfox.addfunc(xfox.funcs)
async def editMessageAfter(*args, **kwargs):
    if "ctx_message_edit_env" in kwargs:
        before = kwargs["ctx_message_edit_env"][1]
        return before.content
    return ""