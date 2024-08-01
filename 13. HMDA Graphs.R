#Date: 2024/03/12
#Author: Carl Romer
#This file takes the HMDA data from the Summary statistics file

#########################################################
#Setup
#########################################################
package_list <- c("tidyverse",
                  "purrr",
                  "scales",
                  "openxlsx", 
                  "scales",
                  "devtools", 
                  "extrafont",
                  'readxl',
                  "tidycensus",
                  'kableExtra')

#install.packages(package_list) #if you need to install remove first # on this line
#webshot::install_phantomjs()
lapply(package_list,
       require,
       character.only = T)
#########################################################
#Build functions
#########################################################
S_sqrt <- function(x){sign(x)*sqrt(abs(x))}
IS_sqrt <- function(x){x^2*sign(x)}
S_sqrt_trans <- function() trans_new("S_sqrt",S_sqrt,IS_sqrt)

#########################################################
#Data importation
#########################################################
setwd("C:/Users/csromer/OneDrive - National Bankers Association/Blogs/2024/HMDA")
climate <- read_csv("2. Data Output/Climate percentile data.csv")
climate_mean <- read_csv("2. Data Output/Climate mean data.csv")
climate_mdi <- read_csv("2. Data Output/Climate percentile data MDI.csv")
climate_meanmdi <- read_csv("2. Data Output/Climate mean data MDI.csv")

overall_mdi <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'Overall MDI Banks'
  ) %>% 
  mutate(type = 'MDI',
         Race = "overall")

race_mdi <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'By race MDI'
)%>% 
  mutate(type = 'MDI')

minority_mdi<- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'By bank race MDI'
)
minority_race_mdi<- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'By bank race by race MDI'
)

overall_non_mdi <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'Overall nonMDI Banks'
)%>% 
  mutate(Race = "overall",
         type = 'nonMDI'
         )

race_non_mdi <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'By race nonMDI bank'
)%>% 
  mutate(type = 'nonMDI'
         )

overall_cdfi <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'Overall CDFI Banks'
)%>% 
  mutate(Race = "overall",
         type = 'CDFI'
  )


race_cdfi <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'By race CDFI bank'
)%>% 
  mutate(
         type = 'CDFI'
  )


overall_community <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'Overall Community Banks'
)%>% 
  mutate(Race = "overall",
         type = 'Community'
  )

race_community <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'By race community bank'
)%>% 
  mutate(
         type = 'Community'
  )


overall_top25 <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'Overall top25 Banks'
)%>% 
  mutate(Race = "overall",
         type = 'Top 25'
  )

race_top25 <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'By race top25 bank'
)%>% 
  mutate(
         type = 'Top 25'
  )


overall_fintech <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'Overall fintech Banks'
)%>% 
  mutate(Race = "overall",
         type = 'Fintech'
  )

race_fintech <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'By race fintech bank'
)%>% 
  mutate(
         type = 'Fintech'
  )

overall_cu <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'Overall credit_union Banks'
)%>% 
  mutate(Race = "overall",
         type = 'Credit union'
  )

race_cu <- readxl::read_xlsx(
  "2. Data Output/Summary Statistics.xlsx",
  sheet = 'By race credit_union bank'
)%>% 
  mutate(
    type = 'Credit union'
  )

combined <- rbind(overall_mdi,
      overall_non_mdi,
      overall_cdfi,
      overall_community,
      overall_fintech,
      overall_top25,
      overall_cu,
      race_mdi,
      race_non_mdi,
      race_cdfi,
      race_community,
      race_fintech,
      race_top25,
      race_cu)
rm(overall_mdi,
   overall_non_mdi,
   overall_cdfi,
   overall_community,
   overall_fintech,
   overall_top25,
   overall_cu,
   race_mdi,
   race_non_mdi,
   race_cdfi,
   race_community,
   race_fintech,
   race_top25,
   race_cu)

#########################################################
#tables
#########################################################

#########################################################
#Denial reason by Bank Type
#########################################################
#Denial reason by Bank Type

table <- minority_mdi %>%
  mutate(type = case_when(`Minority Status` == 'B' ~ "Black",
                          `Minority Status` == 'A' ~ "Asian American or Pacific Islander",
                          `Minority Status` == 'N' ~ "American Indian or Alaska Native",
                          `Minority Status` == 'H' ~ "Hispanic",
                          `Minority Status` == 'M' ~ "Mixed",
  )) %>% 
  select('MDI type'='type',
         Year,
         Loans,
         'Total loan dollars (in thousands)' = 'Total loan dollars',
         'Median loan (in thousands)' = 'Median loan')%>% 
  mutate_at(c('Total loan dollars (in thousands)',
              'Median loan (in thousands)'),
            ~scales::dollar(./1000, accuracy = 1))

write_csv(table,
          '4. Tables/Table MDI.csv')

table_kable <- kbl(table %>% 
                     mutate(Year = as.character(Year)),
                   format.args = list(big.mark = ","),
                   caption = "<b>Tables TK: MDIs<b>") %>% 
  row_spec(seq(1,nrow(table),2), background="#DEDEDE") %>% 
  kable_classic(full_width = F, html_font = "Arial") %>% 
  kable_styling(#bootstrap_options = c("striped", "hover"),
    full_width = F,
    font_size = 12,
    html_font = "Arial")

save_kable(table_kable, file = "4. Tables/Table MDI.html")
webshot::webshot("4. Tables/Table MDI.html", 
                 "4. Tables/Table MDI.pdf")
webshot::webshot("4. Tables/Table MDI.html", 
                 "4. Tables/Table MDI.jpg")

#########################################################
#Denial reason by Bank Type
#########################################################
#Denial reason by Bank Type
table <- combined %>%
  filter(Race=='overall') %>% 
  select('Bank'='type',
         Year,
         "Debt to income"= "DRD2I" ,                           
          "Economic history"="DREH" ,                            
          'Credit history'= "DRCH",                   
          "Collateral"="DRCollat" ,                        
          "Insufficient cash"="DRCash" ,                 
          "Mortgage insurance denied"="DRMID",                    
          'Other'="DRother") %>% 
  mutate_at(c("Debt to income",
              "Economic history",         
               "Credit history",
              "Collateral",
              "Insufficient cash",
              "Mortgage insurance denied",
              "Other"),
            ~scales::percent(., accuracy = 1)) %>% 
  arrange(Year)

write_csv(table,
          '4. Tables/Table Denial Reasons.csv')

table_kable <- kbl(table %>% 
                     mutate(Year = as.character(Year)),
                                  format.args = list(big.mark = ","),
                                  caption = "<b>Tables TK: Denial Reasons<b>") %>% 
  row_spec(seq(1,nrow(table),2), background="#DEDEDE") %>% 
  kable_classic(full_width = F, html_font = "Arial") %>% 
  kable_styling(#bootstrap_options = c("striped", "hover"),
    full_width = F,
    font_size = 12,
    html_font = "Arial")

save_kable(table_kable, file = "4. Tables/Table Denial Reason.html")
webshot::webshot("4. Tables/Table Denial Reason.html", 
        "4. Tables/Table Denial Reason.pdf")
webshot::webshot("4. Tables/Table Denial Reason.html", 
                 "4. Tables/Table Denial Reason.jpg")


#########################################################
#Denial reason by MDI TYPE
#########################################################

table <- minority_mdi %>%
  mutate(type = case_when(`Minority Status` == 'B' ~ "Black",
                          `Minority Status` == 'A' ~ "Asian American or Pacific Islander",
                          `Minority Status` == 'N' ~ "American Indian or Alaska Native",
                          `Minority Status` == 'H' ~ "Hispanic",
                          `Minority Status` == 'M' ~ "Mixed",
                          )) %>% 
  select('MDI type'='type',
         Year,
         "Debt to income"= "DRD2I" ,                           
         "Economic history"="DREH" ,                            
         'Credit history'= "DRCH",                   
         "Collateral"="DRCollat" ,                        
         "Insufficient cash"="DRCash" ,                 
         "Mortgage insurance denied"="DRMID",                    
         'Other'="DRother") %>% 
  mutate_at(c("Debt to income",
              "Economic history",         
              "Credit history",
              "Collateral",
              "Insufficient cash",
              "Mortgage insurance denied",
              "Other"),
            ~scales::percent(., accuracy = 1))

