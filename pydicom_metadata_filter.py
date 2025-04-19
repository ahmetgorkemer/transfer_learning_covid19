
#%%

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
import shutil
from skimage.util import montage as montage2d

#%%

main_directory = '/scratch/users/ager/midrc_data'
os.chdir(main_directory)  

def dicom_metadata(folder_path):                     #Metadata selection
   
   list_dict = []
   
   study_date = {}
   patient_birth_date = {}
   patient_age = {}
   patient_sex = {}
   patient_position = {}
   study_description = {}
   series_description = {}
   slice_thickness = {}
   image_type = {}
   kernel = {}
   manufacturer = {}
   contrast_type = {}
   kvp = {}
   contrast_volume = {}
   contrast_dose = {}
   tube_current = {}
   exposure_time = {}
   gantry = {}
   recons_dia = {}
   exposure = {}
   xy = {}
   spacing = {}
   dcm_count = {}

   for root, dirs, _ in os.walk(folder_path):
      for subfolder in dirs:
         subfolder_path = os.path.join(root, subfolder)
         files = os.listdir(subfolder_path)
         dcm_files = [file for file in files if file.endswith('.dcm')]
         count = len(dcm_files)
         if len(dcm_files) != 0:
            ds = pydicom.dcmread(os.path.join(subfolder_path,dcm_files[0]))
            try:
               study_date_ = ([subfolder_path], ds[0x00080020].value)
            except KeyError:
               study_date_ = ([subfolder_path], '---')
            study_description_ = ([subfolder_path], ds[0x00081030].value)
            try:
               patient_birth_date_ = ([subfolder_path], ds[0x00100030].value)
            except KeyError:
               patient_birth_date_ =  ([subfolder_path], '---')
            try:
               patient_age_ = ([subfolder_path], ds[0x00101010].value)
            except KeyError:
               patient_age_ = ([subfolder_path], '---')
            try:
               patient_sex_ = ([subfolder_path], ds[0x00100040].value)
            except KeyError:
               patient_sex_ = ([subfolder_path], '---')
            try:
               patient_position_ = ([subfolder_path], ds[0x00185100].value)
            except KeyError:
               patient_position_ = ([subfolder_path], '---')
            try:
               series_description_ = ([subfolder_path], ds[0x0008103E].value)
            except KeyError:
               series_description_ = ([subfolder_path], '---')
            try:
               slice_thickness_ = ([subfolder_path], ds[0x00180050].value)
            except KeyError:
               slice_thickness_ = ([subfolder_path], 100)
            image_type_ = ([subfolder_path], ds[0x00080008].value)
            xy_ = ([subfolder_path], (ds[0x00280010].value, ds[0x00280011].value))
            try:
               manufacturer_ = ([subfolder_path], ds[0x00080070].value)
            except KeyError:
               manufacturer_ = ([subfolder_path], '---')
            try:
               spacing_ = ([subfolder_path], ds[0x00280030].value)
            except KeyError:
               spacing_ = ([subfolder_path], 100)
            try:
               kernel_ = ([subfolder_path], ds[0x00181210].value)
            except KeyError:
               kernel_ = ([subfolder_path], '---')
            try:
               contrast_type_ = ([subfolder_path], ds[0x00180010].value)
            except KeyError:
               contrast_type_ = ([subfolder_path], '---')
            try:
               kvp_ = ([subfolder_path], ds[0x00180060].value)
            except KeyError:
               kvp_ = ([subfolder_path], '---')
            try:
               contrast_volume_ = ([subfolder_path], ds[0x00181041].value)
            except KeyError:
               contrast_volume_ = ([subfolder_path], '---')
            try:
               contrast_dose_ = ([subfolder_path], ds[0x00181044].value)
            except KeyError:
               contrast_dose_ = ([subfolder_path], '---')
            try:
               tube_current_ = ([subfolder_path], ds[0x00181151].value)
            except KeyError:
               tube_current_ = ([subfolder_path], '---')
            try:
               exposure_time_ = ([subfolder_path], ds[0x00181150].value)
            except KeyError:
               exposure_time_ = ([subfolder_path], '---')
            try:
               gantry_ = ([subfolder_path], ds[0x00181121].value)
            except KeyError:
               gantry_ = ([subfolder_path], '---')
            try:
               recons_dia_ = ([subfolder_path], ds[0x00181122].value)
            except KeyError:
               recons_dia_ = ([subfolder_path], '---')
            try:
               exposure_modulation_type_ = ([subfolder_path], ds[0x00189323].value)
            except KeyError:
               exposure_modulation_type_ = ([subfolder_path], '---')
            try:
               exposure_ = ([subfolder_path], ds[0x00181152].value)
            except KeyError:
               exposure_ = ([subfolder_path], '---')
            dcm_count_ = ([subfolder_path], count)
            
            study_date[subfolder_path] = study_date_
            patient_sex[subfolder_path] = patient_sex_
            patient_age[subfolder_path] = patient_age_
            patient_birth_date[subfolder_path] = patient_birth_date_
            patient_position[subfolder_path] = patient_position_
            study_description[subfolder_path] = study_description_
            series_description[subfolder_path] = series_description_
            slice_thickness[subfolder_path] = slice_thickness_
            image_type[subfolder_path] = image_type_
            xy[subfolder_path] = xy_
            spacing[subfolder_path] = spacing_
            dcm_count[subfolder_path] = dcm_count_
            kernel[subfolder_path] = kernel_
            manufacturer[subfolder_path] = manufacturer_
            contrast_type[subfolder_path] = contrast_type_
            kvp[subfolder_path] = kvp_
            contrast_volume[subfolder_path] = contrast_volume_
            contrast_dose[subfolder_path] = contrast_dose_
            tube_current[subfolder_path] = tube_current_
            exposure_time[subfolder_path] = exposure_time_
            gantry[subfolder_path] = gantry_
            recons_dia[subfolder_path] = recons_dia_
            exposure[subfolder_path] = exposure_

   list_dict = [study_description, study_date, patient_age, patient_birth_date, patient_position,patient_sex, series_description, slice_thickness, 
                image_type, kernel, manufacturer, contrast_type, kvp, contrast_volume, 
                contrast_dose, tube_current, exposure_time, gantry, recons_dia, exposure, xy, spacing, dcm_count] 

   df = pd.DataFrame(list_dict)
   df = df.T

   df["patient_name"] = np.nan
   df['study_name'] = np.nan

   df = df.rename(columns={0:'study_description',1:'study_date', 2:'patient_age', 3:'patient_birth_date',4:'patient_position',
                          5:'patient_sex', 6:'series_description', 7:'slice_thickness', 8:'image_type', 9: 'kernel', 10: 'manufacturer',
                      11:'contrast_type', 12:'kvp', 13:'contrast_volume', 14:'contrast_dose',
                      15:'tube_current', 16:'exposure_time', 17:'gantry', 18:'recons_dia',
                       19:'exposure', 20:'xy', 21:'spacing', 22:'count'})

   for i, row in df.iterrows():
      df.at[i,'patient_name'] = str(df.at[i,'study_description'][0]).split('/')[1].split('-')[0]
      df.at[i,'study_name'] = str(df.at[i,'study_description'][0]).split('/')[1]
      df.at[i,'study_id'] = str(df.at[i,'study_description'][0]).split('/')[2]
      df.at[i,'study_date'] = df.at[i,'study_date'][1]
      df.at[i,'patient_birth_date'] = df.at[i,'patient_birth_date'][1]
      df.at[i,'patient_age'] = df.at[i,'patient_age'][1]
      df.at[i,'patient_sex'] = df.at[i,'patient_sex'][1]
      df.at[i,'patient_position'] = df.at[i,'patient_position'][1]
      df.at[i,'study_description'] = df.at[i,'study_description'][1]
      df.at[i,'series_description'] = df.at[i,'series_description'][1]
      df.at[i,'slice_thickness'] = df.at[i,'slice_thickness'][1]
      df.at[i,'image_type'] = df.at[i,'image_type'][1]
      df.at[i,'kernel'] = df.at[i,'kernel'][1]
      df.at[i,'contrast_type'] = df.at[i,'contrast_type'][1]
      df.at[i,'kvp'] = df.at[i,'kvp'][1]
      df.at[i,'contrast_volume'] = df.at[i,'contrast_volume'][1]
      df.at[i,'contrast_dose'] = df.at[i,'contrast_dose'][1]
      df.at[i,'tube_current'] = df.at[i,'tube_current'][1]
      df.at[i,'exposure_time'] = df.at[i,'exposure_time'][1]
      df.at[i,'gantry'] = df.at[i,'gantry'][1]
      df.at[i,'recons_dia'] = df.at[i,'recons_dia'][1]
      df.at[i,'exposure'] = df.at[i,'exposure'][1]
      df.at[i,'xy'] = df.at[i,'xy'][1]
      df.at[i,'manufacturer'] = df.at[i,'manufacturer'][1]
      df.at[i,'spacing'] = df.at[i,'spacing'][1]
      df.at[i,'count'] = df.at[i,'count'][1]

   cols = df.columns.tolist()
   cols = ['patient_name','study_name','study_id',
          'study_date','patient_birth_date','patient_age','patient_sex','patient_position',
          'study_description','series_description','slice_thickness','image_type',
          'kernel', 'contrast_type','kvp','contrast_volume','contrast_dose','tube_current',
         'exposure_time','gantry','recons_dia','exposure','manufacturer','xy',
         'spacing','count']

   df = df[cols]

   df['series_id'] = df.index.to_series().apply(lambda x:x.split('/')[3])

   return df

