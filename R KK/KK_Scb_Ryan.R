install.packages("pxweb")
install.packages("ggplot2")
install.packages("dplyr")

library(pxweb)
library(ggplot2)
library(dplyr)

pxweb_query_list <- list(
  "Region" = c("01", "03", "04", "05", "06", "07", "08", "09", "10", "12", "13", "14", "17", "18", "19", "20", "21", "22", "23", "24", "25"), #samtliga län i Sverige
  "Drivmedel" = c("100", "110", "120"),  # Bensin, Diesel, El
  "ContentsCode" = c("TK1001AA"),
    "Tid"=c("2018M01","2018M02","2018M03","2018M04","2018M05","2018M06",
            "2018M07","2018M08","2018M09","2018M10","2018M11","2018M12",
            "2019M01","2019M02","2019M03","2019M04","2019M05","2019M06",
            "2019M07","2019M08","2019M09","2019M10","2019M11","2019M12",
            "2020M01","2020M02","2020M03","2020M04","2020M05","2020M06",
            "2020M07","2020M08","2020M09","2020M10","2020M11","2020M12",
            "2021M01","2021M02","2021M03","2021M04","2021M05","2021M06",
            "2021M07","2021M08","2021M09","2021M10","2021M11","2021M12",
            "2022M01","2022M02","2022M03","2022M04","2022M05","2022M06",
            "2022M07","2022M08","2022M09","2022M10","2022M11","2022M12",
            "2023M01","2023M02","2023M03","2023M04","2023M05","2023M06",
            "2023M07","2023M08","2023M09","2023M10","2023M11","2023M12",
            "2024M01", "2024M02", "2024M03", "2024M04", "2024M05", "2024M06",
            "2024M07", "2024M08", "2024M09", "2024M10", "2024M11", "2024M12",
            "2025M01", "2025M02", "2025M03"
  ) # Från 2018-2025
)


px_data <- pxweb_get(
  url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/TK/TK1001/TK1001A/PersBilarDrivMedel",
            query = pxweb_query_list)


data_frame <- as.data.frame(px_data, column.name.type = "text", variable.value.type = "text") %>%
 
 #Namnger columner till tydligare namn
  rename( datum = månad,
          antal_bilar = Antal) 

colnames(data_frame)
unique(data_frame$drivmedel)
unique(data_frame$datum)

#filtrera data
filtered_data <- data_frame %>%
    filter(drivmedel %in% c("bensin", "diesel", "el"))

#Gruppera datan
#summera antal bilar
summary_data <- filtered_data %>% 
  mutate(datum = as.integer(substr(datum, 1, 4))) %>% 
  group_by(datum, drivmedel) %>%
  summarize(antal_bilar = sum(`antal_bilar`))


# ggplot(summary_data, aes(x = datum, y = antal_bilar, color = drivmedel, group = drivmedel)) +
#  geom_point() +
#  geom_line() +
#  labs(title = "nyregistrerade bilar i Sveriges län baserat på drivmedel (2020 - 2025",
#       x = "År",
#       y = "Antal bilar") +
#  scale_y_continuous(labels = function(x) format(x, scientific = FALSE)) +
#  theme_minimal()



ggplot(summary_data, aes(x = datum, y = antal_bilar, color = drivmedel, group = drivmedel)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  labs(
    title = "Nyregistrerade bilar i Sveriges största län per drivmedel (2018–2025)",
    x = "År",
    y = "Antal bilar",) +
    
  theme_minimal() +
  scale_y_continuous(labels = scales::comma)


file_path <- "D:\\Utbildning\\R\\scb_plot.csv"

write.csv(summary_data, file_path, row.names = FALSE)  



