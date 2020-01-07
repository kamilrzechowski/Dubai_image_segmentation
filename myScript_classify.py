# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 22:48:58 2019

@author: krzec
"""

from shutil import copyfile
import os
from myScript_inputgenerator import*
from myScript_modelgenerator import*
from myScript_tune import*
from myScript_prediction import*
from myScript_evaluate import*

#paths
dir_dataset = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/4/'
dir_images2classify = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/image set/Landsat/Landsat7/rt_fixed/'
dir_mask_training_urban = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/4/masks/mask_ROI_city_training.png'
dir_mask_training_else = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/4/masks/mask_ROI_else_training.png'
dir_file_tunning = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/4/tuning.txt'
dir_mask_test_city = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/4/masks/mask_ROI_city_testing.png'
dir_mask_test_else = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/4/masks/mask_ROI_else_testing.png'
dir_accuracy_txt = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/4/accuracy.txt'

#main classification procedure.
#it follows all steps - input generating, scaling, model generating, training, predicting and accuracy computing.
def classify():
    convert_TIF2LIBSVM_inputfile(dir_images2classify,dir_dataset,dir_mask_training_urban,dir_mask_training_else)
    
    for root, dirs, files in os.walk(dir_dataset):
            for file in files:
                if file[9:] == 'training.scaled':
                    if file == '20010522_training.scaled':
                        origin = os.path.join(root,file)
                        c, g = tune_params(origin,dir_file_tunning)
                        generate_model(origin,c,g);
                        dir_model = origin + '.model'
                        dir_classification_input = os.path.join(root,file[:9] + 'input.scaled')
                        dir_classification_output = os.path.join(root,file[:8] + '_out')
                        if os.path.exists(dir_model) and os.path.exists(dir_classification_input):
                            predict(dir_model, dir_classification_output, os.path.join(root,file[:8] + '_out.png'), dir_classification_input)
                        else:
                            print(dir_model + ' or ' + dir_classification_input + ' does not exist')
                        if os.path.exists(dir_classification_output):
                            evaluate(dir_mask_test_city, dir_mask_test_else, dir_classification_output, file[:8], dir_accuracy_txt)
                        else:
                            print('Cant do evaluation. File doesnt exist: ' + dir_classification_output)
    return

def move_png(dir_destination):
    for root, dirs, files in os.walk(dir_dataset):
        for file in files:
            if file[9:] == 'out.png':
                try:
                    copyfile(os.path.join(root,file), os.path.join(dir_destination, file))
                except:
                    print('Cannot copy file: ' + os.path.join(root,file))
    return

#move_png('C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/3/results/')
classify()
                    
                    


                
                
                