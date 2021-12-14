from datetime import time
import sys
import pandas as pd
import os
import numpy as np
import json

from PyCMLutil.plots.multi_panel import multi_panel_from_flat_data as mpl
 
def generate_data_lists():
    data_dict = dict()
    data_dict['baseline_baro'] = \
        ['../simulations/simulation_AS_100/sim_output/data_AS_100.csv']

    data_dict['multi_panel_data'] = \
        [
        '../simulations/simulation_AS_100/sim_output/data_AS_100.csv',
        '../simulations/simulation_AS_100_rev/sim_output/data_AS_100_rev.csv',
        '../simulations/simulation_AS_100_no_baro/sim_output/data_AS_100_no_baro.csv',
        '../simulations/simulation_AR_0.001/sim_output/data_AR_0.001.csv',
        '../simulations/simulation_AR_0.001_rev/sim_output/data_AR_0.001_rev.csv',
        '../simulations/simulation_AR_0.001_no_baro/sim_output/data_AR_0.001_no_baro.csv',
        '../simulations/simulation_MR_0.002/sim_output/data_MR_0.002.csv',
        '../simulations/simulation_MR_0.002_rev/sim_output/data_MR_0.002_rev.csv',
        '../simulations/simulation_MR_0.002_no_baro/sim_output/data_MR_0.002_no_baro.csv'
        ]

    data_dict['pv_loop_data'] = dict()
    data_dict['pv_loop_data']['baseline_data'] = \
        '../simulations/simulation_AS_100/sim_output/data_AS_100.csv'
    data_dict['pv_loop_data']['valves_data'] = \
        ['../simulations/simulation_AS_50/sim_output/data_AS_50.csv',
        '../simulations/simulation_AS_100/sim_output/data_AS_100.csv',
        '../simulations/simulation_AS_150/sim_output/data_AS_150.csv',
        '../simulations/simulation_MR_0.001/sim_output/data_MR_0.001.csv',
        '../simulations/simulation_MR_0.002/sim_output/data_MR_0.002.csv',
        '../simulations/simulation_MR_0.003/sim_output/data_MR_0.003.csv',
        '../simulations/simulation_AR_0.0005/sim_output/data_AR_0.0005.csv',
        '../simulations/simulation_AR_0.001/sim_output/data_AR_0.001.csv',
        '../simulations/simulation_AR_0.002/sim_output/data_AR_0.002.csv'
        ] 

    data_dict['reversal_growth_data'] =\
        [
        '../simulations/simulation_AS_100_rev/sim_output/data_AS_100_rev.csv',
        '../simulations/simulation_MR_0.002_rev/sim_output/data_MR_0.002_rev.csv',
        '../simulations/simulation_AR_0.001_rev/sim_output/data_AR_0.001_rev.csv'
        ]  

    data_dict['sim_points_data'] = dict()
    data_dict['sim_points_data']['with_baro'] = \
        ['../simulations/simulation_AS_50/sim_output/data_AS_50.csv',
        '../simulations/simulation_AS_100/sim_output/data_AS_100.csv',
        '../simulations/simulation_AS_150/sim_output/data_AS_150.csv',
        '../simulations/simulation_MR_0.001/sim_output/data_MR_0.001.csv',
        '../simulations/simulation_MR_0.002/sim_output/data_MR_0.002.csv',
        '../simulations/simulation_MR_0.003/sim_output/data_MR_0.003.csv',
        '../simulations/simulation_AR_0.0005/sim_output/data_AR_0.0005.csv',
        '../simulations/simulation_AR_0.001/sim_output/data_AR_0.001.csv',
        '../simulations/simulation_AR_0.002/sim_output/data_AR_0.002.csv']

    data_dict['sim_points_data']['no_baro'] = \
        [
            '../simulations/simulation_AS_100_no_baro/sim_output/data_AS_100_no_baro.csv',
            '../simulations/simulation_AR_0.001_no_baro/sim_output/data_AR_0.001_no_baro.csv',
            '../simulations/simulation_MR_0.002_no_baro/sim_output/data_MR_0.002_no_baro.csv'
        ]


    data_dict['baro_effect'] = \
        [
            'sim_data_points/sim_data_points.xlsx',
            'sim_data_points/sim_data_points_no_baro.xlsx'
        ]


    data_dict['clinical_patient_data'] = \
        ['clinical_data/AS_clinical.xlsx',
        'clinical_data/MR_clinical.xlsx',
        'clinical_data/AR_clinical.xlsx']

    data_dict['clinical_control_data'] = \
        ['clinical_data/control_clinical.xlsx']

    data_dict['con_set_point'] = \
        [
        '../simulations/simulation_AS_100/sim_output/data_AS_100.csv'
        ]

    data_dict['sys_duration'] = \
        [
            '../simulations/simulation_AS_100/sim_output/data_AS_100.csv'
        ]

    data_dict['ecc_set_point'] = \
        [
        '../simulations/simulation_MR_0.002/sim_output/data_MR_0.002.csv'
        ]

    data_dict['dias_duration'] = \
        [
            '../simulations/simulation_MR_0.002/sim_output/data_MR_0.002.csv'
        ]

    data_dict['growth_gain'] = \
        [
            '../simulations/simulation_g_con_0.00333/sim_output/data_g_con_0.00333.csv',
            '../simulations/simulation_g_con_0.005/sim_output/data_g_con_0.005.csv',
            '../simulations/simulation_g_con_0.01/sim_output/data_g_con_0.01.csv',
            '../simulations/simulation_g_con_0.02/sim_output/data_g_con_0.02.csv',
            '../simulations/simulation_g_con_0.03/sim_output/data_g_con_0.03.csv',
            '../simulations/simulation_g_ecc_0.00167/sim_output/data_g_ecc_0.00167.csv', 
            '../simulations/simulation_g_ecc_0.0025/sim_output/data_g_ecc_0.0025.csv',
            '../simulations/simulation_g_ecc_0.005/sim_output/data_g_ecc_0.005.csv',
            '../simulations/simulation_g_ecc_0.01/sim_output/data_g_ecc_0.01.csv',
            '../simulations/simulation_g_ecc_0.015/sim_output/data_g_ecc_0.015.csv'  
        ]



    ### the remaining data path are not necessary ###
    data_dict['growth_rate'] = \
        [
            '../simulations/simulation_k_drive_0.01/sim_output/data_k_drive_0.01.csv',
            '../simulations/simulation_k_drive_0.1/sim_output/data_k_drive_0.1.csv',
            '../simulations/simulation_k_drive_0.2/sim_output/data_k_drive_0.2.csv',
            '../simulations/simulation_k_drive_0.5/sim_output/data_k_drive_0.5.csv',
            '../simulations/simulation_k_drive_1/sim_output/data_k_drive_1.csv'
        ]
 
    data_dict['flow'] = \
        [
        '../simulations/simulation_MR_0.003/sim_output/data_MR_0.003.csv'
        ]
    
    data_dict['WCB_data'] =\
        ['../simulations/simulation_AS_100_rev/sim_output/data_AS_100_rev.csv',
        '../simulations/simulation_MR_0.002_rev/sim_output/data_MR_0.002_rev.csv',
        '../simulations/simulation_AR_0.001_rev/sim_output/data_AR_0.001_rev.csv'] 

    data_dict['int_passive'] = \
        [
           '../simulations/simulation_MR_0.002_rev/sim_output/data_MR_0.002_rev.csv' 
        ]
    
    

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

        # start with generating the baseline simulation results 
        # before activating growth mdoule. (Figure S2)
        if sys.argv[1] == 'baseline_baro' or sys.argv[1] == 'all_figures':
            print('Generating baseline simulation figure ...')  

            template_str = 'temp/template_baseline_baro.json'
            output_str = '../figures/baseline_baro.jpeg'

            mpl(data_file_string = data_dict['baseline_baro'][0],
                template_file_string = template_str,
                output_image_file_string = output_str)
            
        # work out multi panel figures for 
        # Fig2, Fig3, Fig4, FigS7, FigS8, FigS9, FigS10, FigS11, and FigS12
        if sys.argv[1] == 'multi_panel' or sys.argv[1] == 'all_figures':
            print('Generating multi panel figures ...')  
            
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
                    output_image_file_string = output_str,
                    dpi = 300)

        # work out pv_loop Fig5
        # first export data from giant spreadsheet out of pymyovent
        if sys.argv[1] == 'pv_loop':

            from multi_panel_pv import multi_panel_from_flat_data as mpv

            output_pv_data_str = 'pv_data/pv_data.xlsx'
            template_str = 'temp/template_pv_loop.json'
            output_str = '../figures/pv_loop.jpeg'
            time_frames = [(298,299),(780,781)]
            
            # handle baseline data first
            pv_loop_data = pd.DataFrame()
            baseline_data = pd.read_csv(data_dict['pv_loop_data']['baseline_data'])
            baseline_data = baseline_data[baseline_data['time'].between(
                                time_frames[0][0],time_frames[0][-1])].reset_index()

            for var in ['volume_ventricle', 'pressure_ventricle']:
                new_var_name = var + '_' + 'baseline'
                pv_loop_data[new_var_name] = baseline_data[var]
            print('baseline data is handled!')

            # now handle valves data
            for d in data_dict['pv_loop_data']['valves_data']:
                temp_data = pd.read_csv(d)
                temp_data = temp_data[temp_data['time'].between(
                    time_frames[-1][0],time_frames[-1][-1])].reset_index()
                for var in ['volume_ventricle', 'pressure_ventricle']: 
                    new_var_name = var + '_' + d.split('data_')[-1].split('.csv')[0]
                    pv_loop_data[new_var_name] = temp_data[var]
                print(f'{d} is completed!')

            # save data if it is asked
            if output_pv_data_str:
                output_dir = os.path.dirname(output_pv_data_str)
                if not os.path.isdir(output_dir):
                    print('Making output dir')
                    os.makedirs(output_dir)
                pv_loop_data.to_excel(output_pv_data_str)
            
            # then plot data
            mpv(pandas_data = pv_loop_data,
                template_file_string= template_str,
                output_image_file_string = output_str)

        elif sys.argv[1] == 'pv_loop_show' or sys.argv[1] == 'all_figures':

            from multi_panel_pv import multi_panel_from_flat_data as mpv

            data_file_str = 'pv_data/pv_data.xlsx'
            template_str = 'temp/template_pv_loop.json'
            output_str = '../figures/pv_loop.jpeg'

            mpv(data_file_string = data_file_str,
                template_file_string= template_str,
                output_image_file_string = output_str)
        
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
                for var in ['volume_ventricle','ventricle_wall_thickness']:
                    new_var_name = var + '_' + ext_name
                    data_rev[new_var_name] = pd.Series()
                    data_rev[new_var_name] = temp_data[var]
                print(f'{d} is completed!')

            mpl(pandas_data = data_rev,
                template_file_string= template_str,
                output_image_file_string = output_str)   
 
        # now start extracting data points usefule for 
        # Fig7, Fig8, and Fig9
        if sys.argv[1] == 'extract_sim_data':

            # extract data based on wether they have baroreflex or not
            for data_sim in data_dict['sim_points_data']:
                print(data_sim.split('_')[0]) 
                if data_sim.split('_')[0] == 'with':
                    extraction_prot_str = 'temp/data_extract_protocol.json'
                    extracted_data_frame_str = 'sim_data_points/sim_data_points.xlsx'
                elif data_sim.split('_')[0] == 'no':
                    extraction_prot_str = 'temp/data_extract_protocol_no_baro.json'
                    extracted_data_frame_str = 'sim_data_points/sim_data_points_no_baro.xlsx'
           
                sim_data_points = pd.DataFrame()

                from library import quantify_ventricle_function as qvf
                from library import return_extracted_data

                for d in data_dict['sim_points_data'][data_sim]:
                    print(d)
                    valvular_disorder = \
                        d.split('data_')[-1].split('.csv')[0].split('_')[0]

                    # chcek if data is belonged to no_baroreflex cases
                    if d.split('data_')[-1].split('.csv')[0].split('_')[-1] == 'baro':
                        extraction_prot_str = 'temp/data_extract_protocol_no_baro.json'
                
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
                    temp_extracted_data['overloading_type'].loc[temp_extracted_data['subject_type']=='Baseline (Sim)'] = 'Baseline' 
                    print(f'data points are extracted from {d}.')
                    sim_data_points = sim_data_points.append(temp_extracted_data,ignore_index = True)
                
                # now save extracted data from processed data 
                if extracted_data_frame_str:
                    output_dir = os.path.dirname(extracted_data_frame_str)
                    if not os.path.isdir(output_dir):
                        print('Making output dir')
                        os.makedirs(output_dir)
                    sim_data_points.to_excel(extracted_data_frame_str)

        # now that you have extracted simulation data
        # you can generate Fig7 (baroreflex effect)
        if sys.argv[1] == 'baro_effect' or sys.argv[1] == 'all_figures':
            
            from multi_panel_cat import multi_panel_cat_from_flat_data as mplc

            output_data_str = 'sim_data_points/baro_effect.xlsx'
            template = 'temp/template_baro_effect.json'
            output_image_file_string = '../figures/baro_effect.jpeg'

            rows_to_pick = ['500.0%','40.0 ml','60.0 ml']
            cols = ['LVEDV', 'LVESV', 'ESP_vent', 'LVMi','SVi',
                    'COi', 'EF', 'SW', 'ESap', 'EDap', 'Vol_wall',
                    'nhs', 'ES_tw', 'ED_tw','overloading_type','valvular_disorder']

            for i,d in enumerate (data_dict['baro_effect']):
                if 'no_baro' in d:
                    no_baro_data = pd.read_excel(d)
                    
                    no_baro_data = \
                        no_baro_data.loc[no_baro_data['overloading_type'].isin(rows_to_pick)].reset_index()

                    no_baro_data = no_baro_data[cols]
                    no_baro_data['baro_status'] = 'No baroreflex'
                    
                else: 
                    baro_data = pd.read_excel(d)
                    baro_data = \
                        baro_data.loc[baro_data['overloading_type'].isin(rows_to_pick)].reset_index()
                    baro_data = baro_data[cols]
                    baro_data['baro_status'] = 'Baroreflex'


            baro_effect_data = baro_data.append(no_baro_data, ignore_index = True)

            # replace accronyms with complete names for valvular disease 
            baro_effect_data['valvular_disorder'].loc[baro_effect_data['valvular_disorder'] == 'AS'] = \
                'Aortic stenosis'
            
            baro_effect_data['valvular_disorder'].loc[baro_effect_data['valvular_disorder'] == 'AR'] = \
                'Aortic insufficiency'

            baro_effect_data['valvular_disorder'].loc[baro_effect_data['valvular_disorder'] == 'MR'] = \
                'Mitral insufficiency'
                                                
            if output_data_str:
                output_dir = os.path.dirname(output_data_str)
                if not os.path.isdir(output_dir):
                    print('Making output dir')
                    os.makedirs(output_dir)
                print(f'Saving to {output_data_str}')
                baro_effect_data.to_excel(output_data_str)
 
            mplc(pandas_data = [baro_effect_data],
                    template_file_string = template,
                    output_image_file_string = output_image_file_string)

                
        # now arrange the extracted simulated data ready to plot
        # Fig8 and Fig9
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
            
            sim_data_str = ['sim_data_points/sim_data_points.xlsx']
            var_to_extract = ['LVEDVi','LVESVi','LVMi','SVi','EF','subject_type']

            # first handle control data and save it to a pandas dataframe
            raw_control_data = pd.read_excel(data_dict['clinical_control_data'][0])
            # now extract data from it 
            control_data = pd.DataFrame()
            for var in var_to_extract: 
                #control_data[var] = pd.Series()
                if var =='subject_type':
                    control_data[var] = 'Control'
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
                        clinical_data[var] = 'Patient'
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
        # we can generate Fig8 and Fig9       
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


        # now handle FigS3
        if sys.argv[1] == 'con_set_point' or sys.argv[1] == 'all_figures':

            pandas_data = pd.read_csv(data_dict['con_set_point'][0])

            pandas_data['mean_ATPase_to_myo'] = \
                pandas_data['ATPase_to_myo'].rolling(window = 40000).mean()

            pandas_data['mean_ATPase_to_myo'].loc[pandas_data['mean_ATPase_to_myo'].isna()] = \
                pandas_data['mean_ATPase_to_myo'].loc[pandas_data['mean_ATPase_to_myo'].notna()].to_numpy()[0]

            print(pandas_data['mean_ATPase_to_myo'].loc[pandas_data['mean_ATPase_to_myo'].notna()].to_numpy()[0])
            template_file_string = 'temp/template_con_set_point.json'
            output_str = '../figures/con_set_point.jpeg'

            mpl(pandas_data = pandas_data,
                template_file_string = template_file_string,
                output_image_file_string = output_str)

        # now handle FigS4
        if sys.argv[1] == 'sys_duration' or sys.argv[1] == 'all_figures':

            data = pd.read_csv(data_dict['sys_duration'][0])
            data = data[['time','ATPase_to_myo']]   
            time_frames = [(289,290),(789.275,790.25)] 
            data_to_plot = pd.DataFrame()

            for i,tf in enumerate(time_frames):
                temp_data = pd.DataFrame()
                temp_data = data.loc[data['time'].between(
                    tf[0],tf[-1])].reset_index()
                temp_data['time'] = temp_data['time'] - tf[0]
                
                if i == 0:
                    ext_name = 'baseline'
                else:
                    ext_name = 'growth'
                for col_name in temp_data.columns:
                    new_col_name = col_name + '_' + ext_name
                    data_to_plot[new_col_name] = temp_data[col_name]

            template_str = 'temp/template_sys_duration.json'
            output_str = '../figures/sys_duration.jpeg'

            mpl(pandas_data = data_to_plot,
                template_file_string= template_str,
                output_image_file_string = output_str,
                dpi=200) 

        # now handle FigS5
        if sys.argv[1] == 'ecc_set_point' or sys.argv[1] == 'all_figures':

            pandas_data = pd.read_csv(data_dict['ecc_set_point'][0])
            pandas_data['mean_cpt_int_pas_stress'] = \
                pandas_data['cpt_int_pas_stress'].rolling(window = 10000).mean()
            pandas_data['mean_cpt_int_pas_stress'].loc[pandas_data['mean_cpt_int_pas_stress'].isna()] = \
                pandas_data['mean_cpt_int_pas_stress'].loc[pandas_data['mean_cpt_int_pas_stress'].notna()].to_numpy()[0]
            template_file_string = 'temp/template_ecc_set_point.json'
            output_str = '../figures/ecc_set_point.jpeg'

            mpl(pandas_data = pandas_data,
                template_file_string = template_file_string,
                output_image_file_string = output_str)

        # now handle FigS6
        if sys.argv[1] == 'dias_duration' or sys.argv[1] == 'all_figures':

            data = pd.read_csv(data_dict['dias_duration'][0])
            data = data[['time','cpt_int_pas_stress']]   
            time_frames = [(289.49,290.49),(789.3,790.25)]
            data_to_plot = pd.DataFrame()

            for i,tf in enumerate(time_frames):
                temp_data = pd.DataFrame()
                temp_data = data.loc[data['time'].between(
                    tf[0],tf[-1])].reset_index()
                temp_data['time'] = temp_data['time'] - tf[0]
                
                if i == 0:
                    ext_name = 'baseline'
                else:
                    ext_name = 'growth'
                for col_name in temp_data.columns:
                    new_col_name = col_name + '_' + ext_name
                    data_to_plot[new_col_name] = temp_data[col_name]

            template_str = 'temp/template_dias_duration.json'
            output_str = '../figures/dias_duration.jpeg'

            mpl(pandas_data = data_to_plot,
                template_file_string= template_str,
                output_image_file_string = output_str,
                dpi=200)

        # now handle FigS1
        if sys.argv[1] == 'growth_gain' or sys.argv[1] == 'all_figures':
            
            output_data_str = 'growth_gain.csv'
            template_str = 'temp/template_growth_gain.json'
            output_str = '../figures/growth_gain.jpeg'
            data_growth_rate = pd.DataFrame()
            
            for d in data_dict['growth_gain']:
                print(d)
                temp_data = pd.read_csv(d)
                ext_name = d.split('data_')[-1].split('.csv')[0]
                if 'time' not in data_growth_rate.columns:
                    data_growth_rate['time'] = pd.Series()
                    data_growth_rate['time']= temp_data['time']
                    print(data_growth_rate['time'])
                for var in ['n_hs','ventricle_wall_volume']:

                    if var in ['growth_concentric_c','growth_eccentric_c',
                                'growth_concentric_g','growth_eccentric_g']:
                        new_var_name = 'mean' + '_' + var + '_' + ext_name
                        data_growth_rate[new_var_name] = \
                            temp_data[var].rolling(window= 50000).mean()
                        data_growth_rate[new_var_name].loc[data_growth_rate[new_var_name].isna()] = \
                            data_growth_rate[new_var_name].loc[data_growth_rate[new_var_name].notna()].to_numpy()[0]
                    else:
                        new_var_name = var + '_' + ext_name
                        data_growth_rate[new_var_name] = pd.Series()
                        data_growth_rate[new_var_name] = temp_data[var]
                print(f'{d} is completed!')

            if output_data_str:
                data_growth_rate.to_csv(output_data_str)

            mpl(pandas_data = data_growth_rate,
                template_file_string= template_str,
                output_image_file_string = output_str) 

        if sys.argv[1] == 'growth_gain_show':

            data_str = 'growth_gain.csv'
            template_str = 'temp/template_growth_gain.json'
            output_str = '../figures/growth_gain.jpeg'
            
            mpl(data_file_string = data_str,
                template_file_string= template_str,
                output_image_file_string = output_str) 
        



        #### below codes are not necessary for the paper ###
        if sys.argv[1] == 'flow':
            template_str = 'temp/template_pressure_volume.json'
            output_str = '../figures/flow.jpeg'
            

            mpl(data_file_string = data_dict['flow'][0],
                template_file_string= template_str,
                output_image_file_string = output_str)  

        if sys.argv[1] == 'growth_rate':

            template_str = 'temp/template_growth_rate.json'
            output_str = '../figures/growth_rate.jpeg'
            data_growth_rate = pd.DataFrame()
            
            for d in data_dict['growth_rate']:
                temp_data = pd.read_csv(d)
                ext_name = d.split('data_')[-1].split('.csv')[0]
                if 'time' not in data_growth_rate.columns:
                    data_growth_rate['time'] = pd.Series()
                    data_growth_rate['time']= temp_data['time']
                for var in ['n_hs','ventricle_wall_volume',\
                            'growth_concentric_c','growth_eccentric_c',
                            'growth_concentric_g','growth_eccentric_g']:

                    if var in ['growth_concentric_c','growth_eccentric_c',
                                'growth_concentric_g','growth_eccentric_g']:
                        new_var_name = 'mean' + '_' + var + '_' + ext_name
                        data_growth_rate[new_var_name] = \
                            temp_data[var].rolling(window= 50000).mean()
                        data_growth_rate[new_var_name].loc[data_growth_rate[new_var_name].isna()] = \
                            data_growth_rate[new_var_name].loc[data_growth_rate[new_var_name].notna()].to_numpy()[0]
                    else:
                        new_var_name = var + '_' + ext_name
                        data_growth_rate[new_var_name] = pd.Series()
                        data_growth_rate[new_var_name] = temp_data[var]
                print(f'{d} is completed!')

            mpl(pandas_data = data_growth_rate,
                template_file_string= template_str,
                output_image_file_string = output_str)

        if sys.argv[1] == 'WCB':
            output_data_str = 'WCB_data.csv'
            template_str = 'temp/template_WCB.json'
            output_str = '../figures/WCB.jpeg'
            data_WCB = pd.DataFrame()
            
            for d in data_dict['WCB_data']:
                temp_data = pd.read_csv(d)
                ext_name = d.split('data_')[-1].split('.csv')[0]
                if 'time' not in data_WCB.columns:
                    data_WCB['time'] = pd.Series()
                    data_WCB['time']= temp_data['time']
                for var in ['volume_ventricle','ventricle_wall_thickness',
                            'cpt_int_pas_stress','gr_eccentric_set',
                            'ATPase_to_myo','gr_concentric_set',
                            'pressure_arteries','baro_b_setpoint','heart_rate',
                            'hs_stress','cb_stress','int_pas_stress',
                            'hs_length']:
                    new_var_name = var + '_' + ext_name
                    data_WCB[new_var_name] = pd.Series()
                    data_WCB[new_var_name] = temp_data[var]
                print(f'{d} is completed!')

            if output_data_str:
                data_WCB.to_csv(output_data_str)

            mpl(pandas_data = data_WCB,
                template_file_string= template_str,
                output_image_file_string = output_str,
                dpi=200)  
        
        if sys.argv[1] == 'WCB_show':
            template_str = 'temp/template_WCB.json'
            output_str = '../figures/WCB.jpeg'
            data_str = 'WCB_data.csv'

            mpl(data_file_string = data_str,
                template_file_string= template_str,
                output_image_file_string = output_str,
                dpi=200)  

        if sys.argv[1] == 'int_passive':
            from multi_panel import multi_panel_from_flat_data as multi_panel
            template_str = ['temp/template_int_passive_baseline.json',
                            'temp/template_int_passive_diseased.json']
            data_int = pd.read_csv(data_dict['int_passive'][0]) 
            data_int = data_int[['time','cpt_int_pas_stress']]
            data_int['cpt_int_pas_stress_systole_base'] = data_int['cpt_int_pas_stress']
            data_int['cpt_int_pas_stress_systole_base'].loc[data_int['time']>290.4] = None
            data_int['cpt_int_pas_stress_diastole_base'] = data_int['cpt_int_pas_stress']
            data_int['cpt_int_pas_stress_diastole_base'].loc[data_int['time']>290.9] = None
            data_int['cpt_int_pas_stress_diastole_diseased'] = data_int['cpt_int_pas_stress']
            data_int['cpt_int_pas_stress_diastole_diseased'].loc[data_int['time']>390.9] = None


            for temp in template_str:
                fig_name = temp.split('template_')[-1].split('.json')[0] + '.jpeg'
                fig_str = '../figures/' + fig_name

                print(fig_str) 
                multi_panel(pandas_data = data_int,
                            template_file_string= temp,
                            output_image_file_string = fig_str,
                            dpi=300)  
        
        


                    



