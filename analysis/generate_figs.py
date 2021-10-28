from datetime import time
import sys
import pandas as pd
import os
import numpy as np

from PyCMLutil.plots.multi_panel import multi_panel_from_flat_data as mpl

def display_pv_loops(data_str = [], time_frames = [], output_str = ''):

    from PyCMLutil.plots.pv_plots import display_pv_loop as pv
    pv(data_file_string = data_str,
                time_frames = time_frames,
                pressure_var_name = 'pressure_ventricle',
                volume_var_name = 'volume_ventricle',
                template_data = {'formatting':{'palette':'Set2'},'layout':{'fig_width':8}},
                time_var_name = 'time',
                legend_labels = ['Baseline','Aortic Stenosis','Mitral Regurgitation','Aortic Regurgitation'],
                output_image_file_string = output_str,
                dpi = 300)
def generate_data_lists():
    data_dict = dict()
    data_dict['pv_loop_data'] = \
        ['../simulations/simulation_AS_100/sim_output/data_AS_100.csv',
        '../simulations/simulation_AS_100/sim_output/data_AS_100.csv',
        '../simulations/simulation_MR_0.002/sim_output/data_MR_0.002.csv',
        '../simulations/simulation_AR_0.001/sim_output/data_AR_0.001.csv']

    data_dict['multi_panel_data'] = \
        ['../simulations/simulation_AS_100/sim_output/data_AS_100.csv',
        '../simulations/simulation_AS_100_rev/sim_output/data_AS_100_rev.csv',
        '../simulations/simulation_MR_0.002/sim_output/data_MR_0.002.csv',
        '../simulations/simulation_MR_0.002_rev/sim_output/data_MR_0.002_rev.csv',
        '../simulations/simulation_AR_0.001/sim_output/data_AR_0.001.csv',
        '../simulations/simulation_AR_0.001_rev/sim_output/data_AR_0.001_rev.csv']
    
    data_dict['reversal_growth_data'] =\
        ['../simulations/simulation_AS_100_rev/sim_output/data_AS_100_rev.csv',
        '../simulations/simulation_MR_0.002_rev/sim_output/data_MR_0.002_rev.csv',
        '../simulations/simulation_AR_0.001_rev/sim_output/data_AR_0.001_rev.csv'] 

    data_dict['multi_panel_discussion_data'] = \
        ['../simulations/simulation_AS_100/sim_output/data_AS_100.csv',
        '../simulations/simulation_MR_0.002/sim_output/data_MR_0.002.csv']

    data_dict['sim_points_data'] = \
        ['../simulations/simulation_AS_50/sim_output/data_AS_50.csv',
        '../simulations/simulation_AS_100/sim_output/data_AS_100.csv',
        '../simulations/simulation_AS_150/sim_output/data_AS_150.csv',
        '../simulations/simulation_MR_0.001/sim_output/data_MR_0.001.csv',
        '../simulations/simulation_MR_0.002/sim_output/data_MR_0.002.csv',
        '../simulations/simulation_MR_0.003/sim_output/data_MR_0.003.csv',
        '../simulations/simulation_AR_0.0005/sim_output/data_AR_0.0005.csv',
        '../simulations/simulation_AR_0.001/sim_output/data_AR_0.001.csv',
        '../simulations/simulation_AR_0.002/sim_output/data_AR_0.002.csv']

    data_dict['clinical_patient_data'] = \
        ['clinical_data/AS_clinical.xlsx',
        'clinical_data/MR_clinical.xlsx',
        'clinical_data/AR_clinical.xlsx']

    data_dict['clinical_control_data'] = \
        ['clinical_data/control_clinical.xlsx']

    return data_dict
