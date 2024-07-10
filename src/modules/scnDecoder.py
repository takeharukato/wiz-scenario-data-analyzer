#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file scnDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報解析機のIF定義
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報解析機のIF定義

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
from abc import ABC, abstractmethod

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.datadef import WizardrySCNTOC

class scnDecoder(ABC):

    @abstractmethod
    def decodeData(self, data:Any, offset:int=-1)->Any:
        """シナリオデータファイル中のデータを解析する

        Args:
            data (Any): シナリオデータファイル情報
            offset (int, optional): シナリオデータファイル中の開始オフセット(単位:バイト). Defaults to -1(自動判定).

        Returns:
            Any: 解析結果のオブジェクト
        """
        return

    @abstractmethod
    def calcDataEntryOffset(self, toc: WizardrySCNTOC, category: str, item_len:int, index: int)->int:
        """シナリオ情報先頭からのオフセット位置(単位:バイト)を算出する

        Args:
            toc (WizardrySCNTOC): 目次情報
            category (str): 目次の項目
                - ZZERO    シナリオ情報
                - ZMAZE    迷宮フロア情報
                - ZENEMY   モンスター情報
                - ZREWARD  報酬情報
                - ZOBJECT  アイテム情報
                - ZCHAR    キャラクター名簿
                - ZSPCCHRS モンスター/宝箱画像
                - ZEXP     経験値表
            item_len (int): アイテム一つ当たりのサイズ(単位:バイト)
            index (int): アイテムの配列中のインデクス

        Returns:
            int: シナリオ情報先頭からのオフセット位置(単位:バイト)
        """
        return

    @property
    @abstractmethod
    def toc(self)->WizardrySCNTOC:
        """目次情報
        """
        return