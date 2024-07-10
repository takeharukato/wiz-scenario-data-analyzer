#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file monsterDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報のモンスターデータを解析する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報のモンスターデータを解析する

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
from typing import Any #,Optional

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.dataEntryDecoder import dataEntryDecoder
from modules.datadef import WizardryMonsterDataEntry, WizardrySCNTOC,dice_type
from modules.utils import getDecodeDict,word_to_resist_dic,word_to_dic
import modules.consts

"""モンスター情報のPascal定義
        TENEMY = RECORD (* モンスター情報 *)
            NAMEUNK  : STRING[ 15]; (* 不確定名称 *)
            NAMEUNKS : STRING[ 15]; (* 不確定名称複数形 *)
            NAME     : STRING[ 15]; (* 名前 *)
            NAMES    : STRING[ 15]; (* 名前複数形 *)
            PIC      : INTEGER;     (* グラフィック *)
            CALC1    : TWIZLONG;    (* 出現数 *)
            HPREC    : THPREC;      (* HP算出ダイス *)
            CLASS    : INTEGER;     (* モンスター種別 *
                                    (* モンスター種別は以下の通り
                                       0 戦士系,
                                       1 魔術師系
                                       2 僧侶系
                                       3 盗賊系
                                       4 未使用(小人, 忍者用?)
                                       5 巨人系
                                       6 神話系
                                       7 竜系
                                       8 動物系
                                       9 リカント系
                                      10 不死系
                                      11 悪魔系
                                      12 昆虫系
                                      13 魔法生物系 *)
            AC       : INTEGER;     (* アーマクラス *)
            RECSN    : INTEGER;     (* 最大攻撃回数 *)
            RECS     : ARRAY[ 1..7] OF THPREC; (* 各攻撃回のダメージダイス *)
            EXPAMT   : TWIZLONG;    (* 獲得経験値 (シナリオ1では, 未使用) *)
            DRAINAMT : INTEGER;     (* エナジードレイン値 *)
            HEALPTS  : INTEGER;     (* リジェネレレーション値 *)
            REWARD1  : INTEGER;     (* ワンダリングモンスターの場合の報酬種別 *)
            REWARD2  : INTEGER;     (* 玄室モンスターの場合の報酬種別 *)
            ENMYTEAM : INTEGER;     (* 後続モンスターのモンスター番号 *)
            TEAMPERC : INTEGER;     (* 後続モンスターの発生確率 *)
            MAGSPELS : INTEGER;     (* 魔術師呪文レベル *)
            PRISPELS : INTEGER;     (* 僧侶呪文レベル *)
            UNIQUE   : INTEGER;     (* 遭遇回数が限定されるモンスターの場合, 1以上の値を設定(シナリオ1では, コントロールセンタのLevel 7 Fighterにのみ1に設定される) *)
            BREATHE  : INTEGER;     (* ブレス種別 *)
            UNAFFCT  : INTEGER;     (* 呪文無効化率 *)
            WEPVSTY3 : PACKED ARRAY[ 0..15] OF BOOLEAN; (* 抵抗特性 *)
                                                        (* 0 無属性グループ攻撃呪文(LORTO,MALIKTO,MOLITO,TILTOWAIT)のダメージ半減
                                                           1 火属性グループ攻撃呪文(LITOKAN,MAHALITO,LAHALITO)のダメージ半減
                                                           2 冷属性グループ攻撃呪文(DALTO,MADALTO)のダメージ半減
                                                         *)
            SPPC     : PACKED ARRAY[ 0..15] OF BOOLEAN; (* モンスターの特殊能力 *)
                       (* SPPC[0]:石化, SPPC[1]:毒,SPPC[2]:麻痺,SPPC[3]:クリティカル,SPPC[4]:石化, SPPC[5]:逃走, SPPC[6]:仲間を呼ぶ *)
          END;
"""
# モンスター情報のサイズ(単位:バイト)
MONSTER_ENTRY_SIZE=158
# モンスター情報のデータレイアウト
WizardryMonsterDataEntryDef:dict[str,Any]={
    'NAMEUNK': {'offset':0, 'type': '15p'},    # パスカル文字列での不確定名称
    'NAMEUNKS': {'offset':16, 'type': '15p'},  # パスカル文字列での不確定名称複数形

    'NAME': {'offset':32, 'type': '15p'},      # パスカル文字列での名称
    'NAMES': {'offset':48, 'type': '15p'},     # パスカル文字列での名称複数形

    'PIC': {'offset':64, 'type': '<H'},        # グラフィック番号

    'CALC1_0': {'offset':66, 'type': '<H'},    # 出現数ダイス 試行回数
    'CALC1_1': {'offset':68, 'type': '<H'},    # 出現数ダイス ダイス面数
    'CALC1_2': {'offset':70, 'type': '<H'},    # 出現数ダイス 加算値

    'HPREC_0': {'offset':72, 'type': '<H'},    # HPダイス 試行回数
    'HPREC_1': {'offset':74, 'type': '<H'},    # HPダイス ダイス面数
    'HPREC_2': {'offset':76, 'type': '<H'},    # HPダイス 加算値

    'CLASS'  :  {'offset':78, 'type': '<H'},   # モンスター種別
    'AC'     :  {'offset':80, 'type': '<h'},   # アーマクラス
    'RECSN'  :  {'offset':82, 'type': '<H'},   # 最大攻撃回数

    'RECS_1_0': {'offset':84, 'type': '<H'},   # 攻撃ダイス1 試行回数
    'RECS_1_1': {'offset':86, 'type': '<H'},   # 攻撃ダイス1 ダイス面数
    'RECS_1_2': {'offset':88, 'type': '<H'},   # 攻撃ダイス1 加算値

    'RECS_2_0': {'offset':90, 'type': '<H'},   # 攻撃ダイス2 試行回数
    'RECS_2_1': {'offset':92, 'type': '<H'},   # 攻撃ダイス2 ダイス面数
    'RECS_2_2': {'offset':94, 'type': '<H'},   # 攻撃ダイス2 加算値

    'RECS_3_0': {'offset':96, 'type': '<H'},   # 攻撃ダイス3 試行回数
    'RECS_3_1': {'offset':98, 'type': '<H'},   # 攻撃ダイス3 ダイス面数
    'RECS_3_2': {'offset':100, 'type': '<H'},  # 攻撃ダイス3 加算値

    'RECS_4_0': {'offset':102, 'type': '<H'},   # 攻撃ダイス4 試行回数
    'RECS_4_1': {'offset':104, 'type': '<H'},   # 攻撃ダイス4 ダイス面数
    'RECS_4_2': {'offset':106, 'type': '<H'},  # 攻撃ダイス4 加算値

    'RECS_5_0': {'offset':108, 'type': '<H'},  # 攻撃ダイス5 試行回数
    'RECS_5_1': {'offset':110, 'type': '<H'},  # 攻撃ダイス5 ダイス面数
    'RECS_5_2': {'offset':112, 'type': '<H'},  # 攻撃ダイス5 加算値

    'RECS_6_0': {'offset':114, 'type': '<H'},  # 攻撃ダイス6 試行回数
    'RECS_6_1': {'offset':116, 'type': '<H'},  # 攻撃ダイス6 ダイス面数
    'RECS_6_2': {'offset':118, 'type': '<H'},  # 攻撃ダイス6 加算値

    'RECS_7_0': {'offset':120, 'type': '<H'},  # 攻撃ダイス7 試行回数
    'RECS_7_1': {'offset':122, 'type': '<H'},  # 攻撃ダイス7 ダイス面数
    'RECS_7_2': {'offset':124, 'type': '<H'},  # 攻撃ダイス7 加算値

    'EXPAMT':   {'offset':126, 'type': '<H'},  # 獲得経験値

    'DRAINAMT': {'offset':132, 'type': '<H'},  # ドレインレベル数
    'HEALPTS':  {'offset':134, 'type': '<H'},  # リジェネレレーション値

    'REWARD1':  {'offset':136, 'type': '<H'},  # ワンダリングモンスターの報酬種別
    'REWARD2':  {'offset':138, 'type': '<H'},  # 玄室モンスターの報酬種別

    'ENMYTEAM': {'offset':140, 'type': '<H'},  # 後続モンスターのモンスター番号
    'TEAMPERC': {'offset':142, 'type': '<H'},  # 後続モンスターの発生確率

    'MAGSPELS': {'offset':144, 'type': '<H'},  # 魔術師呪文レベル
    'PRISPELS': {'offset':146, 'type': '<H'},  # 僧侶呪文レベル

    'UNIQUE':   {'offset':148, 'type': '<h'},  # 遭遇回数制限

    'BREATHE':  {'offset':150, 'type': '<H'},  # ブレス種別
    'UNAFFCT':  {'offset':152, 'type': '<H'},  # 呪文無効化率
    'WEPVSTY3': {'offset':154, 'type': '<H'},  # 抵抗特性
    'SPPC':     {'offset':156, 'type': '<H'},  # 攻撃付与
}

