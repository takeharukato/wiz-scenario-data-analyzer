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
from typing import Optional

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

sys.path.append(os.path.dirname(__file__))

if TYPE_CHECKING:
    pass

from modules.scnInfoImpl import scnInfoImpl, scnInfo
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
    scenario_file = None

    ## メッセージファイル名
    #
    msg_file = None

    ## 出力ファイル名
    #
    outfile = None

    ## デバッグモードでの動作
    #
    is_debug = False

    ## 引数情報を格納した名前空間オブジェクト
    #
    __args = None

    _scnInfo:Optional[scnInfo]
    """シナリオ情報"""

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
        self.scenario_file = self.__args.scenario_file   # type: ignore 入力ファイル名の設定
        self.msg_file = self.__args.msg_file # type: ignore メッセージファイル名の設定
        #self.outfile = self.__args.outfile # type: ignore 出力ファイル名の設定

        #
        # デバッグ出力の有効化
        #
        if self.__args.debug:     # type: ignore デバッグ出力有効時
            self.set_debug()      # デバッグモードを有効
        else:
            self.unset_debug()    # デバッグモードを無効

        self._scnInfo=None

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
        cmdline.add_argument('scenario_file', help='シナリオファイル')

        #  第2位置引数にメッセージファイルを指定
        cmdline.add_argument('msg_file', help='メッセージファイル')

        #  第3位置引数に入力ファイルを指定
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

    def doConvert(self, outfile:Optional[str]=None)->None:
        """シナリオ情報を変換する

        Args:
            outfile (Optional[str], optional): 出力ファイル. Defaults to None.
        """

        msg_data=None

        this_infile=self.scenario_file
        if not this_infile:
            this_infile=modules.consts.DEFAULT_SCENARIO_DATA_FILE

        this_msg_file=self.msg_file
        if not this_msg_file:
            this_msg_file=modules.consts.DEFAULT_MSG_FILE

        with open(this_msg_file, 'rb') as fr:
            msg_data=fr.read()

        if not msg_data: # メッセージデータの読み取りに失敗した
            return

        with open(this_infile, 'rb') as fr:
            scenario=fr.read()
            # TODO: FactoryMethodを適用
            self._scnInfo=scnInfoImpl(scenario=scenario,message=msg_data)
            self._scnInfo.readContents()

        return

    def plainDump(self)->None:

        if not self._scnInfo:
            return
        self._scnInfo.plainDump(fp=sys.stdout)
        return

## メイン処理
#
if __name__ == '__main__':

    cmd = ReadScenario() # オブジェクトを生成
    cmd.doConvert()
    cmd.plainDump()
    pass
