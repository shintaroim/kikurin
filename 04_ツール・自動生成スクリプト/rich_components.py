import math

def generate_svg_pie_chart():
    # 40% BtoB, 25% Retreat, 20% Community, 15% Digital
    data = [
        {"label": "法人顧問・BtoB研修 (高単価)", "share": 0.40, "amount": "1,200万円 (40%)", "color": "#2563eb", "sub": "月100万円目安"},
        {"label": "高単価リトリート・個人伴走 (プレミアム)", "share": 0.25, "amount": "750万円 (25%)", "color": "#059669", "sub": "月62.5万円目安"},
        {"label": "コミュニティ・スクール認定 (ストック・のれん分け)", "share": 0.20, "amount": "600万円 (20%)", "color": "#d97706", "sub": "月50万円目安"},
        {"label": "デジタル講座・物販キット (自動化・不労)", "share": 0.15, "amount": "450万円 (15%)", "color": "#7c3aed", "sub": "月37.5万円目安"},
    ]
    
    cx, cy, r, inner_r = 135, 135, 115, 65
    start_angle = -90
    paths = []
    
    for item in data:
        angle_len = item["share"] * 360
        end_angle = start_angle + angle_len
        
        rad_start = math.radians(start_angle)
        rad_end = math.radians(end_angle)
        
        x1 = cx + r * math.cos(rad_start)
        y1 = cy + r * math.sin(rad_start)
        x2 = cx + r * math.cos(rad_end)
        y2 = cy + r * math.sin(rad_end)
        
        ix1 = cx + inner_r * math.cos(rad_end)
        iy1 = cy + inner_r * math.sin(rad_end)
        ix2 = cx + inner_r * math.cos(rad_start)
        iy2 = cy + inner_r * math.sin(rad_start)
        
        large_arc = 1 if angle_len > 180 else 0
        
        d = f"M {x1:.2f} {y1:.2f} A {r} {r} 0 {large_arc} 1 {x2:.2f} {y2:.2f} L {ix1:.2f} {iy1:.2f} A {inner_r} {inner_r} 0 {large_arc} 0 {ix2:.2f} {iy2:.2f} Z"
        paths.append(f'<path d="{d}" fill="{item["color"]}" stroke="#ffffff" stroke-width="2.5" />')
        
        start_angle = end_angle

    legend_items = []
    for item in data:
        legend_items.append(f'''
        <div style="display: flex; align-items: flex-start; gap: 8px; margin-bottom: 7px;">
            <div style="width: 14px; height: 14px; border-radius: 3px; background: {item["color"]}; flex-shrink: 0; margin-top: 3px;"></div>
            <div>
                <div style="font-weight: bold; font-size: 9.5pt; color: #1e293b;">{item["label"]}</div>
                <div style="font-size: 9pt; color: #475569;"><strong style="color: {item["color"]}; font-size: 10.5pt;">{item["amount"]}</strong> <span style="font-size: 8pt; color: #64748b;">({item["sub"]})</span></div>
            </div>
        </div>
        ''')

    svg_chart = f'''
    <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 12px 18px; margin: 10px 0 14px 0; box-shadow: 0 1px 4px rgba(0,0,0,0.04); page-break-inside: avoid;">
        <div style="text-align: center; font-weight: bold; font-size: 11.5pt; color: #1e3a8a; margin-bottom: 10px; letter-spacing: 0.5px;">
            📊 年商3,000万円（月商250万円）収益ポートフォリオ構成
        </div>
        <div style="display: flex; align-items: center; justify-content: center; gap: 28px; flex-wrap: nowrap;">
            <div style="position: relative; width: 270px; height: 270px; flex-shrink: 0;">
                <svg width="270" height="270" viewBox="0 0 270 270">
                    {''.join(paths)}
                </svg>
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; pointer-events: none;">
                    <div style="font-size: 8pt; color: #64748b; font-weight: 600;">目標年商</div>
                    <div style="font-size: 13pt; font-weight: 800; color: #0f172a;">3,000万円</div>
                    <div style="font-size: 8pt; color: #0284c7; font-weight: 700;">(月商250万)</div>
                </div>
            </div>
            <div style="flex: 1; min-width: 250px;">
                {''.join(legend_items)}
            </div>
        </div>
    </div>
    '''
    return svg_chart

