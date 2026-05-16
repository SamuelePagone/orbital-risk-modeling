# Data Inspection Report

## Dataset Used
- Relative path: `dataset/data/kelvins_competition_data/train_data.csv`
- Absolute path: `/Users/samuelepagone/Desktop/Laurea AI/PROGETTI/orbital-risk-modeling/dataset/data/kelvins_competition_data/train_data.csv`

## Repository Structure Snapshot
- `.DS_Store`
- `.gitignore`
- `README.md`
- `dataset/`
- `main.py`
- `notebooks/`
- `outputs/`
- `project_docs/`
- `reports/`
- `requirements.txt`
- `src/`

## Dataset Files Found
- `dataset/.DS_Store`
- `dataset/data/kelvins_competition_data/.DS_Store`
- `dataset/data/kelvins_competition_data/test_data.csv`
- `dataset/data/kelvins_competition_data/test_data_private.csv`
- `dataset/data/kelvins_competition_data/train_data.csv`
- `dataset/data/kelvins_competition_data/train_data.zip`
- `dataset/data/raw_data/raw_data_2015-2019.gz`
- `dataset/data/raw_data/raw_data_2015-2019.txt`

## Shape
- Rows: `162634`
- Columns: `103`

## Column Names
- `event_id`
- `time_to_tca`
- `mission_id`
- `risk`
- `max_risk_estimate`
- `max_risk_scaling`
- `miss_distance`
- `relative_speed`
- `relative_position_r`
- `relative_position_t`
- `relative_position_n`
- `relative_velocity_r`
- `relative_velocity_t`
- `relative_velocity_n`
- `t_time_lastob_start`
- `t_time_lastob_end`
- `t_recommended_od_span`
- `t_actual_od_span`
- `t_obs_available`
- `t_obs_used`
- `t_residuals_accepted`
- `t_weighted_rms`
- `t_rcs_estimate`
- `t_cd_area_over_mass`
- `t_cr_area_over_mass`
- `t_sedr`
- `t_j2k_sma`
- `t_j2k_ecc`
- `t_j2k_inc`
- `t_ct_r`
- `t_cn_r`
- `t_cn_t`
- `t_crdot_r`
- `t_crdot_t`
- `t_crdot_n`
- `t_ctdot_r`
- `t_ctdot_t`
- `t_ctdot_n`
- `t_ctdot_rdot`
- `t_cndot_r`
- `t_cndot_t`
- `t_cndot_n`
- `t_cndot_rdot`
- `t_cndot_tdot`
- `c_object_type`
- `c_time_lastob_start`
- `c_time_lastob_end`
- `c_recommended_od_span`
- `c_actual_od_span`
- `c_obs_available`
- `c_obs_used`
- `c_residuals_accepted`
- `c_weighted_rms`
- `c_rcs_estimate`
- `c_cd_area_over_mass`
- `c_cr_area_over_mass`
- `c_sedr`
- `c_j2k_sma`
- `c_j2k_ecc`
- `c_j2k_inc`
- `c_ct_r`
- `c_cn_r`
- `c_cn_t`
- `c_crdot_r`
- `c_crdot_t`
- `c_crdot_n`
- `c_ctdot_r`
- `c_ctdot_t`
- `c_ctdot_n`
- `c_ctdot_rdot`
- `c_cndot_r`
- `c_cndot_t`
- `c_cndot_n`
- `c_cndot_rdot`
- `c_cndot_tdot`
- `t_span`
- `c_span`
- `t_h_apo`
- `t_h_per`
- `c_h_apo`
- `c_h_per`
- `geocentric_latitude`
- `azimuth`
- `elevation`
- `mahalanobis_distance`
- `t_position_covariance_det`
- `c_position_covariance_det`
- `t_sigma_r`
- `c_sigma_r`
- `t_sigma_t`
- `c_sigma_t`
- `t_sigma_n`
- `c_sigma_n`
- `t_sigma_rdot`
- `c_sigma_rdot`
- `t_sigma_tdot`
- `c_sigma_tdot`
- `t_sigma_ndot`
- `c_sigma_ndot`
- `F10`
- `F3M`
- `SSN`
- `AP`

