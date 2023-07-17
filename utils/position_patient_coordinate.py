import pydicom 
import numpy as np

def pixel_position_in_patient_coordinate(path_to_image_file) : 
    '''
    This method express the xyz position of the pixels in an image slice in the patient coordinate 
    system (mm).
    
    :param path_to_image_file : complete path of an CT image file

    :return: two arrays of the positions of x and y in mm for all the pixels  and a float for the 
    position in z 
    '''
    open_dicom=pydicom.dcmread(path_to_image_file)
    orientation=open_dicom.ImageOrientationPatient
    position=open_dicom.ImagePositionPatient
    pixel_spacing=open_dicom.PixelSpacing
    colonne=open_dicom.Columns
    rangee=open_dicom.Rows
    
    Xx,Xy,Xz,Yx,Yy,Yz=orientation[0],orientation[1],orientation[2],orientation[3],orientation[4],orientation[5]
    Sx,Sy,Sz=position[0],position[1],position[2]
    deltai,deltaj=pixel_spacing[0],pixel_spacing[1]
    
    M=[[Xx*deltai,Yx*deltaj,0,Sx],[Xy*deltai,Yy*deltaj,0,Sy],[Xz*deltai,Yz*deltaj,0,Sz],[0,0,0,1]] 
    Position=np.empty((colonne,rangee),dtype=object)
    Position_X=np.empty(colonne,dtype=object)
    Position_Y=np.empty(rangee,dtype=object)
    
    for i in range(colonne) : 
        for j in range(rangee) : 
            vecteur = np.array([i,j,0,1]) 
            Position[i][j]=np.dot(M,vecteur)
            Position[i][j]=np.delete(Position[i][j],3)
            Position_Y[j]=Position[0][j][1]
        Position_X[i]=Position[i][0][0]
    
    Position_Z=Position[1][1][2]
    
    return Position_X,Position_Y,Position_Z

def source_position_in_patient_coordinate(path_to_plan,setup_number) :
    '''
    This method extract the position of a source in a RTPLAN dicom files .
    
    :param path_to_plan : complete path of an RTPLAN file
    :param setup_number : the setup number of the source 

    :return: 1 or 2 array of source xyz position in mm 
    '''
    open_plan=pydicom.dcmread(path_to_plan)
    application_setup=open_plan.ApplicationSetupSequence
    
    if hasattr(application_setup[setup_number],'ChannelSequence') : 
        channel_sequence=application_setup[setup_number].ChannelSequence
        Control_point=channel_sequence[0].BrachyControlPointSequence
        if len(Control_point) == 4 : 
            source_position_2=Control_point[2].ControlPoint3DPosition 
        elif len(Control_point) == 2 : 
            source_position_2=None

        source_position_1=Control_point[0].ControlPoint3DPosition 
        
        if source_position_2==None : 
            return source_position_1
        else : 
            return source_position_1,source_position_2 
    
    else : 
        pass
