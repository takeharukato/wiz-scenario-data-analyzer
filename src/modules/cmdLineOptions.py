#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file cmdLineOptions.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief コマンドラインオプション
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details コマンドラインオプション

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os
from dataclasses import dataclass
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@dataclass
class cmdLineOptions:
    """オプション情報"""

    is_debug:bool
    """デバッグモード"""
    strategy_num:int
    """ビットマップ生成ストラテジ番号"""
