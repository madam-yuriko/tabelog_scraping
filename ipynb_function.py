from bs4 import BeautifulSoup
import const
import datetime
import re
import sys
import jaconv
import time
import pandas as pd


def scraping(response, t_id, url):
    if response.status_code == 200:
        failed_cnt = 0
        print(f'load:{url} success!:{response.status_code}')
    else:
        print(f'load:{url} failed:{response.status_code}')
        failed_cnt += 1
        return
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

            df.loc[t_id, key] = value
        except Exception:
            # print(key, sys.exc_info())
            df.loc[t_id, key] = ''
            continue
    df.to_csv(f'data_base_all.csv', mode='a', header=None)