write_csv(table,
          '4. Tables/Table Denial Reasons MDI.csv')

table_kable <- kbl(table %>% mutate(Year = as.character(Year)) ,
                   format.args = list(big.mark = ","),
                   caption = "<b>Tables TK: Denial Reasons by MDI Type<b>") %>% 
  row_spec(seq(1,nrow(table),2), background="#DEDEDE") %>% 
  kable_classic(full_width = F, html_font = "Arial") %>% 
  kable_styling(#bootstrap_options = c("striped", "hover"),
    full_width = F,
    font_size = 12,
    html_font = "Arial")

save_kable(table_kable, file = "4. Tables/Table Denial Reason MDI.html")
webshot::webshot("4. Tables/Table Denial Reason MDI.html", 
                 "4. Tables/Table Denial Reason MDI.pdf")
webshot::webshot("4. Tables/Table Denial Reason MDI.html", 
                 "4. Tables/Table Denial Reason MDI.jpg")

#########################################################
#graphs
#########################################################

#Overall
total_loans <- combined %>% 
  filter(Race == "overall")
race_loans <- combined %>% 
  filter(Race != "overall")

#########################################################
#0
#########################################################
total_loansggplot <- total_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = Loans,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
    )
  ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = c("25,000",
                                 "100,000",
                                 "250,000",
                                 "1,000,000",
                                 "2,500,000",
                                 "5,000,000"),
                      breaks = c(25000,
                                 100000,
                                 250000,
                                 1000000,
                                 2500000,
                                 5000000),
  trans = scales::sqrt_trans(),
  limits = c(0,5000001),
  expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Number of loans",
    title = "Number of loans by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(total_loans,
          '3. Graphs/0. Total loans by institution type.csv')

ggsave(total_loansggplot, 
       filename = "3. Graphs/0. Total loans by institution type.pdf",
       width = 10,
       height = 6)
ggsave(total_loansggplot, 
       filename = "3. Graphs/0. Total loans by institution type.jpg",
       width = 10,
       height = 6)

total_loansggplot_byrace <- race_loans %>% 
  group_by(type, Year) %>% 
  mutate(Loans = Loans/sum(Loans)) %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = Loans,
      fill = Race
      )
    )+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  facet_wrap(~ factor(as.character(Year),
                      levels = c("2019",
                                 "2020",
                                 "2021",
                                 "2022")),
             scales = "free")+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(.01,
                                .05,
                                .1,
                                .25,
                                .5,
                                .75),
                     trans = scales::sqrt_trans(),
                     limits = c(0,.8),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of loans\n(note: axis in square root scale)",
    title = "Percent of loans by race by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(race_loans %>% 
            group_by(type, 
                     Year) %>% 
            mutate(Loans = Loans/sum(Loans)),
          "3. Graphs/0.Race. Total loans by institution type.csv")

ggsave(total_loansggplot_byrace, 
       filename = "3. Graphs/0.Race. Total loans by institution type.pdf",
       width = 10,
       height = 6)
ggsave(total_loansggplot_byrace, 
       filename = "3. Graphs/0.Race. Total loans by institution type.jpg",
       width = 10,
       height = 6)

total_loansggplot_byminoritystatus <- minority_mdi %>% 
  ggplot(
    aes(
      fill = factor(`Minority Status`,
                 levels = c(
                   "A",
                   "B",
                   "H",
                   "N"
                 )
      ),
      y = Loans,
      x = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    )
  )+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::comma,
                     breaks = c(500,
                                1000,
                                2500,
                                5000,
                                10000),
                     trans = scales::sqrt_trans(),
                     limits = c(0,12000),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Number of loans\n(note: axis in square root scale)",
    title = "Number of loans by MDI ownership, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_mdi,
          "3. Graphs/0.MDIType. Total loans by institution type.csv")

ggsave(total_loansggplot_byminoritystatus, 
       filename = "3. Graphs/0.MDIType. Total loans by institution type.pdf",
       width = 10,
       height = 6)
ggsave(total_loansggplot_byminoritystatus, 
       filename = "3. Graphs/0.MDIType. Total loans by institution type.jpg",
       width = 10,
       height = 6)

total_loansggplot_byminoritystatus_byrace <- minority_race_mdi %>% 
  group_by(`Minority Status`, Year) %>% 
  mutate(Loans = Loans/sum(Loans)) %>% 
  ggplot(
    aes(
      x = factor(`Minority Status`,
                    levels = c(
                      "A",
                      "B",
                      "H",
                      "N"
                    )
      ),
      y = Loans,
      fill = Race
    )
  )+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")
  ),
  scales = "free")+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::comma,
                     breaks = c(0.01,
                                0.05,
                                .10,
                                .25,
                                .50,
                                .75,
                                1),
                     trans = scales::sqrt_trans(),
                     limits = c(0,1.000000001),
                     expand = c(0, 0)
  ) +
  coord_flip()+
  labs(
    x = "",
    y = "Percent of loans\n(note: axis in square root scale)",
    title = "Percent of loans by race by MDI ownership, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_race_mdi %>% 
            group_by(`Minority Status`, Year) %>% 
            mutate(Loans = Loans/sum(Loans)),
          "3. Graphs/0.MDIType by race. Total loans by institution type.csv")

ggsave(total_loansggplot_byminoritystatus_byrace, 
       filename = "3. Graphs/0.MDIType by race. Total loans by institution type.pdf",
       width = 10,
       height = 6)
ggsave(total_loansggplot_byminoritystatus_byrace, 
       filename = "3. Graphs/0.MDIType by race. Total loans by institution type.jpg",
       width = 10,
       height = 6)

#########################################################
#1
#########################################################
loans_incomeggplot <- total_loans %>% 
  select(type,
         Year,
         `0-20th income percentile`,
         `20-40th`,
         `40-60th`,
         `60-80th`,
         `80-100th`,
         `Income data missing`
  ) %>% 
  pivot_longer(-c(type,Year), names_to = "Income", values_to = "loans") %>%
  group_by(type, Year) %>% 
  mutate(loans = loans/sum(loans)) %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 ) 
      ),
      y = loans,
      fill = Income 
      )
    )+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_x_discrete(limits = rev)+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")),
             scales = "free")+
  #coord_flip()+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(
    trans = 'S_sqrt',
    breaks = c(
      0.01,
      0.05,
      0.1,
      0.2,
      0.35,
      0.5),
    labels = scales::percent,
    limits = c(0,0.501),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percentage of loans by income\n(note: axis in square root scale)",
    title = "Income of borrowers by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(total_loans %>% 
            select(type,
                   Year,
                   `0-20th income percentile`,
                   `20-40th`,
                   `40-60th`,
                   `60-80th`,
                   `80-100th`,
                   `Income data missing`
            ) %>% 
            pivot_longer(-c(type,Year), names_to = "Income", values_to = "loans") %>%
            group_by(type, Year) %>% 
            mutate(loans = loans/sum(loans)),
          '3. Graphs/1. Income by institution type.csv'
          )

ggsave(loans_incomeggplot, 
       filename = "3. Graphs/1. Income by institution type.pdf",
       width = 10,
       height = 6)
ggsave(loans_incomeggplot, 
       filename = "3. Graphs/1. Income by institution type.jpg",
       width = 10,
       height = 6)

