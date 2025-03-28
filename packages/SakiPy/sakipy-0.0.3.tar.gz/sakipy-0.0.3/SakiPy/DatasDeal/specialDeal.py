"""
处理不规则表头的文件

"""
import numpy as np

from SakiPy.Core.core import ErrorDeal


# 特殊处理之一【模糊标记】
def Special_Type(df):
    '''【模糊】
    针对首行首列为：兴业银行深圳分行账户交易对账单的数据
    '''
    if (df.columns[0].startswith("兴业银行深圳分行账户交易对账单")) and (len(df.columns)==16):
        ding = df[df.iloc[:,0] == "账户名称"].index.tolist()
        if len(ding)==1:
            df.columns = df.iloc[2,:]
            df.drop(index=[0,1,2],inplace=True)#删除被提取的信息
            sheet = "兴业银行深圳分行账户交易对账单"
        else:
            print("兴业银行深圳分行账户交易对账单【模板】发现多个头文件")
    return df

# 特殊处理之一【精准标记】
def Special_Type1(df):
    '''
    针对首行首列为：历史交易明细 的数据
    '''
    if (len(df.columns) == 12):
        ding = df[df.iloc[:, 0] == "交易日"].index.tolist()
        if len(ding) == 1:
            df.columns = df.iloc[1, :]
            df["交易卡号"] = df.iloc[0, 1]
            df["交易户名"] = df.iloc[0, 5]
            df["交易账号"] = df.iloc[0, 8]
            df.drop(index=[0, 1], inplace=True)  # 删除被提取的信息
            sheet = "历史交易明细"
        else:
            print("历史交易明细【模板】发现多个头文件")
    return df


def Special_Type2(df):
    # print("触发Special_Type2")
    if (len(df.columns) == 14):
        if (df.columns[8] == "个人交易明细"):
            ding = df[(df.iloc[:, 0] == "传票号") | (df.iloc[:, 0] == "交易流水号")].index.tolist()
            if len(ding) == 1:
                df.columns = df.iloc[1, :]
                df["交易卡号"] = df.iloc[0, 7]
                df["交易户名"] = df.iloc[0, 5]
                df["交易账号"] = df.iloc[0, 2]
                df["币种"] = df.iloc[0, 10]
                df.drop(index=[0, 1], inplace=True)  # 删除被提取的信息
                sheet = "个人交易明细"
                # print(sheet)
            else:
                print("个人交易明细【模板】发现多个头文件")
        elif (df.columns[4] == "对公交易明细"):
            ding = df[df.iloc[:, 0] == "交易流水号"].index.tolist()
            if len(ding) == 1:
                df.columns = df.iloc[1, :]
                df["交易卡号"] = df.iloc[0, 7]
                df["交易户名"] = df.iloc[0, 5]
                df["交易账号"] = df.iloc[0, 2]
                df.drop(index=[0, 1], inplace=True)  # 删除被提取的信息
                sheet = "对公交易明细"
                # print(sheet)
            else:
                print("对公交易明细【模板】发现多个头文件")
    return df


def Special_Type3(df):
    if (df.columns[0] == "中国银行存款历史交易明细清单(CTIS)") and (len(df.columns) == 18):
        ding = df[df.iloc[:, 0] == "交易日"].index.tolist()
        if len(ding) == 1:
            df.columns = df.iloc[2, :]
            df["交易卡号"] = df.iloc[0, 11]  # 查询账号->
            df["交易户名"] = df.iloc[0, 5]  # 姓名->
            df["交易账号"] = df.iloc[0, 8]  # 客户号->
            df["新账号"] = df.iloc[0, 15]  # 新账号->
            df.drop(index=[0, 1, 2], inplace=True)  # 删除被提取的信息
            sheet = "中国银行存款历史交易明细清单(CTIS)"
        else:
            print("中国银行存款历史交易明细清单(CTIS)【模板】发现多个头文件")
    return df


