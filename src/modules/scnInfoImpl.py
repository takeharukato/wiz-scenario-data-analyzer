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
import tempfile

#
# サードパーティーモジュールの読込み
#

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.datadef import WizardrySCNTOC, WizardryMazeFloorDataEntry, WizardryMonsterDataEntry
from modules.datadef import WizardryItemDataEntry, WizardryRewardDataEntry
from modules.scnInfo import scnInfo
from modules.TOCDecoder import TOCDecoder
from modules.mazeFloorDecoder import mazeFloorDecoder
from modules.monsterDecoder import monsterDecoder
from modules.itemDecoder import itemDecoder
from modules.rewardDecoder import rewardDecoder
from modules.drawMazeSVG import drawMazeSVG
from modules.utils import property_dic_to_string,value_to_string,convertSVGtoRaster
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

    _reward2monster:dict[int,set[int]]
    """報酬番号からモンスター番号の集合への辞書"""

    def __init__(self, scenario:Any) -> None:

        self._scenario=scenario
        self._floors={}
        self._monsters={}
        self._items={}
        self._rewards={}
        self._reward2monster={}
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

    def _fillRewardToMonster(self)->None:
        """報酬番号からモンスターへの関係をマップする"""

        for monster_number in self._monsters.keys():

            monster = self._monsters[monster_number]
            for reward_number in [monster.reward1, monster.reward2]:
                if reward_number in self._rewards:
                    if reward_number not in self._rewards:
                        continue # 無効
                    if reward_number not in self._reward2monster:
                        self._reward2monster[reward_number]=set()
                    self._reward2monster[reward_number].add(monster_number)
        return

        """

        for reward_idx in self._rewards.keys():
            # TODO パーセンテージ取得処理を修正
            reward = self._rewards[reward_idx]
            percentage = reward.percentage
            for mon_num in self._monsters.keys():
                if mon_num not in self._reward2monster:
                    self._reward2monster[mon_num]={} # 辞書を初期化する
                r2m_entry = self._reward2monster[mon_num]
        """
        return

    def readContents(self)->None:
        """シナリオ情報を読み込む
        """
        self._readTOC(data=self._scenario) # 目次情報を読み込む
        self._readFloorTable(data=self._scenario) # 迷宮フロア情報を読み込む
        self._readMonsterTable(data=self._scenario) # モンスター情報を読み込む
        self._readItemTable(data=self._scenario) # アイテム情報を読み込む
        self._readRewardTable(data=self._scenario) # 報酬情報を読み込む
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

    def _plainOneDumpFloorMonsterTable(self, depth:int, floor:WizardryMazeFloorDataEntry, fp: TextIO)->None:

        print(f"#### {depth}階 モンスター出現表", file=fp)
        print(f"", file=fp)

        print(f"##### {depth}階 モンスター出現レンジ一覧", file=fp)
        print(f"", file=fp)

        print(f"|出現系列連番|モンスター出現テーブル番号|モンスター出現テーブル内の系列番号|出現モンスター最小値|出現モンスター最大値|", file=fp)
        print(f"|---|---|---|---|---|", file=fp)
        idx=1
        for idx, info in enumerate(floor.monster_series):

            table_idx, series_num, min_num, max_num = info
            min_mon_string=f"{self._monsters[min_num].name} ({min_num})" if min_num in self._monsters else f"{modules.consts.UNKNOWN_STRING} ({min_num})"
            max_mon_string=f"{self._monsters[max_num].name} ({max_num})" if max_num in self._monsters else f"{modules.consts.UNKNOWN_STRING} ({max_num})"
            print(f"|{idx+1}|{table_idx}|{series_num}|{min_mon_string}|{max_mon_string}|",file=fp)

        print(f"", file=fp)

        print(f"##### {depth}階 モンスター出現テーブル", file=fp)
        print(f"", file=fp)

        """
        min_enemy:int       # MINENEMY 出現モンスター番号の最小値
        multiplier:int      # MULTWORS モンスター出現範囲の系統(0からWORSE01 - 1) * MULTWORS 分最小モンスター番号に加算する
        max_table_index:int # WORSE01 使用するモンスター出現範囲の系統の最大値
        monster_range:int   # RANGE0N 出現モンスターの範囲(0 から RANGE0N - 1 までの範囲の乱数でモンスター番号を決定する)
        inc_series_percentage:int # PERCWORS モンスター出現範囲の系統を加算する確率 系統番号がWORSE01以上の場合は加算しない
        """
        print(f"|モンスター出現テーブル番号|出現モンスター番号最小値(MINENEMY)|モンスター出現範囲系統乗数(MULTWORS)|モンスター出現範囲系統最大値(WORSE01)|出現モンスターの範囲(RANGE0N)|モンスター出現範囲系統加算確率(PERCWORS)|", file=fp)
        print(f"|---|---|---|---|---|---|", file=fp)
        for idx in floor.monster_tables.keys():
            entry=floor.monster_tables[idx]
            print(f"|{idx}|{entry.min_enemy}|{entry.multiplier}|{entry.max_table_index}|{entry.monster_range}|{entry.inc_series_percentage}|", file=fp)

        print(f"", file=fp)

        return

    def _drawFloorLayoutWithSVG(self, drawer:drawMazeSVG, floor:WizardryMazeFloorDataEntry, outfile:str)->None:

        for x in range(modules.consts.FLOOR_WIDTH):
            for y in range(modules.consts.FLOOR_HEIGHT):
                for dir in modules.consts.DIR_VALID:
                    # DIR_NORTH=0,DIR_EAST=1,DIR_SOUTH=2,DIR_WEST=3

                    v=floor.getWallInfo(x=x, y=y, dir=dir)

                    if v == modules.consts.FLOOR_WALL_WALL:
                        if dir == modules.consts.DIR_NORTH: # 北側に壁を配置する場合
                            counter_x = x
                            counter_y = ( (y + 1) + modules.consts.FLOOR_HEIGHT ) % modules.consts.FLOOR_HEIGHT
                            counter_dir = modules.consts.DIR_SOUTH
                        elif dir == modules.consts.DIR_SOUTH: # 南側に壁を配置する場合
                            counter_x = x
                            counter_y = ( (y - 1) + modules.consts.FLOOR_HEIGHT ) % modules.consts.FLOOR_HEIGHT
                            counter_dir = modules.consts.DIR_NORTH
                        elif dir == modules.consts.DIR_WEST: # 西側に壁を配置する場合
                            counter_x = ( (x - 1) + modules.consts.FLOOR_WIDTH ) % modules.consts.FLOOR_WIDTH
                            counter_y = y
                            counter_dir = modules.consts.DIR_EAST
                        else: # 東側に壁を設置する場合
                            counter_x = ( (x + 1) + modules.consts.FLOOR_WIDTH ) % modules.consts.FLOOR_WIDTH
                            counter_y = y
                            counter_dir = modules.consts.DIR_WEST

                        counter_v = floor.getWallInfo(x=counter_x, y=counter_y, dir=counter_dir)
                        if counter_v == modules.consts.FLOOR_WALL_OPEN:
                            drawer.addArrow(x=x, y=y, pos=dir, dir=counter_dir)
                        else:
                            drawer.addWall(x=x, y=y, dir=dir)
                    elif v == modules.consts.FLOOR_WALL_DOOR:
                        drawer.addDoor(x=x, y=y, dir=dir)
                    elif v == modules.consts.FLOOR_WALL_HIDDEN:
                        drawer.addDoor(x=x, y=y, dir=dir, hidden=True)
        drawer.save()
        return

    def _drawFloorEvents(self, floor:WizardryMazeFloorDataEntry, basename:str, format:str=modules.consts.DEFAULT_RASTER_IMAGE_TYPE)->None:

        with tempfile.TemporaryDirectory() as dir_name:

            # SVGファイルを作成
            svg_file=os.path.join(dir_name,f"{basename}.svg")

            # 描画オブジェクトを生成
            drawer=drawMazeSVG(outfile=svg_file, draw_coordinate=True)

            # イベント情報を書き込み
            for x in range(modules.consts.FLOOR_WIDTH): # 各X座標について
                for y in range(modules.consts.FLOOR_HEIGHT): # 各Y座標について

                    pos=(x,y) # 検査する座標
                    if pos in floor.event_map and floor.event_map[pos] != modules.consts.FLOOR_EVENT_NORMAL: # 通常の床でない場合,
                        drawer.addEventNumber(x=x,y=y,event_number=floor.event_map[pos]) # イベント番号を書き込む

            # フロアレイアウト情報を書き込み
            self._drawFloorLayoutWithSVG(drawer=drawer, floor=floor, outfile=svg_file)

            drawer.save() # 画像を保存する

            # PNGに変換
            convertSVGtoRaster(infile=svg_file, outfile=f"{basename}.{modules.consts.DEFAULT_RASTER_IMAGE_EXT}", format=modules.consts.RASTER_IMAGE_TYPE_PNG)

        return

    def _drawFloorRooms(self, floor:WizardryMazeFloorDataEntry, basename:str, format:str=modules.consts.DEFAULT_RASTER_IMAGE_TYPE)->None:

        with tempfile.TemporaryDirectory() as dir_name:

            # SVGファイルを作成
            svg_file=os.path.join(dir_name,f"{basename}.svg")

            # 描画オブジェクトを生成
            drawer=drawMazeSVG(outfile=svg_file, draw_coordinate=True)

            # 玄室情報を書き込み
            for x in range(modules.consts.FLOOR_WIDTH):
                for y in range(modules.consts.FLOOR_HEIGHT):
                    pos=(x,y)
                    if pos in floor.in_room and floor.in_room[pos]: # 玄室の場合
                        drawer.addRoom(x=x, y=y)

            # フロアレイアウト情報を書き込み
            self._drawFloorLayoutWithSVG(drawer=drawer, floor=floor, outfile=svg_file)

            drawer.save()

            # PNGに変換
            convertSVGtoRaster(infile=svg_file, outfile=f"{basename}.{modules.consts.DEFAULT_RASTER_IMAGE_EXT}", format=modules.consts.RASTER_IMAGE_TYPE_PNG)

        return

    def _drawFloorLayout(self, floor:WizardryMazeFloorDataEntry, basename:str, format:str=modules.consts.DEFAULT_RASTER_IMAGE_TYPE)->None:

        with tempfile.TemporaryDirectory() as dir_name:
            # SVGファイルを作成
            svg_file=os.path.join(dir_name,f"{basename}.svg")

            # 描画オブジェクトを生成
            drawer=drawMazeSVG(outfile=svg_file, draw_coordinate=True)

            # フロアレイアウト情報を書き込み
            self._drawFloorLayoutWithSVG(drawer=drawer,floor=floor, outfile=svg_file)

            # PNGに変換
            convertSVGtoRaster(infile=svg_file, outfile=f"{basename}.{modules.consts.DEFAULT_RASTER_IMAGE_EXT}",
                               format=modules.consts.DEFAULT_RASTER_IMAGE_TYPE)

        return

    def _plainOneDumpFloorEventInfo(self, depth:int, floor:WizardryMazeFloorDataEntry, fp: TextIO)->None:

        print(f"##### {depth}階 イベント一覧", file=fp)
        print(f"", file=fp)

        print(f"|イベント番号|イベント種別|イベント引数1|イベント引数2|イベント引数3|", file=fp)
        print(f"|---|---|---|---|---|", file=fp)

        for number in floor.event_info_dic.keys():
            entry=floor.event_info_dic[number]

            event_type_string=f"{modules.consts.FLOOR_EVENT_TO_STRING[entry.event_type]} ({entry.event_type})" if entry.event_type in modules.consts.FLOOR_EVENT_TO_STRING else f"{modules.consts.UNKNOWN_STRING} ({entry.event_type})"
            assert 0 in entry.params and 1 in entry.params and 2 in entry.params, f"invalid entry params [{entry.params}]"
            print(f"|{number}|{event_type_string}|{entry.params[0]}|{entry.params[1]}|{entry.params[2]}|", file=fp)

        print(f"", file=fp)

        return

    def _plainOneDumpFloorEventMap(self, depth:int, floor:WizardryMazeFloorDataEntry, fp: TextIO)->None:

        print(f"#### {depth}階 イベントマップ", file=fp)
        print(f"", file=fp)
        print(f"##### イベントマップ情報", file=fp)
        print(f"", file=fp)

        basename=f"floor-event-map-{depth:02}"
        self._drawFloorEvents(floor=floor, basename=basename)
        outfile=f"{basename}.{modules.consts.DEFAULT_RASTER_IMAGE_EXT}"
        if os.path.exists(outfile):
            print(f"", file=fp)
            print(f"![{depth:02}階イベントマップ]({outfile})", file=fp)
            print(f"", file=fp)

        print(f"```:text", file=fp)
        y_lst=sorted(list(range(modules.consts.FLOOR_HEIGHT)), reverse=True)
        for y in y_lst:
            print(f"{y:2} ",end='', file=fp)
            for x in range(modules.consts.FLOOR_WIDTH):
                pos=(x,y)
                assert pos in floor.in_room, f"No room definition for {pos} on floor {depth}"
                event_number=floor.event_map[pos]
                if event_number in floor.event_info_dic:
                    event_type=floor.event_info_dic[event_number]
                else:
                    event_type = modules.consts.FLOOR_EVENT_NORMAL
                if event_type == modules.consts.FLOOR_EVENT_NORMAL:
                    print(f"{'':4}",end='', file=fp)
                else:
                    print(f" {event_number:2} ",end='', file=fp)
            print("",file=fp)
        print(f"{' ':3}",end='', file=fp)
        for x in range(modules.consts.FLOOR_WIDTH):
            print(f" {x:2} ",end='', file=fp)
        print("", file=fp)
        print(f"```", file=fp)
        print(f"", file=fp)

        return

    def _plainOneDumpFloorRooms(self, depth:int, floor:WizardryMazeFloorDataEntry, fp: TextIO)->None:

        print(f"#### {depth}階 玄室情報", file=fp)
        print(f"", file=fp)

        basename=f"floor-room-{depth:02}"
        self._drawFloorRooms(floor=floor, basename=basename)
        outfile=f"{basename}.{modules.consts.DEFAULT_RASTER_IMAGE_EXT}"
        if os.path.exists(outfile):
            print(f"", file=fp)
            print(f"![{depth:02}階玄室情報]({outfile})", file=fp)
            print(f"", file=fp)

        print(f"```:text", file=fp)

        y_lst=sorted(list(range(modules.consts.FLOOR_HEIGHT)), reverse=True)
        for y in y_lst:
            print(f"{y:2} ",end='', file=fp)
            for x in range(modules.consts.FLOOR_WIDTH):
                pos=(x,y)
                assert pos in floor.in_room, f"No room definition for {pos} on floor {depth}"
                if floor.in_room[pos]:
                    print(f" 玄 ",end='', file=fp)
                else:
                    print(f"{'':4}",end='', file=fp)
            print("",file=fp)
        print(f"{' ':3}",end='', file=fp)
        for x in range(modules.consts.FLOOR_WIDTH):
            print(f" {x:2} ",end='', file=fp)
        print("", file=fp)

        print(f"```", file=fp)

        print(f"", file=fp)

        return

    def _plainOneDumpFloorLayout(self, depth:int, floor:WizardryMazeFloorDataEntry, fp: TextIO)->None:

        order=['西側の壁','南の壁', '東側の壁', '北側の壁']
        wall_dic_lst=[floor.wall_info_west,floor.wall_info_south,floor.wall_info_east,floor.wall_info_north]
        info_dic=zip(order, wall_dic_lst)

        print(f"", file=fp)
        print(f"#### {depth}階 フロアレイアウト情報", file=fp)

        basename=f"floor-layout-{depth:02}"
        self._drawFloorLayout(floor=floor, basename=basename)
        outfile=f"{basename}.{modules.consts.DEFAULT_RASTER_IMAGE_EXT}"
        if os.path.exists(outfile):
            print(f"", file=fp)
            print(f"![{depth:02}階フロアレイアウト]({outfile})", file=fp)
            print(f"", file=fp)

        for title, dic in info_dic:
            print(f"", file=fp)
            print(f"##### {title}", file=fp)
            print(f"", file=fp)

            print(f"```:text", file=fp)

            y_lst=sorted(list(range(modules.consts.FLOOR_HEIGHT)), reverse=True)
            for y in y_lst:
                print(f"{y:2} ",end='', file=fp)
                for x in range(modules.consts.FLOOR_WIDTH):
                    pos=(x,y)
                    assert pos in dic, f"No definition for {pos} on floor {depth}"
                    v=dic[pos]
                    assert v in modules.consts.FLOOR_WALL_DIC, f"No definition for {v} in WALL_DIC"
                    print(f" {modules.consts.FLOOR_WALL_DIC[v]} ",end='', file=fp)
                print("",file=fp)
            print(f"{' ':3}",end='', file=fp)
            for x in range(modules.consts.FLOOR_WIDTH):
                print(f" {x:2} ",end='', file=fp)
            print("", file=fp)

            print("```", file=fp, flush=True)

        print(f"", file=fp)

        return

    def _plainOneDumpFloor(self, depth:int, floor:WizardryMazeFloorDataEntry, fp: TextIO)->None:

        print(f"### {depth}階 フロア情報", file=fp)
        self._plainOneDumpFloorLayout(depth=depth, floor=floor, fp=fp)
        self._plainOneDumpFloorRooms(depth=depth, floor=floor, fp=fp)
        self._plainOneDumpFloorEventMap(depth=depth, floor=floor, fp=fp)
        self._plainOneDumpFloorEventInfo(depth=depth, floor=floor, fp=fp)
        self._plainOneDumpFloorMonsterTable(depth=depth, floor=floor, fp=fp)

        return

    def _plainOneDumpRewardHumanReadable(self, reward_number:int, reward:WizardryRewardDataEntry, fp: TextIO)->None:

        index_string = f"{reward_number}"
        in_chest_string=f"宝箱あり" if reward.in_chest else f"宝箱なし"
        nr_rewards_string = f"{reward.reward_count_value}"
        trap_string=f"{reward.trap_string} ( {value_to_string(val=reward.trap_type_value)} )" if reward.in_chest else f""

        for info_index in sorted(reward.rewards.keys()):

            reward_info=reward.rewards[info_index]

            if reward_info.percentage == 0:
                continue # 無効エントリ

            percentage_string = f"{reward_info.percentage:3} %"
            has_item_string = f"アイテム" if reward_info.has_item else f"お金"

            if info_index > reward.reward_count_value:
                continue # 無効エントリ

            if reward_info.has_item: # アイテム報酬の場合
                range_lst=list(reward_info.item_range_tuple)
            else: # お金報酬の場合
                range_lst=list(reward_info.gold_range_tuple)

            reward_lst:list[str]=[]
            for idx,gold_or_item in enumerate(range_lst):
                if range_lst[idx][0] == 100:
                    reward_lst += [f"{gold_or_item[1]}--{gold_or_item[2]}"]
                else:
                    reward_lst += [f"{gold_or_item[1]}--{gold_or_item[2]} ( {range_lst[idx][0]} % )"]
            each_reward="|".join(reward_lst)
            print(f"|{index_string}|{info_index} / {nr_rewards_string}|{in_chest_string}|{trap_string}|{percentage_string}|{has_item_string}|"
                f"{each_reward}|", file=fp)
            pass
        return

    def _dumpRewards(self, fp:TextIO)->None:

        #
        # 報酬レンジ総数を算出する
        #
        max_reward_range=0
        for idx in sorted(self._rewards.keys()):

            reward = self._rewards[idx]
            for info_index in sorted(reward.rewards.keys()):

                if info_index > reward.reward_count_value:
                    continue # 無効エントリ

                info = reward.rewards[info_index]

                if info.has_item: # アイテム報酬の場合
                    range_lst=list(info.item_range_tuple)
                else:
                    range_lst=list(info.gold_range_tuple)
                max_reward_range=max(max_reward_range, len(range_lst))

        range_names="|".join([f"報酬{i+1}(獲得ゴールド/取得アイテム番号の範囲[最小値--最大値])" for i in range(max_reward_range)])
        print("## 報酬一覧表",file=fp)
        print("",file=fp)
        print(f"|報酬番号|連番 / 総報酬数|宝箱の有無|罠|取得確率|報酬種別|"
              f"{range_names}|",
              file=fp)
        range_cols="|".join([f"---" for _i in range(max_reward_range)])
        print(f"|---|---|---|---|---|---|"
              f"{range_cols}|", file=fp)

        for idx in sorted(self._rewards.keys()):
            self._plainOneDumpRewardHumanReadable(reward_number=idx, reward=self._rewards[idx], fp=fp)
        return

    def _dumpFloors(self, fp:TextIO)->None:
        for idx in sorted(self._floors.keys()):
            self._plainOneDumpFloor(depth=idx+1, floor=self._floors[idx], fp=fp)
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

    def plainDump(self, fp:TextIO)->None:
        """テキスト形式で表示する

        Args:
            fp (TextIO): 表示先ファイルのTextIO.
        """

        self._dumpTOC(fp=fp)
        self._dumpFloors(fp=fp)
        self._dumpMonsters(fp=fp)
        self._dumpItems(fp=fp)
        self._dumpRewards(fp=fp)

        return

    def getWallInfo(self, x:int, y:int, z:int, dir:int)->int:
        """壁情報を得る

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            dir (int): 向き

        Returns:
            int: 壁情報
        """

        if (z - 1) not in self._floors:
            return -1 # 不正な階層

        return self._floors[z-1].getWallInfo(x=x, y=y, dir=dir)

    @property
    def toc(self)->WizardrySCNTOC:
        """目次情報
        """
        return self._toc
