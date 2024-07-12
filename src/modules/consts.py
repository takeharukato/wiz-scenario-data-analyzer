#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file consts.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief 定数定義
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details 定数定義

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

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


#
# 定数定義
#
# Apple Pascal Operating System のディスクブロックサイズ(単位:バイト)
BLK_SIZ=512
# Wizardry キャッシュサイズ
WIZ_CACHE_SIZE=BLK_SIZ * 2
# シナリオデータファイル名
DEFAULT_SCENARIO_DATA_FILE="SCENARIO.DATA"
# データ解析結果不明
UNKNOWN_STRING="不明"
# ダイス情報の種類( nDt + a 形式)
DICE_DATA_ELEMENT_NR=3

# 方角
DIR_NORTH=0
DIR_EAST=1
DIR_SOUTH=2
DIR_WEST=3
DIR_VALID=(DIR_NORTH,DIR_EAST,DIR_SOUTH,DIR_WEST)

#
# シナリオ情報の目次
#
ZZERO="シナリオ情報"
ZMAZE="迷宮フロア情報"
ZENEMY="モンスター情報"
ZREWARD="報酬情報"
ZOBJECT="アイテム情報"
ZCHAR="キャラクター名簿"
ZSPCCHRS="モンスター/宝箱画像"
ZEXP="経験値表"

#
# 目次のインデクス番号から文字列キーへの変換テーブル
#
TOC_INDEX_TO_KEY:dict[int,str]={
    0:ZZERO,
    1:ZMAZE,
    2:ZENEMY,
    3:ZREWARD,
    4:ZOBJECT,
    5:ZCHAR,
    6:ZSPCCHRS,
    7:ZEXP
}

#
#迷宮フロア
#

#
# 1フロアの大きさ
#
FLOOR_WIDTH=20
FLOOR_HEIGHT=20

#
# 壁の種類
#
FLOOR_WALL_OPEN=0    # 壁はない
FLOOR_WALL_WALL=1    # 壁がある
FLOOR_WALL_DOOR=2    # ドアがある
FLOOR_WALL_HIDDEN=3  # シークレットドアがある

FLOOR_WALL_DIC:dict[int,str]={
    FLOOR_WALL_OPEN:"無",
    FLOOR_WALL_WALL:"壁",
    FLOOR_WALL_DOOR:"扉",
    FLOOR_WALL_HIDDEN:"秘",
}

# フロア当たりの設定可能イベント数
FLOOR_EVENTS_PER_FLOOR=16
# イベントパラメタ数
FLOOR_NR_EVENT_PARAMS=3
# フロア当たりのモンスター出現テーブル系統数
FLOOR_NR_MONSTER_TABLE_SERIES=3
#
# イベント種別
#
FLOOR_EVENT_NORMAL=0
FLOOR_EVENT_STAIRS=1
FLOOR_EVENT_PIT=2
FLOOR_EVENT_CHUTE=3
FLOOR_EVENT_SPINNER=4
FLOOR_EVENT_DARK=5
FLOOR_EVENT_TRANSFER=6
FLOOR_EVENT_OUCHY=7
FLOOR_EVENT_BUTTONZ=8
FLOOR_EVENT_ROCKWATE=9
FLOOR_EVENT_FIZZLE=10
FLOOR_EVENT_SCNMSG=11
FLOOR_EVENT_ENCOUNTE=12
FLOOR_EVENT_TO_STRING:dict[int,str]={
    FLOOR_EVENT_NORMAL:"床",
    FLOOR_EVENT_STAIRS:"階段",
    FLOOR_EVENT_PIT:"落とし穴",
    FLOOR_EVENT_CHUTE:"シュート",
    FLOOR_EVENT_SPINNER:"回転床",
    FLOOR_EVENT_DARK:"暗闇",
    FLOOR_EVENT_TRANSFER:"テレポート",
    FLOOR_EVENT_OUCHY:"落とし穴2",
    FLOOR_EVENT_BUTTONZ:"ボタン/エレベータ",
    FLOOR_EVENT_ROCKWATE:"石",
    FLOOR_EVENT_FIZZLE:"呪文無効化",
    FLOOR_EVENT_SCNMSG:"メッセージ",
    FLOOR_EVENT_ENCOUNTE:"固定モンスター",
}
#
# アイテム/モンスター情報共通
#
# モンスター種別
ENEMY_CLASS_DIC:dict[int,str]={
    0:"戦士系",
    1:"魔術師系",
    2:"僧侶系",
    3:"盗賊系",
    4:"未使用",
    5:"巨人系",
    6:"神話系",
    7:"竜系",
    8:"動物系",
    9:"リカント系",
    10:"不死系",
    11:"悪魔系",
    12:"昆虫系",
    13:"魔法生物系",
}
# キャラクタの職業
CHAR_CLASS_DIC:dict[int,str]={
    0:"戦士",
    1:"魔術師",
    2:"僧侶",
    3:"盗賊",
    4:"司教",
    5:"侍",
    6:"君主",
    7:"忍者",
}
# キャラクタの属性
CHAR_ALIGNMENT_DIC:dict[int,str]={
    0:"無属性",
    1:"善",
    2:"中立",
    3:"悪"
}
# 無属性
CHAR_ALIGNMENT_NO_ALIGN=0