def Special_Type4(df):
    if (df.columns[0] == "深圳农商银行账户历史交易明细") and (len(df.columns) == 14):
        ding = df[df.iloc[:, 0] == "交易日期"].index.tolist()
        if len(ding) == 1:
            df.columns = df.iloc[2, :]
            df["交易卡号"] = df.iloc[0, 0].split("：")[1]
            df["子账号"] = df.iloc[1, 0].split("：")[1]
            df["币种"] = df.iloc[1, 4].split("：")[1]
            df["交易户名"] = df.iloc[0, 4].split("：")[1]
            df.drop(index=[0, 1, 2], inplace=True)  # 删除被提取的信息
            df.drop(index=df[df.iloc[:, 0] == "备注："].index, inplace=True)  # 删除被提取的信息
            sheet = "深圳农商银行账户历史交易明细"
        else:
            print("深圳农商银行账户历史交易明细【模板】发现多个头文件")
    elif (df.columns[0] == "深圳农商银行账户历史交易明细") and (len(df.columns) == 13):
        ding = df[df.iloc[:, 0] == "交易日期"].index.tolist()
        if len(ding) == 1:
            df.columns = df.iloc[4, :]
            df["交易卡号"] = df.iloc[1, 0].split("：")[1]
            df["交易账号"] = df.iloc[2, 0].split("：")[1]
            df["交易户名"] = df.iloc[1, 4].split("：")[1]
            df["币种"] = df.iloc[3, 0].split("：")[1]
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
    return df


