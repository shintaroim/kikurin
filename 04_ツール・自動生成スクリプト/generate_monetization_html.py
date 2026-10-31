import re
import os

def build_v2_monetization_html():
    with open(r'c:\AI Workspace\1_Projects\きくりん\business_ideas_monetization.md', 'r', encoding='utf-8') as f:
        md = f.read()

    # 1. Colorful enlarged Funnel Map (Horizontal Grid)
    funnel_html = '''
    <div class="funnel-grid-container no-break">
        <div class="funnel-col col-1">
            <div class="funnel-col-header">① 集客・認知（フロント）</div>
            <div class="funnel-items">
                <div class="f-item">SNS / note / Voicy / Instagram</div>
                <div class="f-item">公式LINE / メルマガ</div>
                <div class="f-item">商業出版 / メディア取材</div>
                <div class="f-item highlight">体験蕎麦打ちWS / 話し方単発講座<br><strong style="color: #c53030;">（5,000円〜1万円）</strong></div>
            </div>
        </div>
        <div class="funnel-arrow-col">➔</div>
        <div class="funnel-col col-2">
            <div class="funnel-col-header">② 継続・信頼（ミドル）</div>
            <div class="funnel-items">
                <div class="f-item">月額サロン「ととのえ部」<br><strong style="color: #2b6cb0;">（月額3,300〜5,500円）</strong></div>
                <div class="f-item">自宅用蕎麦打ちキット＆定期便</div>
                <div class="f-item">オンライン動画講座<br><strong style="color: #2b6cb0;">（1.5万〜5万円）</strong></div>
            </div>
        </div>
        <div class="funnel-arrow-col">➔</div>
        <div class="funnel-col col-3">
            <div class="funnel-col-header">③ 高収益コア（バックエンド）</div>
            <div class="funnel-items">
                <div class="f-item">6ヶ月伴走グループコーチング<br><strong style="color: #2b6cb0;">（30万〜50万円）</strong></div>
                <div class="f-item">四国・松山プレミアムリトリート<br><strong style="color: #2b6cb0;">（15万〜35万円）</strong></div>
                <div class="f-item">蕎麦打ちファシリテーター養成<br><strong style="color: #2b6cb0;">（40万〜60万円）</strong></div>
            </div>
        </div>
        <div class="funnel-arrow-col">➔</div>
        <div class="funnel-col col-4">
            <div class="funnel-col-header">④ 法人（ウルトラハイエンド）</div>
            <div class="funnel-items">
                <div class="f-item">企業オフサイト・チーム研修<br><strong style="color: #1a365d;">（50万〜100万円）</strong></div>
                <div class="f-item">経営者向け個別リトリート<br><strong style="color: #1a365d;">（50万〜150万円）</strong></div>
                <div class="f-item">顧問キャリアシェルパ<br><strong style="color: #1a365d;">（月額15万〜30万円/社）</strong></div>
            </div>
        </div>
    </div>
    '''
    md = re.sub(r'```mermaid[\r\n]+flowchart TD[\s\S]+?```', funnel_html, md)

    # 2. Idea Blocks into structured cards
    def parse_ideas(text):
        pattern = re.compile(r'(####\s+\d+\.[^\n]+)([\s\S]+?)(?=(####|\#\#\#|\#\#|\Z))')
        def replace_fn(m):
            title = m.group(1).replace('####', '').strip()
            body = m.group(2).strip()
            
            rows = []
            for line in body.splitlines():
                line = line.strip()
                if not line:
                    continue
                match = re.match(r'^[\*\-]\s*\*\*(.+?)\*\*[:：]?\s*(.+)$', line)
                if match:
                    label = match.group(1).strip()
                    val = match.group(2).strip()
                    val = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', val)
                    rows.append(f'<div class="idea-row"><span class="idea-label">{label}</span><span class="idea-val">{val}</span></div>')
                else:
                    c = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line).lstrip('*- ').strip()
                    if c:
                        rows.append(f'<div class="idea-row"><span class="idea-val" style="grid-column: 1 / -1;">{c}</span></div>')

            return f'''
            <div class="business-card no-break">
                <div class="card-header">💡 {title}</div>
                <div class="card-body">
                    {''.join(rows)}
                </div>
            </div>
            \n\n'''
        return pattern.sub(replace_fn, text)

    md = parse_ideas(md)

    # Clean list items first
    lines = md.splitlines()
    out_lines = []
    in_ul = False
    for line in lines:
        sline = line.strip()
        if sline.startswith('* ') or sline.startswith('- '):
            if not in_ul:
                out_lines.append('<ul>')
                in_ul = True
            item_text = sline[2:].strip()
            out_lines.append(f'<li>{item_text}</li>')
        else:
            if in_ul:
                out_lines.append('</ul>')
                in_ul = False
            out_lines.append(line)
    if in_ul:
        out_lines.append('</ul>')
    html_body = '\n'.join(out_lines)

    # Headers
    html_body = re.sub(r'(?m)^# (.+)$', r'<div class="doc-header"><h1>\1</h1><div class="concept">独自の強み（対話×五感・手打ち蕎麦）を最大活用した事業ポートフォリオ戦略</div></div>', html_body)
    html_body = re.sub(r'(?m)^## (.+)$', r'<h2>\1</h2>', html_body)
    html_body = re.sub(r'(?m)^### (.+)$', r'<h3>\1</h3>', html_body)
    html_body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_body)

    # Strategic Page Breaks for Monetization:
    # Force page break before Funnel section so Page 6 has Funnel + Roadmap + Summary
    html_body = re.sub(
        r'(<h2>経済的自由を達成するための「収益導線（ファネル設計）」</h2>)',
        r'<div class="page-break"></div>\n\1',
        html_body
    )

    css = """
    @page {
        size: A4 portrait;
        margin: 9.5mm 13.5mm 9.5mm 13.5mm;
        @bottom-right {
            content: counter(page) " / " counter(pages);
            font-size: 8.5pt;
            color: #718096;
        }
    }

    * {
        box-sizing: border-box;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    body {
        font-family: "BIZ UDPGothic", "Meiryo", "Yu Gothic", "Hiragino Kaku Gothic ProN", sans-serif;
        color: #2d3748;
        line-height: 1.5;
        font-size: 9.5pt;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }

    .page-break {
        page-break-before: always;
        break-before: page;
    }

    .doc-header {
        background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 7px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .doc-header h1 {
        color: #ffffff;
        border-bottom: 2px solid #63b3ed;
        font-size: 15.5pt;
        margin: 0 0 4px 0;
        padding-bottom: 3px;
        font-weight: bold;
    }
    .doc-header .concept {
        font-size: 9pt;
        color: #e2e8f0;
        margin: 0;
    }

    h2 {
        font-size: 11.8pt;
        color: #2b6cb0;
        border-left: 5px solid #3182ce;
        padding-left: 9px;
        margin-top: 12px;
        margin-bottom: 7px;
        page-break-after: avoid;
        break-after: avoid;
        background: #ebf8ff;
        padding-top: 3px;
        padding-bottom: 3px;
        border-radius: 0 4px 4px 0;
    }

    h3 {
        font-size: 10.2pt;
        color: #2c5282;
        border-bottom: 1.5px solid #bee3f8;
        padding-bottom: 2px;
        margin-top: 10px;
        margin-bottom: 6px;
        page-break-after: avoid;
        break-after: avoid;
    }

    p {
        margin: 0.25em 0 0.45em 0;
    }

    ul, ol {
        margin: 3px 0 5px 16px;
        padding: 0;
        font-size: 9pt;
    }
    li {
        margin-bottom: 2px;
    }

    .no-break {
        page-break-inside: avoid;
        break-inside: avoid;
    }

    /* Business Card Style */
    .business-card {
        background: #ffffff;
        border: 1px solid #cbd5e0;
        border-left: 5px solid #3182ce;
        border-radius: 6px;
        overflow: hidden;
        page-break-inside: avoid;
        break-inside: avoid;
        margin-bottom: 6px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .card-header {
        background: #edf2f7;
        border-bottom: 1px solid #cbd5e0;
        padding: 4px 10px;
        font-size: 9.8pt;
        font-weight: bold;
        color: #1a365d;
    }
    .card-body {
        padding: 6px 10px;
        display: flex;
        flex-direction: column;
        gap: 2.5px;
    }
    .idea-row {
        display: grid;
        grid-template-columns: 82px 1fr;
        gap: 6px;
        font-size: 8.8pt;
        line-height: 1.35;
    }
    .idea-label {
        font-weight: bold;
        color: #4a5568;
        background: #f7fafc;
        padding: 1px 5px;
        border-radius: 3px;
        text-align: center;
        height: fit-content;
        white-space: nowrap;
        border: 1px solid #e2e8f0;
    }
    .idea-val {
        color: #2d3748;
    }
    .idea-val strong {
        color: #c53030;
    }

    /* Horizontal Funnel Grid */
    .funnel-grid-container {
        display: grid;
        grid-template-columns: 1fr 18px 1fr 18px 1fr 18px 1fr;
        align-items: stretch;
        gap: 4px;
        margin: 8px 0 12px 0;
        page-break-inside: avoid;
        break-inside: avoid;
    }
    .funnel-col {
        border-radius: 6px;
        overflow: hidden;
        border: 1px solid #cbd5e0;
        display: flex;
        flex-direction: column;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .funnel-col-header {
        color: #ffffff;
        font-weight: bold;
        font-size: 8.3pt;
        padding: 5px 3px;
        text-align: center;
    }
    .col-1 .funnel-col-header { background: #3182ce; }
    .col-2 .funnel-col-header { background: #2b6cb0; }
    .col-3 .funnel-col-header { background: #2c5282; }
    .col-4 .funnel-col-header { background: #1a365d; }

    .funnel-items {
        background: #f8fafc;
        padding: 5px 4px;
        display: flex;
        flex-direction: column;
        gap: 3px;
        flex-grow: 1;
    }
    .f-item {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 3px;
        font-size: 7.8pt;
        line-height: 1.25;
        text-align: center;
    }
    .f-item.highlight {
        background: #fffaf0;
        border-color: #fbd38d;
    }
    .funnel-arrow-col {
        display: flex;
        align-items: center;
        justify-content: center;
        color: #3182ce;
        font-weight: bold;
        font-size: 11pt;
    }
    """

    full_html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>きくりん（菊池 伸哉 氏）収益最大化＆ビジネスアイデア大全</title>
<style>
{css}
</style>
</head>
<body>
{html_body}
</body>
</html>'''

    out_path = r'c:\AI Workspace\1_Projects\きくりん\business_ideas_monetization.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("V2 Monetization HTML re-optimized.")

build_v2_monetization_html()
