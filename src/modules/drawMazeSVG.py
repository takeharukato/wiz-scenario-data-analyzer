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
from typing import Optional
from typing import Iterator
from collections.abc import Generator

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os
import math

#
# サードパーティーモジュールの読込み
#
import svgwrite # type: ignore
from svgwrite import cm # type: ignore

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import modules.consts

# 座標書き込み用に左2cmあける
OFFSET_SIZE=2
# 1cm単位でセルを切る
CELL_SIZE=1
# 格子の幅
COORD_STROKE_WIDTH=.5
# ドアの壁部分の幅
DOOR_WALL_STROKE_WIDTH=3
# 壁の幅
WALL_STROKE_WIDTH=4
# 矢印の幅
ARROW_STROKE_WIDTH=2
# 壁の幅の1/4分両端を空けて, ドアの矩形, イベント番号を描画する
DOOR_OFFSET=0.25
# セルの20%の幅でドアを描画する
DOOR_THICK=0.2

#
# 上向き矢印
#
# 矢じりの幅
ARROW_WIDTH=0.25
ARROW_HEIGHT=0.25
# 矢じり壁上位部の高さ( セルの1/8 )
ARROW_BASE_HEIGHT=ARROW_HEIGHT/2
# 矢じり壁上位部の幅( セルの1/8 )
ARROW_BASE_WIDTH=ARROW_WIDTH/2
# 矢じりの高さ( 矢印の高さの半分 )
ARROW_TRIANGLE_HEIGHT=ARROW_HEIGHT/2
# 中心から見た矢印の矢じり(三角形)の左隅
ARROW_LEFT_CORNER=(0 - ARROW_BASE_WIDTH*2, 0 - ARROW_BASE_HEIGHT)
# 中心から見た三角形の頂点
ARROW_CENTER_CORNER=(0, 0 - ARROW_BASE_HEIGHT - ARROW_TRIANGLE_HEIGHT)
# 中心から見た矢印の矢じり(三角形)の右隅
ARROW_RIGHT_CORNER=(1 * ARROW_BASE_WIDTH*2, 0 - ARROW_BASE_HEIGHT)
# 中心から見た矢印の矢じりの基底右上
ARROW_RIGHT_BASE_UPPER_RIGHT=(0 + ARROW_BASE_WIDTH, - ARROW_BASE_HEIGHT)
# 中心から見た矢印の矢じりの基底右下
ARROW_RIGHT_BASE_LOWER_RIGHT=(0 + ARROW_BASE_WIDTH, ARROW_BASE_HEIGHT*2)
# 中心から見た矢印の矢じりの基底左下
ARROW_RIGHT_BASE_LOWER_LEFT=(0 - ARROW_BASE_WIDTH, ARROW_BASE_HEIGHT*2)
# 中心から見た矢印の矢じりの基底左上
ARROW_RIGHT_BASE_UPPER_LEFT=(0 - ARROW_BASE_WIDTH, - ARROW_BASE_HEIGHT)
# 矢印の線分
ARROW_SHAPE=(ARROW_LEFT_CORNER, ARROW_CENTER_CORNER, ARROW_RIGHT_CORNER,
             ARROW_RIGHT_BASE_UPPER_RIGHT, ARROW_RIGHT_BASE_LOWER_RIGHT,
             ARROW_RIGHT_BASE_LOWER_LEFT, ARROW_RIGHT_BASE_UPPER_LEFT,
             ARROW_LEFT_CORNER)
#
# 描画色
#
ROOM_COLOR='red'          # 玄室の色
BACKGROUND_COLOR='white'  # 背景色
NORMAL_DOOR_COLOR='white' # 通常ドアの色
HIDDEN_DOOR_COLOR='black' # 隠し扉の色
LINE_COLOR='black'        # 線の色
TEXT_COLOR='black'        # 文字の色

