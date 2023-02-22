import const
import re
import time
import pandas as pd


def processing_data_frame(df, shop_name='', genre='', only_genre1=False, yosan_night_l='', yosan_night_h='', place1='', place2='', place3='', business_status='', sort_type='', award='', meiten='', special=''):
    start_time = time.time()
    print('df_length', len(df))
    if business_status == const.BUSINESS_STATUS_LIST[0]:
        df = df[~df.ステータス.isin(['閉店', '移転', '休業', '掲載保留'])]
    elif business_status == const.BUSINESS_STATUS_LIST[1]:
        df = df[df._merge == 'left_only']
    elif business_status == const.BUSINESS_STATUS_LIST[2]:
        df = df[df['ステータス'] == '去年閉店']
    elif business_status == const.BUSINESS_STATUS_LIST[3]:
        pass

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
    score_zougen = df[df['点数(増減)_str'] != '-']['点数(増減)'].sum()
    score_zougen = f'+{score_zougen:.2f}' if score_zougen > 0 else f'{score_zougen:.2f}'
    df_total.loc['Total', '点数(増減)_str'] = score_zougen
    df_total.loc['Total', '口コミ数'] = df['口コミ数'].sum()
    df_total.loc['Total', '口コミ数(増減)_str'] = f'+{df["口コミ数(増減)"].sum()}'
    df_total.loc['Total', '保存件数'] = df['保存件数'].sum()

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
        col_1 = list(df_target.columns).index('全国順位') + 1
        col_2 = list(df_target.columns).index('順位変動_str') + 1
        if row[col_1] == 'Total':
            pass
        elif pd.isna(row[col_1]):
            row[col_1] = '-'
            row[col_2] = '-'
        elif row[col_2][0] == '-' and int(row[col_1]) == int(row[col_2][1:]):
            row[col_1] = int(row[col_1])
            row[col_2] = '-'
        elif type(row[col_1]) == float:
            row[col_1] = int(row[col_1])
        # 食べログアワード書き換え
        col = list(df_target.columns).index('食べログアワード') + 1
        for award in row[col].split('/'):
            award_str += award[2:6].replace(' ', '') + '/'
        row[col] = award_str[0:-2]
        # 百名店書き換え
        col = list(df_target.columns).index('百名店') + 1
        meiten_str = re.sub(r'\d', '', row[col].split('/')[0]) + ' '
        for meiten in row[col].split('/'):
            meiten_str += meiten[-2:] + '/'
        row[col] = meiten_str[0:-2]

        tree.insert("", "end", tags=i, values=[i+1] + list(row[1:len(const.DATA_FLAME_LAYOUT)+1]))

        # バックグラウンドカラー変更
        # 閉店他
        col = list(df_target.columns).index('ステータス') + 1
        if row[col] in ['閉店', '移転', '休業', '掲載保留', '去年閉店']:
            tree.tag_configure(i, background="#cccccc")
        elif i % 2 == 0:
            tree.tag_configure(i, background="#ffffff")
        elif i % 2 == 1:
            tree.tag_configure(i, background="#d6f3ff")
        # 新店
        col = list(df_target.columns).index('_merge') + 1
        if row[col] == 'left_only':
            tree.tag_configure(i, background="#f0e68c")
