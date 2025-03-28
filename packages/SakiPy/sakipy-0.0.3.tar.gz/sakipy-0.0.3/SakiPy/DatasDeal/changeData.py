'''
修改数据类型的函数
'''
from SakiPy.Core.core import is_nan

class ChangeData:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ChangeData, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 初始化操作，仅在第一次实例化时执行
        if not hasattr(self, 'initialized'):
            self.initialized = True
    def floatToPercentage(self,num:(str,float,int),save_len=2,suffix="%"):
        """
        把数字转化为百分比样式
        :param num: 转化对象
        :param save_len: 保存小数几位
        :param suffix: 后缀样式
        :return: 字符串
        """
        if type(num) != float:
            try:
                num = self.strToFloat(num)
                print(num)
                num = float(num)
            except:
                print("num不是类float属性")
                return num
        return str(round((num)*100,save_len))+suffix

    def strToFloat(self, num, save_len=2):
        """
        【金额处理函数】
        字符串仅保留数字部分与.与-
        如果转化失败变为0
        :param num:  待转化的字符串【仅保留正确内容的最前部分】
        :param save_len: 保留的小数点长度(默认为2)
        :return: result转化后的浮点数
        Example：
        1687.-00.1 =》1687.0
        -1687.-00.1 =》-1687.0
        16。87.-00.1 =》 1687.0
        - =》 0
        """
        # 处理除-，.数字以外的符号
        result = ''.join(c for c in str(num) if c.isdigit() or c == '.' or c == '-')
        # 处理两个以上的.
        if (result.count('.') > 1):
            result = ".".join(result.split(".")[0:2])
        # 处理两个及其以上的-（包括位置不对的）
        if (result.count('-') > 1):
            if result.startswith('-'):
                result = "-" + result.split("-")[1]
            else:
                result = result.split("-")[0]
        elif (result.count('-') == 1) and (not result.startswith('-')):
            result = result.split("-")[0]
        # 数据为空时
        if is_nan(result) or result == "-":
            result = 0
        # 处理小数保留位数
        if save_len == 0:
            result = int(result)
        else:
            result = round(float(result), save_len)
        return result
    def dataframeStrToFloat(self,df,columns_list=["交易金额","交易余额"]):
        '''
        统一数据类型
        把数字字段变为float类型
        parms：
        df：被统一的数据Dataframe
        columns_list:
        return:
        df
        '''
        for i in columns_list:
            if i in df.columns:
                try:
                    df.loc[:,i] = df.loc[:,i].astype(float)
                except:
                    df.loc[:,i] = df.loc[:,i].apply(self.strToFloat)
                    df.loc[:,i] = df.loc[:,i].astype(float)
        return df