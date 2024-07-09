# シナリオデータ解析

## データ構造
<!-- ZZERO, ZMAZE, ZENEMY, ZREWARD, ZOBJECT, -->
|メンバ名|オフセット(単位:バイト)|サイズ(単位:バイト)|実際の値|備考|
|---|---|---|---|---|
|GAMENAME|0|41|0x24,"PROVING GROUNDS OF THE MAD OVERLORD!"|36(0x24)文字|
|RECPER2B[0]|42|2|0x6|ZZERO(シナリオ情報自身の情報)|
|RECPER2B[1]|44|2|0x1|ZMAZE(迷宮情報)|
|RECPER2B[2]|46|2|0x6|ZENEMY(モンスター情報)|
|RECPER2B[3]|48|2|0x6|ZREWARD(報酬情報)|
|RECPER2B[4]|50|2|0xd|ZOBJECT(アイテム情報)|
|RECPER2B[5]|52|2|0x4|ZCHAR(キャラクタ情報)|
|RECPER2B[6]|54|2|0x2|ZSPCCHRS(モンスターグラフィック情報)|
|RECPER2B[7]|56|2|0x1|ZEXP(経験値表)|
|RECPERDK[0]|58|2|0x1|ZZERO(シナリオ情報自身の情報)の数|
|RECPERDK[1]|60|2|0xa|ZMAZE(フロア情報)の数|
|RECPERDK[2]|62|2|0x65|ZENEMY(モンスター情報)の数|
|RECPERDK[3]|64|2|0x18|ZREWARD(報酬情報)の数|
|RECPERDK[4]|66|2|0x65|ZOBJECT(アイテム情報)の数|
|RECPERDK[5]|68|2|0x14|ZCHAR(キャラクタ情報)の数|
|RECPERDK[6]|70|2|0x14|ZSPCCHRS(モンスターグラフィック情報)の数|
|RECPERDK[7]|72|2|0x1|ZEXP(経験値表)の数|
|UNUSEDXX[0]|74|2|0x14|ZZERO(シナリオ情報自身の情報)未使用情報|
|UNUSEDXX[1]|76|2|0x22|ZMAZE(迷宮情報)未使用情報|
|UNUSEDXX[2]|78|2|0x08|ZENEMY(モンスター情報)未使用情報|
|UNUSEDXX[3]|80|2|0x10|ZREWARD(報酬情報)未使用情報|
|UNUSEDXX[4]|82|2|0xa|ZOBJECT(アイテム情報)未使用情報|
|UNUSEDXX[5]|84|2|0x14|ZCHAR(キャラクタ情報)未使用情報|
|UNUSEDXX[6]|86|2|0x2|ZSPCCHRS(モンスターグラフィック情報)未使用情報|
|UNUSEDXX[7]|88|2|0x0|ZEXP(経験値表)|
|BLOFF[0]|90|2|0x0|ZZERO(シナリオ情報自身の情報)ブロックオフセット|
|BLOFF[1]|92|2|0x6|ZMAZE(迷宮情報)ブロックオフセット|
|BLOFF[2]|94|2|0x1a|ZENEMY(モンスター情報)ブロックオフセット|
|BLOFF[3]|96|2|0x3c|ZREWARD(報酬情報)ブロックオフセット|
|BLOFF[4]|98|2|0x44|ZOBJECT(アイテム情報)ブロックオフセット|
|BLOFF[5]|100|2|0x54|ZCHAR(キャラクタ情報)ブロックオフセット|
|BLOFF[6]|102|2|0x5e|ZSPCCHRS(モンスターグラフィック情報)ブロックオフセット|
|BLOFF[7]|104|2|0x72|ZEXP(経験値表)ブロックオフセット|
|RACE[0]|106|10|0x7,"NO RACE"|NORACE種族名|
|RACE[1]|116|10|0x5,"HUMAN"|HUMAN種族名|
|RACE[2]|126|10|0x3,"ELF"|ELF種族名|
|RACE[3]|136|10|0x5,"DWARF"|DWARF種族名|
|RACE[4]|146|10|0x5,"GNOME"|GNOME種族名|
|RACE[5]|156|10|0x6,"HOBBIT"|HOBBIT種族名|
|CLASS[0]|166|10|0x7,"FIGHTER"|FIGHTER職業名|
|CLASS[1]|176|10|0x4,"MAGE"|MAGE職業名|
|CLASS[2]|186|10|0x6,"PRIEST"|PRIEST職業名|
|CLASS[3]|196|10|0x5,"THIEF"|THIEF職業名|
|CLASS[4]|206|10|0x6,"BISHOP"|BISHOP職業名|
|CLASS[5]|216|10|0x7,"SAMURAI"|SAMURAI職業名|
|CLASS[6]|226|10|0x4,"LORD"|LORD職業名|
|CLASS[7]|236|10|0x5,"NINJA"|NINJA職業名|
|STATUS[0]|246|9|0x2,"OK"|OK状態名|
|STATUS[1]|256|9|0x6,"AFRAID"|AFRAID状態名|
|STATUS[2]|266|9|0x6,"ASLEEP"|ASLEEP状態名|
|STATUS[3]|276|9|0x6,"P-LYZE"|P-LYZE状態名|
|STATUS[4]|286|9|0x6,"STONED"|STONED状態名|
|STATUS[5]|296|9|0x4,"DEAD"|DEAD状態名|
|STATUS[6]|306|9|0x5,"ASHES"|ASHES状態名|
|STATUS[7]|316|9|0x4,"LOST"|LOST状態名|
|ALIGN[0]|326|10|0x7,"NOALIGN"|NOALIGN属性(アラインメント)名|
|ALIGN[1]|336|10|0x4,"GOOD"|GOOD属性(アラインメント)名|
|ALIGN[2]|346|10|0x7,"NEUTRAL"|NEUTRAL属性(アラインメント)名|
|ALIGN[3]|356|10|0x4,"EVIL"|EVIL属性(アラインメント)名|
|SPELLHSH[0]|366|2|0xffff|無効呪文識別番号(-1)|
|SPELLHSH[1]|368|2|0x1052|HALITO呪文識別番号|
|略|
|SPELLHSH[50]|466|2|0x1a11|KADORTO呪文識別番号|
|SPELLGRP[0-4]|468|2|0x9248|2進数で000,001,001,001,001 HALITO,MOGREF,KATINO,DUMAPIC=レベル1|
|SPELLGRP[5-9]|470|2|0xc6d2|2進数で010,010,011,011,100 DILTO,SOPIC=レベル2, MAHALITO,MORLITO=レベル3,MORLIS=レベル4|
|SPELLGRP[10-14]|472|2|0xdb64|2進数で100,100,101,101,101 DALTO,LAHALITO=レベル4, MAMORLIS, MAKANITO, MADALTO=レベル5|
|SPELLGRP[15-19]|474|2|0xfdb6|2進数で110,110,110,110,111 LAKANITO,ZILWAN,MASOPIC,HAMAN=レベル6, MALOR=レベル7|
|SPELLGRP[20-24]|476|2|0x927f|2進数で111,111,001,001,001 MAHAMAN,TILTOWAIT=レベル7,KALKI,DIOS,BADIOS=レベル1|
|SPELLGRP[25-29]|478|2|0xa489|2進数で001,001,010,010,010 MILWA,PORFIC=レベル1,MATU,CALFO,MANIFO=レベル2|
|SPELLGRP[30-34]|480|2|0xb6da|2進数で010,011,011,011,011 MONTINO=レベル2,LOMILWA,DIALKO,LATUMAPIC,BAMATU=レベル3|
|SPELLGRP[35-39]|482|2|0x5924|2進数で100,100,100,100,101 DIAL,BADIAL,LATUMOFIS,MAPORFIC=レベル4,DIALMA=レベル5|
|SPELLGRP[40-44]|484|2|0x5b6d|2進数で101,101,101,101,101 BADIALMA,LITOKAN,KANDI,DI,BADO=レベル5|
|SPELLGRP[45-49]|486|2|0x7db6|2進数で110,110,110,110,111 LORTO,MADI,MABADI,LOKTOFEIT=レベル6,MALIKTO=レベル7|
|SPELLGRP[50]|488|2|0x93df|2進数で111 KADORTO=レベル7|
|SPELL012[0] |490|2|0x8888|2進数で, 00,10,00,10,00,10,00,10, HALITO(グループ),MOGREF(一般),KATINO(グループ),DUMAPIC(一般),DILTO(グループ),SOPIC(一般),DALTO(グループ)|


