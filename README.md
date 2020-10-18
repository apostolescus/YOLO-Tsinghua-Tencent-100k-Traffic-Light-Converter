# Tencent Traffic Light YOLO Dataset Parser
Dataset: https://cg.cs.tsinghua.edu.cn/traffic-light/
This scripts help the user understand, convert to YOLO format and extract useful information from this dataset.

# Scripts:
* ***get_ds_infos_JSON*** : Counts each class apparition from "TL_train.json". Useful for understanding the dataset.

* ***get_image_by_class*** : Extracts a number of images of a specific class from the images directory. 
Useful for understanding what each class represents.

	**arguments:** 
		1. class_id : id of the selected class 
		2. number_of_pictures: number of photos samples

* ***convert_to_yolo*** : Generates  YOLO formatted annotations for the specified class. You should specify the number of annotations you want to extract. **Keep in mind** that there are cases when exists more than one class. In this case you can chose to select only the class you like ( discard the others), or save the image with all classes. 

	This can be challenging when you try to have a balanced dataset. Example: ./convert_to_yolo -c 1 -n 1000 

	*Will have the following output: 
	[(1, 1000), (2, 723), (3, 574), (4, 198), (5, 309), (6, 417)]
	This translates as: 
	1000 samples of the 1 class
	723 samples of the 2 class
	574 samples of the 3 class
	...*

	In order to solve this problem you can add "-x 1". This will make the selection more selective. 
	Example: ./convert_to_yolo -c 1 -n 1000  -x 1
	
	*Will have the following output: 
	[(1, 1000), (2, 70), (3, 242), (4, 22), (5, 20), (6, 65)]*
	
	**arguments:**
	1. -c : selected class id
	2. -n : number of samples
	3. -x : extra priority in selecting the class; use "-x 1" to activate
	4. -exclude : specify the classes you want to exclude. The converted images will not contain any of these classes. 
	Parse them the following way: -exclude 1,2,3 ( will exclude 1, 2, 3 classes)
	ex: ./convert_to_yolo.py -c 1 -n 1000 -x 1 -exclude 4,5,6
	Converts 1000 annotations from class 1 and removes all the annotations from the 4,5,6 classes. 
	
* ***get_ds_infos*** : Counts the classes from the converted dataset and prints the information.
		
	**arguments:**
	1.  -src : directory where from to read the files

* ***copy_images*** : Reads annotations from one file and copies the corresponding images with annotations to a one directory.  You can parse multiple directory and copy the images and annotations in one folder.

	**arguments:**
	1.  -src : directory from which the files are read; 
	Default is "TL_train_data/home/lyf/develop/data/StreetViewCrops/"
	2. -f : folder paths relative to the current directory
	3. -x : Copies all images in one directory instead of separate ones


# How to use the scripts

 1. get_ds_infos_JSON : generates dataset_infos; check the data and see what you have there
 2. get_image_by_class : extract some images and see what each class id represent
 3. convert_to_yolo : convert some classes from json to txt
 4. get_ds_infos : check what you have extracted and make sure your set is equally distributed
 5. copy_images : final step, copy the images and annotations in one directory 
 6. TRAIN THEM!

