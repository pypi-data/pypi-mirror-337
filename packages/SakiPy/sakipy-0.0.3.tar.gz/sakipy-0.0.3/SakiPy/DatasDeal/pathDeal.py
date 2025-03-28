"""
处理关于路径相关的函数
"""
import os

import natsort


class PathDeal:
    def __init__(self):
        pass

    @staticmethod
    def get_file_and_parent_folder(path) -> str:
        """
        获取所给文件路径文件名与文件名父级路径的地址
        :param path:
        :return:
        """
        # 获取文件名
        file_name = os.path.basename(path)
        # 获取父目录的路径
        parent_dir = os.path.dirname(path)
        # 获取父目录的名称
        parent_folder_name = os.path.basename(parent_dir)
        return os.path.join(parent_folder_name, file_name)

    @staticmethod
    def find_file_path_func(search_path: str, include_strs: list = None, filter_strs: list = None,
                            is_explore: bool = False, return_path_type: bool = True, *args, **kwargs):
        """
        查找指定目录下所有的文件及文件夹，返回文件路径与文件夹路径
        var
            :param search_path: 查找的目录路径
            :param include_strs: 获取仅包含字符串的名称，默认为None
            :param filter_strs: 过滤包含字符串的名称，默认为None
            :param is_explore: 是否探索所有文件，默认False【不探索】
            :param return_path_type:规定返回的路径样式，默认True【绝对路径】
                False【相对路径】
        return
            :param files :返回文件路径地址 ：类型list
            :param dirs:返回涉及的文件夹地址 ：类型list
        """
        files = []
        dirs = []
        # 获取路径下所有文件
        try:
            names = natsort.natsorted(os.listdir(search_path), alg=natsort.ns.PATH)
        except:
            names = os.listdir(search_path)

        if is_explore:
            # 探索所有文件
            for name in names:
                path = PathDeal.return_path_type_func(search_path, name, return_path_type)
                if os.path.isfile(path):  # 判断是否为文件
                    # 检测包含指定字符串
                    if include_strs is not None:
                        is_exist = True
                        for include_str in include_strs:
                            if include_str in name:
                                is_exist = False
                                break
                        if is_exist:
                            continue
                    # 检测过滤指定字符串
                    if filter_strs is not None:
                        for filter_str in filter_strs:
                            is_exist = False
                            if filter_str in name:
                                is_exist = True
                                break
                        if is_exist:
                            continue

                    files.append(path)
                else:
                    dirs.append(path)
                    # 递归合并
                    files_list, dirs_list = PathDeal.find_file_path_func(
                        path,
                        include_strs=include_strs,
                        filter_strs=filter_strs,
                        is_explore=is_explore,
                        return_path_type=return_path_type
                    )
                    files.extend(files_list)
                    dirs.extend(dirs_list)
        else:
            for name in names:
                path = PathDeal.return_path_type_func(search_path, name, return_path_type)
                if os.path.isfile(path):  # 判断是否为文件
                    # 检测包含指定字符串
                    if include_strs is not None:
                        is_exist = True
                        for include_str in include_strs:
                            if include_str in name:
                                is_exist = False
                                break
                        if is_exist:
                            continue
                    # 检测过滤指定字符串
                    if filter_strs is not None:
                        for filter_str in filter_strs:
                            is_exist = False
                            if filter_str in name:
                                is_exist = True
                                break
                        if is_exist:
                            continue

                    files.append(path)
                else:
                    dirs.append(path)
            pass

        return files, dirs

    @staticmethod
    def return_path_type_func(search_path, name, is_abs: bool = False) -> str:
        if is_abs:
            path = os.path.abspath(os.path.join(search_path, name))
        else:
            path = os.path.relpath(os.path.join(search_path, name))
        return path