def generate_svg_roadmap_gantt():
    gantt_html = '''
    <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 14px 16px; margin: 12px 0; box-shadow: 0 1px 4px rgba(0,0,0,0.04); page-break-inside: avoid;">
        <div style="text-align: center; font-weight: bold; font-size: 11.5pt; color: #1e3a8a; margin-bottom: 12px;">
            📅 年商3,000万円実現 4四半期実行ロードマップ
        </div>
        <div style="display: flex; flex-direction: column; gap: 9px;">
            <!-- Q1 -->
            <div style="display: grid; grid-template-columns: 130px 1fr; gap: 10px; align-items: center;">
                <div style="background: #eff6ff; border: 1.2px solid #bfdbfe; border-radius: 5px; padding: 6px 8px; text-align: center;">
                    <div style="font-weight: 800; color: #1e40af; font-size: 9.5pt;">Q1 (1〜3ヶ月)</div>
                    <div style="font-size: 7.5pt; color: #3b82f6;">高単価商品の確立</div>
                </div>
                <div style="background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%); color: #ffffff; padding: 7px 12px; border-radius: 5px; box-shadow: 0 1px 2px rgba(59,130,246,0.25);">
                    <div style="font-weight: bold; font-size: 9pt;">単発セッション廃止・値上げ ➔ 四国リトリート＆6ヶ月伴走LP完成</div>
                    <div style="font-size: 8pt; color: #eff6ff; margin-top: 1px;">★既存顧客へ先行オファー実施（目標：モニター成約で300万円突破）</div>
                </div>
            </div>
            <!-- Q2 -->
            <div style="display: grid; grid-template-columns: 130px 1fr; gap: 10px; align-items: center;">
                <div style="background: #ecfdf5; border: 1.2px solid #a7f3d0; border-radius: 5px; padding: 6px 8px; text-align: center;">
                    <div style="font-weight: 800; color: #065f46; font-size: 9.5pt;">Q2 (4〜6ヶ月)</div>
                    <div style="font-size: 7.5pt; color: #10b981;">法人BtoB展開</div>
                </div>
                <div style="background: linear-gradient(90deg, #059669 0%, #34d399 100%); color: #ffffff; padding: 7px 12px; border-radius: 5px; box-shadow: 0 1px 2px rgba(5,150,105,0.25);">
                    <div style="font-weight: bold; font-size: 9pt;">企業向け研修・顧問提案書作成 ➔ 経営者合宿＆チーム研修の受注</div>
                    <div style="font-size: 8pt; color: #ecfdf5; margin-top: 1px;">★同友会・商工会議所・ベンチャー経営者コミュニティへアプローチ（月商100万達成）</div>
                </div>
            </div>
            <!-- Q3 -->
            <div style="display: grid; grid-template-columns: 130px 1fr; gap: 10px; align-items: center;">
                <div style="background: #fffbeb; border: 1.2px solid #fde68a; border-radius: 5px; padding: 6px 8px; text-align: center;">
                    <div style="font-weight: 800; color: #92400e; font-size: 9.5pt;">Q3 (7〜9ヶ月)</div>
                    <div style="font-size: 7.5pt; color: #d97706;">ストック化・サロン</div>
                </div>
                <div style="background: linear-gradient(90deg, #d97706 0%, #fbbf24 100%); color: #ffffff; padding: 7px 12px; border-radius: 5px; box-shadow: 0 1px 2px rgba(217,119,6,0.25);">
                    <div style="font-weight: bold; font-size: 9pt;">オンラインサロン「ととのえ部」開設 ➔ 会員100名突破・月額固定収益化</div>
                    <div style="font-size: 8pt; color: #fffbeb; margin-top: 1px;">★「魔法の質問」と「大丈夫の言霊」で毎朝配信。ベース固定費を完全ストック化</div>
                </div>
            </div>
            <!-- Q4 -->
            <div style="display: grid; grid-template-columns: 130px 1fr; gap: 10px; align-items: center;">
                <div style="background: #f5f3ff; border: 1.2px solid #ddd6fe; border-radius: 5px; padding: 6px 8px; text-align: center;">
                    <div style="font-weight: 800; color: #5b21b6; font-size: 9.5pt;">Q4 (10〜12ヶ月)</div>
                    <div style="font-size: 7.5pt; color: #8b5cf6;">自動化・認定制度</div>
                </div>
                <div style="background: linear-gradient(90deg, #7c3aed 0%, #a78bfa 100%); color: #ffffff; padding: 7px 12px; border-radius: 5px; box-shadow: 0 1px 2px rgba(124,58,237,0.25);">
                    <div style="font-weight: bold; font-size: 9pt;">「蕎麦打ちマインドフルネス®」認定講座開講 ➔ 動画講座・定期便の自動販売</div>
                    <div style="font-size: 8pt; color: #f5f3ff; margin-top: 1px;">★のれん分け認定講師の育成＆D2C蕎麦打ちキット自動販売で年商3,000万円体制完成</div>
                </div>
            </div>
        </div>
    </div>
    '''
    return gantt_html
