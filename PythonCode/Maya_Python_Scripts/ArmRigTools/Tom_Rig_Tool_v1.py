############### Create by Tom Su June,2023


import maya.cmds as cmds
import maya.api.OpenMaya as om2
from functools import partial


########## locator to joint

def create_locator(*args):
    select_vertax = cmds.ls(selection = True, flatten = True)
    locator_grp = []

    for i in select_vertax:
        pos = cmds.pointPosition(i, world = True)
        locator = cmds.spaceLocator()
        cmds.move(pos[0], pos[1], pos[2], locator)
        locator_grp.append(locator)

def convert_to_joints(*args):
    select_locators = cmds.ls(type="locator")
    if not select_locators:
        cmds.warning("select_locators！")
        return

    joints = []
    for locator in select_locators:
        joint = cmds.joint()
        cmds.matchTransform(joint, locator, pos=True, rot=False, scl=False)
        joints.append(joint)

def delete_locators():
    delete_locators = cmds.ls(type="locator")
    cmds.delete(delete_locators)


############### insert joint tool
def SetJointPosition(start_jnt, insert_jnt, end_jnt, number_jnt):
    # position
    start_jnt_position = om2.MVector(cmds.xform(start_jnt, q = True, t = True, ws = True) )
    end_jnt_position = om2.MVector(cmds.xform(end_jnt, q = True, t = True, ws = True))

    #get position
    insert_joint_position = (end_jnt_position - start_jnt_position) * number_jnt + start_jnt_position

    #set position again
    cmds.xform(insert_jnt, t = insert_joint_position, ws = True)

    cmds.parent(end_jnt, insert_jnt)
    cmds.select(insert_jnt)


def InsertJoint(joint,*args):

    joints = cmds.ls(selection=True, l=True, type="joint")

    if not joints:
        cmds.warning("Select a joint first")

    #if one joint select
    if len(joints) == 1:
        # check the joint has children or not, it must have children to work
        end_jnt = cmds.listRelatives(children=True, f=True)

        if end_jnt is None:
            cmds.warning("Joint does not have children")
        else:
           # get the first children from joint
            end_jnt = end_jnt[0]

            number_jnt = 0

            if (joint == 1):
                joints_number = cmds.intField(joint_number_input, q=1, v=1)

                for i in range(0, joints_number):
                    if i > 0:
                        end_jnt = cmds.listRelatives(insert_between_jnt, children=True, f=True)[0]
                    number_jnt = number_jnt + 1 / float(joints_number + 1)
                    radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt)) / 2


                    insert_between_jnt = cmds.joint(rad=radius)
                    SetJointPosition(joints[0], insert_between_jnt, end_jnt, number_jnt)
            else:    
                joints_number = 1

                for i in range(0, joints_number):
                    if i > 0:
                        end_jnt = cmds.listRelatives(insert_between_jnt, children=True, f=True)[0]

                    number_jnt = getSliderValue(positionFloatSlider)

                    radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt)) / 2

                   
                    # create the inbetween joint
                    insert_between_jnt = cmds.joint(rad=radius)

                    SetJointPosition(joints[0], insert_between_jnt, end_jnt, number_jnt)


    #if two joint select
    if len(joints) == 2:
        
        children = cmds.listRelatives(joints[0], children=True, f=True)
        
        if children is not None:
            
            if joints[1] not in children:

                cmds.warning("First joint must be a direct parent of the second joint")
            else:
                
                cmds.select(joints[0])
                
                end_jnt = joints[1]

                number_jnt_2 = []

                if (joint == 1):
                    joints_number = cmds.intField(joint_number_input, q=1, v=1)

                    for i in range(0, joints_number):

                        if i > 0:
                            end_jnt = cmds.listRelatives(insert_between_jnt, children=True, f=True)[0]

                        number_jnt_2 = number_jnt_2 + 1 / (joints_number + 1)

                        radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt)) / 2

                        insert_between_jnt = cmds.joint(rad=radius)

                        SetJointPosition(joints[0], insert_between_jnt, end_jnt, number_jnt_2)
                else:    
                    joints_number = 1

                    for i in range(0, joints_number):

                        if i > 0:
                            end_jnt = cmds.listRelatives(insert_between_jnt, children=True, f=True)[0]
                        number_jnt_2 = getSliderValue(positionFloatSlider)
                        radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt)) / 2


                        insert_between_jnt = cmds.joint(rad=radius)
                        SetJointPosition(joints[0], insert_between_jnt, end_jnt, number_jnt_2)
        else:
            cmds.warning("First joint must be a direct parent of the second joint")

    # if more than two joints selected
    if len(joints) > 2:
        cmds.warning("only select 1 or 2 joints")

