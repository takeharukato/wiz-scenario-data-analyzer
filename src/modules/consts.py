#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# @file consts.py
# @version 1.0
# @author Takeharu KATO
# @date 2024.07.08
# @brief 定数定義
# @copyright 2024年 Takeharu KATO All Rights Reserved.
# @details 定数定義

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

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#
# 定数定義
#
# フォント
FONT_FACES = ['Arial', 'Courier New', 'Georgia', 'Times New Roman', 'Verdana', 'Comic Sans MS']

# ラスタイメージ形式名
RASTER_IMAGE_TYPE_PNG="PNG"
# ラスタイメージ形式名とrenderPMのフォーマット名との対応関係
RASTER_IMAGE_TYPE_DIC:dict[str,str]={
    RASTER_IMAGE_TYPE_PNG:"PNG",
}
# デフォルトラスタイメージ形式(PNG)
DEFAULT_RASTER_IMAGE_TYPE=RASTER_IMAGE_TYPE_PNG
# デフォルトラスタイメージ形式の拡張子(PNG)
DEFAULT_RASTER_IMAGE_EXT='png'

# Apple Pascal Operating System のディスクブロックサイズ(単位:バイト)
BLK_SIZ=512
# Wizardry キャッシュサイズ
WIZ_CACHE_SIZE=BLK_SIZ * 2
# シナリオデータファイル名
DEFAULT_SCENARIO_DATA_FILE="SCENARIO.DATA"
# メッセージファイル名
DEFAULT_MSG_FILE="SCENARIO.MESGS"
# データ解析結果不明
UNKNOWN_STRING="不明"
# 未定義
UNDEFINED_STRING="未定義"
# 正常なイベントなど
OK_STRING="正常"
# ダイス情報の種類( nDt + a 形式)
DICE_DATA_ELEMENT_NR=3

# ブロックあたりのメッセージ数
MSG_PER_BLK=12

# AppleIIの色
PIC_COLOR_BLACK=0
PIC_COLOR_PURPLE=1
PIC_COLOR_GREEN=2
PIC_COLOR_BLUE=3
PIC_COLOR_ORANGE=4
PIC_COLOR_WHITE=5
PIC_COLOR_VALID=(PIC_COLOR_BLACK, PIC_COLOR_PURPLE, PIC_COLOR_GREEN, PIC_COLOR_BLUE, PIC_COLOR_ORANGE, PIC_COLOR_WHITE)
# ビデオRAM上に書き込む色(白は, 紫と緑(色選択ビット0のとき), 青と橙(色選択ビットが1のとき)の組み合わせで表示)
COLORED_PIXEL=(PIC_COLOR_BLUE, PIC_COLOR_GREEN, PIC_COLOR_ORANGE, PIC_COLOR_PURPLE)
# 色名
PIC_COLOR_NAME:dict[int,str]={
    PIC_COLOR_BLACK:"黒",
    PIC_COLOR_PURPLE:"紫",
    PIC_COLOR_GREEN:"緑",
    PIC_COLOR_BLUE:"青",
    PIC_COLOR_ORANGE:"燈",
    PIC_COLOR_WHITE:"白",
}

# モンスター/宝箱画像のサイズ
# 幅 70 ピクセル x 高さ 50 ピクセル
PIC_WIDTH=70
PIC_HEIGHT=50

# モンスター/宝箱画像データ1バイト当たりのピクセル数( 0-6ピクセル )
# 一つ当たり7ピクセル
PIXEL_PER_BYTE=7

# AppleII 1ピクセルを表現するピクセル数
PIC_LEN_PER_PIXEL=2
# AppleII版 WizardryのENEMYPIC手続きでの描画開始X座標
PIC_START_X=7
# 宝箱
PIC_NUM_CHEST=18
# 金額報酬
PIC_NUM_GOLD=19
PIC_NUM_CHEST_DIC:dict[int,str]={
    PIC_NUM_CHEST:"宝箱",
    PIC_NUM_GOLD:"報酬",
}
# ビットマップ生成ストラテジ番号
BITMAP_STRATEGY_SIMPLE=0
BITMAP_STRATEGY_STANDARD=1
BITMAP_STRATEGY_DEFAULT=BITMAP_STRATEGY_STANDARD
# ビットマップ生成ストラテジ辞書
# ストラテジ番号からオプション名,意味への辞書
BITMAP_STRATEGY_DIC:dict[int,tuple[str,str]]={
    BITMAP_STRATEGY_SIMPLE:('simple','表示指示に基づくビットマップ生成'),
    BITMAP_STRATEGY_STANDARD:('standard','標準的な補色処理に基づくビットマップ生成'),
}
# 方角
DIR_NORTH=0
DIR_EAST=1
DIR_SOUTH=2
DIR_WEST=3
DIR_VALID=(DIR_NORTH,DIR_EAST,DIR_SOUTH,DIR_WEST)

DELIMITER_COMMA=","
DELIMITER_SPC=" "

# バックスラッシュ以外のマークダウンエスケープ対象文字
MARKDOWN_ESCAPE_CHARS=['#','+',"-","*","_","`",".","!","{","}","[","]"]

# TWIZLONGの構成要素名
TWIZLONG_PARAMS=('LOW','MID','HIGH')

#
# シナリオ情報の目次
#
ZZERO="目次情報"
ZMAZE="迷宮フロア情報"
ZENEMY="モンスター情報"
ZREWARD="報酬情報"
ZOBJECT="アイテム情報"
ZCHAR="キャラクター名簿"
ZSPCCHRS="モンスター/宝箱画像"
ZEXP="経験値表"

#
# 目次のインデクス番号から文字列キーへの変換テーブル
#
TOC_INDEX_TO_KEY:dict[int,str]={
    0:ZZERO,
    1:ZMAZE,
    2:ZENEMY,
    3:ZREWARD,
    4:ZOBJECT,
    5:ZCHAR,
    6:ZSPCCHRS,
    7:ZEXP
}

#
#迷宮フロア
#

#
# 1フロアの大きさ
#
FLOOR_WIDTH=20
FLOOR_HEIGHT=20

#
# 壁の種類
#
FLOOR_WALL_OPEN=0    # 壁はない
FLOOR_WALL_WALL=1    # 壁がある
FLOOR_WALL_DOOR=2    # ドアがある
FLOOR_WALL_HIDDEN=3  # シークレットドアがある

FLOOR_WALL_DIC:dict[int,str]={
    FLOOR_WALL_OPEN:"無",
    FLOOR_WALL_WALL:"壁",
    FLOOR_WALL_DOOR:"扉",
    FLOOR_WALL_HIDDEN:"秘",
}

# フロア当たりの設定可能イベント数
FLOOR_EVENTS_PER_FLOOR=16
# イベントパラメタ数
FLOOR_NR_EVENT_PARAMS=3
# フロア当たりのモンスター出現テーブル系統数
FLOOR_NR_MONSTER_TABLE_SERIES=3
#
# イベント種別
#
FLOOR_EVENT_NORMAL=0
FLOOR_EVENT_STAIRS=1
FLOOR_EVENT_PIT=2
FLOOR_EVENT_CHUTE=3
FLOOR_EVENT_SPINNER=4
FLOOR_EVENT_DARK=5
FLOOR_EVENT_TRANSFER=6
FLOOR_EVENT_OUCHY=7
FLOOR_EVENT_BUTTONZ=8
FLOOR_EVENT_ROCKWATE=9
FLOOR_EVENT_FIZZLE=10
FLOOR_EVENT_SCRNMSG=11
FLOOR_EVENT_ENCOUNTE=12
FLOOR_EVENT_TO_STRING:dict[int,str]={
    FLOOR_EVENT_NORMAL:"床",
    FLOOR_EVENT_STAIRS:"階段",
    FLOOR_EVENT_PIT:"落とし穴",
    FLOOR_EVENT_CHUTE:"シュート",
    FLOOR_EVENT_SPINNER:"回転床",
    FLOOR_EVENT_DARK:"暗闇",
    FLOOR_EVENT_TRANSFER:"テレポート",
    FLOOR_EVENT_OUCHY:"落とし穴2",
    FLOOR_EVENT_BUTTONZ:"エレベータのボタン",
    FLOOR_EVENT_ROCKWATE:"石",
    FLOOR_EVENT_FIZZLE:"呪文無効化",
    FLOOR_EVENT_SCRNMSG:"メッセージ",
    FLOOR_EVENT_ENCOUNTE:"固定モンスター",
}
# 説明不要なイベント
FLOOR_EVENT_NO_NEED_DESC_EVENTS=(
    FLOOR_EVENT_NORMAL,
    FLOOR_EVENT_PIT,
    FLOOR_EVENT_SPINNER,
    FLOOR_EVENT_DARK,
    FLOOR_EVENT_OUCHY,
)

# 無効イベント
FLOOR_EVENT_DISABLED_AUX2_VALUES=(0,)

# イベントが発動しない理由
FLOOR_EVENT_REASON_NOT_ALLOCATED=0 # 未配置
FLOOR_EVENT_REASON_NOT_IN_ROOM=1   # 玄室外
FLOOR_EVENT_REASON_INVALID_TYPE=2  # イベント種別不明
FLOOR_EVENT_REASON_EMERGENCE_LIMIT=3 # 出現回数制限
FLOOR_EVENT_REASON_AUX2_DISABLED_EVENT=4  # イベント無効(AUX2による)
FLOOR_EVENT_REASON_DISABLED_SCRNMSG=5  # 無効メッセージ
FLOOR_EVENT_BROKEN_REASON_DIC:dict[int,str]={
    FLOOR_EVENT_REASON_NOT_ALLOCATED:"未配置",
    FLOOR_EVENT_REASON_NOT_IN_ROOM:"玄室外",
    FLOOR_EVENT_REASON_INVALID_TYPE:"イベント種別不明",
    FLOOR_EVENT_REASON_EMERGENCE_LIMIT:"出現回数制限",
    FLOOR_EVENT_REASON_AUX2_DISABLED_EVENT:"無効イベント",
    FLOOR_EVENT_REASON_DISABLED_SCRNMSG:"無効メッセージ",
}

# メッセージ種別
SCRNMSG_TYPE_UNKNOWN=0
SCRNMSG_TYPE_NORMAL=1
SCRNMSG_TYPE_TRYGET=2
SCRNMSG_TYPE_WHOWADE=3
SCRNMSG_TYPE_GETYN=4
SCRNMSG_TYPE_ITM2PASS=5
SCRNMSG_TYPE_CHKALIGN=6
SCRNMSG_TYPE_CHKAUX0=7
SCRNMSG_TYPE_BCK2SHOP=8
SCRNMSG_TYPE_LOOKOUT=9
SCRNMSG_TYPE_RIDDLES=10
SCRNMSG_TYPE_FEEIS=11
SCRNMSG_CANCELABLE_MSG_TYPE=(SCRNMSG_TYPE_NORMAL,SCRNMSG_TYPE_GETYN,SCRNMSG_TYPE_BCK2SHOP)
SCRNMSG_DISABLED_AUX0_VALUES=(0,)
#
# アイテム/モンスター情報共通
#
# モンスター種別
ENEMY_CLASS_DIC:dict[int,str]={
    0:"戦士系",
    1:"魔術師系",
    2:"僧侶系",
    3:"盗賊系",
    4:"未使用",
    5:"巨人系",
    6:"神話系",
    7:"竜系",
    8:"動物系",
    9:"リカント系",
    10:"不死系",
    11:"悪魔系",
    12:"昆虫系",
    13:"魔法生物系",
}
# キャラクタの職業
CHAR_CLASS_DIC:dict[int,str]={
    0:"戦士",
    1:"魔術師",
    2:"僧侶",
    3:"盗賊",
    4:"司教",
    5:"侍",
    6:"君主",
    7:"忍者",
}
NR_CLASS=len(CHAR_CLASS_DIC)
# キャラクタの属性
CHAR_ALIGNMENT_DIC:dict[int,str]={
    0:"無属性",
    1:"善",
    2:"中立",
    3:"悪"
}
# 無属性
CHAR_ALIGNMENT_NO_ALIGN=0

