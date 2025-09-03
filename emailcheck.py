import pandas as pd
import re
import requests
from tqdm import tqdm

INPUT_CSV = 'colleges_faculty_links.csv'
OUTPUT_CSV = 'college_links_checked.csv'

def clean_link(raw):
    link_md = re.search(r'\(([a-zA-Z0-9:/\-\._%#?&=+~,]+)\)', str(raw))
    if link_md:
        url = link_md.group(1)
    else:
        url = str(raw)
    url = re.sub(r'\[\d+\]$', '', url)
    url = re.sub(r'\[\d+\]', '', url)
    url = url.strip(" .,")
    url = url.strip()
    return url

def is_pdf(url):
    return str(url).lower().strip().endswith('.pdf')

def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code < 200 or response.status_code >= 400:
            response = requests.get(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

df = pd.read_csv(INPUT_CSV, encoding='utf-8', dtype=str)
df['Cleaned Link'] = df['link'].apply(clean_link)
df['Is PDF'] = df['Cleaned Link'].apply(is_pdf)
exists_list = []
for raw_url in tqdm(df['Cleaned Link'], desc="Checking URLs"):
    url = str(raw_url).strip()
    if pd.isna(url) or url == '':
        exists_list.append(False)
    else:
        if url.startswith('//'):
            url = 'https:' + url
        if url.startswith('http') or url.startswith('https'):
            exists_list.append(check_url(url))
        else:
            exists_list.append(False)


df['Exists'] = exists_list
df_out = df[['name', 'Cleaned Link', 'Is PDF', 'Exists']]
df_out.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
print(f"Done! Output written to: {OUTPUT_CSV}")
print(f"Total valid links found: {df_out['Exists'].sum()}")
