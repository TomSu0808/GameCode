import sys
sys.path.insert(0, r"G:\Utah EAE\StudyProject\SelfStudy\RiggingClassStudy\MyWorks\JointBasedMucleDeformation\Code\Complete\MuscleJointCode")  

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



class LatissimusDorsiMuscleGRP(object):
    
    def __init__ (self, ui_instance):

        self.ui_instance = ui_instance

        self.compressionFactor = 0.5
        self.stretchFactor = 2.0

        self.neck = "neck_01"
        self.head = "head"
        self.back_01 = "back1"
        self.back_02 = "back2"
        self.back_03 = "back3"
        self.twistJoint_01 = None
        self.twistJoint_02 = None
        self.scapulaRoot = None
        self.upperArm = None
        self.acromion = None
        self.inferiorAngle = None

        self.AllJoints_LD_A = []
        self.AllJoints_LD_B = []
        self.AllJoints_TerasMajor = []
        self.AscendingAllJoints = []

        self.axisValue_LD_A = []
        self.axisValue_LD_B = []
        self.axisValue_TerasMajor = []

        self.originAttachObj = None
        self.insertionAttachObj = None
    


    # create LatissimusDorsi A joints
    def createLatissimusDorsiJoints_A(self):

        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)

        self.LD_A_start_joint = cmds.textFieldButtonGrp(self.ui_instance.origin_A, q = True, text = True)
        if not self.LD_A_start_joint.strip():
            self.LD_A_start_joint = self.back_01
        print("LD start is", self.LD_A_start_joint)
        
        self.twistJoint_01 = "upperarm_{0}_TwistJoint_001".format(self.L_R_value)
        self.twistJoint_02 = "upperarm_{0}_TwistJoint_002".format(self.L_R_value)
        self.scapulaRoot = "{0}_ScapulaRoot".format(self.L_R_value)
        self.upperArm = "upperarm_{0}".format(self.L_R_value)
        self.acromion = "{0}_Acromion".format(self.L_R_value)
        self.inferiorAngle = "{0}_InferiorAngle".format(self.L_R_value)

        muscle_origin_joint_name = "{0}_muscleOrigin_LatissimusDorsi_A".format(self.L_R_value)
        muscle_insertion_joint_name = "{0}_muscleInsertion_LatissimusDorsi_A".format(self.L_R_value)

        if self.joint_exists(muscle_origin_joint_name) or self.joint_exists(muscle_insertion_joint_name):
            print("LD A Joints Already Exist !!!")
            return None

        print("Generating LD A Joints")

        cmds.select(clear = True)
        self.muscleOrigin_joint_LD_A = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "LatissimusDorsi_A")
        
        # calculus origin joint position
        LD_A_startPosition = om.MVector(cmds.xform(self.LD_A_start_joint, t = True, ws = True, q = True))
        cmds.xform(self.muscleOrigin_joint_LD_A, t = LD_A_startPosition, ws = True)

        cmds.select(self.muscleOrigin_joint_LD_A)

        # duplicate a new joint call insertion joint
        self.muscleInsertion_joint_LD_A = cmds.duplicate(self.muscleOrigin_joint_LD_A, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "LatissimusDorsi_A")[0]

        # get LD_A_end start and end joint Position
        self.LD_A_end_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_A, q = True, text = True)
        if not self.LD_A_end_joint.strip():
            self.LD_A_end_joint = self.twistJoint_02

        print("LD end is", self.LD_A_end_joint)
  
        LD_A_end_joint_startPosition = om.MVector(cmds.xform(self.twistJoint_01, t = True, ws = True, q = True))
        LD_A_end_joint_endPosition = om.MVector(cmds.xform(self.LD_A_end_joint, t = True, ws = True, q = True))

        # get decending end joint Position
        LD_A_end_joint_finalPosition = (LD_A_end_joint_endPosition - LD_A_end_joint_startPosition) * 2.1 / 5.0 + LD_A_end_joint_startPosition
        cmds.xform(self.muscleInsertion_joint_LD_A, t = LD_A_end_joint_finalPosition, ws = True)

        cmds.select(cl = True)

        # create muscle base
        self.muscleBase_joint_LD_A = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "LatissimusDorsi_A")
        cmds.select(cl = True)
        # create muscle tip
        self.muscleTip_joint_LD_A = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "LatissimusDorsi_A")
        cmds.select(cl = True)
        # create muscle driver and it child
        self.muscleDriver_joint_LD_A = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "LatissimusDorsi_A")
        self.muscleOffset_joint_LD_A = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "LatissimusDorsi_A")
        self.muscleJoint_joint_LD_A = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "LatissimusDorsi_A")
        cmds.select(cl = True)

        # move muscle base to correct position and get it rotation
        self.get_muscleOrigin_joint_position_LD_A = om.MVector(cmds.xform(self.muscleOrigin_joint_LD_A, t = True, ws = True, q = True))
        self.get_muscleOrigin_joint_rotation_LD_A = om.MVector(cmds.xform(self.muscleOrigin_joint_LD_A, ro = True, ws = True, q = True))
        cmds.xform(self.muscleBase_joint_LD_A, t = self.get_muscleOrigin_joint_position_LD_A, ws = True)
        cmds.xform(self.muscleBase_joint_LD_A, ro = self.get_muscleOrigin_joint_rotation_LD_A, ws = True)
        
        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint LD A position
        
        self.get_muscleInsertion_joint_position_LD_A = om.MVector(cmds.xform(self.muscleInsertion_joint_LD_A, t = True, ws = True, q = True))

        muscleDriver_joint_finalPosition_LD_A = (self.get_muscleOrigin_joint_position_LD_A + self.get_muscleInsertion_joint_position_LD_A) * 0.5
        cmds.xform(self.muscleDriver_joint_LD_A, t = muscleDriver_joint_finalPosition_LD_A, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.muscleTip_joint_LD_A, t = self.get_muscleInsertion_joint_position_LD_A, ws = True)

        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.muscleTip_joint_LD_A, apply=True, rotate=True)
        cmds.parent(self.muscleTip_joint_LD_A, self.muscleBase_joint_LD_A)

        cmds.joint(self.muscleBase_joint_LD_A, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        
        # cmds.parent(self.muscleTip_joint_LD_A, self.muscleBase_joint_LD_A, world=True)

        self.get_muscleBase_joint_rotation_LD_A = om.MVector(cmds.xform(self.muscleBase_joint_LD_A, ro = True, ws = True, q = True))
        cmds.xform(self.muscleTip_joint_LD_A, ro = self.get_muscleBase_joint_rotation_LD_A, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.muscleDriver_joint_LD_A, ro = self.get_muscleBase_joint_rotation_LD_A, ws = True)
        cmds.xform(self.muscleOffset_joint_LD_A, ro = self.get_muscleBase_joint_rotation_LD_A, ws = True)
        cmds.xform(self.muscleJoint_joint_LD_A, ro = self.get_muscleBase_joint_rotation_LD_A, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.muscleOrigin_joint_LD_A, apply=True, rotate=True)
        cmds.makeIdentity(self.muscleInsertion_joint_LD_A, apply=True, rotate=True)
        cmds.makeIdentity(self.muscleDriver_joint_LD_A, apply=True, rotate=True)

        # parent joints
        cmds.parent(self.muscleOrigin_joint_LD_A, self.back_01)
        cmds.parent(self.muscleInsertion_joint_LD_A, self.twistJoint_02)
        cmds.parent(self.muscleBase_joint_LD_A, self.muscleOrigin_joint_LD_A)
        cmds.parent(self.muscleDriver_joint_LD_A, self.muscleBase_joint_LD_A)

        # pass joints date to __init__
        self.AllJoints_LD_A.extend([self.muscleOrigin_joint_LD_A, self.muscleInsertion_joint_LD_A, self.muscleBase_joint_LD_A, self.muscleTip_joint_LD_A,
                            self.muscleDriver_joint_LD_A, self.muscleOffset_joint_LD_A, self.muscleJoint_joint_LD_A])

        print("Compelete Generating LD A Joints")

        # update joints color
        orange_color_index = 17

        # # Function to update joint color
        def set_joint_color(joint, color_index):
            
            cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
            cmds.setAttr("{0}.overrideColor".format(joint), color_index)

        for joint in self.AllJoints_LD_A:
            set_joint_color(joint, orange_color_index)

        return True
        


    def createLatissimusDorsiConstraint_A(self):

        result = self.createLatissimusDorsiJoints_A()
        if result == None:
            print("None")
            return None
        
        if result == True:
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.muscleInsertion_joint_LD_A, self.muscleTip_joint_LD_A, maintainOffset = False,
                                weight = 1)

            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_LD_A = cmds.pointConstraint(self.muscleBase_joint_LD_A, self.muscleTip_joint_LD_A, self.muscleDriver_joint_LD_A, maintainOffset = True,
                                weight=1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_LD_A = cmds.aimConstraint(self.muscleInsertion_joint_LD_A, self.muscleBase_joint_LD_A,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.back_01,
                                                        worldUpVector = self.upAixs)

            self.axisValue_LD_A.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_LD_A, self.mainAimConstraint_LD_A])
            
            print("Compelete LD A Constraint")
            self.addSDK_LD_A()
            print("Compelete LD A Set SDK")

            

    # create LatissimusDorsi_B joints
    def createLatissimusDorsiJoints_B(self):
            self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)
            
            self.LD_start_joint_B = cmds.textFieldButtonGrp(self.ui_instance.origin_B, q = True, text = True)
            if not self.LD_start_joint_B.strip():
                self.LD_start_joint_B = "back2"

            self.twistJoint_01 = "upperarm_{0}_TwistJoint_001".format(self.L_R_value)
            self.twistJoint_02 = "upperarm_{0}_TwistJoint_002".format(self.L_R_value)
            self.scapulaRoot = "{0}_ScapulaRoot".format(self.L_R_value)
            self.upperArm = "upperarm_{0}".format(self.L_R_value)
            self.acromion = "{0}_Acromion".format(self.L_R_value)
            self.inferiorAngle = "{0}_InferiorAngle".format(self.L_R_value)
    
            cmds.select(clear = True)
            
            muscle_origin_joint_name = "{0}_muscleOrigin_LatissimusDorsi_B".format(self.L_R_value)
            muscle_insertion_joint_name = "{0}_muscleInsertion_LatissimusDorsi_B".format(self.L_R_value)

            if self.joint_exists(muscle_origin_joint_name) or self.joint_exists(muscle_insertion_joint_name):
                print("LatissimusDorsiMuscle_B Already Exist !!!")
                return None

            print("Generating LatissimusDorsi B Joints")
            self.muscleOrigin_joint_LD_B = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "LatissimusDorsi_B")

            LD_B_start_joint_position = om.MVector(cmds.xform(self.back_02, t = True, ws = True, q = True))
            # final_position_list_A = [decending_start_joint_finalPosition.x, decending_start_joint_finalPosition.y, decending_start_joint_finalPosition.z]

            cmds.xform(self.muscleOrigin_joint_LD_B, t = LD_B_start_joint_position, ws = True)

            cmds.select(self.muscleOrigin_joint_LD_B)

            # duplicate a new joint call insertion joint
            self.muscleInsertion_joint_LD_B = cmds.duplicate(self.muscleOrigin_joint_LD_B, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "LatissimusDorsi_B")[0]
            
            # get twist joint rotation and passing it to muscle insertion joint
            get_twist_rotation_value = cmds.xform(self.twistJoint_01, ro = True, ws = True, q = True)
            cmds.xform(self.muscleInsertion_joint_LD_B, ro = get_twist_rotation_value, ws = True)

            # get Insertion end start and end joint Position
            self.LD_insertion_B_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_B, q = True, text = True)
            if not self.LD_insertion_B_joint.strip():
                self.LD_insertion_B_joint = self.twistJoint_01

            LD_B_insertion_joint_startPosition = om.MVector(cmds.xform(self.LD_insertion_B_joint, t = True, ws = True, q = True))
            LD_B_insertion_joint_endPosition = om.MVector(cmds.xform(self.twistJoint_02, t = True, ws = True, q = True))

            # get LD B end joint Position
            LD_B_insertion_joint_finalPosition = (LD_B_insertion_joint_endPosition - LD_B_insertion_joint_startPosition) * 2.3 / 5.0 + LD_B_insertion_joint_startPosition
            cmds.xform(self.muscleInsertion_joint_LD_B, t = LD_B_insertion_joint_finalPosition, ws = True)

            cmds.select(cl = True)

            # create muscle base
            self.muscleBase_joint_LD_B = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "LatissimusDorsi_B")
            cmds.select(cl = True)
            # create muscle tip
            self.muscleTip_joint_LD_B = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "LatissimusDorsi_B")
            cmds.select(cl = True)
            # create muscle driver and it child
            self.muscleDriver_joint_LD_B = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "LatissimusDorsi_B")
            self.muscleOffset_joint_LD_B = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "LatissimusDorsi_B")
            self.muscleJoint_joint_LD_B = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "LatissimusDorsi_B")
            cmds.select(cl = True)

            # move muscle base to correct position and get it rotation
            get_muscleOrigin_joint_LD_B_position = om.MVector(cmds.xform(self.muscleOrigin_joint_LD_B, t = True, ws = True, q = True))
            get_muscleOrigin_joint_LD_B_rotation = om.MVector(cmds.xform(self.muscleOrigin_joint_LD_B, ro = True, ws = True, q = True))
            cmds.xform(self.muscleBase_joint_LD_B, t = get_muscleOrigin_joint_LD_B_position, ws = True)
            cmds.xform(self.muscleBase_joint_LD_B, ro = get_muscleOrigin_joint_LD_B_rotation, ws = True)

            # move muscle driver and it child to correct position
                # get muscle Origin and Insertion joint decending position
            get_muscleInsertion_joint_LD_B_position = om.MVector(cmds.xform(self.muscleInsertion_joint_LD_B, t = True, ws = True, q = True))

            muscleDriver_joint_LD_B_finalPosition = (get_muscleOrigin_joint_LD_B_position - get_muscleInsertion_joint_LD_B_position) * 4 / 5.0 + get_muscleInsertion_joint_LD_B_position
            cmds.xform(self.muscleDriver_joint_LD_B, t = muscleDriver_joint_LD_B_finalPosition, ws = True)

            # move tip joint to correct position and rotation
            cmds.xform(self.muscleTip_joint_LD_B, t = get_muscleInsertion_joint_LD_B_position, ws = True)

            # use joint orient get muscle base rotation value
            cmds.makeIdentity(self.muscleDriver_joint_LD_B, apply=True, rotate=True)
            cmds.parent(self.muscleDriver_joint_LD_B, self.muscleBase_joint_LD_B)

            cmds.joint(self.muscleBase_joint_LD_B, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                        zeroScaleOrient = True)
            
            # cmds.parent(self.muscleTip_joint_LD_B, self.muscleBase_joint_LD_B, world=True)

            self.get_muscleBase_joint_rotation_LD_B = om.MVector(cmds.xform(self.muscleBase_joint_LD_B, ro = True, ws = True, q = True))
            cmds.xform(self.muscleTip_joint_LD_B, ro = self.get_muscleBase_joint_rotation_LD_B, ws = True)

            # apply muscle base rotation value to muscle driver and it child
            cmds.xform(self.muscleDriver_joint_LD_B, ro = self.get_muscleBase_joint_rotation_LD_B, ws = True)
            cmds.xform(self.muscleOffset_joint_LD_B, ro = self.get_muscleBase_joint_rotation_LD_B, ws = True)
            cmds.xform(self.muscleJoint_joint_LD_B, ro = self.get_muscleBase_joint_rotation_LD_B, ws = True)

            # clear rotation values
            cmds.makeIdentity(self.muscleOrigin_joint_LD_B, apply=True, rotate=True)
            cmds.makeIdentity(self.muscleInsertion_joint_LD_B, apply=True, rotate=True)
            cmds.makeIdentity(self.muscleDriver_joint_LD_B, apply=True, rotate=True)

            # parent joints
            cmds.parent(self.muscleOrigin_joint_LD_B, self.back_02)
            cmds.parent(self.muscleInsertion_joint_LD_B, self.twistJoint_02)
            cmds.parent(self.muscleBase_joint_LD_B, self.muscleOrigin_joint_LD_B)
            cmds.parent(self.muscleTip_joint_LD_B, self.muscleBase_joint_LD_B)

            # pass joints date to __init__
            self.AllJoints_LD_B.extend([self.muscleOrigin_joint_LD_B, self.muscleInsertion_joint_LD_B, self.muscleBase_joint_LD_B, self.muscleTip_joint_LD_B,
                                self.muscleDriver_joint_LD_B, self.muscleOffset_joint_LD_B, self.muscleJoint_joint_LD_B])

            print("Complete Generating LatissimusDorsi B Joints")

            # update joints color
            orange_color_index = 17

            # # Function to update joint color
            def set_joint_color(joint, color_index):
                
                cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
                cmds.setAttr("{0}.overrideColor".format(joint), color_index)

            for joint in self.AllJoints_LD_B:
                set_joint_color(joint, orange_color_index)

            return True



    def createLatissimusDorsiConstraint_B(self):
        
        result = self.createLatissimusDorsiJoints_B()
        if result == None:
            return None
        
        if result == True:
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.muscleInsertion_joint_LD_B, self.muscleTip_joint_LD_B, maintainOffset = False,
                                weight = 1)

            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_LD_B = cmds.pointConstraint(self.muscleBase_joint_LD_B, self.muscleTip_joint_LD_B, self.muscleDriver_joint_LD_B, maintainOffset = True,
                                weight=1)

            # parent constraint neck, head and muscle origin
            # cmds.parentConstraint(self.neck, self.head, self.muscleBase_joint_decending, maintainOffset = True, weight = 1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_LD_B = cmds.aimConstraint(self.muscleInsertion_joint_LD_B, self.muscleBase_joint_LD_B,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.back_02,
                                                        worldUpVector = self.upAixs)

            self.axisValue_LD_B.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_LD_B, self.mainAimConstraint_LD_B])
            print("Compelete LD_B Constraint")
            self.addSDK_LD_B()
            print("Compelete LD_B Set SDK")


    # create Teras Major joints
    def createTerasMajorJoints(self):
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)
        self.TM_start_joint = cmds.textFieldButtonGrp(self.ui_instance.origin_C, q = True, text = True)
        if not self.TM_start_joint.strip():
            self.TM_start_joint = self.inferiorAngle

        self.twistJoint_01 = "upperarm_{0}_TwistJoint_001".format(self.L_R_value)
        self.twistJoint_02 = "upperarm_{0}_TwistJoint_002".format(self.L_R_value)
        self.scapulaRoot = "{0}_ScapulaRoot".format(self.L_R_value)
        self.upperArm = "upperarm_{0}".format(self.L_R_value)
        self.acromion = "{0}_Acromion".format(self.L_R_value)
        self.inferiorAngle = "{0}_InferiorAngle".format(self.L_R_value)

        cmds.select(clear = True)

        muscle_origin_joint_name = "{0}_muscleOrigin_TerasMajor".format(self.L_R_value)
        muscle_insertion_joint_name = "{0}_muscleInsertion_TerasMajor".format(self.L_R_value)

        if self.joint_exists(muscle_origin_joint_name) or self.joint_exists(muscle_insertion_joint_name):
            print("TerasMajor Joints Already Exist !!!")
            return None
        
        print("Generating TerasMajor Joint")

        self.muscleOrigin_joint_TerasMajor = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "TerasMajor")

        # calculus origin joint position
        get_muscleOrigin_joint_TerasMajor_startPosition = om.MVector(cmds.xform(self.scapulaRoot, t = True, ws = True, q = True))
        get_muscleOrigin_joint_TerasMajor_endPosition = om.MVector(cmds.xform(self.TM_start_joint, t = True, ws = True, q = True))
        get_muscleOrigin_joint_TerasMajor_finalPosition = (get_muscleOrigin_joint_TerasMajor_endPosition - get_muscleOrigin_joint_TerasMajor_startPosition) * 3 / 4.0 + get_muscleOrigin_joint_TerasMajor_startPosition

        cmds.xform(self.muscleOrigin_joint_TerasMajor, t = get_muscleOrigin_joint_TerasMajor_finalPosition, ws = True )

        cmds.select(self.muscleOrigin_joint_TerasMajor)

        # duplicate a new joint call insertion joint
        self.muscleInsertion_joint_TerasMajor = cmds.duplicate(self.muscleOrigin_joint_TerasMajor, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "TerasMajor")[0]

        # get TerasMajor_end start and end joint Position
        self.TerasMajor_end_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_C, q = True, text = True)
        if not self.TerasMajor_end_joint.strip():
            self.TerasMajor_end_joint = "upperarm_{0}_TwistJoint_002".format(self.L_R_value)

        terasMajor_end_joint_startPosition = om.MVector(cmds.xform(self.twistJoint_01, t = True, ws = True, q = True))
        terasMajor_end_joint_endPosition = om.MVector(cmds.xform(self.TerasMajor_end_joint, t = True, ws = True, q = True))

        # get decending end joint Position
        terasMajor_end_joint_finalPosition = (terasMajor_end_joint_endPosition - terasMajor_end_joint_startPosition) * 1 / 2.0 + terasMajor_end_joint_startPosition
        cmds.xform(self.muscleInsertion_joint_TerasMajor, t = terasMajor_end_joint_finalPosition, ws = True)

        cmds.select(cl = True)

        # create muscle base
        self.muscleBase_joint_TerasMajor = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "TerasMajor")
        cmds.select(cl = True)
        # create muscle tip
        self.muscleTip_joint_TerasMajor = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "TerasMajor")
        cmds.select(cl = True)
        # create muscle driver and it child
        self.muscleDriver_joint_TerasMajor = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "TerasMajor")
        self.muscleOffset_joint_TerasMajor = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "TerasMajor")
        self.muscleJoint_joint_TerasMajor = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "TerasMajor")
        cmds.select(cl = True)

        # move muscle base to correct position and get it rotation
        self.get_muscleOrigin_joint_position_TerasMajor = om.MVector(cmds.xform(self.muscleOrigin_joint_TerasMajor, t = True, ws = True, q = True))
        self.get_muscleOrigin_joint_rotation_TerasMajor = om.MVector(cmds.xform(self.muscleOrigin_joint_TerasMajor, ro = True, ws = True, q = True))
        cmds.xform(self.muscleBase_joint_TerasMajor, t = self.get_muscleOrigin_joint_position_TerasMajor, ws = True)
        cmds.xform(self.muscleBase_joint_TerasMajor, ro = self.get_muscleOrigin_joint_rotation_TerasMajor, ws = True)

        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint TerasMajor position
        
        self.get_muscleInsertion_joint_position_TerasMajor = om.MVector(cmds.xform(self.muscleInsertion_joint_TerasMajor, t = True, ws = True, q = True))

        muscleDriver_joint_finalPosition_TerasMajor = (self.get_muscleOrigin_joint_position_TerasMajor + self.get_muscleInsertion_joint_position_TerasMajor) * 0.5
        cmds.xform(self.muscleDriver_joint_TerasMajor, t = muscleDriver_joint_finalPosition_TerasMajor, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.muscleTip_joint_TerasMajor, t = self.get_muscleInsertion_joint_position_TerasMajor, ws = True)

        
        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.muscleTip_joint_TerasMajor, apply=True, rotate=True)
        cmds.parent(self.muscleTip_joint_TerasMajor, self.muscleBase_joint_TerasMajor)
        
        cmds.joint(self.muscleBase_joint_TerasMajor, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        
        cmds.parent(self.muscleTip_joint_TerasMajor, self.muscleBase_joint_TerasMajor, world=True)

        self.get_muscleBase_joint_rotation_TerasMajor = om.MVector(cmds.xform(self.muscleBase_joint_TerasMajor, ro = True, ws = True, q = True))
        cmds.xform(self.muscleTip_joint_TerasMajor, ro = self.get_muscleBase_joint_rotation_TerasMajor, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.muscleDriver_joint_TerasMajor, ro = self.get_muscleBase_joint_rotation_TerasMajor, ws = True)
        cmds.xform(self.muscleOffset_joint_TerasMajor, ro = self.get_muscleBase_joint_rotation_TerasMajor, ws = True)
        cmds.xform(self.muscleJoint_joint_TerasMajor, ro = self.get_muscleBase_joint_rotation_TerasMajor, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.muscleOrigin_joint_TerasMajor, apply=True, rotate=True)
        cmds.makeIdentity(self.muscleInsertion_joint_TerasMajor, apply=True, rotate=True)
        cmds.makeIdentity(self.muscleDriver_joint_TerasMajor, apply=True, rotate=True)
        
        # parent joints
        cmds.parent(self.muscleOrigin_joint_TerasMajor, self.inferiorAngle)
        cmds.parent(self.muscleInsertion_joint_TerasMajor, self.twistJoint_02)
        cmds.parent(self.muscleBase_joint_TerasMajor, self.muscleOrigin_joint_TerasMajor)
        cmds.parent(self.muscleDriver_joint_TerasMajor, self.muscleBase_joint_TerasMajor)
        cmds.parent(self.muscleTip_joint_TerasMajor, self.muscleBase_joint_TerasMajor)

        # pass joints date to __init__
        self.AllJoints_TerasMajor.extend([self.muscleOrigin_joint_TerasMajor, self.muscleInsertion_joint_TerasMajor, self.muscleBase_joint_TerasMajor, self.muscleTip_joint_TerasMajor,
                            self.muscleDriver_joint_TerasMajor, self.muscleOffset_joint_TerasMajor, self.muscleJoint_joint_TerasMajor])
        print("Compelete Generating TerasMajor")

        # update joints color
        orange_color_index = 17

        # # Function to update joint color
        def set_joint_color(joint, color_index):
            
            cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
            cmds.setAttr("{0}.overrideColor".format(joint), color_index)

        for joint in self.AllJoints_TerasMajor:
            set_joint_color(joint, orange_color_index)

        return True
            


    def createTerasMajorConstraint(self):
        
        result = self.createTerasMajorJoints()
        if result == None:
            print("Can't Generating Constraint because return None")
            return
        if result == True:
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.muscleInsertion_joint_TerasMajor, self.muscleTip_joint_TerasMajor, maintainOffset = False,
                                weight = 1)
            
            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_TerasMajor = cmds.pointConstraint(self.muscleBase_joint_TerasMajor, self.muscleTip_joint_TerasMajor, self.muscleDriver_joint_TerasMajor, maintainOffset = True,
                                weight=1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_TerasMajor = cmds.aimConstraint(self.muscleInsertion_joint_TerasMajor, self.muscleBase_joint_TerasMajor,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.back_03,
                                                        worldUpVector = self.upAixs)

            self.axisValue_TerasMajor.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_TerasMajor, self.mainAimConstraint_TerasMajor])
            
            print("Compelete TerasMajor Constraint")
            self.addSDK_TerasMajor()
            print("Compelete TerasMajor Set SDK")



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
        self.mainPointConstraint_A = cmds.pointConstraint(self.muscleBase_joint_LD_A, self.muscleTip_joint_LD_A, self.muscleDriver_joint_LD_A, maintainOffset = True,
                                            weight=1)

        self.mainAimConstraint_A = cmds.aimConstraint(self.muscleInsertion_joint_LD_A, self.muscleBase_joint_LD_A,
                                                    aimVector = self.dirAxis, upVector = self.upAixs,
                                                    worldUpType = "objectrotation", worldUpObject = self.back_01,
                                                    worldUpVector = self.upAixs)

        self.mainPointConstraint_B = cmds.pointConstraint(self.muscleBase_joint_LD_B, self.muscleTip_joint_LD_B, self.muscleDriver_joint_LD_B, maintainOffset = True,
                                weight=1)

        self.mainAimConstraint_B = cmds.aimConstraint(self.muscleInsertion_joint_LD_B, self.muscleBase_joint_LD_B,
                                            aimVector = self.dirAxis, upVector = self.upAixs,
                                            worldUpType = "objectrotation", worldUpObject = self.back_02,
                                            worldUpVector = self.upAixs)
        
        self.mainPointConstrain_C = cmds.pointConstraint(self.muscleBase_joint_TerasMajor, self.muscleTip_joint_TerasMajor, self.muscleDriver_joint_TerasMajor, maintainOffset = True,
                                            weight=1)

        self.mainAimConstraint_C = cmds.aimConstraint(self.muscleInsertion_joint_TerasMajor, self.muscleBase_joint_TerasMajor,
                                                    aimVector = self.dirAxis, upVector = self.upAixs,
                                                    worldUpType = "objectrotation", worldUpObject = self.back_03,
                                                    worldUpVector = self.upAixs)


 
        # set joints to templete
        joints =[ self.muscleOrigin_joint_LD_A, self.muscleInsertion_joint_LD_A, 
                 self.muscleOrigin_joint_LD_B, self.muscleInsertion_joint_LD_B,
                 self.muscleOrigin_joint_TerasMajor, self.muscleInsertion_joint_TerasMajor]
        for i in joints:
            cmds.setAttr("{0}.overrideEnabled".format(i), 1)
            cmds.setAttr("{0}.overrideDisplayType".format(i), 1)
        
        self.ptConstraintsTmp_A = []
        self.ptConstraintsTmp_B = []
        self.ptConstraintsTmp_C = []

        self.originLoc_A = createSpaceLocator(3.0, name="{0}_muscleOrigin_loc_A".format(self.L_R_value))
        self.originLoc_B = createSpaceLocator(3.0, name="{0}_muscleOrigin_loc_B".format(self.L_R_value))
        self.originLoc_C = createSpaceLocator(3.0, name="{0}_muscleOrigin_loc_C".format(self.L_R_value))

        if self.originAttachObj:
            cmds.parent(self.originLoc_A, self.originAttachObj)
            cmds.parent(self.originLoc_B, self.originAttachObj)
            cmds.parent(self.originLoc_C, self.originAttachObj)

        cmds.delete(cmds.pointConstraint(self.muscleOrigin_joint_LD_A, self.originLoc_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleOrigin_joint_LD_B, self.originLoc_B, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleOrigin_joint_TerasMajor, self.originLoc_C, mo=False, w=True))

        self.ptConstraintsTmp_A.append(cmds.pointConstraint(self.originLoc_A, self.muscleOrigin_joint_LD_A, mo=False, w=True)[0])
        self.ptConstraintsTmp_B.append(cmds.pointConstraint(self.originLoc_B, self.muscleOrigin_joint_LD_B, mo=False, w=True)[0])
        self.ptConstraintsTmp_C.append(cmds.pointConstraint(self.originLoc_C, self.muscleOrigin_joint_TerasMajor, mo=False, w=True)[0])

        self.insertionLoc_A = createSpaceLocator(3.0, name="{0}_muscleInsertion_loc_A".format(self.L_R_value))
        self.insertionLoc_B = createSpaceLocator(3.0, name="{0}_muscleInsertion_loc_B".format(self.L_R_value))
        self.insertionLoc_C = createSpaceLocator(3.0, name="{0}_muscleInsertion_loc_C".format(self.L_R_value))

        if self.insertionAttachObj:
            cmds.parent(self.insertionLoc_A, self.insertionAttachObj)
            cmds.parent(self.insertionLoc_B, self.insertionAttachObj)
            cmds.parent(self.insertionLoc_C, self.insertionAttachObj)

        def get_reverse_direction():
            return[-value for value in self.dirAxis]
        
        cmds.aimConstraint(self.insertionLoc_A, self.originLoc_A,
                           aimVector = self.dirAxis, upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        cmds.aimConstraint(self.insertionLoc_A, self.originLoc_A,
                           aimVector = get_reverse_direction(), upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)

        cmds.aimConstraint(self.insertionLoc_B, self.originLoc_B,
                           aimVector = self.dirAxis, upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        cmds.aimConstraint(self.insertionLoc_B, self.originLoc_B,
                           aimVector = get_reverse_direction(), upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)

        cmds.aimConstraint(self.insertionLoc_C, self.originLoc_C,
                           aimVector = self.dirAxis, upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        cmds.aimConstraint(self.insertionLoc_C, self.originLoc_C,
                           aimVector = get_reverse_direction(), upVector = self.upAixs,
                           worldUpType = "scene", offset = [0, 0, 0], weight = 1)
        
        cmds.delete(cmds.pointConstraint(self.muscleInsertion_joint_LD_A, self.insertionLoc_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleInsertion_joint_LD_B, self.insertionLoc_B, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleInsertion_joint_TerasMajor, self.insertionLoc_C, mo=False, w=True))

        self.ptConstraintsTmp_A.append(cmds.pointConstraint(self.insertionLoc_A, self.muscleInsertion_joint_LD_A, mo=False, w=True)[0])
        self.ptConstraintsTmp_B.append(cmds.pointConstraint(self.insertionLoc_B, self.muscleInsertion_joint_LD_B, mo=False, w=True)[0])
        self.ptConstraintsTmp_C.append(cmds.pointConstraint(self.insertionLoc_C, self.muscleInsertion_joint_TerasMajor, mo=False, w=True)[0])

        driverGrp_A = cmds.group(name="{0}_muscleCenter_A_grp".format(self.L_R_value), empty=True)
        driverGrp_B = cmds.group(name="{0}_muscleCenter_B_grp".format(self.L_R_value), empty=True)
        driverGrp_C = cmds.group(name="{0}_muscleCenter_C_grp".format(self.L_R_value), empty=True)

        self.centerLoc_A = createSpaceLocator(0.25, name="{0}_muscleCenter_loc".format(self.muscleOrigin_joint_LD_A))
        self.centerLoc_B = createSpaceLocator(0.25, name="{0}_muscleCenter_loc".format(self.muscleOrigin_joint_LD_B))
        self.centerLoc_C = createSpaceLocator(0.25, name="{0}_muscleCenter_loc".format(self.muscleOrigin_joint_TerasMajor))

        cmds.parent(self.centerLoc_A, driverGrp_A)
        cmds.parent(self.centerLoc_B, driverGrp_B)
        cmds.parent(self.centerLoc_C, driverGrp_C)
        
        
        cmds.delete(cmds.pointConstraint(self.muscleDriver_joint_LD_A, driverGrp_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleDriver_joint_LD_B, driverGrp_B, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleDriver_joint_TerasMajor, driverGrp_C, mo=False, w=True))

        cmds.parent(driverGrp_A, self.originLoc_A)
        cmds.parent(driverGrp_B, self.originLoc_B)
        cmds.parent(driverGrp_C, self.originLoc_C)

        
        cmds.pointConstraint(self.originLoc_A, self.insertionLoc_A, driverGrp_A, mo=True, w=True)
        cmds.pointConstraint(self.originLoc_B, self.insertionLoc_B, driverGrp_B, mo=True, w=True)
        cmds.pointConstraint(self.originLoc_C, self.insertionLoc_C, driverGrp_C, mo=True, w=True)

        cmds.setAttr("{0}.r".format(driverGrp_A), 0, 0, 0)
        cmds.setAttr("{0}.r".format(driverGrp_B), 0, 0, 0)
        cmds.setAttr("{0}.r".format(driverGrp_C), 0, 0, 0)

        cmds.delete(self.mainPointConstraint_LD_A)
        cmds.delete(self.mainPointConstraint_LD_B)
        cmds.delete(self.mainPointConstraint_TerasMajor)

        # constraint muscle joint A, C with B
        get_trapeziusMuscle_C = "{0}_muscleJoint_TrapeziusMuscle_C".format(self.L_R_value)
        if cmds.objExists(get_trapeziusMuscle_C) == True:
            print("Trapezius Joints Exist, now running the constraint !!!")

            cmds.pointConstraint(self.muscleJoint_joint_LD_A, get_trapeziusMuscle_C, self.muscleJoint_joint_LD_B, maintainOffset = True,
                                    weight = 1)

        self.ptConstraintsTmp_A.append(cmds.pointConstraint(self.centerLoc_A, self.muscleDriver_joint_LD_A, mo=False, w=True)[0])
        self.ptConstraintsTmp_B.append(cmds.pointConstraint(self.centerLoc_B, self.muscleDriver_joint_LD_B, mo=False, w=True)[0])
        self.ptConstraintsTmp_C.append(cmds.pointConstraint(self.centerLoc_C, self.muscleDriver_joint_TerasMajor, mo=False, w=True)[0])
        
        
  
    def update(self, *args):
        ###
        for ptConstraints_A in self.ptConstraintsTmp_A:
            if cmds.objExists(ptConstraints_A):
                cmds.delete(ptConstraints_A)

        for ptConstraints_B in self.ptConstraintsTmp_B:
            if cmds.objExists(ptConstraints_B):
                cmds.delete(ptConstraints_B)

        for ptConstraints_C in self.ptConstraintsTmp_C:
            if cmds.objExists(ptConstraints_C):
                cmds.delete(ptConstraints_C)

        ###
        for loc_LD_A in [self.originLoc_A, self.insertionLoc_A, self.centerLoc_A]:
            if cmds.objExists(loc_LD_A):
                cmds.delete(loc_LD_A)

        for loc_LD_B in [self.originLoc_B, self.insertionLoc_B, self.centerLoc_B]:
            if cmds.objExists(loc_LD_B):
                cmds.delete(loc_LD_B)

        for loc_TerasMajor in [self.originLoc_C, self.insertionLoc_C, self.centerLoc_C]:
            if cmds.objExists(loc_TerasMajor):
                cmds.delete(loc_TerasMajor)
        
        ###
        joints =[ self.muscleOrigin_joint_LD_A, self.muscleInsertion_joint_LD_A, 
                 self.muscleOrigin_joint_LD_B, self.muscleInsertion_joint_LD_B,
                 self.muscleOrigin_joint_TerasMajor, self.muscleInsertion_joint_TerasMajor]
        for i in joints:
            cmds.setAttr("{0}.overrideEnabled".format(i), 0)
            cmds.setAttr("{0}.overrideDisplayType".format(i), 0)

        cmds.delete(self.mainAimConstraint_LD_A)
        cmds.delete(self.mainAimConstraint_LD_B)
        cmds.delete(self.mainAimConstraint_TerasMajor)
        
        self.mainPointConstraint_LD_A = cmds.pointConstraint(self.muscleBase_joint_LD_A, self.muscleTip_joint_LD_A, self.muscleDriver_joint_LD_A,
                                                        mo=True, weight=1)

        self.mainPointConstraint_LD_B = cmds.pointConstraint(self.muscleBase_joint_LD_B, self.muscleTip_joint_LD_B, self.muscleDriver_joint_LD_B,
                                                        mo=True, weight=1)

        self.mainPointConstraint_TerasMajor = cmds.pointConstraint(self.muscleBase_joint_TerasMajor, self.muscleTip_joint_TerasMajor, self.muscleDriver_joint_TerasMajor,
                                                        mo=True, weight=1)

        cmds.delete(cmds.aimConstraint(self.muscleInsertion_joint_LD_A, self.muscleOrigin_joint_LD_A,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))

        cmds.delete(cmds.aimConstraint(self.muscleInsertion_joint_LD_B, self.muscleOrigin_joint_LD_B,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))
        
        cmds.delete(cmds.aimConstraint(self.muscleInsertion_joint_TerasMajor, self.muscleOrigin_joint_TerasMajor,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))

        self.mainAimConstraint_LD_A = cmds.aimConstraint(self.muscleInsertion_joint_LD_A, self.muscleBase_joint_LD_A,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.back_01,
                                                    worldUpVector=self.upAixs)

        self.mainAimConstraint_LD_B = cmds.aimConstraint(self.muscleInsertion_joint_LD_B, self.muscleBase_joint_LD_B,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.back_02,
                                                    worldUpVector=self.upAixs)
        
        self.mainAimConstraint_TerasMajor = cmds.aimConstraint(self.muscleInsertion_joint_TerasMajor, self.muscleBase_joint_TerasMajor,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.back_03,
                                                    worldUpVector=self.upAixs)

        animCurveNodes_LD_A = cmds.ls(cmds.listConnections(self.muscleJoint_joint_LD_A, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))

        animCurveNodes_LD_B = cmds.ls(cmds.listConnections(self.muscleJoint_joint_LD_B, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))
        
        animCurveNodes_TerasMajor = cmds.ls(cmds.listConnections(self.muscleJoint_joint_TerasMajor, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))
        
        cmds.delete(animCurveNodes_LD_A)
        cmds.delete(animCurveNodes_LD_B)
        cmds.delete(animCurveNodes_TerasMajor)

        self.addSDK_LD_A()
        self.addSDK_LD_B()
        self.addSDK_TerasMajor()
        


    def addSDK_LD_A(self, stretchOffset=None, compressionOffset=None):
        yzSquashScale = math.sqrt(1.0 / self.compressionFactor)
        yzStretchScale = math.sqrt(1.0 / self.stretchFactor)

        if stretchOffset is None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset is None:
            compressionOffset = [0.0, 0.0, 0.0]


        restLength_LD_A = cmds.getAttr("{0}.translate{1}".format(self.muscleTip_joint_LD_A, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            # 处理横向部分
            cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_LD_A, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_LD_A, axis), 0.0)

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_LD_A, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_A, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_LD_A, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_A, self.objectDirectionMenu_value))

            # 设置拉伸因子
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_LD_A, self.objectDirectionMenu_value), restLength_LD_A * self.stretchFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_LD_A, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_LD_A, axis), yzStretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_LD_A, axis), stretchOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_LD_A, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_A, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_LD_A, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_A, self.objectDirectionMenu_value))

            # 设置压缩因子
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_LD_A, self.objectDirectionMenu_value), restLength_LD_A * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_LD_A, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_LD_A, axis), yzSquashScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_LD_A, axis), compressionOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_LD_A, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_A, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_LD_A, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_A, self.objectDirectionMenu_value))

            # 恢复原始长度
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_LD_A, self.objectDirectionMenu_value), restLength_LD_A)



    def addSDK_LD_B(self, stretchOffset=None, compressionOffset=None):
        yzSquashScale = math.sqrt(1.0 / self.compressionFactor)
        yzStretchScale = math.sqrt(1.0 / self.stretchFactor)

        if stretchOffset is None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset is None:
            compressionOffset = [0.0, 0.0, 0.0]

        restLength_LD_B = cmds.getAttr("{0}.translate{1}".format(self.muscleTip_joint_LD_B, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            # 处理下降部分
            cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_LD_B, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_LD_B, axis), 0.0)

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_LD_B, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_B, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_LD_B, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_B, self.objectDirectionMenu_value))

            # 设置拉伸因子
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_LD_B, self.objectDirectionMenu_value), restLength_LD_B * self.stretchFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_LD_B, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_LD_B, axis), yzStretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_LD_B, axis), stretchOffset[index])
            
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_LD_B, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_B, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_LD_B, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_B, self.objectDirectionMenu_value))

            # 设置压缩因子
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_LD_B, self.objectDirectionMenu_value), restLength_LD_B * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_LD_B, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_LD_B, axis), yzSquashScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_LD_B, axis), compressionOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_LD_B, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_B, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_LD_B, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_LD_B, self.objectDirectionMenu_value))
            
            # 恢复原始长度
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_LD_B, self.objectDirectionMenu_value), restLength_LD_B)



    def addSDK_TerasMajor(self, stretchOffset=None, compressionOffset=None):
        yzSquashScale = math.sqrt(1.0 / self.compressionFactor)
        yzStretchScale = math.sqrt(1.0 / self.stretchFactor)

        if stretchOffset is None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset is None:
            compressionOffset = [0.0, 0.0, 0.0]


        restLength_TerasMajor = cmds.getAttr("{0}.translate{1}".format(self.muscleTip_joint_TerasMajor, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            # 处理横向部分
            cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_TerasMajor, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_TerasMajor, axis), 0.0)

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_TerasMajor, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_TerasMajor, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_TerasMajor, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_TerasMajor, self.objectDirectionMenu_value))

            # 设置拉伸因子
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_TerasMajor, self.objectDirectionMenu_value), restLength_TerasMajor * self.stretchFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_TerasMajor, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_TerasMajor, axis), yzStretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_TerasMajor, axis), stretchOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_TerasMajor, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_TerasMajor, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_TerasMajor, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_TerasMajor, self.objectDirectionMenu_value))

            # 设置压缩因子
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_TerasMajor, self.objectDirectionMenu_value), restLength_TerasMajor * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_TerasMajor, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_TerasMajor, axis), yzSquashScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_TerasMajor, axis), compressionOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_TerasMajor, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_TerasMajor, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_TerasMajor, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_TerasMajor, self.objectDirectionMenu_value))

            # 恢复原始长度
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_TerasMajor, self.objectDirectionMenu_value), restLength_TerasMajor)



    def muscleJointLib(self, *args):
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)

        self.muscleOrigin_joint_LD_A = "{0}_muscleOrigin_LatissimusDorsi_A".format(self.L_R_value)
        self.muscleInsertion_joint_LD_A = "{0}_muscleInsertion_LatissimusDorsi_A".format(self.L_R_value)

        self.muscleOrigin_joint_LD_B = "{0}_muscleOrigin_LatissimusDorsi_B".format(self.L_R_value)
        self.muscleInsertion_joint_LD_B = "{0}_muscleInsertion_LatissimusDorsi_B".format(self.L_R_value)

        self.muscleOrigin_joint_TerasMajor = "{0}_muscleOrigin_TerasMajor".format(self.L_R_value)
        self.muscleInsertion_joint_TerasMajor = "{0}_muscleInsertion_TerasMajor".format(self.L_R_value)

        self.muscleBase_joint_LD_A = "{0}_muscleBase_LatissimusDorsi_A".format(self.L_R_value)
        self.muscleBase_joint_LD_B = "{0}_muscleBase_LatissimusDorsi_B".format(self.L_R_value)
        self.muscleBase_joint_TerasMajor = "{0}_muscleBase_TerasMajor".format(self.L_R_value)

        self.muscleDriver_joint_LD_A = "{0}_muscleDriver_LatissimusDorsi_A".format(self.L_R_value)
        self.muscleDriver_joint_LD_B = "{0}_muscleDriver_LatissimusDorsi_B".format(self.L_R_value)
        self.muscleDriver_joint_TerasMajor = "{0}_muscleDriver_TerasMajor".format(self.L_R_value)

        self.muscleOffset_joint_LD_A = "{0}_muscleOffset_LatissimusDorsi_A".format(self.L_R_value)
        self.muscleOffset_joint_LD_B = "{0}_muscleOffset_LatissimusDorsi_B".format(self.L_R_value)
        self.muscleOffset_joint_TerasMajor = "{0}_muscleOffset_TerasMajor".format(self.L_R_value)

        self.muscleJoint_joint_LD_A = "{0}_muscleJoint_LatissimusDorsi_A".format(self.L_R_value)
        self.muscleJoint_joint_LD_B = "{0}_muscleJoint_LatissimusDorsi_B".format(self.L_R_value)
        self.muscleJoint_joint_TerasMajor = "{0}_muscleJoint_TerasMajor".format(self.L_R_value)

        self.muscleTip_joint_LD_A = "{0}_muscleTip_LatissimusDorsi_A".format(self.L_R_value)
        self.muscleTip_joint_LD_B = "{0}_muscleTip_LatissimusDorsi_B".format(self.L_R_value)
        self.muscleTip_joint_TerasMajor = "{0}_muscleTip_TerasMajor".format(self.L_R_value)



    def delete(self, *args):
        self.muscleJointLib()

        joints_to_delete = [
            self.muscleOrigin_joint_LD_A,
            self.muscleInsertion_joint_LD_A,
            self.muscleTip_joint_LD_A,
            self.muscleBase_joint_LD_A,
            self.muscleDriver_joint_LD_A,
            self.muscleOffset_joint_LD_A,
            self.muscleJoint_joint_LD_A,
            self.muscleOrigin_joint_LD_B,
            self.muscleInsertion_joint_LD_B,
            self.muscleTip_joint_LD_B,
            self.muscleBase_joint_LD_B,
            self.muscleDriver_joint_LD_B,
            self.muscleOffset_joint_LD_B,
            self.muscleJoint_joint_LD_B,
            self.muscleOrigin_joint_TerasMajor,
            self.muscleInsertion_joint_TerasMajor,
            self.muscleTip_joint_TerasMajor,
            self.muscleBase_joint_TerasMajor,
            self.muscleDriver_joint_TerasMajor,
            self.muscleOffset_joint_TerasMajor,
            self.muscleJoint_joint_TerasMajor
        ]

        for i in joints_to_delete:
            if cmds.objExists(i):
                cmds.delete(i)



    def joint_exists(self, joint_name):
        return cmds.ls(joint_name, type="joint")




