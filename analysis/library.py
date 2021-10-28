

import numpy as np
import pandas as pd
import json

def quantify_ventricle_function(pandas_data,
                        body_surface_area = 1.9,
                        mayocardial_density = 1265,
                        rolling_window = 2000):

    """
    Parameters
    -------------
    pandas_data: pandas DataFrame
    body_syrface_area: float, optional
        An index for normalizing/ indexing of LV dimensions and systolic functions.
        default : 1.0
    myocardial_density: float, optional
        Density of LV muscle.
        default : 1055 gram/liters
    rolling_window: integer, optional
        Size of the moving window. This is the number of observations used for
        calculating the statistic. Each window will be a fixed size.
        default : 2000 points

    Returns
    -------------
    Pandas data frame with added columns from this script.
    """

     #starting with LV dimensions first

    pandas_data['ED_volume_ventricle'] = \
        pandas_data['volume_ventricle'].rolling(window = rolling_window).max()
    pandas_data['ES_volume_ventricle'] = \
        pandas_data['volume_ventricle'].rolling(window = rolling_window).min()

    pandas_data['ventricle_wall_mass'] = \
        pandas_data['ventricle_wall_volume'] * mayocardial_density

    pandas_data['ES_ventricle_wall_thickness'] = \
        pandas_data['ventricle_wall_thickness'].rolling(window = rolling_window).max()
    pandas_data['ED_ventricle_wall_thickness'] = \
        pandas_data['ventricle_wall_thickness'].rolling(window = rolling_window).min()

    pandas_data['ES_ventricle_pressure'] = \
        pandas_data['pressure_ventricle'].rolling(window = rolling_window).max()
    pandas_data['ES_arterial_pressure'] = \
        pandas_data['pressure_arteries'].rolling(window = rolling_window).max()
    pandas_data['ED_arterial_pressure'] = \
        pandas_data['pressure_arteries'].rolling(window = rolling_window).min()
    # now start indexing LV geometry parameters
    pandas_data['ED_volume_ventricle_indexed'] = \
        pandas_data['ED_volume_ventricle'] / body_surface_area
    pandas_data['ES_volume_ventricle_indexed'] = \
        pandas_data['ES_volume_ventricle'] / body_surface_area

    pandas_data['ventricle_wall_mass_indexed'] = \
        pandas_data['ventricle_wall_mass'] / body_surface_area

    pandas_data['cardiac_output'] = \
        pandas_data['heart_rate'] * pandas_data['stroke_volume']
    pandas_data['stroke_volume_indexed'] = \
        pandas_data['stroke_volume'] /  body_surface_area
    pandas_data['cardiac_output_indexed'] = \
        pandas_data['cardiac_output'] /  body_surface_area

    return pandas_data

def return_extracted_data(pandas_data=[],
                            protocol_file_srt = ""):

    """
    Parameters
    -------------
    pandas_data: pandas DataFrame
    protocol_file_srt : A protocol file in json format for extracting
                    data points from simulated data frame of PyMyoVent.
    Returns
    -------------
    Pandas data frame with added columns from this script.
    """
    with open(protocol_file_srt) as p:
        protocol = json.load(p)

    extracted_df = pd.DataFrame()

    for dp in protocol['data_points']:
        point_no = dp['point']
        print(f'Point number {point_no} is being extracted.')

        index = point_no-1
        # read what type of condition is set for extracting data points
        cond_type = dp['condition']['name']
        cond_value = dp['condition']['value']
        print(cond_type,cond_value)

        for var in dp['variables']:

            extracted_df.at[index,var['out_name']] = \
                pandas_data[var['name']].loc[pandas_data[cond_type].round(4) == cond_value].to_numpy()

        extracted_df.at[index,'subject_type'] = dp['point_label']

    return extracted_df
