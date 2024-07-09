#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file TOCDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の目次部分を解析する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の目次部分を解析する

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
import struct

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.scnDecoder import scnDecoder
from modules.datadef import WizardrySCNTOC
from modules.utils import decodePackedArrayUint16
import modules.consts

"""Table of contentsのPascal定義
        TSCNTOC = RECORD (* シナリオ情報 *)
            GAMENAME : STRING[ 40]; (* シナリオ名(シナリオ1の場合, 'PROVING GROUNDS OF THE MAD OVERLORD!') *)
            RECPER2B : ARRAY[ ZZERO..ZEXP] OF INTEGER; (* キャッシュ領域(1KiB)に格納可能なデータ数 *)
            RECPERDK : ARRAY[ ZZERO..ZEXP] OF INTEGER; (* 各シナリオ情報の最大データ数(例: ZCHARの場合, 最大登録キャラクタ数, ZMAZEの場合, 最大階層(PGMOの場合,10?) *)
            UNUSEDXX : ARRAY[ ZZERO..ZEXP] OF INTEGER; (* 未使用 *)
            BLOFF    : ARRAY[ ZZERO..ZEXP] OF INTEGER; (* 各シナリオ情報の格納先ディスクブロック番号(先頭からのオフセット数(単位ブロック:)) *)
            RACE     : ARRAY[ NORACE..HOBBIT]         OF STRING[ 9]; (* 種族を表す文字列(9文字) *)
            CLASS    : PACKED ARRAY[ FIGHTER..NINJA]  OF STRING[ 9]; (* 職業を表す文字列(9文字) *)
            STATUS   : ARRAY[ OK..LOST]               OF STRING[ 8]; (* 状態を表す文字列(8文字) *)
            ALIGN    : PACKED ARRAY[ UNALIGN..EVIL]   OF STRING[ 9]; (* 属性(アラインメント)を表す文字列(9文字) *)
            SPELLHSH : PACKED ARRAY[ 0..50] OF INTEGER;              (* 各呪文の連番から識別番号への変換テーブル *)
            SPELLGRP : PACKED ARRAY[ 0..50] OF 0..7;                 (* 各呪文の連番から呪文レベルへの変換テーブル *)
            SPELL012 : PACKED ARRAY[ 0..50] OF TSPEL012;             (* 各呪文の連番から呪文種別(対象者選択時に使用)への変換テーブル *)
          END;
"""

#
# Table of contents定数定義
#
TOC_NR_SPELLS=50 # 呪文の数
SPELL_GROUP_BITS_PER_LEVEL=3 # 呪文レベルを表現するビット数
SPELL_TYPE_BITS_PER_LEVEL=2  # 呪文用途を表現するビット数