## Data Types
| Column | Inferred data type |
| --- | --- |
| event_id | int64 |
| time_to_tca | float64 |
| mission_id | int64 |
| risk | float64 |
| max_risk_estimate | float64 |
| max_risk_scaling | float64 |
| miss_distance | float64 |
| relative_speed | float64 |
| relative_position_r | float64 |
| relative_position_t | float64 |
| relative_position_n | float64 |
| relative_velocity_r | float64 |
| relative_velocity_t | float64 |
| relative_velocity_n | float64 |
| t_time_lastob_start | float64 |
| t_time_lastob_end | float64 |
| t_recommended_od_span | float64 |
| t_actual_od_span | float64 |
| t_obs_available | int64 |
| t_obs_used | int64 |
| t_residuals_accepted | float64 |
| t_weighted_rms | float64 |
| t_rcs_estimate | float64 |
| t_cd_area_over_mass | float64 |
| t_cr_area_over_mass | float64 |
| t_sedr | float64 |
| t_j2k_sma | float64 |
| t_j2k_ecc | float64 |
| t_j2k_inc | float64 |
| t_ct_r | float64 |
| t_cn_r | float64 |
| t_cn_t | float64 |
| t_crdot_r | float64 |
| t_crdot_t | float64 |
| t_crdot_n | float64 |
| t_ctdot_r | float64 |
| t_ctdot_t | float64 |
| t_ctdot_n | float64 |
| t_ctdot_rdot | float64 |
| t_cndot_r | float64 |
| t_cndot_t | float64 |
| t_cndot_n | float64 |
| t_cndot_rdot | float64 |
| t_cndot_tdot | float64 |
| c_object_type | object |
| c_time_lastob_start | float64 |
| c_time_lastob_end | float64 |
| c_recommended_od_span | float64 |
| c_actual_od_span | float64 |
| c_obs_available | float64 |
| c_obs_used | float64 |
| c_residuals_accepted | float64 |
| c_weighted_rms | float64 |
| c_rcs_estimate | float64 |
| c_cd_area_over_mass | float64 |
| c_cr_area_over_mass | float64 |
| c_sedr | float64 |
| c_j2k_sma | float64 |
| c_j2k_ecc | float64 |
| c_j2k_inc | float64 |
| c_ct_r | float64 |
| c_cn_r | float64 |
| c_cn_t | float64 |
| c_crdot_r | float64 |
| c_crdot_t | float64 |
| c_crdot_n | float64 |
| c_ctdot_r | float64 |
| c_ctdot_t | float64 |
| c_ctdot_n | float64 |
| c_ctdot_rdot | float64 |
| c_cndot_r | float64 |
| c_cndot_t | float64 |
| c_cndot_n | float64 |
| c_cndot_rdot | float64 |
| c_cndot_tdot | float64 |
| t_span | float64 |
| c_span | float64 |
| t_h_apo | float64 |
| t_h_per | float64 |
| c_h_apo | float64 |
| c_h_per | float64 |
| geocentric_latitude | float64 |
| azimuth | float64 |
| elevation | float64 |
| mahalanobis_distance | float64 |
| t_position_covariance_det | float64 |
| c_position_covariance_det | float64 |
| t_sigma_r | float64 |
| c_sigma_r | float64 |
| t_sigma_t | float64 |
| c_sigma_t | float64 |
| t_sigma_n | float64 |
| c_sigma_n | float64 |
| t_sigma_rdot | float64 |
| c_sigma_rdot | float64 |
| t_sigma_tdot | float64 |
| c_sigma_tdot | float64 |
| t_sigma_ndot | float64 |
| c_sigma_ndot | float64 |
| F10 | float64 |
| F3M | float64 |
| SSN | float64 |
| AP | float64 |

## Missing Values
| Column | Missing values |
| --- | --- |
| event_id | 0 |
| time_to_tca | 0 |
| mission_id | 0 |
| risk | 0 |
| max_risk_estimate | 0 |
| max_risk_scaling | 0 |
| miss_distance | 0 |
| relative_speed | 0 |
| relative_position_r | 0 |
| relative_position_t | 0 |
| relative_position_n | 0 |
| relative_velocity_r | 0 |
| relative_velocity_t | 0 |
| relative_velocity_n | 0 |
| t_time_lastob_start | 0 |
| t_time_lastob_end | 0 |
| t_recommended_od_span | 0 |
| t_actual_od_span | 0 |
| t_obs_available | 0 |
| t_obs_used | 0 |
| t_residuals_accepted | 0 |
| t_weighted_rms | 0 |
| t_rcs_estimate | 3277 |
| t_cd_area_over_mass | 0 |
| t_cr_area_over_mass | 0 |
| t_sedr | 0 |
| t_j2k_sma | 0 |
| t_j2k_ecc | 0 |
| t_j2k_inc | 0 |
| t_ct_r | 0 |
| t_cn_r | 0 |
| t_cn_t | 0 |
| t_crdot_r | 9230 |
| t_crdot_t | 9230 |
| t_crdot_n | 9230 |
| t_ctdot_r | 9230 |
| t_ctdot_t | 9230 |
| t_ctdot_n | 9230 |
| t_ctdot_rdot | 9230 |
| t_cndot_r | 9230 |
| t_cndot_t | 9230 |
| t_cndot_n | 9230 |
| t_cndot_rdot | 9230 |
| t_cndot_tdot | 9230 |
| c_object_type | 0 |
| c_time_lastob_start | 11 |
| c_time_lastob_end | 11 |
| c_recommended_od_span | 11 |
| c_actual_od_span | 11 |
| c_obs_available | 11 |
| c_obs_used | 11 |
| c_residuals_accepted | 11 |
| c_weighted_rms | 11 |
| c_rcs_estimate | 52841 |
| c_cd_area_over_mass | 0 |
| c_cr_area_over_mass | 0 |
| c_sedr | 0 |
| c_j2k_sma | 0 |
| c_j2k_ecc | 0 |
| c_j2k_inc | 0 |
| c_ct_r | 11 |
| c_cn_r | 11 |
| c_cn_t | 11 |
| c_crdot_r | 9241 |
| c_crdot_t | 9241 |
| c_crdot_n | 9241 |
| c_ctdot_r | 9241 |
| c_ctdot_t | 9241 |
| c_ctdot_n | 9241 |
| c_ctdot_rdot | 9241 |
| c_cndot_r | 9241 |
| c_cndot_t | 9241 |
| c_cndot_n | 9241 |
| c_cndot_rdot | 9241 |
| c_cndot_tdot | 9241 |
| t_span | 0 |
| c_span | 0 |
| t_h_apo | 0 |
| t_h_per | 0 |
| c_h_apo | 0 |
| c_h_per | 0 |
| geocentric_latitude | 0 |
| azimuth | 0 |
| elevation | 0 |
| mahalanobis_distance | 0 |
| t_position_covariance_det | 0 |
| c_position_covariance_det | 0 |
| t_sigma_r | 0 |
| c_sigma_r | 11 |
| t_sigma_t | 0 |
| c_sigma_t | 11 |
| t_sigma_n | 0 |
| c_sigma_n | 11 |
| t_sigma_rdot | 9230 |
| c_sigma_rdot | 9241 |
| t_sigma_tdot | 9230 |
| c_sigma_tdot | 9241 |
| t_sigma_ndot | 9230 |
| c_sigma_ndot | 9241 |
| F10 | 6822 |
| F3M | 6822 |
| SSN | 6822 |
| AP | 6822 |

## Duplicated Rows
- Duplicated rows: `0`

