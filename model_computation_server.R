library(rstanarm)
library(tidyverse)
library(lubridate)

# rstanarm options
options(mc.cores = 4)

# Data load
load("full_df.rda")


## Training data

# df:     dataframe to sample from
# years:  vector of years to include
# months: vector of months to include
# dhour:  which hours to pick (hour %% dhour == 0)
data_sampler <- function(df, years, months, ddays, dhour) {
  sample <- df %>% filter(
                    year(datetime) %in% years &
                    month(datetime) %in% months &
                    day(datetime) %% ddays == 0 &
                    hour(datetime) %% dhour == 0
                  )
  return(sample)
}

# training_df_winter <- data_sampler(full_df, c(2018), c(12, 1, 2), 1, 6)
# training_df_winter_ts2 <- data_sampler(full_df_ts2, c(2018), c(12, 1, 2), 1, 6)
# training_df_winter_ts6 <- data_sampler(full_df_ts6, c(2018), c(12, 1, 2), 1, 6)
# training_df_winter_ts24 <- data_sampler(full_df_ts24, c(2018), c(12, 1, 2), 1, 6)

training_df_year <- data_sampler(full_df, c(2018), c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 1, 6)
training_df_year_ts6 <- data_sampler(full_df_ts6, c(2018), c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 1, 6)



## w10 + w100, log target, ts=0, year

post_w10_w100_log_year <- stan_glmer(log_energy ~ w10 + w100 + (w10 + w100 | region) + (w10 + w100 | season),
                      data = training_df_year,
                      family = gaussian(link = "identity"),
                      prior = normal(0, 1),
                      prior_intercept = student_t(df = 2, loc = 4, scale = 1),
                      adapt_delta = 0.999
                    )

# Save the fit
save(post_w10_w100_log_year, file = "post_w10_w100_log_year.rda")
print(post_w10_w100_log_year)



## w10 + w100, log target, ts=6, year

post_w10_w100_log_year_ts6 <- stan_glmer(log_energy ~ w10 + w100 + (w10 + w100 | region) + (w10 + w100 | season),
                      data = training_df_year_ts6,
                      family = gaussian(link = "identity"),
                      prior = normal(0, 1),
                      prior_intercept = student_t(df = 2, loc = 4, scale = 1),
                      adapt_delta = 0.999
                    )

# Save the fit
save(post_w10_w100_log_year_ts6, file = "post_w10_w100_log_year_ts6.rda")
print(post_w10_w100_log_year_ts6)

















