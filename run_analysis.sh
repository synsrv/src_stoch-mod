#!/bin/bash

rm -rf src/analysis
cp -r ~/lab/stoch-mod/analysis-dev/ src/analysis/

#python -m src.post_process.equal_dt
#python -m src.post_process.fixed_start_dt

python -m src.analysis.figures.synsrv_trace
python -m src.analysis.figures.k_effect_equal
python -m src.analysis.figures.npool_effect_equal

python -m src.analysis.figures.xt_trace
python -m src.analysis.figures.single_traces
python -m src.analysis.figures.pdf_estimate_log
