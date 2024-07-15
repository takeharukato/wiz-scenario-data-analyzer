#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file mazeFloorDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の迷宮階層データを解析する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の迷宮階層データを解析する

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

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.dataEntryDecoder import dataEntryDecoder
from modules.datadef import WizardrySCNTOC, WizardryMazeFloorDataEntry, WizardryMazeFloorEventInfo, WizardryMazeMonsterTableEntry
from modules.utils import getDecodeDict,calcDataEntryOffset
import modules.consts

"""迷宮フロア情報のPascal定義
        TWALL = (OPEN, WALL, DOOR, HIDEDOOR); (* 壁の種類:
                                                 OPEN(0 空いている壁(通路) ),
                                                 WALL(1 壁),
                                                 DOOR(2 ドア),
                                                 HIDEDOOR(3 隠し扉)
                                               *)

        TSQUARE = (NORMAL, STAIRS, PIT, CHUTE, SPINNER, DARK, TRANSFER,
                   OUCHY, BUTTONZ, ROCKWATE, FIZZLE, SCNMSG, ENCOUNTE); (* 座標位置に設置されている罠, イベントの種別 *)
                   (* NORMAL(0 床),
                      STAIRS(1 階段),
                      PIT(2 落とし穴(A PIT!表示)),
                      CHUTE(3 シュート),
                      SPINNER(4 回転床),
                      DARK(5 暗闇),
                      TRANSFER(6 テレポーター),
                      OUCHY(7 落とし穴(OUCH!表示) ),
                      BUTTONZ(8 エレベータ/ボタン),
                      ROCKWATE(9 石),
                      FIZZLE(10 呪文無効化) ,
                      SCNMSG(11 メッセージ表示),
                      ENCOUNTE(12 強制戦闘)  *)

        TMAZE = RECORD (* 迷宮情報 *)
            W : PACKED ARRAY[ 0..19] OF PACKED ARRAY[ 0..19] OF TWALL; (* 西側の壁 *)
            S : PACKED ARRAY[ 0..19] OF PACKED ARRAY[ 0..19] OF TWALL; (* 南側の壁 *)
            E : PACKED ARRAY[ 0..19] OF PACKED ARRAY[ 0..19] OF TWALL; (* 東側の壁 *)
            N : PACKED ARRAY[ 0..19] OF PACKED ARRAY[ 0..19] OF TWALL; (* 北側の壁 *)

            FIGHTS : PACKED ARRAY[ 0..19] OF PACKED ARRAY[ 0..19] OF 0..1; (* FIGHTS[X座標][Y座標]: 玄室モンスターとの遭遇有無 FIGHTS[X座標][Y座標]=0 玄室モンスターと遭遇しない, FIGHTS[X座標][Y座標]=1 玄室モンスターと遭遇する *)

            SQREXTRA : PACKED ARRAY[ 0..19] OF PACKED ARRAY[ 0..19] OF 0..15; (* SQREXTRA[X座標][Y座標]: 座標位置のイベント番号 *)

            SQRETYPE : PACKED ARRAY[ 0..15] OF TSQUARE; (* イベント番号から設置されている罠, イベントの種別へのマップ *)

            AUX0   : PACKED ARRAY[ 0..15] OF INTEGER; (* イベント番号から階段出口フロア, テレポート先フロア, イベント取得アイテムのアイテム番号(-1*アイテム番号を設定), イベント戦闘時の出現モンスター出現回数, (泉などに)入った場合のイベント種別, 属性(アラインメント)チェック条件, アーマクラス補正値/MILWA・LOMILWAの残光量(LIGHT)増減種別, 謎解きの答えへのマップ *)
            AUX1   : PACKED ARRAY[ 0..15] OF INTEGER; (* イベント番号から階段出口Y座標, テレポート先Y座標, メッセージ番号, ランダムなモンスターと強制戦闘時のモンスターの出現レンジ, 落とし穴のダメージレンジ, エレベーターボタン最下位層へのマップ *)
            AUX2   : PACKED ARRAY[ 0..15] OF INTEGER; (* イベント番号から階段出口X座標, テレポート先X座標, ランダムなモンスターと強制戦闘時のモンスター番号算出時の加算値, エレベーターボタン最上位層へのマップ *)

            ENMYCALC : PACKED ARRAY[ 1..3] OF RECORD (* モンスター遭遇時の出現モンスター番号算出情報 *)
                         MINENEMY : INTEGER; (* モンスター番号の最小値 *)
                         MULTWORS : INTEGER; (* モンスター番号の開始値算出係数 (0からWORSE01までの数値 * MULTWORSによりモンスター番号の開始値を算出) *)
                         WORSE01  : INTEGER; (* モンスター番号の範囲の数 *)
                         RANGE0N  : INTEGER; (* モンスター番号のレンジ *)
                         PERCWORS : INTEGER; (* モンスター番号の範囲を加算する確率 *)
                       END;
          END;
"""

