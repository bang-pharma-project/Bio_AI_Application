import cv2
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import numpy as np
from pyparsing import empty # Create a VideoCapture object and read from input file
from datetime import date,datetime
from Backend.artificial_intel.detect_box_yolo import detect_box
# from Backend.camera_credentials.roi import centroid_verifier
from Backend.counting_activity_algos.logics import algorithms
import pandas as pd
from Backend.database_functions.Excel_Handler.excel_handler import *
from Backend.video_database import data_manager
from threading import Thread

color_box = (140,101,211)
excel_obj = ExcelHandler()
algos = algorithms()

class Room_M1_Application():
    
    def main_function(self):

        key=0

        if key==0:            # static state
            prev_count_102=prev_count_103=prev_count_104=0           # initial state of all count=0
            clean_flag_prev=deep_clean_flag_prev=False
            run_movavg = True
            frame_counter=0
            dash_102 = dash_103 = dash_104 = 0


        cap_102 = cv2.VideoCapture('rtsp://admin:admin@123@172.19.112.102:554/profile2/media.smp') # Check if camera opened successfully
        cap_103 = cv2.VideoCapture('rtsp://admin:admin@123@172.19.112.103:554/profile2/media.smp') # Check if camera opened successfully
        cap_104 = cv2.VideoCapture('rtsp://admin:admin@123@172.19.112.104:554/profile2/media.smp') # Check if camera opened successfully

        map_image = cv2.imread(r'Backend\images\camera_map_occ.png')
        map_image = cv2.resize(map_image,(224,214))

        if (cap_102.isOpened()== False or cap_103.isOpened()== False or cap_104.isOpened()== False):
            print("Error")

        frame_save_path=data_manager.get_the_saving_folder("m1_saperation_room")
        saving_path = frame_save_path+"//"                     # directory path:  ..//video_database//<YYYY-mm-dd>//<HH>//

        counter=0
        while(cap_102.isOpened()):
            # Capture frame-by-frame
            ret, frame_102 = cap_102.read()
            ret1, frame_103 = cap_103.read()
            ret2, frame_104 = cap_104.read()
            if ret == True:     # Display the resulting frame
        #         cv2.imshow('Frame', frame)     # Press Q on keyboard to exit
                file_name = saving_path+str(datetime.now().strftime("%H_%M_%S_%f"))+".jpg"
                empty_frame = np.zeros([760,1296, 3], dtype=np.uint8)
                empty_frame.fill(255)

                cv2.putText(frame_102, 'Camera:102', (30,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                cv2.putText(frame_103, 'Camera:103', (30,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                cv2.putText(frame_104, 'Camera:104', (30,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                
                # print("before 102:",frame_102.shape)
                cv2.rectangle(frame_102, (1630, 15), (2575, 605), (0,0,255), thickness=2)


                rois = detect_box(frame_102, 0.25)
                frame_102,count_102,clean_flag,deep_clean_flag=algos.draw_roi(frame_102, rois, color_box,0,0,102)
                # print("after 102",frame_102.shape)
        
                rois = detect_box(frame_103, 0.25)
                frame_103,count_103,clean_flag,deep_clean_flag=algos.draw_roi(frame_103, rois, color_box,0,0,103)
                cv2.rectangle(frame_103, (1865, 5), (2590, 1510), (0,0,255), thickness=2)
        
                rois = detect_box(frame_104, 0.25)
                cv2.rectangle(frame_104, (1311, 5), (2585, 570), (0,0,255), thickness=2)
                frame_104,count_104,clean_flag,deep_clean_flag=algos.draw_roi(frame_104, rois, color_box,0,0,104)

                frame_102 = cv2.resize(frame_102,(648,380))
                frame_103 = cv2.resize(frame_103,(648,380))
                frame_104 = cv2.resize(frame_104,(648,380))
                
                empty_frame[0:380,648:1296]=frame_102
                empty_frame[380:760,0:648]= frame_103
                empty_frame[380:760,648:1296]= frame_104
                empty_frame[0:214,424:648] = map_image
                cv2.putText(empty_frame, 'Date :{}'.format(date.today().strftime("%B %d, %Y")), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
                cv2.putText(empty_frame, 'Time :{}'.format(datetime.now().strftime("%H:%M:%S")), (50,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

                cv2.putText(empty_frame, 'Analytics Dashboard', (50,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                cv2.putText(empty_frame, 'Camera 102: {}'.format(dash_102), (80,200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0, 255), 1)
                cv2.putText(empty_frame, 'Camera 103: {}'.format(dash_103), (80,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0, 255), 1)
                cv2.putText(empty_frame, 'Camera 104: {}'.format(dash_104), (80,260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0, 255), 1)
                cv2.putText(empty_frame, 'Overall Occupancy : {}'.format(dash_102+dash_103+dash_104), (70,320), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                
                #print(prev_count_102,count_102,prev_count_103,count_103,prev_count_104,count_104,clean_flag_prev,clean_flag,deep_clean_flag_prev,deep_clean_flag)
                if prev_count_102!=count_102 or prev_count_103!=count_103 or prev_count_104!=count_104 or clean_flag_prev!=clean_flag or deep_clean_flag_prev!=deep_clean_flag:
                    # print("State change Triggered!!!")
                    prev_count_102=count_102
                    prev_count_103=count_103 
                    prev_count_104=count_104 
                    clean_flag_prev=clean_flag 
                    deep_clean_flag_prev=deep_clean_flag
                    run_movavg = True
                    frame_counter = 0
                    # print(prev_count_102,count_102,prev_count_103,count_103,prev_count_104,count_104,clean_flag_prev,clean_flag,deep_clean_flag_prev,deep_clean_flag)
            

                if prev_count_102==count_102 and prev_count_103==count_103 and prev_count_104==count_104 and clean_flag_prev==clean_flag and deep_clean_flag_prev==deep_clean_flag and run_movavg == True:           
                    frame_counter +=1
                    # print("frame_counter:",frame_counter)

                    if frame_counter == 40:#10:
                        print("Data Appended Room M1")
                        frame_counter = 0
                        run_movavg = False
                        dash_102 = count_102
                        dash_103 = count_103
                        dash_104 = count_104

                        analysis_df = excel_obj.get_dataframe('m1',count_102,count_103,count_104,clean_flag,deep_clean_flag)
                        excel_obj.handle_and_write_csv('m1',analysis_df)
                    # frame_count=+1

                #if datetime.now().strftime("%M-%S") in range('00-00',"00-10"): # in range 00min-00sec to 00min-10sec
                if datetime.now().strftime("%M-%S")>='00-00' and datetime.now().strftime("%M-%S")<'00-10': # delay time-delta of 10sec
                    frame_save_path=data_manager.get_the_saving_folder("m1_saperation_room")     # Add new  yy-mm-dd/hourly_sub-dirs
                    saving_path = frame_save_path+"//"                       # directory path:  ..//video_database//<YYYY-mm-dd>//<HH>//
                    # data_manager.delete_previous_directory_m1()               # delete previous sub-dirs
                
                if datetime.now().strftime("%H-%M")>='00-00' and datetime.now().strftime("%H-%M")<'00-10':
                    pass                            # Delete the Previous Day's Data


                #cv2.imshow("frame",empty_frame)
                cv2.imwrite(file_name,empty_frame)
                
                # print("saving images in prog(checkpost-4)!!") 
                prev_count_102=count_102
                prev_count_103=count_103
                prev_count_104=count_104
                key=1
                # counter+=1

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break # Break the loop
            else:
                break # When everything done, release
        # the video capture object
        cap_102.release() # Closes all the frames
        cv2.destroyAllWindows()