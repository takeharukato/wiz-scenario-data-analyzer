#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file drawMaze.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief データクラス定義
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details データクラス定義

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
from typing import Any,Optional
from typing import Callable

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
import svgwrite
from svgwrite import cm

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import modules.consts

# 2cm単位でセルを切る
CELL_SIZE=2
WALL_STROKE_WIDTH=3
ROOM_OPACITY=0.5 # 玄室を半透明でぬる
DARK_OPACITY=0.2 # 暗闇を半透明でぬる
BLOCK_OPACITY=0.2 # 暗闇を半透明でぬる

DRAW_MAZE_DIR_NORTH=0
DRAW_MAZE_DIR_EAST=1
DRAW_MAZE_DIR_SOUTH=2
DRAW_MAZE_DIR_WEST=3

class drawMaze:

    _dwg:svgwrite.Drawing
    def __init__(self, outfile:str) -> None:

        # ドローイング領域を作成
        self._dwg = svgwrite.Drawing(filename=outfile, size = ("24cm", "24cm"), debug=True)
        return

    def fill_coordinate(self, width:int=modules.consts.FLOOR_WIDTH, height:int=modules.consts.FLOOR_HEIGHT)->None:

        hlines = self._dwg.add(self._dwg.g(id='hlines', stroke='black'))
        for y in range(height+1):
            hlines.add(self._dwg.line(start=(CELL_SIZE*cm, (CELL_SIZE+y)*cm), end=((height + CELL_SIZE)*cm, (CELL_SIZE+y)*cm)))
        vlines = self._dwg.add(self._dwg.g(id='vline', stroke='black'))
        for x in range(width+1):
            vlines.add(self._dwg.line(start=((CELL_SIZE+x)*cm, CELL_SIZE*cm), end=((CELL_SIZE+x)*cm, (width+CELL_SIZE)*cm)))

        return
    def addWall(self, x:int, y:int, dir:int)->None:
        wall_lines = self._dwg.add(self._dwg.g(id='wall', stroke='black', stroke_width=WALL_STROKE_WIDTH))
        dx = x
        dy = modules.consts.FLOOR_HEIGHT - 1 - y
        if dir == DRAW_MAZE_DIR_NORTH:
            line = self._dwg.line(start=((CELL_SIZE+x)*cm, (CELL_SIZE + dy ) * cm), end=((CELL_SIZE+x+1)*cm, (CELL_SIZE + dy ) * cm))
        elif dir == DRAW_MAZE_DIR_SOUTH:
            line = self._dwg.line(start=((CELL_SIZE+x)*cm, (CELL_SIZE + dy + 1) * cm), end=((CELL_SIZE+x+1)*cm, (CELL_SIZE + dy + 1 ) * cm))
        elif dir == DRAW_MAZE_DIR_EAST:
            line = self._dwg.line(start=((CELL_SIZE + dx + 1)*cm, (CELL_SIZE + dy) * cm), end=((CELL_SIZE + dx + 1)*cm, (CELL_SIZE + dy + 1) * cm))
        elif dir == DRAW_MAZE_DIR_WEST:
            line = self._dwg.line(start=((CELL_SIZE + dx)*cm, (CELL_SIZE + dy) * cm), end=((CELL_SIZE + dx)*cm, (CELL_SIZE + dy + 1) * cm))

        wall_lines.add(line)

        return
    def save(self)->None:
        self._dwg.save()
        return

if __name__ == '__main__':
    draw=drawMaze(outfile='test.svg')

    draw.fill_coordinate()

    draw.addWall(x=0,y=0,dir=DRAW_MAZE_DIR_NORTH)
    draw.addWall(x=1,y=2,dir=DRAW_MAZE_DIR_SOUTH)
    draw.addWall(x=2,y=2,dir=DRAW_MAZE_DIR_EAST)
    draw.addWall(x=4,y=4,dir=DRAW_MAZE_DIR_WEST)
    draw.save()
    pass