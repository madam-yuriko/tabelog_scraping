import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import webbrowser
import const
import function as func
import re


# アプリの定義
class MouseApp(tk.Frame):
    # 初期化
    def __init__(self, master=None):
        self.link = ''

        # ★バグ対応用の関数を追加
        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]


        tk.Frame.__init__(self, master, width=720, height=1080)

        # タイトルの表示
        self.master.title('食べログ')

        # ラベルの生成
        self.lbl_title = tk.Label(self, text='食べログ',
                        font=(36, 36),
                        foreground='#ffffff',
                        background='#0000aa')

        # 列加工
        def score_zougen(x):
            x = f'{x:.2f}'
            return f'+{x}' if float(x) > 0 else x

        def kutchikomi_zougen(x):
            return f'+{x}' if x > 0 else str(x)

        # データフレーム取得
        df_all = pd.read_csv(const.get_csv_name(const.YEAR), encoding='utf-8', low_memory=False).fillna('')
        df_all['予算'] = df_all['予算(夜)'].apply(lambda x: const.YOSAN_LIST[x])
        df_last_year = pd.read_csv(const.get_csv_name(const.YEAR - 1), usecols=['ID', '点数', '口コミ数'], encoding='utf-8', low_memory=False).fillna('')
        df_all = pd.merge(df_all, df_last_year, on='ID', how='left', indicator=True)
        df_all.columns = const.MERGE_COL_NAMES
        df_all['点数(増減)'] = (df_all['点数'] - df_all['点数(昨年)'].fillna(0))
        df_all['点数(増減)'] = df_all['点数(増減)'].apply(lambda x: score_zougen(x))
        df_all['口コミ数(増減)'] = (df_all['口コミ数'] - df_all['口コミ数(昨年)'].fillna(0)).astype(int)
        df_all['口コミ数(増減)'] = df_all['口コミ数(増減)'].apply(lambda x: kutchikomi_zougen(x))

        # 県別店数カウント
        # print(df_all[df_all['ステータス'] == '']['都道府県'].value_counts())

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

        # 店名
        self.lbl_shop_name = tk.Label(self, text='店名')
        self.txt_shop_name = tk.Entry(self, width=20)
        self.txt_shop_name.bind('<Return>', lambda event, df=df_all: self.on_enter(df))

        # ジャンル
        self.lbl_genre = tk.Label(self, text='ジャンル')
        self.cmb_genre = ttk.Combobox(self, width=20, height=40, values=const.GENRE_LIST)
        self.cmb_genre.bind('<Return>', lambda event, df=df_all: self.on_enter(df))

        # ジャンル1のみ
        self.bv1 = tk.BooleanVar()
        self.bv1.trace("w", lambda name, index, mode, bv=self.bv1, df=df_all: self.on_text_changed(df_all))
        self.chk_only_genre1 = tk.Checkbutton(self, variable=self.bv1, text='ジャンル1のみ')

        # 予算(夜)
        self.lbl_yosan_night_l = tk.Label(self, text='予算(夜) 下限')
        self.cmb_yosan_night_l = ttk.Combobox(self, width=10, height=30, values=const.YOSAN_LIST_L)
        self.cmb_yosan_night_l.bind('<Return>', lambda event, df=df_all: self.on_enter(df))
        self.lbl_yosan_night_h = tk.Label(self, text='上限')
        self.cmb_yosan_night_h = ttk.Combobox(self, width=10, height=30, values=const.YOSAN_LIST_H)
        self.cmb_yosan_night_h.bind('<Return>', lambda event, df=df_all: self.on_enter(df))

        # 所在地、施設名、最寄り駅
        self.lbl_place_1 = tk.Label(self, text='場所1')
        self.txt_place_1 = tk.Entry(self, width=20)
        self.txt_place_1.bind('<Return>', lambda event, df=df_all: self.on_enter(df))
        self.lbl_place_2 = tk.Label(self, text='場所2')
        self.txt_place_2 = tk.Entry(self, width=20)
        self.txt_place_2.bind('<Return>', lambda event, df=df_all: self.on_enter(df))
        self.lbl_place_3 = tk.Label(self, text='場所3')
        self.txt_place_3 = tk.Entry(self, width=20)
        self.txt_place_3.bind('<Return>', lambda event, df=df_all: self.on_enter(df))

        # 閉店・移転
        self.bv2 = tk.BooleanVar()
        self.bv2.trace("w", lambda name, index, mode, bv=self.bv2, df=df_all: self.on_text_changed(df_all))
        self.chk_heiten = tk.Checkbutton(self, variable=self.bv2, text='閉店/移転/休業/掲載保留を含む')

        # 口コミ数順
        self.bv3 = tk.BooleanVar()
        self.bv3.trace("w", lambda name, index, mode, bv=self.bv3, df=df_all: self.on_text_changed(df_all))
        self.chk_kuchikomi_sort = tk.Checkbutton(self, variable=self.bv3, text='口コミ数順でソート')

        # 食べログアワード
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_text_changed(df_all))
        self.lbl_award = tk.Label(self, text='食べログアワード')
        self.cmb_award = ttk.Combobox(self, width=20, textvariable=sv, height=20, values=const.AWARD_LIST)

        # 百名店
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_text_changed(df_all))
        self.lbl_meiten = tk.Label(self, text='百名店')
        self.cmb_meiten = ttk.Combobox(self, width=20, textvariable=sv, height=30, values=const.MEITEN_LIST)

        # 商業施設
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_text_changed(df_all, 'shisetsu'))
        self.lbl_shisetsu = tk.Label(self, text='商業施設')
        self.cmb_shisetsu = ttk.Combobox(self, width=20, textvariable=sv, height=30, values=list(const.SHISETSU_DICT.keys()))

        # その他条件
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv, df=df_all: self.on_text_changed(df))
        self.lbl_special = tk.Label(self, text='その他')
        self.cmb_special = ttk.Combobox(self, width=20, height=30, textvariable=sv, values=const.SPECIAL_LIST)

        # ツリー
        self.tree = ttk.Treeview(self)
        self.tree['height'] = const.VIEW_ROW_CNT
        self.tree["column"] = list(const.DATA_FLAME_LAYOUT.keys())
        self.tree["show"] = "headings"
        [self.tree.heading(k, text=k) for k in const.DATA_FLAME_LAYOUT.keys()]
        [self.tree.column(k, width=v[0], anchor=v[1]) for k, v in const.DATA_FLAME_LAYOUT.items()]
        self.tree.bind("<Double-1>", self.hyper_link)
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_select(event))

        # スクロールバー
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill="y")
        self.tree.pack()
        self.tree["yscrollcommand"] = scroll.set

        # ウィジェット配置
        self.widget()

        # ★バグ対応を処理
        style = ttk.Style()
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
        style.configure("Treeview", font=("Arial", 11, 'bold'), rowheight=28)

        self.reload(df_all)


    def hyper_link(self, event):
        webbrowser.open(self.link)

    def on_tree_select(self, event):
        if len(self.tree.selection()) != 0:
            select = self.tree.selection()[0]
            no = int(self.tree.set(select)['No']) - 1
            self.link = self.df_target.iloc[no].URL

    def on_text_changed(self, df_all, name=''):
        print(name)
        if name == 'area' and self.cmb_area.get() != '':
            self.cmb_tdfkn.set('')
        elif name == 'tdfkn' and self.cmb_tdfkn.get() != '':
            self.cmb_area.set('')
        elif name == 'shisetsu':
            if self.cmb_shisetsu.get() == '':
                self.all_reset(df_all)
            else:
                self.txt_place_1.delete(0, tk.END)
                self.txt_place_2.delete(0, tk.END)
                self.txt_place_3.delete(0, tk.END)
                shisetsu = const.SHISETSU_DICT[self.cmb_shisetsu.get()]
                if shisetsu:
                    self.txt_shop_name.delete(0, tk.END)
                    for k, v in shisetsu.items():
                        if k == '場所1':
                            self.txt_place_1.delete(0, tk.END)
                            self.txt_place_1.insert(tk.END, v)
                        elif k == '場所2':
                            self.txt_place_2.delete(0, tk.END)
                            self.txt_place_2.insert(tk.END, v)
                        elif k == '場所3':
                            self.txt_place_3.delete(0, tk.END)
                            self.txt_place_3.insert(tk.END, v)
        self.reload(df_all)

    def on_enter(self, df_all):
        self.reload(df_all)

    def all_reset(self, df_all):
        print('all_reset()')
        self.cmb_area.set('')
        self.cmb_tdfkn.set('')
        self.txt_shop_name.delete(0, tk.END)
        self.cmb_genre.set('')
        self.cmb_yosan_night_l.set('')
        self.cmb_yosan_night_h.set('')
        self.txt_place_1.delete(0, tk.END)
        self.txt_place_2.delete(0, tk.END)
        self.txt_place_3.delete(0, tk.END)
        self.cmb_award.set('')
        self.cmb_meiten.set('')

    def reload(self, df_all):
        print('reload')
        area = self.cmb_area.get()
        tdfkn = self.cmb_tdfkn.get()
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
        heiten = self.bv2.get()
        kuchikomi_sort = self.bv3.get()
        award = self.cmb_award.get()
        meiten = self.cmb_meiten.get()
        special = self.cmb_special.get()
        if tdfkn not in const.TODOFUKEN_LIST:
            return
        print(f'{area} {tdfkn} {shop_name} {genre} {only_genre1} {yosan_night_l} {yosan_night_h} {place1} {place2} {place3} {heiten} {kuchikomi_sort} {award} {meiten} {special}')
        header_list = list(const.DATA_FLAME_LAYOUT.keys()) + ['URL']+['_merge']
        header_list.remove('No')
        self.df_target = func.processing_data_frame(
            df_all, area, tdfkn, shop_name, genre, only_genre1, yosan_night_l, yosan_night_h, 
            place1, place2, place3, heiten, kuchikomi_sort, award, meiten, special)[header_list]
        self.lbl_title['text'] = f'食べログ {"{:,}".format(len(self.df_target))}件 hit 平均点 {"{:.3f}".format(self.df_target[self.df_target["点数"] != "-"]["点数"].astype(float).mean())}点 口コミ数 {"{:,}".format(self.df_target["口コミ数"].sum())}件 保存件数 {"{:,}".format(self.df_target["保存件数"].sum())}件'
        func.insert_tree(self.tree, self.df_target)

    def widget(self):
        # ウィジェット配置
        self.lbl_title.pack(side=tk.TOP, fill=tk.BOTH)
        self.tree.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.lbl_area.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
        self.cmb_area.pack(side=tk.LEFT, after=self.lbl_area, anchor=tk.W, padx=5, pady=5)
        self.lbl_tdfkn.pack(side=tk.LEFT, after=self.cmb_area, anchor=tk.W, padx=5, pady=5)
        self.cmb_tdfkn.pack(side=tk.LEFT, after=self.lbl_tdfkn, anchor=tk.W, padx=5, pady=5)
        self.lbl_shop_name.pack(side=tk.LEFT, after=self.cmb_tdfkn, anchor=tk.W, padx=5, pady=5)
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
        self.chk_heiten.pack(side=tk.LEFT, after=self.txt_place_3, anchor=tk.W, padx=5, pady=5)
        self.chk_kuchikomi_sort.pack(side=tk.LEFT, after=self.chk_heiten, anchor=tk.W, padx=5, pady=5)
        self.lbl_award.pack(side=tk.LEFT, after=self.chk_kuchikomi_sort, anchor=tk.W, padx=5, pady=5)
        self.cmb_award.pack(side=tk.LEFT, after=self.lbl_award, anchor=tk.W, padx=5, pady=5)
        self.lbl_meiten.pack(side=tk.LEFT, after=self.cmb_award, anchor=tk.W, padx=5, pady=5)
        self.cmb_meiten.pack(side=tk.LEFT, after=self.lbl_meiten, anchor=tk.W, padx=5, pady=5)
        self.lbl_shisetsu.pack(side=tk.LEFT, after=self.cmb_meiten, anchor=tk.W, padx=5, pady=5)
        self.cmb_shisetsu.pack(side=tk.LEFT, after=self.lbl_shisetsu, anchor=tk.W, padx=5, pady=5)
        self.lbl_special.pack(side=tk.LEFT, after=self.cmb_shisetsu, anchor=tk.W, padx=5, pady=5)
        self.cmb_special.pack(side=tk.LEFT, after=self.lbl_special, anchor=tk.W, padx=5, pady=5)
                 
# アプリの実行
f = MouseApp()
f.pack()
f.mainloop()