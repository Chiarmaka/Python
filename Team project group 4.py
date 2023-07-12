#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Import necessary libries
import pandas as pd
import os


# In[5]:


data1 = pd.read_csv('Sales_Data\Sales_January_2019.csv')


# In[6]:


files = [file for file in os.listdir('Sales_Data')]
all_months_data = pd.DataFrame()
for file in files:
    df = pd.read_csv('Sales_Data/'+ file)
    all_months_data = pd.concat([all_months_data, df])
#all_months_data.head()
all_months_data.to_csv('all_data.csv',index=False)
#data1.head()

Read in uploaded datarame
# In[7]:


all_data = pd.read_csv('all_data.csv')
all_data.head()


# In[8]:


#Dropping NaN values from the dataframe
all_data.dropna(inplace=True)
all_data.head()


# In[9]:


#Removing rows based on the condition


# In[10]:


all_data = all_data[all_data['Quantity Ordered'] != 'Quantity Ordered']
all_data.head()


# In[11]:


#Changing the type of the columns to(to_numeric,to_datetime,astype)


# In[64]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data.head()


# In[33]:


#creating new columns (month and city columns)


# In[65]:


all_data['Month'] = all_data['Order Date'].dt.month
all_data.tail(15)


# In[26]:


def city_name(address):
    return address.split(',')[1].strip()
all_data['City'] = all_data['Purchase Address'].apply(city_name)


all_data.head(15)


# In[66]:


all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head(15)


# In[61]:


#Question 1:What was the best month for sales? how much was earned that month?


# In[67]:


results = all_data.groupby('Month').sum()
results


# In[68]:


import matplotlib.pyplot as plt
Months = range(1,13)
plt.bar(Months,results['Sales'])
plt.xticks(Months)
plt.ylabel('Sales in USD($)')
plt.xlabel('Month Number')
plt.title('Total Sales per Month')
plt.show()
#From the barchat below, December was the best months for sales with $4613443.34 earned


# In[69]:


#Question 2:What city sold the most product


# In[70]:


results = all_data.groupby('City').sum()
results



# In[71]:


import matplotlib.pyplot as plt
Cities = [City for City,df in all_data.groupby('City')]
plt.bar(Cities,results['Sales'])
plt.xticks(Cities,rotation = 'vertical', size = 6)
plt.ylabel('Sales in USD($)')
plt.xlabel('City name')
plt.title('Total Sales per Month')
plt.show()
# From the barchat below, San Fransisco sold the most products


# In[72]:


#Question 3:What time should we display advertisement to maximize the likelihood of costomers buying a product


# In[73]:


all_data.head(20)


# In[77]:


all_data['Hour']= all_data['Order Date'].dt.hour
all_data['Minute']= all_data['Order Date'].dt.minute
all_data.head(20)


# In[87]:


hours = [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number Of Orders')
plt.grid()
plt.show()

#My recommendation is around 12am or 7pm based on the graph below


# In[89]:


#Question 4:What product are most often sold together


# In[91]:


all_data.head(20)


# In[122]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
df = df[['Order ID', 'Grouped']].drop_duplicates()
df.head(20)


# In[128]:


from itertools import combinations
from collections import Counter
count = Counter()
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
for key, value in count.most_common(10):
    print(key, value)


# In[129]:


# The products often sold together the most are 'iPhone'and 'Lightning Charging Cable' (1005)


# In[130]:


#Question 5: What products sold the most? Why do you think it sold the most?


# In[131]:


all_data.head()


# In[165]:


product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']
products = [product for product, df in product_group]
plt.bar(products, quantity_ordered)
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.xticks(products, rotation = 'vertical', size = 7)
plt.show()



# In[167]:


#From the above barchat the product sold the most is the AAA Batteries (4-pack)


# In[166]:


prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, 'b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered',color = 'g')
ax2.set_ylabel('Price($)', color = 'b')
ax1.set_xticklabels(products, rotation = 'vertical', size = 7)

plt.show()


# In[168]:


#From the above barchat the reason for the top-selling of the product(AAA Batteries (4-pack)) was due to its low cost


# In[ ]:




