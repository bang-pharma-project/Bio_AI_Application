import cv2
roi_cam102=[(1830, 15), (2575, 605)]
roi_cam103=[(1865, 5), (2590, 1510)]
roi_cam104=[(1510, 5), (2585, 570)]
roi_cam_78_1=[(447,2),(1200,1060)]
roi_cam_78_2=[(447,1060),(2200,1520)]
#roi_cam79 = [(1033, 9), (2581, 1031)]



def centroid_verifier(centroid,cam_num):
    if cam_num==102:
        if centroid[0]> roi_cam102[0][0] and centroid[0] < roi_cam102[1][0] and centroid[1]> roi_cam102[0][1] and centroid[1] < roi_cam102[1][1]:
            return False
        else:
            return True


    elif cam_num==103:
        if centroid[0]> roi_cam103[0][0] and centroid[0] < roi_cam103[1][0] and centroid[1]> roi_cam103[0][1] and centroid[1] < roi_cam103[1][1]:
            return False
        else:
            return True

    elif cam_num==104:
        if centroid[0]> roi_cam104[0][0] and centroid[0] < roi_cam104[1][0] and centroid[1]> roi_cam104[0][1] and centroid[1] < roi_cam104[1][1]:
            return False
        else:
            return True

    elif cam_num==78:  ## cam-78 1st ROI
        if centroid[0]> roi_cam_78_1[0][0] and centroid[0] < roi_cam_78_1[1][0] and centroid[1]> roi_cam_78_1[0][1] and centroid[1] < roi_cam_78_1[1][1]:
            return False
        else:
            if centroid[0]> roi_cam_78_2[0][0] and centroid[0] < roi_cam_78_2[1][0] and centroid[1]> roi_cam_78_2[0][1] and centroid[1] < roi_cam_78_2[1][1]:
                return False
            else:
                return True

    else:
        return True
