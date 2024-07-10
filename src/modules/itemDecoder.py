#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file itemDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報のアイテムデータを解析する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報のアイテムデータを解析する

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
from modules.datadef import WizardryItemDataEntry, dice_type
from modules.utils import getDecodeDict,word_to_use_string,word_to_dic,word_to_resist_dic
import modules.consts

"""アイテム情報のPascal定義
        TOBJREC = RECORD (* アイテム情報 *)
            NAME     : STRING[ 15]; (* 名前(15文字までの文字列) *)
            NAMEUNK  : STRING[ 15]; (* 未鑑定時の名前(15文字までの文字列) *)
            OBJTYPE  : TOBJTYPE;    (* アイテム種別 *)
            ALIGN    : TALIGN;      (* 装備可能な属性(アラインメント): UNALIGN(無属性)の場合は, 全属性で装備可能 *)
            CURSED   : BOOLEAN;     (* 呪いの有無 True=呪われている装備, False=呪われていない装備 *)
            SPECIAL  : INTEGER;     (* スペシャルパワーの分類番号 *)
            CHANGETO : INTEGER;     (* アイテム使用後に変化するアイテムのアイテム番号 *)
            CHGCHANC : INTEGER;     (* アイテム使用後に別のアイテムに変化する確率 *)
            PRICE    : TWIZLONG;    (* 売却/鑑定価格 *)
            BOLTACXX : INTEGER;     (* ボルタック商店の在庫数 *)
            SPELLPWR : INTEGER;     (* アイテム使用時に発動する呪文の呪文番号(呪文番号は, 呪文習得表(SPELLSKN)のインデクスと同じ) *)
            CLASSUSE : PACKED ARRAY[ TCLASS] OF BOOLEAN; (* 装備可能な職業 CLASSUSE[職業]がTrueの場合は, 装備可能, Falseの場合は, 装備不可能 *)
            HEALPTS  : INTEGER;     (* リジェネレーション値 *)
            WEPVSTY2 : PACKED ARRAY[ 0..15] OF BOOLEAN; (* 防御特性 *)
            WEPVSTY3 : PACKED ARRAY[ 0..15] OF BOOLEAN; (* 抵抗特性 *)
            ARMORMOD : INTEGER; (* AC補正値(ACから減算する値) *)
            WEPHITMD : INTEGER; (* アイテムのST値(命中率補正値) *)
            WEPHPDAM : THPREC;  (* アイテムのダメージダイス *)
            XTRASWNG : INTEGER; (* アイテムのAT値(攻撃回数値) 装備しているアイテムのうち最も高いAT値を最大攻撃回数として使用する *)
            CRITHITM : BOOLEAN; (* クリティカルヒット攻撃付与付加の有無, True=クリティカルヒット攻撃を付与, False=クリティカルヒット攻撃を付与しない *)
            WEPVSTYP : PACKED ARRAY[ 0..13] OF BOOLEAN; (* 倍打特性 *)
          END;
"""

