#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file picColorSimple.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief 単純なモンスター/宝箱画像色決定ストラテジ
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details 単純なモンスター/宝箱画像色決定ストラテジ

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.picColorStrategy import WizardryPicDataEntry,picColorStrategy
import modules.consts

class picColorSimple(picColorStrategy):

    def updateColorImage(self, info:WizardryPicDataEntry)->None:
        """画像ファイルに出力するビットマップを更新する
           出力される色情報を単純にマッピングする(白色に隣接する色ビットの補色処理を割愛する)
        Args:
            info (WizardryPicDataEntry): モンスター/宝箱画像
        """

        for y in range(modules.consts.PIC_HEIGHT):
            for x in range(modules.consts.PIC_WIDTH):
                pos=(x,y)
                assert pos in info.bitmap_info,f"{pos} not found"
                bitmap_entry = info.bitmap_info[pos]
                if x > 0:
                    prev_pos=(x-1, y)
                    assert prev_pos in info.bitmap_info,f"{prev_pos} not found"
                    prev_entry = info.bitmap_info[prev_pos]

                    if prev_entry in modules.consts.COLORED_PIXEL and bitmap_entry == modules.consts.PIC_COLOR_BLACK:
                        # 前のビットが色のあるビットで, かつ, 次のビットが黒の場合, 前のビットの色にする
                        info.color_info[pos]=prev_entry
                        info.color_info[prev_pos]=prev_entry
                    elif prev_entry == modules.consts.PIC_COLOR_BLACK and bitmap_entry in modules.consts.COLORED_PIXEL:
                        # 前のビットが黒で, かつ, 次のビットが色のあるビットの場合, 後ろのビットの色にする
                        info.color_info[pos]=bitmap_entry
                        info.color_info[prev_pos]=bitmap_entry
                    elif prev_entry == modules.consts.PIC_COLOR_BLACK and bitmap_entry == modules.consts.PIC_COLOR_BLACK:
                        # 前のビットが黒で, かつ, 次のビットも黒の場合, 黒色にする
                        info.color_info[pos]=modules.consts.PIC_COLOR_BLACK
                        info.color_info[prev_pos]=modules.consts.PIC_COLOR_BLACK
                    else:
                        info.color_info[pos]=modules.consts.PIC_COLOR_WHITE
                        info.color_info[prev_pos]=modules.consts.PIC_COLOR_WHITE
                else:
                    info.color_info[pos]=bitmap_entry

        return