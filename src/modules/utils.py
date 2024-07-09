#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file utils.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief ユーティリティ処理
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details ユーティリティ処理

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
#from typing import Any,Optional

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def decodePackedArrayUint16(data_dic:dict[int,int], bit_len:int, max_index:int)->dict[int,int]:
    """16ビット単位で格納されているpacked array中の整数値を解析し, 各値を格納した辞書を生成する

    Args:
        data_dic (dict[int,int]): 解析するデータ(16bit長)の配列(インデクス->値)
        bit_len (int): 1エントリ当たりのビット数
        max_index: 配列の最大インデクス
    Returns:
        dict[int,int]: 解析結果の連番から解析値への配列
    """
    res:dict[int,int]={}
    # 値を抽出するマスク
    mask = ( 1 << bit_len ) - 1
    array_index=0
    for idx in sorted(data_dic.keys()):
        v = data_dic[idx]
        bits_remain=16 # 残り処理ビット数
        while bits_remain >= bit_len and max_index >= array_index:

            value = v & mask # 値を取得する
            res[array_index] = value # 値を設定する

            v = v >> bit_len # 次の要素を処理する
            array_index += 1 # 配列のインデクスを加算する
            bits_remain -= bit_len # 残りビット数を更新する

    return res
