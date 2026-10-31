import sys

with open(r'c:\AI Workspace\1_Projects\きくりん\business_catalog_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('顧客が自然に高単価へ進む')
sys.stdout.buffer.write(text[idx-200:idx].encode('utf-8'))