## First 5 Rows
| event_id | time_to_tca | mission_id | risk | max_risk_estimate | max_risk_scaling | miss_distance | relative_speed | relative_position_r | relative_position_t | relative_position_n | relative_velocity_r | relative_velocity_t | relative_velocity_n | t_time_lastob_start | t_time_lastob_end | t_recommended_od_span | t_actual_od_span | t_obs_available | t_obs_used | t_residuals_accepted | t_weighted_rms | t_rcs_estimate | t_cd_area_over_mass | t_cr_area_over_mass | t_sedr | t_j2k_sma | t_j2k_ecc | t_j2k_inc | t_ct_r | t_cn_r | t_cn_t | t_crdot_r | t_crdot_t | t_crdot_n | t_ctdot_r | t_ctdot_t | t_ctdot_n | t_ctdot_rdot | t_cndot_r | t_cndot_t | t_cndot_n | t_cndot_rdot | t_cndot_tdot | c_object_type | c_time_lastob_start | c_time_lastob_end | c_recommended_od_span | c_actual_od_span | c_obs_available | c_obs_used | c_residuals_accepted | c_weighted_rms | c_rcs_estimate | c_cd_area_over_mass | c_cr_area_over_mass | c_sedr | c_j2k_sma | c_j2k_ecc | c_j2k_inc | c_ct_r | c_cn_r | c_cn_t | c_crdot_r | c_crdot_t | c_crdot_n | c_ctdot_r | c_ctdot_t | c_ctdot_n | c_ctdot_rdot | c_cndot_r | c_cndot_t | c_cndot_n | c_cndot_rdot | c_cndot_tdot | t_span | c_span | t_h_apo | t_h_per | c_h_apo | c_h_per | geocentric_latitude | azimuth | elevation | mahalanobis_distance | t_position_covariance_det | c_position_covariance_det | t_sigma_r | c_sigma_r | t_sigma_t | c_sigma_t | t_sigma_n | c_sigma_n | t_sigma_rdot | c_sigma_rdot | t_sigma_tdot | c_sigma_tdot | t_sigma_ndot | c_sigma_ndot | F10 | F3M | SSN | AP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1.566798229166667 | 5 | -10.204954629578877 | -7.834755673874688 | 8.602100966916987 | 14923.0 | 13792.0 | 453.8 | 5976.6 | -13666.8 | -7.2 | -12637.0 | -5525.9 | 1.0 | 0.0 | 3.78 | 3.78 | 459 | 458 | 98.9 | 1.265 | 0.402 | 0.013826 | 0.007173000000000001 | 5.12307e-05 | 6996.91886658559 | 0.0039965551645123705 | 97.8064120752813 | -0.397969092862843 | 0.29225770070532564 | 0.04079947600898376 | 0.3942208023827757 | -0.9996740348820246 | -0.03849830357141969 | -0.9810976082182036 | 0.2146117769600234 | -0.3164925446789966 | -0.2102471412826656 | 0.17073694037680856 | -0.00155085845105549 | 0.5315934759177916 | 0.00211707408487376 | -0.17927830141722215 | UNKNOWN | 180.00000000000003 | 2.0 | 15.85 | 15.85 | 15.0 | 15.0 | 100.0 | 2.36 |  | 0.34870100000000004 | 0.126607 | 0.00140562 | 7006.60732021595 | 0.0031437370175118 | 74.045734571957 | -0.8248589064769345 | 0.4739756562852594 | -0.0025757378461846434 | 0.8252158112691431 | -0.9999983930811884 | 0.0035653866444865095 | -0.7329538074970001 | 0.22000618545153167 | -0.8142492108580788 | -0.22062096295999198 | 0.2498551603129017 | 0.19661962372575345 | 0.7221862484186641 | -0.1969080811715406 | -0.6684865871539348 | 1.0 | 2.0 | 646.7454388175174 | 590.818294353664 | 650.4972510156822 | 606.4433894162175 | -73.57409487152383 | -23.618768868084327 | 0.02990999490446665 | 129.4309510080351 | 737347.1252253413 | 4.42992293210681e+16 | 4.0579317391991685 | 266.7223087782497 | 137.6171137613342 | 54366.86490869232 | 1.7814182552112796 | 46.612573411044366 | 0.14735005938241086 | 58.27209452216387 | 0.004091858990727807 | 0.1650437517750975 | 0.0029865732872307016 | 0.3864621585614819 | 89.0 | 83.0 | 42.0 | 11.0 |
| 0 | 1.2074935069444446 | 5 | -10.355758414156274 | -7.848936746646251 | 8.956373808532875 | 14544.0 | 13792.0 | 474.3 | 5821.2 | -13319.8 | -7.0 | -12637.0 | -5525.9 | 1.0 | 0.0 | 3.79 | 3.79 | 456 | 455 | 98.5 | 1.27 | 0.402 | 0.013487 | 0.009139 | 5.99749e-05 | 6996.920255214921 | 0.003996079695824511 | 97.806420155315 | -0.07313749789953182 | 0.2973657469370992 | 0.06054059578932011 | 0.06965234247958707 | -0.9981919984886888 | -0.052511199699003856 | -0.9942404044800326 | -0.02964360662710623 | -0.30233277716833273 | 0.0340299905413217 | 0.17969564102848096 | 0.0015519792562863368 | 0.5611424689122297 | -0.005164808618808446 | -0.1810356543234377 | UNKNOWN | 180.00000000000003 | 2.0 | 15.85 | 15.85 | 15.0 | 15.0 | 100.0 | 2.36 |  | 0.34870100000000004 | 0.126607 | 0.00140562 | 7006.62105312288 | 0.00314406336943447 | 74.04573642004858 | -0.8182074603041941 | 0.4827541248107289 | -0.003578285999328432 | 0.8185727543355672 | -0.9999982678070422 | 0.004573843461652299 | -0.7287593186639387 | 0.20259539726156284 | -0.8174902123306523 | -0.20321595379209612 | 0.2589642854503864 | 0.19571770862538487 | 0.7219030735097328 | -0.196007714435606 | -0.6749790516197182 | 1.0 | 2.0 | 646.7435061800887 | 590.8230042497535 | 650.5133137195116 | 606.4547925262478 | -73.57068984648866 | -23.618768868084327 | 0.02907916185738685 | 271.54042407269867 | 114138.99356944178 | 4.378610043269432e+16 | 3.5267804014426534 | 262.1918190943417 | 56.0701168181412 | 54082.067268180486 | 1.8009586336171075 | 46.59586891560238 | 0.05967212917267156 | 57.96641268872863 | 0.0037526683839636033 | 0.16438254165208666 | 0.00293331535979342 | 0.3863929347180147 | 89.0 | 83.0 | 42.0 | 11.0 |
| 0 | 0.9521927430555556 | 5 | -10.345630909024717 | -7.84740592207253 | 8.932195118749533 | 14475.0 | 13792.0 | 474.6 | 5796.2 | -13256.1 | -7.0 | -12637.0 | -5525.9 | 1.0 | 0.0 | 3.79 | 3.8 | 456 | 455 | 98.5 | 1.2570000000000001 | 0.402 | 0.013356999999999999 | 0.007056999999999998 | 6.049590000000001e-05 | 6996.92055318148 | 0.00399633723028957 | 97.8064180111561 | -0.10922985698061297 | 0.30518864939997564 | 0.04371090365252997 | 0.10707854501414203 | -0.9962352860472666 | -0.03428710740899365 | -0.9966741311567112 | 0.03393327950377705 | -0.3085005951492253 | -0.030161099551586294 | 0.12376028647327425 | 0.019630323345083817 | 0.579274176282337 | -0.02372608240121377 | -0.12573696687127536 | UNKNOWN | 180.00000000000003 | 2.0 | 15.85 | 15.85 | 15.0 | 15.0 | 100.0 | 2.36 |  | 0.34870100000000004 | 0.126607 | 0.00140562 | 7006.62352366059 | 0.00314396209469105 | 74.0457367368626 | -0.8174081228922127 | 0.4838275408712008 | -0.003741683043651569 | 0.8177743180389113 | -0.9999982437958901 | 0.004738356617730665 | -0.7290830856760941 | 0.20169825878912007 | -0.8176622403955005 | -0.2023195514823952 | 0.2600923870559516 | 0.1955583537039789 | 0.7218540353141059 | -0.1958486661523639 | -0.6753470195571843 | 1.0 | 2.0 | 646.7456072855375 | 590.8214990774222 | 650.5150824307502 | 606.457964890431 | -73.57008773629572 | -23.618768868084327 | 0.02907916185738685 | 347.89929171725373 | 46960.04111677254 | 4.369105379024621e+16 | 3.3620365851667944 | 261.6665435243872 | 37.49794661044788 | 54027.391201130566 | 1.8219396257834668 | 46.59275694783472 | 0.03925831122195656 | 57.907598810518806 | 0.0035761291922971686 | 0.16435203071456098 | 0.002966867877071711 | 0.3863807707430586 | 89.0 | 83.0 | 42.0 | 11.0 |
| 0 | 0.579669363425926 | 5 | -10.337809009140992 | -7.8458804744841535 | 8.913444064417831 | 14579.0 | 13792.0 | 472.7 | 5838.9 | -13350.7 | -7.0 | -12637.0 | -5525.9 | 1.0 | 0.0 | 3.86 | 3.86 | 443 | 442 | 98.4 | 1.254 | 0.402 | 0.01349 | 0.00548 | 6.46896e-05 | 6996.920276423679 | 0.00399668272766191 | 97.8064228319524 | 0.021587859441675083 | 0.4236466970991268 | 0.1575442146972655 | -0.032072176859559286 | -0.9909126047957332 | -0.14999794472629474 | -0.9988561992767748 | -0.05939806400364925 | -0.4271661319901169 | 0.07221409838608743 | 0.2280509256227919 | 0.03916318292525799 | 0.5475638911476286 | -0.04997590103068285 | -0.2294969276916624 | UNKNOWN | 180.00000000000003 | 2.0 | 15.85 | 15.85 | 15.0 | 15.0 | 100.0 | 2.36 |  | 0.34870100000000004 | 0.126607 | 0.00140562 | 7006.622932135389 | 0.00314412566026498 | 74.04573583824909 | -0.8175572502050762 | 0.4836776745798751 | -0.003759566455813183 | 0.8179227313659433 | -0.9999979796610778 | 0.0047546456194276785 | -0.7280915962132882 | 0.2005341635158264 | -0.8178827648282616 | -0.20115483102775936 | 0.2596806982059363 | 0.19580765016285376 | 0.7218739016008718 | -0.19609747215980186 | -0.6756562960941411 | 1.0 | 2.0 | 646.747746839289 | 590.8188060080693 | 650.5156350881169 | 606.4562291826613 | -73.57102086231319 | -23.618768868084327 | 0.02907916185738685 | 435.37662634146017 | 12454.77655469364 | 4.382408451184505e+16 | 3.07578087646048 | 261.75971806219536 | 22.232869810260663 | 54107.60575002372 | 1.826767363404547 | 46.597585774372476 | 0.02206564071129592 | 57.99390485214803 | 0.003297914492524025 | 0.164308794652021 | 0.0029183116694417683 | 0.3863996635609301 | 89.0 | 83.0 | 40.0 | 14.0 |
| 0 | 0.2578060416666667 | 5 | -10.391260080931213 | -7.85294232897164 | 9.03683824507026 | 14510.0 | 13792.0 | 478.7 | 5811.1 | -13288.0 | -7.0 | -12637.0 | -5525.9 | 1.0 | 0.0 | 3.86 | 3.86 | 440 | 439 | 98.8 | 1.34 | 0.402 | 0.013906 | 0.007339 | 6.75706e-05 | 6996.920446395021 | 0.00399638987712749 | 97.8064255894727 | 0.4178649334050735 | 0.4060017107465445 | 0.2469106886721982 | -0.4652561186914659 | -0.983143887381659 | -0.2430058194795052 | -0.9997490626217556 | -0.4308950756689379 | -0.4057232356221825 | 0.4799903371793785 | 0.22346912214824624 | 0.11867447454855035 | 0.5434751782488799 | -0.1435416571723791 | -0.22406038040282167 | UNKNOWN | 180.00000000000003 | 2.0 | 15.85 | 15.85 | 15.0 | 15.0 | 100.0 | 2.36 |  | 0.34870100000000004 | 0.126607 | 0.00140562 | 7006.626645672739 | 0.00314416172776001 | 74.0457363677621 | -0.8159801065033689 | 0.4857939048880041 | -0.004080837906341264 | 0.8163473992983172 | -0.9999982461707859 | 0.005076840742316597 | -0.7272568303885825 | 0.1966619973845641 | -0.8185753700539976 | -0.19728363995145745 | 0.261752928708057 | 0.1956571293696912 | 0.7217940571660352 | -0.1959471988609591 | -0.677040993846666 | 1.0 | 2.0 | 646.7458684380607 | 590.8210243519817 | 650.5196130127679 | 606.4596783327115 | -73.57040904924372 | -23.618768868084327 | 0.02907916185738685 | 469.1788021120601 | 7827.098153467933 | 4.374141597485258e+16 | 3.39217629258858 | 260.7274247178459 | 16.11080693199444 | 54063.67542074808 | 1.9582954322573496 | 46.594699269337504 | 0.015075456875332169 | 57.946716904411424 | 0.003669615783702703 | 0.16417170889041754 | 0.003219989130416437 | 0.38638814681612577 | 89.0 | 83.0 | 40.0 | 14.0 |

## Descriptive Statistics for Numerical Columns
| Column | count | mean | std | min | 25% | 50% | 75% | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| event_id | 162634 | 6566.87179803 | 3798.40731371 | 0 | 3306 | 6558 | 9867 | 13153 |
| time_to_tca | 162634 | 3.35018967927 | 2.01311439441 | -0.149808101852 | 1.58808216725 | 3.29762375579 | 5.08366520544 | 6.99383240741 |
| mission_id | 162634 | 7.11778594882 | 5.80014395061 | 1 | 2 | 5 | 9 | 24 |
| risk | 162634 | -19.3406030585 | 10.0116411839 | -30 | -30 | -17.8706324043 | -9.1732936619 | -1.44285385768 |
| max_risk_estimate | 162634 | -6.28233175573 | 1.01254439765 | -9.81417464039 | -7.00519910071 | -6.32661042181 | -5.62055851027 | -1.08244197917 |
| max_risk_scaling | 162634 | 53740.2538085 | 908695.773629 | 1.07079010491e-13 | 8.32392939097 | 31.7449040419 | 304.743714494 | 49829764.1632 |
| miss_distance | 162634 | 16531.6620879 | 14269.0279515 | 9 | 4683 | 12439 | 25281 | 67373 |
| relative_speed | 162634 | 10655.819638 | 4340.23571996 | 4 | 7421 | 12262 | 14488 | 17138 |
| relative_position_r | 162634 | -40.1984511234 | 644.19261744 | -4815 | -301.475 | -27.3 | 236.8 | 5284.1 |
| relative_position_t | 162634 | 53.5783360183 | 14780.3039606 | -62184.2 | -5773.95 | 0.6 | 5827.2 | 62184.3 |
| relative_position_n | 162634 | 95.2534426996 | 16063.4151756 | -50995.5 | -6974.325 | 38.95 | 7434.675 | 50996.8 |
| relative_velocity_r | 162634 | 0.0282653073773 | 145.104894466 | -2295.3 | -24.3 | -0.8 | 24.4 | 2284.8 |
| relative_velocity_t | 162634 | -8761.32704478 | 5244.68385905 | -16924 | -13946 | -9915.5 | -3645.5 | 331.2 |
| relative_velocity_n | 162634 | -54.0090798972 | 5301.2715872 | -10056.6 | -5209.8 | -128 | 5045.7 | 10011.3 |
| t_time_lastob_start | 162634 | 1.02814909552 | 2.21927789031 | 1 | 1 | 1 | 1 | 180 |
| t_time_lastob_end | 162634 | 0.000940762694148 | 0.0353174761011 | 0 | 0 | 0 | 0 | 2 |
| t_recommended_od_span | 162634 | 4.03220698009 | 1.10814118463 | 1.31 | 3.5 | 3.78 | 3.96 | 14.42 |
| t_actual_od_span | 162634 | 3.79974291968 | 1.31243283648 | 0.01 | 3.46 | 3.71 | 3.92 | 8.66 |
| t_obs_available | 162634 | 952.684395637 | 1023.70025767 | 29 | 430 | 483 | 727 | 4467 |
| t_obs_used | 162634 | 907.669220458 | 1014.12991366 | 6 | 398 | 467 | 720 | 4464 |
| t_residuals_accepted | 162634 | 98.9079989424 | 1.61607887588 | 6.8 | 98.8 | 99.2 | 99.5 | 100 |
| t_weighted_rms | 162634 | 1.1232672135 | 0.164461744347 | 0.525 | 0.998 | 1.107 | 1.243 | 2.93 |
| t_rcs_estimate | 159357 | 2.96045931588 | 2.37164018189 | 0.0111 | 0.4465 | 2.6457 | 4.226 | 27.9614 |
| t_cd_area_over_mass | 162634 | 0.0131431927173 | 0.00826429222966 | -0.09869232 | 0.00816202 | 0.01259592 | 0.016551 | 0.371908 |
| t_cr_area_over_mass | 162634 | 0.0113193007278 | 0.0110076298716 | 0 | 0.004615 | 0.009398 | 0.01476657 | 0.117526 |
| t_sedr | 162634 | 0.000121465793311 | 0.000569275710194 | -0.00017134 | 1.26522e-05 | 1.91806e-05 | 3.82344e-05 | 0.0120439 |
| t_j2k_sma | 162634 | 7039.42099862 | 108.234562831 | 6675.03157391 | 6995.62619002 | 7064.01083218 | 7098.52932075 | 7211.09527827 |
| t_j2k_ecc | 162634 | 0.00190422814522 | 0.00158668706203 | 3.0345151232e-05 | 0.000858976931895 | 0.00168233760604 | 0.00273400417159 | 0.0206197378527 |
| t_j2k_inc | 162634 | 95.4086299944 | 4.20704391894 | 87.2366412881 | 92.0239937684 | 97.8932130464 | 98.3192334399 | 98.8483625704 |
| t_ct_r | 162634 | -0.0994216059208 | 0.306196575707 | -0.999928696164 | -0.228236774205 | -0.0928312804355 | 0.0347331394354 | 0.999775206349 |
| t_cn_r | 162634 | 0.138712850865 | 0.278993177977 | -0.982425921633 | -0.0117475976129 | 0.133620675859 | 0.325874621283 | 0.99687522355 |
| t_cn_t | 162634 | 0.00196452697125 | 0.0888169562997 | -0.974607878203 | -0.0369791432322 | 0 | 0.0385608726257 | 0.986718974722 |
| t_crdot_r | 153404 | 0.0893124899403 | 0.285150418418 | -0.999770103075 | -0.041047841595 | 0.0918277536103 | 0.221709957859 | 0.999929437902 |
| t_crdot_t | 153404 | -0.973406141959 | 0.12636283898 | -1.00000055971 | -0.999625368518 | -0.997763280415 | -0.990560648173 | 0.603048891148 |
| t_crdot_n | 153404 | 0.00022644853971 | 0.0865199531943 | -0.987451009833 | -0.0362388829785 | 7.05311810859e-06 | 0.0379957199521 | 0.972085702723 |
| t_ctdot_r | 153404 | -0.971793867935 | 0.154738719312 | -1.00000020669 | -0.999906120526 | -0.999676486074 | -0.998406032702 | 0.990731628082 |
| t_ctdot_t | 153404 | 0.045442496176 | 0.270382223786 | -0.994952781433 | -0.0683702258743 | 0.0502664598077 | 0.16846167637 | 0.998851648841 |
| t_ctdot_n | 153404 | -0.143993248567 | 0.283405718789 | -0.997456233218 | -0.334104841775 | -0.144934271224 | 0.00684289768397 | 0.983070097079 |
| t_ctdot_rdot | 153404 | -0.0494979107666 | 0.264485906066 | -0.999293017877 | -0.171914303768 | -0.0529268853205 | 0.0714158554005 | 0.994686314981 |
| t_cndot_r | 153404 | 0.0626860154018 | 0.199767089863 | -0.982249378164 | -0.0279407380442 | 0.0664094881357 | 0.166510030801 | 0.994134971046 |
| t_cndot_t | 153404 | 0.00128603912139 | 0.0990128081004 | -0.966863022315 | -0.0386603587071 | 0 | 0.03947039949 | 0.971903124735 |
| t_cndot_n | 153404 | 0.209073203376 | 0.436691858417 | -0.997827499069 | -0.0950429070044 | 0.332900506883 | 0.573649137997 | 0.997620012917 |
| t_cndot_rdot | 153404 | 2.90251342215e-05 | 0.0951089609571 | -0.963684286029 | -0.0378480404852 | 0 | 0.038517546697 | 0.966862435951 |
| t_cndot_tdot | 153404 | -0.0638750215277 | 0.201279144998 | -0.995654396324 | -0.16805928675 | -0.0669713141593 | 0.0273673620448 | 0.984890247814 |
| c_time_lastob_start | 162623 | 40.1508335229 | 73.8095029276 | 1 | 1 | 1 | 2 | 180 |
| c_time_lastob_end | 162623 | 0.58966443861 | 0.823215573431 | 0 | 0 | 0 | 1 | 2 |
| c_recommended_od_span | 162623 | 12.6635762469 | 9.93706326873 | 0 | 6.59 | 11.52 | 16.47 | 234.41 |
| c_actual_od_span | 162623 | 12.0267546411 | 7.91263327338 | 0 | 6.43 | 11.25 | 16.27 | 154.04 |
| c_obs_available | 162623 | 65.9333735081 | 102.420347496 | 3 | 21 | 30 | 60 | 2227 |
| c_obs_used | 162623 | 59.1584954158 | 84.9737969801 | 3 | 21 | 30 | 57 | 2227 |
| c_residuals_accepted | 162623 | 98.7842912749 | 2.538686213 | 37.7 | 98.6 | 99.5 | 100 | 100 |
| c_weighted_rms | 162623 | 1.97862727289 | 1.13620954706 | 0.356 | 1.503 | 1.891 | 2.3 | 237.254 |
| c_rcs_estimate | 109793 | 0.46161246983 | 1.70074825705 | 0.0001 | 0.0092 | 0.0131 | 0.032 | 44.6054 |
| c_cd_area_over_mass | 162634 | 0.784301450839 | 2.34173493502 | -128.17863801 | 0.17736147 | 0.43866 | 0.692811 | 147.912748 |
| c_cr_area_over_mass | 162634 | 0.346478346579 | 0.965477977149 | -0.712079 | 0.051765 | 0.18134 | 0.30516309 | 59.154967 |
| c_sedr | 162634 | 0.00298519132526 | 0.014976272 | -0.107293 | 0.00032759 | 0.000703241 | 0.00154146 | 0.876151 |
| c_j2k_sma | 162634 | 7200.00997692 | 1287.12429359 | 6643.20548868 | 6991.4713692 | 7070.52708453 | 7141.90359454 | 41661.1344043 |
| c_j2k_ecc | 162634 | 0.0161326885545 | 0.067357711603 | 4.54757570497e-05 | 0.00233652413681 | 0.00449731223091 | 0.00908004263782 | 0.834097885721 |
| c_j2k_inc | 162634 | 86.4730259224 | 15.4921669891 | 1.87807470877 | 74.0699591181 | 87.4345996342 | 98.7813950522 | 144.675721025 |
| c_ct_r | 162623 | -0.217448981161 | 0.501334459855 | -1.0000000473 | -0.587254091177 | -0.2369335471 | 0.053379948906 | 0.999999962223 |
| c_cn_r | 162623 | 0.109591943379 | 0.472623730736 | -0.999936604073 | -0.192770796268 | 0.116779545688 | 0.466427251653 | 0.998490715321 |
| c_cn_t | 162623 | 0.0144334203574 | 0.201355053366 | -0.999320450572 | -0.0459046538763 | 0.00267955341778 | 0.0639538819507 | 0.999937709513 |
| c_crdot_r | 153393 | 0.20729616552 | 0.50040211127 | -0.999999974591 | -0.0667065229632 | 0.235350805344 | 0.568685992404 | 1.00000029309 |
| c_crdot_t | 153393 | -0.981465547274 | 0.120562424172 | -1.00000061495 | -0.999989902943 | -0.999896621514 | -0.998711852566 | 0.39286811808 |
| c_crdot_n | 153393 | -0.00832120542865 | 0.200551377213 | -0.999937801889 | -0.059687654537 | 0 | 0.0501122011128 | 0.999321357104 |
| c_ctdot_r | 153393 | -0.858330475904 | 0.312060462681 | -1.00000012796 | -0.998446618957 | -0.984335542453 | -0.893587620943 | 0.999998629765 |
| c_ctdot_t | 153393 | 0.170700417164 | 0.340269943272 | -0.999947340876 | 0 | 0.141437568539 | 0.325150656753 | 1.00000009395 |
| c_ctdot_n | 153393 | -0.13108920013 | 0.50799321683 | -0.999653963267 | -0.54116514605 | -0.162393225522 | 0.226801706223 | 0.999902879832 |
| c_ctdot_rdot | 153393 | -0.170459089049 | 0.343282614332 | -0.999999977734 | -0.326177808264 | -0.144726513095 | 0 | 0.999947311098 |
| c_cndot_r | 153393 | 0.16663033459 | 0.464041287858 | -0.999986798036 | -0.122122197258 | 0.17716845622 | 0.516690260511 | 0.999916914131 |
| c_cndot_t | 153393 | -0.000129723407613 | 0.279515640086 | -0.999986142034 | -0.0976134110706 | 0 | 0.0985709373186 | 0.99998429224 |
| c_cndot_n | 153393 | 0.277171809561 | 0.592832486464 | -0.999956390588 | -0.13820727856 | 0.432235947477 | 0.790218398705 | 0.999891831377 |
| c_cndot_rdot | 153393 | 0.00204592656239 | 0.279605428686 | -0.99998432148 | -0.0973317980057 | 0.000585146854788 | 0.100547086607 | 0.999986269775 |
| c_cndot_tdot | 153393 | -0.186401926387 | 0.482129496523 | -0.999842908455 | -0.568691088383 | -0.203279701852 | 0.120415887161 | 0.999968679401 |
| t_span | 162634 | 8.94504095085 | 7.12778134391 | 0.1 | 1.5 | 9.1 | 12 | 27.71 |
| c_span | 162634 | 2.34335175916 | 1.60797590762 | 2 | 2 | 2 | 2 | 30.45 |
| t_h_apo | 162634 | 674.664672229 | 107.436595392 | 299.131162374 | 629.657988772 | 703.978165823 | 732.952585368 | 842.691394751 |
| t_h_per | 162634 | 647.903325016 | 110.138238817 | 273.072769185 | 597.520161119 | 680.183680501 | 709.878920382 | 825.350073401 |
| c_h_apo | 162634 | 1020.43144395 | 2584.38446486 | 302.793662306 | 641.997983787 | 726.164701353 | 812.733087613 | 70032.4604818 |
| c_h_per | 162634 | 623.314509899 | 113.237742748 | 113.247183142 | 550.757364421 | 640.625496763 | 702.281170818 | 834.637804665 |
| geocentric_latitude | 162634 | -0.664117093848 | 67.8402526967 | -87.9695543904 | -72.999960983 | -1.98339297376 | 72.9378203711 | 87.8189095778 |
| azimuth | 162634 | -0.000716233894803 | 46.642788304 | -112.881931389 | -35.7791523854 | -0.812786576069 | 35.9893774459 | 130.158823723 |
| elevation | 162634 | -0.0201288868956 | 2.16280773464 | -66.3940219144 | -0.141703420139 | 0.00398414174677 | 0.139382321585 | 59.910533776 |
| mahalanobis_distance | 162634 | 192.602768165 | 433.680753797 | 4.66132962787e-07 | 22.4055890888 | 71.1695943521 | 198.476650517 | 15427.1607945 |
| t_position_covariance_det | 162634 | 1.02908803369e+45 | 8.25969595511e+45 | 10.4020881208 | 40024.6039497 | 655189.318877 | 9323184.08463 | 6.7322893736e+46 |
| c_position_covariance_det | 162634 | 1.09780419863e+45 | 8.52658299416e+45 | -8.17563268481e+18 | 236187138327 | 4.08551856717e+13 | 6.06441802746e+15 | 6.7322893736e+46 |
| t_sigma_r | 162634 | 974959.138894 | 7825193.0497 | 0.699495675469 | 3.10951788506 | 4.76425859919 | 7.2773709195 | 63781363 |
| c_sigma_r | 162623 | 1040560.02497 | 8078257.65468 | 0.927164740751 | 28.9520336052 | 68.4286708917 | 190.120211807 | 63781363 |
| t_sigma_t | 162634 | 975362.369511 | 7825143.19358 | 2.59839141787 | 32.7769368503 | 85.8884410839 | 199.328965633 | 63781363 |
| c_sigma_t | 162623 | 1071755.03807 | 8084418.67585 | 4.97632896823 | 1026.25600919 | 3965.31335458 | 13897.9860875 | 76548834.0865 |
| t_sigma_n | 162634 | 974955.559462 | 7825193.49566 | 0.732225989705 | 1.55788927717 | 2.05892609862 | 3.18706885133 | 63781363 |
| c_sigma_n | 162623 | 1040225.19072 | 8078297.54969 | 0.916268713602 | 16.8615109036 | 39.9625074288 | 98.8329804089 | 63781363 |
| t_sigma_rdot | 153404 | 1227.34751838 | 9772.05805507 | 0.00252838706589 | 0.0322787652505 | 0.0861349124489 | 0.196866369652 | 79053.6614985 |
| c_sigma_rdot | 153393 | 1160.84588552 | 9380.36354488 | 0.00529264123687 | 1.06013346734 | 4.03412691917 | 14.1930088424 | 80081.9829924 |
| t_sigma_tdot | 153404 | 1227.0066768 | 9772.10053749 | 0.000723634990862 | 0.00319745992935 | 0.00489637064394 | 0.00742780434413 | 79053.6614985 |
| c_sigma_tdot | 153393 | 1127.80451529 | 9373.9704397 | 0.00100563842051 | 0.0266362403503 | 0.0591425902625 | 0.154083191815 | 79053.6614985 |
| t_sigma_ndot | 153404 | 1227.00446458 | 9772.10081526 | 0.000946125731602 | 0.00270244250633 | 0.00336391759084 | 0.00426407346262 | 79053.6614985 |
| c_sigma_ndot | 153393 | 1127.80927334 | 9373.96981415 | 0.00141019041267 | 0.0281089629834 | 0.0656174214672 | 0.167667229953 | 79053.6614985 |
| F10 | 155812 | 78.0958526943 | 14.7017149662 | 66 | 69 | 72 | 80 | 246 |
| F3M | 155812 | 79.0490847945 | 14.0777728326 | 69 | 71 | 74 | 82 | 159 |
| SSN | 155812 | 20.5894796293 | 25.3652545192 | 0 | 0 | 13 | 30 | 172 |
| AP | 155812 | 8.60803404102 | 8.45369337243 | 0 | 4 | 6 | 10 | 108 |

