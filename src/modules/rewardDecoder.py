#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file rewardDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報の報酬データを解析する
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報の報酬データを解析する

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
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.dataEntryDecoder import dataEntryDecoder
from modules.datadef import WizardrySCNTOC, WizardryRewardDataEntry, WizardryRewardInfo
from modules.utils import getDecodeDict,calcDataEntryOffset
import modules.consts

"""報酬情報のPascal定義
        TREWARD = RECORD
            BCHEST   : BOOLEAN; (* 宝箱を持っている場合は真 *)
            BTRAPTYP : PACKED ARRAY[ 0..7] OF BOOLEAN; (* 罠の種類 *)
            REWRDCNT : INTEGER; (* 報酬の数 *)
            REWARDXX : ARRAY[ 1..9] OF TREWARDX; (* 報酬情報 *)
          END;

        TREWARDX = RECORD
            REWDPERC : INTEGER; (* 報酬取得確率 *)
            BITEM    : INTEGER; (* アイテムを取得する場合は真 *)
            REWDCALC : RECORD CASE INTEGER OF
                1: (GOLD:  RECORD (* 取得報奨金額情報 *)
                      TRIES   : INTEGER; (* ダイスを振る回数 *)
                      AVEAMT  : INTEGER; (* ダイスの面数 *)
                      MINADD  : INTEGER; (* ダイスに対する補正値 *)
                      MULTX   : INTEGER; (* 報酬補正乗数 *)
                      TRIES2  : INTEGER; (* ダイスを振る回数2 *)
                      AVEAMT2 : INTEGER; (* ダイスの面数2 *)
                      MINADD2 : INTEGER; (* ダイスに対する補正値2 *)
                    END);
                2: (ITEM:  RECORD (* アイテム情報 *)
                      MININDX  : INTEGER; (* 最小アイテム番号 *)
                      MFACTOR  : INTEGER; (* n番目に見つけたアイテムに対するアイテム番号にかける乗数 *)
                      MAXTIMES : INTEGER; (* 宝箱から取得できる最大アイテム獲得数 *)
                      RANGE    : INTEGER; (* アイテム番号を算出する際に使用するダイスの面数 *)
                      PERCBIGR : INTEGER; (* アイテム取得確率 *)
                      UNUSEDXX : INTEGER; (* 未使用 *)
                      UNUSEDYY : INTEGER; (* 未使用 *)
                    END);
              END;
          END;

"""

# 報酬情報ヘッダ部のサイズ(単位:バイト)
REWARD_HEADER_SIZE=6
# 報酬情報エントリ部のサイズ(単位:バイト)
REWARD_INFO_SIZE=18
# 報酬情報一つ当たりの報酬情報エントリ部の個数(単位:個)
REWARD_NR_INFO=9
# 報酬情報一つ当たりのサイズ(384バイト)
REWARD_ENTRY_SIZE=REWARD_HEADER_SIZE + REWARD_INFO_SIZE * REWARD_NR_INFO
# 報酬情報ヘッダ部のデータレイアウト
WizardryRewardHeaderDef:dict[str,Any]={
    'BCHEST': {'offset':0, 'type': '<h'},     # 宝箱の有無
    'BTRAPTYP': {'offset':2, 'type': '<H'},   # 罠の種別
    'REWRDCNT': {'offset':4, 'type': '<H'},   # 報酬の数
}
# 詳細報酬情報部(9個)のデータレイアウト
WizardryRewardInfoDef:dict[str,Any]={
    'REWDPERC': {'offset':0, 'type': '<H'},     # 報酬獲得率
    'BITEM':    {'offset':2, 'type': '<h'},     # アイテムの有無
    'REWDCALC_0': {'offset':4, 'type': '<H'},   # 報酬情報(TRIES/MININDX)
    'REWDCALC_1': {'offset':6, 'type': '<H'},   # 報酬情報(AVEAMT/MFACTOR)
    'REWDCALC_2': {'offset':8, 'type': '<H'},   # 報酬情報(MINADD/MAXTIMES)
    'REWDCALC_3': {'offset':10, 'type': '<H'},  # 報酬情報(MULTX/RANGE)
    'REWDCALC_4': {'offset':12, 'type': '<H'},  # 報酬情報(TRIES2/PERCBIGR)
    'REWDCALC_5': {'offset':14, 'type': '<H'},  # 報酬情報(AVEAMT2/UNUSEDXX)
    'REWDCALC_6': {'offset':16, 'type': '<H'},  # 報酬情報(MINADD2/UNUSEDYY)
}

