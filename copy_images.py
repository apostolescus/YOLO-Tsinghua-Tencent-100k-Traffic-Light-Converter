import os
import json
import sys
import argparse
from collections import Counter
from PIL import Image as img 
from shutil import copy

cwd = os.getcwd()
img_dir = None
dest_dir_path = None

def arg_parser():

    parser = argparse.ArgumentParser(description='''This scipt extract specific images from the dataset.
                                            It will extract the images that have their name in the directory gave as paramter.
                                            You can specific the own path to the image pool. By default, 
                                            it will copy all images to a new folder formated as foolows: source_folder+ "Images".
                                            If you give as parameter multiple directory, you can save all images in a new made directory.
                                           ''')
    parser.add_argument('-f', help="Folder paths relatively to current directory", dest="folder_path", nargs='+', required=True)
    parser.add_argument('-src', help='''Default images directory is: TL_train_data/home/lyf/develop/data/StreetViewCrops/. 
                        You can specify another using this -src new_path''',dest="personal_path", type=str,
                        default='TL_train_data/home/lyf/develop/data/StreetViewCrops/', required=False)
    parser.add_argument('-x', help="Copies all images in one directory instead of separate ones", dest="one_destination", type=int, default=2)
    
    results = parser.parse_args()
    
    return results

def parse_directory(folder_name):
    
    dest_dir_cpy = dest_dir_path
    if dest_dir_cpy is None:
        dest_dir_cpy = folder_name + " Images"
        dest_dir_cpy_path = os.path.join(cwd, dest_dir_cpy)
        dest_dir_cpy = dest_dir_cpy_path
        try:
            os.mkdir(os.path.join(cwd,dest_dir_cpy))
        except:
            print("Folder already exists")

    ann_source = os.path.join(cwd, folder_name)
    
    for annotation in os.listdir(ann_source):
        img_name = annotation.split(".")[0]+ "." + annotation.split(".")[1] +".jpg"
        img_path = os.path.join(img_dir,img_name)
        copy(img_path, dest_dir_cpy)
        copy(os.path.join(ann_source, annotation), dest_dir_cpy)
        
 
def main():
    global img_dir, dest_dir_path
    
    result = arg_parser()
    one_destination = result.one_destination
   
    if one_destination == 1:
        try:
            dest_dir = "TL_Selected_Images"
            dest_dir_path = os.path.join(cwd, dest_dir)
            os.mkdir(dest_dir)
        except:
            print("Directory already exist")
            
    img_dir = result.personal_path
    
    for folder in result.folder_path:
        parse_directory(folder)
        
        
if __name__ == "__main__":
    # execute only if run as a script
    main()