#-*-coding:utf-8 -*-
import random

# f=file("data/sp","w+")
#
# for j in range(245):
#     li = []
#     for i in range(144):
#         a=random.random()
#         if a>0.4:
#             li.append("1")
#         else:
#             li.append("0")
#     str_convert = ','.join(li)
#     f.writelines(str_convert)
#     f.write("\n")
#
# for j in range(255):
#     li = []
#     for i in range(144):
#         a=random.random()
#         if a>0.4:
#             li.append("0")
#         else:
#             li.append("1")
#     str_convert = ','.join(li)
#     f.writelines(str_convert)
#     f.write("\n")
# f.close()

f=file("data/trec","w+")

for j in range(480):
    li = []
    for i in range(300):
        a=random.random()
        if a>0.66:
            li.append("0")
        else:
            li.append("1")
    str_convert = ','.join(li)
    f.writelines(str_convert)
    f.write("\n")


f.close()

