import re

import numpy as np
import pandas as pd
import PyPDF2 as pdf

def read_pdf_GDYH_GR(pdf_file):
    # pdf_file="H:\工作\光大\复兴健康.pdf"
    # 读取PDF
    source = pdf.PdfReader(pdf_file, "rb")
    pages = len(source.pages)
    Marge = pd.DataFrame()
    for page_int in range(0, pages):
        #         print("正在解析：",page_int)
        # 获取指定页对象【从0开始计数】
        page = source.pages[page_int]
        # 获取该页中内容
        text = page.extract_text()
        if ("在我行无符合条件的开户记录" in text) or ("账号总笔数:0" in text):
            continue
        # 解析整体，进行每一样的划分
        box = ""
        data = []
        isnew = False
        rows = text.split("\n")

        data_df = pd.DataFrame(
            columns=["客户账号", "交易日期", "交易流水号", "存入金额", "转出金额", "账户余额", "摘要", "对方账号",
                     "对方名称"])

        # 每页对象解析
        name = rows[1].split(" ")[0].split(":")[1]
        card = rows[3].split(" ")[0].split(":")[1]

        rows = rows[6:-2]
        # 分割断层问题
        results = []
        # 分割断层问题
        for key, value in enumerate(rows):
            if re.match(r'^第(\d+)页', str(value)) or re.match(r'^========================', str(value)):
                break
            if (value.startswith(card)) | (value.startswith(" ")):
                '''每一行的开头都是对应卡号直接添加'''
                results.append(value)
            elif ("结息" in value) or ("银联消费" in value) or ("银联POS消费" in value) or ("医保" in value):
                '''可能换卡【目前已知的为：医保卡结息】'''
                results.append(value)
            else:
                # 针对名字
                if ")" in value:
                    value = ") ".join(value.split(")"))
                    pass
                try:
                    ss = str(re.findall("\d{11,24}$$", value)[0])
                    # 针对账户
                    value = value.replace(ss, "") + " " + ss
                except:
                    pass
                errs = ["****", "无", "取现", "代付", "货款", "结算", "分润", "交易", "提现"]
                for i in errs:
                    if i in value:
                        value = "{0} ".format(i).join(value.split(i))
                if len(results) == 0 and "不存在交易" in str(value):
                    continue
                else:
                    results[-1] = results[-1] + str(value)
        con = 0
        for row in results:
            row = row.split(" ")
            # 【每个元素】特殊情况类型处理START
            for key, value in enumerate(row):
                if re.match(r"^\d{4}[-|\.]\d{2}[-|\.]\d{2}", value):
                    # 时间格式开头跳过
                    continue
                result = re.search(r'^(\d+\.\d+)(\D+)', value)
                if result:
                    row.remove(value)
                    row.insert(key, result.groups()[0])
                    row.insert(key + 1, result.groups()[1])
            # 特殊情况类型处理END
            # for a in range(data_df.shape[1]-len(row)):
            #     row.append("")
            if data_df.shape[1] == len(row):
                if row[-2].isdigit():
                    data_df.loc[con, :] = row
                else:
                    data_df.loc[con, :] = [row[0], row[1], row[2], row[3], row[4], row[5], " ".join(row[6:-1]), np.nan,
                                           row[-1]]
            else:
                if row[-2].isdigit():
                    data_df.loc[con, :] = [row[0], row[1], row[2], row[3], row[4], row[5], " ".join(row[6:-2]), row[-2],
                                           row[-1]]
                else:
                    data_df.loc[con, :] = [row[0], row[1], row[2], row[3], row[4], row[5], " ".join(row[6:-1]), np.nan,
                                           row[-1]]
            con += 1
            pass
        data_df.insert(0, "交易卡号", card)
        data_df.insert(0, "交易户名", name)
        data_df["页码"] = page_int + 1
        data_df["行"] = data_df.index + 1
        Marge = pd.concat([Marge, data_df], ignore_index=True)
    return Marge