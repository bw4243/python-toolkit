#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib


def generate():
    yield 1
    yield 2
    yield 3


# g=generate()


# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))


def func(a):
    print(a)
    return a ** 2


#
# ret = map(func, (2, 2, 3))
# print(ret)
# print(3 ** 3)

# items = [1, 2, 3, 4, 5]
# ss = map(lambda x: x ** 2, items)
#
# print(ss)


# some_list = ['a', 'b', 'c', 'b', 'c']
#
# duplicates = set([x for x in some_list if some_list.count(x) > 1])
#
# print(duplicates)

valid = {'yellow', 'red', 'blue', 'green'}

input_set = {'yellow', 'red', 'pink'}

print(input_set.intersection(valid))
