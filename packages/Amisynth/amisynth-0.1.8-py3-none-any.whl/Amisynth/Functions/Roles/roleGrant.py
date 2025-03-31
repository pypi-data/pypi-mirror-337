import xfox

@xfox.addfunc(xfox.funcs, name="roleGrant")
async def etcx2(user_id, *args, **kwargs):
    ctx = (kwargs.get("ctx_command") or kwargs.get("ctx_message_env") or kwargs.get("ctx_slash_env") or 
           kwargs.get("ctx_reaction_env") or kwargs.get("ctx_reaction_remove_env") or kwargs.get("ctx_interaction_env") or 
           (kwargs.get("ctx_message_edit_env", (None,))[0]) or kwargs.get("ctx_message_delete_env") or kwargs.get("ctx_bulk_message_delete_env"))

    if not ctx:
        print("[DEBUG ROLEGRANT] No se encontró un contexto válido, Contacta con Soporte")
        raise ValueError(":x: No se encontró un contexto válido.")

    miembro = ctx.guild.get_member(int(user_id))  # Obtener usuario por ID
    if not miembro:
       print("[DEBUG ROLEGRANT] No se encontró al usuario con ID `{user_id}`.")
       raise ValueError(f":x: No se encontró al usuario con ID `{user_id}`.")

    # Verificar si el bot tiene permiso de administrar roles
    if not ctx.guild.me.guild_permissions.manage_roles:
        print("[DEBUG ROLEGRANT] El bot no tiene permisos para administrar roles.")
        raise ValueError(f":x: No tengo permisos para administrar roles.")

    roles_a_agregar = []
    roles_a_remover = []
    bot_highest_role = ctx.guild.me.top_role  # Rol más alto del bot

    for arg in args:
        if arg.startswith('+'):
            role_id = int(arg[1:])  # Obtener ID quitando el "+"
            rol = ctx.guild.get_role(role_id)
            if rol:
                if rol.position >= bot_highest_role.position:
                    print("[DEBUG ROLEGRANT] No puedo agregar el rol `{rol.name}` porque es igual o superior a mi rol más alto.")
                    raise ValueError(f":x: No puedo agregar el rol `{rol.name}` porque es igual o superior a mi rol más alto.")
                roles_a_agregar.append(rol)
            else:
                print(f"[DEBUG ROLEGRANT] No se encontró el rol con ID `{role_id}`, $roleGrant[..;+{role_id}]")
                raise ValueError(f":x: No se encontró el rol con ID `{role_id}`, `$roleGrant[..;+{role_id}]`.")
            

        elif arg.startswith('-'):
            role_id = int(arg[1:])  # Obtener ID quitando el "-"
            rol = ctx.guild.get_role(role_id)
            if rol:
                if rol.position >= bot_highest_role.position:
                    print("[DEBUG ROLEGRANT] No puedo quitar el rol `{rol.name}` porque es igual o superior a mi rol más alto.")
                    raise ValueError(f":x: No puedo quitar el rol `{rol.name}` porque es igual o superior a mi rol más alto.")
                roles_a_remover.append(rol)
            else:
                print(f"[DEBUG ROLEGRANT] No se encontró el rol con ID `{role_id}, `$roleGrant[..;-{role_id}]`")
                raise  ValueError(f":x: No se encontró el rol con ID `{role_id}`, `$roleGrant[..;-{role_id}]`.")

    # Aplicar los cambios de roles
    if roles_a_agregar:
        await miembro.add_roles(*roles_a_agregar)
    if roles_a_remover:
        await miembro.remove_roles(*roles_a_remover)
    
    return ""
