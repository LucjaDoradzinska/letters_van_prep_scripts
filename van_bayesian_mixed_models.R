###################### pas VAN early ###################### 
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
library(parallel)
options(mc.cores = parallel::detectCores())
source("E:\\BM_functions\\factors.r")

#################### load data
lat_ev_data <- read_excel("D:\\letters_van\\Results\\pas\\EEG\\long_comps\\VAN_lat_early_amps_long_format.xlsx")
lat_ev_data = transform(lat_ev_data, hemisphere =factor(side_, levels = c('ipsi', 'contra')), att_cond =factor(att_cond), 
                        masking=factor(masking), stimulus = factor(stimulus), subject = factor(subject))
lat_ev_data <-filter(lat_ev_data, hemisphere == 'contra')

#filtering out outliers
outliers <- filter(lat_ev_data, abs(scale(erp_amp)) > 3)
lat_ev_data = filter(lat_ev_data, abs(scale(erp_amp)) <= 3)

control_data <- filter(lat_ev_data, masking == 'masked')

lat_ev_data <-filter(lat_ev_data, stimulus != 'catch')
lat_ev_data =transform(lat_ev_data, stimulus = factor(stimulus, levels = c('distractor', 'target')))

#################### lat ev models
formulas = get_all_combs(factors = list("att_cond", "masking", "stimulus"),
                         outcome = "erp_amp", random = "(1 + att_cond*masking*stimulus | subject)")

