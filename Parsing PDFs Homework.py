#!/usr/bin/env python
# coding: utf-8

# # Parsing PDFs Homework
# 
# With the power of pdfminer, pytesseract, Camelot, and Tika, let's analyze some documents!
# 
# > If at any point you think, **"I'm close enough, I'd just edit the rest of it in Excel"**: that's fine! Just make a note of it.
# 
# ## A trick to use again and again
# 
# ### Approach 1
# 
# Before we get started: when you want to take the first row of your data and set it as the header, use this trick.

# In[237]:


import pandas as pd
import camelot


# In[238]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[149]:


df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[151]:


# Set the first row as the columns
df.columns = df.loc[0]

# Drop the first row
df = df.drop(0)

df


# 🚀 Done!
# 
# ### Approach 2
# 
# Another alternative is to use `.rename` on your columns and just filter out the columns you aren't interested in. This can be useful if the column name shows up multiple times in your data for some reason or another.

# In[152]:


# Starting with the same-ish data...
df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'fruit name', 'likes' ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[153]:


df = df.rename(columns={
    0: 'fruit name',
    1: 'likes'
})
df = df[df['fruit name'] != 'fruit name']
df


# 🚀 Done!
# 
# ### Useful tips about coordinates
# 
# If you want to grab only a section of the page [Kull](https://jsoma.github.io/kull/#/) might be helpful in finding the coordinates.
# 
# > **Alternatively** run `%matplotlib notebook` in a cell. Afterwards, every time you use something like `camelot.plot(tables[0]).show()` it will get you nice zoomable, hoverable versions that include `x` and `y` coordinates as you move your mouse.
# 
# Coordinates are given as `"left_x,top_y,right_x,bottom_y"` with `(0,0)` being in the bottom left-hand corner.
# 
# Note that all coordinates are strings, for some reason. It won't be `[1, 2, 3, 4]` it will be `['1,2,3,4']`
# 
# # The homework
# 
# This is **mostly Camelot work**, because I don't really have any good image-based PDFs to stretch your wings on tesseract. If you know of any, let me know and I can put together another couple exercises.
# 
# ## Prison Inmates
# 
# Working from [InmateList.pdf](InmateList.pdf), save a CSV file that includes every inmate.
# 
# * Make sure your rows are *all data*, and you don't have any people named "Inmate Name."
# 

# In[492]:


# Include all pages and check how many tables there are on each page
inmate_tables = camelot.read_pdf("InmateList.pdf", flavor='stream', pages='1-end', table_areas=['15,734,365,120'])
inmate_tables


# In[493]:


# Look at where table is
camelot.plot(inmate_tables[15]).show()


# In[494]:


# Display all rows
pd.set_option('display.max_rows', 800)


# In[495]:


# See what first table looks like
inmate_tables[0].df


# In[496]:


# List comprehension
# Combine tables by stacking on top of one another
# Reset index so there are no repeating values
df = [inmate_table.df for inmate_table in inmate_tables]
df = pd.concat(df, ignore_index=True)
df


# In[497]:


# Drop the rows that aren't required
df = df[df[1] != 'Inmate Name']


# In[498]:


# Rename all the columns
df = df.rename(columns={
    0: 'ICN #',
    1: 'Inmate Name',
    2: 'Facility',
    3: 'Booking Date'
})
df


# In[500]:


# Convert it into a csv
df.to_csv('InmateList.csv', index=False)


# In[501]:


# To see if there is missing data, try the following:
# df.count()
# value_counts()
# Scatter plot
# Box plot

# To look for duplicates, try the following:
# df.duplicated()
# df[df.duplicated() == True]
# df.loc[df.duplicated(), :]


# ## WHO resolutions
# 
# Using [A74_R13-en.pdf](A74_R13-en.pdf), what ten member countries are given the highest assessments?
# 
# * You might need to have two separate queries, and combine the results: that last page is pretty awful!
# * Always rename your columns
# * Double-check that your sorting looks right......
# * You can still get the answer even without perfectly clean data

# In[521]:


# Read tables from pages 1-5. Save page 6 for later because it needs cleaning up.
who_tables = camelot.read_pdf("A74_R13-en.pdf", flavor='stream', pages='1-5')
who_tables


# In[522]:


# Look at the first table
who_tables[0].df


# In[523]:


# List comprehension
# Combine tables by stacking on top of one another
# Reset index so there are no repeating values
df = [who_table.df for who_table in who_tables]
df = pd.concat(df, ignore_index = True)
df


# In[524]:


# Drop the first three rows
df = df.drop([0,1,2])


# In[525]:


# Rename all the columns
df = df.rename(columns={
    0: 'Members and Associate Members',
    1: 'WHO scale for 2022–2023'
})
df


# In[526]:


# Remove rows that say 'Members and Associate Members' from first column
df = df[df['Members and Associate Members'] != 'Members and Associate Members']
df


# In[527]:


# Show the rows that still say 'Members and Associate Members' in the first column and '%' in the second column
df['Members and Associate Members'].str.contains('Members')
df['WHO scale for 2022–2023'].str.contains('%')


# In[528]:


# Show only the rows we want
df = df[df['Members and Associate Members'].str.contains('Members') == False]
df = df[df['WHO scale for 2022–2023'].str.contains('%') == False]
df


# In[529]:


# Replace blank cells with NaN
import numpy as np
df = df.replace(r'^\s*$', np.nan, regex=True)
df


# In[530]:


# Remove NaN from second column
df.dropna(subset=['WHO scale for 2022–2023'])


# In[531]:


df.shape


# In[532]:


# See how many tables there are on page 6
who_tables2 = camelot.read_pdf("A74_R13-en.pdf", flavor='stream', pages='6')
who_tables2


# In[533]:


# Look at the table on page 6
df2 = who_tables2[0].df
df2


# In[534]:


# See whether Zambia row can be selected
df2[df2[1] == 'Zambia']


# In[535]:


# Create a second table with Zambia and Zimbabwe rows
df2 = df2[(df2[1]=='Zambia') | (df2[1]=='Zimbabwe')]
df2


# In[536]:


# Drop extra columns
df2 = df2.drop(columns=[0, 2, 4])
df2


# In[537]:


# Rename columns
df2 = df2.rename(columns={
    1: 'Members and Associate Members',
    3: 'WHO scale for 2022–2023'
})
df2


# In[538]:


# Combine the two tables and save as a new table
dfs = [df, df2]
df = pd.concat(dfs)
df


# In[539]:


# Sort the table by assessment
df.sort_values(by=['WHO scale for 2022–2023'], ascending=False)


# In[540]:


# Since it's not sorting correctly, check datatype
df.dtypes


# In[541]:


# Covert second column into a float
df['WHO scale for 2022–2023'] = df['WHO scale for 2022–2023'].astype(float)
df.dtypes


# In[544]:


# Sort table
# Show the top ten countries with the highest assessments
df = df.sort_values(by=['WHO scale for 2022–2023'], ascending=False)
df.head(10)


# In[ ]:





# ## The Avengers
# 
# Using [THE_AVENGERS.pdf](THE_AVENGERS.pdf), approximately how many lines does Captain America have as compared to Thor and Iron Man?
# 
# * Character names only: we're only counting `IRON MAN` as Iron Man, not `TONY`.
# * Your new best friend might be `\n`
# * Look up `.count` for strings

# In[545]:


import tika
from tika import parser


# In[546]:


# Read pdf with Tika
parsed = parser.from_file('THE_AVENGERS.pdf')


# In[547]:


# Look at the keys
parsed.keys()


# In[548]:


# Check pdf
print(parsed['content'].strip())


# In[549]:


# Find out number of lines for IRON MAN
IRON_MAN = parsed['content'].strip().count('\nIRON MAN\n')
IRON_MAN


# In[550]:


# Find out number of lines for THOR
THOR = parsed['content'].strip().count('\nTHOR\n')
THOR


# In[551]:


# Find out number of lines for CAPTAIN AMERICA
CAPTAIN_AMERICA = parsed['content'].strip().count('\nCAPTAIN AMERICA\n')
CAPTAIN_AMERICA


# In[ ]:





# ## COVID data
# 
# Using [covidweekly2721.pdf](covidweekly2721.pdf), what's the total number of tests performed in Minnesota? Use the Laboratory Test Rates by County of Residence chart.
# 
# * You COULD pull both tables separately OR you could pull them both at once and split them in pandas.
# * Remember you can do things like `df[['name','age']]` to ask for multiple columns

# In[588]:


# Read tables on page 6
covid_tables = camelot.read_pdf("covidweekly2721.pdf", flavor='lattice', pages='6')
covid_tables


# In[589]:


# Look at the first table
covid_tables[1].df


# In[590]:


# Save as a table
df = pd.DataFrame(covid_tables[1].df)
df


# In[591]:


# Set the first row as the columns
df.columns = df.loc[0]


# In[592]:


# Drop first row
df = df.drop(0)
df


# In[593]:


# The tables are stacked side by side so that needs to be fixed
# Get the first table by selecting the first three columns
df1 = df.iloc[:, 0:3]
df1


# In[594]:


# Get the second table by selecting the last three columns
df2 = df.iloc[:, 3:6]
df2


# In[595]:


# Since we have to do calculations, remove commas from first table
# Row 5 is wonky - 77865\n9953
df1 = df1.replace(',','', regex=True)
df1


# In[596]:


# To remove 77865\n9953 from row 5, 
df1[['Number of Tests']] = df1[['Number of Tests']].replace('77865\n9953', '77865', regex=False)
df1


# In[597]:


# And remove commas from second table
df2 = df2.replace(',','', regex=True)
df2


# In[598]:


# Convert 'Number of Tests' column from string to integers in both tables
# Check to see whether there are integers
df1[['Number of Tests']] = df1[['Number of Tests']].apply(pd.to_numeric)
df2[['Number of Tests']] = df2[['Number of Tests']].apply(pd.to_numeric)
df1.dtypes


# In[604]:


# Calculate total number of tests in Minnesota by adding the sums of both tables
total_tests = df1.sum() + df2.sum()
total_tests


# In[ ]:





# ## Theme Parks
# 
# Using [2019-Theme-Index-web-1.pdf](2019-Theme-Index-web-1.pdf), save a CSV of the top 10 theme park groups worldwide.
# 
# * You can clean the results or you can restrict the area the table is pulled from, up to you

# In[605]:


# Look at page 11
themeparks_tables = camelot.read_pdf("2019-Theme-Index-web-1.pdf", flavor='stream', pages='11', table_areas=['35,464,408,296'])
themeparks_tables


# In[606]:


# Look at where table is
# Vertical-aligned text makes table wonky so don't include that
# "left_x,top_y,right_x,bottom_y"
camelot.plot(themeparks_tables[0]).show()


# In[607]:


# Look at the table
df = themeparks_tables[0].df
df


# In[608]:


# Rename all the columns
df = df.rename(columns={
    0: 'Rank',
    1: 'Group Name',
    2: '% Change',
    3: 'Attendance 2019',
    4: 'Attendance 2018'
})
df


# In[609]:


# Convert it into a csv
df.to_csv('TopTenThemeParks.csv', index=False)


# In[ ]:





# ## Hunting licenses
# 
# Using [US_Fish_and_Wildlife_Service_2021.pdf](US_Fish_and_Wildlife_Service_2021.pdf) and [a CSV of state populations](http://goodcsv.com/geography/us-states-territories/), find the states with the highest per-capita hunting license holders.

# In[626]:


# Read pdf
hunting_tables = camelot.read_pdf("US_Fish_and_Wildlife_Service_2021.pdf", flavor='lattice', pages='1')
hunting_tables


# In[627]:


# Look at the table
df = hunting_tables[0].df
df


# In[628]:


# Make the first row the columns
df.columns = df.loc[0]
df


# In[629]:


# Drop the first row
df = df.drop(0)
df


# In[630]:


# Remove extra spaces
df['State'] = df.State.str.strip()


# In[631]:


# Read csv file
states = pd.read_csv("us-states-territories.csv")
states


# In[632]:


# Remove extra spaces
states['Abbreviation'] = states.Abbreviation.str.strip()


# In[633]:


# Combine the two dfs
combined_table = df.merge(states, left_on='State', right_on='Abbreviation')
combined_table


# In[634]:


# Clean up table so it only shows the columns needed to calculate per capita hunting licenses - population and total hunting licenses
updated_df = combined_table[['State', 'Name','Population (2019)','Total Hunting License, \nTags,Permits & Stamps**']]
updated_df


# In[635]:


# Check to see whether columns are strings or objects before doing calculations
type(updated_df['Population (2019)'][1])
# type(updated_df['Total Hunting License, \nTags,Permits & Stamps**'][1])


# In[636]:


# Remove spaces and convert license column from string to integer
# Create a new column called 'total licenses'
updated_df['total_licenses'] = updated_df['Total Hunting License, \nTags,Permits & Stamps**'].str.replace(",", "").astype(int)
updated_df


# In[637]:


# Drop NaN values
updated_df = updated_df.dropna()


# In[638]:


# Remove spaces and convert population column from string to integer
# Create a new column called 'population'
updated_df['population'] = updated_df['Population (2019)'].str.replace(",", "").astype(int)
updated_df


# In[639]:


# Calculate per capita licenses 
# Create a new column called 'per_capita'
updated_df['per_capita'] = updated_df['total_licenses'] / updated_df['population']
updated_df


# In[640]:


# Sort table to find the states with the highest per-capita hunting license holders
updated_df = updated_df.sort_values(by=['per_capita'], ascending=False)
updated_df


# In[ ]:




