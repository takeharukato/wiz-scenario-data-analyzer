#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file picColorFactory.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief モンスター/宝箱画像色決定ストラテジ生成クラス
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details モンスター/宝箱画像色決定ストラテジ生成クラス

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.picColorSimple import picColorStrategy,picColorSimple
from modules.picColorStandard import picColorStandard
import modules.consts

class picColorFactory:
    """ビットマップ生成ストラテジ生成クラス"""

    def create(self, strategy_num:int)->picColorStrategy:

        if strategy_num == modules.consts.BITMAP_STRATEGY_SIMPLE:
            # 出力される色情報を単純にマッピングする(白色に隣接する色ビットの補色処理を割愛する)
            return picColorSimple()

        # 標準的な色マッピングによるビットマップ生成
        return picColorStandard()