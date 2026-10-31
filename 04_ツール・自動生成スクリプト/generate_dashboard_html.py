import re
import os
from rich_components import generate_svg_pie_chart, generate_svg_roadmap_gantt

def build_v2_dashboard_html():
    with open(r'c:\AI Workspace\1_Projects\きくりん\business_catalog_dashboard.md', 'r', encoding='utf-8') as f:
        md = f.read()

    # 1. Replace pie chart with colorful enlarged SVG Donut Chart
    pie_svg = generate_svg_pie_chart()
    md = re.sub(
        r'### 🎯 目標年商 3,000万円（月商250万円）の構成比率[\s\S]+?```mermaid[\s\S]+?```',
        f'<div class="page-1-chart">{pie_svg}</div>',
        md
    )

    # 2. Replace gantt chart with colorful enlarged Roadmap Timeline
    gantt_svg = generate_svg_roadmap_gantt()
    md = re.sub(
        r'## 📅 【直感ロードマップ】年商3,000万円達成の4四半期アクション[\s\S]+?```mermaid[\s\S]+?```',
        f'___ROADMAP_SECTION___\n{gantt_svg}',
        md
    )

    # 3. Parse ASCII Cards into rich HTML cards
    card_pattern = re.compile(
        r'```[\r\n]+┌─+┐[\r\n]+│\s*(🏷️\s*CARD\s*\d+:[^│\r\n]+)│[\r\n]+├─+┤[\r\n]+([\s\S]+?)└─+┘[\r\n]+```'
    )

    def replace_card(match):
        header_text = match.group(1).strip()
        body_text = match.group(2).strip()
        
        rows_html = []
        for line in body_text.splitlines():
            line = line.strip()
            if not line.startswith('│') or not line.endswith('│'):
                continue
            content = line[1:-1].strip()
            parts = [p.strip() for p in content.split('│')]
            if len(parts) >= 2:
                label = parts[0]
                val = parts[1]
                val = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', val)
                rows_html.append(f'<div class="card-label">{label}</div><div class="card-value">{val}</div>')
        
        return f'''
        <div class="business-card no-break">
            <div class="card-header">{header_text}</div>
            <div class="card-body">
                {''.join(rows_html)}
            </div>
        </div>
        '''

    md = card_pattern.sub(replace_card, md)

    # 4. Colorful Enlarged Funnel
    funnel_pattern = re.compile(
        r'```[\r\n]+┌─+┐[\r\n]+│\s*①\s*集客・認知（無料〜低価格）\s*│[\s\S]+?└─+┘[\r\n]+```'
    )
    funnel_replacement = '''
    <div class="funnel-container no-break">
        <div class="funnel-step funnel-step-1">
            <div class="funnel-step-title">① 集客・認知（無料〜低価格フロント）</div>
            <div class="funnel-step-desc">Instagram / note / Voicy「大丈夫！ラジオ」 / 出張蕎麦打ちイベント / 話し方体験セミナー（3,000〜5,000円）</div>
        </div>
        <div class="funnel-arrow">▼ ファンが参加・継続（月額サロン＆手軽なキット）</div>
        <div class="funnel-step funnel-step-2">
            <div class="funnel-step-title">② 信頼構築・ベース収益（月額課金・キット）</div>
            <div class="funnel-step-desc">オンラインサロン「ととのえ部」（月額3,850円） / 自宅蕎麦打ちキット＆そば粉定期便 / オンライン動画講座（19,800円）</div>
        </div>
        <div class="funnel-arrow">▼ 人生変革を求める人がステップアップ</div>
        <div class="funnel-step funnel-step-3">
            <div class="funnel-step-title">③ コア高単価プログラム（高利益・人生変革）</div>
            <div class="funnel-step-desc">四国松山リトリート（250,000円） / 6ヶ月パーソナル伴走コーチング（330,000円） / 認定ファシリテーター養成講座（440,000円）</div>
        </div>
        <div class="funnel-arrow">▼ 経営者・企業が自社への導入を依頼</div>
        <div class="funnel-step funnel-step-4">
            <div class="funnel-step-title">④ 法人向けウルトラハイエンド（大口収益）</div>
            <div class="funnel-step-desc">経営者向けマインドフルネス合宿（60万〜120万円） / 企業チームビルディング研修（35万〜60万円） / 顧問ライフ＆キャリアシェルパ（月額15万〜25万円/社）</div>
        </div>
    </div>
    '''
    md = funnel_pattern.sub(funnel_replacement, md)

    # 5. Tables
    def render_tables(text):
        lines = text.splitlines()
        in_table = False
        table_lines = []
        result = []
        for line in lines:
            if '|' in line and not line.strip().startswith('```'):
                in_table = True
                table_lines.append(line)
            else:
                if in_table:
                    result.append(make_table_html(table_lines))
                    table_lines = []
                    in_table = False
                result.append(line)
        if in_table:
            result.append(make_table_html(table_lines))
        return '\n'.join(result)

    def make_table_html(tbl_lines):
        if len(tbl_lines) < 2:
            return '\n'.join(tbl_lines)
        headers = [c.strip().replace('**', '') for c in tbl_lines[0].split('|')[1:-1]]
        html = ['<table><thead><tr>']
        for h in headers:
            html.append(f'<th>{h}</th>')
        html.append('</tr></thead><tbody>')
        for row in tbl_lines[2:]:
            cells = [c.strip() for c in row.split('|')[1:-1]]
            html.append('<tr>')
            for cell in cells:
                c_fmt = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', cell)
                html.append(f'<td>{c_fmt}</td>')
            html.append('</tr>')
        html.append('</tbody></table>')
        return '\n'.join(html)

    md = render_tables(md)

    # 6. Strategic page breaks for EXACT 6-PAGE LAYOUT
    md = md.replace('### 📈 4大エンジン別 収益シミュレーション一覧表', '<div class="page-break"></div>\n### 📈 4大エンジン別 収益シミュレーション一覧表')
    md = md.replace('### ENGINE 2：🌄 高付加価値リトリート＆個人伴走', '<div class="page-break"></div>\n### ENGINE 2：🌄 高付加価値リトリート＆個人伴走')
    md = md.replace('### ENGINE 3：🔄 ストック課金＆認定・のれん分け', '<div class="page-break"></div>\n### ENGINE 3：🔄 ストック課金＆認定・のれん分け')
    md = md.replace('### ENGINE 4：📦 デジタル自動販売＆プロダクト物販', '<div class="page-break"></div>\n### ENGINE 4：📦 デジタル自動販売＆プロダクト物販')
    
    # Page 6: Roadmap + Conclusion
    md = md.replace('___ROADMAP_SECTION___', '<div class="page-break"></div>')

    # Headers
    md = re.sub(r'(?m)^# (.+)$', r'<div class="doc-header"><h1>\1</h1><div class="concept">「対話（心）」×「手打ち蕎麦（五感・身体）」の唯一無二の掛け算で、労働時間を減らしながら年商3,000万円（月商250万円）を安定構築する事業構造設計図</div></div>', md)
    md = re.sub(r'(?m)^> (.+)$', r'', md)
    md = re.sub(r'(?m)^## (.+)$', r'<h2>\1</h2>', md)
    md = re.sub(r'(?m)^### (.+)$', r'<h3>\1</h3>', md)
    md = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md)
    md = re.sub(r'(?m)^---$', r'', md)

    # Conclusion block
    conclusion_pattern = re.compile(r'(<h2>💎 結論：なぜこのモデルなら「ゆとり」と「高年収」が両立するのか？</h2>)([\s\S]+?)$')
    def replace_conclusion(m):
        h2 = m.group(1)
        body = m.group(2).strip()
        return f'''
        <div class="conclusion-box no-break">
            {h2}
            <div style="font-size: 9.2pt; line-height: 1.5; color: #1e293b; padding: 2px 4px;">
                {body}
            </div>
        </div>
        '''
    md = conclusion_pattern.sub(replace_conclusion, md)

    css = """
    @page {
        size: A4 portrait;
        margin: 10mm 14mm 10mm 14mm;
        @bottom-right {
            content: counter(page) " / " counter(pages);
            font-size: 9pt;
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
        font-size: 9.8pt;
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
        padding: 14px 20px;
        border-radius: 7px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .doc-header h1 {
        color: #ffffff;
        border-bottom: 2px solid #63b3ed;
        font-size: 17pt;
        margin: 0 0 5px 0;
        padding-bottom: 4px;
        font-weight: bold;
    }
    .doc-header .concept {
        font-size: 9.3pt;
        color: #e2e8f0;
        margin: 0;
        line-height: 1.45;
    }

    h2 {
        font-size: 12.2pt;
        color: #2b6cb0;
        border-left: 5px solid #3182ce;
        padding-left: 10px;
        margin-top: 14px;
        margin-bottom: 8px;
        page-break-after: avoid;
        break-after: avoid;
        background: #ebf8ff;
        padding-top: 4px;
        padding-bottom: 4px;
        border-radius: 0 4px 4px 0;
    }

    h3 {
        font-size: 10.8pt;
        color: #2c5282;
        border-bottom: 1.5px solid #bee3f8;
        padding-bottom: 3px;
        margin-top: 12px;
        margin-bottom: 7px;
        page-break-after: avoid;
        break-after: avoid;
    }

    p {
        margin: 0.25em 0 0.5em 0;
    }

    .no-break {
        page-break-inside: avoid;
        break-inside: avoid;
    }

    /* Table */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 8px 0 12px 0;
        font-size: 9pt;
        page-break-inside: avoid;
        break-inside: avoid;
    }
    th {
        background: #2b6cb0;
        color: #ffffff;
        font-weight: bold;
        padding: 7px 9px;
        text-align: left;
        border: 1px solid #2b6cb0;
        font-size: 9pt;
    }
    td {
        padding: 6px 9px;
        border: 1px solid #cbd5e0;
        vertical-align: middle;
        line-height: 1.4;
    }
    tr:nth-child(even) td {
        background-color: #f7fafc;
    }

    /* Business Card Style */
    .business-card {
        background: #ffffff;
        border: 1px solid #cbd5e0;
        border-left: 5px solid #3182ce;
        border-radius: 7px;
        overflow: hidden;
        page-break-inside: avoid;
        break-inside: avoid;
        margin-bottom: 9px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .card-header {
        background: #edf2f7;
        border-bottom: 1px solid #cbd5e0;
        padding: 5px 12px;
        font-size: 10pt;
        font-weight: bold;
        color: #1a365d;
    }
    .card-body {
        padding: 7px 12px;
        display: grid;
        grid-template-columns: 105px 1fr;
        gap: 4px 10px;
        font-size: 9.2pt;
    }
    .card-label {
        font-weight: bold;
        color: #4a5568;
        display: flex;
        align-items: center;
        background: #f7fafc;
        padding: 2px 7px;
        border-radius: 4px;
        white-space: nowrap;
        border: 1px solid #e2e8f0;
    }
    .card-value {
        color: #2d3748;
        padding: 1px 0;
        line-height: 1.45;
    }
    .card-value strong {
        color: #c53030;
    }

    /* Funnel Style */
    .funnel-container {
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin: 8px 0;
        page-break-inside: avoid;
        break-inside: avoid;
    }
    .funnel-step {
        border-radius: 6px;
        padding: 6px 12px;
        color: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .funnel-step-1 { background: #3182ce; }
    .funnel-step-2 { background: #2b6cb0; }
    .funnel-step-3 { background: #2c5282; }
    .funnel-step-4 { background: #1a365d; }
    .funnel-step-title {
        font-weight: bold;
        font-size: 9.5pt;
        margin-bottom: 2px;
    }
    .funnel-step-desc {
        font-size: 8.3pt;
        color: #edf2f7;
    }
    .funnel-arrow {
        text-align: center;
        font-size: 8.5pt;
        font-weight: bold;
        color: #2b6cb0;
        margin: -2px 0;
    }

    .conclusion-box {
        margin-top: 8px;
        page-break-inside: avoid;
        break-inside: avoid;
    }

    ol, ul {
        margin: 3px 0 5px 18px;
        padding: 0;
        font-size: 9.2pt;
    }
    li {
        margin-bottom: 2px;
    }
    """

    full_html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>きくりん専用：収益最大化ダッシュボード＆ビジュアルカードカタログ</title>
<style>
{css}
</style>
</head>
<body>
{md}
</body>
</html>'''

    out_path = r'c:\AI Workspace\1_Projects\きくりん\business_catalog_dashboard.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("V2 Dashboard HTML perfectly structured.")

build_v2_dashboard_html()
