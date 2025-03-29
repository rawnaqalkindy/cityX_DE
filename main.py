import pandas as pd
import numpy as np
import re
from datetime import datetime
import pytesseract
from pdf2image import convert_from_path
from sqlalchemy import create_engine

# 1. Extracting data from pdf using OCR
pdf = 'district_info.pdf'
pages = convert_from_path(pdf, dpi=300)

text = ""
for page in pages:
    page_text = pytesseract.image_to_string(page, lang='eng')
    text += page_text + "\n"
lines = [l.strip() for l in text.split('\n') if l.strip()]

# Using regex for each table row 
pattern = re.compile(r'^(\d+)\s+(.+?)\s+([\d,]+)\s+([A-Za-z\s]+)$')
rows = []
for line in lines:
    match = pattern.match(line)
    if match:
        rows.append([match.group(1), match.group(2), match.group(3), match.group(4)])
district_df = pd.DataFrame(rows, columns=['district_id', 'district_name', 'population', 'governor'])
district_df['district_id'] = district_df['district_id'].astype(int)
district_df['population'] = district_df['population'].str.replace(',', '').astype(int)
district_df['district_name'] = district_df['district_name'].str.replace(r'\|$', '', regex=True).str.strip()

# 2. Loading and cleaning crime records 
crime_df = pd.read_json('crime_records.json')
crime_df = crime_df[crime_df['crime_type'].notnull() & (crime_df['crime_type'].str.strip() != '')]

def correct_crime_spelling(crime):
    corrections = {
        'frued': 'fraud',
        'assult': 'assault'
    }
    return corrections.get(crime.lower().strip(), crime.lower().strip())
crime_df['crime_type'] = crime_df['crime_type'].apply(correct_crime_spelling)

def convert_distance(distance_str):
    distance_str = distance_str.lower().strip()
    match = re.match(r"([\d\.]+)\s*(miles|km)", distance_str)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        return value * 1.60934 if unit == 'miles' else value
    else:
        return np.nan

crime_df['nearest_police_patrol'] = crime_df['nearest_police_patrol'].apply(convert_distance)
crime_df['timestamp'] = pd.to_datetime(crime_df['timestamp'])
crime_df['day_of_week'] = crime_df['timestamp'].dt.day_name()
crime_df['date'] = crime_df['timestamp'].dt.date
crime_df['time'] = crime_df['timestamp'].dt.time

# 3. Merge the datasets on district_id
merged_df = pd.merge(crime_df, district_df, on='district_id', how='left')
final_df = merged_df[['district_id', 'district_name', 'crime_type',
                        'nearest_police_patrol', 'population', 'governor',
                        'day_of_week', 'date', 'time']]

engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/de_db')

# Insert the DataFrame into a table named 'de_data'
merged_df.to_sql('de_data', engine, if_exists='replace', index=False)

print("Data successfully inserted into the PostgreSQL database")
print(merged_df.head(15))