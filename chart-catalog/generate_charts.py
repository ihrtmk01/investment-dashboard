#!/usr/bin/env python3
"""Generate 77-chart economic indicator samples HTML."""

# ── Chart definitions: (id, name, category, badge_class, chart_type_label) ──
CHARTS = [
    # 棒グラフ系
    (1, "棒グラフ", "bar", "cb-bar", "Bar"),
    (2, "横棒グラフ", "bar", "cb-bar", "H-Bar"),
    (3, "積み上げ棒", "bar", "cb-bar", "Stacked"),
    (4, "100%積み上げ棒", "bar", "cb-bar", "100% Stacked"),
    (5, "グループ棒", "bar", "cb-bar", "Grouped"),
    (6, "発散棒グラフ", "bar", "cb-bar", "Diverging"),
    # 折れ線系
    (7, "スロープチャート", "line", "cb-line", "Slope"),
    (8, "スパークライン", "line", "cb-line", "Sparkline"),
    (9, "レーダーチャート", "line", "cb-line", "Radar"),
    (10, "折れ線グラフ", "line", "cb-line", "Line"),
    (11, "多軸折れ線", "line", "cb-line", "Dual Axis"),
    (12, "ステップライン", "line", "cb-line", "Step"),
    # エリア系
    (13, "エリアチャート", "area", "cb-line", "Area"),
    (14, "積み上げエリア", "area", "cb-line", "Stacked Area"),
    (15, "100%積み上げエリア", "area", "cb-line", "100% Area"),
    # 時系列系
    (16, "カレンダーヒートマップ", "time", "cb-map", "Calendar"),
    (17, "ガントチャート", "time", "cb-special", "Gantt"),
    (18, "タイムライン", "time", "cb-special", "Timeline"),
    (19, "期間比較チャート", "time", "cb-line", "Period"),
    (20, "ローソク足", "time", "cb-special", "Candlestick"),
    # 分布・統計系
    (21, "ヒストグラム", "stat", "cb-other", "Histogram"),
    (22, "度数ポリゴン", "stat", "cb-other", "Freq Polygon"),
    (23, "箱ひげ図", "stat", "cb-other", "Box Plot"),
    (24, "バイオリンプロット", "stat", "cb-other", "Violin"),
    (25, "ストリップチャート", "stat", "cb-other", "Strip"),
    (26, "QQプロット", "stat", "cb-other", "QQ Plot"),
    (27, "累積分布関数", "stat", "cb-other", "CDF"),
    (28, "リッジラインプロット", "stat", "cb-other", "Ridgeline"),
    # 散布図系
    (29, "散布図（4象限）", "scatter", "cb-scatter", "Scatter"),
    (30, "回帰直線付き散布図", "scatter", "cb-scatter", "Regression"),
    (31, "バブルチャート", "scatter", "cb-scatter", "Bubble"),
    (32, "相関マトリックス", "scatter", "cb-scatter", "Corr Matrix"),
    # ヒートマップ系
    (33, "ヒートマップ", "heat", "cb-map", "Heatmap"),
    # ネットワーク・フロー系
    (34, "ネットワーク図", "network", "cb-special", "Network"),
    (35, "サンキーダイアグラム", "network", "cb-special", "Sankey"),
    (36, "コードダイアグラム", "network", "cb-special", "Chord"),
    (37, "フローチャート", "network", "cb-special", "Flow"),
    # 階層系
    (38, "ツリーマップ", "hierarchy", "cb-other", "Treemap"),
    (39, "サンバースト", "hierarchy", "cb-pie", "Sunburst"),
    (40, "デンドログラム", "hierarchy", "cb-other", "Dendro"),
    (41, "パックドバブル", "hierarchy", "cb-other", "Packed"),
    (42, "アイシクルチャート", "hierarchy", "cb-other", "Icicle"),
    (43, "ツリー図", "hierarchy", "cb-other", "Tree"),
    # 円系
    (44, "ドーナツチャート", "pie", "cb-pie", "Doughnut"),
    (45, "円グラフ", "pie", "cb-pie", "Pie"),
    # 特殊棒系
    (46, "パレート図", "special_bar", "cb-bar", "Pareto"),
    (47, "ウォーターフォール", "special_bar", "cb-bar", "Waterfall"),
    (48, "マリメッコチャート", "special_bar", "cb-bar", "Marimekko"),
    (49, "ロリポップチャート", "special_bar", "cb-bar", "Lollipop"),
    # ファネル
    (50, "ファネルチャート", "funnel", "cb-pie", "Funnel"),
    # 地理系
    (51, "コロプレスマップ", "geo", "cb-map", "Choropleth"),
    (52, "バブルマップ", "geo", "cb-map", "Bubble Map"),
    (53, "ドットマップ", "geo", "cb-map", "Dot Map"),
    (54, "フローマップ", "geo", "cb-map", "Flow Map"),
    # ランキング系
    (55, "バンプチャート", "rank", "cb-line", "Bump"),
    (56, "ランクチャート", "rank", "cb-line", "Rank"),
    (57, "平行座標プロット", "rank", "cb-line", "Parallel"),
    (58, "ダンベルチャート", "rank", "cb-bar", "Dumbbell"),
    # KPI系
    (59, "ブレットチャート", "kpi", "cb-bar", "Bullet"),
    (60, "KPIカード", "kpi", "cb-other", "KPI Card"),
    (61, "進捗バー", "kpi", "cb-other", "Progress"),
    (62, "ゲージチャート", "kpi", "cb-other", "Gauge"),
    (63, "ワッフルチャート", "kpi", "cb-other", "Waffle"),
    (64, "スピードメーター", "kpi", "cb-other", "Speedo"),
    # テキスト・テーブル系
    (65, "データテーブル", "text", "cb-other", "Table"),
    (66, "スパークバー", "text", "cb-bar", "Spark Bar"),
    (67, "ミニチャート付テーブル", "text", "cb-other", "Mini Chart"),
    (68, "アノテーション付チャート", "text", "cb-line", "Annotated"),
    (69, "スモールマルチプル", "text", "cb-other", "Small Multi"),
    (70, "ワードクラウド", "text", "cb-other", "Word Cloud"),
    # 複合系
    (71, "複合チャート", "combo", "cb-bar", "Combo"),
    (72, "ダッシュボードパネル", "combo", "cb-other", "Panel"),
    (73, "比較ダッシュボード", "combo", "cb-other", "Compare"),
    (74, "トレンドインジケーター", "combo", "cb-line", "Trend"),
    (75, "ベンチマーク比較", "combo", "cb-bar", "Benchmark"),
    (76, "セグメント比較", "combo", "cb-bar", "Segment"),
    (77, "サマリーダッシュボード", "combo", "cb-other", "Summary"),
]

CATEGORIES = [
    ("bar", "棒グラフ系", "#2563EB", "棒"),
    ("line", "折れ線系", "#059669", "線"),
    ("area", "エリア系", "#10B981", "面"),
    ("time", "時系列系", "#0891B2", "時"),
    ("stat", "分布・統計系", "#475569", "統"),
    ("scatter", "散布図・相関系", "#D97706", "散"),
    ("heat", "ヒートマップ系", "#0891B2", "熱"),
    ("network", "ネットワーク・フロー系", "#E11D48", "流"),
    ("hierarchy", "階層・構造系", "#7C3AED", "階"),
    ("pie", "円・ドーナツ系", "#8B5CF6", "円"),
    ("special_bar", "特殊棒・比較系", "#2563EB", "比"),
    ("funnel", "ファネル系", "#7C3AED", "漏"),
    ("geo", "地理系", "#0891B2", "地"),
    ("rank", "ランキング系", "#059669", "順"),
    ("kpi", "KPI・ゲージ系", "#D97706", "KPI"),
    ("text", "テキスト・テーブル系", "#475569", "表"),
    ("combo", "複合・ダッシュボード系", "#E11D48", "合"),
]

def main():
    parts = []
    # HEAD
    parts.append(HEAD)
    # HERO + TOC
    parts.append(build_hero_toc())
    # Each category
    for cat_id, cat_name, cat_color, cat_icon in CATEGORIES:
        charts_in_cat = [c for c in CHARTS if c[2] == cat_id]
        if not charts_in_cat:
            continue
        parts.append(f'''
  <div class="cat-header" id="cat-{cat_id}">
    <div class="cat-icon" style="background:{cat_color};">{cat_icon}</div>
    <h2>{cat_name}</h2>
    <span class="cat-count">{len(charts_in_cat)}チャート</span>
  </div>
  <div class="chart-grid">''')
        for cid, cname, _, badge, tlabel in charts_in_cat:
            parts.append(build_chart_card(cid, cname, badge, tlabel))
        parts.append('  </div>')
    # FOOTER + SCRIPT
    parts.append(FOOTER)
    parts.append(SCRIPT)
    parts.append('</div>\n</body>\n</html>')

    with open('chart-samples.html', 'w') as f:
        f.write('\n'.join(parts))
    print("Done: 77 charts generated.")


def build_hero_toc():
    toc_items = ''.join(
        f'<a class="toc-item" href="#chart-{c[0]}"><span class="toc-num">#{c[0]}</span>{c[1]}</a>'
        for c in CHARTS
    )
    return f'''
  <div class="hero">
    <h1>経済指標チャートサンプル集</h1>
    <p>市場調査ダッシュボード v3.0 — 全77仕様チャートをサンプルデータで描画</p>
    <div class="badges">
      <span class="badge">77 チャート</span>
      <span class="badge">17 カテゴリ</span>
      <span class="badge">Chart.js 4.x</span>
    </div>
  </div>
  <div class="toc">
    <h2>チャート目次（77種）</h2>
    <div class="toc-grid">{toc_items}</div>
  </div>'''


def build_chart_card(cid, cname, badge, tlabel):
    # Determine if canvas or custom HTML
    canvas_charts = {1,2,3,4,5,6,7,9,10,11,12,13,14,15,19,20,21,22,24,25,26,27,28,29,30,31,44,45,46,47,49,55,56,57,68,69,71,74,75,76}
    full_width_charts = {60,61,65,67,72,73,77}
    fw = ' full-width' if cid in full_width_charts else ''
    body_id = f'c{cid}' if cid in canvas_charts else f'div{cid}'
    if cid in canvas_charts:
        inner = f'<canvas id="{body_id}"></canvas>'
    else:
        inner = f'<div id="{body_id}"></div>'
    return f'''
    <div class="chart-card{fw}" id="chart-{cid}">
      <div class="chart-head">
        <div class="chart-title"><span class="chart-num">#{cid}</span>{cname}</div>
        <span class="chart-type-badge {badge}">{tlabel}</span>
      </div>
      <div class="chart-body">{inner}</div>
    </div>'''


