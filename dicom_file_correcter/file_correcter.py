import utils.Iterative_closest_point as icp 
import numpy as np 
import utils.point_cloud as pc 
from patient_folder import empty_copy
import os
import pydicom
import shutil

def patient_correcter(path_to_patient,x_translation,y_translation,z_translation) : 
    ###PAS FINI
    series=os.listdir(path_to_patient) 
    for serie in range(len(series)) : 
        if serie==0 : 
            path_series0=os.path.join(path_to_patient,series[serie])
            series0_folder_correcter(path_series0)

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

def delete_DVH(path_to_RTDOSE) : 
    '''
    This method create a RTDOSE Dicom file without DVH data from a RTDOSE 
    file with DVH data

    :param path_to_series_1 : the path of the RTDOSE Dicom file

    return : None 
    '''
    open_dose=pydicom.dcmread(path_to_RTDOSE) 
    del open_dose.DVHNormalizationValue 
    del open_dose.DVHNormalization 
    del open_dose.DVHSequence 
    open_dose.save_as('RTDOSE.dcm')

def series0_folder_correcter(path_to_series0,path_to_new_series0_folder,x_translation,y_translation,z_translation) : 
    '''
    This method create a new series0 folder containing all the CT images file with shifted image 
    position from another series0 folder 

    :param path_to_series0: the path of the series0 of the Dicom file
    :param path_to_new_series0_folder : the path of the folder where all the CT file will go 
    :param x_translation : the value of the x component of the translation
    :param y_translation : the value of the y component of the translation
    :param z_translation : the value of the z component of the translation  

    :return : None
    '''
    images_files=os.listdir(path_to_series0)
    for image in range(len(images_files)) : 
        complete_path=os.path.join(path_to_series0,images_files[image])
        title='New'+images_files[image]
        new_path=os.path.join(path_to_series0,title)
        CT_image_file_correcter(complete_path,x_translation,y_translation,z_translation,title)
        shutil.move(new_path,path_to_new_series0_folder) 



def CT_image_file_correcter(path_to_CT_file,x_translation,y_translation,z_translation,title) : 
    '''
    This method create a CT image file with a shifted image position from an another CT image file 

    :param path_to_CT_file: the path of the CT Dicom file 
    :param x_translation : the value of the x component of the translation
    :param y_translation : the value of the y component of the translation
    :param z_translation : the value of the z component of the translation 
    :param title : the title of the new CT Dicom file 

    :return : None
    '''
    open_image=pydicom.dcmread(path_to_CT_file) 
    open_image.ImagePositionPatient[0]+=x_translation
    open_image.ImagePositionPatient[1]+=y_translation
    open_image.ImagePositionPatient[2]+=z_translation
    open_image.save_as(title)
    

def contour_correcter(contour_sequence,contour,x_translation,y_translation,z_translation) :
    '''
    This method shift a structure contour in any direction and inverse the z coordinate 

    :param contour_sequence : The contour sequence in which the contour position data are located 
    :param contour : the number link to the contour  
    :param x_translation : the value of the x component of the translation
    :param y_translation : the value of the y component of the translation
    :param z_translation : the value of the z component of the translation  

    :return : the contour array shifted by the translation  
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
        z_contour_data[i]=-z_contour_data[i]
        z_contour_data[i]+=z_translation
    for i in range(len(x_contour_data)) :
        corrected_contour_data+=[x_contour_data[i],]
        corrected_contour_data += [y_contour_data[i], ]
        corrected_contour_data += [z_contour_data[i], ]
    return corrected_contour_data

