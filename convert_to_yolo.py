import os
import json
import sys
import argparse
from collections import Counter
from PIL import Image as img 

final_dict = {}
save_folder = None
class_list = ['1','2','3','4','5','6']

img_path = os.path.join(os.getcwd(),"TL_train_data/home/lyf/develop/data/StreetViewCrops/")

def convert(size, box):
    #converts to yolo format
    
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def arg_parser():

    parser = argparse.ArgumentParser(description='''This scipt converts the annotations from Tencent Dataset json to Yolo format. 
                                            It extracts the annotations for the images from one class (-c:class_id).
                                            You must specify the number of total annotations to extract. 
                                            When a image contains the specific class it's adnotation will be converted and added to the generated directory. 
                                            Keep in mind that if that image contains another class too, that class will be added and converted. 
                                            You can eliminate unwanted classes from beeing converted using "-exclude".
                                            Optionally, you can select an agressive method to extract the classes, where the algorithm will try to select mostly 
                                            images with the main classes. 
                                            The one that have other predominant classes will be excluded.  
                                           ''')
    parser.add_argument('-c', help="class id", dest="class_id", type=int)
    parser.add_argument('-n', help="number of samples", dest="sample_number", type=int)
    parser.add_argument('-x', help="extra priority in extracting the class", dest="priority", type=bool, default=False)
    parser.add_argument('-exclude', help="specify the classes you want to exclude like this: 1,2,3 ", dest="exclude_cls", type=str, default='')
    
    results = parser.parse_args()
    
    if results.exclude_cls != '': 
        for elem in results.exclude_cls.split(","):
            class_list.remove(elem)

    return results

def load_json():
    f= open("TL_train.json","r")
    js = json.load(f)
    
    return js

def add_dict(class_dict):
    
    a = Counter(final_dict) + Counter(class_dict)
    return dict(a)

def check_max_number(max_counter, class_id):
    
    try:
        if final_dict[class_id] >= max_counter:
            return False
        else:
            return True
    except:
        return True
    
def check_dict(class_id, class_dict, priority):
    
    sorted_dict = {k: v for k, v in sorted(class_dict.items(), key=lambda item: item[1])}
    
    try:
        class_number = class_dict[class_id]
    except:
        class_number = 0
        
    if priority is True:
        for key, val in class_dict.items():
            if class_number < val:
                return False
    else:
        for key, val in class_dict.items():
            if class_number + 2 < val:
                return False
    
    return True
            
def write_to_file(coef_list, path):
    
    txt_name = path.split(".")[0] + "." + path.split(".")[1] +".txt"
    out_f = os.path.join(os.getcwd(), save_folder, txt_name)
    out_handler = open(out_f, "w")
    
    for line in coef_list:
        if line == coef_list[-1]:
            out_handler.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + " " + str(line[3]))
        else:
            out_handler.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + " " + str(line[3])+ "\n")
    # if line != coef_list[]:
    #     out_handler.write("\n")
    out_handler.close()
  
def write_statistics():
  
    out_f = open(os.path.join(os.getcwd(),save_folder+"_dsInfos"), "w")
    
    sorted_dict = sorted(final_dict.items())
    print(sorted_dict)
    #sorted_dict = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
    # for key,val in sorted_dict.items():
    for i in sorted_dict:
            out_f.write(str(i[0]) + " " + str(i[1]) + "\n")
        
def parse_json(json_file, params):
    
    for each in json_file:
        class_dict = {}
        path = each["Path"]
        objects = each["Objects"]
        checK_if_exist_one_class = False
        
        final_path = os.path.join(img_path, path)
        image = img.open(final_path)

        width, height = image.size
        size = (float(width), float(height))
        coef_list = []
        
        for obj in objects:
            category = int(obj["Category"])
            if str(category) in class_list:
                checK_if_exist_one_class = True
                out_l = []
                try:
                    class_dict[category] += 1
                except:
                    class_dict[category] = 1
                bbox = obj["BBox"]
                bbx_update = [int(bbox[0]), int(bbox[2]), int(bbox[1]), int(bbox[3])]
                x,y,w,h = convert(size, bbx_update)
                
                out_l.append(category)
                out_l.append(x)
                out_l.append(y)
                out_l.append(w)
                out_l.append(h)
                coef_list.append(out_l)
        if checK_if_exist_one_class is True:
            if check_max_number(params.sample_number, params.class_id) is False:
                return
            if check_dict(params.class_id, class_dict, params.priority) is True:
                global final_dict 
                final_dict = add_dict(class_dict)
                write_to_file(coef_list, path)
                print(final_dict)
 
def main():
    global save_folder
    args = arg_parser()
    jsonFile = load_json()
    
    try:
        save_folder = str(args.class_id) + "_" + str(args.sample_number)
        os.mkdir(str(args.class_id) + "_" + str(args.sample_number))
       
    except:
        print("file already exists")
        
    parse_json(jsonFile, args)
    write_statistics()
    
if __name__ == "__main__":
    # execute only if run as a script
    main()