## Columns Relevant to Satellite Collision Avoidance Decision Support
| Column(s) | Why relevant |
| --- | --- |
| risk | Collision risk proxy/target in log-scale form; likely central to risk assessment. |
| max_risk_estimate | Maximum estimated collision risk; directly relevant to alert severity. |
| max_risk_scaling | Risk scaling factor; useful for interpreting or normalizing risk. |
| miss_distance | Closest approach distance; directly relevant to collision avoidance. |
| relative_speed | Relative speed magnitude; relevant to encounter severity. |
| relative_position_r, relative_position_t, relative_position_n | Relative position components in radial/transverse/normal frame. |
| relative_velocity_r, relative_velocity_t, relative_velocity_n | Relative velocity components; can support relative velocity derivation and dynamics-aware decisions. |
| time_to_tca | Time remaining to closest approach; important for operational urgency. |
| mahalanobis_distance | Uncertainty-normalized separation metric; relevant for conjunction screening. |
| t_position_covariance_det, c_position_covariance_det | Covariance determinant features for target/chaser uncertainty. |
| t_sigma_*, c_sigma_* | Position/velocity uncertainty components for both objects. |
| t_j2k_*, c_j2k_* | Orbital elements for target/chaser context. |
| t_h_apo, t_h_per, c_h_apo, c_h_per | Apoapsis/periapsis altitude features; useful orbital regime context. |
| mission_id | Mission identifier; may encode operational grouping, but not mission priority by itself. |
| c_object_type | Chaser/object classification; useful for object-specific risk interpretation. |
| F10, F3M, SSN, AP | Space-weather features that can affect drag and orbit prediction uncertainty. |

