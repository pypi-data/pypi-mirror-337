#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 十六夜咲月
# @email   : ma18387890737@.outlook.com
# @time    : 2025/2/13 20:33
# @version : 0.0.1
# @project : SakiPy.dealBankCCB
# @function: the script is used to do something.
import numpy as np
import pandas as pd

class DealBankCCB:
    @staticmethod
    def personalCurrentDetails(df):
        """
        处理：个人活期明细信息-新一代
        :param df:
        :return:
        """
        datas = df.copy()
        ding = datas[datas.iloc[:, 0] == "交易日期"].index.tolist()
        ding.append(datas.shape[0] + 1)

        # 处理数据为空行问题
        if len(ding) == 1:
            return None
        df_detail = pd.DataFrame()
        for i in range(1 if len(ding) - 1 == 0 else len(ding) - 1):
            start = ding[i] + 1
            s = i + 1
            try:
                end = ding[s] - 1
            except:
                end = datas.index[-1]
            cache = datas.iloc[start:end, :].copy()
            cache.columns = datas.iloc[start - 1, :]
            cache.columns.name = "ID"
            dd = ding[i] - 1
            try:
                for values in datas.iloc[dd, 0].split("，"):
                    cache.insert(loc=0, column=values.split(":")[0], value=values.split(":")[1])
            except:
                pass
            if np.nan in cache.columns.tolist():
                cache = cache.drop(columns=[np.nan])
            df_detail = pd.concat([df_detail, cache], ignore_index=True)
        return df_detail
    @staticmethod
    def businessCurrentDetails(df):
        """
        处理：企业活期明细信息
        :param df:
        :return:
        """
        datas = df.copy()
        ding = datas[datas.iloc[:, 0] == "交易日期"].index.tolist()
        ding.append(datas.shape[0] + 1)
        # print(ding)
        # 处理数据为空行问题
        if len(ding)==1:
            return None
        df_detail = pd.DataFrame()
        for i in range(1 if len(ding) - 1 == 0 else len(ding) - 1):
            start = ding[i] + 1
            s = i + 1
            try:
                end = ding[s] - 1
            except:
                end = datas.index[-1]
            cache = datas.iloc[start:end, :].copy()
            cache.columns = datas.iloc[start - 1, :]
            cache.columns.name = "ID"
            dd = ding[i] - 1
            try:
                for values in datas.iloc[dd, 0].split("，"):
                    cache.insert(loc=0, column=values.split(":")[0], value=values.split(":")[1])
            except:
                pass
            if np.nan in cache.columns.tolist():
                cache = cache.drop(columns=[np.nan])
            df_detail = pd.concat([df_detail, cache], ignore_index=True)
        return df_detail
    @staticmethod
    def personalRegularDetails(df):
        """
        个人定期明细信息-新一代
        :param df:
        :return:
        """
        datas = df.copy()
        ding = datas[datas.iloc[:, 0] == "交易日期"].index.tolist()
        ding.append(datas.shape[0] + 1)
        # print(ding)
        # 处理数据为空行问题
        if len(ding) == 1:
            return None
        df_detail = pd.DataFrame()
        for i in range(1 if len(ding) - 1 == 0 else len(ding) - 1):
            start = ding[i] + 1
            s = i + 1
            try:
                end = ding[s] - 1
            except:
                end = datas.index[-1]
            cache = datas.iloc[start:end, :].copy()
            cache.columns = datas.iloc[start - 1, :]
            cache.columns.name = "ID"
            dd = ding[i] - 1
            try:
                for values in datas.iloc[dd, 0].split("，"):
                    cache.insert(loc=0, column=values.split(":")[0], value=values.split(":")[1])
                if cache.shape[0] > 0:
                    if np.nan in cache.columns.tolist():
                        cache = cache.drop(columns=[np.nan])
                    df_detail = pd.concat([df_detail, cache], ignore_index=True)
            except:
                pass
            pass
        return df_detail
    @staticmethod
    def businessRegularDetails(df):
        """
        企业定期明细信息
        :param df:
        :return:
        """
        datas = df.copy()
        ding = datas[datas.iloc[:, 0] == "交易日期"].index.tolist()
        ding.append(datas.shape[0] + 1)
        # print(ding)
        # 处理数据为空行问题
        if len(ding) == 1:
            return None
        df_detail = pd.DataFrame()
        for i in range(1 if len(ding) - 1 == 0 else len(ding) - 1):
            start = ding[i] + 1
            s = i + 1
            try:
                end = ding[s] - 1
            except:
                end = datas.index[-1]
            cache = datas.iloc[start:end, :].copy()
            cache.columns = datas.iloc[start - 1, :]
            cache.columns.name = "ID"
            dd = ding[i] - 1
            try:
                for values in datas.iloc[dd, 0].split("，"):
                    cache.insert(loc=0, column=values.split(":")[0], value=values.split(":")[1])
                if cache.shape[0] > 0:
                    if np.nan in cache.columns.tolist():
                        cache = cache.drop(columns=[np.nan])
                    df_detail = pd.concat([df_detail, cache], ignore_index=True)
            except:
                pass
            pass
        return df_detail
    @staticmethod
    def personalCardInfo(df):
        """
        新一代个人账户信息
        :param df:
        :return:
        """
        datas = df.copy()
        ding = datas[datas.iloc[:, 0] == "序号"].index.tolist()
        # 处理数据为空行问题
        if len(ding) == 1:
            return None
        i = 0
        df_detail = pd.DataFrame()
        for i in range(1 if len(ding) - 1 == 0 else len(ding) - 1):
            start = ding[i] + 1
            s = i + 1
            try:
                end = ding[s] - 1
            except:
                end = datas.index[-1]
            cache = datas.iloc[start:end, :].copy()
            cache.columns = datas.iloc[start - 1, :]
            cache.columns.name = "ID"
            ls = ["个人定期账户信息-新一代", "根据查询条件 【 卡号 】查询结果如下：","根据查询条件 【 证件号码 】查询结果如下：", "查无结果", "个人电子现金账户信息"]
            for i in ls:
                df = cache[cache.iloc[:, 0] == i]
                if df.shape[0] > 0:
                    cache.drop(index=df.index, inplace=True)
            if cache.shape[0] > 0:
                if np.nan in cache.columns.tolist():
                    cache = cache.drop(columns=[np.nan])
                df_detail = pd.concat([df_detail, cache], ignore_index=True)
            pass
        return df_detail
    @staticmethod
    def businessCardInfo(df):
        """
        企业账户信息
        :param self:
        :return:
        """
        datas = df.copy()
        ding = datas[datas.iloc[:, 0] == "序号"].index.tolist()
        # print(ding)
        # 处理数据为空行问题
        if len(ding) == 1:
            return None
        i = 0
        df_detail = pd.DataFrame()
        for i in range(1 if len(ding) - 1 == 0 else len(ding) - 1):
            start = ding[i] + 1
            s = i + 1
            try:
                end = ding[s] - 1
            except:
                end = datas.index[-1]
            cache = datas.iloc[start:end, :].copy()
            cache.columns = datas.iloc[start - 1, :]
            cache.columns.name = "ID"
            ls = ["个人定期账户信息-新一代", "根据查询条件 【 卡号 】查询结果如下：", "查无结果", "个人电子现金账户信息"]
            for i in ls:
                df = cache[cache.iloc[:, 0] == i]
                if df.shape[0] > 0:
                    cache.drop(index=df.index, inplace=True)
            if cache.shape[0] > 0:
                if np.nan in cache.columns.tolist():
                    cache = cache.drop(columns=[np.nan])
                df_detail = pd.concat([df_detail, cache], ignore_index=True)
            pass
        return df_detail

