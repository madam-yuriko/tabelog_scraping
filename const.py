import tkinter as tk

YEAR = 2024

INPUT_FILE_NAME = f'data_base_all_{YEAR}_processed.csv'

VIEW_ROW_CNT = 60
MAX_ROW_CNT = 500

SELECTOR_DIC = {
    'ID': None,
    'URL': None,
    '取得日時': None,
    '都道府県': 0,
    '所在地': 1,
    '施設名': 3,
    '最寄り駅': ['span', 'linktree__parent-target-text'],
    'ステータス': ['#rstdtl-head > div.rstdtl-header.unofficial > section > div.rst-status-badge-red > a', '#rstdtl-head > div.rstdtl-header > section > div.rst-status-badge-red > a'],
    '店名': '#rstdtl-head > div.rstdtl-header > section > div.rdheader-title-data > div.rdheader-rstname-wrap > div > h2 > span',
    '店名(補足)': '#rstdtl-head > div.rstdtl-header > section > div.rdheader-title-data > div.rdheader-rstname-wrap > div > span',
    '食べログアワード': None,
    '百名店': None,
    '点数': ['span', 'rdheader-rating__score-val-dtl'],
    '口コミ数': ['span', 'rdheader-rating__review-target'],
    '保存件数': ['span', 'rdheader-rating__hozon-target'],
    '予算(夜)': 0,
    '予算(昼)': 1,
    'ジャンル1': '#rstdtl-head > div.rstdtl-header > section > div.rdheader-info-data > div > div > div:nth-child(1) > dl:nth-child(3) > dd > div:nth-child(1) > div.linktree__parent > a > span',
    'ジャンル2': '#rstdtl-head > div.rstdtl-header > section > div.rdheader-info-data > div > div > div:nth-child(1) > dl:nth-child(3) > dd > div:nth-child(2) > div.linktree__parent > a > span',
    'ジャンル3': '#rstdtl-head > div.rstdtl-header > section > div.rdheader-info-data > div > div > div:nth-child(1) > dl:nth-child(3) > dd > div:nth-child(3) > div.linktree__parent > a > span',
    '説明': ['h3', 'pr-comment-title'],
    '説明詳細': ['span', 'pr-comment__first'],
    '予約可否': ['p', 'rstinfo-table__reserve-status'],
    'オープン日': ['p', 'rstinfo-opened-date'],
    '席数': ['table', 'c-table c-table--form rstinfo-table__table'],
    '備考': ['p', 'rstinfo-remarks-item'],
    'ホームページ': '#rst-data-head > table:nth-child(9) > tbody > tr:nth-child(5) > td > p > a > span',
    '公式アカウント': '#rst-data-head > table:nth-child(9) > tbody > tr:nth-child(6) > td > div > a > span'
}

# DataFrameレイアウト
DATA_FLAME_LAYOUT = {
    'No': [40, tk.E], '全国順位': [60, tk.E], '順位変動_str': [70, tk.E], '都道府県': [80, tk.W], '店名': [300, tk.W], 'ステータス': [80, tk.W], '点数_str': [60, tk.E], '点数(昨年)_str': [60, tk.E], '点数(一昨年)_str': [60, tk.E], 
    '口コミ数': [70, tk.E], '口コミ数(増減)_str': [70, tk.E], '口コミ数(増減2)_str': [70, tk.E], '保存件数': [90, tk.E], '予算(夜)': [150, tk.E], '予算(昼)': [150, tk.E], 
    '食べログアワード': [200, tk.W], '百名店': [220, tk.W], 'ジャンル1': [130, tk.W], 'ジャンル2': [130, tk.W], 'ジャンル3': [130, tk.W], 
    '所在地': [200, tk.W], '施設名': [240, tk.W], '最寄り駅': [100, tk.W], '席数': [70, tk.E], 'オープン日': [130, tk.E], '説明詳細': [600, tk.W]
}

# DF全カラムヘッダー
MERGE_COL_NAMES = [
    'ID', 'URL', '取得日時', '都道府県', '所在地', '施設名', '最寄り駅', 'ステータス', '店名', '食べログアワード',
    '百名店', '点数', '口コミ数', '保存件数', '予算(夜)', '予算(昼)', 'ジャンル1', 'ジャンル2', 'ジャンル3', '説明',
    '説明詳細', '予約可否', 'オープン日', '席数', '備考', 'ホームページ', 'アカウント', '予算', 'ステータス(昨年)', '点数(昨年)',
    '口コミ数(昨年)', '保存件数(昨年)', '全国順位(昨年)', 'indicator_1', '点数(一昨年)', '口コミ数(一昨年)', 'indicator_2'
]

