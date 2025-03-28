from collections import Counter
import pandas as pd
class FindDuplicates:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FindDuplicates, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 初始化操作，仅在第一次实例化时执行
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def list(self, lst,model:("all", "unique", "repeat") = "all"):
        """
        返回list中的不重复原始
        :param lst:需要处理的list
        :param model: 3中模式all去重后的所有数据；unique返回不重复的数据；repeat返回重复元素(仅一个）
        :return: 默认返回去重后的所有数据
        """
        if isinstance(lst, pd.core.indexes.base.Index):
            lst = lst.tolist()
        # 使用Counter计算每个元素出现的次数
        counts = Counter(lst)

        # 初始化两个空列表用于存储唯一元素和重复元素
        self.unique_elements = []
        self.duplicate_elements = []
        self.all_elements = []

        # 遍历counts字典，根据元素出现的次数分类
        for element, count in counts.items():
            if count == 1:
                self.unique_elements.append(element)
            else:
                self.duplicate_elements.append(element)
            self.all_elements.append(element)
        return self.listReturn(model=model)

    def listReturn(self,model:("all", "unique", "repeat") = "all"):
        """
        返回list运行的其他modeal结果
        :param model: all：返回去重后的所有元素
                        unique：返回仅出现一次的元素
                        repeat：返回出现多次的元素
        :return: 默认
            []
        """
        try:
            if model == "all":
                return self.all_elements
            elif model == "unique":
                return self.unique_elements
            else:
                return self.duplicate_elements
        except:
            print("请先运行list")
            return []
    def list_repeat(self,lst):
        '''
        返回list中的重复元素
        '''
        if isinstance(lst,pd.core.indexes.base.Index):
            lst = lst.tolist()
        return [x for x in set(lst) if lst.count(x) > 1]
    def list_repeat_no(self,lst):
        '''
        返回list中的不重复元素
        '''
        if isinstance(lst,pd.core.indexes.base.Index):
            lst = lst.tolist()
        return [x for x in set(lst) if lst.count(x) == 1]
    def list_all(self,lst):
        '''
        返回list中的不重复元素
        '''
        if isinstance(lst,pd.core.indexes.base.Index):
            lst = lst.tolist()
        # 使用Counter计算每个元素出现的次数
        return list(set(lst))
    def help(self):
        print("""
        对list数据进行处理：第一次运行list函数并加入要处理的list数据
        获取其他处理结果可用listReturn然后设置不同的模式就行，他会返回list函数处理的其他结果;
        单独每次运行可用【每次都需要重复计算输入的值】：list_all【返回去重的结果】，list_repeat_no【返回重复元素】，list_repeat【返回不重复元素】
        """)