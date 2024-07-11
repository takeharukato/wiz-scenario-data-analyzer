#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file scnInfoImpl.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報実装部
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報実装クラス

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
from typing import Any
from typing import TextIO

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.datadef import WizardrySCNTOC, WizardryMazeFloorDataEntry, WizardryMazeFloorEventInfo, WizardryMonsterDataEntry, WizardryItemDataEntry, WizardryRewardDataEntry, WizardryRewardInfo
from modules.scnInfo import scnInfo
from modules.TOCDecoder import TOCDecoder
from modules.mazeFloorDecoder import mazeFloorDecoder
from modules.monsterDecoder import monsterDecoder
from modules.itemDecoder import itemDecoder
from modules.rewardDecoder import rewardDecoder
from modules.utils import property_dic_to_string,value_to_string
import modules.consts

class scnInfoImpl(scnInfo):

    _scenario:Any
    """シナリオ情報ファイルのメモリイメージ"""
    _toc:WizardrySCNTOC
    """目次情報"""
    _floors:dict[int, WizardryMazeFloorDataEntry]
    """迷宮フロア情報"""
    _monsters:dict[int,WizardryMonsterDataEntry]
    """モンスター情報"""
    _items:dict[int,WizardryItemDataEntry]
    """アイテム情報"""
    _rewards:dict[int,WizardryRewardDataEntry]
    """報酬情報"""

    def __init__(self, scenario:Any) -> None:

        self._scenario=scenario
        self._floors={}
        self._monsters={}
        self._items={}
        self._rewards={}
        return

    def _readTOC(self, data:Any)->None:
        """目次情報を読込む

        Args:
            data (Any): シナリオデータ
        """

        toc_decoder=TOCDecoder(data=data)
        toc_decoder.decodeData(data=data, offset=0)
        self._toc = toc_decoder.toc
        return

    def _readFloorTable(self, data:Any)->None:
        decoder=mazeFloorDecoder()
        nr_floors=self.toc.RECPERDK[modules.consts.ZMAZE]
        for idx in range(nr_floors):
            floor=decoder.decodeOneData(toc=self.toc, data=data, index=idx)
            if isinstance(floor, WizardryMazeFloorDataEntry):
                self._floors[idx]=floor

        return

    def _readMonsterTable(self, data:Any)->None:
        decoder=monsterDecoder()
        nr_monsters=self.toc.RECPERDK[modules.consts.ZENEMY]
        for idx in range(nr_monsters):
            monster=decoder.decodeOneData(toc=self.toc, data=data, index=idx)
            if isinstance(monster, WizardryMonsterDataEntry):
                self._monsters[idx]=monster

        return

    def _readItemTable(self, data:Any)->None:
        decoder=itemDecoder()
        nr_items=self.toc.RECPERDK[modules.consts.ZOBJECT]
        for idx in range(nr_items):
            item=decoder.decodeOneData(toc=self.toc, data=data, index=idx)
            if isinstance(item, WizardryItemDataEntry):
                self._items[idx]=item

        return

    def _readRewardTable(self, data:Any)->None:
        decoder=rewardDecoder()
        nr_rewards=self.toc.RECPERDK[modules.consts.ZREWARD]
        for idx in range(nr_rewards):
            reward=decoder.decodeOneData(toc=self.toc, data=data, index=idx)
            if isinstance(reward, WizardryRewardDataEntry):
                self._rewards[idx]=reward

        return

    def _plainOneDumpMonster(self, index:int, data:Any, fp: TextIO)->None:
        """格納しているモンスター情報をテキストとして出力する

        Args:
            index (int): インデクス
            data (Any): 表示対象データ
            fp (TextIO): 出力先.
        """

        if not isinstance(data, WizardryMonsterDataEntry):
            return

        # TODO: ZREWARDの報酬情報と統合して, どのアイテムを何%の確率で出すのかを表示すること
        #       ZMAZEの出現テーブルに基づいて, 出現階層, 出現率, 後続のみ出現を表示すること
        name=data.name
        names=data.plural_name
        unknown_name=data.name_unknown
        unknown_names=data.plural_name_unknown
        pic=data.pic
        nr_member=f"{data.calc1.name} ({data.calc1.min}--{data.calc1.max})"
        hp_dice=f"{data.hprec.name} ({data.hprec.min}--{data.hprec.max})"
        enemy_class=f"{modules.consts.ENEMY_CLASS_DIC[data.enemy_class_value]} ({data.enemy_class_value})" if data.enemy_class_value in modules.consts.ENEMY_CLASS_DIC else f"{modules.consts.UNKNOWN_STRING} ({data.enemy_class_value})"
        ac=f"{data.ac}"
        swing_count=f"{data.max_swing_count}"
        dmg_dice_table=",".join([data.damage_dices[key].name for key in sorted(data.damage_dices.keys()) if data.damage_dices[key].trial != 0 or data.damage_dices[key].add_val != 0 ])
        exp=f"{data.exp_amount}"
        drain=f"{data.drain_amount}"
        heal_pts=f"{data.heal_pts}"
        reward1=f"{data.reward1}"
        reward2=f"{data.reward2}"
        follower=self._monsters[data.enemy_team].name if data.enemy_team in self._monsters else modules.consts.UNKNOWN_STRING
        follows=f"{follower} ({data.enemy_team})" if data.team_percentage != 0 else f""
        follow_percentage=f"{data.team_percentage}"

        mage_spell=f"{data.mage_spells}"
        pri_spell=f"{data.priest_spells}"
        uniq=f"無制限 ({data.unique})" if data.unique == -1 else f"{data.unique - -1} 回 ({data.unique})"
        breathe=f"{data.breathe} ({hex(data.breathe_value)} = {bin(data.breathe_value)})" if data.breathe_value != 0 else f""
        unaffect_ratio=f"{data.unaffect_ratio}"
        resist_set=property_dic_to_string(dic=data.resist_dic)
        resist_string=f"{resist_set} ({hex(data.wepvsty3_value)} = {bin(data.wepvsty3_value)})" if data.wepvsty3_value != 0 else f""
        sppc_string=f"{data.sppc_value} ({hex(data.sppc_value)} = {bin(data.sppc_value)})"
        special_attack_string = property_dic_to_string(dic=data.special_attack_dic)
        weak_points_string = property_dic_to_string(dic=data.weak_point_dic)
        capability_string = property_dic_to_string(dic=data.capability_dic)
        print(f"|{index}|{name}|{names}|{unknown_name}|{unknown_names}|{pic}|{nr_member}|{hp_dice}|"
              f"{enemy_class}|{ac}|{swing_count}|{dmg_dice_table}|{exp}|{drain}|{heal_pts}|{reward1}|{reward2}|"
              f"{follows}|{follow_percentage} %|{mage_spell}|{pri_spell}|{uniq}|{breathe}|"
              f"{unaffect_ratio} %|{resist_string}|{special_attack_string}|{weak_points_string}|"
              f"{capability_string}|{sppc_string}|",file=fp)
        return

    def _plainOneDumpItem(self, index:int, data:Any, fp: TextIO)->None:
        """格納しているアイテム情報をテキストとして出力する

        Args:
            index (int): インデクス
            data (Any): 表示対象データ
            fp (TextIO): 出力先.
        """

        if not isinstance(data, WizardryItemDataEntry):
            return

        # TODO: ZREWARDの報酬情報と統合して, どのモンスターが何%の確率で出すのかを表示すること
        item_type_string=f"{data.obj_type_string} ({value_to_string(data.obj_type_value)})"
        if data.alignment_value == modules.consts.CHAR_ALIGNMENT_NO_ALIGN:
            alignment_string=f"無属性 ( {data.alignment_string} ({value_to_string(data.alignment_value)}) )"
        else:
            alignment_string=f"{data.alignment_string} ({value_to_string(data.alignment_value)})"
        cursed_string=f"呪" if data.cursed else ""
        special_pwr_string=f"{modules.consts.ITEM_SPECIAL_DIC[data.special_value]} ({data.special_value})" if data.special_value in modules.consts.ITEM_SPECIAL_DIC else f"{modules.consts.UNKNOWN_STRING} ({data.special_value})" if data.special_value > 0 else f""
        change_to_string=f"{self._items[data.change_to_value].name} ({data.change_to_value})" if data.change_percentage > 0 and data.change_to_value in self._items else f""
        change_percentage_string=f"{data.change_percentage}"
        price_string=f"{data.price_value}"
        stock_string=f"無制限 ({data.stock_value})" if 0 > data.stock_value else f"{data.stock_value}"
        spell_power_string = f"{modules.consts.DBG_WIZ_SPELL_NAMES[data.spell_power_value]} ({data.spell_power_value})" if data.spell_power_value > 0 and len(modules.consts.DBG_WIZ_SPELL_NAMES) > (data.spell_power_value) else f""
        class_equip_string = f"{data.class_use_string} ({value_to_string(data.class_use_value)})"
        heal_pts_string=f"{data.heal_pts}"
        prot_string = f"{property_dic_to_string(dic=data.prot_dic)} ({value_to_string(data.wepvsty2_value)})" if data.wepvsty2_value != 0 else f""
        resist_string = f"{property_dic_to_string(dic=data.resist_dic)} ({value_to_string(data.wepvsty3_value)})" if data.wepvsty3_value != 0 else f""
        ac_string = f"{-1 * data.ac_mod_value} ({data.ac_mod_value})"
        wephitmd_string = f"{data.wephitmd_value}" if data.wephitmd_value != 0 else f""
        wephpdam_string = f"{data.wephpdam.name} ({data.wephpdam.min}--{data.wephpdam.max})" if data.wephpdam.min > 0 else f""
        swing_count_string = f"{data.swing_count_value}" if data.swing_count_value != 0 else f""
        critical_hit = f"有" if data.critical_hit else f""
        purpose_string = f"{property_dic_to_string(dic=data.purpose_dic)} ({value_to_string(data.wepvstyp_value)})" if data.wepvstyp_value != 0 else f""

        print(f"|{index}|{data.name}|{data.name_unknown}|{item_type_string}|"
              f"{alignment_string}|{cursed_string}|{special_pwr_string}|{change_to_string}|"
              f"{change_percentage_string}|{price_string}|{stock_string}|{spell_power_string}|"
              f"{class_equip_string}|{heal_pts_string}|{prot_string}|{resist_string}|{ac_string}|"
              f"{wephitmd_string}|{wephpdam_string}|{swing_count_string}|{critical_hit}|{purpose_string}|"
              ,file=fp)
        return

    def _dumpMonsters(self, fp:TextIO)->None:

        print("## モンスター一覧表",file=fp)
        print("",file=fp)
        print(f"|連番|名前|名前複数形|不確定名称|不確定名称複数形|画像ファイルインデクス|出現数|HP|"
              f"種別|アーマクラス|最大攻撃回数|各回の攻撃ダイス|経験値|ドレインレベル|リジェネレーション値|ワンダリングモンスター時報酬|玄室モンスター時報酬|"
              f"後続モンスター|後続モンスター出現率|魔術師呪文レベル|僧侶呪文レベル|出現回数制限|ブレス種別|"
              f"呪文無効化率|抵抗|攻撃付与|弱点|"
              f"能力|能力値|",file=fp)
        print(f"|---|---|---|---|---|---|---|---|"
              f"---|---|---|---|---|---|---|---|---|"
              f"---|---|---|---|---|---|"
              f"---|---|---|---|"
              f"---|---|",file=fp)

        for idx in sorted(self._monsters.keys()):
            self._plainOneDumpMonster(index=idx,data=self._monsters[idx],fp=fp)
        print("",file=fp)
        return

    def _dumpItems(self, fp: TextIO)->None:

        print("## アイテム一覧表",file=fp)
        print("",file=fp)
        print(f"|連番|名前|不確定名称|種別|"
              f"属性(アラインメント)|呪い|スペシャルパワーの効果|破損後のアイテム(使用後に変化するアイテム)|"
              f"使用に伴うアイテム破損率|価格|商店の初期在庫数|使用時に発動する呪文|"
              f"装備可能職業|リジェネレレーション値|防御特性|抵抗属性|アーマクラス(括弧内は補正値)|"
              f"命中率補正値|ダメージダイス|最大攻撃回数|クリティカルヒット付与|倍打特性|",file=fp)
        print(f"|---|---|---|---|"
              f"---|---|---|---|"
              f"---|---|---|---|"
              f"---|---|---|---|---|"
              f"---|---|---|---|---|",file=fp)

        for idx in sorted(self._items.keys()):
            self._plainOneDumpItem(index=idx, data=self._items[idx], fp=fp)

        print("",file=fp)

        return

    def _dumpTOC(self, fp: TextIO)->None:
        """目次情報をテキストとして出力する

        Args:
            fp (TextIO): 出力先.
        """

        print(f"# シナリオ情報", file=fp)
        print(f"", file=fp)
        print(f"## ディスクレイアウト", file=fp)
        print(f"", file=fp)
        print(f"|項目|キャッシュ領域に格納可能なアイテム数(RECPER2B 単位:個)|総要素数(RECPERDK 単位:個)|シナリオ情報中のオフセット(BLOFF 単位:ブロック)|シナリオ情報ファイル中のオフセットアドレス(単位:バイト)|")
        print(f"|---|---|---|---|---|", file=fp)
        for section in (modules.consts.TOC_INDEX_TO_KEY[sub_key] for sub_key in modules.consts.TOC_INDEX_TO_KEY):
            hex_offset=hex(self.toc.BLOFF[section]*modules.consts.BLK_SIZ)
            print(f"|{section}|{self.toc.RECPER2B[section]}|{self.toc.RECPERDK[section]}|{self.toc.BLOFF[section]}|{self.toc.BLOFF[section]*modules.consts.BLK_SIZ} ({hex_offset})|",file=fp)
        print(f"", file=fp)

        print(f"## 種族名", file=fp)
        print(f"", file=fp)
        print(f"|連番|種族名文字列|", file=fp)
        print(f"|---|---|", file=fp)
        for idx,name in self.toc.RACE.items():
            print(f"|{idx}|{name}|", file=fp)
        print(f"", file=fp)

        print(f"## 職業名", file=fp)
        print(f"", file=fp)
        print(f"|連番|職業名文字列|", file=fp)
        print(f"|---|---|", file=fp)
        for idx,name in self.toc.CLASS_NAME.items():
            print(f"|{idx}|{name}|", file=fp)
        print(f"", file=fp)

        print(f"## 状態名", file=fp)
        print(f"", file=fp)
        print(f"|連番|状態名文字列|", file=fp)
        print(f"|---|---|", file=fp)
        for idx,name in self.toc.STATUS.items():
            print(f"|{idx}|{name}|", file=fp)
        print(f"", file=fp)

        print(f"## 属性名", file=fp)
        print(f"", file=fp)
        print(f"|連番|属性名文字列|", file=fp)
        print(f"|---|---|", file=fp)
        for idx,name in self.toc.ALIGN.items():
            print(f"|{idx}|{name}|", file=fp)
        print(f"", file=fp)

        print(f"## 呪文情報", file=fp)
        print(f"", file=fp)
        print(f"|連番|呪文名文字列|ハッシュ値(SPELLHSH)|呪文レベル(SPELLGRP)|呪文種別(SPELL012)|", file=fp)
        print(f"|---|---|---|---|---|---|", file=fp)
        for idx,name in enumerate(modules.consts.DBG_WIZ_SPELL_NAMES):
            print(f"|{idx}|{name}|{self.toc.SPELLHSH[idx]}({hex(self.toc.SPELLHSH[idx])})|{self.toc.SPELLGRP[idx]}|{modules.consts.DBG_WIZ_SPELL_TYPES[self.toc.SPELL012[idx]]}({self.toc.SPELL012[idx]})|", file=fp)
        print(f"", file=fp)

        return

    def doConvert(self)->None:
        """シナリオ情報を変換する
        """
        self._readTOC(data=self._scenario) # 目次情報を読み込む
        self._readFloorTable(data=self._scenario) # 迷宮フロア情報を読み込む
        self._readMonsterTable(data=self._scenario) # モンスター情報を読み込む
        self._readItemTable(data=self._scenario) # アイテム情報を読み込む
        self._readRewardTable(data=self._scenario) # 報酬情報を読み込む
        return

    def plainDump(self, fp:TextIO)->None:
        """テキスト形式で表示する

        Args:
            fp (TextIO): 表示先ファイルのTextIO.
        """

        self._dumpTOC(fp=fp)
        self._dumpMonsters(fp=fp)
        self._dumpItems(fp=fp)
        return

    @property
    def toc(self)->WizardrySCNTOC:
        """目次情報
        """
        return self._toc
