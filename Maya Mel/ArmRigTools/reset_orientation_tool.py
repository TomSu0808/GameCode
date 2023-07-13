import maya.cmds as cmds

####### reset orientation from worldspace
def reset_orientation_worldspace():
    selected_joints = cmds.ls(selection=True, type="joint")

    if len(selected_joints) == 0:
        cmds.warning("must select a joint!!!")
        return
    
    for joint in selected_joints:
        cmds.joint(joint, edit=True, zeroScaleOrient=True, orientJoint="xyz")
        cmds.xform(joint, ro=(0, 0, 0), os=True)

####### reset orientation from localspace
def reset_orientation_localspace(*args):

    selection = cmds.ls(selection=True)
    if len(selection) == 0:
        cmds.warning("select a joint!!!")
        return
    
    joint = selection[0]
    joint_parent = cmds.listRelatives(joint, parent=True)
    
    if not joint_parent:
        cmds.warning("select joint no parent!!!")
        return
    
    parent_rotation = cmds.getAttr(joint_parent[0] + ".rotate")
    cmds.setAttr(joint + ".rotate", parent_rotation[0][0], parent_rotation[0][1], parent_rotation[0][2])



####### create ui
def create_UI():
    window = cmds.window("resetUI", title="Reset Orientation", widthHeight=(250, 100))
    cmds.columnLayout(adjustableColumn=True)
    ### worldspace button

    cmds.text("Reset Orientation From World Space", font = "smallBoldLabelFont")
    cmds.button(label="Reset WorldSpace", command="reset_orientation_worldspace()")
    ### localspace button
    cmds.separator( height=15 )
    cmds.text("Reset Orientation From Local Space", font = "smallBoldLabelFont")
    cmds.button(label="Reset LocalSpace", command = "reset_orientation_localspace()")


    cmds.showWindow(window)
create_UI()
