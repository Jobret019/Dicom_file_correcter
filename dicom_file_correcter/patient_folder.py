import os 
import utils.Iterative_closest_point as icp
import numpy as np 
import utils.point_cloud as pc 

def flip_image_point_cloud(image_cloud) : 
    '''
    This method flip an image point cloud relative to the z axis 
    
    :param image_cloud : the image cloud to flip 

    :return : an image point cloud with the z inverse
    '''
    inversion_matrix=np.array([[1,0,0],[0,1,0],[0,0,-1]])
    inverse_image_cloud=np.dot(inversion_matrix,image_cloud ) 
    return inverse_image_cloud 

def icp_translation(path_series0,path_RTPLAN,inverse=None) : 
    '''
    This method find the optimal translation to register two point cloud together 
    using the ICP algorithm  

    :param path_series0 : the path of series0 of the patient 
    :param path_RTPALN : The path of the RTPLAN file of the patient
    :param inverse : if inverse is True, the method will first inverse the image point 
    cloud in the z axis

    :return : the translation to register the 2 point cloud 

    '''
    image_cloud=pc.image_point_cloud(path_series0) 
    source_cloud=pc.source_point_cloud(path_RTPLAN)
    if inverse==True : 
        image_cloud=flip_image_point_cloud(image_cloud)
    transformation=icp.IterativeClosestPoint(image_cloud,source_cloud) 
    translation = transformation[1]    
    return translation

def patients_folder_translation(path_to_patients_folder,inverse=None) : 
    '''
    This method takes a folder of patient and create a dictionnary that associate 
    a patient with the translation that is necessary to register his 2 point cloud

    :param path_to_patients_folder : the path of the folder containing all the patients 
    that need a correction 

    :param inverse : if inverse is True, the method will first inverse the image point 
    cloud in the z axis of all the patient 

    :return : a dictionnary with all the patient as keys and the translation needed as 
    values
    '''
    patients=os.listdir(path_to_patients_folder)
    dict_patient_translation={} 
    dict_paths_of_folder=dict_path_folder_of_patient(path_to_patients_folder) 
    
    for i in range(len(dict_paths_of_folder['list_path_series0'])) : 
        path_series0=dict_paths_of_folder['list_path_series0'][i] 
        path_RTPLAN=dict_paths_of_folder['list_path_RTPLAN'][i] 
        translation=icp_translation(path_series0,path_RTPLAN)
        dict_patient_translation[patients[i]]=translation 
    
    return dict_patient_translation

def dict_path_folder_of_patient(path_to_patients_folder) : 
    '''
    This method takes a folder with many patient and put , in a dictionnary, all the series0 and
    the RTPLAN file of patients. Note that we have to have all the CT files in the series0 and the RT 
    plan in the series2.

    :param path_to_patient_folder : The complete path of the folder containing all the patient

    :return : a dictionnary with a key for the path of the series0 of all the patient and a key for the 
    path of the RTPLAN of all the patient. 
    '''

    dict_path = {} 
    dict_path['list_path_series0']=[]
    dict_path['list_path_RTPLAN']=[]
    patients=os.listdir(path_to_patients_folder) 
    for patient in range(len(patients)) : 
        path_patient=os.path.join(path_to_patients_folder,patients[patient])
        path_study=os.path.join(path_patient,'study0')
        path_series0=os.path.join(path_study,'series0')
        path_series2=os.path.join(path_study,'series2')
        path_RTPLAN=os.path.join(path_series2,'RTPLAN0.dcm')
        dict_path['list_path_series0']+=[path_series0,]
        dict_path['list_path_RTPLAN']+=[path_RTPLAN,]
    
    return dict_path



