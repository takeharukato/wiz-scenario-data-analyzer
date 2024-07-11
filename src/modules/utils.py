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
from typing import Any #,Optional

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os
import struct

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import modules.consts

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

def word_to_use_string(class_value:int)->str:
    """符号なし整数16bitであらわされた装備可能職業文字列に変換する

    Args:
        class_value (int): 符号なし整数16bitであらわされた装備可能職業
        dic (dict[int,str]): ビットから意味を表す文字列への辞書
    Returns:
        str: 装備可能職業文字列
    """

    res:str=""
    v = class_value # 装備職業を表す整数を取得
    for bit in range(16): # 16ビットの各ビットについて

        if bit >= len(modules.consts.CHAR_CLASS_EQUIP_STRING):
            break

        if v & (1 << bit): # ビットが立っていて有効なら
            res += modules.consts.CHAR_CLASS_EQUIP_STRING[bit]
        else:
            res += '-'

    return res

def word_to_dic(word_value:int, dic:dict[int,str])->dict[int,str]:
    """符号なし整数16bitであらわされた倍打/防御/抵抗属性を文字列の辞書に変換する

    Args:
        word_value (int): 符号なし整数16bitであらわされた倍打/防御/抵抗属性
        dic (dict[int,str]): ビットから意味を表す文字列への辞書
    Returns:
        dict[int,str]: ビット->倍打/防御/抵抗属性
    """
    res:dict[int,str]={}
    v = word_value # 倍打/防御/抵抗属性を表す整数を取得
    for bit in range(16): # 16ビットの各ビットについて
        if v & (1 << bit) and bit in dic: # ビットが立っていて有効な属性なら
            res[bit]=dic[bit]

    return res

def getDecodeDict(data:Any, layout:dict[str,dict[str,Any]],offset:int)->dict[str,Any]:
    """データレイアウトを元に各データをpythonのbytesデータにアンパックする

    Args:
        data (Any): シナリオデータ
        layout (dict[str,dict[str,Any]]): データレイアウト
        offset (int): 解析対象データのシナリオデータ開始位置からのオフセットアドレス(単位:バイト)

    Returns:
        dict[str,Any]: キーからアンパック後のデータへの辞書
    """
    decode_dict:dict[str,Any]={}

    for k, v in layout.items(): # データレイアウトのキーと値を得る
        # データ構造メンバのオフセット位置を得る
        member_offset = offset + v['offset']
        data_type = v['type']
        # pythonのデータ型に変換する
        decode_dict[k] = struct.unpack_from(data_type, data, member_offset)

    return decode_dict

def value_to_string(val:int)->str:
    """値を表示用の文字列に変換

    Args:
        val (int): 値

    Returns:
        str: 文字列
    """
    return f"{val} {hex(val)} = {bin(val)}"

def property_dic_to_string(dic:dict[int,str])->str:
    """倍打/防御/抵抗辞書を文字列化する

    Args:
        dic (dict[int,str]): 倍打/防御/抵抗辞書

    Returns:
        str: キー値昇順で値を','で区切った文字列
    """
    return ','.join([dic[key] for key in sorted(dic.keys())])