def Special_Type5(df):
    # 司法个人客户信息查询/司法个人账户信息查询
    if (df.columns[0] == "司法个人客户信息查询") or (df.columns[0] == "司法个人账户信息查询"):
        ding = df[df.iloc[:, 0] == "客户号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.iloc[3, :]
            df.drop(index=[0, 1, 2, 3], inplace=True)  # 删除被提取的信息
            sheet = "司法个人客户信息查询"
        else:
            print("司法个人客户信息查询【模板】发现多个头文件")
            pass
        pass
    return df


def Special_Type6(df):
    # 中国邮政储蓄银行账户交易明细,中国邮政储蓄银行账户交易明细专用回单,中国邮政储蓄银行账户交易明细专用回单
    if ((len(df.columns) == 12) | (len(df.columns) == 13)):
        ding = df[df.iloc[:, 0] == "交易日期"].index.tolist()
        if len(ding) == 1:
            df.columns = df.iloc[3, :]
            df["交易卡号"] = df.iloc[0, 1]  # 查询账号->
            df["交易户名"] = df.iloc[0, 5]  # 姓名->
            df.drop(index=[0, 1, 2, 3], inplace=True)
            pass
        ding = df[df.iloc[:, 0] == "交易时间"].index.tolist()
        if len(ding) == 1:
            df.columns = df.iloc[3, :]
            df["交易卡号"] = df.iloc[0, 1]  # 查询账号->
            df["交易户名"] = df.iloc[0, 5]  # 姓名->
            df.drop(index=[0, 1, 2, 3], inplace=True)
            pass
    return df


def Special_Type7(df):
    if (len(df.columns) == 14) and (df.columns[0] == r"中国民生银行账户交易明细清单"):
        ding = df[df.iloc[:, 0] == "查询卡号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.iloc[ding[0], :]
            if df.iloc[ding[0]+1:, :].shape[0] == 0:
                if df.iloc[1, 0] == "客户账号":
                    df.loc[0, "查询卡号"] = df.iloc[1,1]
                if df.iloc[2, 0] == "账户账号":
                    df.loc[0, "交易账号"] = df.iloc[2,1]
                if df.iloc[0, 0] == "客户名称":
                    df.loc[0, "交易户名"] = df.iloc[0,1]
                df.rename(columns={"查询卡号": "交易卡号"}, inplace=True)
                df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            else:
                if df.iloc[2, 0] == "账户账号":
                    df["交易账号"] = df.iloc[2,1]
                if df.iloc[0, 0] == "客户名称":
                    df["交易户名"] = df.iloc[0,1]
                if df.iloc[1, 0] == "客户账号":
                    df["查询卡号"] = df.iloc[1,1]
                df.rename(columns={"查询卡号": "交易卡号"}, inplace=True)
                df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
        else:
            # TODO 出现两个的情况【后面出现复杂情况再修改定位方法】目前先简单合并
            if ding[0] == 0:
                df.columns = df.iloc[ding[0], :].tolist()
                df.rename(columns={"查询卡号": "交易卡号"}, inplace=True)
                df.drop(index=ding, inplace=True)
    if len(df.columns) == 14:
        ding = df[df.iloc[:, 0] == "序号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.iloc[ding[0], :]
            df["交易户名"] = df.iloc[0, 1].split(" ")[-1]  # 姓名->
            df["交易卡号"] = df.iloc[0, 1].split(" ")[0]  # 查询账号->
            df["交易账号"] = df.iloc[0, 6]
            df.drop(index=[0, 1], inplace=True)
            pass
        pass
    return df


def Special_Type8(df):
    if (len(df.columns) == 23):
        ding = df[df.iloc[:, 0] == "产品号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.iloc[1, :]
            df.rename(columns={"产品号": "交易卡号", "客户代码": "交易账号", "客户名称": "交易户名",
                               "交易对手账号": "对手卡号", "交易对手客户代码": "对手账号", "交易对手户名": "对手户名"},
                      inplace=True)

            df.drop(index=[0, 1], inplace=True)
            # df.drop(df.loc[df[df.iloc[:,0].isna()].index[0]:,:].index,inplace=True)

            if "进出标志" not in df.columns:
                df["交易金额"] = df["交易金额"].astype(float)
                df["进出标志"] = np.nan
                df.loc[df[df["交易金额"] > 0].index, "进出标志"] = "进"
                df.loc[df[df["交易金额"] <= 0].index, "进出标志"] = "出"
                df["交易金额"] = abs(df["交易金额"])
            pass
        pass
    return df


def Special_Type9(df):
    if (len(df.columns) == 14):
        ding = df[df.iloc[:, 0] == "序号"].index.tolist()
        if len(ding) == 1:
            print(ding)
            df.columns = df.iloc[1, :]
            df["交易户名"] = df.iloc[0, 0].split(" ")[0].split("：")[-1]  # 姓名->
            df["交易卡号"] = df.iloc[0, 0].split(" ")[4].split("：")[-1]  # 查询账号->
            df["交易账号"] = df.iloc[0, 0].split(" ")[2].split("：")[-1]
            df.drop(index=[0, 1], inplace=True)
            map_dict = {'序号': '序号', '过账日期': '交易时间', '业务类型': '交易类型', '借贷标志': '进出标志',
                        '币种': '币种', '发生额': '交易金额', '凭证号': '凭证号', '余额': '交易余额',
                        '摘要': '交易摘要', '对方账号(或商户编号)': '对手卡号', '对方户名(或商户名称)': '对手户名',
                        '对方银行': '对手开户行', '交易机构': '交易机构', '操作员': '操作员'}
            df.rename(columns=map_dict, inplace=True)
            pass
        pass
    return df


def Special_Type10(df):
    if (len(df.columns) == 11):
        ding = df[df.iloc[:, 0] == "序号"].index.tolist()
        if len(ding) == 1:
            print(ding)
            df.columns = df.iloc[4, :]
            df["交易户名"] = df.iloc[0, 7]  # 姓名->
            df["交易卡号"] = df.iloc[0, 1]  # 查询账号->
            df.drop(index=[0, 1, 2, 3, 4], inplace=True)
            map_dict = {'账户余额': '交易余额', '对方行名': "对手开户行"}
            df.rename(columns=map_dict, inplace=True)
            pass
        pass
    return df


def Special_Type11(df):
    if (df.columns[0] == "账户名称") & (df.columns[1] == "账号") & (df.columns[2] == "币种") & (
            df.columns[3] == "介质类型") & (len(df.columns) == 13):
        ding = df[df.iloc[:, 0] == "交易日期1"].index.tolist()
        if len(ding) == 1:
            print(ding)
            df.columns = df.iloc[1, :]
            df["交易户名"] = df.iloc[0, 0]  # 姓名->
            # df["交易卡号"] = df.iloc[0,1] # 查询账号->
            df.drop(index=[0, 1], inplace=True)
            if df[df["可用余额"] != df["余额"]].shape[0] == 0:
                df.drop(columns=["可用余额"], inplace=True)
            map_dict = {'介质号': '交易卡号', '交易日期1': "交易时间", "交易摘要描述": "交易摘要", "余额": "交易余额"}
            df.rename(columns=map_dict, inplace=True)
            pass
        pass
    return df


def Special_Type12(df):
    if (df.columns[0] == "根据账号卡号查询存款交易明细") & (len(df.columns) == 23):
        ding = df[df.iloc[:, 0] == "交易日期"].index.tolist()
        if len(ding) == 1:
            print(ding)
            df.columns = df.iloc[8, :]
            # df["交易户名"] = df.iloc[1,4] # 姓名->
            # df["交易卡号"] = df.iloc[2,4] # 查询账号->
            df.drop(index=[i for i in range(9)], inplace=True)
            # if df[df["可用余额"]!=df["余额"]].shape[0]==0:
            #     df.drop(columns=["可用余额"],inplace=True)
            # map_dict = {'介质号':'交易卡号', '交易日期1':"交易时间","交易摘要描述":"交易摘要","余额":"交易余额"}
            # df.rename(columns=map_dict,inplace=True)
            pass
        pass
    return df


def Special_Type13(df):
    if (df.columns[0] == r"根据账号/卡号查明细") & (len(df.columns) == 24):
        ding = df[df.iloc[:, 0] == "序号"].index.tolist()
        if len(ding) == 1:
            print(ding)
            df.columns = df.iloc[4, :]
            df["交易户名"] = df.iloc[2, 1]  # 姓名->
            df["交易证件号码"] = df.iloc[2, 5]  # 姓名->
            # df["交易卡号"] = df.iloc[2,4] # 查询账号->
            df.drop(index=[i for i in range(5)], inplace=True)
            # if df[df["可用余额"]!=df["余额"]].shape[0]==0:
            #     df.drop(columns=["可用余额"],inplace=True)
            # map_dict = {'介质号':'交易卡号', '交易日期1':"交易时间","交易摘要描述":"交易摘要","余额":"交易余额"}
            # df.rename(columns=map_dict,inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type13")
        pass
    return df


def Special_Type14(df):
    if (df.columns[0] == r"账户交易明细表_doris") & (len(df.columns) == 42):
        ding = df[df.iloc[:, 0] == "户名"].index.tolist()
        if len(ding) == 1:
            print(ding)
            df.columns = df.loc[ding[0], :]
            # df["交易户名"] = df.iloc[2,1] # 姓名->
            # df["交易证件号码"] = df.iloc[2,5] # 姓名->
            # df["交易卡号"] = df.iloc[2,4] # 查询账号->
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            # if df[df["可用余额"]!=df["余额"]].shape[0]==0:
            #     df.drop(columns=["可用余额"],inplace=True)
            # map_dict = {'介质号':'交易卡号', '交易日期1':"交易时间","交易摘要描述":"交易摘要","余额":"交易余额"}
            # df.rename(columns=map_dict,inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type14")
        pass
    return df


def Special_Type15(df):
    if (df.columns[0] == r"对公CTIS查询") & (len(df.columns) == 31):
        ding = df[df.iloc[:, 0] == "交易账号"].index.tolist()
        if len(ding) == 1:
            print(ding, "Special_Type15")
            df.columns = df.loc[ding[0], :]
            # df["交易户名"] = df.iloc[2,1] # 姓名->
            # df["交易证件号码"] = df.iloc[2,5] # 姓名->
            # df["交易卡号"] = df.iloc[2,4] # 查询账号->
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            # if df[df["可用余额"]!=df["余额"]].shape[0]==0:
            #     df.drop(columns=["可用余额"],inplace=True)
            # map_dict = {'介质号':'交易卡号', '交易日期1':"交易时间","交易摘要描述":"交易摘要","余额":"交易余额"}
            # df.rename(columns=map_dict,inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type15")
        pass
    return df


def Special_Type16(df):
    if df.shape[0] <= 2:
        return df
    if (df.columns[0] == r"账户开户名称") & (df.columns[1] == r"开户人证件号码") & (df.iloc[1, 0] == r'交易卡号') & (
            len(df.columns) == 45):
        ding = df[df.iloc[:, 0] == "交易卡号"].index.tolist()
        if len(ding) == 1:
            # print(ding, "Special_Type16")
            df.columns = df.loc[ding[0], :]
            df["交易户名"] = df.iloc[0, 0]
            df["交易证件号码"] = df.iloc[0, 1]
            df["交易开户行"] = df.iloc[0, 23]
            df["交易卡号"] = df.iloc[0, 2]
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            # df.dropna(axis=1, how="all", inplace=True)
            # df.dropna(axis=0, how="all", inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type16")
        pass
    return df

def Special_Type17(df):
    if df.shape[0] <= 2:
        return df
    if (df.columns[0] == r"交易对手批量查询导出") & (len(df.columns) == 16):
        ding = df[df.iloc[:, 0] == "序号"].index.tolist()
        if len(ding) == 1:
            # print(ding, "Special_Type17")
            df.columns = df.loc[ding[0], :]
            df.rename(columns={"账号":"交易账号","客户账号":"交易卡号"}, inplace=True)
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            # df.dropna(axis=1, how="all", inplace=True)
            # df.dropna(axis=0, how="all", inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type17")
        pass
    elif (len(df.columns) == 67):
        ding = df[df.iloc[:, 0] == "序号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.loc[ding[0], :]
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            # 自定义删除列【修改这里模板识别对应的也要改】
            df = df.drop(columns=["批量交易明细标志", '起息日','牌价','主机日期','前台交易日期','前台流水号','原交易日期','原柜员流水号',
                                  '交易柜员','授权柜员','账户营业机构','账户会计机构','业务代号','事件编号','传票组序号','传票组内序号',
                                  '柜员流水号','科目号','科目存储代码','科目存储描述','交易代码','营业机构','帐务机构','渠道类型编号',])
            df.rename(columns={"账号": "交易卡号", "客户账号": "交易账号"}, inplace=True)
    return df
def Special_Type18(df):
    if df.shape[0] <= 2:
        return df
    if (df.columns[0] == r"司法个人客户基本信息查询") & (len(df.columns) == 21):
        ding = df[df.iloc[:, 0] == "客户号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.loc[ding[0], :]
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            # df.dropna(axis=1, how="all", inplace=True)
            # df.dropna(axis=0, how="all", inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type18")
        pass
    elif (df.columns[0] == r"司法个人账户基本信息查询") & (len(df.columns) == 24):
        ding = df[df.iloc[:, 0] == "查询类型"].index.tolist()
        if len(ding) == 1:
            df.columns = df.loc[ding[0], :]
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            # df.dropna(axis=1, how="all", inplace=True)
            # df.dropna(axis=0, how="all", inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type18")
    return df

def Special_Type19(df):
    if df.shape[0] <= 2:
        return df
    if (df.columns[0] == r"中国民生银行个人客户信息") & (len(df.columns) == 12):
        ding = df[df.iloc[:, 0] == "序号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.loc[ding[0], :]
            df["交易户名"] = df.iloc[3, 1]
            df["交易证件号码"] = df.iloc[5, 1]
            df["联系手机"] = df.iloc[7,4]
            df["工作单位"] = df.iloc[10, 1]
            df["住宅地址"] = df.iloc[8, 1]
            df["证件登记地址"] = df.iloc[6, 1]
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            # df.dropna(axis=1, how="all", inplace=True)
            # df.dropna(axis=0, how="all", inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type18")
        pass
    return df
def Special_Type20(df):
    if df.shape[0] <= 2:
        return df
    else:
        df = df.copy()
    if (len(df.columns) == 58):
        columns_list = ['司法编号','序号','交易日期','交易时间','客户号','客户名称','交易卡号','交易流水','交易套号','交易机构','账户代码','交易方向(D:借|C:贷)','币种名称','交易金额','联机余额','摘要名称','文字摘要','交易渠道','冲补账标记','经办柜员','对方帐号','对方客户名称','对方帐号开户机构名称','对手公私标识','对手客户证件国别','对手客户证件类型','对手客户证件号码','对方开户机构号','对手开户机构国别代码','对方开户地区','对手方账户类别','代办人','网上交易IP地址','网银MAC地址','网银设备号','代办人证件国别','代办人证件类型','代办人证件号码','跨境交易标识','交易方式标识','ATM机具编号','账户类型','账户类别','客户序号(客户号+户口序号唯一标识一个户口[识别新旧卡])','ATM所属机构编号','对方客户号','交易地区编码','交易代码','交易摘要','交易地区名称','交易机构编号','币种','渠道名称','证件号','手机号','是否手机号转账标识','户口名称','账号']
        df.index = df.index + 1
        df.loc[0, :] = df.columns.tolist()
        df.columns = columns_list
        # 检验是否存在非法字符
        illegal_characters = ErrorDeal.findIllegalCharacters(df)
        if len(illegal_characters) > 0:
            # 去除非法字符
            df = ErrorDeal.dealIllegalCharacters(df, illegal_characters)
    elif (len(df.columns) == 23):
        columns_list = ['司法编号', '序号', '交易日期', '交易时间', '客户号', '客户名称', '交易卡号', '交易流水', '交易套号',
         '交易机构', '账户代码', '交易方向(D:借|C:贷)', '币种名称', '交易金额', '联机余额', '摘要名称', '文字摘要',
         '交易渠道', '冲补账标记', '经办柜员', '对方帐号', '对方客户名称', '对方帐号开户机构名称']
        df.index = df.index + 1
        df.loc[0, :] = df.columns.tolist()
        df.columns = columns_list
        # 检验是否存在非法字符
        illegal_characters = ErrorDeal.findIllegalCharacters(df)
        if len(illegal_characters) > 0:
            # 去除非法字符
            df = ErrorDeal.dealIllegalCharacters(df, illegal_characters)
    else:
        print("调证模板未知Special_Type20")
    return df

def Special_Type21(df):
    if df.shape[0] <= 2:
        return df
    else:
        df = df.copy()
    # 验证
    columns = ['交易日期', '借贷标识', '交易金额', '账户余额', '对手账号', '对手名称', '对手行名', '交易机构', '交易柜员',
     '交易渠道', '摘要代码', '凭证号', '附言信息']
    if set(df.loc[2,:].tolist()) == set(columns):
        ding = df[df.iloc[:, 0] == "交易日期"].index.tolist()
        if len(ding) == 1:
            k1,v1 = df.columns[0].split("：")
            k2, v2 = df.columns[4].split("：")
            df.columns = columns
            df.loc[:,k1] = v1
            df.loc[:,k2] = v2
            k, v = df.iloc[0, 0].split("：")
            df.loc[:, k] = v
            k, v = df.iloc[1, 0].split("：")
            df.loc[:, k] = v
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            df.reset_index(drop=True, inplace=True)
            df.index = df.index + 4
    return df
def Special_Type22(df):
    """
    处理：司法协查数字化查控平台交易明细（个人客户活期明细）
    :param df:
    :return:
    """
    if df.shape[0] <= 2:
        return df
    if (df.columns[0] == r"司法协查数字化查控平台交易明细（个人客户活期明细）") & (len(df.columns) == 18):
        ding = df[df.iloc[:, 0] == "序号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.loc[ding[0], :]
            for i in df.iloc[0,0].split("\n"):
                k,v = i.split("：")
                if k=='证件类型及证件号码':
                    df["交易证件号码"] = v.split("(")[0]
                    break
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type18")
    else:
        print("司法协查数字化查控平台交易明细（个人客户活期明细）【有新结构】")
    return df
def Special_Type23(df):
    """
    处理：司法协查数字化查控平台客户信息（个人客户开户信息）
    :param df:
    :return:
    """
    if df.shape[0] <= 2:
        return df
    if (df.columns[0] == r"司法协查数字化查控平台客户信息（个人客户开户信息）") & (len(df.columns) == 9):
        ding = df[df.iloc[:, 0] == "序号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.loc[ding[0], :]
            for i in df.iloc[0,0].split("\n"):
                k,v = i.split("：")
                if k=='证件类型及证件号码':
                    df["交易证件号码"] = v.split("(")[0]
                    break
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type22")
    else:
        print("司法协查数字化查控平台客户信息（个人客户开户信息）【有新结构】")
    return df
def Special_Type24(df):
    """
    处理：司法协查数字化查控平台客户信息（个人客户信息）
    :param df:
    :return:
    """
    if df.shape[0] <= 2:
        return df
    if (df.columns[0] == r"司法协查数字化查控平台客户信息（个人客户信息）") & (len(df.columns) == 10):
        ding = df[df.iloc[:, 0] == "序号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.loc[ding[0], :]
            for i in df.iloc[0,0].split("\n"):
                k,v = i.split("：")
                if k=='证件类型及证件号码':
                    df["交易证件号码"] = v.split("(")[0]
                    break
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type22")
    else:
        print("司法协查数字化查控平台客户信息（个人客户开户信息）【有新结构】")
    return df

def Special_Type25(df):
    """
    处理：司法对公客户基本信息查询
    :param df:
    :return:
    """
    if df.shape[0] <= 2:
        return df
    if (df.columns[0] == r"司法对公客户基本信息查询") & (len(df.columns) == 56):
        ding = df[df.iloc[:, 0] == "客户号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.loc[ding[0], :]
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type25")
    else:
        print("司法对公客户基本信息查询【有新结构】")
    return df
def Special_Type26(df):
    """
    处理：司法对公账户基本信息查询
    :param df:
    :return:
    """
    if df.shape[0] <= 2:
        return df
    if (df.columns[0] == r"司法对公账户基本信息查询") & (len(df.columns) == 30):
        ding = df[df.iloc[:, 0] == "客户号"].index.tolist()
        if len(ding) == 1:
            df.columns = df.loc[ding[0], :]
            df.drop(index=[i for i in range(ding[0] + 1)], inplace=True)
            pass
        else:
            print("【多定位问题】Special_Type26")
    else:
        print("司法对公账户基本信息查询【有新结构】")
    return df



