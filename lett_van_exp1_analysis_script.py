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
beh_folder = 'Results\\pas\\behavior\\'
pas_folder = 'Results\\pas\\pas\\'

raw_beh_df_folder = beh_folder + 'raw_beh_df\\'
beh_log_folder = beh_folder + 'beh_logs\\'
beh_plot_folder = beh_folder + 'beh_plots\\'

raw_pas_df_folder = pas_folder + 'raw_beh_df\\'
pas_log_folder = pas_folder + 'pas_logs\\'
pas_plot_folder = pas_folder + 'pas_plots\\'



log_extention = '_letters_van.log'

raw_signal_folder = 'Raw_EEG\\'
eeg_folder = 'Results\\pas\\EEG\\'

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



subjects = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', 
            '011', '012', '013', '014', '015', '016', '017', '018', '019', '020']



beh_stim_coding = OrderedDict({'att_cond':{'attended':'att', 'unattended':'opo'},
                               'masking':{'masked':'mask', 'unmasked':'unmask'},
                               'stimulus': {'catch': 'catch', 'target': 'targ', 'distractor':'dist'},
                               'side':{'left':'left', 'right':'right'}, 
                               'left_letter':{'U':'U', 'H':'H', 'T':'T', 'X':'X'}, 
                               'right_letter':{'U':'U', 'H':'H', 'T':'T', 'X':'X'}, 
                               'att_side':{'left':'left', 'right':'right'}, 
                               'target_lett':{'U':'U', 'H':'H', 'T':'T'},
                               'pas_trial':{'attended':'pasatt', 'unattended':'pasopo'}})


quest_codes = ['lett']
valid_resps = {'201':'incorrect', '211':'correct', '204':'incorrect', '214':'correct'}

pas_quest_codes = ['pas']
pas_valid_resps = {'221':'1', '222':'2', '223':'3', '224':'4'}

trial_end_codes = ['fix', 'break', 'end', 'inst', 'pas']


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


eeg_catch_coding = OrderedDict({'att_cond':{'attended':51, 'unattended':53},
                               'masking':{'masked':0},
                               'stimulus':{'catch':0},
                               'side':{'left':0, 'right':1}})



reduce_factors = ['side']
markers = lab_mn.Eeg_markers_manager([eeg_catch_coding, eeg_stim_coding], reduce_factors)


resp_markers = [201, 211, 204, 214]



#%% LOGFILES TO DATAFRAME


factors = lab_mn.get_beh_factors(beh_stim_coding)

stim_conditions = lab_mn.get_stim_conditions(beh_stim_coding)


my.beh.logfiles_to_array(subjects, path, logfile_folder, log_extention, raw_beh_df_folder, factors, stim_conditions, quest_codes, trial_end_codes, valid_resps)



pas_conditions = OrderedDict({'pas_masking':{'masked':[{'att_cond':'attended', 'masking':'masked'}, 
                                                       {'att_cond':'unattended', 'pas_trial':'attended'},
                                                       {'att_cond':'unattended',  'masking':'masked', 'pas_trial':'unattended'}],
                                             'unmasked':[{'att_cond':'attended', 'masking':'unmasked'}, 
                                                         {'att_cond':'unattended',  'masking':'unmasked', 'pas_trial':'unattended'}]},
                                            
                              'pas_stimulus':{'target':[{'att_cond':'attended', 'stimulus':'target'}, 
                                                        {'att_cond':'unattended', 'stimulus':'target', 'pas_trial':'unattended'}],
                                              'distractor':[{'att_cond':'attended', 'stimulus':'distractor'}, 
                                                            {'att_cond':'unattended', 'stimulus':'distractor', 'pas_trial':'unattended'},
                                                            {'att_cond':'unattended', 'pas_trial':'attended'}],
                                              'catch':[{'att_cond':'attended', 'stimulus':'catch'}, 
                                                        {'att_cond':'unattended', 'stimulus':'catch', 'pas_trial':'unattended'}]}})


factors = lab_mn.get_beh_factors(beh_stim_coding, pas_conditions)
stim_conditions = lab_mn.get_stim_conditions(beh_stim_coding, pas_conditions)

my.beh.logfiles_to_array(subjects, path, logfile_folder, log_extention, raw_pas_df_folder, factors, stim_conditions, pas_quest_codes, trial_end_codes, pas_valid_resps)

    
#%% BEHAVIOURAL RESULTS


beh_analizer = my.beh.Beh_analizer(subjects, path, raw_beh_df_folder, beh_log_folder)

beh_long_df = beh_analizer.get_beh_raw_long ('raw_beh_long', save_csv = True)