# Table of Contentsのデータレイアウト
WizardrySCNTOCDef:dict[str,Any]={
    'GAMENAME': {'offset':0, 'type': '40p'},   # パスカル文字列でのシナリオ名

    'RECPER2B_0': {'offset':42, 'type': '<H'}, # ZZERO(シナリオ情報自身の情報)
    'RECPER2B_1': {'offset':44, 'type': '<H'}, # ZMAZE(迷宮情報)
    'RECPER2B_2': {'offset':46, 'type': '<H'}, # ZENEMY(モンスター情報)
    'RECPER2B_3': {'offset':48, 'type': '<H'}, # ZREWARD(3 報酬情報),
    'RECPER2B_4': {'offset':50, 'type': '<H'}, # ZOBJECT(4 アイテム情報),
    'RECPER2B_5': {'offset':52, 'type': '<H'}, # ZCHAR(5 キャラクタ名簿),
    'RECPER2B_6': {'offset':54, 'type': '<H'}, # ZSPCCHRS(6 魔物/宝箱/報酬のグラフィック),
    'RECPER2B_7': {'offset':56, 'type': '<H'}, # ZEXP(7 経験値表)

    'RECPERDK_0': {'offset':58, 'type': '<H'}, # ZZERO(シナリオ情報自身の情報)
    'RECPERDK_1': {'offset':60, 'type': '<H'}, # ZMAZE(迷宮情報)
    'RECPERDK_2': {'offset':62, 'type': '<H'}, # ZENEMY(モンスター情報)
    'RECPERDK_3': {'offset':64, 'type': '<H'}, # ZREWARD(3 報酬情報),
    'RECPERDK_4': {'offset':66, 'type': '<H'}, # ZOBJECT(4 アイテム情報),
    'RECPERDK_5': {'offset':68, 'type': '<H'}, # ZCHAR(5 キャラクタ名簿),
    'RECPERDK_6': {'offset':70, 'type': '<H'}, # ZSPCCHRS(6 魔物/宝箱/報酬のグラフィック),
    'RECPERDK_7': {'offset':72, 'type': '<H'}, # ZEXP(7 経験値表)

    'BLOFF_0': {'offset':90, 'type': '<H'}, # ZZERO(シナリオ情報自身の情報)
    'BLOFF_1': {'offset':92, 'type': '<H'}, # ZMAZE(迷宮情報)
    'BLOFF_2': {'offset':94, 'type': '<H'}, # ZENEMY(モンスター情報)
    'BLOFF_3': {'offset':96, 'type': '<H'}, # ZREWARD(3 報酬情報),
    'BLOFF_4': {'offset':98, 'type': '<H'}, # ZOBJECT(4 アイテム情報),
    'BLOFF_5': {'offset':100, 'type': '<H'}, # ZCHAR(5 キャラクタ名簿),
    'BLOFF_6': {'offset':102, 'type': '<H'}, # ZSPCCHRS(6 魔物/宝箱/報酬のグラフィック),
    'BLOFF_7': {'offset':104, 'type': '<H'}, # ZEXP(7 経験値表)

    'RACE_0':  {'offset':106, 'type': '9p'}, # NORACE種族名
    'RACE_1':  {'offset':116, 'type': '9p'}, # HUMAN種族名
    'RACE_2':  {'offset':126, 'type': '9p'}, # ELF種族名
    'RACE_3':  {'offset':136, 'type': '9p'}, # DWARF種族名
    'RACE_4':  {'offset':146, 'type': '9p'}, # GNOME種族名
    'RACE_5':  {'offset':156, 'type': '9p'}, # HOBBIT種族名

    'CLS_0':   {'offset':166, 'type': '9p'}, # FIGHTER職業名
    'CLS_1':   {'offset':176, 'type': '9p'}, # MAGE職業名
    'CLS_2':   {'offset':186, 'type': '9p'}, # PRIEST職業名
    'CLS_3':   {'offset':196, 'type': '9p'}, # THIEF職業名
    'CLS_4':   {'offset':206, 'type': '9p'}, # BISHOP職業名
    'CLS_5':   {'offset':216, 'type': '9p'}, # SAMURAI職業名
    'CLS_6':   {'offset':226, 'type': '9p'}, # LORD職業名
    'CLS_7':   {'offset':236, 'type': '9p'}, # NINJA職業名

    'STATUS_0': {'offset':246, 'type': '8p'}, # OK状態名
    'STATUS_1': {'offset':256, 'type': '8p'}, # AFRAID状態名
    'STATUS_2': {'offset':266, 'type': '8p'}, # ASLEEP状態名
    'STATUS_3': {'offset':276, 'type': '8p'}, # P-LYZE状態名
    'STATUS_4': {'offset':286, 'type': '8p'}, # STONED状態名
    'STATUS_5': {'offset':296, 'type': '8p'}, # DEAD状態名
    'STATUS_6': {'offset':306, 'type': '8p'}, # ASHES状態名
    'STATUS_7': {'offset':316, 'type': '8p'}, # LOST状態名

    'ALIGN_0':  {'offset':326, 'type': '9p'}, # UNALIGN属性(アラインメント)
    'ALIGN_1':  {'offset':336, 'type': '9p'}, # GOOD属性(アラインメント)
    'ALIGN_2':  {'offset':346, 'type': '9p'}, # NEUTRAL属性(アラインメント)
    'ALIGN_3':  {'offset':356, 'type': '9p'}, # EVIL属性(アラインメント)

    'SPELLHSH_0':  {'offset':366, 'type': '<h'}, # スペルハッシュ値(無効エントリ)
    'SPELLHSH_1':  {'offset':368, 'type': '<H'}, # スペルハッシュ値(HALITO)
    'SPELLHSH_2':  {'offset':370, 'type': '<H'}, # スペルハッシュ値(MOGREF)
    'SPELLHSH_3':  {'offset':372, 'type': '<H'}, # スペルハッシュ値(KATINO)
    'SPELLHSH_4':  {'offset':374, 'type': '<H'}, # スペルハッシュ値(DUMAPIC)
    'SPELLHSH_5':  {'offset':376, 'type': '<H'}, # スペルハッシュ値(DILTO)
    'SPELLHSH_6':  {'offset':378, 'type': '<H'}, # スペルハッシュ値(SOPIC)
    'SPELLHSH_7':  {'offset':380, 'type': '<H'}, # スペルハッシュ値(MAHALITO)
    'SPELLHSH_8':  {'offset':382, 'type': '<H'}, # スペルハッシュ値(MOLITO)
    'SPELLHSH_9':  {'offset':384, 'type': '<H'}, # スペルハッシュ値(MORLIS)
    'SPELLHSH_10':  {'offset':386, 'type': '<H'}, # スペルハッシュ値(DALTO)
    'SPELLHSH_11':  {'offset':388, 'type': '<H'}, # スペルハッシュ値(LAHALITO)
    'SPELLHSH_12':  {'offset':390, 'type': '<H'}, # スペルハッシュ値(MAMORLIS)
    'SPELLHSH_13':  {'offset':392, 'type': '<H'}, # スペルハッシュ値(MAKANITO)
    'SPELLHSH_14':  {'offset':394, 'type': '<H'}, # スペルハッシュ値(MADALTO)
    'SPELLHSH_15':  {'offset':396, 'type': '<H'}, # スペルハッシュ値(LAKANITO)
    'SPELLHSH_16':  {'offset':398, 'type': '<H'}, # スペルハッシュ値(ZILWAN)
    'SPELLHSH_17':  {'offset':400, 'type': '<H'}, # スペルハッシュ値(MASOPIC)
    'SPELLHSH_18':  {'offset':402, 'type': '<H'}, # スペルハッシュ値(HAMAN)
    'SPELLHSH_19':  {'offset':404, 'type': '<H'}, # スペルハッシュ値(MALOR)
    'SPELLHSH_20':  {'offset':406, 'type': '<H'}, # スペルハッシュ値(MAHAMAN)
    'SPELLHSH_21':  {'offset':408, 'type': '<H'}, # スペルハッシュ値(TILTOWAIT)
    'SPELLHSH_22':  {'offset':410, 'type': '<H'}, # スペルハッシュ値(KALKI)
    'SPELLHSH_23':  {'offset':412, 'type': '<H'}, # スペルハッシュ値(DIOS)
    'SPELLHSH_24':  {'offset':414, 'type': '<H'}, # スペルハッシュ値(BADIOS)
    'SPELLHSH_25':  {'offset':416, 'type': '<H'}, # スペルハッシュ値(MILWA)
    'SPELLHSH_26':  {'offset':418, 'type': '<H'}, # スペルハッシュ値(PORFIC)
    'SPELLHSH_27':  {'offset':420, 'type': '<H'}, # スペルハッシュ値(MATU)
    'SPELLHSH_28':  {'offset':422, 'type': '<H'}, # スペルハッシュ値(CALFO)
    'SPELLHSH_29':  {'offset':424, 'type': '<H'}, # スペルハッシュ値(MANIFO)
    'SPELLHSH_30':  {'offset':426, 'type': '<H'}, # スペルハッシュ値(MONTINO)
    'SPELLHSH_31':  {'offset':428, 'type': '<H'}, # スペルハッシュ値(LOMILWA)
    'SPELLHSH_32':  {'offset':430, 'type': '<H'}, # スペルハッシュ値(DIALKO)
    'SPELLHSH_33':  {'offset':432, 'type': '<H'}, # スペルハッシュ値(LATUMAPIC)
    'SPELLHSH_34':  {'offset':434, 'type': '<H'}, # スペルハッシュ値(BAMATU)
    'SPELLHSH_35':  {'offset':436, 'type': '<H'}, # スペルハッシュ値(DIAL)
    'SPELLHSH_36':  {'offset':438, 'type': '<H'}, # スペルハッシュ値(BADIAL)
    'SPELLHSH_37':  {'offset':440, 'type': '<H'}, # スペルハッシュ値(LATUMOFIS)
    'SPELLHSH_38':  {'offset':442, 'type': '<H'}, # スペルハッシュ値(MAPORFIC)
    'SPELLHSH_39':  {'offset':444, 'type': '<H'}, # スペルハッシュ値(DIALMA)
    'SPELLHSH_40':  {'offset':446, 'type': '<H'}, # スペルハッシュ値(BADIALMA)
    'SPELLHSH_41':  {'offset':448, 'type': '<H'}, # スペルハッシュ値(LITOKAN)
    'SPELLHSH_42':  {'offset':450, 'type': '<H'}, # スペルハッシュ値(KANDI)
    'SPELLHSH_43':  {'offset':452, 'type': '<H'}, # スペルハッシュ値(DI)
    'SPELLHSH_44':  {'offset':454, 'type': '<H'}, # スペルハッシュ値(BADI)
    'SPELLHSH_45':  {'offset':456, 'type': '<H'}, # スペルハッシュ値(LORTO)
    'SPELLHSH_46':  {'offset':458, 'type': '<H'}, # スペルハッシュ値(MADI)
    'SPELLHSH_47':  {'offset':460, 'type': '<H'}, # スペルハッシュ値(MABADI)
    'SPELLHSH_48':  {'offset':462, 'type': '<H'}, # スペルハッシュ値(LOKTOFEIT)
    'SPELLHSH_49':  {'offset':464, 'type': '<H'}, # スペルハッシュ値(MALIKTO)
    'SPELLHSH_50':  {'offset':466, 'type': '<H'}, # スペルハッシュ値(KADORTO)

    #
    # 呪文レベル情報(16ビット単位でのpacked array)
    #
    'SPELLGRP_0':   {'offset':468, 'type': '<H'},
    'SPELLGRP_1':   {'offset':470, 'type': '<H'},
    'SPELLGRP_2':   {'offset':472, 'type': '<H'},
    'SPELLGRP_3':   {'offset':474, 'type': '<H'},
    'SPELLGRP_4':   {'offset':476, 'type': '<H'},
    'SPELLGRP_5':   {'offset':478, 'type': '<H'},
    'SPELLGRP_6':   {'offset':480, 'type': '<H'},
    'SPELLGRP_7':   {'offset':482, 'type': '<H'},
    'SPELLGRP_8':   {'offset':484, 'type': '<H'},
    'SPELLGRP_9':   {'offset':486, 'type': '<H'},
    'SPELLGRP_10':   {'offset':488, 'type': '<H'},

    #
    # 呪文の用途(16ビット単位でのpacked array)
    #
    'SPELL012_0':   {'offset':490, 'type': '<H'},
    'SPELL012_1':   {'offset':492, 'type': '<H'},
    'SPELL012_2':   {'offset':494, 'type': '<H'},
    'SPELL012_3':   {'offset':496, 'type': '<H'},
    'SPELL012_4':   {'offset':498, 'type': '<H'},
    'SPELL012_5':   {'offset':500, 'type': '<H'},
    'SPELL012_6':   {'offset':502, 'type': '<H'},
    'SPELL012_7':   {'offset':504, 'type': '<H'},
}