#
# 塗りつぶしの透明度
#
# 玄室を半透明でぬる
ROOM_OPACITY=0.5
# 暗闇を半透明でぬる
DARK_OPACITY=0.2
# 岩を半透明でぬる
ROCK_OPACITY=0.2

# 文字のスケール
TEXT_SCALE_FACTOR=0.4

#
# 壁描画種別
#
LINE_TYPE_COORD=0 # 格子
LINE_TYPE_WALL=1  # 壁
LINE_TYPE_DOOR=2  # ドア
#
# 線分描画カテゴリ
#
LINE_STYLE_SOLID=1 # 実線
LINE_STYLE_DASH=2  # 破線

# 壁描画の種別一覧
LINE_TYPES=(LINE_TYPE_COORD,LINE_TYPE_WALL,LINE_TYPE_DOOR)

#
# 壁を描画する向き
#
DRAW_MAZE_DIR_NORTH=modules.consts.DIR_NORTH  # 北側(上)
DRAW_MAZE_DIR_EAST=modules.consts.DIR_EAST    # 東側(右)
DRAW_MAZE_DIR_SOUTH=modules.consts.DIR_SOUTH  # 南側(下)
DRAW_MAZE_DIR_WEST=modules.consts.DIR_WEST    # 西側(左)
DRAW_MAZE_DIR_VALID=(DRAW_MAZE_DIR_NORTH, DRAW_MAZE_DIR_EAST, DRAW_MAZE_DIR_SOUTH, DRAW_MAZE_DIR_WEST)
DRAW_MAZE_DIR_TO_DEGREE:dict[int,int]={
    DRAW_MAZE_DIR_NORTH:0,   #  上 (0度)
    DRAW_MAZE_DIR_EAST:90,   #  右 (90度)
    DRAW_MAZE_DIR_SOUTH:180, #  下 (180度)
    DRAW_MAZE_DIR_WEST:270   #  下 (270度)
}

