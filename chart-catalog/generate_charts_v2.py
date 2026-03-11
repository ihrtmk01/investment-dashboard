#!/usr/bin/env python3
"""Generate 79-chart visualization samples HTML with 作り方ガイド."""

# ── Guide data per chart ──
# Each: (id, name, cat, badge, tlabel, guide_desc, data_fields, how_to_steps)
# data_fields: list of (field_name, purpose)  — NO table refs like T1/T2
# how_to_steps: list of step strings
GUIDES = {
    1: {
        "desc": "カテゴリごとの値を縦棒で比較。大小差が一目でわかる最も基本的なチャート。",
        "data": [("カテゴリ名", "X軸ラベル"), ("件数", "棒の高さ（Y値）")],
        "how": ["カテゴリ名を labels 配列に設定", "対応する数値を data 配列に設定", "borderRadius で角丸、barPercentage で棒幅を調整"]
    },
    2: {
        "desc": "ランキング表示に最適。ラベルが長い場合に横方向で見やすくなる。",
        "data": [("部門名", "Y軸ラベル（ランキング対象）"), ("売上額", "棒の長さ（X値）")],
        "how": ["indexAxis:'y' で横棒に切替", "売上額の降順にソートして labels/data を設定", "barPercentage で棒幅調整"]
    },
    3: {
        "desc": "複数系列の値を棒内に積み上げ、合計と内訳を同時に表示。",
        "data": [("四半期", "X軸ラベル"), ("チャネル名", "系列ごとの分類"), ("受注件数", "各系列の値")],
        "how": ["属性ごとに datasets を作成（VC / CVC / PE など）", "scales の x,y 両方に stacked:true を設定", "色を系列ごとに設定し凡例を表示"]
    },
    4: {
        "desc": "構成比の変化を年度間で比較。全体を100%に正規化して表示。",
        "data": [("年度", "X軸ラベル"), ("ステージ", "分類（直販/EC/卸売等）"), ("構成比", "割合（%）")],
        "how": ["各年度の合計が100%になるよう正規化", "stacked:true + max:100 で100%棒に", "Y軸 ticks に callback: v=>v+'%' を設定"]
    },
    5: {
        "desc": "2系列を横並びで直接比較。国内vs海外のような対比に最適。",
        "data": [("カテゴリ名", "X軸ラベル"), ("国内件数", "系列1の値"), ("海外件数", "系列2の値")],
        "how": ["2つの datasets を定義（stacked は false）", "色を明確に区別（青/緑など）", "barPercentage と categoryPercentage でグループ幅を調整"]
    },
    6: {
        "desc": "正負の値を中心軸から左右に伸ばし、増減を直感的に表現。",
        "data": [("カテゴリ名", "Y軸ラベル"), ("前年比(%)", "正負の値")],
        "how": ["indexAxis:'y' で横棒に設定", "値の正負で backgroundColor を動的に切替（正→緑、負→赤）", "X軸の0を中心にグリッドを表示"]
    },
    7: {
        "desc": "2時点間の順位・値の変化を線の傾きで表現。上昇/下降が直感的。",
        "data": [("カテゴリ名", "各線のラベル"), ("開始年の値", "左端の値"), ("終了年の値", "右端の値")],
        "how": ["labels を2時点（例：2024 / 2025）に設定", "カテゴリごとに dataset を作成し2点を結ぶ", "tension:0 で直線、pointRadius を大きめに"]
    },
    8: {
        "desc": "極小サイズの折れ線。KPIカードやテーブル内にインライン配置。",
        "data": [("指標名", "ラベル"), ("時系列値", "SVGポリラインのポイント")],
        "how": ["SVG の polyline でミニ折れ線を描画", "viewBox を小さく設定（例：0 0 120 45）", "最新値をテキストで併記"]
    },
    9: {
        "desc": "多軸スコアリング。企業の強み・弱みを多角形の面積で比較。",
        "data": [("評価軸", "放射状ラベル（成長性/収益性/技術力…）"), ("製品名", "比較対象"), ("スコア", "各軸の値（0-100）")],
        "how": ["type:'radar' で作成", "scales.r に beginAtZero:true, max:100 を設定", "2社比較なら datasets を2つ、fill で面積着色"]
    },
    10: {
        "desc": "時系列トレンドの可視化。月別推移や年度比較に定番。",
        "data": [("月/四半期", "X軸ラベル"), ("設立企業数", "Y軸の値")],
        "how": ["type:'line'、tension:0.4 で滑らかに", "fill:true + 低透明度 backgroundColor でエリア付き", "複数年なら datasets を分け色で区別"]
    },
    11: {
        "desc": "単位の異なる2指標を左右Y軸で重ねて相関を観察。",
        "data": [("四半期", "X軸ラベル"), ("売上高（百万円）", "左Y軸の値"), ("受注件数", "右Y軸の値")],
        "how": ["datasets に yAxisID:'y' と 'y1' をそれぞれ指定", "scales に y（左）と y1（右、position:'right'）を定義", "右Y軸の grid は display:false で重複回避"]
    },
    12: {
        "desc": "離散的な変化を段階状に表示。累計カウント系に最適。",
        "data": [("月", "X軸ラベル"), ("累計契約数", "段階的に増加する値")],
        "how": ["stepped:'before' または 'after' を設定", "fill:false で線のみ表示", "pointRadius を大きめにして各ステップを明示"]
    },
    13: {
        "desc": "折れ線の下を塗りつぶし、量のボリューム感を表現。",
        "data": [("四半期", "X軸ラベル"), ("累積売上高", "エリアの高さ")],
        "how": ["fill:true + backgroundColor に透過色を設定", "複数系列ならそれぞれ異なる色で塗り分け", "tension で曲線の滑らかさを調整"]
    },
    14: {
        "desc": "複数系列のエリアを積み上げ、合計トレンドと内訳を同時に把握。",
        "data": [("四半期", "X軸ラベル"), ("カテゴリ名", "系列分類"), ("売上高", "各系列の値")],
        "how": ["y軸に stacked:true を設定", "各 dataset に fill:true を設定", "色の透明度を高め（0.3程度）に設定して重なりを表現"]
    },
    15: {
        "desc": "積み上げエリアを100%に正規化。構成比の推移を面積で表現。",
        "data": [("四半期", "X軸ラベル"), ("カテゴリ名", "系列分類"), ("構成比(%)", "正規化後の値")],
        "how": ["各時点の合計が100になるよう正規化", "stacked:true + max:100 を設定", "ticks callback で '%' を追加"]
    },
    16: {
        "desc": "日付を曜日×週のグリッドで表示。イベント頻度の時間パターンを発見。",
        "data": [("日付", "グリッド位置（曜日×週）"), ("イベント件数", "セルの色濃度")],
        "how": ["CSS Grid で 曜日(列) × 週(行) のグリッドを構成", "値を 0〜max で正規化し rgba の alpha に変換", "セル内に値を表示、ラベル行/列を追加"]
    },
    17: {
        "desc": "タスクやプロジェクトの期間を横棒で表示。期間の重複が一目瞭然。",
        "data": [("プロジェクト名", "行ラベル"), ("開始時点", "棒の左端位置(%)"), ("終了時点", "棒の右端位置(%)")],
        "how": ["各行に flex レイアウト：ラベル + トラック + バー", "left と width を % で設定し期間を表現", "下部にスケール（年号）を配置"]
    },
    18: {
        "desc": "イベントを時系列に縦並びで表示。マイルストーン一覧に最適。",
        "data": [("日付", "イベントの発生日"), ("イベント内容", "テキスト説明"), ("カテゴリ色", "ドットの色分け")],
        "how": ["各イベントを flex で横配置：ドット + 縦線 + コンテンツ", "ドットの色でカテゴリを区別", "最後のイベントには縦線を付けない"]
    },
    19: {
        "desc": "今期と前期を重ねて比較。成長/減速を視覚的に判断。",
        "data": [("月", "X軸ラベル"), ("今期の値", "実線で表示"), ("前期の値", "破線で表示")],
        "how": ["今期は実線（borderWidth:2.5）で強調", "前期は borderDash:[5,5] で破線 + 薄い色", "同一スケールで重ね合わせ"]
    },
    20: {
        "desc": "始値・終値・高値・安値を1本の棒で表現。単価変動の把握に。",
        "data": [("月", "X軸ラベル"), ("始値", "棒のベース位置"), ("終値", "棒の上端位置")],
        "how": ["stacked bar で base(透明) + body(着色) を積む", "終値≧始値→緑、終値<始値→赤で色分け", "ヒゲ（高値/安値）は line dataset で追加可能"]
    },
    21: {
        "desc": "連続値の分布を区間（ビン）に分けて度数を棒で表示。",
        "data": [("価格レンジ", "X軸ラベル（ビン名）"), ("企業数", "各ビンの度数")],
        "how": ["barPercentage:1, categoryPercentage:0.95 で棒を密着", "X軸にレンジ名、Y軸に度数を設定", "borderWidth を薄く設定してビン境界を表現"]
    },
    22: {
        "desc": "ヒストグラムの折れ線版。2つ以上の分布を重ねて比較しやすい。",
        "data": [("価格レンジ", "X軸ラベル"), ("国内企業数", "系列1の度数"), ("海外企業数", "系列2の度数")],
        "how": ["type:'line' で各ビン中央点を結ぶ", "fill:false で線のみ表示", "複数系列を色で区別し重ねて比較"]
    },
    23: {
        "desc": "中央値・四分位・外れ値を表示。カテゴリ間の分布比較に最適。",
        "data": [("カテゴリ名", "行ラベル"), ("Q1/中央値/Q3/min/max", "統計量")],
        "how": ["SVG で rect（IQR箱）+ line（ひげ/中央値）を描画", "横方向のスケールで値を位置に変換", "カテゴリごとに Y 位置をずらして並べる"]
    },
    24: {
        "desc": "箱ひげ図の拡張。密度分布の形状まで表現できる。",
        "data": [("単価", "X軸（値の範囲）"), ("密度", "Y軸（各点での確率密度）")],
        "how": ["type:'line' の fill:true で密度曲線を面で表現", "tension:0.4 で滑らかなカーブに", "複数カテゴリを重ねて透過色で区別"]
    },
    25: {
        "desc": "個々のデータ点を表示。分布の偏りやクラスタが見える。",
        "data": [("カテゴリID", "X軸（ジッター付き）"), ("単価", "Y軸の値")],
        "how": ["type:'scatter' で散布図として描画", "X軸にランダムなジッター（±0.15）を加えて点を分散", "ticks callback でカテゴリ名に変換"]
    },
    26: {
        "desc": "データが正規分布に従うか検証。理論線からの乖離で判断。",
        "data": [("理論分位点", "X軸"), ("サンプル分位点", "Y軸")],
        "how": ["逆正規分布関数でX値、ソート済みデータでY値を計算", "対角線（y=x）を破線の line dataset で追加", "点が対角線に沿えば正規分布と判断"]
    },
    27: {
        "desc": "値がある閾値以下になる確率を累積で表示。パーセンタイル把握に。",
        "data": [("単価", "X軸（値）"), ("累積確率", "Y軸（0〜1）")],
        "how": ["データをソートし、i/n で累積確率を計算", "fill:true で下を塗りつぶし", "Y軸 ticks で '%' 表記に変換"]
    },
    28: {
        "desc": "複数期間の分布を縦にずらして重ね、変化を一覧比較。",
        "data": [("価格レンジ", "X軸"), ("年度別の密度", "各系列（オフセット付き）")],
        "how": ["各年の密度カーブを Y にオフセットを加えてずらす", "fill:true + 透過色で重なりを視覚化", "凡例で年度を区別"]
    },
    29: {
        "desc": "2軸の関係性を点で表示。4象限に分けて分類・評価に使う。",
        "data": [("広告費", "X軸"), ("単価", "Y軸")],
        "how": ["type:'scatter' で描画", "annotation プラグインで十字線を引き4象限に", "pointRadius で点サイズを調整"]
    },
    30: {
        "desc": "散布図に回帰直線を追加。相関の強さと方向を視覚的に示す。",
        "data": [("広告費", "X軸"), ("単価", "Y軸")],
        "how": ["散布図 dataset + 回帰線 line dataset を重ねる", "回帰線は始点と終点の2点で定義", "borderDash:[6,3] で破線にして目立たせすぎない"]
    },
    31: {
        "desc": "散布図に第3変数（バブルサイズ）を追加。3次元の関係を2Dで表現。",
        "data": [("単価", "X軸"), ("成長率", "Y軸"), ("資金売上高", "バブルの半径 r")],
        "how": ["type:'bubble'、data に {x, y, r} オブジェクトを設定", "r の値で面積が変わるため、sqrt変換で面積比例にすると正確", "透過色で重なりを視認可能に"]
    },
    32: {
        "desc": "変数間の相関係数をグリッドで一覧表示。多変量分析の第一歩。",
        "data": [("変数名", "行/列ラベル"), ("相関係数", "セルの値と色濃度")],
        "how": ["CSS Grid で N×N のマトリックスを構成", "相関係数（-1〜1）を色濃度に変換", "対角線は常に 1.00、対称配置"]
    },
    33: {
        "desc": "2軸のクロス集計値を色濃度で表現。集中度やパターンの発見に。",
        "data": [("カテゴリ名", "行ラベル"), ("ステージ名", "列ラベル"), ("受注件数", "セルの色濃度")],
        "how": ["CSS Grid で行×列のグリッドを構成", "最大値で正規化し rgba の alpha に変換", "セル内に数値を表示"]
    },
    34: {
        "desc": "取引先⇔製品などの関係性をノードとエッジで表示。",
        "data": [("部門名", "ノード（大きめ円）"), ("製品名", "ノード（小さめ円）"), ("投資関係", "エッジ（接続線）")],
        "how": ["SVG で circle（ノード）と line（エッジ）を描画", "ノードサイズで重要度、色でカテゴリを区別", "テキストラベルを各ノード下に配置"]
    },
    35: {
        "desc": "フロー（流れ）の量を帯の太さで表現。資金の流れの全体像を把握。",
        "data": [("チャネル名", "左側ノード"), ("製品カテゴリ", "右側ノード"), ("売上額", "フローの太さ")],
        "how": ["SVG で左右に rect ノードを配置", "path のベジェ曲線でフローを接続", "stroke-width で量を表現（透過度を下げて重なりを可視化）"]
    },
    36: {
        "desc": "グループ間の相互関係量を円弧と帯で表現。共同投資分析に。",
        "data": [("カテゴリ名", "円弧上のセグメント"), ("共同受注件数", "帯（コード）の太さ")],
        "how": ["SVG で円弧を配置（三角関数で座標計算）", "2カテゴリ間をベジェ曲線で接続", "opacity を低めに設定し重なりを表現"]
    },
    37: {
        "desc": "データパイプラインやプロセスの流れを矢印で接続して表示。",
        "data": [("工程名", "ノードのラベル"), ("接続関係", "矢印の始点/終点")],
        "how": ["SVG で rect ノード + line + marker（矢印）を配置", "marker-end で矢印ヘッドを設定", "色でカテゴリを区別"]
    },
    38: {
        "desc": "面積で量を比較。階層構造の全体像と詳細を同時に把握。",
        "data": [("プロジェクト名", "セルのラベル"), ("売上額", "セルの面積（span数）")],
        "how": ["CSS Grid で構成（大きい項目は grid-column:span 2）", "セルの面積比が値に比例するよう配置", "色でカテゴリを区別、hover で強調"]
    },
    39: {
        "desc": "放射状に階層を表現。内側→外側で親→子の関係を表示。",
        "data": [("親カテゴリ", "内輪のセグメント"), ("子カテゴリ", "外輪のセグメント"), ("値", "各セグメントの角度")],
        "how": ["2つの doughnut datasets で内輪/外輪を表現", "cutout:'30%' で中心を空ける", "内輪の親に対応する子を外輪で角度を合わせて配置"]
    },
    40: {
        "desc": "クラスタリング結果を階層的な樹形図で表示。類似度の構造を可視化。",
        "data": [("カテゴリ名", "葉ノードのラベル"), ("距離/類似度", "結合の高さ")],
        "how": ["SVG で垂直線（各葉）+ 水平線（結合）を描画", "結合の高さが距離に比例するよう Y 座標を設定", "段階的に結合を上方向に描画"]
    },
    41: {
        "desc": "サイズの異なる円を密に詰めて面積比較。ツリーマップの円形版。",
        "data": [("カテゴリ名", "ラベル"), ("件数", "円の半径")],
        "how": ["SVG で circle を配置（重ならないよう座標調整）", "面積が値に比例するよう r = sqrt(value) でスケーリング", "透過色 + stroke で境界を表現"]
    },
    42: {
        "desc": "ツリーマップの縦版。階層を上→下の矩形分割で表現。",
        "data": [("カテゴリ階層", "各レベルのラベル"), ("値", "矩形の幅")],
        "how": ["SVG で各レベルを横帯として描画", "子ノードは親の幅を按分して横に分割", "レベルごとに色のトーンを変える"]
    },
    43: {
        "desc": "親子関係をノードとエッジで階層表示。組織図やカテゴリ分類に。",
        "data": [("ノード名", "各ノードのラベル"), ("親子関係", "エッジ接続")],
        "how": ["SVG で circle/rect ノードを階層的に配置", "親→子を line で接続", "レベルごとに色を変えてノードサイズを小さくする"]
    },
    44: {
        "desc": "円グラフの中央を空けた版。構成比を表示しつつ中心に補足情報を配置可能。",
        "data": [("チャネル名", "セグメントのラベル"), ("構成比", "各セグメントの値")],
        "how": ["type:'doughnut' で作成", "cutout:'60%' で中央を空ける", "hoverOffset で hover 時にセグメントを浮き出す"]
    },
    45: {
        "desc": "全体に対する各部分の割合を扇形で表示。構成比の一覧把握に。",
        "data": [("カテゴリ名", "セグメントのラベル"), ("件数", "各セグメントの値")],
        "how": ["type:'pie' で作成", "borderWidth:2, borderColor:'#FFF' でセグメント境界を明確に", "凡例を右側に配置して色との対応を表示"]
    },
    46: {
        "desc": "棒グラフ（降順）＋累積折れ線。80-20法則（パレート原則）の検証に。",
        "data": [("カテゴリ名", "X軸ラベル（降順）"), ("件数", "棒の高さ"), ("累積%", "折れ線の値")],
        "how": ["値の降順にソートし棒グラフを描画", "累積%を計算して折れ線を重ねる（yAxisID:'y1'）", "右Y軸に 0-100% のスケールを設定"]
    },
    47: {
        "desc": "増加・減少の積み上げで最終値への推移を表現。累計変動分析に。",
        "data": [("期間/項目", "X軸ラベル"), ("増加額", "正の棒"), ("減少額", "負の棒")],
        "how": ["3つの datasets: ベース(透明) + 増加(緑) + 減少(赤)", "stacked:true で積み上げ", "ベースの高さで棒の開始位置を制御"]
    },
    48: {
        "desc": "棒の幅と高さの両方で値を表現。市場サイズ×構成比の同時把握に。",
        "data": [("カテゴリ名", "列ラベル"), ("市場サイズ", "列の幅"), ("ステージ構成比", "行の高さ")],
        "how": ["CSS flex で列を横に配置（width を市場サイズに比例）", "各列内を flex-direction:column でステージ分割", "高さをステージの構成比に比例させる"]
    },
    49: {
        "desc": "棒グラフの代替。棒を細くして先端に丸を付けたスタイリッシュな表現。",
        "data": [("カテゴリ名", "Y軸ラベル"), ("件数", "棒の長さ")],
        "how": ["indexAxis:'y' + barPercentage:0.15 で細い棒に", "borderRadius:20 で先端を丸く", "棒グラフの代替としてモダンな見た目に"]
    },
    50: {
        "desc": "プロセスの段階的な絞り込みを表現。コンバージョン分析に。",
        "data": [("ステージ名", "各段階のラベル"), ("件数", "棒の幅（%）"), ("変換率", "表示用テキスト")],
        "how": ["各ステージを div で横棒として配置", "width を全体に対する比率で設定", "上から順に幅を狭くして漏斗型に"]
    },
    51: {
        "desc": "地域データを塗り分けで表示。都道府県/国別の投資集中度を可視化。",
        "data": [("地域名", "矩形のラベル"), ("受注件数", "色の濃度")],
        "how": ["SVG で地域ごとに rect を配置（簡易版）", "値を最大値で正規化し rgba の alpha に変換", "本格実装は D3.js + GeoJSON を使用"]
    },
    52: {
        "desc": "地図上にバブルを配置。位置と値の両方を同時に表現。",
        "data": [("都市名", "バブルの位置"), ("売上額", "バブルのサイズ")],
        "how": ["SVG で背景地図 + circle を配置", "半径を売上額に比例させる（sqrt スケーリング推奨）", "ラベルとして都市名・金額をテキスト表示"]
    },
    53: {
        "desc": "個々の拠点を点で表示。分布パターンや集中エリアの把握に。",
        "data": [("位置座標", "ドットの配置"), ("カテゴリ", "ドットの色分け")],
        "how": ["SVG で小さな circle を多数配置", "色でカテゴリを区別", "ランダム配置ではなく実座標が理想（簡易版はランダム）"]
    },
    54: {
        "desc": "拠点間の資金の流れを矢印で表現。クロスボーダー投資の可視化に。",
        "data": [("拠点名", "ノードの位置"), ("投資フロー量", "線の太さ")],
        "how": ["SVG で circle ノード + line エッジを配置", "stroke-width でフロー量を表現", "方向性を矢印で示す"]
    },
    55: {
        "desc": "順位の変動を時系列で可視化。順位が入れ替わるダイナミクスを表現。",
        "data": [("カテゴリ名", "各線のラベル"), ("四半期", "X軸"), ("順位", "Y軸（逆順）")],
        "how": ["Y軸に reverse:true を設定（1位が上）", "各カテゴリを line dataset として描画", "tension:0.3 で線の交差を滑らかに"]
    },
    56: {
        "desc": "シンプルな順位変動チャート。少数グループの推移に最適。",
        "data": [("カテゴリ名", "各線のラベル"), ("年度", "X軸"), ("順位", "Y軸（逆順）")],
        "how": ["Y軸に reverse:true、min:1、max:N を設定", "ticks callback で '位' を付加", "pointRadius を大きめに設定して各点を明示"]
    },
    57: {
        "desc": "多変量データを平行な軸上に折れ線で表示。企業プロファイルの比較に。",
        "data": [("評価軸", "X軸の各軸ラベル"), ("製品名", "各線のラベル"), ("スコア", "各軸上の値")],
        "how": ["type:'line' の labels に各軸名を設定", "tension:0 で直線（軸間を直結）", "X軸のグリッドを表示して各軸を明示"]
    },
    58: {
        "desc": "2時点の値を点で示し線で結ぶ。変化量と方向を同時に表現。",
        "data": [("カテゴリ名", "Y軸ラベル"), ("旧値", "左端の点"), ("新値", "右端の点")],
        "how": ["SVG で2つの circle + 接続 line を描画", "旧値（灰色）と新値（青）で色を変える", "凡例で時点を説明"]
    },
    59: {
        "desc": "目標に対する達成度をコンパクトに表示。複数KPIの一覧比較に。",
        "data": [("指標名", "Y軸ラベル"), ("実績値(%)", "前面の棒"), ("目標値(%)", "背面の棒")],
        "how": ["2つの datasets: 目標（淡い色）と 実績（濃い色）", "indexAxis:'y' で横棒、barPercentage で太さを変える", "実績の棒を細く（0.5）、目標を太く（0.9）"]
    },
    60: {
        "desc": "主要KPIを大きな数字で一覧表示。ダッシュボードのヘッダーに定番。",
        "data": [("指標名", "カードのタイトル"), ("現在値", "大きく表示する数値"), ("変化率", "前期比の増減")],
        "how": ["CSS Grid で横並びカードを配置", "数値は大きめフォント（26px+）のモノスペースで", "変化率は正→緑、負→赤で色分け"]
    },
    61: {
        "desc": "完了率をバー形式で表示。プロジェクト進捗の一覧に。",
        "data": [("工程名", "行ラベル"), ("完了率(%)", "バーの長さ")],
        "how": ["外枠 div（背景色）+ 内枠 div（完了色）で構成", "width を完了率 % で設定", "数値ラベルを右端に配置"]
    },
    62: {
        "desc": "円弧型のメーター表示。達成率や健全性スコアの表現に。",
        "data": [("指標名", "ラベル"), ("達成率(%)", "円弧の長さ")],
        "how": ["SVG で半円の arc path を描画（背景 + 実績）", "三角関数で端点座標を計算", "中央に大きな数値テキストを配置"]
    },
    63: {
        "desc": "100個のセルで構成比を直感的に表現。パーセンテージの実感に最適。",
        "data": [("指標名", "ラベル"), ("割合(%)", "塗りつぶすセル数")],
        "how": ["CSS Grid で 10×10 のセルを配置", "i < pct のセルを着色、それ以外はグレー", "下部にパーセンテージを大きく表示"]
    },
    64: {
        "desc": "アナログメーター風の表示。スコアやパフォーマンス指標の直感的表現。",
        "data": [("指標名", "ラベル"), ("スコア", "針の角度")],
        "how": ["SVG で3色の半円弧（赤/橙/緑）を描画", "値を角度に変換し needle（line）を配置", "中心に circle、下部にスコア数値を表示"]
    },
    65: {
        "desc": "構造化データをテーブル形式で一覧表示。詳細確認やソートに対応。",
        "data": [("製品名", "行データ"), ("カテゴリ/単価/従業員/ステージ", "列データ")],
        "how": ["HTML table で thead + tbody を構成", "border-collapse で枠線を整理", "tr:hover で行ハイライト、適切な padding で余白を確保"]
    },
    66: {
        "desc": "テーブル行内に極小の棒グラフを配置。数値比較を視覚的に補助。",
        "data": [("カテゴリ名", "行ラベル"), ("時系列値", "各棒の高さ")],
        "how": ["各行に div を flex で横並びの棒として配置", "棒の height を最大値で正規化", "最新値をテキストで併記"]
    },
    67: {
        "desc": "テーブルの各行にミニ折れ線（スパークライン）を配置。トレンド付き一覧。",
        "data": [("カテゴリ名", "行ラベル"), ("件数", "数値カラム"), ("トレンド", "ミニ折れ線用の時系列値")],
        "how": ["CSS Grid でテーブル的なレイアウトを構成", "各行に SVG polyline でミニ折れ線を描画", "変化量を ▲/▼ + 色で表示"]
    },
    68: {
        "desc": "折れ線グラフに注目ポイントのアノテーション（注釈）を追加。",
        "data": [("月", "X軸ラベル"), ("売上高", "折れ線の値"), ("注目ポイント", "特定のデータ点を強調")],
        "how": ["pointRadius を配列で指定し特定点のみ大きく", "pointBackgroundColor で強調点の色を変更", "chartjs-plugin-annotation で吹き出し追加も可能"]
    },
    69: {
        "desc": "同一チャートを小さく並べてカテゴリ間を比較。パターン発見に最適。",
        "data": [("カテゴリ名", "各パネルのタイトル"), ("時系列値", "各パネルの折れ線データ")],
        "how": ["CSS Grid で 4列に canvas を並べる", "各 canvas に独立した Chart を生成", "全パネルの Y 軸を統一するか個別にするか選択"]
    },
    70: {
        "desc": "テキストの出現頻度をフォントサイズで表現。事業領域の俯瞰に。",
        "data": [("キーワード", "表示テキスト"), ("出現頻度", "フォントサイズ")],
        "how": ["flex-wrap で単語を自然に折り返し配置", "font-size を頻度に比例させる", "色をランダムまたはカテゴリ別に設定"]
    },
    71: {
        "desc": "棒と折れ線を重ね合わせた複合チャート。量と件数を同時表示。",
        "data": [("四半期", "X軸ラベル"), ("売上額", "棒グラフの値"), ("受注件数", "折れ線の値")],
        "how": ["棒 dataset + type:'line' の dataset を同時に定義", "yAxisID で左右のY軸を分ける", "order プロパティで描画順を制御"]
    },
    72: {
        "desc": "複数KPIをコンパクトなパネルで一覧。ダッシュボードのサマリー部に。",
        "data": [("指標名", "パネルのタイトル"), ("値", "大きく表示"), ("変化率", "補足テキスト")],
        "how": ["CSS Grid で 3列のパネルカードを配置", "border + border-radius でカード枠", "中央揃えで数値を大きく表示"]
    },
    73: {
        "desc": "今期vs前期の指標を左右に並べて直接比較。差分を一目で把握。",
        "data": [("指標名", "各行のラベル"), ("今期の値", "左カラム"), ("前期の値", "右カラム")],
        "how": ["CSS Grid で2列カードを配置", "各カード内に指標を key-value 形式で一覧", "今期は鮮やかな色、前期はグレーで区別"]
    },
    74: {
        "desc": "指数やスコアの推移を表示。上昇/下降トレンドを面で直感的に把握。",
        "data": [("月", "X軸ラベル"), ("指数値", "折れ線+エリアの値")],
        "how": ["fill:true + 低透明度背景でエリア付き折れ線", "pointRadius:0 で点を非表示にしクリーンな表現", "borderWidth:2 で線を適度に目立たせる"]
    },
    75: {
        "desc": "自社と業界平均を横並びで比較。競争力の可視化に。",
        "data": [("評価軸", "X軸ラベル"), ("自社スコア", "メイン棒の値"), ("業界平均", "比較棒の値")],
        "how": ["2つの datasets: 自社（色付き）と業界平均（グレー）", "グループ棒として横並び表示", "差分が大きい軸にフォーカスして分析"]
    },
    76: {
        "desc": "バブル散布図が年ごとにアニメーション。再生ボタンで時間変化を可視化。",
        "data": [("年", "時間軸（アニメーションフレーム）"), ("カテゴリ名", "各バブルの識別"), ("X指標", "横軸の値"), ("Y指標", "縦軸の値"), ("規模", "バブルの大きさ")],
        "how": ["年ごとのデータ配列を用意", "SVG でバブルを描画し setInterval でフレームを切替", "再生/停止ボタンを設置してユーザー操作を可能に"]
    },
    77: {
        "desc": "折れ線グラフが2秒ごとに自動更新。ローリングウィンドウでリアルタイム監視。",
        "data": [("時刻", "X軸ラベル（自動追加）"), ("値", "Y軸の数値（ストリーム入力）")],
        "how": ["Chart.js で折れ線グラフを作成", "setInterval で新データを push し古いデータを shift", "chart.update() で再描画。animation.duration で滑らかに"]
    },
    78: {
        "desc": "セグメント別の値を単一棒グラフで色分け表示。構成比較に。",
        "data": [("セグメント名", "X軸ラベル"), ("売上額", "各棒の高さ")],
        "how": ["backgroundColor を配列で各棒に異なる色を設定", "降順にソートして視認性を高める", "凡例非表示でラベルで識別"]
    },
    79: {
        "desc": "KPIカード＋進捗バーの統合ビュー。プロジェクト全体を一画面で把握。",
        "data": [("指標名", "KPIカードのタイトル"), ("現在値", "大きく表示する数値"), ("進捗率(%)", "バーの長さ")],
        "how": ["上段：CSS Grid で KPI カードを横並び", "下段：CSS Grid で進捗バーを横並び", "各パーツの色をKPIカードと揃えて統一感を出す"]
    },
}

