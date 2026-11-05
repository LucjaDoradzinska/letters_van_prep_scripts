# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 15:47:31 2022

@author: ldoradzinska
"""

from collections import OrderedDict 

"""
####################### FUNCTIONS #######################
"""

def get_beh_factors(beh_stim_coding, new_conditions = {}):
    
    factors = list(beh_stim_coding.keys())
    factors.extend(list(new_conditions.keys()))
    return factors

"""
#######################
"""

def get_stim_conditions(beh_stim_coding, new_conditions = {}):
    
    stim_conditions = OrderedDict()
    stim_conditions[''] = {}
    stim_cond_holder = OrderedDict()
    
    for factor in beh_stim_coding:
        for label in stim_conditions:
            for cond in beh_stim_coding[factor]:
                if label == '':
                    new_label = beh_stim_coding[factor][cond]
                else:
                    new_label = label + '_' + beh_stim_coding[factor][cond]
                stim_cond_holder[new_label] = stim_conditions[label].copy()
                stim_cond_holder[new_label][factor] = cond
        
        stim_conditions = stim_cond_holder
        stim_cond_holder = OrderedDict()
    
    for label in stim_conditions:
        for contr in new_conditions:
            for cond in new_conditions[contr]:
                for case in new_conditions[contr][cond]:
                    if all([case[cond] == stim_conditions[label][cond] for cond in case]):
                        stim_conditions[label][contr] = cond
    
    return stim_conditions

"""
#######################
"""

def beh_combine_conds(beh_combine):
    
    beh_compare = OrderedDict()
    beh_compare[''] = {}
    lab_holder = OrderedDict()
    
    for factor in beh_combine:
        for label in beh_compare:
            for cond in beh_combine[factor]:
                if label =='':
                    new_lab = cond
                else:
                    new_lab = label + '_' + cond
                lab_holder[new_lab] = beh_compare[label].copy()
                lab_holder[new_lab][factor] = cond
        
        beh_compare = lab_holder
        lab_holder = OrderedDict()

    return beh_compare




"""
#######################
"""   
class Eeg_markers_manager:
    
    def __init__(self, eeg_codings, reduce_factors = {}):
        self.stim_codings = eeg_codings
        self.reduce_factors = reduce_factors
    
    
    
    def get_markers(self):
    
        eeg_markers = {}
        
        for stim_coding in self.stim_codings:
            stim_markers = {'':0}
            lab_holder = {}
            
            for factor in stim_coding:
                for cond in stim_coding[factor]:
                    for lab in stim_markers:
                        if lab == '':
                            key = cond
                        else:   
                            key = lab + '_' + cond
                        lab_holder[key] = stim_markers[lab] + stim_coding[factor][cond]
                
                stim_markers = lab_holder
                lab_holder = {}
                
            eeg_markers.update(stim_markers)
            
        
        return eeg_markers
       

    def reduce_markers(self, erp_marker_shift = 300):
        
        reduce_markers = []
        
        for stim_coding in self.stim_codings:
            reduce_markers_holder = [{'new_label':'', 'new_marker':erp_marker_shift, 'old_labels':['']}]
            lab_holder = []
            
            for factor in stim_coding:
                if factor in self.reduce_factors:
                    for marker in reduce_markers_holder:
                        
                        if marker['old_labels'] == ['']:
                            old_labels = [cond for cond in stim_coding[factor]]
                        else:
                            old_labels = [lab + '_' + cond for lab in marker['old_labels']for cond in stim_coding[factor]]
                        
                        lab_holder.append({'new_label':marker['new_label'], 'new_marker':marker['new_marker'], 
                                           'old_labels':old_labels})
                
                else:
                    for marker in reduce_markers_holder:
                        
                        for cond in stim_coding[factor]:#self.stim_coding[factor]:
                            if marker['new_label'] == '':
                                label = cond
                            else:
                                label = marker['new_label'] + '_' + cond
                            
                            if marker['old_labels'] == ['']:
                                old_labels = [cond]
                            else:
                                old_labels = [lab + '_' + cond for lab in marker['old_labels']]
        
                            
                            lab_holder.append({'new_label':label, 'new_marker':marker['new_marker'] + stim_coding[factor][cond],
                                              'old_labels':old_labels})
                
                reduce_markers_holder = lab_holder
                lab_holder = []
            
            reduce_markers.extend(reduce_markers_holder)         
        
        return reduce_markers
    
    
    
    def evoked_labels(self, equalize_within = {}):
        
        evoked_labels = []
       
        for stim_coding in self.stim_codings:
            evoked_labels_holder = [['']]
            lab_holder = []
            for factor in stim_coding:
                    
                if factor in equalize_within:
                    for group in evoked_labels_holder:
                        if group == ['']:
                            for contr in equalize_within[factor]:
                                lab_holder.append([])
                                for lab in contr:
                                    if lab in stim_coding[factor]:
                                        lab_holder[-1].append(lab)
                        else:
                            for contr in equalize_within[factor]:
                                lab_holder.append([])
                                for lab in contr:
                                    if lab in stim_coding[factor]:
                                        for old_lab in group:
                                            lab_holder[-1].append(old_lab + '_' + lab)
                
                else:
                     for group in evoked_labels_holder:
                        if group == ['']:
                            lab_holder.append([lab for lab in stim_coding[factor]])
                        else:
                            lab_holder.append([old_lab + '_' + lab for old_lab in group for lab in stim_coding[factor]])
             
                
                evoked_labels_holder = lab_holder     
                lab_holder = [] 
            
            if evoked_labels == []:
                evoked_labels = evoked_labels_holder.copy()
            else:
                for i in range(len(evoked_labels)):
                    evoked_labels[i].extend(evoked_labels_holder[i]) 
                    
        return evoked_labels
     


    
    def evoked_labels_reduced(self, equalize_within = {}):
        
        evoked_labels = []
       
        for stim_coding in self.stim_codings:
            evoked_labels_holder = [['']]
            lab_holder = []
            for factor in stim_coding:
                    
                if factor in equalize_within:
                    for group in evoked_labels_holder:
                        if group == ['']:
                            for contr in equalize_within[factor]:
                                lab_holder.append([])
                                for lab in contr:
                                    if lab in stim_coding[factor]:
                                        lab_holder[-1].append(lab)
                        else:
                            for contr in equalize_within[factor]:
                                lab_holder.append([])
                                for lab in contr:
                                    if lab in stim_coding[factor]:
                                        for old_lab in group:
                                            lab_holder[-1].append(old_lab + '_' + lab)
                
                elif factor not in self.reduce_factors:
                     for group in evoked_labels_holder:
                        if group == ['']:
                            lab_holder.append([lab for lab in stim_coding[factor]])
                        else:
                            lab_holder.append([old_lab + '_' + lab for old_lab in group for lab in stim_coding[factor]])
             
                
                if factor not in self.reduce_factors:
                    evoked_labels_holder = lab_holder     
                    lab_holder = [] 
            
            if evoked_labels == []:
                evoked_labels = evoked_labels_holder.copy()
            else:
                for i in range(len(evoked_labels)):
                    evoked_labels[i].extend(evoked_labels_holder[i]) 
                    
        return evoked_labels           
    
    
    
    
    
    
    def erp_labels(self, comp_by = {}, contrast = {}, reduced = True):
        
        erp_labels = OrderedDict()
        
        for stim_coding in self.stim_codings:
            erp_labels_holder = OrderedDict()
            erp_labels_holder[''] = {'':['']}
            lab_holder = OrderedDict()
            
            for factor in stim_coding:
                    
                if factor in comp_by:
                    
                    for label in erp_labels_holder:
                        for cond in comp_by[factor]:
                            if comp_by[factor][cond] in list(stim_coding[factor].keys()):
                                if label == '':
                                    new_label = cond
                                elif cond == '':
                                    new_label = label
                                else:
                                    new_label = label + '_' + cond
                                
                                lab_holder[new_label] = {}
                                
                                for contr in erp_labels_holder[label]:
                                    if erp_labels_holder[label][contr] == ['']:
                                        lab_holder[new_label][contr] = [comp_by[factor][cond]]
                                    else:
                                        lab_holder[new_label][contr] = [lab + '_' + comp_by[factor][cond] for lab in erp_labels_holder[label][contr]]
                        
                elif factor in contrast:
                    
                    for label in erp_labels_holder:
                        lab_holder[label] = {}
                        
                        for contr in erp_labels_holder[label]:
                            
                            for contr_lab in contrast[factor]:
                                if any(cond in stim_coding[factor].keys() for cond in contrast[factor][contr_lab]):
                                    if contr == '':
                                        new_lab = contr_lab
                                    elif contr_lab == '':
                                        new_lab = contr
                                    else:
                                        new_lab = contr + '_' + contr_lab
                                    
                                    lab_holder[label][new_lab] = []
                                    if erp_labels_holder[label][contr] == ['']:
                                        for cond in contrast[factor][contr_lab]:
                                            if cond in stim_coding[factor].keys():
                                                lab_holder[label][new_lab].append(cond)
                                    else:
                                        for cond in contrast[factor][contr_lab]:
                                            if cond in stim_coding[factor].keys():
                                                lab_holder[label][new_lab].extend([lab + '_' + cond for lab in erp_labels_holder[label][contr]])
                                    
                                   
                elif not reduced or factor not in self.reduce_factors:
                    for label in erp_labels_holder:
                        lab_holder[label] = {}
                        
                        for contr in erp_labels_holder[label]:
                            if erp_labels_holder[label][contr] == ['']:
                                lab_holder[label][contr] = [cond for cond in stim_coding[factor]]
                            else:
                                lab_holder[label][contr] = [lab + '_' + cond for lab in erp_labels_holder[label][contr] 
                                                             for cond in stim_coding[factor]]            
                            
                            
                if not reduced or factor not in self.reduce_factors:
                    erp_labels_holder = lab_holder.copy()
                
                lab_holder = OrderedDict()  
            
            if erp_labels == {}:
                erp_labels = erp_labels_holder.copy()
            
            else:
                for label in erp_labels_holder:
                    if label in erp_labels.keys():
                        for contr in erp_labels_holder[label]:
                            if contr in erp_labels[label].keys():
                                erp_labels[label][contr].extend(erp_labels_holder[label][contr])
                            else:
                                erp_labels[label][contr] = erp_labels_holder[label][contr].copy()
                    else:
                        erp_labels[label] = erp_labels_holder[label].copy()
            
        return erp_labels         
    


           
    def mixed_models_labels(self, conditions = {}, reduced = True):
        
        mixed_labels = [{'labels':[], 'conds':{}}]
        
        
        stim_coding = self.stim_codings[0]
        lab_holder = []
        for factor in stim_coding:
            if factor in conditions:
                for label in mixed_labels:
                    for cond in conditions[factor]:
                        if label['labels'] == []:
                            new_labels = conditions[factor][cond]
                        else:
                            new_labels = [lab + '_' + l for lab in label['labels'] for l in conditions[factor][cond]]
                        
                        new_conds = label['conds'].copy()
                        new_conds[factor] = cond
                        lab_holder.append({'labels':new_labels, 'conds' : new_conds})
                        
            elif not reduced or factor not in self.reduce_factors:
                for label in mixed_labels:
                    if label['labels'] == []:
                        new_labels = [cond for cond in stim_coding[factor]]
                    else:
                        new_labels = [lab + '_' + cond for lab in label['labels']for cond in stim_coding[factor]]
                    
                    lab_holder.append({'labels':new_labels, 'conds' : label['conds']})
                
            if not reduced or factor not in self.reduce_factors:
                mixed_labels = lab_holder.copy()
            lab_holder = []
        
        return mixed_labels
    
    