rm(list=ls())

library(readxl)
library(tidyverse)
library(rstanarm)

library(patchwork)
########################## DATA CURATION ######################################

data_survey <- read_excel("D:\\letters_van\\Results\\nopas\\pas\\pas_logs\\survey_log.xlsx")


data_pas = data.frame(subjects=character(0),side=character(0),resp=numeric(0))

for (i in 1:nrow(data_survey)){
  row = data_survey[i,]
  resp_att = row[["Jak dobrze widziałeś/aś litery pojawiające się po attended stronie?"]]
  resp_unatt = row[["Jak dobrze widziałeś/aś litery pojawiające się po unattended stronie?"]]
  
  if (resp_att =="Widziałem/am bardzo wyraźnie"){
    r_att = 4
  } else if (resp_att =="Widziałem/am niewyraźnie i rozpoznawałem/am") {
    r_att = 3
  } else if (resp_att =="Widziałem/am ale nie rozpoznawałem/am") {
    r_att = 2
  } else{
    r_att = 1
  }
    
  if (resp_unatt =="Widziałem/am bardzo wyraźnie"){
    r_unatt = 4
  } else if (resp_unatt =="Widziałem/am niewyraźnie i rozpoznawałem/am") {
    r_unatt = 3
  } else if (resp_unatt =="Widziałem/am ale nie rozpoznawałem/am") {
    r_unatt = 2
  } else{
    r_unatt = 1
  }
  
  new_row = data.frame(subjects=row[["subjects"]], side='attended', resp=r_att)
  data_pas = rbind(data_pas,new_row)
  new_row = data.frame(subjects=row[["subjects"]], side='unattended', resp=r_unatt)
  data_pas = rbind(data_pas,new_row)
}

data_pas = transform(data_pas, resp = factor(resp, levels=c(1,2,3,4)),
                     side = factor(side), subjects = factor(subjects))


data_seen = data.frame(subjects=character(0),stim=character(0),resp=numeric(0))

for (i in 1:nrow(data_survey)){
  row = data_survey[i,]
  resp_targ = row[["Czy widziałeś/aś literę target pojawiającą się po unattended stronie?"]]
  resp_dist = row[["Czy widziałeś/aś inne litery pojawiające się po unattended stronie?"]]
  
  if (resp_targ =="Widziałem/am"){
    r_targ = 2
  } else if (resp_targ =="Nie widziałem/am") {
    r_targ = 1
  }
  
  if (resp_dist =="Widziałem/am"){
    r_dist = 2
  } else if (resp_dist =="Nie widziałem/am") {
    r_dist = 1
  }
  
  new_row = data.frame(subjects=row[["subjects"]], stim = 'target', resp=r_targ)
  data_seen = rbind(data_seen,new_row)
  new_row = data.frame(subjects=row[["subjects"]], stim = 'distractor', resp=r_dist)
  data_seen = rbind(data_seen,new_row)
}


data_seen = transform(data_seen, stim = factor(stim),subjects = factor(subjects))

data_perc = data.frame(subjects=character(0), block=character(0),resp=numeric(0))

for (i in 1:nrow(data_survey)){
  row = data_survey[i,]
  resp_last = row[["W jakiej części prób widziałeś/aś jakąkolwiek literę (U, H lub T) po dowolnej stronie?"]]
  resp_all = row[["We wcześniejszych częściach eksperymentu w jakiej części prób widziałeś/aś jakąkolwiek literę (U, H lub T) po dowolnej stronie?"]]
  
  if (resp_last == "100% prób"){
    r_last = 4
  } else if (resp_last =="Ok. 75% prób") {
    r_last = 3
  } else if (resp_last =="Ok. 50% prób") {
    r_last = 2
  } else{
    r_last = 1
  }
  
  if (is.na(resp_all)){
  } else if (resp_all =="100% prób"){
    r_all = 4
  } else if (resp_all =="Ok. 75% prób") {
    r_all = 3
  } else if (resp_all =="Ok. 50% prób") {
    r_all = 2
  } else{
    r_all = 1
  }
  
  new_row = data.frame(subjects=row[["subjects"]], block='last', resp=r_last)
  data_perc = rbind(data_perc,new_row)
  new_row = data.frame(subjects=row[["subjects"]], block='all', resp=r_all)
  data_perc = rbind(data_perc,new_row)
}

data_perc = transform(data_perc, block = factor(block, levels=c('last', 'all')),subjects = factor(subjects))

data_sides = data.frame(subjects=character(0), block=character(0),resp=numeric(0))

