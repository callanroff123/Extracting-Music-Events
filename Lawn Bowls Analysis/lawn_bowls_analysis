# Load required libraries
library(dplyr)
library(ggplot2)
library(lattice)
library(tidyverse)
library(MASS)
library(car)
library(nlme)
library(lme4)
library(mice)
library(gridExtra)

# Read in/clean this season's data
lawn_bowls_CURRENT_raw <- read.csv("C:\\Users\\croff\\OneDrive - Kmart Australia Limited\\KHome\\My Offline Files\\Desktop\\Lawn Bowls\\lawn_bowls.csv")
lawn_bowls_CURRENT_raw$Year <- factor(2021)
lawn_bowls_CURRENT <- na.omit(lawn_bowls_CURRENT_raw)
lawn_bowls_CURRENT <- lawn_bowls_CURRENT[(lawn_bowls_CURRENT$Result == "Win"|lawn_bowls_CURRENT$Result == "Lose"),]
lawn_bowls_CURRENT$Name <- lawn_bowls_CURRENT$ï..Name

# Read in/clean archived data
lawn_bowls_ARCHIVE_raw <- read.csv("C:\\Users\\croff\\OneDrive - Kmart Australia Limited\\KHome\\My Offline Files\\Desktop\\Lawn Bowls\\lawn_bowls_archive.csv")
lawn_bowls_ARCHIVE_raw$Result <- ifelse(lawn_bowls_ARCHIVE_raw$Result == "Loss", "Lose", lawn_bowls_ARCHIVE_raw$Result)
lawn_bowls_ARCHIVE <- lawn_bowls_ARCHIVE_raw[(lawn_bowls_ARCHIVE_raw$Result == "Win") |(lawn_bowls_ARCHIVE_raw$Result == "Lose"),]
lawn_bowls_ARCHIVE$Year <- factor(lawn_bowls_ARCHIVE$Year)
lawn_bowls_ARCHIVE$Round <- substring(lawn_bowls_ARCHIVE$Round, 7)
lawn_bowls_ARCHIVE$Round <- as.numeric(lawn_bowls_ARCHIVE$Round)
lawn_bowls_ARCHIVE$Name <- lawn_bowls_ARCHIVE$ï..Name

# Combined data
lawn_bowls_ALL <- union_all(lawn_bowls_ARCHIVE, lawn_bowls_CURRENT)
lawn_bowls_ALL$Year <- factor(lawn_bowls_ALL$Year, ordered = TRUE)
lawn_bowls_ALL$Season_Type <- ifelse(lawn_bowls_ALL$Year == 2021, "Current Season", "Previous Seasons")

# Augmented datasets for exploatory plots.
tot_wins_position <- as.data.frame(lawn_bowls_ALL %>% group_by(Position, Season_Type) %>% summarise(Tot_Position_Wins = sum(Result_Binary), Tot_Position_Games = sum(Result_Binary == 0|Result_Binary == 1)))
tot_wins_year <- as.data.frame(lawn_bowls_ALL %>% group_by(Year) %>% summarise(Tot_Year_Wins = sum(Result_Binary), Tot_Year_Games = sum(Result_Binary == 0|Result_Binary == 1)))
tot_wins_score <- as.data.frame(lawn_bowls_ALL %>% group_by(Score) %>% summarise(Tot_Score_Wins = sum(Result_Binary), Tot_Score_Games = sum(Result_Binary == 0|Result_Binary == 1)))

# Exploratory plots
p1 <- ggplot(lawn_bowls_ALL, aes(x = Year, y = Score)) +
  geom_boxplot() +
  geom_abline(intercept = mean(lawn_bowls_ALL$Score), slope = 0, color = "blue", lty = 2) +
  ggtitle("Average Individual Scores by Season")
p2 <- ggplot(lawn_bowls_ALL, aes(x = Round, y = Score, color = Season_Type)) +
  geom_point(size = 1) +
  geom_smooth(se = T, lwd = 1.25) +
  ggtitle("Average Individual Score by Round")
p3 <- ggplot(lawn_bowls_ARCHIVE, aes(x = Round, y = Score, color = Position)) +
  geom_point(size = 1) +
  geom_smooth(se = F, lwd = 1.25) +
  ggtitle("Average Individual Score by Round in 2019 and 2020") +
  geom_abline(intercept = mean(lawn_bowls_ARCHIVE$Score), slope = 0, color = "black", lty = 2)
p4 <- ggplot(lawn_bowls_CURRENT, aes(x = Round, y = Score, color = Position)) +
  geom_point(size = 1) +
  geom_smooth(se = F, lwd = 1.25) +
  ggtitle("Average Individual Score by Round in Current Season") +
  geom_abline(intercept = mean(lawn_bowls_CURRENT$Score), slope = 0, color = "black", lty = 2)
p5 <- ggplot(lawn_bowls_ARCHIVE, aes(x = Position, y = Score)) +
  geom_boxplot() +
  geom_abline(intercept = mean(lawn_bowls_ARCHIVE$Score), slope = 0, color = "blue", lty = 2) +
  ggtitle("Average Individual Score by Position in 2019 and 2020")
p5 <- ggplot(lawn_bowls_CURRENT, aes(x = Position, y = Score)) +
  geom_boxplot() +
  geom_abline(intercept = mean(lawn_bowls_CURRENT$Score), slope = 0, color = "blue", lty = 2) +
  ggtitle("Average Individual Score by Position in Current Season")
p6 <- ggplot(lawn_bowls_ARCHIVE, aes(x = Result, y = Score)) +
  geom_boxplot() +
  geom_abline(intercept = mean(lawn_bowls_ARCHIVE$Score), slope = 0, color = "blue", lty = 2) +
  ggtitle("Average Individual Score by Result in 2019 and 2020")
p7 <- ggplot(lawn_bowls_CURRENT, aes(x = Result, y = Score)) +
  geom_boxplot() +
  geom_abline(intercept = mean(lawn_bowls_CURRENT$Score), slope = 0, color = "blue", lty = 2) +
  ggtitle("Average Individual Score by Result in Current Season")
p8 <- ggplot(tot_wins_position, aes(x = Position, y = Tot_Position_Wins/Tot_Position_Games*100, color = Season_Type)) +
  geom_point(aes(shape = Season_Type), size = 3) +
  geom_abline(intercept = sum(tot_wins_poisition$Tot_Position_Wins)/sum(tot_wins_poisition$Tot_Postion_Games)*100, slope = 0, color = "black", lty = 2) +
  geom_abline(intercept = sum(tot_wins_poisition[tot_wins_poisition$Season_Type == "Current Season", "Tot_Position_Wins"])/sum(tot_wins_poisition[tot_wins_poisition$Season_Type == "Current Season", "Tot_Postion_Games"])*100, slope = 0, color = "red", lty = 2) +
  geom_abline(intercept = sum(tot_wins_poisition[tot_wins_poisition$Season_Type == "Previous Seasons", "Tot_Position_Wins"])/sum(tot_wins_poisition[tot_wins_poisition$Season_Type == "Previous Seasons", "Tot_Postion_Games"])*100, slope = 0, color = "4DBBD5B2", lty = 2) +
  ylab("Win Percentage") +
  ggtitle("OVerall Win Percentage by Position") +
  ylim(c(60, 75))
p9 <- ggplot(tot_wins_year, aes(x = Year, y = Tot_Year_Wins/Tot_Year_Games*100, group = 1)) +
  geom_point() +
  geom_line() +
  ylab("Win Percentage") +
  ggtitle("Overall Win Percentage by Year")
p10 <- ggplot(tot_wins_score[tot_wins_score$Tot_Score_Games >= 9,], aes(x = Score, y = Tot_Score_Wins/Tot_Score_Games*100)) +
  geom_point() +
  geom_smooth() +
  ylab("Win Percentage") +
  ggtitle("Win Percentage by an Individual's Score (All Seasons)")