main_combine = {'att_cond':['attended', 'unattended'],
                'masking':['masked', 'unmasked'],
                'stimulus': ['target', 'distractor', 'catch']}

main_compare = lab_mn.beh_combine_conds(main_combine)

resp_count_log = beh_analizer.summarize_corr_resps('resp_log', main_compare, pool_all = True, save_csv = True)


accuracy_log = beh_analizer.calculate_accuracy('accuracy_log', main_compare, save_csv = True)
RT_log = beh_analizer.aggregate_RTs ('RT_log', main_compare, 200, 10000, resps_types = ['correct', 'incorrect'], method = 'median', save_csv = True)
        

pas_analizer = my.beh.Beh_analizer(subjects, path, raw_pas_df_folder, pas_log_folder)

pas_long_df = pas_analizer.get_beh_raw_long ('raw_pas_long', save_csv = True)

main_combine = {'pas_trial':['attended', 'unattended'],
                'pas_masking':['masked', 'unmasked'],
                'pas_stimulus': ['target', 'distractor', 'catch']}

main_compare = lab_mn.beh_combine_conds(main_combine)

resps_types = pas_valid_resps.values()

resp_count_log = pas_analizer.summarize_resps_types('resp_log', main_compare, resps_types, save_csv = True)
rates_log = pas_analizer.calculate_rates('rates_log', main_compare, resps_types, save_csv = True)
RT_log = pas_analizer.aggregate_RTs ('RT_log', main_compare, 200, 10000, resps_types = resps_types, method = 'median', save_csv = True)


d_combine = {'att_cond':['attended', 'unattended']}
d_compare = lab_mn.beh_combine_conds(d_combine)
signal = [{'masked_target':{'pas_masking':['masked'],'pas_stimulus':['target']}},
          {'masked_distractor':{'pas_masking':['masked'],'pas_stimulus':['distractor']}},
          {'unmasked_target':{'pas_masking':['unmasked'],'pas_stimulus':['target']}},
          {'unmasked_distractor':{'pas_masking':['unmasked'],'pas_stimulus':['distractor']}}]
noise = {'pas_masking':['masked'], 'pas_stimulus':['catch']}
resp_mapping = {'noise_resp':['1'], 'signal_resp':['2', '3', '4']}

d_log, c_log, hit_fa_log = pas_analizer.calculate_sdt_params('all_vs_catch', d_compare, signal, noise, resp_mapping = resp_mapping, d_corr = True, 
                                                             save_hit_fa_log = True, save_csv = True)
 
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
                  fig_size = fig_size, xlim = xlim, x_ticks = x_ticks, save_format = 'png')

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
                          fig_size = fig_size, xlim = xlim,x_ticks = x_ticks, save_format = 'svg')




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
                           save_format = 'png')
    








#%% PLOT MASKED AND UNMASKED TOPO
evokeds_labels = []
for labs in markers.evoked_labels_reduced():
    evokeds_labels = evokeds_labels + labs

erp = my.erps.Erp_waveform(subjects, path, evokeds_folder, evokeds_labels)

evokeds_labels = []
for labs in markers.evoked_labels():
    evokeds_labels = evokeds_labels + labs
erp_lat = my.erps.Erp_waveform(subjects, path, evokeds_side_folder, evokeds_labels)

plot_folder = van_folder + 'plots\\'

erp_labels = markers.erp_labels()

erp_name = 'all'
erp.mean_topo(plot_folder, erp_name, erp_labels, 0.07, 0.38, time_step=0.05, volt_min=-6, volt_max=6,
              cmap='magma', save_format='png')


temp_roi = ['P7', 'P8', 'PO7', 'PO8', 'P9', 'P10']
left_roi =  ['P7', 'P9', 'PO7']
right_roi = ['P8', 'P10', 'PO8']

erp.comp_plot(plot_folder, 'avg', erp_labels, temp_roi, colors=['#a9327dff'], legend=[], save_format='png')

time_windows = {'early': [140, 190], 'late': [190, 285]}

#VAN calc and plotting
contrast = {'masking': {'masked': ['masked'], 'unmasked': ['unmasked']},
             'stimulus':{'catch':['catch'], 'target':['target'], 'distractor':['distractor']}}
contrast_left = {'masking': {'masked': ['masked'], 'unmasked': ['unmasked']},
                 'stimulus':{'catch':['catch'],'target':['target'], 'distractor':['distractor']}, 
                 'side':{'':['left']}}
contrast_right = {'masking': {'masked': ['masked'], 'unmasked': ['unmasked']},
                 'stimulus':{'catch':['catch'], 'target':['target'], 'distractor':['distractor']},
                 'side':{'':['right']}}
