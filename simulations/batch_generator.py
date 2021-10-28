"""
Created on Thu Sep 23 10:04:38 2021

@author: Hossein
"""
import os
import sys
import json
import shutil

def generate_batch_files(input_str="",
                        model_to_change = [],
                        protocol_to_change = [],
                        reverse_protocol = [],
                        growth_gains = []):
    # get roots
    base_files = os.listdir(input_str)
    cwd = os.getcwd()

    # Read base files
    with open (os.path.join(input_str,'model.json'),'r') as m:
        model_base = json.load(m)
    with open (os.path.join(input_str,'protocol.json'),'r') as p:
        protocol_base = json.load(p)
    with open (os.path.join(input_str,'batch.json'),'r') as b:
        batch_base = json.load(b)
    temp_batch = batch_base
    temp_batch['job'] = []
    
    #print(json.dumps(protocol_base,indent=4))
    if not protocol_to_change == []:
        with open (os.path.join(input_str,'protocol.json'),'r') as p:
            protocol_base = json.load(p)
        for p in protocol_to_change:

            for value in p['total_change']:
                #define a job and complete it as the input files are getting generated
                job = dict()
                job['relative_path'] = True

                temp_protocol = protocol_base
                temp_protocol['perturbation']['perturbations'] = \
                    [p]
                temp_protocol['perturbation']['perturbations'][0]['total_change'] = \
                    value
                # handle file_name
                if p['variable'] == 'aorta_resistance':
                    valve_name = 'AS'
                elif p['variable'] == 'mitral_insufficiency_conductance':
                    valve_name = 'MR'
                elif p['variable'] == 'aortic_insufficiency_conductance':
                    valve_name = 'AR'

                sim_folder_name = 'simulation_' + valve_name + '_' + str(value)
                pr_file_name = 'protocol_' + valve_name + '_' + str(value) +'.json'
                sim_input_path_str = os.path.join(cwd,sim_folder_name,'sim_inputs')
                pr_file_path = os.path.join(sim_input_path_str,pr_file_name)

                job['protocol_file_string'] = sim_folder_name + '/' + 'sim_inputs' + '/' + pr_file_name
                #print(pr_file_path)

                # make directory
                if not os.path.isdir(sim_input_path_str):
                    print('Making dir')
                    os.makedirs(sim_input_path_str)

                with open(pr_file_path,'w') as f:
                    json.dump(temp_protocol,f,indent=4)

                # now make a copy of all input files from base
                job = handle_model_and_option_files(input_str = input_str,
                                                sim_input_path_str = sim_input_path_str,
                                                sim_folder_name = sim_folder_name,
                                                base_files = base_files,
                                                valve_name = valve_name,
                                                pert_value = value,
                                                job_dict= job,
                                                reverse_mode = False)

                job = handle_output_handler_file(input_str = input_str,
                                                sim_input_path_str = sim_input_path_str,
                                                sim_folder_name = sim_folder_name,
                                                base_files = base_files,
                                                valve_name = valve_name,
                                                pert_value = value,
                                                job_dict= job,
                                                reverse_mode=False)

                # now handle batch file     
                
                temp_batch['job'].append(job)
        
    if not reverse_protocol == []:
        with open (os.path.join(input_str,'protocol_rev.json'),'r') as p:
            protocol_rev_base = json.load(p)
        for rv in reverse_protocol:
            job = dict()
            job['relative_path'] = True

            temp_protocol = protocol_rev_base
            temp_protocol['perturbation']['perturbations'] = []
            for i,t_span in enumerate(rv['time_s']):
            
                pert=dict()
                pert['level'] = rv['level']
                pert['variable'] = rv['variable']
                pert['t_start_s'] = t_span['t_start_s']
                pert['t_stop_s'] = t_span['t_stop_s']
                value = rv['total_change']
                if i == 0:
                    pert['total_change'] = value
                elif i == 1:
                    pert['total_change'] = -1*value

                temp_protocol['perturbation']['perturbations'].append(pert)
            
            # handle file_name
            if rv['variable'] == 'aorta_resistance':
                valve_name = 'AS'
            elif rv['variable'] == 'mitral_insufficiency_conductance':
                valve_name = 'MR'
            elif rv['variable'] == 'aortic_insufficiency_conductance':
                valve_name = 'AR'

            sim_folder_name = 'simulation_' + valve_name + '_' + str(value) + '_rev'
            pr_file_name = 'protocol_' + valve_name + '_' + str(value) + '_rev' +'.json'
            sim_input_path_str = os.path.join(cwd,sim_folder_name,'sim_inputs')
            pr_file_path = os.path.join(sim_input_path_str,pr_file_name)

            job['protocol_file_string'] = \
                sim_folder_name + '/' + 'sim_inputs' + '/' + pr_file_name

            if not os.path.isdir(sim_input_path_str):
                    print('Making dir')
                    os.makedirs(sim_input_path_str)

            with open(pr_file_path,'w') as f:
                json.dump(temp_protocol,f,indent=4)

            job = handle_model_and_option_files(input_str = input_str,
                                                sim_input_path_str = sim_input_path_str,
                                                sim_folder_name = sim_folder_name,
                                                base_files = base_files,
                                                valve_name = valve_name,
                                                pert_value = value,
                                                job_dict= job,
                                                reverse_mode=True)


            job = handle_output_handler_file(input_str = input_str,
                                                sim_input_path_str = sim_input_path_str,
                                                sim_folder_name = sim_folder_name,
                                                base_files = base_files,
                                                valve_name = valve_name,
                                                pert_value = value,
                                                job_dict= job,
                                                reverse_mode=True)
            temp_batch['job'].append(job)
    # now dump batch file 
    with open ('batch.json','w') as b:
        json.dump(temp_batch,b,indent=4)

    """if not growth_gains == []:
        main_folder_name = 'sensetivity_gain'
        # go through the value
        for gg in growth_gains:
            if gg["type"] == "eccentric":
                ecc_gain_list = gg["growth_factor"]
            else:
                conc_gain_list = gg["growth_factor"]

        #start with eccentric
        for ge in ecc_gain_list:
            ecc_extension = 'ecc' + '_' + str(ge)
            for gc in conc_gain_list:
                con_extension = 'conc' + '_' + str(gc)
                file_ext = '_' + ecc_extension + '_' +con_extension
                folder_name = 'sens' + file_ext
                folder_path_str = os.path.join(cwd,main_folder_name,folder_name)

                temp_model = model_base
                for comp in temp_model['growth']['components']:
                    comp['k_drive'] = 0.01
                    if comp['type'] == 'eccentric':
                        comp['growth_factor'] = ge
                        comp['antigrowth_factor'] = -1*ge
                    else:
                        comp['growth_factor'] = gc
                        comp['antigrowth_factor'] = -1*gc


                sim_input_path_str = os.path.join(folder_path_str,'sim_inputs')
                new_model_file_name = 'model' + file_ext + '.json'
                new_model_str = os.path.join(sim_input_path_str,new_model_file_name)
                #model_ext = 'model' + '_' + ecc_extension + '_' +con_extension
                if not os.path.isdir(sim_input_path_str):
                    print('Making dir')
                    os.makedirs(sim_input_path_str)
                with open(new_model_str,'w') as f:
                    json.dump(temp_model,f,indent=4)

                # now make a copy of all input files from base
                for f in base_files:
                    if f =='options.json':
                        base_file_str = os.path.join(input_str,f)
                        new_file_name = f.split('.')[0]+file_ext+'.json'
                        new_file_str = os.path.join(sim_input_path_str,new_file_name)
                        shutil.copy(base_file_str, new_file_str)
                    elif f == 'protocol.json':
                        temp_protocol = protocol_base
                        temp_protocol["perturbation"]["perturbations"] = []
                        temp_protocol['protocol']['no_of_time_steps'] = 600000
                        new_prot_file_name = 'protocol' + file_ext + '.json'
                        new_prot_str = os.path.join(sim_input_path_str,new_prot_file_name)
                        with open(new_prot_str,'w') as f:
                            json.dump(temp_protocol,f,indent=4)
                    elif f == 'output_handler.json':
                        with open (os.path.join(input_str,'output_handler.json'),'r') as o:
                                output_handler_base = json.load(o)
                        output_handler_new = output_handler_base
                        output_handler_new['templated_images']=[]

                        for img in ['summary_growth']:

                            templated_image = {"relative_path": True,
                                    "template_file_string": "../template/",
                                    "output_file_string": "../sim_output/"}

                            if img == 'summary_growth':
                                extension = 'growth'

                            template_file_name = extension + '.json'
                            templated_image['template_file_string'] = \
                                    templated_image['template_file_string'] + template_file_name
                            # create "template" folder if it does not exist
                            template_dir_str = os.path.join(folder_path_str,'template')
                            if not os.path.isdir(template_dir_str):
                                print('Making template dir')
                                os.makedirs(template_dir_str)

                            template_base_str = os.path.join(input_str,template_file_name)
                            shutil.copy(template_base_str, template_dir_str)

                            templated_image['output_file_string'] = \
                                    templated_image['output_file_string'] + img +'_'+\
                                    file_ext +'.png'

                            output_handler_new['templated_images'].append(templated_image)
                        file_name = 'output_handler'+ file_ext+'.json'
                        file_path = os.path.join(sim_input_path_str,file_name)
                        with open(file_path,'w') as f:
                            json.dump(output_handler_new,f,indent=4)"""
                #print(model_ext)


                        #    output_handler_new['templated_images']
   