# アイテム情報のサイズ(単位:バイト)
ITEM_ENTRY_SIZE=78
# アイテム情報のデータレイアウト
WizardryItemDataEntryDef:dict[str,Any]={
    'NAME': {'offset':0, 'type': '16p'},      # パスカル文字列での名称
    'NAMEUNK': {'offset':16, 'type': '16p'},  # パスカル文字列での不確定名称
    'OBJTYPE': {'offset':32, 'type': '<H'},   # アイテム種別
    'ALIGN':  {'offset':34, 'type': '<H'},    # 属性
    'CURSED': {'offset':36, 'type': '<h'},    # 呪いの有無
    'SPECIAL': {'offset':38, 'type': '<h'},   # スペシャルパワー番号
    'CHANGETO': {'offset':40, 'type': '<H'},  # 使用後のアイテム
    'CHGCHANC': {'offset':42, 'type': '<H'},  # 使用後の変化確率
    'PRICE_0':{'offset':44, 'type': '<H'},  # 価格下位4桁
    'PRICE_1':{'offset':46, 'type': '<H'},  # 価格中位4桁
    'PRICE_2':{'offset':48, 'type': '<H'}, # 価格上位4桁
    'BOLTACXX':{'offset':50, 'type': '<h'}, # 在庫
    'SPELLPWR':{'offset':52, 'type': '<H'}, # 使用時の呪文番号
    'CLASSUSE':{'offset':54, 'type': '<H'}, # 装備可能な職業
    'HEALPTS':{'offset':56, 'type': '<H'}, # リジェネレレーション値
    'WEPVSTY2':{'offset':58, 'type': '<H'}, # 防御特性ビットマップ
    'WEPVSTY3':{'offset':60, 'type': '<H'}, # 抵抗属性ビットマップ
    'ARMORMOD':{'offset':62, 'type': '<H'}, # アーマクラス補正値
    'WEPHITMD':{'offset':64, 'type': '<H'}, # 命中補正値
    'WEPHPDAM_0':{'offset':66, 'type': '<H'}, # 攻撃ダイス試行回数
    'WEPHPDAM_1':{'offset':68, 'type': '<H'}, # 攻撃ダイス面数
    'WEPHPDAM_2':{'offset':70, 'type': '<H'}, # 攻撃ダイス加算値
    'XTRASWNG':{'offset':72, 'type': '<H'}, # 最大攻撃回数
    'CRITHITM':{'offset':74, 'type': '<h'}, # クリティカル付与
    'WEPVSTYP':{'offset':76, 'type': '<H'}, # 倍打特性ビットマップ
}

class itemDecoder(dataEntryDecoder):


    def _dict2ItemDataEntry(self, scn:scnDecoder, decode_dict:dict[str,Any])->WizardryItemDataEntry:
        """unpackしたアイテム情報をpythonのオブジェクトに変換

        Args:
            scn (scnDecoder): シナリオ解析機
            decode_dict (dict[str,Any]): unpackしたアイテム情報の辞書(unpackしたデータの要素名->bytes列のタプル)

        Returns:
            WizardryItemDataEntry: pythonのオブジェクトであらわしたアイテム情報
        """
        res=WizardryItemDataEntry(name=modules.consts.UNKNOWN_STRING, name_unknown=modules.consts.UNKNOWN_STRING,
                                  obj_type_value=0, obj_type_string=modules.consts.UNKNOWN_STRING,
                                  alignment_value=0, alignment_string=modules.consts.UNKNOWN_STRING,
                                  cursed=False, special_value=0, change_to_value=0, change_percentage=0,
                                  price_value=0, stock_value=0, spell_power_value=0, class_use_value=0,
                                  class_use_string=modules.consts.UNKNOWN_STRING,class_use_dic={},
                                  heal_pts=0,
                                  wepvsty2_value=0, prot_dic={},
                                  wepvsty3_value=0, resist_dic={},
                                  ac_mod_value=0,
                                  wephitmd_value=0, wephpdam=dice_type(0,0,0),
                                  swing_count_value=0, critical_hit=False,
                                  wepvstyp_value=0, purpose_dic={})

        for key in decode_dict.keys():
            match key:
                case 'NAMEUNK': # 不確定名称
                    res.name_unknown=decode_dict[key][0].decode()
                case 'NAME': # 名称
                    res.name=decode_dict[key][0].decode()
                case 'OBJTYPE': # アイテム種別
                    res.obj_type_value=int(decode_dict[key][0])
                    if res.obj_type_value in modules.consts.OBJ_TYPE_TO_STR:
                        res.obj_type_string=modules.consts.OBJ_TYPE_TO_STR[res.obj_type_value]
                    else:
                        res.obj_type_string=modules.consts.UNKNOWN_STRING
                case 'ALIGN':
                    res.alignment_value=int(decode_dict[key][0])
                    if res.alignment_value in scn.toc.ALIGN:
                        res.alignment_string=scn.toc.ALIGN[res.alignment_value]
                    else:
                        res.alignment_string=modules.consts.UNKNOWN_STRING
                case 'CURSED':
                    v=int(decode_dict[key][0])
                    if v != 0:
                        res.cursed=True
                    else:
                        res.cursed=False
                case 'SPECIAL':
                    v=int(decode_dict[key][0])
                    if v > 0:
                        res.special_value = v
                    else:
                        res.special_value = -1
                case 'CHANGETO':
                    res.change_to_value=int(decode_dict[key][0])
                case 'CHGCHANC':
                    res.change_percentage=int(decode_dict[key][0])
                case 'BOLTACXX':
                    res.stock_value=int(decode_dict[key][0])
                case 'SPELLPWR':
                    res.spell_power_value=int(decode_dict[key][0])
                case 'CLASSUSE':
                    res.class_use_value=int(decode_dict[key][0])
                    res.class_use_string=word_to_use_string(res.class_use_value)
                    pass
                case 'HEALPTS':
                    res.heal_pts=int(decode_dict[key][0])
                case 'WEPVSTY2':
                    res.wepvsty2_value=int(decode_dict[key][0])
                    res.prot_dic=word_to_dic(word_value=res.wepvsty2_value, dic=modules.consts.ENEMY_CLASS_DIC)
                    pass
                case 'WEPVSTY3':
                    res.wepvsty3_value=int(decode_dict[key][0])
                    res.resist_dic=word_to_dic(word_value=res.wepvsty3_value, dic=modules.consts.RESIST_BREATH_DIC)
                    pass
                case 'ARMORMOD':
                    res.ac_mod_value=int(decode_dict[key][0])
                case 'WEPHITMD':
                    res.wephitmd_value=int(decode_dict[key][0])
                case 'XTRASWNG':
                    res.swing_count_value=int(decode_dict[key][0])
                case 'CRITHITM':
                    v=int(decode_dict[key][0])
                    if v != 0:
                        res.critical_hit=True
                    else:
                        res.critical_hit=False
                case 'WEPVSTYP':
                    res.wepvstyp_value=int(decode_dict[key][0])
                    res.purpose_dic=word_to_dic(word_value=res.wepvstyp_value, dic=modules.consts.ENEMY_CLASS_DIC)
                    pass
                case _:
                    pass
        #
        # 値段
        #
        assert 'PRICE_0' in decode_dict, f"Invalid PRICE"
        assert 'PRICE_1' in decode_dict, f"Invalid PRICE"
        assert 'PRICE_2' in decode_dict, f"Invalid PRICE"
        price  = int(decode_dict['PRICE_0'][0])
        price += int(decode_dict['PRICE_1'][0]) * 10000
        price += int(decode_dict['PRICE_2'][0]) * 100000000
        res.price_value=price
        #
        # ダメージダイス
        #
        assert 'WEPHPDAM_0' in decode_dict, f"Invalid WEPHPDAM"
        assert 'WEPHPDAM_1' in decode_dict, f"Invalid WEPHPDAM"
        assert 'WEPHPDAM_2' in decode_dict, f"Invalid WEPHPDAM"
        res.wephpdam=dice_type(int(decode_dict['WEPHPDAM_0'][0]),int(decode_dict['WEPHPDAM_1'][0]),int(decode_dict['WEPHPDAM_2'][0]))

        return res

    def decodeOneData(self, scn:scnDecoder, data: Any, index: int)->Optional[Any]:
        """シナリオデータファイル中のアイテムデータを解析する

        Args:
            scn (scnDecoder): シナリオ解析機
            data (Any): シナリオデータファイル情報
            index (int): 調査対象アイテムのインデクス

        Returns:
            Optional[Any]: 解析結果のオブジェクト, インデクスがレンジ外の場合, None
        """
        nr_items=scn.toc.RECPERDK[modules.consts.ZOBJECT] # アイテムの数

        if 0 > index or index >= nr_items:
            return None # 不正インデクス

        # 対象のアイテム情報開始オフセット位置(単位:バイト)を得る
        data_offset = scn.calcDataEntryOffset(category=modules.consts.ZOBJECT, item_len=ITEM_ENTRY_SIZE, index=index)

        # 解析対象データをunpackする
        decode_dict = getDecodeDict(data=data,layout=WizardryItemDataEntryDef,offset=data_offset)

        # unpackしたデータをpythonのオブジェクトに変換
        return self._dict2ItemDataEntry(scn=scn, decode_dict=decode_dict)