# 装備可能職業文字列
CHAR_CLASS_EQUIP_STRING="FMPTBSLN"
#
# アイテム種別
#
OBJ_TYPE_WEAPON=0
OBJ_TYPE_ARMOR=1
OBJ_TYPE_SHIELD=2
OBJ_TYPE_HELM=3
OBJ_TYPE_GLOVE=4
OBJ_TYPE_SPECIAL=5
OBJ_TYPE_MISC=6
# アイテム種別からアイテム種別名への変換テーブル
OBJ_TYPE_TO_STR:dict[int,str]={
    OBJ_TYPE_WEAPON:"武器",
    OBJ_TYPE_ARMOR:"鎧",
    OBJ_TYPE_SHIELD:"盾",
    OBJ_TYPE_HELM:"兜",
    OBJ_TYPE_GLOVE:"手甲",
    OBJ_TYPE_SPECIAL:"特殊(装備対象外)",
    OBJ_TYPE_MISC:"その他",
}
# 抵抗属性,ブレス/呪文属性(WEPVSTYP3)のビット位置と意味
RESIST_BREATH_DIC:dict[int,str]={
    0:"無", # 抵抗なし, 無属性ブレス/呪文
    1:"火", # 火属性ブレス/呪文
    2:"冷", # 冷属性ブレス/呪文
    3:"毒", # 毒属性ブレス/呪文
    4:"吸", # ドレイン属性ブレス/呪文
    5:"石", # 石化抵抗
    6:"呪", # 呪文抵抗(呪文詠唱を取りやめさせる)
}
# 攻撃付与属性/能力・弱点(モンスター情報のSPPC)のビット位置と意味
SPPC_DIC:dict[int,str]={
    0:"石", # 石化
    1:"毒", # 毒
    2:"麻", # 麻痺
    3:"首", # クリティカル
    4:"眠", # 休眠可能(弱点)
    5:"逃", # 逃走可能
    6:"呼", # 仲間を呼ぶ
}
# 攻撃付与属性
SPPC_SPECIAL_ATTACK_DIC:dict[int,str]={
    0:"石", # 石化
    1:"毒", # 毒
    2:"麻", # 麻痺
    3:"首", # クリティカル
}

#
# モンスター情報
#

# 攻撃回数最大値
ENEMY_MAX_SWING_COUNT=7

# 弱点
SPPC_WEAK_POINT_DIC:dict[int,str]={
    4:"眠", # 休眠可能(弱点)
}

# 能力
SPPC_CAPABILITY_DIC:dict[int,str]={
    5:"逃", # 逃走可能
    6:"呼", # 仲間を呼ぶ
}

#
# スペシャルパワー効果
#
ITEM_SPECIAL_DIC:dict[int,str]={
    1:"能力値STRENGTHに1加算する",
    2:"能力値I.Q.に1加算する",
    3:"能力値PIETYに1加算する",
    4:"能力値VITALITYに1加算する",
    5:"能力値AGILITYに1加算する",
    6:"能力値LUCKに1加算する",
    7:"能力値STRENGTHから1減算する",
    8:"能力値I.Q.から1減算する",
    9:"能力値PIETYから1減算する",
    10:"能力値VITALITYから1減算する",
    11:"能力値AGILITYから1減算する",
    12:"能力値LUCKから1減算する",
    13:"年齢が20歳を超えていたら年齢を1歳減算する",
    14:"年齢を1歳加算する",
    15:"侍に転職する",
    16:"君主に転職する",
    17:"忍者に転職する",
    18:"GOLDに50,000加算する",
    19:"経験値に50,000加算する",
    20:"状態を喪失(LOST)にする",
    21:"状態を正常に変更,HPを全回復させ, 毒状態を解除する",
    22:"最大HPに1加算する",
    23:"パーティの全メンバーのHPを最大HPまで回復させる",
}

#
# 報酬情報
#
NR_REWARD_PARAM=7 # 報酬情報パラメタ数
# トラップ番号内のビットとトラップ種別の対応表
REWARD_TRAP_DIC:dict[int,list[str]]={
    0:["無し"], # トラップなし
    1:["毒針"], # 毒針
    2:["石弓の矢","爆弾","スプリンター","ブレイズ","スタナー"],
    3:["テレポータ"],
    4:["メイジブラスター"],
    5:["プリーストブラスター"],
    6:["警報"],
}

