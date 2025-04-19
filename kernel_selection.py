import os
import pydicom
import pandas as pd
import numpy as np
from itables import init_notebook_mode
init_notebook_mode(all_interactive=True)
import csv
import matplotlib.pyplot as plt 
from pydicom.multival import MultiValue
import dicom2nifti
import nibabel as nib


hrct_kernels = [
    MultiValue(str, ['I70f', '2']), 
    'BONEPLUS',   
    'BONE',
    'B45f',
    'LUNG',
    'B70f',
    'B60f',
    'B45s',
    'Br54s',
    'B70s',
    MultiValue(str, ['Br54d', '2']),
    'FC56',
    'FC52',
    'B80s',
    'B60s',
    'FC86',
    'YB',
    'YD',
    MultiValue(str, ['Br58f', '2']),
    'Br58f',
    'B80f',
    'YC',
    'FC55',
    MultiValue(str, ['I70f', '1']),
]


#%%

df_filtered = pd.read_pickle('/home/users/ager/midrc_project/data/df_metadata_filtered_all_0_1.pkl')

hrct_matching_indices = df_filtered[df_filtered['kernel'].isin(hrct_kernels)].index
hrct_non_matching_indices = df_filtered[~df_filtered['kernel'].isin(hrct_kernels)].index

#%%
df_filtered['sharp_series'] = 0
df_filtered['non_sharp_series'] = 0
df_filtered.loc[hrct_matching_indices,'sharp_series'] = 1
df_filtered.loc[hrct_non_matching_indices,'non_sharp_series'] = 1

#%%

df_groupby_kernels = df_filtered.groupby('_imaging_study_id')[['sharp_series', 'non_sharp_series']].max()
df_groupby_kernels['kernel_group'] = df_groupby_kernels.apply(lambda row: 
    'group_sharp' if row['sharp_series'] and not row['non_sharp_series'] else
    'group_non_sharp' if row['non_sharp_series'] and not row['sharp_series'] else
    'group_both', axis=1)

df_groupby_kernels = df_groupby_kernels[['kernel_group']]

#%%

df_filtered = df_filtered.merge(df_groupby_kernels,on='_imaging_study_id',how='left').set_index(df_filtered.index)

#%%

df_filtered['sharp_selected'] = 0
df_filtered['non_sharp_selected'] = 0

#%%

for i in df_filtered['_imaging_study_id']:
   df_temp = df_filtered.loc[df_filtered['_imaging_study_id'] == i]
   count_sharp = (df_temp['sharp_series'] == 1).sum()
   count_non_sharp = (df_temp['non_sharp_series'] == 1).sum()

   if count_sharp == 1:
      temp_index = df_temp.loc[df_temp['sharp_series'] == 1].index[0]
      df_filtered.loc[temp_index, 'sharp_selected'] = 1

   elif count_sharp >= 2:
      df_temp_temp = df_temp.loc[df_temp['sharp_series'] == 1] 
      df_temp_temp['slice_thickness'] = pd.to_numeric(df_temp_temp['slice_thickness'])
      min_index = df_temp_temp['slice_thickness'].idxmin() 
      df_filtered.loc[min_index, 'sharp_selected'] = 1

   if count_non_sharp == 1:
      temp_index = df_temp.loc[df_temp['non_sharp_series'] == 1].index[0]
      df_filtered.loc[temp_index, 'non_sharp_selected'] = 1

   elif count_non_sharp >= 2:
      df_temp_temp = df_temp.loc[df_temp['non_sharp_series'] == 1] 
      df_temp_temp['slice_thickness'] = pd.to_numeric(df_temp_temp['slice_thickness'])
      min_index = df_temp_temp['slice_thickness'].idxmin() 
      df_filtered.loc[min_index, 'non_sharp_selected'] = 1

#%%

df_filtered['selected_nifti'] = (df_filtered['sharp_selected'] | df_filtered['non_sharp_selected'])

df_filtered.to_pickle(os.path.join('/home/users/ager/midrc_project/data','df_filtered_selected_series.pkl'))

