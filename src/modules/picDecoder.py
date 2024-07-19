#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file picDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の画像データを解析する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の画像データを解析する

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
from typing import Any,Optional

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os
import struct

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.dataEntryDecoder import dataEntryDecoder
from modules.datadef import WizardrySCNTOC, WizardryPicDataEntry
import modules.consts

"""画像データのPascal定義
レコード型データ構造としては定義なし,
1画像番号あたり512バイト(以下参照)
            ENEMYPIC( GETREC( ZSPCCHRS, BATTLERC[ 1].B.PIC, 512));
1行70ピクセルの情報を10バイトで, 表現
1画像あたり50行(500バイト)
"""

# 画像イメージ1行当たりのバイト数 (1行70ピクセル)
PIC_BYTE_PER_LINE=(modules.consts.PIC_WIDTH // modules.consts.PIXEL_PER_BYTE)

# 色1のピクセル (色選択ビット0のとき, 緑, 色選択ビット1のとき, 橙 のピクセル (X=0ピクセルからX=6ピクセルまで))
APPLE_BIT_PTN1=0b1010101
# 色2のピクセル (色選択ビット0のとき, 紫, 色選択ビット1のとき, 青 (X=0ピクセルからX=6ピクセルまで))
APPLE_BIT_PTN2=0b0101010
# 色選択ビット
APPLE_COLOR_DECISION_BIT=0x80

# 色選択ビット0のときの表示色 (緑,紫)
COLOR_PAIR1=(modules.consts.PIC_COLOR_GREEN,modules.consts.PIC_COLOR_PURPLE)
# 色選択ビット1のときの表示色 (橙,青)
COLOR_PAIR2=(modules.consts.PIC_COLOR_ORANGE,modules.consts.PIC_COLOR_BLUE)

# ビデオRAM上に書き込む色(白は, 紫と緑(色選択ビット0のとき), 青と橙(色選択ビットが1のとき)の組み合わせで表示)
COLORED_PIXEL=(modules.consts.PIC_COLOR_BLUE,modules.consts.PIC_COLOR_GREEN,
            modules.consts.PIC_COLOR_ORANGE, modules.consts.PIC_COLOR_PURPLE)

class picDecoder(dataEntryDecoder):
    """画像イメージデコーダ"""

    def _dumpColorInfo(self, bitmap:dict[tuple[int,int],int])->None:
        """解析したピクセルを文字表示する

        Args:
            bitmap (dict[tuple[int,int],int]): ビットマップの座標から色情報への辞書
        """
        for line in range(modules.consts.PIC_HEIGHT): # 各行について
            for x in range(modules.consts.PIC_WIDTH): # 70ピクセル単位で展開
                pos = (x,line)
                assert pos in bitmap, f"No info for ({x},{line})"
                color=bitmap[pos]
                if color == modules.consts.PIC_COLOR_BLACK:
                    color_str='  '
                else:
                    color_str=modules.consts.PIC_COLOR_NAME[color]
                print(f"{color_str}",end='')
            print("")

        return

    def _byteToPixel(self, bitmap_x:int, val:int)->list[int]:

        # コード上, グラフィック画面のX=1から画像を表示するため,
        # ビットマップ上のX座標に1加算し, ビデオメモリ上でのピクセルのX座標に
        # 変換する
        scrn_x_offset = bitmap_x + modules.consts.PIC_START_X

        #
        # AppleIIのビデオメモリ
        #
        # AppleIIは, 1バイトのデータをビデオメモリに書き込むことで, 連続した
        # 7ピクセルのON/OFF(発光の有無)を制御する
        #
        # 書き込みデータ(ビデオメモリに書込む1バイトのデータ)の構成
        #
        # - 0から6ビット目
        #   0ビットから6ビット目までの画面上の各ビットのON/OFFで左から右へピクセルの
        #   発光のON/OFFを決定する
        #
        #   - ビットが0の場合
        #
        #     発光しない(黒色になる)
        #
        #   - ビットが1の場合
        #
        #     a. 直前(画面左側)のピクセルのビットが立っており, (発光していた)
        #        両者が補色の関係(緑,紫の組, または, 橙,青の組)にある場合は,
        #        対象ピクセルを白として発光する(補色により白に見える)
        #
        #     b. 直前(画面左側)のピクセルのビットが立っていない場合
        #        書き込みデータ7ビット目のカラー選択ビットと対象ビットによって
        #        発光されるピクセルに対するビデオメモリ上のX座標の値によって,
        #        発光色を決定する
        #
        # - 7ビット目
        #   カラー選択ビット
        #
        #   最上位ビットは, カラー選択ビットとなっており,
        #   直前のピクセルのビットが立っていない場合, バイトの最上位ビットと
        #   対象ビットによって発光されるビデオメモリ上のピクセルのX座標の値によって,
        #   発光色を選択する
        #
        #   本来は, 信号の位相に依存する発色となるため, 以下は正確な色表現ではないが,
        #   おおよそ, 以下のように色を決定する
        #
        #   1. ビデオメモリ上のピクセルのX座標が偶数の場合,
        #
        #      a. ビデオメモリ上のピクセルのX座標が偶数の場合, かつ, カラー選択ビットが立っていたら
        #         青色を発光する
        #
        #      b. ビデオメモリ上のピクセルのX座標が偶数の場合, かつ, カラー選択ビットが立っていたら
        #         紫を発光する
        #
        #   2. ビデオメモリ上のピクセルのX座標が奇数の場合
        #
        #      i. ビデオメモリ上のピクセルのX座標が奇数の場合, かつ, カラー選択ビットが立っていたら
        #         橙色を発光する
        #
        #     ii. ビデオメモリ上のピクセルのX座標が奇数の場合, かつ, カラー選択ビットが立っていたら
        #         緑を発光する
        #

        color_select = APPLE_COLOR_DECISION_BIT & val # カラー選択ビット

        res:list[int] = [] # 返却するピクセルの色情報(7ビット分)
        for bit in range(7): # 最上位ビットを除く0から6ビット目まで

            mask = 1 << bit

            if val & mask: # ビットが立っている場合,

                scrn_x = scrn_x_offset + bit # ビデオメモリ上の対象ピクセルのX座標を算出

                if scrn_x % 2 == 0: # ビデオメモリ上の偶数ピクセルの場合
                    if color_select: # カラー選択ビットが立っていたら
                        candidate = modules.consts.PIC_COLOR_BLUE # 青
                    else:
                        candidate = modules.consts.PIC_COLOR_PURPLE # 紫
                else:
                    if color_select: # カラー選択ビットが立っていたら
                        candidate = modules.consts.PIC_COLOR_ORANGE # 橙
                    else:
                        candidate = modules.consts.PIC_COLOR_GREEN # 緑

            else: # ビットが0の場合は黒に設定する
                candidate = modules.consts.PIC_COLOR_BLACK # 黒に設定する

            res.append(candidate)

        return res

    def _updateColorImage(self, info:WizardryPicDataEntry)->None:

        for y in range(modules.consts.PIC_HEIGHT):
            for x in range(modules.consts.PIC_WIDTH):
                pos=(x,y)
                assert pos in info.bitmap_info,f"{pos} not found"
                bitmap_entry = info.bitmap_info[pos]
                if x > 0:
                    prev_pos=(x-1, y)
                    assert prev_pos in info.bitmap_info,f"{prev_pos} not found"
                    prev_entry = info.bitmap_info[prev_pos]

                    # 連続した2ビットを白色として扱う
                    if ( bitmap_entry in COLOR_PAIR1 and prev_entry in COLOR_PAIR1 ) or \
                        ( bitmap_entry in COLOR_PAIR2 and prev_entry in COLOR_PAIR2 ):
                        info.color_info[pos]=modules.consts.PIC_COLOR_WHITE
                        info.color_info[prev_pos]=modules.consts.PIC_COLOR_WHITE
                    elif prev_entry in COLORED_PIXEL and bitmap_entry == modules.consts.PIC_COLOR_BLACK:
                        # 前のビットが色のあるビットで, かつ, 次のビットが黒の場合, 前のビットの色にする
                        info.color_info[pos]=prev_entry
                        info.color_info[prev_pos]=prev_entry
                    elif prev_entry == modules.consts.PIC_COLOR_BLACK and bitmap_entry in COLORED_PIXEL:
                        # 前のビットが黒で, かつ, 次のビットが色のあるビットの場合, 後ろのビットの色にする
                        info.color_info[pos]=bitmap_entry
                        info.color_info[prev_pos]=bitmap_entry
                    else:
                        info.color_info[pos]=modules.consts.PIC_COLOR_BLACK
                        info.color_info[prev_pos]=modules.consts.PIC_COLOR_BLACK
                else:
                    info.color_info[pos]=bitmap_entry
        return

    def _updateBitmapImage(self, info:WizardryPicDataEntry)->None:

        index = 0
        for line in range(modules.consts.PIC_HEIGHT): # 各行について

            for bitmap_byte in range(PIC_BYTE_PER_LINE): # 10バイト単位で展開

                bitmap_x = bitmap_byte * modules.consts.PIXEL_PER_BYTE  # bitmap内でのX座標

                res = self._byteToPixel(bitmap_x=bitmap_x, val=info.raw_data[index])
                index += 1
                #
                # ビットマップ情報を更新する
                #
                for offset,val in enumerate(res):
                    pos = (bitmap_x + offset, line)
                    info.bitmap_info[pos]=val

        return

    def _decodeOneImage(self, index:int, info:WizardryPicDataEntry)->None:

        self._updateBitmapImage(info=info) # ビットマップ情報を更新する
        # デバッグ用
        #self._dumpColorInfo(bitmap=info.bitmap_info)

        self._updateColorImage(info=info)  # 描画情報を更新する
        # デバッグ用
        #self._dumpColorInfo(bitmap=info.color_info)
        pass
        return

    def decodeOneData(self, toc:WizardrySCNTOC, data: Any, index: int)->Optional[Any]:
        """シナリオデータファイル中の文字セットデータを解析する

        Args:
            toc (WizardrySCNTOC): 目次情報
            data (Any): シナリオデータファイル情報
            index (int): 画像番号

        Returns:
            Optional[Any]: キャラクタセット情報
        """

        res = WizardryPicDataEntry(raw_data=[], bitmap_info={}, color_info={})

        # 対象画像の開始オフセット位置(単位:ブロック)を得る
        blk_offset = toc.BLOFF[modules.consts.ZSPCCHRS] + index
        # 項目の開始オフセット位置(単位:バイト)を算出
        start_offset = modules.consts.BLK_SIZ * blk_offset

        # 対象のデータ位置(単位:バイト)を得る
        for data_offset in range(modules.consts.BLK_SIZ):
            # # 解析対象データを1バイト単位でunpackする
            byte_val = struct.unpack_from('B', data, start_offset + data_offset)
            val = int(byte_val[0])
            res.raw_data.append(val)

        # 画像イメージをデコードする
        self._decodeOneImage(index=index, info=res)

        return res