for (i in 1:nrow(data_survey)){
  row = data_survey[i,]
  resp_last = row[["Gdy już widziałeś/aś literę to jak często była ona po stronie attended a jak często po unattended?"]]
  resp_all = row[["We wcześniejszych częściach eksperymentu gdy już widziałeś/aś literę to jak często była ona po stronie, po której rozwiązywałeś/aś zadanie, a jak często po przeciwnej?"]]
  
  if (is.na(resp_last)){
  } else if (resp_last == "Zawsze po attended"){
    r_last = 1
  } else if (resp_last =="Częściej po attended") {
    r_last = 2
  } else if (resp_last =="Pół na pół") {
    r_last = 3
  } else{
    r_last = 4
  }
  
  if (is.na(resp_all)){
  } else if (resp_all == "Zawsze po attended"){
    r_all = 1
  } else if (resp_all =="Częściej po attended") {
    r_all = 2
  } else if (resp_all =="Pół na pół") {
    r_all = 3
  } else{
    r_all = 4
  }
  
  new_row = data.frame(subjects=row[["subjects"]], block='last', resp=r_last)
  data_sides = rbind(data_sides,new_row)
  new_row = data.frame(subjects=row[["subjects"]], block='all', resp=r_all)
  data_sides = rbind(data_sides,new_row)
}

data_sides = transform(data_sides, block = factor(block, levels=c('last', 'all')),subjects = factor(subjects))





#################################plotting###############################################################

df_pas = complete(count(data_pas, resp, side), resp = unique(resp), side = unique(side), 
              fill = list(n = 0))
df_seen = complete(count(data_seen, resp, stim), resp = unique(resp), stim = unique(stim), 
              fill = list(n = 0))
df_perc = complete(count(data_perc, resp, block), resp = 4, block = unique(block), 
         fill = list(n = 0))
df_sides = complete(count(data_sides, resp, block), resp = unique(resp), block = unique(block), 
         fill = list(n = 0))



cbPalette <- c("#c33b75ff", "#120d31ff")
plot_pas <- ggplot(df_pas, aes(x= factor(resp), y = n, fill = side, color = side)) +
  geom_bar(alpha=0.5, stat = 'identity', position=position_dodge(preserve = "single"), width = 0.5, linewidth = 1)+
  scale_y_continuous(name ="counts",
                     breaks = seq(0, 20, 5),
                     limits = c(0, 20), 
                     expand = c(0,0),
                     labels=c("0", "5", "10", "15", "20"))+ 
  
  scale_x_discrete(name ="",
                   labels=c("haven't at all", "not clearly,\nnot\nrecognized", "not clearly,\nrecognized", "clearly"))+
  scale_fill_manual(name = "side", values = cbPalette) +
  scale_color_manual(name = "side", values = cbPalette) +
  theme_bw() + 
  theme(axis.ticks = element_line(color = "gray79"), panel.border = element_blank(),
        panel.grid.major = element_line(colour = 'gray79'), 
        panel.grid.minor = element_blank(), axis.text.y = element_text(size = 10),
        axis.text.x = element_text(size = 10),
        plot.title = element_text(margin=margin(0,0,20,0)),
        plot.margin = margin(0.3,0.3,0.3, 0.3, "cm"), legend.position="right",
        legend.text=element_text(size=11)) +
  ggtitle('How well have you seen\nthe letters?')
plot_pas


cbPalette <- c("#fb8961ff", "#762181ff")
plot_seen <- ggplot(df_seen, aes(x= factor(resp), y = n, fill = stim, color = stim)) +
  geom_bar(alpha=0.5, stat = 'identity', position=position_dodge(preserve = "single"), width = 0.5, linewidth = 1)+
  scale_y_continuous(name ="counts",
                     breaks = seq(0, 20, 5),
                     limits = c(0, 20), 
                     expand = c(0,0),
                     labels=c("0", "5", "10", "15", "20"))+ 
  
  scale_x_discrete(name ="",
                   labels=c("yes", "no"))+
  scale_fill_manual(name = "stimulus", values = cbPalette) +
  scale_color_manual(name = "stimulus", values = cbPalette) +
  theme_bw() + 
  theme(axis.ticks = element_line(color = "gray79"), panel.border = element_blank(),
        panel.grid.major = element_line(colour = 'gray79'), 
        panel.grid.minor = element_blank(), axis.text.y = element_text(size = 10),
        axis.text.x = element_text(size = 10),
        plot.title = element_text(margin=margin(0,0,20,0)),
        plot.margin = margin(0.3,0.3,0.3, 0.3, "cm"), legend.position="right",
        legend.text=element_text(size=11)) +
  ggtitle('Have you seen a letter\non an unattended side?')
plot_seen




cbPalette <- c("#fece91ff", "#c33b75ff")
plot_perc <- ggplot(df_perc, aes(x= factor(resp), y = n, fill = block, color = block)) +
  geom_bar(alpha=0.5, stat = 'identity', position=position_dodge(preserve = "single"), width = 0.5, linewidth = 1)+
  scale_y_continuous(name ="counts",
                     breaks = seq(0, 20, 5),
                     limits = c(0, 20), 
                     expand = c(0,0),
                     labels=c("0", "5", "10", "15", "20"))+ 
  
  scale_x_discrete(name ="", 
                   labels=c("around 25%", "around 50%","around 75%", "100%"))+
  scale_fill_manual(name = "part", values = cbPalette, labels = c('final block', 'whole experiment')) +
  scale_color_manual(name = "part", values = cbPalette, labels = c('final block', 'whole experiment')) +
  theme_bw() + 
  theme(axis.ticks = element_line(color = "gray79"), panel.border = element_blank(),
        panel.grid.major = element_line(colour = 'gray79'), 
        panel.grid.minor = element_blank(), axis.text.y = element_text(size = 10),
        axis.text.x = element_text(size = 10),
        plot.title = element_text(margin=margin(0,0,20,0)),
        plot.margin = margin(0.3,0.3,0.3, 0.3, "cm"), legend.position="right",
        legend.text=element_text(size=11)) +
  ggtitle('In what percentage of trials\nhave you seen any letter?')
plot_perc


cbPalette <- c("#fece91ff", "#c33b75ff")
plot_sides <- ggplot(df_sides, aes(x= factor(resp), y = n, fill = block, color = block)) +
  geom_bar(alpha=0.5, stat = 'identity', position=position_dodge(preserve = "single"), width = 0.5, linewidth = 1)+
  scale_y_continuous(name ="counts",
                     breaks = seq(0, 20, 5),
                     limits = c(0, 20), 
                     expand = c(0,0),
                     labels=c("0", "5", "10", "15", "20"))+ 
  
  scale_x_discrete(name ="",
                   labels=c( "always\non the\nattended\nside", "more often\non the\nattended\nside", "fifty fifty","more often\non the\nunattended\nside"))+
  scale_fill_manual(name = "part", values = cbPalette, labels = c('final block', 'whole experiment')) +
  scale_color_manual(name = "part", values = cbPalette, labels = c('final block', 'whole experiment')) +
  theme_bw() + 
  theme(axis.ticks = element_line(color = "gray79"), panel.border = element_blank(),
        panel.grid.major = element_line(colour = 'gray79'), 
        panel.grid.minor = element_blank(), axis.text.y = element_text(size = 10),
        axis.text.x = element_text(size = 10),
        plot.title = element_text(margin=margin(0,0,20,0)),
        plot.margin = margin(0.3,0.3,0.3, 0.3, "cm"), legend.position="right",
        legend.text=element_text(size=11)) +
  ggtitle('When you saw the letter\nhow often it was presented\non each side?')
plot_sides


plot_all_1 <- plot_pas  + plot_seen + plot_spacer() +
  plot_layout(ncol=3,widths=c(2,1, 1)) &
  theme(legend.position= "none")
plot_all_1

plot_all_2 <- plot_perc + plot_sides  +
  plot_layout(ncol = 2, widths = c(2, 2)) & 
  #plot_layout(guides = 'collect') &
  theme(legend.position = "none")
plot_all_2


layout <- "
AABB
CCDD
"
plot_all <- plot_pas  + plot_seen + plot_perc + plot_sides + 
  plot_layout(design = layout) &
  theme(legend.position = "none")
plot_all




############################################################################################################
data_seen = data.frame(subjects=character(0),stim=character(0),resp=numeric(0))

for (i in 1:nrow(data_survey)){
  row = data_survey[i,]
  resp_targ = row[["Czy widziałeś/aś literę target pojawiającą się po unattended stronie?"]]
  resp_dist = row[["Czy widziałeś/aś inne litery pojawiające się po unattended stronie?"]]
  
  if (resp_targ =="Widziałem/am"){
    r_targ = 2
  } else if (resp_targ =="Nie widziałem/am") {
    r_targ = 1
  }
  
  if (resp_dist =="Widziałem/am"){
    r_dist = 2
  } else if (resp_dist =="Nie widziałem/am") {
    r_dist = 1
  }
  
  new_row = data.frame(subjects=row[["subjects"]], stim = 'target', resp=r_targ)
  data_seen = rbind(data_seen,new_row)
  new_row = data.frame(subjects=row[["subjects"]], stim = 'distractor', resp=r_dist)
  data_seen = rbind(data_seen,new_row)
}


