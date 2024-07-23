#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file picColorStrategy.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief モンスター/宝箱画像色決定ストラテジ
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details モンスター/宝箱画像色決定ストラテジ

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os
from abc import ABC, abstractmethod

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.datadef import WizardryPicDataEntry

class picColorStrategy(ABC):

    @abstractmethod
    def updateColorImage(self, info:WizardryPicDataEntry)->None:
        """画像ファイルに出力するビットマップを更新する

        Args:
            info (WizardryPicDataEntry): モンスター/宝箱画像
        """
        return