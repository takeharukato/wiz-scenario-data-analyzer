#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file msgDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief メッセージ解析処理のIF定義
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details メッセージ解析処理のIF定義

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
from typing import Any

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os
from abc import ABC, abstractmethod

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.datadef import WizardryMessageData

class msgDecoder(ABC):

    @abstractmethod
    def decodeMessageFile(self, data:Any)->WizardryMessageData:
        """メッセージデータファイル中のデータを解析する

        Args:
            data (Any): メッセージファイル情報

        Returns:
            WizardryMessageData: 解析結果のオブジェクト
        """
        return
