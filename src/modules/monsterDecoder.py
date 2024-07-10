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
from typing import Any,Optional

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.scnDecoder import scnDecoder
from modules.dataEntryDecoder import dataEntryDecoder
from modules.datadef import WizardryMonsterDataEntry, dice_type
from modules.utils import getDecodeDict, word_to_dic
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
    'NAMEUNK': {'offset':0, 'type': '16p'},    # パスカル文字列での不確定名称
    'NAMEUNKS': {'offset':16, 'type': '16p'},  # パスカル文字列での不確定名称複数形

    'NAME': {'offset':32, 'type': '16p'},      # パスカル文字列での名称
    'NAMES': {'offset':48, 'type': '16p'},     # パスカル文字列での名称複数形

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
        """unpackしたモンスター情報をpythonのオブジェクトに変換

        Args:
            decode_dict (dict[str,Any]): unpackしたモンスター情報の辞書(unpackしたデータの要素名->bytes列のタプル)

        Returns:
            WizardryMonsterDataEntry: pythonのオブジェクトであらわしたモンスター情報
        """
        res=WizardryMonsterDataEntry(name_unknown=modules.consts.UNKNOWN_STRING,
                                     plural_name_unknown=modules.consts.UNKNOWN_STRING,
                                     name=modules.consts.UNKNOWN_STRING,
                                     plural_name=modules.consts.UNKNOWN_STRING,
                                     pic=0,
                                     calc1=dice_type(0,0,0),
                                     hprec=dice_type(0,0,0),
                                     enemy_class_value=0,
                                     enemy_class_str=modules.consts.UNKNOWN_STRING,
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
                                     breathe=modules.consts.UNKNOWN_STRING,
                                     unaffect_ratio=0,
                                     wepvsty3_value=0,
                                     resist_dic={},
                                     sppc_value=0,
                                     special_attack_dic={},
                                     weak_point_dic={},
                                     capability_dic={})

        for key in decode_dict.keys():
            match key:
                case 'NAMEUNK': # 不確定名称
                    res.name_unknown=decode_dict[key][0].decode()
                case 'NAMEUNKS': # 不確定名称複数形
                    res.plural_name_unknown=decode_dict[key][0].decode()
                case 'NAME': # 名称
                    res.name=decode_dict[key][0].decode()
                case 'NAMES': # 名称複数形
                    res.plural_name=decode_dict[key][0].decode()
                case 'PIC': # グラフィック番号
                    res.pic=int(decode_dict[key][0])
                case 'CLASS': # モンスター種別
                    v = int(decode_dict[key][0])
                    res.enemy_class_value=v
                    if v in modules.consts.ENEMY_CLASS_DIC: # 有効なモンスター種別番号なら
                        res.enemy_class_str=modules.consts.ENEMY_CLASS_DIC[v] # モンスター種別名を格納
                    else:
                        res.enemy_class_str=modules.consts.UNKNOWN_STRING # 不明な場合は"不明"とする
                case 'AC': # アーマクラス
                    res.ac=int(decode_dict[key][0])
                case 'RECSN': # 最大攻撃回数
                    res.max_swing_count=int(decode_dict[key][0])
                case 'EXPAMT': # 取得経験値
                    res.exp_amount=int(decode_dict[key][0])
                case 'DRAINAMT': # ドレインレベル数
                    res.drain_amount=int(decode_dict[key][0])
                case 'HEALPTS': # リジェネレーション値
                    res.heal_pts=int(decode_dict[key][0])
                case 'REWARD1': # 報酬1 (ワンダリングモンスターとして出現時)
                    res.reward1=int(decode_dict[key][0])
                case 'REWARD2': # 報酬2 (玄室)
                    res.reward2=int(decode_dict[key][0])
                case 'ENMYTEAM': # 後続モンスターのモンスター番号
                    res.enemy_team=int(decode_dict[key][0])
                case 'TEAMPERC': # 後続モンスターの出現確率
                    res.team_percentage=int(decode_dict[key][0])
                case 'MAGSPELS': # 魔術師呪文レベル
                    res.mage_spells=int(decode_dict[key][0])
                case 'PRISPELS': # 僧侶呪文レベル
                    res.priest_spells=int(decode_dict[key][0])
                case 'UNIQUE': # 出現回数制限
                    res.unique=int(decode_dict[key][0])
                case 'BREATHE': # ブレス種別
                    num=int(decode_dict[key][0])
                    res.breathe_value=num
                    if num > 0:
                        if num in modules.consts.RESIST_BREATH_DIC: # 有効なブレス種別の場合
                            res.breathe=modules.consts.RESIST_BREATH_DIC[num] # ブレス種別を格納
                        else:
                            res.breathe=modules.consts.UNKNOWN_STRING # 不明
                    else:
                        res.breathe="" # ブレスなし
                case 'UNAFFCT': # 呪文無効化率
                    res.unaffect_ratio=int(decode_dict[key][0])
                case 'WEPVSTY3': # 抵抗属性
                    res.wepvsty3_value=int(decode_dict[key][0])
                case 'SPPC': # 攻撃付与/弱点/能力
                    res.sppc_value=int(decode_dict[key][0])
                case _:
                    pass
        #
        # 出現数ダイス
        #
        res.calc1=dice_type(int(decode_dict['CALC1_0'][0]),
                            int(decode_dict['CALC1_1'][0]),
                            int(decode_dict['CALC1_2'][0]))
        #
        # HPダイス
        #
        res.hprec=dice_type(int(decode_dict['HPREC_0'][0]),
                            int(decode_dict['HPREC_1'][0]),
                            int(decode_dict['HPREC_2'][0]))
        #
        # 攻撃ダイス
        #
        damage_dices={}
        for i in range(modules.consts.ENEMY_MAX_SWING_COUNT): # 攻撃回数分
            for j in range(modules.consts.DICE_DATA_ELEMENT_NR): # 各ダイス情報の値を取り出す
                dice_key=f"RECS_{i+1}_{j}" # 攻撃ダイスのキー
                if dice_key not in decode_dict: # 対象キーが見つからなければ,
                    continue # 次の要素へ

            # 各攻撃回数ごとのダメージダイスを辞書に登録, 辞書のキーは攻撃回数
            damage_dices[ i + 1 ] = dice_type(int(decode_dict[f"RECS_{i+1}_0"][0]),int(decode_dict[f"RECS_{i+1}_1"][0]),int(decode_dict[f"RECS_{i+1}_2"][0]))

        # ダメージダイスを設定
        res.damage_dices=damage_dices
        # 攻撃抵抗値を設定
        res.resist_dic=word_to_dic(word_value=res.wepvsty3_value, dic=modules.consts.RESIST_BREATH_DIC)
        # 攻撃付与属性を設定
        res.special_attack_dic=word_to_dic(word_value=res.sppc_value, dic=modules.consts.SPPC_SPECIAL_ATTACK_DIC)
        # 弱点を設定
        res.weak_point_dic=word_to_dic(word_value=res.sppc_value, dic=modules.consts.SPPC_WEAK_POINT_DIC)
        # 能力を設定
        res.capability_dic=word_to_dic(word_value=res.sppc_value,dic=modules.consts.SPPC_CAPABILITY_DIC)

        return res

    def decodeOneData(self, scn:scnDecoder, data: Any, index: int)->Optional[Any]:
        """シナリオデータファイル中のモンスターデータを解析する

        Args:
            scn (scnDecoder): シナリオ解析機
            data (Any): シナリオデータファイル情報
            index (int): 調査対象アイテムのインデクス

        Returns:
            Optional[Any]: 解析結果のオブジェクト, インデクスがレンジ外の場合, None
        """
        nr_monsters=scn.toc.RECPERDK[modules.consts.ZENEMY] # モンスターの数

        if 0 > index or index >= nr_monsters:
            return None # 不正インデクス
        if index == 99:
            pass
        # 対象のモンスター情報開始オフセット位置(単位:バイト)を得る
        data_offset = scn.calcDataEntryOffset(category=modules.consts.ZENEMY, item_len=MONSTER_ENTRY_SIZE, index=index)

        # 解析対象データをunpackする
        decode_dict = getDecodeDict(data=data,layout=WizardryMonsterDataEntryDef,offset=data_offset)

        # unpackしたデータをpythonのオブジェクトに変換
        return self._dict2MonsterDataEntry(decode_dict=decode_dict)
