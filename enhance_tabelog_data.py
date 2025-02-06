import polars as pl
import time
import const
import sys
import io
from polars import Config

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# すべての列を表示する設定
Config.set_tbl_cols(-1)

YEAR = 2025
INPUT_FILE_NAME = f'data_base_all_{YEAR}.csv'
EXPORT_FILE_NAME_CSV = f'data_base_all_{YEAR}_processed.csv'
INPUT_L_FILE_NAME = f'data_base_all_{YEAR - 1}.csv'
INPUT_L2_FILE_NAME = f'data_base_all_{YEAR - 2}.csv'
INPUT_L3_FILE_NAME = f'data_base_all_{YEAR - 3}.csv'

def rank_hendo(x):
    return pl.when(x > 0).then(pl.format("+{}", x)).otherwise(pl.format("{}", x))
    
def score_zougen(indicator, score_diff):
    return pl.when(indicator == 'left_only').then(pl.lit("-"))\
                .when(score_diff >= 2.00).then(pl.lit("-"))\
                .when(score_diff > 0).then(pl.concat_str(pl.lit("+"), score_diff.round(2).cast(pl.Utf8)))\
                .otherwise(score_diff.round(2).cast(pl.Utf8))

def kutchikomi_zougen(x):
    return pl.when(x > 0).then(pl.format("+{}", x)).otherwise(pl.format("{}", x))

start_time = time.time()

print(f'--------{YEAR} year csv file read start-------')
df_all = pl.read_csv(INPUT_FILE_NAME, encoding='utf-8').fill_null('')
print(f'--------{YEAR} year read complete-------', f'{time.time() - start_time}sec')

print(f'--------{YEAR - 1} year csv file read start-------')
df_last_year = pl.read_csv(INPUT_L_FILE_NAME, encoding='utf-8').fill_null('')
df_last_year = df_last_year.select(['ID', 'ステータス', '点数', '口コミ数', '保存件数'])
df_rank_last_year = df_last_year.filter(~pl.col('ステータス').is_in(['閉店', '移転', '休業', '掲載保留', '去年閉店']))\
                                .sort(['点数', '口コミ数', '保存件数'], descending=True)
df_rank_last_year = df_rank_last_year.with_row_count('全国順位', offset=1)
df_last_year = df_last_year.join(df_rank_last_year.select(['ID', '全国順位']), on='ID', how='left')
print(f'--------{YEAR - 1} year read complete-------', f'{time.time() - start_time}sec')

print(f'--------{YEAR - 2} year csv file read start-------')
df_two_years_ago = pl.read_csv(INPUT_L2_FILE_NAME, encoding='utf-8').fill_null('')
df_two_years_ago = df_two_years_ago.select(['ID', '点数', '口コミ数'])
print(f'--------{YEAR - 2} year read complete-------', f'{time.time() - start_time}sec')

print(f'--------{YEAR - 3} year csv file read start-------')
df_three_years_ago = pl.read_csv(INPUT_L3_FILE_NAME, encoding='utf-8').fill_null('')
df_three_years_ago = df_three_years_ago.select(['ID', '点数', '口コミ数'])
print(f'--------{YEAR - 3} year read complete-------', f'{time.time() - start_time}sec')

df_all = df_all.with_columns([
    pl.col('予算(夜)').cast(pl.Utf8).alias('予算(夜)_str')
])

df_all = df_all.with_columns([
    pl.when(pl.col('予算(夜)_str') == '0').then(pl.lit('-')).otherwise(pl.col('予算(夜)_str')).alias('予算(夜)'),
    pl.col('予算(夜)_str').map_dict(const.YOSAN_LIST, default=0).alias('予算')
])

df_all = df_all.drop('予算(夜)_str')

# 本年度と昨年度を結合
df_all = df_all.join(df_last_year, on='ID', how='left', suffix='_昨年')
df_all = df_all.with_columns([
    pl.when(pl.col('ステータス_昨年').is_null()).then(pl.lit('left_only'))
        .otherwise(pl.lit('both')).alias('indicator_1')
])

# 一昨年のデータとの結合
df_all = df_all.join(df_two_years_ago, on='ID', how='left', suffix='_一昨年')
df_all = df_all.with_columns([
    pl.when(pl.col('点数_一昨年').is_null()).then(pl.lit('left_only'))
        .otherwise(pl.lit('both')).alias('indicator_2')
])

# 3年前のデータとの結合
df_all = df_all.join(df_three_years_ago, on='ID', how='left', suffix='_3年前')
df_all = df_all.with_columns([
    pl.when(pl.col('点数_3年前').is_null()).then(pl.lit('left_only'))
        .otherwise(pl.lit('both')).alias('indicator_3')
])

