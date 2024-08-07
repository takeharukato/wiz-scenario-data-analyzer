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
from typing import Optional
from typing import Iterator

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os

from dataclasses import dataclass

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import modules.consts
from modules.calcMisc import simple_round

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
    """ダイス型"""

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
class WizardryMazeFloorEventInfo:
    """迷宮フロアイベント情報"""

    event_type:int
    """イベント種別"""
    params:dict[int,int]
    """イベントパラメタ番号(0-2)からパラメタ値への辞書"""

    broken_reason:dict[int,bool]
    """無効なイベントの場合の原因(該当箇所がTrueになる, 被該当箇所は登録されない)"""

    positions:list[tuple[int,int]]
    """発生座標(X,Y)のリスト"""

    @property
    def is_enabled(self)-> bool:
        """有効なイベントの場合は, 真
        """
        return len(self.broken_reason) == 0

    @property
    def reason_string(self)->str:
        """無効な理由を表す文字列
        """
        if len(self.broken_reason) == 0:
            return modules.consts.OK_STRING
        return modules.consts.DELIMITER_COMMA.join([modules.consts.FLOOR_EVENT_BROKEN_REASON_DIC[id] for id in sorted(modules.consts.FLOOR_EVENT_BROKEN_REASON_DIC.keys()) if id in self.broken_reason and self.broken_reason[id]])

    @property
    def encounte_range(self)->Optional[tuple[int,int,int]]:
        """遭遇モンスターレンジを返す

        Returns:
            Optional[tuple[int, int, int]]: (遭遇回数, 最小モンスター番号, 最大モンスター番号)のタプル(戦闘イベントでない場合はNoneを返す)
        """
        if self.event_type != modules.consts.FLOOR_EVENT_ENCOUNTE:
            return None

        if 0 not in self.params or 1 not in self.params or 2 not in self.params:
            return None # 不正データ

        min = max = self.params[2]
        if self.params[1] > 1:
            max = self.params[2] + self.params[1] - 1

        return self.params[0],min,max

@dataclass
class WizardryMazeMonsterTableEntry:
    """モンスター出現テーブルエントリ"""

    number:int          # エントリの系統番号
    min_enemy:int       # MINENEMY 出現モンスター番号の最小値
    multiplier:int      # MULTWORS モンスター出現範囲の系統(0からWORSE01 - 1) * MULTWORS 分最小モンスター番号に加算する
    max_series:int # WORSE01 使用するモンスター出現範囲の系統の最大値
    monster_range:int   # RANGE0N 出現モンスターの範囲(0 から RANGE0N - 1 までの範囲の乱数でモンスター番号を決定する)
    inc_series_percentage:int # PERCWORS モンスター出現範囲の系統を加算する確率 系統番号がWORSE01以上の場合は加算しない

    @property
    def min(self)->int:
        """最小モンスター番号を得る"""
        return self.min_enemy + (self.number) * self.multiplier

    @property
    def max(self)->int:
        """最大モンスター番号を得る"""
        return self.min + self.monster_range - 1

