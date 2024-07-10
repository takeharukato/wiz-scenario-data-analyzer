#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file scenario.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief ファイル内のコードの概要
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオデータファイル解析

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
from typing import TextIO
from typing import Optional,Any

"""
使用法: scenario.py [-h] [-v] 入力ファイル 出力ファイル

処理概要

位置引数:
  入力ファイル シナリオファイルのバイナリファイル
  出力ファイル 将来予約

オプション引数:
  -h, --help     ヘルプを表示して修了
  -v, --version  バージョン番号を表示して修了
  -o  --option1  オプション引数の説明
具体的な使用方法
"""


#
# 標準モジュールの読込み
#
import sys
import argparse   # 引数解析
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

if TYPE_CHECKING:
    pass

from modules.datadef import WizardrySCNTOC,WizardryMonsterDataEntry,WizardryItemDataEntry,WizardryRewardDataEntry
from modules.scnDecoder import scnDecoder
from modules.TOCDecoder import TOCDecoder
from modules.monsterDecoder import monsterDecoder
from modules.itemDecoder import itemDecoder
from modules.rewardDecoder import rewardDecoder
import modules.consts

#
# 非標準モジュールの読込み
#

#
# 型定義
#

## クラス定義
#
class ReadScenario:

    """
    クラス変数
    """

    ## 入力ファイル名
    #
    infile = None

    ## 出力ファイル名
    #
    outfile = None

    ## デバッグモードでの動作
    #
    is_debug = False

    ## 引数情報を格納した名前空間オブジェクト
    #
    __args = None

    _scenario:Any
    """シナリオ情報ファイルのメモリイメージ"""

    _toc_decoder:scnDecoder
    """目次情報"""
    _monsters:dict[int,WizardryMonsterDataEntry]
    """モンスター情報"""
    _items:dict[int,WizardryItemDataEntry]
    """アイテム情報"""
    _rewards:dict[int,WizardryRewardDataEntry]
    """報酬情報"""

    ## 初期化
    #
    def __init__(self):

        #
        # コマンドライン解析に必要なクラス変数を初期化
        #

        #
        # コマンドラインを解析
        #
        self.__parse_cmdline() # コマンドラインを解析する

        #
        # 他のクラス変数の初期化
        #
        self.infile = self.__args.infile   # type: ignore 入力ファイル名の設定
        #self.outfile = self.__args.outfile # type: ignore 出力ファイル名の設定

        #
        # デバッグ出力の有効化
        #
        if self.__args.debug:     # type: ignore デバッグ出力有効時
            self.set_debug()      # デバッグモードを有効
        else:
            self.unset_debug()    # デバッグモードを無効

        self._monsters={}
        self._items={}
        self._rewards={}
        return

    def __parse_cmdline(self):
        """コマンドライン解析
        """

        cmdline = None # コマンドラインパーサー

        # コマンドラインオプション定義
        cmdline = argparse.ArgumentParser(                         \
                description="",
                epilog="")

        #
        # 位置引数定義
        #

        #  第1位置引数に入力ファイルを指定
        cmdline.add_argument('infile', help='入力ファイル')

        #  第2位置引数に入力ファイルを指定
        # cmdline.add_argument('outfile', help='出力ファイル')

        #
        # オプション引数
        #

        # バージョン表示オプション
        cmdline.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

        # デバッグ表示有効化
        cmdline.add_argument('-d', '--debug', help='デバッグ表示を有効化',
                            action='store_true', dest='debug')

        self.__args = cmdline.parse_args() # コマンドラインを解析

    ## デバッグモードを有効にしデバッグレベルのログを残す
    #
    def set_debug(self):

        self.is_debug = True # デバッグモードを有効にする

    ## デバッグモードを無効にし情報レベルのログを残す
    #
    def unset_debug(self)->None:

        self.is_debug = False # デバッグモードを無効にする
        return

    def readTOC(self, data:Any)->None:
        """目次情報を読込む

        Args:
            data (Any): シナリオデータ
        """

        self._toc_decoder=TOCDecoder(data=data)
        self._toc_decoder.decodeData(data=data, offset=0)

        return

    def readMonsterTable(self, data:Any)->None:
        decoder=monsterDecoder()
        nr_monsters=self.toc.RECPERDK[modules.consts.ZENEMY]
        for idx in range(nr_monsters):
            monster=decoder.decodeOneData(scn=self._toc_decoder, data=data, index=idx)
            if isinstance(monster, WizardryMonsterDataEntry):
                self._monsters[idx]=monster

        return

    def readItemTable(self, data:Any)->None:
        decoder=itemDecoder()
        nr_items=self.toc.RECPERDK[modules.consts.ZOBJECT]
        for idx in range(nr_items):
            item=decoder.decodeOneData(scn=self._toc_decoder, data=data, index=idx)
            if isinstance(item, WizardryItemDataEntry):
                self._items[idx]=item

        return

    def readRewardTable(self, data:Any)->None:
        decoder=rewardDecoder()
        nr_rewards=self.toc.RECPERDK[modules.consts.ZREWARD]
        for idx in range(nr_rewards):
            reward=decoder.decodeOneData(scn=self._toc_decoder, data=data, index=idx)
            if isinstance(reward, WizardryRewardDataEntry):
                self._rewards[idx]=reward

        return

    def doConvert(self, infile:Optional[str]=None, outfile:Optional[str]=None)->None:
        """シナリオ情報を変換する

        Args:
            infile (Optional[str], optional): 入力ファイル. Defaults to None("SCENARIO.DATA"を読み込む).
            outfile (Optional[str], optional): 出力ファイル. Defaults to None.
        """
        this_infile=self.infile
        if not infile or not this_infile:
            this_infile=modules.consts.DEFAULT_SCENARIO_DATA_FILE

        self._scenario=None
        with open(this_infile, 'rb') as fr:
            self._scenario=fr.read()

        self.readTOC(data=self._scenario) # 目次情報を読み込む
        self.readMonsterTable(data=self._scenario) # モンスター情報を読み込む
        self.readItemTable(data=self._scenario) # アイテム情報を読み込む
        self.readRewardTable(data=self._scenario) # 報酬情報を読み込む
        return

    def plainOneDumpMonster(self, index:int, data:Any, fp: Optional[TextIO]=None)->None:
        """格納しているモンスター情報をテキストとして出力する

        Args:
            index (int): インデクス
            data (Any): 表示対象データ
            fp (Optional[TextIO], optional): 出力先. Defaults to None.
        """

        if not isinstance(data, WizardryMonsterDataEntry):
            return

        if not fp:
            fp = sys.stdout
        """
        name_unknown:str
        plural_name_unknown:str
        name:str
        plural_name:str
        pic:int
        calc1:dice_type
        hprec:dice_type
        enemy_class_value:int
        enemy_class_str:str
        ac:int
        max_swing_count:int
        damage_dices:dict[int,dice_type]
        exp_amount:int
        drain_amount:int
        heal_pts:int
        reward1:int
        reward2:int
        enemy_team:int
        team_percentage:int
        mage_spells:int
        priest_spells:int
        unique:int
        breathe_value:int
        breathe:str
        unaffect_ratio:int
        wepvsty3_value:int
        resist_dic:dict[int,str]
        sppc_value:int
        special_attack_dic:dict[int,str]
        weak_point_dic:dict[int,str]
        capability_dic:dict[int,str]
        """
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
        resist_set=','.join([data.resist_dic[key] for key in sorted(data.resist_dic.keys())])
        resist_string=f"{resist_set} ({hex(data.wepvsty3_value)} = {bin(data.wepvsty3_value)})" if data.wepvsty3_value != 0 else f""
        sppc_string=f"{data.sppc_value} ({hex(data.sppc_value)} = {bin(data.sppc_value)})"
        special_attack_string=','.join([data.special_attack_dic[key] for key in sorted(data.special_attack_dic.keys())])
        weak_points_string = ','.join([data.weak_point_dic[key] for key in sorted(data.weak_point_dic.keys())])
        capability_string =  ','.join([data.capability_dic[key] for key in sorted(data.capability_dic.keys())])
        print(f"|{index}|{name}|{names}|{unknown_name}|{unknown_names}|{pic}|{nr_member}|{hp_dice}|"
              f"{enemy_class}|{ac}|{swing_count}|{dmg_dice_table}|{exp}|{drain}|{heal_pts}|{reward1}|{reward2}|"
              f"{follows}|{follow_percentage} %|{mage_spell}|{pri_spell}|{uniq}|{breathe}|"
              f"{unaffect_ratio} %|{resist_string}|{special_attack_string}|{weak_points_string}|"
              f"{capability_string}|{sppc_string}|",file=fp)
        return

    def plainDump(self, fp:Optional[TextIO]=None)->None:
        self._toc_decoder.plainDump(fp=fp)

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
            self.plainOneDumpMonster(index=idx,data=self._monsters[idx],fp=fp)
        print("",file=fp)
        return

    @property
    def toc(self)->WizardrySCNTOC:
        """目次情報
        """
        return self._toc_decoder.toc

## メイン処理
#
if __name__ == '__main__':

    cmd = ReadScenario() # オブジェクトを生成
    cmd.doConvert()
    cmd.plainDump()
    pass
