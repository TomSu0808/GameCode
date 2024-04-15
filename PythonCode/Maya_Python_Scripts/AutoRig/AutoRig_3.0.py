import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2
from functools import partial


class CreateSkeletonB(object):
    #Spine Skeleton
    def __CreateSpineSkeleton__(self):
        self.HipJoint = cmds.joint(name='A_Hip_Jt', position=(0.008, 4.451, 0))
        cmds.joint('A_Hip_Jt', edit=True, zso=True, oj='xyz')
        
        numJt = range(4)
        jtPosX = 0.08
        jtPosY = 0.05
        for joints in numJt: 
                extraStrJt ="Hip_Jt_"
                extraJt = cmds.joint(name= extraStrJt+str(joints), position=(0.008, 4.451,0))
                cmds.joint(extraStrJt+str(joints), edit=True, zso=True, oj='xyz')
                cmds.select(extraStrJt+str(joints))
                jointList = cmds.ls(selection=True)
                if joints:
                        jtPosY += 0.18
                        jtPosX += -0.08
                        cmds.select(extraStrJt+str(joints))
                        cmds.move(0.3,0.0,0.0)
                        cmds.move(joints*0.008-0.2,4.751+joints*jtPosY,0, extraStrJt+str(joints), absolute= True)
        
                            

        cmds.move(jtPosX, 4.451+0.9*2, 0)
        
        self.NeckJoint = cmds.joint(name='D_Neck_Jt', position=(-0.089, 6.965, 0))
        cmds.joint('D_Neck_Jt', edit=True, zso=True, oj='xyz')
        
        self.HeadJoint = cmds.joint(name='E_Head_Jt', position=(-0.026, 7.306, 0))
        cmds.joint('E_Head_Jt', edit=True, zso=True, oj='xyz')

        self.HeadTipJoint = cmds.joint(name='F_HeadTip_Jt', position=(-0.015, 8.031, 0))
        cmds.select('A_Hip_Jt')
        cmds.joint(name='Root', position=(0, 0, 0))
        #Move the first created back joint a little upward
        cmds.select("Hip_Jt_0")
        cmds.move(-0.008,4.701,0)
        #0.008, 4.451, 0
        cmds.select('A_Hip_Jt')
        
    #Leg Skeleton  
    def __CreateSkeletonLeg__(self):
        self.L_HipJoint =  cmds.joint(name='L_Hip_Jt', position=(-0.12, 4.369, -0.689))
        #cmds.joint(name='l_hipFront_tempJt', position=(1.2, 10.7, 0.8))
        cmds.select('L_Hip_Jt')
        self.L_KneeJoint = cmds.joint(name='L_Knee_Jt', position=(0.2, 2.36, -0.689))
        #cmds.joint(name='l_kneeFront_tempJt', position=(1.2, 5.8, 1.3))
        cmds.select('L_Knee_Jt')
        cmds.joint('L_Hip_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_AnkleJoint = cmds.joint(name='L_Ankle_Jt', position=(-0.24, 0.486, -0.689))
        cmds.joint('L_Knee_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        #self.L_HeelFootJoint = cmds.joint(name='L_HeelFoot_Jt', position=(-0.486, 0.065, -0.6898));
        cmds.joint('L_Ankle_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_ToeJoint = cmds.joint(name='L_Toe_Jt', position=(0.32, 0.051, -0.689))
        #cmds.joint('L_HeelFoot_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_ToeEndJoint = cmds.joint(name='L_ToeEnd_Jt', position=(0.69, 0.062, -0.689))
        cmds.joint('L_Toe_Jt', edit=True, zso=True, oj='xyz', sao='yup')
		
    def __CreateSkeletonArm__(self):
        cmds.select('D_Neck_Jt')
        self.L_CollarBoneJoint = cmds.joint(name='L_Collarbone_Jt', position=(-0.233, 6.565, -0.793))
        self.L_ShoulderJoint = cmds.joint(name='L_Shoulder_Jt', position=(0, 6.749, -1.31))
        cmds.joint('L_Collarbone_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_ElbowJoint = cmds.joint(name='L_Elbow_Jt', position=(0, 5.773, -2.092))
        cmds.joint('L_Shoulder_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_WristJoint = cmds.joint(name='L_Wrist_Jt', position=(0.503, 5.126, -2.82))
        cmds.joint('L_Elbow_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_MiddleHandJoint = cmds.joint(name='L_MiddleHand_Jt', position=(0.641, 4.961, -2.963))
        cmds.joint('L_Wrist_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        cmds.select('L_Wrist_Jt')
        
    def __CreateSkeletonFingers__(self):
        #Thumb
        self.L_Thumb01Joint = cmds.joint(name='L_Thumb01_Jt', position=(0.782, 4.973, -2.855))
        self.L_Thumb02Joint = cmds.joint(name='L_Thumb02_Jt', position=(0.895, 4.867, -2.855))
        cmds.joint('L_Thumb01_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_Thumb03Joint = cmds.joint(name='L_Thumb03_Jt', position=(0.938, 4.79, -2.855))
        cmds.joint('L_Thumb02_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        #Index
        cmds.select('L_Wrist_Jt')
        self.L_IndexFinger01Joint = cmds.joint(name='L_IndexFinger01_Jt', position=(0.749, 4.841, -3.093))
        self.L_IndexFinger02Joint = cmds.joint(name='L_IndexFinger02_Jt', position=(0.816, 4.697, -3.159))
        cmds.joint('L_IndexFinger01_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_IndexFinger03Joint = cmds.joint(name='L_IndexFinger03_Jt', position=(0.849, 4.568, -3.19))
        cmds.joint('L_IndexFinger02_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_IndexFinger04Joint = cmds.joint(name='l_indexFinger04_Jt', position=(0.861, 4.484, -3.198))
        cmds.joint('L_IndexFinger03_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        #Middle
        cmds.select('L_Wrist_Jt')
        self.L_MiddleFinger01Joint = cmds.joint(name='L_MiddleFinger01_Jt', position=(0.637, 4.833, -3.183))
        self.L_MiddleFinger02Joint = cmds.joint(name='L_MiddleFinger02_Jt', position=(0.682, 4.703, -3.276))
        cmds.joint('L_MiddleFinger01_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_MiddleFinger03Joint = cmds.joint(name='L_MiddleFinger03_Jt', position=(0.702, 4.554, -3.322))
        cmds.joint('L_MiddleFinger02_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_MiddleFinger04Joint = cmds.joint(name='L_MiddleFinger04_Jt', position=(0.711, 4.441, -3.334))
        cmds.joint('L_MiddleFinger03_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        #Ring
        cmds.select('L_Wrist_Jt')
        self.L_RingFinger01Joint = cmds.joint(name='L_RingFinger01_Jt', position=(0.488, 4.827, -3.25))
        self.L_RingFinger02Joint =cmds.joint(name='L_RingFinger02_Jt', position=(0.528, 4.713, -3.31))
        cmds.joint('L_RingFinger01_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_RingFinger03Joint =cmds.joint(name='L_RingFinger03_Jt', position=(0.541, 4.584, -3.354 ))
        cmds.joint('L_RingFinger02_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_RingFinger04Joint = cmds.joint(name='L_RingFinger04_Jt', position=(0.546, 4.49, -3.361))
        cmds.joint('L_RingFinger03_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
        cmds.select('L_Wrist_Jt')
        self.L_Pinky01Joint = cmds.joint(name='L_Pinky01_tJt', position=(0.362, 4.818, -3.251))
        self.L_Pinky02Joint = cmds.joint(name='L_Pinky02_Jt', position=(0.375, 4.73, -3.283))
        cmds.joint('L_Pinky01_tJt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_Pinky03Joint = cmds.joint(name='L_Pinky03_Jt', position=(0.38, 4.617, -3.329))
        cmds.joint('L_Pinky02_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        self.L_Pinky04Joint = cmds.joint(name='L_Pinky04_Jt', position=(0.385, 4.534, -3.341))
        cmds.joint('L_Pinky03_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
    def __CreateFingerCtrl_(**kwargs):
        joints = kwargs.setdefault("joints")
        
        for jt in joints:
            cmds.select(jt, hierarchy=True)
            jointList = cmds.ls(selection=True)
            
            for joint in jointList[:-2]:
                pos = cmds.joint(joint, q=True, position=True)
                nameSplit = joint.rsplit('_', 1)
                name = nameSplit[0]
                cmds.select(joint)
                cmds.joint(name=name+'Up_Jt', position=(pos[0]+0.01, pos[1]+0.05, pos[2]-0.06))
                
    def __MirrorJointsHands__(self, **kwargs):   
        cmds.select('D_Neck_Jt')
        self.MirrorEachJoint = cmds.mirrorJoint('L_Collarbone_Jt',mirrorXY=True,mirrorBehavior=True,searchReplace=('L_','R_'))
    def __MirrorJointsLegs__(self, **kwargs):
        cmds.select('Root')
        self.MirrorEachJoint = cmds.mirrorJoint('L_Hip_Jt',mirrorXY=True,mirrorBehavior=True,searchReplace=('L_', 'R_'))	
        slBone = cmds.select('A_Hip_Jt')
		
    def __create__(*args):
        skeletonJT = CreateSkeletonB()
        skeletonJT.__CreateSpineSkeleton__()
        skeletonJT.__CreateSkeletonLeg__()
        skeletonJT.__CreateSkeletonArm__()
        skeletonJT.__CreateSkeletonFingers__()
        skeletonJT.__MirrorJointsHands__()
        skeletonJT.__MirrorJointsLegs__()


class CreateSkeletonQ():
    #Front Legs Skeleton
    def _CreateFrontLegsSkeleton_L(self):
        self.F_HipJoint = cmds.joint(name='Hip', position=(4.086, 8.755, 0.002))
        cmds.joint('Hip', edit=True, zso=True, oj='xyz')
                         
        self.F_ShoulderJoint = cmds.joint(name='L_Front_Shoulder_Jt', position=(3.76, 6.725, -1.448))
        cmds.joint('L_Front_Shoulder_Jt', edit=True, zso=True, oj='xyz')
        
        self.F_ElbowJoint = cmds.joint(name='L_Front_Elbow_Jt', position=(2.729, 4.374, -1.503))
        cmds.joint('L_Front_Elbow_Jt', edit=True, zso=True, oj='xyz')

        self.F_WristJoint = cmds.joint(name='L_Front_Wrist_Jt', position=(3.5, 2.18, -1.466))
        cmds.joint('L_Front_Wrist_Jt', edit = True, zso=True, oj='xyz')
        
        self.F_ToeJoint = cmds.joint(name='L_Front_WristExtra_Jt', position=(3.354, 0.388, -1.437))
        cmds.joint('L_Front_WristExtra_Jt', edit = True, zso=True, oj='xyz')
        
        self.F_ToeJoint = cmds.joint(name='L_Front_Toe_Jt', position=(4.862, -0.144, -1.437))
        cmds.joint('L_Front_Toe_Jt', edit = True, zso=True, oj='xyz')
        
        cmds.select('Hip')
    

    def _CreateFrontLegsSkeleton_R(self):

        cmds.select('Hip')
                         
        self.F_ShoulderJointR = cmds.joint(name='R_Front_Shoulder_Jt', position=(3.76, 6.725, 1.448))
        cmds.joint('R_Front_Shoulder_Jt', edit=True, zso=True, oj='xyz')
        
        self.F_ElbowJointR = cmds.joint(name='R_Front_Elbow_Jt', position=(2.729, 4.374, 1.503))
        cmds.joint('R_Front_Elbow_Jt', edit=True, zso=True, oj='xyz')

        self.F_WristJointR = cmds.joint(name='R_Front_Wrist_Jt', position=(3.5, 2.18, 1.466))
        cmds.joint('R_Front_Wrist_Jt', edit = True, zso=True, oj='xyz')
        
        self.F_ToeJointR = cmds.joint(name='R_Front_WristExtra_Jt', position=(3.354, 0.388, 1.437))
        cmds.joint('R_Front_WristExtra_Jt', edit = True, zso=True, oj='xyz')
        
        self.F_ToeJointR = cmds.joint(name='R_Front_Toe_Jt', position=(4.862, -0.144, 1.437))
        cmds.joint('R_Front_Toe_Jt', edit = True, zso=True, oj='xyz')



    #Spine Skeleton    
    def __CreateSpineSkeleton__(self):
        cmds.select('Hip')
        self.Backbone_01 = cmds.joint(name ='B01', position=(2.064,8.829, 0.041))
        cmds.joint('B01', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.Backbone_02 = cmds.joint(name ='B02', position=(0.216, 9.445, 0.038))
        cmds.joint('B02', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.Backbone_03 = cmds.joint(name ='B03', position=(-1.813, 9.481, 0.042))
        cmds.joint('B03', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.Backbone_04 = cmds.joint(name ='B04', position=(-3.761, 9.253, 0.038))
        cmds.joint('B04', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.BackHipJoint = cmds.joint(name ='B_Back_Hip_Jt', position=(-5.321, 8.599, 0.04))
        cmds.joint('B_Back_Hip_Jt', edit=True, zso=True, oj='xyz', sao='yup')

    #Back Legs Skeleton  
    def _CreateBackLegsSkeleton_L(self):
        
        cmds.select('B_Back_Hip_Jt')
        
        self.B_PelvicJoint = cmds.joint(name='L_Back_Pelvic_Jt', position=(-4.754, 7.296, -1.494))
        cmds.joint(name='L_Back_Pelvic_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.B_KneeJoint = cmds.joint(name='L_Back_Knee_Jt', position=(-2.06, 5.671, -1.542))
        cmds.joint(name='L_Back_Knee_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.B_HeelJoint = cmds.joint(name='L_Back_Heel_Jt', position=(-6.112,2.462,-1.445))
        cmds.joint(name='L_Back_Heel_Jt',edit=True, zso=True, oj='xyz', sao='yup')
        
        self.B_Toe01Joint = cmds.joint(name='L_Back_Toe01_Jt', position=(-6.006, 0.25, -1.45))
        cmds.joint(name='L_Back_Toe01_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.B_Toe02Joint = cmds.joint(name='L_Back_Toe02_Jt', position=(-4.992, -0.103, -1.449))
        cmds.joint(name='L_Back_Toe02_Jt', edit=True, zso=True, oj='xyz', sao='yup')

    def _CreateBackLegsSkeleton_R(self):
        
        cmds.select('B_Back_Hip_Jt')
        
        self.B_PelvicJoint = cmds.joint(name='R_Back_Pelvic_Jt', position=(-4.754, 7.296, 1.494))
        cmds.joint(name='R_Back_Pelvic_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.B_KneeJoint = cmds.joint(name='R_Back_Knee_Jt', position=(-2.06, 5.671, 1.542))
        cmds.joint(name='R_Back_Knee_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.B_HeelJoint = cmds.joint(name='R_Back_Heel_Jt', position=(-6.112,2.462,1.445))
        cmds.joint(name='R_Back_Heel_Jt',edit=True, zso=True, oj='xyz', sao='yup')
        
        self.B_Toe01Joint = cmds.joint(name='R_Back_Toe01_Jt', position=(-6.006, 0.25, 1.45))
        cmds.joint(name='R_Back_Toe01_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.B_Toe02Joint = cmds.joint(name='R_Back_Toe02_Jt', position=(-4.992, -0.103, 1.449))
        cmds.joint(name='R_Back_Toe02_Jt', edit=True, zso=True, oj='xyz', sao='yup')

        
    # Tail Skeleton
    def __Tail__(self):
        
        cmds.select('B_Back_Hip_Jt')
        
        self.A_TailJoint = cmds.joint(name = 'Tail_Jt_A', position=(-6.141,8.196,0))
        cmds.joint(name='Tail_Jt_A', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.B_TailJoint = cmds.joint(name = 'Tail_Jt_B', position=(-7.002,7.895,0))
        cmds.joint(name='Tail_Jt_B', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.C_TailJoint = cmds.joint(name = 'Tail_Jt_C', position=(-7.77,7.752,0))
        cmds.joint(name='Tail_Jt_C', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.D_TailJoint = cmds.joint(name = 'Tail_Jt_D', position=(-8.498,7.719,0))
        cmds.joint(name='Tail_Jt_D', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.E_TailJoint = cmds.joint(name = 'Tail_Jt_E', position=(-9.225,7.848,0))
        cmds.joint(name='Tail_Jt_E', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.F_TailJoint = cmds.joint(name = 'Tail_Jt_F', position=(-9.866,8.115,0))
        cmds.joint(name='Tail_Jt_F', edit=True, zso=True, oj='xyz', sao='yup')
        
    # Head Skeleton   
    def __Head__(self):
        cmds.select('Hip')
        self.NeckJoint = cmds.joint(name = 'Neck_Jt', position=(6.016,9.717,0))  
        cmds.joint(name='Neck_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.HeadJoint = cmds.joint(name = 'Head_Jt', position=(7.634,12.322,0))  
        cmds.joint(name='Head_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
        self.JawJoint = cmds.joint(name = 'Jaw_Jt', position=(10.758,10.99,0))  
        cmds.joint(name='Jaw_Jt', edit=True, zso=True, oj='xyz', sao='yup')
        
        cmds.select("Hip")
    
    # Ear Skeleton
    def _Ears_L(self):
        cmds.select("Head_Jt")
        
        self.EarJoint = cmds.joint(name="L_Ear_Jt", position=(7.71,12.503,-0.896))
        cmds.joint(name="L_Ear_Jt", edit=True, zso=True,oj="xyz", sao="yup")
        
        self.EarJoint = cmds.joint(name="L_Ear_Tip_Jt", position=(7.515,13.229,-1.142))
        cmds.joint(name="L_Ear_Tip_Jt", edit=True, zso=True,oj="xyz", sao="yup")    

    def _Ears_R(self):
        cmds.select("Head_Jt")
        
        self.EarJoint = cmds.joint(name="R_Ear_Jt", position=(7.71,12.503, 0.896))
        cmds.joint(name="R_Ear_Jt", edit=True, zso=True,oj="xyz", sao="yup")
        
        self.EarJoint = cmds.joint(name="R_Ear_Tip_Jt", position=(7.515,13.229, 1.142))
        cmds.joint(name="R_Ear_Tip_Jt", edit=True, zso=True,oj="xyz", sao="yup")  
    
    # Jaw Skeleton
    def __Jaw__(self):
	
        cmds.select("Head_Jt")
        self.LowerJawJoint = cmds.joint(name = "Lower_Jaw_Jt",position=(7.723,10.89,0.0))
        cmds.joint(name="Lower_Jaw_Jt",edit=True, zso=True, oj="xyz", sao="yup")
        self.TipJawJoint = cmds.joint(name = "Tip_Jaw_Jt",position=(10.119,9.707,0.019))
        cmds.joint(name="Tip_Jaw_Jt",edit=True, zso=True, oj="xyz", sao="yup")
        
    def __Tongue__(self):
	
        cmds.select("Lower_Jaw_Jt")
        self.FirstTongueJoint = cmds.joint(name="First_Tongue_Jt", position =(8.106,11.268,0.0))
        cmds.joint(name="First_Tongue_Jt",edit=True, zso=True, oj="xyz", sao="yup")
        self.SecondTongueJoint = cmds.joint(name="Second_Tongue_Jt", position =(8.524,11.148,0.0))
        cmds.joint(name="Second_Tongue_Jt",edit=True, zso=True, oj="xyz", sao="yup")
        self.ThirdTongueJoint = cmds.joint(name="Third_Tongue_Jt", position =(8.838,10.949,0.0))
        cmds.joint(name="Third_Tongue_Jt",edit=True, zso=True, oj="xyz", sao="yup")
        self.FourthTongueJoint = cmds.joint(name="Fourth_Tongue_Jt", position =(9.162,10.698,0.0))
        cmds.joint(name="Fourth_Tongue_Jt",edit=True, zso=True, oj="xyz", sao="yup")
        self.FifthTongueJoint = cmds.joint(name="Fifth_Tongue_Jt", position =(9.47,10.426,0.0))
        cmds.joint(name="Fifth_Tongue_Jt",edit=True, zso=True, oj="xyz", sao="yup")
		



    def __create__(*args):
        skeletonQT = CreateSkeletonQ()
        skeletonQT._CreateFrontLegsSkeleton_L()
        skeletonQT._CreateFrontLegsSkeleton_R()
        skeletonQT.__CreateSpineSkeleton__()
        skeletonQT._CreateBackLegsSkeleton_L()
        skeletonQT._CreateBackLegsSkeleton_R()
        skeletonQT.__Tail__()
        skeletonQT.__Head__()
        skeletonQT.__Jaw__()
        skeletonQT._Ears_L()
        skeletonQT._Ears_R()
        skeletonQT.__Tongue__()


####### JointTab #######   
class JointTab():

    def create_joints():
        cmds.snapMode(cmds = True)
        cmds.setToolTo('jointContext')

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

    def joint_scale():

        scale_var = cmds.floatSliderGrp(jointScaleVar, query = True, value = True)

        cmds.jointDisplayScale(scale_var)

    def showLabels():

        mel.eval('displayJointLabels 2;')

    def quick_label():

        prefix = cmds.checkBox(usePrefixVar, query=True,value=True)
        selectedObject = cmds.ls(sl=True)
        labelType = cmds.optionMenu(labelTypeVar, query = True, value = True)
        label = 3

        if labelType == 'Center':
            label = 0
        elif labelType == 'Left':
            label = 1
        elif labelType == 'Right':
            label = 2
        else:
            label = 3

        try:
            List = cmds.listRelatives(selectedObject, ad=True, typ='joint')+selectedObject
        except:
            List = selectedObject

        for obj in List:
            name = ''.join(obj)
            cmds.setAttr(name+'.drawLabel', True)
            cmds.setAttr(name+'.type', 18)
            cmds.setAttr(name+'.otherType', name, type = 'string')
            if prefix == True:
                if 'lt_' in name:
                    cmds.setAttr(name+'.side', 1)
                elif 'rt_' in name:
                    cmds.setAttr(name+'.side', 2)
                elif 'ct_' in name:
                    cmds.setAttr(name+'.side', 0)
                else:
                    cmds.setAttr(name+'.side', label)
            else:
                cmds.setAttr(name+'.side', label)

    def select_label():

        jointLabelName = cmds.textFieldGrp(jointLabelVar, query = True, text = True)
        labelType = cmds.optionMenu(labelTypeVar, query = True, value = True)
        prefix = cmds.checkBox(usePrefixVar, query=True,value=True)
        label = 3

        if labelType == 'Center':
            label = 0
        elif labelType == 'Left':
            label = 1
        elif labelType == 'Right':
            label = 2
        else:
            label = 3

        selectedObj = cmds.ls(sl=True)

        for obj in selectedObj:
            name = ''.join(obj)
            cmds.setAttr(name+'.drawLabel', True)
            cmds.setAttr(name+'.type', 18)
            cmds.setAttr(name+'.otherType', jointLabelName, type = 'string')
            if prefix == True:
                if 'lt_' in name:
                    cmds.setAttr(name+'.side', 1)
                elif 'rt_' in name:
                    cmds.setAttr(name+'.side', 2)
                elif 'ct_' in name:
                    cmds.setAttr(name+'.side', 0)
                else:
                    cmds.setAttr(name+'.side', label)
            else:
                cmds.setAttr(name+'.side', label)

    def get_joint_orientation():
        selection = cmds.ls(sl=True)

        if len(selection) >= 2:
            selection = selection[0]

        name = ''.join(selection[0])
        orientationX = cmds.getAttr(name+'.jointOrientX')
        orientationY = cmds.getAttr(name+'.jointOrientY')
        orientationZ = cmds.getAttr(name+'.jointOrientZ')
        cmds.floatSliderGrp(JOrientationX, edit = True, value = orientationX)
        cmds.floatSliderGrp(JOrientationY, edit = True, value = orientationY)
        cmds.floatSliderGrp(JOrientationZ, edit = True, value = orientationZ)

    def orient_joints():
        orientation = cmds.optionMenu(JointOrientation, query = True, value = True)

        if orientation == 'yxz':
            mel.eval('joint -e  -oj yxz -secondaryAxisOrient xup -ch -zso;')
        elif orientation == 'xyz':
            mel.eval('joint -e  -oj xyz -secondaryAxisOrient xup -ch -zso;')
        elif orientation == 'yzx':
            mel.eval('joint -e  -oj yzx -secondaryAxisOrient xup -ch -zso;')
        elif orientation == 'zxy':
            mel.eval('joint -e  -oj zxy -secondaryAxisOrient xup -ch -zso;')
        elif orientation == 'zyx':
            mel.eval('joint -e  -oj zyx -secondaryAxisOrient xup -ch -zso;')
        else:
            mel.eval('joint -e  -oj xzy -secondaryAxisOrient xup -ch -zso;')

    def custom_joints_orientation(axis):
        orientationX = cmds.floatSliderGrp(JOrientationX, query = True, value = True)
        orientationY = cmds.floatSliderGrp(JOrientationY, query = True, value = True)
        orientationZ = cmds.floatSliderGrp(JOrientationZ, query = True, value = True)

        selection = cmds.ls(sl=True)

        if axis == "x":
            for obj in selection:
                name = ''.join(obj)
                cmds.setAttr(name+'.jointOrientX',orientationX)
        elif axis == "y":
            for obj in selection:
                name = ''.join(obj)
                cmds.setAttr(name+'.jointOrientY',orientationY)
        elif axis == "z":
            for obj in selection:
                name = ''.join(obj)
                cmds.setAttr(name+'.jointOrientZ',orientationZ)

    def mirror_joints():
        axis = cmds.optionMenu(MirrorAxis,query=True,value=True)
        selection = cmds.ls(sl=True)

        for obj in selection:
            if axis == "YZ":
                cmds.mirrorJoint(obj,mirrorYZ=True,mirrorBehavior= True)
            elif axis == "XY":
                cmds.mirrorJoint(obj,mirrorXY=True,mirrorBehavior= True)
            elif axis == "XZ":
                cmds.mirrorJoint(obj,mirrorXZ=True,mirrorBehavior= True)
            else:
                return
            
    #################### insert joint tool ####################
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
                        JointTab.SetJointPosition(joints[0], insert_between_jnt, end_jnt, number_jnt)
                else:    
                    joints_number = 1

                    for i in range(0, joints_number):
                        if i > 0:
                            end_jnt = cmds.listRelatives(insert_between_jnt, children=True, f=True)[0]

                        number_jnt = JointTab.getSliderValue(positionFloatSlider)

                        radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt)) / 2

                    
                        # create the inbetween joint
                        insert_between_jnt = cmds.joint(rad=radius)

                        JointTab.SetJointPosition(joints[0], insert_between_jnt, end_jnt, number_jnt)


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

                            JointTab.SetJointPosition(joints[0], insert_between_jnt, end_jnt, number_jnt_2)
                    else:    
                        joints_number = 1

                        for i in range(0, joints_number):

                            if i > 0:
                                end_jnt = cmds.listRelatives(insert_between_jnt, children=True, f=True)[0]
                            number_jnt_2 = JointTab.getSliderValue(positionFloatSlider)
                            radius = (cmds.getAttr("%s.radius" % joints[0]) + cmds.getAttr("%s.radius" % end_jnt)) / 2


                            insert_between_jnt = cmds.joint(rad=radius)
                            JointTab.SetJointPosition(joints[0], insert_between_jnt, end_jnt, number_jnt_2)
            else:
                cmds.warning("First joint must be a direct parent of the second joint")

        # if more than two joints selected
        if len(joints) > 2:
            cmds.warning("only select 1 or 2 joints")

    def getSliderValue(slider):
        return cmds.floatSliderGrp(slider, q=1, v=1)


########## FK Tab ##########
class FK_Tab():
    
    def create_controller():
        
        rValue = cmds.floatSliderGrp(rVar, query = True, value = True)
        xValue = cmds.floatSliderGrp(xVar, query = True, value = True)
        yValue = cmds.floatSliderGrp(yVar, query = True, value = True)
        zValue = cmds.floatSliderGrp(zVar, query = True, value = True)
        colorValue = cmds.colorSliderGrp(FK_color_slider, query = True, rgb = True)
        controllerList = []
        #get selected joints name
        selectObjs = cmds.ls(sl = True)
        for obj in range(0,len(selectObjs)):
            convertedList = ''.join(selectObjs[obj])
            controllerName = convertedList + '_ctrl'

            #setting up other variables
            group01Name = controllerName + '_grp01'
            creationNodeName = controllerName + '_creation'
            shapeNodeName = controllerName + 'Shape'
            
            #create controller
            cmds.circle(n = controllerName, r = rValue, nrx = xValue, nry = yValue, nrz = zValue)
            cmds.select(controllerName)
            cmds.group(n=group01Name)

            #get and set transformations for the controller groups
            cmds.parentConstraint(selectObjs[obj], group01Name, w=1, mo=0)
            cmds.delete(group01Name+'_parentConstraint1')
            #adding a parent constrain
            cmds.parentConstraint(controllerName, selectObjs[obj], w=1, mo=0)

            #cleaning node name
            cmds.rename('makeNurbCircle1',creationNodeName)

            #select actual controller
            controllerList.append(controllerName)

            #enable color override for advanced options
            cmds.setAttr(shapeNodeName+'.overrideEnabled', True)
            cmds.setAttr(shapeNodeName+'.overrideRGBColors', True)
            cmds.setAttr(shapeNodeName+'.useOutlinerColor', True)

            cmds.setAttr(shapeNodeName+'.overrideColorRGB', colorValue[0], colorValue[1], colorValue[2])
           
        cmds.select(clear=True)
        for i in range(0,len(controllerList)):
            cmds.select(controllerList[i], add=True)


    def set_parent_controller_FK():

        weightVar = cmds.floatSliderGrp(parentWeightVarFK, query=True,value=True)
        selectObjs = cmds.ls(sl=True)
        for i in range(0,len(selectObjs)-1):
            childGrp = ''.join(selectObjs[i])+'_grp01'
            parentObj = ''.join(selectObjs[i+1])        
            cmds.parentConstraint(parentObj, childGrp, w=weightVar, mo=1)

    def change_radius():
        rUpdate = cmds.floatSliderGrp(rVar, query = True, value = True)
        controller = cmds.ls (sl = True)
        for obj in controller:
            convertedList = ''.join(obj)
            attrName = convertedList + '_creation.radius'

            if cmds.objExists(attrName):
                cmds.setAttr(attrName,rUpdate)
            else:
                return

    def changeX():
        xUpdate = cmds.floatSliderGrp(xVar, query = True, value = True)
        controller = cmds.ls (sl = True)
        for obj in range(0,len(controller)):
            convertedList = ''.join(controller[obj])
            attrName = convertedList + '_creation.normalX'

            if cmds.objExists(attrName):
                cmds.setAttr(attrName,xUpdate)
            else:
                return

    def changeY():
        yUpdate = cmds.floatSliderGrp(yVar, query = True, value = True)
        controller = cmds.ls (sl = True)
        for obj in range(0,len(controller)):
            convertedList = ''.join(controller[obj])
            attrName = convertedList + '_creation.normalY'

            if cmds.objExists(attrName):
                cmds.setAttr(attrName,yUpdate)
            else:
                return

    def changeZ():
        zUpdate = cmds.floatSliderGrp(zVar, query = True, value = True)
        controller = cmds.ls (sl = True)
        for obj in range(0,len(controller)):
            convertedList = ''.join(controller[obj])
            attrName = convertedList + '_creation.normalZ'

            if cmds.objExists(attrName):
                cmds.setAttr(attrName,zUpdate)
            else:
                return

    def zero_out():
        defaultAttr = {'sx':1, 'sy':1, 'sz':1, 'rx':0, 'ry':0, 'rz':0, 'tx':0, 'ty':0, 'tz':0}
        allControlls = cmds.ls(sl=1)
        for obj in allControlls:
            for attr in defaultAttr:
                try:
                    cmds.setAttr('%s.%s'%(obj, attr), defaultAttr[attr])
                except:
                    pass
                
    def FK_change_color():
        colorValue = cmds.colorSliderGrp(FK_color_slider, query = True, rgb = True)

        selectObjs = cmds.ls(sl = True)

        for obj in selectObjs:
            shapeNodeName = obj + 'Shape'
            cmds.setAttr(shapeNodeName+'.overrideColorRGB', colorValue[0], colorValue[1], colorValue[2])


########## Controller Group ##########
class ControllerGroup():

    def make_star():
        #get vertices
        selectedObjects = cmds.ls(sl=True)
        for obj in range(0,len(selectedObjects)):
            manipulator01 = ''.join(selectedObjects[obj])+'.cv[0]'
            manipulator02 = ''.join(selectedObjects[obj])+'.cv[2]'
            manipulator03 = ''.join(selectedObjects[obj])+'.cv[4]'
            manipulator04 = ''.join(selectedObjects[obj])+'.cv[6]'

            #select vertices
            starVertices = cmds.ls(manipulator01,manipulator02,manipulator03,manipulator04)
            #scale
            cmds.scale(0,0,0,starVertices,a=True)


########## IK Tab ##########
class IK_Tab():

    def set_parent_controller_IK():
        weightVar = cmds.floatSliderGrp(parentWeightVarIK, query=True,value=True)
        selectObjs = cmds.ls(sl=True)
        for i in range(0,len(selectObjs)-1):
            childGrp = ''.join(selectObjs[i])+'_grp01'
            parentObj = ''.join(selectObjs[i+1])        
            cmds.parentConstraint(parentObj, childGrp, w=weightVar, mo=1)

    def Ik_controller():
        rValueIK = cmds.floatSliderGrp(rVarIK, query = True, value = True)
        xValueIK = cmds.floatSliderGrp(xVarIK, query = True, value = True)
        yValueIK = cmds.floatSliderGrp(yVarIK, query = True, value = True)
        zValueIK = cmds.floatSliderGrp(zVarIK, query = True, value = True)
        colorValue = cmds.colorSliderGrp(IK_color_slider, query = True, rgb = True)
        rCheck = cmds.checkBoxGrp(RotationCheck, query = True, v1 = True)
        spsCheck = cmds.checkBoxGrp(RotationCheck, query = True, v2 = True)
        autoColor = cmds.checkBoxGrp(RotationCheck, query = True, v3 = True)
        
        #getting naming data and ik objects
        selectObj = cmds.ls(sl = True)
        ikPosition = selectObj[1]
        endEffector = selectObj[0]

        #creating IK handle
        if(spsCheck == True):
            mel.eval('ikSpringSolver;')
            cmds.ikHandle(sj=ikPosition,ee=endEffector,sol='ikSpringSolver')
        else:
            cmds.ikHandle(sj=ikPosition,ee=endEffector,sol='ikRPsolver')

        #getting names
        namingObj = selectObj.pop(0)
        convertedList = ''.join(namingObj)
        controllerName = convertedList + '_ctrl'
        ikHandleName = convertedList + '_ikHandle'
        group02Name = controllerName + '_grp01'
       
        creationNodeName = controllerName + '_creation'
        shapeNodeName = controllerName + 'Shape'

        #rename IK handle
        cmds.rename('ikHandle1', ikHandleName)
        
        #create controller
        cmds.circle(n = controllerName, r = rValueIK, nrx = xValueIK, nry = yValueIK, nrz = zValueIK)
        cmds.select(controllerName)
        cmds.group(n=group02Name)
        
        #get and set transformations for the controller groups
        cmds.parentConstraint(ikHandleName, group02Name, w=1, mo=0)
        cmds.delete(group02Name+'_parentConstraint1')

        #adding a parent constrain
        cmds.parentConstraint(controllerName, ikHandleName, w=1, mo=0)
        if rCheck == True:
            cmds.orientConstraint(controllerName, endEffector, w=1, mo=1)

        #cleaning node name
        cmds.rename('makeNurbCircle1', creationNodeName)
        cmds.select(controllerName)

        #enable color override for advanced options
        cmds.setAttr(shapeNodeName+'.overrideEnabled', True)
        cmds.setAttr(shapeNodeName+'.overrideRGBColors', True)
        cmds.setAttr(shapeNodeName+'.useOutlinerColor', True)

        get_select_name = cmds.ls(sl = True, long = True)
        print( get_select_name)

        if autoColor == True:
        
            if len(get_select_name) < 1:

                cmds.setAttr(shapeNodeName + '.overrideColorRGB', 1, 1, 1)
            elif len(get_select_name) > 1:
                cmds.setAttr(shapeNodeName + '.overrideColorRGB', 1, 1, 1)

        else:
            cmds.setAttr(shapeNodeName+'.overrideColorRGB', colorValue[0], colorValue[1], colorValue[2])

    def change_radius_IK():

        rUpdate = cmds.floatSliderGrp(rVarIK, query = True, value = True)
        controller = cmds.ls (sl = True)
        for obj in controller:
            convertedList = ''.join(obj)
            attrName = convertedList + '_creation.radius'

            if cmds.objExists(attrName):
                cmds.setAttr(attrName,rUpdate)
            else:
                return

    def changeX_IK():

        xUpdate = cmds.floatSliderGrp(xVarIK, query = True, value = True)
        controller = cmds.ls (sl = True)
        for obj in range(0,len(controller)):
            convertedList = ''.join(controller[obj])
            attrName = convertedList + '_creation.normalX'

            if cmds.objExists(attrName):
                cmds.setAttr(attrName,xUpdate)
            else:
                return

    def changeY_IK():

        yUpdate = cmds.floatSliderGrp(yVarIK, query = True, value = True)
        controller = cmds.ls (sl = True)
        for obj in range(0,len(controller)):
            convertedList = ''.join(controller[obj])
            attrName = convertedList + '_creation.normalY'

            if cmds.objExists(attrName):
                cmds.setAttr(attrName,yUpdate)
            else:
                return

    def changeZ_IK():

        zUpdate = cmds.floatSliderGrp(zVarIK, query = True, value = True)
        controller = cmds.ls (sl = True)
        for obj in range(0,len(controller)):
            convertedList = ''.join(controller[obj])
            attrName = convertedList + '_creation.normalZ'

            if cmds.objExists(attrName):
                cmds.setAttr(attrName,zUpdate)
            else:
                return
            

    def poleVectorMath(offset, jointNameEnd, jointNameMid, jointNameStart):
    
        start = cmds.xform(jointNameStart, q= True, ws = True, t=True)
        mid = cmds.xform(jointNameMid, q= True, ws = True, t=True)
        end = cmds.xform(jointNameEnd, q= True, ws = True, t=True)

        startV = om.MVector(start[0], start[1], start[2])
        midV = om.MVector(mid[0], mid[1], mid[2])
        endV = om.MVector(end[0], end[1], end[2])

        startEnd = endV - startV
        startMid = midV - startV

        dotP = startMid * startEnd

        proj = float(dotP)/float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj
        arrowV = startMid - projV
        arrowV*= offset
        finalV = arrowV + midV

        return finalV


    def pole_vectorC():
        colorValue = cmds.colorSliderGrp(IK_color_slider, query = True, rgb = True)
        offset = cmds.floatSliderGrp(OffsetVar, query = True, value = True)
        selectedObjects = cmds.ls(sl=True)
        locatorName = selectedObjects[0].replace('_ctrl', '_poleVector')
        ikHandleVar = selectedObjects[0].replace('_ctrl','_ikHandle')
        if len(selectedObjects) == 3:
            poleVectorPos = IK_Tab.poleVectorMath(offset, selectedObjects[0].replace('_ctrl',''), selectedObjects[1], selectedObjects[2])
        elif len(selectedObjects) == 1:
            jointNameEnd = selectedObjects[0].replace('_ctrl','')
            jointNameMid = cmds.listRelatives(jointNameEnd, p=True)
            jointNameStart = cmds.listRelatives(jointNameMid, p=True)
            poleVectorPos = IK_Tab.poleVectorMath(offset, jointNameEnd, jointNameMid, jointNameStart)
        else:
            cmds.warning('ERROR: invalid selection! please select either 1 IK controller OR 3 objects')
            return
        shapeNodeName = locatorName+'Shape'
        group01Name = locatorName + '_grp01'
        group02Name = locatorName + '_grp02'
        cmds.spaceLocator(n = locatorName)[0]
        cmds.select(locatorName)
        cmds.group(n=group01Name)
        cmds.select(group01Name)
        locGrp = cmds.group(n=group02Name)

        cmds.xform(locGrp, ws=True, t=(poleVectorPos.x, poleVectorPos.y, poleVectorPos.z))

        cmds.poleVectorConstraint(locatorName,ikHandleVar)
        cmds.select(locatorName)

        #enable color override for advanced options
        cmds.setAttr(shapeNodeName+'.overrideEnabled', True)
        cmds.setAttr(shapeNodeName+'.overrideRGBColors', True)
        cmds.setAttr(shapeNodeName+'.useOutlinerColor', True)
        cmds.setAttr(shapeNodeName+'.overrideColorRGB', colorValue[0], colorValue[1], colorValue[2])


    def pole_vector_offset():
        offset = cmds.floatSliderGrp(OffsetVar, query = True, value = True)
        selectedObjects = cmds.ls(sl=True)
        locatorName = selectedObjects[0]
        if len(selectedObjects) == 4:
            poleVectorPos = IK_Tab.poleVectorMath(offset, selectedObjects[1].replace('_ctrl',''), selectedObjects[2], selectedObjects[3])
        elif len(selectedObjects) == 2:
            jointNameEnd = selectedObjects[1].replace('_ctrl','')
            jointNameMid = cmds.listRelatives(jointNameEnd, p=True)
            jointNameStart = cmds.listRelatives(jointNameMid, p=True)
            poleVectorPos = IK_Tab.poleVectorMath(offset, jointNameEnd, jointNameMid, jointNameStart)
        else:
            return
        
        shapeNodeName = locatorName+'Shape'
        group02Name = locatorName + '_grp02'
        
        cmds.xform(group02Name, ws=True, t=(poleVectorPos.x, poleVectorPos.y, poleVectorPos.z))

    def IK_change_color():
        colorValue = cmds.colorSliderGrp(IK_color_slider, query = True, rgb = True)

        selectObjs = cmds.ls(sl = True)

        for obj in selectObjs:
            shapeNodeName = obj + 'Shape'
            cmds.setAttr(shapeNodeName+'.overrideColorRGB', colorValue[0], colorValue[1], colorValue[2])


class FK_IK_Switch():
    
    def select_original_joints():
        select_objects = cmds.ls(sl=True, type='joint')
        return select_objects
    
    
    def rename_joint(joint, suffix_name):

        new_name = joint + suffix_name
        cmds.rename(joint, new_name)
        return new_name

    ########## fk chain ##########
    def FK_IK_chain():
        # select_objects = cmds.ls(sl=True, type='joint')
        get_select_original_joints = FK_IK_Switch.select_original_joints()
        
        if not get_select_original_joints:
            raise Exception("No joints selected. Please select a joint chain.")
    
        original_joints_list = []
        original_joints_list.append(get_select_original_joints)

        print(original_joints_list)
        duplicated_joints_fk = cmds.duplicate(get_select_original_joints, rc=True)
        # duplicated_joints_fk = cmds.duplicate(get_select_original_joints, po=True)

        fk_controller_grp = cmds.group(em = True, n = "FK_Ctl_Grp")

        controls = []
        
        fk_chain_list = []

        for fk_chain in duplicated_joints_fk:
            generate_fk = FK_IK_Switch.rename_joint(fk_chain, "_fk")    
            
            fk_chain_list.append(generate_fk)

            position = cmds.xform(generate_fk, query=True, worldSpace=True, translation=True)
            
            controller = cmds.circle(name= generate_fk + "_ctrl", normal=[1, 0, 0], radius=0.5)[0]

            cmds.move(position[0], position[1], position[2], controller)

            orientation = cmds.xform(generate_fk, query=True, worldSpace=True, rotation=True)
            
            cmds.rotate(orientation[0], orientation[1], orientation[2], controller)

            controller_constraint = cmds.parentConstraint(controller, generate_fk, maintainOffset=True)

            cmds.parent(controller, fk_controller_grp) 

            controls.append(controller)

        start_joint_fk = fk_chain_list[0]
        end_joint_fk = fk_chain_list[-1]
        
        for i, controller in enumerate(controls):
            if i != 0:  
                cmds.parent(controller, controls[i - 1])

        #####
        fk_joints = fk_chain_list
        fk_controller = controls
        
        ###### ik chain ######
        
        duplicated_joints_ik = cmds.duplicate(get_select_original_joints, rc=True)
        # duplicated_joints_ik = cmds.duplicate(get_select_original_joints, po=True)

        ik_chain_list = []
        ik_controller_list = []

        for ik_chain in duplicated_joints_ik:
            ik_chain_rename = FK_IK_Switch.rename_joint(ik_chain, "_ik")
            
            ik_chain_list.append(ik_chain_rename)

        start_joint = ik_chain_list[0]
        end_joint = ik_chain_list[-1]
        

        ik_handle, effector = cmds.ikHandle( startJoint = start_joint, endEffector = end_joint)

        start_ctrl = cmds.circle(name = "iK_ctrl")[0]

        end_ctrl = cmds.circle(name = end_joint + "_ctrl", radius=0.2)[0]

        cmds.delete(cmds.pointConstraint(start_joint, start_ctrl))
        cmds.delete(cmds.pointConstraint(end_joint, end_ctrl))
        cmds.delete(start_ctrl)

        cmds.parent(ik_handle, end_ctrl)

        ### pole vector controller ###
        get_middle_index = ik_chain_list[1]
        select_middle_joint = cmds.select(get_middle_index)
        middle_pos = cmds.xform(get_middle_index, query=True, worldSpace=True, translation=True)
        
        pole_vector_ctrl = cmds.spaceLocator( name="poleVector_ctrl")[0]
        cmds.move(middle_pos[0] - 2, middle_pos[1], middle_pos[2], pole_vector_ctrl)
        cmds.poleVectorConstraint(pole_vector_ctrl, ik_handle)
        cmds.makeIdentity(pole_vector_ctrl, apply=True, translate=True, rotate=True, scale=True)
        
        ik_controller_list.append(end_ctrl)
        ik_controller_list.append(ik_handle)
        ik_controller_list.append(effector)
        ik_controller_list.append(pole_vector_ctrl)

        root_group = cmds.group(em = True, name="IK_pole_vector_Grp")
        cmds.parent(pole_vector_ctrl, "IK_pole_vector_Grp")
        
        cmds.group(em=True, name="IK_Ctl_Grp")
        cmds.parent(end_ctrl, "IK_Ctl_Grp")
        
        ik_data = ik_chain_list + ik_controller_list
          
        ###IK_FK Controller locator
        locator = cmds.spaceLocator(name="FKIK_Switch")[0]
        cmds.addAttr(locator, longName='IKFK_Switch', attributeType='enum', enumName='IK:FK', keyable=True )
        

        # FK_IK_Switch.switch_fk_visibility(locator, original_joints_list[0], fk_joints, fk_controller)
        FK_IK_Switch.switch_fk_visibility(locator, fk_joints, fk_controller, ik_data, original_joints_list[0])

    
    def switch_fk_visibility(switch_locator, fk_joints, fk_controller, ik_data, original_joints):
        switch_attribute = switch_locator +  ".IKFK_Switch"
        
        def fk_visibility_switch(*args):
            if cmds.getAttr(switch_attribute):
                
                for joint in original_joints:
                    cmds.setAttr(joint + ".visibility", 0)
                    
                for ik_joint in ik_data:
                    cmds.setAttr(ik_joint + ".visibility", 0)
                
                for joint in fk_joints:      
                    cmds.setAttr(joint + ".visibility", 1)
                for control in fk_controller:
                    cmds.setAttr(control + ".visibility", 1)
                
                    
            else:
                for joint in original_joints:
                    cmds.setAttr(joint + ".visibility", 0)
                
                for ik_joint in ik_data:
                    cmds.setAttr(ik_joint + ".visibility", 1)
                for joint in fk_joints:      
                    cmds.setAttr(joint + ".visibility", 0)
                for control in fk_controller:
                    cmds.setAttr(control + ".visibility", 0)
                
        cmds.scriptJob(attributeChange=[switch_attribute, fk_visibility_switch])
    
        



##################### mainwindow #################################

cmds.inViewMessage( amg= "Welcome to the Tom's Auto Rig 3.0", pos='midCenter', fade=True )

if cmds.window("Window", exists = True):
    cmds.deleteUI("Window")
    
#Global Joint Axis
x = 'x'
y = 'y'
z = 'z'

controllerWindow = cmds.window("Window", title = "Tom's AutoRig 3.0", widthHeight=(250, 800))
cmds.columnLayout( adjustableColumn=True )

tabs = cmds.tabLayout(w=250, h=900)

###Joints Tab###
jointTab = cmds.scrollLayout (horizontalScrollBarThickness = 10, verticalScrollBarThickness = 16)

cmds.separator(h = 5, st = 'none')
cmds.text("Select Preset Skeleton or Click Create Custom Joints", al = "center")
cmds.separator(h = 10, st = 'none')
cmds.button(label = "Create Biped Skeleton", w=325, h=25, bgc = [0.5,0.5,0.5], c = "CreateSkeletonB.__create__()" )
cmds.separator(h = 10, st = 'none')
cmds.button(label = "Create Quadruped Skeleton", w=325, h=25, bgc = [0.5,0.5,0.5], c = "CreateSkeletonQ.__create__()" )
cmds.separator(h = 10, st = 'none')

cmds.button(label = "Create Custom Joints", ann = "Creates joints on mesh center tool", w=325, h=25, bgc = [0.5,0.5,0.5], c = "JointTab.create_joints()")

cmds.separator(h = 10, st = 'none')
cmds.text("Select One or Multiple Joint, then Rename Joint", al = "center")
cmds.button(label = "Rename", w=325, h=25, bgc = [0.5,0.5,0.5], c = "JointTab.full_rename_numerals_object()" )

cmds.separator(h = 10, st = 'none')

cmds.text(label='Joint Size:', h = 25)

jointScaleVar = cmds.floatSliderGrp(min = 0.1, max = 5, v = 1, field=True, changeCommand = 'JointTab.joint_scale()', dragCommand= "JointTab.joint_scale()")

cmds.separator(h = 10)


cmds.text("Select a Joint, Add New Joint Between Select Joints Position ", al="center")
cmds.separator(h = 10)
positionFloatSlider = cmds.floatSliderGrp(min=0.1, max=0.9,  field=True)
cmds.separator(h = 10)
insert_Button_1 = cmds.button(l="Run", al="center",w=325, h=25, bgc = [0.5,0.5,0.5], c= lambda self: JointTab.InsertJoint(self, 0))
cmds.separator(h = 10)
cmds.text("Select a Joint, Add Number of Joint Between Select Joint", al="center")
cmds.separator(h = 10)
joint_number_input = cmds.intField(min=2, max=50)
cmds.separator(h = 10)

insert_Button_2 = cmds.button(label="Run", al="center", w=325, h=25, bgc = [0.5,0.5,0.5], c= partial(JointTab.InsertJoint, 1))
cmds.separator(h = 10)

cmds.text(label='Custom Joint Orientation:',h=25)
cmds.text(label="X Orientation:",h=25)
JOrientationX = cmds.floatSliderGrp(min = -360, max = 360, v = 0, field=True, changeCommand = "JointTab.custom_joints_orientation(x)", dragCommand= "JointTab.custom_joints_orientation(x)")
cmds.text(label="Y Orientation:",h=25)
JOrientationY = cmds.floatSliderGrp(min = -360, max = 360, v = 0, field=True, changeCommand = "JointTab.custom_joints_orientation(y)", dragCommand= "JointTab.custom_joints_orientation(y)")
cmds.text(label="Z Orientation:",h=25)
JOrientationZ = cmds.floatSliderGrp(min = -360, max = 360, v = 0, field=True, changeCommand = "JointTab.custom_joints_orientation(z)", dragCommand= "JointTab.custom_joints_orientation(z)")
cmds.separator(h = 15)

cmds.text(label='Orientation:', h = 25)
JointOrientation = cmds.optionMenu(w = 325, h=25, bgc = [0.5,0.5,0.5])
cmds.menuItem(l="YXZ")
cmds.menuItem(l="XYZ")
cmds.menuItem(l="YZX")
cmds.menuItem(l="ZXY")
cmds.menuItem(l="ZYX")
cmds.menuItem(l="XZY")
cmds.separator(h = 15, st = 'none')
cmds.button(label = "Orient Joint", ann = "Orient joint Y = Up, Z = Front", w=325, h=25, bgc = [0.5,0.5,0.5], c = 'JointTab.orient_joints()')
cmds.separator(h = 15, st = 'none')

cmds.text(label='Mirror Joints:', h = 25)
cmds.text(label='Mirror Axis:', h = 25)
MirrorAxis = cmds.optionMenu(w = 325, h=25, bgc = [0.5,0.5,0.5])
cmds.menuItem(l="YZ")
cmds.menuItem(l="XY")
cmds.menuItem(l="XZ")
cmds.separator(h = 15)
cmds.button(label = "Mirror Joints", ann = "select a Joint and press this button to mirror it along the selected axis", w=325, h=25, bgc = [0.5,0.5,0.5], c = 'JointTab.mirror_joints()')
cmds.separator(h = 25)

cmds.text(label="Joint Label:", h = 25)
jointLabelVar = cmds.textFieldGrp(text='Label',h=20,w=325)
cmds.separator(h = 5, st="none")

cmds.text(label='Label Side:', h = 25)
labelTypeVar = cmds.optionMenu(w = 325, h=25, bgc = [0.5,0.5,0.5])
cmds.menuItem(l="None")
cmds.menuItem(l="Center")
cmds.menuItem(l="Left")
cmds.menuItem(l="Right")
usePrefixVar = cmds.checkBox(l='Use Prefix', w= 325, h = 25)
cmds.separator(h = 10, st = 'none')
cmds.button(label = "Create Custom Label", ann = "Creates label for selected Joints based on a string", w=325, h=25, bgc = [0.5,0.5,0.5], c = 'JointTab.select_label()')
cmds.separator(h = 10, st = 'none')
cmds.button(label = "Create Quick Label", ann = "Creates label for selected Joints based on their names", w=325, h=25, bgc = [0.5,0.5,0.5], c = 'JointTab.quick_label()')
cmds.separator(h = 10)
cmds.button(label = "Show/Hide Label", ann = "toggles label visability", w=325, h=25, bgc = [0.5,0.5,0.5], c = 'JointTab.showLabels()')
cmds.separator(h = 15)
cmds.setParent('..')


########## FK Tab ##########
FKTab = cmds.rowColumnLayout (numberOfColumns = 1)
cmds.separator(h = 10)
cmds.text(label='Select Joint Chain, and Click the Button', h = 15)
cmds.separator(h = 10)
cmds.select(cl = True)
cmds.button(label = "Create FK / IK Switch", w = 325, h = 25, bgc = [0.5, 0.5, 0.5], c = "FK_IK_Switch.FK_IK_chain()")
cmds.separator(h = 10)
cmds.text(label='Select a Joint, and Create FK Controller', h = 15)
cmds.separator(h = 10)
cmds.button(label = "Create FK Controller", ann = "confirm creation", w = 325, h = 25, bgc = [0.5, 0.5, 0.5], c = "FK_Tab.create_controller()")

cmds.separator(h = 15)
cmds.text(label='Controller Color:', h = 15)
FK_color_slider = cmds.colorSliderGrp(rgb=(1, 0, 0), columnWidth=(5, 30), changeCommand = "FK_Tab.FK_change_color()")
cmds.separator(h = 15)
cmds.text(label='Radius:', h = 15)
rVar = cmds.floatSliderGrp(min = 0.1, max = 10, v = 1, field=True, changeCommand = "FK_Tab.change_radius()", dragCommand= "FK_Tab.change_radius()")
cmds.separator(h = 15)
cmds.text(label='X Orientation:', h = 15)
xVar = cmds.floatSliderGrp(min = -1, max = 1, v = 0, field=True, changeCommand = 'FK_Tab.changeX()', dragCommand= 'FK_Tab.changeX()')
cmds.text(label='Y Orientation:', h = 15)
yVar = cmds.floatSliderGrp(min = -1, max = 1, v = 1, field=True, changeCommand = 'FK_Tab.changeY()', dragCommand= 'FK_Tab.changeY()')
cmds.text(label='Z Orientation:', h = 15)
zVar = cmds.floatSliderGrp(min = -1, max = 1, v = 0, field=True, changeCommand = 'FK_Tab.changeZ()', dragCommand= 'FK_Tab.changeZ()')
cmds.separator(h = 15)
cmds.text(label='Parent Weight:', h = 25)
parentWeightVarFK = cmds.floatSliderGrp(min = 0, max = 1, v = 1, field=True)
cmds.separator(h=10, st='none')
cmds.text(label='select the child first, then the parent', h = 30)
cmds.button(label = "Set Parent", ann = "define parent controller", w=325, h=25, bgc = [0.5,0.5,0.5], c = "FK_Tab.set_parent_controller_FK()")
cmds.separator(h = 15)
cmds.button(label = "Zero Out", ann = "zero out all selected controller", w=325, h=25, bgc = [0.5,0.5,0.5], c = "FK_Tab.zero_out()")
cmds.separator(h = 15)
cmds.text(label='Change Controller Shader:', h = 25)
cmds.button(label = "Star", ann = "changes the controller into a star", w=325, h=25, bgc = [.5,.5,.5], c = "ControllerGroup.make_star()")
cmds.separator(h = 20)
cmds.setParent('..')

########## IK Tab ##########
IKTab = cmds.rowColumnLayout (numberOfColumns = 1)
cmds.separator(h = 10)
cmds.text(label='Select Joint Chain, and Click the Button', h = 15)
cmds.separator(h = 10)
cmds.button(label = "Create FK / IK Switch", w = 325, h = 25, bgc = [0.5, 0.5, 0.5], c = "FK_IK_Switch.FK_IK_chain()")
cmds.separator(h = 10)
cmds.text(label='Select a Parent and Child Joint, and Create FK Controller', h = 15)
cmds.separator(h = 10)
cmds.button(label = "Create IK Controller", ann = "confirm creation", w = 325, h = 25, bgc = [.5, .5, .5], c = "IK_Tab.Ik_controller()" )
cmds.separator(h = 10)
RotationCheck = cmds.checkBoxGrp(numberOfCheckBoxes=3,labelArray3 = ['Include Rotation','Spring Solver','Auto Colorize'], w= 325, h = 25)
cmds.separator(h = 10)
IK_color_slider = cmds.colorSliderGrp(rgb=(1, 0, 0), columnWidth=(5, 30), changeCommand = "IK_Tab.IK_change_color()")
cmds.separator(h = 15)
cmds.text(label='Radius:', h = 15)
rVarIK = cmds.floatSliderGrp(min = 0.1, max = 100, v = 1, field=True, changeCommand = "IK_Tab.change_radius_IK()", dragCommand= "IK_Tab.change_radius_IK()")
cmds.separator(h = 15)
cmds.text(label='X Orientation:', h = 15)
xVarIK = cmds.floatSliderGrp(min = -1, max = 1, v = 0, field=True, changeCommand = 'IK_Tab.changeX_IK()', dragCommand= 'IK_Tab.changeX_IK()')
cmds.text(label='Y Orientation:', h = 15)
yVarIK = cmds.floatSliderGrp(min = -1, max = 1, v = 1, field=True, changeCommand = 'IK_Tab.changeY_IK()', dragCommand= 'IK_Tab.changeY_IK()')
cmds.text(label='Z Orientation:', h = 15)
zVarIK = cmds.floatSliderGrp(min = -1, max = 1, v = 0, field=True, changeCommand = 'IK_Tab.changeZ_IK()', dragCommand= 'IK_Tab.changeZ_IK()')
cmds.separator(h = 15)
cmds.text(label='select the IK controller and choose your offset.', h = 25)
cmds.separator(h = 15)
cmds.text(label='Offset:', h = 25)
OffsetVar = cmds.floatSliderGrp(min = 0.0, max = 10, v = 1, field=True, changeCommand = "IK_Tab.pole_vector_offset()", dragCommand= "IK_Tab.pole_vector_offset()" )
cmds.separator(h = 25, st='none')
cmds.button(label = "Pole Vector", ann = "creates a pole Vector at the correct position", w=325, h=25, bgc = [.5,.5,.5], c = "IK_Tab.pole_vectorC()")
cmds.separator(h = 15)
cmds.text(label='Parent Weight:', h = 25)
parentWeightVarIK = cmds.floatSliderGrp(min = 0, max = 1, v = 1, field=True)
cmds.separator(h = 10,st='none')
cmds.button(label = "Set Parent", ann = "define parent controller", w=325, h=25, bgc = [.5,.5,.5], c = "IK_Tab.set_parent_controller_IK()" )
cmds.setParent('..')




cmds.tabLayout(tabs, edit=True, tabLabel= ( (jointTab, 'Joints Set Up'), (FKTab, 'FK Set Up') , (IKTab, 'IK Set Up')) )

cmds.showWindow("Window")