install.packages("readxl")
install.packages("ggplot2")
install.packages("car")
install.packages("leaps")

library(readxl)
library(ggplot2)
library(car)
library(leaps)

data <- read_excel("D:\\Utbildning\\R\\data_insamling_volvo_blocket.xlsx")


dim(data)
head(data)
str(data)
summary(data)

# gör om datan jag har valt till numeriska
data$Pris <- as.numeric(data$Försäljningspris)
data$Miltal <- as.numeric(data$Miltal)
data$Modellår <- as.numeric(data$Modellår)

# Tar bort okända väden
clean_data <- na.omit(data[, c("Pris", "Miltal", "Modellår", "Bränsle", "Växellåda")])

#Skapa regressionsmodell
model <- lm(Pris ~ Miltal + Modellår + Bränsle + Växellåda, data = clean_data)


summary(model)

#plottar resultatet
par(mfrow = c(2, 2))
plot(model)

vif(model)

#Utan bränsle, för att kontrollera ifall det är en viktig variabel
model2 <- lm(Pris ~ Miltal + Modellår + Växellåda, data = clean_data)

summary(model2)

par(mfrow = c(2,2))
plot(model2)


#skapar en regsubsets för att säkerställa valen av variabler
model3 <- regsubsets(Pris ~ Miltal + Modellår + Bränsle + Växellåda, data = clean_data, nvmax = 10)

par(mfrow = c(1,1))
plot(model3, scale = "adjr2")

#Model enligt regsubsets resultat och lägger log för att få bättre resultat på pris värden
model_reg <- lm (log(Pris) ~ Modellår + Bränsle + Växellåda, data = clean_data)
summary(model_reg)

par(mfrow = c(2,2))
plot(model_reg)
vif(model_reg)
