import argparse
import requests
import pandas as pd
import numpy as np
import const
import ipynb_function as ipfunc
import concurrent.futures
import sys
import pickle


# 途中スタート位置
def main(args):
    process = int(args.p)
    year = args.y

    # 出力済みの店舗IDは削除
    output_id_list = ipfunc.preprocessing(args.y)
    print(f'Process {len(output_id_list)} IDs\n')
    # 各プロセスに分割
    id_list_split = np.array_split(output_id_list, process)

    try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=process) as executor:
            futures = []
            for i, p_id in enumerate(range(1, process+1)):
                futures.append(executor.submit(request, year, str(p_id).zfill(2), id_list_split[i]))
            for future in futures:
                future.result()
    except Exception:
        print('\nEXCEPTION:マルチプロセス処理でエラーが発生しました。\n%s', sys.exc_info())
        sys.exit(0)
    print('end')


def request(year, p_id, id_list):
    for store_id in id_list:
        tdfkn = const.TODOFUKEN_URL_LIST[store_id[:2]]
        url = f'https://tabelog.com/{tdfkn}/A0101/A010101/{store_id}/'
        # HTTPリクエスト
        response = requests.get(url)
        if response.status_code == 200:
            # 店舗が存在
            print(f'Process ID={p_id} {tdfkn}:{store_id} success!\r', end="")
        else:
            # 店舗が存在しない
            print(f'Process ID={p_id} {tdfkn}:{store_id} failed!!\r', end="")
            continue
        # 店舗ごとに処理
        ipfunc.extraction(response, store_id, url)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, required=True) # プロセス数指定
    parser.add_argument('-y', type=int, required=True) # 入力ファイルの年度指定
    args = parser.parse_args()

    main(args)