def getSliderValue(slider):
    return cmds.floatSliderGrp(slider, q=1, v=1)


################################ rig curve tool

class var (object):
    select = None
    length = None
    joint1 = None
    joint2 = None
    number_joint = None


def rig_curve():
    select_object = cmds.ls(sl = True)
    var.select = select_object[0]

    object_length()

    create_joint()

    var.number_joint = cmds.intSliderGrp ("joint_number", q = True, value = True)
    cmds.select(var.joint1, var.joint2)
    split(var.number_joint)

    var.joint1 = cmds.rename(var.joint1, "curves1_jnt")
    var.joint2 = cmds.rename (var.joint2, "curve" + str(var.number_joint +2) + "_jnt")

    create_ikHandle()

def object_length():
    var.length = cmds.arclen(var.select)

def create_joint():
    var.joint1 = cmds.joint(p = (0, 0, 0))
    var.joint2 = cmds.joint(p = (var.length, 0, 0))

    cmds.parent(var.select + '|' + var.joint1, world = True)

def split(div):
    start_joint = cmds.ls(selection=True)[0]
    end_joint = cmds.ls(selection=True)[1]
    distance = cmds.getAttr(end_joint+".tx")
    move_distance = distance/(div+1)

    for i in range(1,div+1):
        new_joint = cmds.insertJoint(start_joint)
        new_joint = cmds.rename(new_joint, "curves" + str(i+1) + "_jnt")

        cmds.move(move_distance, 0, 0, new_joint + " .rotatePivot", r = True, os =True)
        start_joint = new_joint





#### window
if cmds.window("Tom's Joint Tool", exists = True):
    cmds.deleteUI("Tom's Joint Tool", window = True)

window = cmds.window(title="Tom's Joint Tool", iconName="Insert", widthHeight=(300, 470) )

##### page1
cmds.columnLayout("window", adjustableColumn=True, rs=10)

cmds.frameLayout ("layoutFrame01", label = "Locator To Joint", collapsable = True, borderVisible=True, parent = "window", bgc=(0.7,0.3,0.1))

cmds.text("Select vertax and generate locator", font = "boldLabelFont", al="center")

cmds.separator(height=2, style = "none", parent = "layoutFrame01")

cmds.button(label = "Generate Locator", c = "create_locator()", parent = "layoutFrame01")
cmds.button(label = "Convert to Joints", c = "convert_to_joints(); delete_locators() ", parent = "layoutFrame01")


####### page2
cmds.frameLayout ("layoutFrame02", label = "Curve Rigging", collapsable = True, borderVisible=True, parent = "window", bgc=(0.57,0.54,0.21))

cmds.text("Select curves to rig", font = "smallBoldLabelFont", al="center")

startEnd_label = cmds.text("Number of Joint: ", al="left")

cmds.intSliderGrp ( "joint_number", field = True,  minValue = 1, maxValue = 30, value = 5, parent = "layoutFrame02")
cmds.separator(height=2, style = "none", parent = "layoutFrame02")

cmds.button(label = "Run", c = "rig_curve()", parent = "layoutFrame02")


##### page3
cmds.frameLayout ("layoutFrame03", label = "Insert Joint", collapsable = True, borderVisible=True, parent = "window", bgc=(0.26,0.33,0.16))

cmds.text("Select One Joint", font = "smallBoldLabelFont", al="center")

startEnd_label = cmds.text("Between Start and End Position: ", al="left")

####
positionFloatSlider = cmds.floatSliderGrp(min=0.0, max=1.0,  field=True)

insert_Button_1 = cmds.button(l="Run", al="center", c= partial(InsertJoint, 0) )

cmds.text("Select Multiple Joint", font = "smallBoldLabelFont", al="center")
multiple_Jnt_label = cmds.text("Number of Joints:", al="left")

###
joint_number_input = cmds.intField(min=2, max=50)

insert_Button_2 = cmds.button(label="Run", c = partial(InsertJoint, 1) )


cmds.showWindow(window)
