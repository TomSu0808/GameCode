import sys
sys.path.insert(0, r"G:\Utah EAE\StudyProject\SelfStudy\RiggingClassStudy\MyWorks\JointBasedMucleDeformation\Code\Complete\MuscleJointCode")
from functools import partial
import importlib

import TrapeziusMuscle
import LatissimusDorsiMuscle
import DeltoidMuscle
import PectoralisMajorMuscle

importlib.reload(TrapeziusMuscle)
importlib.reload(LatissimusDorsiMuscle)
importlib.reload(DeltoidMuscle)
importlib.reload(PectoralisMajorMuscle)

from TrapeziusMuscle import TrapeziusMuscleGRP
from LatissimusDorsiMuscle import LatissimusDorsiMuscleGRP
from DeltoidMuscle import DeltoidMuscleGRP
from PectoralisMajorMuscle import PectoralisMuscleGRP

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



class UI_GRP(object):

    def __init__(self):

        self.UI()
        self.selectModule = None
        self.pick_L_R_ui = None
        self.update_factors()

        # self.compressionFactor = 0.5
        # self.stretchFactor = 2.0

        self.origin_A = None
        self.origin_B = None
        self.origin_C = None
        self.selected_module_instance = None

        self.trapeziusMuscle = TrapeziusMuscleGRP(self)
        self.latissimus_dorsi_muscle = LatissimusDorsiMuscleGRP(self)
        self.deltoid_muscle = DeltoidMuscleGRP(self)
        self.pectoralis_major_muscle = PectoralisMuscleGRP(self)



    def Trapezius_GRP(self, *args):
        self.trapeziusMuscle.createDecendingConstraint()
        self.trapeziusMuscle.createTraverseConstraint()
        self.trapeziusMuscle.createAscendingConstraint()

    def LatissimusDorsi_GRP(self, *args):
        self.latissimus_dorsi_muscle.createLatissimusDorsiConstraint_A()
        self.latissimus_dorsi_muscle.createLatissimusDorsiConstraint_B()
        self.latissimus_dorsi_muscle.createTerasMajorConstraint()

    def Deltoid_GRP(self, *args):
        self.deltoid_muscle.create_DT_A_Constraint()
        self.deltoid_muscle.create_DT_B_Constraint()
        self.deltoid_muscle.create_DT_C_Constraint()

    def PectoralisMajorMuscle_GRP(self, *args):
        self.pectoralis_major_muscle.createPMConstraint_A()
        self.pectoralis_major_muscle.createPMConstraint_B()

    def chooseRunModule(self, *args):
        selected_module = cmds.optionMenuGrp("pick_module_menu", query=True, value=True)
        self.selectModule = selected_module

        if selected_module == "Trapezius Muscle":
            self.selected_module_instance = self.trapeziusMuscle
            self.Trapezius_GRP()
        if selected_module == "Latissimus Dorsi":
            self.selected_module_instance = self.latissimus_dorsi_muscle
            self.LatissimusDorsi_GRP()
        if selected_module == "Deltoid Muscle":
            self.selected_module_instance = self.deltoid_muscle
            self.Deltoid_GRP()
        if selected_module == "Pectoralis Muscle":
            self.selected_module_instance = self.pectoralis_major_muscle
            self.PectoralisMajorMuscle_GRP()
        else:
            print("Meet Error !!!")

    def assumbleMuscleGrp(self, *args):
        self.chooseRunModule()

    def chooseDeleteModule(self, *args):
        selected_module = cmds.optionMenuGrp("pick_module_menu", query=True, value=True)
        self.selectModule = selected_module

        if selected_module == "Trapezius Muscle":
            self.selected_module_instance = self.trapeziusMuscle
            self.Trapezius_GRP()
        if selected_module == "Latissimus Dorsi":
            self.selected_module_instance = self.latissimus_dorsi_muscle
            self.LatissimusDorsi_GRP()
        if selected_module == "Deltoid Muscle":
            self.selected_module_instance = self.deltoid_muscle
            self.Deltoid_GRP()
        if selected_module == " Pectoralis Muscle":
            self.selected_module_instance = self.pectoralis_major_muscle
            self.PectoralisMajorMuscle_GRP()
        else:
            print("Meet Error !!!")



    def UI(self):
        if cmds.window("MuscleUnits", exists=True):
            cmds.deleteUI("MuscleUnits")

        window = cmds.window("MuscleUnits", title="UI", s=True, rtf=True, widthHeight=(150, 100))

        cmds.columnLayout(adjustableColumn=True)

        cmds.separator(h=2, st='none')

        self.selectModule = cmds.optionMenuGrp("pick_module_menu", label="Step1: Select Moduel", width = 200,
                                        columnAlign=(1, 'left'), columnAttach=[(1, 'left', 0), (2, 'left', 0)])

        for i in ["Trapezius Muscle", "Latissimus Dorsi", "Deltoid Muscle", "Pectoralis Muscle"]:
            cmds.menuItem(label = i)

        cmds.setParent("..")

        cmds.columnLayout(adjustableColumn=True)

        cmds.separator(h=2, st='none')

        cmds.text("Step1: Choose Joint")

        cmds.rowLayout(numberOfColumns=3, columnWidth2=(150, 100))
        self.origin_A = cmds.textFieldButtonGrp(label="Origin_A", text=" ", buttonLabel="Select",
                                                buttonCommand = lambda: self.load_joint("A_origin"))
        print(self.origin_A)

        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=3, columnWidth2=(150, 100))
        self.insertion_A = cmds.textFieldButtonGrp(label="Insertion_A", text="", buttonLabel="Select",
                                                buttonCommand = lambda: self.load_joint("A_insertion"))
        print(self.insertion_A)

        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=3, columnWidth2=(150, 100))
        self.origin_B = cmds.textFieldButtonGrp(label="Origin_B", text=" ", buttonLabel="Select",
                                                        buttonCommand = lambda: self.load_joint("B_origin"))
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=3, columnWidth2=(150, 100))
        self.insertion_B = cmds.textFieldButtonGrp(label="Insertion_B", text=" ", buttonLabel="Select",
                                                            buttonCommand = lambda: self.load_joint("B_insertion"))
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=3, columnWidth2=(150, 100))
        self.origin_C = cmds.textFieldButtonGrp(label="Origin_C", text=" ", buttonLabel="Select",
                                                            buttonCommand = lambda: self.load_joint("C_origin"))
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=3, columnWidth2=(150, 100))
        self.insertion_C = cmds.textFieldButtonGrp(label="Insertion_C", text=" ", buttonLabel="Select",
                                                            buttonCommand = lambda: self.load_joint("C_insertion"))
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2, columnWidth2=(180, 120), adjustableColumn=2, columnAlign=(1, "left"))

        self.pick_L_R_ui = cmds.optionMenuGrp("pick_L_R_Menu", label="Step2: Select L/R Side", width = 200,
                                        columnAlign=(1, 'left'), columnAttach=[(1, 'left', 0), (2, 'left', 0)])

        for y in ["L", "R"]:
            cmds.menuItem(label=y)

        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=5, columnWidth2=(200, 120),
                       adjustableColumn=5, columnAlign=(1, 'center'))
        cmds.text("Step3:")
        # Stretch factor input
        cmds.text(label='stretch factor')
        self.stretchField = cmds.textField(text="2.0", changeCommand=self.update_factors)

        # Compression factor input
        cmds.text(label='compression factor')
        self.compressionField = cmds.textField(text="0.5", changeCommand=self.update_factors)
        cmds.setParent('..')

        cmds.rowLayout(adjustableColumn=True)
        cmds.text("Step4: Choose Direction")
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

        cmds.rowLayout(adjustableColumn=True)
        self.excute = cmds.button(label="Run", c = self.assumbleMuscleGrp)
        cmds.setParent("..")

        cmds.separator(h = 5, st = 'none')
        cmds.text("Step5: Click Button into Edit Mode or Exist")
        cmds.separator(h = 2, st = 'none')

        cmds.rowLayout(adjustableColumn=True)
        cmds.button(label="Edit Mode", c = self.runEditMode)
        cmds.setParent('..')

        cmds.separator(h = 5, st = 'none')
        cmds.text("Option: Delete Joints")
        cmds.separator(h = 2, st = 'none')

        cmds.rowLayout(adjustableColumn=True)
        cmds.button(label="Delete Generate Joints", c = self.selectDeleteGrp)
        cmds.setParent('..')

        cmds.rowLayout(adjustableColumn=True)
        cmds.button(label="Export Joints Data", c=self.exportDataAssumble)
        cmds.setParent('..')

        cmds.rowLayout(adjustableColumn=True)
        cmds.button(label="Import Joints Data", c=self.importDataAssumble)
        cmds.setParent('..')

        cmds.showWindow(window)



    def load_joint(self, joint_type, *args):
        selected = cmds.ls(selection=True)
        if selected:
            if joint_type == 'A_origin':
                cmds.textFieldButtonGrp(self.origin_A, edit=True, text=selected[0])
            elif joint_type == 'A_insertion':
                cmds.textFieldButtonGrp(self.insertion_A, edit=True, text=selected[0])
            elif joint_type == 'B_origin':
                cmds.textFieldButtonGrp(self.origin_B, edit=True, text=selected[0])
            elif joint_type == 'B_insertion':
                cmds.textFieldButtonGrp(self.insertion_B, edit=True, text=selected[0])
            elif joint_type == 'C_origin':
                cmds.textFieldButtonGrp(self.origin_C, edit=True, text=selected[0])
            elif joint_type == 'C_insertion':
                cmds.textFieldButtonGrp(self.insertion_C, edit=True, text=selected[0])

    def get_LR_value(self, *args):
        if self.pick_L_R_ui:
            return cmds.optionMenuGrp(self.pick_L_R_ui, query=True, value=True)
        return None

    def runEditMode(self, *args):
        lr_value = cmds.optionMenuGrp(self.pick_L_R_ui, query=True, value=True)
        if cmds.objExists("{0}_muscleOrigin_loc_A".format(lr_value)) or cmds.objExists("{0}_muscleOrigin_loc_B".format(lr_value)):
            if self.selected_module_instance:
                if self.selectModule == "Trapezius Muscle":
                    self.selected_module_instance.update()
                if self.selectModule == "Latissimus Dorsi":
                    self.selected_module_instance.update()
                if self.selectModule == "Deltoid Muscle":
                    self.selected_module_instance.update()
                if self.selectModule == "Pectoralis Muscle":
                    self.selected_module_instance.update()

        else:
            if self.selected_module_instance:
                if self.selectModule == "Trapezius Muscle":
                    self.selected_module_instance.edit()
                if self.selectModule == "Latissimus Dorsi":
                    self.selected_module_instance.edit()
                if self.selectModule == "Deltoid Muscle":
                    self.selected_module_instance.edit()
                if self.selectModule == "Pectoralis Muscle":
                    self.selected_module_instance.edit()

    def selectDeleteGrp(self, *args):
        selected_module = cmds.optionMenuGrp("pick_module_menu", query=True, value=True)

        if selected_module == "Latissimus Dorsi":
            self.selected_module_instance = self.latissimus_dorsi_muscle
        elif selected_module == "Trapezius Muscle":
            self.selected_module_instance = self.trapeziusMuscle
        elif selected_module == "Deltoid Muscle":
            self.selected_module_instance = self.deltoid_muscle
        elif selected_module == "Pectoralis Muscle":
            self.selected_module_instance = self.pectoralis_major_muscle
        else:
            self.selected_module_instance = None

        if self.selected_module_instance and selected_module == "Latissimus Dorsi":
            print("Deleting Latissimus Dorsi joints")
            self.selected_module_instance.delete()
        elif selected_module == "Trapezius Muscle":
            print("Deleting Trapezius Muscle joints")
            self.selected_module_instance.delete()
        elif selected_module == "Deltoid Muscle":
            print("Deleting Deltoid Muscle joints")
            self.selected_module_instance.delete()
        elif selected_module == "Pectoralis Muscle":
            print("Deleting Pectoralis Muscle joints")
            self.selected_module_instance.delete()
        else:
            print("No module selected or no delete function available for this module.")

    def update_factors(self, *args):
        self.stretchFactor = float(cmds.textField(self.stretchField, query=True, text=True))
        self.compressionFactor = float(cmds.textField(self.compressionField, query=True, text=True))

    def exportDataAssumble(self, *args):
        selected_module = cmds.optionMenuGrp("pick_module_menu", query=True, value=True)

        if selected_module == "Latissimus Dorsi":
            self.selected_module_instance = self.latissimus_dorsi_muscle
        elif selected_module == "Trapezius Muscle":
            self.selected_module_instance = self.trapeziusMuscle
            filepath = r"G:\Utah EAE\StudyProject\SelfStudy\RiggingClassStudy\MyWorks\JointBasedMucleDeformation\Code\allMuscle.json"
            self.selected_module_instance.exportMuscle(filepath)
        elif selected_module == "Deltoid Muscle":
            self.selected_module_instance = self.deltoid_muscle
        elif selected_module == "Pectoralis Muscle":
            self.selected_module_instance = self.pectoralis_major_muscle
        else:
            self.selected_module_instance = None

    def importDataAssumble(self, *args):
        selected_module = cmds.optionMenuGrp("pick_module_menu", query=True, value=True)

        if selected_module == "Latissimus Dorsi":
            self.selected_module_instance = self.latissimus_dorsi_muscle
        elif selected_module == "Trapezius Muscle":
            self.selected_module_instance = self.trapeziusMuscle
            filepath = r"G:\Utah EAE\StudyProject\SelfStudy\RiggingClassStudy\MyWorks\JointBasedMucleDeformation\Code\allMuscle.json"
            self.selected_module_instance.importMuscle(filepath)
        elif selected_module == "Deltoid Muscle":
            self.selected_module_instance = self.deltoid_muscle
        elif selected_module == "Pectoralis Muscle":
            self.selected_module_instance = self.pectoralis_major_muscle
        else:
            self.selected_module_instance = None

if __name__ == "__main__":
    class_grp = UI_GRP()
    class_grp.UI()