# 商業施設一覧
SHISETSU_DICT = {
    '': {},
    '北海道 札幌ステラプレイス': {'都道府県': '北海道', '場所1': '中央区北五|中央区北5', '場所2': 'ステラプレイス', '場所3': ''},
    '北海道 PASEO': {'都道府県': '北海道', '場所1': '北区北六|北区北6', '場所2': 'パセオ|PASEO', '場所3': ''},
    '北海道 札幌エスタ': {'都道府県': '北海道', '場所1': '中央区北五|中央区北5', '場所2': 'エスタ|ESTA', '場所3': ''},
    '北海道 アピア': {'都道府県': '北海道', '場所1': '中央区北五|中央区北5', '場所2': 'アピア|APIA', '場所3': ''},
    '北海道 大丸札幌店': {'都道府県': '北海道', '場所1': '大丸札幌', '場所2': '8F', '場所3': ''},
    '北海道 サッポロファクトリー': {'都道府県': '北海道', '場所1': '北2条東4|サッポロファクトリー', '場所2': '', '場所3': ''},
    '北海道 札幌PARCO': {'都道府県': '北海道', '場所1': '南1条西3-3|南1条西3丁目3', '場所2': '', '場所3': ''},
    '北海道 日本生命 noasis': {'都道府県': '北海道', '場所1': '北3条西4-1-1|日本生命札幌ビル', '場所2': '', '場所3': ''},
    '北海道 赤れんがテラス': {'都道府県': '北海道', '場所1': '北2条西4-1|赤れんがテラス|赤レンガテラス', '場所2': '', '場所3': ''},
    '北海道 sitatte sapporo': {'都道府県': '北海道', '場所1': '札幌', '場所2': 'sitatte|フコク生命', '場所3': ''},
    '北海道 大通BISSE': {'都道府県': '北海道', '場所1': '中央区大通西3', '場所2': '', '場所3': ''},
    '北海道 miredo': {'都道府県': '北海道', '場所1': '札幌', '場所2': '大同生命', '場所3': ''},
    '北海道 狸COMICHI': {'都道府県': '北海道', '場所1': '中央区南2条西2-5|狸COMICH', '場所2': '', '場所3': ''},
    '北海道 moyuk SAPPORO': {'都道府県': '北海道', '場所1': '中央区南2条西3-20|モユク|moyuk', '場所2': '', '場所3': ''},
    '北海道 cocono susukino': {'都道府県': '北海道', '場所1': '中央区南4条西4-1-1|ココノ|cocono', '場所2': '', '場所3': ''},
    '北海道 新さっぽろ アークシティ': {'都道府県': '北海道', '場所1': '厚別区厚別中央', '場所2': 'サンピアザ|カテプリ|イオン|DUO', '場所3': ''},
    '北海道 BiVi新さっぽろ': {'都道府県': '北海道', '場所1': '厚別区厚別中央1条6-3-3|BiVi新さっぽろ|BiVi新札幌', '場所2': '', '場所3': ''},
    '北海道 新千歳空港': {'都道府県': '北海道', '場所1': '新千歳空港', '場所2': '', '場所3': ''},
    '宮城県 仙台駅': {'都道府県': '宮城県', '場所1': '仙台市青葉区中央1-1-1', '場所2': '', '場所3': ''},
    '千代田区 東京駅': {'都道府県': '東京都', '場所1': '丸の内1-9-1|丸ノ内1-9-1', '場所2': '', '場所3': ''},
    '千代田区 東京交通会館': {'都道府県': '東京都', '場所1': '有楽町2-10-1|交通会館', '場所2': '', '場所3': ''},
    '千代田区 丸の内ビルディング': {'都道府県': '東京都', '場所1': '千代田区丸の内2-4-1|^丸の内ビルディング', '場所2': '', '場所3': ''},
    '千代田区 ヨドバシAkiba': {'都道府県': '東京都', '場所1': '神田花岡町1-1$|ヨドバシAkiba', '場所2': '', '場所3': ''},
    '千代田区 新丸の内ビルディング': {'都道府県': '東京都', '場所1': '千代田区丸の内1-5-1$|新丸の内ビルディング', '場所2': '', '場所3': ''},
    '千代田区 有楽町イトシア': {'都道府県': '東京都', '場所1': '有楽町2-7-1', '場所2': '', '場所3': ''},
    '千代田区 丸の内ブリックスクエア': {'都道府県': '東京都', '場所1': '丸の内2-6-1|丸の内ブリックスクエア', '場所2': '', '場所3': ''},
    '千代田区 KITTE JPタワー': {'都道府県': '東京都', '場所1': '丸の内2-7-2', '場所2': '', '場所3': ''},
    '千代田区 ガーデンテラス紀尾井町': {'都道府県': '東京都', '場所1': '紀尾井町1-2|紀尾井町1-3|ガーデンテラス紀尾井町', '場所2': '', '場所3': ''},
    '千代田区 東京ミッドタウン日比谷': {'都道府県': '東京都', '場所1': '有楽町1-1-2|有楽町1-1-3|有楽町1-1-4', '場所2': '', '場所3': ''},
    '千代田区 日比谷OKUROJI': {'都道府県': '東京都', '場所1': '内幸町1-7-1$', '場所2': '', '場所3': ''},
    '千代田区 大手町 TOKYO TORCH 常盤橋タワー': {'都道府県': '東京都', '場所1': '大手町2-6-4', '場所2': '', '場所3': ''},
    '中央区 八重洲地下街': {'都道府県': '東京都', '場所1': '八重洲地下街', '場所2': '', '場所3': ''},
    '中央区 晴海アイランドトリトンスクエア': {'都道府県': '東京都', '場所1': '晴海トリトン|晴海アイランド', '場所2': '', '場所3': ''},
    '中央区 コレド日本橋': {'都道府県': '東京都', '場所1': '日本橋1-4-1', '場所2': '', '場所3': ''},
    '中央区 コレド室町1･2･3': {'都道府県': '東京都', '場所1': '室町2-2-1|室町2-3-1|室町1-5-5', '場所2': '', '場所3': ''},
    '中央区 コレド室町テラス': {'都道府県': '東京都', '場所1': '室町3-2-1', '場所2': '', '場所3': ''},
    '中央区 東急プラザ銀座': {'都道府県': '東京都', '場所1': '銀座5-2-1', '場所2': '', '場所3': ''},
    '中央区 京橋エドグラン': {'都道府県': '東京都', '場所1': '京橋2-2-1|京橋エドグラン', '場所2': '', '場所3': ''},
    '中央区 GINZA SIX': {'都道府県': '東京都', '場所1': '銀座6-10-1', '場所2': '', '場所3': ''},
    '中央区 東京ミッドタウン八重洲': {'都道府県': '東京都', '場所1': '八重洲2-2-1', '場所2': '', '場所3': ''},
    '港区 アトレ品川': {'都道府県': '東京都', '場所1': '港区港南2-18-1|アトレ品川', '場所2': '', '場所3': ''},
    '港区 ニュー新橋ビル': {'都道府県': '東京都', '場所1': '新橋2-16-1|ニュー新橋ビル', '場所2': '', '場所3': ''},
    '港区 アクアシティお台場': {'都道府県': '東京都', '場所1': '台場1-7-1', '場所2': '', '場所3': ''},
    '港区 六本木ヒルズ': {'都道府県': '東京都', '場所1': '六本木ヒルズ', '場所2': '', '場所3': ''},
    '港区 東京ミッドタウン': {'都道府県': '東京都', '場所1': '赤坂9-7-1|赤坂9-7-2|赤坂9-7-3|赤坂9-7-4', '場所2': '', '場所3': ''},
    '港区 msb田町': {'都道府県': '東京都', '場所1': '芝浦3-1-21|芝浦3-1-1|msb Tamachi', '場所2': '', '場所3': ''},
    '港区 虎ノ門ヒルズビジネスタワー': {'都道府県': '東京都', '場所1': '虎ノ門1-17-1|虎ノ門ヒルズビジネスタワー', '場所2': '', '場所3': ''},
    '港区 虎ノ門ヒルズ ステーションタワー': {'都道府県': '東京都', '場所1': '虎ノ門2-6-1|虎ノ門2-6-2|虎ノ門2-6-3|虎ノ門2-6-4|虎ノ門2-6-5|虎ノ門ヒルズステーションタワー', '場所2': '', '場所3': ''},
    '港区 麻布台ヒルズ': {'都道府県': '東京都', '場所1': '麻布台a-6-6-14|麻布台1-3-1|麻布台ヒルズ', '場所2': '', '場所3': ''},
    '新宿区 ルミネエスト': {'都道府県': '東京都', '場所1': '新宿3-38-1', '場所2': '', '場所3': ''},
    '新宿区 ルミネ1': {'都道府県': '東京都', '場所1': '新宿1-1-5', '場所2': '', '場所3': ''},
    '新宿区 ルミネ2': {'都道府県': '東京都', '場所1': '新宿3-38-2', '場所2': '', '場所3': ''},
    '新宿区 サブナード': {'都道府県': '東京都', '場所1': 'サブナード', '場所2': '', '場所3': ''},
    '新宿区 オペラシティ': {'都道府県': '東京都', '場所1': '西新宿3-20-2|オペラシティ', '場所2': '', '場所3': ''},
    '新宿区 NEWoMan新宿': {'都道府県': '東京都', '場所1': '渋谷区千駄ヶ谷5-24-55', '場所2': '', '場所3': ''},
    '新宿区 コモレ四谷': {'都道府県': '東京都', '場所1': '新宿区四谷1-6-1', '場所2': '', '場所3': ''},
    '新宿区 歌舞伎町タワー': {'都道府県': '東京都', '場所1': '新宿区歌舞伎町1-29-1|東急歌舞伎町タワー', '場所2': '', '場所3': ''},
    '渋谷区 恵比寿ガーデンプレイス': {'都道府県': '東京都', '場所1': '恵比寿4-20-1|恵比寿4-20-2|恵比寿4-20-3|恵比寿4-20-4|恵比寿4-20-5|恵比寿4-20-6|恵比寿4-20-7|三田1-13-1|三田1-13-4|恵比寿ガーデンプレイス', '場所2': '', '場所3': ''},
    '渋谷区 新宿高島屋タイムズスクエア': {'都道府県': '東京都', '場所1': '渋谷区千駄ヶ谷5-24-2', '場所2': '', '場所3': ''},
    '渋谷区 アトレ恵比寿': {'都道府県': '東京都', '場所1': '恵比寿南1-5-5|恵比寿南1-6-1|アトレ恵比寿', '場所2': '', '場所3': ''},
    '渋谷区 渋谷ヒカリエ': {'都道府県': '東京都', '場所1': '渋谷2-21-1|渋谷ヒカリエ', '場所2': '', '場所3': ''},
    '渋谷区 渋谷ストリーム': {'都道府県': '東京都', '場所1': '渋谷3-21-3|渋谷ストリーム', '場所2': '', '場所3': ''},
    '渋谷区 渋谷スクランブルスクエア': {'都道府県': '東京都', '場所1': '渋谷2-24-12|渋谷スクランブルスクエア', '場所2': '', '場所3': ''},
    '渋谷区 渋谷パルコ': {'都道府県': '東京都', '場所1': '宇田川町15-1|渋谷PARCO|渋谷パルコ', '場所2': '', '場所3': ''},
    '渋谷区 渋谷フクラス': {'都道府県': '東京都', '場所1': '道玄坂1-2-3|東急プラザ渋谷|渋谷フクラス', '場所2': '', '場所3': ''},
    '渋谷区 ミヤシタパーク': {'都道府県': '東京都', '場所1': '神宮前', '場所2': '6-20-10|六丁目20-10|MIYASHITA PARK', '場所3': ''},
    '渋谷区 WITH HARAJUKU': {'都道府県': '東京都', '場所1': '神宮前1-14-30|WITH HARAJUKU|ウィズ原宿', '場所2': '', '場所3': ''},
    '渋谷区 神宮前COMICHI': {'都道府県': '東京都', '場所1': '神宮前1-23-26|JUNGUMAE COMICHI', '場所2': '', '場所3': ''},
    '豊島区 池袋駅(池袋パルコ)': {'都道府県': '東京都', '場所1': '南池袋1-28-2|池袋パルコ', '場所2': '', '場所3': ''},
    '豊島区 東武百貨店 スパイス': {'都道府県': '東京都', '場所1': '池袋', '場所2': '東武百貨店', '場所3': '11F|12F|13F|14F|15F'},
    '豊島区 西武池袋本店': {'都道府県': '東京都', '場所1': '西武池袋本店', '場所2': '8F|9F', '場所3': ''},
    '豊島区 サンシャインシティ': {'都道府県': '東京都', '場所1': '東池袋3-1-1|東池袋3-1-2|東池袋3-1-3|東池袋3-1-5|サンシャインシティ|サンシャイン60|サンシャインアルパ', '場所2': '', '場所3': ''},
    '文京区 東京ドームシティ ラクーア': {'都道府県': '東京都', '場所1': '春日1-1-1', '場所2': '', '場所3': ''},
    '台東区 浅草EKIMISE': {'都道府県': '東京都', '場所1': '花川戸1-4-1|EKIMISE', '場所2': '', '場所3': ''},
    '台東区 上野マルイ': {'都道府県': '東京都', '場所1': '上野6-15-1|上野マルイ', '場所2': '', '場所3': ''},
    '台東区 上野パルコヤ': {'都道府県': '東京都', '場所1': '上野3-24-6', '場所2': '', '場所3': ''},
    '墨田区 錦糸町テルミナ1･2･3': {'都道府県': '東京都', '場所1': '江東橋3-14-5|錦糸1-2-47|江東橋2-19-1', '場所2': '', '場所3': ''},
    '墨田区 オリナス錦糸町': {'都道府県': '東京都', '場所1': '太平4-1-1|太平4-1-2|太平4-1-3|太平4-1-5', '場所2': '', '場所3': ''},
    '墨田区 錦糸町アルカキット': {'都道府県': '東京都', '場所1': '錦糸2-2-1', '場所2': '', '場所3': ''},
    '墨田区 錦糸町パルコ': {'都道府県': '東京都', '場所1': '江東橋4-27-14', '場所2': '', '場所3': ''},
    '墨田区 錦糸町マルイ': {'都道府県': '東京都', '場所1': '墨田区江東橋3-9-10', '場所2': '', '場所3': ''},
    '墨田区 東京ソラマチ': {'都道府県': '東京都', '場所1': '押上1-1-2|ソラマチ', '場所2': '', '場所3': ''},
    '江東区 ららぽーと豊洲': {'都道府県': '東京都', '場所1': '豊洲2-4-9|豊洲2-2-1|ららぽーと豊洲', '場所2': '', '場所3': ''},
    '江東区 南砂町SUNAMO': {'都道府県': '東京都', '場所1': '新砂3-4-31|SUNAMO', '場所2': '', '場所3': ''},
    '江東区 アリオ北砂': {'都道府県': '東京都', '場所1': '北砂2-17-1|アリオ北砂', '場所2': '', '場所3': ''},
    '江東区 ダイバーシティ東京プラザ': {'都道府県': '東京都', '場所1': '青梅1-1-10|ダイバーシティ', '場所2': '', '場所3': ''},
    '江東区 有明ガーデン': {'都道府県': '東京都', '場所1': '有明2-1-8|有明ガーデン', '場所2': '', '場所3': ''},
    '江東区 カメイドクロック': {'都道府県': '東京都', '場所1': '亀戸6-31-6|カメイドクロック', '場所2': '', '場所3': ''},
    '品川区 大崎ニューシティ': {'都道府県': '東京都', '場所1': '大崎1-6-4|大崎1-6-5|大崎ニューシティ', '場所2': '', '場所3': ''},
    '品川区 ゲートシティ大崎': {'都道府県': '東京都', '場所1': '大崎1-11-1|大崎1-11-2|大崎1-11-5|大崎1-11-6|ゲートシティ大崎', '場所2': '', '場所3': ''},
    '大田区 グランデュオ蒲田': {'都道府県': '東京都', '場所1': '蒲田5-13-1|西蒲田7-68-1|グランデュオ蒲田', '場所2': '', '場所3': ''},
    '大田区 羽田空港第1旅客ターミナル': {'都道府県': '東京都', '場所1': '羽田空港3-3-2|羽田空港第1', '場所2': '', '場所3': ''},
    '大田区 羽田空港第2旅客ターミナル': {'都道府県': '東京都', '場所1': '羽田空港3-4-2|羽田空港第2', '場所2': '', '場所3': ''},
    '大田区 羽田空港第3旅客ターミナル': {'都道府県': '東京都', '場所1': '羽田空港2-6-5|羽田空港第3', '場所2': '', '場所3': ''},
    '大田区 羽田エアポートガーデン': {'都道府県': '東京都', '場所1': '羽田空港2-7-1|エアポートガーデン', '場所2': '', '場所3': ''},
    '世田谷区 玉川高島屋S・C': {'都道府県': '東京都', '場所1': '玉川3-17-1|玉川高島屋|玉川タカシマヤ', '場所2': '', '場所3': ''},
    '世田谷区 二子玉川ライズ': {'都道府県': '東京都', '場所1': '玉川1-14-1|玉川2-21-1|玉川2-23-1|二子玉川ライズ', '場所2': '', '場所3': ''},
    '中野区 中野ブロードウェイ': {'都道府県': '東京都', '場所1': '中野5-52-15|中野ブロードウェイ', '場所2': '', '場所3': ''},
    '杉並区 ビーンズ阿佐ヶ谷': {'都道府県': '東京都', '場所1': '阿佐谷南2-42-1阿佐谷南3-58-1|ビーンズ阿佐ヶ谷', '場所2': '', '場所3': ''},
    '荒川区 LaLaテラス南千住': {'都道府県': '東京都', '場所1': '南千住4-7-2', '場所2': '', '場所3': ''},
    '練馬区 光が丘IMA': {'都道府県': '東京都', '場所1': '光が丘5-1-1|光が丘3-9-2|光が丘2-10-2|光が丘IMA', '場所2': '', '場所3': ''},
    '足立区 ルミネ北千住': {'都道府県': '東京都', '場所1': '千住旭町42-2|ルミネ北千住', '場所2': '', '場所3': ''},
    '足立区 アリオ西新井': {'都道府県': '東京都', '場所1': '西新井栄町1-20-1|アリオ西新井', '場所2': '', '場所3': ''},
    '足立区 ポンテポルタ千住': {'都道府県': '東京都', '場所1': '足立区千住橋戸町1-13', '場所2': '', '場所3': ''},
    '足立区 千住ミルディス': {'都道府県': '東京都', '場所1': '千住3-92|千住ミルディス|北千住マルイ', '場所2': '', '場所3': ''},
    '葛飾区 ユアエルム青戸': {'都道府県': '東京都', '場所1': '青戸3-36-1|ユアエルム青戸', '場所2': '', '場所3': ''},
    '葛飾区 リリオ亀有': {'都道府県': '東京都', '場所1': '亀有3-26-1|亀有3-26-2|亀有3-29-1', '場所2': '', '場所3': ''},
    '葛飾区 アリオ亀有': {'都道府県': '東京都', '場所1': '亀有3-49-3|アリオ亀有', '場所2': '', '場所3': ''},
    '葛飾区 ヴィナシス金町ブライトコート&ベルトーレ金町': {'都道府県': '東京都', '場所1': '金町6-2-1|金町6丁目2-1|金町6-2-7|金町6-5-1|金町6丁目5-1', '場所2': '', '場所3': ''},
    '江戸川区 アリオ葛西': {'都道府県': '東京都', '場所1': '東葛西9-3-3|アリオ葛西', '場所2': '', '場所3': ''},
    '町田市 南町田グランベリーパーク': {'都道府県': '東京都', '場所1': '鶴間3-3-1|鶴間3-4-1', '場所2': '', '場所3': ''},
    '神奈川県 横浜ランドマークタワー': {'都道府県': '神奈川県', '場所1': 'みなとみらい2-2-1|ランドマークタワー|ランドマークプラザ', '場所2': '', '場所3': ''},
    '神奈川県 MARK IS みなとみらい': {'都道府県': '神奈川県', '場所1': 'みなとみらい3-5-1|マークイズ|MARK IS', '場所2': '', '場所3': ''},
    '埼玉県 コクーンシティ': {'都道府県': '埼玉県', '場所1': '吉敷町4-267-2|吉敷町4-267-11|吉敷町4-263-1|コクーン', '場所2': '', '場所3': ''},
    '埼玉県 イオンレイクタウン mori': {'都道府県': '埼玉県', '場所1': '越谷レイクタウン3-1-1|mori', '場所2': '', '場所3': ''},
    '埼玉県 イオンレイクタウン kaze': {'都道府県': '埼玉県', '場所1': '越谷レイクタウン4-2-2|kaze', '場所2': '', '場所3': ''},
    '埼玉県 イオンレイクタウン アウトレット': {'都道府県': '埼玉県', '場所1': '越谷レイクタウン4-1-1|レイクタウンアウトレット', '場所2': '', '場所3': ''},
    '埼玉県 ららぽーと新三郷': {'都道府県': '埼玉県', '場所1': '三郷市新三郷ららシティ3-1-1', '場所2': '', '場所3': ''},
    '千葉県 東京ディズニーランド': {'都道府県': '千葉県', '場所1': 'ディズニーランド', '場所2': '', '場所3': ''},
    '千葉県 東京ディズニーシー': {'都道府県': '千葉県', '場所1': 'ディズニーシー', '場所2': '', '場所3': ''},
    '千葉県 アトレ松戸': {'都道府県': '千葉県', '場所1': '松戸市松戸1181|アトレ松戸', '場所2': '', '場所3': ''},
    '千葉県 プラーレ松戸': {'都道府県': '千葉県', '場所1': '松戸1149|プラーレ松戸', '場所2': '', '場所3': ''},
    '千葉県 キテミテマツド': {'都道府県': '千葉県', '場所1': '松戸1307-1|キテミテマツド', '場所2': '', '場所3': ''},
    '千葉県 テラスモール松戸': {'都道府県': '千葉県', '場所1': '八ヶ崎2-8-1|八ケ崎2-8-1|テラスモール松戸', '場所2': '', '場所3': ''},
    '千葉県 イオンモール幕張新都心': {'都道府県': '千葉県', '場所1': 'イオンモール幕張新都心', '場所2': '', '場所3': ''},
    '千葉県 ららぽーと柏の葉': {'都道府県': '千葉県', '場所1': '柏市若柴175', '場所2': '', '場所3': ''},
    '千葉県 流山おおたかの森S･C': {'都道府県': '千葉県', '場所1': '流山市西初石6-185-2|流山市おおたかの森南1-5-1|流山市おおたかの森南1-2-1|おおたかの森SC|おおたかの森S･C', '場所2': '', '場所3': ''},
    '熊本県 サクラマチクマモト': {'都道府県': '熊本県', '場所1': '桜町3-10', '場所2': '', '場所3': ''},
    '愛知県 セントラルタワーズ': {'都道府県': '愛知県', '場所1': '名駅1-1-4', '場所2': 'タワーズ', '場所3': ''},
    '愛知県 JRゲートタワー': {'都道府県': '愛知県', '場所1': 'ゲートタワー', '場所2': '', '場所3': ''},
    '愛知県 JPタワー': {'都道府県': '愛知県', '場所1': '名駅1-1-1', '場所2': '', '場所3': ''},
    '福岡県 博多駅': {'都道府県': '福岡県', '場所1': '博多駅中央街1-1', '場所2': '', '場所3': ''},
}

