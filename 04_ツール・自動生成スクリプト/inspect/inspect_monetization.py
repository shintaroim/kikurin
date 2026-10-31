import pymupdf

doc = pymupdf.open(r'c:\AI Workspace\1_Projects\きくりん\business_ideas_monetization.pdf')
for i, p in enumerate(doc):
    text = p.get_text()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    f = lines[0] if lines else 'EMPTY'
    l = lines[-1] if lines else 'EMPTY'
    print(f"Page {i+1}: lines={len(lines)}")
