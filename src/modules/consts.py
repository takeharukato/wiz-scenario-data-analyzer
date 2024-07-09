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

# シナリオデータファイル名
DEFAULT_SCENARIO_DATA_FILE="SCENARIO.DATA"

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
