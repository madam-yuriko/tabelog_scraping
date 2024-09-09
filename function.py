import const
import re
import time
import polars as pl


def processing_data_frame(df, area='', tdfkn='', score_condition='', shop_name='', genre='', only_genre1=False, yosan_night_l='', yosan_night_h='', place1='', place2='', place3='', business_status='', sort_type='', award='', meiten='', special=''):
    start_time = time.time()
    if df is None:
        return
    
    print('-------processing_data_frame start------', df.shape)
    
    if area:
        df = df.filter(pl.col('都道府県').str.contains(const.AREA_DICT[area]))
            
    if tdfkn:
        df = df.filter(pl.col('都道府県') == tdfkn)
        
    if score_condition:
        if score_condition == '3.00未満':
            df = df.filter(pl.col('点数') < 3.00)
        else:
            df = df.filter(pl.col('点数') >= float(score_condition[:4]))
    
    # 標準/営業中のみ/新規オープンのみ/昨年閉店のみ/過去店全表示のパターンでフィルタ
    if business_status == const.BUSINESS_STATUS_LIST[0]:
        df = df.filter(~pl.col('ステータス').is_in(['閉店', '移転', '休業', '掲載保留']))
    elif business_status == const.BUSINESS_STATUS_LIST[1]:
        df = df.filter(~pl.col('ステータス').is_in(['閉店', '移転', '休業', '掲載保留', '去年閉店']))
    elif business_status == const.BUSINESS_STATUS_LIST[2]:
        df = df.filter(pl.col('indicator_1') == 'left_only')
    elif business_status == const.BUSINESS_STATUS_LIST[3]:
        df = df.filter(pl.col('ステータス') == '去年閉店')
    elif business_status == const.BUSINESS_STATUS_LIST[4]:
        pass

    # ソート
    if sort_type == const.SORT_TYPE_LIST[0]:
        df = df.sort(by=['点数', '口コミ数', '保存件数'], descending=True)
    elif sort_type == const.SORT_TYPE_LIST[1]:
        df = df.filter(pl.col('点数(増減') != '-')
        df = df.with_column(pl.col('点数(増減').cast(pl.Float64))
        df = df.filter(pl.col('点数(増減') < 2)
        df = df.sort(by=['点数(増減)', '点数', '口コミ数', '保存件数'], descending=True)
    elif sort_type == const.SORT_TYPE_LIST[2]:
        df = df.sort(by=['口コミ数', '点数', '保存件数'], descending=True)
    elif sort_type == const.SORT_TYPE_LIST[3]:
        df = df.sort(by=['口コミ数(増減)', '口コミ数', '点数', '保存件数'], descending=True)
    else:
        df = df.sort(by=['保存件数', '点数', '口コミ数'], descending=True)

    df = df.with_columns(pl.Series('エリア順位', range(1, len(df) + 1)))

    # 各パラメータでフィルタ
    if shop_name:
        df = df.filter(pl.col('店名').str.to_lowercase().str.replace_all(' ', '').str.contains(shop_name.lower().replace(' ', '')))
    
    if genre:
        df = df.filter(pl.col('ジャンル1').str.contains(genre) | 
                        pl.col('ジャンル2').str.contains(genre) | 
                        pl.col('ジャンル3').str.contains(genre))
    
    if only_genre1:
        df = df.filter(pl.col('ジャンル1').str.contains(genre))
    
    if yosan_night_l != 1 or yosan_night_h != 17:
        df = df.filter((pl.col('予算') != 0) & 
                        (pl.col('予算') >= yosan_night_l) & 
                        (pl.col('予算') <= yosan_night_h))
    
    if not (place1 == '' and place2 == '' and place3 == '') and (place1[-1] == '駅' and (place2 == '' or place2[-1] == '駅') and (place3 == '' or place3[-1] == '駅')):
        df = df.filter(pl.col('最寄り駅').is_in([place1, place2, place3]))
    else:
        for place in [place1, place2, place3]:
            if place:
                df = df.filter(
                    pl.col('所在地').str.to_lowercase().str.replace_all(' ', '').str.contains(place.lower().replace(' ', '')) |
                    pl.col('施設名').str.to_lowercase().str.replace_all(' ', '').str.contains(place.lower().replace(' ', '')) |
                    pl.col('最寄り駅').str.to_lowercase().str.replace_all(' ', '').str.contains(place.lower().replace(' ', ''))
                )
    
    if award:
        df = df.filter(pl.col('食べログアワード').str.contains(award))
    
    if meiten:
        df = df.filter(pl.col('百名店').str.contains(meiten))

    if special == '県別表示':
        df = df.with_columns([
            pl.col('都道府県').apply(lambda x: const.TODOFUKEN_LIST.index(x)).alias('order')
        ])
        df = df.sort(['order', '点数', '口コミ数', '保存件数'], descending=[False, True, True, True])
        df_store_count = df.groupby('都道府県').agg(
            pl.count().alias('店舗数')
        )
        df_store_count = df_store_count.with_columns([
            pl.col('都道府県').apply(lambda x: const.TODOFUKEN_LIST.index(x)).alias('order')
        ])
        df_store_count = df_store_count.sort(['order'], descending=[False])

        result = []
        for row in df_store_count.iter_rows(named=True):
            prefecture = row['都道府県']
            count = row['店舗数']
            
            # 都道府県のデータを追加
            result.extend(df.filter(pl.col('都道府県') == prefecture).to_dicts())
            
            # 統計行を追加
            stats_row = {col: '' for col in df.columns}
            stats_row['店名'] = f"店舗数: {count}"
            stats_row['都道府県'] = prefecture
            result.append(stats_row)
        
        df = pl.DataFrame(result).fill_null('')

    elif special == '県別店舗数':
        df_store_count = df.groupby('都道府県').agg(pl.count().alias('店舗数'))
        todofuken_df = pl.DataFrame({'都道府県': const.TODOFUKEN_LIST[1:]})
        
        result_df = todofuken_df.join(df_store_count, on='都道府県', how='left').fill_null(0)
        result_df = result_df.with_columns([pl.col('店舗数').cast(pl.Int64)])
        result_df = result_df.sort('店舗数', descending=True)
        
        result = []
        for row in result_df.iter_rows(named=True):
            stats_row = {col: '' for col in df.columns}
            stats_row['店名'] = f"店舗数: {row['店舗数']}"
            stats_row['都道府県'] = row['都道府県']
            result.append(stats_row)
        
        df = pl.DataFrame(result)

    elif special == 'ジャンル別トップ':
        df = df.with_columns([
            pl.col('ジャンル1').apply(lambda x: const.GENRE_LIST.index(x)).alias('order')
        ])
        df = df.sort(['order', '点数', '口コミ数', '保存件数'])
        df = df.groupby('order').last().sort(['点数', '口コミ数', '保存件数'], descending=True)
            
    print('-------df.shape------', df.shape)
    print('processing time:', time.time() - start_time)
    return df