## Required Decision-Support Variables
| Variable | Status | Note |
| --- | --- | --- |
| collision probability | Partially present | `risk` and `max_risk_estimate` appear to represent collision-risk/probability information in log-scale form. A direct probability column may need to be derived, depending on project convention. |
| miss distance | Present | `miss_distance` is present. |
| relative velocity | Present | `relative_speed` is present, and component columns `relative_velocity_r`, `relative_velocity_t`, `relative_velocity_n` are present. |
| time to closest approach | Present | `time_to_tca` is present. |
| fuel cost | Not present | No explicit fuel, delta-v, maneuver, or propellant-cost column is present; this would need to be created from maneuver assumptions or external data. |
| mission priority | Not directly present | `mission_id` is present, but no explicit mission-priority/criticality column is present; it would need to be created or joined from external mission metadata. |

## Risk Column Interpretation
The `risk` column appears to be represented on a log10 scale because its values range approximately from `-30` to `-1.44`. A derived collision probability can therefore be computed as:

```text
collision_probability = 10 ** risk
```

The `max_risk_estimate` column appears to be a maximum estimated risk using the same log-scale convention. A derived maximum collision probability can therefore be computed as:

```text
max_collision_probability = 10 ** max_risk_estimate
```

Short examples:

- `risk = -6` corresponds to `collision_probability = 10^-6`
- `risk = -3` corresponds to `collision_probability = 10^-3`

The project will keep the original `risk` and `max_risk_estimate` columns for traceability, while creating derived probability columns for interpretability and recommendation scoring.

## Scope Note
This report only inspects the dataset. No model training, recommendation generation, dataset deletion, dataset movement, dataset renaming, or dataset modification was performed.
