# 昨年のdata_base_all_[yyyy - 1].csvを読み込み最新店舗差分を食べログからスクレイピングしてカウント
command:
    python store_count.py -p 1 -y 2022

return: 
    store_count_[yyyy].csv

# 上記csvを元にマルチプロセスで本スクレイピング
command:
    python .\scraping.py -p 12 -y 2022

return:
    data_base_all_[yyyy].csv