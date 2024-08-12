# create by Tom Su, 2023

import maya.cmds as cmds

def create_circle_controller(*args):
    # get joint from scene
    get_joints = cmds.ls(selection = True, type="joint")

    if not get_joints:
        cmds.warning("No joint select!!!")
        return

    for joint in get_joints:
        # create controller
        controller = cmds.circle( name = joint + "_ctrl", normal=(1, 0, 0), radius=1)[0]

        # get joint information from world space
        joint_position = cmds.xform(joint, query=True, translation=True, worldSpace=True)
        joint_rotation = cmds.xform(joint, query=True, rotation=True, worldSpace=True)

        # put controller in joint and get translation and rotation
        cmds.xform(controller, translation=joint_position, worldSpace=True)
        cmds.xform(controller, rotation=joint_rotation, worldSpace=True)

        # #add controller to layer
        # control_layer = "controller_layer"

        # if not cmds.objExists(control_layer):
        #     control_layer = cmds.createDisplayLayer(name=control_layer)
        # cmds.editDisplayLayerMembers(control_layer, controller)

    cmds.select(clear=True)


def create_cross_circle(*args):
     
    get_joints = cmds.ls(selection = True, type="joint")

    if not get_joints:
        cmds.warning("No joint select!!!")
        return

    for joint in get_joints:
        
        controller = cmds.curve(name = joint + "_ctrl", d=1, p=[(-1, 0, -3), (1, 0, -3), (1, 0, -1), (3, 0, -1), (3, 0, 1), (1, 0, 1), (1, 0, 3), (-1, 0, 3),
                          (-1, 0, 1), (-3, 0, 1), (-3, 0, -1), (-1, 0, -1), (-1, 0, -3)],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ws = True)

        joint_position = cmds.xform(joint, query=True, translation=True, worldSpace=True)
        joint_rotation = cmds.xform(joint, query=True, rotation=True, worldSpace=True)

        
        cmds.xform(controller, translation=joint_position, worldSpace=True)
        cmds.xform(controller, rotation=joint_rotation, worldSpace=True)
 
        cmds.setAttr(controller + " .scaleX")
        cmds.setAttr(controller + " .scaleY")
        cmds.setAttr(controller + " .scaleZ")


