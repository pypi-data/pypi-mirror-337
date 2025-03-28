# 标签编码
import json
import os

import numpy as np
import requests

from sklearn.preprocessing import LabelEncoder
import pandas as pd

import joblib
from SakiPy._version import __base_path__
from SakiPy.Core.core import singleton,listRemove

from SakiPy.Core.global_resource import BankNameDict

class DataProcess:
    def __init__(self, df, colum_name=None, lable_name=None, str_max=None, lableMap=None, fill_value="#", **kwargs):
        self.df = df
        self.df = self.df.astype(str)
        if colum_name is None:
            self.colum_name = self.df.columns[0]
        else:
            self.colum_name = colum_name
        self.fill_value = fill_value
        if colum_name is None:
            self.lable_name = self.df.columns[-1]
        else:
            self.lable_name = lable_name
        if str_max is None:
            self.str_max = self.df[colum_name].str.len().max()
            print("当前模型str_max：", self.str_max)
        else:
            if self.df[colum_name].str.len().max() > int(str_max):
                print("【注意】识别对象参数大于你设定的最多参数值")
            self.str_max = int(str_max)

        self.__data = self.df[self.colum_name].apply(self.preprocess_text)
        if lableMap is None:
            self.__lableMap = LabelEncoder()
        else:
            self.__lableMap = lableMap

    def preprocess_text(self, s):
        """
        把数据每个字符分开，不足的按照fill_value进行填充，多的进行剪短
        """
        l = []
        l.extend(str(s))
        Enough = self.str_max - len(l)
        l.extend(self.fill_value * Enough)
        # 获取字符串中所有字符的Unicode码点
        code_points = [ord(char) for char in l[0:self.str_max]]

        return pd.Series(code_points)

    def preprocess_text_len(self):
        """
        计算字符的长度
        """
        self.__data = pd.concat([self.__data, self.df[self.colum_name].apply(len)], axis=1)

    def data(self):
        return self.__data.to_numpy()

    def lable(self):
        # 创建编码器

        self.__lable = self.__lableMap.fit_transform(self.df[self.lable_name])
        print("""请调用lableMap获取编辑后的标签对应模型
        lableMap.inverse_transform([识别的结果进行标签对应])""")
        return self.__lable

    def lableMap(self):
        return self.__lableMap

def read_model(name="",base=True):
    if base:
        path = os.path.join(__base_path__,"Resources", name)
    else:
        path = name
    print(path)
    return joblib.load(path)

def save_model(model,name="oo.pkl",base=True):
    if base:
        path = os.path.join(__base_path__,"Resources", name)
    else:
        path = name
    print(path)
    joblib.dump(model, path)

