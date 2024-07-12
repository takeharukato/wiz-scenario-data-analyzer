#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file drawMazeSVG.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief SVG迷宮描画実装部
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details SVG迷宮描画実装部

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
import svgwrite
from svgwrite import cm

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import modules.consts

# 2cm単位でセルを切る
OFFSET_SIZE=2
CELL_SIZE=1
COORD_STROKE_WIDTH=1
DOOR_WALL_STROKE_WIDTH=3
WALL_STROKE_WIDTH=4
DOOR_OFFSET=0.25
DOOR_THICK=0.2

ROOM_OPACITY=0.5 # 玄室を半透明でぬる
DARK_OPACITY=0.2 # 暗闇を半透明でぬる
BLOCK_OPACITY=0.2 # 暗闇を半透明でぬる

LINE_TYPE_COORD=0
LINE_TYPE_WALL=1
LINE_TYPE_DOOR=2
LINE_TYPES=(LINE_TYPE_COORD,LINE_TYPE_WALL,LINE_TYPE_DOOR)

DRAW_MAZE_DIR_NORTH=modules.consts.DIR_NORTH
DRAW_MAZE_DIR_EAST=modules.consts.DIR_EAST
DRAW_MAZE_DIR_SOUTH=modules.consts.DIR_SOUTH
DRAW_MAZE_DIR_WEST=modules.consts.DIR_WEST

