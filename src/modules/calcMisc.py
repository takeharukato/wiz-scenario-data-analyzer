#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file calcMisc.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief 雑多な計算ユーティリティ処理
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details 雑多な計算ユーティリティ処理

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
#from typing import Any #,Optional

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os

#
# サードパーティーモジュールの読込み
#

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def simple_round(number:float, ndigits:int=0)-> float:
    """四捨五入する

    Args:
        number (float): 四捨五入する値
        ndigits (int, optional): 四捨五入する桁数. Defaults to 0.

    Returns:
        float: 小数点ndigitsで四捨五入した値
    """
    p = 10 ** ndigits
    return (number * p * 2 + 1) // 2 / p
