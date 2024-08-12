import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.mel as mm

class CSW(object):

    def __init__(self, source, targets, method='closestPoint'):
        self.source = source
        self.targets = targets
        self.method = method

    def switchSkinMethod(self):
        select_source_geo_list = []
        select_target_geo_list = []

        get_source_geo = cmds.ls(self.source, flatten=True)
        get_target_geo = cmds.ls(self.targets, flatten=True)

        select_source_geo_list.extend(get_source_geo)
        select_target_geo_list.extend(get_target_geo)

        combined_geo_list = select_source_geo_list + select_target_geo_list
        print(combined_geo_list)

        if any('.' in item for item in combined_geo_list):
            print("Use Vertex Copy Weight")
            self.copy_edit_model()
        else:
            print("Use One to One / Multiple Copy Weight")
            self.copy_skin_weights()

        '''
        if any('.' in name for name in combined_geo_list if isinstance(name, str)):
            print("Use Vertex Copy Weight")
            # self.copy_edit_model()
        else:
            print("Use One to One / Multiple Copy Weight")
            # self.copy_skin_weights()
        '''

    def copy_skin_weights(self):

        print("running copy_skin_weights function !!!")

        if not cmds.objExists(self.source):
            cmds.warning("source target {} not found".format(self.source))
            return

        source_skin_cluster = cmds.ls(cmds.listHistory(self.source), type='skinCluster')
        if not source_skin_cluster:
            cmds.warning("Can't find source object in skin cluster: {}".format(self.source))
            return

        source_skin_cluster_01 = source_skin_cluster[0]

        source_joints = cmds.skinCluster(source_skin_cluster_01, query=True, influence=True)
        print("source joints: {}".format(source_joints))
        if not source_joints:
            cmds.warning("source object skin cluster can't found affect joints: {}".format(self.source))
            return

        for target in self.targets:
            if not cmds.objExists(target):
                cmds.warning("target object {} not found".format(target))
                continue

            target_skin_cluster = cmds.ls(cmds.listHistory(target), type='skinCluster')
            if not target_skin_cluster:
                cmds.select(clear=True)
                cmds.select(source_joints, replace=True)
                cmds.select(target, add=True)
                add_target_skin_cluster = cmds.skinCluster(source_joints, target, toSelectedBones=1, bindMethod=0,
                                                           maximumInfluences=4, dropoffRate=4,
                                                           obeyMaxInfluences=True, removeUnusedInfluence=True)[0]
            else:
                add_target_skin_cluster = target_skin_cluster[0]

            
            cmds.copySkinWeights(ss=source_skin_cluster_01, ds=add_target_skin_cluster, noMirror=True,
                                 surfaceAssociation='closestPoint', influenceAssociation= ["label","closestJoint","oneToOne"])

            cmds.select(clear=True)
            cmds.select(target, replace=True)
            csw_instance = CSW(self.source, self.targets)
            csw_instance.lockSkinClusterWeights(add_target_skin_cluster,lock=False,lockAttr=False)
            mm.eval('doPruneSkinClusterWeightsArgList 1 { "0.01" }')
            csw_instance.lockSkinClusterWeights(add_target_skin_cluster,lock=True,lockAttr=True)

            print(" Already copy skin wieght from {0} to {1}".format(self.source, self.targets) )
        
    def same_mesh_copy(self):
        # Call copy_edit_model function
        CSW_Class = CSW(self.source, self.targets)
        CSW_Class.copy_edit_model()

    def copy_edit_model(self):

        print("running copy_edit_model function !!!")

        select_source_geo_list = []
        select_target_geo_list = []
        filter_source_geo_list = []
        filter_target_geo_list = []
        filter_target_data_list = []
        
        get_source_geo = cmds.ls(self.source, flatten=True)
        get_target_geo = cmds.ls(self.targets, flatten=True)

        filter_source_geo = list(set([geo.split('.')[0] for geo in get_source_geo]))
        filter_source_geo_list.extend(filter_source_geo)

        filter_target = list(set([geo.split('.')[0] for geo in get_target_geo]))
        filter_target_geo_list.extend(filter_target)

        select_source_geo_list.append(get_source_geo)
        select_target_geo_list.append(sorted(get_target_geo))

        source_history = cmds.listHistory(filter_source_geo_list)
        source_skin_clusters = cmds.ls(source_history, type='skinCluster')

        target_history = cmds.listHistory(filter_target_geo_list)
        target_skin_clusters = cmds.ls(target_history, type='skinCluster')

        if source_skin_clusters == target_skin_clusters:
            cmds.warning("Source and Target have same skin cluster !!!")
        
            # get target geo 
            copy_target_geo_list = []
            for geo in filter_source_geo_list:
                copy_target_geo_01 = cmds.duplicate(geo, name=geo + "_copyTarget")[0]
                source_joints = cmds.skinCluster(geo, query=True, influence=True)
                cmds.select(clear=True)
                cmds.select(get_source_geo, replace=True)
                cmds.select(copy_target_geo_01, add=True)
                cmds.skinCluster(source_joints, copy_target_geo_01, toSelectedBones=1, bindMethod=0, maximumInfluences=4,
                                dropoffRate=4, obeyMaxInfluences=True, removeUnusedInfluence=True)
                copy_target_geo_list.append(copy_target_geo_01)

            # get target geo name and remove prefix
            filter_target_geo = list(set([geo.split('.', 1)[1] for geo in get_target_geo if '.' in geo]))
            filter_target_data_list.extend(filter_target_geo)

            # print("Filtered Source List:", filter_source_geo_list)
            # print("Filtered Target List:", filter_target_data_list) 

            selection_list = []
            for copy_geo in copy_target_geo_list:
                for target_data in filter_target_data_list:
                    selection_list.append("{0}.{1}".format(copy_geo, target_data)) 
            
            get_orgnize_selectionlist = sorted(selection_list)
            
            #   Select object
            all_elements = []
            for copy_geo in copy_target_geo_list:
                if filter_target_data_list[0].startswith('vtx'):
                    all_elements.extend(cmds.ls("{0}.vtx[*]".format(copy_geo), flatten=True))
                elif filter_target_data_list[0].startswith('f'):
                    all_elements.extend(cmds.ls("{0}.f[*]".format(copy_geo), flatten=True))

            # Get invert data
            inverted_selection = list(set(all_elements) - set(selection_list))

            # print("get_target_geo_list:", get_target_geo)
            # print("copy_target_geo_list:", copy_target_geo_list)
            # print("selection_list:", selection_list)
            
            

            # Invert Selection 
            convert_to_face = cmds.polyListComponentConversion(inverted_selection, fv=True, fe=True, 
                                                            fuv=True, fvf=True, tf=True)
        
            # get target geo and delete extra face

            ### Version 1: temperary not use this method to delete face
            cmds.select(convert_to_face)
            cmds.delete(convert_to_face)
            cmds.delete(copy_target_geo_01, ch=True)

            # get source geo
            copy_source_geo_list = []
            for geo in filter_source_geo_list:
                copy_source_geo_02 = cmds.duplicate(geo, name = geo + "_copySource")[0]
                copy_source_geo_list.append(copy_source_geo_02)
                cmds.select(clear=True)

            source_geo_selection_list = []

            for copy_source_geo in copy_source_geo_list:
                for target_data in filter_target_data_list:
                    source_geo_selection_list.append("{0}.{1}".format(copy_source_geo, target_data))
            
            source_geo_all_elements = []
            for copy_geo in copy_source_geo_list:
                if filter_target_data_list[0].startswith('vtx'):
                    source_geo_all_elements.extend(cmds.ls("{0}.vtx[*]".format(copy_geo), flatten=True))
                elif filter_target_data_list[0].startswith('f'):
                    source_geo_all_elements.extend(cmds.ls("{0}.f[*]".format(copy_geo), flatten=True))

            convert_to_face = cmds.polyListComponentConversion(source_geo_selection_list, fv=True, fe=True, 
                                                            fuv=True, fvf=True, tf=True)
            
            #   get source geo and delete it's poly face
            cmds.select(convert_to_face)
            cmds.delete(convert_to_face)
            cmds.delete(copy_source_geo_02, ch=True)
            cmds.select(clear=True)

            #   copy original model skin weight to source model
            source_skin_cluster = cmds.ls(cmds.listHistory(self.source), type='skinCluster')
            source_skin_cluster_01 = source_skin_cluster[0]
            cmds.select(clear=True)
            cmds.select(get_source_geo, replace=True)
            cmds.select(copy_source_geo_02, add=True)
            create_copySource_cluster = cmds.skinCluster(source_joints, copy_source_geo_02, toSelectedBones=1, bindMethod=0, maximumInfluences=4,
                            dropoffRate=4, obeyMaxInfluences=True, removeUnusedInfluence=0)[0]
            cmds.select(clear=True)
            query_copySource_skin_cluster = cmds.ls(cmds.listHistory(copy_source_geo_02), type='skinCluster')[0]
            cmds.copySkinWeights(ss = source_skin_cluster_01 , ds = query_copySource_skin_cluster, noMirror=True,
                                    surfaceAssociation='closestPoint', influenceAssociation= ['closestJoint', 'oneToOne', 'oneToOne'])
            
            # copy source model skin weight to target model
            cmds.select(get_source_geo, replace=True)
            cmds.select(copy_target_geo_01, add=True)
            
            create_copyTarget_cluster = cmds.skinCluster(source_joints, copy_target_geo_01, toSelectedBones=1, bindMethod=0, maximumInfluences=4,
                            dropoffRate=4, obeyMaxInfluences=True, removeUnusedInfluence=0)[0]
            cmds.select(clear=True)
            query_copyTarget_skin_cluster = cmds.ls(cmds.listHistory(copy_target_geo_01), type='skinCluster')[0]
            cmds.copySkinWeights(ss = query_copySource_skin_cluster , ds = query_copyTarget_skin_cluster, noMirror=True,
                                    surfaceAssociation='closestPoint', influenceAssociation= ['closestJoint','oneToOne', 'oneToOne'])
            

            # copy target skin weight to original model

            # Version 3, select copy target model and original model match vertex then applying copy skin weight command
            cmds.select(copy_target_geo_01, replace=True)
            cmds.select(get_target_geo, add=True)
            cmds.copySkinWeights(noMirror = 1, surfaceAssociation = "closestPoint", influenceAssociation = ['closestJoint','oneToOne', 'oneToOne'])
            cmds.select(clear = True)

            # lock skin weight
            # cmds.select(clear=True)
            # cmds.select(get_target_geo, replace=True)
            # csw_instance = CSW(self.source, self.targets)
            # csw_instance.lockSkinClusterWeights(target_skin_clusters,lock=False,lockAttr=False)
            # mm.eval('doPruneSkinClusterWeightsArgList 1 { "0.01" }')
            # csw_instance.lockSkinClusterWeights(target_skin_clusters,lock=True,lockAttr=True)
            
            # # delete source and target models
            cmds.delete(copy_target_geo_01)
            cmds.delete(copy_source_geo_02)
        
        if source_skin_clusters != target_skin_clusters:
            cmds.warning("Source and Target are not same skin cluster !!!")
            get_target_history = cmds.listHistory(filter_target_geo_list)
            get_target_skin_clusters = cmds.ls(get_target_history, type='skinCluster')
            if not get_target_skin_clusters:
                get_source_joints = cmds.skinCluster(filter_source_geo_list, query=True, influence=True)
                bindSkin = cmds.skinCluster(get_source_joints, filter_target_geo_list, toSelectedBones=1, bindMethod=0, maximumInfluences=4,
                                            dropoffRate=4, obeyMaxInfluences=True, removeUnusedInfluence=True)
            else:
                cmds.select(clear=True)
                cmds.select(get_source_geo, replace=True)
                cmds.select(get_target_geo, add=True)
                cmds.copySkinWeights(noMirror = 1, surfaceAssociation = "closestPoint", influenceAssociation = ["closestJoint", 'oneToOne', 'oneToOne'])
                cmds.select(clear = True)

            # lock skin weight
            # cmds.select(clear=True)
            # cmds.select(get_target_geo, replace=True)
            # csw_instance = CSW(self.source, self.targets)
            # csw_instance.lockSkinClusterWeights(target_skin_clusters,lock=False,lockAttr=False)
            # mm.eval('doPruneSkinClusterWeightsArgList 1 { "0.01" }')
            # csw_instance.lockSkinClusterWeights(target_skin_clusters,lock=True,lockAttr=True)    



    def lockInfluenceWeights(self, influence,lock=True,lockAttr=False):

        # Check SkinCluster
        if not cmds.objExists(influence):
            raise Exception('Influence "'+influence+'" does not exist!')
        
        # Check Lock Influence Weights Attr
        if not cmds.attributeQuery('liw',n=influence,ex=True):
            raise Exception('Influence ("'+influence+'") does not contain attribute "lockInfluenceWeights" ("liw")!')
            
        # Set Lock Influence Weights Attr
        try:
            cmds.setAttr(influence+'.liw',l=False)
            cmds.setAttr(influence+'.liw',lock)
            if lockAttr: cmds.setAttr(influence+'.liw',l=True)
        except: pass
        
        # Return Result
        return lock

    def lockSkinClusterWeights(self, skinCluster,lock=True,lockAttr=False):
        
        influenceList = cmds.skinCluster(skinCluster,q=True,inf=True) or []
        
        for influence in influenceList:
            # Set Lock Influence Weights Attr
            csw_instance = CSW(self.source, self.targets)

            csw_instance.lockInfluenceWeights(influence,lock=lock,lockAttr=lockAttr)
        
        # Return Result
        return influenceList
        
