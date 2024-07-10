#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file datadef.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief データクラス定義
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details データクラス定義

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
from dataclasses import dataclass

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@dataclass
class WizardrySCNTOC:
    """目次情報"""
    game_name:str
    """シナリオ名"""
    RECPER2B:dict[str,int]
    """キャッシュ領域( 1KiB= 2 Block (2B) (512Byte x 2 Byte) )に格納可能なデータ数"""
    RECPERDK:dict[str,int]
    """最大データ数"""
    BLOFF:dict[str,int]
    """オフセットブロック数(単位:ブロック)"""
    RACE:dict[int,str]
    """種族名"""
    STATUS:dict[int,str]
    """状態名"""
    ALIGN:dict[int,str]
    """属性(アラインメント)名"""
    SPELLHSH:dict[int,int]
    """呪文ハッシュ値"""
    SPELLGRP:dict[int,int]
    """呪文グループ"""
    SPELL012:dict[int,int]
    """呪文の対象者選択方式"""

@dataclass
class dice_type:
    trial:int
    """ダイスを振る回数(nDt+aのn)"""
    factor:int
    """ダイスの面数(nDt+aのt)"""
    add_val:int
    """ダイスの補正値(nDt+aのa)"""

@dataclass
class WizardryMonsterDataEntry:
    """モンスター情報"""

    name_unknown:str
    """不確定名称"""
    plural_name_unknown:str
    """不確定名称複数形"""
    name:str
    """名前"""
    plural_name:str
    """名前複数形"""
    pic:int
    """グラフィック番号"""
    calc1:dice_type
    """出現数算出ダイス"""
    hprec:dice_type
    """HP算出ダイス"""
    cls:int
    """モンスター種別"""
    ac:int
    """アーマクラス"""
    max_swing_count:int
    """最大攻撃回数"""
    damage_dices:dict[int,dice_type]
    """各攻撃回でのダメージダイス"""
    exp_amount:int
    """獲得経験値"""
    drain_amount:int
    """ドレインレベル値"""
    heal_pts:int
    """リジェネレレーション値"""
    reward1:int
    """報酬1"""
    reward2:int
    """報酬2"""
    enemy_team:int
    """後続モンスターのモンスター番号"""
    team_percentage:int
    """後続モンスターの出現率"""
    mage_spells:int
    """魔術師呪文レベル"""
    priest_spells:int
    """僧侶呪文レベル"""
    unique:int
    """遭遇回数制限"""
    breathe_value:int
    """ブレス種別値"""
    breathe:str
    """ブレス種別"""
    unaffect_ratio:int
    """呪文無効化率"""
    wepvsty3_value:int
    """抵抗特性値"""
    resist_dic:dict[int,str]
    """抵抗特性"""
    sppc_value:int
    """攻撃属性値"""
    special_attack_dic:dict[int,str]
    """攻撃属性"""
    weak_point_dic:dict[int,str]
    """弱点"""
    capability_dic:dict[int,str]
    """能力"""
