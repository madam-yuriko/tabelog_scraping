import argparse
import requests
import pandas as pd


# 途中スタート位置
def main(args):
    year = int(args.y)
    # 指定した年の前年の各県の最終店舗を辞書化
    exist_id = pd.read_csv(f'data_base_all_{year - 1}.csv', usecols=['ID'], dtype = {'ID': str}, encoding='utf-8', low_memory=False)
    last_store = {}
    for id in exist_id['ID'].tolist():
        last_store[id[:2]] = id

    # 最終店舗の次の店舗からHTTPリクエストして本年の最終店舗を探索
    df = pd.DataFrame.from_dict(request(last_store), orient='index')
    df.to_csv(f'store_count_{year}.csv', header=None)
    print('end')


def request(last_store):
    update_last_id_dict = {}
    for tdfkn, last_id in last_store.items():
        failed_cnt = 0
        start_id = int(last_id[2:]) + 1
        for j in range(start_id, 1000000):
            t_id = str(int(tdfkn)*1000000+j).zfill(8)
            if failed_cnt >= 50:
                break
            url = f'https://tabelog.com/{tdfkn}/A0101/A010101/{t_id}/'
            response = requests.get(url) # HTTPリクエスト
            if response.status_code == 200:
                failed_cnt = 0
                update_last_id_dict[tdfkn] = t_id
                print(f'{t_id} success!:{response.status_code}\r', end="")
            else:
                print(f'{t_id} failed!:{response.status_code}\r', end="")
                failed_cnt += 1
                continue
    return update_last_id_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', type=int, required=True) # 入力ファイルの年度指定
    args = parser.parse_args()
    main(args)