print(df_all.columns) 
df_all = df_all.rename(dict(zip(df_all.columns, const.MERGE_COL_NAMES)))

df_all = df_all.with_columns([
    (pl.col('点数').fill_null(0).cast(pl.Float64) - pl.col('点数(昨年)').fill_null(0).cast(pl.Float64)).alias('点数(増減)'),
    (pl.col('口コミ数').fill_null(0).cast(pl.Int64) - pl.col('口コミ数(昨年)').fill_null(0).cast(pl.Int64)).alias('口コミ数(増減)'),
    (pl.col('点数(昨年)').fill_null(0).cast(pl.Float64) - pl.col('点数(一昨年)').fill_null(0).cast(pl.Float64)).alias('点数(増減2)'),
    (pl.col('口コミ数(昨年)').fill_null(0).cast(pl.Int64) - pl.col('口コミ数(一昨年)').fill_null(0).cast(pl.Int64)).alias('口コミ数(増減2)'),
    (pl.col('点数(一昨年)').fill_null(0).cast(pl.Float64) - pl.col('点数(3年前)').fill_null(0).cast(pl.Float64)).alias('点数(増減3)'),
    (pl.col('口コミ数(一昨年)').fill_null(0).cast(pl.Int64) - pl.col('口コミ数(3年前)').fill_null(0).cast(pl.Int64)).alias('口コミ数(増減3)'),
    pl.when(pl.col('ステータス').is_in(['閉店', '移転', '休業', '掲載保留']) & pl.col('ステータス(昨年)').eq('')).then(pl.lit('去年閉店')).otherwise(pl.col('ステータス')).alias('ステータス')
])

df_rank = df_all.filter(~pl.col('ステータス').is_in(['閉店', '移転', '休業', '掲載保留', '去年閉店']))\
                .sort(['点数', '口コミ数', '保存件数'], descending=True)\
                .with_row_count('全国順位', offset=1)\
                .select(['ID', '全国順位'])

df_all = df_all.join(df_rank, on='ID', how='left')

df_all = df_all.with_columns([
    (pl.col('全国順位(昨年)').fill_null(0).cast(pl.Int64) - pl.col('全国順位').fill_null(0).cast(pl.Int64)).alias('順位変動'),
])

df_all = df_all.with_columns([
    rank_hendo(pl.col('順位変動')).alias('順位変動_str'),
])

df_all = df_all.with_columns([
    # pl.col('点数').round(2).fill_null("-").apply(lambda x: f"{x:.2f}" if isinstance(x, float) else x, return_dtype=pl.Utf8).alias('点数_str'),
    # pl.col('点数(昨年)').round(2).fill_null("-").apply(lambda x: f"{x:.2f}" if isinstance(x, float) else x, return_dtype=pl.Utf8).alias('点数(昨年)_str'),
    # pl.col('点数(一昨年)').round(2).fill_null("-").apply(lambda x: f"{x:.2f}" if isinstance(x, float) else x, return_dtype=pl.Utf8).alias('点数(一昨年)_str'),
    pl.col('点数').fill_null(0.00).round(2).apply(lambda x: f"{x:.2f}").alias('点数_str'),
    pl.col('点数(昨年)').fill_null(0.00).round(2).apply(lambda x: f"{x:.2f}").alias('点数(昨年)_str'),
    pl.col('点数(一昨年)').fill_null(0.00).round(2).apply(lambda x: f"{x:.2f}").alias('点数(一昨年)_str'),
    pl.col('点数(3年前)').fill_null(0.00).round(2).apply(lambda x: f"{x:.2f}").alias('点数(3年前)_str'),
    score_zougen(pl.col('indicator_1'), pl.col('点数(増減)')).alias('点数(増減)_str'),
    kutchikomi_zougen(pl.col('口コミ数(増減)')).alias('口コミ数(増減)_str'),
    score_zougen(pl.col('indicator_2'), pl.col('点数(増減2)')).alias('点数(増減2)_str'),
    kutchikomi_zougen(pl.col('口コミ数(増減2)')).alias('口コミ数(増減2)_str'),
    score_zougen(pl.col('indicator_3'), pl.col('点数(増減3)')).alias('点数(増減3)_str'),
    kutchikomi_zougen(pl.col('口コミ数(増減3)')).alias('口コミ数(増減3)_str'),
])

print('----------------', df_all.filter(pl.col("店名") == "ビオラルカフェ 有明ガーデン店"))

print('--------Merge DataFrame complete--------', f'{time.time() - start_time}sec')

df_all.write_csv(EXPORT_FILE_NAME_CSV)
print('--------Export to parquet complete--------')