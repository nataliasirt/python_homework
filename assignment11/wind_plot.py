import plotly.express as px
import plotly.data as pldata
import pandas as pd

df = pldata.wind(return_type='pandas')

print("First 10 lines of the DataFrame:")
print(df.head(10))
print("\nLast 10 lines of the DataFrame:")
print(df.tail(10))

df['strength'] = df['strength'].str.replace(r'[^\d.]', '', regex=True).astype(float)

fig = px.scatter(df, x='strength', y='frequency', color='direction',
                 title='Wind Strength vs. Frequency by Direction',
                 labels={'strength': 'Wind Strength', 'frequency': 'Frequency'},
                 color_continuous_scale=px.colors.sequential.Viridis)

fig.write_html('wind.html')

with open('wind.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
    print("\nHTML file 'wind.html' has been created successfully.")