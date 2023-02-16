import const
import re
import time
import pandas as pd


def processing_data_frame(df, shop_name='', genre='', only_genre1=False, yosan_night_l='', yosan_night_h='', place1='', place2='', place3='', new_open=False, heiten=False, sort_type='', award='', meiten='', special=''):
    start_time = time.time()
    print('df_length', len(df))
    if heiten is False:
        df = df[~df.ステータス.isin(['閉店', '移転', '休業', '掲載保留'])]
    if sort_type == const.SORT_TYPE_LIST[0]:
        df = df.sort_values(['点数', '口コミ数', '保存件数'], ascending=False)
    elif sort_type == const.SORT_TYPE_LIST[1]:
        df = df[df['点数(増減)'] != '-']
        df['点数(増減)'] = df['点数(増減)'].astype(float)
        df = df[df['点数(増減)'] < 2]
        df = df.sort_values(['点数(増減)', '点数', '口コミ数', '保存件数'], ascending=False)
    elif sort_type == const.SORT_TYPE_LIST[2]:
        df = df.sort_values(['口コミ数', '点数', '保存件数'], ascending=False)
    elif sort_type == const.SORT_TYPE_LIST[3]:
        df = df.sort_values(['口コミ数(増減)', '口コミ数', '点数', '保存件数'], ascending=False)
    else:
        df = df.sort_values(['保存件数', '点数', '口コミ数'], ascending=False)

    df['エリア順位'] = pd.RangeIndex(start=1, stop=len(df.index) + 1, step=1)

    if shop_name:
        df = df[df.店名.str.lower().str.replace(' ', '').str.contains(shop_name.lower().replace(' ', ''))]
    if genre:
        df = df[df.ジャンル1.str.contains(genre) | df.ジャンル2.str.contains(genre) | df.ジャンル3.str.contains(genre)]
    if only_genre1:
        df = df[df.ジャンル1.str.contains(genre)]
    if yosan_night_l != 1 or yosan_night_h != 17:
        df = df[(df.予算 != 0) & ((df.予算 >= yosan_night_l) & (df.予算 <= yosan_night_h))]
    if place1:
        df = df[df.所在地.str.lower().str.replace(' ', '').str.contains(place1.lower().replace(' ', '')) | df.施設名.str.lower().str.replace(' ', '').str.contains(place1.lower().replace(' ', '')) | df.最寄り駅.str.lower().str.replace(' ', '').str.contains(place1.lower().replace(' ', ''))]
    if place2:
        df = df[df.所在地.str.lower().str.replace(' ', '').str.contains(place2.lower().replace(' ', '')) | df.施設名.str.lower().str.replace(' ', '').str.contains(place2.lower().replace(' ', '')) | df.最寄り駅.str.lower().str.replace(' ', '').str.contains(place2.lower().replace(' ', ''))]
    if place3:
        df = df[df.所在地.str.lower().str.replace(' ', '').str.contains(place3.lower().replace(' ', '')) | df.施設名.str.lower().str.replace(' ', '').str.contains(place3.lower().replace(' ', '')) | df.最寄り駅.str.lower().str.replace(' ', '').str.contains(place3.lower().replace(' ', ''))]
    if new_open:
        df = df[df._merge == 'left_only']
    if award:
        df = df[df.食べログアワード.str.contains(award)]
    if meiten:
        df = df[df.百名店.str.contains(meiten)]

    if special:
        if special == '県別トップ':  
            df['order'] = df['都道府県'].apply(lambda x: const.TODOFUKEN_LIST.index(x))
            df = df.sort_values(['order', '点数', '口コミ数', '保存件数'])
            df = df[~df.duplicated(subset=['order'], keep='last')]
        elif special == 'ジャンル別トップ':
            df['order'] = df['ジャンル1'].apply(lambda x: const.GENRE_LIST.index(x))
            df = df.sort_values(['order', '点数', '口コミ数', '保存件数'])
            df = df[~df.duplicated(subset=['order'], keep='last')]
            df = df.sort_values(['点数', '口コミ数', '保存件数'], ascending=False)

    df_total = pd.DataFrame(columns=df.columns)
    df_total.loc['Total'] = ''
    df_total.loc['Total', '全国順位'] = 'Total'
    df['点数(増減)'] = df['点数(増減)'].apply(lambda x: score_zougen_int(x))
    score_zougen = df[df['点数(増減)'] != '-']['点数(増減)'].sum()
    score_zougen = f'+{score_zougen:.2f}' if score_zougen > 0 else f'{score_zougen:.2f}'
    df_total.loc['Total', '点数(増減)'] = score_zougen
    df_total.loc['Total', '口コミ数'] = df['口コミ数'].sum()
    df_total.loc['Total', '口コミ数(増減)'] = f'+{df["口コミ数(増減)"].sum()}'
    df_total.loc['Total', '保存件数'] = df['保存件数'].sum()

    # 列加工
    df['順位変動'] = df['順位変動'].apply(lambda x: rank_hendo(x))
    df['点数'] = df['点数'].apply(lambda x: score(x))
    df['点数(増減)'] = df['点数(増減)'].apply(lambda x: score_zougen_str(x))
    df['口コミ数(増減)'] = df['口コミ数(増減)'].apply(lambda x: kutchikomi_zougen(x))

    print('processing time:', time.time() - start_time)
    return df, df_total


def insert_tree(tree, df_target):
    # ツリーを全削除
    for i in tree.get_children():
        tree.delete(i)
    # 再描画
    for i, row in enumerate(df_target.itertuples()):
        # 一覧に入力
        award_str = ''
        row = list(row)
        # 全国順位整数化
        if row[1] == 'Total':
            continue
        elif pd.isna(row[1]):
            row[1] = '-'
            row[2] = '-'
        elif row[2][0] == '-' and int(row[1]) == int(row[2][1:]):
            row[1] = int(row[1])
            row[2] = '-'
        elif type(row[1]) == float:
            row[1] = int(row[1])

        # 食べログアワード書き換え
        if type(row[12]) == str:
            for award in row[12].split('/'):
                award_str += award[2:6].replace(' ', '') + '/'
            row[11] = award_str[0:-2]
        # 百名店書き換え
        if type(row[13]) == str:
            meiten_str = re.sub(r'\d', '', row[12].split('/')[0]) + ' '
            for meiten in row[13].split('/'):
                meiten_str += meiten[-2:] + '/'
            row[13] = meiten_str[0:-2]

        tree.insert("", "end", tags=i, values=[i+1] + list(row[1:len(const.DATA_FLAME_LAYOUT)+1]))

        # バックグラウンドカラー変更
        # 閉店他
        if row[4] in ['閉店', '移転', '休業', '掲載保留', '去年閉店']:
            tree.tag_configure(i, background="#cccccc")
        elif i % 2 == 0:
            tree.tag_configure(i, background="#ffffff")
        elif i % 2 == 1:
            tree.tag_configure(i, background="#d6f3ff")
        # 新店
        if row[25] == 'left_only':
            tree.tag_configure(i, background="#f0e68c")


# 列加工
def rank_hendo(x):
    if x > 0:
        return f'+{x}'
    else:
        return f'{x}'

def score(x):
    return f'{x:.2f}'

def score_zougen_int(x):
    if x >= 1.00:
        return 0
    else:
        return x

def score_zougen_str(x):
    if x >= 2.00:
        return '-'
    elif x > 0:
        return f'+{x:.2f}'
    else:
        return f'{x:.2f}'

def kutchikomi_zougen(x):
    return f'+{x}' if x > 0 else str(x)

