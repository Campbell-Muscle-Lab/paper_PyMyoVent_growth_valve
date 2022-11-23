# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 12:20:56 2022

@author: kscamp3
"""

import os
import json
import shutil
import copy

import numpy as np

from pathlib import Path


def characterize_models():
    """ Characterize_models """

    # Variables
    rel_base_folder = '../base'
    base_model_file = 'base_model.json'
    options_file = 'options.json'
    
    rel_sim_data_folder = '../sim_data'

    rel_template_folder = '../templates'
    template_files = ['single_beat.json', 'summary.json']
    output_image_formats = ['png', 'svg']
    
    time_step = 0.001
    no_of_points = [60000, 60000, 60000, 60000, 60000]
    baro_start_s = [20, 20, 20, 1000, 1000]
    baro_stop_s = [1000, 1000, 1000, 1000, 1000]
    pert_level = ['circulation', 'circulation', 'circulation',
                  'circulation', 'circulation']
    pert_variable = ['ventricle_wall_volume', 'ventricle_wall_volume', 'n_hs',
                     'ventricle_wall_volume', 'n_hs']
    pert_start_s = [40, 40, 40, 40, 40]
    pert_stop_s = [40.1, 40.1, 40.1, 40.1, 40.1]
    pert_total_change = [0.0, 0.03, 15000, 0.03, 15000]
    
    PyMyoVent_code_dir = 'c:/ken/github/campbellmusclelab/models/PyMyovent/Python_code'
    batch_mode = 'create_figures'
    # batch_mode = 'run_batch'
   
    # Work out this folder
    code_folder = Path(__file__).parent.absolute()
    
    # Now work out other relevant folders
    sim_data_folder = Path(os.path.join(code_folder,
                                   rel_sim_data_folder)).resolve()
    base_folder = Path(os.path.join(code_folder,
                                    rel_base_folder)).resolve()
    template_folder = Path(os.path.join(code_folder,
                                        rel_template_folder)).resolve()
  
    # Try to clear existing data
    if not (batch_mode == 'create_figures'):
        try:
            print('Trying to remove: %s' % sim_data_folder)
            shutil.rmtree(sim_data_folder)
        except OSError as e:
            print('Error: %s :%s' % (sim_data_folder, e.strerror))

    # Create batch
    b = dict()
    b['job'] = []
    
    # Create protocols
    for i in range(len(no_of_points)):
        p = dict()
        p['protocol'] = dict()
        p['protocol']['time_step'] = time_step
        p['protocol']['no_of_time_steps'] = no_of_points[i]
        
        p['baroreflex'] = dict()
        p['baroreflex']['activations'] = []
        ba = dict()
        ba['t_start_s'] = baro_start_s[i]
        ba['t_stop_s'] = baro_stop_s[i]
        p['baroreflex']['activations'].append(ba)
        
        p['perturbation'] = dict()
        p['perturbation']['perturbations'] = []
        pe = dict()
        pe['level'] = pert_level[i]
        pe['variable'] = pert_variable[i]
        pe['t_start_s'] = pert_start_s[i]
        pe['t_stop_s'] = pert_stop_s[i]
        pe['total_change'] = pert_total_change[i]
        p['perturbation']['perturbations'].append(pe)
        
        # Make sim_input and sim_output folders
        sim_input_folder = os.path.join(sim_data_folder,
                                        'sim_input',
                                        ('%i' % (i+1)))
        sim_output_folder = os.path.join(sim_data_folder,
                                         'sim_output',
                                         ('%i' % (i+1)))

        for f in [sim_input_folder, sim_output_folder]:
            if not os.path.isdir(f):
                os.makedirs(f)

        # Create the job        
        j = dict()
        j['relative_to'] = 'this_file'
        j['protocol_file_string'] = os.path.join(sim_input_folder,
                                                 'protocol.json')
        j['model_file_string'] = os.path.join(sim_input_folder,
                                              'model.json')
        j['sim_options_file_string'] = os.path.join(sim_input_folder,
                                                    'options.json')
        j['sim_results_file_string'] = os.path.join(sim_output_folder,
                                                    'sim_results.txt')
        j['output_handler_file_string'] = os.path.join(sim_input_folder,
                                                       'output_handler.json')
        
        # Create the files
        
        # Open the model file and rewrite
        orig_model_file = os.path.join(base_folder, base_model_file)
        with open(orig_model_file, 'r') as f:
            m = json.load(f)
        with open(j['model_file_string'], 'w') as f:
            json.dump(m, f, indent=4)
                
        # Open the base options and rewrite
        orig_options_file = os.path.join(base_folder, options_file)
        with open(orig_options_file, 'r') as f:
            o = json.load(f)
        
        # Tweak the options
        o['rates_dump']['file_string'] = ('../../sim_output/%i/rates.txt' % (i+1))
        o['rates_dump']['output_image_file'] = ('../../sim_output/%i/rates' % (i+1))
        o['pas_stress_dump']['file_string'] = ('../../sim_output/%i/pas_stress.txt' % (i+1))
        o['pas_stress_dump']['output_image_file'] = ('../../sim_output/%i/pas_stress' % (i+1))
            
        with open(j['sim_options_file_string'], 'w') as f:
            json.dump(o, f, indent=4)

        # Write the protocol        
        with open(j['protocol_file_string'], 'w') as f:
            json.dump(p, f, indent=4)
        
        # Create the output_handler
        t = dict()
        t['templated_images'] = []
        for k in range(len(template_files)):
            tj = dict()
            tj['relative_to'] = "False"
            tj['template_file_string'] = os.path.join(sim_input_folder,
                                                     template_files[k])
            tj['output_image_file'] = os.path.join(sim_output_folder,
                                                  template_files[k].split('.')[0])
            tj['output_image_formats'] = output_image_formats
            
            t['templated_images'].append(tj)
            
            # Copy template
            orig_template_file = os.path.join(template_folder,
                                              template_files[k])
            with open(orig_template_file, 'r') as f:
                template = json.load(f)
            with open(tj['template_file_string'], 'w') as f:
                json.dump(template, f, indent=4)
        
        # Now write the output handler
        with open(j['output_handler_file_string'], 'w') as f:
            json.dump(t, f, indent=4)
            
        # Append the job
        b['job'].append(j)
        
    # Create the PyMyoVent_batch
    Pb = dict()
    Pb['PyMyoVent_batch'] = b
        
    # Write the batch
    batch_file_string = os.path.join(sim_data_folder, 'batch.json')
    with open(batch_file_string, 'w') as f:
        json.dump(Pb, f, indent=4)
    
    # Generate a command line
    cs = 'pushd \"%s\" & python PyMyoVent.py %s %s & popd' % \
            (PyMyoVent_code_dir, batch_mode, batch_file_string)
            
    print(cs)
    
    # And run it
    os.system(cs)    
    

if __name__ == "__main__":
    characterize_models()
