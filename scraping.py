import argparse
import requests
import pandas as pd
import numpy as np
import const
import ipynb_function as ipfunc
import concurrent.futures
import sys
import os
import pickle


# 途中スタート位置
def main(args):
    process = int(args.p)
    year = args.y

    # 全ての店舗IDと残店舗IDを取得
    all_id_count, remaining_id_list = ipfunc.preprocessing(args.y)
    
    # 各プロセスに分割
    id_list_split = np.array_split(remaining_id_list, process)

    try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=process) as executor:
            # マルチプロセス
            futures = []
            for i, p_id in enumerate(range(1, process+1)):
                futures.append(executor.submit(request, year, str(p_id).zfill(2), id_list_split[i], all_id_count))
            for future in futures:
                future.result()
    except Exception:
        print('\nEXCEPTION:マルチプロセス処理でエラーが発生しました。\n%s', sys.exc_info())
        sys.exit(0)
    finally:
        # ソート
        ipfunc.sort_csv_file(year)
        print('end')


def request(year, p_id, id_list, all_id_count):
    try:
        loaded_store_id = set()
        for store_id in id_list:
            tdfkn = const.TODOFUKEN_URL_LIST[store_id[:2]]
            url = f'https://tabelog.com/{tdfkn}/A0101/A010101/{store_id}/'

            # HTTPリクエスト
            response = requests.get(url)
            loaded_store_id.add(store_id)
            count = ipfunc.add_count()
            print(f'Process ID:{p_id} progress:{count} / {all_id_count} status:{response.status_code}\r', end="")
            if response.status_code != 200:
                continue
            # 店舗ごとに処理
            ipfunc.extraction(response, store_id, url, year)
    finally:
        # 処理が終了または中止した場合はpickleに残店舗IDを保存
        ipfunc.update_remining_id(year, loaded_store_id)
        print(f'{p_id}: write pickle')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, required=True) # プロセス数指定
    parser.add_argument('-y', type=int, required=True) # 入力ファイルの年度指定
    args = parser.parse_args()

    main(args)