loans_incomeraceggplot <- race_loans %>% 
  select(type,
         Race,
         Year,
         `0-20th income percentile`,
         `20-40th`,
         `40-60th`,
         `60-80th`,
         `80-100th`,
         `Income data missing`
  ) %>% 
  pivot_longer(-c(type,Year,Race), names_to = "Income", values_to = "loans") %>%
  group_by(type, Year, Race) %>% 
  mutate(loans = loans/sum(loans, na.rm = T)) %>% 
  filter(Year==2022) %>% 
  ggplot(
    aes(
      fill = Income,
      y = loans,
      x =Race 
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  #scale_x_discrete(limits = rev)+
  facet_wrap(~factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 ) 
      ),
             scales = "free")+
  coord_flip()+
  scale_fill_manual(
    values = c(
      "light gray",
      "red",
      "blue",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(
    trans = 'S_sqrt',
    breaks = c(
      0.01,
      0.05,
      0.1,
      0.2,
      0.35,
      0.5),
    labels = scales::percent,
    limits = c(0,0.501),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percentage of loans by income\n(note: axis in square root scale)",
    title = "Income of borrowers by institution type in 2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(race_loans %>% 
            select(type,
                   Race,
                   Year,
                   `0-20th income percentile`,
                   `20-40th`,
                   `40-60th`,
                   `60-80th`,
                   `80-100th`,
                   `Income data missing`
            ) %>% 
            pivot_longer(-c(type,Year,Race), names_to = "Income", values_to = "loans") %>%
            group_by(type, Year, Race) %>% 
            mutate(loans = loans/sum(loans, na.rm = T)) %>% 
            filter(Year==2022),
          "3. Graphs/1.Race Income by institution type.csv"
          )

ggsave(loans_incomeraceggplot, 
       filename = "3. Graphs/1.Race Income by institution type.pdf",
       width = 10,
       height = 6)
ggsave(loans_incomeraceggplot, 
       filename = "3. Graphs/1.Race Income by institution type.jpg",
       width = 10,
       height = 6)

loans_income_minorityggplot <- minority_mdi %>% 
  select(
         `Minority Status`,
         Year,
         `0-20th income percentile`,
         `20-40th`,
         `40-60th`,
         `60-80th`,
         `80-100th`,
         `Income data missing`
  ) %>% 
  pivot_longer(-c(Year,`Minority Status`), names_to = "Income", values_to = "loans") %>%
  group_by( Year, `Minority Status`) %>% 
  mutate(loans = loans/sum(loans, na.rm = T)) %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = loans,
      fill = Income
      )
    )+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  #scale_x_discrete(limits = rev)+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")),
             scales = "free")+
  scale_fill_manual(
    values = c(
      "light gray",
      "red",
      "blue",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(
    trans = 'S_sqrt',
     breaks = c(
       0.01,
       0.05,
       0.1,
       0.2,
       0.3,
       0.4),
    labels = scales::percent,
    limits = c(0,.41),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percentage of loans by income\n(note: axis in square root scale)",
    title = "Income of borrowers by MDI type",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_mdi %>% 
            select(
              `Minority Status`,
              Year,
              `0-20th income percentile`,
              `20-40th`,
              `40-60th`,
              `60-80th`,
              `80-100th`,
              `Income data missing`
            ) %>% 
            pivot_longer(-c(Year,`Minority Status`), names_to = "Income", values_to = "loans") %>%
            group_by( Year, `Minority Status`) %>% 
            mutate(loans = loans/sum(loans, na.rm = T)),
          "3. Graphs/1.MDItype Income by institution type.csv"
          )
ggsave(loans_income_minorityggplot, 
       filename = "3. Graphs/1.MDItype Income by institution type.pdf",
       width = 10,
       height = 6)
ggsave(loans_income_minorityggplot, 
       filename = "3. Graphs/1.MDItype Income by institution type.jpg",
       width = 10,
       height = 6)

loans_incomerace_minorityggplot <- minority_race_mdi %>% 
  select(`Minority Status`,
         Race,
         Year,
         `0-20th income percentile`,
         `20-40th`,
         `40-60th`,
         `60-80th`,
         `80-100th`,
         `Income data missing`
  ) %>% 
  pivot_longer(-c(`Minority Status`,Year,Race), names_to = "Income", values_to = "loans") %>%
  group_by(`Minority Status`, Year, Race) %>% 
  mutate(loans = loans/sum(loans, na.rm = T)) %>% 
  filter(Year==2022) %>% 
  ggplot(
    aes(
      fill = Income,
      y = loans,
      x =Race 
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  #scale_x_discrete(limits = rev)+
  facet_wrap(~`Minority Status`,
             scales = "free")+
  coord_flip()+
  scale_fill_manual(
    values = c(
      "light gray",
      "red",
      "blue",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(
    trans = 'S_sqrt',
    breaks = c(
      0.01,
      .05,
      0.1,
      0.25,
      0.5,
      .75,
      1),
    labels = scales::percent,
    limits = c(0,1.0001),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percentage of loans by income\n(note: axis in square root scale)",
    title = "Income of borrowers by borrower race by MDI type in 2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_race_mdi %>% 
            select(`Minority Status`,
                   Race,
                   Year,
                   `0-20th income percentile`,
                   `20-40th`,
                   `40-60th`,
                   `60-80th`,
                   `80-100th`,
                   `Income data missing`
            ) %>% 
            pivot_longer(-c(`Minority Status`,Year,Race), names_to = "Income", values_to = "loans") %>%
            group_by(`Minority Status`, Year, Race) %>% 
            mutate(loans = loans/sum(loans, na.rm = T)) %>% 
            filter(Year==2022),
          "3. Graphs/1.MDItype by Race Income by institution type.csv"
          )
ggsave(loans_incomerace_minorityggplot, 
       filename = "3. Graphs/1.MDItype by Race Income by institution type.pdf",
       width = 10,
       height = 6)
ggsave(loans_incomerace_minorityggplot, 
       filename = "3. Graphs/1.MDItype by Race Income by institution type.jpg",
       width = 10,
       height = 6)
#########################################################
#2
#########################################################
total_loandollarsggplot <- total_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = `Total loan dollars`/1000000,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = c("5,000",
                                "25,000",
                                "100,000",
                                "250,000",
                                "1,000,000",
                                "1,000,000"),
                     breaks = c(5000,
                                25000,
                                100000,
                                250000,
                                1000000,
                                2000000),
                     trans = scales::sqrt_trans(),
                     limits = c(0,2000001),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Loan dollars (in millions)",
    title = "Loan dollars by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(total_loans,
          "3. Graphs/2. Total loan dollars by institution type.csv"
          )

ggsave(total_loandollarsggplot, 
       filename = "3. Graphs/2. Total loan dollars by institution type.pdf",
       width = 10,
       height = 6)
ggsave(total_loandollarsggplot, 
       filename = "3. Graphs/2. Total loan dollars by institution type.jpg",
       width = 10,
       height = 6)

race_loandollarsggplot <- race_loans %>% 
  group_by(type, Year) %>% 
  mutate(`Total loan dollars` = `Total loan dollars`/sum(`Total loan dollars`)) %>% 
  ungroup()%>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = `Total loan dollars`,
      fill = Race))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
  ),
  scales = "free"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                                0.01,
                                0.05,
                                0.1,
                                0.25,
                                0.5,
                                0.75),
                     trans = scales::sqrt_trans(),
                     limits = c(0,.8),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of loan dollars",
    title = "Percent of loan dollars by race by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(race_loans %>% 
            group_by(type, Year) %>% 
            mutate(`Total loan dollars` = `Total loan dollars`/sum(`Total loan dollars`)),
          '3. Graphs/2.Race Total loan dollars by institution type.csv'
          )

ggsave(race_loandollarsggplot, 
       filename = "3. Graphs/2.Race Total loan dollars by institution type.pdf",
       width = 10,
       height = 6)
ggsave(race_loandollarsggplot, 
       filename = "3. Graphs/2.Race Total loan dollars by institution type.jpg",
       width = 10,
       height = 6)

total_loandollars_mdiggplot <- minority_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = `Total loan dollars`/1000000,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::dollar,
                     breaks = c(10,
                                300,
                                1000,
                                3000,
                                6000),
                     trans = scales::sqrt_trans(),
                     limits = c(0,6100),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Loan dollars (in millions)",
    title = "Loan dollars by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_mdi,
          "3. Graphs/2.MDItype Total loan dollars by institution type.csv")

ggsave(total_loandollars_mdiggplot, 
       filename = "3. Graphs/2.MDItype Total loan dollars by institution type.pdf",
       width = 10,
       height = 6)
ggsave(total_loandollars_mdiggplot, 
       filename = "3. Graphs/2.MDItype Total loan dollars by institution type.jpg",
       width = 10,
       height = 6)

