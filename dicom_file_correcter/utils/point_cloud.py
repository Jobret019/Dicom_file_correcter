from position_patient_coordinate import pixel_position_in_patient_coordinate,source_position_in_patient_coordinate
import pydicom 
import numpy as np
import os 
from dicompylercore import dicomparser


def image_point_cloud(path_to_serie) : 
    '''
    This method create an array of 3 array (x,y,z position) with all the position of the pixels with the 
    highest radiodensity value which correspond to source position in an image 
    
    :param path_to_serie : complete path of the serie containing all the CT files

    :return : an array with array of x, y and z coordinates in patient
    '''    
    max=0
    index_x=0
    index_y=0
    Position_x=0
    Position_y=0
    Position_z=0
    points_coordinate=[]
    list_x_position=np.array([])
    list_y_position=np.array([])
    list_z_position=np.array([])

    paths = os.listdir(path_to_serie)
    pixel_positions_x,pixel_positions_y,_=pixel_position_in_patient_coordinate(os.path.join(path_to_serie,paths[0]))

    for i in range(len(paths)) : 
        complete_path=os.path.join(path_to_serie,paths[i])
        data=image_hu_data(complete_path)
        if max<=np.max(data) :
            max=np.amax(data) 

    for i in range(len(paths)) : 
        complete_path=os.path.join(path_to_serie,paths[i])
        open_dicom=pydicom.dcmread(complete_path)
        data=image_hu_data(complete_path)
        maximum_HU_pixels_indexs=np.where(data==max)
        Position_z=open_dicom.ImagePositionPatient[2]
        for j in range(len(maximum_HU_pixels_indexs[0])) : 
            index_x=maximum_HU_pixels_indexs[1][j]
            index_y=maximum_HU_pixels_indexs[0][j]
            Position_x=pixel_positions_x[index_x]
            Position_y=pixel_positions_y[index_y]
            list_x_position=np.append(list_x_position,Position_x)
            list_y_position=np.append(list_y_position,Position_y)
            list_z_position=np.append(list_z_position,Position_z)

    points_coordinate=np.array([list_x_position,list_y_position,list_z_position])     

    return points_coordinate


def source_point_cloud(path_to_plan) : 
    '''
    This method create an array of 3 array (x,y,z position) with all the position of the sources given by the 
    RTPLAN file.  
    
    :param path_to_plan : complete path of the RTPLAN file

    :return : an array with array of x, y and z coordinates in patient
    '''    
    list_source_position=[]
    open_plan=pydicom.dcmread(path_to_plan)
    aplication_setups=open_plan.ApplicationSetupSequence

    for i in range(len(aplication_setups)) :
        source_position= source_position_in_patient_coordinate(path_to_plan,i) 
        if source_position==None : 
            list_source_position+=[]       
        elif len(source_position)==2 :
            list_source_position+=[np.array(source_position[0]),]
            list_source_position+=[np.array(source_position[1]),]
        else : 
            list_source_position+=[np.array(source_position),]
    list_source_position= np.array(list_source_position)  
    
    new_list_source_position=[] 
    Position_x=np.array([])
    Position_y=np.array([])
    Position_z=np.array([])
    for i in range(len(list_source_position)) : 
        Position_x=np.append(Position_x,list_source_position[i][0])
        Position_y=np.append(Position_y,list_source_position[i][1])
        Position_z=np.append(Position_z,list_source_position[i][2])
    new_list_source_position+=[np.array(Position_x),]
    new_list_source_position+=[np.array(Position_y),]
    new_list_source_position+=[np.array(Position_z),]
    source_coordinates=np.array(new_list_source_position)
    
    return source_coordinates

def image_hu_data(path_to_image_file) : 
    '''
    This method create a 2D array with all the value of radiodensity in HU associated with every pixel 
    of an image 
    
    :param path_to_image_file : complete path of an CT image file

    :return : a 2d array of radiodensity value
    '''
    open_dicom=pydicom.dcmread(path_to_image_file)

    rescale_slop=open_dicom.RescaleSlope
    rescale_intercept=open_dicom.RescaleIntercept
    
    pixel_data=open_dicom.pixel_array 

    data=pixel_data*rescale_slop+rescale_intercept
    return data