class TOCDecoder(scnDecoder):
    def __init__(self) -> None:
        super().__init__()
        return

    def decodeSpellGroup(self,spell_group_dic:dict[int,int])->dict[int,int]:
        """呪文レベル情報を解析する

        Args:
            spell_group_dic (dict[int,int]): 呪文グループのワード配列(インデクス->値)

        Returns:
            dict[int,int]: 呪文の連番から呪文レベルへの配列
        """
        return decodePackedArrayUint16(data_dic=spell_group_dic,bit_len=3,max_index=TOC_NR_SPELLS)

    def decodeSpellType(self,spell_type_dic:dict[int,int])->dict[int,int]:
        """呪文使用用途種別(SPELL012)を解析する

        Args:
            spell_type_dic (dict[int,int]): 呪文使用用途種別のワード配列(インデクス->値)

        Returns:
            dict[int,int]: 呪文の連番から呪文使用用途種別への配列
        """

        return decodePackedArrayUint16(data_dic=spell_type_dic,bit_len=2,max_index=TOC_NR_SPELLS)

    def convertTableOfContents(self, data_dic:dict[str,Any])->WizardrySCNTOC:

        res = WizardrySCNTOC(game_name="",RECPER2B={},RECPERDK={},BLOFF={},RACE={},STATUS={},ALIGN={},SPELLHSH={},SPELLGRP={},SPELL012={})
        res.game_name=data_dic['GAMENAME'][0].decode()
        spell_group_dic:dict[int,int]={}
        spell_type_dic:dict[int,int]={}
        spell_bin_dic:dict[int,str]={} # TODO: 削除

        for key_name in ['RECPER2B','RECPERDK','BLOFF','RACE','CLS',
                         'STATUS','ALIGN','SPELLHSH','SPELLGRP','SPELL012']:
            for key in ( key for key in data_dic.keys() if re.match(key_name+'_', key) ):
                idx = int(re.sub(key_name + '_','', key))
                assert key_name not in ['RECPER2B','RECPERDK','BLOFF'] or idx in modules.consts.TOC_INDEX_TO_KEY, f"No key string found for {idx}"
                if key_name == 'RECPER2B':
                    assert idx not in res.RECPER2B, f"duplicate index {idx} in {key_name}"
                    res.RECPER2B[modules.consts.TOC_INDEX_TO_KEY[idx]]=int(data_dic[key][0])
                elif key_name == 'RECPERDK':
                    assert idx not in res.RECPERDK, f"duplicate index {idx} in {key_name}"
                    res.RECPERDK[modules.consts.TOC_INDEX_TO_KEY[idx]]=int(data_dic[key][0])
                elif key_name == 'BLOFF':
                    assert idx not in res.BLOFF, f"duplicate index {idx} in {key_name}"
                    res.BLOFF[modules.consts.TOC_INDEX_TO_KEY[idx]]=int(data_dic[key][0])
                elif key_name == 'RACE':
                    assert idx not in res.RACE, f"duplicate index {idx} in {key_name}"
                    res.RACE[idx]=data_dic[key][0].decode()
                elif key_name == 'STATUS':
                    assert idx not in res.STATUS, f"duplicate index {idx} in {key_name}"
                    res.STATUS[idx]=data_dic[key][0].decode()
                elif key_name == 'ALIGN':
                    assert idx not in res.ALIGN, f"duplicate index {idx} in {key_name}"
                    res.ALIGN[idx]=data_dic[key][0].decode()
                elif key_name == 'SPELLHSH':
                    assert idx not in res.SPELLHSH, f"duplicate index {idx} in {key_name}"
                    res.SPELLHSH[idx]=int(data_dic[key][0])
                elif key_name == 'SPELLGRP':
                    assert idx not in spell_group_dic, f"duplicate index {idx} in {key_name}"
                    spell_group_dic[idx]=int(data_dic[key][0])
                elif key_name == 'SPELL012':
                    assert idx not in spell_type_dic, f"duplicate index {idx} in {key_name}"
                    spell_type_dic[idx]=int(data_dic[key][0])
                    spell_bin_dic[idx]=f"{bin(spell_type_dic[idx])}"

        # 呪文グループ情報を解析する
        res.SPELLGRP=self.decodeSpellGroup(spell_group_dic=spell_group_dic)
        # 呪文用途情報を解析する
        res.SPELL012=self.decodeSpellType(spell_type_dic=spell_type_dic)

        return res

    def decodeData(self, data: Any, offset: int=-1) -> Any:
        """シナリオデータ目次の読込み

        Args:
            data (Any): シナリオデータファイルのメモリイメージ
            offset (int, optional): シナリオデータファイルのメモリイメージ中の目次情報のオフセット位置(単位:バイト). Defaults to 0.

        Returns:
            WizardrySCNTOC: シナリオ情報目次
        """

        decode_dict:dict[str,Any]={}

        for k, v in WizardrySCNTOCDef.items(): # データレイアウトのキーと値を得る
            # データ構造メンバのオフセット位置を得る
            member_offset = offset + v['offset']
            data_type = v['type']
            # pythonのデータ型に変換する
            decode_dict[k] = struct.unpack_from(data_type, data, member_offset)

        return self.convertTableOfContents(data_dic=decode_dict)