race_loandollars_mdiggplot <- minority_race_mdi %>% 
  group_by(`Minority Status`, Year) %>% 
  mutate(`Total loan dollars` = `Total loan dollars`/sum(`Total loan dollars`)) %>% 
  ungroup()%>% 
  ggplot(
    aes(
      x =`Minority Status`,
      y = `Total loan dollars`,
      fill = Race))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")
  ),
  scales = "free"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       0.01,
                       0.05,
                       0.1,
                       0.25,
                       0.5,
                       0.75),
                     trans = scales::sqrt_trans(),
                     limits = c(0,.8),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of loan dollars",
    title = "Percent of loan dollars by race by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_race_mdi %>% 
            group_by(`Minority Status`, Year) %>% 
            mutate(`Total loan dollars` = `Total loan dollars`/sum(`Total loan dollars`)) %>% 
            ungroup(),
          "3. Graphs/2.MDItype by race Total loan dollars by institution type.csv"
          )

ggsave(race_loandollars_mdiggplot, 
       filename = "3. Graphs/2.MDItype by race Total loan dollars by institution type.pdf",
       width = 10,
       height = 6)
ggsave(race_loandollars_mdiggplot, 
       filename = "3. Graphs/2.MDItype by race Total loan dollars by institution type.jpg",
       width = 10,
       height = 6)
#########################################################
#3
#########################################################
median_loansggplot <- total_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = `Median loan`,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::dollar,
                     breaks = c(
                                175000,
                                250000,
                                325000,
                                400000),
                     
                     limits = c(0,400001),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Median loans",
    title = "Median loan by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(total_loans,
          "3. Graphs/3. Median loan dollars by institution type.csv")

ggsave(median_loansggplot, 
       filename = "3. Graphs/3. Median loan dollars by institution type.pdf",
       width = 10,
       height = 6)
ggsave(median_loansggplot, 
       filename = "3. Graphs/3. Median loan dollars by institution type.jpg",
       width = 10,
       height = 6)

median_loans_by_raceggplot <- race_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = `Median loan`,
      fill = Race))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")),
             scales = "free"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::dollar,
                     breaks = c(
                       100000,
                       200000,
                       300000,
                       400000,
                       500000,
                       600000,
                       700000),
                     
                     limits = c(0,700001),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Median loans",
    title = "Median loan by race by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(race_loans,
          "3. Graphs/3.Race Median loan dollars by institution type.csv")

ggsave(median_loans_by_raceggplot, 
       filename = "3. Graphs/3.Race Median loan dollars by institution type.pdf",
       width = 10,
       height = 6)
ggsave(median_loans_by_raceggplot, 
       filename = "3. Graphs/3.Race Median loan dollars by institution type.jpg",
       width = 10,
       height = 6)

median_loans_mdiggplot <- minority_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = `Median loan`,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::dollar,
                     breaks = c(
                       100000,
                       200000,
                       300000,
                       400000,
                       500000),
                     
                     limits = c(0,500001),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Median loans",
    title = "Median loan by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_mdi,
          '3. Graphs/3.MDItype Median loan dollars by institution type.csv')

ggsave(median_loans_mdiggplot, 
       filename = "3. Graphs/3.MDItype Median loan dollars by institution type.pdf",
       width = 10,
       height = 6)
ggsave(median_loans_mdiggplot, 
       filename = "3. Graphs/3.MDItype Median loan dollars by institution type.jpg",
       width = 10,
       height = 6)

median_loans_by_mdi_raceggplot <- minority_race_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = `Median loan`,
      fill = Race))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")),
             scales = "free"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::dollar,
                     breaks = c(
                       100000,
                       250000,
                       500000,
                       1000000,
                       2500000),
                     trans = 'S_sqrt',
                     
                     limits = c(0,2500001),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Median loans\n(note: axis in square root scale)",
    title = "Median loan by race by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_race_mdi,
          "3. Graphs/3.MDItype by race Median loan dollars by institution type.csv")
ggsave(median_loans_by_mdi_raceggplot, 
       filename = "3. Graphs/3.MDItype by race Median loan dollars by institution type.pdf",
       width = 10,
       height = 6)
ggsave(median_loans_by_mdi_raceggplot, 
       filename = "3. Graphs/3.MDItype by race Median loan dollars by institution type.jpg",
       width = 10,
       height = 6)
#########################################################
#4
#########################################################
denial_ratesggplot <- total_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = Denial,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(
                     breaks = c(0.05,
                                0.075,
                                0.1,
                                0.125,
                                0.15,
                                0.175,
                                0.2,
                                0.225),
                     labels = scales::percent,
                     limits = c(0,0.2251),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial percentage",
    title = "Denial rate by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(total_loans,
          "3. Graphs/4. Denial rate by institution type.csv")

ggsave(denial_ratesggplot, 
       filename = "3. Graphs/4. Denial rate by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_ratesggplot, 
       filename = "3. Graphs/4. Denial rate by institution type.jpg",
       width = 10,
       height = 6)

denial_rates_raceggplot <- race_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = Denial,
      fill = Race
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")),
             scales = "free"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(
    breaks = c(
               0.1,
               0.2,
               0.3,
               0.4,
               0.5),
    labels = scales::percent,
    limits = c(0,0.5),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial percentage",
    title = "Denial rate by race by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(race_loans,
          "3. Graphs/4.Race. Denial rate by institution type.csv")

ggsave(denial_rates_raceggplot, 
       filename = "3. Graphs/4.Race. Denial rate by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_rates_raceggplot, 
       filename = "3. Graphs/4.Race. Denial rate by institution type.jpg",
       width = 10,
       height = 6)

denial_rates_minorityggplot <- minority_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = Denial,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(
    breaks = c(0.01,
               0.05,
               0.1,
               0.15,
               0.20,
               0.25),
    labels = scales::percent,
    limits = c(0,0.2501),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial percentage",
    title = "Denial rate by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_mdi,
          '3. Graphs/4.MDItype Denial rate by institution type.csv')

ggsave(denial_rates_minorityggplot, 
       filename = "3. Graphs/4.MDItype Denial rate by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_rates_minorityggplot, 
       filename = "3. Graphs/4.MDItype Denial rate by institution type.jpg",
       width = 10,
       height = 6)

denial_rates_race_mdiggplot <- minority_race_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = Denial,
      fill = Race
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")),
             scales = "free"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(
    breaks = c(
      0.1,
      0.25,
      0.5,
      0.75),
    labels = scales::percent,
    limits = c(0,0.81),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial percentage",
    title = "Denial rate by race by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_race_mdi,
          '3. Graphs/4.MDItype by race. Denial rate by institution type.csv')

ggsave(denial_rates_race_mdiggplot, 
       filename = "3. Graphs/4.MDItype by race. Denial rate by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_rates_race_mdiggplot, 
       filename = "3. Graphs/4.MDItype by race. Denial rate by institution type.jpg",
       width = 10,
       height = 6)
#########################################################
#5
#########################################################
denial_rates_incomeggplot <- total_loans %>% 
  select(type,
         Year,
         `Denied: 0-20th income percentile`,
         `Denied: 20-40th`,
         `Denied: 40-60th`,
         `Denied: 60-80th`,
         `Denied: 80-100th`,
         `Denied: Income data missing`
  ) %>% 
  pivot_longer(-c(type,Year), names_to = "Income", values_to = "Denial") %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 ) 
      ),
      y = Denial,
      fill = Income
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")
  ),
             scales = "free")+
  #coord_flip()+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous( 
    trans = 'S_sqrt',
    breaks = c(0.01,
               0.05,
               0.10,
               0.20,
               0.35,
               0.5),
    labels = scales::percent,
    limits = c(0,0.7),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial percentage\n(note: axis in square root scale)",
    title = "Denial rate by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(total_loans %>% 
            select(type,
                   Year,
                   `Denied: 0-20th income percentile`,
                   `Denied: 20-40th`,
                   `Denied: 40-60th`,
                   `Denied: 60-80th`,
                   `Denied: 80-100th`,
                   `Denied: Income data missing`
            ) %>% 
            pivot_longer(-c(type,Year), names_to = "Income", values_to = "Denial") ,
          "3. Graphs/5. Denial rate by income by institution type.csv")