def insert_tree(tree, df_target, special):
    
    # ツリーを全削除
    for i in tree.get_children():
        tree.delete(i)
    
    # DataFrameをリストに変換
    rows = df_target.rows()
    column_names = df_target.columns

    # 再描画
    for idx, row in enumerate(rows):
        # 値を書き換えるためlistに変換
        row = list(row)
        
        # 一覧に入力
        award_str = ''
        
        # 全国順位整数化
        col_1 = column_names.index('全国順位')
        col_2 = column_names.index('順位変動_str')
        if row[col_1] == 'Total' or special in ('県別表示', '県別店舗数'):
            pass
        elif row[col_1] is None:
            row[col_1] = '-'
            row[col_2] = '-'
        elif row[col_2][0] == '-' and int(row[col_1]) == int(row[col_2][1:]):
            row[col_1] = int(row[col_1])
            row[col_2] = '-'
        elif isinstance(row[col_1], float):
            row[col_1] = int(row[col_1])
        
        # 食べログアワード書き換え
        col = column_names.index('食べログアワード')
        for award in row[col].split('/'):
            award_str += award[2:6].replace(' ', '') + '/'
        row[col] = award_str[:-1]
        
        # 百名店書き換え
        col = column_names.index('百名店')
        meiten_str = re.sub(r'\d', '', row[col].split('/')[0]) + ' '
        for meiten in row[col].split('/'):
            meiten_str += meiten[-2:] + '/'
        row[col] = meiten_str[:-1]

        tree.insert("", "end", tags=idx, values=[idx+1] + list(row[:len(const.DATA_FLAME_LAYOUT)]))

        # バックグラウンドカラー変更
        # 閉店、新規店他
        col_1 = column_names.index('ステータス')
        col_2 = column_names.index('indicator_1')
        col_3 = column_names.index('indicator_2')
        col_4 = column_names.index('全国順位')
        if row[col_1] in ['閉店', '移転', '休業', '掲載保留', '去年閉店']:
            tree.tag_configure(idx, background="#cccccc", foreground="#000000")
        elif row[col_2] == 'left_only':
            tree.tag_configure(idx, background="#ffb993", foreground="#000000")
        elif row[col_3] == 'left_only':
            tree.tag_configure(idx, background="#f0e68c", foreground="#000000")
        elif row[col_4] == '':
            tree.tag_configure(idx, background="#a0144f", foreground="#ffffff")
        elif idx % 2 == 0:
            tree.tag_configure(idx, background="#ffffff", foreground="#000000")
        elif idx % 2 == 1:
            tree.tag_configure(idx, background="#d6f3ff", foreground="#000000")
        
        
