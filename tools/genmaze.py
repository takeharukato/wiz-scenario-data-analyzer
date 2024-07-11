#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file mazeFloorDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の迷宮階層データのレイアウト定義を出力する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の迷宮階層データのレイアウト定義を出力するツール

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

dir_dic:dict[str,str]={
    'W':"西",
    'S':"南",
    'E':"東",
    'N':"北",
}
if __name__ == "__main__":
    offset = 0
    # 壁
    for dir in ['W','S','E','N']:
        print(f"#")
        print(f"# {dir_dic[dir]}側の壁")
        print(f"#")
        for idx in range(60):
            if idx % 4 == 3:
                print(f"'{dir}_{idx}': {{ 'offset':{offset}, 'type': '<H' }}, # {dir_dic[dir]}の壁4つ分")
            else:
                print(f"'{dir}_{idx}': {{ 'offset':{offset}, 'type': '<H' }}, # {dir_dic[dir]}の壁8つ分")
            offset += 2
        print("")

    print("")

    # 玄室情報
    print(f"#")
    print(f"# 玄室情報")
    print(f"#")
    for idx in range(40):
        if idx % 2 == 1:
            print(f"'FIGHTS_{idx}': {{ 'offset':{offset}, 'type': '<H' }}, # 玄室情報4個分")
        else:
            print(f"'FIGHTS_{idx}': {{ 'offset':{offset}, 'type': '<H' }}, # 玄室情報16個分")
        offset += 2
    print("")

    # イベント番号
    print(f"#")
    print(f"# 各座標で発生するイベントのイベント番号")
    print(f"#")
    for idx in range(100):
        print(f"'SQREXTRA_{idx}': {{ 'offset':{offset}, 'type': '<H' }}, # イベント番号4つ分")
        offset += 2
    print("")

    # イベント番号からイベント種別へのマップ
    print(f"#")
    print(f"# イベント番号(0から15)とイベント種別(TSQUARE)との関係")
    print(f"#")
    for idx in range(4):
        print(f"'SQRETYPE_{idx}': {{ 'offset':{offset}, 'type': '<H' }}, # イベント種別4つ分")
        offset += 2
    print("")

    print(f"#")
    print(f"# イベント番号(0から15)のイベントパラメタ1(AUX0)")
    print(f"#")
    # AUX0
    for idx in range(16):
        print(f"'AUX0_{idx}': {{ 'offset':{offset}, 'type': '<h' }}, # イベント情報{idx}")
        offset += 2
    print("")

    print(f"#")
    print(f"# イベント番号(0から15)のイベントパラメタ2(AUX1)")
    print(f"#")
    # AUX1
    for idx in range(16):
        print(f"'AUX1_{idx}': {{ 'offset':{offset}, 'type': '<h' }}, # イベント情報{idx}")
        offset += 2
    print("")

    print(f"#")
    print(f"# イベント番号(0から15)のイベントパラメタ3(AUX2)")
    print(f"#")
    # AUX2
    for idx in range(16):
        print(f"'AUX2_{idx}': {{ 'offset':{offset}, 'type': '<h' }}, # イベント情報{idx}")
        offset += 2
    print("")

    print(f"#")
    print(f"# モンスター出現テーブル")
    print(f"#")
    # モンスター出現テーブル
    for idx in range(3):
        print(f"'MINENEMY_{idx+1}': {{ 'offset':{offset}, 'type': '<H' }}, # モンスター番号最小値{idx+1}")
        offset += 2
        print(f"'MULTWORS_{idx+1}': {{ 'offset':{offset}, 'type': '<H' }}, # 開始モンスター番号算出係数{idx+1}")
        offset += 2
        print(f"'WORSE01_{idx+1}': {{ 'offset':{offset}, 'type': '<H' }}, # モンスター番号レンジの系統数{idx+1}")
        offset += 2
        print(f"'RANGE0N_{idx+1}': {{ 'offset':{offset}, 'type': '<H' }}, # モンスター番号レンジ{idx+1}")
        offset += 2
        print(f"'PERCWORS_{idx+1}': {{ 'offset':{offset}, 'type': '<H' }}, # モンスター番号レンジ切り替え確率{idx+1}")
        offset += 2
    print("")

    pass
