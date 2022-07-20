"""
created on 18-jul-2022
@author : leowkimteck@gmail.com

"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import earthpy as et
import json

#open json data as pandas data frame
pd.set_option('display.max_rows', None)  # or to display 1000 rows
url = "https://raw.githubusercontent.com/wesm/pydata-book/2nd-edition/datasets/usda_food/database.json"
url = url.replace(" ", "%20")
usda_food_db = pd.read_json(url)
usda_food_db

type(usda_food_db)
len(usda_food_db)
usda_food_db.head()


#view list of food groups that linked to each food id in usda food database
usda_food_db_foodgroup = usda_food_db[["id", "group"]]

#open json data as list of dictionaries
import urllib, json

url = "https://raw.githubusercontent.com/wesm/pydata-book/2nd-edition/datasets/usda_food/database.json"
response = urllib.request.urlopen(url)
usda_food_database = json.loads(response.read())

#view quantity of food items (the data base contains 6,636 food items)
len(usda_food_database) ## 6636 
type(usda_food_database) ## list

#view keys for the first food item [0]
usda_food_database[0].keys()

## dict_keys(['id', 'description', 'tags', 'manufacturer', 'group', 'portions', 'nutrients'])

#view keys for the last food item-food item no. 6636 [6635]
usda_food_database[6635].keys()

## dict_keys(['id', 'description', 'tags', 'manufacturer', 'group', 'portions', 'nutrients'])

#view First food component for the first food item
#SR-Legacy  in 2015 contains up to 150 food components for each food item
usda_food_database[0]['nutrients'][0]

## {'value': 25.18, 'units': 'g', 'description': 'Protein', 'group': 'Composition'}

#view last food component(the 161st) for the first food item
usda_food_database[0]['nutrients'][161]

## {'value': 0.83, 'units': 'g', 'description': 'Fatty acids, total polyunsaturated', 'group': 'Other'}

#call any key(name) of a Python list and see the associated values
#data_sample["name"]

usda_food_database[0]["id"]
usda_food_database[0]["description"]
usda_food_database[6635]["id"]
usda_food_database[6635]["description"]
usda_food_database[0]["group"]
usda_food_database[0]["portions"]
usda_food_database[0]["tags"]
usda_food_database[0]["manufacturer"]


#view Nutrient data for food item no.1-'Cheese, caraway' in SR Legacy

pd.set_option('display.max_rows', None)  # or 1000
nutrients = pd.DataFrame(usda_food_database[0]['nutrients'])
nutrients.info()
nutrients.head(20)
nutrients.tail()

#view the first eighth nutrients info
nutrients[:8]

#view Nutrient data for food item no.6635-'Babyfood, banana no tapioca, strained' in SR Legacy
pd.set_option('display.max_rows', None)  # or 1000
nutrients_foodid_6635 = pd.DataFrame(usda_food_database[6635]['nutrients'])
nutrients_foodid_6635

#convert a list of dicts to a DataFrame, by specify a list of fields to extract.
#take the food names (description), group, id, and manufacturer
info_keys = ['id', 'description', 'group', 'manufacturer']
info = pd.DataFrame(usda_food_database, columns=info_keys)
info.info()

#see the distribution of food groups with value_counts
pd.value_counts(info.group)

#view the length (quantity) of food groups with value_counts
len(pd.value_counts(info.group)) ## 25
type(pd.value_counts(info.group)) ## pandas.core.series.Series

#see the distribution of food manufacturer with value_counts
pd.value_counts(info.manufacturer)

#view the length (quantity) of manufacturer with value_counts
len(pd.value_counts(info.manufacturer)) ## 67


#To do analysis on all of the nutrient data, assemble the nutrients for each food into a single large table.
#First, convert each list of food nutrients to a DataFrame, add a column for the food id, 
#and append the DataFrame to a list. Then, these can be concatenated together with concat

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import earthpy as et
import json
import urllib, json

url = "https://raw.githubusercontent.com/wesm/pydata-book/2nd-edition/datasets/usda_food/database.json"
response = urllib.request.urlopen(url)
usda_food_database = json.loads(response.read())


nutrients = []
for rec in usda_food_database:
    fnuts = pd.DataFrame(rec['nutrients'])
    fnuts['id'] = rec['id']
    nutrients.append(fnuts)
nutrients = pd.concat(nutrients, ignore_index=True)
nutrients.head()
nutrients.info() ## 389355 rows × 5 columns


#drop duplicates in the nutrients DataFrame
nutrients.duplicated().sum() ## number of duplicates ## 14179

#remove duplicates
nutrients = nutrients.drop_duplicates()
nutrients.info() ## 375176 rows × 5 columns

#rename columns and apply to info dataframe

#convert a list of dicts to a DataFrame, by specify a list of fields to extract.
#take the food names (description), group, id, and manufacturer
info_keys = ['id', 'description', 'group', 'manufacturer']
info = pd.DataFrame(usda_food_database, columns=info_keys)
col_mapping = {'description' : 'food',
               'group' : 'food_group'}
info = info.rename(columns=col_mapping, copy=False)
info.head()

#rename columns in nutrients data frame and apply to the dataframe
nut_col_mapping = {'description' : 'nutrient','group' : 'nutgroup'}
nutrients = nutrients.rename(columns=nut_col_mapping, copy=False)
nutrients.head()

#merging data
nutrient_data = pd.merge(nutrients, info, on='id', how='outer')
nutrient_data ## 375176 rows × 8 columns
nutrient_data.info()

#select 'nutgroup' data from the nutrient_data DataFrame
nut_group = nutrient_data[["nutgroup"]]

#view unique values in column of 'nutgroup' in the nutrient_data DataFrame
nut_group['nutgroup'].unique()

## array(['Composition', 'Other', 'Energy', 'Elements', 'Vitamins','Amino Acids', 'Sugars'], dtype=object)


#Select data for a specific food id(cheese), rows equal to 1008 in the column of id
nutrient_data_cheese = nutrient_data[nutrient_data["id"] == 1008]
nutrient_data_cheese

#Select data for a nutrient constitient(protein), rows equal to "Protein" in the column of nutrient
nutrient_data_protein = nutrient_data[nutrient_data["nutrient"] == "Protein" ]
nutrient_data_protein  ## 6636 rows × 8 columns (A total of 6636 food items with corresondent food id contain protein)

# Sort in descending order for food id with protein contents
nutrient_data_protein_desc = nutrient_data_protein.sort_values(by="value", ascending=False)

#display top 25 food id with highest protein contents
pd.set_option('display.max_rows', None)  #to display up to 1000 rows
top25_food_protein = nutrient_data_protein_desc.head(25)

#Select data for a nutrient constitient(Zinc, Zn), rows equal to "Zinc, Zn" in the column of nutrient
food_zinc = nutrient_data[nutrient_data["nutrient"] == "Zinc, Zn"]
food_zinc ##  ## 6137 rows × 8 columns (A total of 6137 food items with corresondent food id contain zinc)

#Sort in descending order for food id with zinc contents
food_zinc_desc = food_zinc.sort_values(by="value", ascending=False)

#display top 25 food id with highest zinc contents
pd.set_option('display.max_rows', None)  #to display up to 1000 rows
top25_food_zinc = food_zinc_desc.head(25)

#For all the different foods groups (beef Products, Pork Products, dairy and egg products etc.), calculate the median Zinc content (median of the zinc content in all the foods that constitute the nutrient group)
#Plot the distribution of median Zinc Content for different foods groups as a bar chart.

result = nutrient_data.groupby(['nutrient', 'food_group'])['value'].quantile(0.5)
plt.figure(figsize=[16,10])
result['Zinc, Zn'].plot(kind='barh', title = "Distribution of Median Zinc Content for Different Food Groups")
plt.xlabel("Zinc Content, mg/100 g")
plt.show()

#Plot the distribution of median Protein Content for different foods groups as a bar chart.
result = nutrient_data.groupby(['nutrient', 'food_group'])['value'].quantile(0.5)
plt.figure(figsize=[16,10])
result['Protein'].plot(kind='barh', title = "Distribution of Median Protein Content for Different Food Groups")
plt.xlabel("Protein Content, g/100 g")
plt.show()

#Plot the distribution of median Total lipid (fat) Content for different foods groups as a bar chart.
result = nutrient_data.groupby(['nutrient', 'food_group'])['value'].quantile(0.5)
plt.figure(figsize=[16,10])
result['Total lipid (fat)'].plot(kind='barh', title = "Distribution of Median Total lipid Content for Different Food Groups")
plt.xlabel("Total lipid Content, g/100 g")
plt.show()


#Plot the distribution of median Carbohydrate Content for different foods groups as a bar chart.
result = nutrient_data.groupby(['nutrient', 'food_group'])['value'].quantile(0.5)
plt.figure(figsize=[16,10])
result['Carbohydrate, by difference'].plot(kind='barh', title = "Distribution of Median Carbohydrate Content for Different Food Groups")
plt.xlabel("Carbohydrate Content, g/100 g")
plt.show()

"""
For a nutrient group (‘Amino Acids, etc’), create a table to show the different constituents of the group (Alanine, Glycine, Histidine, etc) and the foods in which they are present (Gelatins, dry powder, beluga, meat, etc)

"""
by_nutrient = nutrient_data.groupby(['nutgroup', 'nutrient'])
get_maximum = lambda x: x.loc[x.value.idxmax()]
get_minimum = lambda x: x.loc[x.value.idxmin()]
max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]
max_foods
max_foods.info() ## 94 x 2 columns

type(max_foods) ## pandas.core.frame.DataFrame

#make the max_foods data smaller
max_foods.food = max_foods.food.str[:50]
max_foods.food

type(max_foods.food) ## pandas.core.series.Series

#tabel of Amino Acid  
max_foods.loc['Amino Acids']

#table of Vitamins
max_foods.loc['Vitamins']

#table of Composition
max_foods.loc['Composition']

#table of Elements
max_foods.loc['Elements']

#table of Sugars
max_foods.loc['Sugars']

#table of Energy
max_foods.loc['Energy']

#table of Other
max_foods.loc['Other']











