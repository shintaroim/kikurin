import re
import os
import subprocess
import pymupdf

# Common CSS for professional PDF rendering
BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800&family=Outfit:wght@600;700&display=swap');

@page {
    size: A4 portrait;
    margin: 14mm 14mm 14mm 14mm;
    @bottom-right {
        content: counter(page) " / " counter(pages);
        font-size: 8pt;
        color: #94a3b8;
    }
}

* {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}

body {
    font-family: 'Noto Sans JP', 'Meiryo', 'Hiragino Sans', sans-serif;
    color: #1e293b;
    line-height: 1.6;
    font-size: 9.5pt;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
}

h1, h2, h3, h4 {
    color: #0f172a;
    font-weight: 700;
    margin-top: 1.4em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
    break-after: avoid;
}

h1 {
    font-size: 19pt;
    border-bottom: 3px solid #1e3a8a;
    padding-bottom: 6px;
    margin-top: 0;
}

h2 {
    font-size: 13.5pt;
    background: #f1f5f9;
    padding: 6px 12px;
    border-left: 5px solid #1e3a8a;
    border-radius: 2px;
}

h3 {
    font-size: 11pt;
    color: #1e3a8a;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 3px;
}

h4 {
    font-size: 10pt;
    color: #334155;
    margin-bottom: 0.3em;
}

p {
    margin: 0.5em 0;
}

/* Header Banner */
.doc-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 8px;
    margin-bottom: 18px;
}
.doc-header h1 {
    color: #ffffff;
    border-bottom: 2px solid #38bdf8;
    font-size: 18pt;
    margin: 0 0 6px 0;
    padding-bottom: 4px;
}
.doc-header .concept {
    font-size: 9.5pt;
    color: #cbd5e1;
    margin: 0;
}

/* Callout / Blockquote */
blockquote, .callout {
    background: #f8fafc;
    border-left: 4px solid #0284c7;
    padding: 8px 14px;
    margin: 10px 0;
    border-radius: 0 6px 6px 0;
    font-size: 9pt;
    color: #334155;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
    break-inside: avoid;
}
th {
    background: #1e3a8a;
    color: #ffffff;
    font-weight: 700;
    padding: 7px 8px;
    text-align: left;
    border: 1px solid #1e3a8a;
}
td {
    padding: 6px 8px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
}
tr:nth-child(even) td {
    background-color: #f8fafc;
}

/* Cards */
.card-grid {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin: 10px 0;
}
.card {
    background: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    overflow: hidden;
    page-break-inside: avoid;
    break-inside: avoid;
    margin-bottom: 10px;
}
.card-header {
    background: #f1f5f9;
    border-bottom: 1.5px solid #cbd5e1;
    padding: 6px 12px;
    font-size: 10pt;
    font-weight: 700;
    color: #0f172a;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.card-body {
    padding: 8px 12px;
    display: grid;
    grid-template-columns: 85px 1fr;
    gap: 5px 10px;
    font-size: 8.5pt;
}
.card-label {
    font-weight: 700;
    color: #475569;
    display: flex;
    align-items: center;
    background: #f8fafc;
    padding: 2px 6px;
    border-radius: 4px;
}
.card-value {
    color: #1e293b;
    padding: 2px 0;
}
.card-value strong {
    color: #b45309;
}

/* Funnel Steps */
.funnel-container {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin: 12px 0;
    page-break-inside: avoid;
    break-inside: avoid;
}
.funnel-step {
    border-radius: 6px;
    padding: 8px 14px;
    color: #ffffff;
}
.funnel-step-1 { background: #0284c7; }
.funnel-step-2 { background: #0369a1; }
.funnel-step-3 { background: #1e3a8a; }
.funnel-step-4 { background: #0f172a; }
.funnel-step-title {
    font-weight: 700;
    font-size: 9pt;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.funnel-step-desc {
    font-size: 8.2pt;
    color: #e2e8f0;
}

/* Page Break Helpers */
.page-break {
    page-break-before: always;
    break-before: page;
}
.no-break {
    page-break-inside: avoid;
    break-inside: avoid;
}

/* Mermaid SVG container */
.mermaid-box {
    text-align: center;
    margin: 10px 0;
    page-break-inside: avoid;
    break-inside: avoid;
    background: #f8fafc;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #e2e8f0;
}
"""

print("Base CSS configured successfully.")