class monsterDecoder(dataEntryDecoder):


    def _dict2MonsterDataEntry(self, decode_dict:dict[str,Any])->WizardryMonsterDataEntry:

        res=WizardryMonsterDataEntry(name_unknown="",
                                     plural_name_unknown="",
                                     name="",
                                     plural_name="",
                                     pic=0,
                                     calc1=dice_type(0,0,0),
                                     hprec=dice_type(0,0,0),
                                     cls=0,
                                     ac=0,
                                     max_swing_count=0,
                                     damage_dices={},
                                     exp_amount=0,
                                     drain_amount=0,
                                     heal_pts=0,
                                     reward1=0,
                                     reward2=0,
                                     enemy_team=0,
                                     team_percentage=0,
                                     mage_spells=0,
                                     priest_spells=0,
                                     unique=0,
                                     breathe_value=0,
                                     breathe="",
                                     unaffect_ratio=0,
                                     wepvsty3_value=0,
                                     resist_dic={},
                                     sppc_value=0,
                                     special_attack_dic={},
                                     weak_point_dic={},
                                     capability_dic={})

        for key in decode_dict.keys():
            match key:
                case 'NAMEUNK':
                    res.name_unknown=decode_dict[key][0].decode()
                case 'NAMEUNKS':
                    res.plural_name_unknown=decode_dict[key][0].decode()
                case 'NAME':
                    res.name=decode_dict[key][0].decode()
                case 'NAMES':
                    res.plural_name=decode_dict[key][0].decode()
                case 'PIC':
                    res.pic=int(decode_dict[key][0])
                case 'CLASS':
                    res.cls=int(decode_dict[key][0])
                case 'AC':
                    res.ac=int(decode_dict[key][0])
                case 'RECSN':
                    res.max_swing_count=int(decode_dict[key][0])
                case 'EXPAMT':
                    res.exp_amount=int(decode_dict[key][0])
                case 'DRAINAMT':
                    res.drain_amount=int(decode_dict[key][0])
                case 'HEALPTS':
                    res.heal_pts=int(decode_dict[key][0])
                case 'REWARD1':
                    res.reward1=int(decode_dict[key][0])
                case 'REWARD2':
                    res.reward2=int(decode_dict[key][0])
                case 'ENMYTEAM':
                    res.enemy_team=int(decode_dict[key][0])
                case 'TEAMPERC':
                    res.team_percentage=int(decode_dict[key][0])
                case 'MAGSPELS':
                    res.mage_spells=int(decode_dict[key][0])
                case 'PRISPELS':
                    res.priest_spells=int(decode_dict[key][0])
                case 'UNIQUE':
                    res.unique=int(decode_dict[key][0])
                case 'BREATHE':
                    num=int(decode_dict[key][0])
                    res.breathe_value=num
                    if num > 0 and num in modules.consts.RESIST_BREATH_DIC:
                        res.breathe=modules.consts.RESIST_BREATH_DIC[num]
                    else:
                        res.breathe=""
                case 'UNAFFCT':
                    res.unaffect_ratio=int(decode_dict[key][0])
                case 'WEPVSTY3':
                    res.wepvsty3_value=int(decode_dict[key][0])
                case 'SPPC':
                    res.sppc_value=int(decode_dict[key][0])
                case _:
                    pass
        res.calc1=dice_type(int(decode_dict['CALC1_0'][0]),
                            int(decode_dict['CALC1_1'][0]),
                            int(decode_dict['CALC1_2'][0]))
        #
        # 攻撃ダイス
        #
        damage_dices={}
        for i in range(7):
            for j in range(3):
                dice_key=f"RECS_{i+1}_{j}"
                if dice_key not in decode_dict:
                    continue
            damage_dices[ i + 1 ] = dice_type(int(decode_dict[f"RECS_{i+1}_0"][0]),int(decode_dict[f"RECS_{i+1}_1"][0]),int(decode_dict[f"RECS_{i+1}_2"][0]))
        res.damage_dices=damage_dices
        res.resist_dic=word_to_resist_dic(resist_value=res.wepvsty3_value)
        res.special_attack_dic=word_to_dic(resist_value=res.sppc_value,dic=modules.consts.SPPC_SPECIAL_ATTACK_DIC)
        res.weak_point_dic=word_to_dic(resist_value=res.sppc_value,dic=modules.consts.SPPC_WEAK_POINT_DIC)
        res.capability_dic=word_to_dic(resist_value=res.sppc_value,dic=modules.consts.SPPC_CAPABILITY_DIC)

        return res

    def decodeOneData(self, toc: WizardrySCNTOC, data: Any, index: int) -> Any | None:
        """シナリオデータファイル中のモンスターデータを解析する

        Args:
            toc (WizardrySCNTOC)
            data (Any): シナリオデータファイル情報
            index (int): 調査対象アイテムのインデクス

        Returns:
            Optional[Any]: 解析結果のオブジェクト, インデクスがレンジ外の場合, None
        """

        nr_monsters=toc.RECPERDK[modules.consts.ZENEMY] # モンスターの数

        if 0 > index or index >= nr_monsters:
            return None # 不正インデクス

        # モンスター情報開始オフセットアドレス
        start_block = toc.BLOFF[modules.consts.ZENEMY]
        start_offset = modules.consts.BLK_SIZ * start_block

        # 対象データの位置
        data_block = 2 * ( index // toc.RECPER2B[modules.consts.ZENEMY] )
        data_block_offset = modules.consts.BLK_SIZ * data_block
        entry_offset = (index % toc.RECPER2B[modules.consts.ZENEMY]) * MONSTER_ENTRY_SIZE
        data_offset = start_offset + data_block_offset + entry_offset
        if index == 32:
            pass
        decode_dict = getDecodeDict(data=data,layout=WizardryMonsterDataEntryDef,offset=data_offset)
        return self._dict2MonsterDataEntry(decode_dict=decode_dict)