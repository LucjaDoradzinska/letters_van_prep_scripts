###################### pas early VAN evaluation ######################
rm(list=ls())

library(brms)
library(tidyverse)
library(loo)

load("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_early_bayesian_models.RData")

loo_comp <- as.data.frame(loo_compare(lat_early_van_loos))
loo_comp$SEs <- abs(loo_comp$elpd_diff / loo_comp$se_diff)

winning_model<-lat_early_van_models["erp_amp ~ 1 + att_cond * masking * stimulus + (1 + att_cond * masking * stimulus | subject)"][[1]]

summary(winning_model)
ce <-conditional_effects(winning_model, effect = 'masking', conditions = make_conditions(lat_ev_data, vars = c('att_cond', 'stimulus')))
ce_dt <- as.data.frame(ce[['masking']])
ce


hypotheses <- c("maskingunmasked + att_condunattended:maskingunmasked < 0",
                "maskingunmasked + att_condunattended:maskingunmasked + maskingunmasked:stimulustarget + att_condunattended:maskingunmasked:stimulustarget < 0",
                "maskingunmasked < 0","maskingunmasked + maskingunmasked:stimulustarget   < 0",
                
                "maskingunmasked:stimulustarget + att_condunattended:maskingunmasked:stimulustarget < 0", "maskingunmasked:stimulustarget < 0", 
                "att_condunattended:maskingunmasked > 0", "att_condunattended:maskingunmasked + att_condunattended:maskingunmasked:stimulustarget > 0",
                
                "maskingunmasked:stimulustarget + att_condunattended:maskingunmasked:stimulustarget = 0", 
                "maskingunmasked:stimulustarget = 0",
                "att_condunattended:maskingunmasked = 0",
                
                "stimulustarget + att_condunattended:stimulustarget < 0",
                "stimulustarget + maskingunmasked:stimulustarget + att_condunattended:stimulustarget + att_condunattended:maskingunmasked:stimulustarget < 0",
                "stimulustarget < 0", "stimulustarget + maskingunmasked:stimulustarget < 0", 
                
                "stimulustarget + att_condunattended:stimulustarget = 0",
                "stimulustarget + maskingunmasked:stimulustarget + att_condunattended:stimulustarget + att_condunattended:maskingunmasked:stimulustarget = 0",
                "stimulustarget = 0", "stimulustarget + maskingunmasked:stimulustarget = 0",
                
                "att_condunattended > 0", "att_condunattended + att_condunattended:stimulustarget > 0",
                "att_condunattended + att_condunattended:maskingunmasked > 0",
                "att_condunattended + att_condunattended:maskingunmasked + att_condunattended:stimulustarget + att_condunattended:maskingunmasked:stimulustarget > 0",
                
                "att_condunattended = 0", "att_condunattended + att_condunattended:stimulustarget < 0",
                "att_condunattended + att_condunattended:maskingunmasked = 0",
                "att_condunattended + att_condunattended:maskingunmasked + att_condunattended:stimulustarget + att_condunattended:maskingunmasked:stimulustarget = 0")

hypothesis(winning_model, hypotheses)

save.image("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_early_bayesian_models.RData")

###################### pas late VAN evaluation ######################
rm(list=ls())

library(brms)
library(tidyverse)
library(loo)

load("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_late_bayesian_models.RData")

loo_comp <- as.data.frame(loo_compare(lat_late_van_loos))
loo_comp$SEs <- abs(loo_comp$elpd_diff / loo_comp$se_diff)

winning_model<-lat_late_van_models["erp_amp ~ 1 + att_cond * masking + att_cond * stimulus + masking * stimulus + (1 + att_cond * masking * stimulus | subject)"][[1]]

summary(winning_model)
ce <-conditional_effects(winning_model, effect = 'masking', conditions = make_conditions(lat_lv_data, vars = c('att_cond', 'stimulus')))
ce_dt <- as.data.frame(ce[['masking']])
ce


hypotheses <- c("maskingunmasked + att_condunattended:maskingunmasked < 0",
                "maskingunmasked + att_condunattended:maskingunmasked + maskingunmasked:stimulustarget < 0",
                "maskingunmasked < 0","maskingunmasked + maskingunmasked:stimulustarget   < 0",
                
                "maskingunmasked:stimulustarget < 0", 
                "att_condunattended:maskingunmasked > 0",
                
                "maskingunmasked:stimulustarget = 0",
                "att_condunattended:maskingunmasked = 0",
                
                "stimulustarget + att_condunattended:stimulustarget < 0",
                "stimulustarget + maskingunmasked:stimulustarget + att_condunattended:stimulustarget < 0",
                "stimulustarget < 0", "stimulustarget + maskingunmasked:stimulustarget < 0", 
                
                "stimulustarget + att_condunattended:stimulustarget > 0",
                "stimulustarget + maskingunmasked:stimulustarget + att_condunattended:stimulustarget = 0",
                "stimulustarget > 0", "stimulustarget + maskingunmasked:stimulustarget = 0",
                
                "att_condunattended > 0", "att_condunattended + att_condunattended:stimulustarget > 0",
                "att_condunattended + att_condunattended:maskingunmasked > 0",
                "att_condunattended + att_condunattended:maskingunmasked + att_condunattended:stimulustarget > 0",
                
                "att_condunattended = 0", "att_condunattended + att_condunattended:stimulustarget < 0",
                "att_condunattended + att_condunattended:maskingunmasked = 0",
                "att_condunattended + att_condunattended:maskingunmasked + att_condunattended:stimulustarget = 0")

hypothesis(winning_model, hypotheses)

save.image("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_late_bayesian_models.RData")


