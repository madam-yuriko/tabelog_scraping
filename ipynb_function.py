from bs4 import BeautifulSoup
import const
import datetime
import re
import sys
import jaconv
import pandas as pd
import fasteners
import pickle


def extraction(response, store_id, url):
    df = pd.DataFrame()
    soup = BeautifulSoup(response.text, "html.parser")
    for key, selector in const.SELECTOR_DIC.items():
        elems_address = soup.find_all('p', class_='rstinfo-table__address')
        elems_price = soup.find_all('span', class_='rdheader-budget__price')
        elems_price_r = soup.find_all('em', class_='gly-b-dinner')
        elems_award = soup.find_all('div', class_='rstinfo-table-badge-award')
        if key in ['説明', '説明詳細']:
            elsms_attr = soup.find_all(selector[0], class_=selector[1])
        if key == 'ID':
            continue
        try:
            value = None
            if key in 'URL':
                value = url
            elif key in ['取得日時']:
                value = datetime.datetime.now()
            elif key in ['都道府県', '所在地', '施設名']:
                value = elems_address[0].contents[selector].get_text()
            elif key in ['説明']:
                value = elsms_attr[0].contents[0]
            elif key in ['説明詳細']:
                value = elsms_attr[0].get_text()
            elif key in ['予算(夜)', '予算(昼)']:
                value = elems_price[selector].get_text()
            elif key in ['ステータス']:
                for selec in selector:
                    elems = soup.select(selec)
                    if len(elems) >= 1:
                        value = elems[0].contents[0]
            elif key in ['食べログアワード']:
                value = ''
                for elem in elems_award:
                    text = elem.contents[1].get_text()
                    if '受賞店' in text:
                        value += text.strip().replace('年', ' ').replace('受賞店', '') + '/'
            elif key in ['百名店']:
                value = ''
                for elem in elems_award:
                    text = elem.contents[1].get_text()
                    if '選出店' in text:
                        value += text.strip().replace('百名店', '').replace('選出店', '').replace(' ', '') + '/'
            elif key in ['席数']:
                elems = soup.find_all(selector[0], class_=selector[1])
                value = elems[1].find_all('p')[0].get_text()
                value = value if re.search(r'席$', value) else ''
            elif key in ['ホームページ']:
                elems = soup.find_all('a', rel='nofollow noopener')
                value = elems[0].attrs['href']
            elif key in ['公式アカウント']:
                elems = soup.find_all('a', rel='nofollow noopener')
                value = elems[1].attrs['href']
            elif key in ['最寄り駅', '点数', 'オープン日', '予約可否', '備考']:
                elems = soup.find_all(selector[0], class_=selector[1])
                value = elems[0].get_text()
            elif key in ['口コミ数', '保存件数']:
                elems = soup.find_all(selector[0], class_=selector[1])
                value = elems[0].find_all('em', class_='num')[0].get_text()
                value = '0' if value == ' - ' else value
            else:
                elems = soup.select(selector)
                value = elems[0].contents[0]
            if key not in ['取得日時']:
                value = jaconv.z2h(value, kana=False, digit=True, ascii=True).replace('~', '～').replace(',', '').replace('\n', '').strip()

            df.loc[store_id, key] = value
        except Exception:
            # print(key, sys.exc_info())
            df.loc[store_id, key] = ''
            continue
    write_csv(df)


def preprocessing(year):
    # 全ての店舗ID
    all_id_list = []
    df = pd.read_csv(f'store_count_{year}.csv', header=None)
    for i in df.itertuples():
        all_id_list += range(i[1]*1000000, i[2])
    current_id_set = set([str(j).zfill(8) for j in all_id_list])
    print(f'All store id count: {len(all_id_list)}')
    
    # 出力済みの店舗ID
    df = pd.read_csv('data_base_all.csv', usecols=['ID'], dtype = {'ID': str}, encoding='utf-8', low_memory=False)
    exist_id_set = set(df['ID'].tolist())
    print(f'Exist store id count: {len(exist_id_set)}')
    return list(current_id_set - exist_id_set)
    

@fasteners.interprocess_locked(f'lock_file_c')
def write_csv(df):
    df.to_csv(f'data_base_all.csv', mode='a', header=None)


@fasteners.interprocess_locked(f'lock_file_p')
def dump_pickle(year, store_id):
    with open(f'store_ids_{year}.binaryfile', mode='rb') as f:
        current_id_list = pickle.load(f)

    current_id_list.remove(store_id)
    with open(f'store_ids_{year}.binaryfile', mode='wb') as f:
        pickle.dump(current_id_list , f)
    