# ── Chart definitions ──
CHARTS = [
    (1,"棒グラフ","bar","cb-bar","Bar"),(2,"横棒グラフ","bar","cb-bar","H-Bar"),
    (3,"積み上げ棒","bar","cb-bar","Stacked"),(4,"100%積み上げ棒","bar","cb-bar","100% Stacked"),
    (5,"グループ棒","bar","cb-bar","Grouped"),(6,"発散棒グラフ","bar","cb-bar","Diverging"),
    (7,"スロープチャート","line","cb-line","Slope"),(8,"スパークライン","line","cb-line","Sparkline"),
    (9,"レーダーチャート","line","cb-line","Radar"),(10,"折れ線グラフ","line","cb-line","Line"),
    (11,"多軸折れ線","line","cb-line","Dual Axis"),(12,"ステップライン","line","cb-line","Step"),
    (13,"エリアチャート","area","cb-line","Area"),(14,"積み上げエリア","area","cb-line","Stacked Area"),
    (15,"100%積み上げエリア","area","cb-line","100% Area"),
    (16,"カレンダーヒートマップ","time","cb-map","Calendar"),(17,"ガントチャート","time","cb-special","Gantt"),
    (18,"タイムライン","time","cb-special","Timeline"),(19,"期間比較チャート","time","cb-line","Period"),
    (20,"ローソク足","time","cb-special","Candlestick"),
    (21,"ヒストグラム","stat","cb-other","Histogram"),(22,"度数ポリゴン","stat","cb-other","Freq Polygon"),
    (23,"箱ひげ図","stat","cb-other","Box Plot"),(24,"バイオリンプロット","stat","cb-other","Violin"),
    (25,"ストリップチャート","stat","cb-other","Strip"),(26,"QQプロット","stat","cb-other","QQ Plot"),
    (27,"累積分布関数","stat","cb-other","CDF"),(28,"リッジラインプロット","stat","cb-other","Ridgeline"),
    (29,"散布図（4象限）","scatter","cb-scatter","Scatter"),(30,"回帰直線付き散布図","scatter","cb-scatter","Regression"),
    (31,"バブルチャート","scatter","cb-scatter","Bubble"),(32,"相関マトリックス","scatter","cb-scatter","Corr Matrix"),
    (33,"ヒートマップ","heat","cb-map","Heatmap"),
    (34,"ネットワーク図","network","cb-special","Network"),(35,"サンキーダイアグラム","network","cb-special","Sankey"),
    (36,"コードダイアグラム","network","cb-special","Chord"),(37,"フローチャート","network","cb-special","Flow"),
    (38,"ツリーマップ","hierarchy","cb-other","Treemap"),(39,"サンバースト","hierarchy","cb-pie","Sunburst"),
    (40,"デンドログラム","hierarchy","cb-other","Dendro"),(41,"パックドバブル","hierarchy","cb-other","Packed"),
    (42,"アイシクルチャート","hierarchy","cb-other","Icicle"),(43,"ツリー図","hierarchy","cb-other","Tree"),
    (44,"ドーナツチャート","pie","cb-pie","Doughnut"),(45,"円グラフ","pie","cb-pie","Pie"),
    (46,"パレート図","special_bar","cb-bar","Pareto"),(47,"ウォーターフォール","special_bar","cb-bar","Waterfall"),
    (48,"マリメッコチャート","special_bar","cb-bar","Marimekko"),(49,"ロリポップチャート","special_bar","cb-bar","Lollipop"),
    (50,"ファネルチャート","funnel","cb-pie","Funnel"),
    (51,"コロプレスマップ","geo","cb-map","Choropleth"),(52,"バブルマップ","geo","cb-map","Bubble Map"),
    (53,"ドットマップ","geo","cb-map","Dot Map"),(54,"フローマップ","geo","cb-map","Flow Map"),
    (55,"バンプチャート","rank","cb-line","Bump"),(56,"ランクチャート","rank","cb-line","Rank"),
    (57,"平行座標プロット","rank","cb-line","Parallel"),(58,"ダンベルチャート","rank","cb-bar","Dumbbell"),
    (59,"ブレットチャート","kpi","cb-bar","Bullet"),(60,"KPIカード","kpi","cb-other","KPI Card"),
    (61,"進捗バー","kpi","cb-other","Progress"),(62,"ゲージチャート","kpi","cb-other","Gauge"),
    (63,"ワッフルチャート","kpi","cb-other","Waffle"),(64,"スピードメーター","kpi","cb-other","Speedo"),
    (65,"データテーブル","text","cb-other","Table"),(66,"スパークバー","text","cb-bar","Spark Bar"),
    (67,"ミニチャート付テーブル","text","cb-other","Mini Chart"),(68,"アノテーション付チャート","text","cb-line","Annotated"),
    (69,"スモールマルチプル","text","cb-other","Small Multi"),(70,"ワードクラウド","text","cb-other","Word Cloud"),
    (71,"複合チャート","combo","cb-bar","Combo"),(72,"ダッシュボードパネル","combo","cb-other","Panel"),
    (73,"比較ダッシュボード","combo","cb-other","Compare"),(74,"トレンドインジケーター","combo","cb-line","Trend"),
    (75,"ベンチマーク比較","combo","cb-bar","Benchmark"),
    (76,"モーションチャート","interactive","cb-special","Motion"),(77,"リアルタイムストリームチャート","interactive","cb-special","Stream"),
    (78,"セグメント比較","combo","cb-bar","Segment"),
    (79,"サマリーダッシュボード","combo","cb-other","Summary"),
]

