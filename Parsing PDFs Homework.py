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

# In[1]:


import pandas as pd
import camelot


# In[2]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[3]:


df = pd.DataFrame([
    [ 'fruit name', 'likes' ],
    [ 'apple', 15 ],
    [ 'carrot', 3 ],
    [ 'sweet potato', 45 ],
    [ 'peach', 12 ],
])
df


# In[4]:


# Set the first column as the columns
df.columns = df.loc[0]

# Drop the first row
df = df.drop(0)

df


# 🚀 Done!
# 
# ### Approach 2
# 
# Another alternative is to use `.rename` on your columns and just filter out the columns you aren't interested in. This can be useful if the column name shows up multiple times in your data for some reason or another.

# In[5]:


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


# In[6]:


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

# In[ ]:


# Include all pages and check how many tables there are on each page
inmate_tables = camelot.read_pdf("InmateList.pdf", flavor='stream', pages='1-end')
inmate_tables


# In[7]:


pd.set_option('display.max_rows', 800)


# In[ ]:


inmate_tables[0].df


# In[ ]:


df = [inmate_table.df for inmate_table in inmate_tables]
df = pd.concat(df, ignore_index=True)
df


# In[ ]:


# Drop the first three rows
df = df.drop([0,1,2])


# In[ ]:


# Rename all the columns
df = df.rename(columns={
    0: 'ICN #',
    1: 'Inmate Name',
    2: 'Facility',
    3: 'Booking Date',
    4: 'Booking Date',
    5: 'Booking Date'
})
df


# In[ ]:


InmateNames = pd.DataFrame(df['Inmate Name'])
InmateNames


# In[ ]:


# Convert it into a csv
InmateNames.to_csv('InmateNames.csv', index=False)


# ## WHO resolutions
# 
# Using [A74_R13-en.pdf](A74_R13-en.pdf), what ten member countries are given the highest assessments?
# 
# * You might need to have two separate queries, and combine the results: that last page is pretty awful!
# * Always rename your columns
# * Double-check that your sorting looks right......
# * You can still get the answer even without perfectly clean data

# In[ ]:


# Include all pages and check how many tables there are
who_tables = camelot.read_pdf("A74_R13-en.pdf", flavor='stream', pages='1-end')
who_tables


# In[ ]:


df = [who_table.df for who_table in who_tables]
df = pd.concat(df, ignore_index = True)


# In[ ]:





# In[ ]:





# In[ ]:





# ## The Avengers
# 
# Using [THE_AVENGERS.pdf](THE_AVENGERS.pdf), approximately how many lines does Captain America have as compared to Thor and Iron Man?
# 
# * Character names only: we're only counting `IRON MAN` as Iron Man, not `TONY`.
# * Your new best friend might be `\n`
# * Look up `.count` for strings

# In[ ]:


import tika
from tika import parser


# In[ ]:


parsed = parser.from_file('THE_AVENGERS.pdf')


# In[ ]:


parsed.keys()


# In[ ]:


# Check pdf
print(parsed['content'].strip())


# In[ ]:


# Find out number of lines for IRON MAN
IRON_MAN = parsed['content'].strip().count('\nIRON MAN\n')
IRON_MAN


# In[ ]:


# Find out number of lines for THOR
THOR = parsed['content'].strip().count('\nTHOR\n')
THOR


# In[ ]:


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

# In[ ]:


# Include all pages and check how many tables there are
covid_tables = camelot.read_pdf("covidweekly2721.pdf", flavor='lattice', pages='1-end')


# In[ ]:


# Look at page 6
covid_tables = camelot.read_pdf("covidweekly2721.pdf", flavor='lattice', pages='6')
covid_tables


# In[ ]:


covid_tables[1].df


# In[ ]:


df = pd.DataFrame(covid_tables[1].df)
df


# In[ ]:


df.columns = df.loc[0]


# In[ ]:


df = df.drop(0)
df


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## Theme Parks
# 
# Using [2019-Theme-Index-web-1.pdf](2019-Theme-Index-web-1.pdf), save a CSV of the top 10 theme park groups worldwide.
# 
# * You can clean the results or you can restrict the area the table is pulled from, up to you

# In[ ]:


# Include all pages and check how many tables there are
theme_tables = camelot.read_pdf("2019-Theme-Index-web-1.pdf", flavor='stream', pages='1-end')
theme_tables


# In[ ]:


# Look at page 11
theme_tables = camelot.read_pdf("2019-Theme-Index-web-1.pdf", flavor='stream', pages='11)
theme_tables


# In[ ]:


df = theme_tables[0].df
df


# In[ ]:





# ## Hunting licenses
# 
# Using [US_Fish_and_Wildlife_Service_2021.pdf](US_Fish_and_Wildlife_Service_2021.pdf) and [a CSV of state populations](http://goodcsv.com/geography/us-states-territories/), find the states with the highest per-capita hunting license holders.

# In[ ]:


hunting_tables = camelot.read_pdf("US_Fish_and_Wildlife_Service_2021.pdf", flavor='lattice', pages='1')
hunting_tables


# In[ ]:


df = tables[0].df
df


# In[ ]:


# Make the first row the columns
df.columns = df.loc[0]


# In[ ]:


# Drop the first row
df = df.drop(0)


# In[ ]:


df['State'] = df.State.str.strip()


# In[ ]:


states = pd.read_csv("us-states-territories.csv")
states


# In[ ]:


states['Abbreviation'] = states.Abbreviation.str.strip()


# In[ ]:


# Combine
combined = df.merge(statse, left_on='State', right_on='Abbreviation')
combined


# In[ ]:


updated_df = combined[['State', 'Name','Population (2019)','Paid Hunting License \nHolders*']]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