# 迷宮フロア情報のサイズ(単位:バイト)
MAZE_FLOOR_ENTRY_SIZE=894
# アイテム情報のデータレイアウト
WizardryMazeFloorDataEntryDef:dict[str,Any]={
    #
    # 西側の壁
    #
    'W_0': { 'offset':0, 'type': '<H' }, # 西の壁8つ分
    'W_1': { 'offset':2, 'type': '<H' }, # 西の壁8つ分
    'W_2': { 'offset':4, 'type': '<H' }, # 西の壁8つ分
    'W_3': { 'offset':6, 'type': '<H' }, # 西の壁4つ分
    'W_4': { 'offset':8, 'type': '<H' }, # 西の壁8つ分
    'W_5': { 'offset':10, 'type': '<H' }, # 西の壁8つ分
    'W_6': { 'offset':12, 'type': '<H' }, # 西の壁8つ分
    'W_7': { 'offset':14, 'type': '<H' }, # 西の壁4つ分
    'W_8': { 'offset':16, 'type': '<H' }, # 西の壁8つ分
    'W_9': { 'offset':18, 'type': '<H' }, # 西の壁8つ分
    'W_10': { 'offset':20, 'type': '<H' }, # 西の壁8つ分
    'W_11': { 'offset':22, 'type': '<H' }, # 西の壁4つ分
    'W_12': { 'offset':24, 'type': '<H' }, # 西の壁8つ分
    'W_13': { 'offset':26, 'type': '<H' }, # 西の壁8つ分
    'W_14': { 'offset':28, 'type': '<H' }, # 西の壁8つ分
    'W_15': { 'offset':30, 'type': '<H' }, # 西の壁4つ分
    'W_16': { 'offset':32, 'type': '<H' }, # 西の壁8つ分
    'W_17': { 'offset':34, 'type': '<H' }, # 西の壁8つ分
    'W_18': { 'offset':36, 'type': '<H' }, # 西の壁8つ分
    'W_19': { 'offset':38, 'type': '<H' }, # 西の壁4つ分
    'W_20': { 'offset':40, 'type': '<H' }, # 西の壁8つ分
    'W_21': { 'offset':42, 'type': '<H' }, # 西の壁8つ分
    'W_22': { 'offset':44, 'type': '<H' }, # 西の壁8つ分
    'W_23': { 'offset':46, 'type': '<H' }, # 西の壁4つ分
    'W_24': { 'offset':48, 'type': '<H' }, # 西の壁8つ分
    'W_25': { 'offset':50, 'type': '<H' }, # 西の壁8つ分
    'W_26': { 'offset':52, 'type': '<H' }, # 西の壁8つ分
    'W_27': { 'offset':54, 'type': '<H' }, # 西の壁4つ分
    'W_28': { 'offset':56, 'type': '<H' }, # 西の壁8つ分
    'W_29': { 'offset':58, 'type': '<H' }, # 西の壁8つ分
    'W_30': { 'offset':60, 'type': '<H' }, # 西の壁8つ分
    'W_31': { 'offset':62, 'type': '<H' }, # 西の壁4つ分
    'W_32': { 'offset':64, 'type': '<H' }, # 西の壁8つ分
    'W_33': { 'offset':66, 'type': '<H' }, # 西の壁8つ分
    'W_34': { 'offset':68, 'type': '<H' }, # 西の壁8つ分
    'W_35': { 'offset':70, 'type': '<H' }, # 西の壁4つ分
    'W_36': { 'offset':72, 'type': '<H' }, # 西の壁8つ分
    'W_37': { 'offset':74, 'type': '<H' }, # 西の壁8つ分
    'W_38': { 'offset':76, 'type': '<H' }, # 西の壁8つ分
    'W_39': { 'offset':78, 'type': '<H' }, # 西の壁4つ分
    'W_40': { 'offset':80, 'type': '<H' }, # 西の壁8つ分
    'W_41': { 'offset':82, 'type': '<H' }, # 西の壁8つ分
    'W_42': { 'offset':84, 'type': '<H' }, # 西の壁8つ分
    'W_43': { 'offset':86, 'type': '<H' }, # 西の壁4つ分
    'W_44': { 'offset':88, 'type': '<H' }, # 西の壁8つ分
    'W_45': { 'offset':90, 'type': '<H' }, # 西の壁8つ分
    'W_46': { 'offset':92, 'type': '<H' }, # 西の壁8つ分
    'W_47': { 'offset':94, 'type': '<H' }, # 西の壁4つ分
    'W_48': { 'offset':96, 'type': '<H' }, # 西の壁8つ分
    'W_49': { 'offset':98, 'type': '<H' }, # 西の壁8つ分
    'W_50': { 'offset':100, 'type': '<H' }, # 西の壁8つ分
    'W_51': { 'offset':102, 'type': '<H' }, # 西の壁4つ分
    'W_52': { 'offset':104, 'type': '<H' }, # 西の壁8つ分
    'W_53': { 'offset':106, 'type': '<H' }, # 西の壁8つ分
    'W_54': { 'offset':108, 'type': '<H' }, # 西の壁8つ分
    'W_55': { 'offset':110, 'type': '<H' }, # 西の壁4つ分
    'W_56': { 'offset':112, 'type': '<H' }, # 西の壁8つ分
    'W_57': { 'offset':114, 'type': '<H' }, # 西の壁8つ分
    'W_58': { 'offset':116, 'type': '<H' }, # 西の壁8つ分
    'W_59': { 'offset':118, 'type': '<H' }, # 西の壁4つ分

    #
    # 南側の壁
    #
    'S_0': { 'offset':120, 'type': '<H' }, # 南の壁8つ分
    'S_1': { 'offset':122, 'type': '<H' }, # 南の壁8つ分
    'S_2': { 'offset':124, 'type': '<H' }, # 南の壁8つ分
    'S_3': { 'offset':126, 'type': '<H' }, # 南の壁4つ分
    'S_4': { 'offset':128, 'type': '<H' }, # 南の壁8つ分
    'S_5': { 'offset':130, 'type': '<H' }, # 南の壁8つ分
    'S_6': { 'offset':132, 'type': '<H' }, # 南の壁8つ分
    'S_7': { 'offset':134, 'type': '<H' }, # 南の壁4つ分
    'S_8': { 'offset':136, 'type': '<H' }, # 南の壁8つ分
    'S_9': { 'offset':138, 'type': '<H' }, # 南の壁8つ分
    'S_10': { 'offset':140, 'type': '<H' }, # 南の壁8つ分
    'S_11': { 'offset':142, 'type': '<H' }, # 南の壁4つ分
    'S_12': { 'offset':144, 'type': '<H' }, # 南の壁8つ分
    'S_13': { 'offset':146, 'type': '<H' }, # 南の壁8つ分
    'S_14': { 'offset':148, 'type': '<H' }, # 南の壁8つ分
    'S_15': { 'offset':150, 'type': '<H' }, # 南の壁4つ分
    'S_16': { 'offset':152, 'type': '<H' }, # 南の壁8つ分
    'S_17': { 'offset':154, 'type': '<H' }, # 南の壁8つ分
    'S_18': { 'offset':156, 'type': '<H' }, # 南の壁8つ分
    'S_19': { 'offset':158, 'type': '<H' }, # 南の壁4つ分
    'S_20': { 'offset':160, 'type': '<H' }, # 南の壁8つ分
    'S_21': { 'offset':162, 'type': '<H' }, # 南の壁8つ分
    'S_22': { 'offset':164, 'type': '<H' }, # 南の壁8つ分
    'S_23': { 'offset':166, 'type': '<H' }, # 南の壁4つ分
    'S_24': { 'offset':168, 'type': '<H' }, # 南の壁8つ分
    'S_25': { 'offset':170, 'type': '<H' }, # 南の壁8つ分
    'S_26': { 'offset':172, 'type': '<H' }, # 南の壁8つ分
    'S_27': { 'offset':174, 'type': '<H' }, # 南の壁4つ分
    'S_28': { 'offset':176, 'type': '<H' }, # 南の壁8つ分
    'S_29': { 'offset':178, 'type': '<H' }, # 南の壁8つ分
    'S_30': { 'offset':180, 'type': '<H' }, # 南の壁8つ分
    'S_31': { 'offset':182, 'type': '<H' }, # 南の壁4つ分
    'S_32': { 'offset':184, 'type': '<H' }, # 南の壁8つ分
    'S_33': { 'offset':186, 'type': '<H' }, # 南の壁8つ分
    'S_34': { 'offset':188, 'type': '<H' }, # 南の壁8つ分
    'S_35': { 'offset':190, 'type': '<H' }, # 南の壁4つ分
    'S_36': { 'offset':192, 'type': '<H' }, # 南の壁8つ分
    'S_37': { 'offset':194, 'type': '<H' }, # 南の壁8つ分
    'S_38': { 'offset':196, 'type': '<H' }, # 南の壁8つ分
    'S_39': { 'offset':198, 'type': '<H' }, # 南の壁4つ分
    'S_40': { 'offset':200, 'type': '<H' }, # 南の壁8つ分
    'S_41': { 'offset':202, 'type': '<H' }, # 南の壁8つ分
    'S_42': { 'offset':204, 'type': '<H' }, # 南の壁8つ分
    'S_43': { 'offset':206, 'type': '<H' }, # 南の壁4つ分
    'S_44': { 'offset':208, 'type': '<H' }, # 南の壁8つ分
    'S_45': { 'offset':210, 'type': '<H' }, # 南の壁8つ分
    'S_46': { 'offset':212, 'type': '<H' }, # 南の壁8つ分
    'S_47': { 'offset':214, 'type': '<H' }, # 南の壁4つ分
    'S_48': { 'offset':216, 'type': '<H' }, # 南の壁8つ分
    'S_49': { 'offset':218, 'type': '<H' }, # 南の壁8つ分
    'S_50': { 'offset':220, 'type': '<H' }, # 南の壁8つ分
    'S_51': { 'offset':222, 'type': '<H' }, # 南の壁4つ分
    'S_52': { 'offset':224, 'type': '<H' }, # 南の壁8つ分
    'S_53': { 'offset':226, 'type': '<H' }, # 南の壁8つ分
    'S_54': { 'offset':228, 'type': '<H' }, # 南の壁8つ分
    'S_55': { 'offset':230, 'type': '<H' }, # 南の壁4つ分
    'S_56': { 'offset':232, 'type': '<H' }, # 南の壁8つ分
    'S_57': { 'offset':234, 'type': '<H' }, # 南の壁8つ分
    'S_58': { 'offset':236, 'type': '<H' }, # 南の壁8つ分
    'S_59': { 'offset':238, 'type': '<H' }, # 南の壁4つ分

    #
    # 東側の壁
    #
    'E_0': { 'offset':240, 'type': '<H' }, # 東の壁8つ分
    'E_1': { 'offset':242, 'type': '<H' }, # 東の壁8つ分
    'E_2': { 'offset':244, 'type': '<H' }, # 東の壁8つ分
    'E_3': { 'offset':246, 'type': '<H' }, # 東の壁4つ分
    'E_4': { 'offset':248, 'type': '<H' }, # 東の壁8つ分
    'E_5': { 'offset':250, 'type': '<H' }, # 東の壁8つ分
    'E_6': { 'offset':252, 'type': '<H' }, # 東の壁8つ分
    'E_7': { 'offset':254, 'type': '<H' }, # 東の壁4つ分
    'E_8': { 'offset':256, 'type': '<H' }, # 東の壁8つ分
    'E_9': { 'offset':258, 'type': '<H' }, # 東の壁8つ分
    'E_10': { 'offset':260, 'type': '<H' }, # 東の壁8つ分
    'E_11': { 'offset':262, 'type': '<H' }, # 東の壁4つ分
    'E_12': { 'offset':264, 'type': '<H' }, # 東の壁8つ分
    'E_13': { 'offset':266, 'type': '<H' }, # 東の壁8つ分
    'E_14': { 'offset':268, 'type': '<H' }, # 東の壁8つ分
    'E_15': { 'offset':270, 'type': '<H' }, # 東の壁4つ分
    'E_16': { 'offset':272, 'type': '<H' }, # 東の壁8つ分
    'E_17': { 'offset':274, 'type': '<H' }, # 東の壁8つ分
    'E_18': { 'offset':276, 'type': '<H' }, # 東の壁8つ分
    'E_19': { 'offset':278, 'type': '<H' }, # 東の壁4つ分
    'E_20': { 'offset':280, 'type': '<H' }, # 東の壁8つ分
    'E_21': { 'offset':282, 'type': '<H' }, # 東の壁8つ分
    'E_22': { 'offset':284, 'type': '<H' }, # 東の壁8つ分
    'E_23': { 'offset':286, 'type': '<H' }, # 東の壁4つ分
    'E_24': { 'offset':288, 'type': '<H' }, # 東の壁8つ分
    'E_25': { 'offset':290, 'type': '<H' }, # 東の壁8つ分
    'E_26': { 'offset':292, 'type': '<H' }, # 東の壁8つ分
    'E_27': { 'offset':294, 'type': '<H' }, # 東の壁4つ分
    'E_28': { 'offset':296, 'type': '<H' }, # 東の壁8つ分
    'E_29': { 'offset':298, 'type': '<H' }, # 東の壁8つ分
    'E_30': { 'offset':300, 'type': '<H' }, # 東の壁8つ分
    'E_31': { 'offset':302, 'type': '<H' }, # 東の壁4つ分
    'E_32': { 'offset':304, 'type': '<H' }, # 東の壁8つ分
    'E_33': { 'offset':306, 'type': '<H' }, # 東の壁8つ分
    'E_34': { 'offset':308, 'type': '<H' }, # 東の壁8つ分
    'E_35': { 'offset':310, 'type': '<H' }, # 東の壁4つ分
    'E_36': { 'offset':312, 'type': '<H' }, # 東の壁8つ分
    'E_37': { 'offset':314, 'type': '<H' }, # 東の壁8つ分
    'E_38': { 'offset':316, 'type': '<H' }, # 東の壁8つ分
    'E_39': { 'offset':318, 'type': '<H' }, # 東の壁4つ分
    'E_40': { 'offset':320, 'type': '<H' }, # 東の壁8つ分
    'E_41': { 'offset':322, 'type': '<H' }, # 東の壁8つ分
    'E_42': { 'offset':324, 'type': '<H' }, # 東の壁8つ分
    'E_43': { 'offset':326, 'type': '<H' }, # 東の壁4つ分
    'E_44': { 'offset':328, 'type': '<H' }, # 東の壁8つ分
    'E_45': { 'offset':330, 'type': '<H' }, # 東の壁8つ分
    'E_46': { 'offset':332, 'type': '<H' }, # 東の壁8つ分
    'E_47': { 'offset':334, 'type': '<H' }, # 東の壁4つ分
    'E_48': { 'offset':336, 'type': '<H' }, # 東の壁8つ分
    'E_49': { 'offset':338, 'type': '<H' }, # 東の壁8つ分
    'E_50': { 'offset':340, 'type': '<H' }, # 東の壁8つ分
    'E_51': { 'offset':342, 'type': '<H' }, # 東の壁4つ分
    'E_52': { 'offset':344, 'type': '<H' }, # 東の壁8つ分
    'E_53': { 'offset':346, 'type': '<H' }, # 東の壁8つ分
    'E_54': { 'offset':348, 'type': '<H' }, # 東の壁8つ分
    'E_55': { 'offset':350, 'type': '<H' }, # 東の壁4つ分
    'E_56': { 'offset':352, 'type': '<H' }, # 東の壁8つ分
    'E_57': { 'offset':354, 'type': '<H' }, # 東の壁8つ分
    'E_58': { 'offset':356, 'type': '<H' }, # 東の壁8つ分
    'E_59': { 'offset':358, 'type': '<H' }, # 東の壁4つ分

    #
    # 北側の壁
    #
    'N_0': { 'offset':360, 'type': '<H' }, # 北の壁8つ分
    'N_1': { 'offset':362, 'type': '<H' }, # 北の壁8つ分
    'N_2': { 'offset':364, 'type': '<H' }, # 北の壁8つ分
    'N_3': { 'offset':366, 'type': '<H' }, # 北の壁4つ分
    'N_4': { 'offset':368, 'type': '<H' }, # 北の壁8つ分
    'N_5': { 'offset':370, 'type': '<H' }, # 北の壁8つ分
    'N_6': { 'offset':372, 'type': '<H' }, # 北の壁8つ分
    'N_7': { 'offset':374, 'type': '<H' }, # 北の壁4つ分
    'N_8': { 'offset':376, 'type': '<H' }, # 北の壁8つ分
    'N_9': { 'offset':378, 'type': '<H' }, # 北の壁8つ分
    'N_10': { 'offset':380, 'type': '<H' }, # 北の壁8つ分
    'N_11': { 'offset':382, 'type': '<H' }, # 北の壁4つ分
    'N_12': { 'offset':384, 'type': '<H' }, # 北の壁8つ分
    'N_13': { 'offset':386, 'type': '<H' }, # 北の壁8つ分
    'N_14': { 'offset':388, 'type': '<H' }, # 北の壁8つ分
    'N_15': { 'offset':390, 'type': '<H' }, # 北の壁4つ分
    'N_16': { 'offset':392, 'type': '<H' }, # 北の壁8つ分
    'N_17': { 'offset':394, 'type': '<H' }, # 北の壁8つ分
    'N_18': { 'offset':396, 'type': '<H' }, # 北の壁8つ分
    'N_19': { 'offset':398, 'type': '<H' }, # 北の壁4つ分
    'N_20': { 'offset':400, 'type': '<H' }, # 北の壁8つ分
    'N_21': { 'offset':402, 'type': '<H' }, # 北の壁8つ分
    'N_22': { 'offset':404, 'type': '<H' }, # 北の壁8つ分
    'N_23': { 'offset':406, 'type': '<H' }, # 北の壁4つ分
    'N_24': { 'offset':408, 'type': '<H' }, # 北の壁8つ分
    'N_25': { 'offset':410, 'type': '<H' }, # 北の壁8つ分
    'N_26': { 'offset':412, 'type': '<H' }, # 北の壁8つ分
    'N_27': { 'offset':414, 'type': '<H' }, # 北の壁4つ分
    'N_28': { 'offset':416, 'type': '<H' }, # 北の壁8つ分
    'N_29': { 'offset':418, 'type': '<H' }, # 北の壁8つ分
    'N_30': { 'offset':420, 'type': '<H' }, # 北の壁8つ分
    'N_31': { 'offset':422, 'type': '<H' }, # 北の壁4つ分
    'N_32': { 'offset':424, 'type': '<H' }, # 北の壁8つ分
    'N_33': { 'offset':426, 'type': '<H' }, # 北の壁8つ分
    'N_34': { 'offset':428, 'type': '<H' }, # 北の壁8つ分
    'N_35': { 'offset':430, 'type': '<H' }, # 北の壁4つ分
    'N_36': { 'offset':432, 'type': '<H' }, # 北の壁8つ分
    'N_37': { 'offset':434, 'type': '<H' }, # 北の壁8つ分
    'N_38': { 'offset':436, 'type': '<H' }, # 北の壁8つ分
    'N_39': { 'offset':438, 'type': '<H' }, # 北の壁4つ分
    'N_40': { 'offset':440, 'type': '<H' }, # 北の壁8つ分
    'N_41': { 'offset':442, 'type': '<H' }, # 北の壁8つ分
    'N_42': { 'offset':444, 'type': '<H' }, # 北の壁8つ分
    'N_43': { 'offset':446, 'type': '<H' }, # 北の壁4つ分
    'N_44': { 'offset':448, 'type': '<H' }, # 北の壁8つ分
    'N_45': { 'offset':450, 'type': '<H' }, # 北の壁8つ分
    'N_46': { 'offset':452, 'type': '<H' }, # 北の壁8つ分
    'N_47': { 'offset':454, 'type': '<H' }, # 北の壁4つ分
    'N_48': { 'offset':456, 'type': '<H' }, # 北の壁8つ分
    'N_49': { 'offset':458, 'type': '<H' }, # 北の壁8つ分
    'N_50': { 'offset':460, 'type': '<H' }, # 北の壁8つ分
    'N_51': { 'offset':462, 'type': '<H' }, # 北の壁4つ分
    'N_52': { 'offset':464, 'type': '<H' }, # 北の壁8つ分
    'N_53': { 'offset':466, 'type': '<H' }, # 北の壁8つ分
    'N_54': { 'offset':468, 'type': '<H' }, # 北の壁8つ分
    'N_55': { 'offset':470, 'type': '<H' }, # 北の壁4つ分
    'N_56': { 'offset':472, 'type': '<H' }, # 北の壁8つ分
    'N_57': { 'offset':474, 'type': '<H' }, # 北の壁8つ分
    'N_58': { 'offset':476, 'type': '<H' }, # 北の壁8つ分
    'N_59': { 'offset':478, 'type': '<H' }, # 北の壁4つ分


    #
    # 玄室情報
    #
    'FIGHTS_0': { 'offset':480, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_1': { 'offset':482, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_2': { 'offset':484, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_3': { 'offset':486, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_4': { 'offset':488, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_5': { 'offset':490, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_6': { 'offset':492, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_7': { 'offset':494, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_8': { 'offset':496, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_9': { 'offset':498, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_10': { 'offset':500, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_11': { 'offset':502, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_12': { 'offset':504, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_13': { 'offset':506, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_14': { 'offset':508, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_15': { 'offset':510, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_16': { 'offset':512, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_17': { 'offset':514, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_18': { 'offset':516, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_19': { 'offset':518, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_20': { 'offset':520, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_21': { 'offset':522, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_22': { 'offset':524, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_23': { 'offset':526, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_24': { 'offset':528, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_25': { 'offset':530, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_26': { 'offset':532, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_27': { 'offset':534, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_28': { 'offset':536, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_29': { 'offset':538, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_30': { 'offset':540, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_31': { 'offset':542, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_32': { 'offset':544, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_33': { 'offset':546, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_34': { 'offset':548, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_35': { 'offset':550, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_36': { 'offset':552, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_37': { 'offset':554, 'type': '<H' }, # 玄室情報4個分
    'FIGHTS_38': { 'offset':556, 'type': '<H' }, # 玄室情報16個分
    'FIGHTS_39': { 'offset':558, 'type': '<H' }, # 玄室情報4個分

    #
    # 各座標で発生するイベントのイベント番号
    #
    'SQREXTRA_0': { 'offset':560, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_1': { 'offset':562, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_2': { 'offset':564, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_3': { 'offset':566, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_4': { 'offset':568, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_5': { 'offset':570, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_6': { 'offset':572, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_7': { 'offset':574, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_8': { 'offset':576, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_9': { 'offset':578, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_10': { 'offset':580, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_11': { 'offset':582, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_12': { 'offset':584, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_13': { 'offset':586, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_14': { 'offset':588, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_15': { 'offset':590, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_16': { 'offset':592, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_17': { 'offset':594, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_18': { 'offset':596, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_19': { 'offset':598, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_20': { 'offset':600, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_21': { 'offset':602, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_22': { 'offset':604, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_23': { 'offset':606, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_24': { 'offset':608, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_25': { 'offset':610, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_26': { 'offset':612, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_27': { 'offset':614, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_28': { 'offset':616, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_29': { 'offset':618, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_30': { 'offset':620, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_31': { 'offset':622, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_32': { 'offset':624, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_33': { 'offset':626, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_34': { 'offset':628, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_35': { 'offset':630, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_36': { 'offset':632, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_37': { 'offset':634, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_38': { 'offset':636, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_39': { 'offset':638, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_40': { 'offset':640, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_41': { 'offset':642, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_42': { 'offset':644, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_43': { 'offset':646, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_44': { 'offset':648, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_45': { 'offset':650, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_46': { 'offset':652, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_47': { 'offset':654, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_48': { 'offset':656, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_49': { 'offset':658, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_50': { 'offset':660, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_51': { 'offset':662, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_52': { 'offset':664, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_53': { 'offset':666, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_54': { 'offset':668, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_55': { 'offset':670, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_56': { 'offset':672, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_57': { 'offset':674, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_58': { 'offset':676, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_59': { 'offset':678, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_60': { 'offset':680, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_61': { 'offset':682, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_62': { 'offset':684, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_63': { 'offset':686, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_64': { 'offset':688, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_65': { 'offset':690, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_66': { 'offset':692, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_67': { 'offset':694, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_68': { 'offset':696, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_69': { 'offset':698, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_70': { 'offset':700, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_71': { 'offset':702, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_72': { 'offset':704, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_73': { 'offset':706, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_74': { 'offset':708, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_75': { 'offset':710, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_76': { 'offset':712, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_77': { 'offset':714, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_78': { 'offset':716, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_79': { 'offset':718, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_80': { 'offset':720, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_81': { 'offset':722, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_82': { 'offset':724, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_83': { 'offset':726, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_84': { 'offset':728, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_85': { 'offset':730, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_86': { 'offset':732, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_87': { 'offset':734, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_88': { 'offset':736, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_89': { 'offset':738, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_90': { 'offset':740, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_91': { 'offset':742, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_92': { 'offset':744, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_93': { 'offset':746, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_94': { 'offset':748, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_95': { 'offset':750, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_96': { 'offset':752, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_97': { 'offset':754, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_98': { 'offset':756, 'type': '<H' }, # イベント番号4つ分
    'SQREXTRA_99': { 'offset':758, 'type': '<H' }, # イベント番号4つ分

    #
    # イベント番号(0から15)とイベント種別(TSQUARE)との関係
    #
    'SQRETYPE_0': { 'offset':760, 'type': '<H' }, # イベント種別4つ分
    'SQRETYPE_1': { 'offset':762, 'type': '<H' }, # イベント種別4つ分
    'SQRETYPE_2': { 'offset':764, 'type': '<H' }, # イベント種別4つ分
    'SQRETYPE_3': { 'offset':766, 'type': '<H' }, # イベント種別4つ分

    #
    # イベント番号(0から15)のイベントパラメタ1(AUX0)
    #
    'AUX0_0': { 'offset':768, 'type': '<h' }, # イベント情報0
    'AUX0_1': { 'offset':770, 'type': '<h' }, # イベント情報1
    'AUX0_2': { 'offset':772, 'type': '<h' }, # イベント情報2
    'AUX0_3': { 'offset':774, 'type': '<h' }, # イベント情報3
    'AUX0_4': { 'offset':776, 'type': '<h' }, # イベント情報4
    'AUX0_5': { 'offset':778, 'type': '<h' }, # イベント情報5
    'AUX0_6': { 'offset':780, 'type': '<h' }, # イベント情報6
    'AUX0_7': { 'offset':782, 'type': '<h' }, # イベント情報7
    'AUX0_8': { 'offset':784, 'type': '<h' }, # イベント情報8
    'AUX0_9': { 'offset':786, 'type': '<h' }, # イベント情報9
    'AUX0_10': { 'offset':788, 'type': '<h' }, # イベント情報10
    'AUX0_11': { 'offset':790, 'type': '<h' }, # イベント情報11
    'AUX0_12': { 'offset':792, 'type': '<h' }, # イベント情報12
    'AUX0_13': { 'offset':794, 'type': '<h' }, # イベント情報13
    'AUX0_14': { 'offset':796, 'type': '<h' }, # イベント情報14
    'AUX0_15': { 'offset':798, 'type': '<h' }, # イベント情報15

    #
    # イベント番号(0から15)のイベントパラメタ2(AUX1)
    #
    'AUX1_0': { 'offset':800, 'type': '<h' }, # イベント情報0
    'AUX1_1': { 'offset':802, 'type': '<h' }, # イベント情報1
    'AUX1_2': { 'offset':804, 'type': '<h' }, # イベント情報2
    'AUX1_3': { 'offset':806, 'type': '<h' }, # イベント情報3
    'AUX1_4': { 'offset':808, 'type': '<h' }, # イベント情報4
    'AUX1_5': { 'offset':810, 'type': '<h' }, # イベント情報5
    'AUX1_6': { 'offset':812, 'type': '<h' }, # イベント情報6
    'AUX1_7': { 'offset':814, 'type': '<h' }, # イベント情報7
    'AUX1_8': { 'offset':816, 'type': '<h' }, # イベント情報8
    'AUX1_9': { 'offset':818, 'type': '<h' }, # イベント情報9
    'AUX1_10': { 'offset':820, 'type': '<h' }, # イベント情報10
    'AUX1_11': { 'offset':822, 'type': '<h' }, # イベント情報11
    'AUX1_12': { 'offset':824, 'type': '<h' }, # イベント情報12
    'AUX1_13': { 'offset':826, 'type': '<h' }, # イベント情報13
    'AUX1_14': { 'offset':828, 'type': '<h' }, # イベント情報14
    'AUX1_15': { 'offset':830, 'type': '<h' }, # イベント情報15

    #
    # イベント番号(0から15)のイベントパラメタ3(AUX2)
    #
    'AUX2_0': { 'offset':832, 'type': '<h' }, # イベント情報0
    'AUX2_1': { 'offset':834, 'type': '<h' }, # イベント情報1
    'AUX2_2': { 'offset':836, 'type': '<h' }, # イベント情報2
    'AUX2_3': { 'offset':838, 'type': '<h' }, # イベント情報3
    'AUX2_4': { 'offset':840, 'type': '<h' }, # イベント情報4
    'AUX2_5': { 'offset':842, 'type': '<h' }, # イベント情報5
    'AUX2_6': { 'offset':844, 'type': '<h' }, # イベント情報6
    'AUX2_7': { 'offset':846, 'type': '<h' }, # イベント情報7
    'AUX2_8': { 'offset':848, 'type': '<h' }, # イベント情報8
    'AUX2_9': { 'offset':850, 'type': '<h' }, # イベント情報9
    'AUX2_10': { 'offset':852, 'type': '<h' }, # イベント情報10
    'AUX2_11': { 'offset':854, 'type': '<h' }, # イベント情報11
    'AUX2_12': { 'offset':856, 'type': '<h' }, # イベント情報12
    'AUX2_13': { 'offset':858, 'type': '<h' }, # イベント情報13
    'AUX2_14': { 'offset':860, 'type': '<h' }, # イベント情報14
    'AUX2_15': { 'offset':862, 'type': '<h' }, # イベント情報15

    #
    # モンスター出現テーブル
    #
    'MINENEMY_1': { 'offset':864, 'type': '<H' }, # モンスター番号最小値1
    'MULTWORS_1': { 'offset':866, 'type': '<H' }, # 開始モンスター番号算出係数1
    'WORSE01_1': { 'offset':868, 'type': '<H' }, # モンスター番号レンジの系統数1
    'RANGE0N_1': { 'offset':870, 'type': '<H' }, # モンスター番号レンジ1
    'PERCWORS_1': { 'offset':872, 'type': '<H' }, # モンスター番号レンジ切り替え確率1
    'MINENEMY_2': { 'offset':874, 'type': '<H' }, # モンスター番号最小値2
    'MULTWORS_2': { 'offset':876, 'type': '<H' }, # 開始モンスター番号算出係数2
    'WORSE01_2': { 'offset':878, 'type': '<H' }, # モンスター番号レンジの系統数2
    'RANGE0N_2': { 'offset':880, 'type': '<H' }, # モンスター番号レンジ2
    'PERCWORS_2': { 'offset':882, 'type': '<H' }, # モンスター番号レンジ切り替え確率2
    'MINENEMY_3': { 'offset':884, 'type': '<H' }, # モンスター番号最小値3
    'MULTWORS_3': { 'offset':886, 'type': '<H' }, # 開始モンスター番号算出係数3
    'WORSE01_3': { 'offset':888, 'type': '<H' }, # モンスター番号レンジの系統数3
    'RANGE0N_3': { 'offset':890, 'type': '<H' }, # モンスター番号レンジ3
    'PERCWORS_3': { 'offset':892, 'type': '<H' }, # モンスター番号レンジ切り替え確率3
}

class mazeFloorDecoder(dataEntryDecoder):

    def _setBool(self, out_dic:dict[tuple[int,int],Any], key:tuple[int,int], value:int)->None:
        """真偽値を格納する

        Args:
            out_dic (dict[tuple[int,int], Any]): 出力先辞書
            key (tuple[int,int]): 座標(x,y)を表すタプル
            value (int): 格納値
        """
        out_dic[key]=True if value != 0 else False
        return

    def _setInteger(self, out_dic:dict[tuple[int,int],Any], key:tuple[int,int], value:int)->None:
        """整数値を格納する

        Args:
            out_dic (dict[tuple[int,int], Any]): 出力先辞書
            key (tuple[int,int]): 座標(x,y)を表すタプル
            value (int): 格納値
        """
        out_dic[key]=value
        return

    def _decodeMapData(self, toc:WizardrySCNTOC, decode_dict:dict[str,Any], element_prefix:str, out_dic:dict[tuple[int,int], Any], data_bit_len:int, data_per_word:int, set_func:Callable[[dict[tuple[int,int],int],tuple[int,int],Any],None])->None:
        """マップ情報をデコードする

        Args:
            toc (WizardrySCNTOC): 目次情報
            decode_dict (dict[str,Any]): unpackしたフロア情報の辞書(unpackしたデータの要素名->bytes列のタプル)
            element_prefix (str): データレイアウト中の配列変数のプレフィクス(W,S,E,N,FIGHTS,SQREXTRA)
            out_dic (dict[tuple[int,int], Any]): 出力先辞書
            data_bit_len (int): データの格納ビット長(単位:ビット)
            data_per_word (int): ワード長データ内での格納データエントリ数(単位:個)
            set_func (Callable): 出力先辞書にデータを格納する関数
        """
        # 各X座標の要素を入れるのに必要なワード数
        words_per_x = ( ( (data_per_word - 1) + (modules.consts.FLOOR_HEIGHT - 1) ) // data_per_word )

        for x in range(modules.consts.FLOOR_WIDTH):
            array_start = x * words_per_x # 各X座標開始時の配列インデクス
            for y in range(modules.consts.FLOOR_HEIGHT):
                pos_key=(x,y)               # 座標
                pos_idx = y % data_per_word # 何番目の要素を探すか
                array_index = array_start + y // data_per_word # 配列のインデクス
                array_element = f"{element_prefix}_{array_index}" # 配列要素名
                assert array_element in decode_dict, f"{array_element} not found."
                array_value = int(decode_dict[array_element][0]) # 配列の値を取得
                value_mask = ( ( 1 << data_bit_len ) - 1 )            # マスク値
                value =  ( array_value >> ( pos_idx * data_bit_len ) ) & value_mask # データ値を取得する
                set_func(out_dic, pos_key, value) # データ値を格納する

        return

    def _decodeFloorLayout(self, toc:WizardrySCNTOC, decode_dict:dict[str,Any], res:WizardryMazeFloorDataEntry)->None:
        """フロアレイアウト情報を格納する

        Args:
            toc (WizardrySCNTOC): 目次情報
            decode_dict (dict[str,Any]): unpackしたフロア情報の辞書(unpackしたデータの要素名->bytes列のタプル)
            res (WizardryMazeFloorDataEntry): 格納先データ
        """

        # 向きと格納先辞書とのマッピング
        ref_dict={
            'W':res.wall_info_west,
            'S':res.wall_info_south,
            'E':res.wall_info_east,
            'N':res.wall_info_north,
        }

        for dir in ['W','S','E','N']: # 各向き(西,南,東,北)について, 壁の情報を取得する
            dic=ref_dict[dir] # 格納先辞書
            # 各向きについての壁の情報を取得する
            self._decodeMapData(toc=toc, decode_dict=decode_dict, element_prefix=dir, out_dic=dic, data_bit_len=2, data_per_word=8, set_func=self._setInteger)

        return

    def _decodeEventType(self, toc:WizardrySCNTOC, decode_dict:dict[str,Any], out_dic:dict[int,int])->None:
        """各イベント番号のイベントに設定されているイベント種別を取得する

        Args:
            toc (WizardrySCNTOC): 目次情報
            decode_dict (dict[str,Any]): unpackしたフロア情報の辞書(unpackしたデータの要素名->bytes列のタプル)
            out_dic (dict[int,int]): 出力先辞書
        """

        data_bit_len=4 # TSQUARE型のビット長
        elements_per_word=4 # 1ワード中の格納データ数
        for number in range(modules.consts.FLOOR_EVENTS_PER_FLOOR):
            idx = number // elements_per_word    # ワード配列のインデクス
            pos_idx = number % elements_per_word # ワード配列要素中の位置(単位:TSQUARE型の要素単位で, 0番目から数えた個数)
            array_element=f"SQRETYPE_{idx}" # データ格納先
            assert array_element in decode_dict, f"{array_element} not found"
            array_value = int(decode_dict[array_element][0]) # 配列の値を取得
            value_mask = ( ( 1 << data_bit_len ) - 1 ) # マスク値
            value =  ( array_value >> ( pos_idx * data_bit_len ) ) & value_mask # データ値を取得する
            out_dic[number]=value # 値を設定する

        return

    def _decodeEventParams(self, toc:WizardrySCNTOC, decode_dict:dict[str,Any], event_type_dic:dict[int,int], res: WizardryMazeFloorDataEntry)->None:
        """イベントのパラメタを格納する

        Args:
            toc (WizardrySCNTOC): 目次情報
            decode_dict (dict[str,Any]): unpackしたフロア情報の辞書(unpackしたデータの要素名->bytes列のタプル)
            event_type_dic (dict[int,int]): イベント番号からイベント種別への辞書
            res (WizardryMazeFloorDataEntry): pythonのオブジェクトであらわしたフロア情報
        """
        for event_number in range(modules.consts.FLOOR_EVENTS_PER_FLOOR): # 0から15番のイベントについて

            if event_number not in event_type_dic: # 対象のイベント情報がない場合
                continue # 読み飛ばす

            #
            # パラメタを設定する
            #
            event_param=WizardryMazeFloorEventInfo(event_type=event_type_dic[event_number], params={})
            for aux_number in range(modules.consts.FLOOR_NR_EVENT_PARAMS): # AUX0からAUX2について
                array_element=f"AUX{aux_number}_{event_number}" # データ格納先を算出
                assert array_element in decode_dict, f"{array_element} not found"
                array_value = int(decode_dict[array_element][0]) # 配列の値を取得
                event_param.params[aux_number]=array_value # パラメタを格納

            res.event_info_dic[event_number]=event_param # イベント情報を設定

        return

    def _decodeMonsterTables(self, toc:WizardrySCNTOC, decode_dict:dict[str,Any], res: WizardryMazeFloorDataEntry)->None:

        for series in range(modules.consts.FLOOR_NR_MONSTER_TABLE_SERIES): # 全ての系統について

            entry = WizardryMazeMonsterTableEntry(number=series, min_enemy=0, multiplier=0,
                                                  max_series=0, monster_range=0,
                                                  inc_series_percentage=0)

            for param in ['MINENEMY', 'MULTWORS', 'WORSE01', 'RANGE0N', 'PERCWORS']: # 各パラメタについて

                array_element=f"{param}_{series + 1}" # データ格納先
                assert array_element in decode_dict, f"{array_element} not found"
                array_value = int(decode_dict[array_element][0]) # 配列の値を取得
                match param:
                    case 'MINENEMY':
                        entry.min_enemy = array_value
                    case 'MULTWORS':
                        entry.multiplier = array_value
                    case 'WORSE01':
                        entry.max_series = array_value
                    case 'RANGE0N':
                        entry.monster_range = array_value
                    case 'PERCWORS':
                        entry.inc_series_percentage = array_value
                    case _:
                        pass
            # パラメタを設定する
            res.monster_tables[series]=entry

        return

    def _dict2MazeFloorDataEntry(self, toc:WizardrySCNTOC, decode_dict:dict[str,Any])->WizardryMazeFloorDataEntry:
        """unpackしたフロア情報をpythonのオブジェクトに変換

        Args:
            toc (WizardrySCNTOC): 目次情報
            decode_dict (dict[str,Any]): unpackしたフロア情報の辞書(unpackしたデータの要素名->bytes列のタプル)

        Returns:
            WizardryMazeFloorDataEntry: pythonのオブジェクトであらわしたフロア情報
        """

        event_number_to_type:dict[int,int]={} # イベント番号からイベント種別への辞書(TSQUARE)

        res = WizardryMazeFloorDataEntry(wall_info_west={}, wall_info_south={}, wall_info_east={}, wall_info_north={},
                                         in_room={}, event_map={}, event_info_dic={}, monster_tables={})

        # フロアレイアウト情報を格納
        self._decodeFloorLayout(toc=toc, decode_dict=decode_dict, res=res)

        # 各座標の玄室情報を格納
        self._decodeMapData(toc=toc, decode_dict=decode_dict, element_prefix='FIGHTS',
                            out_dic=res.in_room, data_bit_len=1, data_per_word=16, set_func=self._setBool)

        # 各座標のイベント番号を格納
        self._decodeMapData(toc=toc, decode_dict=decode_dict, element_prefix='SQREXTRA',
                            out_dic=res.event_map, data_bit_len=4, data_per_word=4, set_func=self._setInteger)

        # 各イベント番号のイベント種別を取得
        self._decodeEventType(toc=toc, decode_dict=decode_dict, out_dic=event_number_to_type)

        # イベントパラメタを格納
        self._decodeEventParams(toc=toc, decode_dict=decode_dict, event_type_dic=event_number_to_type, res=res)

        # モンスター出現テーブルを格納
        self._decodeMonsterTables(toc=toc, decode_dict=decode_dict, res=res)

        return res

    def decodeOneData(self, toc:WizardrySCNTOC, data: Any, index: int)->Optional[Any]:
        """シナリオデータファイル中の迷宮フロアデータを解析する

        Args:
            toc (WizardrySCNTOC): 目次情報
            data (Any): シナリオデータファイル情報
            index (int): 調査対象アイテムのインデクス

        Returns:
            Optional[Any]: 解析結果のオブジェクト, インデクスがレンジ外の場合, None
        """
        nr_items=toc.RECPERDK[modules.consts.ZMAZE] # フロア数

        if 0 > index or index >= nr_items:
            return None # 不正インデクス

        # 対象のアイテム情報開始オフセット位置(単位:バイト)を得る
        data_offset = calcDataEntryOffset(toc=toc, category=modules.consts.ZMAZE, item_len=MAZE_FLOOR_ENTRY_SIZE, index=index)

        # 解析対象データをunpackする
        decode_dict = getDecodeDict(data=data,layout=WizardryMazeFloorDataEntryDef,offset=data_offset)

        # unpackしたデータをpythonのオブジェクトに変換
        return self._dict2MazeFloorDataEntry(toc=toc, decode_dict=decode_dict)