def handle_model_and_option_files(input_str = "",
                                    sim_input_path_str = "",
                                    sim_folder_name=[],
                                    base_files=[],
                                    valve_name="",
                                    pert_value=[],
                                    job_dict={},
                                    reverse_mode=False):
  
    for f in base_files:
        if f in ['model.json','options.json']:

            # first get the path from the base files
            base_file_str = os.path.join(input_str,f)

            # now work on the festination path and file name
            if reverse_mode:
                new_file_name = f.split('.')[0]+'_'+valve_name+'_'+str(pert_value)+'_rev'+'.json'
            else:
                new_file_name = f.split('.')[0]+'_'+valve_name+'_'+str(pert_value)+'.json'
            new_file_str = os.path.join(sim_input_path_str,new_file_name)

            if f == 'model.json':
                job_dict['model_file_string'] = \
                    sim_folder_name + '/' + 'sim_inputs' + '/' + new_file_name
            elif f == 'options.json':
                job_dict['sim_options_file_string'] = \
                    sim_folder_name + '/' + 'sim_inputs' + '/' + new_file_name
            # now copy from base to the new directory
            shutil.copy(base_file_str, new_file_str)
           
    return job_dict
def handle_output_handler_file(input_str = "",
                                    sim_input_path_str = "",
                                    sim_folder_name=[],
                                    base_files=[],
                                    valve_name="",
                                    pert_value=[],
                                    job_dict={},
                                    reverse_mode=False):
    cwd = os.getcwd()
    rev_marker = ""
    if reverse_mode:
        rev_marker = '_rev'
    for f in base_files:

        if f == 'output_handler.json':

            with open (os.path.join(input_str,'output_handler.json'),'r') as o:
                output_handler_base = json.load(o)
            output_handler_new = output_handler_base
            output_handler_new['templated_images']=[]

            for img in ['summary_growth','pv']:

                templated_image = {"relative_path": True,
                                "template_file_string": "../template/",
                                "output_file_string": "../sim_output/"}

                if img == 'summary_growth':
                    extension = 'growth_'
                elif img == 'pv':
                    extension = 'pv_'
                template_file_name = extension + valve_name + '.json'
                templated_image['template_file_string'] = \
                    templated_image['template_file_string'] + template_file_name

                # create "template" folder if it does not exist
                template_dir_str = os.path.join(cwd,sim_folder_name,'template')
                if not os.path.isdir(template_dir_str):
                    print('Making template dir')
                    os.makedirs(template_dir_str)

                # get tha path to the base template file name for genrating images
                template_base_str = os.path.join(input_str,template_file_name)
                # now make a copy
                shutil.copy(template_base_str, template_dir_str)

                templated_image['output_file_string'] = \
                            templated_image['output_file_string'] + img +'_'+\
                            valve_name + '_' + str(pert_value)+ rev_marker +'.png'

                output_handler_new['templated_images'].append(templated_image)
            oh_file_name = 'output_handler_'+valve_name+'_'+str(pert_value)+rev_marker +'.json'
            oh_file_path = os.path.join(sim_input_path_str,oh_file_name)
            
            with open(oh_file_path,'w') as f:
                json.dump(output_handler_new,f,indent=4)

            job_dict['output_handler_file_string'] = \
                            sim_folder_name + '/' + 'sim_inputs' + '/' + oh_file_name
            job_dict['sim_results_file_string'] = \
                            sim_folder_name + '/' + 'sim_output' + '/' + 'data' +\
                                 '_' +valve_name+'_'+str(pert_value)+ rev_marker +'.csv'

    return job_dict

