# SVM for image segmentation  
## Segmentation of satelite image of Dubai 2000-2019 using SVM
Following repository conatins python scripts for Dubai satelite image segmentation using SVM. The images were taken from Landsat7 satelite
(https://landsat.gsfc.nasa.gov/landsat-7/). For SVM implementation the LIBSVM was used (https://www.csie.ntu.edu.tw/~cjlin/libsvm/).  

Landsat7 bands:  

|  Bands  | Wavelength [μm] |
| ------------- | ------------- |
| Band 1  | 0.45-0.52  |
| Band 2  |  0.52-0.60  |
| Band 3  | 0.63-0.69  |
| Band 4  |  0.77-0.90  |
| Band 5  | 1.55-1.75 |
| Band 6  |  2.09-2.35  |  

Features scaling was done in ranege <-1;1>. Cross validation was used for C and gamma parameters tuning. As the kernel radial-bases 
function was chosen.
  
The main file is myScript_classify.py.
