#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file charImgDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の高解像度用文字ビットマップを解析する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の高解像度用文字ビットマップを解析する

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
from typing import Any,Optional

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.dataEntryDecoder import dataEntryDecoder
from modules.datadef import WizardrySCNTOC, WizardryCharImgData,WizardryCharImgDataEntry
from modules.utils import getDecodeDict
import modules.consts

"""高解像度モード用文字情報のPascal定義
    TCHRIMAG = PACKED ARRAY[ 0..7] OF 0..255; (* 8バイト(各バイトは, 1ラインのビットマップ) *)
    CHARSET  : PACKED ARRAY[ 0..63] OF TCHRIMAG; (* 1セット64文字 *)
"""

# 高解像度モード用文字情報のサイズ(単位:バイト)
CHARIMG_ENTRY_SIZE=8

# 高解像度モード用文字アイテム情報のデータレイアウト
WizardryCharImgDataEntryDef:dict[str,Any]={
    'LINE_0': {'offset':0, 'type': 'B'}, # 0ライン
    'LINE_1': {'offset':1, 'type': 'B'}, # 1ライン
    'LINE_2': {'offset':2, 'type': 'B'}, # 2ライン
    'LINE_3': {'offset':3, 'type': 'B'}, # 3ライン
    'LINE_4': {'offset':4, 'type': 'B'}, # 4ライン
    'LINE_5': {'offset':5, 'type': 'B'}, # 5ライン
    'LINE_6': {'offset':6, 'type': 'B'}, # 6ライン
    'LINE_7': {'offset':7, 'type': 'B'}, # 7ライン
}

class charImgDecoder(dataEntryDecoder):
    """文字イメージデコーダ"""

    def _dict2CharImgDataEntry(self, toc:WizardrySCNTOC, decode_dict:dict[str,Any])->WizardryCharImgDataEntry:
        """unpackしたアイテム情報をpythonのオブジェクトに変換

        Args:
            toc (WizardrySCNTOC): 目次情報
            decode_dict (dict[str,Any]): unpackしたアイテム情報の辞書(unpackしたデータの要素名->bytes列のタプル)

        Returns:
            WizardryCharImgDataEntry: pythonのオブジェクトであらわした文字情報
        """
        res = WizardryCharImgDataEntry(bitmap={})

        for line in range(modules.consts.CHARIMG_HEIGHT):
            idx_key = f"LINE_{line}" # ライン情報
            if idx_key in decode_dict:
                res.bitmap[line]=int(decode_dict[idx_key][0])
            else:
                res.bitmap[line]=0

        return res

    def _decodeOneChar(self, toc:WizardrySCNTOC, data: Any, char_type:int, ch_idx: int)->WizardryCharImgDataEntry:

        # 対象文字の開始オフセット位置(単位:バイト)を得る
        blk_offset = modules.consts.CHARIMG_TYPE_TO_BLK_OFFSET[char_type] * modules.consts.BLK_SIZ

        # 対象文字のデータ位置(単位:バイト)を得る
        data_offset = CHARIMG_ENTRY_SIZE * ch_idx + blk_offset

        # 解析対象データをunpackする
        decode_dict = getDecodeDict(data=data,layout=WizardryCharImgDataEntryDef,offset=data_offset)

        return self._dict2CharImgDataEntry(toc=toc, decode_dict=decode_dict)

    def decodeOneData(self, toc:WizardrySCNTOC, data: Any, index: int)->Optional[Any]:
        """シナリオデータファイル中の文字セットデータを解析する

        Args:
            toc (WizardrySCNTOC): 目次情報
            data (Any): シナリオデータファイル情報
            index (int): 未使用

        Returns:
            Optional[Any]: キャラクタセット情報
        """
        res = WizardryCharImgData(normal_bitmap={},cemetary_bitmap={})

        # 各文字をデコードする
        for ch_idx in range(modules.consts.CHARIMG_PER_CHARSET):
            res.normal_bitmap[ch_idx]=self._decodeOneChar(toc=toc, data=data, char_type=modules.consts.CHARIMG_TYPE_NORMAL, ch_idx=ch_idx)
            res.cemetary_bitmap[ch_idx]=self._decodeOneChar(toc=toc, data=data, char_type=modules.consts.CHARIMG_TYPE_CEMETARY, ch_idx=ch_idx)

        return res