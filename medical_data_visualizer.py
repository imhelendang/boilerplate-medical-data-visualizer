import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# first calculate their BMI by dividing their weight in kilograms by the square of their height in meters.
# If that value is > 25 then the person is overweight. 
# Add 'overweight' column
df['overweight'] = df['weight'] / ((df['height'] / 100) ** 2)
df.loc[(df['overweight'] <= 25), 'overweight'] = 0
df.loc[(df['overweight'] > 25), 'overweight'] = 1
df['overweight'] = pd.to_numeric(df['overweight'], downcast='integer')

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[(df['cholesterol'] <= 1), 'cholesterol'] = 0
df.loc[(df['gluc'] <= 1), 'gluc'] = 0

df.loc[(df['cholesterol'] > 1), 'cholesterol'] = 1
df.loc[(df['gluc'] > 1), 'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars = 'cardio', var_name = 'variable', value_vars = ['alco', 'active','cholesterol', 'gluc', 'overweight','smoke'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['variable','cardio','value'])['variable'].size().reset_index(name='total')
    
    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x='variable', y='total', col='cardio', data=df_cat, kind='bar', hue='value').figure
 
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))

    # Set up the matplotlib figure
    # A selfnote:
    # Matplotlib and Seaborn also support plotting multiple charts in a grid, using plt.subplots, 
    # which returns a set of axes for plotting.
    fig, axes = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=corr, fmt='.1f', annot=True, mask=mask)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig