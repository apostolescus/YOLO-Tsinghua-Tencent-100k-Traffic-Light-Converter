import os
import json
import sys
from PIL import Image
import cv2

class_id = sys.argv[1]
counter = int(sys.argv[2])
cwd = os.getcwd()

im_path = os.path.join(cwd, "TL_train_data","home","lyf","develop","data","StreetViewCrops")
folder_path = os.path.join(cwd, class_id)

def read_json():
    ct = 0
    f = open("TL_train.json","r")
    js = json.load(f)
    try:
        os.mkdir(folder_path) 
    except:
        print("file already exists")
        
    for j in js:
        img_name = j["Path"]
        objects = j["Objects"]
        
        if objects != []:
            for obj in objects:
                if str(class_id) == str(obj["Category"]):
                    if ct == counter:
                        return
                    else:
                        ct += 1
                        
                        x_min = int(obj["BBox"][0])
                        y_min = int(obj["BBox"][1])
                        x_max = int(obj["BBox"][2])
                        y_max = int(obj["BBox"][3])
                        print(x_max, x_min, y_min, y_max)
                        img_path = os.path.join(im_path, img_name)
                        
                        image = cv2.imread(img_path)
                        image = cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,255,0),2) # add rectangle to image
                        img_final_pth = os.path.join(folder_path, img_name)
                        cv2.imwrite(img_final_pth,image)
                # if obj["Category"] not in sign_categories.keys():
                #     sign_categories[a] = 1
                # else:
                #     sign_categories[a] += 1 
                
read_json()