def create_oneway_arrow_circle(*args):
     
    get_joints = cmds.ls(selection = True, type="joint")

    if not get_joints:
        cmds.warning("No joint select!!!")
        return

    for joint in get_joints:
        
        controller = cmds.curve(name = joint + "_ctrl", d=1, p=[(0, 1.003235, 0), (0.668823, 0, 0), (0.334412, 0, 0), (0.334412, -0.167206, 0),
                               (0.334412, -0.501617, 0), (0.334412, -1.003235, 0), (-0.334412, -1.003235, 0),
                               (-0.334412, -0.501617, 0), (-0.334412, -0.167206, 0), (-0.334412, 0, 0),
                               (-0.668823, 0, 0), (0, 1.003235, 0)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

        joint_position = cmds.xform(joint, query=True, translation=True, worldSpace=True)
        joint_rotation = cmds.xform(joint, query=True, rotation=True, ws=True)

        
        cmds.xform(controller, translation=joint_position, worldSpace=True)
        cmds.xform(controller, rotation=joint_rotation, ws=True)


def create_twoway_arrow(*args):
     
    get_joints = cmds.ls(selection = True, type="joint")

    if not get_joints:
        cmds.warning("No joint select!!!")
        return

    for joint in get_joints:
        
        controller = cmds.curve(name = joint + "_ctrl", d=1, p=[(0, 1, 0), (1, 1, 0), (2, 1, 0), (3, 1, 0), (3, 2, 0), (4, 1, 0), (5, 0, 0), (4, -1, 0),
                               (3, -2, 0), (3, -1, 0), (2, -1, 0), (1, -1, 0), (0, -1, 0), (-1, -1, 0), (-2, -1, 0),
                               (-3, -1, 0), (-3, -2, 0), (-4, -1, 0), (-5, 0, 0), (-4, 1, 0), (-3, 2, 0), (-3, 1, 0),
                               (-2, 1, 0), (-1, 1, 0), (0, 1, 0), ],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
        

        joint_position = cmds.xform(joint, query=True, translation=True, worldSpace=True)
        joint_rotation = cmds.xform(joint, query=True, rotation=True, worldSpace=True)

        
        cmds.xform(controller, translation=joint_position, worldSpace=True)
        cmds.xform(controller, rotation=joint_rotation, worldSpace=True)

        #cmds.setAttr(controller + " .translateZ",5)
    

def create_fourway_arrow(*args):
     
    get_joints = cmds.ls(selection = True, type="joint")

    if not get_joints:
        cmds.warning("No joint select!!!")
        return

    for joint in get_joints:
        
        controller = cmds.curve(name = joint + "_ctrl", d=1, p=[(1, 0, 1), (3, 0, 1), (3, 0, 2), (5, 0, 0), (3, 0, -2), (3, 0, -1), (1, 0, -1), (1, 0, -3),
                          (2, 0, -3), (0, 0, -5), (-2, 0, -3), (-1, 0, -3), (-1, 0, -1), (-3, 0, -1), (-3, 0, -2),
                          (-5, 0, 0), (-3, 0, 2), (-3, 0, 1), (-1, 0, 1), (-1, 0, 3), (-2, 0, 3), (0, 0, 5), (2, 0, 3),
                          (1, 0, 3), (1, 0, 1), ],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])

        
        joint_position = cmds.xform(joint, query=True, translation=True, worldSpace=True)
        joint_rotation = cmds.xform(joint, query=True, rotation=True, os=True)
        #joint_scale = cmds.xform(joint, query=True, scale=True, os=True)

        
        cmds.xform(controller, translation=joint_position, worldSpace=True)
        cmds.xform(controller, rotation=joint_rotation, os=True)
        #cmds.xform(controller, s=(9,9,9), os=True)


def apply_object_translate(*args):
    
    selection = cmds.ls(selection=True)
    
    obj = selection[0]
    
    move_object = cmds.floatSliderGrp("translate_slider", query=True, value=True)
    
    cmds.move(0, 0, move_object, obj, relative=True)
    
    cmds.warning("Object scale has been updated.")

    cmds.select(clear = True)


def apply_object_scale(*args):
    
    selection = cmds.ls(selection=True)
    
    obj = selection[0]
    
    scale = cmds.floatSliderGrp("scale_slider", query=True, value=True)
    
    cmds.scale(scale, scale, scale, obj, relative=True)
    
    cmds.warning("Object scale has been updated.")

    cmds.select(clear = True)



def apply_controller_color(*args):
    
    selection = cmds.ls(selection=True)
    
    controller = selection[0]
    
    # Get the RGB values from the color slider
    color = cmds.colorSliderGrp("colorSlider", query=True, rgb=True)
    
    # Set the color for the controller curve
    cmds.setAttr(controller + ".overrideEnabled", 1)
    cmds.setAttr(controller + ".overrideRGBColors", 1)
    cmds.setAttr(controller + ".overrideColorRGB", *color)
    
    cmds.warning("Controller color has been updated.")

    cmds.select(clear = True)


def parent_select_object(*args):

    selection_object = cmds.ls( selection = True)

    parent_object = selection_object[0]
    children_object = selection_object[1]

    cmds.makeIdentity( parent_object, apply=True, translate=True, rotate=True, scale = True)

    constraint = cmds.parentConstraint(parent_object, children_object, maintainOffset=True)

    cmds.select(clear = True)


def create_UI(*args):
    if cmds.window("control_creator_ui", exists=True):
        cmds.deleteUI("control_creator_ui", window=True)

    window = cmds.window("control_creator_ui", title="Controller Curve Tool", sizeable = False, widthHeight=(370, 430))

    cmds.columnLayout(adjustableColumn=True)

    ###
    cmds.separator(height=5, style = "none")
    cmds.text(" Step 1: Select a joint and create curve", font = "smallBoldLabelFont", al="center", bgc = (0.26,0.33,0.16))
    cmds.separator(height=5, style = "none")

    cmds.button(label="Circle Curve", command = create_circle_controller )

    cmds.button(label="Cross Curve", command = create_cross_circle)

    cmds.button(label="1 Way Arrow", command = create_oneway_arrow_circle)

    cmds.button(label="2 Way Arrow", command = create_twoway_arrow)

    cmds.button(label="4 Way Arrow", command = create_fourway_arrow)

    cmds.separator(height=5, style = "none")
    
    ### translate
    cmds.text(" Step 2: match translate and scale for curve", font = "smallBoldLabelFont", al="center", bgc = (0.26,0.33,0.16))
    cmds.separator(height=5, style = "none")

    cmds.floatSliderGrp("translate_slider", label="Translate Size", field=True, minValue=-2.0, maxValue=2.0, value=1.0, columnAlign=(1, 'left'))
    cmds.button(label = "Apply", c= "apply_object_translate()" )

    cmds.separator(height=5, style = "none")

    ### scale
    cmds.floatSliderGrp("scale_slider", label="Scale Size", field=True, minValue=0.1, maxValue=5.0, value=1.0, columnAlign=(1, 'left'))
    cmds.button(label = "Apply", c= "apply_object_scale()" )

    cmds.separator(height=5, style = "none")

    ### parent object
    cmds.text(" Step 3: select curve and joint, then parent", font = "smallBoldLabelFont", al="center", bgc = (0.26,0.33,0.16))
    cmds.separator(height=5, style = "none")
    cmds.button(label = "Parent", c = "parent_select_object()")
    cmds.separator(height=5, style = "none")

    ###
    cmds.text("Step 4: Select curve and choose color", font = "smallBoldLabelFont", al="center", bgc = (0.26,0.33,0.16))
    cmds.separator(height=5, style = "none")
    cmds.colorSliderGrp("colorSlider", label="Color", rgb=(1, 1, 1), columnAlign=(1, 'left'))

    cmds.separator(height=5, style = "none")

    cmds.button(label = "Set Color", c ="apply_controller_color()" )

    cmds.showWindow(window)

create_UI()