THEME_DICT = {
    '': {},
    '純すみ系': {'店名': 'すみれ 中の島本店|すみれ 札幌すすきの店|すみれ 札幌里塚店|すみれ 横浜店|さっぽろ純連 札幌店|さっぽろ純連 仙台店|さっぽろ純連 北31条店|麺屋 彩未|^大島$|八乃木|^ラーメン 郷$|三ん寅|あさひ町内会|麺屋つくし|らぁめん 千寿|狼スープ|^らーめん庵|らーめん 空 本店|らーめん空 新千歳空港店', 'ジャンル': 'ラーメン'},
    '北海道系他県進出': {'店名': """175°DENO担担麺 GINZa|175°DENO担担麺 TOKYO|松尾ジンギスカン 銀座店|松尾ジンギスカン 赤坂店|旭川成吉思汗 大黒屋 吉祥寺店|^大島$|三ん寅|あさひ町内会|らーめん 福籠|さっぽろ羅偉伝|
    すみれ 横浜店|ラーメン 郷|さっぽろ純連 仙台店|麺屋つくし|えびそば 一幻 新宿店|えびそば 一幻 八重洲地下街店|ニッポン ラーメン 凛 トウキョウ|博多川端どさんこ|根室花まる KITTE丸の内店|
    回転寿司 根室花まる 銀座店|回転寿司 根室花まる メトロエム後楽園店|根室花まる エキュートエディション新橋店|回転寿司 根室花まる 銀座店|立食い寿司 根室花まる 丸の内オアゾ店|
    立食い寿司 根室花まる 東京ミッドタウン八重洲店|回転寿し トリトン 東京ソラマチ店|回転寿し トリトン 池袋東武店|海鮮寿し トリトン アトレ品川店|札幌魚河岸 五十七番寿し 東京駅店|なごやか亭 草津木川店|北海道スープカレー Suage 渋谷店|北海道スープカレー Suage 渋谷店|
    北海道スープカレー Suage 池袋店|北海道スープカレーSuage 吉祥寺店|Rojiura Curry SAMURAI. 下北沢店|イエローカンパニー 恵比寿本店|イエローカンパニー 新宿店|The Yellow Company TOKYO|マジックスパイス 東京下北沢店|札幌ドミニカ 銀座店|東京ドミニカ|札幌スープカレーJACK 新町店|
    Rojiura Curry SAMURAI． 神楽坂店|CHUTTA！ 新潟駅南店|タイガーカレー 新潟店|スープカリー ばぐばぐ 仙台店|KINO_ """},
}

