import maya.cmds as cmds

def select_skin_influencing_joints():

    selection = cmds.ls(selection=True)

    if len(selection) != 1:
        cmds.error("Please select just one mesh at a time")
        return
    
    skin = cmds.ls(cmds.listHistory(selection[0]), type='skinCluster')
    
    if skin:

        bind_joints = cmds.skinCluster(skin[0], query=True, influence=True)
        

        cmds.select(bind_joints, replace=True)
    else:

        cmds.error("Selected object doesn't have a skinCluster applied to it")
        return

def create_ui():
    if cmds.window("selectSkinInfluenceUI", exists=True):
        cmds.deleteUI("selectSkinInfluenceUI")
        
    window = cmds.window("selectSkinInfluenceUI", title="Select Skin Influencing Joints", widthHeight=(300, 100))
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.text(label="Select a skinned mesh and click the button below:")
    cmds.button(label="Select Influencing Joints", command=lambda x: select_skin_influencing_joints())
    
    cmds.setParent("..")
    cmds.showWindow(window)
create_ui()
