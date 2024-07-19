#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file expTblDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の経験値表データを解析する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の経験値表データを解析する

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
from modules.datadef import WizardrySCNTOC, WizardryExpTblClassEntry,WizardryExpTblDataEntry
from modules.utils import getDecodeDict
import modules.consts

"""経験値テーブル情報のPascal定義
    TEXP = ARRAY[ FIGHTER..NINJA] OF ARRAY[ 0..12] OF TWIZLONG;
"""

# 職業当たりの経験値表情報のサイズ(単位:バイト)
EXP_TBL_ENTRY_SIZE=78

# 職業当たりの経験値表情報のデータレイアウト
WizardryExpTableDataEntryDef:dict[str,Any]={
    'EXP_0_LOW': { 'offset':0, 'type': '<H' },    # レベル13から14への必要経験値下位4桁
    'EXP_0_MID': { 'offset':2, 'type': '<H' },    # レベル13から14への必要経験値中位4桁
    'EXP_0_HIGH': { 'offset':4, 'type': '<H' },   # レベル13から14への必要経験値上位4 桁
    'EXP_1_LOW': { 'offset':6, 'type': '<H' },    # レベル2に到達するための累積経験値下位4桁
    'EXP_1_MID': { 'offset':8, 'type': '<H' },    # レベル2に到達するための累積経験値中位4桁
    'EXP_1_HIGH': { 'offset':10, 'type': '<H' },  # レベル2に到達するための累積経験値上位4桁
    'EXP_2_LOW': { 'offset':12, 'type': '<H' },   # レベル3に到達するための累積経験値 下位4桁
    'EXP_2_MID': { 'offset':14, 'type': '<H' },   # レベル3に到達するための累積経験値 中位4桁
    'EXP_2_HIGH': { 'offset':16, 'type': '<H' },  # レベル3に到達するための累積経験値上位4桁
    'EXP_3_LOW': { 'offset':18, 'type': '<H' },   # レベル4に到達するための累積経験値 下位4桁
    'EXP_3_MID': { 'offset':20, 'type': '<H' },   # レベル4に到達するための累積経験値 中位4桁
    'EXP_3_HIGH': { 'offset':22, 'type': '<H' },  # レベル4に到達するための累積経験値上位4桁
    'EXP_4_LOW': { 'offset':24, 'type': '<H' },   # レベル5に到達するための累積経験値 下位4桁
    'EXP_4_MID': { 'offset':26, 'type': '<H' },   # レベル5に到達するための累積経験値 中位4桁
    'EXP_4_HIGH': { 'offset':28, 'type': '<H' },  # レベル5に到達するための累積経験値上位4桁
    'EXP_5_LOW': { 'offset':30, 'type': '<H' },   # レベル6に到達するための累積経験値 下位4桁
    'EXP_5_MID': { 'offset':32, 'type': '<H' },   # レベル6に到達するための累積経験値 中位4桁
    'EXP_5_HIGH': { 'offset':34, 'type': '<H' },  # レベル6に到達するための累積経験値上位4桁
    'EXP_6_LOW': { 'offset':36, 'type': '<H' },   # レベル7に到達するための累積経験値 下位4桁
    'EXP_6_MID': { 'offset':38, 'type': '<H' },   # レベル7に到達するための累積経験値 中位4桁
    'EXP_6_HIGH': { 'offset':40, 'type': '<H' },  # レベル7に到達するための累積経験値上位4桁
    'EXP_7_LOW': { 'offset':42, 'type': '<H' },   # レベル8に到達するための累積経験値 下位4桁
    'EXP_7_MID': { 'offset':44, 'type': '<H' },   # レベル8に到達するための累積経験値 中位4桁
    'EXP_7_HIGH': { 'offset':46, 'type': '<H' },  # レベル8に到達するための累積経験値上位4桁
    'EXP_8_LOW': { 'offset':48, 'type': '<H' },   # レベル9に到達するための累積経験値 下位4桁
    'EXP_8_MID': { 'offset':50, 'type': '<H' },   # レベル9に到達するための累積経験値 中位4桁
    'EXP_8_HIGH': { 'offset':52, 'type': '<H' },  # レベル9に到達するための累積経験値上位4桁
    'EXP_9_LOW': { 'offset':54, 'type': '<H' },   # レベル10に到達するための累積経験値下位4桁
    'EXP_9_MID': { 'offset':56, 'type': '<H' },   # レベル10に到達するための累積経験値中位4桁
    'EXP_9_HIGH': { 'offset':58, 'type': '<H' },  # レベル10に到達するための累積経験 値上位4桁
    'EXP_10_LOW': { 'offset':60, 'type': '<H' },  # レベル11に到達するための累積経験 値下位4桁
    'EXP_10_MID': { 'offset':62, 'type': '<H' },  # レベル11に到達するための累積経験 値中位4桁
    'EXP_10_HIGH': { 'offset':64, 'type': '<H' }, # レベル11に到達するための累積経験値上位4桁
    'EXP_11_LOW': { 'offset':66, 'type': '<H' },  # レベル12に到達するための累積経験 値下位4桁
    'EXP_11_MID': { 'offset':68, 'type': '<H' },  # レベル12に到達するための累積経験 値中位4桁
    'EXP_11_HIGH': { 'offset':70, 'type': '<H' }, # レベル12に到達するための累積経験値上位4桁
    'EXP_12_LOW': { 'offset':72, 'type': '<H' },  # レベル13に到達するための累積経験 値下位4桁
    'EXP_12_MID': { 'offset':74, 'type': '<H' },  # レベル13に到達するための累積経験 値中位4桁
    'EXP_12_HIGH': { 'offset':76, 'type': '<H' }, # レベル13に到達するための累積経験値上位4桁
}