# ===================== HTML HEAD =====================
HEAD = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>経済指標チャートサンプル集 — 市場調査ダッシュボード v3.0</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#FAFBFD;--surface:#FFF;--border:#E5E9F0;--border-light:#F1F5F9;--text:#1A2332;--text-secondary:#5A6B82;--text-muted:#8C99AB;--primary:#2563EB;--primary-bg:#EFF6FF;--green:#059669;--green-bg:#ECFDF5;--orange:#D97706;--orange-bg:#FEF3C7;--red:#DC2626;--red-bg:#FEE2E2;--purple:#7C3AED;--purple-bg:#EDE9FE;--cyan:#0891B2;--cyan-bg:#ECFEFF;--font:'Inter',-apple-system,BlinkMacSystemFont,'Hiragino Sans','Noto Sans JP',sans-serif;--mono:'SF Mono','Fira Code',Consolas,monospace}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.6}
.container{max-width:1280px;margin:0 auto;padding:40px 32px 80px}
.hero{text-align:center;padding:48px 24px;background:linear-gradient(135deg,#0F172A,#1E3A5F);border-radius:16px;color:#fff;margin-bottom:40px;position:relative;overflow:hidden}
.hero h1{font-size:28px;font-weight:800;letter-spacing:-.5px;position:relative}
.hero p{font-size:13px;opacity:.7;margin-top:6px;position:relative}
.hero .badges{display:flex;justify-content:center;gap:8px;margin-top:16px;position:relative;flex-wrap:wrap}
.hero .badge{padding:3px 12px;border-radius:16px;font-size:11px;font-weight:600;background:rgba(255,255,255,.12)}
.toc{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:20px 24px;margin-bottom:32px}
.toc h2{font-size:13px;font-weight:800;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:12px}
.toc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:4px}
.toc-item{display:flex;align-items:center;gap:5px;padding:4px 8px;border-radius:5px;font-size:10.5px;font-weight:600;color:var(--text-secondary);text-decoration:none;transition:.15s;border:1px solid transparent}
.toc-item:hover{background:var(--primary-bg);color:var(--primary);border-color:#BFDBFE}
.toc-num{font-family:var(--mono);font-size:9px;color:var(--text-muted);min-width:22px}
.cat-header{display:flex;align-items:center;gap:12px;margin:36px 0 16px;padding-bottom:10px;border-bottom:2px solid var(--border)}
.cat-icon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:13px;color:#fff;font-weight:800;flex-shrink:0}
.cat-header h2{font-size:17px;font-weight:800}
.cat-count{font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;background:var(--border-light);color:var(--text-muted)}
.chart-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.chart-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;overflow:hidden;transition:box-shadow .2s}
.chart-card:hover{box-shadow:0 4px 16px rgba(0,0,0,.06)}
.chart-card.full-width{grid-column:1/-1}
.chart-head{padding:12px 16px 8px;border-bottom:1px solid var(--border-light);display:flex;align-items:center;justify-content:space-between}
.chart-title{font-size:12px;font-weight:700;display:flex;align-items:center;gap:6px}
.chart-num{font-family:var(--mono);font-size:10px;padding:2px 5px;border-radius:4px;background:var(--primary-bg);color:var(--primary);font-weight:700}
.chart-type-badge{font-size:9px;font-weight:700;padding:2px 6px;border-radius:4px}
.cb-bar{background:#EFF6FF;color:#2563EB}
.cb-line{background:#ECFDF5;color:#059669}
.cb-pie{background:#EDE9FE;color:#7C3AED}
.cb-scatter{background:#FEF3C7;color:#D97706}
.cb-map{background:#ECFEFF;color:#0891B2}
.cb-special{background:#FFF1F2;color:#E11D48}
.cb-other{background:#F8FAFC;color:#475569}
.chart-body{padding:14px;position:relative;min-height:240px}
.chart-body canvas{max-height:260px}
.footer{text-align:center;margin-top:48px;padding-top:20px;border-top:1px solid var(--border);font-size:11px;color:var(--text-muted)}
@media(max-width:900px){.chart-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="container">'''

# ===================== FOOTER =====================
FOOTER = '''
  <div class="footer">
    経済指標チャートサンプル集 — 市場調査ダッシュボード v3.0<br>
    77 チャート | 17 カテゴリ | Generated: 2026-03-10
  </div>'''

# ===================== SCRIPT (All chart logic) =====================
SCRIPT = r'''
<script>
// Shared
const MC=['#2563EB','#059669','#D97706','#7C3AED','#E11D48','#0891B2','#475569','#DC2626','#10B981','#F59E0B'];
const Q=['Q1 24','Q2 24','Q3 24','Q4 24','Q1 25','Q2 25','Q3 25','Q4 25'];
const M=['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'];
const S=['食品','家電','衣料','日用品','飲料','文具','家具','スポーツ'];
Chart.defaults.font.family="'Inter',-apple-system,'Hiragino Sans','Noto Sans JP',sans-serif";
Chart.defaults.font.size=11;Chart.defaults.color='#5A6B82';
Chart.defaults.plugins.legend.labels.usePointStyle=true;
Chart.defaults.plugins.legend.labels.pointStyleWidth=8;
const gO={responsive:true,maintainAspectRatio:false};
const gS={x:{grid:{display:false}},y:{beginAtZero:true,grid:{color:'#F1F5F9'}}};
const noL={plugins:{legend:{display:false}}};
function cc(id,type,data,opt){const el=document.getElementById(id);if(!el)return;new Chart(el,{type,data,options:Object.assign({},gO,opt)});}

// #1 棒グラフ
cc('c1','bar',{labels:S,datasets:[{data:[342,289,215,178,134,112,98,87],backgroundColor:MC,borderRadius:5,barPercentage:.7}]},{...noL,scales:gS});

// #2 横棒
cc('c2','bar',{labels:['Tech Capital','Accel VC','GS Growth','SoftBank','JAFCO','SBI','DNX','Coral','Angel Br','Globis'],datasets:[{data:[4200,3800,3200,2900,2400,2100,1800,1500,1200,980],backgroundColor:'#2563EB',borderRadius:4,barPercentage:.65}]},{indexAxis:'y',...noL,scales:{x:{beginAtZero:true,grid:{color:'#F1F5F9'}},y:{grid:{display:false}}}});

// #3 積み上げ棒
cc('c3','bar',{labels:Q,datasets:[{label:'VC',data:[45,52,48,61,55,63,58,72],backgroundColor:'#2563EB'},{label:'CVC',data:[22,28,25,30,35,32,38,41],backgroundColor:'#059669'},{label:'PE',data:[8,10,12,9,14,11,15,13],backgroundColor:'#D97706'}]},{scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,beginAtZero:true,grid:{color:'#F1F5F9'}}}});

// #4 100%積み上げ棒
cc('c4','bar',{labels:['2021','2022','2023','2024','2025'],datasets:[{label:'小売',data:[30,28,25,22,20],backgroundColor:'#93C5FD'},{label:'A',data:[25,27,28,30,32],backgroundColor:'#2563EB'},{label:'B',data:[20,22,25,27,28],backgroundColor:'#059669'},{label:'卸売',data:[25,23,22,21,20],backgroundColor:'#D97706'}]},{scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,max:100,grid:{color:'#F1F5F9'},ticks:{callback:v=>v+'%'}}}});

// #5 グループ棒
cc('c5','bar',{labels:['食品','家電','衣料','日用品','飲料'],datasets:[{label:'国内',data:[180,160,120,95,70],backgroundColor:'#2563EB',borderRadius:4},{label:'海外',data:[162,129,95,83,64],backgroundColor:'#059669',borderRadius:4}]},{scales:gS});

// #6 発散棒
cc('c6','bar',{labels:S.slice(0,6),datasets:[{label:'前年比(%)',data:[18,-5,12,-8,25,3],backgroundColor:ctx=>[18,-5,12,-8,25,3].map(v=>v>=0?'#059669':'#DC2626'),borderRadius:4}]},{indexAxis:'y',...noL,scales:{x:{grid:{color:'#F1F5F9'}},y:{grid:{display:false}}}});

// #7 スロープ
cc('c7','line',{labels:['2024','2025'],datasets:S.slice(0,5).map((s,i)=>({label:s,data:[[342,289,215,178,134][i],[420,310,198,225,168][i]],borderColor:MC[i],pointRadius:5,borderWidth:2.5,tension:0}))},{scales:{y:{grid:{color:'#F1F5F9'}},x:{grid:{display:false}}}});

// #8 スパークライン (mini line charts in HTML)
(function(){
  const el=document.getElementById('div8');if(!el)return;
  const series=[{name:'売上高',data:[12,15,13,18,22,20,25,28],color:'#2563EB'},{name:'顧客数',data:[30,28,35,32,38,42,40,45],color:'#059669'},{name:'成約',data:[3,5,4,6,8,7,9,12],color:'#D97706'}];
  let h='<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">';
  series.forEach(s=>{
    const max=Math.max(...s.data),min=Math.min(...s.data);
    const pts=s.data.map((v,i)=>`${i/(s.data.length-1)*120},${40-(v-min)/(max-min)*35}`).join(' ');
    h+=`<div style="text-align:center"><div style="font-size:10px;font-weight:700;color:var(--text-muted);margin-bottom:4px">${s.name}</div><svg viewBox="-2 0 124 45" width="120" height="45"><polyline points="${pts}" fill="none" stroke="${s.color}" stroke-width="2"/></svg><div style="font-size:16px;font-weight:800;color:${s.color}">${s.data[s.data.length-1]}</div></div>`;
  });
  h+='</div>';el.innerHTML=h;
})();

// #9 レーダー
cc('c9','radar',{labels:['成長性','収益性','技術力','市場規模','チーム力','資金力'],datasets:[{label:'商品A',data:[92,68,95,85,78,88],borderColor:'#2563EB',backgroundColor:'rgba(37,99,235,.12)',pointBackgroundColor:'#2563EB'},{label:'商品B',data:[75,85,72,90,82,70],borderColor:'#059669',backgroundColor:'rgba(5,150,105,.12)',pointBackgroundColor:'#059669'}]},{scales:{r:{beginAtZero:true,max:100,grid:{color:'#E5E9F0'},pointLabels:{font:{size:10,weight:'600'}}}}});

// #10 折れ線
cc('c10','line',{labels:M,datasets:[{label:'2024',data:[32,28,45,38,42,55,48,52,61,58,63,72],borderColor:'#2563EB',backgroundColor:'rgba(37,99,235,.08)',fill:true,tension:.4,pointRadius:2},{label:'2025',data:[38,35,52,45,50,62,58,65,71,68,75,82],borderColor:'#059669',backgroundColor:'rgba(5,150,105,.08)',fill:true,tension:.4,pointRadius:2}]},{scales:gS});

// #11 多軸折れ線
cc('c11','line',{labels:Q,datasets:[{label:'売上高(億)',data:[120,150,180,210,240,270,300,350],borderColor:'#2563EB',yAxisID:'y',tension:.3,pointRadius:3},{label:'件数',data:[45,52,48,61,55,63,58,72],borderColor:'#D97706',yAxisID:'y1',tension:.3,pointRadius:3}]},{scales:{x:{grid:{display:false}},y:{beginAtZero:true,grid:{color:'#F1F5F9'},title:{display:true,text:'億円'}},y1:{position:'right',beginAtZero:true,grid:{display:false},title:{display:true,text:'件数'}}}});

// #12 ステップライン
cc('c12','line',{labels:M.slice(0,8),datasets:[{label:'累計成約',data:[2,2,5,5,5,8,8,12],borderColor:'#7C3AED',stepped:'before',pointRadius:3,fill:false}]},{...noL,scales:gS});

// #13 エリア
cc('c13','line',{labels:Q,datasets:[{label:'国内',data:[1200,1450,1680,1920,2150,2380,2610,2850],borderColor:'#2563EB',backgroundColor:'rgba(37,99,235,.15)',fill:true,tension:.4},{label:'海外',data:[2800,3200,3650,4100,4500,4920,5350,5800],borderColor:'#059669',backgroundColor:'rgba(5,150,105,.15)',fill:true,tension:.4}]},{scales:{...gS,y:{beginAtZero:true,grid:{color:'#F1F5F9'},ticks:{callback:v=>'¥'+v+'億'}}}});

// #14 積み上げエリア
cc('c14','line',{labels:Q,datasets:[{label:'食品',data:[320,380,420,490,540,610,680,750],borderColor:'#2563EB',backgroundColor:'rgba(37,99,235,.3)',fill:true,tension:.4},{label:'家電',data:[280,310,350,380,420,460,500,540],borderColor:'#059669',backgroundColor:'rgba(5,150,105,.3)',fill:true,tension:.4},{label:'衣料',data:[200,230,260,290,310,340,370,400],borderColor:'#D97706',backgroundColor:'rgba(217,119,6,.3)',fill:true,tension:.4}]},{scales:{y:{stacked:true,beginAtZero:true,grid:{color:'#F1F5F9'}},x:{grid:{display:false}}}});

// #15 100%積み上げエリア
(function(){
  const d=[[40,35,25],[38,37,25],[35,38,27],[33,39,28],[30,40,30],[28,42,30],[26,43,31],[25,44,31]];
  cc('c15','line',{labels:Q,datasets:[{label:'食品',data:d.map(r=>r[0]),borderColor:'#2563EB',backgroundColor:'rgba(37,99,235,.4)',fill:true,tension:.4},{label:'家電',data:d.map(r=>r[1]),borderColor:'#059669',backgroundColor:'rgba(5,150,105,.4)',fill:true,tension:.4},{label:'その他',data:d.map(r=>r[2]),borderColor:'#D97706',backgroundColor:'rgba(217,119,6,.4)',fill:true,tension:.4}]},{scales:{y:{stacked:true,max:100,grid:{color:'#F1F5F9'},ticks:{callback:v=>v+'%'}},x:{grid:{display:false}}}});
})();

// #16 カレンダーHM (HTML)
(function(){
  const el=document.getElementById('div16');if(!el)return;
  const days=['月','火','水','木','金'];const weeks=['W1','W2','W3','W4','W5'];
  let h='<div style="display:grid;grid-template-columns:30px repeat(5,1fr);gap:2px"><div></div>';
  days.forEach(d=>{h+=`<div style="font-size:9px;font-weight:600;color:var(--text-muted);text-align:center">${d}</div>`;});
  weeks.forEach(w=>{
    h+=`<div style="font-size:9px;font-weight:600;color:var(--text-muted);text-align:right;padding-right:4px;line-height:28px">${w}</div>`;
    for(let i=0;i<5;i++){const v=Math.floor(Math.random()*10);const a=(v/10*.8+.1).toFixed(2);
      h+=`<div style="background:rgba(5,150,105,${a});border-radius:3px;min-height:28px;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:600;color:#fff">${v}</div>`;}
  });
  h+='</div>';el.innerHTML=h;
})();

// #17 ガント (HTML)
(function(){
  const el=document.getElementById('div17');if(!el)return;
  const funds=[{n:'プロジェクトA',s:10,e:80,c:'#2563EB'},{n:'プロジェクトB',s:20,e:90,c:'#059669'},{n:'プロジェクトC',s:35,e:95,c:'#D97706'},{n:'プロジェクトD',s:45,e:85,c:'#7C3AED'},{n:'プロジェクトE',s:55,e:100,c:'#0891B2'}];
  let h='';funds.forEach(f=>{h+=`<div style="display:flex;align-items:center;gap:10px;padding:5px 0"><span style="font-size:11px;font-weight:600;min-width:100px">${f.n}</span><div style="flex:1;height:20px;background:var(--border-light);border-radius:4px;position:relative"><div style="position:absolute;height:100%;left:${f.s}%;width:${f.e-f.s}%;background:${f.c};border-radius:4px"></div></div></div>`;});
  h+=`<div style="display:flex;justify-content:space-between;margin-left:110px;font-size:9px;color:var(--text-muted)"><span>2018</span><span>2020</span><span>2022</span><span>2024</span><span>2026</span><span>2028</span></div>`;
  el.innerHTML=h;
})();

// #18 タイムライン (HTML)
(function(){
  const el=document.getElementById('div18');if(!el)return;
  const ev=[{d:'2024/01',t:'新製品Aリリース',c:'#2563EB'},{d:'2024/04',t:'全国展開開始',c:'#059669'},{d:'2024/07',t:'海外進出（アジア）',c:'#D97706'},{d:'2024/10',t:'新サービスBリリース',c:'#7C3AED'},{d:'2025/01',t:'パートナーシップ締結',c:'#E11D48'},{d:'2025/03',t:'年間売上目標達成',c:'#2563EB'}];
  let h='';ev.forEach((e,i)=>{h+=`<div style="display:flex;gap:12px;padding:8px 0;position:relative"><div style="width:10px;height:10px;border-radius:50%;background:${e.c};flex-shrink:0;margin-top:4px"></div>${i<ev.length-1?'<div style="position:absolute;left:4px;top:20px;bottom:-8px;width:2px;background:var(--border)"></div>':''}<div><div style="font-size:10px;font-weight:700;color:var(--text-muted);font-family:var(--mono)">${e.d}</div><div style="font-size:12px;font-weight:600;margin-top:1px">${e.t}</div></div></div>`;});
  el.innerHTML=h;
})();

// #19 期間比較
cc('c19','line',{labels:M.slice(0,6),datasets:[{label:'今期',data:[55,62,58,72,68,78],borderColor:'#2563EB',borderWidth:2.5,tension:.3,pointRadius:3},{label:'前期',data:[42,48,45,55,52,60],borderColor:'#94A3B8',borderDash:[5,5],borderWidth:1.5,tension:.3,pointRadius:2}]},{scales:gS});

// #20 ローソク足 (bar chart simulation)
(function(){
  const el=document.getElementById('c20');if(!el)return;
  const labels=['1月','2月','3月','4月','5月','6月'];
  const open=[100,110,105,120,115,125];
  const close=[110,105,120,115,125,130];
  const colors=open.map((o,i)=>close[i]>=o?'#059669':'#DC2626');
  const base=open.map((o,i)=>Math.min(o,close[i]));
  const body=open.map((o,i)=>Math.abs(close[i]-o));
  new Chart(el,{type:'bar',data:{labels,datasets:[{label:'ベース',data:base,backgroundColor:'transparent',borderSkipped:false},{label:'実体',data:body,backgroundColor:colors,borderRadius:2}]},options:{...gO,...noL,scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{color:'#F1F5F9'},title:{display:true,text:'価格指数'}}}}});
})();

// #21 ヒストグラム
cc('c21','bar',{labels:['0-10','10-30','30-50','50-100','100-200','200-500','500+'],datasets:[{data:[45,120,180,150,90,42,15],backgroundColor:'rgba(37,99,235,.7)',borderColor:'#2563EB',borderWidth:1,borderRadius:2,barPercentage:1,categoryPercentage:.95}]},{...noL,scales:{...gS,x:{grid:{display:false},title:{display:true,text:'単価(万円)'}},y:{beginAtZero:true,grid:{color:'#F1F5F9'},title:{display:true,text:'顧客数'}}}});

// #22 度数ポリゴン
cc('c22','line',{labels:['0-10','10-30','30-50','50-100','100-200','200-500','500+'],datasets:[{label:'国内',data:[45,120,180,150,90,42,15],borderColor:'#2563EB',tension:.3,pointRadius:4,fill:false},{label:'海外',data:[30,80,140,200,120,65,25],borderColor:'#059669',tension:.3,pointRadius:4,fill:false}]},{scales:{...gS,x:{title:{display:true,text:'価格レンジ'}}}});

// #23 箱ひげ図 (simulated)
(function(){
  const el=document.getElementById('div23');if(!el)return;
  const data=[{n:'食品',q1:45,med:85,q3:150,min:10,max:250,c:'#2563EB'},{n:'家電',q1:30,med:62,q3:110,min:5,max:200,c:'#059669'},{n:'衣料',q1:22,med:48,q3:85,min:8,max:160,c:'#D97706'},{n:'日用品',q1:28,med:55,q3:95,min:12,max:180,c:'#7C3AED'},{n:'飲料',q1:18,med:38,q3:72,min:5,max:130,c:'#0891B2'}];
  const maxV=260;
  let h='<svg viewBox="0 0 400 200" style="width:100%;height:200px">';
  data.forEach((d,i)=>{
    const y=20+i*36;const scale=v=>v/maxV*350+30;
    h+=`<line x1="${scale(d.min)}" y1="${y+8}" x2="${scale(d.max)}" y2="${y+8}" stroke="${d.c}" stroke-width="1" opacity=".5"/>`;
    h+=`<rect x="${scale(d.q1)}" y="${y}" width="${scale(d.q3)-scale(d.q1)}" height="16" rx="3" fill="${d.c}" opacity=".3" stroke="${d.c}" stroke-width="1"/>`;
    h+=`<line x1="${scale(d.med)}" y1="${y}" x2="${scale(d.med)}" y2="${y+16}" stroke="${d.c}" stroke-width="2.5"/>`;
    h+=`<text x="5" y="${y+12}" font-size="10" font-weight="600" fill="var(--text-secondary)">${d.n}</text>`;
  });
  h+='</svg>';el.innerHTML=h;
})();

// #24 バイオリン (area approx)
cc('c24','line',{labels:['0','20','40','60','80','100','120','140','160','180','200'],datasets:[{label:'食品',data:[2,8,18,32,45,38,28,15,8,4,1],borderColor:'#2563EB',backgroundColor:'rgba(37,99,235,.2)',fill:true,tension:.4,pointRadius:0},{label:'家電',data:[5,15,28,35,30,22,14,8,3,1,0],borderColor:'#059669',backgroundColor:'rgba(5,150,105,.2)',fill:true,tension:.4,pointRadius:0}]},{scales:{y:{title:{display:true,text:'密度'},grid:{color:'#F1F5F9'}},x:{title:{display:true,text:'単価(万)'},grid:{display:false}}}});

// #25 ストリップ
(function(){
  const data=[];for(let i=0;i<60;i++){data.push({x:Math.floor(Math.random()*5),y:Math.random()*200+10});}
  cc('c25','scatter',{datasets:[{data:data.map(d=>({x:d.x+Math.random()*.3-.15,y:d.y})),backgroundColor:'rgba(37,99,235,.4)',pointRadius:4}]},{...noL,scales:{x:{title:{display:true,text:'カテゴリ'},ticks:{callback:v=>['食品','家電','衣料','日用品','飲料'][v]||''},grid:{display:false}},y:{title:{display:true,text:'単価'},grid:{color:'#F1F5F9'}}}});
})();

// #26 QQプロット
(function(){
  const n=30;const data=[];for(let i=0;i<n;i++){const t=(i+.5)/n;const q=Math.sqrt(2)*erfinv(2*t-1);data.push({x:q,y:q+(.5-Math.random())*.8});}
  function erfinv(x){let a=.147;let ln=Math.log(1-x*x);let s=Math.sign(x);let t1=2/(Math.PI*a)+ln/2;return s*Math.sqrt(Math.sqrt(t1*t1-ln/a)-t1);}
  cc('c26','scatter',{datasets:[{label:'データ',data,backgroundColor:'rgba(37,99,235,.5)',pointRadius:4},{label:'理論線',data:[{x:-2.5,y:-2.5},{x:2.5,y:2.5}],type:'line',borderColor:'#DC2626',borderDash:[5,5],pointRadius:0,borderWidth:1.5}]},{scales:{x:{title:{display:true,text:'理論分位点'},grid:{color:'#F1F5F9'}},y:{title:{display:true,text:'サンプル分位点'},grid:{color:'#F1F5F9'}}}});
})();

// #27 累積分布
cc('c27','line',{labels:['0','20','40','60','80','100','150','200','300','500'],datasets:[{label:'CDF',data:[0,.05,.15,.35,.55,.72,.85,.92,.97,1],borderColor:'#2563EB',backgroundColor:'rgba(37,99,235,.1)',fill:true,tension:.4,pointRadius:2,stepped:false}]},{...noL,scales:{x:{title:{display:true,text:'単価(万)'},grid:{display:false}},y:{title:{display:true,text:'累積確率'},max:1,grid:{color:'#F1F5F9'},ticks:{callback:v=>(v*100)+'%'}}}});

// #28 リッジライン
cc('c28','line',{labels:['0','20','40','60','80','100','120','140','160'],datasets:[{label:'2023',data:[2,8,20,35,28,15,8,3,1].map(v=>v+30),borderColor:'#93C5FD',backgroundColor:'rgba(147,197,253,.3)',fill:true,tension:.4,pointRadius:0},{label:'2024',data:[3,10,25,40,32,18,10,4,1].map(v=>v+15),borderColor:'#2563EB',backgroundColor:'rgba(37,99,235,.3)',fill:true,tension:.4,pointRadius:0},{label:'2025',data:[5,15,30,42,35,22,12,5,2],borderColor:'#1E40AF',backgroundColor:'rgba(30,64,175,.3)',fill:true,tension:.4,pointRadius:0}]},{scales:{y:{grid:{color:'#F1F5F9'}},x:{grid:{display:false}}}});

// #29 散布図
(function(){
  const data=[];for(let i=0;i<40;i++){data.push({x:Math.random()*200,y:Math.random()*500+10});}
  cc('c29','scatter',{datasets:[{data,backgroundColor:'rgba(37,99,235,.5)',borderColor:'#2563EB',pointRadius:5}]},{...noL,scales:{x:{title:{display:true,text:'広告費'},grid:{color:'#F1F5F9'}},y:{title:{display:true,text:'単価(万)'},grid:{color:'#F1F5F9'}}}});
})();

// #30 回帰直線付き
(function(){
  const data=[];for(let i=0;i<35;i++){const x=Math.random()*200;data.push({x,y:x*2+Math.random()*100-50+20});}
  cc('c30','scatter',{datasets:[{label:'データ',data,backgroundColor:'rgba(37,99,235,.5)',pointRadius:4},{label:'回帰線',data:[{x:0,y:20},{x:200,y:420}],type:'line',borderColor:'#DC2626',borderWidth:2,pointRadius:0,borderDash:[6,3]}]},{scales:{x:{title:{display:true,text:'広告費'},grid:{color:'#F1F5F9'}},y:{title:{display:true,text:'単価(万)'},grid:{color:'#F1F5F9'}}}});
})();

// #31 バブル
cc('c31','bubble',{datasets:[{label:'SU',data:[{x:50,y:120,r:18},{x:120,y:80,r:14},{x:80,y:200,r:22},{x:180,y:60,r:10},{x:30,y:280,r:25},{x:150,y:150,r:16},{x:200,y:220,r:12}],backgroundColor:MC.slice(0,7).map(c=>c+'88'),borderColor:MC.slice(0,7)}]},{...noL,scales:{x:{title:{display:true,text:'単価(万)'},grid:{color:'#F1F5F9'}},y:{title:{display:true,text:'成長率(%)'},grid:{color:'#F1F5F9'}}}});

// #32 相関マトリックス (HTML)
(function(){
  const el=document.getElementById('div32');if(!el)return;
  const vars=['単価','広告費','売上高','成長率','特許数'];
  const corr=[[1,.72,.85,.45,.38],[.72,1,.68,.52,.25],[.85,.68,1,.55,.42],[.45,.52,.55,1,.18],[.38,.25,.42,.18,1]];
  let h='<div style="display:grid;grid-template-columns:60px repeat(5,1fr);gap:2px">';
  h+='<div></div>';vars.forEach(v=>{h+=`<div style="font-size:9px;font-weight:600;color:var(--text-muted);text-align:center;padding:2px">${v}</div>`;});
  vars.forEach((v,i)=>{
    h+=`<div style="font-size:9px;font-weight:600;color:var(--text-muted);text-align:right;padding:2px 4px;line-height:28px">${v}</div>`;
    corr[i].forEach(c=>{
      const r=Math.round(c*255),b=Math.round((1-c)*255);
      h+=`<div style="background:rgba(37,99,235,${(c*.8+.1).toFixed(2)});border-radius:3px;min-height:28px;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;color:#fff">${c.toFixed(2)}</div>`;
    });
  });
  h+='</div>';el.innerHTML=h;
})();

// #33 ヒートマップ (HTML)
(function(){
  const el=document.getElementById('div33');if(!el)return;
  const rows=['食品','家電','衣料','日用品','飲料'];
  const cols=['Q1','Q2','Q3','Q4','通期'];
  const data=[[42,35,28,18,8],[28,32,25,15,5],[18,22,20,12,3],[15,18,15,10,5],[10,12,8,5,2]];
  let h='<div style="display:grid;grid-template-columns:60px repeat(5,1fr);gap:2px"><div></div>';
  cols.forEach(c=>{h+=`<div style="font-size:9px;font-weight:600;color:var(--text-muted);text-align:center">${c}</div>`;});
  rows.forEach((r,ri)=>{
    h+=`<div style="font-size:9px;font-weight:600;color:var(--text-muted);text-align:right;padding-right:6px;line-height:28px">${r}</div>`;
    data[ri].forEach(v=>{h+=`<div style="background:rgba(37,99,235,${(v/42*.8+.15).toFixed(2)});border-radius:3px;min-height:28px;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:600;color:#fff">${v}</div>`;});
  });
  h+='</div>';el.innerHTML=h;
})();

// #34 ネットワーク (SVG)
(function(){
  const el=document.getElementById('div34');if(!el)return;
  const nodes=[{x:160,y:50,r:18,c:'#2563EB',l:'本社'},{x:60,y:120,r:14,c:'#2563EB',l:'営業'},{x:280,y:100,r:12,c:'#059669',l:'開発'},{x:120,y:170,r:10,c:'#D97706',l:'食品'},{x:220,y:190,r:10,c:'#D97706',l:'家電'},{x:200,y:130,r:9,c:'#D97706',l:'衣料'},{x:80,y:210,r:8,c:'#7C3AED',l:'日用品'},{x:300,y:190,r:8,c:'#7C3AED',l:'飲料'}];
  const edges=[[0,3],[0,4],[0,5],[1,3],[1,6],[2,4],[2,5],[2,7],[1,5]];
  let s='<svg viewBox="0 0 360 240" style="width:100%;height:240px">';
  edges.forEach(([a,b])=>{s+=`<line x1="${nodes[a].x}" y1="${nodes[a].y}" x2="${nodes[b].x}" y2="${nodes[b].y}" stroke="#CBD5E1" stroke-width="1.5" opacity=".5"/>`;});
  nodes.forEach(n=>{s+=`<circle cx="${n.x}" cy="${n.y}" r="${n.r}" fill="${n.c}" opacity=".85"/><text x="${n.x}" y="${n.y+n.r+11}" text-anchor="middle" font-size="8" font-weight="600" fill="var(--text-secondary)">${n.l}</text>`;});
  s+='</svg>';el.innerHTML=s;
})();

// #35 サンキー (SVG)
(function(){
  const el=document.getElementById('div35');if(!el)return;
  let s='<svg viewBox="0 0 350 200" style="width:100%;height:220px">';
  // Left
  s+=`<rect x="10" y="15" width="55" height="55" rx="4" fill="#2563EB" opacity=".8"/><text x="37" y="46" text-anchor="middle" font-size="9" fill="#fff" font-weight="700">VC</text>`;
  s+=`<rect x="10" y="75" width="55" height="40" rx="4" fill="#059669" opacity=".8"/><text x="37" y="99" text-anchor="middle" font-size="9" fill="#fff" font-weight="700">CVC</text>`;
  s+=`<rect x="10" y="120" width="55" height="28" rx="4" fill="#D97706" opacity=".8"/><text x="37" y="138" text-anchor="middle" font-size="9" fill="#fff" font-weight="700">PE</text>`;
  // Right
  const right=[{y:15,h:35,c:'#2563EB',l:'Series A'},{y:55,h:25,c:'#3B82F6',l:'Series B'},{y:85,h:22,c:'#059669',l:'Seed'},{y:112,h:18,c:'#10B981',l:'Series A'},{y:135,h:15,c:'#D97706',l:'Later'},{y:155,h:13,c:'#F59E0B',l:'Series C'}];
  right.forEach(r=>{s+=`<rect x="280" y="${r.y}" width="55" height="${r.h}" rx="4" fill="${r.c}" opacity=".8"/><text x="307" y="${r.y+r.h/2+3}" text-anchor="middle" font-size="8" fill="#fff" font-weight="600">${r.l}</text>`;});
  // Flows
  [[42,32,.2,'#2563EB'],[42,67,.15,'#3B82F6'],[95,96,.12,'#059669'],[95,121,.1,'#10B981'],[134,142,.08,'#D97706'],[134,161,.06,'#F59E0B']].forEach(([fy,ty,op,c])=>{
    s+=`<path d="M65,${fy} C172,${fy} 172,${ty} 280,${ty}" fill="none" stroke="${c}" stroke-width="18" opacity="${op}"/>`;});
  s+='</svg>';el.innerHTML=s;
})();

// #36 コード (SVG)
(function(){
  const el=document.getElementById('div36');if(!el)return;
  const cx=170,cy=130,r=95;const sects=['食品','家電','衣料','日用品','飲料'];
  let s='<svg viewBox="0 0 340 260" style="width:100%;height:240px">';
  sects.forEach((sec,i)=>{
    const a=(i/5)*Math.PI*2-Math.PI/2;
    const x1=cx+r*Math.cos(a-.25),y1=cy+r*Math.sin(a-.25);
    const x2=cx+r*Math.cos(a+.25),y2=cy+r*Math.sin(a+.25);
    s+=`<path d="M${x1},${y1} A${r},${r} 0 0,1 ${x2},${y2}" fill="none" stroke="${MC[i]}" stroke-width="12" opacity=".7"/>`;
    const lx=cx+(r+18)*Math.cos(a),ly=cy+(r+18)*Math.sin(a);
    s+=`<text x="${lx}" y="${ly}" text-anchor="middle" font-size="9" font-weight="700" fill="${MC[i]}">${sec}</text>`;
  });
  [[0,1],[0,2],[1,3],[2,4],[0,3],[1,4]].forEach(([a,b])=>{
    const aa=(a/5)*Math.PI*2-Math.PI/2,ab=(b/5)*Math.PI*2-Math.PI/2;
    s+=`<path d="M${cx+r*.93*Math.cos(aa)},${cy+r*.93*Math.sin(aa)} Q${cx},${cy} ${cx+r*.93*Math.cos(ab)},${cy+r*.93*Math.sin(ab)}" fill="${MC[a]}" opacity=".1" stroke="${MC[a]}" stroke-width=".5"/>`;
  });
  s+='</svg>';el.innerHTML=s;
})();

// #37 フローチャート (SVG)
(function(){
  const el=document.getElementById('div37');if(!el)return;
  const boxes=[{x:130,y:10,w:80,h:30,t:'データ収集',c:'#2563EB'},{x:130,y:60,w:80,h:30,t:'正規化',c:'#059669'},{x:50,y:120,w:70,h:30,t:'mart加工',c:'#D97706'},{x:220,y:120,w:70,h:30,t:'QA検証',c:'#7C3AED'},{x:130,y:180,w:80,h:30,t:'チャート生成',c:'#E11D48'}];
  let s='<svg viewBox="0 0 340 220" style="width:100%;height:220px">';
  [[170,40,170,60],[170,90,85,120],[170,90,255,120],[85,150,170,180],[255,150,170,180]].forEach(([x1,y1,x2,y2])=>{
    s+=`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ah)"/>`;});
  s+=`<defs><marker id="ah" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#94A3B8"/></marker></defs>`;
  boxes.forEach(b=>{
    s+=`<rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" rx="6" fill="${b.c}" opacity=".85"/>`;
    s+=`<text x="${b.x+b.w/2}" y="${b.y+b.h/2+4}" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">${b.t}</text>`;
  });
  s+='</svg>';el.innerHTML=s;
})();

// #38 ツリーマップ (HTML)
(function(){
  const el=document.getElementById('div38');if(!el)return;
  const items=[{n:'プロジェクトA',v:'¥320億',c:'#2563EB',s:2},{n:'プロジェクトB',v:'¥280億',c:'#3B82F6',s:2},{n:'プロジェクトC',v:'¥220億',c:'#059669',s:1},{n:'プロジェクトD',v:'¥180億',c:'#10B981',s:1},{n:'プロジェクトE',v:'¥150億',c:'#D97706',s:1},{n:'施策F',v:'¥120億',c:'#7C3AED',s:1},{n:'施策G',v:'¥100億',c:'#0891B2',s:1},{n:'施策H',v:'¥80億',c:'#E11D48',s:1}];
  let h='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3px;grid-auto-rows:75px">';
  items.forEach(it=>{h+=`<div style="background:${it.c};border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;${it.s>1?'grid-column:span 2':''}"><span style="font-size:11px;font-weight:700">${it.n}</span><span style="font-size:9px;opacity:.85;font-family:var(--mono)">${it.v}</span></div>`;});
  h+='</div>';el.innerHTML=h;
})();

// #39 サンバースト (2-ring doughnut)
cc('c39','doughnut',{labels:['食品','家電','衣料','日用品','菓子','飲料','調味料','冷凍','日配','惣菜'],datasets:[{data:[35,28,22,15,0,0,0,0,0,0],backgroundColor:['#2563EB','#059669','#D97706','#7C3AED','transparent','transparent','transparent','transparent','transparent','transparent'],borderWidth:2,borderColor:'#FFF',weight:1},{data:[0,0,0,0,18,17,16,12,12,10],backgroundColor:['transparent','transparent','transparent','transparent','#60A5FA','#93C5FD','#34D399','#6EE7B7','#FBBF24','#A78BFA'],borderWidth:1,borderColor:'#FFF',weight:1.5}]},{cutout:'30%',plugins:{legend:{display:false},tooltip:{filter:i=>i.raw>0}}});

// #40 デンドログラム (SVG)
(function(){
  const el=document.getElementById('div40');if(!el)return;
  let s='<svg viewBox="0 0 340 220" style="width:100%;height:220px">';
  const leaves=[{x:30,l:'食品'},{x:80,l:'飲料'},{x:130,l:'家電'},{x:180,l:'衣料'},{x:230,l:'日用品'},{x:280,l:'文具'}];
  leaves.forEach(lf=>{s+=`<text x="${lf.x}" y="210" text-anchor="middle" font-size="9" font-weight="600" fill="var(--text-secondary)">${lf.l}</text><line x1="${lf.x}" y1="195" x2="${lf.x}" y2="180" stroke="#94A3B8" stroke-width="1.5"/>`;});
  [[30,80,160],[130,180,120],[230,280,140]].forEach(([a,b,h])=>{
    s+=`<line x1="${a}" y1="180" x2="${a}" y2="${h}" stroke="#2563EB" stroke-width="1.5"/><line x1="${b}" y1="180" x2="${b}" y2="${h}" stroke="#2563EB" stroke-width="1.5"/><line x1="${a}" y1="${h}" x2="${b}" y2="${h}" stroke="#2563EB" stroke-width="1.5"/>`;});
  [[55,155,80],[155,255,50]].forEach(([a,b,h])=>{s+=`<line x1="${a}" y1="${a<100?160:120}" x2="${a}" y2="${h}" stroke="#059669" stroke-width="1.5"/><line x1="${b}" y1="${b>200?140:120}" x2="${b}" y2="${h}" stroke="#059669" stroke-width="1.5"/><line x1="${a}" y1="${h}" x2="${b}" y2="${h}" stroke="#059669" stroke-width="1.5"/>`;});
  s+=`<line x1="105" y1="80" x2="105" y2="25" stroke="#D97706" stroke-width="2"/><line x1="205" y1="50" x2="205" y2="25" stroke="#D97706" stroke-width="2"/><line x1="105" y1="25" x2="205" y2="25" stroke="#D97706" stroke-width="2"/>`;
  s+='</svg>';el.innerHTML=s;
})();

// #41 パックドバブル (SVG)
(function(){
  const el=document.getElementById('div41');if(!el)return;
  const bubbles=[{x:140,y:110,r:45,c:'#2563EB',l:'食品'},{x:240,y:90,r:35,c:'#059669',l:'家電'},{x:80,y:170,r:30,c:'#D97706',l:'衣料'},{x:200,y:180,r:25,c:'#7C3AED',l:'日用品'},{x:280,y:170,r:20,c:'#0891B2',l:'飲料'},{x:60,y:80,r:22,c:'#E11D48',l:'文具'},{x:310,y:110,r:18,c:'#475569',l:'家具'}];
  let s='<svg viewBox="0 0 360 230" style="width:100%;height:230px">';
  bubbles.forEach(b=>{
    s+=`<circle cx="${b.x}" cy="${b.y}" r="${b.r}" fill="${b.c}" opacity=".6" stroke="${b.c}" stroke-width="1.5"/>`;
    s+=`<text x="${b.x}" y="${b.y+4}" text-anchor="middle" font-size="${Math.max(8,b.r/4)}" font-weight="700" fill="#fff">${b.l}</text>`;
  });
  s+='</svg>';el.innerHTML=s;
})();

// #42 アイシクル (SVG)
(function(){
  const el=document.getElementById('div42');if(!el)return;
  let s='<svg viewBox="0 0 340 200" style="width:100%;height:200px">';
  s+=`<rect x="10" y="10" width="320" height="30" rx="4" fill="#2563EB" opacity=".85"/><text x="170" y="30" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">全カテゴリ</text>`;
  const l1=[{x:10,w:130,c:'#059669',l:'テクノロジー'},{x:145,w:100,c:'#D97706',l:'ファイナンス'},{x:250,w:80,c:'#7C3AED',l:'ヘルスケア'}];
  l1.forEach(b=>{s+=`<rect x="${b.x}" y="45" width="${b.w}" height="28" rx="4" fill="${b.c}" opacity=".85"/><text x="${b.x+b.w/2}" y="63" text-anchor="middle" font-size="9" font-weight="600" fill="#fff">${b.l}</text>`;});
  const l2=[{x:10,w:65,c:'#34D399',l:'菓子'},{x:78,w:62,c:'#6EE7B7',l:'飲料'},{x:145,w:50,c:'#FBBF24',l:'調味料'},{x:198,w:47,c:'#FDE68A',l:'冷凍'},{x:250,w:40,c:'#A78BFA',l:'日配'},{x:293,w:37,c:'#C4B5FD',l:'惣菜'}];
  l2.forEach(b=>{s+=`<rect x="${b.x}" y="78" width="${b.w}" height="25" rx="3" fill="${b.c}" opacity=".85"/><text x="${b.x+b.w/2}" y="94" text-anchor="middle" font-size="8" font-weight="600" fill="#fff">${b.l}</text>`;});
  s+='</svg>';el.innerHTML=s;
})();

// #43 ツリー図 (SVG)
(function(){
  const el=document.getElementById('div43');if(!el)return;
  let s='<svg viewBox="0 0 340 200" style="width:100%;height:200px">';
  s+=`<circle cx="170" cy="25" r="14" fill="#2563EB"/><text x="170" y="29" text-anchor="middle" font-size="8" font-weight="700" fill="#fff">Root</text>`;
  [[80,80,'#059669','Tech'],[170,80,'#D97706','Fin'],[260,80,'#7C3AED','HC']].forEach(([x,y,c,l])=>{
    s+=`<line x1="170" y1="39" x2="${x}" y2="${y-12}" stroke="#CBD5E1" stroke-width="1.5"/>`;
    s+=`<circle cx="${x}" cy="${y}" r="12" fill="${c}"/><text x="${x}" y="${y+4}" text-anchor="middle" font-size="7" font-weight="700" fill="#fff">${l}</text>`;
  });
  [[40,145,'#34D399','菓子'],[80,145,'#10B981','飲料'],[120,145,'#6EE7B7','調味料'],[145,145,'#FBBF24','冷凍'],[195,145,'#FDE68A','日配'],[235,145,'#A78BFA','惣菜'],[285,145,'#C4B5FD','乳製品']].forEach(([x,y,c,l],i)=>{
    const px=i<3?80:i<5?170:260;
    s+=`<line x1="${px}" y1="92" x2="${x}" y2="${y-10}" stroke="#CBD5E1" stroke-width="1"/>`;
    s+=`<circle cx="${x}" cy="${y}" r="10" fill="${c}"/><text x="${x}" y="${y+3}" text-anchor="middle" font-size="7" font-weight="600" fill="#fff">${l}</text>`;
  });
  s+='</svg>';el.innerHTML=s;
})();

// #44 ドーナツ
cc('c44','doughnut',{labels:['独立系VC','CVC','PE','エンジェル','政府系','その他'],datasets:[{data:[35,25,15,12,8,5],backgroundColor:MC.slice(0,6),borderWidth:2,borderColor:'#FFF',hoverOffset:8}]},{cutout:'60%'});

// #45 円グラフ
cc('c45','pie',{labels:['食品','家電','衣料','日用品','飲料','その他'],datasets:[{data:[28,22,18,15,10,7],backgroundColor:MC.slice(0,6),borderWidth:2,borderColor:'#FFF',hoverOffset:6}]},{});

// #46 パレート
(function(){
  const vals=[342,289,215,178,134,112,80];const total=vals.reduce((a,b)=>a+b,0);let cum=0;
  cc('c46','bar',{labels:S.slice(0,6).concat('他'),datasets:[{label:'件数',data:vals,backgroundColor:'#2563EB',borderRadius:4,order:2},{label:'累積%',data:vals.map(v=>{cum+=v;return Math.round(cum/total*100);}),type:'line',borderColor:'#E11D48',pointBackgroundColor:'#E11D48',pointRadius:3,tension:.3,yAxisID:'y1',order:1}]},{scales:{x:{grid:{display:false}},y:{beginAtZero:true,grid:{color:'#F1F5F9'}},y1:{position:'right',min:0,max:100,grid:{display:false},ticks:{callback:v=>v+'%'}}}});
})();

// #47 ウォーターフォール
cc('c47','bar',{labels:['Q1開始','Q1増','Q2増','Q2減','Q3増','Q3減','Q4増','累計'],datasets:[{label:'ベース',data:[0,0,120,0,280,0,400,0],backgroundColor:'transparent'},{label:'増',data:[0,120,180,0,150,0,200,650],backgroundColor:'#059669',borderRadius:4},{label:'減',data:[0,0,0,20,0,30,0,0],backgroundColor:'#DC2626',borderRadius:4}]},{scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{color:'#F1F5F9'}}}});

// #48 マリメッコ (HTML)
(function(){
  const el=document.getElementById('div48');if(!el)return;
  const segs=[{l:'食品',w:30,items:[{h:40,c:'#2563EB',t:'直販'},{h:35,c:'#3B82F6',t:'EC'},{h:25,c:'#93C5FD',t:'卸'}]},{l:'家電',w:25,items:[{h:30,c:'#059669',t:'直販'},{h:40,c:'#10B981',t:'EC'},{h:30,c:'#6EE7B7',t:'卸'}]},{l:'衣料',w:20,items:[{h:25,c:'#D97706',t:'直販'},{h:35,c:'#F59E0B',t:'EC'},{h:40,c:'#FBBF24',t:'卸'}]},{l:'その他',w:25,items:[{h:35,c:'#7C3AED',t:'直販'},{h:30,c:'#8B5CF6',t:'EC'},{h:35,c:'#A78BFA',t:'卸'}]}];
  let h='<div style="display:flex;height:200px;gap:2px">';
  segs.forEach(s=>{
    h+=`<div style="width:${s.w}%;display:flex;flex-direction:column;gap:1px">`;
    s.items.forEach(it=>{h+=`<div style="flex:${it.h};background:${it.c};border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:600;color:#fff">${it.t}</div>`;});
    h+=`<div style="text-align:center;font-size:9px;font-weight:600;color:var(--text-muted);padding-top:4px">${s.l}</div></div>`;
  });
  h+='</div>';el.innerHTML=h;
})();

// #49 ロリポップ
(function(){
  const labels=['食品','家電','衣料','日用品','飲料','文具'];
  const data=[342,289,215,178,134,112];
  cc('c49','bar',{labels,datasets:[{data,backgroundColor:'#2563EB',borderRadius:20,barPercentage:.15,borderSkipped:false}]},{indexAxis:'y',...noL,scales:{x:{beginAtZero:true,grid:{color:'#F1F5F9'}},y:{grid:{display:false}}}});
})();

// #50 ファネル (HTML)
(function(){
  const el=document.getElementById('div50');if(!el)return;
  const steps=[{l:'問い合わせ',v:1200,p:100,c:'#2563EB'},{l:'ヒアリング',v:480,p:40,c:'#3B82F6'},{l:'提案',v:120,p:10,c:'#059669'},{l:'受注',v:48,p:4,c:'#D97706'},{l:'成約',v:12,p:1,c:'#7C3AED'}];
  let h='';steps.forEach(s=>{h+=`<div style="display:flex;align-items:center;gap:10px;padding:5px 0"><span style="font-size:11px;font-weight:600;min-width:80px">${s.l}</span><div style="height:28px;width:${s.p}%;background:${s.c};border-radius:5px;display:flex;align-items:center;padding:0 10px;color:#fff;font-size:10px;font-weight:700;min-width:50px">${s.v}件</div><span style="font-size:10px;font-weight:700;font-family:var(--mono);color:var(--text-muted)">${s.p}%</span></div>`;});
  el.innerHTML=h;
})();

// #51 コロプレス (SVG)
(function(){
  const el=document.getElementById('div51');if(!el)return;
  const regions=[{n:'北海道',x:200,y:25,w:75,h:45,v:45},{n:'東北',x:210,y:75,w:55,h:35,v:32},{n:'関東',x:190,y:115,w:65,h:40,v:280},{n:'中部',x:140,y:115,w:48,h:35,v:85},{n:'近畿',x:120,y:138,w:50,h:32,v:120},{n:'中国',x:65,y:140,w:50,h:28,v:38},{n:'四国',x:90,y:170,w:42,h:22,v:22},{n:'九州',x:30,y:155,w:50,h:40,v:55}];
  let s='<svg viewBox="0 0 310 210" style="width:100%;height:210px">';
  regions.forEach(r=>{const a=(r.v/280*.8+.15).toFixed(2);
    s+=`<rect x="${r.x}" y="${r.y}" width="${r.w}" height="${r.h}" rx="5" fill="rgba(37,99,235,${a})" stroke="#fff" stroke-width="2"/><text x="${r.x+r.w/2}" y="${r.y+r.h/2-3}" text-anchor="middle" font-size="8" font-weight="700" fill="#1A2332">${r.n}</text><text x="${r.x+r.w/2}" y="${r.y+r.h/2+8}" text-anchor="middle" font-size="7" fill="#5A6B82" font-family="monospace">${r.v}社</text>`;});
  s+='</svg>';el.innerHTML=s;
})();

// #52 バブルマップ (SVG)
(function(){
  const el=document.getElementById('div52');if(!el)return;
  const cities=[{n:'東京',x:195,y:130,r:32,v:'¥420億'},{n:'大阪',x:130,y:145,r:20,v:'¥180億'},{n:'名古屋',x:155,y:130,r:14,v:'¥95億'},{n:'福岡',x:55,y:165,r:12,v:'¥72億'},{n:'札幌',x:215,y:35,r:10,v:'¥45億'},{n:'仙台',x:220,y:85,r:9,v:'¥38億'}];
  let s='<svg viewBox="0 0 310 210" style="width:100%;height:210px"><rect x="15" y="15" width="280" height="185" rx="10" fill="#F0F4FF" stroke="#BFDBFE"/>';
  cities.forEach(c=>{s+=`<circle cx="${c.x}" cy="${c.y}" r="${c.r}" fill="rgba(37,99,235,.4)" stroke="#2563EB" stroke-width="1.5"/><text x="${c.x}" y="${c.y-2}" text-anchor="middle" font-size="8" font-weight="700" fill="#1A2332">${c.n}</text><text x="${c.x}" y="${c.y+8}" text-anchor="middle" font-size="7" fill="#5A6B82">${c.v}</text>`;});
  s+='</svg>';el.innerHTML=s;
})();

// #53 ドットマップ (SVG)
(function(){
  const el=document.getElementById('div53');if(!el)return;
  let s='<svg viewBox="0 0 310 210" style="width:100%;height:210px"><rect x="15" y="15" width="280" height="185" rx="10" fill="#F0F4FF" stroke="#BFDBFE"/>';
  for(let i=0;i<50;i++){const x=30+Math.random()*250,y=30+Math.random()*160;s+=`<circle cx="${x}" cy="${y}" r="3" fill="${MC[Math.floor(Math.random()*5)]}" opacity=".6"/>`;};
  s+=`<text x="155" y="205" text-anchor="middle" font-size="9" fill="var(--text-muted)">各ドット=拠点1件</text></svg>`;el.innerHTML=s;
})();

// #54 フローマップ (SVG)
(function(){
  const el=document.getElementById('div54');if(!el)return;
  let s='<svg viewBox="0 0 320 210" style="width:100%;height:210px"><rect x="10" y="10" width="300" height="190" rx="10" fill="#F0F4FF" stroke="#BFDBFE"/>';
  const nodes=[{x:60,y:60,l:'US',c:'#2563EB'},{x:160,y:40,l:'EU',c:'#059669'},{x:260,y:80,l:'JP',c:'#D97706'},{x:160,y:150,l:'CN',c:'#7C3AED'},{x:260,y:160,l:'SEA',c:'#0891B2'}];
  [[0,2,3],[1,2,2],[3,2,2.5],[4,2,1.5],[0,3,1.5]].forEach(([a,b,w])=>{
    s+=`<line x1="${nodes[a].x}" y1="${nodes[a].y}" x2="${nodes[b].x}" y2="${nodes[b].y}" stroke="${nodes[a].c}" stroke-width="${w}" opacity=".3"/>`;});
  nodes.forEach(n=>{s+=`<circle cx="${n.x}" cy="${n.y}" r="15" fill="${n.c}" opacity=".8"/><text x="${n.x}" y="${n.y+4}" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">${n.l}</text>`;});
  s+='</svg>';el.innerHTML=s;
})();

// #55 バンプチャート
cc('c55','line',{labels:['Q1','Q2','Q3','Q4'],datasets:['食品','家電','衣料','日用品','飲料'].map((s,i)=>({label:s,data:[[1,1,1,1],[2,3,2,3],[3,2,3,2],[4,4,5,4],[5,5,4,5]][i],borderColor:MC[i],borderWidth:2.5,tension:.3,pointRadius:5}))},{scales:{y:{reverse:true,min:1,max:5,grid:{color:'#F1F5F9'},ticks:{callback:v=>v+'位'}},x:{grid:{display:false}}}});

// #56 ランクチャート
cc('c56','line',{labels:['2021','2022','2023','2024','2025'],datasets:['食品','家電','衣料'].map((s,i)=>({label:s,data:[[3,2,1,1,1],[1,1,2,2,3],[2,3,3,3,2]][i],borderColor:MC[i],borderWidth:2,tension:.3,pointRadius:4}))},{scales:{y:{reverse:true,min:1,max:3,grid:{color:'#F1F5F9'},ticks:{callback:v=>v+'位'}},x:{grid:{display:false}}}});

// #57 平行座標
cc('c57','line',{labels:['成長性','収益性','技術力','市場規模','チーム'],datasets:['A社','B社','C社','D社'].map((s,i)=>({label:s,data:[[90,65,88,72,80],[70,82,55,90,75],[85,45,92,60,68],[60,78,70,85,90]][i],borderColor:MC[i],borderWidth:2,pointRadius:4,tension:0}))},{scales:{y:{min:0,max:100,grid:{color:'#F1F5F9'}},x:{grid:{color:'#E5E9F0'}}}});

// #58 ダンベル (HTML)
(function(){
  const el=document.getElementById('div58');if(!el)return;
  const data=[{l:'食品',v1:45,v2:92},{l:'家電',v1:55,v2:78},{l:'衣料',v1:35,v2:68},{l:'日用品',v1:40,v2:72},{l:'飲料',v1:30,v2:58}];
  let h='<svg viewBox="0 0 340 180" style="width:100%;height:180px">';
  data.forEach((d,i)=>{
    const y=15+i*34;
    h+=`<text x="55" y="${y+5}" text-anchor="end" font-size="10" font-weight="600" fill="var(--text-secondary)">${d.l}</text>`;
    h+=`<line x1="${60+d.v1*2.5}" y1="${y}" x2="${60+d.v2*2.5}" y2="${y}" stroke="#CBD5E1" stroke-width="3"/>`;
    h+=`<circle cx="${60+d.v1*2.5}" cy="${y}" r="5" fill="#94A3B8"/><circle cx="${60+d.v2*2.5}" cy="${y}" r="5" fill="#2563EB"/>`;
  });
  h+=`<text x="120" y="178" font-size="9" fill="#94A3B8" font-weight="600">● 2024</text><text x="200" y="178" font-size="9" fill="#2563EB" font-weight="600">● 2025</text>`;
  h+='</svg>';el.innerHTML=h;
})();

// #59 ブレット
cc('c59','bar',{labels:['新規顧客','売上達成','成約件数','NPS'],datasets:[{label:'目標',data:[100,100,100,100],backgroundColor:'#E5E9F0',borderRadius:4,barPercentage:.9,categoryPercentage:.7},{label:'実績',data:[85,72,64,78],backgroundColor:MC.slice(0,4),borderRadius:4,barPercentage:.5,categoryPercentage:.7}]},{indexAxis:'y',scales:{x:{max:110,grid:{color:'#F1F5F9'},ticks:{callback:v=>v+'%'}},y:{grid:{display:false}}}});

// #60 KPIカード (HTML)
(function(){
  const el=document.getElementById('div60');if(!el)return;
  const kpis=[{l:'累計売上高',v:'¥847B',d:'▲+12.3% YoY',dc:'#059669',bg:'#EFF6FF',vc:'#2563EB'},{l:'顧客数',v:'3,842',d:'▲+8.7% QoQ',dc:'#059669',bg:'#ECFDF5',vc:'#059669'},{l:'平均単価',v:'¥28.5B',d:'▼-3.1% MoM',dc:'#DC2626',bg:'#FEF3C7',vc:'#D97706'},{l:'成約件数',v:'127',d:'▲+22.1% YoY',dc:'#059669',bg:'#EDE9FE',vc:'#7C3AED'}];
  let h='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">';
  kpis.forEach(k=>{h+=`<div style="padding:16px;border-radius:10px;text-align:center;background:${k.bg}"><div style="font-size:10px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px">${k.l}</div><div style="font-size:26px;font-weight:800;font-family:var(--mono);color:${k.vc}">${k.v}</div><div style="font-size:11px;font-weight:600;color:${k.dc};margin-top:2px">${k.d}</div></div>`;});
  h+='</div>';el.innerHTML=h;
})();

// #61 進捗バー (HTML)
(function(){
  const el=document.getElementById('div61');if(!el)return;
  const bars=[{l:'データ収集',v:85,c:'#2563EB'},{l:'正規化処理',v:72,c:'#059669'},{l:'チャート生成',v:64,c:'#7C3AED'},{l:'QA検証',v:41,c:'#D97706'},{l:'公開準備',v:18,c:'#DC2626'}];
  let h='';bars.forEach(b=>{h+=`<div style="display:flex;align-items:center;gap:12px;padding:7px 0;border-bottom:1px solid var(--border-light)"><span style="font-size:11px;font-weight:600;min-width:90px">${b.l}</span><div style="flex:1;height:18px;background:var(--border-light);border-radius:9px;overflow:hidden"><div style="height:100%;width:${b.v}%;background:${b.c};border-radius:9px"></div></div><span style="font-size:11px;font-weight:700;font-family:var(--mono);color:${b.c};min-width:35px;text-align:right">${b.v}%</span></div>`;});
  el.innerHTML=h;
})();

// #62 ゲージ (SVG)
(function(){
  const el=document.getElementById('div62');if(!el)return;
  const pct=73;const angle=-90+(pct/100*180);
  let s='<svg viewBox="0 0 200 130" style="width:100%;height:200px;max-width:280px;margin:0 auto;display:block">';
  s+=`<path d="M30,110 A70,70 0 0,1 170,110" fill="none" stroke="#E5E9F0" stroke-width="14" stroke-linecap="round"/>`;
  const endAngle=Math.PI+pct/100*Math.PI;
  const ex=100+70*Math.cos(endAngle),ey=110+70*Math.sin(endAngle);
  s+=`<path d="M30,110 A70,70 0 ${pct>50?1:0},1 ${ex.toFixed(1)},${ey.toFixed(1)}" fill="none" stroke="#2563EB" stroke-width="14" stroke-linecap="round"/>`;
  s+=`<text x="100" y="105" text-anchor="middle" font-size="28" font-weight="800" fill="#2563EB" font-family="var(--mono)">${pct}%</text>`;
  s+=`<text x="100" y="122" text-anchor="middle" font-size="10" fill="var(--text-muted)">目標達成率</text>`;
  s+='</svg>';el.innerHTML=s;
})();

// #63 ワッフル (HTML)
(function(){
  const el=document.getElementById('div63');if(!el)return;
  const pct=73;
  let h='<div style="text-align:center"><div style="display:inline-grid;grid-template-columns:repeat(10,1fr);gap:3px">';
  for(let i=0;i<100;i++){const filled=i<pct;h+=`<div style="width:16px;height:16px;border-radius:3px;background:${filled?'#2563EB':'#E5E9F0'}"></div>`;}
  h+=`</div><div style="font-size:22px;font-weight:800;color:#2563EB;margin-top:8px">${pct}%</div><div style="font-size:10px;color:var(--text-muted)">データカバレッジ</div></div>`;
  el.innerHTML=h;
})();

// #64 スピードメーター (SVG)
(function(){
  const el=document.getElementById('div64');if(!el)return;
  const val=78;
  let s='<svg viewBox="0 0 200 140" style="width:100%;height:200px;max-width:280px;margin:0 auto;display:block">';
  const segs=[{start:0,end:33,c:'#DC2626'},{start:33,end:66,c:'#D97706'},{start:66,end:100,c:'#059669'}];
  segs.forEach(sg=>{
    const sa=Math.PI+sg.start/100*Math.PI,ea=Math.PI+sg.end/100*Math.PI;
    const x1=100+70*Math.cos(sa),y1=115+70*Math.sin(sa),x2=100+70*Math.cos(ea),y2=115+70*Math.sin(ea);
    s+=`<path d="M${x1},${y1} A70,70 0 0,1 ${x2},${y2}" fill="none" stroke="${sg.c}" stroke-width="10" opacity=".3"/>`;
  });
  const na=Math.PI+val/100*Math.PI;
  s+=`<line x1="100" y1="115" x2="${100+55*Math.cos(na)}" y2="${115+55*Math.sin(na)}" stroke="#1A2332" stroke-width="2.5" stroke-linecap="round"/>`;
  s+=`<circle cx="100" cy="115" r="5" fill="#1A2332"/>`;
  s+=`<text x="100" y="107" text-anchor="middle" font-size="24" font-weight="800" fill="#059669">${val}</text>`;
  s+=`<text x="100" y="135" text-anchor="middle" font-size="9" fill="var(--text-muted)">パフォーマンススコア</text>`;
  s+='</svg>';el.innerHTML=s;
})();

// #65 データテーブル (HTML)
(function(){
  const el=document.getElementById('div65');if(!el)return;
  const rows=[['商品A','食品','¥85億','120件','好調'],['商品B','家電','¥62億','85件','安定'],['商品C','衣料','¥48億','65件','好調'],['商品D','日用品','¥35億','45件','成長中'],['商品E','飲料','¥28億','38件','新規']];
  let h='<div style="overflow-x:auto;border:1px solid var(--border);border-radius:8px"><table style="width:100%;border-collapse:collapse;font-size:11px"><thead style="background:#F8FAFC"><tr>';
  ['商品名','カテゴリ','売上','取引数','ステータス'].forEach(th=>{h+=`<th style="padding:8px 12px;text-align:left;font-size:10px;font-weight:800;color:var(--text-muted);border-bottom:2px solid var(--border)">${th}</th>`;});
  h+='</tr></thead><tbody>';
  rows.forEach(r=>{h+='<tr>';r.forEach(td=>{h+=`<td style="padding:7px 12px;border-bottom:1px solid var(--border-light)">${td}</td>`;});h+='</tr>';});
  h+='</tbody></table></div>';el.innerHTML=h;
})();

// #66 スパークバー (HTML)
(function(){
  const el=document.getElementById('div66');if(!el)return;
  const data=[{l:'食品',vals:[3,5,4,7,6,8,9]},{l:'家電',vals:[4,3,5,4,6,5,7]},{l:'衣料',vals:[2,4,3,5,4,3,6]}];
  let h='';data.forEach(d=>{
    const max=Math.max(...d.vals);
    h+=`<div style="display:flex;align-items:center;gap:10px;padding:6px 0"><span style="font-size:11px;font-weight:600;min-width:60px">${d.l}</span><div style="display:flex;gap:2px;align-items:end;height:24px">`;
    d.vals.forEach(v=>{h+=`<div style="width:12px;height:${v/max*24}px;background:#2563EB;border-radius:2px;opacity:${.4+v/max*.6}"></div>`;});
    h+=`</div><span style="font-size:11px;font-weight:700;color:#2563EB">${d.vals[d.vals.length-1]}</span></div>`;
  });
  el.innerHTML=h;
})();

// #67 ミニチャート付テーブル (HTML)
(function(){
  const el=document.getElementById('div67');if(!el)return;
  const rows=[{n:'食品',v:'342',trend:[2,4,3,6,5,8,9],c:'#2563EB'},{n:'家電',v:'289',trend:[3,3,4,5,4,6,7],c:'#059669'},{n:'衣料',v:'215',trend:[2,3,2,4,3,5,5],c:'#D97706'}];
  let h='<div style="border:1px solid var(--border);border-radius:8px;overflow:hidden">';
  h+='<div style="display:grid;grid-template-columns:80px 60px 1fr 60px;padding:8px 12px;background:#F8FAFC;font-size:10px;font-weight:800;color:var(--text-muted);border-bottom:2px solid var(--border)"><span>カテゴリ</span><span>件数</span><span>7日トレンド</span><span>変化</span></div>';
  rows.forEach(r=>{
    const max=Math.max(...r.trend);
    const pts=r.trend.map((v,i)=>`${i*16},${28-v/max*24}`).join(' ');
    const delta=r.trend[r.trend.length-1]-r.trend[0];
    h+=`<div style="display:grid;grid-template-columns:80px 60px 1fr 60px;padding:6px 12px;align-items:center;border-bottom:1px solid var(--border-light)"><span style="font-size:11px;font-weight:600">${r.n}</span><span style="font-size:11px;font-family:var(--mono)">${r.v}</span><svg viewBox="-2 0 100 32" width="96" height="28"><polyline points="${pts}" fill="none" stroke="${r.c}" stroke-width="1.5"/></svg><span style="font-size:11px;font-weight:700;color:${delta>=0?'#059669':'#DC2626'}">${delta>=0?'▲':'▼'}${Math.abs(delta)}</span></div>`;
  });
  h+='</div>';el.innerHTML=h;
})();

// #68 アノテーション付チャート
cc('c68','line',{labels:M,datasets:[{label:'月次売上高',data:[120,110,180,150,160,220,190,200,280,250,270,350],borderColor:'#2563EB',tension:.4,pointRadius:v=>[0,0,0,0,0,0,0,0,0,0,0,6][v.dataIndex]||2,pointBackgroundColor:v=>v.dataIndex===11?'#DC2626':'#2563EB',backgroundColor:'rgba(37,99,235,.08)',fill:true}]},{...noL,scales:gS});

// #69 スモールマルチプル
(function(){
  const sectors=['食品','家電','衣料','日用品'];
  const allData=[[32,28,45,38,55,48,61],[28,35,32,42,38,45,40],[22,25,28,30,32,28,35],[18,20,25,22,28,32,30]];
  sectors.forEach((s,i)=>{
    cc('c69_'+i,'line',{labels:['1','2','3','4','5','6','7'],datasets:[{data:allData[i],borderColor:MC[i],backgroundColor:MC[i]+'22',fill:true,tension:.4,pointRadius:0,borderWidth:1.5}]},{...noL,scales:{y:{display:false},x:{display:false}},plugins:{title:{display:true,text:s,font:{size:10,weight:'700'},color:'#5A6B82'}}});
  });
  // Replace div69 with 4 canvases
  const el=document.getElementById('div69');if(!el)return;
  el.innerHTML='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">'+sectors.map((_,i)=>`<canvas id="c69_${i}" height="80"></canvas>`).join('')+'</div>';
  setTimeout(()=>{
    sectors.forEach((s,i)=>{
      cc('c69_'+i,'line',{labels:['1','2','3','4','5','6','7'],datasets:[{data:allData[i],borderColor:MC[i],backgroundColor:MC[i]+'22',fill:true,tension:.4,pointRadius:0,borderWidth:1.5}]},{...noL,scales:{y:{display:false},x:{display:false}},plugins:{title:{display:true,text:s,font:{size:10,weight:'700'},color:'#5A6B82'}}});
    });
  },100);
})();

// #70 ワードクラウド (HTML)
(function(){
  const el=document.getElementById('div70');if(!el)return;
  const words=[{t:'売上',s:36,c:'#2563EB'},{t:'顧客満足',s:30,c:'#DC2626'},{t:'成長率',s:32,c:'#059669'},{t:'コスト削減',s:28,c:'#3B82F6'},{t:'品質',s:25,c:'#E11D48'},{t:'利益率',s:26,c:'#D97706'},{t:'効率化',s:24,c:'#0891B2'},{t:'DX推進',s:22,c:'#10B981'},{t:'データ分析',s:21,c:'#7C3AED'},{t:'マーケティング',s:20,c:'#0891B2'},{t:'在庫管理',s:20,c:'#8B5CF6'},{t:'物流',s:19,c:'#E11D48'},{t:'リピート率',s:18,c:'#D97706'},{t:'顧客獲得',s:17,c:'#F59E0B'},{t:'ブランド',s:16,c:'#7C3AED'},{t:'生産性',s:17,c:'#475569'},{t:'採用',s:15,c:'#2563EB'},{t:'研修',s:14,c:'#059669'},{t:'新規開拓',s:16,c:'#3B82F6'},{t:'パートナー',s:14,c:'#475569'}];
  let h='<div style="display:flex;flex-wrap:wrap;gap:6px;justify-content:center;align-items:center;padding:8px">';
  words.forEach(w=>{h+=`<span style="font-size:${w.s}px;font-weight:700;color:${w.c};cursor:default;transition:transform .15s" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">${w.t}</span>`;});
  h+='</div>';el.innerHTML=h;
})();

// #71 複合チャート
cc('c71','bar',{labels:Q,datasets:[{label:'売上高(億)',data:[120,150,130,180,160,200,185,220],backgroundColor:'#2563EB',borderRadius:4,order:2},{label:'件数',data:[45,52,48,61,55,63,58,72],type:'line',borderColor:'#D97706',pointBackgroundColor:'#D97706',tension:.3,yAxisID:'y1',order:1}]},{scales:{x:{grid:{display:false}},y:{beginAtZero:true,grid:{color:'#F1F5F9'},title:{display:true,text:'億円'}},y1:{position:'right',beginAtZero:true,grid:{display:false},title:{display:true,text:'件数'}}}});

// #72 ダッシュボードパネル (HTML)
(function(){
  const el=document.getElementById('div72');if(!el)return;
  let h='<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px">';
  [{l:'月間売上',v:'¥285億',d:'↑12%',c:'#2563EB'},{l:'新規顧客',v:'148社',d:'↑8%',c:'#059669'},{l:'成約',v:'12件',d:'↑22%',c:'#7C3AED'}].forEach(k=>{
    h+=`<div style="padding:12px;border:1px solid var(--border);border-radius:8px;text-align:center"><div style="font-size:9px;font-weight:700;color:var(--text-muted)">${k.l}</div><div style="font-size:20px;font-weight:800;color:${k.c};font-family:var(--mono)">${k.v}</div><div style="font-size:10px;color:#059669;font-weight:600">${k.d}</div></div>`;
  });
  h+='</div>';el.innerHTML=h;
})();

// #73 比較ダッシュボード (HTML)
(function(){
  const el=document.getElementById('div73');if(!el)return;
  let h='<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">';
  [{title:'今期',items:[['売上高','¥285億','#2563EB'],['件数','72件','#059669'],['平均','¥3.9億','#D97706']]},{title:'前期',items:[['売上高','¥254億','#94A3B8'],['件数','61件','#94A3B8'],['平均','¥4.2億','#94A3B8']]}].forEach(col=>{
    h+=`<div style="border:1px solid var(--border);border-radius:8px;padding:12px"><div style="font-size:12px;font-weight:800;margin-bottom:8px;color:var(--text)">${col.title}</div>`;
    col.items.forEach(([l,v,c])=>{h+=`<div style="display:flex;justify-content:space-between;padding:4px 0;font-size:11px"><span style="color:var(--text-secondary)">${l}</span><span style="font-weight:700;color:${c};font-family:var(--mono)">${v}</span></div>`;});
    h+='</div>';
  });
  h+='</div>';el.innerHTML=h;
})();

// #74 トレンドインジケーター
cc('c74','line',{labels:M.slice(0,8),datasets:[{data:[100,105,102,112,108,118,115,125],borderColor:'#2563EB',backgroundColor:'rgba(37,99,235,.1)',fill:true,tension:.4,pointRadius:0,borderWidth:2}]},{...noL,scales:{y:{grid:{color:'#F1F5F9'}},x:{grid:{display:false}}}});

// #75 ベンチマーク比較
cc('c75','bar',{labels:['成長率','利益率','売上高','人材数','特許数'],datasets:[{label:'自社',data:[85,62,78,70,55],backgroundColor:'#2563EB',borderRadius:4},{label:'業界平均',data:[65,58,60,65,48],backgroundColor:'#E5E9F0',borderRadius:4}]},{scales:gS});

// #76 モーションチャート (Interactive)
(function(){
  const el=document.getElementById('div76');if(!el)return;
  const years=[2018,2019,2020,2021,2022,2023,2024];
  const items=['Product A','Product B','Product C','Product D','Product E','Product F','Product G'];
  const allData=years.map((_,yi)=>items.map((_,ii)=>({
    x:30+Math.round(Math.random()*40+yi*2+ii*3),
    y:30+Math.round(Math.random()*35+yi*3),
    r:5+Math.round(Math.random()*15+yi*1.5)
  })));
  let frame=0,playing=false,timer=null;
  function render(){
    const d=allData[frame];
    let svg='<div style="text-align:center;margin-bottom:8px"><button id="motionPlay76" style="padding:6px 20px;border-radius:20px;border:none;background:linear-gradient(135deg,#2563EB,#7C3AED);color:#fff;font-weight:700;font-size:12px;cursor:pointer;box-shadow:0 2px 8px rgba(37,99,235,.3)">▶ 再生</button></div>';
    svg+='<div style="font-size:12px;font-weight:700;text-align:center;color:var(--text-secondary);margin-bottom:6px">Year: '+years[frame]+'</div>';
    const W=380,H=220,P=40,PB=30,PR=10,PT=10;
    svg+='<svg viewBox="0 0 '+W+' '+H+'" style="width:100%;max-height:220px">';
    // grid
    for(let i=0;i<=5;i++){const y=PT+(H-PT-PB)/5*i;svg+='<line x1="'+P+'" y1="'+y+'" x2="'+(W-PR)+'" y2="'+y+'" stroke="#F1F5F9" stroke-width="1"/>';svg+='<text x="'+(P-4)+'" y="'+(y+3)+'" text-anchor="end" font-size="9" fill="#8C99AB">'+(65-i*7)+'</text>';}
    for(let i=0;i<=5;i++){const x=P+(W-P-PR)/5*i;svg+='<text x="'+x+'" y="'+(H-PB+14)+'" text-anchor="middle" font-size="9" fill="#8C99AB">'+(30+i*8)+'</text>';}
    // bubbles
    const colors=['#2563EB','#059669','#D97706','#DC2626','#7C3AED','#0891B2','#E11D48'];
    d.forEach((p,i)=>{const cx=P+(p.x-30)/(40+years.length*2+items.length*3)*(W-P-PR);const cy=PT+(65-p.y)/(35+years.length*3)*(H-PT-PB);svg+='<circle cx="'+cx+'" cy="'+cy+'" r="'+p.r+'" fill="'+colors[i%7]+'" opacity="0.6" stroke="'+colors[i%7]+'" stroke-width="1.5"/>';});
    svg+='</svg>';
    el.innerHTML=svg;
    document.getElementById('motionPlay76').textContent=playing?'⏸ 停止':'▶ 再生';
    document.getElementById('motionPlay76').onclick=function(){
      if(playing){playing=false;clearInterval(timer);this.textContent='▶ 再生';}
      else{playing=true;this.textContent='⏸ 停止';timer=setInterval(function(){frame=(frame+1)%years.length;render();},1200);}
    };
  }
  render();
})();

// #77 リアルタイムストリームチャート (Interactive)
(function(){
  const el=document.getElementById('c77');if(!el)return;
  const ctx=el.getContext('2d');
  const maxPts=12;
  let labels=Array.from({length:maxPts},(_,i)=>''+String(7+i).padStart(2,'0'));
  let data=[33,24,25,28,32,31,30,30,42,41,47,46];
  const chart=new Chart(ctx,{type:'line',data:{labels:labels,datasets:[{data:data,borderColor:'#2563EB',backgroundColor:'rgba(37,99,235,.08)',fill:true,tension:.4,pointRadius:4,pointBackgroundColor:'#2563EB',pointBorderColor:'#fff',pointBorderWidth:2,borderWidth:2.5}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{min:15,max:55,grid:{color:'#F1F5F9'},ticks:{font:{size:10},color:'#8C99AB'}},x:{grid:{display:false},ticks:{font:{size:10},color:'#8C99AB'}}},animation:{duration:600}}});
  let tick=19;
  setInterval(function(){
    const v=20+Math.round(Math.random()*30);
    chart.data.labels.push(String(tick).padStart(2,'0'));
    chart.data.datasets[0].data.push(v);
    if(chart.data.labels.length>maxPts){chart.data.labels.shift();chart.data.datasets[0].data.shift();}
    chart.update();tick++;
  },2000);
})();

// #78 セグメント比較
cc('c78','bar',{labels:['直販','代理店','EC','卸売','その他'],datasets:[{label:'売上額',data:[320,480,180,250,60],backgroundColor:MC.slice(0,5),borderRadius:4}]},{...noL,scales:gS});

// #79 サマリーダッシュボード (HTML)
(function(){
  const el=document.getElementById('div79');if(!el)return;
  let h='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px">';
  [{l:'顧客数',v:'3,842',c:'#2563EB',d:'↑8.7%'},{l:'受注総額',v:'¥847B',c:'#059669',d:'↑12.3%'},{l:'平均単価',v:'¥28.5B',c:'#D97706',d:'↓3.1%'},{l:'成約',v:'127',c:'#7C3AED',d:'↑22.1%'}].forEach(k=>{
    h+=`<div style="padding:10px;border-radius:8px;text-align:center;background:${k.c}11;border:1px solid ${k.c}33"><div style="font-size:9px;font-weight:700;color:var(--text-muted)">${k.l}</div><div style="font-size:18px;font-weight:800;color:${k.c};font-family:var(--mono)">${k.v}</div><div style="font-size:10px;color:${k.d.includes('↑')?'#059669':'#DC2626'};font-weight:600">${k.d}</div></div>`;
  });
  h+='</div>';
  h+='<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px">';
  [['データ収集','85%','#2563EB'],['正規化','72%','#059669'],['公開準備','41%','#D97706']].forEach(([l,v,c])=>{
    const pct=parseInt(v);
    h+=`<div style="padding:8px;border:1px solid var(--border);border-radius:8px"><div style="font-size:9px;font-weight:700;color:var(--text-muted);margin-bottom:4px">${l}</div><div style="height:8px;background:var(--border-light);border-radius:4px;overflow:hidden"><div style="height:100%;width:${pct}%;background:${c};border-radius:4px"></div></div><div style="font-size:10px;font-weight:700;color:${c};text-align:right;margin-top:2px">${v}</div></div>`;
  });
  h+='</div>';el.innerHTML=h;
})();
</script>'''

if __name__ == '__main__':
    main()