CATEGORIES = [
    ("bar","棒グラフ系","#2563EB","棒"),("line","折れ線系","#059669","線"),
    ("area","エリア系","#10B981","面"),("time","時系列系","#0891B2","時"),
    ("stat","分布・統計系","#475569","統"),("scatter","散布図・相関系","#D97706","散"),
    ("heat","ヒートマップ系","#0891B2","熱"),("network","ネットワーク・フロー系","#E11D48","流"),
    ("hierarchy","階層・構造系","#7C3AED","階"),("pie","円・ドーナツ系","#8B5CF6","円"),
    ("special_bar","特殊棒・比較系","#2563EB","比"),("funnel","ファネル系","#7C3AED","漏"),
    ("geo","地理系","#0891B2","地"),("rank","ランキング系","#059669","順"),
    ("kpi","KPI・ゲージ系","#D97706","KPI"),("text","テキスト・テーブル系","#475569","表"),
    ("combo","複合・ダッシュボード系","#E11D48","合"),
    ("interactive","インタラクティブ系","#7C3AED","動"),
]

import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extend_guides import EXT

def build_guide_html(cid):
    g = GUIDES.get(cid)
    e = EXT.get(cid)
    if not g:
        return ''
    # Data fields
    fields_html = ''.join(
        f'<div class="gd-row"><span class="gd-field">{f}</span><span class="gd-purpose">{p}</span></div>'
        for f, p in g["data"]
    )
    # How-to steps
    steps_html = ''.join(f'<li>{s}</li>' for s in g["how"])
    # Extended: flow, tips, warnings, lib, ctype, code, config, analysis, use_cases
    flow_html = ''
    tabs_html = ''
    if e:
        fp, ft, fm = e["flow"]
        flow_html = f'''<div class="gflow">
          <div class="gflow-step"><div class="gflow-icon">📦</div><div class="gflow-phase">データ準備</div><div class="gflow-text">{fp}</div></div>
          <div class="gflow-arrow">→</div>
          <div class="gflow-step"><div class="gflow-icon">⚙️</div><div class="gflow-phase">加工・変換</div><div class="gflow-text">{ft}</div></div>
          <div class="gflow-arrow">→</div>
          <div class="gflow-step"><div class="gflow-icon">📊</div><div class="gflow-phase">描画方法</div><div class="gflow-text">{fm}</div></div>
        </div>'''
        tips_html = ''.join(f'<div class="gtip">💡 {t}</div>' for t in e.get("tips",[]))
        warn_html = ''.join(f'<div class="gwarn">⚠️ {w}</div>' for w in e.get("warn",[]))
        code_esc = e["code"].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        detail_html = f'''<div class="gdetail-grid">
          <div class="gdetail-row"><span class="gdetail-k">ライブラリ</span><span class="gdetail-v">{e["lib"]}</span></div>
          <div class="gdetail-row"><span class="gdetail-k">チャート型</span><span class="gdetail-v">{e["ctype"]}</span></div>
        </div>
        <div class="gcode"><pre><code>{code_esc}</code></pre></div>
        <div class="gconfig"><b>設定ポイント:</b> {e["config"]}</div>'''
        analysis_html = f'<div class="ganalysis"><b>分析のポイント:</b> {e["analysis"]}</div>'
        usecase_html = f'<div class="gusecase"><b>使いどころ:</b> {e["use"]}</div>'
        tabs_html = f'''<div class="gtabs" data-cid="{cid}">
          <div class="gtab-bar">
            <button class="gtab-btn active" onclick="switchTab(this,\'easy\')">👤 かんたん</button>
            <button class="gtab-btn" onclick="switchTab(this,\'detail\')">💻 くわしく</button>
          </div>
          <div class="gtab-pane gtab-easy" style="display:block">
            {flow_html}
            <div class="guide-section"><div class="gs-title">📋 作成ステップ</div><ol class="gh-steps">{steps_html}</ol></div>
            {tips_html}{warn_html}
          </div>
          <div class="gtab-pane gtab-detail" style="display:none">
            {detail_html}
          </div>
        </div>
        {analysis_html}{usecase_html}'''
    # Data template table (Excel-like)
    datatable_html = ''
    if e and e.get("datatable"):
        dt = e["datatable"]
        th_cells = ''.join(f'<th>{h}</th>' for h in dt["headers"])
        tr_rows = ''.join(
            '<tr>' + ''.join(f'<td>{v}</td>' for v in row) + '</tr>'
            for row in dt["rows"]
        )
        datatable_html = f'''<div class="guide-section">
          <div class="gs-title">📊 データフォーマット（テンプレート）</div>
          <div class="gdt-wrap">
            <table class="gdt-table">
              <thead><tr>{th_cells}</tr></thead>
              <tbody>{tr_rows}</tbody>
            </table>
            <div class="gdt-note">※ 別の指標で使用する場合は、同じ列構成でデータを収集してください</div>
          </div>
        </div>'''
    return f'''<div class="guide">
      <div class="guide-toggle" onclick="this.parentElement.classList.toggle('open')">
        <span class="guide-label">チャートの作り方ガイド</span><span class="guide-arrow">▸</span>
      </div>
      <div class="guide-content">
        <div class="guide-desc">{g["desc"]}</div>
        <div class="guide-section">
          <div class="gs-title">用意するデータ</div>
          <div class="gd-grid">{fields_html}</div>
        </div>
        {datatable_html}
        {tabs_html if tabs_html else f'<div class="guide-section"><div class="gs-title">作り方</div><ol class="gh-steps">{steps_html}</ol></div>'}
      </div>
    </div>'''


