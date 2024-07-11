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
from abc import ABC, abstractmethod

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class scnInfo(ABC):

    @abstractmethod
    def __init__(self, scenario:Any) -> None:
        """シナリオ情報を初期化する

        Args:
            scenario (Any): シナリオ情報のメモリイメージ
        """
        return

    @abstractmethod
    def doConvert(self)->None:
        """シナリオ情報を変換する
        """
        return
    @abstractmethod
    def plainDump(self, fp:TextIO)->None:
        """テキスト形式で表示する

        Args:
            fp (TextIO): 表示先ファイルのTextIO.
        """
        return
