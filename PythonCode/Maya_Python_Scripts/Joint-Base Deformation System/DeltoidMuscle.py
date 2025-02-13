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



class DeltoidMuscleGRP(object):
    
    def __init__(self, ui_instance):
        self.ui_instance = ui_instance

        self.AllJoints_DT_A = []
        self.AllJoints_DT_B = []
        self.AllJoints_DT_C = []
        self.axisValue_DT_A = []
        self.axisValue_DT_B = []
        self.axisValue_DT_C = []
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
    def create_DT_A_Joint(self):
        # update joints information
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)

        self.twistJoint_01 = "upperarm_{0}_TwistJoint_001".format(self.L_R_value)
        self.twistJoint_02 = "upperarm_{0}_TwistJoint_002".format(self.L_R_value)
        self.scapulaRoot = "{0}_ScapulaRoot".format(self.L_R_value)
        self.upperArm = "upperarm_{0}".format(self.L_R_value)
        self.acromion = "{0}_Acromion".format(self.L_R_value)
        self.inferiorAngle = "{0}_InferiorAngle".format(self.L_R_value)
        self.clavicle = "clavicle_{0}".format(self.L_R_value)

        DT_A_origin = cmds.textFieldButtonGrp(self.ui_instance.origin_A, q = True, text = True)

        if not DT_A_origin.strip():
            DT_A_origin = self.clavicle

        DT_B_origin = cmds.textFieldButtonGrp(self.ui_instance.origin_B, q = True, text = True)
        if not DT_B_origin.strip():
            DT_B_origin = self.acromion

        DT_C_origin = cmds.textFieldButtonGrp(self.ui_instance.origin_C, q = True, text = True)
        if not DT_C_origin.strip():
            DT_C_origin = self.scapulaRoot

        # check joints already generate or not
        if cmds.ls("{0}_muscleOrigin_DeltoidMuscle_A".format(self.L_R_value), type = "joint") and cmds.ls("{0}_muscleInsertion_DeltoidMuscle_A".format(self.L_R_value), type = "joint"):
            cmds.warning("DT A already Exist !!!") 
            return None
        
        print("Generating DT A Joints")
        cmds.select(clear = True)
        self.DT_A_muscleOrigin = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "DeltoidMuscle_A")

        # calculus origin joint position
        DT_A_startPosition_start = om.MVector(cmds.xform(DT_A_origin, t = True, ws = True, q = True))
        DT_A_startPosition_end = om.MVector(cmds.xform( DT_B_origin, t = True, ws = True, q = True))
        DT_A_startPosition_finalPosition = ( DT_A_startPosition_end - DT_A_startPosition_start) * 5 / 6.0 + DT_A_startPosition_start
        cmds.xform(self.DT_A_muscleOrigin, t = DT_A_startPosition_finalPosition, ws = True)

        cmds.select(self.DT_A_muscleOrigin)

        # duplicate a new joint call insertion joint
        self.DT_A_muscleInsertion = cmds.duplicate(self.DT_A_muscleOrigin, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "DeltoidMuscle_A")[0]

        # get DT_A_end start and end joint Position
        DT_A_end_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_A, q = True, text = True)
        if not DT_A_end_joint.strip():
            DT_A_end_joint = self.twistJoint_02

        DT_A_end_joint_position = om.MVector(cmds.xform(DT_A_end_joint, t = True, ws = True, q = True))
        cmds.xform(self.DT_A_muscleInsertion, t = DT_A_end_joint_position, ws = True)
        cmds.select(cl = True)

        # create muscle base
        self.DT_A_muscleBase = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "DeltoidMuscle_A")
        cmds.select(cl = True)
        # create muscle tip
        self.DT_A_muscleTip = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "DeltoidMuscle_A")
        cmds.select(cl = True)
        # create muscle driver and it child
        self.DT_A_muscleDriver = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "DeltoidMuscle_A")
        self.DT_A_muscleOffset = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "DeltoidMuscle_A")
        self.DT_A_muscleJoint = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "DeltoidMuscle_A")
        cmds.select(cl = True)

        # move muscle base to correct position and get it rotation
        get_DT_A_muscleOrigin_joint_position = om.MVector(cmds.xform(self.DT_A_muscleOrigin, t = True, ws = True, q = True))
        get_DT_A_muscleOrigin_joint_rotation = om.MVector(cmds.xform(self.DT_A_muscleOrigin, ro = True, ws = True, q = True))
        cmds.xform(self.DT_A_muscleBase, t = get_DT_A_muscleOrigin_joint_position, ws = True)
        cmds.xform(self.DT_A_muscleBase, ro = get_DT_A_muscleOrigin_joint_rotation, ws = True)
        
        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint LD A position
        get_DT_A_muscleInsertion_position = om.MVector(cmds.xform(self.DT_A_muscleInsertion, t = True, ws = True, q = True))
        muscleDriver_finalPosition = ( get_DT_A_muscleOrigin_joint_position + get_DT_A_muscleInsertion_position) * 0.5
        cmds.xform(self.DT_A_muscleDriver, t = muscleDriver_finalPosition, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.DT_A_muscleTip, t = get_DT_A_muscleInsertion_position, ws = True)

        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.DT_A_muscleTip, apply=True, rotate=True)
        cmds.parent(self.DT_A_muscleTip, self.DT_A_muscleBase)
        cmds.joint(self.DT_A_muscleBase, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        DT_A_get_muscleBase_rotation = om.MVector(cmds.xform(self.DT_A_muscleBase, ro = True, ws = True, q = True))
        cmds.xform(self.DT_A_muscleTip, ro = DT_A_get_muscleBase_rotation, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.DT_A_muscleDriver, ro = DT_A_get_muscleBase_rotation, ws = True)
        cmds.xform(self.DT_A_muscleOffset, ro = DT_A_get_muscleBase_rotation, ws = True)
        cmds.xform(self.DT_A_muscleJoint, ro = DT_A_get_muscleBase_rotation, ws = True)

        # apply origin joint rotation to base joint
        cmds.xform(self.DT_A_muscleOrigin, ro = DT_A_get_muscleBase_rotation, ws = True)

        # apply end joint rotation to insertion joint
        DT_A_end_joint_rotation = om.MVector(cmds.xform(DT_A_end_joint, ro = True, ws = True, q = True))
        cmds.xform(self.DT_A_muscleInsertion, ro = DT_A_end_joint_rotation, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.DT_A_muscleOrigin, apply=True, rotate=True)
        cmds.makeIdentity(self.DT_A_muscleInsertion, apply=True, rotate=True)
        cmds.makeIdentity(self.DT_A_muscleDriver, apply=True, rotate=True)
        cmds.makeIdentity(self.DT_A_muscleTip, apply=True, rotate=True)

        # parent joints
        cmds.parent(self.DT_A_muscleOrigin, DT_A_origin)
        cmds.parent(self.DT_A_muscleInsertion, DT_A_end_joint)
        cmds.parent(self.DT_A_muscleBase, self.DT_A_muscleOrigin)
        cmds.parent(self.DT_A_muscleDriver, self.DT_A_muscleBase)

        # pass joints date to __init__
        self.AllJoints_DT_A.extend([self.DT_A_muscleOrigin, self.DT_A_muscleInsertion, self.DT_A_muscleBase, self.DT_A_muscleTip,
                            self.DT_A_muscleDriver, self.DT_A_muscleOffset, self.DT_A_muscleJoint])
        print("Compelete Generating DT A Joints")

        # update joints color
        orange_color_index = 7
        def set_joint_color(joint, color_index):
            cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
            cmds.setAttr("{0}.overrideColor".format(joint), color_index)
        for joint in self.AllJoints_DT_A:
            set_joint_color(joint, orange_color_index)

        return True
            
        
    
    def create_DT_A_Constraint(self):

        result = self.create_DT_A_Joint()
        if result == None:
            return None
        
        if result == True:
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.DT_A_muscleInsertion, self.DT_A_muscleTip, maintainOffset = False,
                                weight = 1)

            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_DT_A = cmds.pointConstraint(self.DT_A_muscleBase, self.DT_A_muscleTip, self.DT_A_muscleDriver, maintainOffset = True,
                                weight=1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_DT_A = cmds.aimConstraint(self.DT_A_muscleInsertion, self.DT_A_muscleBase,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.twistJoint_01,
                                                        worldUpVector = self.upAixs)
            self.axisValue_DT_A.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_DT_A, self.mainAimConstraint_DT_A])
    
            print("Compelete DT A Constraint")
            self.addSDK_A()
            print("Compelete DT A Set SDK")



    def create_DT_B_Joint(self):
        # update joints information
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)
        self.twistJoint_01 = "upperarm_{0}_TwistJoint_001".format(self.L_R_value)
        self.twistJoint_02 = "upperarm_{0}_TwistJoint_002".format(self.L_R_value)
        self.scapulaRoot = "{0}_ScapulaRoot".format(self.L_R_value)
        self.upperArm = "upperarm_{0}".format(self.L_R_value)
        self.acromion = "{0}_Acromion".format(self.L_R_value)
        self.inferiorAngle = "{0}_InferiorAngle".format(self.L_R_value)
        self.clavicle = "clavicle_{0}".format(self.L_R_value)

        DT_B_origin = cmds.textFieldButtonGrp(self.ui_instance.origin_B, q = True, text = True)

        if not DT_B_origin.strip():
            DT_B_origin = self.acromion

        # check joints already generate or not
        if cmds.ls("{0}_muscleOrigin_DeltoidMuscle_B".format(self.L_R_value), type = "joint") and cmds.ls("{0}_muscleInsertion_DeltoidMuscle_B".format(self.L_R_value), type = "joint"):
            cmds.warning("DT B already Exist !!!") 
            return None
        
        print("Generating DT B Joints")
        cmds.select(clear = True)
        self.DT_B_muscleOrigin = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "DeltoidMuscle_B")

        # calculus origin joint position
        DT_B_startPosition = om.MVector(cmds.xform(DT_B_origin, t = True, ws = True, q = True))
        cmds.xform(self.DT_B_muscleOrigin, t = DT_B_startPosition, ws = True)
        cmds.select(self.DT_B_muscleOrigin)

        # duplicate a new joint call insertion joint
        self.DT_B_muscleInsertion = cmds.duplicate(self.DT_B_muscleOrigin, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "DeltoidMuscle_B")[0]

        # get DT_B_end start and end joint Position
        DT_B_end_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_B, q = True, text = True)
        if not DT_B_end_joint.strip():
            DT_B_end_joint = self.twistJoint_02
        DT_B_end_joint_position = om.MVector(cmds.xform(DT_B_end_joint, t = True, ws = True, q = True))
        cmds.xform(self.DT_B_muscleInsertion, t = DT_B_end_joint_position, ws = True)
        cmds.select(cl = True)

        # create muscle base
        self.DT_B_muscleBase = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "DeltoidMuscle_B")
        cmds.select(cl = True)
        # create muscle tip
        self.DT_B_muscleTip = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "DeltoidMuscle_B")
        cmds.select(cl = True)
        # create muscle driver and it child
        self.DT_B_muscleDriver = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "DeltoidMuscle_B")
        self.DT_B_muscleOffset = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "DeltoidMuscle_B")
        self.DT_B_muscleJoint = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "DeltoidMuscle_B")
        cmds.select(cl = True)

        # move muscle base to correct position and get it rotation
        get_DT_B_muscleOrigin_joint_position = om.MVector(cmds.xform(self.DT_B_muscleOrigin, t = True, ws = True, q = True))
        get_DT_B_muscleOrigin_joint_rotation = om.MVector(cmds.xform(self.DT_B_muscleOrigin, ro = True, ws = True, q = True))
        cmds.xform(self.DT_B_muscleBase, t = get_DT_B_muscleOrigin_joint_position, ws = True)
        cmds.xform(self.DT_B_muscleBase, ro = get_DT_B_muscleOrigin_joint_rotation, ws = True)
        
        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint LD A position
        get_DT_B_muscleInsertion_position = om.MVector(cmds.xform(self.DT_B_muscleInsertion, t = True, ws = True, q = True))
        muscleDriver_joint_finalPosition = (get_DT_B_muscleOrigin_joint_position + get_DT_B_muscleInsertion_position) * 0.5
        cmds.xform(self.DT_B_muscleDriver, t = muscleDriver_joint_finalPosition, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.DT_B_muscleTip, t = get_DT_B_muscleInsertion_position, ws = True)

        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.DT_B_muscleTip, apply=True, rotate=True)
        cmds.parent(self.DT_B_muscleTip, self.DT_B_muscleBase)
        cmds.joint(self.DT_B_muscleBase, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        DT_B_get_muscleBase_rotation = om.MVector(cmds.xform(self.DT_B_muscleBase, ro = True, ws = True, q = True))
        cmds.xform(self.DT_B_muscleTip, ro = DT_B_get_muscleBase_rotation, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.DT_B_muscleDriver, ro = DT_B_get_muscleBase_rotation, ws = True)
        cmds.xform(self.DT_B_muscleOffset, ro = DT_B_get_muscleBase_rotation, ws = True)
        cmds.xform(self.DT_B_muscleJoint, ro = DT_B_get_muscleBase_rotation, ws = True)

        # apply origin joint rotation to base joint
        cmds.xform(self.DT_B_muscleOrigin, ro =  DT_B_get_muscleBase_rotation, ws = True)

        # apply end joint rotation to insertion joint
        DT_B_end_joint_rotation = om.MVector(cmds.xform(DT_B_end_joint, ro = True, ws = True, q = True))
        cmds.xform(self.DT_B_muscleInsertion, ro = DT_B_end_joint_rotation, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.DT_B_muscleOrigin, apply=True, rotate=True)
        cmds.makeIdentity(self.DT_B_muscleInsertion, apply=True, rotate=True)
        cmds.makeIdentity(self.DT_B_muscleDriver, apply=True, rotate=True)
        cmds.makeIdentity(self.DT_B_muscleTip, apply=True, rotate=True)

        # parent joints
        cmds.parent(self.DT_B_muscleOrigin, DT_B_origin)
        cmds.parent(self.DT_B_muscleInsertion, DT_B_end_joint)
        cmds.parent(self.DT_B_muscleBase, self.DT_B_muscleOrigin)
        cmds.parent(self.DT_B_muscleDriver, self.DT_B_muscleBase)

        # pass joints date to __init__
        self.AllJoints_DT_B.extend([self.DT_B_muscleOrigin, self.DT_B_muscleInsertion, self.DT_B_muscleBase, self.DT_B_muscleTip,
                            self.DT_B_muscleDriver, self.DT_B_muscleOffset, self.DT_B_muscleJoint])
    
        print("Compelete Generating DT B Joints")

        # update joints color
        orange_color_index = 7

        # # Function to update joint color
        def set_joint_color(joint, color_index):
            cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
            cmds.setAttr("{0}.overrideColor".format(joint), color_index)
        for joint in self.AllJoints_DT_B:
            set_joint_color(joint, orange_color_index)
        return True



    def create_DT_B_Constraint(self):
        result = self.create_DT_B_Joint()
        if result == None:
            return None
        
        if result == True:
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.DT_B_muscleInsertion, self.DT_B_muscleTip, maintainOffset = False,
                                weight = 1)

            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_DT_B = cmds.pointConstraint(self.DT_B_muscleBase, self.DT_B_muscleTip, self.DT_B_muscleDriver, maintainOffset = True,
                                weight=1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_DT_B = cmds.aimConstraint(self.DT_B_muscleInsertion, self.DT_B_muscleBase,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.twistJoint_01,
                                                        worldUpVector = self.upAixs)

            self.axisValue_DT_B.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_DT_B, self.mainAimConstraint_DT_B])
            
            print("Compelete DT B Constraint")
            self.addSDK_B()
            print("Compelete DT B Set SDK")



    def create_DT_C_Joint(self):
        # update joints information
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)
        self.twistJoint_01 = "upperarm_{0}_TwistJoint_001".format(self.L_R_value)
        self.twistJoint_02 = "upperarm_{0}_TwistJoint_002".format(self.L_R_value)
        self.scapulaRoot = "{0}_ScapulaRoot".format(self.L_R_value)
        self.acromion = "{0}_Acromion".format(self.L_R_value)
        self.upperArm = "upperarm_{0}".format(self.L_R_value)

        DT_C_origin = cmds.textFieldButtonGrp(self.ui_instance.origin_C, q = True, text = True)
        if not DT_C_origin.strip():
            DT_C_origin = self.acromion

        # check joints already generate or not
        if cmds.ls("{0}_muscleOrigin_DeltoidMuscle_C".format(self.L_R_value), type = "joint") and cmds.ls("{0}_muscleInsertion_DeltoidMuscle_C".format(self.L_R_value), type = "joint"):
            cmds.warning("DT C already Exist !!!") 
            return None
        
        print("Generating DT C Joints")
        cmds.select(clear = True)
        self.DT_C_muscleOrigin = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "DeltoidMuscle_C")

        # calculus origin joint position
        DT_C_origin_startPosition = om.MVector(cmds.xform(DT_C_origin, t = True, ws = True, q = True))
        DT_C_origin_endPosition = om.MVector(cmds.xform(self.scapulaRoot, t = True, ws = True, q = True))

        DT_C_origin_finalPosition = (DT_C_origin_endPosition - DT_C_origin_startPosition) * 1 / 6.0 + DT_C_origin_startPosition
        cmds.xform(self.DT_C_muscleOrigin, t = DT_C_origin_finalPosition, ws = True)

        cmds.select(self.DT_C_muscleOrigin)

        # duplicate a new joint call insertion joint
        self.DT_C_muscleInsertion = cmds.duplicate(self.DT_C_muscleOrigin, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "DeltoidMuscle_C")[0]

        # get DT_C_end start and end joint Position
        DT_C_end_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_C, q = True, text = True)
        if not DT_C_end_joint.strip():
            DT_C_end_joint = self.twistJoint_02

        DT_C_end_joint_position = om.MVector(cmds.xform(DT_C_end_joint, t = True, ws = True, q = True))
        cmds.xform(self.DT_C_muscleInsertion, t = DT_C_end_joint_position, ws = True)
        cmds.select(cl = True)

        # create muscle base
        self.DT_C_muscleBase = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "DeltoidMuscle_C")
        cmds.select(cl = True)
        # create muscle tip
        self.DT_C_muscleTip = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "DeltoidMuscle_C")
        cmds.select(cl = True)
        # create muscle driver and it child
        self.DT_C_muscleDriver = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "DeltoidMuscle_C")
        self.DT_C_muscleOffset = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "DeltoidMuscle_C")
        self.DT_C_muscleJoint = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "DeltoidMuscle_C")
        cmds.select(cl = True)

        # move muscle base to correct position and get it rotation
        get_DT_C_muscleOrigin_joint_position = om.MVector(cmds.xform(self.DT_C_muscleOrigin, t = True, ws = True, q = True))
        get_DT_C_muscleOrigin_joint_rotation = om.MVector(cmds.xform(self.DT_C_muscleOrigin, ro = True, ws = True, q = True))
        cmds.xform(self.DT_C_muscleBase, t = get_DT_C_muscleOrigin_joint_position, ws = True)
        cmds.xform(self.DT_C_muscleBase, ro = get_DT_C_muscleOrigin_joint_rotation, ws = True)
        
        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint DT C position
        get_DT_C_muscleInsertion_position = om.MVector(cmds.xform(self.DT_C_muscleInsertion, t = True, ws = True, q = True))
        muscleDriver_finalPosition = (get_DT_C_muscleOrigin_joint_position + get_DT_C_muscleInsertion_position) * 0.5
        cmds.xform(self.DT_C_muscleDriver, t = muscleDriver_finalPosition, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.DT_C_muscleTip, t = get_DT_C_muscleInsertion_position, ws = True)

        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.DT_C_muscleTip, apply=True, rotate=True)
        cmds.parent(self.DT_C_muscleTip, self.DT_C_muscleBase)
        cmds.joint(self.DT_C_muscleBase, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        DT_C_get_muscleBase_rotation = om.MVector(cmds.xform(self.DT_C_muscleBase, ro = True, ws = True, q = True))
        cmds.xform(self.DT_C_muscleTip, ro = DT_C_get_muscleBase_rotation, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.DT_C_muscleDriver, ro = DT_C_get_muscleBase_rotation, ws = True)
        cmds.xform(self.DT_C_muscleOffset, ro = DT_C_get_muscleBase_rotation, ws = True)
        cmds.xform(self.DT_C_muscleJoint, ro = DT_C_get_muscleBase_rotation, ws = True)

        # apply origin joint rotation to base joint
        DT_C_end_joint_rotation = om.MVector(cmds.xform(DT_C_end_joint, ro = True, ws = True, q = True))
        cmds.xform(self.DT_C_muscleInsertion, ro = DT_C_end_joint_rotation, ws = True)

        # apply end joint rotation to insertion joint
        cmds.xform(self.DT_C_muscleOrigin, ro =  DT_C_get_muscleBase_rotation, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.DT_C_muscleOrigin, apply=True, rotate=True)
        cmds.makeIdentity(self.DT_C_muscleInsertion, apply=True, rotate=True)
        cmds.makeIdentity(self.DT_C_muscleDriver, apply=True, rotate=True)
        cmds.makeIdentity(self.DT_C_muscleTip, apply=True, rotate=True)

        # parent joints
        cmds.parent(self.DT_C_muscleOrigin, DT_C_origin)
        cmds.parent(self.DT_C_muscleInsertion, DT_C_end_joint)
        cmds.parent(self.DT_C_muscleBase, self.DT_C_muscleOrigin)
        cmds.parent(self.DT_C_muscleDriver, self.DT_C_muscleBase)

        # pass joints date to __init__
        self.AllJoints_DT_C.extend([self.DT_C_muscleOrigin, self.DT_C_muscleInsertion, self.DT_C_muscleBase, self.DT_C_muscleTip,
                            self.DT_C_muscleDriver, self.DT_C_muscleOffset, self.DT_C_muscleJoint])
    
        print("Compelete Generating DT C Joints")

        # update joints color
        orange_color_index = 7

        # # Function to update joint color
        def set_joint_color(joint, color_index):
            cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
            cmds.setAttr("{0}.overrideColor".format(joint), color_index)
        for joint in self.AllJoints_DT_C:
            set_joint_color(joint, orange_color_index)

        cmds.select(cl = True)

        return True
    
    def create_DT_C_Constraint(self):
        result = self.create_DT_C_Joint()
        if result == None:
            return None
        
        if result == True:
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.DT_C_muscleInsertion, self.DT_C_muscleTip, maintainOffset = False,
                                weight = 1)

            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_DT_C = cmds.pointConstraint(self.DT_C_muscleBase, self.DT_C_muscleTip, self.DT_C_muscleDriver, maintainOffset = True,
                                weight = 1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_DT_C = cmds.aimConstraint(self.DT_C_muscleInsertion, self.DT_C_muscleBase,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.twistJoint_01,
                                                        worldUpVector = self.upAixs)
            
            # # point constraint muscleOffset A, C with B
            # self.offsetAllMuscleJnt = cmds.pointConstraint(self.DT_A_muscleOffset, self.DT_C_muscleOffset, self.DT_B_muscleOffset, maintainOffset = True, 
            #                      weight = 1)
            
            # self.keepOffsetSet = cmds.pointConstraint(self.upperArm, self.DT_C_muscleOffset, maintainOffset = True, skip = ["x","y"], 
            #                      weight = 1)

            self.axisValue_DT_C.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_DT_C, self.mainAimConstraint_DT_C])
            
            print("Compelete DT C Constraint")
            self.addSDK_C()
            print("Compelete DT C Set SDK")

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
        self.mainPointConstraint_DT_A = cmds.pointConstraint(self.DT_A_muscleBase, self.DT_A_muscleTip, self.DT_A_muscleDriver, maintainOffset = True,
                                            weight=1)
        self.mainAimConstraint_DT_A = cmds.aimConstraint(self.DT_A_muscleInsertion, self.DT_A_muscleBase,
                                                    aimVector = self.dirAxis, upVector = self.upAixs,
                                                    worldUpType = "objectrotation", worldUpObject = self.twistJoint_01,
                                                    worldUpVector = self.upAixs)
        self.mainPointConstraint_DT_B = cmds.pointConstraint(self.DT_B_muscleBase, self.DT_B_muscleTip, self.DT_B_muscleDriver, maintainOffset = True,
                                weight=1)
        self.mainAimConstraint_DT_B = cmds.aimConstraint(self.DT_B_muscleInsertion, self.DT_B_muscleBase,
                                            aimVector = self.dirAxis, upVector = self.upAixs,
                                            worldUpType = "objectrotation", worldUpObject = self.twistJoint_01,
                                            worldUpVector = self.upAixs)
        
        self.mainPointConstrain_DT_C = cmds.pointConstraint(self.DT_C_muscleBase, self.DT_C_muscleTip, self.DT_C_muscleDriver, maintainOffset = True,
                                            weight=1)

        self.mainAimConstraint_DT_C = cmds.aimConstraint(self.DT_C_muscleInsertion, self.DT_C_muscleBase,
                                                    aimVector = self.dirAxis, upVector = self.upAixs,
                                                    worldUpType = "objectrotation", worldUpObject = self.twistJoint_01,
                                                    worldUpVector = self.upAixs)


 
        # set joints to templete
        joints =[ self.DT_A_muscleOrigin, self.DT_A_muscleInsertion, 
                 self.DT_B_muscleOrigin, self.DT_B_muscleInsertion,
                ]
        for i in joints:
            cmds.setAttr("{0}.overrideEnabled".format(i), 1)
            cmds.setAttr("{0}.overrideDisplayType".format(i), 1)
        
        self.ptConstraintsTmp_DT_A = []
        self.ptConstraintsTmp_DT_B = []
        self.ptConstraintsTmp_DT_C = []

        self.originLoc_DT_A = createSpaceLocator(5.0, name="{0}_muscleOrigin_loc_A".format(self.L_R_value))
        self.originLoc_DT_B = createSpaceLocator(5.0, name="{0}_muscleOrigin_loc_B".format(self.L_R_value))
        self.originLoc_DT_C = createSpaceLocator(5.0, name="{0}_muscleOrigin_loc_C".format(self.L_R_value))

        if self.originAttachObj:
            cmds.parent(self.originLoc_DT_A, self.originAttachObj)
            cmds.parent(self.originLoc_DT_B, self.originAttachObj)
            cmds.parent(self.originLoc_DT_C, self.originAttachObj)

        cmds.delete(cmds.pointConstraint(self.DT_A_muscleOrigin, self.originLoc_DT_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.DT_B_muscleOrigin, self.originLoc_DT_B, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.DT_C_muscleOrigin, self.originLoc_DT_C, mo=False, w=True))

        self.ptConstraintsTmp_DT_A.append(cmds.pointConstraint(self.originLoc_DT_A, self.DT_A_muscleOrigin, mo=False, w=True)[0])
        self.ptConstraintsTmp_DT_B.append(cmds.pointConstraint(self.originLoc_DT_B, self.DT_B_muscleOrigin, mo=False, w=True)[0])
        self.ptConstraintsTmp_DT_C.append(cmds.pointConstraint(self.originLoc_DT_C, self.DT_C_muscleOrigin, mo=False, w=True)[0])

        self.insertionLoc_DT_A = createSpaceLocator(5.0, name="{0}_muscleInsertion_loc_A".format(self.L_R_value))
        self.insertionLoc_DT_B = createSpaceLocator(5.0, name="{0}_muscleInsertion_loc_B".format(self.L_R_value))
        self.insertionLoc_DT_C = createSpaceLocator(5.0, name="{0}_muscleInsertion_loc_C".format(self.L_R_value))

        if self.insertionAttachObj:
            cmds.parent(self.insertionLoc_DT_A, self.insertionAttachObj)
            cmds.parent(self.insertionLoc_DT_B, self.insertionAttachObj)
            cmds.parent(self.insertionLoc_DT_C, self.insertionAttachObj)

        def get_reverse_direction():
            return[-value for value in self.dirAxis]
        
        cmds.aimConstraint(self.insertionLoc_DT_A, self.originLoc_DT_A,
                           aimVector = self.dirAxis, upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        
        cmds.aimConstraint(self.insertionLoc_DT_A, self.originLoc_DT_A,
                           aimVector = get_reverse_direction(), upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)

        cmds.aimConstraint(self.insertionLoc_DT_B, self.originLoc_DT_B,
                           aimVector = self.dirAxis, upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        
        cmds.aimConstraint(self.insertionLoc_DT_B, self.originLoc_DT_B,
                           aimVector = get_reverse_direction(), upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)

        cmds.aimConstraint(self.insertionLoc_DT_C, self.originLoc_DT_C,
                           aimVector = self.dirAxis, upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        
        cmds.aimConstraint(self.insertionLoc_DT_C, self.originLoc_DT_C,
                           aimVector = get_reverse_direction(), upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        
        cmds.delete(cmds.pointConstraint(self.DT_A_muscleInsertion, self.insertionLoc_DT_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.DT_B_muscleInsertion, self.insertionLoc_DT_B, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.DT_C_muscleInsertion, self.insertionLoc_DT_C, mo=False, w=True))

        self.ptConstraintsTmp_DT_A.append(cmds.pointConstraint(self.insertionLoc_DT_A, self.DT_A_muscleInsertion, mo=False, w=True)[0])
        self.ptConstraintsTmp_DT_B.append(cmds.pointConstraint(self.insertionLoc_DT_B, self.DT_B_muscleInsertion, mo=False, w=True)[0])
        self.ptConstraintsTmp_DT_C.append(cmds.pointConstraint(self.insertionLoc_DT_C, self.DT_C_muscleInsertion, mo=False, w=True)[0])

        driverGrp_DT_A = cmds.group(name="{0}_muscleCenter_A_grp".format(self.L_R_value), empty=True)
        driverGrp_DT_B = cmds.group(name="{0}_muscleCenter_B_grp".format(self.L_R_value), empty=True)
        driverGrp_DT_C = cmds.group(name="{0}_muscleCenter_C_grp".format(self.L_R_value), empty=True)

        self.centerLoc_DT_A = createSpaceLocator(5.0, name="{0}_muscleCenter_loc".format(self.DT_A_muscleOrigin))
        self.centerLoc_DT_B = createSpaceLocator(5.0, name="{0}_muscleCenter_loc".format(self.DT_B_muscleOrigin))
        self.centerLoc_DT_C = createSpaceLocator(5.0, name="{0}_muscleCenter_loc".format(self.DT_C_muscleOrigin))

        cmds.parent(self.centerLoc_DT_A, driverGrp_DT_A)
        cmds.parent(self.centerLoc_DT_B, driverGrp_DT_B)
        cmds.parent(self.centerLoc_DT_C, driverGrp_DT_C)
        
        
        cmds.delete(cmds.pointConstraint(self.DT_A_muscleDriver, driverGrp_DT_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.DT_B_muscleDriver, driverGrp_DT_B, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.DT_C_muscleDriver, driverGrp_DT_C, mo=False, w=True))

        cmds.parent(driverGrp_DT_A, self.originLoc_DT_A)
        cmds.parent(driverGrp_DT_B, self.originLoc_DT_B)
        cmds.parent(driverGrp_DT_C, self.originLoc_DT_C)

        
        cmds.pointConstraint(self.originLoc_DT_A, self.insertionLoc_DT_A, driverGrp_DT_A, mo=True, w=True)
        cmds.pointConstraint(self.originLoc_DT_B, self.insertionLoc_DT_B, driverGrp_DT_B, mo=True, w=True)
        cmds.pointConstraint(self.originLoc_DT_C, self.insertionLoc_DT_C, driverGrp_DT_C, mo=True, w=True)

        cmds.setAttr("{0}.r".format(driverGrp_DT_A), 0, 0, 0)
        cmds.setAttr("{0}.r".format(driverGrp_DT_B), 0, 0, 0)
        cmds.setAttr("{0}.r".format(driverGrp_DT_C), 0, 0, 0)

        cmds.delete(self.mainPointConstraint_DT_A)
        cmds.delete(self.mainPointConstraint_DT_B)
        cmds.delete(self.mainPointConstraint_DT_C)

        self.ptConstraintsTmp_DT_A.append(cmds.pointConstraint(self.centerLoc_DT_A, self.DT_A_muscleDriver, mo=False, w=True)[0])
        self.ptConstraintsTmp_DT_B.append(cmds.pointConstraint(self.centerLoc_DT_B, self.DT_B_muscleDriver, mo=False, w=True)[0])
        self.ptConstraintsTmp_DT_C.append(cmds.pointConstraint(self.centerLoc_DT_C, self.DT_C_muscleDriver, mo=False, w=True)[0])

        cmds.select(cl = True)
        
        
  
    def update(self, *args):
        ###
        for ptConstraintsTmp_A in self.ptConstraintsTmp_DT_A:
            if cmds.objExists(ptConstraintsTmp_A):
                cmds.delete(ptConstraintsTmp_A)

        for ptConstraintsTmp_B in self.ptConstraintsTmp_DT_B:
            if cmds.objExists(ptConstraintsTmp_B):
                cmds.delete(ptConstraintsTmp_B)

        for ptConstraintsTmp_C in self.ptConstraintsTmp_DT_C:
            if cmds.objExists(ptConstraintsTmp_C):
                cmds.delete(ptConstraintsTmp_C)

        ###
        for loc_DT_A in [self.originLoc_DT_A, self.insertionLoc_DT_A, self.centerLoc_DT_A]:
            if cmds.objExists(loc_DT_A):
                cmds.delete(loc_DT_A)

        for loc_DT_B in [self.originLoc_DT_B, self.insertionLoc_DT_B, self.centerLoc_DT_B]:
            if cmds.objExists(loc_DT_B):
                cmds.delete(loc_DT_B)

        for loc_DT_C in [self.originLoc_DT_C, self.insertionLoc_DT_C, self.centerLoc_DT_C]:
            if cmds.objExists(loc_DT_C):
                cmds.delete(loc_DT_C)
        
        ###
        joints =[ self.DT_A_muscleOrigin, self.DT_A_muscleInsertion, 
                 self.DT_B_muscleOrigin, self.DT_B_muscleInsertion,
                 self.DT_C_muscleOrigin, self.DT_C_muscleInsertion
                ]
        for i in joints:
            cmds.setAttr("{0}.overrideEnabled".format(i), 0)
            cmds.setAttr("{0}.overrideDisplayType".format(i), 0)

        cmds.delete(self.mainAimConstraint_DT_A)
        cmds.delete(self.mainAimConstraint_DT_B)
        cmds.delete(self.mainAimConstraint_DT_C)
        
        self.mainPointConstraint_DT_A = cmds.pointConstraint(self.DT_A_muscleBase, self.DT_A_muscleTip, self.DT_A_muscleDriver,
                                                        mo=True, weight=1)

        self.mainPointConstraint_DT_B = cmds.pointConstraint(self.DT_B_muscleBase, self.DT_B_muscleTip, self.DT_B_muscleDriver,
                                                        mo=True, weight=1)

        self.mainPointConstraint_DT_C = cmds.pointConstraint(self.DT_C_muscleBase, self.DT_C_muscleTip, self.DT_C_muscleDriver,
                                                        mo=True, weight=1)

        cmds.delete(cmds.aimConstraint(self.DT_A_muscleInsertion, self.DT_A_muscleOrigin,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))

        cmds.delete(cmds.aimConstraint(self.DT_B_muscleInsertion, self.DT_B_muscleOrigin,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))
        
        cmds.delete(cmds.aimConstraint(self.DT_C_muscleInsertion, self.DT_C_muscleOrigin,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))

        self.mainAimConstraint_DT_A = cmds.aimConstraint(self.DT_A_muscleInsertion, self.DT_A_muscleBase,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.twistJoint_01,
                                                    worldUpVector=self.upAixs)

        self.mainAimConstraint_DT_B = cmds.aimConstraint(self.DT_B_muscleInsertion, self.DT_B_muscleBase,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.twistJoint_01,
                                                    worldUpVector=self.upAixs)
        
        self.mainAimConstraint_DT_C = cmds.aimConstraint(self.DT_C_muscleInsertion, self.DT_C_muscleBase,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.twistJoint_01,
                                                    worldUpVector=self.upAixs)

        animCurveNodes_DT_A = cmds.ls(cmds.listConnections(self.DT_A_muscleJoint, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))

        animCurveNodes_DT_B = cmds.ls(cmds.listConnections(self.DT_B_muscleJoint, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))
        
        animCurveNodes_DT_C = cmds.ls(cmds.listConnections(self.DT_C_muscleJoint, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))
        
        cmds.delete(animCurveNodes_DT_A)
        cmds.delete(animCurveNodes_DT_B)
        cmds.delete(animCurveNodes_DT_C)

        self.addSDK_A()
        self.addSDK_B()
        self.addSDK_C()
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
        restLength_DT_A = cmds.getAttr("{0}.translate{1}".format(self.DT_A_muscleTip, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            cmds.setAttr("{0}.scale{1}".format(self.DT_A_muscleJoint, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.DT_A_muscleJoint, axis), 0.0)
        
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.DT_A_muscleJoint, axis),
                                    currentDriver = "{0}.translate{1}".format(self.DT_A_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.DT_A_muscleJoint, axis),
                                   currentDriver = "{0}.translate{1}".format(self.DT_A_muscleTip, self.objectDirectionMenu_value))
           
            # set stretch factor
            cmds.setAttr("{0}.translate{1}".format(self.DT_A_muscleTip, self.objectDirectionMenu_value), restLength_DT_A * self.stretchFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.DT_A_muscleJoint, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.DT_A_muscleJoint, axis), stretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.DT_A_muscleJoint, axis), stretchOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.DT_A_muscleJoint, axis),
                                   currentDriver = "{0}.translate{1}".format(self.DT_A_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.DT_A_muscleJoint, axis),
                                   currentDriver = "{0}.translate{1}".format(self.DT_A_muscleTip, self.objectDirectionMenu_value))
           
            # set squash factor
            cmds.setAttr("{0}.translate{1}".format(self.DT_A_muscleTip, self.objectDirectionMenu_value), restLength_DT_A * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.DT_A_muscleJoint, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.DT_A_muscleJoint, axis), squashScale)
                cmds.setAttr("{0}.translate{1}".format(self.DT_A_muscleJoint, axis), compressionOffset[index])
            
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.DT_A_muscleJoint, axis),
                                   currentDriver = "{0}.translate{1}".format(self.DT_A_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.DT_A_muscleJoint, axis),
                                   currentDriver = "{0}.translate{1}".format(self.DT_A_muscleTip, self.objectDirectionMenu_value))

            cmds.setAttr("{0}.translate{1}".format(self.DT_A_muscleTip, self.objectDirectionMenu_value), restLength_DT_A)



    def addSDK_B(self, stretchOffset=None, compressionOffset=None):
        self.stretchFactor = float(cmds.textField(self.ui_instance.stretchField, query=True, text=True))
        self.compressionFactor = float(cmds.textField(self.ui_instance.compressionField, query=True, text=True))
        yzSquashScale = math.sqrt(1.0 / self.compressionFactor)
        yzStretchScale = math.sqrt(1.0 / self.stretchFactor)

        if stretchOffset == None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset == None:
            compressionOffset = [0.0, 0.0, 0.0]

        restLength_LD_B = cmds.getAttr("{0}.translate{1}".format(self.DT_B_muscleTip, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            # 处理下降部分
            cmds.setAttr("{0}.scale{1}".format(self.DT_B_muscleJoint, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.DT_B_muscleJoint, axis), 0.0)
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.DT_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_B_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.DT_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_B_muscleTip, self.objectDirectionMenu_value))

            # 设置拉伸因子
            cmds.setAttr("{0}.translate{1}".format(self.DT_B_muscleTip, self.objectDirectionMenu_value), restLength_LD_B * self.stretchFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.DT_B_muscleJoint, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.DT_B_muscleJoint, axis), yzStretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.DT_B_muscleJoint, axis), stretchOffset[index])
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.DT_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_B_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.DT_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_B_muscleTip, self.objectDirectionMenu_value))

            # 设置压缩因子
            cmds.setAttr("{0}.translate{1}".format(self.DT_B_muscleTip, self.objectDirectionMenu_value), restLength_LD_B * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.DT_B_muscleJoint, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.DT_B_muscleJoint, axis), yzSquashScale)
                cmds.setAttr("{0}.translate{1}".format(self.DT_B_muscleJoint, axis), compressionOffset[index])
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.DT_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_B_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.DT_B_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_B_muscleTip, self.objectDirectionMenu_value))
            
            # 恢复原始长度
            cmds.setAttr("{0}.translate{1}".format(self.DT_B_muscleTip, self.objectDirectionMenu_value), restLength_LD_B)



    def addSDK_C(self, stretchOffset=None, compressionOffset=None):
        self.stretchFactor = float(cmds.textField(self.ui_instance.stretchField, query=True, text=True))
        self.compressionFactor = float(cmds.textField(self.ui_instance.compressionField, query=True, text=True))
        yzSquashScale = math.sqrt(1.0 / self.compressionFactor)
        yzStretchScale = math.sqrt(1.0 / self.stretchFactor)

        if stretchOffset is None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset is None:
            compressionOffset = [0.0, 0.0, 0.0]

        restLength_DT_C = cmds.getAttr("{0}.translate{1}".format(self.DT_C_muscleTip, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            # 处理横向部分
            cmds.setAttr("{0}.scale{1}".format(self.DT_C_muscleJoint, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.DT_C_muscleJoint, axis), 0.0)
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.DT_C_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_C_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.DT_C_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_C_muscleTip, self.objectDirectionMenu_value))

            # 设置拉伸因子
            cmds.setAttr("{0}.translate{1}".format(self.DT_C_muscleTip, self.objectDirectionMenu_value), restLength_DT_C * self.stretchFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.DT_C_muscleJoint, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.DT_C_muscleJoint, axis), yzStretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.DT_C_muscleJoint, axis), stretchOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.DT_C_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_C_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.DT_C_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_C_muscleTip, self.objectDirectionMenu_value))

            # 设置压缩因子
            cmds.setAttr("{0}.translate{1}".format(self.DT_C_muscleTip, self.objectDirectionMenu_value), restLength_DT_C * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.DT_C_muscleJoint, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.DT_C_muscleJoint, axis), yzSquashScale)
                cmds.setAttr("{0}.translate{1}".format(self.DT_C_muscleJoint, axis), compressionOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.DT_C_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_C_muscleTip, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.DT_C_muscleJoint, axis),
                                currentDriver="{0}.translate{1}".format(self.DT_C_muscleTip, self.objectDirectionMenu_value))

            # 恢复原始长度
            cmds.setAttr("{0}.translate{1}".format(self.DT_C_muscleTip, self.objectDirectionMenu_value), restLength_DT_C)



    def muscleJointLib(self, *args):
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)

        self.DT_A_muscleOrigin = "{0}_muscleOrigin_DeltoidMuscle_A".format(self.L_R_value)
        self.DT_A_muscleInsertion = "{0}_muscleInsertion_DeltoidMuscle_A".format(self.L_R_value)

        self.DT_B_muscleOrigin = "{0}_muscleOrigin_DeltoidMuscle_B".format(self.L_R_value)
        self.DT_B_muscleInsertion = "{0}_muscleInsertion_DeltoidMuscle_B".format(self.L_R_value)

        self.DT_C_muscleOrigin = "{0}_muscleOrigin_DeltoidMuscle_C".format(self.L_R_value)
        self.DT_C_muscleInsertion = "{0}_muscleInsertion_DeltoidMuscle_C".format(self.L_R_value)

        self.DT_A_muscleBase = "{0}_muscleBase_DeltoidMuscle_A".format(self.L_R_value)
        self.DT_B_muscleBase = "{0}_muscleBase_DeltoidMuscle_B".format(self.L_R_value)
        self.DT_C_muscleBase = "{0}_muscleBase_DeltoidMuscle_C".format(self.L_R_value)

        self.DT_A_muscleDriver = "{0}_muscleDriver_DeltoidMuscle_A".format(self.L_R_value)
        self.DT_B_muscleDriver = "{0}_muscleDriver_DeltoidMuscle_B".format(self.L_R_value)
        self.DT_C_muscleDriver = "{0}_muscleDriver_DeltoidMuscle_C".format(self.L_R_value)

        self.DT_A_muscleOffset = "{0}_muscleOffset_DeltoidMuscle_A".format(self.L_R_value)
        self.DT_B_muscleOffset = "{0}_muscleOffset_DeltoidMuscle_B".format(self.L_R_value)
        self.DT_C_muscleOffset = "{0}_muscleOffset_DeltoidMuscle_C".format(self.L_R_value)

        self.DT_A_muscleJoint = "{0}_muscleJoint_DeltoidMuscle_A".format(self.L_R_value)
        self.DT_B_muscleJoint = "{0}_muscleJoint_DeltoidMuscle_B".format(self.L_R_value)
        self.DT_C_muscleJoint = "{0}_muscleJoint_DeltoidMuscle_C".format(self.L_R_value)

        self.DT_A_muscleTip = "{0}_muscleTip_DeltoidMuscle_A".format(self.L_R_value)
        self.DT_B_muscleTip = "{0}_muscleTip_DeltoidMuscle_B".format(self.L_R_value)
        self.DT_C_muscleTip = "{0}_muscleTip_DeltoidMuscle_C".format(self.L_R_value)



    def delete(self, *args):
        self.muscleJointLib()

        joints_to_delete = [
            self.DT_A_muscleOrigin,
            self.DT_A_muscleInsertion,
            self.DT_A_muscleTip,
            self.DT_A_muscleBase,
            self.DT_A_muscleDriver,
            self.DT_A_muscleOffset,
            self.DT_A_muscleJoint,
            self.DT_B_muscleOrigin,
            self.DT_B_muscleInsertion,
            self.DT_B_muscleTip,
            self.DT_B_muscleBase,
            self.DT_B_muscleDriver,
            self.DT_B_muscleOffset,
            self.DT_B_muscleJoint,
            self.DT_C_muscleOrigin,
            self.DT_C_muscleInsertion,
            self.DT_C_muscleTip,
            self.DT_C_muscleBase,
            self.DT_C_muscleDriver,
            self.DT_C_muscleOffset,
            self.DT_C_muscleJoint
        ]

        for i in joints_to_delete:
            if cmds.objExists(i):
                cmds.delete(i)



    def joint_exists(self, joint_name):
        return cmds.ls(joint_name, type="joint")

