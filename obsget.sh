#!/bin/bash

/usr/bin/wget http://www.jma.go.jp/jma/kishou/know/amedas/ame_master.zip -q -O -\
 |/usr/bin/funzip \
 |nkf >obs.txt