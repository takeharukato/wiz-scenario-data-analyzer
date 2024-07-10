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
