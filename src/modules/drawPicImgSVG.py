#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file drawPicImgSVG.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief SVGモンスター/宝箱画像描画実装部
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details SVGモンスター/宝箱画像描画実装部

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

from modules.datadef import WizardryPicDataEntry
import modules.consts

OFFSET_MARGIN=0
OFFSET_SIZE=OFFSET_MARGIN*modules.consts.PIC_LEN_PER_PIXEL

BACKGROUND_COLOR='black'
FOREGROUND_COLOR='white'
PIC_COLOR_TO_NAME:dict[int,str]={
    modules.consts.PIC_COLOR_BLACK:'black',
    modules.consts.PIC_COLOR_PURPLE:'purple',
    modules.consts.PIC_COLOR_ORANGE:'orange',
    modules.consts.PIC_COLOR_BLUE:'blue',
    modules.consts.PIC_COLOR_GREEN:'green',
    modules.consts.PIC_COLOR_WHITE:'white',
}
class drawPicImgSVG:

    _dwg:svgwrite.Drawing # type: ignore
    """描画領域"""
    _outfile_path:str
    """描画ファイルのパス名"""
    _margin_len:int
    """フレーム幅"""
    def __init__(self, outfile:str, frame_len:int=0) -> None:
        """描画処理オブジェクトの初期化

        Args:
            outfile (str): 出力先ファイルへのパス
        """

        # 背景余白の幅
        self._margin_len = frame_len*modules.consts.PIC_LEN_PER_PIXEL

        # ドローイング領域を作成
        self._dwg = svgwrite.Drawing(filename=outfile, # type: ignore
                                     size = (self._margin_len * 2 + modules.consts.PIC_LEN_PER_PIXEL * modules.consts.PIC_WIDTH + OFFSET_SIZE * 2,
                                            self._margin_len * 2 + modules.consts.PIC_LEN_PER_PIXEL * modules.consts.PIC_HEIGHT + OFFSET_SIZE * 2), debug=True)
        self.fill_background()     # 背景を塗りつぶす
        self._outfile_path = outfile # パスを記憶する

        return

    def drawBitMap(self, pic:WizardryPicDataEntry, off_x: int=0, off_y:int=0) -> None:
        """モンスター/宝箱画像を描画する

        Args:
            pic (WizardryPicDataEntry): キャラクタビットマップ情報
        """
        # 配置位置
        offset_x = off_x * modules.consts.PIC_WIDTH
        offset_y = off_x * modules.consts.PIC_HEIGHT
        # 背景余白の幅
        this_margin = self._margin_len

        # 要素のグループを定義
        output_bitmap = self._dwg.add(self._dwg.g(id='picImg')) # type: ignore

        #
        # 余白
        #
        if this_margin > 0:
            frame_sx = modules.consts.PIC_LEN_PER_PIXEL*modules.consts.PIC_WIDTH + OFFSET_SIZE + offset_x
            frame_sy = modules.consts.PIC_LEN_PER_PIXEL*modules.consts.PIC_HEIGHT + OFFSET_SIZE + offset_y

            back_ground_rectangle = self._dwg.rect( # type: ignore
                insert=(frame_sx, frame_sy),
                size=((modules.consts.PIC_LEN_PER_PIXEL + this_margin*2), (modules.consts.PIC_LEN_PER_PIXEL + this_margin*2)),
                fill=BACKGROUND_COLOR)
            output_bitmap.add(back_ground_rectangle) # type: ignore
        for pos in pic.color_info:

            x,y = pos

            sx = this_margin + x*modules.consts.PIC_LEN_PER_PIXEL + OFFSET_SIZE + offset_x
            sy = this_margin + y*modules.consts.PIC_LEN_PER_PIXEL + OFFSET_SIZE + offset_y

            color = pic.color_info[pos]
            if color not in PIC_COLOR_TO_NAME:
                fill = PIC_COLOR_TO_NAME[modules.consts.PIC_COLOR_BLACK]
            else:
                fill = PIC_COLOR_TO_NAME[color]

            rectangle = self._dwg.rect(insert=(sx,sy), # type: ignore
                                    size=((modules.consts.PIC_LEN_PER_PIXEL), (modules.consts.PIC_LEN_PER_PIXEL)),
                                    fill=fill)
            # 描画内容を反映する
            output_bitmap.add(rectangle) # type: ignore

        self._dwg.save() # type: ignore 画像を保存する

        return

    def save(self)->None:
        """画像を保存する
        """
        self._dwg.save() # type: ignore 画像を保存する
        return

    def fill_background(self)->None:
        """背景色を設定する
        """

        # バックグラウンド要素のグループを定義
        back_ground = self._dwg.add(self._dwg.g(id='background', stroke=BACKGROUND_COLOR)) # type: ignore

        # 四角で塗りつぶす
        rectangle = self._dwg.rect(insert=(0, 0), # type: ignore
                                   size=(self._margin_len * 2 + (modules.consts.PIC_WIDTH*modules.consts.PIC_LEN_PER_PIXEL + OFFSET_SIZE*2),
                                         self._margin_len * 2 + (modules.consts.PIC_HEIGHT*modules.consts.PIC_LEN_PER_PIXEL + OFFSET_SIZE*2)),
                                   fill=BACKGROUND_COLOR)
        # 描画内容を反映する
        back_ground.add(rectangle) # type: ignore

        return
