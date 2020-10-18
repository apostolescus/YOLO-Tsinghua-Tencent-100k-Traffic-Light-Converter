import os
import json

sign_categories = {}

def read_json():
    f = open("TL_train.json","r")
    js = json.load(f)
    
    for j in js:
        objects = j["Objects"]
        
        if objects != []:
            for obj in objects:
                a = obj["Category"]
                print(a)
                if obj["Category"] not in sign_categories.keys():
                    sign_categories[a] = 1
                else:
                    sign_categories[a] += 1


read_json()

sorted_dict = {k: v for k, v in sorted(sign_categories.items(), key=lambda item: item[1], reverse=True)}

out_f = open("dataset_infos","w")
for i,j in sorted_dict.items():
    out_f.write(str(i)+ " " + str(j)+ "\n")

out_f.close()