ggsave(denial_rates_incomeggplot, 
       filename = "3. Graphs/5. Denial rate by income by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_rates_incomeggplot, 
       filename = "3. Graphs/5. Denial rate by income by institution type.jpg",
       width = 10,
       height = 6)

denial_rates_income_raceggplot <- race_loans %>% 
  select(type,
         Year,
         Race,
         `Denied: 0-20th income percentile`,
         `Denied: 20-40th`,
         `Denied: 40-60th`,
         `Denied: 60-80th`,
         `Denied: 80-100th`,
         `Denied: Income data missing`
  ) %>% 
  pivot_longer(-c(type,Year, Race), names_to = "Income", values_to = "Denial") %>%
  filter(Year ==2022) %>% 
  ggplot(
    aes(
      x = Race,
      y = Denial,
      fill = Income ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_x_discrete(limits = rev)+
  facet_wrap(~factor(type,
                     levels = c(
                       "MDI",
                       "nonMDI",
                       "CDFI",
                       "Community",
                       "Top 25",
                       "Fintech",
                       "Credit union"
                     ) 
  ),
             scales = "free")+
  coord_flip()+
  scale_fill_manual(
    limits = rev,
    guide = guide_legend(reverse = T),
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous( 
    trans = 'S_sqrt',
    breaks = c(
               0.01,
               0.05,
               0.1,
               0.25,
               0.5,
               0.75),
    labels = scales::percent,
    limits = c(0,0.9),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial percentage\n(note: axis in square root scale)",
    title = "Denial rate by race by institution type, 2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(race_loans %>% 
            select(type,
                   Year,
                   Race,
                   `Denied: 0-20th income percentile`,
                   `Denied: 20-40th`,
                   `Denied: 40-60th`,
                   `Denied: 60-80th`,
                   `Denied: 80-100th`,
                   `Denied: Income data missing`
            ) %>% 
            pivot_longer(-c(type,Year, Race), names_to = "Income", values_to = "Denial") %>%
            filter(Year ==2022),
          "3. Graphs/5.Race. Denial rate by income by institution type.csv")

ggsave(denial_rates_income_raceggplot, 
       filename = "3. Graphs/5.Race. Denial rate by income by institution type.pdf",
       width = 15,
       height = 8)
ggsave(denial_rates_income_raceggplot, 
       filename = "3. Graphs/5.Race. Denial rate by income by institution type.jpg",
       width = 15,
       height = 8)

denial_rates_income_mdiggplot <- minority_mdi %>% 
  select(`Minority Status`,
         Year,
         `Denied: 0-20th income percentile`,
         `Denied: 20-40th`,
         `Denied: 40-60th`,
         `Denied: 60-80th`,
         `Denied: 80-100th`,
         `Denied: Income data missing`
  ) %>% 
  pivot_longer(-c(`Minority Status`,Year), names_to = "Income", values_to = "Denial") %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = Denial,
      fill = Income
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_x_discrete(limits = rev)+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")
  ),
             scales = "free")+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous( 
    trans = 'S_sqrt',
    breaks = c(0.01,
               .05,
               0.10,
               0.25,
               0.5,
               0.75),
    labels = scales::percent,
    limits = c(0,0.85),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial percentage\n(note: axis in square root scale)",
    title = "Denial rate by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_mdi %>% 
            select(`Minority Status`,
                   Year,
                   `Denied: 0-20th income percentile`,
                   `Denied: 20-40th`,
                   `Denied: 40-60th`,
                   `Denied: 60-80th`,
                   `Denied: 80-100th`,
                   `Denied: Income data missing`
            ) %>% 
            pivot_longer(-c(`Minority Status`,Year), names_to = "Income", values_to = "Denial"),
          "3. Graphs/5.MDItype Denial rate by income by institution type.csv")

ggsave(denial_rates_income_mdiggplot, 
       filename = "3. Graphs/5.MDItype Denial rate by income by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_rates_income_mdiggplot, 
       filename = "3. Graphs/5.MDItype Denial rate by income by institution type.jpg",
       width = 10,
       height = 6)

denial_rates_income_race_mdiggplot <- minority_race_mdi %>% 
  select(`Minority Status`,
         Year,
         Race,
         `Denied: 0-20th income percentile`,
         `Denied: 20-40th`,
         `Denied: 40-60th`,
         `Denied: 60-80th`,
         `Denied: 80-100th`,
         `Denied: Income data missing`
  ) %>% 
  pivot_longer(-c(`Minority Status`,Year, Race), names_to = "Income", values_to = "Denial") %>%
  filter(Year ==2022) %>% 
  ggplot(
    aes(
      fill =Race,
      y = Denial,
      x = Income))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_x_discrete(limits = rev)+
  facet_wrap(~`Minority Status`,
             scales = "free")+
  coord_flip()+
  scale_fill_manual(
    limits = rev,
    guide = guide_legend(reverse = T),
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous( 
    trans = 'S_sqrt',
    breaks = c(
      0.01,
      0.05,
      0.1,
      0.25,
      0.5,
      0.75,
      1),
    labels = scales::percent,
    limits = c(0,1.0001),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial percentage\n(note: axis in square root scale)",
    title = "Denial rate by race by MDI type, 2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_race_mdi %>% 
            select(`Minority Status`,
                   Year,
                   Race,
                   `Denied: 0-20th income percentile`,
                   `Denied: 20-40th`,
                   `Denied: 40-60th`,
                   `Denied: 60-80th`,
                   `Denied: 80-100th`,
                   `Denied: Income data missing`
            ) %>% 
            pivot_longer(-c(`Minority Status`,Year, Race), names_to = "Income", values_to = "Denial") %>%
            filter(Year ==2022),
          "3. Graphs/5.MDItype by race. Denial rate by income by institution type.csv")

ggsave(denial_rates_income_race_mdiggplot, 
       filename = "3. Graphs/5.MDItype by race. Denial rate by income by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_rates_income_race_mdiggplot, 
       filename = "3. Graphs/5.MDItype by race. Denial rate by income by institution type.jpg",
       width = 10,
       height = 6)
#########################################################
#6
#########################################################
denial_reasonsggplot <- total_loans %>% 
  select(type,
         Year,
         DRCash,
         DRCH,
         DRCollat,
         DRD2I,
         DREH,
         DRMID,
         DRother
  ) %>% 
  pivot_longer(-c(type,Year), names_to = "Reason", values_to = "Denial") %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 ) 
      ),
      y = Denial,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_x_discrete(limits = rev)+
  facet_wrap(~Reason,
             scales = "free")+
  coord_flip()+
  scale_fill_manual(
    limits = rev,
    guide = guide_legend(reverse = T),
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous( 
    trans = 'S_sqrt',
    breaks = c(0.001,
               0.02,
               0.1,
               0.2,
               0.35,
               0.5),
    labels = scales::percent,
    limits = c(0,0.501),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial reason\n(note: axis in square root scale)",
    title = "Denial reason given by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data\n(Note: institutions may list multiple reasons for denial")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(total_loans %>% 
            select(type,
                   Year,
                   DRCash,
                   DRCH,
                   DRCollat,
                   DRD2I,
                   DREH,
                   DRMID,
                   DRother
            ) %>% 
            pivot_longer(-c(type,Year), names_to = "Reason", values_to = "Denial"),
          "3. Graphs/6. Denial reason by institution type.csv"
          )
ggsave(denial_reasonsggplot, 
       filename = "3. Graphs/6. Denial reason by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_reasonsggplot, 
       filename = "3. Graphs/6. Denial reason by institution type.jpg",
       width = 10,
       height = 6)

denial_reasons_raceggplot <- race_loans %>% 
  select(type,
         Race,
         Year,
         DRCash,
         DRCH,
         DRCollat,
         DRD2I,
         DREH,
         DRMID,
         DRother
  ) %>% 
  pivot_longer(-c(type,Year, Race), names_to = "Reason", values_to = "Denial") %>% 
  filter(Year == 2022) %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 ) 
      ),
      y = Denial,
      fill = Race
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_x_discrete(limits = rev)+
  facet_wrap(~Reason,
             scales = "free")+
  coord_flip()+
  scale_fill_manual(
    limits = rev,
    guide = guide_legend(reverse = T),
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous( 
    trans = 'S_sqrt',
    breaks = c(0.001,
               0.02,
               0.1,
               0.2,
               0.35,
               0.5),
    labels = scales::percent,
    limits = c(0,0.6),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial reason\n(note: axis in square root scale)",
    title = "Denial reason given by institution type, in 2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data\n(Note: institutions may list multiple reasons for denial")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(race_loans %>% 
            select(type,
                   Race,
                   Year,
                   DRCash,
                   DRCH,
                   DRCollat,
                   DRD2I,
                   DREH,
                   DRMID,
                   DRother
            ) %>% 
            pivot_longer(-c(type,Year, Race), names_to = "Reason", values_to = "Denial") %>% 
            filter(Year == 2022),
          "3. Graphs/6.Race Denial reason by institution type.csv")

ggsave(denial_reasons_raceggplot, 
       filename = "3. Graphs/6.Race Denial reason by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_reasons_raceggplot, 
       filename = "3. Graphs/6.Race Denial reason by institution type.jpg",
       width = 10,
       height = 6)

denial_reasons_mdiggplot <- minority_mdi %>% 
  select(`Minority Status`,
         Year,
         DRCash,
         DRCH,
         DRCollat,
         DRD2I,
         DREH,
         DRMID,
         DRother
  ) %>% 
  pivot_longer(-c(`Minority Status`,Year), names_to = "Reason", values_to = "Denial") %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = Denial,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_x_discrete(limits = rev)+
  facet_wrap(~Reason,
             scales = "free")+
  coord_flip()+
  scale_fill_manual(
    limits = rev,
    guide = guide_legend(reverse = T),
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous( 
    trans = 'S_sqrt',
    breaks = c(0.01,
               0.05,
               0.2,
               0.35,
               0.5,
               0.65),
    labels = scales::percent,
    limits = c(0,0.7),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial reason\n(note: axis in square root scale)",
    title = "Denial reason given by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data\n(Note: institutions may list multiple reasons for denial")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_mdi %>% 
            select(`Minority Status`,
                   Year,
                   DRCash,
                   DRCH,
                   DRCollat,
                   DRD2I,
                   DREH,
                   DRMID,
                   DRother
            ) %>% 
            pivot_longer(-c(`Minority Status`,Year), names_to = "Reason", values_to = "Denial"),
          "3. Graphs/6.MDItype Denial reason by institution type.csv")
ggsave(denial_reasons_mdiggplot, 
       filename = "3. Graphs/6.MDItype Denial reason by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_reasons_mdiggplot, 
       filename = "3. Graphs/6.MDItype Denial reason by institution type.jpg",
       width = 10,
       height = 6)

denial_reasons_race_mdiggplot <- minority_race_mdi %>% 
  select(`Minority Status`,
         Race,
         Year,
         DRCash,
         DRCH,
         DRCollat,
         DRD2I,
         DREH,
         DRMID,
         DRother
  ) %>% 
  pivot_longer(-c(`Minority Status`,Year, Race), names_to = "Reason", values_to = "Denial") %>% 
  filter(Year == 2022) %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = Denial,
      fill = Race
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_x_discrete(limits = rev)+
  facet_wrap(~Reason,
             scales = "free")+
  coord_flip()+
  scale_fill_manual(
    limits = rev,
    guide = guide_legend(reverse = T),
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous( 
    trans = 'S_sqrt',
    breaks = c(0.01,
               0.05,
               0.1,
               0.25,
               0.5,
               .75,
               1),
    labels = scales::percent,
    limits = c(0,1.0001),
    expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Denial reason\n(note: axis in square root scale)",
    title = "Denial reason given by MDI type by race, 2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data\n(Note: institutions may list multiple reasons for denial")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_race_mdi %>% 
            select(`Minority Status`,
                   Race,
                   Year,
                   DRCash,
                   DRCH,
                   DRCollat,
                   DRD2I,
                   DREH,
                   DRMID,
                   DRother
            ) %>% 
            pivot_longer(-c(`Minority Status`,Year, Race), names_to = "Reason", values_to = "Denial") %>% 
            filter(Year == 2022),
          "3. Graphs/6.MDItype by race Denial reason by institution type.csv")

ggsave(denial_reasons_race_mdiggplot, 
       filename = "3. Graphs/6.MDItype by race Denial reason by institution type.pdf",
       width = 10,
       height = 6)
ggsave(denial_reasons_race_mdiggplot, 
       filename = "3. Graphs/6.MDItype by race Denial reason by institution type.jpg",
       width = 10,
       height = 6)
#########################################################
#7
#########################################################
interest_rateggplot <- total_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = `Median Interest Rate`/100,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .01,
                       .02,
                       .025,
                       .03,
                       .035,
                       .04,
                       .045,
                       .05,
                       .055),
                     
                     limits = c(0,.0551),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Median interest rate",
    title = "Median interest rate by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(total_loans,
          "3. Graphs/7.Interest Rate by institution type.csv")

