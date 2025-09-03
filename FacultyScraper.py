import re
import pandas as pd

with open("colleges_faculty_links.txt","r",encoding="utf-8") as f:
    raw = f.read()

cleaned = re.sub(r"[\*'`\"]|^\s*[-+]\s*|^\s*#{1,6}\s*", "", raw)
pattern = re.compile(r"(?:(?:\*|-)\s*)?([^\n:]+):\s*(\S+)")

rows = []
for match in pattern.finditer(cleaned):
    name,link = match.groups()
    rows.append({"name": name.strip(), "link": link.strip()})

df = pd.DataFrame(rows)
df.to_csv("colleges_faculty_links.csv", index=False)
print(f"Extracted faculty links for {len(rows)} colleges.")