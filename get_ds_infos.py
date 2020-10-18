import os
import sys
import argparse

cwd = os.getcwd()
dest_file = None
dest_path = None
class_dict = {}

def arg_parser():
    global dest_file, dest_path, out_f_name, out_f_path
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-src', help="Directory where from to read the txts.", dest="dest_file", type=str, required=True)
    
    results = parser.parse_args()
    dest_file = results.dest_file.split("/")[0]
    dest_path = os.path.join(cwd, dest_file)
    print(dest_file)
    print(dest_path)
    return results


def add_to_dict(class_id):
    
    if class_id not in class_dict.keys():
        class_dict[class_id] = 0
    else:
        class_dict[class_id] += 1    
    

def read_data():
    # print(dest_path)
    # print(dest_file)
    for txt in os.listdir(dest_path):
        #print(txt)
        if txt.endswith(".txt"):
            txt_path = os.path.join(dest_path, txt)
            f_open = open(txt_path, "r")
            
            line =  f_open.readline().split("\n")[0].split()
            # print(line)
            
            if line != '[]':
                class_id = int(line[0])
                # print(class_id)
                add_to_dict(class_id)
                
                while line:
                    line =  f_open.readline().split("\n")[0].split()
                    if line != []:
                        class_id = int(line[0])
                        add_to_dict(class_id)
            
def write_class_infos():
    out_f_name = str(dest_file) +".ds_infos" 
    out_f_path = os.path.join(cwd, out_f_name)
    
    out_f = open(out_f_path,"w")
    #sort = {k: v for k, v in sorted(class_dict.items(), key=lambda item: item[1], reverse=True)}
    
    sort = dict(sorted(class_dict.items()))
    print(sort)
    for i, v in sort.items():
        out_f.write(str(i) + " " + str(v) + "\n")
    out_f.close() 

if __name__ == "__main__":
    arg_parser() 
    read_data()
    write_class_infos()