# Analysis 1: Logistic regression. Model the probability of winning a game given an individual scores, position and round in the competition and season.
# Let's test what degree of feature interaction we need to account for.
lawn_bowls_ALL_new <- lawn_bowls_ALL
lawn_bowls_ALL_new$Year <- factor(lawn_bowls_ALL$Year, ordered = FALSE)
model1 <- glm(factor(Result_Binary) ~ Score*Round*Position*Year, family = binomial(link = "logit"), data = lawn_bowls_ALL_new)
model2 <- glm(factor(Result_Binary) ~ Score*Round*Position + Score*Round*Year + Score*Position*Year + Round*Position*Year, family = binomial(link = "logit"), data = lawn_bowls_ALL_new)
model3 <- glm(factor(Result_Binary) ~ Score*Round + Score*Position + Score*Year + Round*Position + Round*Year + Position*Year, family = binomial(link = "logit"), data = lawn_bowls_ALL_new)
model4 <- glm(factor(Result_Binary) ~ Score + Round + Position + Year, family = binomial(link = "logit"), data = lawn_bowls_ALL_new)
model5 <- glm(factor(Result_Binary) ~ 1, family = binomial(link = "logit"), data = lawn_bowls_ALL_new)
AIC(model1, model2, model3, model4, model5) #...model4 has lower AIC than model5 and model3 => ideal candidate model (which includes all terms) between model3 and model4
# Lets assume the relationship between the odds of winning and individual score is different across bowler position.
# Lets also assume the relationship between the odds of winning and individual score is different across seasons.
final_mod <- glm(factor(Result_Binary) ~ Score*Position + Score*Year + Round, family = binomial(link = "logit"), data = lawn_bowls_ALL_new)
anova(final_mod, test = "Chisq")
summary(final_mod)

# Analysis 2: Linear regression: Model an individual's score given their position, Round in the competition and season (Year)
# First, we should test if an appropriate transformation of the response is needed.
# y = g(n(x)) for: g(t) = t, g(t) = log(t) and g(t) = t^(1/2)
dist_plot <- function(x){
  hist(x, probability = TRUE)
  lines(density(x), col = "blue", lwd = 1)
}
norm_qq <- function(x){
  qqnorm(x)
  qqline(x)
}
par(mfrow = c(1,2))
dist_plot(lawn_bowls_ALL_new$Score)
norm_qq(lawn_bowls_ALL_new$Score)
par(mfrow = c(1,2))
dist_plot(log(lawn_bowls_ALL_new$Score))
norm_qq(log(lawn_bowls_ALL_new$Score))
par(mfrow = c(1,2))
dist_plot(sqrt(lawn_bowls_ALL_new$Score))
norm_qq(sqrt(lawn_bowls_ALL_new$Score))
linmod1 <- lm(Score ~ Round * Position * Year, data = lawn_bowls_ALL_new)
linmod2 <- lm(log(Score) ~ Round * Position * Year, data = lawn_bowls_ALL_new)
linmod3 <- lm(sqrt(Score) ~ Round * Position * Year, data = lawn_bowls_ALL_new)
plot(linmod1, which = 1:2)
plot(linmod2, which = 1:2)
plot(linmod3, which = 1:2)
# For the full model (all possible feature interactions), it appears as though the square root transformation most adequately satisfies linear model assumptions.
linmod31 <- linmod3
linmod32 <- lm(sqrt(Score) ~ Round * Position + Round * Year + Position * Year, data = lawn_bowls_ALL_new)
linmod33 <- lm(sqrt(Score) ~ Round + Position + Year, data = lawn_bowls_ALL_new)
AIC(linmod31, linmod32, linmod33)
# Conveniently, the model with no interactions has the lowest AIC. Let's turn our attention only to that.
anova(linmod33)
summary(linmod33)