pos_dicom_paths = ['pos_cases_df_1',
'pos_cases_df_2',
'pos_cases_df_3',
'pos_cases_df_4',
'pos_cases_df_5',
'pos_cases_df_6',
'pos_cases_df_7',
'pos_cases_df_8',
'pos_cases_df_9',
'pos_cases_df_10',
'pos_cases_df_11',
'pos_cases_df_12',
'pos_cases_df_13',
'pos_cases_df_14',
'pos_cases_df_15',
'pos_cases_df_16',
'pos_cases_df_17',
'pos_cases_df_18',
'pos_cases_df_19',
'pos_cases_df_20',
'pos_cases_df_21',
'pos_cases_df_22',
'pos_cases_df_23']

neg_dicom_paths = ['neg_cases_df_1',
'neg_cases_df_2',
'neg_cases_df_3',
'neg_cases_df_4',
'neg_cases_df_5',
'neg_cases_df_6',
'neg_cases_df_7',
'neg_cases_df_8',
'neg_cases_df_9',
'neg_cases_df_10',
'neg_cases_df_11',
'neg_cases_df_12',
'neg_cases_df_13',
'neg_cases_df_14',
'neg_cases_df_15',
'neg_cases_df_16',
'neg_cases_df_17',
'neg_cases_df_18',
'neg_cases_df_19',
'neg_cases_df_20',
'neg_cases_df_21',
'neg_cases_df_22',
'neg_cases_df_23',
'neg_cases_df_24']


