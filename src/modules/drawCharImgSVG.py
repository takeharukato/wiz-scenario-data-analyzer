#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file drawCharImgSVG.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief SVGビットマップ描画実装部
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details SVGビットマップ描画実装部

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os

#
# サードパーティーモジュールの読込み
#
import svgwrite # type: ignore
from svgwrite import cm # type: ignore

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

OFFSET_SIZE=0
LEN_PER_PIXEL=1

BACKGROUND_COLOR='black'
FOREGROUND_COLOR='white'
from modules.datadef import WizardryCharImgDataEntry
import modules.consts

class drawCharImgSVG:

    _dwg:svgwrite.Drawing
    """描画領域"""
    _outfile_path:str
    """描画ファイルのパス名"""

    def __init__(self, outfile:str) -> None:
        """描画処理オブジェクトの初期化

        Args:
            outfile (str): 出力先ファイルへのパス
        """
        # ドローイング領域を作成
        self._dwg = svgwrite.Drawing(filename=outfile,
                                     size = (LEN_PER_PIXEL * modules.consts.CHARIMG_WIDTH + OFFSET_SIZE * 2,
                                            LEN_PER_PIXEL * modules.consts.CHARIMG_HEIGHT + OFFSET_SIZE * 2), debug=True)
        self.fill_background()     # 背景を塗りつぶす
        self._outfile_path = outfile # パスを記憶する

        return

    def drawBitMap(self, char_img:WizardryCharImgDataEntry) -> None:
        """キャラクタビットマップを描画する

        Args:
            char_img (WizardryCharImgDataEntry): キャラクタビットマップ情報
        """

        # バックグラウンド要素のグループを定義
        output_bitmap = self._dwg.add(self._dwg.g(id='charImg')) # type: ignore
        for row in range(modules.consts.CHARIMG_HEIGHT):
            if row not in char_img.bitmap:
                continue # 読み飛ばす
            line = char_img.bitmap[row]
            for col in range(modules.consts.CHARIMG_WIDTH):
                # ビットが立っているところを四角で塗りつぶす
                if line & (1 << col):
                    color=FOREGROUND_COLOR
                else:
                    color=BACKGROUND_COLOR
                rectangle = self._dwg.rect(insert=(col*LEN_PER_PIXEL + OFFSET_SIZE, # type: ignore
                                                   row*LEN_PER_PIXEL + OFFSET_SIZE),
                                        size=((LEN_PER_PIXEL), (LEN_PER_PIXEL)),
                                        fill=color)
                # 描画内容を反映する
                output_bitmap.add(rectangle) # type: ignore

        self._dwg.save() # 画像を保存する

        return

    def save(self)->None:
        """画像を保存する
        """
        self._dwg.save()
        return

    def fill_background(self)->None:
        """背景色を設定する
        """

        # バックグラウンド要素のグループを定義
        back_ground = self._dwg.add(self._dwg.g(id='background', stroke=BACKGROUND_COLOR)) # type: ignore

        # 四角で塗りつぶす
        rectangle = self._dwg.rect(insert=(0, 0), # type: ignore
                                   size=((modules.consts.CHARIMG_WIDTH + OFFSET_SIZE*2),
                                         (modules.consts.CHARIMG_HEIGHT + OFFSET_SIZE*2)),
                                   fill=BACKGROUND_COLOR)
        # 描画内容を反映する
        back_ground.add(rectangle) # type: ignore

        return
