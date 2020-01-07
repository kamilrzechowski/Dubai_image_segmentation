# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 13:35:19 2019

@author: krzec
"""
from svmutil import *
import cv2
import os
import subprocess
import numpy as np


#dir_images2classify = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/image set/Landsat/Landsat7/rt_fixed/'
#dir_saving_input = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/'
#dir_mask_training_urban = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/masks/mask_ROI_city_testing.png'
#dir_mask_training_else = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/masks/mask_ROI_else_testing.png'

def calculate_file_input(path2save_inputfile, directory_img, dir_mask_training_urban):
    img_mask_city = cv2.imread(dir_mask_training_urban)
    height, width, n_channels = img_mask_city.shape
    
    im1 = cv2.imread(directory_img[0], cv2.IMREAD_GRAYSCALE)
    im2 = cv2.imread(directory_img[1], cv2.IMREAD_GRAYSCALE)
    im3 = cv2.imread(directory_img[2], cv2.IMREAD_GRAYSCALE)
    im4 = cv2.imread(directory_img[3], cv2.IMREAD_GRAYSCALE)
    im5 = cv2.imread(directory_img[4], cv2.IMREAD_GRAYSCALE)
    im6 = cv2.imread(directory_img[5], cv2.IMREAD_GRAYSCALE)

    f_input = open(path2save_inputfile, "a")
    for j in range(0, height):
        for i in range(0, width):
            f_input.write('3' + ' 1:' + str(im1[j,i]) + ' 2:' + str(im2[j,i]) + ' 3:' + str(im3[j,i]) + ' 4:' + str(im4[j,i]) + ' 5:' + str(im5[j,i]) + ' 6:' + str(im6[j,i]) + '\n')
    f_input.close()
    
    return

def calculate_file_training(path2save_trainingfile, directory_img, dir_mask_training_urban,dir_mask_training_else):
    img_mask_city = cv2.imread(dir_mask_training_urban,cv2.IMREAD_GRAYSCALE)
    img_mask_else = cv2.imread(dir_mask_training_else,cv2.IMREAD_GRAYSCALE)
    height, width = img_mask_city.shape
    
    im1 = cv2.imread(directory_img[0], cv2.IMREAD_GRAYSCALE)
    im2 = cv2.imread(directory_img[1], cv2.IMREAD_GRAYSCALE)
    im3 = cv2.imread(directory_img[2], cv2.IMREAD_GRAYSCALE)
    im4 = cv2.imread(directory_img[3], cv2.IMREAD_GRAYSCALE)
    im5 = cv2.imread(directory_img[4], cv2.IMREAD_GRAYSCALE)
    im6 = cv2.imread(directory_img[5], cv2.IMREAD_GRAYSCALE)
    
    img = np.zeros((height,width,3), np.uint8)

    f_training = open(path2save_trainingfile, "a")
    for j in range(0, height):
        for i in range(0, width):
            img[j,i] = [im1[j,i],im2[j,i],im3[j,i]]
            if img_mask_city[j,i] == 0:
                f_training.write('0' + ' 1:' + str(im1[j,i]) + ' 2:' + str(im2[j,i]) + ' 3:' + str(im3[j,i]) + ' 4:' + str(im4[j,i]) + ' 5:' + str(im5[j,i]) + ' 6:' + str(im6[j,i]) + '\n')
                img[j,i] = [255,0,0]
            if img_mask_else[j,i] == 0:
                f_training.write('1' + ' 1:' + str(im1[j,i]) + ' 2:' + str(im2[j,i]) + ' 3:' + str(im3[j,i]) + ' 4:' + str(im4[j,i]) + ' 5:' + str(im5[j,i]) + ' 6:' + str(im6[j,i]) + '\n')
                img[j,i] = [0,255,0]
    f_training.close()
    
    cv2.imwrite('C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/4/tst.png',img)
    
    return
            
'''
procedure takes TIF images from specified folder, try to group in set of 6 bands and extarct features (unedr ROI - mask)
	dir_images2classify - directory of images to classify
	dir_saving_input - directory to save generated files
	dir_mask_training_urban - mask for training urban areas
	dir_mask_training_else - mask for training 'else' areas
	
all generated files (input file, input_scaled file, taining file, training_scaled file) are saved to directory specified abouve
'''
def convert_TIF2LIBSVM_inputfile(dir_images2classify,dir_saving_input,dir_mask_training_urban,dir_mask_training_else):
    directory_img = [None] * 6
    prev_file = ''
    error = 0
    counter = 0 #counter to check if we found 6 images of one image

    for root, dirs, files in os.walk(dir_images2classify):
        for file in files:
            if file.endswith(".TIF"):
                origin = os.path.join(root, file)
                if error == 0:  #n error we proced normaly
                    if counter == 0:
                        print('Starting new set. ' + origin)
                        directory_img[counter] = origin
                    if counter > 0 and counter < 6:
                        if prev_file[:len(prev_file) - 6] == file[:len(file) - 6]:
                            directory_img[counter] = origin
                            #print(origin)
                        else:
                            print('Error. File: ' + file + ' is not from the set of files ' + prev_file)
                            error = 1
                    if counter == 5 and error == 0:
                        saving_LIBSVM_input_file = dir_saving_input + file[len(file) - 30:len(file) - 22]
                        if not os.path.exists(saving_LIBSVM_input_file):
                            os.makedirs(saving_LIBSVM_input_file)
                        saving_LIBSVM_training_file = saving_LIBSVM_input_file + '/' + file[len(file) - 30:len(file) - 22] +  '_training'
                        sving_range_file = saving_LIBSVM_input_file + '/range'
                        saving_LIBSVM_input_file = saving_LIBSVM_input_file + '/' + file[len(file) - 30:len(file) - 22] +  '_input'
                        #do classification
                        if not os.path.isfile(saving_LIBSVM_input_file):
                            print('Generating input ' + saving_LIBSVM_input_file)
                            calculate_file_input(saving_LIBSVM_input_file,directory_img, dir_mask_training_urban)
                        if not os.path.isfile(saving_LIBSVM_training_file):
                            print('Generating training file ' + saving_LIBSVM_training_file)
                            calculate_file_training(saving_LIBSVM_training_file,directory_img, dir_mask_training_urban, dir_mask_training_else)
                        saving_scaled_training = saving_LIBSVM_training_file + '.scaled'
                        saving_scaled_input = saving_LIBSVM_input_file + '.scaled'
                        sving_range_file = sving_range_file.replace("/","\\")
                        if not os.path.isfile(saving_scaled_training):
                            saving_scaled_training = saving_scaled_training.replace('/','\\')
                            saving_LIBSVM_training_file = saving_LIBSVM_training_file.replace("/","\\")
                            print('start /b /wait /d "C:\libsvm-3.23\windows\" svm-scale -l -1 -u 1 -s "' + sving_range_file + '" "' + saving_LIBSVM_training_file + '" > "' + saving_scaled_training + '"')
                            subprocess.call('start /b /wait /d "C:\libsvm-3.23\windows\" svm-scale -l -1 -u 1 -s "' + sving_range_file + '" "' + saving_LIBSVM_training_file + '" > "' + saving_scaled_training + '"', shell=True)
                        if not os.path.isfile(saving_scaled_input):
                            saving_scaled_input = saving_scaled_input.replace('/','\\')
                            saving_LIBSVM_input_file = saving_LIBSVM_input_file.replace("/","\\")
                            print('start /b /wait /d "C:\libsvm-3.23\windows\" svm-scale -r "' + sving_range_file + '" "' + saving_LIBSVM_input_file + '" > "' + saving_scaled_input + '"')
                            subprocess.call('start /b /wait /d "C:\libsvm-3.23\windows\" svm-scale -r "' + sving_range_file + '" "' + saving_LIBSVM_input_file + '" > "' + saving_scaled_input + '"',shell=True)
                    prev_file = file
                    counter += 1
                    if counter > 5:
                        counter = 0
                else:
                    #skip error files and try to start classifing next set
                    if file[len(file)-6:len(file)-4] == 'B7':
                        counter == 0
                        error = 0

                        
                        
                        
                        
                        
                        