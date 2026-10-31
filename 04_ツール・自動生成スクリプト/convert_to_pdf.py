import subprocess
import os
import pymupdf

edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
work_dir = r'c:\AI Workspace\1_Projects\きくりん'

files = [
    ('business_catalog_dashboard.html', 'business_catalog_dashboard.pdf'),
    ('business_ideas_monetization.html', 'business_ideas_monetization.pdf')
]

for html_name, pdf_name in files:
    html_path = os.path.join(work_dir, html_name)
    pdf_path = os.path.join(work_dir, pdf_name)
    
    print(f"Converting {html_name} to {pdf_name}...")
    cmd = [
        edge,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--no-pdf-header-footer',
        '--virtual-time-budget=8000',
        f'--print-to-pdf={pdf_path}',
        html_path
    ]
    res = subprocess.run(cmd)
    
    if os.path.exists(pdf_path):
        doc = pymupdf.open(pdf_path)
        print(f"SUCCESS: {pdf_name} generated with {len(doc)} pages.")
        # Render pages to PNG for visual inspection
        img_dir = os.path.join(work_dir, f"preview_{pdf_name.replace('.pdf', '')}")
        os.makedirs(img_dir, exist_ok=True)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            img_path = os.path.join(img_dir, f"page_{i+1}.png")
            pix.save(img_path)
        print(f"Rendered {len(doc)} preview images in {img_dir}")
    else:
        print(f"ERROR: Failed to generate {pdf_name}")