lat_early_van_models <- list()
lat_early_van_loos <- list()
for (f in formulas){
  if (f == formulas[[1]]){
    model<- brm(formula = bf(f), data = lat_ev_data ,family = gaussian(link = 'identity'), 
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
    sd_erp<-summary(model)$spec_pars$Estimate
    
  } else{
    model<- brm(formula = bf(f), data = lat_ev_data ,family = gaussian(link = 'identity'), 
                set_prior(paste("normal(0,", 10*sd_erp, ")", sep = ""), class = "b"),
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
  }
  
  lat_early_van_models <- c(lat_early_van_models, list(model))
}

names(lat_early_van_models) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_early_bayesian_models.RData")

###########################loos
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
options(mc.cores = parallel::detectCores())

source("E:\\BM_functions\\factors.r")

load("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_early_bayesian_models.RData")
for (model in lat_early_van_models){
  lat_early_van_loos <-  c(lat_early_van_loos, list(loo(model, cores = 2)))
}

names(lat_early_van_loos) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_early_bayesian_models.RData")

#################### control models
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
options(mc.cores = parallel::detectCores())

source("E:\\BM_functions\\factors.r")

load("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_early_bayesian_models.RData")

formulas = get_all_combs(factors = list("att_cond", "stimulus"),
                         outcome = "erp_amp", random = "(1 + att_cond*stimulus | subject)")

control_models <- list()
control_loos <- list()
for (f in formulas){
  if (f == formulas[[1]]){
    model<- brm(formula = bf(f), data = control_data ,family = gaussian(link = 'identity'), 
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
    sd_erp<-summary(model)$spec_pars$Estimate
    
  } else{
    model<- brm(formula = bf(f), data = control_data ,family = gaussian(link = 'identity'), 
                set_prior(paste("normal(0,", 10*sd_erp, ")", sep = ""), class = "b"),
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
  }
  
  control_models <- c(control_models, list(model))
}

names(control_models) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_early_bayesian_models.RData")

###########################loos
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
options(mc.cores = parallel::detectCores())

source("E:\\BM_functions\\factors.r")

load("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_early_bayesian_models.RData")
for (model in control_models){
  control_loos <-  c(control_loos, list(loo(model, cores = 2)))
}

names(control_loos) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_early_bayesian_models.RData")




###################### pas VAN late ###################### 
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
library(parallel)
options(mc.cores = parallel::detectCores())
source("E:\\BM_functions\\factors.r")

#################### load data
lat_lv_data <- read_excel("D:\\letters_van\\Results\\pas\\EEG\\long_comps\\VAN_lat_late_amps_long_format.xlsx")
lat_lv_data = transform(lat_lv_data, hemisphere =factor(side_, levels = c('ipsi', 'contra')), att_cond =factor(att_cond), 
                        masking=factor(masking), stimulus = factor(stimulus), subject = factor(subject))
lat_lv_data <-filter(lat_lv_data, hemisphere == 'contra')

#filtering out outliers
outliers <- filter(lat_lv_data, abs(scale(erp_amp)) > 3)
lat_lv_data = filter(lat_lv_data, abs(scale(erp_amp)) <= 3)

control_data <- filter(lat_lv_data, masking == 'masked')


lat_lv_data <-filter(lat_lv_data, stimulus != 'catch')
lat_lv_data =transform(lat_lv_data, stimulus = factor(stimulus, levels = c('distractor', 'target')))

#################### lat lv models
formulas = get_all_combs(factors = list("att_cond", "masking", "stimulus"),
                         outcome = "erp_amp", random = "(1 + att_cond*masking*stimulus | subject)")

lat_late_van_models <- list()
lat_late_van_loos <- list()
for (f in formulas){
  if (f == formulas[[1]]){
    model<- brm(formula = bf(f), data = lat_lv_data ,family = gaussian(link = 'identity'), 
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
    sd_erp<-summary(model)$spec_pars$Estimate
    
  } else{
    model<- brm(formula = bf(f), data = lat_lv_data ,family = gaussian(link = 'identity'), 
                set_prior(paste("normal(0,", 10*sd_erp, ")", sep = ""), class = "b"),
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
  }
  
  lat_late_van_models <- c(lat_late_van_models, list(model))
}

names(lat_late_van_models) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_late_bayesian_models.RData")

###########################loos
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
options(mc.cores = parallel::detectCores())

source("E:\\BM_functions\\factors.r")

load("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_late_bayesian_models.RData")
for (model in lat_late_van_models){
  lat_late_van_loos <-  c(lat_late_van_loos, list(loo(model, cores = 2)))
}

names(lat_late_van_loos) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_late_bayesian_models.RData")


#################### control models
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
options(mc.cores = parallel::detectCores())

source("E:\\BM_functions\\factors.r")

load("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_late_bayesian_models.RData")

formulas = get_all_combs(factors = list("att_cond", "stimulus"),
                         outcome = "erp_amp", random = "(1 + att_cond*stimulus | subject)")

control_models <- list()
control_loos <- list()
for (f in formulas){
  if (f == formulas[[1]]){
    model<- brm(formula = bf(f), data = control_data ,family = gaussian(link = 'identity'), 
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
    sd_erp<-summary(model)$spec_pars$Estimate
    
  } else{
    model<- brm(formula = bf(f), data = control_data ,family = gaussian(link = 'identity'), 
                set_prior(paste("normal(0,", 10*sd_erp, ")", sep = ""), class = "b"),
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
  }
  
  control_models <- c(control_models, list(model))
}

names(control_models) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_late_bayesian_models.RData")

###########################loos
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
options(mc.cores = parallel::detectCores())

source("E:\\BM_functions\\factors.r")

load("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_late_bayesian_models.RData")
for (model in control_models){
  control_loos <-  c(control_loos, list(loo(model, cores = 2)))
}

names(control_loos) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\pas\\EEG\\models\\van_lat_late_bayesian_models.RData")

###################### nopas VAN early ###################### 
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
library(parallel)
options(mc.cores = parallel::detectCores())
source("E:\\BM_functions\\factors.r")

#################### load data
lat_ev_data <- read_excel("D:\\letters_van\\Results\\nopas\\EEG\\long_comps\\VAN_lat_early_amps_long_format.xlsx")
lat_ev_data = transform(lat_ev_data, hemisphere =factor(side_, levels = c('ipsi', 'contra')), att_cond =factor(att_cond), 
                        masking=factor(masking), stimulus = factor(stimulus), subject = factor(subject))
lat_ev_data <-filter(lat_ev_data, hemisphere == 'contra')

#filtering out outliers
outliers <- filter(lat_ev_data, abs(scale(erp_amp)) > 3)
lat_ev_data = filter(lat_ev_data, abs(scale(erp_amp)) <= 3)


#################### lat ev models
formulas = get_all_combs(factors = list("att_cond", "masking", "stimulus"),
                         outcome = "erp_amp", random = "(1 + att_cond*masking*stimulus | subject)")

lat_early_van_models <- list()
lat_early_van_loos <- list()
for (f in formulas){
  if (f == formulas[[1]]){
    model<- brm(formula = bf(f), data = lat_ev_data ,family = gaussian(link = 'identity'), 
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
    sd_erp<-summary(model)$spec_pars$Estimate
    
  } else{
    model<- brm(formula = bf(f), data = lat_ev_data ,family = gaussian(link = 'identity'), 
                set_prior(paste("normal(0,", 10*sd_erp, ")", sep = ""), class = "b"),
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
  }
  
  lat_early_van_models <- c(lat_early_van_models, list(model))
}

names(lat_early_van_models) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\nopas\\EEG\\models\\van_lat_early_bayesian_models.RData")

###########################loos
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
options(mc.cores = parallel::detectCores())

source("E:\\BM_functions\\factors.r")

load("D:\\letters_van\\Results\\nopas\\EEG\\models\\van_lat_early_bayesian_models.RData")
for (model in lat_early_van_models){
  lat_early_van_loos <-  c(lat_early_van_loos, list(loo(model, cores = 2)))
}

names(lat_early_van_loos) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\nopas\\EEG\\models\\van_lat_early_bayesian_models.RData")


###################### letters nopas VAN late ###################### 
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
library(parallel)
options(mc.cores = parallel::detectCores())
source("E:\\BM_functions\\factors.r")

#################### load data
lat_lv_data <- read_excel("D:\\letters_van\\Results\\nopas\\EEG\\long_comps\\VAN_lat_late_amps_long_format.xlsx")
lat_lv_data = transform(lat_lv_data, hemisphere =factor(side_, levels = c('ipsi', 'contra')), att_cond =factor(att_cond), 
                        masking=factor(masking), stimulus = factor(stimulus), subject = factor(subject))
lat_lv_data <-filter(lat_lv_data, hemisphere == 'contra')

#filtering out outliers
outliers <- filter(lat_lv_data, abs(scale(erp_amp)) > 3)
lat_lv_data = filter(lat_lv_data, abs(scale(erp_amp)) <= 3)

#################### lat ev models
formulas = get_all_combs(factors = list("att_cond", "masking", "stimulus"),
                         outcome = "erp_amp", random = "(1 + att_cond*masking*stimulus | subject)")

lat_late_van_models <- list()
lat_late_van_loos <- list()
for (f in formulas){
  if (f == formulas[[1]]){
    model<- brm(formula = bf(f), data = lat_lv_data ,family = gaussian(link = 'identity'), 
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
    sd_erp<-summary(model)$spec_pars$Estimate
    
  } else{
    model<- brm(formula = bf(f), data = lat_lv_data ,family = gaussian(link = 'identity'), 
                set_prior(paste("normal(0,", 10*sd_erp, ")", sep = ""), class = "b"),
                sample_prior = "yes", chains = 2, iter = 8000, cores = 2, warmup = 4000)
  }
  
  lat_late_van_models <- c(lat_late_van_models, list(model))
}

names(lat_late_van_models) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\nopas\\EEG\\models\\van_lat_late_bayesian_models.RData")

###########################loos
rm(list=ls())

library(brms)
library(readxl)
library(tidyverse)
library(loo)
options(mc.cores = parallel::detectCores())

source("E:\\BM_functions\\factors.r")

load("D:\\letters_van\\Results\\nopas\\EEG\\models\\van_lat_late_bayesian_models.RData")
for (model in lat_late_van_models){
  lat_late_van_loos <-  c(lat_late_van_loos, list(loo(model, cores = 2)))
}

names(lat_late_van_loos) <- as.character(formulas)
save.image("D:\\letters_van\\Results\\nopas\\EEG\\models\\van_lat_late_bayesian_models.RData")