list_pos_metadata = [dicom_metadata(path) for path in pos_dicom_paths]
list_neg_metadata = [dicom_metadata(path) for path in neg_dicom_paths]

#%%

df_pos_metadata = pd.concat(list_pos_metadata)
df_pos_metadata['class'] = 1
df_neg_metadata = pd.concat(list_neg_metadata)
df_neg_metadata['class'] = 0

df_metadata = pd.concat([df_pos_metadata,df_neg_metadata])

#%%

df_metadata.to_pickle('/home/users/ager/midrc_project/data/df_metadata_all_0_1.pkl')

#%%


#%%

df_filtered = df_metadata.loc[
         (df_metadata['patient_position'].isin(['FFS', 'HFS'])) & 
         df_metadata['image_type'].apply(lambda x: 'ORIGINAL' in x) &
         (df_metadata['count'] > 30) &
         df_metadata['xy'].apply(lambda x: x == (512, 512)) &
         (~df_metadata['series_description'].str.contains('exp', case=False))
         ]

df_filtered.to_pickle('/home/users/ager/midrc_project/data/df_metadata_filtered_all_0_1.pkl')

#%%

df_filtered = pd.read_pickle('/home/users/ager/midrc_project/data/df_metadata_filtered_all_0_1.pkl')



# %%

filtered_pos = df_filtered[df_filtered['class'] == 1]
filtered_neg = df_filtered[df_filtered['class'] == 0]
# %%
