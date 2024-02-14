#!c:\Python27\python.exe
#-*- coding: ibm852 -*-

import pandas as pd
import matplotlib.pyplot as plt
import csv

# Pobranie danych ze strony internetowej.
url = 'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=data/une_rt_m.tsv.gz'
df = pd.read_csv(url, sep='\t', compression='gzip', header=0)

# usuni©cie niepotrzebnych wierszy i kolumn.
df = df.iloc[:, [0, 4]]
df = df.drop(index=list(range(0, 74)) + list(range(82, 84))+list(range(95, 96)) + list(range(109, len(df))))

# usuni©cie zb©dnych oznaczeä.
df.iloc[:, 0] = df.iloc[:, 0].str.replace('NSA,TOTAL,PC_ACT,T,', '')
col_names = {}
for col in df.columns:
    new_col = col.replace('s_adj,age,unit,sex,', '')
    col_names[col] = new_col

# zamian kodu paästwa na jego peˆn¥ nazw© i zapisanie pliku csv.
df = df.rename(columns=col_names)
country_codes = {
    'AT': 'Austria',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CY': 'Cyprus',
    'CZ': 'Czechia',
    'DE': 'Germany',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'EL': 'Greece',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IT': 'Italy',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'TR': 'Turkey',
    'NO': 'Norway',
    'CH': 'Switzerland',
    'IS': 'Iceland',
    'EU27_2020': 'EU27_2020'
}
df['geo\\time'] = df['geo\\time'].replace(country_codes)
df.to_csv('dane_przefiltorwane.csv', index=False)

# Posortowanie warto˜ci stopy bezrobocia rosn¥co i zapisanie posortowanego pliku.
with open('dane_przefiltorwane.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    sorted_rows = sorted(reader,
                         key=lambda row: float(row[1]))
with open('dane_przefiltorwane.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(sorted_rows)
df = pd.read_csv('dane_przefiltorwane.csv')

# Utowrzenie wykresu sˆupkowego i zapisanie go jako plik ".png".
df = df.rename(columns={'geo\\time': 'Paästwa'}).set_index('Paästwa')
plt.figure(figsize=(10, 5))
ax = df.plot(kind='bar')
ax.patches[0].set_facecolor('green')
ax.patches[-1].set_facecolor('red')
plt.xticks(rotation=0)
plt.ylabel('Stopa bezrobocia [%]')
plt.title('Stopa bezrobocia w krajach UE w grudniu 2022 roku')
labels = df.index.tolist()
plt.gca().set_xticklabels(labels, rotation=90, ha='right')
plt.subplots_adjust(bottom=0.25)
plt.xlabel('Paästwa')
plt.savefig('wykres.png', dpi=300, bbox_inches='tight')
plt.show()