# 地域一覧
AREA_DICT = {
    '': '北海道|青森県|岩手県|宮城県|秋田県|山形県|福島県|茨城県|栃木県|群馬県|埼玉県|千葉県|東京都|神奈川県|新潟県|山梨県|長野県|岐阜県|静岡県|愛知県|富山県|石川県|福井県|三重県|滋賀県|京都府|大阪府|兵庫県|奈良県|和歌山県|鳥取県|島根県|岡山県|広島県|山口県|徳島県|香川県|愛媛県|高知県|福岡県|佐賀県|長崎県|熊本県|大分県|宮崎県|鹿児島県|沖縄県',
    '東日本': '北海道|青森県|岩手県|宮城県|秋田県|山形県|福島県|茨城県|栃木県|群馬県|埼玉県|千葉県|東京都|神奈川県|新潟県|山梨県|長野県|岐阜県|静岡県|愛知県', 
    '東日本(東京除く)': '北海道|青森県|岩手県|宮城県|秋田県|山形県|福島県|茨城県|栃木県|群馬県|埼玉県|千葉県|神奈川県|新潟県|山梨県|長野県|岐阜県|静岡県|愛知県', 
    '西日本': '富山県|石川県|福井県|三重県|滋賀県|京都府|大阪府|兵庫県|奈良県|和歌山県|鳥取県|島根県|岡山県|広島県|山口県|徳島県|香川県|愛媛県|高知県|福岡県|佐賀県|長崎県|熊本県|大分県|宮崎県|鹿児島県|沖縄県', 
    '北海道・東北': '北海道|青森県|岩手県|宮城県|秋田県|山形県|福島県', 
    '東北': '青森県|岩手県|宮城県|秋田県|山形県|福島県', 
    '関東': '茨城県|栃木県|群馬県|埼玉県|千葉県|東京都|神奈川県', 
    '中部': '山梨県|長野県|岐阜県|静岡県|愛知県', 
    '北陸': '新潟県|富山県|石川県|福井県',
    '近畿': '三重県|滋賀県|京都府|大阪府|兵庫県|奈良県|和歌山県', 
    '中国・四国': '鳥取県|島根県|岡山県|広島県|山口県|徳島県|香川県|愛媛県|高知県', 
    '中国': '鳥取県|島根県|岡山県|広島県|山口県', 
    '四国': '徳島県|香川県|愛媛県|高知県', 
    '九州・沖縄': '福岡県|佐賀県|長崎県|熊本県|大分県|宮崎県|鹿児島県|沖縄県'
}

