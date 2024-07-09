#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file datadef.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief データクラス定義
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details データクラス定義

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
#from typing import Any,Optional

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
class WizardrySCNTOC:
    """目次情報"""
    game_name:str
    """シナリオ名"""
    RECPER2B:dict[str,int]
    """キャッシュ領域( 1KiB= 2 Block (2B) (512Byte x 2 Byte) )に格納可能なデータ数"""
    RECPERDK:dict[str,int]
    """最大データ数"""
    BLOFF:dict[str,int]
    """オフセットブロック数(単位:ブロック)"""
    RACE:dict[int,str]
    """種族名"""
    STATUS:dict[int,str]
    """状態名"""
    ALIGN:dict[int,str]
    """属性(アラインメント)名"""
    SPELLHSH:dict[int,int]
    """呪文ハッシュ値"""
    SPELLGRP:dict[int,int]
    """呪文グループ"""
    SPELL012:dict[int,int]
    """呪文の対象者選択方式"""
