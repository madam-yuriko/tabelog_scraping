import pandas as pd
import time
import const

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

YEAR = 2024
INPUT_FILE_NAME = f'data_base_all_{YEAR}.csv'
EXPORT_FILE_NAME = f'data_base_all_{YEAR}.pcl'
INPUT_L_FILE_NAME = f'data_base_all_{YEAR - 1}.csv'

def rank_hendo(x):
    if x > 0:
        return f'+{x}'
    else:
        return f'{x}'

def score(x):
    return f'{x:.2f}'

def score_zougen(x):
    if x >= 2.00:
        return '-'
    elif x > 0:
        return f'+{x:.2f}'
    else:
        return f'{x:.2f}'

def kutchikomi_zougen(x):
    return f'+{x}' if x > 0 else str(x)

start_time = time.time()

print(f'--------{YEAR} year csv file read start-------')
df_all = pd.read_csv(INPUT_FILE_NAME, encoding='utf-8', low_memory=False).fillna('')
print(f'--------{YEAR} year read complete-------', f'{time.time() - start_time}sec')
print(f'--------{YEAR - 1} yaer csv file read start-------')
df_last_year = pd.read_csv(INPUT_L_FILE_NAME, encoding='utf-8', low_memory=False).fillna('')
df_last_year = df_last_year[['ID', 'ステータス', '点数', '口コミ数', '保存件数']]
df_rank_last_year = df_last_year[~df_last_year['ステータス'].isin(['閉店', '移転', '休業', '掲載保留', '去年閉店'])].sort_values(['点数', '口コミ数', '保存件数'], ascending=False)
df_rank_last_year.reset_index(inplace=True, drop=True)
df_rank_last_year['全国順位'] = df_rank_last_year.index + 1
df_last_year = pd.merge(df_last_year, df_rank_last_year[['ID', '全国順位']], on='ID', how='left')
print(f'--------{YEAR - 1} yaer read complete-------', f'{time.time() - start_time}sec')

df_all['予算(夜)'] = df_all['予算(夜)'].replace(0, '-')
df_all['予算'] = df_all['予算(夜)'].apply(lambda x: const.YOSAN_LIST.get(x, 0))

# 本年度と昨年度を結合
df_all = pd.merge(df_all, df_last_year, on='ID', how='left', indicator=True)
df_all.columns = const.MERGE_COL_NAMES
df_all['点数(増減)'] = (df_all['点数'].fillna(0).replace('', 0).astype(float) - df_all['点数(昨年)'].fillna(0).replace('', 0).astype(float))
df_all['口コミ数(増減)'] = (df_all['口コミ数'].fillna(0).replace('-', 0).astype(int) - df_all['口コミ数(昨年)'].fillna(0).replace('-', 0).astype(int))
df_all['ステータス'] = df_all[['ステータス', 'ステータス(昨年)']].apply(lambda x: '去年閉店' if x[0] in ['閉店', '移転', '休業', '掲載保留'] and x[1] == '' else x[0], axis=1)
df_rank = df_all[~df_all['ステータス'].isin(['閉店', '移転', '休業', '掲載保留', '去年閉店'])].sort_values(['点数', '口コミ数', '保存件数'], ascending=False)
df_rank.reset_index(inplace=True, drop=True)
df_rank['全国順位'] = df_rank.index + 1
df_all = pd.merge(df_all, df_rank[['ID', '全国順位']], on='ID', how='left')
df_all['順位変動'] = (df_all['全国順位(昨年)'].fillna(0).replace('', 0).astype(int) - df_all['全国順位'].fillna(0).replace('', 0).astype(int))
# 加工
df_all['順位変動_str'] = df_all['順位変動'].apply(lambda x: rank_hendo(x))
df_all['点数_str'] = df_all['点数'].apply(lambda x: score(x))
df_all['点数(増減)_str'] = df_all['点数(増減)'].apply(lambda x: score_zougen(x))
df_all['口コミ数(増減)_str'] = df_all['口コミ数(増減)'].apply(lambda x: kutchikomi_zougen(x))
print('--------Merge DataFrame complete--------', f'{time.time() - start_time}sec')

df_all.to_pickle(EXPORT_FILE_NAME)
print('--------Export to pickle complete--------')

import const
import pandas as pd
import os

YEAR = 2024
DIRNAME = f'{YEAR}_csv'
if not os.path.exists(DIRNAME):
    os.makedirs(DIRNAME)

df_all = pd.read_pickle(f'data_base_all_{YEAR}.pcl')
for i in const.TODOFUKEN_LIST:
    if i:
        df = df_all[df_all['都道府県'] == i]
        df.to_pickle(f'{YEAR}_pcl\data_base_{i}_{YEAR}.pcl')
print('--------Export to all pickle complete--------')

import const
import pandas as pd
import os
YEAR = 2024
df_all = pd.read_pickle(f'{YEAR}_csv\data_base_岡山県_{YEAR}.pcl')
print(df_all)