#!/bin/sh

#AppleGraphic.md  SCENARIO-FILE.md  TOC.md  charSet.md  diskLayout.md  figures

rm -f data-structure-draft.md

cat headPage.md diskLayout.md TOC.md charSet.md AppleGraphic.md \
    references.md \
    > data-structure-draft.md