def build_chart_card(cid, cname, badge, tlabel):
    canvas_charts = {1,2,3,4,5,6,7,9,10,11,12,13,14,15,19,20,21,22,24,25,26,27,28,29,30,31,39,44,45,46,47,49,55,56,57,59,68,71,74,75,77,78}
    full_width_charts = {60,61,65,67,72,73,79}
    fw = ' full-width' if cid in full_width_charts else ''
    body_id = f'c{cid}' if cid in canvas_charts else f'div{cid}'
    inner = f'<canvas id="{body_id}"></canvas>' if cid in canvas_charts else f'<div id="{body_id}"></div>'
    guide = build_guide_html(cid)
    e = EXT.get(cid)
    sample_title = f'<div class="chart-sample-title">{e["title"]}</div>' if e and e.get("title") else ''
    return f'''
    <div class="chart-card{fw}" id="chart-{cid}">
      <div class="chart-head">
        <div class="chart-title"><span class="chart-num">#{cid}</span>{cname}</div>
        <span class="chart-type-badge {badge}">{tlabel}</span>
      </div>
      {sample_title}
      <div class="chart-body">{inner}</div>
      {guide}
    </div>'''


def main():
    parts = []
    parts.append(HEAD)
    # HERO + TOC
    toc_items = ''.join(
        f'<a class="toc-item" href="#chart-{c[0]}"><span class="toc-num">#{c[0]}</span>{c[1]}</a>'
        for c in CHARTS
    )
    parts.append(f'''
  <div class="hero">
    <h1>チャートサンプル集</h1>
    <p>全79種ビジュアライゼーション・カタログ — サンプルデータで描画</p>
    <div class="badges">
      <span class="badge">79 チャート</span>
      <span class="badge">18 カテゴリ</span>
      <span class="badge">Chart.js 4.x</span>
    </div>
  </div>
  <div class="toc">
    <h2>チャート目次（79種）</h2>
    <div class="toc-grid">{toc_items}</div>
  </div>''')

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

    parts.append(FOOTER)
    # Tab switching script (before chart rendering script)
    parts.append('''<script>
function switchTab(btn, tab) {
  const tabs = btn.closest('.gtabs');
  tabs.querySelectorAll('.gtab-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  tabs.querySelectorAll('.gtab-pane').forEach(p=>p.style.display='none');
  tabs.querySelector('.gtab-'+tab).style.display='block';
}
</script>''')
    parts.append(SCRIPT)
    parts.append('</div>\n</body>\n</html>')

    with open('chart-samples.html', 'w') as f:
        f.write('\n'.join(parts))
    print("Done: 79 charts with guides generated.")


