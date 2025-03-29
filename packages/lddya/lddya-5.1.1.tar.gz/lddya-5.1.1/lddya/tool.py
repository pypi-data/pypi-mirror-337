import datetime
import pandas as pd
import numpy as np
import os


class Clock():
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

    def start(self):
        self.start_time = datetime.datetime.now()

    def end(self):
        self.end_time = datetime.datetime.now()
        self.delta_t = self.end_time - self.start_time
    
    def get_delta(self):
        return self.delta_t.seconds+self.delta_t.microseconds*(10**(-6))
    
    def show(self):
        print('The program runs for ',self.delta_t,' microsecond')

class DataOperater():
    def __init__(self):
        pass
    
    def save_to_excel(self, data, filename):
        # 检查data类型，确保其是一个一维或二维的列表或np矩阵
        if isinstance(data, (list, np.ndarray)):
            # 将数据转换为numpy数组，以确保统一处理
            data = np.array(data)
            
            # 如果数据是一维列表或数组，转换为二维（单列）
            if data.ndim == 1:
                data = data.reshape(1, -1)
                
             # 确保目录存在，不存在则创建
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # 使用pandas将数据转换为DataFrame
            df = pd.DataFrame(data)
            
            # 保存为Excel文件
            df.to_excel(filename, index=False, header=False)
            print(f"Data has been saved to {filename}")
        else:
            raise TypeError("Input data must be a list or numpy array!")
        
    def read_excel(self, filename,row_index=None,column_index=None):
        try:
            # 使用pandas读取Excel文件
            df = pd.read_excel(filename,index_col=row_index, header=column_index)  # header=None表示不把第一行当作列名
            # 将DataFrame转换为numpy数组
            data = df.to_numpy()
            return data
        except FileNotFoundError:
            print(f"Error: The file {filename} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")