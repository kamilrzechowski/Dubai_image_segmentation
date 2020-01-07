# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 02:54:43 2019

@author: krzec
"""

from svmutil import *
import cv2
import os
import numpy as np

#dir_data2classify = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/20000519_input.scaled'
#dir_model = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/20000519_training.scaled.model'
#dir_classified_file = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/out'
#dir_out_png = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/out.png'

'''
procedure generates classification output file and classification png
    dir_model - path to pre-trained model (see modelgenerator.py)
    dir_classified_file - output path (with file name) to the classification output file
    dir_out_png - path to output png (with file name)
    dir_data2classify - input data for classificaion (pre-scaled. see input_generator.py)
'''
def predict(dir_model, dir_classified_file, dir_out_png, dir_data2classify):
    if not os.path.exists(dir_classified_file) and not os.path.exists(dir_out_png):
        height = 2468
        width = 2569
        img = np.zeros((height,width,1), np.uint8)
        
        # Read data to classify
        y1, x1 = svm_read_problem(dir_data2classify)
        # read model
        m = svm_load_model(dir_model)
        # predict
        p_labels, p_acc, p_vals = svm_predict([], x1, m)
        
        row = -1
        f = open(dir_classified_file, "a")
        for i in range(len(p_labels)):
            f.write(str(p_labels[i]) + '\n')
            if i % width == 0:
                row += 1
            if p_labels[i] == 1.0:
                    img[row,i - (row*width)] = 255
            else:
                img[row,i - (row*width)] = 0
        #for item in p_labels: 
        #    f.write(str(item) + '\n')
        f.close()
        
        cv2.imwrite(dir_out_png,img)
    
    return
            
            
            
            
            
            