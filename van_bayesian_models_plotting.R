rm(list=ls())
library(tidyverse)
library(patchwork)

load("D:\\ff_experiment\\Results\\EEG\\models\\van_temp_early_bayesian_models.RData")
#load("D:\\ff_experiment\\Results\\EEG\\models\\van_temp_late_bayesian_models.RData")
#load("D:\\ff_experiment\\Results\\EEG\\models\\van_occ_early_bayesian_models.RData")
#load("D:\\ff_experiment\\Results\\EEG\\models\\van_occ_late_bayesian_models.RData")
#load("D:\\ff_experiment\\Results\\EEG\\models\\p3_bayesian_models.RData")

cbPalette <- c("#fb8961ff", "#762181ff")


ce_dt <- as.data.frame(ce[['masking']])
ce_att_dt <- filter(ce_dt, att_cond == 'attended')
ce_unatt_dt <- filter(ce_dt, att_cond == 'unattended')

plot_att <- ggplot(ce_att_dt, aes(x = stimulus, color = masking)) +
  geom_errorbar(aes(ymin=lower__, ymax=upper__),width=0, linewidth=1, position = position_dodge(width=0.4)) +
  geom_point(aes(y=estimate__), size=2, position = position_dodge(width=0.4)) +
  scale_y_continuous(name ="ERP values [μV]",
                     breaks = seq(-4, 4, 2),# #,(-2, 6, 2),(-6, 2, 2), 
                     limits = c(-4, 4), #(-2, 6), (-6, 2),
                     expand = c(0,0),
                     labels=c("-4", "-2", "0", "2", "4")) +#("-2", "0", "2", "4", "6")) +("-6", "-4", "-2", "0", "2")) + 
  scale_x_discrete(name ="stimulus",
                   limits=c("distractor","target"), expand = c(0.2,0.2), labels=c("distractor", "target")) + #limits=c("distractor","target"), expand = c(0.2,0.2))+
  scale_color_manual(name = "masking", values = cbPalette) +
  theme_bw() + 
  theme(axis.ticks = element_line(color = "gray79"), panel.border = element_blank(),
        panel.grid.major = element_line(colour = 'gray79'), 
        panel.grid.minor = element_blank(), axis.text.y = element_text(size = 10),
        axis.text.x = element_text(size = 11),
        plot.title = element_text(margin=margin(0,0,20,0)),
        plot.margin = margin(0.3,0.7,0.3, 0.3, "cm"), legend.position="bottom",
        legend.text=element_text(size=11)) +
  ggtitle('attended')
plot_att

plot_unatt <- ggplot(ce_unatt_dt, aes(x = stimulus, color = masking)) +
  geom_errorbar(aes(ymin=lower__, ymax=upper__),width=0, linewidth=1, position = position_dodge(width=0.4)) +
  geom_point(aes(y=estimate__), size=2, position = position_dodge(width=0.4)) +
  scale_y_continuous(name ="ERP values [μV]",
                     breaks = seq(-4, 4, 2),# #,(-2, 6, 2),(-6, 2, 2), 
                     limits = c(-4, 4), #(-2, 6), (-6, 2),
                     expand = c(0,0),
                     labels=c("-4", "-2", "0", "2", "4")) +#("-2", "0", "2", "4", "6")) +("-6", "-4", "-2", "0", "2")) + 
  scale_x_discrete(name ="stimulus",
                   limits=c("distractor","target"), expand = c(0.2,0.2), labels=c("distractor", "target")) + #limits=c("distractor","target"), expand = c(0.2,0.2))+
  scale_color_manual(name = "masking", values = cbPalette) +
  theme_bw() + 
  theme(axis.ticks = element_line(color = "gray79"), panel.border = element_blank(),
        panel.grid.major = element_line(colour = 'gray79'), 
        panel.grid.minor = element_blank(), axis.text.y = element_text(size = 10),
        axis.text.x = element_text(size = 11),
        plot.title = element_text(margin=margin(0,0,20,0)),
        plot.margin = margin(0.3,0.3,0.3, 0.3, "cm"), legend.position="bottom",
        legend.text=element_text(size=11)) +
  ggtitle('unattended')
plot_unatt

plot_all_H <- plot_unatt  +plot_att + 
  plot_layout(guides = 'collect') &
  theme(legend.position='bottom')
plot_all_H

