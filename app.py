import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import webbrowser
import const
import function as func
import time

from const import MAX_ROW_CNT

# アプリの定義
class MouseApp(tk.Frame):
    start_flg = True

    # 初期化
    def __init__(self, master=None):
        self.link = ''
        self.df_small = None

        # ★バグ対応用の関数を追加
        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]


        tk.Frame.__init__(self, master, width=720, height=1080)

        start_time = time.time()

        # タイトルの表示
        self.master.title('食べログ')

        # ラベルの生成
        self.lbl_title = tk.Label(self, text='食べログ',
                        font=(36, 36),
                        foreground='#ffffff',
                        background='#0000aa')

        # データフレーム取得
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        print('----------------Pickle読み込み----------------')
        df_all = pd.read_pickle(const.INPUT_FILE_NAME)
        self.df_small = df_all
        print('----------------Pickle読み込み完了----------------')

        # ジャンル抽出
        const.GENRE_LIST = sorted(list(set(list(df_all['ジャンル1']) + list(df_all['ジャンル2']) + list(df_all['ジャンル3']))))

        # 地域
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_text_changed(df_all, 'area'))
        self.lbl_area = tk.Label(self, text='地方')
        self.cmb_area = ttk.Combobox(self, width=20, height=50, textvariable=sv, values=list(const.AREA_DICT.keys()))

        # 都道府県
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_text_changed(df_all, 'tdfkn'))
        self.lbl_tdfkn = tk.Label(self, text='都道府県')
        self.cmb_tdfkn = ttk.Combobox(self, width=10, height=50, textvariable=sv, values=const.TODOFUKEN_LIST)

        # 点数
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_text_changed(df_all, 'score'))
        self.lbl_score_condition = tk.Label(self, text='点数')
        self.cmb_score_condition = ttk.Combobox(self, width=10, height=50, textvariable=sv, values=const.SCORE_LIST)

        # 店名
        self.lbl_shop_name = tk.Label(self, text='店名')
        self.txt_shop_name = tk.Entry(self, width=20)
        self.txt_shop_name.bind('<Return>', lambda event, df=df_all: self.on_enter())

        # ジャンル
        self.lbl_genre = tk.Label(self, text='ジャンル')
        self.cmb_genre = ttk.Combobox(self, width=20, height=40, values=const.GENRE_LIST)
        self.cmb_genre.bind('<Return>', lambda event, df=df_all: self.on_enter())

        # ジャンル1のみ
        self.bv1 = tk.BooleanVar()
        self.bv1.trace("w", lambda name, index, mode, bv=self.bv1, df=df_all: self.on_enter())
        self.chk_only_genre1 = tk.Checkbutton(self, variable=self.bv1, text='ジャンル1のみ')

        # 予算(夜)
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_select_changed())
        self.lbl_yosan_night_l = tk.Label(self, text='予算(夜) 下限')
        self.cmb_yosan_night_l = ttk.Combobox(self, width=10, textvariable=sv, height=30, values=const.YOSAN_LIST_L)
        
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_select_changed())
        self.lbl_yosan_night_h = tk.Label(self, text='上限')
        self.cmb_yosan_night_h = ttk.Combobox(self, width=10, textvariable=sv, height=30, values=const.YOSAN_LIST_H)

        # 所在地、施設名、最寄り駅
        self.lbl_place_1 = tk.Label(self, text='場所1')
        self.txt_place_1 = tk.Entry(self, width=20)
        self.txt_place_1.bind('<Return>', lambda event, df=df_all: self.on_enter())
        self.lbl_place_2 = tk.Label(self, text='場所2')
        self.txt_place_2 = tk.Entry(self, width=20)
        self.txt_place_2.bind('<Return>', lambda event, df=df_all: self.on_enter())
        self.lbl_place_3 = tk.Label(self, text='場所3')
        self.txt_place_3 = tk.Entry(self, width=20)
        self.txt_place_3.bind('<Return>', lambda event, df=df_all: self.on_enter())

        # 営業状況
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_select_changed())
        self.lbl_buisiness_status = tk.Label(self, text='営業状況')
        self.cmb_buisiness_status = ttk.Combobox(self, width=14, textvariable=sv, height=30, values=const.BUSINESS_STATUS_LIST)

        # ソート種別
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_select_changed())
        self.lbl_sort_type = tk.Label(self, text='ソート種別')
        self.cmb_sort_type = ttk.Combobox(self, width=12, textvariable=sv, height=30, values=const.SORT_TYPE_LIST)

        # 食べログアワード
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_select_changed())
        self.lbl_award = tk.Label(self, text='食べログアワード')
        self.cmb_award = ttk.Combobox(self, width=12, textvariable=sv, height=20, values=const.AWARD_LIST)

        # 百名店
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_select_changed())
        self.lbl_meiten = tk.Label(self, text='百名店')
        self.cmb_meiten = ttk.Combobox(self, width=12, textvariable=sv, height=30, values=const.MEITEN_LIST)

        # 商業施設
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_text_changed(df_all, 'shisetsu'))
        self.lbl_shisetsu = tk.Label(self, text='商業施設')
        self.cmb_shisetsu = ttk.Combobox(self, width=32, textvariable=sv, height=30, values=list(const.SHISETSU_DICT.keys()))
        
        # テーマ別
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_text_changed(df_all, 'theme'))
        self.lbl_theme = tk.Label(self, text='テーマ別')
        self.cmb_theme = ttk.Combobox(self, width=16, textvariable=sv, height=30, values=list(const.THEME_DICT.keys()))

        # その他条件
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_text_changed(df))
        self.lbl_special = tk.Label(self, text='その他')
        self.cmb_special = ttk.Combobox(self, width=16, height=30, textvariable=sv, values=const.SPECIAL_LIST)

        # ツリーレイアウト
        self.tree = None
        self.make_tree()

        # スクロールバー
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill="y")
        self.tree.pack()
        self.tree["yscrollcommand"] = scroll.set

        # ウィジェット配置
        self.widget()

        # 初期値
        self.cmb_buisiness_status.current(0)
        self.cmb_sort_type.current(0)

        # ★バグ対応を処理
        style = ttk.Style()
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
        style.configure("Treeview", font=("Arial", 11, 'bold'), rowheight=28)

        self.reload()

    def make_tree(self):
        self.tree = ttk.Treeview(self)
        self.tree['height'] = const.VIEW_ROW_CNT
        self.tree["column"] = list(const.DATA_FLAME_LAYOUT.keys())
        self.tree["show"] = "headings"
        [self.tree.heading(k, text=k.replace('_str', '')) for k in const.DATA_FLAME_LAYOUT.keys()]
        [self.tree.column(k, width=v[0], anchor=v[1]) for k, v in const.DATA_FLAME_LAYOUT.items()]
        self.tree.bind("<Double-1>", self.hyper_link)
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_select(event))

    def hyper_link(self, event):
        webbrowser.open(self.link)

    def on_tree_select(self, event):
        if len(self.tree.selection()) != 0:
            select = self.tree.selection()[0]
            no = int(self.tree.set(select)['No']) - 1
            self.link = self.df_target.iloc[no].URL

    def on_text_changed(self, df_all, name=''):
        print('on_text_changed', name)
        df_temp = df_all.copy()
        area = self.cmb_area.get()
        tdfkn = self.cmb_tdfkn.get()
        shisetsu = self.cmb_shisetsu.get()
        theme = self.cmb_theme.get()
        score_condition = self.cmb_score_condition.get()

        if shisetsu and name == 'shisetsu':
            self.txt_place_1.delete(0, tk.END)
            self.txt_place_2.delete(0, tk.END)
            self.txt_place_3.delete(0, tk.END)
            self.txt_shop_name.delete(0, tk.END)
            shisetsu = const.SHISETSU_DICT[self.cmb_shisetsu.get()]
            for k, v in shisetsu.items():
                if k == '都道府県':
                    tdfkn = self.cmb_tdfkn.get()
                    if tdfkn != v:
                        self.cmb_tdfkn.set(v)
                elif k == '場所1':
                    self.txt_place_1.insert(tk.END, v)
                elif k == '場所2':
                    self.txt_place_2.insert(tk.END, v)
                elif k == '場所3':
                    self.txt_place_3.insert(tk.END, v)
        elif theme and name == 'theme':
            theme = const.THEME_DICT[self.cmb_theme.get()]
            for k, v in theme.items():
                if k == '店名':
                    self.txt_shop_name.insert(tk.END, v)
                elif k == 'ジャンル':
                    genre = self.cmb_genre.get()
                    if genre != v:
                        self.cmb_genre.set(v)
        else:
            self.all_reset()

        if area:
            df_temp = df_temp[df_temp.都道府県.str.contains(const.AREA_DICT[area])]
            self.cmb_tdfkn['values'] = const.AREA_DICT[area].split('|')
        else:
            self.cmb_tdfkn['values'] = const.TODOFUKEN_LIST

        if tdfkn:
            # df_temp = df_temp[df_temp.都道府県.str.contains(tdfkn)]
            df_temp = pd.read_pickle(f'{const.YEAR}_pcl\data_base_{tdfkn}_{const.YEAR}.pcl')

        if score_condition:
            if score_condition == '3.00未満':
                df_temp = df_temp[df_temp.点数 < 3.00]
            else:
                df_temp = df_temp[df_temp.点数 >= float(score_condition[:4])]

        self.df_small = df_temp.copy()
        self.reload()

    def on_check_changed(self):
        print('on_check_changed')
        self.reload()

    def on_select_changed(self):
        print('on_select_changed')
        if self.start_flg:
            self.start_flg = False
            return
        self.reload()

    def on_enter(self):
        print('on_enter')
        self.reload()

    def all_reset(self):
        print('all_reset()')
        self.txt_shop_name.delete(0, tk.END)
        self.cmb_genre.set('')
        self.cmb_yosan_night_l.set('')
        self.cmb_yosan_night_h.set('')
        self.txt_place_1.delete(0, tk.END)
        self.txt_place_2.delete(0, tk.END)
        self.txt_place_3.delete(0, tk.END)

    def reload(self):
        print('reload')
        area = self.cmb_area.get()
        tdfkn = self.cmb_tdfkn.get()
        score_condition = self.cmb_score_condition.get()
        shop_name = self.txt_shop_name.get().replace(' ', '')
        genre = self.cmb_genre.get()
        only_genre1 = self.bv1.get()
        yosan_night_l = self.cmb_yosan_night_l.get()
        yosan_night_l = const.YOSAN_LIST_L.index(yosan_night_l) + 1
        yosan_night_h = self.cmb_yosan_night_h.get()
        yosan_night_h = const.YOSAN_LIST_H.index(yosan_night_h) + 1
        place1 = self.txt_place_1.get()
        place2 = self.txt_place_2.get()
        place3 = self.txt_place_3.get()
        business_status = self.cmb_buisiness_status.get()
        sort_type = self.cmb_sort_type.get()
        award = self.cmb_award.get()
        meiten = self.cmb_meiten.get()
        special = self.cmb_special.get()
        if tdfkn not in const.TODOFUKEN_LIST:
            return
        print(f'{area} {tdfkn} {score_condition} {shop_name} {genre} {only_genre1} {yosan_night_l} {yosan_night_h} {place1} {place2} {place3} {business_status} {sort_type} {award} {meiten} {special}')
        header_list = list(const.DATA_FLAME_LAYOUT.keys()) + ['URL'] + ['順位変動_str'] + ['点数_str'] + ['点数(増減)_str'] + ['口コミ数(増減)_str'] + ['_merge']
        header_list.remove('No')
        self.df_target, df_total = func.processing_data_frame(
            self.df_small, shop_name, genre, only_genre1, yosan_night_l, yosan_night_h, 
            place1, place2, place3, business_status, sort_type, award, meiten, special
        )
        if special not in ('県別表示', '県別店舗数'):
            self.lbl_title['text'] = f'{const.YEAR}年食べログ {"{:,}".format(len(self.df_target))}件 hit 平均点 {"{:.3f}".format(self.df_target[self.df_target["点数"] != "0.00"]["点数"].astype(float).mean())}点 ' \
                                    f'口コミ数 {"{:,}".format(self.df_target["口コミ数"].astype(int).sum())}件 保存件数 {"{:,}".format(self.df_target["保存件数"].astype(int).sum())}件'
            func.insert_tree(self.tree, pd.concat([self.df_target[0:MAX_ROW_CNT], df_total])[header_list], special)
        else:
            func.insert_tree(self.tree, pd.concat([self.df_target[0:MAX_ROW_CNT], df_total])[header_list], special)

    def widget(self):
        # ウィジェット配置
        self.lbl_title.pack(side=tk.TOP, fill=tk.BOTH)
        self.tree.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.lbl_area.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
        self.cmb_area.pack(side=tk.LEFT, after=self.lbl_area, anchor=tk.W, padx=5, pady=5)
        self.lbl_tdfkn.pack(side=tk.LEFT, after=self.cmb_area, anchor=tk.W, padx=5, pady=5)
        self.cmb_tdfkn.pack(side=tk.LEFT, after=self.lbl_tdfkn, anchor=tk.W, padx=5, pady=5)
        self.lbl_score_condition.pack(side=tk.LEFT, after=self.cmb_tdfkn, anchor=tk.W, padx=5, pady=5)
        self.cmb_score_condition.pack(side=tk.LEFT, after=self.lbl_score_condition, anchor=tk.W, padx=5, pady=5)
        self.lbl_shop_name.pack(side=tk.LEFT, after=self.cmb_score_condition, anchor=tk.W, padx=5, pady=5)
        self.txt_shop_name.pack(side=tk.LEFT, after=self.lbl_shop_name, anchor=tk.W, padx=5, pady=5)
        self.lbl_genre.pack(side=tk.LEFT, after=self.txt_shop_name, anchor=tk.W, padx=5, pady=5)
        self.cmb_genre.pack(side=tk.LEFT, after=self.lbl_genre, anchor=tk.W, padx=5, pady=5)
        self.chk_only_genre1.pack(side=tk.LEFT, after=self.cmb_genre, anchor=tk.W, padx=5, pady=5)
        self.lbl_yosan_night_l.pack(side=tk.LEFT, after=self.chk_only_genre1, anchor=tk.W, padx=5, pady=5)
        self.cmb_yosan_night_l.pack(side=tk.LEFT, after=self.lbl_yosan_night_l, anchor=tk.W, padx=5, pady=5)
        self.lbl_yosan_night_h.pack(side=tk.LEFT, after=self.cmb_yosan_night_l, anchor=tk.W, padx=5, pady=5)
        self.cmb_yosan_night_h.pack(side=tk.LEFT, after=self.lbl_yosan_night_h, anchor=tk.W, padx=5, pady=5)
        self.lbl_place_1.pack(side=tk.LEFT, after=self.cmb_yosan_night_h, anchor=tk.W, padx=5, pady=5)
        self.txt_place_1.pack(side=tk.LEFT, after=self.lbl_place_1, anchor=tk.W, padx=5, pady=5)
        self.lbl_place_2.pack(side=tk.LEFT, after=self.txt_place_1, anchor=tk.W, padx=5, pady=5)
        self.txt_place_2.pack(side=tk.LEFT, after=self.lbl_place_2, anchor=tk.W, padx=5, pady=5)
        self.lbl_place_3.pack(side=tk.LEFT, after=self.txt_place_2, anchor=tk.W, padx=5, pady=5)
        self.txt_place_3.pack(side=tk.LEFT, after=self.lbl_place_3, anchor=tk.W, padx=5, pady=5)
        self.lbl_buisiness_status.pack(side=tk.LEFT, after=self.txt_place_3, anchor=tk.W, padx=5, pady=5)
        self.cmb_buisiness_status.pack(side=tk.LEFT, after=self.lbl_buisiness_status, anchor=tk.W, padx=5, pady=5)
        self.lbl_sort_type.pack(side=tk.LEFT, after=self.cmb_buisiness_status, anchor=tk.W, padx=5, pady=5)
        self.cmb_sort_type.pack(side=tk.LEFT, after=self.lbl_sort_type, anchor=tk.W, padx=5, pady=5)
        self.lbl_award.pack(side=tk.LEFT, after=self.cmb_sort_type, anchor=tk.W, padx=5, pady=5)
        self.cmb_award.pack(side=tk.LEFT, after=self.lbl_award, anchor=tk.W, padx=5, pady=5)
        self.lbl_meiten.pack(side=tk.LEFT, after=self.cmb_award, anchor=tk.W, padx=5, pady=5)
        self.cmb_meiten.pack(side=tk.LEFT, after=self.lbl_meiten, anchor=tk.W, padx=5, pady=5)
        self.lbl_shisetsu.pack(side=tk.LEFT, after=self.cmb_meiten, anchor=tk.W, padx=5, pady=5)
        self.cmb_shisetsu.pack(side=tk.LEFT, after=self.lbl_shisetsu, anchor=tk.W, padx=5, pady=5)
        self.lbl_theme.pack(side=tk.LEFT, after=self.cmb_shisetsu, anchor=tk.W, padx=5, pady=5)
        self.cmb_theme.pack(side=tk.LEFT, after=self.lbl_theme, anchor=tk.W, padx=5, pady=5)
        self.lbl_special.pack(side=tk.LEFT, after=self.cmb_theme, anchor=tk.W, padx=5, pady=5)
        self.cmb_special.pack(side=tk.LEFT, after=self.lbl_special, anchor=tk.W, padx=5, pady=5)

# アプリの実行
f = MouseApp()
f.pack()
f.mainloop()