@singleton
class BankCardLook:
    """
    """
    def __init__(self):
        self.bank_dict = {}
        '''储存识别开户字典'''
        path = os.path.join(__base_path__,"Resources", "银行开户行字典.json")
        with open(path, 'r', encoding='utf-8') as file:
            self.bank_dict = json.load(file)

        self.bank_type = {}
        '''储存识别的银行所属行'''
        path = os.path.join(__base_path__, "Resources", "银行所属行.json")
        with open(path, 'r', encoding='utf-8') as file:
            self.bank_type = json.load(file)

        self.__request_param = {"name": "小红", "content": "Hello World!"}

        self.bank_cardType = {
            'CC': "信用卡",
            'DC': "储蓄卡",
            'SCC': "准贷记卡",
            'PC': "预付费卡"
        }
        '''存储卡种类别'''

    def seekBank(self, card,cut=None):
        """
        查询银行卡开户行
        :param card: 需要识别的银行卡【支持数据类型字符串，长字符串（能够切割），列表，pd.DataFrame，
        :param cut: 仅长字符串类型有效
        :return:
        pd.DataFrame
        """
        df = pd.DataFrame()
        name = "卡号"
        if isinstance(card,pd.Series):
            df[name] = card
            df["开户行"] = df[name].apply(lambda row: self.__lookLocal(card=row))
            df.loc[df[df["开户行"].isna()].index, "开户行"] = df.loc[df[df["开户行"].isna()].index, name].apply(lambda row: self.__lookWeb(card=row))
        elif isinstance(card,pd.DataFrame):
            df = card.copy()
            for k, v in card.iloc[[0], :].iterrows():
                for i, e in v.items():
                    if str(e).isdigit() and len(str(e)) >= 6:
                        name = i
                        break
            if "开户行" not in df.columns.tolist():
                df["开户行"] = np.nan
            df["开户行"] = df[name].apply(lambda row: self.__lookLocal(card=row))
            df.loc[df[df["开户行"].isna()].index, "开户行"] = df.loc[df[df["开户行"].isna()].index, name].apply(lambda row: self.__lookWeb(card=row))
        elif isinstance(card,list):
            df = pd.DataFrame(columns=[name,"开户行"])
            df[name] = card
            df["开户行"] = df[name].apply(lambda row:self.__lookLocal(card=row))
            df.loc[df[df["开户行"].isna()].index, "开户行"] = df.loc[df[df["开户行"].isna()].index, name].apply(lambda row: self.__lookWeb(card=row))
        elif isinstance(card,str):
            card = listRemove(card,cut)
            df = pd.DataFrame(columns=[name, "开户行"])
            df[name] = card
            df["开户行"] = df[name].apply(lambda row: self.__lookLocal(card=row))
            df.loc[df[df["开户行"].isna()].index,"开户行"] = df.loc[df[df["开户行"].isna()].index,name].apply(lambda row: self.__lookWeb(card=row))
        return df
    def __lookLocal(self,card:str=None,bank_dict = None,*warg,**kwargs):
        """
        本地资源查询开户行
        :param card: 卡号
        :param bank_dict: 自定义的查询字典
        :param warg:
        :param kwargs:
        :return: 开户行
        """
        if bank_dict is None:
            bank_dict = self.bank_dict
        if isinstance(bank_dict,dict):
            card_13 = str(card[0:13])
            if card_13 in bank_dict.keys():
                return bank_dict.get(card_13,np.nan)
            card_9 = str(card[0:9])
            if card_9 in bank_dict.keys():
                return bank_dict.get(card_9,np.nan)
            card_8 = str(card[0:8])
            if card_8 in bank_dict.keys():
                return bank_dict.get(card_8,np.nan)
            card_6 = str(card[0:6])
            if card_6 in bank_dict.keys():
                return bank_dict.get(card_6,np.nan)
            card_5 = str(card[0:5])
            if card_5 in bank_dict.keys():
                return bank_dict.get(card_5,np.nan)
            card_4 = str(card[0:4])
            if card_4 in bank_dict.keys():
                return bank_dict.get(card_4,np.nan)
    def __lookWeb(self,card,url=None,param=None):
        '''

        :param card: 卡号
        :param url: 查询卡的链接
        :param param:
        :return: 开户行
        '''
        if url is None:
            url = 'https://ccdcapi.alipay.com/validateAndCacheCardInfo.json?_input_charset=utf-8&cardNo='+ card +'&cardBinCheck=true'
        if param is None:
            param = self.__request_param
        fails = 0
        while True:
            try:
                if fails >= 2:
                    break
                ret = requests.get(url=url, params=param, timeout=10)

                if ret.status_code == 200:
                    text = json.loads(ret.text)
                    try:
                        a = self.bank_type[text['bank']]
                    except:
                        a = text['bank']
                    try:
                        b = self.bank_cardType[text['cardType']]
                    except:
                        b = text['cardType']
                    if text['validated']:
                        return a + "-" + b + "-【网络查询】"
                    break
                else:
                    fails += 1
            except:
                fails += 1
        return np.nan


def identify_bank(text:str)->list:
    """
    根据输入文本识别涉及的银行名称
    :param text:  要识别的字符串
    :return: 匹配到的银行全名列表（可能多个）

    :Example
    df1 = df["数据来源"].apply(identify_bank)
    df1 = df1.str[0]
    """
    # 预处理文本：转为小写并去除空格
    clean_text = text.lower().replace(" ", "")

    matched_banks = []

    # 遍历所有银行进行匹配
    for bank, keywords in BankNameDict.items():
        for keyword in keywords:
            # 检查关键词是否存在于处理后的文本中
            if keyword.lower().replace(" ", "") in clean_text:
                matched_banks.append(bank)
                break  # 找到任一关键词即停止检查该银行

    return list(set(matched_banks))  # 去重后返回





