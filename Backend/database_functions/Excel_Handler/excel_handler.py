import pandas as pd
from datetime import datetime

class ExcelHandler():
    """ExcelHandler creates connection with the input excel sheet and will fetch data from it, it will also create results.csv with process information
    """

    # def __init__(self, excel_path="Backend\\database_function\\excel_database\\analytics_excel.csv"):
    #     self.input_dataframe = pd.read_csv(excel_path, encoding='utf-8')

    def handle_and_write_csv(self,room, dataframe):
        # if room == 'm1':
        dataframe.to_csv("Backend\\database_functions\\excel_database\\master_analytics.csv", mode='a', header=False,index=False)
        # elif room == 'm2':
        #     dataframe.to_csv("Backend\\database_functions\\excel_database\\M2_Analytics.csv", mode='a', header=False,index=False)


    def get_dataframe(self,room,count_1,count_2,count_3,clean_flag,deep_clean_flag):
        if room == 'm1': 
            analysis_dict = {'date': [datetime.today().strftime('%d-%m-%Y')], 
                         'time': [datetime.now().strftime('%H:%M:%S')],
                         'room': ['M1 Saperation Room'], 
                         'camera1': [count_1],
                         'camera2': [count_2],
                         'camera3': [count_3], 
                         'total_occupancy': [count_1+count_2+count_3],
                         'cleaning':[clean_flag],
                         'Deep Cleaning':[deep_clean_flag]}
        
        elif room == 'm2':
            analysis_dict = {'date': [datetime.today().strftime('%d-%m-%Y')], 
                         'time': [datetime.now().strftime('%H:%M:%S')],
                         'room': ['M2 Purification Room'], 
                         'camera1': [count_1],
                         'camera2': [count_2],
                         'camera3': [None],
                         'total_occupancy': [count_1+count_2],
                         'cleaning':[clean_flag],
                         'Deep Cleaning':[deep_clean_flag]}
                        
        analysis_df = pd.DataFrame(analysis_dict)
        return analysis_df
    