class CopySkinWeightsUI(object):

    def __init__(self):
        self.window = "CopySkinWeightsWindow"
        self.title = "Tom's Copy Skin Weight Tool V2.1 (07/2024)"
        self.size = (480, 300)

        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title=self.title, sizeable=False, widthHeight=self.size)
        self.form_layout = cmds.formLayout()

        self.source_layout = cmds.columnLayout(adjustableColumn=True, parent=self.form_layout)
        cmds.text(label="Source", parent=self.source_layout)
        self.source_list = cmds.textScrollList(allowMultiSelection=False, parent=self.source_layout)
        cmds.button(label="Load Source", command=self.load_source, parent=self.source_layout)
        cmds.button(label="Clear Source List", command=self.clear_source_list, parent=self.source_layout)

        self.target_layout = cmds.columnLayout(adjustableColumn=True, parent=self.form_layout)
        cmds.text(label="Target", parent=self.target_layout)
        self.target_list = cmds.textScrollList(allowMultiSelection=True, parent=self.target_layout)
        cmds.button(label="Load Targets", command=self.load_targets, parent=self.target_layout)
        cmds.button(label="Clear Target List", command=self.clear_target_list, parent=self.target_layout)

        cmds.formLayout(self.form_layout, edit=True,
                        attachForm=[
                            (self.source_layout, 'top', 5),
                            (self.source_layout, 'left', 5),
                            (self.target_layout, 'top', 5),
                            (self.target_layout, 'right', 5)
                        ],
                        attachPosition=[
                            (self.source_layout, 'right', 5, 50),
                            (self.target_layout, 'left', 5, 50)
                        ]
                        )

        self.bottom_layout = cmds.columnLayout(adjustableColumn=True, parent=self.form_layout)
        cmds.button(label="Copy Skin Weight", command=self.copy_weights, parent=self.bottom_layout)
        cmds.separator(h=10, style="none")
        self.status = cmds.text(label="", parent=self.bottom_layout)

        '''
        cmds.button(label="Vertex Copy Weight", command=self.copy_weights_001, parent=self.bottom_layout)
        self.status = cmds.text(label="", parent=self.bottom_layout)
        '''

        self.method_layout = cmds.rowLayout(numberOfColumns=5, parent=self.form_layout)
        self.method_collection = cmds.radioCollection()
        self.methods = ['closestPoint', 'rayCast', 'closestComponent', 'uvSpace', 'closestVertex']
        self.method_buttons = {}
        for method in self.methods:
            self.method_buttons[method] = cmds.radioButton(
                label=method, 
                onCommand=lambda x, m=method: self.set_method(m),
                parent=self.method_layout
            )
        cmds.radioButton(self.method_buttons['closestPoint'], edit=True, select=True)

        cmds.formLayout(self.form_layout, edit=True,
                        attachForm=[
                            (self.bottom_layout, 'left', 10),
                            (self.bottom_layout, 'right', 10),
                            (self.bottom_layout, 'bottom', 60),
                            (self.method_layout, 'left', 10),
                            (self.method_layout, 'right', 10),
                            (self.method_layout, 'bottom', 10)
                        ],
                        attachControl=[
                            (self.bottom_layout, 'top', 10, self.source_layout),
                            (self.method_layout, 'top', 10, self.bottom_layout)
                        ]
                        )

        cmds.showWindow(self.window)

    def load_source(self, *args):
        selected = cmds.ls(selection=True)
        if selected:
            cmds.textScrollList(self.source_list, edit=True, append=selected)

    def load_targets(self, *args):
        selected = cmds.ls(selection=True)
        if selected:
            cmds.textScrollList(self.target_list, edit=True, append=selected)

    def clear_source_list(self, *args):
        cmds.textScrollList(self.source_list, edit=True, removeAll=True)

    def clear_target_list(self, *args):
        cmds.textScrollList(self.target_list, edit=True, removeAll=True)

    def copy_weights(self, *args):
        source = cmds.textScrollList(self.source_list, query=True, allItems=True)
        targets = cmds.textScrollList(self.target_list, query=True, allItems=True)

        if source and targets:
            source_string = source[0]
            COPYSKINWEIGHTS = CSW(source_string, targets)
            COPYSKINWEIGHTS.switchSkinMethod()
            cmds.text(self.status, edit=True, label="Weights copied successfully!")
        else:
            cmds.text(self.status, edit=True, label="Please select source and target objects.")

    '''
    def copy_weights_001(self, *args):
        source = cmds.textScrollList(self.source_list, query=True, allItems=True)
        targets = cmds.textScrollList(self.target_list, query=True, allItems=True)

        if source and targets:
            source_string = source[0]
            COPYSKINWEIGHTS = CSW(source_string, targets)
            COPYSKINWEIGHTS.same_mesh_copy()
            cmds.text(self.status, edit=True, label="Weights copied successfully!")
        else:
            cmds.text(self.status, edit=True, label="Please select source and target objects.")
    '''

    def set_method(self, method):
        self.method = method


CopySkinWeightsUI()
