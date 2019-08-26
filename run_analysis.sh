#!/bin/bash

rm -rf code/analysis
cp -r ~/lab/stoch-mod/analysis-dev/ code/analysis/

python -m code.analysis.kx_trace
