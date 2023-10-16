### Tom Su   10/15/2023 ###

import unreal

# get select actor information
class select_actor_information():
        
    # get select static mesh actor information
    def get_select_mesh():
        selected_actor = unreal.EditorActorSubsystem().get_selected_level_actors()

        static_mesh_actor_list = []
        
        for actors in selected_actor:
            if (actors.get_class().get_name()) == "StaticMeshActor":
                get_static_mesh_component = actors.static_mesh_component
                get_static_mesh = get_static_mesh_component.static_mesh
                static_mesh_actor_list.append(get_static_mesh.get_name())
                
        print("Mesh Name:" , static_mesh_actor_list)
        return static_mesh_actor_list
        
    def get_select_class():
        #get select static mesh actors then get actors class
        all_level_actors = unreal.EditorActorSubsystem().get_selected_level_actors()

        static_mesh_actors = []
        
        input_get_select_mesh = select_actor_information.get_select_mesh()
         
        for actor in all_level_actors:
            if (actor.get_class().get_name()) == "StaticMeshActor":
                static_mesh_actors.append(actor)
                text_class = ("Class Name: ")
                actor_class = actor.get_class().get_name()
    
                actor_combine_get_class = (text_class + str(actor_class))

                print(actor_combine_get_class)
        #return to list   
        return static_mesh_actors
            
                
    def get_materials():
        #get information from previous function
        static_mesh_actors = select_actor_information.get_select_class()

        materials = []
        
        for static_mesh_actor in static_mesh_actors:
            static_mesh_component = static_mesh_actor.static_mesh_component
            get_all_material = static_mesh_component.get_materials()
            
            for all_material in get_all_material:
                if all_material not in materials:

                    materials.append(all_material)
                #get material name
                material_name_text = ("Material Name: " + all_material.get_name())  
                print(material_name_text)
        #get material number
        materials_count_text = ("Number of Material: " + str(len(materials)))      
        print(materials_count_text)
        
        return materials
        
    def get_textures():
        # get information from function:get_materials()
        materials = select_actor_information.get_materials()
        texture_list = []
        
        for material in materials:
            texture_parameter = material.texture_parameter_values
            for texture_param in texture_parameter:
                textures = texture_param.parameter_value
                if textures not in texture_list:
                    get_texture_name = textures.get_name()
                    texture_list.append(get_texture_name)
        #output texture information
        print("Number of Texture Applying:", len(texture_list))      
        print("Texture Name: ", texture_list)

        return texture_list

# get select mesh lod information  
class select_mesh_lod():

    def get_lod_number():
        #get select static mesh in folder
        selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
        
        
        for asset in selected_assets:
            asset_lod_count = asset.get_num_lods()
            
            return asset_lod_count
        
            
    def get_lod_group():
        #get lod number
        get_lod_number_func = select_mesh_lod.get_lod_number()
        
        select_assets = unreal.EditorUtilityLibrary.get_selected_assets()
        
        for asset in select_assets:
            # get lod group
            lod_group_info = asset.get_editor_property("lod_group")       
            
            lod_group_text = ("LOD Group: ")
            
            print(lod_group_text, lod_group_info)
        
            print("LOD Number:" , get_lod_number_func)
    
    
    def get_lod_diameter():

        select_assets = unreal.EditorUtilityLibrary.get_selected_assets()
        
        for select_asset in select_assets:
            section_vert_list = []
            section_tri_list = []
            
            get_lod = select_asset.get_num_lods()
            
            for i in range(get_lod):
                number_section = select_asset.get_num_sections(i)

                for j in range (number_section):
                    section_data = unreal.ProceduralMeshLibrary.get_section_from_static_mesh(select_asset, i, j)        
                    #get vertex number
                    section_vert_count = int(len(section_data[0]))
                    section_vert_list.append(section_vert_count)
                    #get triangle number
                    section_tri_count = int(len(section_data[1])/3)
                    section_tri_list.append(section_tri_count)

            
            print("LOD Vertex Number:", section_vert_list)
            print("LOD Triangle Number:", section_tri_list)
            return section_tri_list, section_vert_list

# auto convert lod data                   
class lod_data_convert():
    
    def auto_convert_lod_grp():
        select_assets = unreal.EditorUtilityLibrary.get_selected_assets()
        
        for asset in select_assets:
            asset_bounds = asset.get_bounds()
            asset_radius = asset_bounds.sphere_radius
            asset_diameter = (asset_radius * 2)
            
            asset.get_editor_property("lod_group")
            #when diameter greater than 200 convert to largeProp or vertex to smallProp
            if asset_diameter > 200:
                asset.set_editor_property("lod_group", "LargeProp")
                unreal.log_warning("Already Convert to LargeProp")
            if asset_diameter < 200:
                asset.set_editor_property("lod_group", "SmallProp")
                unreal.log_warning("Already Convert to SmallProp")

# enable nanite system
class nanite_edit():
                    
    def get_static_mesh():
        # get static mesh
        select_actors = unreal.EditorActorSubsystem().get_selected_level_actors()

        for static_mesh_actor in select_actors:
            nanite_edit.enable_nanite(static_mesh_actor)
            unreal.log_warning("Nanite Enable Success")
 
    
    def enable_nanite(static_mesh_actor):
            
            static_mesh = static_mesh_actor.static_mesh_component.static_mesh
            if static_mesh:
                #get nanite attribute in setting
                mesh_nanite_settings = static_mesh.get_editor_property("nanite_settings")
                if not mesh_nanite_settings.enabled:
                    mesh_nanite_settings.enabled = True
                    unreal.StaticMeshEditorSubsystem().set_nanite_settings(static_mesh, mesh_nanite_settings, apply_changes = True)

#export assets & texture to folder
class assets_manager():
        
    ### Export select assets
    def export_select_fbx_assets():

        select_assets = unreal.EditorUtilityLibrary.get_selected_assets()
        
        # iterate over selection and export
        for select_asset in select_assets:
            asset_name = select_asset.get_name()
            
            #create asset export task
            asset_export_task = unreal.AssetExportTask()
            asset_export_task.automated = True
            
            
            # object is the asset to be exported
            asset_export_task.object = select_asset
            asset_export_task.prompt = False
            
            # export static mesh assets
            if isinstance(select_asset, unreal.StaticMesh):
                asset_export_task.filename = "E:\\Study2\\StudyProject\\SelfStudy\\UnrealPlugin\\" + asset_name + ".fbx"
                
                #create class specific exporter
                asset_export_task.options = unreal.FbxExportOption()
                fbx_exporter = unreal.StaticMeshExporterFBX()
                asset_export_task.exporter = fbx_exporter
                fbx_exporter.run_asset_export_task(asset_export_task)
                print("Export Static Mesh Success")
                
                
    def export_select_texture_assets():

        select_assets = unreal.EditorUtilityLibrary.get_selected_assets()
        
        # iterate over selection and export
        for select_asset in select_assets:
            asset_name = select_asset.get_name()
            
            #create asset export task
            export_task = unreal.AssetExportTask()
            export_task.automated = True
            
            
            # object is the asset to be exported
            export_task.object = select_asset
            export_task.prompt = False
                
            #export textures
            if isinstance(select_asset, unreal.Texture):
                export_task.filename = "E:\\Study2\\StudyProject\\SelfStudy\\UnrealPlugin\\" + asset_name + ".tga"
                tag_exporter = unreal.TextureExporterTGA()
                export_task.exporter = tag_exporter
                tag_exporter.run_asset_export_task(export_task)
                print("Export Texture Success")
