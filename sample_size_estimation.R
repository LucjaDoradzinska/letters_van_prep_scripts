library(brms)
library(tidyverse)
library(future.apply)
library(dplyr)
library(writexl)
library(readxl)


#settings for max speed 
Sys.setenv(MAKEFLAGS = "-j4") 
options(brms.backend = "rstan")
total_cores <- availableCores()
safe_cores <- total_cores - 4 
plan(multisession, workers = safe_cores)


#simulation params
n_subjects_grid <- c (15, 20, 25, 30) # testing for different sample sizes
n_trials_per_cond <- 86            # n trials per cond (in EXP1)
target_evidence_ratio <- 3         # target Evidence Ratio threshold
n_simulations <- 500                

# model params based on VAN-ff, early time-window
interaction_effect <- -0.46  # masking:taskID
sd_between_subjects  <- 2.23  #  intercept
sd_residual          <- 6.53  


# simulating data grid function
generate_sim_data <- function(i, N) {
  set.seed(202610 + i + N*1000)
  expand.grid(
    subject = 1:N,
    masking = c("masked", "unmasked"),
    taskID = c("distractor", "target"),
    att = c("att", "unatt"),
    trial = 1:n_trials_per_cond
  ) %>%
    mutate(
      subject = as.factor(subject),
      taskID = factor(taskID, levels = c("distractor", "target")),
      masking = factor(masking, levels = c("masked", "unmasked")),
      sub_intercept = rnorm(N, mean = 0, sd = sd_between_subjects)[subject],
      effect = ifelse(masking == "unmasked" & taskID == "target", interaction_effect, 0),
      y = rnorm(nrow(.), mean = effect + sub_intercept, sd = sd_residual)
    )
}


priors <- c(
  # interaction prior
  set_prior(sprintf("normal(0, %f)", sd_residual), class = "b", coef = "maskingunmasked:taskIDtarget"),
  # between subj variance
  set_prior(sprintf("normal(0, %f)", sd_between_subjects), class = "sd"),
  # residuals
  set_prior(sprintf("normal(0, %f)", sd_residual), class = "sigma")
)


# initial model for updating
data_init <- generate_sim_data(i = 1, N = 15) 
fit_base <- brm(y ~ masking * taskID * att + (1 + masking * taskID * att | subject), data = data_init, 
                family = gaussian(link = 'identity'), prior = priors,
                sample_prior = "no", refresh = 0, 
                iter = 1, chains = 1, warmup = 0,
                backend = "rstan")


successes <- list()


# simulation loop
for(N in n_subjects_grid) {
  
  
  successes_for_N <- future_lapply(1:n_simulations, function(i) {
    data_sim <- generate_sim_data(i, N)
    
    fit_sim <- update(fit_base, newdata = data_sim, iter = 800, warmup = 300, 
                      recompile = FALSE, refresh = 0)
    
    
    hyp <- hypothesis(fit_sim, "maskingunmasked:taskIDtarget < 0")
    ev_ratio <- hyp$hypothesis$Evid.Ratio
    n_div <- sum(subset(nuts_params(fit_sim), Parameter == "divergent__")$Value)
    
    
    return(data.frame(
      N = N,
      iter = i,
      evidence_ratio = ev_ratio,
      n_divergent = n_div
    ))
    }, future.seed = TRUE)
  successes[[as.character(N)]] <- bind_rows(successes_for_N)
}

report_er <- bind_rows(successes)




success_summary <- report_er %>%
  mutate(if_success = evidence_ratio > target_evidence_ratio) %>%
  
  group_by(N) %>%
  
  summarise(
    Number_of_simulations = n(),
    Number_of_successes  = sum(if_success),
    Percent_of_successes = mean(if_success) * 100,
    Median_ER = median(evidence_ratio) 
  )