ggsave(interest_rateggplot, 
       filename = "3. Graphs/7.Interest Rate by institution type.pdf",
       width = 10,
       height = 6)
ggsave(interest_rateggplot, 
       filename = "3. Graphs/7. Interest rate by institution type.jpg",
       width = 10,
       height = 6)

interest_rate_raceggplot <- race_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = `Median Interest Rate`/100,
      fill = Race
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")
  ),
  scales = "free")+
    
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .01,
                       .02,
                       .025,
                       .03,
                       .035,
                       .04,
                       .045,
                       .05,
                       .055),
                     
                     limits = c(0,.0565),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Median interest rate",
    title = "Median interest rate by race institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(race_loans,
          "3. Graphs/7.RaceInterest Rate by institution type.csv")

ggsave(interest_rate_raceggplot, 
       filename = "3. Graphs/7.RaceInterest Rate by institution type.pdf",
       width = 10,
       height = 6)
ggsave(interest_rate_raceggplot, 
       filename = "3. Graphs/7.Race Interest rate by institution type.jpg",
       width = 10,
       height = 6)

interest_rate_mdiggplot <- minority_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = `Median Interest Rate`/100,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .01,
                       .02,
                       .03,
                       .04,
                       .05,
                       .06,
                       .075),
                     
                     limits = c(0,.07501),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Median interest rate",
    title = "Median interest rate by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_mdi,
          "3. Graphs/7.MDItype Interest Rate by institution type.csv")

ggsave(interest_rate_mdiggplot, 
       filename = "3. Graphs/7.MDItype Interest Rate by institution type.pdf",
       width = 10,
       height = 6)
ggsave(interest_rate_mdiggplot, 
       filename = "3. Graphs/7.MDItype Interest rate by institution type.jpg",
       width = 10,
       height = 6)

interest_rate_race_mdiggplot <- minority_race_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = `Median Interest Rate`/100,
      fill = Race
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")
  ),
  scales = "free")+
  
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .01,
                       .02,
                       .03,
                       .04,
                       .05,
                       .06,
                       .075),
                     limits = c(0,0.08),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Median interest rate",
    title = "Median interest rate by race by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_race_mdi,
          "3. Graphs/7.MDItype by race Interest Rate by institution type.csv")

ggsave(interest_rate_race_mdiggplot, 
       filename = "3. Graphs/7.MDItype by race Interest Rate by institution type.pdf",
       width = 10,
       height = 6)
ggsave(interest_rate_race_mdiggplot, 
       filename = "3. Graphs/7.MDItype by race Interest rate by institution type.jpg",
       width = 10,
       height = 6)
#########################################################
#8
#########################################################
majority_minorityggplot <- total_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = `Percent majority minority`,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .1,
                       .2,
                       .3,
                       .4,
                       .5),
                     limits = c(0,.51),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of neighborhoods served\nthat are majority minority",
    title = "Majority minority neighborhoods served by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(total_loans,
          '3. Graphs/8.Majmin neighborhoods by institution type.csv')

ggsave(majority_minorityggplot, 
       filename = "3. Graphs/8.Majmin neighborhoods by institution type.pdf",
       width = 10,
       height = 6)
ggsave(majority_minorityggplot, 
       filename = "3. Graphs/8.Majmin neighborhoods by institution type.jpg",
       width = 10,
       height = 6)

