import maya.cmds as cmds
import maya.api.OpenMaya as om
import math


direction_axis_vectors = {
    "X": om.MVector.kXaxisVector,
    "-X": om.MVector.kXnegAxisVector,
    "Y": om.MVector.kYaxisVector,
    "-Y": om.MVector.kYnegAxisVector,
    "Z": om.MVector.kZaxisVector,
    "-Z": om.MVector.kZnegAxisVector
}

up_axis_vectors = {
    "Y": om.MVector.kYaxisVector,
    "-Y": om.MVector.kYnegAxisVector,
    "X": om.MVector.kXaxisVector,
    "-X": om.MVector.kXnegAxisVector,
    "Z": om.MVector.kZaxisVector,
    "-Z": om.MVector.kZnegAxisVector
}


def CreateJoint(name, query = False):
    if not query:
        cmds.joint(name = name)
    if query and not cmds.ls(name, type = "joint"):
        return None
    return name

class MuscleJointGRP(object):

    def __init__ (self):
        
        self.UI()
        self.joint_suffix = " "
        self.pick_L_R_ui = None
        self.update_factors()
        self.initialLocator = []
        self.allJoints = []
        self.start_end_joint_choose = []
        self.axisValue = []
        self.locator_position = []
        self.originAttachObj = None
        self.insertionAttachObj = None
        self.selected_module_instance = None
        


    def chooseRunModule(self, *args):
        selected_module = cmds.optionMenuGrp("pick_module_menu", query=True, value=True)
        self.selectModule = selected_module

        if selected_module == "Biceps Muscle":
            print("Biceps Muscle")
            self.selected_module_instance = self.createJoints
            self.joint_suffix = "_Biceps"
        if selected_module == "Tricep Muscle":
            print("Tricep Muscle")
            self.selected_module_instance = self.createJoints
            self.joint_suffix = "_Tricep"
        else:
            print("Meet Error !!!")



    def createJoints(self, *args):
        self.chooseRunModule()
        
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)
        self.start_joint = cmds.textFieldButtonGrp(self.start_list, q = True, text = True)
        self.end_joint = cmds.textFieldButtonGrp(self.end_list, q = True, text = True)

        muscle_origin_joint_name = "{0}_muscleOrigin{1}".format(self.L_R_value, self.joint_suffix)
        muscle_insertion_joint_name = "{0}_muscleInsertion{1}".format(self.L_R_value, self.joint_suffix)

        if cmds.objExists(muscle_origin_joint_name) and cmds.objExists(muscle_insertion_joint_name):
            print("Joint {0} Already Exist !!!".format(self.joint_suffix))
            return None
        
        print("Generating the joints")
        # generate joint chain first
        cmds.select(clear = True)
        self.muscleOrigin_joint = cmds.joint(n = self.L_R_value + "_muscleOrigin{0}".format(self.joint_suffix))
        
        

        cmds.select(cl = True)
        self.muscleInsertion_joint = cmds.joint(n = self.L_R_value + "_muscleInsertion{0}".format(self.joint_suffix))
        cmds.select(cl = True)

        ### get origin joint position
        origin_joint_position = om.MVector(cmds.xform(self.start_joint, q = True, t = True, ws = True))
        cmds.xform(self.muscleOrigin_joint, t = origin_joint_position, ws = True)

        # move insertion joint position
        insertion_joint_position = om.MVector(cmds.xform(self.end_joint, q = True, t = True, ws = True))
        cmds.xform(self.muscleInsertion_joint, t = insertion_joint_position)

        #create base joint
        self.muscleBase_joint = cmds.joint(n = self.L_R_value + "_muscleBase{0}".format(self.joint_suffix))
        cmds.xform(self.muscleBase_joint, t = origin_joint_position, ws = True)

        # move base joint position
        cmds.xform(self.muscleBase_joint, t = origin_joint_position, ws = True)
        cmds.select(cl = True)

        # create muscle tip joint
        self.muscleTip_joint = cmds.joint(n = self.L_R_value + "_muscleTip{0}".format(self.joint_suffix))
        cmds.select(cl = True)

        # create muscle driver and it child
        self.muscleDriver_joint = cmds.joint(n = self.L_R_value + "_" + "muscleDriver{0}".format(self.joint_suffix))
        self.muscleOffset_joint = cmds.joint(n = self.L_R_value + "_" + "muscleOffset{0}".format(self.joint_suffix))
        self.muscleJoint_joint = cmds.joint(n = self.L_R_value + "_" + "muscleJoint{0}".format(self.joint_suffix))
        cmds.select(cl = True)

        # move muscle base to correct position and get it rotation
        self.get_muscleOrigin_joint_rotation = om.MVector(cmds.xform(self.muscleOrigin_joint, ro = True, ws = True, q = True))
        cmds.xform(self.muscleBase_joint, t = origin_joint_position, ws = True)
        cmds.xform(self.muscleBase_joint, ro = self.get_muscleOrigin_joint_rotation, ws = True)

        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint decending position
        muscleDriver_joint_position = (origin_joint_position + insertion_joint_position) * 0.5
        cmds.xform(self.muscleDriver_joint, t = muscleDriver_joint_position, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.muscleTip_joint, t = insertion_joint_position, ws = True)

        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.muscleTip_joint, apply=True, rotate=True)
        cmds.parent(self.muscleTip_joint, self.muscleBase_joint)
        cmds.joint(self.muscleBase_joint, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        
        # match origin joint's rotate with base joint
        get_muscleBase_rotation = om.MVector(cmds.xform(self.muscleBase_joint, q = True, ro = True, ws = True))
        cmds.xform(self.muscleOrigin_joint, ro = get_muscleBase_rotation, ws = True)
        
        # match muscle tip joint's rotate with muscle base joint
        cmds.xform(self.muscleTip_joint, ro = get_muscleBase_rotation, ws = True)

        # match muscle insertion joint's rotate with end joint
        endJoint_rotation = om.MVector(cmds.xform(self.end_joint, q = True, ro = True, ws = True))
        cmds.xform(self.muscleInsertion_joint, ro = endJoint_rotation, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.muscleDriver_joint, ro = get_muscleBase_rotation, ws = True)
        cmds.xform(self.muscleOffset_joint, ro = get_muscleBase_rotation, ws = True)
        cmds.xform(self.muscleJoint_joint, ro = get_muscleBase_rotation, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.muscleOrigin_joint, apply = True, rotate = True)
        cmds.makeIdentity(self.muscleInsertion_joint, apply = True, rotate = True)
        cmds.makeIdentity(self.muscleDriver_joint, apply = True, rotate = True)

        # parent joints
        cmds.parent(self.muscleOrigin_joint, self.start_joint)
        cmds.parent(self.muscleInsertion_joint, self.end_joint)
        cmds.parent(self.muscleBase_joint, self.muscleOrigin_joint)
        cmds.parent(self.muscleDriver_joint, self.muscleBase_joint)

        # pass joints date to __init__
        self.allJoints.extend([self.muscleOrigin_joint, self.muscleInsertion_joint, self.muscleBase_joint, self.muscleTip_joint,
                               self.muscleDriver_joint, self.muscleOffset_joint, self.muscleJoint_joint])
        


    def constraintJoints(self, *args):
        self.createJoints()
        self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
        self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
        self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
        self.upAixs = up_axis_vectors[self.worldUpMenu_value]

        # Use muscle insertion joint point constraint tip joint
        cmds.pointConstraint(self.muscleInsertion_joint, self.muscleTip_joint, maintainOffset = False,
                             weight = 1)

        # pointConstraint driver joint at middle of base/tip joints
        self.mainPointConstraint = cmds.pointConstraint(self.muscleBase_joint, self.muscleTip_joint, self.muscleDriver_joint, maintainOffset = True,
                             weight=1)

        # aimConstraint insertion and muscle driver joint
        self.mainAimConstraint = cmds.aimConstraint(self.muscleInsertion_joint, self.muscleBase_joint,
                                                    aimVector = self.dirAxis, upVector = self.upAixs,
                                                    worldUpType = "objectrotation", worldUpObject = self.muscleOrigin_joint,
                                                    worldUpVector = self.upAixs)
        
        # cmds.delete(self.locator_origin, self.locator_driver, self.locator_tip)

        self.axisValue.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                               self.upAixs, self.mainPointConstraint])
        
        self.addSDK()



    def edit(self, *args):
        
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)

        if not hasattr(self, 'muscleOrigin_joint') or not hasattr(self, 'muscleInsertion_joint'):
            cmds.error("Muscle joints have not been created yet. Please create them before entering edit mode.")
            return
        
        def createSpaceLocator(scaleValue, **kwargs):
            loc = cmds.spaceLocator(**kwargs)[0]
            for axis in "XYZ":
                cmds.setAttr("{0}.localScale{1}".format(loc, axis), scaleValue)
            return loc
        
        self.originLoc = "{0}_muscleOrigin_loc".format(self.start_joint)
        self.centerLoc = "{0}_muscleCenter_loc".format(self.start_joint)
        self.insertionLoc = "{0}_muscleInsertion_loc".format(self.end_joint)

        if cmds.objExists(self.originLoc) and cmds.objExists(self.insertionLoc):
            print("Locators already exist in the scene!")
        else:
            print("Generating Locators!")
            self.originLoc = createSpaceLocator(1, name="{0}_muscleOrigin_loc".format(self.start_joint))
            self.centerLoc = createSpaceLocator(1, name="{0}_muscleCenter_loc".format(self.start_joint))
            self.insertionLoc = createSpaceLocator(1, name="{0}_muscleInsertion_loc".format(self.end_joint))

        ###
        self.mainPointConstraint = cmds.pointConstraint(self.muscleBase_joint, self.muscleTip_joint, self.muscleDriver_joint, maintainOffset = True,
                                weight=1)

        self.mainAimConstraint = cmds.aimConstraint(self.muscleInsertion_joint, self.muscleBase_joint,
                                            aimVector = self.dirAxis, upVector = self.upAixs,
                                            worldUpType = "objectrotation", worldUpObject = self.muscleOrigin_joint,
                                            worldUpVector = self.upAixs)
        
        cmds.setAttr("{0}.overrideEnabled".format(self.muscleOrigin_joint), 1)
        cmds.setAttr("{0}.overrideDisplayType".format(self.muscleOrigin_joint), 1)
        cmds.setAttr("{0}.overrideEnabled".format(self.muscleInsertion_joint), 1)
        cmds.setAttr("{0}.overrideDisplayType".format(self.muscleInsertion_joint), 1)
        
        self.ptConstraintsTmp = []

        # self.originLoc = createSpaceLocator(1, name="{0}_muscleOrigin_loc".format(self.start_joint))
        # self.centerLoc = createSpaceLocator(1, name="{0}_muscleCenter_loc".format(self.start_joint))
        # self.insertionLoc = createSpaceLocator(1, name="{0}_muscleInsertion_loc".format(self.end_joint))
        
        if self.originAttachObj:
            cmds.parent(self.originLoc, self.originAttachObj)
        cmds.delete(cmds.pointConstraint(self.muscleOrigin_joint, self.originLoc, mo=False, w=True))

        self.ptConstraintsTmp.append(cmds.pointConstraint(self.originLoc, self.muscleOrigin_joint, mo=False, w=True)[0])

        if self.insertionAttachObj:
            cmds.parent(self.insertionLoc, self.insertionAttachObj)

        # get reverse direction
        def get_reverse_direction():
            return[-value for value in self.dirAxis]

        cmds.aimConstraint(self.insertionLoc, self.originLoc,
                           aimVector = self.dirAxis, upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)

        ###
        cmds.aimConstraint(self.insertionLoc, self.originLoc,
                           aimVector = get_reverse_direction(), upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)

        cmds.delete(cmds.pointConstraint(self.muscleInsertion_joint, self.insertionLoc, mo=False, w=True))
        
        self.ptConstraintsTmp.append(cmds.pointConstraint(self.insertionLoc, self.muscleInsertion_joint, mo=False, w=True)[0])

        driverGrpName = "{0}_muscleCenter_grp".format(self.start_joint)
        if cmds.objExists(driverGrpName):
            print("Group {0} already exists in the scene.".format(driverGrpName))
        if not cmds.objExists(driverGrpName):
            driverGrpName = cmds.group(name="{0}_muscleCenter_grp".format(self.start_joint), empty=True)

        cmds.parent(self.centerLoc, driverGrpName)
        cmds.delete(cmds.pointConstraint(self.muscleDriver_joint, driverGrpName, mo=False, w=True))
        cmds.parent(driverGrpName, self.originLoc)
        cmds.pointConstraint(self.originLoc, self.insertionLoc, driverGrpName, mo=True, w=True)
        cmds.setAttr("{0}.r".format(driverGrpName), 0, 0, 0)
        cmds.delete(self.mainPointConstraint)
        self.ptConstraintsTmp.append(cmds.pointConstraint(self.centerLoc, self.muscleDriver_joint, mo=False, w=True)[0])

        cmds.select(self.originLoc, self.centerLoc, self.insertionLoc)


    def update(self, *args):

        for ptConstraintsTmp in self.ptConstraintsTmp:
            if cmds.objExists(ptConstraintsTmp):
                cmds.delete(ptConstraintsTmp)

        for loc in [self.originLoc, self.insertionLoc, self.centerLoc]:
            if cmds.objExists(loc):
                cmds.delete(loc)

        cmds.setAttr("{0}.overrideEnabled".format(self.muscleOrigin_joint), 0)
        cmds.setAttr("{0}.overrideDisplayType".format(self.muscleOrigin_joint), 0)
        cmds.setAttr("{0}.overrideEnabled".format(self.muscleInsertion_joint), 0)
        cmds.setAttr("{0}.overrideDisplayType".format(self.muscleInsertion_joint), 0)

        cmds.delete(self.mainAimConstraint)

        self.mainPointConstraint = cmds.pointConstraint(self.muscleBase_joint, self.muscleTip_joint, self.muscleDriver_joint,
                                                        mo=True, weight=1)

        cmds.delete(cmds.aimConstraint(self.muscleInsertion_joint, self.muscleOrigin_joint,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))

        self.mainAimConstraint = cmds.aimConstraint(self.muscleInsertion_joint, self.muscleBase_joint,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.muscleOrigin_joint,
                                                    worldUpVector=self.upAixs)

        animCurveNodes = cmds.ls(cmds.listConnections(self.muscleJoint_joint, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))
        
        cmds.delete(animCurveNodes)
        self.addSDK()
        

    def addSDK(self, stretchOffset=None, compressionOffset=None):
        self.compressionScale = float(cmds.textField(self.compressionScaleField, query=True, text=True))
        self.stretchScale = float(cmds.textField(self.stretchScaleField, query=True, text=True))

        yzSquashScale = math.sqrt(1.0 / self.compressionScale)
        yzStretchScale = math.sqrt(1.0 / self.stretchScale)

        if stretchOffset is None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset is None:
            compressionOffset = [0.0, 0.0, 0.0]

        restLength = cmds.getAttr("{0}.translate{1}".format(self.muscleTip_joint, self.objectDirectionMenu_value))
        
       
        for index, axis in enumerate("XYZ"):
            
            # get original scale and translate value
            cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint, axis), 0.0)

            # set driven keyframe at original position
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint, axis),
                                   currentDriver="{0}.translate{1}".format(self.muscleTip_joint, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint, axis),
                                   currentDriver="{0}.translate{1}".format(self.muscleTip_joint, self.objectDirectionMenu_value))

            # set driven keyframe at stretch position
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint, self.objectDirectionMenu_value), restLength * self.stretchScale)
            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint, axis), self.stretchScale)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint, axis), yzStretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint, axis), stretchOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint, axis),
                                   currentDriver="{0}.translate{1}".format(self.muscleTip_joint, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint, axis),
                                   currentDriver="{0}.translate{1}".format(self.muscleTip_joint, self.objectDirectionMenu_value))

            # set driven keyframe at compression position
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint, self.objectDirectionMenu_value), restLength * self.compressionScale)

            
            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint, axis), self.compressionScale)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint, axis), yzSquashScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint, axis), compressionOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint, axis),
                                   currentDriver="{0}.translate{1}".format(self.muscleTip_joint, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint, axis),
                                   currentDriver="{0}.translate{1}".format(self.muscleTip_joint, self.objectDirectionMenu_value))

            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint, self.objectDirectionMenu_value), restLength)
            


    def UI(self):
        if cmds.window("ArmMuscleJoint", exists=True):
            cmds.deleteUI("ArmMuscleJoint")

        window = cmds.window("ArmMuscleJoint", title="Add Arm Muscle Units", s=True, rtf=True, widthHeight=(150, 100))

        cmds.columnLayout(adjustableColumn=True)
        
        cmds.separator(h=2, st='none')

        self.selectModule = cmds.optionMenuGrp("pick_module_menu", label="Step1: Select Moduel", width = 200, 
                                        columnAlign=(1, 'left'), columnAttach=[(1, 'left', 0), (2, 'left', 0)])
        
        for i in ["Biceps Muscle", "Tricep Muscle"]:
            cmds.menuItem(label = i)

        cmds.setParent("..")

        cmds.columnLayout(adjustableColumn=True)
        
        cmds.separator(h=2, st='none')

        cmds.text("Step2: Choose Start and End joint")

        cmds.rowLayout(numberOfColumns=3, columnWidth2=(150, 100))
        self.start_list = cmds.textFieldButtonGrp(label='Start Joint', text='', buttonLabel='Select', 
                                                buttonCommand=self.load_startJoint)
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=3, columnWidth2=(150, 100))
        self.end_list = cmds.textFieldButtonGrp(label='End Joint', text='', buttonLabel='Select',
                                                buttonCommand=self.load_endJoint)
        cmds.setParent("..")

        # cmds.separator(h = 2, st = 'none')
    
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(180, 120), adjustableColumn=2, columnAlign=(1, 'left'))

        global pick_L_R_ui
        pick_L_R_ui = cmds.optionMenuGrp("pick_L_R_Menu", label="Step2: Select L/R Side + Loc", width = 200, 
                                     columnAlign=(1, 'left'), columnAttach=[(1, 'left', 0), (2, 'left', 0)])
        
        for y in ["L", "R"]:
            cmds.menuItem(label=y)

        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=5, columnWidth2=(200, 120), 
                       adjustableColumn=5, columnAlign=(1, 'center'))
        cmds.text("Step3:")
        # Stretch factor input
        cmds.text(label='stretch scale')
        self.stretchScaleField = cmds.textField(text="2.0", changeCommand=self.update_factors)
        
        # Compression factor input
        cmds.text(label='compression scale')
        self.compressionScaleField = cmds.textField(text="0.5", changeCommand=self.update_factors)
        cmds.setParent('..')

        cmds.rowLayout(adjustableColumn=True)
        # cmds.separator(h = 2, st = 'none')
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=5, columnWidth2=(200, 120), 
                       adjustableColumn=5, columnAlign=(1, 'left'))
        
        global objectDirection_ui
        objectDirection_ui = cmds.optionMenuGrp("objectMenu", label="Object Direction", width = 200, 
                                     columnAlign=(1, 'left'), columnAttach=[(1, 'left', 0), (2, 'left', 0)])
        for i in direction_axis_vectors.keys():
            cmds.menuItem(label = i)

        global worldUp_ui
        worldUp_ui = cmds.optionMenuGrp("worldUpMenu", label="WorldUp Direction", width = 200, 
                                     columnAlign=(1, 'left'), columnAttach=[(1, 'left', 0), (2, 'left', 0)])
        for j in up_axis_vectors.keys():
            cmds.menuItem(label = j)

        cmds.setParent('..')

        cmds.separator(h = 2, st = 'none')
        cmds.text("Step4: Generate Joints")
        cmds.rowLayout(adjustableColumn=True)
        cmds.button(label="Create Joints", c=self.constraintJoints)
        cmds.setParent('..')

        cmds.separator(h = 5, st = 'none')
        cmds.text("(Option)Step5: Edit Mode")
        cmds.separator(h = 2, st = 'none')

        cmds.rowLayout(adjustableColumn=True)
        cmds.button(label="Edit Mode", c = self.edit)
        cmds.setParent('..')

        cmds.rowLayout(adjustableColumn=True)
        cmds.button(label="Complete Update", c = self.update)
        cmds.setParent('..')

        cmds.showWindow(window)

    def load_startJoint(self, *args):
        selected = cmds.ls(selection=True)
        if selected:
            cmds.textFieldButtonGrp(self.start_list, edit=True, text = selected[0])

    def load_endJoint(self, *args):
        selected = cmds.ls(selection=True)
        if selected:
            cmds.textFieldButtonGrp(self.end_list, edit=True, text = selected[0])

    def update_factors(self, *args):
        float(cmds.textField(self.stretchScaleField, query=True, text=True))
        float(cmds.textField(self.compressionScaleField, query=True, text=True))



if __name__ == "__main__":
    
    MuscleGrp = MuscleJointGRP()
    MuscleGrp.UI()
