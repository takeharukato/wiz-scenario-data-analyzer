#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file genExpTbl.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の経験値表のレイアウト定義を出力する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の経験値表のレイアウト定義を出力する

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

NR_IDX=13

if __name__ == "__main__":
    offset = 0
    #
    for idx in range(NR_IDX):
        desc = f"レベル13から14への必要経験値" if idx == 0 else f"レベル{idx+1}に到達するための累積経験値"
        print(f"'EXP_{idx}_LOW': {{ 'offset':{offset}, 'type': '<H' }}, # {desc}下位4桁")
        offset += 2
        print(f"'EXP_{idx}_MID': {{ 'offset':{offset}, 'type': '<H' }}, # {desc}中位4桁")
        offset += 2
        print(f"'EXP_{idx}_HIGH': {{ 'offset':{offset}, 'type': '<H' }}, # {desc}上位4桁")
        offset += 2
    print("")

    pass