comp_by = {'att_cond': {'attended': 'attended', 'unattended': 'unattended'}}
erp_labels = markers.erp_labels(comp_by, contrast)
erp_labels_left = markers.erp_labels(comp_by, contrast_left, reduced = False)
erp_labels_right = markers.erp_labels(comp_by, contrast_right, reduced = False)

for tw in ['early', 'late']:
    erp.calc_central_erp_amp(van_folder, 'VAN_' + tw, erp_labels, temp_roi, time_windows[tw])
    
    erp_lat.calc_lateral_erp_amp(van_folder, 'VAN_lat_' + tw, erp_labels_left, erp_labels_right, 
                                 left_roi, right_roi, time_windows[tw])


legend = ['attended', 'unattended']
legend_loc = (0.5, 1.1)
ylim = [-6.5, 6]
y_ticks = [-6, -3, 0, 3, 6]
xlim = [-50, 500]
x_ticks = [0, 100, 200, 300, 400, 500]
colors_centr = ["#fece91ff", "#fb8961ff", "#c33b75ff", "#762181ff", "#120d31ff"]
colors_lat = ["#fece91ff", "#fece91ff", "#fb8961ff", "#fb8961ff", "#c33b75ff","#c33b75ff", "#762181ff", "#762181ff", "#120d31ff", "#120d31ff"]
styles_lat = ['--','-','--','-', '--','-', '--','-', '--','-']
fig_size = [7.2, 6]
for tw in ['early', 'late']:
    
    erp.comp_plot(plot_folder, 'VAN_' + tw, erp_labels, temp_roi, plot_time_wind=True, 
                  time_wind = time_windows[tw], colors = colors_centr, #styles = styles, 
                  legend = legend, legend_loc = legend_loc, fig_size = fig_size, xlim = xlim, 
                  x_ticks = x_ticks, save_format = 'png')
    
    erp_lat.lat_comp_plot(plot_folder, 'VAN_lat_' + tw, erp_labels_left, erp_labels_right, 
                          left_roi, right_roi, plot_time_wind = True, time_wind = time_windows[tw], 
                          colors = colors_lat, styles = styles_lat, legend = legend, legend_loc = legend_loc, 
                          fig_size = fig_size, xlim = xlim,x_ticks = x_ticks, save_format = 'png')


#differential plot
comp_by_att = {'att_cond':{'':'attended'}, 'stimulus':{'distractor':'distractor','target':'target'}}
comp_by_unatt = {'att_cond':{'':'unattended'}, 'stimulus':{'distractor':'distractor','target':'target'}}
comp_by_left_att = {'att_cond':{'':'attended'}, 'stimulus':{'distractor':'distractor','target':'target'}, 'side':{'':'left'}}
comp_by_left_unatt = {'att_cond':{'':'unattended'}, 'stimulus':{'distractor':'distractor','target':'target'}, 'side':{'':'left'}}
comp_by_right_att = {'att_cond':{'':'attended'}, 'stimulus':{'distractor':'distractor','target':'target'}, 'side':{'':'right'}}
comp_by_right_unatt = {'att_cond':{'':'unattended'}, 'stimulus':{'distractor':'distractor','target':'target'}, 'side':{'':'right'}}
contrast = {'masking':{'masked':['masked'], 'unmasked':['unmasked']}}
erp_labels_att = markers.erp_labels(comp_by_att, contrast) 
erp_labels_unatt = markers.erp_labels(comp_by_unatt, contrast) 
erp_labels_left_att = markers.erp_labels(comp_by_left_att, contrast, reduced = False)
erp_labels_right_att = markers.erp_labels(comp_by_right_att, contrast, reduced = False)
erp_labels_left_unatt = markers.erp_labels(comp_by_left_unatt, contrast, reduced = False)
erp_labels_right_unatt = markers.erp_labels(comp_by_right_unatt, contrast, reduced = False)
ylim = [-6.5, 6]
y_ticks = [-6, -3, 0, 3, 6]
styles = ['--', '-' ,'--', '-' ]
colors_centr = ["#c33b75ff", "#120d31ff"]
colors_lat = ["#c33b75ff","#c33b75ff", "#120d31ff", "#120d31ff"]


