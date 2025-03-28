import sys
import warnings
import re

from .查询 import 查询
from .繁體廣韻搜索 import 繁體廣韻搜索

列字典 = {
    "拼音":"tupa_js",
    "白一平":"baxter_js",
    "高本漢":"karlgren_js",
    "潘悟雲":"panwuyun_js",
    "高汉本":"karlgren_js",
    "潘悟云":"panwuyun_js",
    "王力汉语语音史魏晋":"wangli魏晋南北朝_js",
    "王力汉语语音史隋唐": "wangli隋唐_js",
    "王力汉语史稿":"wangli汉语史稿_js",
    "0":"tupa_js",
    "1":"baxter_js",
    "2":"karlgren_js",
    "3":"panwuyun_js",
    "4":"wangli魏晋南北朝_js",
    "5": "wangli隋唐_js",
    "6":"wangli汉语史稿_js",
}

class 繁體擬音搜索:
    def __init__(self,源="王力汉语语音史魏晋"):
        self.列名 = 列字典.get(str(源)) if str(源) in 列字典 else sys.exit(warnings.warn("没有此源", SyntaxWarning))


    def __獲取音韻地位(self,list_a):
        result = {}

        for a in list_a:
            result[a] = {}
            b = 繁體廣韻搜索("nk2028").返回表字典(a)
            total = int(b["总行数"])
            data_list = b["数据"]

            for i in range(total):
                e = data_list[i]
                if "字頭" in e:
                    del e["字頭"]  # 删除"字頭"键

                f = e["音韻地位"]  # 音韻地位
                擬音查詢結果 = 查询().单列查询("基礎擬音", f"{self.列名}", "音韻地位", f)

                # 提取拟音字符串，如果查询结果不为空，则取第一个元组的第一个元素，否则设为空字符串
                擬音 = 擬音查詢結果[0][0] if 擬音查詢結果 else ""

                # 获取音韻地位中的最后一个字作为声调
                聲調 = f[-1] if f else ""  # 如果音韻地位存在且不为空，取最后一个字作为声调

                # 存储拟音和声调为一个列表 ["拟音", "声调"]
                e["擬音"] = [擬音, 聲調]
                result[a][f] = e  # 直接赋值

        return result

    @staticmethod
    def __構造擬音釋義列表(獲取音韻地位返回的字典):
        擬音釋義字典 = {}

        for 字頭, 音韻項 in 獲取音韻地位返回的字典.items():
            擬音釋義字典[字頭] = []  # 初始化列表

            for 音韻地位, 詳細數據 in 音韻項.items():
                擬音_聲調 = 詳細數據[f"擬音"]
                擬音 = 擬音_聲調[0]  # 第一个元素是拟音
                聲調 = 擬音_聲調[1]  # 第二个元素是声调
                釋義 = 詳細數據["釋義"]
                補充釋義 = 詳細數據["釋義補充"]

                # 如果釋義或補充釋義是null，則設為None
                if 釋義 is None:
                    釋義 = None
                if 補充釋義 is None:
                    補充釋義 = None

                # 添加 [拟音, 声调, 释义, 补充释义] 到列表
                擬音釋義字典[字頭].append([擬音, 聲調, 釋義, 補充釋義])

        return 擬音釋義字典

    def 返回擬音(self,字头):
        return 繁體擬音搜索.__構造擬音釋義列表(self.__獲取音韻地位(list(字头))) if re.match(r'^[\u4e00-\u9fa5]+$', 字头) else warnings.warn("只允许输入汉字.", UserWarning)
