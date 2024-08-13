from file import *
import pickle

a = ['light',0,[2,10,22],0,0,0]
'''     |    |  |  |     | | |
|       |    |  |  |     | | |
名称 明暗主题 |  |  |     | | |
 f1CB1的停留位置 |  |     | | |
    f1CB2的停留位置 |     | | |
        两个自定义的值    | | |
             f1CB3的停留位置| |
            随机延迟的停留位置 |
              长按触发的停留位置
         
'''

BinaryWriteFile('./UsersTheme.pkl',pickle.dumps(a))

print('重置完成')