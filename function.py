import const
import re
import time
from const import MAX_ROW_CNT


def processing_data_frame(df, area='', tdfkn='', shop_name='', genre='', only_genre1=False, yosan_night_l='', yosan_night_h='', place1='', place2='', place3='', heiten=False, kuchikomi_sort=False, award='', meiten='', special=''):
    start_time = time.time()
    if area:
        df = df[df.都道府県.str.contains(const.AREA_LIST[area])]
    if tdfkn:
        df = df[df.都道府県.str.contains(tdfkn)]
    if shop_name:
        df = df[df.店名.str.lower().str.contains(shop_name.lower())]
    if genre:
        df = df[df.ジャンル1.str.contains(genre) | df.ジャンル2.str.contains(genre) | df.ジャンル3.str.contains(genre)]
    if only_genre1:
        df = df[df.ジャンル1.str.contains(genre)]
    if yosan_night_l != 1 or yosan_night_h != 17:
        df = df[(df.予算 != 0) & ((df.予算 >= yosan_night_l) & (df.予算 <= yosan_night_h))]
    if place1:
        df = df[df.所在地.str.lower().str.contains(place1.lower()) | df.施設名.str.lower().str.contains(place1.lower()) | df.最寄り駅.str.lower().str.contains(place1.lower())]
    if place2:
        df = df[df.所在地.str.lower().str.contains(place2.lower()) | df.施設名.str.lower().str.contains(place2.lower()) | df.最寄り駅.str.lower().str.contains(place2.lower())]
    if place3:
        df = df[df.所在地.str.lower().str.contains(place3.lower()) | df.施設名.str.lower().str.contains(place3.lower()) | df.最寄り駅.str.lower().str.contains(place3.lower())]
    if award:
        df = df[df.食べログアワード.str.contains(award)]
    if meiten:
        df = df[df.百名店.str.contains(meiten)]
    if heiten is False:
        df = df[~df.ステータス.isin(['閉店', '移転', '休業', '掲載保留'])]
    if kuchikomi_sort:
        df = df.sort_values(['口コミ数', '点数', '保存件数'], ascending=False)
    else:
        df = df.sort_values(['点数', '口コミ数', '保存件数'], ascending=False)

    if special:
        if special == '県別トップ':  
            df['order'] = df['都道府県'].apply(lambda x: const.TODOFUKEN_LIST.index(x))
            df = df.sort_values(['order', '点数', '口コミ数', '保存件数'])
            df = df[~df.duplicated(subset=['order'], keep='last')]
        elif special == 'ジャンル別トップ':
            df['order'] = df['ジャンル1'].apply(lambda x: const.ALL_GENRE.index(x))
            df = df.sort_values(['order', '点数', '口コミ数', '保存件数'])
            df = df[~df.duplicated(subset=['order'], keep='last')]
            df = df.sort_values(['点数', '口コミ数', '保存件数'], ascending=False)
        
    print('processing time:', time.time() - start_time)
    return df


def insert_tree(tree, df_target):
    # ツリーを全削除
    for i in tree.get_children():
        tree.delete(i)
    # 再描画
    df_target = df_target.iloc[0:MAX_ROW_CNT]
    for i, row in enumerate(df_target.itertuples()):
        # 一覧に入力
        award_str = ''
        row = list(row)
        # 食べログアワード書き換え
        for award in row[8].split('/'):
            award_str += award[2:6].replace(' ', '') + '/'
        row[8] = award_str[0:-2]
        # 百名店書き換え
        meiten_str = re.sub(r'\d', '', row[9].split('/')[0]) + ' '
        for meiten in row[9].split('/'):
            meiten_str += meiten[-2:] + '/'
        row[9] = meiten_str[0:-2]
        tree.insert("", "end", tags=i, values=[i+1] + list(row[1:len(const.DATA_FLAME_LAYOUT)+1]))
        if row[2] in ['閉店', '移転', '休業', '掲載保留']:
            tree.tag_configure(i, background="#cccccc")
        elif i % 2 == 0:
            tree.tag_configure(i, background="#ffffff")
        elif i % 2 == 1:
            tree.tag_configure(i, background="#d6f3ff")