@dataclass
class WizardryMazeFloorDataEntry:
    """迷宮フロア情報"""

    wall_info_west:dict[tuple[int,int],int]
    """座標(x,y)を表すタプルから西側の壁の種類への辞書"""
    wall_info_south:dict[tuple[int,int],int]
    """座標(x,y)を表すタプルから南側の壁の種類への辞書"""
    wall_info_east:dict[tuple[int,int],int]
    """座標(x,y)を表すタプルから東側の壁の種類への辞書"""
    wall_info_north:dict[tuple[int,int],int]
    """座標(x,y)を表すタプルから北側の壁の種類への辞書"""
    in_room:dict[tuple[int,int],bool]
    """座標(x,y)を表すタプルから当該座標が玄室内にあること確認する辞書(FIGHTS)"""
    event_map:dict[tuple[int,int], int]
    """座標(x,y)を表すタプルから当該座標から当該座標で発生するイベントのイベント番号への辞書(SQREXTRA)"""
    event_info_dic:dict[int, WizardryMazeFloorEventInfo]
    """イベント番号からイベント情報への辞書"""
    monster_tables:dict[int,WizardryMazeMonsterTableEntry]
    """モンスター出現テーブルの辞書 モンスター出現系統番号からテーブルへの辞書"""

    depth:int
    """階層"""

    event_to_coord:dict[int,list[tuple[int,int]]]
    """イベント番号から発生座標へのマップ"""

    def getWallInfo(self, x:int, y:int, dir:int)->int:
        """壁の種類を返却する

        Args:
            x (int): X座標
            y (int): Y座標
            dir (int): 確認する向き
                - DIR_NORTH 北
                - DIR_EAST  東
                - DIR_SOUTH 南
                - DIR_WEST  西

        Returns:
            int: 壁の種類
                - FLOOR_WALL_OPEN      通路
                - FLOOR_WALL_WALL=1    壁
                - FLOOR_WALL_DOOR=2    ドア
                - FLOOR_WALL_HIDDEN=3  シークレットドア
        """

        dic_map:dict[int,dict[tuple[int,int],int]]={
            modules.consts.DIR_NORTH:self.wall_info_north,
            modules.consts.DIR_EAST:self.wall_info_east,
            modules.consts.DIR_SOUTH:self.wall_info_south,
            modules.consts.DIR_WEST:self.wall_info_west
        }

        pos=(x,y) # 確認対象座標

        if dir not in dic_map: # 不正な方角の場合
            return -1

        dic = dic_map[dir] # マップを取得
        if pos not in dic: # 不正座標の場合
            return -1

        return dic[pos] # 壁の情報を返す

    @property
    def monster_series(self)->Iterator[tuple[int, int, int, int, float, float]]:
        """モンスター出現範囲を返すイテレータ
            ENCOUNTR手続きを元に実装
        Yields:
            Iterator[tuple[int, int, int, int, float, float]]: テーブルインデクス, テーブル内のモンスター出現系列番号, モンスター出現範囲最小値, 最大値, モンスター出現系列上昇確率, 本系列の発生確率
        """
        def series_generator():
            """モンスター出現テーブルの範囲を返す"""
            """
                    if self.item_maxtimes > idx:
                        this_percentage = simple_round(remain_percentage - ( (remain_percentage) / 100 ) * ( (self.item_percbigr) / 100 ) * 100, ndigits=1)
                    else:
                        this_percentage = simple_round(remain_percentage,ndigits=1)
                    remain_percentage -= this_percentage
            """

            for idx in range(modules.consts.FLOOR_NR_MONSTER_TABLE_SERIES): # 各系統について
                assert idx in self.monster_tables, f"{idx} not found"
                entry = self.monster_tables[idx] # 出現テーブルエントリを参照
                if 0 >= entry.inc_series_percentage or 0 >= entry.max_series: # 系列が一意に決定する場合
                    yield (idx, 0, entry.min_enemy, entry.min_enemy + entry.monster_range - 1, 0, 100) # 最小レンジ
                else: # 系列変更を伴う場合

                    remain_percentile = 100 # 残りパーセンタイル
                    for series_idx in range(0,entry.max_series+1): # 乗数値の最大係数を取得

                        if entry.max_series > series_idx: # 上昇する余地がある場合

                            # 上昇確率の余事象の発生確率(上昇しない確率)を算出し, 本系列の発生確率とする
                            this_percentile = simple_round(remain_percentile - ( (remain_percentile) / 100 ) * ( (entry.inc_series_percentage) / 100 ) * 100, ndigits=2)
                            # モンスター番号加算確率
                            this_inc_percentage = entry.inc_series_percentage
                        else:
                            # 上昇確率の余事象の発生確率(上昇しない確率)を算出し, 本系列の発生確率とする
                            this_percentile = simple_round(remain_percentile, ndigits=2)
                            # モンスター番号加算確率
                            this_inc_percentage = 0

                        remain_percentile -= this_percentile # 残りの確率
                        multiplied_base = entry.multiplier * series_idx # 最小モンスター番号加算値
                        yield (idx, series_idx, entry.min_enemy + multiplied_base,entry.min_enemy + multiplied_base + entry.monster_range - 1, this_inc_percentage, this_percentile)
            return
        return series_generator()

    @property
    def min_monster(self)-> int:
        """最小モンスター値"""
        return min([self.monster_tables[idx].min_enemy for idx in self.monster_tables.keys()])

    @property
    def max_monster(self)-> int:
        """最大モンスター値

        """
        # モンスター出現テーブル中の最大モンスター番号を返す
        return max([ max for _idx, _sub_idx, _min, max, _chg_ratio, _this_ratio in self.monster_series])

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

    follows:set[tuple[int,int]]
    """後続につくモンスターの番号と確率のタプルの集合"""
    emergence_floor:set[int]
    """出現フロア"""

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
    has_item_value:int
    """アイテム有無を表す数値"""
    reward_param:dict[int,int]
    """報酬情報0-6の内容(インデクス->値への辞書)"""

    @property
    def gold_range_tuple(self)->Iterator[tuple[float, int, int]]:
        """総獲得Gold値の範囲のイテレータを返す

        Returns:
            tuple[int, int,int]: 獲得確率, 獲得最小値, 獲得最大値
        報酬情報一つ当たりの取得金額 =
            報酬情報の報酬額ダイス1(TRIES D AVEAMT + MINADD のダイスで決定)
          * 報酬情報の報酬乗数値(MULTX)
          * 報酬情報の報酬額ダイス2(TRIES2 D AVEAMT2 + MINADD2 のダイスで決定)
        """

        if self.has_item: # アイテム取得の場合
            return iter([(0,0,0)])  # 0を返す

        # 報酬情報の報酬額ダイス1
        dice1=dice_type(self.gold_tries, self.gold_aveamt, self.gold_minadd)
        # 報酬情報の報酬額ダイス2
        dice2=dice_type(self.gold_tries2, self.gold_aveamt2, self.gold_minadd2)

        # 最小金額
        min = dice1.min * self.gold_multx * dice2.min
        # 最大金額
        max = dice1.max * self.gold_multx * dice2.max

        return iter([(100, min, max)])

    @property
    def item_range_tuple(self)->Iterator[tuple[float, int, int]]:
        """獲得アイテムの範囲のイテレータを返す

        Returns:
            tuple[float, int,int]: 獲得確率, 獲得アイテム番号最小値, 獲得アイテム番号最大値

        取得するアイテムのアイテム番号 = アイテム番号最小値(MININDX) +
        アイテム出現レンジ基数(CHARIII) * アイテム出現値乗数(MFACTOR)
        + アイテム番号を算出する際に使用するダイス(ダイスの面数:RANGE) の値(1 D RANGE + 1 )

        """

        def item_range_generator():

            # アイテム番号算出ダイス
            dice=dice_type(0, 0, 0)
            if self.item_range > 1:
                dice=dice_type(1, self.item_range, 1)

            if self.item_maxtimes == 0 or self.item_percbigr == 0:

                #
                # 補正値がない場合
                #

                # 最小アイテム番号
                min = self.item_minindx + dice.min

                # 最大アイテム番号
                max = self.item_minindx + dice.max

                yield 100, min, max

            else:

                # 残りパーセンタイル
                remain_percentile=100
                for idx in range(self.item_maxtimes+1):

                    # アイテムレンジ基数(CHARIII)
                    char_iii = idx

                    # 補正値を算出(補正値 = アイテムレンジ基数 *  アイテム出現値乗数)
                    mod_val =  char_iii * self.item_mfactor

                    # 最小アイテム番号
                    min = self.item_minindx + mod_val + dice.min

                    # 最大アイテム番号
                    max = self.item_minindx + mod_val + dice.max

                    # アイテム出現パーセンタイル
                    if self.item_maxtimes > idx:
                        this_percentile = simple_round(remain_percentile - ( (remain_percentile) / 100 ) * ( (self.item_percbigr) / 100 ) * 100, ndigits=1)
                    else:
                        this_percentile = simple_round(remain_percentile,ndigits=1)
                    remain_percentile -= this_percentile # 残りパーセンタイルの更新
                    yield this_percentile, min, max


            return

        if not self.has_item: # アイテム取得スロットでない場合
            return iter([(0,0,0)])

        return item_range_generator()

    @property
    def gold_tries(self)->int:
        """ダイスを振る回数(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 0 not in self.reward_param:
            return 0  # パラメタがない

        return self.reward_param[0]

    @property
    def gold_aveamt(self)->int:
        """ダイスの面数(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 1 not in self.reward_param:
            return 0 # パラメタがない

        return self.reward_param[1]

    @property
    def gold_minadd(self)->int:
        """ダイスの加算値(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 2 not in self.reward_param:
            return 0 # パラメタがない

        return self.reward_param[2]

    @property
    def gold_multx(self)->int:
        """報酬補正乗数(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 3 not in self.reward_param:
            return 0 # パラメタがない

        return self.reward_param[3]

    @property
    def gold_tries2(self)->int:
        """ダイスを振る回数2(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 4 not in self.reward_param:
            return 0  # パラメタがない

        return self.reward_param[4]

    @property
    def gold_aveamt2(self)->int:
        """ダイスの面数2(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 5 not in self.reward_param:
            return 0 # パラメタがない

        return self.reward_param[5]

    @property
    def gold_minadd2(self)->int:
        """ダイスの加算値(お金の場合)"""

        if self.has_item:
            return 0 # お金による報酬でない

        if 6 not in self.reward_param:
            return 0 # パラメタがない

        return self.reward_param[6]

    @property
    def item_minindx(self)->int:
        """最小アイテム番号(アイテムの場合)"""

        if not self.has_item:
            return 0 # アイテム報酬でない

        if 0 not in self.reward_param:
            return 0 # パラメタがない

        return self.reward_param[0]

    @property
    def item_mfactor(self)->int:
        """n番目に見つけたアイテムの場合, 報酬で設定されている最小アイテム番号にかける乗数(アイテムの場合)"""

        if not self.has_item:
            return 0 # アイテム報酬でない

        if 1 not in self.reward_param:
            return 0 # パラメタがない

        return self.reward_param[1]

    @property
    def item_maxtimes(self)->int:
        """宝箱から取得できる最大アイテム獲得数(アイテムの場合)"""

        if not self.has_item:
            return 0 # アイテム報酬でない

        if 2 not in self.reward_param:
            return 0 # パラメタがない

        return self.reward_param[2]

    @property
    def item_range(self)->int:
        """アイテム番号算出時に使用するダイスの面数(アイテムの場合)"""

        if not self.has_item:
            return 0 # アイテム報酬でない

        if 3 not in self.reward_param:
            return 0 # パラメタがない

        return self.reward_param[3]

    @property
    def item_percbigr(self)->int:
        """アイテム取得確率(アイテムの場合)"""

        if not self.has_item:
            return 0 # アイテム報酬でない

        if 4 not in self.reward_param:
            return 0 # パラメタがない

        return self.reward_param[4]

@dataclass
class WizardryRewardDataEntry:
    in_chest:bool
    """宝箱を出すことを表す真偽値(真の場合は, 宝箱を出す)"""
    in_chest_value:int
    """宝箱を出すことを表す真偽値の値"""
    trap_type_value:int
    """罠の種別を表すビットマップ"""
    reward_count_value:int
    """報酬の数"""
    rewards:dict[int,WizardryRewardInfo]
    """報酬詳細情報"""

    @property
    def trap_string(self)->str:
        """罠の一覧を返す"""

        candidate_traps:list[str]=[] # 罠の候補を初期化する
        trap_bit_len = len(modules.consts.REWARD_TRAP_DIC) # 有効なビット数を得る
        for shift in range(trap_bit_len): # 各ビットについて
            if self.trap_type_value & (1 << shift): # 対象のビットが立っていたら
                candidate_traps += modules.consts.REWARD_TRAP_DIC[shift] # 罠の候補を加える

        return modules.consts.DELIMITER_COMMA.join(candidate_traps)

@dataclass
class WizardryMessageDataEntry:
    """メッセージデータエントリ"""

    num:int
    """メッセージ開始番号"""
    lines:list[str]
    """メッセージの内容"""

@dataclass
class WizardryMessageData:
    """メッセージデータ"""

    messages:dict[int,WizardryMessageDataEntry]
    """メッセージ番号からメッセージへの辞書"""

    msg_to_pos:dict[int,tuple[int,int,int]]
    """メッセージ番号から発生座標への辞書"""
    pos_to_msg:dict[tuple[int,int,int],int]
    """発生座標からメッセージ番号への辞書"""
    def numberInMessages(self, number:int)->tuple[bool,int,int]:
        """メッセージ番号に対応するメッセージが存在することを確認する

        Args:
            number (int): メッセージ番号

        Returns:
            tuple[bool, int, int]: (メッセージの妥当性の真偽値, メッセージ番号, オフセット行)を返す
        """
        if len(self.messages) == 0:
            return True,number,0 # メッセージの存在を仮置きする

        if number in self.messages:
            return True,number,0 # メッセージの先頭から表示する場合

        #
        # メッセージファイル内にない場合
        #
        max_num = max(self.messages.keys())
        max_lines = max_num + len(self.messages[max_num].lines)
        if number >= max_lines:
            return False,0,0

        #
        # メッセージの途中から表示する場合
        #
        candidate=number
        while candidate >= 0 and candidate not in self.messages:
            candidate -= 1
            if candidate in self.messages:
                this_msg=self.messages[candidate]
                offset = number - candidate
                assert len(this_msg.lines) > offset, f"Invalid index {offset} len=({len(this_msg.lines)})"
                return True, candidate, offset

        return False,0,0

    def getOneLineMessage(self, number:int)->str:
        """メッセージを空白で区切って一行で返す

        Args:
            number (int): メッセージ番号

        Returns:
            str: メッセージ文字列
        """
        if len(self.messages) == 0:
            return modules.consts.UNKNOWN_STRING # 該当するメッセージがない
        does_exist,idx,offset = self.numberInMessages(number=number)
        if not does_exist:
            return modules.consts.UNKNOWN_STRING # 該当するメッセージがない

        assert idx in self.messages, f"Invalid index:{idx}"
        # メッセージを返す
        return modules.consts.DELIMITER_SPC.join(self.messages[idx].lines[offset:])

@dataclass
class WizardryCharImgDataEntry:
    """高解像度表示モード用文字データ"""
    bitmap:dict[int,int]
    """ビットマップ(7x8ドット)"""

@dataclass
class WizardryCharImgData:
    """高解像度表示モード用文字データ"""

    normal_bitmap:dict[int,WizardryCharImgDataEntry]
    """通常文字"""
    cemetary_bitmap:dict[int,WizardryCharImgDataEntry]
    """全滅時文字"""
    def index_to_char(self, index:int)->str:
        """インデクス番号から文字を返す

        Args:
            index (int): インデクス番号

        Returns:
            str: 文字を表す文字列
        """
        if 0 > index or index >= modules.consts.CHARIMG_PER_CHARSET:
            return modules.consts.UNDEFINED_STRING # 未定義

        char_code = index + modules.consts.CHARIMG_CH_CODE_START # 空白文字から開始
        return chr(char_code) # 文字を返す

    def char_to_index(self, char:str)->int:
        """文字からキャラクタセット配列のインデックスを返す

        Args:
            char (str): 文字を表す文字列

        Returns:
            int: インデクス
        """
        if len(char) != 0:
            return 0 # 0を返す
        char_code = ord(char)
        if char_code >= (modules.consts.CHARIMG_CH_CODE_START + modules.consts.CHARIMG_PER_CHARSET):
            return 0 # 0を返す
        return char_code - modules.consts.CHARIMG_CH_CODE_START

@dataclass
class WizardryPicDataEntry:
    """モンスター/宝箱画像"""

    raw_data:list[int]
    """生データ"""
    bitmap_info:dict[tuple[int,int],int]
    """書き込みデータ"""
    color_info:dict[tuple[int,int],int]
    """描画用データ"""

@dataclass
class WizardryExpTblClassEntry:
    """職業ごとの経験値表情報"""

    exp_table:dict[int,int]
    """次のレベルまでの経験値"""

@dataclass
class WizardryExpTblDataEntry:
    """経験値表情報"""

    exp_table:dict[int,WizardryExpTblClassEntry]
    """職業番号から経験値テーブルへの辞書"""

@dataclass
class WizardrySpellNameTblEntry:
    """呪文名情報"""

    has_delimiter:bool
    """呪文レベルの区切りの場合は真"""
    name:str
    """呪文名"""
    spell_level:int
    """呪文レベル"""

@dataclass
class WizardrySpellTblDataEntry:
    """呪文名情報"""

    tables:dict[str,dict[int,list[WizardrySpellNameTblEntry]]]
    """呪文種別から呪文名情報への辞書"""