# ===================== HTML HEAD =====================
HEAD = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>チャートサンプル集 — 全79種ビジュアライゼーション・カタログ</title>
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
.cb-special{background:#EDE9FE;color:#7C3AED}
.cb-other{background:#F8FAFC;color:#475569}
.chart-sample-title{padding:4px 16px 0;font-size:11px;font-weight:600;color:var(--text-secondary);background:var(--primary-bg);border-bottom:1px solid var(--border-light);letter-spacing:.3px}
.chart-body{padding:14px;position:relative;min-height:240px}
.chart-body canvas{max-height:260px}

/* Guide Accordion */
.guide{border-top:1px solid var(--border-light)}
.guide-toggle{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;cursor:pointer;transition:background .15s;user-select:none}
.guide-toggle:hover{background:#FAFBFD}
.guide-label{font-size:11px;font-weight:700;color:var(--primary);display:flex;align-items:center;gap:5px}
.guide-label::before{content:'📘';font-size:12px}
.guide-arrow{font-size:11px;color:var(--text-muted);transition:transform .2s}
.guide.open .guide-arrow{transform:rotate(90deg)}
.guide-content{display:none;padding:0 16px 14px}
.guide.open .guide-content{display:block}
.guide-desc{font-size:11px;color:var(--text-secondary);line-height:1.6;padding:8px 10px;background:var(--primary-bg);border-radius:6px;margin-bottom:10px;border-left:3px solid var(--primary)}
.guide-section{margin-bottom:10px}
.gs-title{font-size:10px;font-weight:800;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;display:flex;align-items:center;gap:4px}
.gs-title::before{content:'';width:6px;height:6px;border-radius:2px;background:var(--primary)}
.gd-grid{display:flex;flex-direction:column;gap:3px}
.gd-row{display:flex;align-items:center;gap:8px;padding:4px 8px;border-radius:5px;background:var(--border-light);font-size:10.5px}
.gd-field{font-family:var(--mono);font-weight:700;color:var(--text);min-width:90px;white-space:nowrap}
.gd-purpose{color:var(--text-secondary)}
.gh-steps{padding-left:18px;font-size:10.5px;color:var(--text-secondary);line-height:1.8}
.gh-steps li{padding-left:4px}
.gh-steps code{font-family:var(--mono);font-size:10px;background:var(--border-light);padding:1px 4px;border-radius:3px;color:var(--primary)}

/* Guide Tabs */
.gtabs{margin-top:8px}
.gtab-bar{display:flex;gap:0;margin-bottom:10px;border-radius:8px;overflow:hidden;border:1px solid var(--border)}
.gtab-btn{flex:1;padding:7px 12px;font-size:11px;font-weight:700;border:none;cursor:pointer;background:var(--bg);color:var(--text-secondary);transition:.15s}
.gtab-btn.active{background:var(--primary);color:#fff}
.gtab-btn:first-child{border-right:1px solid var(--border)}
.gtab-pane{padding:0}
/* Flow Diagram */
.gflow{display:flex;align-items:stretch;gap:0;margin-bottom:12px;border:1px solid var(--border);border-radius:8px;overflow:hidden;background:var(--surface)}
.gflow-step{flex:1;padding:12px 10px;text-align:center}
.gflow-icon{font-size:20px;margin-bottom:2px}
.gflow-phase{font-size:9px;font-weight:700;color:var(--text-muted);letter-spacing:.5px;margin-bottom:3px}
.gflow-text{font-size:11px;font-weight:700;color:var(--text);line-height:1.4}
.gflow-arrow{display:flex;align-items:center;font-size:16px;color:var(--text-muted);padding:0 2px}
/* Tips & Warnings */
.gtip{font-size:11px;padding:8px 12px;border-radius:6px;background:#ECFDF5;border-left:3px solid #059669;color:#065F46;margin-top:6px;line-height:1.5}
.gwarn{font-size:11px;padding:8px 12px;border-radius:6px;background:#FEF3C7;border-left:3px solid #D97706;color:#92400E;margin-top:6px;line-height:1.5}
/* Detail Tab */
.gdetail-grid{display:flex;flex-direction:column;gap:3px;margin-bottom:8px;border:1px solid var(--border);border-radius:6px;overflow:hidden}
.gdetail-row{display:flex;align-items:center;padding:6px 10px;font-size:11px;border-bottom:1px solid var(--border-light)}
.gdetail-row:last-child{border-bottom:none}
.gdetail-k{font-weight:700;color:var(--text-muted);min-width:80px}
.gdetail-v{color:var(--text)}
.gcode{margin-bottom:8px;border-radius:6px;overflow:hidden;background:#1E293B}
.gcode pre{margin:0;padding:10px 12px;font-family:var(--mono);font-size:10px;color:#E2E8F0;line-height:1.6;white-space:pre-wrap;word-break:break-all}
.gconfig{font-size:11px;padding:8px 10px;border-radius:6px;background:var(--surface);border:1px solid var(--border);color:var(--text-secondary);line-height:1.5}
.gconfig b{color:var(--text)}
/* Analysis & Use Cases */
.ganalysis{font-size:11px;padding:8px 10px;border-radius:6px;background:#F8FAFC;border-left:3px solid var(--border);color:var(--text-secondary);margin-top:8px;line-height:1.5}
.ganalysis b{color:var(--text)}
.gusecase{font-size:11px;padding:8px 10px;border-radius:6px;background:#F8FAFC;border-left:3px solid var(--primary);color:var(--text-secondary);margin-top:6px;line-height:1.5}
.gusecase b{color:var(--text)}
/* Data Template Table (Excel-like) */
.gdt-wrap{border:1px solid var(--border);border-radius:6px;overflow:hidden;background:var(--surface)}
.gdt-table{width:100%;border-collapse:collapse;font-size:10.5px}
.gdt-table thead{background:linear-gradient(135deg,#1E3A5F,#2563EB)}
.gdt-table th{padding:6px 10px;color:#fff;font-weight:700;text-align:left;font-size:10px;letter-spacing:.3px;border-right:1px solid rgba(255,255,255,.15)}
.gdt-table th:last-child{border-right:none}
.gdt-table td{padding:5px 10px;border-bottom:1px solid var(--border-light);border-right:1px solid var(--border-light);font-family:var(--mono);font-size:10px;color:var(--text)}
.gdt-table td:last-child{border-right:none}
.gdt-table tbody tr:last-child td{border-bottom:none}
.gdt-table tbody tr:nth-child(even){background:#F8FAFC}
.gdt-table tbody tr:hover{background:var(--primary-bg)}
.gdt-note{padding:5px 10px;font-size:9.5px;color:var(--text-muted);border-top:1px solid var(--border-light);background:#FAFBFD}

.footer{text-align:center;margin-top:48px;padding-top:20px;border-top:1px solid var(--border);font-size:11px;color:var(--text-muted)}
@media(max-width:900px){.chart-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="container">'''

FOOTER = '''
  <div class="footer">
    チャートサンプル集 — 全79種ビジュアライゼーション・カタログ<br>
    79 チャート | 18 カテゴリ | Generated: 2026-03-11
  </div>'''

# Read the script from previous version
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generate_charts.py')) as f:
    content = f.read()
# Extract SCRIPT block — the raw string already contains <script>...</script>
import re
m = re.search(r"^SCRIPT = r'''(.+?)'''$", content, re.DOTALL | re.MULTILINE)
SCRIPT = m.group(1) if m else '<script></script>'

if __name__ == '__main__':
    main()