class expTblDecoder(dataEntryDecoder):

    def _dict2ExpTableClassEntry(self, toc:WizardrySCNTOC, decode_dict:dict[str,Any])->WizardryExpTblClassEntry:
        """unpackした職業単位での経験値表情報をpythonのオブジェクトに変換

        Args:
            toc (WizardrySCNTOC): 目次情報
            decode_dict (dict[str,Any]): unpackした経験値表情報の辞書(unpackしたデータの要素名->bytes列のタプル)

        Returns:
            WizardryExpTblClassEntry: pythonのオブジェクトであらわした職業単位での経験値表
        """
        res = WizardryExpTblClassEntry(exp_table={})
        for level in range(modules.consts.EXP_TBL_ELEMENT_NR):
            long_val_array={}
            for idx,wizlong_key_name in enumerate(modules.consts.TWIZLONG_PARAMS):

                key_name=f"EXP_{level}_{wizlong_key_name}"
                assert key_name in decode_dict, f"{key_name} not found."
                long_val_array[idx]=int(decode_dict[key_name][0])
            res.exp_table[level]=long_val_array[0] + long_val_array[1] * 10000 + long_val_array[2] * 100000000

        return res

    def decodeOneData(self, toc:WizardrySCNTOC, data: Any, index: int)->Optional[Any]:
        """シナリオデータファイル中のアイテムデータを解析する

        Args:
            toc (WizardrySCNTOC): 目次情報
            data (Any): シナリオデータファイル情報
            index (int): 調査対象アイテムのインデクス

        Returns:
            Optional[Any]: 解析結果のオブジェクト, インデクスがレンジ外の場合, None
        """

        nr_tables=toc.RECPERDK[modules.consts.ZEXP] # 経験値表の数

        if 0 > index or index >= nr_tables:
            return None # 不正インデクス

        res = WizardryExpTblDataEntry(exp_table={})

        # 項目の開始オフセットブロック(単位:ブロック)を算出
        start_block = toc.BLOFF[modules.consts.ZEXP]
        # 項目の開始オフセット位置(単位:バイト)を算出
        data_block_offset = modules.consts.BLK_SIZ * start_block

        for cls_idx in range(modules.consts.NR_CLASS):

            # 対象職業の開始オフセット位置(単位:バイト)を算出
            data_offset = cls_idx * EXP_TBL_ENTRY_SIZE + data_block_offset

            # 解析対象データをunpackする
            decode_dict = getDecodeDict(data=data,layout=WizardryExpTableDataEntryDef,offset=data_offset)

            # unpackしたデータをpythonのオブジェクトに変換
            res.exp_table[cls_idx] = self._dict2ExpTableClassEntry(toc=toc, decode_dict=decode_dict)

        return res