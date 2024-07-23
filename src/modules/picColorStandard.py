#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file picColorStandard.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief 標準的なモンスター/宝箱画像色決定ストラテジ
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details 標準的なモンスター/宝箱画像色決定ストラテジ

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

class picColorStandard(picColorStrategy):

    def updateColorImage(self, info:WizardryPicDataEntry)->None:
        """画像ファイルに出力するビットマップを更新する
           標準的な色マッピングによるビットマップ生成
        Args:
            info (WizardryPicDataEntry): モンスター/宝箱画像
        """
        #
        # 1. 連続したビットを白色にする
        #
        for y in range(modules.consts.PIC_HEIGHT):
            for x in range(1,modules.consts.PIC_WIDTH):

                prev_pos=(x-1, y)
                assert prev_pos in info.bitmap_info,f"{prev_pos} not found"
                prev_entry = info.bitmap_info[prev_pos]

                pos=(x,y)
                assert pos in info.bitmap_info,f"{pos} not found"
                bitmap_entry = info.bitmap_info[pos]

                if prev_entry in modules.consts.COLORED_PIXEL and bitmap_entry in modules.consts.COLORED_PIXEL:
                    # 前のビットが色のあるビットで, かつ, 現在のビットも色がついてるビットの場合は, 両者を白色にする
                    info.color_info[pos]=modules.consts.PIC_COLOR_WHITE
                    info.color_info[prev_pos]=modules.consts.PIC_COLOR_WHITE
        #
        # 2.白色以外のビットを埋める
        #
        for y in range(modules.consts.PIC_HEIGHT):
            for x in range(1,modules.consts.PIC_WIDTH):

                pos=(x,y)

                if pos in info.color_info and info.color_info[pos] == modules.consts.PIC_COLOR_WHITE:
                    continue # 白色を飛ばす

                assert pos in info.bitmap_info,f"{pos} not found"
                bitmap_entry = info.bitmap_info[pos]

                prev_pos=(x-1, y)
                assert prev_pos in info.bitmap_info,f"{prev_pos} not found"
                prev_entry = info.bitmap_info[prev_pos]

                next_pos=(x+1, y)
                prev_prev_pos=(x-2, y)

                if prev_entry in modules.consts.COLORED_PIXEL and bitmap_entry == modules.consts.PIC_COLOR_BLACK:

                    # 前のビットが色のあるビットで, かつ, 次のビットが黒の場合, 前のビットの色にする
                    if next_pos in info.bitmap_info and info.bitmap_info[next_pos] == modules.consts.PIC_COLOR_BLACK:
                        # 現在のビットの次のビットも黒なら黒色にする
                        info.color_info[pos]=modules.consts.PIC_COLOR_BLACK
                    else:
                        # 現在のビットの次のビットが黒でなければ前のビットの色にする
                        info.color_info[pos]=prev_entry
                    info.color_info[prev_pos]=prev_entry # 前のビットの色を決定する
                elif prev_entry == modules.consts.PIC_COLOR_BLACK and bitmap_entry in modules.consts.COLORED_PIXEL:

                    # 前のビットが黒で, かつ, 次のビットが色のあるビットの場合, 後ろのビットの色にする
                    if prev_prev_pos in info.bitmap_info and info.bitmap_info[prev_prev_pos] == modules.consts.PIC_COLOR_BLACK:
                        # 現在のビットの前のビットも黒なら前のビットを黒色にする
                        info.color_info[prev_pos]=modules.consts.PIC_COLOR_BLACK
                    else:
                        # 現在のビットの前のビットが色つきなら前のビットを後続のビットに合わせる
                        info.color_info[prev_pos]=bitmap_entry
                    info.color_info[pos]=bitmap_entry # 現在のビットの色を決定する

                elif prev_entry == modules.consts.PIC_COLOR_BLACK and bitmap_entry == modules.consts.PIC_COLOR_BLACK:
                    # 前のビットが黒で, かつ, 次のビットも黒の場合, 黒色にする
                    info.color_info[pos]=modules.consts.PIC_COLOR_BLACK
                    info.color_info[prev_pos]=modules.consts.PIC_COLOR_BLACK
        #
        # 表示色に合わせて右端以外のビット中の連続ビットを白色にする
        # (両端の処理は上記で実施済みなため)
        #
        for y in range(modules.consts.PIC_HEIGHT):
            for x in range(1,modules.consts.PIC_WIDTH-1):

                prev_pos=(x-1, y)
                if prev_pos not in info.color_info: # マップされていない部分は黒にする
                    info.color_info[prev_pos]=modules.consts.PIC_COLOR_BLACK

                prev_entry = info.color_info[prev_pos]

                pos=(x,y)
                assert pos in info.color_info,f"{pos} not found"
                bitmap_entry = info.color_info[pos]

                next_pos=(x+1,y)

                if prev_entry == modules.consts.PIC_COLOR_WHITE \
                    and bitmap_entry in modules.consts.COLORED_PIXEL \
                    and ( next_pos in info.bitmap_info and info.bitmap_info[next_pos] == modules.consts.PIC_COLOR_BLACK ) or \
                    ( next_pos not in info.bitmap_info):
                    # 前のビットが白色で, かつ, 現在のビットが色がついてるビットで次のビットへの表示指示がなければ
                    # 白色にマップする
                    info.color_info[pos]=modules.consts.PIC_COLOR_WHITE

        return
