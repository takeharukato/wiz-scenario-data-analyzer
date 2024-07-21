#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file genExpTbl.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の呪文ハッシュ表のレイアウト定義を出力する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の呪文ハッシュ表のレイアウト定義を出力する

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

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import modules.consts

if __name__ == "__main__":
    offset = 366
    #
    for idx,name in enumerate(modules.consts.DBG_WIZ_SPELL_NAMES):
        print(f"|SPELLHSH[{idx}]|{offset}|2|{name}呪文識別番号(SPELLHSHのハッシュ値)|")
        offset += 2
    print("")

    pass
