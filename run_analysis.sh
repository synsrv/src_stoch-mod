#!/bin/bash

rm -rf code/analysis
cp -r ~/lab/stoch-mod/analysis-dev/ code/analysis/

#python -m code.post_process.equal_dt
#python -m code.post_process.fixed_start_dt

python -m code.analysis.figures.xt_trace
python -m code.analysis.figures.pdf_estimate_log

python -m code.analysis.figures.synsrv_trace
python -m code.analysis.figures.k_effect_equal
python -m code.analysis.figures.npool_effect_equal
