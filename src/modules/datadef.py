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
    CLASS_NAME:dict[int,str]
    """職業名"""
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
    @property
    def name(self)->str:
        """ダイス文字列を返す"""
        if self.trial == 0 or self.factor == 0:
            return f"{self.add_val}" if self.add_val != 0 else f"0"

        return f"{self.trial}D{self.factor}+{self.add_val}" if self.add_val != 0 else f"{self.trial}D{self.factor}"

    @property
    def min(self)->int:
        """ダイスの最小値を返す"""
        if self.trial == 0 or self.factor == 0:
            return self.add_val
        return self.trial + self.add_val

    @property
    def max(self)->int:
        """ダイスの最大値を返す"""
        return self.trial * self.factor + self.add_val

    @property
    def range(self)->str:
        """ダイスの値範囲文字列を返す"""
        return f"{self.min}--{self.max}"

@dataclass
class wiz_long_type:
    low:int
    """下位4桁(0-9999)"""
    mid:int
    """中位4桁(10,000-19,999)"""
    high:int
    """上位4桁(100,000,000-999,900,000,000)"""

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
    enemy_class_value:int
    """モンスター種別値"""
    enemy_class_str:str
    """モンスター種別名"""
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

@dataclass
class WizardryItemDataEntry:
    """アイテム情報"""
    name:str
    """名称"""
    name_unknown:str
    """不確定名称"""
    obj_type_value:int
    """アイテム種別値"""
    obj_type_string:str
    """アイテム種別文字列"""
    alignment_value:int
    """属性(アラインメント)値"""
    alignment_string:str
    """属性(アラインメント)文字列"""
    cursed:bool
    """呪いの有無"""
    special_value:int
    """スペシャルパワー分類番号"""
    change_to_value:int
    """使用後のアイテム番号"""
    change_percentage:int
    """使用後に変化する確率"""
    price_value:int
    """鑑定/売却価格値"""
    stock_value:int
    """商店の在庫"""
    spell_power_value:int
    """使用時に発動する呪文番号"""
    class_use_value:int
    """装備可能な職業を表すビットマップ"""
    class_use_string:str
    """装備可能な職業を表す文字列"""
    class_use_dic:dict[int,str]
    """装備可能な職業を表す辞書"""
    heal_pts:int
    """リジェネレレーション値"""
    wepvsty2_value:int
    """防御特性を表すビットマップ値"""
    prot_dic:dict[int,str]
    """防御特性を表す辞書"""
    wepvsty3_value:int
    """抵抗特性を表すビットマップ値"""
    resist_dic:dict[int,str]
    """抵抗特性を表す辞書"""
    ac_mod_value:int
    """アーマクラス補正値"""
    wephitmd_value:int
    """戦闘スキル(命中)補正値"""
    wephpdam:dice_type
    """攻撃ダイス"""
    swing_count_value:int
    """攻撃回数値"""
    critical_hit:bool
    """クリティカルヒット付与の有無"""
    wepvstyp_value:int
    """倍打特性を表すビットマップ値"""
    purpose_dic:dict[int,str]
    """倍打特性を表す辞書"""

@dataclass
class WizardryRewardInfo:
    percentage:int
    """報酬獲得確率"""
    has_item:bool
    """アイテムを含む場合は真"""
    reward_param:dict[int,int]
    """報酬情報0-6の内容(インデクス->値への辞書)"""

    @property
    def gold_tries(self)->int:
        """ダイスを振る回数(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 0 not in self.reward_param:
            return 0
        return self.reward_param[0]

    @property
    def gold_aveamt(self)->int:
        """ダイスの面数(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 1 not in self.reward_param:
            return 0

        return self.reward_param[1]

    @property
    def gold_minadd(self)->int:
        """ダイスの加算値(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 2 not in self.reward_param:
            return 0

        return self.reward_param[2]

    @property
    def gold_multx(self)->int:
        """報酬補正乗数(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 3 not in self.reward_param:
            return 0

        return self.reward_param[3]

    @property
    def gold_tries2(self)->int:
        """ダイスを振る回数2(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 4 not in self.reward_param:
            return 0

        return self.reward_param[4]

    @property
    def gold_aveamt2(self)->int:
        """ダイスの面数2(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 5 not in self.reward_param:
            return 0

        return self.reward_param[5]

    @property
    def gold_minadd2(self)->int:
        """ダイスの加算値(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 6 not in self.reward_param:
            return 0

        return self.reward_param[6]

    @property
    def item_minindx(self)->int:
        """最小アイテム番号(アイテムの場合)"""

        if not self.has_item:
            return 0 # アイテム報酬でない

        if 0 not in self.reward_param:
            return 0

        return self.reward_param[0]

    @property
    def item_mfactor(self)->int:
        """n番目に見つけたアイテムの場合, 報酬で設定されている最小アイテム番号にかける乗数(アイテムの場合)"""

        if not self.has_item:
            return 0 # アイテム報酬でない

        if 1 not in self.reward_param:
            return 0

        return self.reward_param[1]

    @property
    def item_maxtimes(self)->int:
        """宝箱から取得できる最大アイテム獲得数(アイテムの場合)"""

        if not self.has_item:
            return 0 # アイテム報酬でない

        if 2 not in self.reward_param:
            return 0

        return self.reward_param[2]

    @property
    def item_range(self)->int:
        """アイテム番号算出時に使用するダイスの面数(アイテムの場合)"""

        if not self.has_item:
            return 0 # アイテム報酬でない

        if 3 not in self.reward_param:
            return 0

        return self.reward_param[3]

    @property
    def item_percbigr(self)->int:
        """アイテム取得確率(アイテムの場合)"""

        if not self.has_item:
            return 0 # アイテム報酬でない

        if 4 not in self.reward_param:
            return 0

        return self.reward_param[4]

@dataclass
class WizardryRewardDataEntry:
    in_chest:bool
    """宝箱を出すか"""
    trap_type_value:int
    """罠の種別を表すビットマップ"""
    reward_count_value:int
    """報酬の数"""
    rewards:dict[int,WizardryRewardInfo]
    """報酬詳細情報"""