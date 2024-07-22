## 目次情報

### 目次情報のPascal定義

```:pascal
        TSCNTOC = RECORD (* シナリオ情報 *)
            GAMENAME : STRING[ 40]; (* シナリオ名(シナリオ1の場合, 'PROVING GROUNDS OF THE MAD OVERLORD!') *)
            RECPER2B : ARRAY[ ZZERO..ZEXP] OF INTEGER; (* キャッシュ領域(1KiB)に格納可能なデータ数 *)
            RECPERDK : ARRAY[ ZZERO..ZEXP] OF INTEGER; (* 各シナリオ情報の最大データエントリ数 *)
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

### 目次情報データ構造

|メンバ名|オフセット(単位:バイト)|サイズ(単位:バイト)|意味|
|---|---|---|---|
|GAMENAME|0|41|シナリオ名のPascal文字列|
|RECPER2B[0]|42|2|キャッシュ領域に格納可能なZZERO(目次情報)の数(単位:個)|
|RECPER2B[1]|44|2|キャッシュ領域に格納可能なZMAZE(迷宮フロア情報)の数(単位:個)|
|RECPER2B[2]|46|2|キャッシュ領域に格納可能なZENEMY(モンスター情報)の数(単位:個)|
|RECPER2B[3]|48|2|キャッシュ領域に格納可能なZREWARD(報酬情報)の数(単位:個)|
|RECPER2B[4]|50|2|キャッシュ領域に格納可能なZOBJECT(アイテム情報)の数(単位:個)|
|RECPER2B[5]|52|2|キャッシュ領域に格納可能なZCHAR(キャラクタ情報)の数(単位:個)|
|RECPER2B[6]|54|2|キャッシュ領域に格納可能なZSPCCHRS(モンスターグラフィック情報)の数(単位:個)|
|RECPER2B[7]|56|2|キャッシュ領域に格納可能なZEXP(経験値表)|
|RECPERDK[0]|58|2|ZZERO(目次情報)の数|
|RECPERDK[1]|60|2|ZMAZE(フロア情報)の数|
|RECPERDK[2]|62|2|ZENEMY(モンスター情報)の数|
|RECPERDK[3]|64|2|ZREWARD(報酬情報)の数|
|RECPERDK[4]|66|2|ZOBJECT(アイテム情報)の数|
|RECPERDK[5]|68|2|ZCHAR(キャラクタ情報)の数|
|RECPERDK[6]|70|2|ZSPCCHRS(モンスターグラフィック情報)の数|
|RECPERDK[7]|72|2|ZEXP(経験値表)の数|
|UNUSEDXX[0]|74|2|ZZERO(目次情報)未使用情報|
|UNUSEDXX[1]|76|2|ZMAZE(迷宮フロア情報)未使用情報|
|UNUSEDXX[2]|78|2|ZENEMY(モンスター情報)未使用情報|
|UNUSEDXX[3]|80|2|ZREWARD(報酬情報)未使用情報|
|UNUSEDXX[4]|82|2|ZOBJECT(アイテム情報)未使用情報|
|UNUSEDXX[5]|84|2|ZCHAR(キャラクタ情報)未使用情報|
|UNUSEDXX[6]|86|2|ZSPCCHRS(モンスターグラフィック情報)未使用情報|
|UNUSEDXX[7]|88|2|ZEXP(経験値表)未使用情報|
|BLOFF[0]|90|2|ZZERO(目次情報)ブロックオフセット|
|BLOFF[1]|92|2|ZMAZE(迷宮フロア情報)ブロックオフセット|
|BLOFF[2]|94|2|ZENEMY(モンスター情報)ブロックオフセット|
|BLOFF[3]|96|2|ZREWARD(報酬情報)ブロックオフセット|
|BLOFF[4]|98|2|ZOBJECT(アイテム情報)ブロックオフセット|
|BLOFF[5]|100|2|ZCHAR(キャラクタ情報)ブロックオフセット|
|BLOFF[6]|102|2|ZSPCCHRS(モンスターグラフィック情報)ブロックオフセット|
|BLOFF[7]|104|2|ZEXP(経験値表)ブロックオフセット|
|RACE[0]|106|10|NORACE種族名|
|RACE[1]|116|10|HUMAN種族名|
|RACE[2]|126|10|ELF種族名|
|RACE[3]|136|10|DWARF種族名|
|RACE[4]|146|10|GNOME種族名|
|RACE[5]|156|10|HOBBIT種族名|
|CLASS[0]|166|10|FIGHTER職業名|
|CLASS[1]|176|10|MAGE職業名|
|CLASS[2]|186|10|PRIEST職業名|
|CLASS[3]|196|10|THIEF職業名|
|CLASS[4]|206|10|BISHOP職業名|
|CLASS[5]|216|10|SAMURAI職業名|
|CLASS[6]|226|10|LORD職業名|
|CLASS[7]|236|10|NINJA職業名|
|STATUS[0]|246|9|OK状態名|
|STATUS[1]|256|9|AFRAID状態名|
|STATUS[2]|266|9|ASLEEP状態名|
|STATUS[3]|276|9|P-LYZE状態名|
|STATUS[4]|286|9|STONED状態名|
|STATUS[5]|296|9|DEAD状態名|
|STATUS[6]|306|9|ASHES状態名|
|STATUS[7]|316|9|LOST状態名|
|ALIGN[0]|326|10|NOALIGN属性(アラインメント)名|
|ALIGN[1]|336|10|GOOD属性(アラインメント)名|
|ALIGN[2]|346|10|NEUTRAL属性(アラインメント)名|
|ALIGN[3]|356|10|EVIL属性(アラインメント)名|
|SPELLHSH[0]|366|2|無効呪文識別番号(-1)|
|SPELLHSH[1]|368|2|HALITO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[2]|370|2|MOGREF呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[3]|372|2|KATINO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[4]|374|2|DUMAPIC呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[5]|376|2|DILTO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[6]|378|2|SOPIC呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[7]|380|2|MAHALITO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[8]|382|2|MOLITO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[9]|384|2|MORLIS呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[10]|386|2|DALTO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[11]|388|2|LAHALITO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[12]|390|2|MAMORLIS呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[13]|392|2|MAKANITO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[14]|394|2|MADALTO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[15]|396|2|LAKANITO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[16]|398|2|ZILWAN呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[17]|400|2|MASOPIC呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[18]|402|2|HAMAN呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[19]|404|2|MALOR呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[20]|406|2|MAHAMAN呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[21]|408|2|TILTOWAIT呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[22]|410|2|KALKI呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[23]|412|2|DIOS呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[24]|414|2|BADIOS呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[25]|416|2|MILWA呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[26]|418|2|PORFIC呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[27]|420|2|MATU呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[28]|422|2|CALFO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[29]|424|2|MANIFO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[30]|426|2|MONTINO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[31]|428|2|LOMILWA呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[32]|430|2|DIALKO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[33]|432|2|LATUMAPIC呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[34]|434|2|BAMATU呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[35]|436|2|DIAL呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[36]|438|2|BADIAL呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[37]|440|2|LATUMOFIS呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[38]|442|2|MAPORFIC呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[39]|444|2|DIALMA呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[40]|446|2|BADIALMA呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[41]|448|2|LITOKAN呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[42]|450|2|KANDI呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[43]|452|2|DI呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[44]|454|2|BADI呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[45]|456|2|LORTO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[46]|458|2|MADI呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[47]|460|2|MABADI呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[48]|462|2|LOKTOFEIT呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[49]|464|2|MALIKTO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLHSH[50]|466|2|KADORTO呪文識別番号(SPELLHSHのハッシュ値)|
|SPELLGRP[0-4]|468|2|2進数3桁であらわした無効呪文, HALITO,MOGREF,KATINO,DUMAPICの呪文レベル|
|SPELLGRP[5-9]|470|2|2進数3桁であらわしたDILTO,SOPIC, MAHALITO,MOLITO,MORLISの呪文レベル|
|SPELLGRP[10-14]|472|2|2進数3桁であらわしたDALTO,LAHALITO, MAMORLIS, MAKANITO, MADALTOの呪文レベル|
|SPELLGRP[15-19]|474|2|2進数3桁であらわしたLAKANITO,ZILWAN,MASOPIC,HAMAN, MALORの呪文レベル|
|SPELLGRP[20-24]|476|2|2進数3桁であらわしたMAHAMAN,TILTOWAIT,KALKI,DIOS,BADIOSの呪文レベル|
|SPELLGRP[25-29]|478|2|2進数3桁であらわしたMILWA,PORFIC,MATU,CALFO,MANIFOの呪文レベル|
|SPELLGRP[30-34]|480|2|2進数3桁であらわしたMONTINO,LOMILWA,DIALKO,LATUMAPIC,BAMATUの呪文レベル|
|SPELLGRP[35-39]|482|2|2進数で3桁であらわしたDIAL,BADIAL,LATUMOFIS,MAPORFIC,DIALMAの呪文レベル|
|SPELLGRP[40-44]|484|2|2進数で3桁であらわしたBADIALMA,LITOKAN,KANDI,DI,BADIの呪文レベル|
|SPELLGRP[45-49]|486|2|2進数で3桁であらわしたLORTO,MADI,MABADI,LOKTOFEIT,MALIKTOの呪文レベル|
|SPELLGRP[50]|488|2|2進数で3桁であらわしたKADORTOの呪文レベル|
|SPELL012[0-7] |490|2|2進数で2桁であらわした無効呪文,HALITO,MOGREF,KATINO,DUMAPIC,DILTO,SOPIC,MAHALITOの呪文種別|
|SPELL012[8-15] |492|2|2進数で2桁であらわしたMOLITO,MORLIS,DALTO,LAHALITO, MAMORLIS, MAKANITO, MADALTO, LAKANITOの呪文種別|
|SPELL012[16-23] |494|2|2進数で2桁であらわしたZILWAN, MASOPIC,HAMAN,MALOR,MAHAMAN,TILTOWAIT,KALKI,DIOSの呪文種別|
|SPELL012[24-31] |496|2|2進数で2桁であらわしたBADIOS,MILWA,PORFIC,MATU,CALFO,MANIFO,MONTINO,LOMILWAの呪文種別|
|SPELL012[32-39] |498|2|2進数で2桁であらわしたDIALKO,LATUMAPIC,BAMATU,DIAL,BADIAL,LATUMOFIS,MAPORFIC,DIALMAの呪文種別|
|SPELL012[40-47] |500|2|2進数で2桁であらわしたBADIALMA,LITOKAN,KANDI,DI,BADI,LORTO,MADI,MABADIの呪文種別|
|SPELL012[48-50] |502|2|2進数で2桁であらわしたLOKTOFEIT,MALIKTO,KADORTOの呪文種別|

### 目次情報の内容

目次情報には, 以下の情報が含まれる。

1. GAMENAME シナリオ名のPascal文字列
2. RECPER2B キャッシュ領域中に格納可能なシナリオ情報各要素数の配列
3. RECPERDK シナリオ情報各要素数の配列
4. BLOFF    シナリオ情報各要素開始ブロックの配列
5. RACE     種族名の配列
6. CLASS    職業名の配列
7. STATUS   キャラクターの状態名の配列
8. ALIGN    キャラクターの属性(アラインメント)名の配列
9. SPELLHSH
10. SPELLGRP 各呪文の識別番号(ハッシュ番号)
11. SPELL012 各呪文の種別(汎用, 単体呪文, グループ呪文)

#### GAMENAMEに格納されている情報

GAMENAMEには, シナリオ名称がPascal文字列形式で格納されている。迷宮に入った際に表示されるメッセージに使用される。

シナリオ1の場合, \"PROVING GROUNDS OF THE MAD OVERLORD!\"が格納されている。

#### RECPER2Bに格納されている情報

指定された情報種別のデータをキャッシュ領域(1KiB)に格納可能な数が, RECPER2Bに格納されている。
RECPER2Bには, [キャッシュ領域](#appleii版-wizardryでのキャッシュ領域の扱い)中に格納可能な要素数が格納されている。配列のインデクスは, [シナリオ情報種別](#シナリオ情報種別tzscn型)である。

例えば, シナリオ1でのアイテム情報の場合, アイテム情報のサイズは78バイトであるため, キャッシュ領域には, 13個(計1014バイト)格納可能である。
このため, RECPER2Bのアイテム情報に対応する要素(RECPER2B\[5\])には, 13が格納されている。

#### RECPERDKに格納されている情報

指定された情報種別のデータに関する総格納数が, RECPERDKに格納されている。
配列のインデクスは, [シナリオ情報種別](#シナリオ情報種別tzscn型)である。

例えば, シナリオ1でのアイテム情報の場合, 総アイテム数は101個であるため, RECPER2DKのアイテム情報に対応する要素(RECPERDK\[5\])には, 101が格納されている。

#### BLOFFに格納されている情報

指定された情報種別のデータの格納先ディスクブロックに関する情報が, BLOFFに格納されている。
BLOFFには, シナリオ情報の先頭からのオフセット位置が格納されている(単位:ブロック)。

例えば, シナリオ1でのアイテム情報の場合, シナリオ情報の先頭からのオフセット位置34816バイト目にアイテム情報が格納されている。ブロック単位でのオフセット位置は, ブロックサイズが512バイトであることから, `34816 // 512 = 68`から, 68ブロック目となる。このため, BLOFFのアイテム情報に対応する要素(RECPERDK\[5\])には, 68が格納されている。

#### RACEに格納されている情報

RACEには, シナリオ中に登場するプレイヤーキャラクタの種族名を表すPascal文字列が格納されている。
配列のインデクスは, 種族の列挙型(TRACE)の値である。

種族の列挙型(TRACE)は以下のように定義されている。

```:pascal
TRACE = (NORACE, HUMAN, ELF, DWARF, GNOME, HOBBIT); (* 種族の列挙型: NORACE(0 種族なし), HUMAN(1 人間), ELF(2 エルフ), DWARF(3 ドワーフ), GNOME(4 ノーム), HOBBIT(5 ホビット) *)
```

種族の列挙型(TRACE)の列挙子と列挙値の関係は以下の通り:

|列挙子|列挙値|意味|
|---|---|---|
|NORACE|0|種族なし|
|HUMAN|1|人間|
|ELF|2|エルフ|
|DWARF|3|ドワーフ|
|GNOME|4|ノーム|
|HOBBIT|5|ホビット|

例えば, シナリオ1のHUMAN(列挙値1)の場合, RACE\[1\]には, \"HUMAN\"が格納されている。

#### CLASSに格納されている情報

CLASSには, シナリオ中に登場するプレイヤーキャラクタの職業名を表すPascal文字列が格納されている。
配列のインデクスは, 職業の列挙型(TCLASS)の値である。

職業の列挙型(TCLASS)は以下のように定義されている。

```:pascal
        TCLASS = (FIGHTER, MAGE, PRIEST, THIEF,
                  BISHOP, SAMURAI, LORD, NINJA);  (* 種族の列挙型:FIGHTER(0 戦士), MAGE(1 魔術師), PRIEST(2 僧侶), THIEF(3 盗賊), BISHOP(4 司教), SAMURAI(5 侍), LORD(6 君主), NINJA(7 忍者)  *)
```

職業の列挙型(TCLASS)の列挙子と列挙値の関係は以下の通り:

|列挙子|列挙値|意味|
|---|---|---|
|FIGHTER|0|戦士|
|MAGE|1|魔術師|
|PRIEST|2|僧侶|
|THIEF|3|盗賊|
|BISHOP|4|司教|
|SAMURAI|5|侍|
|LORD|6|君主|
|NINJA|7|忍者|

例えば, シナリオ1のSAMURAI(列挙値5)の場合, RACE\[5\]には, \"SAMURAI\"が格納されている。
