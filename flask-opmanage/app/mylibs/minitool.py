#!/usr/bin/evn python
#coding:utf-8
import random
from hashlib import md5
from itertools import *
from operator import itemgetter
def GetMd5(Msg):
    m = md5()
    m.update(Msg)
    return m.hexdigest()

def GetRandomString():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def formatString(verList):
    resultValue = ""
    d = {}
    for i in  range(len(verList)):
        d.setdefault(verList[i]['agent'],[]).append(int(verList[i]['zone']))
        print d
    for key in d:
        d[key].sort()
        resultValue = resultValue + "%s:" %(key)
        for k, g in groupby(enumerate(d[key]), lambda (i, x): i - x):
            ret = map(itemgetter(1), g)
            if len(ret) > 1:
                resultValue = resultValue + "%s-%s," %(str(ret[0]), str(ret[-1]))
            elif len(ret) == 1:
                resultValue = resultValue + "%s," %(str(ret[0]))
        resultValue = resultValue.rstrip(',') + "<br>"
    return resultValue.rstrip("<br>")