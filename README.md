# W06 Summative
## "Is London really as rainy as the movies make it out to be?"
<br><br>

### About  
This project conducts data analysis on rain and indicators of rain in London, and compared to other countries.  
<br><br>

### Data Sources  
**OpenMeteo's API** was used due to its (1) high-resolution data (2) detailed documentation (3) accessibility.  

world_cities.csv was also used to obtain the latitude and longitude of other cities. 
<br><br>

### Points of consideration
* **Time period**: 2019-2023 (data from the last 5 years)  
*Rationale*: Sufficient data to analyse trends, and recent enough to be indicative of London's raininess in recent years 

* **Global analysis**: 
United States (North America), Mexico (North America), Brazil (South America), Nigeria (Africa), Egypt (Africa), Germany (Europe), India (Asia), Japan (Asia), Singapore (Asia), Australia (Oceania)  
*Rationale*: 10 other countries were chosen. There is a significant diversity in climates and geographical contexts, thus providing a comprehensive basis for comparison in this data analysis project. 

* **Measure of raininess**:
The 2 key metrics are  
(1) Amount of rainfall  
(2) Frequency of rainy days (provided time period for comparison is greater than 1 day)

* **Variables of weather**:  
Actual rain parameters: precipitation (rain, showers, snow), rain, showers (intermittent rainfall)  
Predictors/indicators of rain: precipitation probability, cloud cover total, dewpoint (moisture in air), relative humidity  
<br><br>

### Data Analysis  
The following was analysed. The parameters that will be used from the OpenMeteo API are bracketed in italics. 

**(1) Analysing London**  
* Rainiest day (*rain*)
* Rainiest month (*rain*)
* Rainiest season (*rain*)
* Rainiest year (*rain*)

**(2) Comparisons between London and set of other countries**   
**(a) Actual rain parameters**
* Amount of rainfall (*rain*)
* Frequency of rainy days (*rain*)
    * Frequency of rainy days in daylight hours
    * Frequency of rainy days across seasons
* Frequency of showers (*showers*)
* Frequency of precipitation (*precipitation*)
* Ratio of showers to rain (*rain*, *showers*)
* Longest continual periods of rain (*rain*)

**(b) Predictors/indicators of rain**
* Graphical analysis to compare predictors of rain
* What is the best predictor of rain?
<br><br>

### How to program works (and expected outputs)
<br><br>

### Author  
Vienna (So Hoi Ling), Year 1 LSE Econs student

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/16Ytx_fz)