if __name__ == '__main__':
    base_inputs_path = 'base_inputs'
    protocol_to_change = [
                        {"level": "circulation",
                        "variable": "aorta_resistance",
                        "t_start_s": 300,
                        "t_stop_s": 400,
                        "total_change": [50,100,150]},
                        {'level': "circulation",
                        "variable": "mitral_insufficiency_conductance",
                        "t_start_s": 300,
                        "t_stop_s": 400,
                        "total_change": [0.001,0.002,0.003]},
                        {'level': "circulation",
                        "variable": "aortic_insufficiency_conductance",
                        "t_start_s": 300,
                        "t_stop_s": 400,
                        "total_change": [0.0005,0.001,0.002]}
                        ]
    reverse_protocol = [
                        {"level": "circulation",
                        "variable": "aorta_resistance",
                        "time_s": [{
                                    "t_start_s": 300,
                                    "t_stop_s": 400,
                                    },
                                    {
                                    "t_start_s": 900,
                                    "t_stop_s": 1000,
                                    }],
                        "total_change": 100},
                        {"level": "circulation",
                        "variable": "mitral_insufficiency_conductance",
                        "time_s": [{
                                    "t_start_s": 300,
                                    "t_stop_s": 400,
                                    },
                                    {
                                    "t_start_s": 900,
                                    "t_stop_s": 1000,
                                    }],
                        "total_change": 0.002},
                        {"level": "circulation",
                        "variable": "aortic_insufficiency_conductance",
                        "time_s": [{
                                    "t_start_s": 300,
                                    "t_stop_s": 400,
                                    },
                                    {
                                    "t_start_s": 900,
                                    "t_stop_s": 1000,
                                    }],
                        "total_change": 0.001}
                       ]
    growth_gains = [{"type": "eccentric",
                    "growth_factor": [1e-5,1e-3,5e-3,1e-2,1e-1]
                    },
                    {"type": "concentric",
                    "growth_factor": [1e-5,1e-3,5e-3,1e-2,1e-1]
                    }


                        ]
    #print(json.dumps(protocol_to_change,indent=4))
    generate_batch_files(input_str = base_inputs_path,
                        protocol_to_change=protocol_to_change,
                        reverse_protocol = reverse_protocol)
