'''
自定义归一化进出标志的函数
'''
import pandas as pd
def deal_sign_turnover(deal_data:pd.DataFrame):
    subset = ["进", "出"]
    try:
        if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) != 0:
            if deal_data["进出标志"].dropna().nunique() == 2:
                # 默认的字典位置
                subset = ["贷", "借"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"贷": "进", "借": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                    pass

                subset = ["贷方", "借方"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"贷": "进", "借": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ["存", "取"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"存": "进", "取": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ["贷(转入)", "借(转出)"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"贷(转入)": "进", "借(转出)": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ["2", "1"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"2": "进", "1": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ["２", "１"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"２": "进", "１": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ["0", "1"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"1": "进", "0": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ["+", "-"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"+": "进", "-": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ['C - 贷', 'D - 借']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"C - 贷": "进", "D - 借": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ['D 借方', 'C 贷方']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"C 贷方": "进", "D 借方": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ['C-贷', 'D-借']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"C-贷": "进", "D-借": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ['CREDIT', 'DEBIT']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"CREDIT": "进", "DEBIT": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ['C:贷', 'D:借']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"C:贷": "进", "D:借": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ['C 贷', 'D 借']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"C 贷": "进", "D 借": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ['C', 'D']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"C": "进", "D": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ['贷方', '借方']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"贷方": "进", "借方": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                    pass
                subset = ['入', '出']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"入": "进", "出": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                    pass
                subset = ['转入', '转出']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"转入": "进", "转出": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                    pass
                subset = ['入账', '出账']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"入账": "进", "出账": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                    pass
                subset = ['收', '支']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"收": "进", "支": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ['收', '付']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"收": "进", "付": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ['收入', '支出']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"收入": "进", "支出": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
            elif deal_data["进出标志"].dropna().nunique() == 3:
                subset = ["贷", "借", " "]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"贷": "进", "借": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                    pass
            else:
                # 进出标志多样性问题
                subset = ["+", "-", "贷"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"+": "进", "-": "出", "贷": "进"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                subset = ["C - 贷", "D - 借", "出", "进"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"C - 贷": "进", "D - 借": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                    pass
                subset = ['转出', '转入', '-']
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"转入": "进", "转出": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)

                subset = ["C", "D", "出", "进"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"C": "进", "D": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                else:
                    print("进出标志【异常】{0}".format(deal_data["进出标志"].dropna().unique()))
                subset = ['贷', '借', "出", "进"]
                if len(list(set(deal_data["进出标志"].dropna().unique().tolist()) - set(subset))) == 0:
                    deal_dict = {"贷": "进", "借": "出"}
                    deal_data["进出标志"] = deal_data["进出标志"].replace(deal_dict)
                else:
                    print("进出标志【异常】{0}".format(deal_data["进出标志"].dropna().unique()))
    except:
        return deal_data
    return deal_data
