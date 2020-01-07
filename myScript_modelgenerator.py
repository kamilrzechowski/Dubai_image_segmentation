# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 00:13:31 2019

@author: krzec
"""

from svmutil import *
import os
import subprocess

#dir_input_files = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/'
dir_svmtrin_exe = 'C:\\libsvm-3.23\\windows\\'


'''
procedure takes path to the training_scaled input and generates *.model file in the same directory
	path_training_scaled - directory to the file training_scaled
	c - C parameter for training
	g - Gamma parameter for training
as output procedure generates model, that can be use to classification
'''
def generate_model(path_training_scaled, c, g):
    if not os.path.exists(path_training_scaled + '.model'):
        origin = path_training_scaled.replace('/','\\')
        subprocess.call('start /b /wait /d "' + dir_svmtrin_exe + '" svm-train -s 0 -c ' + str(c) + ' -t 2 -g ' + str(g) + ' -e 0.1 "' + origin + '"', shell=True)
        print('start /b /wait /d "' + dir_svmtrin_exe + '" svm-train -s 0 -c ' + str(c) + ' -t 2 -g ' + str(g) + ' -e 0.1 "' + origin + '"\n')
    
    return