###################### nopas early VAN evaluation ######################
rm(list=ls())

library(brms)
library(tidyverse)
library(loo)

load("D:\\letters_van\\Results\\nopas\\EEG\\models\\van_lat_early_bayesian_models.RData")

loo_comp <- as.data.frame(loo_compare(lat_early_van_loos))
loo_comp$SEs <- abs(loo_comp$elpd_diff / loo_comp$se_diff)

winning_model<-lat_early_van_models["erp_amp ~ 1 + att_cond * masking * stimulus + (1 + att_cond * masking * stimulus | subject)"][[1]]

summary(winning_model)
ce <-conditional_effects(winning_model, effect = 'masking', conditions = make_conditions(lat_ev_data, vars = c('att_cond', 'stimulus')))
ce_dt <- as.data.frame(ce[['masking']])
ce


hypotheses <- c("maskingunmasked + att_condunatt:maskingunmasked < 0",
                "maskingunmasked + att_condunatt:maskingunmasked + maskingunmasked:stimulustarg + att_condunatt:maskingunmasked:stimulustarg < 0",
                "maskingunmasked < 0","maskingunmasked + maskingunmasked:stimulustarg   < 0",
                
                "maskingunmasked + att_condunatt:maskingunmasked = 0",
                
                "maskingunmasked:stimulustarg + att_condunatt:maskingunmasked:stimulustarg < 0", "maskingunmasked:stimulustarg < 0", 
                "att_condunatt:maskingunmasked > 0", "att_condunatt:maskingunmasked + att_condunatt:maskingunmasked:stimulustarg > 0",
                
                "maskingunmasked:stimulustarg + att_condunatt:maskingunmasked:stimulustarg = 0", 
                
                "stimulustarg + att_condunatt:stimulustarg < 0",
                "stimulustarg + maskingunmasked:stimulustarg + att_condunatt:stimulustarg + att_condunatt:maskingunmasked:stimulustarg < 0",
                "stimulustarg < 0", "stimulustarg + maskingunmasked:stimulustarg < 0", 
                
                "stimulustarg + att_condunatt:stimulustarg = 0",
                "stimulustarg + maskingunmasked:stimulustarg + att_condunatt:stimulustarg + att_condunatt:maskingunmasked:stimulustarg = 0",
                "stimulustarg = 0", 
                
                "att_condunatt > 0", "att_condunatt + att_condunatt:stimulustarg > 0",
                "att_condunatt + att_condunatt:maskingunmasked > 0",
                "att_condunatt + att_condunatt:maskingunmasked + att_condunatt:stimulustarg + att_condunatt:maskingunmasked:stimulustarg > 0",
                
                "att_condunatt = 0", "att_condunatt + att_condunatt:stimulustarg = 0")

hypothesis(winning_model, hypotheses)

save.image("D:\\letters_van\\Results\\nopas\\EEG\\models\\van_lat_early_bayesian_models.RData")


###################### nopas late VAN evaluation ######################
rm(list=ls())

library(brms)
library(tidyverse)
library(loo)

load("D:\\letters_van\\Results\\nopas\\EEG\\models\\van_lat_late_bayesian_models.RData")

loo_comp <- as.data.frame(loo_compare(lat_late_van_loos))
loo_comp$SEs <- abs(loo_comp$elpd_diff / loo_comp$se_diff)

winning_model<-lat_late_van_models["erp_amp ~ 1 + att_cond * masking * stimulus + (1 + att_cond * masking * stimulus | subject)"][[1]]

summary(winning_model)
ce <-conditional_effects(winning_model, effect = 'masking', conditions = make_conditions(lat_lv_data, vars = c('att_cond', 'stimulus')))
ce_dt <- as.data.frame(ce[['masking']])
ce


hypotheses <- c("maskingunmasked + att_condunatt:maskingunmasked < 0",
                "maskingunmasked + att_condunatt:maskingunmasked + maskingunmasked:stimulustarg + att_condunatt:maskingunmasked:stimulustarg < 0",
                "maskingunmasked < 0","maskingunmasked + maskingunmasked:stimulustarg   < 0",
                
                
                "maskingunmasked:stimulustarg + att_condunatt:maskingunmasked:stimulustarg < 0", "maskingunmasked:stimulustarg < 0", 
                "att_condunatt:maskingunmasked > 0", "att_condunatt:maskingunmasked + att_condunatt:maskingunmasked:stimulustarg > 0",
                
                "maskingunmasked:stimulustarg + att_condunatt:maskingunmasked:stimulustarg = 0", 
                
                "stimulustarg + att_condunatt:stimulustarg < 0",
                "stimulustarg + maskingunmasked:stimulustarg + att_condunatt:stimulustarg + att_condunatt:maskingunmasked:stimulustarg < 0",
                "stimulustarg < 0", "stimulustarg + maskingunmasked:stimulustarg < 0", 
                
                "stimulustarg + att_condunatt:stimulustarg = 0",
                "stimulustarg = 0", 
                
                "att_condunatt > 0", "att_condunatt + att_condunatt:stimulustarg > 0",
                "att_condunatt + att_condunatt:maskingunmasked > 0",
                "att_condunatt + att_condunatt:maskingunmasked + att_condunatt:stimulustarg + att_condunatt:maskingunmasked:stimulustarg > 0",
                
                "att_condunatt < 0", "att_condunatt + att_condunatt:stimulustarg < 0",
                "att_condunatt + att_condunatt:maskingunmasked = 0")


hypothesis(winning_model, hypotheses)

save.image("D:\\letters_van\\Results\\nopas\\EEG\\models\\van_lat_late_bayesian_models.RData")

