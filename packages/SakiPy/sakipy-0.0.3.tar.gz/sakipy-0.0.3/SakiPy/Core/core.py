import math
import pandas as pd
import re

import chardet

def singleton(cls):
    '''
    实现单例效果
    :param cls:
    :return:
    '''
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

class Switch:
    def __init__(self):
        self.cases = {}
        self.noknow_cases = {}

    def register(self, option, function):
        """
        注册方法与执行函数
        :param option: 方法名
        :param function: 函数
        :return:
        """
        self.cases[option] = function

    def execute(self, option, *args, **kwargs):
        """
        根据名称调用注册的方法
        :param option:方法名
        :param args:函数的参数
        :param kwargs:函数的参数
        :return:
        """
        selected_function = self.cases.get(option, self.default_case)
        return selected_function(*args, **kwargs)

    def default_case(self, *args, **kwargs):
        self.noknow_cases[len(self.noknow_cases)] = args
        return False

def is_nan(s):
    '''
    判断字符串是否为nan类型
    '''
    try:
        if isinstance(s, str):
            if s == "":
                return True
            elif s == "nan":
                return True
            else:
                return False
        elif s is None:
            return True
        elif math.isnan(float(s)):
            return True
        else:
            return False
    except:
        print(s)

def get_encoding(file):
    '''
    介绍：进制方式读取，获取字节数据，检测编码类型【支出：CSV,TXT】
    Functtion Name: get_encoding 【获取文件编码类型】
    parameter ：
        file：str = None 文件地址
    return ：str 【编码类型】
    explain：
        使用前提：加载chardet库
    '''
    with open(file, 'rb') as f:
        file_encoding=chardet.detect(f.read())['encoding']
        f.close()
        return file_encoding
    pass

class ErrorDeal:
    @staticmethod
    def findIllegalCharacters(data:pd.DataFrame):
        '''
        发现数据中的非法字符
        Parma：
            data:pd.DataFrame()
        return:
            [(,,)]
        '''
        illegal_characters = []
        for index, row in data.iterrows():
            for key, column in row.items():
                if isinstance(column, str) and re.search(r'[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD]',
                                                         column):
                    illegal_characters.append((index, key, column))
        return illegal_characters

    @staticmethod
    def dealIllegalCharacters(data:pd.DataFrame, illegal_characters):
        '''
        发现数据中的非法字符
        Parma：
            data:pd.DataFrame()
            illegal_characters:find_illegal_characters()
        return:
            pd.DataFrame()
        '''
        for i in illegal_characters:
            s = re.search(r'[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD]', i[2])
            data.loc[i[0], i[1]] = i[2].replace(s.group(), "")
        return data

def listRemove(gangMembers_nameList, cut=None, is_duplicate=True, **kwar):
    if (type(gangMembers_nameList) == str) & (cut is None):
        gangMembers_nameList = gangMembers_nameList.splitlines()
    elif (type(gangMembers_nameList) == str) & (cut is not None):
        gangMembers_nameList = gangMembers_nameList.split(cut)
    new_list = []
    for x in gangMembers_nameList:
        if is_duplicate:
            if x not in new_list:
                x = x.strip()
                if x != "":
                    new_list.append(x)
        else:
            x = x.strip()
            if x != "":
                new_list.append(x)
    return new_list


import pandas as pd
from xlsxwriter import Workbook
from tqdm import tqdm  # 进度条


def save_large_dataframe(df, filename, rows_per_sheet=1_000_000, chunk_size=100_000):
    """
    高效保存大数据DataFrame到Excel

    参数：
    df : pd.DataFrame - 要保存的DataFrame
    filename : str - 输出文件名（推荐.xlsb格式）
    rows_per_sheet : int - 每个Sheet最大行数（默认100万）
    chunk_size : int - 每次处理的数据块大小（默认10万）
    """
    # 预处理优化
    df = df.reset_index(drop=True)  # 移除无用索引
    df = df.apply(lambda x: x.astype('string') if x.dtype == 'object' else x)  # 统一文本类型

    total_rows = len(df)
    num_chunks = (total_rows + chunk_size - 1) // chunk_size

    with Workbook(filename, {
        'constant_memory': True,  # 启用流式写入
        'strings_to_numbers': True,  # 禁用自动类型检测
        'default_date_format': 'yyyy-mm-dd'  # 日期格式预定义
    }) as workbook:
        sheet_num = 1
        current_row = 0
        worksheet = None

        # 使用tqdm创建进度条
        with tqdm(total=total_rows, desc="导出进度") as pbar:
            for chunk_idx in range(num_chunks):
                # 分块提取数据
                start = chunk_idx * chunk_size
                end = min((chunk_idx + 1) * chunk_size, total_rows)
                chunk = df.iloc[start:end]

                # 计算当前Sheet剩余容量
                if worksheet is None or current_row + len(chunk) > rows_per_sheet:
                    if worksheet is not None:
                        current_row = 0
                    sheet_name = f"Data_{sheet_num}"
                    worksheet = workbook.add_worksheet(sheet_name)
                    # 写入列头
                    worksheet.write_row(0, 0, df.columns.tolist())
                    sheet_num += 1
                    current_row = 1  # 从第2行开始写数据

                # 批量写入数据（优化核心）
                for row_idx, (_, row) in enumerate(chunk.iterrows(), start=current_row):
                    worksheet.write_row(row_idx, 0, row.tolist())

                current_row += len(chunk)
                pbar.update(len(chunk))

