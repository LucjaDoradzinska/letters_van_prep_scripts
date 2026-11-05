# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:13:04 2022

@author: ldoradzinska
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 15:45:38 2022

@author: ldoradzinska
"""
from collections import OrderedDict 


path='D:\\letters_van\\'

import os
os.chdir('E:\\letters_van_scripts\\')
import lett_van_label_manager as lab_mn


import erp_exp_ld as my


logfile_folder = 'Logfiles\\'
beh_folder = 'Results\\nopas\\behavior\\'
pas_folder = 'Results\\nopas\\pas\\'


raw_beh_df_folder = beh_folder + 'raw_beh_df\\'
beh_log_folder = beh_folder + 'beh_logs\\'
beh_plot_folder = beh_folder + 'beh_plots\\'

raw_pas_df_folder = pas_folder + 'raw_beh_df\\'
pas_log_folder = pas_folder + 'pas_logs\\'
pas_plot_folder = pas_folder + 'pas_plots\\'


log_extention = '_letters_van.log'

raw_signal_folder = 'Raw_EEG\\'
eeg_folder = 'Results\\nopas\\EEG\\'

eeg_log_folder = eeg_folder
raw_prep_folder = eeg_folder + 'raws_prep\\'
filt_folder = eeg_folder + 'filt\\'
epochs_raw_folder = eeg_folder + 'epochs_raw\\'
epochs_noeog_folder = eeg_folder + 'epochs_noeog\\'
epochs_clean_folder = eeg_folder + 'epochs_clean\\'
evokeds_side_folder = eeg_folder + 'evokeds_side\\'
evokeds_folder = eeg_folder + 'evokeds\\'
erps_folder = eeg_folder + 'ERPs\\'
van_folder = erps_folder + 'VAN\\'
van_lat_folder = erps_folder + 'VAN_lat\\'

mixed_models_folder = eeg_folder + 'long_comps\\'

#%% VARIABLES



subjects = ['021', '022', '023', '024', '025', '026', '027', '028', '029', '030',
            '031', '032', '033', '034', '035', '036', '037', '038', '039', '040']



beh_stim_coding = OrderedDict({'part':{'main':'main', 'consc':'consc'},
                               'att_cond':{'attended':'att', 'unattended':'opo'},
                               'masking':{'masked':'mask', 'unmasked':'unmask'},
                               'stimulus': {'target': 'targ', 'distractor':'dist', 'catch': 'catch'},
                               'side':{'left':'left', 'right':'right'}, 
                               'left_letter':{'U':'U', 'H':'H', 'T':'T', 'X':'X'}, 
                               'right_letter':{'U':'U', 'H':'H', 'T':'T', 'X':'X'}, 
                               'att_side':{'left':'left', 'right':'right'}, 
                               'target_lett':{'U':'U', 'H':'H', 'T':'T'}})



quest_codes = ['lett']
valid_resps = {'201':'incorrect', '211':'correct', '204':'incorrect', '214':'correct'}


trial_end_codes = ['fix', 'break', 'end', 'inst']


#EEG CHANNELS
stim_channel = 'Status'
montage_kind = 'biosemi64'
veog_channels = ['EXG1', 'EXG2']
heog_channels = ['EXG3', 'EXG4']
exclude_channels = ['EXG7', 'EXG8']
reref_channels = ['EXG5', 'EXG6']


#EEG MARKERS
eeg_stim_coding = OrderedDict({'att_cond':{'attended':1, 'unattended':9},
                               'masking':{'masked':0, 'unmasked':4},
                               'stimulus':{'target':0, 'distractor':2},
                               'side':{'left':0, 'right':1}})


reduce_factors = ['side']
markers = lab_mn.Eeg_markers_manager([eeg_stim_coding], reduce_factors)


resp_markers = [201, 211, 204, 214]


#%% LOGFILES TO DATAFRAME


factors = lab_mn.get_beh_factors(beh_stim_coding)

stim_conditions = lab_mn.get_stim_conditions(beh_stim_coding)


my.beh.logfiles_to_array(subjects, path, logfile_folder, log_extention, raw_beh_df_folder, factors, stim_conditions, quest_codes, trial_end_codes, valid_resps)

beh_analizer = my.beh.Beh_analizer(subjects, path, raw_beh_df_folder, beh_log_folder)
beh_long_df = beh_analizer.get_beh_raw_long ('raw_beh_long', save_csv = True)

main_combine = {'part':['main'],
                'att_cond':['attended', 'unattended'],
                'masking':['masked', 'unmasked'],
                'stimulus': ['target', 'distractor']}

main_compare = lab_mn.beh_combine_conds(main_combine)

resp_count_log = beh_analizer.summarize_corr_resps('resp_log', main_compare, pool_all =True,  save_csv = True)


accuracy_log = beh_analizer.calculate_accuracy('accuracy_log', main_compare, save_csv = True)

RT_log = beh_analizer.aggregate_RTs ('RT_log', main_compare, 200, 10000, resps_types = ['correct', 'incorrect'], method = 'median', save_csv = True)

d_combine = {'part':['main'],
             'att_cond':['attended'],
             'masking':['masked', 'unmasked']}

d_compare = lab_mn.beh_combine_conds(d_combine)

signal = {'stimulus':['target']}
noise = {'stimulus':['distractor']}

d_log, c_log, hit_fa_log = beh_analizer.calculate_sdt_params('attended_std', d_compare, signal, noise, d_corr = True, 
                                                                save_hit_fa_log = True, save_csv = True)


consc_combine = {'part':['consc'],
                'att_cond':['attended', 'unattended'],
                'masking':['unmasked'],
                'stimulus': ['target', 'distractor']}

consc_compare = lab_mn.beh_combine_conds(consc_combine)

resp_count_log = beh_analizer.summarize_corr_resps('consc_resp_log', consc_compare, save_csv = True)


accuracy_log = beh_analizer.calculate_accuracy('consc_accuracy_log', consc_compare, save_csv = True)
  

#%% PAS ANALYSIS

quests = OrderedDict({'quest_pas_att':{'content':'Jak dobrze widziałeś/aś litery pojawiające się po attended stronie?',
                                       'resps':{'211':'W ogóle nie widziałem/am', 
                                                '212':'Widziałem/am ale nie rozpoznawałem/am', 
                                                '213':'Widziałem/am niewyraźnie i rozpoznawałem/am', 
                                                '214':'Widziałem/am bardzo wyraźnie'}},
                      'quest_pas_opo':{'content':'Jak dobrze widziałeś/aś litery pojawiające się po unattended stronie?',
                                       'resps':{'211':'W ogóle nie widziałem/am', 
                                                '212':'Widziałem/am ale nie rozpoznawałem/am', 
                                                '213':'Widziałem/am niewyraźnie i rozpoznawałem/am', 
                                                '214':'Widziałem/am bardzo wyraźnie'}},
                      'quest_target_opo':{'content':'Czy widziałeś/aś literę target pojawiającą się po unattended stronie?',
                                        'resps':{'211':'Nie widziałem/am', 
                                                 '214':'Widziałem/am'}},
                      'quest_dist_opo':{'content':'Czy widziałeś/aś inne litery pojawiające się po unattended stronie?',
                                        'resps':{'211':'Nie widziałem/am', 
                                                 '214':'Widziałem/am'}},
                      'quest_last_rates':{'content':'W jakiej części prób widziałeś/aś jakąkolwiek literę (U, H lub T) po dowolnej stronie?',
                                          'resps':{'211':'Ok. 25% prób', 
                                                   '212':'Ok. 50% prób', 
                                                   '213':'Ok. 75% prób', 
                                                   '214':'100% prób'}},
                      'quest_side_rates':{'content':'Gdy już widziałeś/aś literę to jak często była ona po stronie attended a jak często po unattended?',
                                          'resps':{'211':'Zawsze po attended', 
                                                   '212':'Częściej po attended', 
                                                   '213':'Pół na pół', 
                                                   '214':'Częściej po unattended'}},
                      'quest_all_rates':{'content':'We wcześniejszych częściach eksperymentu w jakiej części prób widziałeś/aś jakąkolwiek literę (U, H lub T) po dowolnej stronie?',
                                         'resps':{'211':'Ok. 25% prób', 
                                                  '212':'Ok. 50% prób', 
                                                  '213':'Ok. 75% prób', 
                                                  '214':'100% prób'}},
                      'quest_all_side_rates':{'content':'We wcześniejszych częściach eksperymentu gdy już widziałeś/aś literę to jak często była ona po stronie, po której rozwiązywałeś/aś zadanie, a jak często po przeciwnej?',
                                              'resps':{'211':'Zawsze po stronie zadania', 
                                                       '212':'Częściej po stronie zadania', 
                                                       '213':'Pół na pół', 
                                                       '214':'Częściej po stronie przeciwnej'}}})


my.beh.survey_to_df(subjects, path, logfile_folder, log_extention, raw_pas_df_folder, quests)

surv_analizer = my.beh.Surv_analizer(subjects, path, raw_pas_df_folder, pas_log_folder)
surv_analizer.summarize_resps('survey_log', quests, save_csv = True)

#%% EEG PREPROCESSING

#REREFERENCING RAW DATA
#DEFAULTS: montage = 'biosemi', set_reref = True
my.eeg_prep.raw_prep(subjects, path, raw_signal_folder, raw_prep_folder, stim_channel, set_eog = True, 
                     veog_channels = veog_channels, heog_channels = heog_channels, exclude_channels = exclude_channels, 
                     reref_channels = reref_channels)


#FILTERING RAW DATA
#DEFAULTS: filt_method = 'fir', low_cutoff = 0.1, high_cutoff = 40, set_notch = False
my.eeg_prep.filter_raw(subjects, path, raw_prep_folder, filt_folder, plot_psd = True, save_psd_plots = True)



# EPOCHING, REJECTING INVALID TRIALS AND RESAMPLING
#DEFAULTS: reject_miss = True, reject_to_early = True, epoch_tmin = -0.2, epoch_tmax = 1.2, epoch_baseline = (None, 0),
#resample_freq = 256, save_xlsx = True, save_csv = False
stim_markers = markers.get_markers()

invalid_resp_log = my.eeg_prep.to_epochs(subjects, path, filt_folder, epochs_raw_folder, eeg_log_folder, stim_channel, 
                                         stim_markers, resp_markers, reject_to_early = False, epoch_baseline = None, 
                                         resample = True)


# REMOVING EOGS FROM EPOCHS
#DEFAULTS: veog_thresh = 140e-6, veog_window = [-0.1, 0.1], heog_thresh = 80e-6, heog_window = [0, 0.5],
#ica_thresh = 3, n_components = 64, ica_method = 'fastica', save_xlsx = True, save_csv = False
eog_artifacts_log = my.eeg_prep.remove_eogs(subjects, path, epochs_raw_folder, epochs_noeog_folder, eeg_log_folder, 
                                            reject_veog = True, reject_heog = True, perform_ica = True)


# CLEANING EPOCHS FROM ARTIFACTS
#DEFAULTS: autorej_method = 'random_search', rej_by_amplitude = False, eeg_thresh = 140e-6, rej_manually = False, 
#save_xlsx = True, save_csv = False,plot_save_format = 'png'
epochs_clean_log = my.eeg_prep.clean_epochs(subjects, path, epochs_noeog_folder, epochs_clean_folder, eeg_log_folder,
                                            autoreject = True, plot_psd = True, save_psd_plots = True)


#%% EVOKEDS
evoked_labels = markers.evoked_labels()

evoked_log = my.eeg_prep.calculate_evoked(subjects, path, epochs_clean_folder, evokeds_side_folder, evokeds_side_folder, 
                                          evoked_labels = evoked_labels, equalize = False)

reduce_markers = markers.reduce_markers()
evoked_labels_reduced = markers.evoked_labels_reduced()

evoked_log = my.eeg_prep.calculate_evoked(subjects, path, epochs_clean_folder, evokeds_folder, evokeds_folder, 
                                          reduce_markers = reduce_markers, evoked_labels = evoked_labels_reduced, equalize = False)


#%% AVG PLOTS

evokeds_labels = []
for labs in markers.evoked_labels_reduced():
    evokeds_labels = evokeds_labels + labs
    
    
erp = my.erps.Erp_waveform(subjects, path, evokeds_folder, evokeds_labels)


erp_labels = markers.erp_labels()
plot_folder = erps_folder + 'avg_erp\\'
legend_loc = (0.5, 1.1)
ylim = [-6.5, 6]
y_ticks = [-6, -3, 0, 3, 6]
xlim = [-50, 500]
x_ticks = [0, 100, 200, 300, 400, 500]
fig_size = [7.2, 6]
temp_roi = ['P7', 'P8', 'PO7', 'PO8', 'P9', 'P10']
time_windows = {'early': [140, 190], 'late': [190, 285]}

for tw in ['early', 'late']:
    erp.comp_plot(plot_folder, 'avg_' + tw, erp_labels, temp_roi, plot_time_wind = True, 
                  time_wind = time_windows[tw], colors=['#bd5887ff'], legend = [], 
                  fig_size = fig_size, xlim = xlim, x_ticks = x_ticks, save_format = 'svg')
    erp.comp_plot(plot_folder, 'avg_' + tw, erp_labels, temp_roi, plot_time_wind = True, 
                  time_wind = time_windows[tw], colors=['#bd5887ff'], legend = [],
                  fig_size = fig_size, xlim = xlim, x_ticks = x_ticks, save_format = 'svg')

#%% COMP PLOTS

evokeds_labels = []
for labs in markers.evoked_labels():
    evokeds_labels = evokeds_labels + labs
erp_lat = my.erps.Erp_waveform(subjects, path, evokeds_side_folder, evokeds_labels)

plot_folder = van_lat_folder + 'plots\\'


left_roi =  ['P7', 'P9', 'PO7']
right_roi = ['P8', 'P10', 'PO8']
time_windows = {'early': [140, 190], 'late': [190, 285]}


contrast_left = {'att_cond': {'attended':['attended'], 'unattended':['unattended']},
                 'masking': {'masked': ['masked'], 'unmasked': ['unmasked']},
                 'stimulus': {'target': ['target'], 'distractor': ['distractor']},
                 'side':{'':['left']}}
contrast_right = {'att_cond': {'attended':['attended'], 'unattended':['unattended']},
                  'masking': {'masked': ['masked'], 'unmasked': ['unmasked']},
                 'stimulus': {'target': ['target'], 'distractor': ['distractor']},
                 'side':{'':['right']}}

erp_labels_left = markers.erp_labels(contrast = contrast_left, reduced = False)
erp_labels_right = markers.erp_labels(contrast = contrast_right, reduced = False)

legend = ['']
fig_size = [7.2, 6]
legend_loc = (0.5, 1.1)
ylim = [-6.5, 6]
y_ticks = [-6, -3, 0, 3, 6]
xlim = [-50, 500]
x_ticks = [0, 100, 200, 300, 400, 500]
colors_lat = ['#dc4868ff','#1f114bff','#fb8961ff','#762181ff','#dc4868ff','#1f114bff', '#fb8961ff','#762181ff']
styles = ['--', '--' ,'--', '--' ,'-', '-', '-', '-' ]



for tw in ['early', 'late']:
    #erp.calc_lateral_erp_amp(van_lat_folder, 'VAN_lat_' + tw, erp_labels_left, erp_labels_right, 
   
    erp_lat.lat_comp_plot(plot_folder, 'VAN_lat_' + tw, erp_labels_left, erp_labels_right, 
                          left_roi, right_roi, plot_ipsi = False, plot_time_wind = True, time_wind = time_windows[tw], 
                          colors = colors_lat, styles = styles, legend = legend, legend_loc = legend_loc, 
                          fig_size = fig_size, xlim = xlim,x_ticks = x_ticks, save_format = 'png')




comp_by_left = {'att_cond': {'attended':'attended', 'unattended':'unattended'}, 'stimulus': {'target': 'target', 'distractor': 'distractor'},
                    'side':{'':'left'}}
comp_by_right = {'att_cond': {'attended':'attended', 'unattended':'unattended'}, 'stimulus': {'target': 'target', 'distractor': 'distractor'},
                    'side':{'':'right'}}


contrast = {'masking':{'masked':['masked'], 'unmasked':['unmasked']}}

erp_labels_left = markers.erp_labels(comp_by_left, contrast, reduced = False)
erp_labels_right = markers.erp_labels(comp_by_right, contrast, reduced = False)

legend = ['']
fig_size = [7.2, 6]
legend_loc = (0.5, 1.1)
ylim = [-6.5, 6]
y_ticks = [-6, -3, 0, 3, 6]
xlim = [-50, 500]
x_ticks = [0, 100, 200, 300, 400, 500]
colors_lat = ['#fb8961ff','#762181ff']
styles = ['--', '--', '-', '-' ]

for tw in ['early', 'late']:
    erp_lat.lat_diff_plot (plot_folder, 'VAN_diff_lat' + tw, erp_labels_left, erp_labels_right, left_roi, right_roi, plot_ipsi = False,
                           plot_time_wind = True, time_wind = time_windows[tw], colors = colors_lat[:2], styles = styles[:2], legend=[''], 
                           legend_loc=legend_loc, fig_size = fig_size, ylim = ylim, y_ticks = y_ticks,  xlim = xlim, x_ticks = x_ticks, 
                           save_format = 'svg')
    





#%% TOPO PLOTS
evokeds_labels = []
for labs in markers.evoked_labels_reduced():
    evokeds_labels = evokeds_labels + labs
    
    
erp = my.erps.Erp_waveform(subjects, path, evokeds_folder, evokeds_labels)

plot_folder = erps_folder + 'avg_topo_plots\\'
erp_labels = markers.erp_labels()
erp_name = 'all_erps_magma'
erp.mean_topo(plot_folder, erp_name, erp_labels, 0.07, 0.38, time_step = 0.05, volt_min = -6, volt_max = 6,
              cmap ='magma', save_format = 'svg')


plot_folder = erps_folder + 'avg_topo_plots\\'
contrast = {'masking':{'unmasked':['unmasked'], 'masked':['masked']}}
erp_labels = markers.erp_labels(contrast = contrast)

erp.diff_topo(plot_folder,'diff_masking', erp_labels, 0.07, 0.38, time_step=0.05, volt_min = -5, volt_max = 5, 
              cmap='magma', save_format='svg')


contrast = {'att_cond':{'attended':['attended'], 'unattended':['unattended']}}
erp_labels = markers.erp_labels(contrast = contrast)

erp.diff_topo(plot_folder, 'diff_task', erp_labels, 0.07, 0.38, time_step=0.05, volt_min = -2.5, volt_max = 2.5, 
              cmap='magma', save_format='svg')

contrast = {'stimulus':{'target':['target'], 'distractor':['distractor']}}
erp_labels = markers.erp_labels(contrast = contrast)

erp.diff_topo(plot_folder, 'diff_stim', erp_labels, 0.07, 0.38, time_step=0.05, volt_min = -1.5, volt_max = 1.5, 
              cmap='magma', save_format='svg')



plot_folder = erps_folder + 'avg_topo_plots\\'
contrast = {'masking':{'unmasked':['unmasked'], 'masked':['masked']}}
erp_labels = markers.erp_labels(contrast = contrast)

erp.diff_topo(plot_folder,'diff_masking_r', erp_labels, 0.09, 0.34, time_step=0.04, volt_min = -4, volt_max = 4, 
              cmap='magma_r', save_format='svg')


contrast = {'att_cond':{'attended':['attended'], 'unattended':['unattended']}}
comp_by = {'masking':{'unmasked':'unmasked'}}
erp_labels = markers.erp_labels(comp_by, contrast)

erp.diff_topo(plot_folder, 'diff_task_unmasked_r', erp_labels, 0.09, 0.34, time_step=0.04, volt_min = -4, volt_max = 4, 
              cmap='magma_r', save_format='svg')

contrast = {'stimulus':{'target':['target'], 'distractor':['distractor']}}
comp_by = {'masking':{'unmasked':'unmasked'}}
erp_labels = markers.erp_labels(comp_by, contrast)

erp.diff_topo(plot_folder, 'diff_stim_unmasked_r', erp_labels, 0.09, 0.34, time_step=0.04, volt_min = -1.5, volt_max = 1.5, 
              cmap='magma_r', save_format='svg')



#%% MIXED MODELS
temp_roi = ['P7', 'P8', 'PO7', 'PO8', 'P9', 'P10']
left_roi =  ['P7', 'P9', 'PO7']
right_roi = ['P8', 'P10', 'PO8']
time_windows = {'early': [140, 190], 'late': [190, 285]}


reduce_markers = markers.reduce_markers()
evoked_labels_reduced = markers.evoked_labels_reduced()
epochs_data = my.comps_long.Trials_data(subjects, path, epochs_clean_folder, reduce_markers, evoked_labels = evoked_labels_reduced)

conditions = {'att_cond':{'att':['attended'], 'unatt':['unattended']}, 'masking':{'masked':['masked'], 'unmasked':['unmasked']}, 
              'stimulus':{'targ':['target'], 'dist':['distractor']}}

mixed_labels = markers.mixed_models_labels(conditions)

for tw in ['early', 'late']:
     epochs_data.get_central_comp(mixed_models_folder, 'VAN_' + tw, mixed_labels, temp_roi, time_windows[tw])



evoked_labels = markers.evoked_labels()
epochs_data = my.comps_long.Trials_data(subjects, path, epochs_clean_folder, evoked_labels = evoked_labels)
conditions_left = {'att_cond':{'att':['attended'], 'unatt':['unattended']}, 'masking':{'masked':['masked'], 'unmasked':['unmasked']}, 
                   'stimulus':{'targ':['target'], 'dist':['distractor']}, 'side':{'left':['left']}}
conditions_right = {'att_cond':{'att':['attended'], 'unatt':['unattended']}, 'masking':{'masked':['masked'], 'unmasked':['unmasked']}, 
                   'stimulus':{'targ':['target'], 'dist':['distractor']}, 'side':{'right':['right']}}
long_labels_left = markers.mixed_models_labels(conditions_left, reduced = False)
long_labels_right = markers.mixed_models_labels(conditions_right, reduced = False)

for tw in ['early', 'late']:
    epochs_data.get_lateral_comp(mixed_models_folder, 'VAN_lat_' + tw, long_labels_left, long_labels_right, left_roi, right_roi, time_windows[tw])
