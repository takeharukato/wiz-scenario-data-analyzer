#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file spellNameDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の呪文名データを解析する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の呪文名データを解析する

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
from modules.datadef import WizardrySCNTOC, WizardrySpellTblDataEntry,WizardrySpellNameTblEntry
import modules.consts

"""呪文情報
文字を表すバイト列を改行コードで区切って記録されている。
'*'で始まる名前は, 呪文レベルの区切りとして認識される
"""

class spellNameDecoder(dataEntryDecoder):

    def _decodeOneSpellData(self, spell_tbl:dict[int,list[WizardrySpellNameTblEntry]], blk_img:tuple[Any,...])->None:



        sp_level = 1
        idx=0

        code = int(blk_img[0])

        while code != modules.consts.SPELL_DELIMITER and len(blk_img) > idx:

            name=""
            spell_info = WizardrySpellNameTblEntry(has_delimiter=False,name="",spell_level=0)
            while True:

                code = int(blk_img[idx]) # 文字コードを取得する
                idx += 1 # 次の文字へ

                if code > 255: # 不正コード
                    continue # 読み飛ばす

                if code == modules.consts.SPELL_DELIMITER or idx > len(blk_img):
                    code = int(blk_img[idx]) # 文字コードを取得する
                    break # 呪文名の終端

                ch = chr(code) # 文字を読み取る
                if ch == modules.consts.SPELL_LEVEL_DELIMITER:
                    spell_info.has_delimiter = True # 呪文レベル更新
                    sp_level += 1 # 呪文レベルをあげる
                    continue # 読み飛ばす

                name += ch # 文字を追加する

            spell_info.spell_level = sp_level # 呪文レベルを格納する
            spell_info.name = name # 呪文名を格納する
            if sp_level not in spell_tbl:
                spell_tbl[sp_level]=[]
            spell_tbl[sp_level].append(spell_info)

        return

    def decodeOneData(self, toc:WizardrySCNTOC, data: Any, index: int)->Optional[Any]:
        """シナリオデータファイル中の呪文名データを解析する

        Args:
            toc (WizardrySCNTOC): 目次情報
            data (Any): シナリオデータファイル情報
            index (int): 調査対象のインデクス(未使用)

        Returns:
            Optional[Any]: 解析結果のオブジェクト
        """

        res = WizardrySpellTblDataEntry(tables={})
        for idx in range(len(modules.consts.SPELL_CATEGORY_VALID)):

            if modules.consts.SPELL_CATEGORY_VALID[idx] not in res.tables:
                res.tables[modules.consts.SPELL_CATEGORY_VALID[idx]] = {}

            spell_tbl = res.tables[modules.consts.SPELL_CATEGORY_VALID[idx]]

            offset = modules.consts.SPELL_NAME_BLOCK_DIC[modules.consts.SPELL_CATEGORY_VALID[idx]]
            raw_data = struct.unpack_from("512B", data, offset * modules.consts.BLK_SIZ) # ブロックを読み込む
            self._decodeOneSpellData(spell_tbl=spell_tbl, blk_img=raw_data)

        return res