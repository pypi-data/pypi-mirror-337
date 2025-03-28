"""
处理时间格式相关的函数
"""
import re
import pandas as pd
import numpy as np

from SakiPy.Core.core import is_nan

class DealDateAndTime:
    def __init__(self, df, columns=["交易日期", "交易时间"], type=["date", "time"]):
        '''
        parm:
            type:三种类型
                date:
                time:
                date+time
        '''
        self.df = df[columns].copy()
        if len(columns) >= 2:
            self.isMaege = True
        else:
            self.isMaege = False

        # 返回数据
        self.return_df = df[columns].copy()

        for x, y in zip(columns, type):
            self.return_df[x] = self.dealClassify(x, y)

    def dealClassify(self, x, y):
        deal_func_dict = {
            "date": self.dealDate(x),
            "time": self.dealTime(x),
            "date+time": self.dealDateTime(x),
        }
        return deal_func_dict.get(y, "")

    def dealDate_map(self, datetimes_df):

        if re.match(r'^(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})$', str(datetimes_df)):
            s = re.match(r'^(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})$', str(datetimes_df))
            if len(s.groups()) == 3:
                str_year = s.groups()[0]  # 年
                str_month = s.groups()[1]  # 月
                str_month = self.fillZero(str_month, 2)
                str_day = s.groups()[2]  # 日
                str_day = self.fillZero(str_day, 2)
                return str_year + "-" + str_month + "-" + str_day
        elif re.match(r'^(\d{8}?)$', str(datetimes_df)):  # 仅含有8个数字的字符串【日期】
            str_year = datetimes_df[0:4]  # 年
            str_month = datetimes_df[4:6]  # 月
            str_day = datetimes_df[6:8]  # 日
            return str_year + "-" + str_month + "-" + str_day
        elif re.match(r'^(\d{4})[年](\d{1,2})[月](\d{1,2})[日]$', str(datetimes_df)):
            s = re.match(r'^(\d{4})[年](\d{1,2})[月](\d{1,2})[日]$', str(datetimes_df))
            if len(s.groups()) == 3:
                str_year = s.groups()[0]  # 年
                str_month = s.groups()[1]  # 月
                str_month = self.fillZero(str_month, 2)
                str_day = s.groups()[2]  # 日
                str_day = self.fillZero(str_day, 2)
                return str_year + "-" + str_month + "-" + str_day
        else:
            return self.dealDateTime_map(datetimes_df)
        pass

    def dealDate(self, x):
        df = self.df.copy()
        df[x] = df[x].map(self.dealDate_map)

        return df[[x]]

    def defTime_init(self, x):
        ## 纯数字与非纯数字
        try:
            df_digit = self.df[self.df[x].str.isdigit()].copy()
            df_digit_no = self.df[~self.df[x].str.isdigit()].copy()
            # 获取df_digit的最长度
            df_digit_max = df_digit[x].str.len().max()
            # 把纯数字处理为同一逻辑
            df_digit[[x]] = df_digit[[x]].map(lambda x: self.fillZero(x, df_digit_max))
            df = pd.concat([df_digit, df_digit_no])
            return df[[x]]
        except:
            return self.df[[x]].copy()

    def dealTime_map(self, datetimes_df):
        # 处理时间格式的函数
        if re.match(r'^(\d{6,8}?)$', str(datetimes_df)):  # 仅含有8个数字的字符串【时间】
            str_hour = datetimes_df[0:2]  # 时
            str_minute = datetimes_df[2:4]  # 分
            str_second = datetimes_df[4:6]  # 秒
            str_second = self.dealSecond(str_second)
            str_df = str_hour + ":" + str_minute + ":" + str_second
            if str_df == "24:00:00":
                return "23:59:59"
            else:
                return str_df
        elif re.match(r'^(\d{1,2})[.|:](\d{1,2})[.|:](\d{1,2})$', str(datetimes_df)):
            # 时间格式通过.或：进行切割
            s = re.match(r'^(\d{1,2})[.|:](\d{1,2})[.|:](\d{1,2})$', str(datetimes_df))
            if len(s.groups()) == 3:
                str_hour = str(s.groups()[0])  # 时
                str_hour = self.fillZero(str_hour, 2)
                str_minute = str(s.groups()[1])  # 分
                str_minute = self.fillZero(str_minute, 2)
                str_second = str(s.groups()[2])  # 秒
                str_second = self.fillZero(str_second, 2)
                str_second = self.dealSecond(str_second)
                str_df = str_hour + ":" + str_minute + ":" + str_second
                if str_df == "24:00:00":
                    return "23:59:59"
                else:
                    return str_df
        elif is_nan(datetimes_df):
            # 时间为空时处理方法
            return "00:00:00"
        else:
            # 日期格式与时间格式合并的情况
            return self.dealDateTime_map(datetimes_df)

    def dealTime(self, x):
        df = self.defTime_init(x)
        df[x] = df[x].replace("'", "", regex=True)

        df[x] = df[x].map(self.dealTime_map)
        return df[[x]]

    def dealDateTime_map(self, datetimes_df):
        # 处理日期加时间格式
        if re.match(r'^(\d{4})[/|-](\d{1,2})[/|-](\d{2}) (\d{1,2})[:|.](\d{1,2})[:|.](\d{1,2})$', str(datetimes_df)):
            str_year = str(datetimes_df[0:4])  # 年
            str_month = str(datetimes_df[5:7])  # 月
            str_day = str(datetimes_df[8:10])  # 日
            str_hour = str(datetimes_df[11:13])  # 时
            str_minute = str(datetimes_df[14:16])  # 分
            str_second = str(datetimes_df[17:19])  # 秒
            str_second = self.dealSecond(str_second)
            if str_year == "0000":
                return str_hour + ":" + str_minute + ":" + str_second
            else:
                return str_year + "-" + str_month + "-" + str_day + " " + str_hour + ":" + str_minute + ":" + str_second
        elif re.match(r'^(\d{14,17}?)$', str(datetimes_df)):  # 仅含有8个数字的字符串【日期】
            str_year = datetimes_df[0:4]  # 年
            str_month = datetimes_df[4:6]  # 月
            str_day = datetimes_df[6:8]  # 日
            str_hour = str(datetimes_df[8:10])  # 时
            str_minute = str(datetimes_df[10:12])  # 分
            str_second = str(datetimes_df[12:14])  # 秒
            str_second = self.dealSecond(str_second)
            if str_year == "0000":
                return str_hour + ":" + str_minute + ":" + str_second
            else:
                return str_year + "-" + str_month + "-" + str_day + " " + str_hour + ":" + str_minute + ":" + str_second
        elif re.match(r'^(\d{4})[/|-](\d{1,2})[/|-](\d{2})(\d{1,2})[:|.](\d{1,2})[:|.](\d{1,2})$', str(datetimes_df)):
            s = re.match(r'^(\d{4})[/|-](\d{1,2})[/|-](\d{2})(\d{1,2})[:|.](\d{1,2})[:|.](\d{1,2})$', str(datetimes_df))
            if len(s.groups()) == 6:
                str_year = s.groups()[0]  # 年
                str_month = s.groups()[1]  # 月
                str_month = self.fillZero(str_month, 2)
                str_day = s.groups()[2]  # 日
                str_day = self.fillZero(str_day, 2)
                str_hour = s.groups()[3]  # 时
                str_hour = self.fillZero(str_hour, 2)
                str_minute = s.groups()[4]  # 分
                str_minute = self.fillZero(str_minute, 2)
                str_second = s.groups()[5]  # 秒
                str_second = self.fillZero(str_second, 2)
                str_second = self.dealSecond(str_second)
                if str_year == "0000":
                    return str_hour + ":" + str_minute + ":" + str_second
                else:
                    return str_year + "-" + str_month + "-" + str_day + " " + str_hour + ":" + str_minute + ":" + str_second
        elif re.match(r'^(\d{4})[/|-](\d{1,2})[/|-](\d{2}) (\d{1,2})(\d{1,2})(\d{1,2})$', str(datetimes_df)):
            s = re.match(r'^(\d{4})[/|-](\d{1,2})[/|-](\d{2}) (\d{1,2})(\d{1,2})(\d{1,2})$', str(datetimes_df))
            if len(s.groups()) == 6:
                str_year = s.groups()[0]  # 年
                str_month = s.groups()[1]  # 月
                str_month = self.fillZero(str_month, 2)
                str_day = s.groups()[2]  # 日
                str_day = self.fillZero(str_day, 2)
                str_hour = s.groups()[3]  # 时
                str_hour = self.fillZero(str_hour, 2)
                str_minute = s.groups()[4]  # 分
                str_minute = self.fillZero(str_minute, 2)
                str_second = s.groups()[5]  # 秒
                str_second = self.fillZero(str_second, 2)
                str_second = self.dealSecond(str_second)
                if str_year == "0000":
                    return str_hour + ":" + str_minute + ":" + str_second
                else:
                    return str_year + "-" + str_month + "-" + str_day + " " + str_hour + ":" + str_minute + ":" + str_second
        elif re.match(r'^(\d{4})[/|-](\d{1,2})[/|-](\d{2})(\d{1,2})(\d{1,2})(\d{1,2})$', str(datetimes_df)):
            s = re.match(r'^(\d{4})[/|-](\d{1,2})[/|-](\d{2})(\d{1,2})(\d{1,2})(\d{1,2})$', str(datetimes_df))
            if len(s.groups()) == 6:
                str_year = s.groups()[0]  # 年
                str_month = s.groups()[1]  # 月
                str_month = self.fillZero(str_month, 2)
                str_day = s.groups()[2]  # 日
                str_day = self.fillZero(str_day, 2)
                str_hour = s.groups()[3]  # 时
                str_hour = self.fillZero(str_hour, 2)
                str_minute = s.groups()[4]  # 分
                str_minute = self.fillZero(str_minute, 2)
                str_second = s.groups()[5]  # 秒
                str_second = self.fillZero(str_second, 2)
                str_second = self.dealSecond(str_second)
                if str_year == "0000":
                    return str_hour + ":" + str_minute + ":" + str_second
                else:
                    return str_year + "-" + str_month + "-" + str_day + " " + str_hour + ":" + str_minute + ":" + str_second
        elif re.match(r'^(\d{8}?)$', str(datetimes_df)):  # 仅含有8个数字的字符串【日期】
            str_year = datetimes_df[0:4]  # 年
            str_month = datetimes_df[4:6]  # 月
            str_day = datetimes_df[6:8]  # 日
            return str_year + "-" + str_month + "-" + str_day +" 00:00:00"
        else:
            return datetimes_df

        pass

    def dealDateTime(self, x):
        df = self.df.copy()
        df[x] = df[x].map(self.dealDateTime_map)
        # self.return_df.loc[df.index,x] = df[x]
        return df[[x]]

    def fillZero(self, x, max):
        return "0" * (max - len(str(x))) + str(x)

    def dealSecond(self, str_second):
        '''
        处理异常的秒
        '''
        if str_second == "60":
            str_second = "59"
        return str_second

    def dealReturn(self, merge=""):
        '''
        Parma：
            merge：是否智能合并
        外界调用返回执行结果
        '''
        if merge != "":
            self.isMaege = merge
        if self.isMaege:
            return self.return_df.apply(self.dealMarge, axis=1)
        else:
            return self.return_df

    def dealMarge(self, x):
        '''
        进行处理完毕的数据进行合并
        '''
        try:
            if x.iloc[0] in x.iloc[1]:
                return x.iloc[1]
            elif x.iloc[1] in x.iloc[0]:
                return x.iloc[0]
            elif len(x.iloc[0]) >= 19 and x.iloc[1] == "00:00:00":
                return x.iloc[0]
            else:
                # print(x.iloc[1],len(x.iloc[1]))
                return x.iloc[0] + " " + x.iloc[1]
        except:
            return np.nan

    @staticmethod
    def testData():
        df = pd.DataFrame(data=[
            ["20240320", ""],
            ["20240320", "185059"],
            ["20240321", "85059"],
            ["20240322", "23"],
            ["20240323", "5"],
            ["20240324", "18:50:59"],
            ["20240325", "8:5:59"],
            ["20240326", "8.5.59"],
            ["20241025", "20241025121520"],
            ["20241025", "2024-10-25 121520"],
            ["20240323", "2024-03-23121520"],
            ["20240323121520", "2024-3-23121520"],
            ["20240323121520", "2024-3-2312:15:20"],
            ["20240323121520", ""],
            ["20170826", "20170826150111464"],
        ], columns=["交易日期", "交易时间"])
        return df

    @staticmethod
    def help():
        print('''
        测试用例：
        DealDateAndTime.testData() # 测试数据
        dealdatafunc = DealDateAndTime(DealDateAndTime.testData()) # 实例化
        # 获取最终结果
        dealdatafunc.dealReturn()
        # 获取指定情况结果
        dealdatafunc.dealDate("交易日期") #仅解析日期格式【参数为要解析的列明】
        dealdatafunc.dealTime("交易时间") #仅解析时间格式
        dealdatafunc.dealDateTime("交易日期时间") #仅解析日期加时间组合格式
        ''')