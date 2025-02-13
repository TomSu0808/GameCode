import sys
sys.path.insert(0, r"G:\Utah EAE\StudyProject\SelfStudy\RiggingClassStudy\MyWorks\JointBasedMucleDeformation\Code\Complete\MuscleJointCode")
from functools import partial   
import importlib

import UI
import LatissimusDorsiMuscle

importlib.reload(UI)
importlib.reload(LatissimusDorsiMuscle)

import maya.cmds as cmds
import maya.api.OpenMaya as om
import math

def main():
    ui_display = UI()
    ui_display.UI_GRP()




if __name__ == "__main__":
    main()