for tw in ['early', 'late']:
    erp.diff_plot(plot_folder, 'VAN_diff_att_' + tw , erp_labels_att, temp_roi, plot_time_wind=True,
                  time_wind = time_windows[tw], colors = colors_centr, legend=[''], legend_loc = legend_loc, 
                  fig_size = fig_size, ylim = ylim, y_ticks = y_ticks, xlim = xlim, x_ticks = x_ticks, save_format = 'png')
    erp.diff_plot(plot_folder, 'VAN_diff_unatt_' + tw , erp_labels_unatt, temp_roi, plot_time_wind=True,
                  time_wind = time_windows[tw], colors = colors_centr, legend=[''], legend_loc = legend_loc, 
                  fig_size = fig_size, ylim = ylim, y_ticks = y_ticks, xlim = xlim, x_ticks = x_ticks, save_format = 'png')
    
    
    
    erp_lat.lat_diff_plot (plot_folder, 'VAN_diff_lat_att_' + tw, erp_labels_left_att, erp_labels_right_att, left_roi, right_roi, 
                   plot_time_wind = True, time_wind = time_windows[tw], colors = colors_lat, styles = styles, legend=[''], 
                   legend_loc=legend_loc, fig_size = fig_size, ylim = ylim, y_ticks = y_ticks,  xlim = xlim, x_ticks = x_ticks, 
                   save_format = 'png')
    erp_lat.lat_diff_plot (plot_folder, 'VAN_diff_lat_unattl_' + tw, erp_labels_left_unatt, erp_labels_right_unatt, left_roi, right_roi, 
                   plot_time_wind = True, time_wind = time_windows[tw], colors = colors_lat, styles = styles, legend=[''], 
                   legend_loc=legend_loc, fig_size = fig_size, ylim = ylim, y_ticks = y_ticks,  xlim = xlim, x_ticks = x_ticks, 
                   save_format = 'png')




# differential topoplots
contrast = {'masking':{'unmasked':['unmasked'], 'masked':['masked']}}
erp_labels = markers.erp_labels(contrast = contrast)
erp.diff_topo(plot_folder, 'diff_masking', erp_labels, 0.07, 0.38, time_step=0.05, volt_min =-6, volt_max = 6, 
              cmap='magma', save_format='svg')

contrast = {'att_cond': {'attended': ['attended'], 'unattended': ['unattended']}}
erp_labels = markers.erp_labels(contrast = contrast)
erp.diff_topo(plot_folder, 'diff_task', erp_labels, 0.07, 0.38, time_step=0.05, volt_min = -1.5, volt_max = 1.5, 
              cmap='magma', save_format='svg')



contrast = {'stimulus': {'target':['target'], 'distractor':['distractor']}}
erp_labels = markers.erp_labels(contrast = contrast)
erp.diff_topo(plot_folder, 'diff_task', erp_labels, 0.07, 0.38, time_step=0.05, volt_min = -1.5, volt_max = 1.5, 
              cmap='magma', save_format='svg')

#%% MIXED MODELS
temp_roi = ['P7', 'P8', 'PO7', 'PO8', 'P9', 'P10']
left_roi =  ['P7', 'P9', 'PO7']
right_roi = ['P8', 'P10', 'PO8']
time_windows = {'early': [140, 190], 'late': [190, 285]}


reduce_markers = markers.reduce_markers()
evoked_labels_reduced = markers.evoked_labels_reduced()
epochs_data = my.comps_long.Trials_data(subjects, path, epochs_clean_folder, reduce_markers, evoked_labels = evoked_labels_reduced)

conditions = {'att_cond':{'attended':['attended'], 'unattended':['unattended']}, 'masking':{'masked':['masked'], 'unmasked':['unmasked']}, 
              'stimulus':{'catch':['catch'], 'target':['target'], 'distractor':['distractor']}}


mixed_labels = markers.mixed_models_labels(conditions)

for tw in ['early', 'late']:
     epochs_data.get_central_comp(mixed_models_folder, 'VAN_' + tw, mixed_labels, temp_roi, time_windows[tw])



evoked_labels = markers.evoked_labels()
epochs_data = my.comps_long.Trials_data(subjects, path, epochs_clean_folder, evoked_labels = evoked_labels)
conditions_left = {'att_cond':{'attended':['attended'], 'unattended':['unattended']}, 'masking':{'masked':['masked'], 'unmasked':['unmasked']}, 
                   'stimulus':{'catch':['catch'], 'target':['target'], 'distractor':['distractor']}, 'side':{'left':['left']}}
conditions_right = {'att_cond':{'attended':['attended'], 'unattended':['unattended']}, 'masking':{'masked':['masked'], 'unmasked':['unmasked']}, 
                   'stimulus':{'catch':['catch'], 'target':['target'], 'distractor':['distractor']}, 'side':{'right':['right']}}
long_labels_left = markers.mixed_models_labels(conditions_left, reduced = False)
long_labels_right = markers.mixed_models_labels(conditions_right, reduced = False)

for tw in ['early', 'late']:
    epochs_data.get_lateral_comp(mixed_models_folder, 'VAN_lat_' + tw, long_labels_left, long_labels_right, left_roi, right_roi, time_windows[tw])