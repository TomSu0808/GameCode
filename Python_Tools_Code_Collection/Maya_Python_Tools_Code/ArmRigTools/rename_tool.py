###### Create by Tom Su June,2023

import maya.cmds as cmds

def custom_rename_objects():
    selected_objects = cmds.ls(selection=True)
    
    if not selected_objects:
        cmds.warning("No objects selected.")
        return
    
    result = cmds.promptDialog(
        title="Rename",
        message='Enter new name:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')
    
    if result == 'OK':
        new_name = cmds.promptDialog(query=True, text=True)
        
        for obj in selected_objects:
            cmds.rename(obj, new_name + "_" + obj)

def left_rename_object():
    select_objects = cmds.ls(selection=True)
    
    if not select_objects:
        cmds.warning("No objects selected.")
        return
    
    for obj in select_objects:
        cmds.rename(obj, "L" + "_" + obj)


def right_rename_object():
    select_objects = cmds.ls(selection=True)
    
    if not select_objects:
        cmds.warning("No objects selected.")
        return
    
        
    for obj in select_objects:
        new_obj_name = cmds.rename(obj, "R" + "_" + obj)
    


def full_rename_object():
    select_objects = cmds.ls(selection=True)
    
    if not select_objects:
        cmds.warning("No objects selected.")
        return
    
    result = cmds.promptDialog(
        title="Rename",
        message='Enter new name:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')
    
    if result == 'OK':

        new_name = cmds.promptDialog(query=True, text=True)
        
        for i in select_objects:
            new_obj_name = cmds.rename(i, new_name)




def full_rename_numerals_object():
    select_objects = cmds.ls(selection=True)
    
    if not select_objects:
        cmds.warning("No objects selected.")
        return
    
    result = cmds.promptDialog(
        title="Rename",
        message='Enter new name:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')
    
    if result == 'OK':

        new_name = cmds.promptDialog(query=True, text=True)
        
        for i, obj in enumerate(select_objects, start=1):
            new_obj_name = new_name + '_' + str(i)

            if obj != new_obj_name:
                cmds.rename(obj, new_obj_name)

def create_ui():
    if cmds.window("customRenameUI", exists=True):
        cmds.deleteUI("customRenameUI", window=True)
    
    window = cmds.window("customRenameUI", title="Custom Rename", widthHeight=(200, 320))
    cmds.columnLayout(adjustableColumn=True)

    cmds.text("Select object and run script", font = "smallBoldLabelFont", al="center")

    cmds.separator(height=10, style = "none")
    cmds.button(label="Full Rename", command="full_rename_object()")
    cmds.separator(height=10, style = "none")

    cmds.button(label="Full Rename + Numerals", command="full_rename_numerals_object()")
    cmds.separator(height=10, style = "none")

    cmds.button(label="Prefix_ --->", command="custom_rename_objects()")
    cmds.separator(height=10, style = "none")

    cmds.button(label="L_--->", command="left_rename_object()")
    cmds.separator(height=10, style = "none")

    cmds.button(label="R_--->", command="right_rename_object()")

    cmds.showWindow(window)
create_ui()
