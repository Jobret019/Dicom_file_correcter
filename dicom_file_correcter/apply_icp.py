import numpy as np 
import utils.point_cloud as pc 
import utils.Iterative_closest_point as icp

def apply_transformation_on_image_cloud(image_cloud,source_cloud) : 
    '''
    This method shift an image point cloud in the correct position in the case of a point
    cloud inverted relative to the z axis

    :param image_cloud : the image point cloud to be shifted 
    :param source_cloud : the source point cloud that the image_cloud is gonna be register 
    on 

    :return : the corrected image point cloud witgh new point position. 
    '''
    image_cloud=flip_image_point_cloud(image_cloud) 
    translation=icp_translation(image_cloud,source_cloud) 
    I_matrix=np.array([[1,0,0],[0,1,0],[0,0,1]])
    corrected_image_point_cloud=icp.ApplyTransformation(image_cloud,I_matrix,translation) 
    return corrected_image_point_cloud 

def icp_translation(image_cloud,source_cloud) : 
    '''
    This method find the optimal translation to register two point cloud together 
    using the ICP algorithm  

    :param path_series0 : the path of series0 of the patient 
    :param path_RTPALN : The path of the RTPLAN file of the patient
    :param inverse : if inverse is True, the method will first inverse the image point 
    cloud in the z axis

    :return : the translation to register the 2 point cloud 

    '''
    transformation=icp.IterativeClosestPoint(image_cloud,source_cloud) 
    translation = transformation[1]    
    return translation

def flip_image_point_cloud(image_cloud) : 
    '''
    This method flip an image point cloud relative to the z axis 
    
    :param image_cloud : the image cloud to flip 

    :return : an image point cloud with the z inverse
    '''
    inversion_matrix=np.array([[1,0,0],[0,1,0],[0,0,-1]])
    inverse_image_cloud=np.dot(inversion_matrix,image_cloud ) 
    return inverse_image_cloud 