class rewardDecoder(dataEntryDecoder):

    def _setHeader(self, toc:WizardrySCNTOC, reward:WizardryRewardDataEntry, header:dict[str,Any])->None:

        v = int(header['BCHEST'][0])
        reward.in_chest_value=v
        if v != 0:
            reward.in_chest = True
        else:
            reward.in_chest = False
        reward.trap_type_value = int(header['BTRAPTYP'][0])
        reward.reward_count_value = int(header['REWRDCNT'][0])

        return

    def _setInfo(self, toc:WizardrySCNTOC, reward:WizardryRewardDataEntry, index:int, info:dict[str,Any])->None:

        new_inf=WizardryRewardInfo(percentage=0, has_item=False, has_item_value=0, reward_param={})

        new_inf.percentage = int(info['REWDPERC'][0])
        v = int(info['BITEM'][0])
        new_inf.has_item_value=v
        if v != 0:
            new_inf.has_item = True
        else:
            new_inf.has_item = False
        for key in (key for key in info if re.match("REWDCALC_", key)):
            idx = int(re.sub('REWDCALC_','',key))
            new_inf.reward_param[idx]=int(info[key][0])

        reward.rewards[index]=new_inf
        return

    def _dict2RewardDataEntry(self, toc:WizardrySCNTOC, header:dict[str,Any], info:dict[int,dict[str,Any]])->WizardryRewardDataEntry:

        res = WizardryRewardDataEntry(in_chest=False,
                                      in_chest_value=0,
                                      trap_type_value=0,
                                      reward_count_value=0,
                                      rewards={})
        # ヘッダ部を設定する
        self._setHeader(toc=toc, reward=res, header=header)
        for idx in info.keys():
            self._setInfo(toc=toc, reward=res, index=idx, info=info[idx])
        return res

    def decodeOneData(self, toc:WizardrySCNTOC, data: Any, index: int)->Optional[Any]:
        """シナリオデータファイル中のアイテムデータを解析する

        Args:
            toc (WizardrySCNTOC): 目次情報
            data (Any): シナリオデータファイル情報
            index (int): 調査対象アイテムのインデクス

        Returns:
            Optional[Any]: 解析結果のオブジェクト, インデクスがレンジ外の場合, None
        """

        reward_info_dic:dict[int,dict[str,Any]]={} # 詳細報酬情報の辞書

        nr_rewards=toc.RECPERDK[modules.consts.ZREWARD] # 報酬情報の数

        if 0 > index or index >= nr_rewards:
            return None # 不正インデクス

        # 対象の報酬情報開始オフセット位置(単位:バイト)を得る
        data_offset = calcDataEntryOffset(toc=toc, category=modules.consts.ZREWARD, item_len=REWARD_ENTRY_SIZE, index=index)

        # ヘッダ情報をunpackする
        header_dict=getDecodeDict(data=data, layout=WizardryRewardHeaderDef, offset=data_offset)

        # 報酬詳細情報の配列をunpackする
        for idx in range(REWARD_NR_INFO):
            reward_index = idx + 1 # 報酬番号は1番から開始するため1加算する
            reward_array_offset = idx * REWARD_INFO_SIZE # ヘッダ終了位置から詳細報酬情報までのオフセット(単位:バイト)
            reward_info_offset = data_offset + REWARD_HEADER_SIZE + reward_array_offset # 詳細報酬情報のシナリオファイル中でのオフセット(単位:バイト)
            # 報酬詳細情報をunpackする
            info_dict = getDecodeDict(data=data,layout=WizardryRewardInfoDef, offset=reward_info_offset)
            # 報酬詳細情報の辞書に格納する
            reward_info_dic[reward_index] = info_dict

        # unpackしたデータをpythonのオブジェクトに変換
        return self._dict2RewardDataEntry(toc=toc, header=header_dict, info=reward_info_dic)