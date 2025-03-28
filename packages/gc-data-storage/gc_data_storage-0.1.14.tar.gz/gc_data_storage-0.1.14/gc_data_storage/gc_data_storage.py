"""
Author: Aymone Jeanne Kouame
Date Released: 03/26/2025
Last Updated: 03/26/2025

"""

import pandas as pd
import os
import subprocess
from IPython.display import Image
import pkg_resources

class gc_data_storage:
    
    def __init__(self, bucket = os.getenv('WORKSPACE_BUCKET')):
        
        self.bucket = bucket
        
    def install_if_not_installed(modules):  
        uninstalled_packages = [p for p in modules if p not in sorted(["%s==%s" % (i.key, i.version) for i in pkg_resources.working_set])]
        uninstalled_packages_f = " ".join(uninstalled_packages)
        res = subprocess.run(['pip', 'install', '--upgrade', uninstalled_packages_f], capture_output=True)

        install_if_not_installed(modules = ['pyarrow', 'openpyxl'])
    
    def save_data_to_bucket(self
                            , data, filename, to_directory = 'data/shared'
                            , index:bool = True
                            , dpi = 'figure'):
        
        bucket = self.bucket
        print(f"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Saving data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    To location =  '{bucket}/{to_directory}'
        """)

        full_filename = f'{bucket}/{to_directory}/{filename}'    
        file_ext = '.'+filename.split('.')[1].lower()

        fun_dd = {'.csv': pd.DataFrame.to_csv , '.xlsx': pd.DataFrame.to_excel, '.parquet': pd.DataFrame.to_parquet}

        df_extensions = ['.csv', '.xlsx', '.tsv', '.parquet']
        plot_extensions = ['.png', '.jpeg', '.bmp', '.tiff', '.pdf', '.emf']

        if file_ext in df_extensions:
            if file_ext == '.tsv': pd.DataFrame.to_csv(data, full_filename, sep="\t")
            else: fun_dd[file_ext](data, full_filename, index = index)
            print(f"Dataframe saved as '{filename}' in location.")
     
        elif file_ext in plot_extensions:   
            data.savefig(filename, dpi = dpi)   
            result = subprocess.run(["gsutil", "cp", filename, full_filename], capture_output=True, text=True)
            print(result.stderr, result.stdout)
  
        else:
            print(f"""
    Your file extension is NOT in {df_extensions+plot_extensions}
    We assume it is already saved to the persistent disk.\n""")
            result = subprocess.run(["gsutil", "cp", filename, full_filename], capture_output=True, text=True)
            print(result.stderr, result.stdout)


    def read_data_from_bucket(self, filename, from_directory = 'data/shared', keep_copy_in_pd:bool = True):
        bucket = self.bucket
        print(f"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Reading data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    From location =  '{bucket}/{from_directory}'
        """)

        full_filename = f'{bucket}/{from_directory}/{filename}'    
        file_ext = '.'+filename.split('.')[1].lower()

        df_extensions = ['.csv', '.xlsx', '.tsv', '.parquet']
        plot_extensions = ['.png', '.jpeg', '.bmp', '.tiff', '.pdf', '.emf']

        fun_dd = {'.csv': pd.read_csv, '.xlsx': pd.read_excel, '.parquet': pd.read_parquet}

        if file_ext in df_extensions:
            if file_ext == '.tsv': data = pd.read_csv(full_filename, sep="\t", engine = 'pyarrow')
            else: data = fun_dd[file_ext](full_filename, engine = 'pyarrow')
      
        elif file_ext in plot_extensions:   
            result = subprocess.run(["gsutil", "cp", full_filename, filename], capture_output=True, text=True)      
            #print(result.stderr, result.stdout)       
            data = Image(filename)
            subprocess.run(["rm", filename], capture_output=True, text=True).stdout.strip("\n")
                
        elif file_ext not in df_extensions+plot_extensions:
            result = subprocess.run(["gsutil", "cp", full_filename, filename], capture_output=True, text=True)
            data = '' 
            if result.returncode == 0: print(f'''
    Your file extension is NOT in {df_extensions+plot_extensions}
    It will just be copied to the persistent disk.''')

        if keep_copy_in_pd == True:
            result = subprocess.run(["gsutil", "cp", full_filename, filename], capture_output=True, text=True)
            if result.returncode == 0: print(f"'{filename}' is in the persistent disk.")               

        return data

    def copy_from_bucket_to_bucket(origin_filename, origin_bucket_directory, destination_bucket_directory
                                   , destination_filename = None):
        
        if destination_filename == None: destination_filename = origin_filename
        origin_fullfilename = f"{origin_bucket_directory}/{origin_filename}"
        dest_fullfilename = f"{destination_bucket_directory}/{destination_filename}"

        print(f"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ copying data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    From {origin_fullfilename}
    To {dest_fullfilename}
        """)

        subprocess.run(["gsutil", "cp", origin_fullfilename, dest_fullfilename])


    def list_saved_data(self, in_bucket:bool = True, in_directory = '', pattern = '*'):
        
        bucket = self.bucket
            
        print(f"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Listing data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """)

        if (in_bucket == True) & (in_directory.strip() == ''):                                         
            subprocess.run(["gsutil", "ls", f"{bucket}/{pattern}"])
        elif (in_bucket == True) & (in_directory.strip() != ''): 
            subprocess.run(["gsutil", "ls", f"{bucket}/{in_directory}/{pattern}"])
        elif in_bucket == False:
            os.system(f'ls {in_directory}{pattern}')