# 都道府県一覧
TODOFUKEN_LIST = [
    '', '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県',
    '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県',
    '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
]

# 都道府県コード
TODOFUKEN_URL_LIST = {
    '01': 'hokkaido', '02': 'aomori', '03': 'iwate', '04': 'miyagi', '05': 'akita', '06': 'yamagata', '07': 'fukushima', '08': 'ibaraki', '09': 'tochigi', '10': 'gunma',
    '11': 'saitama', '12': 'chiba', '13': 'tokyo', '14': 'kanagawa', '15': 'niigata', '16': 'toyama', '17': 'ishikawa', '18': 'fukui', '19': 'yamanashi', '20': 'nagano',
    '21': 'gifu', '22': 'shizuoka', '23': 'aichi', '24': 'mie', '25': 'shiga', '26': 'kyoto', '27': 'osaka', '28': 'hyogo', '29': 'nara', '30': 'wakayama',
    '31': 'tottori', '32': 'shimane', '33': 'okayama', '34': 'hiroshima', '35': 'yamaguchi', '36': 'tokushima', '37': 'kagawa', '38': 'ehime', '39': 'kochi', '40': 'fukuoka',
    '41': 'saga', '42': 'nagasaki', '43': 'kumamoto', '44': 'oita', '45': 'miyazaki', '46': 'kagoshima', '47': 'okinawa',
}

