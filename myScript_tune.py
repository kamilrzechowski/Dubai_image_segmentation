# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:41:21 2019

@author: krzec
"""

from svmutil import *
from grid import *
import ntpath
from shutil import copyfile
import os

#dir_dataset = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/'
#dir_file_tunning = 'C:/Kamil/VCC-TN/2 semester/Rocognition Systems/libsvm/2/tuning.txt'

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def compute_params(dataset_path, file_name):
    dir_script = os.path.dirname(os.path.realpath(__file__))
    #copy file to script directory (otherwise find_parameters is not working)
    print(os.path.join(dir_script,file_name))
    copyfile(dataset_path, os.path.join(dir_script,file_name))  
    
    rate, param = find_parameters(file_name, '-log2c -5,11,1 -log2g 3,-15,-2 -v 5 -out null')
    
    print('rate = ' + str(rate) + ' param = ' + str(param))
    
    #copy all file back
    original_file_path = os.path.join(dir_script,file_name)
    try:
        os.remove(original_file_path)
    except:
        print("Error while deleting file ", dir_script,file_name)
    #copyfile(os.path.join(dir_script,file_name + '.png'), os.path.join(dir_current_dataset,file_name + '.png'))
    
    return rate, param['c'], param['g']


'''
procedure tune c and gamma parameters and save them to txt file.
if parameters are already in txt file, procedures get parameters from there
    dir_dataset - path to the input file 'training.scaled'
    dir_file_tunning - path to output txt file to save params (or read if allready there)
'''
def tune_params(dir_dataset,dir_file_tunning):
    c = 0
    g = 0
    content = ''
    try:
        with open(dir_file_tunning) as f:
            content = f.readlines()
    except:
        print('No such file ' + dir_file_tunning)
    file = path_leaf(dir_dataset)
    if file[9:] == 'training.scaled':
        str_incontent = False
        index = -1
        for elem in content:
            index += 1
            if file[:8] in elem:
                str_incontent = True
                break;
        if not str_incontent:
            rate, c, g = compute_params(dir_dataset ,file)
            try:
                f = open(dir_file_tunning,'a')
                f.write(file[:8] + ' rate= ' + str(rate) + ' c= ' + str(c) + ' g= ' + str(g) + '\n')
            except:
                print('Cannot open file ' + dir_file_tunning)
            finally:
                f.close()
        else:
            line = content[index].split(' ')
            prev_elem = ''
            for elem in line:
                if prev_elem == 'c=':
                    c = float(elem)
                if prev_elem == 'g=':
                    g = float(elem)
                prev_elem=elem
    return c, g


# procedure tune c and gamma parameters and save them to txt file.
# if parameters are already in txt file, procedures get parameters from there
def tune_params2(dir_dataset,dir_file_tunning):
    c = 0
    g = 0
    content = ''
    try:
        with open(dir_file_tunning) as f:
            content = f.readlines()
    except:
        print('No such file ' + dir_file_tunning)
    for root, dirs, files in os.walk(dir_dataset):
        for file in files:
            if file[9:] == 'training.scaled':
                str_incontent = False
                index = -1
                for elem in content:
                    index += 1
                    if file[:8] in elem:
                        str_incontent = True
                        break;
                if not str_incontent:
                    rate, c, g = compute_params(os.path.join(root, file),file, root)
                    try:
                        f = open(dir_file_tunning,'a')
                        f.write(file[:8] + ' rate= ' + str(rate) + ' c= ' + str(c) + ' g= ' + str(g) + '\n')
                    except:
                        print('Cannot open file ' + dir_file_tunning)
                    finally:
                        f.close()
                else:
                    line = content[index].split(' ')
                    prev_elem = ''
                    for elem in line:
                        if prev_elem == 'c=':
                            c = float(elem)
                        if prev_elem == 'g=':
                            g = float(elem)
                        prev_elem=elem
    return c, g



