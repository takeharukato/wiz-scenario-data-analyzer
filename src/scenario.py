#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file scenario.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief ファイル内のコードの概要
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details シナリオデータファイル解析

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
from typing import Optional,Any

"""
使用法: scenario.py [-h] [-v] 入力ファイル 出力ファイル

処理概要

位置引数:
  入力ファイル シナリオファイルのバイナリファイル
  出力ファイル 将来予約

オプション引数:
  -h, --help     ヘルプを表示して修了
  -v, --version  バージョン番号を表示して修了
  -o  --option1  オプション引数の説明
具体的な使用方法
"""


#
# 標準モジュールの読込み
#
import sys
import argparse   # 引数解析
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

if TYPE_CHECKING:
    pass

from modules.datadef import WizardrySCNTOC,WizardryMonsterDataEntry
from modules.scnDecoder import scnDecoder
from modules.TOCDecoder import TOCDecoder
from modules.monsterDecoder import monsterDecoder
import modules.consts

#
# 非標準モジュールの読込み
#

#
# 型定義
#

## クラス定義
#
class ReadScenario:

    """
    クラス変数
    """

    ## 入力ファイル名
    #
    infile = None

    ## 出力ファイル名
    #
    outfile = None

    ## デバッグモードでの動作
    #
    is_debug = False

    ## 引数情報を格納した名前空間オブジェクト
    #
    __args = None

    _scenario:Any
    """シナリオ情報ファイルのメモリイメージ"""

    _toc_decoder:scnDecoder
    """目次情報"""
    _monsters:dict[int,WizardryMonsterDataEntry]
    """モンスター情報"""

    ## 初期化
    #
    def __init__(self):

        #
        # コマンドライン解析に必要なクラス変数を初期化
        #

        #
        # コマンドラインを解析
        #
        self.__parse_cmdline() # コマンドラインを解析する

        #
        # 他のクラス変数の初期化
        #
        self.infile = self.__args.infile   # type: ignore 入力ファイル名の設定
        #self.outfile = self.__args.outfile # type: ignore 出力ファイル名の設定

        #
        # デバッグ出力の有効化
        #
        if self.__args.debug:     # type: ignore デバッグ出力有効時
            self.set_debug()      # デバッグモードを有効
        else:
            self.unset_debug()    # デバッグモードを無効

        self._monsters={}

        return

    def __parse_cmdline(self):
        """コマンドライン解析
        """

        cmdline = None # コマンドラインパーサー

        # コマンドラインオプション定義
        cmdline = argparse.ArgumentParser(                         \
                description="",
                epilog="")

        #
        # 位置引数定義
        #

        #  第1位置引数に入力ファイルを指定
        cmdline.add_argument('infile', help='入力ファイル')

        #  第2位置引数に入力ファイルを指定
        # cmdline.add_argument('outfile', help='出力ファイル')

        #
        # オプション引数
        #

        # バージョン表示オプション
        cmdline.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

        # デバッグ表示有効化
        cmdline.add_argument('-d', '--debug', help='デバッグ表示を有効化',
                            action='store_true', dest='debug')

        self.__args = cmdline.parse_args() # コマンドラインを解析

    ## デバッグモードを有効にしデバッグレベルのログを残す
    #
    def set_debug(self):

        self.is_debug = True # デバッグモードを有効にする

    ## デバッグモードを無効にし情報レベルのログを残す
    #
    def unset_debug(self)->None:

        self.is_debug = False # デバッグモードを無効にする
        return

    def readTOC(self, data:Any)->None:
        """目次情報を読込む

        Args:
            data (Any): シナリオデータ
        """

        self._toc_decoder=TOCDecoder(data=data)
        self._toc_decoder.decodeData(data=data, offset=0)

        return

    def readMonsterTable(self, data:Any)->None:
        decoder=monsterDecoder()
        nr_monsters=self.toc.RECPERDK[modules.consts.ZENEMY]
        for idx in range(nr_monsters):
            monster=decoder.decodeOneData(scn=self._toc_decoder, data=data, index=idx)
            if isinstance(monster, WizardryMonsterDataEntry):
                self._monsters[idx]=monster

        return

    def doConvert(self, infile:Optional[str]=None, outfile:Optional[str]=None)->None:
        """シナリオ情報を変換する

        Args:
            infile (Optional[str], optional): 入力ファイル. Defaults to None("SCENARIO.DATA"を読み込む).
            outfile (Optional[str], optional): 出力ファイル. Defaults to None.
        """
        this_infile=self.infile
        if not infile or not this_infile:
            this_infile=modules.consts.DEFAULT_SCENARIO_DATA_FILE

        self._scenario=None
        with open(this_infile, 'rb') as fr:
            self._scenario=fr.read()

        self.readTOC(data=self._scenario) # 目次情報を読み込む
        self.readMonsterTable(data=self._scenario) # モンスター情報を読み込む
        return

    @property
    def toc(self)->WizardrySCNTOC:
        """目次情報
        """
        return self._toc_decoder.toc

## メイン処理
#
if __name__ == '__main__':

    cmd = ReadScenario() # オブジェクトを生成
    cmd.doConvert()
    pass
