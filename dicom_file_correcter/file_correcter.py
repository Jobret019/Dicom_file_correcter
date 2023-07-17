import utils.Iterative_closest_point as icp 
import numpy as np 
import utils.point_cloud as pc 
from patient_folder import dict_path_folder_of_patient 
import os
import pydicom

def contour_correcter(contour_sequence,contour,x_translation,y_translation,z_translation) :
    '''
    This method shift a structure contour in any direction 

    :param contour_sequence : The contour sequence in which the contour position data are located 
    :param contour : the number link to the contour  
    :param x_translation : the value of the x component of the translation
    :param y_translation : the value of the y component of the translation
    :param z_translation : the value of the z component of the translation  

    :return : the contour shifted by the translation  
    '''
    contour_data=contour_sequence[contour].ContourData
    corrected_contour_data=[]
    x_contour_data=contour_data[0::3]
    y_contour_data=contour_data[1::3]
    z_contour_data=contour_data[2::3]
    for i in range(len(x_contour_data)) :
        x_contour_data[i]+=x_translation
    for i in range(len(y_contour_data)) :
        y_contour_data[i]+=y_translation
    for i in range(len(z_contour_data)) :
        z_contour_data[i]+=z_translation
    for i in range(len(x_contour_data)) :
        corrected_contour_data+=[x_contour_data[i],]
        corrected_contour_data += [y_contour_data[i], ]
        corrected_contour_data += [z_contour_data[i], ]
    return corrected_contour_data

def RTSTRUCT_file_correcter(path_to_structure,x_translation,y_translation,z_translation,title) :
    '''
    This method create a corrected RTSTRUCT file from an RTSTRUCT file with incorrect contour 
    position data  

    :param path_to_structure : the path of the RTSTRUCT Dicom file  
    :param x_translation : the value of the x component of the translation
    :param y_translation : the value of the y component of the translation
    :param z_translation : the value of the z component of the translation  
    :param title : The title of the corrected RTSTRUCT file

    :return : None 
    '''
    open_structure=pydicom.dcmread(path_to_structure)
    contours_sequence=open_structure.ROIContourSequence
    for structure in range(len(contours_sequence)) :
        contour_sequence=contours_sequence[structure].ContourSequence
        for contour in range(len(contour_sequence)) :
            corrected_contour_data=contour_correcter(contour_sequence,contour,x_translation,y_translation,z_translation)
            ((open_structure.ROIContourSequence)[structure].ContourSequence)[contour].ContourData=corrected_contour_data
    open_structure.save_as(title)


