#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file picDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の画像データを解析する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の画像データを解析する

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
import struct

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.dataEntryDecoder import dataEntryDecoder
from modules.datadef import WizardrySCNTOC, WizardryPicDataEntry
#from modules.utils import getDecodeDict,word_to_use_string,word_to_dic,calcDataEntryOffset
import modules.consts

"""画像データのPascal定義
レコード型データ構造としては定義なし,
1画像番号あたり512バイト(以下参照)
            ENEMYPIC( GETREC( ZSPCCHRS, BATTLERC[ 1].B.PIC, 512));
1行70ピクセルの情報を10バイトで, 表現
1画像あたり50行(500バイト)
"""
PIC_HEIGHT=50
PIC_WIDTH=70
PIC_BYTE_PER_LINE=10
PIC_START_X=1

APPLE_BIT_PTN1=0b1010101
APPLE_BIT_PTN2=0b0101010
APPLE_COLOR_DECISION_BIT=0x80
class picDecoder(dataEntryDecoder):
    """画像イメージデコーダ"""
    def _decideColor(self, x:int, y:int, val:int)->list[int]:

        scrn_x = x + PIC_START_X
        color_select = APPLE_COLOR_DECISION_BIT & val
        return []

    def _decodeOneImage(self, index:int, info:WizardryPicDataEntry)->None:


        return

    def decodeOneData(self, toc:WizardrySCNTOC, data: Any, index: int)->Optional[Any]:
        """シナリオデータファイル中の文字セットデータを解析する

        Args:
            toc (WizardrySCNTOC): 目次情報
            data (Any): シナリオデータファイル情報
            index (int): 画像番号

        Returns:
            Optional[Any]: キャラクタセット情報
        """

        res = WizardryPicDataEntry(raw_data=[],color_info={})

        # 対象画像の開始オフセット位置(単位:ブロック)を得る
        blk_offset = toc.BLOFF[modules.consts.ZSPCCHRS] + index
        # 項目の開始オフセット位置(単位:バイト)を算出
        start_offset = modules.consts.BLK_SIZ * blk_offset

        # 対象のデータ位置(単位:バイト)を得る
        for data_offset in range(modules.consts.BLK_SIZ):
            # # 解析対象データを1バイト単位でunpackする
            byte_val = struct.unpack_from('B', data, start_offset + data_offset)
            val = int(byte_val[0])
            res.raw_data.append(val)
        if index == 7: # TODO
            self._decodeOneImage(index=index, info=res)
        pass

        return None