class drawMazeSVG:

    _dwg:svgwrite.Drawing
    def __init__(self, outfile:str, draw_coordinate: bool=True) -> None:

        # ドローイング領域を作成
        self._dwg = svgwrite.Drawing(filename=outfile, size = (f"{modules.consts.FLOOR_WIDTH+OFFSET_SIZE*2}cm", f"{modules.consts.FLOOR_HEIGHT+OFFSET_SIZE*2}cm"), debug=True)
        self.fill_background() # 背景を塗りつぶす
        if draw_coordinate:
            self.fill_coordinate() # 格子を描く
        return

    def addLine(self, x:int, y:int, dir:int, line_type:int=LINE_TYPE_COORD)->None:

        if line_type not in LINE_TYPES:
            line_type = LINE_TYPE_COORD

        if line_type == LINE_TYPE_COORD:
            stroke_width = COORD_STROKE_WIDTH
        elif line_type == LINE_TYPE_DOOR:
            stroke_width = DOOR_WALL_STROKE_WIDTH
        else:
            stroke_width = WALL_STROKE_WIDTH

        lines = self._dwg.add(self._dwg.g(id='lines', stroke='black', stroke_width=stroke_width))

        dx = x
        dy = modules.consts.FLOOR_HEIGHT - 1 - y

        if dir == DRAW_MAZE_DIR_NORTH:
            sx = dx
            sy = dy
            ex = dx + 1
            ey = dy
            #line = self._dwg.line(start=((OFFSET_SIZE+dx)*cm, (OFFSET_SIZE + dy ) * cm), end=((OFFSET_SIZE+dx+1)*cm, (OFFSET_SIZE + dy ) * cm))
            line = self._dwg.line(start=((OFFSET_SIZE + sx)*cm, (OFFSET_SIZE + sy) * cm), end=((OFFSET_SIZE + ex)*cm, (OFFSET_SIZE + ey) * cm))
        elif dir == DRAW_MAZE_DIR_SOUTH:
            sx = dx
            sy = dy + 1
            ex = dx + 1
            ey = dy + 1
            #line = self._dwg.line(start=((OFFSET_SIZE+dx)*cm, (OFFSET_SIZE + dy + 1) * cm), end=((OFFSET_SIZE+dx+1)*cm, (OFFSET_SIZE + dy + 1 ) * cm))
            line = self._dwg.line(start=((OFFSET_SIZE + sx)*cm, (OFFSET_SIZE + sy) * cm), end=((OFFSET_SIZE + ex)*cm, (OFFSET_SIZE + ey) * cm))
        elif dir == DRAW_MAZE_DIR_EAST:
            sx = dx + 1
            sy = dy
            ex = dx + 1
            ey = dy + 1
            line = self._dwg.line(start=((OFFSET_SIZE + sx)*cm, (OFFSET_SIZE + sy) * cm), end=((OFFSET_SIZE + ex)*cm, (OFFSET_SIZE + ey) * cm))
        elif dir == DRAW_MAZE_DIR_WEST:
            sx = dx
            sy = dy
            ex = dx
            ey = dy + 1

            line = self._dwg.line(start=((OFFSET_SIZE + sx)*cm, (OFFSET_SIZE + sy) * cm), end=((OFFSET_SIZE + ex)*cm, (OFFSET_SIZE + ey) * cm))

        lines.add(line)

        return

    def addWall(self, x:int, y:int, dir:int)->None:
        self.addLine(x=x,y=y,dir=dir,line_type=LINE_TYPE_WALL)
        return

    def addDoor(self, x:int, y:int, dir:int, hidden: bool=False)->None:

        #self.addWall(x=x, y=y, dir=dir) # 壁を書く

        door_grp = self._dwg.add(self._dwg.g(id='lines', stroke='black', stroke_width=COORD_STROKE_WIDTH))

        dx = x
        dy = modules.consts.FLOOR_HEIGHT - 1 - y
        fill_param = 'black' if hidden else 'white'
        if dir == DRAW_MAZE_DIR_NORTH:

            # 壁の下側に小さい四角を描く
            sx = dx + DOOR_OFFSET*CELL_SIZE
            sy = dy
            door=self._dwg.rect(insert=((OFFSET_SIZE + sx) * cm, (OFFSET_SIZE + sy) * cm),
                size=( (CELL_SIZE - DOOR_OFFSET * 2) * cm, DOOR_THICK*CELL_SIZE * cm ),
                fill=fill_param)
            pass
        elif dir == DRAW_MAZE_DIR_SOUTH:

            # 壁の上側に小さい四角を描く
            sx = dx + DOOR_OFFSET*CELL_SIZE
            sy = dy + 1 - DOOR_THICK*CELL_SIZE

            door=self._dwg.rect(insert=((OFFSET_SIZE + sx) * cm, (OFFSET_SIZE + sy) * cm),
                size=( (CELL_SIZE - DOOR_OFFSET * 2) * cm, DOOR_THICK*CELL_SIZE * cm ),
                fill=fill_param)

            pass
        elif dir == DRAW_MAZE_DIR_EAST:

            # 壁の左側に小さい四角を描く
            sx = dx + 1 - DOOR_THICK*CELL_SIZE
            sy = dy + DOOR_OFFSET*CELL_SIZE
            door=self._dwg.rect(insert=((OFFSET_SIZE + sx) * cm, (OFFSET_SIZE + sy) * cm),
                size=( DOOR_THICK * CELL_SIZE * cm, (CELL_SIZE - DOOR_OFFSET * 2) * cm ),
                fill=fill_param)

            pass

        elif dir == DRAW_MAZE_DIR_WEST:

            # 壁の右側に小さい四角を描く
            sx = dx
            sy = dy + DOOR_OFFSET*CELL_SIZE
            door=self._dwg.rect(insert=((OFFSET_SIZE + sx) * cm, (OFFSET_SIZE + sy) * cm),
                size=( DOOR_THICK * CELL_SIZE * cm, (CELL_SIZE - DOOR_OFFSET * 2) * cm ),
                fill=fill_param)
            # 壁を描く
            # line = self._dwg.line(start=((OFFSET_SIZE + dx)*cm, (OFFSET_SIZE + dy) * cm), end=((OFFSET_SIZE + dx)*cm, (OFFSET_SIZE + dy + 1) * cm))
            pass

        door_grp.add(door)
        self.addLine(x=x,y=y,dir=dir,line_type=LINE_TYPE_DOOR)
        return

    #
    # 初期化関連
    #
    def fill_coordinate(self, width:int=modules.consts.FLOOR_WIDTH, height:int=modules.consts.FLOOR_HEIGHT)->None:

        for x in range(width):
            for y in range(height):
                for dir in [DRAW_MAZE_DIR_NORTH,DRAW_MAZE_DIR_EAST,DRAW_MAZE_DIR_SOUTH,DRAW_MAZE_DIR_WEST]:
                    self.addLine(x=x, y=y, dir=dir, line_type=LINE_TYPE_COORD)
        return

    def fill_background(self)->None:
        back_ground = self._dwg.add(self._dwg.g(id='back', stroke='white'))
        rectangle = self._dwg.rect(insert=(0, 0),
                                   size=((modules.consts.FLOOR_WIDTH+OFFSET_SIZE*2)*cm, (modules.consts.FLOOR_HEIGHT+OFFSET_SIZE*2)*cm),
                                   rx=10, ry=10, fill='white')
        back_ground.add(rectangle)
        return

    def save(self)->None:
        self._dwg.save()
        return

if __name__ == '__main__':

    draw=drawMazeSVG(outfile='test.svg')

    draw.addWall(x=0,y=0,dir=DRAW_MAZE_DIR_NORTH)
    draw.addWall(x=2,y=2,dir=DRAW_MAZE_DIR_SOUTH)
    draw.addWall(x=3,y=3,dir=DRAW_MAZE_DIR_EAST)
    draw.addWall(x=4,y=4,dir=DRAW_MAZE_DIR_WEST)
    draw.addDoor(x=5,y=5,dir=DRAW_MAZE_DIR_NORTH)
    draw.addDoor(x=5,y=6,dir=DRAW_MAZE_DIR_SOUTH)
    draw.addDoor(x=5,y=6,dir=DRAW_MAZE_DIR_EAST)
    draw.addDoor(x=5,y=6,dir=DRAW_MAZE_DIR_WEST)
    draw.save()
    pass