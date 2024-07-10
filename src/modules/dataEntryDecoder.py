#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file dataEntryDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief データエントリ解析処理のIF定義
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details データエントリ解析処理のIF定義

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
from typing import TextIO
from typing import Any,Optional

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os
from abc import ABC, abstractmethod

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.scnDecoder import scnDecoder

class dataEntryDecoder(ABC):

    @abstractmethod
    def decodeOneData(self, scn:scnDecoder, data:Any, index:int)->Optional[Any]:
        """シナリオデータファイル中のデータを解析する

        Args:
            scn (scnDecoder): シナリオ解析機
            data (Any): シナリオデータファイル情報
            index (int): 調査対象アイテムのインデクス

        Returns:
            Optional[Any]: 解析結果のオブジェクト, インデクスがレンジ外の場合, None
        """
        return
