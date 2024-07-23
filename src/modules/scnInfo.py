#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file scnInfoImpl.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief シナリオ情報処理
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオ情報処理

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
from modules.datadef import WizardrySCNTOC
from modules.cmdLineOptions import cmdLineOptions

class scnInfo(ABC):

    @abstractmethod
    def __init__(self, scenario:Any, message:Any, opts:cmdLineOptions) -> None:
        """シナリオ情報を初期化する

        Args:
            scenario (Any): シナリオ情報のメモリイメージ
            message  (Any): メッセージ情報のメモリイメージ
            opts (cmdLineOptions): オプション情報
        """
        return

    @abstractmethod
    def readContents(self)->None:
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

    @abstractmethod
    def getWallInfo(self, x:int, y:int, z:int, dir:int)->int:
        """壁情報を得る

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            dir (int): 向き

        Returns:
            int: 壁情報
        """
        return

    @property
    @abstractmethod
    def toc(self)->WizardrySCNTOC:
        """目次情報
        """
        return
