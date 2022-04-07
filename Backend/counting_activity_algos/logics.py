import cv2
from Backend.camera_credentials.roi import centroid_verifier


class algorithms():
    def draw_roi(self,frame, rois, color_box,person_counter,raw_person_counter,cam_number):
        clean_flag=deep_clean_flag=False

        for roi in rois:
                # creating the centroid
            center = (int((roi[0] + roi[2]) / 2), int((roi[1] + roi[3]) / 2))
            cv2.circle(frame, center, 3, (0, 0, 255), 2)
            
            raw_person_counter = raw_person_counter+1    # Count persons(including Red-ROI)
            if centroid_verifier(center,cam_number):
                    person_counter=person_counter+1
            
            if roi[4] == 2:  
                cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), color_box, thickness=2)
                bbox_message = 'Not cleaning'
                cv2.putText(frame, bbox_message, (roi[0] +30 , roi[1] - 2), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 255), 2, lineType=cv2.LINE_AA)	
            elif roi[4] == 0:  
                cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), color_box, thickness=2)
                bbox_message ='Cleaning'
                clean_flag=True
                cv2.putText(frame, bbox_message, (roi[0] +30 , roi[1] - 2), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 255), 2, lineType=cv2.LINE_AA)	
            elif roi[4] == 1:  
                cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), color_box, thickness=2)
                bbox_message ='Deep Cleaning'
                deep_clean_flag=True
                cv2.putText(frame, bbox_message, (roi[0] +30 , roi[1] - 2), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 255), 2, lineType=cv2.LINE_AA)	 
            
        return frame,person_counter,clean_flag,deep_clean_flag
