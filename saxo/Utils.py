from collections import namedtuple

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def DicToObj(name, dic = {}):
        keys = list(dic.keys())
        vals = list(dic.values())
        Data = namedtuple('data', keys)
        return Data._make(vals)

    @staticmethod
    def DicToObjList(name, dicList = []):
        ret = []
        for item in dicList:
            if isinstance(item, dict):
                ret.append(Utils.DicToObj(name, item))
        return ret