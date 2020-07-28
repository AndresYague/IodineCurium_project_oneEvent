All the tools needed to generate the delta files are found in this directory.

The tEvents*.in files needed to generate the delta files are created by
running the python3 get_tEvents_*.py scripts. After running the script, the
appropriate tEvents*.in file is generated, which can then be converted to a
deltas*.in file by running tEvents_to_deltas.py python3 script.

A mixed delta file can be obtained by running the tEvents_to_deltas.py python3
script with two tEvents*.in files, a tEvents_pow*.in and a tEvents_box*.in.

Our recommended deltas*.in files are:

deltas_box_3e6_5e7_gamma_1.00e8_tend_1e11_1e3runs.in
deltas_box_3e6_5e7_gamma_2.00e8_tend_1e11_1e3runs.in
deltas_box_3e6_5e7_gamma_3.00e8_tend_1e11_1e3runs.in
deltas_box_3e6_5e7_gamma_4.00e8_tend_1e11_1e3runs.in
deltas_box_3e6_5e7_gamma_5.00e8_tend_1e11_1e3runs.in

deltas_pow_5e7_1e10_gamma_1.00e8_tend_1e11_1e3runs.in
deltas_pow_5e7_1e10_gamma_2.00e8_tend_1e11_1e3runs.in
deltas_pow_5e7_1e10_gamma_3.00e8_tend_1e11_1e3runs.in
deltas_pow_5e7_1e10_gamma_4.00e8_tend_1e11_1e3runs.in
deltas_pow_5e7_1e10_gamma_5.00e8_tend_1e11_1e3runs.in

deltas_mixed_gamma_2.00e8_tend_1e11_1e3runs.in
deltas_mixed_gamma_4.00e8_tend_1e11_1e3runs.in
deltas_mixed_gamma_6.00e8_tend_1e11_1e3runs.in
deltas_mixed_gamma_8.00e8_tend_1e11_1e3runs.in
deltas_mixed_gamma_1.00e9_tend_1e11_1e3runs.in