class drawMazeSVG:

    _dwg:svgwrite.Drawing # type: ignore
    """描画領域"""
    _outfile_path:str
    """描画ファイルのパス名"""

    def __init__(self, outfile:str, draw_coordinate: bool=True) -> None:
        """描画処理オブジェクトの初期化

        Args:
            outfile (str): 出力先ファイルへのパス
            draw_coordinate (bool, optional): 格子を描画する. Defaults to True.
        """
        # ドローイング領域を作成
        self._dwg = svgwrite.Drawing(filename=outfile, # type: ignore
                                    size = (f"{modules.consts.FLOOR_WIDTH+OFFSET_SIZE*2}cm",
                                            f"{modules.consts.FLOOR_HEIGHT+OFFSET_SIZE*2}cm"),
                                    debug=True)

        self.fill_background()     # 背景を塗りつぶす
        self.fill_position_mark()  # 座標を書き込む

        if draw_coordinate:        # 格子の描画指示がある場合
            self.fill_coordinate() # 格子を描く

        self._outfile_path = outfile # パスを記憶する

        return

    def getDrawCoord(self, x:int, y:int, width:int=modules.consts.FLOOR_WIDTH, height:int=modules.consts.FLOOR_HEIGHT)->tuple[int,int]:
        """マップ座標を描画座標に変換する

        Args:
            x (int): マップX座標
            y (int): マップY座標
            width (int, optional): フロアの幅. Defaults to modules.consts.FLOOR_WIDTH.
            height (int, optional): フロアの高さ. Defaults to modules.consts.FLOOR_HEIGHT.

        Returns:
            tuple[int,int]: (描画座標X,描画座標Y)のタプル
        """
        # 描画領域の最下端にY軸のy=0がくるように変換する
        return x, height - 1 - y

    def addLine(self, x:int, y:int, dir:int, line_type:int=LINE_TYPE_COORD, line_style:int=LINE_STYLE_SOLID)->None:
        """壁, ドア, マップ格子で使用する線分描画処理

        Args:
            x (int): X座標
            y (int): Y座標
            dir (int): 壁の線分を描画する位置
                - DRAW_MAZE_DIR_NORTH 北側の壁の位置
                - DRAW_MAZE_DIR_EAST  東側の壁の位置
                - DRAW_MAZE_DIR_SOUTH 南側の壁の位置
                - DRAW_MAZE_DIR_WEST  西側の壁の位置
            line_type (int, optional): 描画する線分種別. Defaults to LINE_TYPE_COORD.
                - LINE_TYPE_COORD 格子
                - LINE_TYPE_WALL  壁
                - LINE_TYPE_DOOR  ドア
        """

        if dir not in DRAW_MAZE_DIR_VALID: # 不正な向きの場合
            return # 何もせず戻る

        #
        # 線の幅を設定する
        #
        if line_type == LINE_TYPE_WALL: # 壁の場合
            stroke_width = WALL_STROKE_WIDTH
        elif line_type == LINE_TYPE_DOOR: # ドアの場合
            stroke_width = DOOR_WALL_STROKE_WIDTH
        else: # それ以外の場合, 格子の幅とする
            stroke_width = COORD_STROKE_WIDTH

        # 描画グループを生成
        lines = self._dwg.add(self._dwg.g(id='lines', stroke=LINE_COLOR, stroke_width=stroke_width)) # type: ignore

        dx,dy = self.getDrawCoord(x=x, y=y) # 座標変換

        sx,sy,ex,ey=dx,dy,dx,dy # 線分の座標を初期化
        if dir == DRAW_MAZE_DIR_NORTH:   # 北側の壁の位置に描画する場合

            sx = dx     # 左上の座標から
            sy = dy
            ex = dx + 1 # 右上の座標まで水平線を引く
            ey = dy

        elif dir == DRAW_MAZE_DIR_SOUTH: # 南側の壁の位置に描画する場合

            sx = dx     # 一つ下の座標の左上から
            sy = dy + 1
            ex = dx + 1 # 一つ下の座標の右上まで水平線を引く
            ey = dy + 1

        elif dir == DRAW_MAZE_DIR_EAST:  # 東側の壁の位置に描画する場合

            sx = dx + 1 # 右上から
            sy = dy
            ex = dx + 1 # 右下まで垂直線を引く
            ey = dy + 1

        elif dir == DRAW_MAZE_DIR_WEST:  # 西側の壁の位置に描画する場合

            sx = dx     # 左上の座標から
            sy = dy
            ex = dx     # 左下の座標まで垂直線を引く
            ey = dy + 1

        if line_style == LINE_STYLE_DASH:
            line_unit=CELL_SIZE / 8
            if dir in [DRAW_MAZE_DIR_NORTH,DRAW_MAZE_DIR_SOUTH]:
                # 水平線
                last_x=sx
                count=0
                while ex > last_x:
                    count += 1
                    next_x=min(ex,last_x + line_unit)
                    if count % 2:
                        # 線分を描画する
                        line = self._dwg.line(start=((OFFSET_SIZE + last_x)*cm, (OFFSET_SIZE + sy) * cm),  # type: ignore
                                        end=((OFFSET_SIZE + next_x)*cm, (OFFSET_SIZE + ey) * cm))
                        # 描画した線分を反映
                        lines.add(line) # type: ignore
                    last_x = next_x
            else:
                # 垂直線
                last_y=sy
                count=0
                while ey > last_y:
                    count += 1
                    next_y=min(ey,last_y + line_unit)
                    if count % 2:
                        # 線分を描画する
                        line = self._dwg.line(start=((OFFSET_SIZE + sx)*cm, (OFFSET_SIZE + last_y) * cm),  # type: ignore
                                        end=((OFFSET_SIZE + ex)*cm, (OFFSET_SIZE + next_y) * cm))
                        # 描画した線分を反映
                        lines.add(line) # type: ignore
                    last_y = next_y

        else:
            # 線分を描画する
            line = self._dwg.line(start=((OFFSET_SIZE + sx)*cm, (OFFSET_SIZE + sy) * cm),  # type: ignore
                              end=((OFFSET_SIZE + ex)*cm, (OFFSET_SIZE + ey) * cm))
            # 描画した線分を反映
            lines.add(line) # type: ignore

        return

    def arrowShape(self)->Iterator[tuple[tuple[float,float],tuple[float,float]]]:
        """中心を0,0とした矢印を描く線分のイテレータを返す

        Yields:
            Iterator[tuple[tuple[float,float],tuple[float,float]]]: 矢印の線分
        """
        def arrowShapeGenerator()->Generator[tuple[tuple[float,float],tuple[float,float]],None,None]:
            """中心を0,0とした矢印を描く線分を生成"""
            for idx in range(len(ARROW_SHAPE) - 1):
                yield ARROW_SHAPE[idx],ARROW_SHAPE[idx+1]
            return
        return arrowShapeGenerator()

    def rotatePosition(self, degree:float, multi:int, x:float, y:float)->tuple[float,float]:
        nx = x * multi * math.cos(math.radians(degree)) - y * multi * math.sin(math.radians(degree))
        ny = x * multi * math.sin(math.radians(degree)) + y * multi * math.cos(math.radians(degree))
        return nx, ny

    def movePosition(self, x:float, y:float, vx:float, vy:float)->tuple[float,float]:
        return x + vx, y + vy
    def getPathPoint(self, x:float, y:float, degree:float, vx:float,vy:float)-> tuple[float, float]:
        dx,dy = self.rotatePosition(degree=degree, multi=CELL_SIZE, x=x, y=y)
        dx,dy = self.movePosition(x=dx,y=dy,vx=vx,vy=vy)
        return dx, dy
    def getArrowOffset(self, pos:int)->tuple[float,float]:
        """矢印を配置する場所を設定する

        Args:
            pos (int): 場所指定
                - DRAW_MAZE_DIR_NORTH 北側の壁に設置する
                - DRAW_MAZE_DIR_SOUTH 南側の壁に設置する
                - DRAW_MAZE_DIR_WEST  西側の壁に設置する
                - DRAW_MAZE_DIR_WEST  東の壁に設置する
        Returns:
            tuple[float,float]: _description_
        """
        if pos == DRAW_MAZE_DIR_NORTH:
            return CELL_SIZE / 2, 0
        elif pos == DRAW_MAZE_DIR_SOUTH:
            return CELL_SIZE / 2, CELL_SIZE
        elif pos == DRAW_MAZE_DIR_WEST:
            return 0, CELL_SIZE / 2
        else:
            return CELL_SIZE, CELL_SIZE / 2

    def addArrow(self, x:int, y:int, dir:int, pos:int, fill: Optional[str]=None)->None:

        # 矢印の向きを決定する
        degree = DRAW_MAZE_DIR_TO_DEGREE[dir] if dir in DRAW_MAZE_DIR_TO_DEGREE else 0

        # 描画グループを生成
        arrow = self._dwg.add(self._dwg.g(id='arrow', stroke=LINE_COLOR, stroke_width=ARROW_STROKE_WIDTH)) # type: ignore

        dx,dy = self.getDrawCoord(x=x, y=y)      # 座標変換

        # 設置位置(東西南北)に応じて中心位置を移動
        off_x, off_y = self.getArrowOffset(pos=pos)
        mx = dx + off_x
        my = dy + off_y

        point_list = list(self.arrowShape())       # (一筆書き可能な)線分
        for start,end in point_list:

            sx,sy=self.rotatePosition(degree=degree, multi=CELL_SIZE, x=start[0], y=start[1])
            sx,sy = self.movePosition(x=sx,y=sy,vx=mx,vy=my)

            ex,ey=self.rotatePosition(degree=degree, multi=CELL_SIZE, x=end[0], y=end[1])
            ex,ey = self.movePosition(x=ex,y=ey,vx=mx,vy=my)

            #print(f"({start[0]},{start[1]})-({end[0]}, {end[1]}) => ({sx},{sy})-({ex},{ey})")

            # 線分を描画する
            line = self._dwg.line(start=((OFFSET_SIZE + sx)*cm, (OFFSET_SIZE + sy) * cm),  # type: ignore
                                end=((OFFSET_SIZE + ex)*cm, (OFFSET_SIZE + ey) * cm))

            # 描画した線分を反映
            arrow.add(line) # type: ignore

        return

    def addWall(self, x:int, y:int, dir:int)->None:
        """壁を描画する

        Args:
            x (int): X座標
            y (int): Y座標
            dir (int): 壁の線分を描画する位置
        """

        # 壁を指定して, 線分を描画する
        self.addLine(x=x,y=y,dir=dir,line_type=LINE_TYPE_WALL)
        return

    def addDoor(self, x:int, y:int, dir:int, hidden: bool=False)->None:

        # 描画グループを生成
        door_grp = self._dwg.add(self._dwg.g(id='lines', stroke=LINE_COLOR,     # type: ignore
                                             stroke_width=COORD_STROKE_WIDTH))  # type: ignore

        dx,dy = self.getDrawCoord(x=x, y=y)      # 座標変換
        sx,sy,door_width,door_height=dx,dy,dx,dy # 矩形座標を初期化

        # 通常の扉とシークレットドアとで描画する色を変更
        fill_param = HIDDEN_DOOR_COLOR if hidden else NORMAL_DOOR_COLOR

        if dir == DRAW_MAZE_DIR_NORTH: # 北側のドア

            # 壁の下側に小さい四角を描く
            sx = dx + DOOR_OFFSET*CELL_SIZE
            sy = dy
            door_width = CELL_SIZE - DOOR_OFFSET * 2
            door_height = DOOR_THICK*CELL_SIZE

        elif dir == DRAW_MAZE_DIR_SOUTH: # 南側のドア

            # 壁の上側に小さい四角を描く
            sx = dx + DOOR_OFFSET*CELL_SIZE
            sy = dy + 1 - DOOR_THICK*CELL_SIZE
            door_width = CELL_SIZE - DOOR_OFFSET * 2
            door_height = DOOR_THICK*CELL_SIZE

        elif dir == DRAW_MAZE_DIR_EAST: # 東側のドア

            # 壁の左側に小さい四角を描く
            sx = dx + 1 - DOOR_THICK*CELL_SIZE
            sy = dy + DOOR_OFFSET*CELL_SIZE
            door_width = DOOR_THICK * CELL_SIZE
            door_height = CELL_SIZE - DOOR_OFFSET * 2

        elif dir == DRAW_MAZE_DIR_WEST: # 西側のドア

            # 壁の右側に小さい四角を描く
            sx = dx
            sy = dy + DOOR_OFFSET*CELL_SIZE
            door_width = DOOR_THICK * CELL_SIZE
            door_height = CELL_SIZE - DOOR_OFFSET * 2

        # 矩形を描画する
        door=self._dwg.rect(insert=((OFFSET_SIZE + sx) * cm, (OFFSET_SIZE + sy) * cm), # type: ignore
            size=( door_width * cm, door_height * cm ), fill=fill_param)

        # 描画した矩形を反映
        door_grp.add(door) # type: ignore

        # ドアの位置に壁を描画し, ドアの描画を完成させる
        self.addLine(x=x,y=y,dir=dir,line_type=LINE_TYPE_DOOR)

        return

    def addRoom(self, x:int, y:int)->None:
        """指定された座標を玄室として色づけする

        Args:
            x (int): X座標
            y (int): Y座標
        """

        # 描画グループを生成
        room_grp = self._dwg.add(self._dwg.g(id='lines', stroke=LINE_COLOR, stroke_width=0)) # type: ignore

        dx,dy = self.getDrawCoord(x=x, y=y) # 座標変換
        fill_param = ROOM_COLOR             # 玄室の色で塗りつぶす

        # 玄室として指定された座標のセルを塗りつぶす
        room=self._dwg.rect(insert=((OFFSET_SIZE + dx * CELL_SIZE) * cm, (OFFSET_SIZE + dy * CELL_SIZE) * cm), # type: ignore
            size=( CELL_SIZE * cm, CELL_SIZE * cm ),
            fill=fill_param, opacity=ROOM_OPACITY)

        # 描画を反映
        room_grp.add(room) # type: ignore

        return

    def addEventNumber(self, x:int, y:int, event_number:int)->None:
        """イベント番号を書込む

        Args:
            x (int): X座標
            y (int): Y座標
            event_number (int): イベント番号(3桁以上のイベント番号が渡された場合は, 下2桁を表示)
        """

        # イベント番号テキストのグループを生成
        event_num_grp = self._dwg.add(self._dwg.g(id='lines', stroke=TEXT_COLOR, stroke_width=0)) # type: ignore

        dx,dy = self.getDrawCoord(x=x, y=y) # 座標変換し, 対象マップ座標の左上の描画座標を得る
        dx,dy = dx, dy + 1                  # 左下の描画座標を開始座標として文字を書き込む
        this_number = event_number % 100    # イベント番号下2桁を取得

        #
        # イベント番号文字列を描画
        #

        text = svgwrite.text.Text(f'{this_number:02}', # type: ignore
                insert=((OFFSET_SIZE + dx * CELL_SIZE + DOOR_OFFSET * CELL_SIZE ) * cm,
                        (OFFSET_SIZE + dy * CELL_SIZE - DOOR_OFFSET * CELL_SIZE ) * cm),
                fill=TEXT_COLOR) # 文字列を設定
        text['font-size'] = f'{CELL_SIZE*TEXT_SCALE_FACTOR}cm' # 文字サイズを調整
        text['font-family'] = modules.consts.FONT_FACES[0]     # フォントを設定

        event_num_grp.add(text) # type:ignore 文字列を反映

        return

    #
    # 初期化関連
    #
    def fill_coordinate(self, width:int=modules.consts.FLOOR_WIDTH, height:int=modules.consts.FLOOR_HEIGHT)->None:
        """マップの格子を描画する

        Args:
            width (int, optional): フロアの幅. Defaults to modules.consts.FLOOR_WIDTH.
            height (int, optional): フロアの高さ. Defaults to modules.consts.FLOOR_HEIGHT.
        """

        for x in range(width): # X座標について
            for y in range(height): # Y座標について
                for dir in [DRAW_MAZE_DIR_NORTH,DRAW_MAZE_DIR_EAST,DRAW_MAZE_DIR_SOUTH,DRAW_MAZE_DIR_WEST]: # 全ての向きについて
                    self.addLine(x=x, y=y, dir=dir, line_type=LINE_TYPE_COORD, line_style=LINE_STYLE_DASH) # 格子描画幅で壁を書き込む

        return

    def fill_position_mark(self, width:int=modules.consts.FLOOR_WIDTH, height:int=modules.consts.FLOOR_HEIGHT)->None:
        """座標に目盛を書き込む

        Args:
            width (int, optional): フロアの幅. Defaults to modules.consts.FLOOR_WIDTH.
            height (int, optional): フロアの高さ. Defaults to modules.consts.FLOOR_HEIGHT.
        """

        for x in range(width):
                #
                # X軸の目盛を書き込む
                #
                text = svgwrite.text.Text(f'{x:02}', # type: ignore
                        insert=( ( OFFSET_SIZE + x * CELL_SIZE + CELL_SIZE * DOOR_OFFSET ) * cm,
                                (OFFSET_SIZE + (height + 1) * CELL_SIZE - CELL_SIZE * DOOR_OFFSET ) * cm ,), # Y=0の一つ下の位置に書き込む
                        fill=TEXT_COLOR) # テキストを得る
                text['font-size'] = f'{CELL_SIZE*TEXT_SCALE_FACTOR}cm'  # 文字サイズを調整する
                text['font-family'] = modules.consts.FONT_FACES[0]      # フォントを選択する

                # 書き込んだ文字列を反映する
                self._dwg.add(text) # type: ignore

        for y in range(height):
                #
                # Y軸の目盛を書き込む
                #

                dx = 0
                dy = height - y # 座標0が最下点に来るように描画座標を変換
                text = svgwrite.text.Text(f'{y:02}', # type: ignore
                        insert=( (dx + CELL_SIZE * DOOR_OFFSET ) * cm,
                                (OFFSET_SIZE + ( CELL_SIZE * dy - CELL_SIZE * DOOR_OFFSET ) ) * cm ,),
                        fill=TEXT_COLOR) # テキストを得る
                text['font-size'] = f'{ CELL_SIZE * TEXT_SCALE_FACTOR}cm' # 文字サイズを調整する
                text['font-family'] = modules.consts.FONT_FACES[0]     # フォントを選択する
                self._dwg.add(text) # type: ignore 書き込んだ文字列を反映する

        return

    def fill_background(self)->None:
        """背景色を設定する
        """

        # バックグラウンド要素のグループを定義
        back_ground = self._dwg.add(self._dwg.g(id='background', stroke=BACKGROUND_COLOR)) # type: ignore

        # 角を丸めて四角で塗りつぶす
        rectangle = self._dwg.rect(insert=(0, 0), # type: ignore
                                   size=((modules.consts.FLOOR_WIDTH+OFFSET_SIZE*2)*cm,
                                         (modules.consts.FLOOR_HEIGHT+OFFSET_SIZE*2)*cm),
                                   rx=10, ry=10, fill=BACKGROUND_COLOR)
        # 描画内容を反映する
        back_ground.add(rectangle) # type: ignore

        return

    def save(self)->None:
        """ファイルに保存する
        """

        self._dwg.save() # type: ignore 画像を保存する
        return

    @property
    def outfile(self)->str:
        """出力先ファイルへのパス
        """
        return self._outfile_path