if __name__ == '__main__':
    no_of_arguments = len(sys.argv)
    if no_of_arguments == 1:
        print(no_of_arguments)
        print('No instruction file has been called!')
        print('Exiting...')
    elif no_of_arguments == 2:
        print(no_of_arguments)
        print(sys.argv[1])

        # first define data list 
        data_dict = generate_data_lists()

        # work out multi panel figures for 
        # Fig2, Fig3, Fig4, FigS1, FigS2, and FigS3
        if sys.argv[1] == 'multi_panel' or sys.argv[1] == 'all_figures':
            
            for d in data_dict['multi_panel_data']:

                pert_type = d.split('data_')[-1].split('_')[0]
                sim_type = d.split('data_')[-1].split('.csv')[0]
                print(pert_type)

                output_str = '../figures/' + sim_type + '.jpeg'
                template_file_string = 'temp/template_'+ sim_type + '.json'
                pandas_data = pd.read_csv(d)

                if pert_type == 'MR':
                    pandas_data['mitral_reg_volume_max'] = \
                    (-1*pandas_data['mitral_reg_volume']).rolling(window = 2000).max()

                elif pert_type == 'AR':
                    pandas_data['aortic_reg_volume_max'] = \
                    (-1*pandas_data['aortic_reg_volume']).rolling(window = 2000).max()

                mpl(pandas_data = pandas_data,
                    template_file_string = template_file_string,
                    output_image_file_string = output_str)

        # work out pv_loop Fig5
        if sys.argv[1] == 'pv_loop' or sys.argv[1] == 'all_figures':

            output_str = '../figures/pv_loop.jpeg'
            time_frames = [(298,299),(780,781),(780,781),(780,781)]
            display_pv_loops(data_str = data_dict['pv_loop_data'],
                            time_frames = time_frames,
                            output_str = output_str)

        # work out pv_loop Fig6
        if sys.argv[1] == 'reverse_growth' or sys.argv[1] == 'all_figures':
            
            template_str = 'temp/template_reverse.json'
            output_str = '../figures/reversal_growth.jpeg'
            data_rev = pd.DataFrame()
            
            for d in data_dict['reversal_growth_data']:
                temp_data = pd.read_csv(d)
                ext_name = d.split('data_')[-1].split('.csv')[0]
                if 'time' not in data_rev.columns:
                    data_rev['time'] = pd.Series()
                    data_rev['time']= temp_data['time']
                for var in ['volume_ventricle','ventricle_wall_thickness',
                            'cpt_int_pas_stress','gr_eccentric_set',
                            'ATPase_to_myo','gr_concentric_set']:
                    new_var_name = var + '_' + ext_name
                    data_rev[new_var_name] = pd.Series()
                    data_rev[new_var_name] = temp_data[var]
                print(f'{d} is completed!')

            mpl(pandas_data = data_rev,
                template_file_string= template_str,
                output_image_file_string = output_str)        
        
        # work out Fig7 and Fig8
        # first extract data points from simulated pymyovent raw data
        if sys.argv[1] == 'extract_sim_data' or sys.argv[1] == 'all_figures':
            
            extraction_prot_str = 'temp/data_extract_protocol.json'
            extracted_data_frame_str = 'sim_data_points/sim_data_points.xlsx'
            sim_data_points = pd.DataFrame()

            from library import quantify_ventricle_function as qvf
            from library import return_extracted_data

            for d in data_dict['sim_points_data']:
                valvular_disorder = \
                    d.split('data_')[-1].split('.csv')[0].split('_')[0]
                # first do some data proccessing on raw data from pymyovent
                temp_data = qvf(pandas_data = pd.read_csv(d))
                # then extract data point according to the protocol: extraction_prot_str
                temp_extracted_data = return_extracted_data(pandas_data = temp_data,
                                                            protocol_file_srt = extraction_prot_str)
                print(f'data {d} is processed now')

                if valvular_disorder == 'AS':
                    aorta_res_list = \
                        temp_data['aorta_resistance'].to_numpy()
                    overloading_level = \
                        float(((aorta_res_list[-1]-aorta_res_list[0])/aorta_res_list[0]).round(2))*100
                    overloading_type = str(overloading_level) + '%'

                elif valvular_disorder in ['MR', 'AR']:
                    if valvular_disorder == 'MR':
                        reg_var_name = 'mitral_reg_volume'
                    else:
                        reg_var_name = 'aortic_reg_volume'
                    regurgitatnt_volume = \
                        (-1*temp_data[reg_var_name]).rolling(window = 2000).max()
                    regurgitatnt_volume_list = regurgitatnt_volume.to_numpy()
                    overloading_level = float(1000*regurgitatnt_volume_list[-1].round(2))
                    overloading_type = str(overloading_level) + ' ' + 'ml'

                temp_extracted_data['valvular_disorder'] = valvular_disorder
                temp_extracted_data['overloading_type'] = overloading_type
                temp_extracted_data['overloading_type'].loc[temp_extracted_data['subject_type']=='control'] = 'baseline'
                print(f'data points are extracted from {d}.')
                sim_data_points = sim_data_points.append(temp_extracted_data,ignore_index = True)
            
            # now save extracted data from processed data 
            if extracted_data_frame_str:
                output_dir = os.path.dirname(extracted_data_frame_str)
                if not os.path.isdir(output_dir):
                    print('Making output dir')
                    os.makedirs(output_dir)
                sim_data_points.to_excel(extracted_data_frame_str)
                
        # now arrange extracted simulated data ready to plot
        if sys.argv[1] == 'arrange_sim_data' or sys.argv[1] == 'all_figures':

            sim_data_str = ['sim_data_points/sim_data_points.xlsx']
            cols_to_pick = \
                ['LVEDVi','LVESVi','LVMi','SVi','EF','subject_type','overloading_type']

            sim_data = pd.read_excel(sim_data_str[0])

            for valve in sim_data['valvular_disorder'].unique():

                temp_sim_data = sim_data.loc[sim_data['valvular_disorder']==\
                        valve].drop_duplicates(subset=['overloading_type']).reset_index()

                temp_sim_data = temp_sim_data[cols_to_pick]
                # convert volumes to ml
                temp_sim_data[['LVEDVi','LVESVi','SVi']] = temp_sim_data[['LVEDVi','LVESVi','SVi']]*1e3
                # convert EF to percent
                temp_sim_data['EF'] = temp_sim_data['EF']*1e2
                data_file_name = valve + '_sim.xlsx'
                output_data_str = os.path.join('sim_data_points',data_file_name)

                output_dir = os.path.dirname(output_data_str)
                if not os.path.isdir(output_dir):
                    print('Making output dir')
                    os.makedirs(output_dir)
                print(f'saving clinical data to {output_data_str}')
                temp_sim_data.to_excel(output_data_str)

        # now work out clinical data
        if sys.argv[1] == 'arrange_clinical_data' or sys.argv[1] == 'all_figures':
            
            patients_clinical_data_str = ['clinical_data/AS_clinical.xlsx',
                                        'clinical_data/MR_clinical.xlsx',
                                        'clinical_data/AR_clinical.xlsx']
            control_clinical_data_str = ['clinical_data/control_clinical.xlsx']
            sim_data_str = ['sim_data_points/sim_data_points.xlsx']
            #output_data_str = 'clinical_data/clinical_data.xlsx'
            var_to_extract = ['LVEDVi','LVESVi','LVMi','SVi','EF','subject_type']

            # handle control data and save it to a pandas dataframe
            raw_control_data = pd.read_excel(data_dict['clinical_control_data'][0])
            # now extract data from it 
            control_data = pd.DataFrame()
            for var in var_to_extract: 
                #control_data[var] = pd.Series()
                if var =='subject_type':
                    control_data[var] = 'control'
                else:
                    control_data[var] = raw_control_data[var]

            # now that you have control data, handle the patient data
            clinical_data = pd.DataFrame()
            for cd in data_dict['clinical_patient_data']:
                clinical_data = pd.DataFrame()
                print(cd)
           
                valvular_type = cd.split('clinical_data/')[-1].split('_')[0]
                data_file_name = valvular_type + '_to_plot.xlsx'
                
                raw_patient_data = pd.read_excel(cd)
                for var in var_to_extract:
                    #clinical_data[var]= pd.Series() 
                    if var =='subject_type':
                        clinical_data[var] = 'patients'
                    else:
                        clinical_data[var] = raw_patient_data[var]
                
                # now append control data
                clinical_data = clinical_data.append(control_data,ignore_index = True)

                # if SVi is not availble in clinical data, 
                # then calculate it from LV volumes
                clinical_data['SVi'].loc[clinical_data['SVi'].isnull()] = \
                        clinical_data['LVEDVi'] - clinical_data['LVESVi']

                # now save the file 
                output_data_str = os.path.join('clinical_data',data_file_name)
                output_dir = os.path.dirname(output_data_str)
                if not os.path.isdir(output_dir):
                    print('Making output dir')
                    os.makedirs(output_dir)
                print(f'saving clinical data to {output_data_str}')
                clinical_data.to_excel(output_data_str)

        # now that we have extracted simulated data and arranged clinical data
        # we can generate Fig7 and Fig8       
        if sys.argv[1] == 'validate' or sys.argv[1] == 'all_figures':
            from multi_panel_cat import multi_panel_cat_from_flat_data as mplc

            data_str = ['clinical_data/AS_to_plot.xlsx',
                        'clinical_data/MR_to_plot.xlsx',
                        'clinical_data/AR_to_plot.xlsx',
                        'sim_data_points/AS_sim.xlsx',
                        'sim_data_points/MR_sim.xlsx',
                        'sim_data_points/AR_sim.xlsx']
            
            template_str = ['temp/template_clinical_dim.json',
                            'temp/template_clinical_sys.json']
            for template in template_str:
                type = template.split('clinical_')[-1].split('.json')[0]
                output_image_file_string = '../figures/' + 'clinical_' + type +'.jpeg'
                mplc(data_file_string=data_str,
                        template_file_string=template,
                        output_image_file_string=output_image_file_string,
                        dpi=300)

        # finally generate discussion figure (Fig9 and Fig10)
        if sys.argv[1] == 'cell_level_multi_panel' or sys.argv[1] == 'all_figures':

            for d in data_dict['multi_panel_discussion_data']:

                pert_type = d.split('data_')[-1].split('_')[0]
                sim_type = d.split('data_')[-1].split('.csv')[0] + '_cell'
                
                output_str = '../figures/' + sim_type + '.jpeg'
                template_file_string = 'temp/template_'+ sim_type + '.json'
                pandas_data = pd.read_csv(d)

                mpl(pandas_data = pandas_data,
                    template_file_string = template_file_string,
                    output_image_file_string = output_str)

                