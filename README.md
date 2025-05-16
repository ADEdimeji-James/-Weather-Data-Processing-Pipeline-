# -Weather-Data-Processing-Pipeline-
This project is a simple end-to-end data pipeline designed to ingest, clean, transform, analyze, and visualize raw weather data from a CSV file. The goal is to demonstrate data engineering skills by preparing weather data for analysis and producing meaningful outputs.

Step-by-step instructions to run the pipeline locally.
1. clone the repository:
   open a terminal and run: git clone https://github.com/ADEdimeji-James/Weather-Data-Processing-pipeline.git then cd weather-pipeline-project
2. Install requires python libraries such as pandas, matplotlib and seaborn: pip install pandas matplotlib seaborn
3. Add the raw data file in the same folder
4. RUn the full pipeline by executing: pipeline.py

A brief explanation of my approach 
  I did the work in a jupyter notebook where i had to first run codes and confirm it does the intended use before adding it to a pipeline stage. WHen i was done, i converted the .ipynb jupyter notenook to a .py python file using anaconda prompt. A brief explanation about the project itself:

  1. Data Ingestion: I loaded the raw CSV files containing weather measurements for different cities.
  2. Data Cleaning and Transformation: i handled missing values in numerical columns such as temperature(in celcius), humidity and wind speed by imputing the 
     average city-wise value, i then proceded to drop empty rows in the date column and weather condition column. I then proceded to convert the date column into 
     a dtaetime format and standardized the dates. I then created a new column called temperature_fahrenheit which was made by calculations applied to the 
     temperation_celcius column. Finally, i removed values such as "Unknown" or "Null" from the weather column.
  3. Output Generation: The cleaned dataset is saved as a new CSV file. Additionally, the pipeline 
     produces a text report highlighting the top five cities with the highest average temperature, 
     providing a quick summary of key insights.
  4. Visualization (Bonus):   A horizontal bar chart using matplotlib, visualizes average temperatures 
     per city, saved as an image to aid in quick, visual data interpretation.

Challenges Faced
  The challenged i face was dealing with the date column. Initially, i tried converting the whole 
  column from an object datatype to a datetime format which did not work. i then tried converting to 
  string which failed too. I even tried removing whitespaces which the effort was not succesful. I had 
  to research ways to succesfully convert the column from object to time format which i later found 
  solution to. it was the greatest challenge i faced concerning this project. 


Sample Output/Visualization

![avg_temperature_per_city](https://github.com/user-attachments/assets/1147a797-d70e-4bc4-b049-e193a61b0510)

  
