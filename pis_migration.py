#!/usr/bin/python
# -*-coding:utf-8-*-

# pis数据迁移

import evernote_me

# # 1.迁移普通文本
# plainData=open("/Users/zhouzhipeng/Documents/pis_migration/plainData.txt").read()
# for line in plainData.split("\r\n"):
#     array=line.split("\t\t")
#     evernote.createPlainNote(array[0],array[1])


# 1.迁移普通文本
fileData=open("/Users/zhouzhipeng/Documents/pis_migration/filesData.txt").read()
for line in fileData.split("\r\n"):
    array=line.split("\t\t")
    if len(array)>0:
        evernote_me.createFileNote(array[0], "/Users/zhouzhipeng/Documents/pis_migration/" + array[1])