if __name__ == '__main__':

    draw=drawMazeSVG(outfile='test.svg')

    draw.addWall(x=0,y=0,dir=DRAW_MAZE_DIR_NORTH)
    draw.addWall(x=2,y=2,dir=DRAW_MAZE_DIR_SOUTH)
    draw.addWall(x=3,y=3,dir=DRAW_MAZE_DIR_EAST)
    draw.addWall(x=4,y=4,dir=DRAW_MAZE_DIR_WEST)
    draw.addDoor(x=5,y=5,dir=DRAW_MAZE_DIR_NORTH)
    draw.addDoor(x=5,y=6,dir=DRAW_MAZE_DIR_NORTH,hidden=True)
    draw.addDoor(x=5,y=6,dir=DRAW_MAZE_DIR_SOUTH)
    draw.addDoor(x=5,y=6,dir=DRAW_MAZE_DIR_EAST)
    draw.addDoor(x=5,y=6,dir=DRAW_MAZE_DIR_WEST)
    draw.addRoom(x=6,y=6)
    draw.addEventNumber(x=7,y=7,event_number=15)
    draw.addArrow(x=8,y=8,  pos=DRAW_MAZE_DIR_NORTH, dir=DRAW_MAZE_DIR_SOUTH)
    draw.addArrow(x=8,y=9,  pos=DRAW_MAZE_DIR_EAST, dir=DRAW_MAZE_DIR_WEST)
    draw.addArrow(x=8,y=10, pos=DRAW_MAZE_DIR_WEST, dir=DRAW_MAZE_DIR_EAST)
    draw.addArrow(x=8,y=11, pos=DRAW_MAZE_DIR_SOUTH, dir=DRAW_MAZE_DIR_NORTH)
    draw.save()
    pass