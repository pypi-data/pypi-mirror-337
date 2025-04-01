from __future__ import annotations

import random
from typing import Final

from beni import btask, bcolor
from beni.bfunc import syncCall
import pyperclip

app: Final = btask.app

_RANDOM_SIZE = 5

_TEMPLATE = '''
Dash Cover Custom Fit for {PRODUCT_NAME}, Dashboard Mat Pad {COLOR}
Dashboard Cover Dash Mat Fit for {PRODUCT_NAME} {COLOR}
Dashboard Cover Dash Cover Mat Pad Custom Fit for {PRODUCT_NAME} {COLOR}
Dashboard Cover Dash Cover Mat Pad Carpet Custom Fit for {PRODUCT_NAME} {COLOR}
Dashboard Cover Dash Cover Mat Carpet Pad Custom Fit for {PRODUCT_NAME} {COLOR}
Dashboard Cover Dash Cover Mat Custom Fit for {PRODUCT_NAME} {COLOR}
Dashboard Cover Dash Cover Mat Fit for {PRODUCT_NAME} {COLOR}
Dash Cover Custom Fit for {PRODUCT_NAME}, Dashboard Cover Mat Carpet Pad {COLOR}
Dashboard Cover Dash Mat Pad Custom Fit for {PRODUCT_NAME} {COLOR}
Dash Cover Mat Custom Fit for {PRODUCT_NAME}, Dashboard Cover Pad Carpet {COLOR}
Dash Cover Mat Fit for {PRODUCT_NAME}, Dashboard Carpet Pad {COLOR}
Dash Cover Mat Pad Custom Fit for {PRODUCT_NAME}, Dashboard Cover Carpet {COLOR}
Dash Cover Mat Custom Fit for {PRODUCT_NAME}, Dashboard Pad Carpet {COLOR}
'''


@app.command()
@syncCall
async def title():
    '创建遮光垫产品标题'

    # 输入产品名称和产品颜色
    productName = ''
    while not productName:
        productName = input('输入产品名称：').strip()
    color = input('输入产品颜色（没有可以不写）：').strip()

    # 整理随机5个
    templateList = _TEMPLATE.strip().split('\n')
    random.shuffle(templateList)
    templateList = templateList[:_RANDOM_SIZE]

    resultList = []
    for i, template in enumerate(templateList):
        result = template.format(
            PRODUCT_NAME=productName,
            COLOR=color,
        ).strip()
        print(f'{i + 1}. {result}')
        resultList.append(result)

    pyperclip.copy('\n'.join(resultList))
    print('标题已复制到剪贴板')
    bcolor.printGreen('OK')
