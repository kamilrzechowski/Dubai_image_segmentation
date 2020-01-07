# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:14:14 2019

@author: krzec
"""

from svmutil import *
import cv2

#dir_mask_test_city = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/masks/mask_ROI_city_testing.png'
#dir_mask_test_else = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/masks/mask_ROI_else_testing.png'
#dir_classification_output = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/20000519/out'
#dir_accuracy_txt = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/accuracy.txt'

# procedure takes png mask of city, png mask of everything else and output file of classification
# procedure returns accurasce, meane square error and someting else 
def evaluate(dir_mask_test_city, dir_mask_test_else, dir_classification_output, title,dir_accuracy_txt):
    img_mask_city = cv2.imread(dir_mask_test_city,cv2.IMREAD_GRAYSCALE)
    img_mask_else = cv2.imread(dir_mask_test_else,cv2.IMREAD_GRAYSCALE)
    height, width = img_mask_city.shape
    ACC = 0.0 
    MSE = 0.0 
    SCC = 0.0
    content = ''
    try:
        with open(dir_accuracy_txt) as f_save:
            content = f_save.readlines()
    except:
        print('No such file ' + dir_accuracy_txt)
    
    str_incontent = False
    index = -1
    for elem in content:
        index += 1
        if title in elem:
            str_incontent = True
            break;
    if not str_incontent:
        tv = []     #list of true values
        pv = []     #list of predicted values
        
        row = -1
        f = open(dir_classification_output,'r')
        for i, line in enumerate(f):
            if i % width == 0:
                row += 1
            if img_mask_city[row,i - (row*width)] == 0:
                    tv.append(0.0)
                    pv.append(float(line))
            elif img_mask_else[row,i - (row*width)] == 0:
                tv.append(1.0)
                pv.append(float(line))
            
        f.close()
        
        
        (ACC, MSE, SCC) = evaluations(tv, pv)
        
        try:
            f_save = open(dir_accuracy_txt,'a')
            f_save.write(title + ' ACC= ' + str(ACC) + ' MSE= ' + str(MSE) + ' SCC= ' + str(SCC) + '\n')
        except:
            print('Cannot open file ' + dir_accuracy_txt)
        finally:
            f_save.close() 
    else:
        line = content[index].split(' ')
        prev_elem = ''
        for elem in line:
            if prev_elem == 'ACC=':
                ACC = float(elem)
            if prev_elem == 'MSE=':
                MSE = float(elem)
            if prev_elem == 'MSE=':
                SCC = float(elem)
            prev_elem=elem
    
    print('ACC = ' + str(ACC) + ' MSE = ' + str(MSE) + ' SCC = ' + str(SCC))
    
    return ACC, MSE, SCC