# 装備可能職業文字列
CHAR_CLASS_EQUIP_STRING="FMPTBSLN"
# アイテム種別からアイテム種別名への変換テーブル
OBJ_TYPE_TO_STR:dict[int,str]={
    0:"武器",
    1:"鎧",
    2:"盾",
    3:"兜",
    4:"手甲",
    5:"特殊(装備対象外)",
    6:"その他",
}
# 抵抗属性,ブレス/呪文属性(WEPVSTYP3)のビット位置と意味
RESIST_BREATH_DIC:dict[int,str]={
    0:"無", # 抵抗なし, 無属性ブレス/呪文
    1:"火", # 火属性ブレス/呪文
    2:"冷", # 冷属性ブレス/呪文
    3:"毒", # 毒属性ブレス/呪文
    4:"吸", # ドレイン属性ブレス/呪文
    5:"石", # 石化抵抗
    6:"呪", # 呪文抵抗(呪文詠唱を取りやめさせる)
}
# 攻撃付与属性/能力・弱点(モンスター情報のSPPC)のビット位置と意味
SPPC_DIC:dict[int,str]={
    0:"石", # 石化
    1:"毒", # 毒
    2:"麻", # 麻痺
    3:"首", # クリティカル
    4:"眠", # 休眠可能(弱点)
    5:"逃", # 逃走可能
    6:"呼", # 仲間を呼ぶ
}
# 攻撃付与属性
SPPC_SPECIAL_ATTACK_DIC:dict[int,str]={
    0:"石", # 石化
    1:"毒", # 毒
    2:"麻", # 麻痺
    3:"首", # クリティカル
}

#
# モンスター情報
#

# 攻撃回数最大値
ENEMY_MAX_SWING_COUNT=7

# 弱点
SPPC_WEAK_POINT_DIC:dict[int,str]={
    4:"眠", # 休眠可能(弱点)
}

# 能力
SPPC_CAPABILITY_DIC:dict[int,str]={
    5:"逃", # 逃走可能
    6:"呼", # 仲間を呼ぶ
}
ITEM_SPECIAL_DIC:dict[int,str]={
    1:"能力値STRENGTHに1加算する",
    2:"能力値I.Q.に1加算する",
    3:"能力値PIETYに1加算する",
    4:"能力値VITALITYに1加算する",
    5:"能力値AGILITYに1加算する",
    6:"能力値LUCKに1加算する",
    7:"能力値STRENGTHから1減算する",
    8:"能力値I.Q.から1減算する",
    9:"能力値PIETYから1減算する",
    10:"能力値VITALITYから1減算する",
    11:"能力値AGILITYから1減算する",
    12:"能力値LUCKから1減算する",
    13:"年齢が20歳を超えていたら年齢を1歳減算する",
    14:"年齢を1歳加算する",
    15:"侍に転職する",
    16:"君主に転職する",
    17:"忍者に転職する",
    18:"GOLDに50,000加算する",
    19:"経験値に50,000加算する",
    20:"状態を喪失(LOST)にする",
    21:"状態を正常に変更,HPを全回復させ, 毒状態を解除する",
    22:"最大HPに1加算する",
    23:"パーティの全メンバーのHPを最大HPまで回復させる",
}
#
# 呪文用途(デバッグ用)
# (* 呪文種別(対象者選択時に使用): GENERIC(0 一般), PERSON(1 単体), GROUP(2 グループ) *)
# TSPEL012 = (GENERIC, PERSON, GROUP);
DBG_WIZ_SPELL_TYPES:dict[int,str]={
    0:"GENERIC",
    1:"PERSON",
    2:"GROUP"
}

# 呪文名(デバッグ用)
DBG_WIZ_SPELL_NAMES=(
    "NONAME",
    "HALITO",
    "MOGREF",
    "KATINO",
    "DUMAPIC",
    "DILTO",
    "SOPIC",
    "MAHALITO",
    "MOLITO",
    "MORLIS",
    "DALTO",
    "LAHALITO",
    "MAMORLIS",
    "MAKANITO",
    "MADALTO",
    "LAKANITO",
    "ZILWAN",
    "MASOPIC",
    "HAMAN",
    "MALOR",
    "MAHAMAN",
    "TILTOWAIT",
    "KALKI",
    "DIOS",
    "BADIOS",
    "MILWA",
    "PORFIC",
    "MATU",
    "CALFO",
    "MANIFO",
    "MONTINO",
    "LOMILWA",
    "DIALKO",
    "LATUMAPIC",
    "BAMATU",
    "DIAL",
    "BADIAL",
    "LATUMOFIS",
    "MAPORFIC",
    "DIALMA",
    "BADIALMA",
    "LITOKAN",
    "KANDI",
    "DI",
    "BADI",
    "LORTO",
    "MADI",
    "MABADI",
    "LOKTOFEIT",
    "MALIKTO",
    "KADORTO")