```:pascal
        TSCNTOC = RECORD (* シナリオ情報 *)
            GAMENAME : STRING[ 40]; (* シナリオ名(シナリオ1の場合, 'PROVING GROUNDS OF THE MAD OVERLORD!') *)
            RECPER2B : ARRAY[ ZZERO..ZEXP] OF INTEGER; (* キャッシュ領域(1KiB)に格納可能なデータ数 *)
            RECPERDK : ARRAY[ ZZERO..ZEXP] OF INTEGER; (* 各シナリオ情報の最大データ数(例: ZCHARの場合, 最大登録キャラクタ数, ZMAZEの場合, 最大階層(PGMOの場合,10?) *)
            UNUSEDXX : ARRAY[ ZZERO..ZEXP] OF INTEGER; (* 未使用 *)
            BLOFF    : ARRAY[ ZZERO..ZEXP] OF INTEGER; (* 各シナリオ情報の格納先ディスクブロック番号 *)
            RACE     : ARRAY[ NORACE..HOBBIT]         OF STRING[ 9]; (* 種族を表す文字列(9文字) *)
            CLASS    : PACKED ARRAY[ FIGHTER..NINJA]  OF STRING[ 9]; (* 職業を表す文字列(9文字) *)
            STATUS   : ARRAY[ OK..LOST]               OF STRING[ 8]; (* 状態を表す文字列(8文字) *)
            ALIGN    : PACKED ARRAY[ UNALIGN..EVIL]   OF STRING[ 9]; (* 属性(アラインメント)を表す文字列(9文字) *)
            SPELLHSH : PACKED ARRAY[ 0..50] OF INTEGER;              (* 各呪文の連番から識別番号への変換テーブル *)
            SPELLGRP : PACKED ARRAY[ 0..50] OF 0..7;                 (* 各呪文の連番から呪文レベルへの変換テーブル *)
            SPELL012 : PACKED ARRAY[ 0..50] OF TSPEL012;             (* 各呪文の連番から呪文種別(対象者選択時に使用)への変換テーブル *)
          END;
```