# 点数帯リスト
SCORE_LIST = [
    '', '3.00未満', '3.00以上', '3.10以上', '3.20以上', '3.30以上', '3.40以上', '3.50以上', '3.60以上', '3.70以上', '3.80以上', '3.90以上',
    '4.00以上', '4.10以上', '4.20以上', '4.30以上', '4.40以上', '4.50以上', '4.60以上', '4.70以上',
]

# ジャンル一覧
GENRE_LIST = None

# 予算
YOSAN_LIST = {
    '-': 0, '～￥999': 1, '￥1000～￥1999': 2, '￥2000～￥2999': 3, '￥3000～￥3999': 4, '￥4000～￥4999': 5, '￥5000～￥5999': 6, '￥6000～￥7999': 7, '￥8000～￥9999': 8, 
    '￥10000～￥14999': 9, '￥15000～￥19999': 10, '￥20000～￥29999': 11, '￥30000～￥39999': 12, '￥40000～￥49999': 13, '￥50000～￥59999': 14, '￥60000～￥79999': 15, '￥80000～￥99999': 15, '￥100000～': 16, 
}

YOSAN_LIST_L = ['', '￥1000', '￥2000', '￥3000', '￥4000', '￥5000', '￥6000', '￥8000', '￥10000', '￥15000', '￥20000', '￥30000', '￥40000', '￥50000', '￥60000', '￥80000', '￥100000']
YOSAN_LIST_H = ['￥999', '￥1999', '￥2999', '￥3999', '￥4999', '￥5999', '￥7999', '￥9999', '￥14999', '￥19999', '￥29999', '￥39999', '￥49999', '￥59999', '￥79999', '￥99999', '']

# 営業状況
BUSINESS_STATUS_LIST = ['標準', '営業中のみ', '新規オープンのみ', '昨年閉店のみ', '過去店全表示']

# ソート
SORT_TYPE_LIST = ['点数順', '点数増減順', '口コミ数順', '口コミ数増減順', '保存件数']

# 食べログアワード
AWARD_LIST = ['', f'{YEAR} Gold', f'{YEAR} Silver', f'{YEAR} Bronze', 'Gold', 'Silver', 'Bronze']

# 百名店
MEITEN_LIST = [
    '', '日本料理', 'フレンチ', 'イタリアン', '中国料理', '定食', '喫茶店', 'ビストロ', '洋食',
    '寿司', 'ラーメン', 'うどん', 'そば', 'カレー', 'ステーキ', 'ハンバーガー', '焼肉', 'うなぎ', 'とんかつ', 'お好み焼き', '焼鳥', 'ピザ', '餃子', 'パン', 'スイーツ'
]

# その他
SPECIAL_LIST = [
    '', '県別表示', '県別店舗数', 'ジャンル別トップ'
]