majority_minority_raceggplot <- race_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = `Percent majority minority`,
      fill = Race
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")
  ),
  scales = "free")+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .15,
                       .3,
                       .45,
                       .6,
                       .75),
                     limits = c(0,.85),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of neighborhoods served\nthat are majority minority",
    title = "Majority minority neighborhoods served by race by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(race_loans,
          '3. Graphs/8.Race Majmin neighborhoods by institution type.csv')

ggsave(majority_minority_raceggplot, 
       filename = "3. Graphs/8.Race Majmin neighborhoods by institution type.pdf",
       width = 10,
       height = 6)
ggsave(majority_minority_raceggplot, 
       filename = "3. Graphs/8.Race Majmin neighborhoods by institution type.jpg",
       width = 10,
       height = 6)

majority_minority_mdiggplot <- minority_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = `Percent majority minority`,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .2,
                       .4,
                       .6,
                       .8,
                       1),
                     limits = c(0,1.0001),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of neighborhoods served\nthat are majority minority",
    title = "Majority minority neighborhoods served by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_mdi,
          '3. Graphs/8.MDItype Majmin neighborhoods by institution type.csv')

ggsave(majority_minority_mdiggplot, 
       filename = "3. Graphs/8.MDItype Majmin neighborhoods by institution type.pdf",
       width = 10,
       height = 6)
ggsave(majority_minority_mdiggplot, 
       filename = "3. Graphs/8.MDItype Majmin neighborhoods by institution type.jpg",
       width = 10,
       height = 6)


majority_minority_race_mdiggplot <- minority_race_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = `Percent majority minority`,
      fill = Race
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")
  ),
  scales = "free")+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .25,
                       .5,
                       .75,
                       1),
                     limits = c(0,1.00001),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of neighborhoods served\nthat are majority minority",
    title = "Majority minority neighborhoods served by race by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_race_mdi,
          '3. Graphs/8.MDItype by race Majmin neighborhoods by institution type.csv')

ggsave(majority_minority_race_mdiggplot, 
       filename = "3. Graphs/8.MDItype by race Majmin neighborhoods by institution type.pdf",
       width = 10,
       height = 6)
ggsave(majority_minority_race_mdiggplot, 
       filename = "3. Graphs/8.MDItype by race Majmin neighborhoods by institution type.jpg",
       width = 10,
       height = 6)

#########################################################
#9
#########################################################

lmi_ggplot <- total_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = `Percent LMI`-.1,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = c("12.5%",
                                "15%",
                                "17.5%",
                                "20%"),
                     breaks = c(
                       .025,
                       .05,
                       .075,
                       .1),
                     limits = c(0,.11),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of neighborhoods served that are LMI\n(note:Y axis does not start at zero)",
    title = "LMI neighborhoods served by institution type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(total_loans,
          '3. Graphs/9.LMI neighborhoods by institution type.csv')
ggsave(lmi_ggplot, 
       filename = "3. Graphs/9.LMI neighborhoods by institution type.pdf",
       width = 10,
       height = 6)
ggsave(lmi_ggplot, 
       filename = "3. Graphs/9.LMI neighborhoods by institution type.jpg",
       width = 10,
       height = 6)

lmi_raceggplot <- race_loans %>% 
  ggplot(
    aes(
      x = factor(type,
                 levels = c(
                   "MDI",
                   "nonMDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = `Percent LMI`,
      fill = Race
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")
  ),
  scales = "free")+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .1,
                       .15,
                       .20,
                       .25,
                       .3,
                       .35),
                     limits = c(0,.351),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of neighborhoods served that are LMI",
    title = "LMI neighborhoods served by race by institution type, 2019\u00ad2022",
    fill = "Borrower Race:",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(race_loans,
          '3. Graphs/9.Race LMI neighborhoods by institution type.csv')

ggsave(lmi_raceggplot, 
       filename = "3. Graphs/9.Race LMI neighborhoods by institution type.pdf",
       width = 10,
       height = 6)
ggsave(lmi_raceggplot, 
       filename = "3. Graphs/9.Race LMI neighborhoods by institution type.jpg",
       width = 10,
       height = 6)

lmi_mdiggplot <- minority_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = `Percent LMI`,
      fill = factor(as.character(Year),
                    levels = c("2019",
                               "2020",
                               "2021",
                               "2022")
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .1,
                       .2,
                       .3,
                       .4,
                       .5),
                     limits = c(0,.51),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of neighborhoods served that are LMI",
    title = "LMI neighborhoods served by MDI type, 2019\u00ad2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_mdi,
          '3. Graphs/9.MDItype LMI neighborhoods by institution type.csv')
ggsave(lmi_mdiggplot, 
       filename = "3. Graphs/9.MDItype LMI neighborhoods by institution type.pdf",
       width = 10,
       height = 6)
ggsave(lmi_mdiggplot, 
       filename = "3. Graphs/9.MDItype LMI neighborhoods by institution type.jpg",
       width = 10,
       height = 6)

