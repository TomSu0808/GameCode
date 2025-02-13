import logging
import json
import maya.cmds as cmds
import maya.api.OpenMaya as om
import math

logger = logging.getLogger(__name__)
fp = r"G:\Utah EAE\StudyProject\SelfStudy\RiggingClassStudy\MyWorks\JointBasedMucleDeformation\Code\allMuscle.json"

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



class TrapeziusMuscleGRP(object):
    
    def __init__(self, ui_instance):

        ### Lesson9 Test
        self.ui_instance = ui_instance
        # self.L_R_value = L_R_value
        ###


        self.neck = "neck_01"
        self.head = "head"
        self.back = "back3"
        self.clavicle = None
        self.upperArm = None
        self.acromion = None
        self.scapulaRoot = None

        self.DecendingAllJoints = []
        self.TraverseAllJoints = []
        self.AscendingAllJoints = []
        self.axisValueDecending = []
        self.axisValueTraverse = []
        self.axisValueAscending = []
        self.originAttachObj = None
        self.insertionAttachObj = None

        # Lesson9 Test
        self.trapeziusA = None
        self.trapeziusB = None
        self.trapeziusC = None



    # create decending joints
    def createDecendingJoints(self):

        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)
        if self.ui_instance and hasattr(self.ui_instance, 'origin_A'):
            self.decending_start_joint = cmds.textFieldButtonGrp(self.ui_instance.origin_A, q=True, text=True)
        else:
            self.decending_start_joint = self.neck

        self.clavicle = "clavicle_{0}".format(self.L_R_value)
        self.upperArm = "upperarm_{0}".format(self.L_R_value)
        # self.decending_start_joint = cmds.textFieldButtonGrp(self.ui_instance.origin_A, q = True, text = True)
        # if not self.decending_start_joint.strip():
        #     self.decending_start_joint = self.neck

        cmds.select(clear = True)
        
        muscle_origin_joint_name = "{0}_muscleOrigin_TrapeziusMuscle_A".format(self.L_R_value)
        muscle_insertion_joint_name = "{0}_muscleInsertion_TrapeziusMuscle_A".format(self.L_R_value)

        # if self.joint_exists(muscle_origin_joint_name) or self.joint_exists(muscle_insertion_joint_name):
        #     print("TrapeziusMuscle_A Already Exist !!!")
        #     return None

        print("Generating Decending Joints")

        self.muscleOrigin_joint_decending = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "TrapeziusMuscle_A")

        decending_start_joint_startPosition = om.MVector(cmds.xform(self.head, t = True, ws = True, q = True))
        decending_start_joint_endPosition = om.MVector(cmds.xform(self.decending_start_joint, t = True, ws = True, q = True))
        decending_start_joint_finalPosition = (decending_start_joint_startPosition + decending_start_joint_endPosition) * 0.5
        final_position_list_A = [decending_start_joint_finalPosition.x, decending_start_joint_finalPosition.y, decending_start_joint_finalPosition.z]

        cmds.xform(self.muscleOrigin_joint_decending, t = final_position_list_A, ws = True)

        cmds.select(self.muscleOrigin_joint_decending)

        # duplicate a new joint call insertion joint
        self.muscleInsertion_joint_decending = cmds.duplicate(self.muscleOrigin_joint_decending, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "TrapeziusMuscle_A")[0]
        
        # get clavicle joint rotation and get it to muscle insertion joint decending
        get_clavicle_rotation_value = cmds.xform(self.clavicle, ro = True, ws = True, q = True)
        cmds.xform(self.muscleInsertion_joint_decending, ro = get_clavicle_rotation_value, ws = True)

        # get decending_end start and end joint Position

        if self.ui_instance and hasattr(self.ui_instance, 'insertion_A'):
            self.decending_end_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_A_A, q=True, text=True)
        else:
            self.decending_end_joint = self.clavicle
        # self.decending_end_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_A, q = True, text = True)
        # if not self.decending_end_joint.strip():
        #     self.decending_end_joint = self.clavicle

        decending_end_joint_startPosition = om.MVector(cmds.xform(self.decending_end_joint, t = True, ws = True, q = True))
        decending_end_joint_endPosition = om.MVector(cmds.xform(self.upperArm, t = True, ws = True, q = True))

        # get decending end joint Position
        decending_end_joint_finalPosition = (decending_end_joint_endPosition - decending_end_joint_startPosition) * 5 / 6.0 + decending_end_joint_startPosition
        cmds.xform(self.muscleInsertion_joint_decending, t = decending_end_joint_finalPosition, ws = True)

        cmds.select(cl = True)

        # create muscle base
        self.muscleBase_joint_decending = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "TrapeziusMuscle_A")
        cmds.select(cl = True)
        # create muscle tip
        self.muscleTip_joint_decending = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "TrapeziusMuscle_A")
        cmds.select(cl = True)
        # create muscle driver and it child
        self.muscleDriver_joint_decending = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "TrapeziusMuscle_A")
        self.muscleOffset_joint_decending = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "TrapeziusMuscle_A")
        self.muscleJoint_joint_decending = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "TrapeziusMuscle_A")
        cmds.select(cl = True)


        # move muscle base to correct position and get it rotation
        self.get_muscleOrigin_joint_decending_position = om.MVector(cmds.xform(self.muscleOrigin_joint_decending, t = True, ws = True, q = True))
        self.get_muscleOrigin_joint_decending_rotation = om.MVector(cmds.xform(self.muscleOrigin_joint_decending, ro = True, ws = True, q = True))
        cmds.xform(self.muscleBase_joint_decending, t = self.get_muscleOrigin_joint_decending_position, ws = True)
        cmds.xform(self.muscleBase_joint_decending, ro = self.get_muscleOrigin_joint_decending_rotation, ws = True)

        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint decending position
        self.get_muscleInsertion_joint_decending_position = om.MVector(cmds.xform(self.muscleInsertion_joint_decending, t = True, ws = True, q = True))

        muscleDriver_joint_decending_finalPosition = (self.get_muscleOrigin_joint_decending_position + self.get_muscleInsertion_joint_decending_position) * 0.5
        cmds.xform(self.muscleDriver_joint_decending, t = muscleDriver_joint_decending_finalPosition, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.muscleTip_joint_decending, t = self.get_muscleInsertion_joint_decending_position, ws = True)

        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.muscleTip_joint_decending, apply=True, rotate=True)
        cmds.parent(self.muscleTip_joint_decending, self.muscleBase_joint_decending)

        cmds.joint(self.muscleBase_joint_decending, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        
        cmds.parent(self.muscleTip_joint_decending, self.muscleBase_joint_decending, world=True)

        self.get_muscleBase_joint_rotation_decending = om.MVector(cmds.xform(self.muscleBase_joint_decending, ro = True, ws = True, q = True))
        cmds.xform(self.muscleTip_joint_decending, ro = self.get_muscleBase_joint_rotation_decending, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.muscleDriver_joint_decending, ro = self.get_muscleBase_joint_rotation_decending, ws = True)
        cmds.xform(self.muscleOffset_joint_decending, ro = self.get_muscleBase_joint_rotation_decending, ws = True)
        cmds.xform(self.muscleJoint_joint_decending, ro = self.get_muscleBase_joint_rotation_decending, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.muscleOrigin_joint_decending, apply=True, rotate=True)
        cmds.makeIdentity(self.muscleInsertion_joint_decending, apply=True, rotate=True)
        cmds.makeIdentity(self.muscleDriver_joint_decending, apply=True, rotate=True)

        # parent joints
        cmds.parent(self.muscleOrigin_joint_decending, self.neck)
        cmds.parent(self.muscleInsertion_joint_decending, self.clavicle)
        cmds.parent(self.muscleBase_joint_decending, self.muscleOrigin_joint_decending)
        cmds.parent(self.muscleDriver_joint_decending, self.muscleBase_joint_decending)
        cmds.parent(self.muscleTip_joint_decending, self.muscleBase_joint_decending)

        # pass joints date to __init__
        self.DecendingAllJoints.extend([self.muscleOrigin_joint_decending, self.muscleInsertion_joint_decending, self.muscleBase_joint_decending, self.muscleTip_joint_decending,
                            self.muscleDriver_joint_decending, self.muscleOffset_joint_decending, self.muscleJoint_joint_decending])

        print("Complete Generating Decending Joints")

        # update joints color
        orange_color_index = 14

        # # Function to update joint color
        def set_joint_color(joint, color_index):
            
            cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
            cmds.setAttr("{0}.overrideColor".format(joint), color_index)

        for joint in self.DecendingAllJoints:
            set_joint_color(joint, orange_color_index)

        return True
        


    def createDecendingConstraint(self):
        
        result = self.createDecendingJoints()
        if result == None:
            return None
        
        if result == True:
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.muscleInsertion_joint_decending, self.muscleTip_joint_decending, maintainOffset = False,
                                weight = 1)

            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_decending = cmds.pointConstraint(self.muscleBase_joint_decending, self.muscleTip_joint_decending, self.muscleDriver_joint_decending, maintainOffset = True,
                                weight=1)

            # parent constraint neck, head and muscle origin
            # cmds.parentConstraint(self.neck, self.head, self.muscleBase_joint_decending, maintainOffset = True, weight = 1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_decending = cmds.aimConstraint(self.muscleInsertion_joint_decending, self.muscleBase_joint_decending,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.back,
                                                        worldUpVector = self.upAixs)

            self.axisValueDecending.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_decending, self.mainAimConstraint_decending])
            print("Compelete Decending Constraint")
            self.addSDK_Decending()
            print("Compelete Decending Set SDK")
            


    # create Traverse joints
    def createTraverseJoints(self):
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)
        self.acromion = "{0}_Acromion".format(self.L_R_value)
        self.scapulaRoot = "{0}_ScapulaRoot".format(self.L_R_value)

        self.traverse_start_joint = cmds.textFieldButtonGrp(self.ui_instance.origin_B, q = True, text = True)
        if not self.traverse_start_joint.strip():
            self.traverse_start_joint = "back3"

        muscle_origin_joint_name = "{0}_muscleOrigin_TrapeziusMuscle_B".format(self.L_R_value)
        muscle_insertion_joint_name = "{0}_muscleInsertion_TrapeziusMuscle_B".format(self.L_R_value)

        if self.joint_exists(muscle_origin_joint_name) or self.joint_exists(muscle_insertion_joint_name):
            print("Traverse Joints Already Exist !!!")
            return None

        print("Generating Traverse Joints")
        cmds.select(clear = True)
        self.muscleOrigin_joint_traverse = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "TrapeziusMuscle_B")

        # calculus origin joint position
        traverse_start_joint_startPosition = om.MVector(cmds.xform(self.neck, t = True, ws = True, q = True))
        traverse_start_joint_endPosition = om.MVector(cmds.xform(self.traverse_start_joint, t = True, ws = True, q = True))
        traverse_start_joint_finalPosition_001 = (traverse_start_joint_startPosition + traverse_start_joint_endPosition) * 0.5
        traverse_start_joint_finalPosition_002 = (traverse_start_joint_startPosition + traverse_start_joint_finalPosition_001) * 0.5
        final_position_list_traverse_A_002 = [traverse_start_joint_finalPosition_002.x, traverse_start_joint_finalPosition_002.y, traverse_start_joint_finalPosition_002.z]
        cmds.xform(self.muscleOrigin_joint_traverse, t = final_position_list_traverse_A_002, ws = True)

        cmds.select(self.muscleOrigin_joint_traverse)

        # duplicate a new joint call insertion joint
        self.muscleInsertion_joint_traverse = cmds.duplicate(self.muscleOrigin_joint_traverse, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "TrapeziusMuscle_B")[0]
        
        # get acromion joint rotation and get it to muscle insertion joint traverse
        get_acromion_rotation_value = cmds.xform(self.acromion, ro = True, ws = True, q = True)
        cmds.xform(self.muscleInsertion_joint_traverse, ro = get_acromion_rotation_value, ws = True)

        # get traverse_end start and end joint Position
        self.traverse_end_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_B, q = True, text = True)
        if not self.traverse_end_joint.strip():
            self.traverse_end_joint = "{0}_Acromion".format(self.L_R_value)

        traverse_end_joint_startPosition = om.MVector(cmds.xform(self.traverse_end_joint, t = True, ws = True, q = True))
        traverse_end_joint_endPosition = om.MVector(cmds.xform(self.scapulaRoot, t = True, ws = True, q = True))

        # get decending end joint Position
        traverse_end_joint_finalPosition = (traverse_end_joint_endPosition - traverse_end_joint_startPosition) * 1 / 4.0 + traverse_end_joint_startPosition
        cmds.xform(self.muscleInsertion_joint_traverse, t = traverse_end_joint_finalPosition, ws = True)

        cmds.select(cl = True)

        # create muscle base
        self.muscleBase_joint_traverse = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "TrapeziusMuscle_B")
        cmds.select(cl = True)
        # create muscle tip
        self.muscleTip_joint_traverse = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "TrapeziusMuscle_B")
        cmds.select(cl = True)
        # create muscle driver and it child
        self.muscleDriver_joint_traverse = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "TrapeziusMuscle_B")
        self.muscleOffset_joint_traverse = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "TrapeziusMuscle_B")
        self.muscleJoint_joint_traverse = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "TrapeziusMuscle_B")
        cmds.select(cl = True)

        # move muscle base to correct position and get it rotation
        self.get_muscleOrigin_joint_position_traverse = om.MVector(cmds.xform(self.muscleOrigin_joint_traverse, t = True, ws = True, q = True))
        self.get_muscleOrigin_joint_rotation_traverse = om.MVector(cmds.xform(self.muscleOrigin_joint_traverse, ro = True, ws = True, q = True))
        cmds.xform(self.muscleBase_joint_traverse, t = self.get_muscleOrigin_joint_position_traverse, ws = True)
        cmds.xform(self.muscleBase_joint_traverse, ro = self.get_muscleOrigin_joint_rotation_traverse, ws = True)

        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint traverse position
        
        self.get_muscleInsertion_joint_position_traverse = om.MVector(cmds.xform(self.muscleInsertion_joint_traverse, t = True, ws = True, q = True))

        muscleDriver_joint_finalPosition_traverse = (self.get_muscleOrigin_joint_position_traverse + self.get_muscleInsertion_joint_position_traverse) * 0.5
        cmds.xform(self.muscleDriver_joint_traverse, t = muscleDriver_joint_finalPosition_traverse, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.muscleTip_joint_traverse, t = self.get_muscleInsertion_joint_position_traverse, ws = True)

        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.muscleTip_joint_traverse, apply=True, rotate=True)
        cmds.parent(self.muscleTip_joint_traverse, self.muscleBase_joint_traverse)

        cmds.joint(self.muscleBase_joint_traverse, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        
        cmds.parent(self.muscleTip_joint_traverse, self.muscleBase_joint_traverse, world=True)

        self.get_muscleBase_joint_rotation_traverse = om.MVector(cmds.xform(self.muscleBase_joint_traverse, ro = True, ws = True, q = True))
        cmds.xform(self.muscleTip_joint_traverse, ro = self.get_muscleBase_joint_rotation_traverse, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.muscleDriver_joint_traverse, ro = self.get_muscleBase_joint_rotation_traverse, ws = True)
        cmds.xform(self.muscleOffset_joint_traverse, ro = self.get_muscleBase_joint_rotation_traverse, ws = True)
        cmds.xform(self.muscleJoint_joint_traverse, ro = self.get_muscleBase_joint_rotation_traverse, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.muscleOrigin_joint_traverse, apply=True, rotate=True)
        cmds.makeIdentity(self.muscleInsertion_joint_traverse, apply=True, rotate=True)
        cmds.makeIdentity(self.muscleDriver_joint_traverse, apply=True, rotate=True)

        # parent joints
        cmds.parent(self.muscleOrigin_joint_traverse, self.back)
        cmds.parent(self.muscleInsertion_joint_traverse, self.acromion)
        cmds.parent(self.muscleBase_joint_traverse, self.muscleOrigin_joint_traverse)
        cmds.parent(self.muscleDriver_joint_traverse, self.muscleBase_joint_traverse)
        cmds.parent(self.muscleTip_joint_traverse, self.muscleBase_joint_traverse)

        # pass joints date to __init__
        self.TraverseAllJoints.extend([self.muscleOrigin_joint_traverse, self.muscleInsertion_joint_traverse, self.muscleBase_joint_traverse, self.muscleTip_joint_traverse,
                            self.muscleDriver_joint_traverse, self.muscleOffset_joint_traverse, self.muscleJoint_joint_traverse])

        print("Compelete Generating Traverse Joints")

        # update joints color
        orange_color_index = 14

        # # Function to update joint color
        def set_joint_color(joint, color_index):
            
            cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
            cmds.setAttr("{0}.overrideColor".format(joint), color_index)

        for joint in self.TraverseAllJoints:
            set_joint_color(joint, orange_color_index)

        return True
    


    def createTraverseConstraint(self):

        result = self.createTraverseJoints()
        if result == None:
            return None
        
        if result == True:
            self.createTraverseJoints()
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.muscleInsertion_joint_traverse, self.muscleTip_joint_traverse, maintainOffset = False,
                                weight = 1)

            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_traverse = cmds.pointConstraint(self.muscleBase_joint_traverse, self.muscleTip_joint_traverse, self.muscleDriver_joint_traverse, maintainOffset = True,
                                weight=1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_traverse = cmds.aimConstraint(self.muscleInsertion_joint_traverse, self.muscleBase_joint_traverse,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.back,
                                                        worldUpVector = self.upAixs)

            self.axisValueTraverse.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_traverse, self.mainAimConstraint_traverse])
            print("Compelete Traverse Constraint")
            self.addSDK_Traverse()
            print("Compelete Traverse Set SDK")


    # create Ascending joints
    def createAscendingJoints(self):
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)
        self.ascending_start_joint = cmds.textFieldButtonGrp(self.ui_instance.origin_C, q = True, text = True)
        if not self.ascending_start_joint.strip():
            self.ascending_start_joint = "back3"

        cmds.select(clear = True)

        muscle_origin_joint_name = "{0}_muscleOrigin_TrapeziusMuscle_C".format(self.L_R_value)
        muscle_insertion_joint_name = "{0}_muscleInsertion_TrapeziusMuscle_C".format(self.L_R_value)

        if self.joint_exists(muscle_origin_joint_name) or self.joint_exists(muscle_insertion_joint_name):
            print("Ascending Joints Already Exist !!!")
            return None
        
        print("Generating TrapeziusMuscle_C")

        self.muscleOrigin_joint_ascending = cmds.joint(n = self.L_R_value + "_" + "muscleOrigin" + "_" + "TrapeziusMuscle_C")

        # calculus origin joint position
        get_muscleOrigin_joint_ascending_startPosition = om.MVector(cmds.xform(self.ascending_start_joint, t = True, ws = True, q = True))
        cmds.xform(self.muscleOrigin_joint_ascending, t = get_muscleOrigin_joint_ascending_startPosition, ws = True )

        cmds.select(self.muscleOrigin_joint_ascending)

        # duplicate a new joint call insertion joint
        self.muscleInsertion_joint_ascending = cmds.duplicate(self.muscleOrigin_joint_ascending, n = self.L_R_value + "_" + "muscleInsertion" + "_" + "TrapeziusMuscle_C")[0]
        
        # get acromion joint rotation and get it to muscle insertion joint ascending
        get_acromion_rotation_value = cmds.xform(self.acromion, ro = True, ws = True, q = True)
        cmds.xform(self.muscleInsertion_joint_ascending, ro = get_acromion_rotation_value, ws = True)

        # get ascending_end start and end joint Position
        self.ascending_end_joint = cmds.textFieldButtonGrp(self.ui_instance.insertion_C, q = True, text = True)
        if not self.ascending_end_joint.strip():
            self.ascending_end_joint = "{0}_Acromion".format(self.L_R_value)

        ascending_end_joint_startPosition = om.MVector(cmds.xform(self.ascending_end_joint, t = True, ws = True, q = True))
        ascending_end_joint_endPosition = om.MVector(cmds.xform(self.scapulaRoot, t = True, ws = True, q = True))

        # get decending end joint Position
        ascending_end_joint_finalPosition = (ascending_end_joint_endPosition - ascending_end_joint_startPosition) * 3 / 4.0 + ascending_end_joint_startPosition
        cmds.xform(self.muscleInsertion_joint_ascending, t = ascending_end_joint_finalPosition, ws = True)

        cmds.select(cl = True)

        # create muscle base
        self.muscleBase_joint_ascending = cmds.joint(n = self.L_R_value + "_" + "muscleBase" + "_" + "TrapeziusMuscle_C")
        cmds.select(cl = True)
        # create muscle tip
        self.muscleTip_joint_ascending = cmds.joint(n = self.L_R_value + "_" + "muscleTip" + "_" + "TrapeziusMuscle_C")
        cmds.select(cl = True)
        # create muscle driver and it child
        self.muscleDriver_joint_ascending = cmds.joint(n = self.L_R_value + "_" + "muscleDriver" + "_" + "TrapeziusMuscle_C")
        self.muscleOffset_joint_ascending = cmds.joint(n = self.L_R_value + "_" + "muscleOffset" + "_" + "TrapeziusMuscle_C")
        self.muscleJoint_joint_ascending = cmds.joint(n = self.L_R_value + "_" + "muscleJoint" + "_" + "TrapeziusMuscle_C")
        cmds.select(cl = True)

        # move muscle base to correct position and get it rotation
        self.get_muscleOrigin_joint_position_ascending = om.MVector(cmds.xform(self.muscleOrigin_joint_ascending, t = True, ws = True, q = True))
        self.get_muscleOrigin_joint_rotation_ascending = om.MVector(cmds.xform(self.muscleOrigin_joint_ascending, ro = True, ws = True, q = True))
        cmds.xform(self.muscleBase_joint_ascending, t = self.get_muscleOrigin_joint_position_ascending, ws = True)
        cmds.xform(self.muscleBase_joint_ascending, ro = self.get_muscleOrigin_joint_rotation_ascending, ws = True)

        # move muscle driver and it child to correct position
            # get muscle Origin and Insertion joint ascending position
        
        self.get_muscleInsertion_joint_position_ascending = om.MVector(cmds.xform(self.muscleInsertion_joint_ascending, t = True, ws = True, q = True))

        muscleDriver_joint_finalPosition_ascending = (self.get_muscleOrigin_joint_position_ascending + self.get_muscleInsertion_joint_position_ascending) * 0.5
        cmds.xform(self.muscleDriver_joint_ascending, t = muscleDriver_joint_finalPosition_ascending, ws = True)

        # move tip joint to correct position and rotation
        cmds.xform(self.muscleTip_joint_ascending, t = self.get_muscleInsertion_joint_position_ascending, ws = True)

        
        # use joint orient get muscle base rotation value
        cmds.makeIdentity(self.muscleTip_joint_ascending, apply=True, rotate=True)
        cmds.parent(self.muscleTip_joint_ascending, self.muscleBase_joint_ascending)
        
        cmds.joint(self.muscleBase_joint_ascending, edit = True, orientJoint = "xzy", secondaryAxisOrient = "yup", children = True,
                    zeroScaleOrient = True)
        
        cmds.parent(self.muscleTip_joint_ascending, self.muscleBase_joint_ascending, world=True)

        self.get_muscleBase_joint_rotation_ascending = om.MVector(cmds.xform(self.muscleBase_joint_ascending, ro = True, ws = True, q = True))
        cmds.xform(self.muscleTip_joint_ascending, ro = self.get_muscleBase_joint_rotation_ascending, ws = True)

        # apply muscle base rotation value to muscle driver and it child
        cmds.xform(self.muscleDriver_joint_ascending, ro = self.get_muscleBase_joint_rotation_ascending, ws = True)
        cmds.xform(self.muscleOffset_joint_ascending, ro = self.get_muscleBase_joint_rotation_ascending, ws = True)
        cmds.xform(self.muscleJoint_joint_ascending, ro = self.get_muscleBase_joint_rotation_ascending, ws = True)

        # clear rotation values
        cmds.makeIdentity(self.muscleOrigin_joint_ascending, apply=True, rotate=True)
        cmds.makeIdentity(self.muscleInsertion_joint_ascending, apply=True, rotate=True)
        cmds.makeIdentity(self.muscleDriver_joint_ascending, apply=True, rotate=True)
        
        # parent joints
        cmds.parent(self.muscleOrigin_joint_ascending, self.back)
        cmds.parent(self.muscleInsertion_joint_ascending, self.acromion)
        cmds.parent(self.muscleBase_joint_ascending, self.muscleOrigin_joint_ascending)
        cmds.parent(self.muscleDriver_joint_ascending, self.muscleBase_joint_ascending)
        cmds.parent(self.muscleTip_joint_ascending, self.muscleBase_joint_ascending)

        # pass joints date to __init__
        self.AscendingAllJoints.extend([self.muscleOrigin_joint_ascending, self.muscleInsertion_joint_ascending, self.muscleBase_joint_ascending, self.muscleTip_joint_ascending,
                            self.muscleDriver_joint_ascending, self.muscleOffset_joint_ascending, self.muscleJoint_joint_ascending])
        print("Compelete Generating TrapeziusMuscle_C")

        # update joints color
        orange_color_index = 14

        # # Function to update joint color
        def set_joint_color(joint, color_index):
            
            cmds.setAttr("{0}.overrideEnabled".format(joint), 1)
            cmds.setAttr("{0}.overrideColor".format(joint), color_index)

        for joint in self.AscendingAllJoints:
            set_joint_color(joint, orange_color_index)

        return True
            


    def createAscendingConstraint(self):
        
        result = self.createAscendingJoints()
        if result == None:
            print("Can't Generating Constraint because return None")
            return
        if result == True:
            # self.createAscendingJoints()
            self.objectDirectionMenu_value = cmds.optionMenuGrp("objectMenu", query=True, value=True)
            self.worldUpMenu_value = cmds.optionMenuGrp("worldUpMenu", query=True, value=True)
            self.dirAxis = direction_axis_vectors[self.objectDirectionMenu_value]
            self.upAixs = up_axis_vectors[self.worldUpMenu_value]

            # print(self.muscleInsertion_joint_ascending)
            # print(self.muscleTip_joint_ascending)
            # Use muscle insertion joint point constraint tip joint
            cmds.pointConstraint(self.muscleInsertion_joint_ascending, self.muscleTip_joint_ascending, maintainOffset = False,
                                weight = 1)
            
            # pointConstraint driver joint at middle of base/tip joints
            self.mainPointConstraint_ascending = cmds.pointConstraint(self.muscleBase_joint_ascending, self.muscleTip_joint_ascending, self.muscleDriver_joint_ascending, maintainOffset = True,
                                weight=1)

            # aimConstraint insertion and muscle driver joint
            self.mainAimConstraint_ascending = cmds.aimConstraint(self.muscleInsertion_joint_ascending, self.muscleBase_joint_ascending,
                                                        aimVector = self.dirAxis, upVector = self.upAixs,
                                                        worldUpType = "objectrotation", worldUpObject = self.back,
                                                        worldUpVector = self.upAixs)

            self.axisValueAscending.extend([self.objectDirectionMenu_value, self.worldUpMenu_value, self.dirAxis, 
                                self.upAixs, self.mainPointConstraint_ascending, self.mainAimConstraint_ascending])
            
            print("Compelete Ascending Constraint")
            self.addSDK_Ascending()
            print("Compelete Ascending Set SDK")

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
        self.mainPointConstraint_decending = cmds.pointConstraint(self.muscleBase_joint_decending, self.muscleTip_joint_decending, self.muscleDriver_joint_decending, maintainOffset = True,
                                weight=1)

        self.mainAimConstraint_decending = cmds.aimConstraint(self.muscleInsertion_joint_decending, self.muscleBase_joint_decending,
                                            aimVector = self.dirAxis, upVector = self.upAixs,
                                            worldUpType = "objectrotation", worldUpObject = self.back,
                                            worldUpVector = self.upAixs)
        
        self.mainPointConstraint_traverse = cmds.pointConstraint(self.muscleBase_joint_traverse, self.muscleTip_joint_traverse, self.muscleDriver_joint_traverse, maintainOffset = True,
                                            weight=1)

        self.mainAimConstraint_traverse = cmds.aimConstraint(self.muscleInsertion_joint_traverse, self.muscleBase_joint_traverse,
                                                    aimVector = self.dirAxis, upVector = self.upAixs,
                                                    worldUpType = "objectrotation", worldUpObject = self.back,
                                                    worldUpVector = self.upAixs)
        
        self.mainPointConstraint_ascending = cmds.pointConstraint(self.muscleBase_joint_ascending, self.muscleTip_joint_ascending, self.muscleDriver_joint_ascending, maintainOffset = True,
                                            weight=1)

        self.mainAimConstraint_ascending = cmds.aimConstraint(self.muscleInsertion_joint_ascending, self.muscleBase_joint_ascending,
                                                    aimVector = self.dirAxis, upVector = self.upAixs,
                                                    worldUpType = "objectrotation", worldUpObject = self.back,
                                                    worldUpVector = self.upAixs)


 
        # set joints to templete
        joints =[ self.muscleOrigin_joint_decending, self.muscleInsertion_joint_decending, 
                 self.muscleOrigin_joint_traverse, self.muscleInsertion_joint_traverse,
                 self.muscleOrigin_joint_decending, self.muscleInsertion_joint_decending]
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

        cmds.delete(cmds.pointConstraint(self.muscleOrigin_joint_decending, self.originLoc_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleOrigin_joint_traverse, self.originLoc_B, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleOrigin_joint_ascending, self.originLoc_C, mo=False, w=True))

        self.ptConstraintsTmp_A.append(cmds.pointConstraint(self.originLoc_A, self.muscleOrigin_joint_decending, mo=False, w=True)[0])
        self.ptConstraintsTmp_B.append(cmds.pointConstraint(self.originLoc_B, self.muscleOrigin_joint_traverse, mo=False, w=True)[0])
        self.ptConstraintsTmp_C.append(cmds.pointConstraint(self.originLoc_C, self.muscleOrigin_joint_ascending, mo=False, w=True)[0])

        self.insertionLoc_A = createSpaceLocator(3.0, name="{0}_muscleInsertion_loc_A".format(self.L_R_value))
        self.insertionLoc_B = createSpaceLocator(3.0, name="{0}_muscleInsertion_loc_B".format(self.L_R_value))
        self.insertionLoc_C = createSpaceLocator(3.0, name="{0}_muscleInsertion_loc_C".format(self.L_R_value))

        if self.insertionAttachObj:
            cmds.parent(self.insertionLoc_A, self.insertionAttachObj)
            cmds.parent(self.insertionLoc_B, self.insertionAttachObj)
            cmds.parent(self.insertionLoc_C, self.insertionAttachObj)

        # get reverse direction
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
        
        cmds.delete(cmds.pointConstraint(self.muscleInsertion_joint_decending, self.insertionLoc_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleInsertion_joint_traverse, self.insertionLoc_B, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleInsertion_joint_ascending, self.insertionLoc_C, mo=False, w=True))

        self.ptConstraintsTmp_A.append(cmds.pointConstraint(self.insertionLoc_A, self.muscleInsertion_joint_decending, mo=False, w=True)[0])
        self.ptConstraintsTmp_B.append(cmds.pointConstraint(self.insertionLoc_B, self.muscleInsertion_joint_traverse, mo=False, w=True)[0])
        self.ptConstraintsTmp_C.append(cmds.pointConstraint(self.insertionLoc_C, self.muscleInsertion_joint_ascending, mo=False, w=True)[0])

        driverGrp_A = cmds.group(name="{0}_muscleCenter_A_grp".format(self.L_R_value), empty=True)
        driverGrp_B = cmds.group(name="{0}_muscleCenter_B_grp".format(self.L_R_value), empty=True)
        driverGrp_C = cmds.group(name="{0}_muscleCenter_C_grp".format(self.L_R_value), empty=True)

        self.centerLoc_A = createSpaceLocator(0.25, name="{0}_muscleCenter_loc".format(self.muscleOrigin_joint_decending))
        self.centerLoc_B = createSpaceLocator(0.25, name="{0}_muscleCenter_loc".format(self.muscleOrigin_joint_traverse))
        self.centerLoc_C = createSpaceLocator(0.25, name="{0}_muscleCenter_loc".format(self.muscleOrigin_joint_ascending))

        cmds.parent(self.centerLoc_A, driverGrp_A)
        cmds.parent(self.centerLoc_B, driverGrp_B)
        cmds.parent(self.centerLoc_C, driverGrp_C)

        cmds.delete(cmds.pointConstraint(self.muscleDriver_joint_decending, driverGrp_A, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleDriver_joint_traverse, driverGrp_B, mo=False, w=True))
        cmds.delete(cmds.pointConstraint(self.muscleDriver_joint_ascending, driverGrp_C, mo=False, w=True))

        cmds.parent(driverGrp_A, self.originLoc_A)
        cmds.parent(driverGrp_B, self.originLoc_B)
        cmds.parent(driverGrp_C, self.originLoc_C)

        cmds.pointConstraint(self.originLoc_A, self.insertionLoc_A, driverGrp_A, mo=True, w=True)
        cmds.pointConstraint(self.originLoc_B, self.insertionLoc_B, driverGrp_B, mo=True, w=True)
        cmds.pointConstraint(self.originLoc_C, self.insertionLoc_C, driverGrp_C, mo=True, w=True)

        cmds.setAttr("{0}.r".format(driverGrp_A), 0, 0, 0)
        cmds.setAttr("{0}.r".format(driverGrp_B), 0, 0, 0)
        cmds.setAttr("{0}.r".format(driverGrp_C), 0, 0, 0)

        cmds.delete(self.mainPointConstraint_decending)
        cmds.delete(self.mainPointConstraint_traverse)
        cmds.delete(self.mainPointConstraint_ascending)

        self.ptConstraintsTmp_A.append(cmds.pointConstraint(self.centerLoc_A, self.muscleDriver_joint_decending, mo=False, w=True)[0])
        self.ptConstraintsTmp_B.append(cmds.pointConstraint(self.centerLoc_B, self.muscleDriver_joint_traverse, mo=False, w=True)[0])
        self.ptConstraintsTmp_C.append(cmds.pointConstraint(self.centerLoc_C, self.muscleDriver_joint_ascending, mo=False, w=True)[0])

        
  
    def update(self, *args):
        ###
        for ptConstraintsTmp_A in self.ptConstraintsTmp_A:
            if cmds.objExists(ptConstraintsTmp_A):
                cmds.delete(ptConstraintsTmp_A)

        for ptConstraintsTmp_B in self.ptConstraintsTmp_B:
            if cmds.objExists(ptConstraintsTmp_B):
                cmds.delete(ptConstraintsTmp_B)

        for ptConstraintsTmp_C in self.ptConstraintsTmp_C:
            if cmds.objExists(ptConstraintsTmp_C):
                cmds.delete(ptConstraintsTmp_C)

        ###
        for loc_decending in [self.originLoc_A, self.insertionLoc_A, self.centerLoc_A]:
            if cmds.objExists(loc_decending):
                cmds.delete(loc_decending)

        for loc_traverse in [self.originLoc_B, self.insertionLoc_B, self.centerLoc_B]:
            if cmds.objExists(loc_traverse):
                cmds.delete(loc_traverse)

        for loc_ascending in [self.originLoc_C, self.insertionLoc_C, self.centerLoc_C]:
            if cmds.objExists(loc_ascending):
                cmds.delete(loc_ascending)
        
        ###
        joints =[ self.muscleOrigin_joint_decending, self.muscleInsertion_joint_decending, 
                 self.muscleOrigin_joint_traverse, self.muscleInsertion_joint_traverse,
                 self.muscleOrigin_joint_decending, self.muscleInsertion_joint_decending]
        for i in joints:
            cmds.setAttr("{0}.overrideEnabled".format(i), 0)
            cmds.setAttr("{0}.overrideDisplayType".format(i), 0)

        
        cmds.delete(self.mainAimConstraint_decending)
        cmds.delete(self.mainAimConstraint_traverse)
        cmds.delete(self.mainAimConstraint_ascending)
        
        self.mainPointConstraint_decending = cmds.pointConstraint(self.muscleBase_joint_decending, self.muscleTip_joint_decending, self.muscleDriver_joint_decending,
                                                        mo=True, weight=1)
        self.mainPointConstraint_traverse = cmds.pointConstraint(self.muscleBase_joint_traverse, self.muscleTip_joint_traverse, self.muscleDriver_joint_traverse,
                                                        mo=True, weight=1)

        self.mainPointConstraint_ascending = cmds.pointConstraint(self.muscleBase_joint_ascending, self.muscleTip_joint_ascending, self.muscleDriver_joint_ascending,
                                                        mo=True, weight=1)

        cmds.delete(cmds.aimConstraint(self.muscleInsertion_joint_decending, self.muscleOrigin_joint_decending,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))
        cmds.delete(cmds.aimConstraint(self.muscleInsertion_joint_traverse, self.muscleOrigin_joint_traverse,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))
        cmds.delete(cmds.aimConstraint(self.muscleInsertion_joint_ascending, self.muscleOrigin_joint_ascending,
                                       aimVector = self.dirAxis, upVector=self.upAixs,
                                       worldUpType="scene", offset=[0, 0, 0], weight=1))

        self.mainAimConstraint_decending = cmds.aimConstraint(self.muscleInsertion_joint_decending, self.muscleBase_joint_decending,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.back,
                                                    worldUpVector=self.upAixs)
        self.mainAimConstraint_traverse = cmds.aimConstraint(self.muscleInsertion_joint_traverse, self.muscleBase_joint_traverse,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.back,
                                                    worldUpVector=self.upAixs)
        self.mainAimConstraint_ascending = cmds.aimConstraint(self.muscleInsertion_joint_ascending, self.muscleBase_joint_ascending,
                                                    aimVector=self.dirAxis, upVector=self.upAixs,
                                                    worldUpType="objectrotation", worldUpObject=self.back,
                                                    worldUpVector=self.upAixs)

        animCurveNodes_decending = cmds.ls(cmds.listConnections(self.muscleJoint_joint_decending, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))
        animCurveNodes_traverse = cmds.ls(cmds.listConnections(self.muscleJoint_joint_traverse, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))
        animCurveNodes_ascending = cmds.ls(cmds.listConnections(self.muscleJoint_joint_ascending, s=True, d=False),
                                 type=("animCurveUU", "animCurveUL"))
        
        cmds.delete(animCurveNodes_decending)
        cmds.delete(animCurveNodes_traverse)
        cmds.delete(animCurveNodes_ascending)
        self.addSDK_Decending()
        self.addSDK_Traverse()
        self.addSDK_Ascending()
        


    def addSDK_Decending(self, stretchOffset=None, compressionOffset=None):
        self.stretchFactor = float(cmds.textField(self.ui_instance.stretchField, query=True, text=True))
        self.compressionFactor = float(cmds.textField(self.ui_instance.compressionField, query=True, text=True))

        yzSquashScale = math.sqrt(1.0 / self.compressionFactor)
        yzStretchScale = math.sqrt(1.0 / self.stretchFactor)

        if stretchOffset is None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset is None:
            compressionOffset = [0.0, 0.0, 0.0]

        restLength_decending = cmds.getAttr("{0}.translate{1}".format(self.muscleTip_joint_decending, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            # decending part
            cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_decending, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_decending, axis), 0.0)

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_decending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_decending, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_decending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_decending, self.objectDirectionMenu_value))

            # set up stretch factor
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_decending, self.objectDirectionMenu_value), restLength_decending * self.stretchFactor)

            
            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_decending, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_decending, axis), yzStretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_decending, axis), stretchOffset[index])
            
            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_decending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_decending, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_decending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_decending, self.objectDirectionMenu_value))

            # set up compression factor
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_decending, self.objectDirectionMenu_value), restLength_decending * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_decending, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_decending, axis), yzSquashScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_decending, axis), compressionOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_decending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_decending, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_decending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_decending, self.objectDirectionMenu_value))
            
            # reset back to origin length
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_decending, self.objectDirectionMenu_value), restLength_decending)
            


    def addSDK_Traverse(self, stretchOffset=None, compressionOffset=None):
        self.stretchFactor = float(cmds.textField(self.ui_instance.stretchField, query=True, text=True))
        self.compressionFactor = float(cmds.textField(self.ui_instance.compressionField, query=True, text=True))
    
        yzSquashScale = math.sqrt(1.0 / self.compressionFactor)
        yzStretchScale = math.sqrt(1.0 / self.stretchFactor)

        if stretchOffset is None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset is None:
            compressionOffset = [0.0, 0.0, 0.0]


        restLength_traverse = cmds.getAttr("{0}.translate{1}".format(self.muscleTip_joint_traverse, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            # traverse part
            cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_traverse, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_traverse, axis), 0.0)

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_traverse, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_traverse, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_traverse, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_traverse, self.objectDirectionMenu_value))

            # set up stretch factor
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_traverse, self.objectDirectionMenu_value), restLength_traverse * self.stretchFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_traverse, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_traverse, axis), yzStretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_traverse, axis), stretchOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_traverse, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_traverse, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_traverse, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_traverse, self.objectDirectionMenu_value))

            # set up compression factor
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_traverse, self.objectDirectionMenu_value), restLength_traverse * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_traverse, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_traverse, axis), yzSquashScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_traverse, axis), compressionOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_traverse, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_traverse, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_traverse, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_traverse, self.objectDirectionMenu_value))

            # reset back to origin length
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_traverse, self.objectDirectionMenu_value), restLength_traverse)



    def addSDK_Ascending(self, stretchOffset=None, compressionOffset=None):
        self.stretchFactor = float(cmds.textField(self.ui_instance.stretchField, query=True, text=True))
        self.compressionFactor = float(cmds.textField(self.ui_instance.compressionField, query=True, text=True))
        yzSquashScale = math.sqrt(1.0 / self.compressionFactor)
        yzStretchScale = math.sqrt(1.0 / self.stretchFactor)

        if stretchOffset is None:
            stretchOffset = [0.0, 0.0, 0.0]
        if compressionOffset is None:
            compressionOffset = [0.0, 0.0, 0.0]


        restLength_ascending = cmds.getAttr("{0}.translate{1}".format(self.muscleTip_joint_ascending, self.objectDirectionMenu_value))

        for index, axis in enumerate("XYZ"):
            # ascending part
            cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_ascending, axis), 1.0)
            cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_ascending, axis), 0.0)

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_ascending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_ascending, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_ascending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_ascending, self.objectDirectionMenu_value))

            # set up stretch factor
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_ascending, self.objectDirectionMenu_value), restLength_ascending * self.stretchFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_ascending, axis), self.stretchFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_ascending, axis), yzStretchScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_ascending, axis), stretchOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_ascending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_ascending, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_ascending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_ascending, self.objectDirectionMenu_value))

            # set up compression factor
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_ascending, self.objectDirectionMenu_value), restLength_ascending * self.compressionFactor)

            if axis == "X":
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_ascending, axis), self.compressionFactor)
            else:
                cmds.setAttr("{0}.scale{1}".format(self.muscleJoint_joint_ascending, axis), yzSquashScale)
                cmds.setAttr("{0}.translate{1}".format(self.muscleJoint_joint_ascending, axis), compressionOffset[index])

            cmds.setDrivenKeyframe("{0}.scale{1}".format(self.muscleJoint_joint_ascending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_ascending, self.objectDirectionMenu_value))
            cmds.setDrivenKeyframe("{0}.translate{1}".format(self.muscleJoint_joint_ascending, axis),
                                currentDriver="{0}.translate{1}".format(self.muscleTip_joint_ascending, self.objectDirectionMenu_value))

            # reset back to origin length
            cmds.setAttr("{0}.translate{1}".format(self.muscleTip_joint_ascending, self.objectDirectionMenu_value), restLength_ascending)



    def muscleJointLib(self, *args):
        self.L_R_value = cmds.optionMenuGrp("pick_L_R_Menu", query=True, value=True)

        self.muscleOrigin_joint_decending = "{0}_muscleOrigin_TrapeziusMuscle_A".format(self.L_R_value)
        self.muscleInsertion_joint_decending = "{0}_muscleInsertion_TrapeziusMuscle_A".format(self.L_R_value)

        self.muscleOrigin_joint_traverse = "{0}_muscleOrigin_TrapeziusMuscle_B".format(self.L_R_value)
        self.muscleInsertion_joint_traverse = "{0}_muscleInsertion_TrapeziusMuscle_B".format(self.L_R_value)

        self.muscleOrigin_joint_ascending = "{0}_muscleOrigin_TrapeziusMuscle_C".format(self.L_R_value)
        self.muscleInsertion_joint_ascending = "{0}_muscleInsertion_TrapeziusMuscle_C".format(self.L_R_value)

        self.muscleBase_joint_decending = "{0}_muscleBase_TrapeziusMuscle_A".format(self.L_R_value)
        self.muscleBase_joint_traverse = "{0}_muscleBase_TrapeziusMuscle_B".format(self.L_R_value)
        self.muscleBase_joint_ascending = "{0}_muscleBase_TrapeziusMuscle_C".format(self.L_R_value)

        self.muscleDriver_joint_decending = "{0}_muscleDriver_TrapeziusMuscle_A".format(self.L_R_value)
        self.muscleDriver_joint_traverse = "{0}_muscleDriver_TrapeziusMuscle_B".format(self.L_R_value)
        self.muscleDriver_joint_ascending = "{0}_muscleDriver_TrapeziusMuscle_C".format(self.L_R_value)

        self.muscleOffset_joint_decending = "{0}_muscleOffset_TrapeziusMuscle_A".format(self.L_R_value)
        self.muscleOffset_joint_traverse = "{0}_muscleOffset_TrapeziusMuscle_B".format(self.L_R_value)
        self.muscleOffset_joint_ascending = "{0}_muscleOffset_TrapeziusMuscle_C".format(self.L_R_value)

        self.muscleJoint_joint_decending = "{0}_muscleJoint_TrapeziusMuscle_A".format(self.L_R_value)
        self.muscleJoint_joint_traverse = "{0}_muscleJoint_TrapeziusMuscle_B".format(self.L_R_value)
        self.muscleJoint_joint_ascending = "{0}_muscleJoint_TrapeziusMuscle_C".format(self.L_R_value)

        self.muscleTip_joint_decending = "{0}_muscleTip_TrapeziusMuscle_A".format(self.L_R_value)
        self.muscleTip_joint_traverse = "{0}_muscleTip_TrapeziusMuscle_B".format(self.L_R_value)
        self.muscleTip_joint_ascending = "{0}_muscleTip_TrapeziusMuscle_C".format(self.L_R_value)



    def delete(self, *args):
        self.muscleJointLib()

        joints_to_delete = [
            self.muscleOrigin_joint_decending,
            self.muscleInsertion_joint_decending,
            self.muscleTip_joint_decending,
            self.muscleBase_joint_decending,
            self.muscleDriver_joint_decending,
            self.muscleOffset_joint_decending,
            self.muscleJoint_joint_decending,
            self.muscleOrigin_joint_traverse,
            self.muscleInsertion_joint_traverse,
            self.muscleTip_joint_traverse,
            self.muscleBase_joint_traverse,
            self.muscleDriver_joint_traverse,
            self.muscleOffset_joint_traverse,
            self.muscleJoint_joint_traverse,
            self.muscleOrigin_joint_ascending,
            self.muscleInsertion_joint_ascending,
            self.muscleTip_joint_ascending,
            self.muscleBase_joint_ascending,
            self.muscleDriver_joint_ascending,
            self.muscleOffset_joint_ascending,
            self.muscleJoint_joint_ascending
        ]

        for i in joints_to_delete:
            if cmds.objExists(i):
                cmds.delete(i)



    def joint_exists(self, joint_name):
        return cmds.ls(joint_name, type="joint")



    def serialize(self):
        pass


    @classmethod
    def deserialize(cls, dataMode):
        pass





    def getTrapeziusMuscle(self):
        trapeziusData = {}
        for side in ["L", "R"]:
            trapeziusData[side] = {}

            for muscleType in "ABC":

                muscleOrigin = "{0}_muscleOrigin_TrapeziusMuscle_{1}".format(side, muscleType)
                muscleInsertion = "{0}_muscleInsertion_TrapeziusMuscle_{1}".format(side, muscleType)
                muscleCenter = "{0}_muscleJoint_TrapeziusMuscle_{1}".format(side, muscleType)
                # muscleOrigin = cmds.ls("{0}_muscleOrigin_TrapeziusMuscle_{1}".format(side, muscleType))[0]
                # muscleInsertion = cmds.ls("{0}_muscleInsertion_TrapeziusMuscle_{1}".format(side, muscleType))[0]
                # muscleCenter = cmds.ls("{0}_muscleJoint_TrapeziusMuscle_{1}".format(side, muscleType))[0]

                if not cmds.objExists(muscleOrigin) or not cmds.objExists(muscleInsertion) or not cmds.objExists(muscleCenter):
                    logger.error("Object {0}, {1}, and {2} not in the project !!!".format(muscleOrigin, muscleInsertion, muscleCenter))
                    continue

                muscleOriginPos = cmds.xform(muscleOrigin, translation = True, worldSpace = True, query = True)
                muscleInsertionPos = cmds.xform(muscleInsertion, translation=True, worldSpace=True, query=True)
                muscleCenterPos = cmds.xform(muscleCenter, translation=True, worldSpace=True, query=True)

                trapeziusData[side].update({
                    muscleOrigin: muscleOriginPos,
                    muscleInsertion: muscleInsertionPos,
                    muscleCenter: muscleCenterPos
                })
                # Old method 1
                # trapeziusData[side].update({muscleOrigin: muscleOriginPos})
                # trapeziusData[side].update({muscleInsertion: muscleInsertionPos})
                # trapeziusData[side].update({muscleCenter: muscleCenterPos})

                # Old method 2
                # trapeziusData[side][muscleOrigin] = muscleOriginPos
                # trapeziusData[side][muscleInsertion] = muscleInsertionPos
                # trapeziusData[side][muscleCenter] = muscleCenterPos


        logger.info(trapeziusData)
        return trapeziusData


    def exportMuscle(self, filepath):
        muscleData = {}
        trapeziusData = self.getTrapeziusMuscle()
        muscleData["Trapezius"] = trapeziusData
        logger.info(muscleData)

        with open(filepath, "w") as fp:
            json.dump(muscleData, fp, ensure_ascii = False, indent = 4, separators = (",", ":"), sort_keys = True)

    def importMuscle(self, filepath):
        with open(filepath) as fp:
            muscleData = json.load(fp)

        #trapezius
        trapeziusData = muscleData.get("Trapezius", None)
        if trapeziusData:
            for side in trapeziusData.keys():
                if not trapeziusData.get(side):
                    continue

                #
                muscleBuilder = TrapeziusMuscleGRP(ui_instance = self)
                muscleBuilder.createDecendingJoints()



                #A
                originPos = trapeziusData.get(side).get("{0}_muscleOrigin_TrapeziusMuscle_A".format(side))
                print(originPos)
                # cmds.xform(muscleBuilder.muscleOrigin_joint_decending, translation = originPos, worldSpace = True)
                # cmds.xform(muscleBuilder.createDecendingJoints.originLoc_A, translation=originPos, worldSpace=True)
                #B

                #C

# exportMuscle(fp)
# importMuscle(fp)