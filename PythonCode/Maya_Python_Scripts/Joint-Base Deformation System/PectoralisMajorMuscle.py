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



class PectoralisMuscleGRP(object):
    
    def __init__(self, ui_instance):
        self.ui_instance = ui_instance

        self.AllJoints_PM_A = []
        self.AllJoints_PM_B = []
        self.axisValue_PM_A = []
        self.axisValue_PM_B = []
        self.twistJoint_01 = None
        self.twistJoint_02 = None
        self.scapulaRoot = None
        self.upperArm = None
        self.acromion = None
        self.inferiorAngle = None
        self.originAttachObj = None
        self.insertionAttachObj = None

        self.back2 = "back2"
    


    # create Deltoid muscle joints  
    def createPMJnt_A(self):
        # update joints information
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)

        self.twistJoint_01 = "upperarm_{0}_TwistJoint_001".format(self.L_R_value)
        self.twistJoint_02 = "upperarm_{0}_TwistJoint_002".format(self.L_R_value)
        self.back = "back3".format(self.L_R_value)
        
        # pm = pectoralis major muscle
        self.PM_A_origin = cmds.textFieldButtonGrp(self.ui_instance.origin_A, q = True, text = True)

        if not self.PM_A_origin.strip():
            self.PM_A_origin = self.back

        # check joints already generate or not
        if cmds.ls("{0}_muscleOrigin_PectoralisMuscle_A".format(self.L_R_value), type = "joint") and cmds.ls("{0}_muscleInsertion_PectoralisMuscle_A".format(self.L_R_value), type = "joint"):
            cmds.warning("PM A already Exist !!!") 
            return None
        
        print("Generating PM A Joints")
        cmds.select(clear = True)
        self.PM_A_muscleOrigin = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "PectoralisMuscle_A")

        # calculus origin joint position
        PM_A_startPosition = om.MVector(cmds.xform(self.PM_A_origin, t = True, ws = True, q = True))
        cmds.xform(self.PM_A_muscleOrigin, t = PM_A_startPosition, ws = True)

        cmds.select(self.PM_A_muscleOrigin)

        # duplicate a new joint call insertion joint
        self.PM_A_muscleInsertion = cmds.duplicate(self.PM_A_muscleOrigin, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "PectoralisMuscle_A")[0]

        # get PM_A_end start and end joint Position
        PM_A_endJnt = cmds.textFieldButtonGrp(self.ui_instance.insertion_A, q = True, text = True)
        if not PM_A_endJnt.strip():
            PM_A_endJnt = self.twistJoint_02

        PM_A_endJntStartPosition = om.MVector(cmds.xform(PM_A_endJnt, t = True, ws = True, q = True))


        PM_A_endJntEndPosition = om.MVector(cmds.xform(self.twistJoint_01, t=True, ws=True, q=True))
        PM_A_endJntFinalPosition = ((PM_A_endJntEndPosition - PM_A_endJntStartPosition) * 1.0 / 2.0 + PM_A_endJntStartPosition)
        cmds.xform(self.PM_A_muscleInsertion, t = PM_A_endJntFinalPosition, ws=True)

        cmds.select(cl=True)

        # PM_A_end_joint_position = om.MVector(cmds.xform(PM_A_end_joint, t = True, ws = True, q = True))
        # cmds.xform(self.PM_A_muscleInsertion, t = PM_A_end_joint_position, ws = True)
        # cmds.select(cl = True)

        # create muscle base
        self.PM_A_muscleBase = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "PectoralisMuscle_A")
        cmds.select(cl = True)
        # create muscle tip
        self.PM_A_muscleTip = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "PectoralisMuscle_A")
        cmds.select(cl = True)
        # create muscle driver and it child
        self.PM_A_muscleDriver = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "PectoralisMuscle_A")
        self.PM_A_muscleOffset = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "PectoralisMuscle_A")
        self.PM_A_muscleJoint = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "PectoralisMuscle_A")
        cmds.select(cl = True)

        # move muscle base to correct position and get it rotation
        get_PM_A_muscleOrigin_joint_position = om.MVector(cmds.xform(self.PM_A_muscleOrigin, t = True, ws = True, q = True))
        get_PM_A_muscleOrigin_joint_rotation = om.MVector(cmds.xform(self.PM_A_muscleOrigin, ro = True, ws = True, q = True))
        cmds.xform(self.PM_A_muscleBase, t = get_PM_A_muscleOrigin_joint_position, ws = True)
        cmds.xform(self.PM_A_muscleBase, ro = get_PM_A_muscleOrigin_joint_rotation, ws = True)
        
        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint LD A position
        get_PM_A_muscleInsertion_position = om.MVector(cmds.xform(self.PM_A_muscleInsertion, t = True, ws = True, q = True))
        muscleDriver_finalPosition = ( get_PM_A_muscleOrigin_joint_position + get_PM_A_muscleInsertion_position) * 0.5
        cmds.xform(self.PM_A_muscleDriver, t = muscleDriver_finalPosition, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.PM_A_muscleTip, t = get_PM_A_muscleInsertion_position, ws = True)

        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.PM_A_muscleTip, apply=True, rotate=True)
        cmds.parent(self.PM_A_muscleTip, self.PM_A_muscleBase)
        cmds.joint(self.PM_A_muscleBase, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        PM_A_get_muscleBase_rotation = om.MVector(cmds.xform(self.PM_A_muscleBase, ro = True, ws = True, q = True))
        cmds.xform(self.PM_A_muscleTip, ro = PM_A_get_muscleBase_rotation, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.PM_A_muscleDriver, ro = PM_A_get_muscleBase_rotation, ws = True)
        cmds.xform(self.PM_A_muscleOffset, ro = PM_A_get_muscleBase_rotation, ws = True)
        cmds.xform(self.PM_A_muscleJoint, ro = PM_A_get_muscleBase_rotation, ws = True)

        # apply origin joint rotation to base joint
        cmds.xform(self.PM_A_muscleOrigin, ro = PM_A_get_muscleBase_rotation, ws = True)

        # apply end joint rotation to insertion joint
        PM_A_end_joint_rotation = om.MVector(cmds.xform(self.PM_A_muscleInsertion, ro = True, ws = True, q = True))
        cmds.xform(self.PM_A_muscleInsertion, ro = PM_A_end_joint_rotation, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.PM_A_muscleOrigin, apply=True, rotate=True)
        cmds.makeIdentity(self.PM_A_muscleInsertion, apply=True, rotate=True)
        cmds.makeIdentity(self.PM_A_muscleDriver, apply=True, rotate=True)
        cmds.makeIdentity(self.PM_A_muscleTip, apply=True, rotate=True)

        # parent joints
        cmds.parent(self.PM_A_muscleOrigin, self.PM_A_origin)
        cmds.parent(self.PM_A_muscleInsertion, PM_A_endJnt)
        cmds.parent(self.PM_A_muscleBase, self.PM_A_muscleOrigin)
        cmds.parent(self.PM_A_muscleDriver, self.PM_A_muscleBase)

        # pass joints date to __init__
        self.AllJoints_PM_A.extend([self.PM_A_muscleOrigin, self.PM_A_muscleInsertion, self.PM_A_muscleBase, self.PM_A_muscleTip,
                            self.PM_A_muscleDriver, self.PM_A_muscleOffset, self.PM_A_muscleJoint])
        print("Compelete Generating DT A Joints")

        # update joints color
        orange_color_index = 7
        def setJointColor(joint, colorIndex):
            cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
            cmds.setAttr("{0}.overrideColor".format(joint), colorIndex)
        for joint in self.AllJoints_PM_A:
            setJointColor(joint, orange_color_index)

        return True
            
        
    
    def createPMConstraint_A(self):

        result = self.createPMJnt_A()
        if result == None:
            return None
        
        if result == True:
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.PM_A_muscleInsertion, self.PM_A_muscleTip, maintainOffset = False,
                                weight = 1)

            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_PM_A = cmds.pointConstraint(self.PM_A_muscleBase, self.PM_A_muscleTip, self.PM_A_muscleDriver, maintainOffset = True,
                                weight=1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_PM_A = cmds.aimConstraint(self.PM_A_muscleInsertion, self.PM_A_muscleBase,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.PM_A_origin,
                                                        worldUpVector = self.upAixs)
            self.axisValue_PM_A.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_PM_A, self.mainAimConstraint_PM_A])
    
            print("Compelete DT A Constraint")
            self.addSDK_A()
            print("Compelete DT A Set SDK")



    def createPMJnt_B(self):
        # update joints information
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)
        self.twistJoint_01 = "upperarm_{0}_TwistJoint_001".format(self.L_R_value)
        self.twistJoint_02 = "upperarm_{0}_TwistJoint_002".format(self.L_R_value)
        self.clavicle = "clavicle_{0}".format(self.L_R_value)

        self.PM_B_origin = cmds.textFieldButtonGrp(self.ui_instance.origin_B, q = True, text = True)

        if not self.PM_B_origin.strip():
            self.PM_B_origin = self.clavicle

        # check joints already generate or not
        if cmds.ls("{0}_muscleOrigin_PectoralisMuscle_B".format(self.L_R_value), type = "joint") and cmds.ls("{0}_muscleInsertion_PectoralisMuscle_B".format(self.L_R_value), type = "joint"):
            cmds.warning("PM B already Exist !!!")
            return None
        
        print("Generating PM B Joints")
        cmds.select(clear = True)
        self.PM_B_muscleOrigin = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "PectoralisMuscle_B")

        # calculus origin joint position
        PM_B_startJntStartPosition = om.MVector(cmds.xform(self.PM_B_origin, t = True, ws = True, q = True))

        PM_B_startJntEndPosition = om.MVector(cmds.xform(self.twistJoint_01, t=True, ws=True, q=True))

        PM_B_startJntFinalPosition = (
                    (PM_B_startJntEndPosition - PM_B_startJntStartPosition) * 1.0 / 4.0 + PM_B_startJntStartPosition)
        cmds.xform(self.PM_B_muscleOrigin, t = PM_B_startJntFinalPosition, ws=True)

        cmds.select(self.PM_B_muscleOrigin)

        # duplicate a new joint call insertion joint
        self.PM_B_muscleInsertion = cmds.duplicate(self.PM_B_muscleOrigin, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "PectoralisMuscle_B")[0]

        # get PM_B_end start and end joint Position
        self.PM_B_end_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_B, q = True, text = True)
        if not self.PM_B_end_joint.strip():
            self.PM_B_end_joint = self.twistJoint_02

        PM_B_endJntStartPosition = om.MVector(cmds.xform(self.PM_B_end_joint, t=True, ws=True, q=True))
        PM_B_endJntEndPosition = om.MVector(cmds.xform(self.twistJoint_01, t=True, ws=True, q=True))
        PM_B_endJntFinalPosition = (
                    (PM_B_endJntEndPosition - PM_B_endJntStartPosition) * 1.0 / 2.0 + PM_B_endJntStartPosition)
        cmds.xform(self.PM_B_muscleInsertion, t = PM_B_endJntFinalPosition, ws=True)

        cmds.select(cl = True)

        # create muscle base
        self.PM_B_muscleBase = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "PectoralisMuscle_B")
        cmds.select(cl = True)
        # create muscle tip
        self.PM_B_muscleTip = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "PectoralisMuscle_B")
        cmds.select(cl = True)
        # create muscle driver and it child
        self.PM_B_muscleDriver = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "PectoralisMuscle_B")
        self.PM_B_muscleOffset = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "PectoralisMuscle_B")
        self.PM_B_muscleJoint = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "PectoralisMuscle_B")
        cmds.select(cl = True)

        # move muscle base to correct position and get it rotation
        get_PM_B_muscleOrigin_joint_position = om.MVector(cmds.xform(self.PM_B_muscleOrigin, t = True, ws = True, q = True))
        get_PM_B_muscleOrigin_joint_rotation = om.MVector(cmds.xform(self.PM_B_muscleOrigin, ro = True, ws = True, q = True))
        cmds.xform(self.PM_B_muscleBase, t = get_PM_B_muscleOrigin_joint_position, ws = True)
        cmds.xform(self.PM_B_muscleBase, ro = get_PM_B_muscleOrigin_joint_rotation, ws = True)
        
        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint LD A position
        get_PM_B_muscleInsertion_position = om.MVector(cmds.xform(self.PM_B_muscleInsertion, t = True, ws = True, q = True))
        muscleDriver_joint_finalPosition = (get_PM_B_muscleOrigin_joint_position + get_PM_B_muscleInsertion_position) * 0.5
        cmds.xform(self.PM_B_muscleDriver, t = muscleDriver_joint_finalPosition, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.PM_B_muscleTip, t = get_PM_B_muscleInsertion_position, ws = True)

        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.PM_B_muscleTip, apply=True, rotate=True)
        cmds.parent(self.PM_B_muscleTip, self.PM_B_muscleBase)
        cmds.joint(self.PM_B_muscleBase, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        PM_B_get_muscleBase_rotation = om.MVector(cmds.xform(self.PM_B_muscleBase, ro = True, ws = True, q = True))
        cmds.xform(self.PM_B_muscleTip, ro = PM_B_get_muscleBase_rotation, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.PM_B_muscleDriver, ro = PM_B_get_muscleBase_rotation, ws = True)
        cmds.xform(self.PM_B_muscleOffset, ro = PM_B_get_muscleBase_rotation, ws = True)
        cmds.xform(self.PM_B_muscleJoint, ro = PM_B_get_muscleBase_rotation, ws = True)

        # apply origin joint rotation to base joint
        cmds.xform(self.PM_B_muscleOrigin, ro =  PM_B_get_muscleBase_rotation, ws = True)

        # apply end joint rotation to insertion joint
        PM_B_end_joint_rotation = om.MVector(cmds.xform(self.PM_B_end_joint, ro = True, ws = True, q = True))
        cmds.xform(self.PM_B_muscleInsertion, ro = PM_B_end_joint_rotation, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.PM_B_muscleOrigin, apply=True, rotate=True)
        cmds.makeIdentity(self.PM_B_muscleInsertion, apply=True, rotate=True)
        cmds.makeIdentity(self.PM_B_muscleDriver, apply=True, rotate=True)
        cmds.makeIdentity(self.PM_B_muscleTip, apply=True, rotate=True)

        # parent joints
        cmds.parent(self.PM_B_muscleOrigin, self.PM_B_origin)
        cmds.parent(self.PM_B_muscleInsertion, self.PM_B_end_joint)
        cmds.parent(self.PM_B_muscleBase, self.PM_B_muscleOrigin)
        cmds.parent(self.PM_B_muscleDriver, self.PM_B_muscleBase)

        # pass joints date to __init__
        self.AllJoints_PM_B.extend([self.PM_B_muscleOrigin, self.PM_B_muscleInsertion, self.PM_B_muscleBase, self.PM_B_muscleTip,
                            self.PM_B_muscleDriver, self.PM_B_muscleOffset, self.PM_B_muscleJoint])
    
        print("Compelete Generating PM B Joints")

        # update joints color
        orange_color_index = 7

        # # Function to update joint color
        def set_joint_color(joint, color_index):
            cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
            cmds.setAttr("{0}.overrideColor".format(joint), color_index)
        for joint in self.AllJoints_PM_B:
            set_joint_color(joint, orange_color_index)
        return True



    def createPMConstraint_B(self):
        result = self.createPMJnt_B()
        if result == None:
            return None
        
        if result == True:
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.PM_B_muscleInsertion, self.PM_B_muscleTip, maintainOffset = False,
                                weight = 1)

            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_PM_B = cmds.pointConstraint(self.PM_B_muscleBase, self.PM_B_muscleTip, self.PM_B_muscleDriver, maintainOffset = True,
                                weight=1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_PM_B = cmds.aimConstraint(self.PM_B_muscleInsertion, self.PM_B_muscleBase,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.PM_B_origin,
                                                        worldUpVector = self.upAixs)

            self.axisValue_PM_B.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_PM_B, self.mainAimConstraint_PM_B])
            
            print("Compelete PM B Constraint")
            self.addSDK_B()
            print("Compelete PM B Set SDK")



    def edit(self, *args):
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)
        def createSpaceLocator(scaleValue, **kwargs):
            loc = cmds.spaceLocator(**kwargs)[0]
            for axis in "XYZ":
                cmds.setAttr("{0}.localScale{1}".format(loc, axis), scaleValue)
            return loc
        
        ###
        self.muscleJointLib()

        ###
        self.mainPointConstraint_PM_A = cmds.pointConstraint(self.PM_A_muscleBase, self.PM_A_muscleTip, self.PM_A_muscleDriver, maintainOffset = True,
                                            weight=1)
        self.mainAimConstraint_PM_A = cmds.aimConstraint(self.PM_A_muscleInsertion, self.PM_A_muscleBase,
                                                    aimVector = self.dirAxis, upVector = self.upAixs,
                                                    worldUpType = "objectrotation", worldUpObject = self.PM_A_origin,
                                                    worldUpVector = self.upAixs)
        self.mainPointConstraint_PM_B = cmds.pointConstraint(self.PM_B_muscleBase, self.PM_B_muscleTip, self.PM_B_muscleDriver, maintainOffset = True,
                                weight=1)
        self.mainAimConstraint_PM_B = cmds.aimConstraint(self.PM_B_muscleInsertion, self.PM_B_muscleBase,
                                            aimVector = self.dirAxis, upVector = self.upAixs,
                                            worldUpType = "objectrotation", worldUpObject = self.PM_B_origin,
                                            worldUpVector = self.upAixs)


 
        # set joints to templete
        joints =[self.PM_A_muscleOrigin, self.PM_A_muscleInsertion,
                 self.PM_B_muscleOrigin, self.PM_B_muscleInsertion]
        for i in joints:
            cmds.setAttr("{0}.overrideEnabled".format(i), 1)
            cmds.setAttr("{0}.overrideDisplayType".format(i), 1)
        
        self.ptConstraintsTmp_PM_A = []
        self.ptConstraintsTmp_PM_B = []

        self.originLoc_PM_A = createSpaceLocator(5.0, name="{0}_muscleOrigin_loc_A".format(self.L_R_value))
        self.originLoc_PM_B = createSpaceLocator(5.0, name="{0}_muscleOrigin_loc_B".format(self.L_R_value))

        if self.originAttachObj:
            cmds.parent(self.originLoc_PM_A, self.originAttachObj)
            cmds.parent(self.originLoc_PM_B, self.originAttachObj)

        cmds.delete(cmds.pointConstraint(self.PM_A_muscleOrigin, self.originLoc_PM_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.PM_B_muscleOrigin, self.originLoc_PM_B, mo=False, w=True))

        self.ptConstraintsTmp_PM_A.append(cmds.pointConstraint(self.originLoc_PM_A, self.PM_A_muscleOrigin, mo=False, w=True)[0])
        self.ptConstraintsTmp_PM_B.append(cmds.pointConstraint(self.originLoc_PM_B, self.PM_B_muscleOrigin, mo=False, w=True)[0])

        self.insertionLoc_PM_A = createSpaceLocator(5.0, name="{0}_muscleInsertion_loc_A".format(self.L_R_value))
        self.insertionLoc_PM_B = createSpaceLocator(5.0, name="{0}_muscleInsertion_loc_B".format(self.L_R_value))

        if self.insertionAttachObj:
            cmds.parent(self.insertionLoc_PM_A, self.insertionAttachObj)
            cmds.parent(self.insertionLoc_PM_B, self.insertionAttachObj)

        def get_reverse_direction():
            return[-value for value in self.dirAxis]
        
        cmds.aimConstraint(self.insertionLoc_PM_A, self.originLoc_PM_A,
                           aimVector = self.dirAxis, upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        
        cmds.aimConstraint(self.insertionLoc_PM_A, self.originLoc_PM_A,
                           aimVector = get_reverse_direction(), upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)

        cmds.aimConstraint(self.insertionLoc_PM_B, self.originLoc_PM_B,
                           aimVector = self.dirAxis, upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        
        cmds.aimConstraint(self.insertionLoc_PM_B, self.originLoc_PM_B,
                           aimVector = get_reverse_direction(), upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        
        cmds.delete(cmds.pointConstraint(self.PM_A_muscleInsertion, self.insertionLoc_PM_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.PM_B_muscleInsertion, self.insertionLoc_PM_B, mo=False, w=True))

        self.ptConstraintsTmp_PM_A.append(cmds.pointConstraint(self.insertionLoc_PM_A, self.PM_A_muscleInsertion, mo=False, w=True)[0])
        self.ptConstraintsTmp_PM_B.append(cmds.pointConstraint(self.insertionLoc_PM_B, self.PM_B_muscleInsertion, mo=False, w=True)[0])

        driverGrp_PM_A = cmds.group(name="{0}_muscleCenter_A_grp".format(self.L_R_value), empty=True)
        driverGrp_PM_B = cmds.group(name="{0}_muscleCenter_B_grp".format(self.L_R_value), empty=True)

        self.centerLoc_PM_A = createSpaceLocator(5.0, name="{0}_muscleCenter_loc".format(self.PM_A_muscleOrigin))
        self.centerLoc_PM_B = createSpaceLocator(5.0, name="{0}_muscleCenter_loc".format(self.PM_B_muscleOrigin))

        cmds.parent(self.centerLoc_PM_A, driverGrp_PM_A)
        cmds.parent(self.centerLoc_PM_B, driverGrp_PM_B)
        
        cmds.delete(cmds.pointConstraint(self.PM_A_muscleDriver, driverGrp_PM_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.PM_B_muscleDriver, driverGrp_PM_B, mo=False, w=True))

        cmds.parent(driverGrp_PM_A, self.originLoc_PM_A)
        cmds.parent(driverGrp_PM_B, self.originLoc_PM_B)

        cmds.pointConstraint(self.originLoc_PM_A, self.insertionLoc_PM_A, driverGrp_PM_A, mo=True, w=True)
        cmds.pointConstraint(self.originLoc_PM_B, self.insertionLoc_PM_B, driverGrp_PM_B, mo=True, w=True)

        cmds.setAttr("{0}.r".format(driverGrp_PM_A), 0, 0, 0)
        cmds.setAttr("{0}.r".format(driverGrp_PM_B), 0, 0, 0)

        cmds.delete(self.mainPointConstraint_PM_A)
        cmds.delete(self.mainPointConstraint_PM_B)

        self.ptConstraintsTmp_PM_A.append(cmds.pointConstraint(self.centerLoc_PM_A, self.PM_A_muscleDriver, mo=False, w=True)[0])
        self.ptConstraintsTmp_PM_B.append(cmds.pointConstraint(self.centerLoc_PM_B, self.PM_B_muscleDriver, mo=False, w=True)[0])

        cmds.select(cl = True)
        
        
  
    def update(self, *args):
        ###
        for ptConstraintsTmp_A in self.ptConstraintsTmp_PM_A:
            if cmds.objExists(ptConstraintsTmp_A):
                cmds.delete(ptConstraintsTmp_A)

        for ptConstraintsTmp_B in self.ptConstraintsTmp_PM_B:
            if cmds.objExists(ptConstraintsTmp_B):
                cmds.delete(ptConstraintsTmp_B)

        ###
        for loc_PM_A in [self.originLoc_PM_A, self.insertionLoc_PM_A, self.centerLoc_PM_A]:
            if cmds.objExists(loc_PM_A):
                cmds.delete(loc_PM_A)

        for loc_PM_B in [self.originLoc_PM_B, self.insertionLoc_PM_B, self.centerLoc_PM_B]:
            if cmds.objExists(loc_PM_B):
                cmds.delete(loc_PM_B)
        
        ###
        joints = [self.PM_A_muscleOrigin, self.PM_A_muscleInsertion,
                 self.PM_B_muscleOrigin, self.PM_B_muscleInsertion]

        for i in joints:
            cmds.setAttr("{0}.overrideEnabled".format(i), 0)
            cmds.setAttr("{0}.overrideDisplayType".format(i), 0)

        cmds.delete(self.mainAimConstraint_PM_A)
        cmds.delete(self.mainAimConstraint_PM_B)
        
        self.mainPointConstraint_PM_A = cmds.pointConstraint(self.PM_A_muscleBase, self.PM_A_muscleTip, self.PM_A_muscleDriver,
                                                        mo=True, weight=1)

        self.mainPointConstraint_PM_B = cmds.pointConstraint(self.PM_B_muscleBase, self.PM_B_muscleTip, self.PM_B_muscleDriver,
                                                        mo=True, weight=1)

        cmds.delete(cmds.aimConstraint(self.PM_A_muscleInsertion, self.PM_A_muscleOrigin,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))

        cmds.delete(cmds.aimConstraint(self.PM_B_muscleInsertion, self.PM_B_muscleOrigin,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))

        self.mainAimConstraint_PM_A = cmds.aimConstraint(self.PM_A_muscleInsertion, self.PM_A_muscleBase,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.PM_A_origin,
                                                    worldUpVector=self.upAixs)

        self.mainAimConstraint_PM_B = cmds.aimConstraint(self.PM_B_muscleInsertion, self.PM_B_muscleBase,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.PM_B_origin,
                                                    worldUpVector=self.upAixs)

        animCurveNodes_PM_A = cmds.ls(cmds.listConnections(self.PM_A_muscleJoint, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))

        animCurveNodes_PM_B = cmds.ls(cmds.listConnections(self.PM_B_muscleJoint, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))
        
        cmds.delete(animCurveNodes_PM_A)
        cmds.delete(animCurveNodes_PM_B)

        self.addSDK_A()
        self.addSDK_B()
        cmds.select(cl = True)
        


    def addSDK_A(self, stretchOffset=None, compressionOffset=None):
        self.stretchFactor = float(cmds.textField(self.ui_instance.stretchField, query=True, text=True))
        self.compressionFactor = float(cmds.textField(self.ui_instance.compressionField, query=True, text=True))
        squashScale = math.sqrt(1.0 / self.compressionFactor)
        stretchScale = math.sqrt(1.0 / self.stretchFactor)

        if stretchOffset == None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset == None:
            compressionOffset = [0.0, 0.0, 0.0]
        restLength_PM_A = cmds.getAttr("{0}.translate{1}".format(self.PM_A_muscleTip, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            cmds.setAttr("{0}.scale{1}".format(self.PM_A_muscleJoint, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.PM_A_muscleJoint, axis), 0.0)
        
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.PM_A_muscleJoint, axis),
                                    currentDriver = "{0}.translate{1}".format(self.PM_A_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.PM_A_muscleJoint, axis),
                                   currentDriver = "{0}.translate{1}".format(self.PM_A_muscleTip, self.objectDirectionMenu_value))
           
            # set stretch factor
            cmds.setAttr("{0}.translate{1}".format(self.PM_A_muscleTip, self.objectDirectionMenu_value), restLength_PM_A * self.stretchFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.PM_A_muscleJoint, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.PM_A_muscleJoint, axis), stretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.PM_A_muscleJoint, axis), stretchOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.PM_A_muscleJoint, axis),
                                   currentDriver = "{0}.translate{1}".format(self.PM_A_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.PM_A_muscleJoint, axis),
                                   currentDriver = "{0}.translate{1}".format(self.PM_A_muscleTip, self.objectDirectionMenu_value))
           
            # set squash factor
            cmds.setAttr("{0}.translate{1}".format(self.PM_A_muscleTip, self.objectDirectionMenu_value), restLength_PM_A * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.PM_A_muscleJoint, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.PM_A_muscleJoint, axis), squashScale)
                cmds.setAttr("{0}.translate{1}".format(self.PM_A_muscleJoint, axis), compressionOffset[index])
            
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.PM_A_muscleJoint, axis),
                                   currentDriver = "{0}.translate{1}".format(self.PM_A_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.PM_A_muscleJoint, axis),
                                   currentDriver = "{0}.translate{1}".format(self.PM_A_muscleTip, self.objectDirectionMenu_value))

            cmds.setAttr("{0}.translate{1}".format(self.PM_A_muscleTip, self.objectDirectionMenu_value), restLength_PM_A)



    def addSDK_B(self, stretchOffset=None, compressionOffset=None):
        self.stretchFactor = float(cmds.textField(self.ui_instance.stretchField, query=True, text=True))
        self.compressionFactor = float(cmds.textField(self.ui_instance.compressionField, query=True, text=True))
        yzSquashScale = math.sqrt(1.0 / self.compressionFactor)
        yzStretchScale = math.sqrt(1.0 / self.stretchFactor)

        if stretchOffset == None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset == None:
            compressionOffset = [0.0, 0.0, 0.0]

        restLength_LD_B = cmds.getAttr("{0}.translate{1}".format(self.PM_B_muscleTip, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            # 处理下降部分
            cmds.setAttr("{0}.scale{1}".format(self.PM_B_muscleJoint, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.PM_B_muscleJoint, axis), 0.0)
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.PM_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.PM_B_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.PM_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.PM_B_muscleTip, self.objectDirectionMenu_value))

            # 设置拉伸因子
            cmds.setAttr("{0}.translate{1}".format(self.PM_B_muscleTip, self.objectDirectionMenu_value), restLength_LD_B * self.stretchFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.PM_B_muscleJoint, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.PM_B_muscleJoint, axis), yzStretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.PM_B_muscleJoint, axis), stretchOffset[index])
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.PM_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.PM_B_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.PM_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.PM_B_muscleTip, self.objectDirectionMenu_value))

            # 设置压缩因子
            cmds.setAttr("{0}.translate{1}".format(self.PM_B_muscleTip, self.objectDirectionMenu_value), restLength_LD_B * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.PM_B_muscleJoint, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.PM_B_muscleJoint, axis), yzSquashScale)
                cmds.setAttr("{0}.translate{1}".format(self.PM_B_muscleJoint, axis), compressionOffset[index])
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.PM_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.PM_B_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.PM_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.PM_B_muscleTip, self.objectDirectionMenu_value))
            
            # 恢复原始长度
            cmds.setAttr("{0}.translate{1}".format(self.PM_B_muscleTip, self.objectDirectionMenu_value), restLength_LD_B)



    def muscleJointLib(self, *args):
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)

        self.PM_A_muscleOrigin = "{0}_muscleOrigin_PectoralisMuscle_A".format(self.L_R_value)
        self.PM_A_muscleInsertion = "{0}_muscleInsertion_PectoralisMuscle_A".format(self.L_R_value)

        self.PM_B_muscleOrigin = "{0}_muscleOrigin_PectoralisMuscle_B".format(self.L_R_value)
        self.PM_B_muscleInsertion = "{0}_muscleInsertion_PectoralisMuscle_B".format(self.L_R_value)

        self.PM_A_muscleBase = "{0}_muscleBase_PectoralisMuscle_A".format(self.L_R_value)
        self.PM_B_muscleBase = "{0}_muscleBase_PectoralisMuscle_B".format(self.L_R_value)

        self.PM_A_muscleDriver = "{0}_muscleDriver_PectoralisMuscle_A".format(self.L_R_value)
        self.PM_B_muscleDriver = "{0}_muscleDriver_PectoralisMuscle_B".format(self.L_R_value)

        self.PM_A_muscleOffset = "{0}_muscleOffset_PectoralisMuscle_A".format(self.L_R_value)
        self.PM_B_muscleOffset = "{0}_muscleOffset_PectoralisMuscle_B".format(self.L_R_value)

        self.PM_A_muscleJoint = "{0}_muscleJoint_PectoralisMuscle_A".format(self.L_R_value)
        self.PM_B_muscleJoint = "{0}_muscleJoint_PectoralisMuscle_B".format(self.L_R_value)

        self.PM_A_muscleTip = "{0}_muscleTip_PectoralisMuscle_A".format(self.L_R_value)
        self.PM_B_muscleTip = "{0}_muscleTip_PectoralisMuscle_B".format(self.L_R_value)



    def delete(self, *args):
        self.muscleJointLib()

        joints_to_delete = [
            self.PM_A_muscleOrigin,
            self.PM_A_muscleInsertion,
            self.PM_A_muscleTip,
            self.PM_A_muscleBase,
            self.PM_A_muscleDriver,
            self.PM_A_muscleOffset,
            self.PM_A_muscleJoint,
            self.PM_B_muscleOrigin,
            self.PM_B_muscleInsertion,
            self.PM_B_muscleTip,
            self.PM_B_muscleBase,
            self.PM_B_muscleDriver,
            self.PM_B_muscleOffset,
            self.PM_B_muscleJoint,
        ]

        for i in joints_to_delete:
            if cmds.objExists(i):
                cmds.delete(i)



    def joint_exists(self, joint_name):
        return cmds.ls(joint_name, type="joint")