data_seen = transform(data_seen, stim = factor(stim),subjects = factor(subjects))

data_perc = data.frame(subjects=character(0), block=character(0),resp=numeric(0))

for (i in 1:nrow(data_survey)){
  row = data_survey[i,]
  resp_last = row[["W jakiej części prób widziałeś/aś jakąkolwiek literę (U, H lub T) po dowolnej stronie?"]]
  resp_all = row[["We wcześniejszych częściach eksperymentu w jakiej części prób widziałeś/aś jakąkolwiek literę (U, H lub T) po dowolnej stronie?"]]
  
  if (resp_last == "100% prób"){
    r_last = 4
  } else if (resp_last =="Ok. 75% prób") {
    r_last = 3
  } else if (resp_last =="Ok. 50% prób") {
    r_last = 2
  } else{
    r_last = 1
  }
  
  if (is.na(resp_all)){
    r_all = NA
  } else if (resp_all =="100% prób"){
    r_all = 4
  } else if (resp_all =="Ok. 75% prób") {
    r_all = 3
  } else if (resp_all =="Ok. 50% prób") {
    r_all = 2
  } else{
    r_all = 1
  }
  
  new_row = data.frame(subjects=row[["subjects"]], block='last', resp=r_last)
  data_perc = rbind(data_perc,new_row)
  new_row = data.frame(subjects=row[["subjects"]], block='all', resp=r_all)
  data_perc = rbind(data_perc,new_row)
}

data_perc = transform(data_perc, block = factor(block),subjects = factor(subjects))

data_sides = data.frame(subjects=character(0), block=character(0),resp=numeric(0))

for (i in 1:nrow(data_survey)){
  row = data_survey[i,]
  resp_last = row[["Gdy już widziałeś/aś literę to jak często była ona po stronie attended a jak często po unattended?"]]
  resp_all = row[["We wcześniejszych częściach eksperymentu gdy już widziałeś/aś literę to jak często była ona po stronie, po której rozwiązywałeś/aś zadanie, a jak często po przeciwnej?"]]
  
  if (is.na(resp_last)){
    r_all = NA
  } else if (resp_last == "Zawsze po attended"){
    r_last = 4
  } else if (resp_last =="Częściej po attended") {
    r_last = 3
  } else if (resp_last =="Pół na pół") {
    r_last = 2
  } else{
    r_last = 1
  }
  
  if (is.na(resp_all)){
    r_all = NA
  } else if (resp_all == "Zawsze po attended"){
    r_all = 4
  } else if (resp_all =="Częściej po attended") {
    r_all = 3
  } else if (resp_all =="Pół na pół") {
    r_all = 2
  } else{
    r_all = 1
  }
  
  new_row = data.frame(subjects=row[["subjects"]], block='last', resp=r_last)
  data_sides = rbind(data_sides,new_row)
  new_row = data.frame(subjects=row[["subjects"]], block='all', resp=r_all)
  data_sides = rbind(data_sides,new_row)
}

data_sides = transform(data_sides, block = factor(block),subjects = factor(subjects))


################################### MODELS #################################################


model_pas<- brm(resp ~ side, data = data_pas, family = cumulative(link = "probit", threshold = "flexible"),
              sample_prior = "yes")

model_seen<- brm(resp ~ stim, data = data_seen ,family = bernoulli(link = "probit"), prior = set_prior("normal(0, 10)", class = "b"), 
              sample_prior = "yes")

model_perc<- brm(resp ~ block, data = data_perc, family = cumulative(link = "probit", threshold = "flexible"),
                sample_prior = "yes")

model_sides<- brm(resp ~ block, data = data_sides, family = cumulative(link = "probit", threshold = "flexible"),
                 sample_prior = "yes")

ce <-conditional_effects(model_pas, effect = 'side')#, categorical =TRUE)
ce
ce <-conditional_effects(model_seen, effect = 'stim')#, categorical =TRUE)
ce
ce <-conditional_effects(model_perc, effect = 'block')#, categorical =TRUE)
ce
ce <-conditional_effects(model_sides, effect = 'block')#, categorical =TRUE)
ce
