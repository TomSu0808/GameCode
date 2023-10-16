import maya.cmds as base
import Locators
import Joints
import SecondaryLocators as SL
import Controller
import Constraints
import CreateIK
import FaceJoints as FJ
import os

reload(Locators)
reload(Joints)
reload(SL)
reload(Controller)
reload(Constraints)
reload(CreateIK)
reload(FJ)

class AutoRigger():
   
    def __init__(self):
        base.currentUnit(linear = 'meter')
        base.grid(size = 12, spacing = 5, divisions = 5)
        print os.path.dirname(os.path.realpath(__file__))
        self.BuildUI()
       
    def BuildUI(self): 
        # Create the basic window
    
        base.window("Tom AutoRigger 2.0")

        form = base.formLayout()
        tabs = base.tabLayout(imh = 2, imw = 2)
        
        base.formLayout(form, edit = True, attachForm=((tabs, 'top',0), (tabs,'left', 0), (tabs, 'right', 0), (tabs, 'bottom',0)))

        # set the layout of the window

        ch = base.rowColumnLayout(nc = 1, cal = (1, 'right'), adjustableColumn = True)
        
        self.spineCount = base.intSliderGrp(l = "Spine Number", min = 1, max = 8, value = 4, step = 1, field = True)
        self.fingerCount = base.intSliderGrp(l = "Finger Number", min = 1, max = 8, value = 5, step = 1, field = True)         
     
        base.separator(h = 10, st = 'none') 
        base.button(l = "Add Locators", w = 200, c = self.DoLocators)          
        base.separator(st = 'none')
        base.button(l = "Secondary Locators", w = 200, c = "SL.SecondaryLocators()")
        base.separator(st = 'none')
        base.button(l = "Mirror Left to Right", w = 200, c = "Locators.mirrorLocators()")
        base.separator(st = 'none')
        base.button(l = "Facial Locators", w = 200, c = self.FaceLocators)
        base.separator(st = 'none')        
        base.button(l = "Delete All Locators", w = 200, c = "Locators.deleteLocators()")
        base.separator(h = 10, st = 'none')    

        base.button(l = "Create Joints", w = 200, c = "Joints.createJoints()")
        base.separator(st = 'none')
        base.button(l = "Delete Joints", w = 200, c = "Joints.deleteJoints()") 
        base.separator(st = 'none')   
        base.button(l = "Facial Joints", w = 200, c = self.FaceJoints)
        base.separator(st = 'none', h = 20)
     
        
        base.button(l = "Finalize Rig", w = 200, c = self.FinalizeRig)
        base.separator(st = 'none')    
        base.button(l = "Bind Skin", w = 200, c = "Constraints.BindSkin()")
        base.separator(st = 'none')
        base.button(l = "Paint Weight", w = 200, c = "base.artAttrSkinPaintCtx('artAttrSkinPaintCtx1', edit=True, sao='smooth')")
        base.separator(st = 'none')
        base.button(l = "Clear Locators", w = 200, c = self.ClearScene)
        self.doubleElbow = base.checkBox(l = 'Double Elbow', align = 'left', visible = False )
        base.tabLayout(tabs, edit = True, tabLabel = ((ch, 'Settings')))
               
        # show the actual window
        base.showWindow()
    
    def NextTab(self, void):
        base.tabLayout(edit = True, st = "2")
        
    def DoLocators(self, void):
        _spineCount = base.intSliderGrp(self.spineCount, q = True, v = True)
        _fingerCount = base.intSliderGrp(self.fingerCount, q = True, v = True)
        _doubleElbow = base.checkBox(self.doubleElbow, q = True, v = True)
        Locators.CreateLocators(_spineCount, _fingerCount, _doubleElbow)
    
    def FaceLocators(self, void):
        FJ.FaceJoints().CreateFaceWindow(self)
    
    def FaceJoints(self, void):
        FJ.FaceJoints().CreateJoints(self)
    
    def FinalizeRig(self, void):
        
        _spineCount = base.intSliderGrp(self.spineCount, q = True, v = True)
        _fingerCount = base.intSliderGrp(self.fingerCount, q = True, v = True) 
        Controller.CreateController(_spineCount, _fingerCount)
        CreateIK.IKHandles()
        Constraints.CreateConstraints(_fingerCount, _spineCount)  
        if(base.objExists("FACERIG_*")):        
            FJ.FaceJoints().AddConstraints(self)     

    def ClearScene(self, void):
        base.delete("Loc_Master")
        base.delete("SECONDARY")
        base.delete("FACE_LOC")  