import tkinter as tk

YEAR = 2022

def get_csv_name(yaer):
    return f'data_base_all_{yaer}.csv'

VIEW_ROW_CNT = 50
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
    'No': [40, tk.E], '全国順位': [60, tk.E], '店名': [300, tk.W], 'ステータス': [80, tk.W], '点数': [60, tk.E], '点数(増減)': [60, tk.E], 
    '口コミ数': [60, tk.E], '口コミ数(増減)': [60, tk.E], '保存件数': [80, tk.E], '予算(夜)': [150, tk.E], '予算(昼)': [150, tk.E], 
    '食べログアワード': [200, tk.W], '百名店': [220, tk.W], 'ジャンル1': [130, tk.W], 'ジャンル2': [130, tk.W], 'ジャンル3': [130, tk.W], 
    '都道府県': [80, tk.W], '所在地': [200, tk.W], '施設名': [240, tk.W], '最寄り駅': [100, tk.W], '席数': [70, tk.E], 'オープン日': [130, tk.E], '説明詳細': [600, tk.W]
}

MERGE_COL_NAMES = [
    'ID', 'URL', '取得日時', '都道府県', '所在地', '施設名', '最寄り駅', 'ステータス', '店名',
    '食べログアワード', '百名店', '点数', '口コミ数', '保存件数', '予算(夜)', '予算(昼)', 'ジャンル1',
    'ジャンル2', 'ジャンル3', '説明', '説明詳細', '予約可否', 'オープン日', '席数', '備考', 'ホームページ',
    'アカウント', '予算', '点数(昨年)', '口コミ数(昨年)', '_merge'
]

