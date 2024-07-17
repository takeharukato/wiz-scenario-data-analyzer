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

#
# サードパーティーモジュールの読込み
#
from svglib.svglib import svg2rlg # type: ignore
from reportlab.graphics import renderPM

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.datadef import WizardrySCNTOC
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
    return modules.consts.DELIMITER_COMMA.join([dic[key] for key in sorted(dic.keys())])

def calcDataEntryOffset(toc:WizardrySCNTOC, category: str, item_len:int, index: int)->int:
    """シナリオ情報先頭からのオフセット位置(単位:バイト)を算出する

    Args:
        toc (WizardrySCNTOC): 目次情報
        category (str): 目次の項目
            - ZZERO    シナリオ情報
            - ZMAZE    迷宮フロア情報
            - ZENEMY   モンスター情報
            - ZREWARD  報酬情報
            - ZOBJECT  アイテム情報
            - ZCHAR    キャラクター名簿
            - ZSPCCHRS モンスター/宝箱画像
            - ZEXP     経験値表
        item_len (int): アイテム一つ当たりのサイズ(単位:バイト)
        index (int): アイテムの配列中のインデクス

    Returns:
        int: シナリオ情報先頭からのオフセット位置(単位:バイト)
    """

    # 項目の開始オフセットブロック(単位:ブロック)を算出
    start_block = toc.BLOFF[category]
    # 項目の開始オフセット位置(単位:バイト)を算出
    start_offset = modules.consts.BLK_SIZ * start_block

    # キャッシュに読み込むディスクデータのシナリオ情報ファイルの先頭からのオフセット位置(単位:ブロック)を算出
    data_block = 2 * ( index // toc.RECPER2B[category] )
    data_block_offset = modules.consts.BLK_SIZ * data_block # オフセット位置をバイト単位に変換
    # 対象データのキャッシュ内でのオフセット位置(単位:バイト)を算出
    entry_offset = (index % toc.RECPER2B[category]) * item_len

    # 解析対象データのシナリオ情報先頭からのオフセット位置(単位:バイト)を算出
    data_offset = start_offset + data_block_offset + entry_offset

    return data_offset

def convertSVGtoRaster(infile:str, outfile:str, format:str=modules.consts.DEFAULT_RASTER_IMAGE_TYPE)->None:
    """SVG形式のベクタグラフィックスをラスタイメージに変換する

    Args:
        infile (str): 入力ファイル名
        outfile (str): 出力ファイル名
        format (str, optional): 出力フォーマット. Defaults to modules.consts.DEFAULT_RASTER_IMAGE_TYPE('png').
    """

    # ラスタイメージに変換するためのドロワーを取得
    drawing = svg2rlg(infile)
    if not drawing: # 入力ファイルを開けなかった場合
        return  # 何もせず抜ける

    upper_format=format.upper() # 大文字に変換する

    if upper_format not in modules.consts.RASTER_IMAGE_TYPE_DIC: # 対応フォーマットにない場合は, 何もせず抜ける
        return

    # 指定された形式にファイルを変換する
    renderPM.drawToFile(drawing, outfile, fmt=modules.consts.RASTER_IMAGE_TYPE_DIC[upper_format])

    return

def escapeMarkdownChars(in_str:str)->str:
    """マークダウンの特殊文字をエスケープする

    Args:
        in_str (str): 文字列

    Returns:
        str: 変換後の文字列
    """
    # バックスラッシュを変換
    res=in_str.replace('\\', '\\\\')

    for ch in modules.consts.MARKDOWN_ESCAPE_CHARS:
        res=res.replace(ch, f"\\{ch}") # エスケープ

    return res