#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file msgDecoder.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief メッセージ情報を解析する実装部
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details メッセージ情報を解析する実装部

from __future__ import annotations # 型定義のみを参照する
from typing import TYPE_CHECKING   # 型チェック実施判定
from typing import Any,Optional

if TYPE_CHECKING:
    pass

#
# 標準モジュールの読込み
#
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.msgDecoder import msgDecoder
from modules.datadef import WizardryMessageData,WizardryMessageDataEntry
from modules.utils import getDecodeDict
import modules.consts

"""メッセージ情報のPascal定義
         STRBUFF  : RECORD
                      BUFF: STRING[ 38]; (* メッセージ文字列 *)
                      ENDMSG : BOOLEAN;  (* メッセージ終端の場合真 *)
                    END;
"""
# メッセージ情報のサイズ(単位:バイト)
MSG_ENTRY_SIZE=42

# メッセージ情報のデータレイアウト
WizardryMessageDataEntryDef:dict[str,Any]={
    'BUFF': {'offset':0, 'type': '39p'},    # パスカル文字列でのメッセージ文字列
    'ENDMSG': {'offset':40, 'type': '<h'},  # 終端判定
}

class messageDecoder(msgDecoder):
    """メッセージ解析"""

    def _line_number_to_offset(self, line_num:int)->int:

        # 対象メッセージの開始ブロック位置(単位:ブロック)を得る
        blk_no = line_num // modules.consts.MSG_PER_BLK

        # 対象メッセージのブロック内オフセットアドレス(単位:バイト)を得る
        offset = (line_num % modules.consts.MSG_PER_BLK) * MSG_ENTRY_SIZE

        # データオフセットアドレス
        data_offset = blk_no * modules.consts.BLK_SIZ + offset

        return data_offset

    def _decodeOneMessage(self, data:Any, line_num:int)->tuple[int,Optional[WizardryMessageDataEntry]]:

        msg_data_size = len(data) # ファイル長
        msg = WizardryMessageDataEntry(num=-1, lines=[])
        cur_line_num = line_num # 読み取るメッセージの行番号
        while True:

            # オフセット位置を得る
            data_offset = self._line_number_to_offset(line_num=cur_line_num)
            if data_offset >= msg_data_size:
                break # 不正オフセット

            # 解析対象データをunpackする
            decode_dict = getDecodeDict(data=data,layout=WizardryMessageDataEntryDef,offset=data_offset)

            line = decode_dict['BUFF'][0].decode()  # 文字列をデコード
            end_msg = int(decode_dict['ENDMSG'][0]) # 終端判定

            msg.lines.append(line) # 行を追加

            cur_line_num += 1 # 次の行へ

            if end_msg != 0: # メッセージ終端
                break

        if len(msg.lines) == 0: # 空の場合
            return cur_line_num,None

        msg.num = line_num # 番号を設定

        return cur_line_num,msg

    def decodeMessageFile(self, data:Any)->WizardryMessageData:
        """メッセージ解析

        Args:
            data (Any): メッセージ情報のイメージ

        Returns:
            WizardryMessageData: メッセージ情報
        """

        msg_data_size = len(data) # ファイル長

        res = WizardryMessageData(messages={})

        line_num = 0 # 行番号を初期化
        data_offset = self._line_number_to_offset(line_num=line_num)
        while msg_data_size > data_offset:

            # メッセージを一つ解析
            line_num, msg = self._decodeOneMessage(data=data, line_num=line_num)

            if msg: # 有効なデータがある場合
                res.messages[msg.num] = msg # メッセージを登録する

            # 次のデータへ
            data_offset = self._line_number_to_offset(line_num=line_num)

        return res

if __name__ == "__main__":
    this_msg_file=modules.consts.DEFAULT_MSG_FILE
    msg_data=None
    with open(this_msg_file, 'rb') as fr:
        msg_data=fr.read()

    decoder = messageDecoder()
    res = decoder.decodeMessageFile(data=msg_data)
    pass