# 商業施設一覧
SHISETSU_DICT = {
    '': {},
    '札幌ステラプレイス': {'都道府県': '北海道', '場所1': 'ステラプレイス', '場所2': '', '場所3': ''},
    '札幌 PASEO': {'都道府県': '北海道', '場所1': '札幌', '場所2': 'パセオ|PASEO', '場所3': ''},
    '札幌エスタ': {'都道府県': '北海道', '場所1': '札幌市中央区北', '場所2': 'エスタ|ESTA', '場所3': ''},
    '札幌 サッポロファクトリー': {'都道府県': '北海道', '場所1': 'サッポロファクトリー', '場所2': '', '場所3': ''},
    '札幌 日本生命 noasis': {'都道府県': '北海道', '場所1': '札幌', '場所2': '日本生命', '場所3': ''},
    '札幌 赤れんがテラス': {'都道府県': '北海道', '場所1': '札幌', '場所2': '赤れんが|赤レンガ', '場所3': ''},
    '札幌 sitatte sapporo': {'都道府県': '北海道', '場所1': '札幌', '場所2': 'sitatte|フコク生命', '場所3': ''},
    '札幌 大通BISSE': {'都道府県': '北海道', '場所1': '中央区大通西3', '場所2': '', '場所3': ''},
    '札幌 miredo': {'都道府県': '北海道', '場所1': '札幌', '場所2': '大同生命', '場所3': ''},
    '熊本 サクラマチクマモト': {'都道府県': '熊本県', '場所1': '桜町3-10', '場所2': '', '場所3': ''},
    '渋谷ヒカリエ': {'都道府県': '東京都', '場所1': '渋谷2-21-1', '場所2': '', '場所3': ''},
    '渋谷ストリーム': {'都道府県': '東京都', '場所1': '渋谷3-21-3', '場所2': '', '場所3': ''},
    '渋谷スクランブルスクエア': {'都道府県': '東京都', '場所1': '渋谷2-24-12', '場所2': '12F|13F', '場所3': ''},
    '渋谷パルコ': {'都道府県': '東京都', '場所1': '宇田川町15-1', '場所2': '', '場所3': ''},
    '渋谷フクラス': {'都道府県': '東京都', '場所1': '道玄坂1-2-3', '場所2': '', '場所3': ''},
    '渋谷 ミヤシタパーク': {'都道府県': '東京都', '場所1': '神宮前', '場所2': '6-20-10|六丁目20-10', '場所3': ''},
    '渋谷6種商業施設': {'都道府県': '東京都', '場所1': '渋谷2-21-1|渋谷3-21-3|渋谷2-24-12|宇田川町15-1|道玄坂1-2-3|神宮前6-20-10', '場所2': '', '場所3': ''},
    '原宿 WITH HARAJUKU': {'都道府県': '東京都', '場所1': '神宮前1-14-30', '場所2': '', '場所3': ''},
    '原宿 神宮前COMICHI': {'都道府県': '東京都', '場所1': '神宮前1-23-26', '場所2': '', '場所3': ''},
    '恵比寿 アトレ恵比寿': {'都道府県': '東京都', '場所1': 'アトレ恵比寿', '場所2': '5F|6F', '場所3': ''},
    '池袋 東武百貨店 スパイス': {'都道府県': '東京都', '場所1': '池袋', '場所2': '東武百貨店', '場所3': '11F|12F|13F|14F|15F'},
    '日比谷 東京ミッドタウン日比谷': {'都道府県': '東京都', '場所1': 'ミッドタウン日比谷', '場所2': '', '場所3': ''},
    '日比谷 OKUROJI': {'都道府県': '東京都', '場所1': '内幸町1-7-1', '場所2': '', '場所3': ''},
    '銀座 東急プラザ': {'都道府県': '東京都', '場所1': '銀座5-2-1', '場所2': '', '場所3': ''},
    '銀座 GINZA SIX': {'都道府県': '東京都', '場所1': '銀座6-10-1', '場所2': '', '場所3': ''},
    '大手町 TOKYO TORCH 常盤橋タワー': {'都道府県': '東京都', '場所1': '大手町2-6-4', '場所2': '', '場所3': ''},
    '丸の内 丸の内ビルディング': {'都道府県': '東京都', '場所1': '丸の内2-4-1', '場所2': '', '場所3': ''},
    '丸の内 新丸の内ビルディング': {'都道府県': '東京都', '場所1': '丸の内1-5-1', '場所2': '', '場所3': ''},
    '四谷 コモレ四谷': {'都道府県': '東京都', '場所1': '新宿区四谷1-6-1', '場所2': '', '場所3': ''},
    '豊洲 ららぽーと豊洲': {'都道府県': '東京都', '場所1': '豊洲', '場所2': '2-4-9|2-2-1', '場所3': ''},
    '有明ガーデン': {'都道府県': '東京都', '場所1': '有明2-1-8', '場所2': '', '場所3': ''},
    '後楽園 ラクーア': {'都道府県': '東京都', '場所1': '春日1-1-1', '場所2': '', '場所3': ''},
    '金町 ベルトーレ金町': {'都道府県': '東京都', '場所1': '金町6-5-1', '場所2': '', '場所3': ''},
    '亀有 アリオ亀有': {'都道府県': '東京都', '場所1': '亀有3-49-3', '場所2': '', '場所3': ''},
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

TODOFUKEN_URL_LIST = {
    '01': 'hokkaido', '02': 'aomori', '03': 'iwate', '04': 'miyagi', '05': 'akita', '06': 'yamagata', '07': 'fukushima', '08': 'ibaraki', '09': 'tochigi', '10': 'gunma',
    '11': 'saitama', '12': 'chiba', '13': 'tokyo', '14': 'kanagawa', '15': 'niigata', '16': 'toyama', '17': 'ishikawa', '18': 'fukui', '19': 'yamanashi', '20': 'nagano',
    '21': 'gifu', '22': 'shizuoka', '23': 'aichi', '24': 'mie', '25': 'shiga', '26': 'kyoto', '27': 'osaka', '28': 'hyogo', '29': 'nara', '30': 'wakayama',
    '31': 'tottori', '32': 'shimane', '33': 'okayama', '34': 'hiroshima', '35': 'yamaguchi', '36': 'tokushima', '37': 'kagawa', '38': 'ehime', '39': 'kochi', '40': 'fukuoka',
    '41': 'saga', '42': 'nagasaki', '43': 'kumamoto', '44': 'oita', '45': 'miyazaki', '46': 'kagoshima', '47': 'okinawa',
}

# ジャンル一覧
GENRE_LIST = None

# 予算
YOSAN_LIST = {
    '-': 0, '～￥999': 1, '￥1000～￥1999': 2, '￥2000～￥2999': 3, '￥3000～￥3999': 4, '￥4000～￥4999': 5, '￥5000～￥5999': 6, '￥6000～￥7999': 7, '￥8000～￥9999': 8, 
    '￥10000～￥14999': 9, '￥15000～￥19999': 10, '￥20000～￥29999': 11, '￥30000～￥39999': 12, '￥40000～￥49999': 13, '￥50000～￥59999': 14, '￥60000～￥79999': 15, '￥80000～￥99999': 15, '￥100000～': 16, 
}

YOSAN_LIST_L = ['', '￥1000', '￥2000', '￥3000', '￥4000', '￥5000', '￥6000', '￥8000', '￥10000', '￥15000', '￥20000', '￥30000', '￥40000', '￥50000', '￥60000', '￥80000', '￥100000']
YOSAN_LIST_H = ['￥999', '￥1999', '￥2999', '￥3999', '￥4999', '￥5999', '￥7999', '￥9999', '￥14999', '￥19999', '￥29999', '￥39999', '￥49999', '￥59999', '￥79999', '￥99999', '']

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
    '', '県別トップ', 'ジャンル別トップ'
]