#
# 文字イメージ
#
CHARIMG_LEN_PER_PIXEL=2
CHARIMG_WIDTH=7 # 幅7ビット
CHARIMG_HEIGHT=8 # 高さ8ビット
CHARIMG_PER_CHARSET=64 # 64種類
CHARIMG_TYPE_NORMAL=0   # 通常の文字セット
CHARIMG_TYPE_CEMETARY=1 # 全滅表示時の文字セット
CHARIMG_CEMETARY_WIDTH=4 # CEMETARY横幅
CHARIMG_CEMETARY_HEIGHT=6 # CEMETARY高さ

# CEMETARY表示文字インデクス
CHARIMG_CEMETARY_CHAR_INDEXES=[
                        11,12,13,14,
                        15,16,17,18,
                        19,20,21,22,
                        23,24,25,26,
                        27,28,29,30,
                        31,56,57,58
                    ]
# デバッグ用(未使用)
DBG_CHARIMG_CEMETARY_CHAR_INDEXES=[
                        11,12,13,14,
                        15,16,17,18,
                        19,20,21,22,
                        23,24,25,26,
                        27,28,29,30,
                        31,32,33,34
                    ]
CHARIMG_TYPE_VALID=(CHARIMG_TYPE_NORMAL, CHARIMG_TYPE_CEMETARY)
CHARIMG_FILENAME_PREFIX_DIC:dict[int,str]={
    CHARIMG_TYPE_NORMAL:"charset-normal",
    CHARIMG_TYPE_CEMETARY:"charset-cemetary",
}

CHARIMG_CH_CODE_START=32 # 空白文字から開始

# 文字セット種別からシナリオ情報先頭からのオフセット位置へのマップ
CHARIMG_TYPE_TO_BLK_OFFSET:dict[int,int]={
    CHARIMG_TYPE_NORMAL:1, # シナリオ情報オフセットブロック 1
    CHARIMG_TYPE_CEMETARY:2, # シナリオ情報オフセットブロック 2
}

# 経験値表の格納エントリ数
EXP_TBL_ELEMENT_NR=13

SPELL_CATEGORY_MAGE="魔術師呪文"
SPELL_CATEGORY_PRIEST="僧侶呪文"
SPELL_CATEGORY_VALID=(SPELL_CATEGORY_MAGE,SPELL_CATEGORY_PRIEST)
SPELL_DELIMITER=13
SPELL_LEVEL_DELIMITER="*"
# 呪文種別名からブロック位置への辞書
SPELL_NAME_BLOCK_DIC:dict[str,int]={
    SPELL_CATEGORY_MAGE:4,
    SPELL_CATEGORY_PRIEST:5,
}
# 呪文用途(デバッグ用)
# (* 呪文種別(対象者選択時に使用): GENERIC(0 一般), PERSON(1 単体), GROUP(2 グループ) *)
# TSPEL012 = (GENERIC, PERSON, GROUP);
DBG_WIZ_SPELL_TYPES:dict[int,str]={
    0:"GENERIC",
    1:"PERSON",
    2:"GROUP"
}

# 呪文名(デバッグ用)
DBG_WIZ_SPELL_NAMES=(
    "NONAME",
    "HALITO",
    "MOGREF",
    "KATINO",
    "DUMAPIC",
    "DILTO",
    "SOPIC",
    "MAHALITO",
    "MOLITO",
    "MORLIS",
    "DALTO",
    "LAHALITO",
    "MAMORLIS",
    "MAKANITO",
    "MADALTO",
    "LAKANITO",
    "ZILWAN",
    "MASOPIC",
    "HAMAN",
    "MALOR",
    "MAHAMAN",
    "TILTOWAIT",
    "KALKI",
    "DIOS",
    "BADIOS",
    "MILWA",
    "PORFIC",
    "MATU",
    "CALFO",
    "MANIFO",
    "MONTINO",
    "LOMILWA",
    "DIALKO",
    "LATUMAPIC",
    "BAMATU",
    "DIAL",
    "BADIAL",
    "LATUMOFIS",
    "MAPORFIC",
    "DIALMA",
    "BADIALMA",
    "LITOKAN",
    "KANDI",
    "DI",
    "BADI",
    "LORTO",
    "MADI",
    "MABADI",
    "LOKTOFEIT",
    "MALIKTO",
    "KADORTO")