lmi_race_mdiggplot <- minority_race_mdi %>% 
  ggplot(
    aes(
      x = `Minority Status`,
      y = `Percent LMI`,
      fill = Race
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  facet_wrap(~factor(as.character(Year),
                     levels = c("2019",
                                "2020",
                                "2021",
                                "2022")
  ),
  scales = "free")+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = scales::percent,
                     breaks = c(
                       .1,
                       .2,
                       .3,
                       .4,
                       .5,
                       .6,
                       .7),
                     limits = c(0,.701),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Percent of neighborhoods served that are LMI",
    title = "LMI neighborhoods served by race by MDI type, 2019\u00ad2022",
    fill = "Borrower Race:",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(minority_race_mdi,
          '3. Graphs/9.MDItype by race LMI neighborhoods by institution type.csv')

ggsave(lmi_race_mdiggplot, 
       filename = "3. Graphs/9.MDItype by race LMI neighborhoods by institution type.pdf",
       width = 10,
       height = 6)
ggsave(lmi_race_mdiggplot, 
       filename = "3. Graphs/9.MDItype by race LMI neighborhoods by institution type.jpg",
       width = 10,
       height = 6)

#########################################################
#10 Climate
#########################################################

climate_meanggplot <- climate_mean %>% 
  select(-`...1`) %>% 
  pivot_longer(everything()) %>% 
  ggplot(
    aes(
      x = factor(name,
                 levels = c(
                   "MDI",
                   "Non-MDI",
                   "CDFI",
                   "Community",
                   "Top 25",
                   "Fintech",
                   "Credit union"
                 )
      ),
      y = value-40,
      fill = factor(name,
                   levels = c(
                     "MDI",
                     "Non-MDI",
                     "CDFI",
                     "Community",
                     "Top 25",
                     "Fintech",
                     "Credit union"
                   )
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400",
      "black"
    ))+
  scale_y_continuous(labels = c('40',
                               '45',
                               "50",
                               '55'),
                     breaks = c(
                       0,5,10,15),
                     limits = c(0,20),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Mean climate risk\n(note:Y axis does not start at zero)",
    title = "Mean climate risk by institution type, 2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(
    axis.text.x = element_text(face = 'bold'),
    panel.background = element_rect(color = NA, fill = NA),
    #face="bold" ,
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(climate_mean %>% 
            select(-`...1`) %>% 
            pivot_longer(everything()),
          '3. Graphs/10.Mean climate risk by institution type.csv')

ggsave(climate_meanggplot, 
       filename = "3. Graphs/10.Mean climate risk by institution type.pdf",
       width = 10,
       height = 6)
ggsave(climate_meanggplot, 
       filename = "3. Graphs/10.Mean climate by institution type.jpg",
       width = 10,
       height = 6)


climate_plot <- climate %>% 
  select(-`...1`) %>%
  pivot_longer(-Percentile) %>% 
  #filter(name == "MDI") %>% 
  ggplot()+
  geom_line(aes(x = Percentile,
                y = value-Percentile,
                color = name)) + 
  geom_hline(yintercept = 0) +  
  scale_color_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400",
      "pink"
    )) +
  scale_y_continuous(breaks = c(-2.5,
                                0,
                                2.5,
                                5,
                                7.5,
                                10),
                     limits = c(-2.6,10.5),
                     expand = c(0,0))+
  scale_x_continuous(expand = c(0,0),
                     breaks = c(0,10,25,50,75,90,100),
                     limits = c(-0.05,100.05))+
  labs(
    x = "Community climate risk percentile",
    y = "Institutional risk score \nminus community risk percentile",
    title = "Climate risk portfolios by institution type, 2022",
    subtitle = "FEMA scores each neighborhood on a scale from 0-100\nIn 2022, CDFIs and MDIs lent to communities with higher climate risk scores",
    color = "",
    fill = "Borrower Race:",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA and FEMA Climate Resiliancy Data\n(note: a positive number on the y axis indicates lending to \nhigher risk communities while a negative number indicates\nlending to lower risk communities)")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(climate %>% 
            select(-`...1`) %>%
            pivot_longer(-Percentile),
          "3. Graphs/10.Climate.csv")

ggsave(climate_plot, 
       filename = "3. Graphs/10.Climate.pdf",
       width = 10,
       height = 6)
ggsave(climate_plot, 
       filename = "3. Graphs/10.Climate.jpg",
       width = 10,
       height = 6)
  
climate_explainplot <- climate %>% 
  select(-`...1`) %>%
  pivot_longer(-Percentile) %>% 
  #filter(name == "MDI") %>% 
  ggplot()+
  geom_line(aes(x = Percentile,
                y = value,
                color = name)) + 
  geom_abline(slope =1, intercept = 0, linewidth = 1) +  
  scale_color_manual(
    values = c(
      "light gray",
      "blue",
      "red",
      "#0F2453",
      "#2FB3A1",
      "#FFB400",
      "pink"
    )) +
  scale_y_continuous(
                     limits = c(0,100.5),
                     expand = c(0,0))+
  scale_x_continuous(expand = c(0,0),
                     breaks = c(0,10,25,50,75,90,100),
                     limits = c(-0.05,100.05))+
  labs(
    x = "Community climate risk percentile",
    y = "Institutional risk score",
    title = "Climate risk portfolios by institution type, 2022",
    subtitle = "FEMA scores each neighborhood on a scale from 0-100\nIn 2022, CDFIs and MDIs lent to communities with higher climate risk scores",
    color = "",
    fill = "Borrower Race:",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA and FEMA Climate Resiliancy Data\n(note: a positive number on the y axis indicates lending to \nhigher risk communities while a negative number indicates\nlending to lower risk communities)")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(climate %>% 
            select(-`...1`) %>%
            pivot_longer(-Percentile),
          "3. Graphs/10.Climate explain.csv")

ggsave(climate_explainplot, 
       filename = "3. Graphs/10.Climate explain.pdf",
       width = 10,
       height = 6)
ggsave(climate_explainplot, 
       filename = "3. Graphs/10.Climate explain.jpg",
       width = 10,
       height = 6)

#TK
climate_meanMDIggplot <- climate_meanmdi %>% 
  select(-`...1`) %>% 
  pivot_longer(everything()) %>% 
  ggplot(
    aes(
      x = factor(name,
                 levels = c(
                   'AAPI',
                   'AIAN',
                   'Black',
                   'Hispanic'
                 )
      ),
      y = value-40,
      fill = factor(name,
                    levels = c(
                      'AAPI',
                      'AIAN',
                      'Black',
                      'Hispanic'
                    )
      )
    ))+
  geom_bar(
    position = "dodge",
    stat = "identity"
  )+
  scale_fill_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    ))+
  scale_y_continuous(labels = c('40',
                                '45',
                                "50",
                                '55',
                                "60",
                                "65"),
                     breaks = c(
                       0,5,10,15,20, 25),
                     limits = c(0,27.55),
                     expand = c(0, 0)
  ) +
  labs(
    x = "",
    y = "Mean climate risk\n(note:Y axis does not start at zero)",
    title = "Mean climate risk by MDI type, 2022",
    fill = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA Data")+
  theme_bw()+
  theme(axis.text.x = element_text(
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(climate_meanmdi %>% 
            select(-`...1`) %>% 
            pivot_longer(everything()),
          "3. Graphs/10.MDI Mean climate risk by institution type.csv")

ggsave(climate_meanMDIggplot, 
       filename = "3. Graphs/10.MDI Mean climate risk by institution type.pdf",
       width = 10,
       height = 6)
ggsave(climate_meanMDIggplot, 
       filename = "3. Graphs/10.MDI Mean climate by institution type.jpg",
       width = 10,
       height = 6)


climate_MDIplot <- climate_mdi %>% 
  select(-`...1`) %>%
  pivot_longer(-Percentile) %>% 
  #filter(name == "MDI") %>% 
  ggplot()+
  geom_line(aes(x = Percentile,
                y = value-Percentile,
                color = name)) + 
  geom_hline(yintercept = 0) +  
  scale_color_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    )) +
  scale_y_continuous(breaks = c(-10,
                                -5,
                                0,
                                5,
                                10,
                                15,
                                10,
                                25),
                     limits = c(-5,27.5),
                     expand = c(0,0))+
  scale_x_continuous(expand = c(0,0),
                     breaks = c(0,10,25,50,75,90,100),
                     limits = c(-0.05,100.05))+
  labs(
    x = "Community climate risk percentile",
    y = "Institutional risk score \nminus community risk percentile",
    title = "Climate risk portfolios by MDI type, 2022",
    subtitle = "FEMA scores each neighborhood on a scale from 0-100\nIn 2022, CDFIs and MDIs lent to communities with higher climate risk scores",
    color = "",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA and FEMA Climate Resiliancy Data\n(note: a positive number on the y axis indicates lending to \nhigher risk communities while a negative number indicates\nlending to lower risk communities)")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(climate_mdi %>% 
            select(-`...1`) %>%
            pivot_longer(-Percentile),
          "3. Graphs/10.MDI Climate.csv")

ggsave(climate_MDIplot, 
       filename = "3. Graphs/10.MDI Climate.pdf",
       width = 10,
       height = 6)
ggsave(climate_MDIplot, 
       filename = "3. Graphs/10.MDI Climate.jpg",
       width = 10,
       height = 6)

climate_explain_MDIplot <- climate_mdi %>% 
  select(-`...1`) %>%
  pivot_longer(-Percentile) %>% 
  #filter(name == "MDI") %>% 
  ggplot()+
  geom_line(aes(x = Percentile,
                y = value,
                color = name)) + 
  geom_abline(slope =1, intercept = 0, linewidth = 1) +  
  scale_color_manual(
    values = c(
      "light gray",
      "#0F2453",
      "#2FB3A1",
      "#FFB400"
    )) +
  scale_y_continuous(
    limits = c(0,100.5),
    expand = c(0,0))+
  scale_x_continuous(expand = c(0,0),
                     breaks = c(0,10,25,50,75,90,100),
                     limits = c(-0.05,100.05))+
  labs(
    x = "Community climate risk percentile",
    y = "Institutional risk score",
    title = "Climate risk portfolios by MDI type, 2022",
    subtitle = "FEMA scores each neighborhood on a scale from 0-100\nIn 2022, CDFIs and MDIs lent to communities with higher climate risk scores",
    color = "",
    fill = "Borrower Race:",
    caption = "Source: National Bankers Association Foundation analysis \n of HMDA and FEMA Climate Resiliancy Data\n(note: a positive number on the y axis indicates lending to \nhigher risk communities while a negative number indicates\nlending to lower risk communities)")+
  theme_bw()+
  theme(axis.text.x = element_text(#angle = 45,
    # vjust=  .8,
    # hjust = .9,
    face="bold"),
    title = element_text(face="bold"),
    text=element_text(family="Arial Rounded MT Bold"),
    legend.position = "bottom")

write_csv(climate_mdi %>% 
            select(-`...1`) %>%
            pivot_longer(-Percentile),
          "3. Graphs/10.MDI Climate explain.csv")

ggsave(climate_explain_MDIplot, 
       filename = "3. Graphs/10.MDI Climate explain.pdf",
       width = 10,
       height = 6)
ggsave(climate_explain_MDIplot, 
       filename = "3. Graphs/10.MDI Climate explain.jpg",
       width = 10,
       height = 6)
