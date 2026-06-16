import re
import os

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

idx_news = html.find("<!-- NEWS -->")
idx_vote = html.find("<!-- ガチ投票 セクション (Firebase) -->")
idx_ref = html.find("<!-- REFERENCES -->")
idx_footer = html.find("<!-- Footer -->")

if -1 in [idx_news, idx_vote, idx_ref, idx_footer]:
    print("Could not find sections")
    exit(1)

head_part = html[:idx_news]
vote_part = html[idx_vote:idx_ref]
footer_part = html[idx_footer:]

react_scripts = """
    <!-- React & Babel -->
    <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
    <script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
"""

head_part = head_part.replace("</head>", react_scripts + "\n</head>")

react_root_main = """    <div id="react-root-main"></div>\n\n"""

react_root_refs_and_script = """    <div id="react-root-refs"></div>

    <script type="text/babel">
        const DATA = {
            news: [
                { date: "2026.06.16", icon: "fa-triangle-exclamation", color: "text-red-400", title: "第3話公開", text: "佐々木・相沢が殺害される。ダイイングメッセージと100万円盗難事件が発生し、殺人鬼はだいにメンバー内にいることが確定した。", link: "#story" },
                { date: "2026.06.06", icon: "fa-triangle-exclamation", color: "text-red-400", title: "第2話公開", text: "第2の事件発生。スナック前で黒崎凛が殺害。数々の秘密が露呈。", link: "#story" },
                { date: "2026.05.30", icon: "fa-video", color: "text-gray-400", title: "第1話公開", text: "第1の事件（清掃員・田中芳子殺害）のアリバイデータを格納。", link: "#incidents" }
            ],
            story: [
                { title: "プロローグ: ゲームの幕開け", time: "DAY 1 - 14:00", text: "雪山の奥深くに佇むホテル「山幸閣」に集められた参加者たち。突如告げられた連続殺人ゲーム。吹雪で完全孤立する中、メンバーは金庫から自身の役職を確認し、探索を開始する。", isIncident: false },
                { title: "第1の事件: 清掃員・田中芳子殺害", time: "DAY 1 - 15:50頃発見", text: "別館のエレベーター内で清掃員・田中芳子の遺体が発見される。死因は絞殺。エレベーター内には掃除機のコードが目いっぱい引っ張り出された状態の掃除機が一緒に残されていた。第1回緊急集会が開かれ、全員のアリバイが検証される。", isIncident: true },
                { title: "第2の事件: 三女・黒崎凛殺害", time: "DAY 1 - 18:25頃発見", text: "本館1階スナック（クラブアルカディア）前の廊下で黒崎凛が殺害される。死因は絞殺（首に索状痕）。集会では、参加者たちが隠していたパパ活関係、不倫関係、週刊誌ライターとしての素性、そして支配人が遺産を狙う「神谷家の一族」であるという凄まじい裏事情が暴露される。", isIncident: true },
                { title: "第3・第4の事件と100万円盗難", time: "DAY 2", text: "第3の事件で佐々木、第4の事件で相沢が殺害される。相沢は血文字のダイイングメッセージを残していた。さらに岩田が手に入れた100万円が盗まれる事件が発生。公式より『殺人鬼はだいにぐるーぷ内の1人』と明言され、メンバー同士の疑心暗鬼が加速する。", isIncident: true }
            ],
            characters: {
                daini: [
                    { name: "岩田", room: "本館 303", role: "検視官", roleColor: "text-ice", roleBg: "border-ice/50 bg-ice/10", items: "手帳、黒いペン、ライト、時計、館内マップ", desc: "能力①死体の第一発見者になると正確な死亡時刻と最後に話した人物が判明。②死亡者の部屋に入り正体（金庫の中身）を知れる。部屋から出るとすぐ渡り廊下。" },
                    { name: "飯野", room: "本館 215", role: "不明", roleColor: "text-gray-300", roleBg: "border-gray-600 bg-gray-800", items: "手帳、青い三色ペン、ライト、？？", desc: "視点映像が少なく行動が見えにくい。全事件（第1〜第4）でアリバイがない。しかし「頻繁に部屋にいる・ゴミ箱を覗く」などの描写から、「部屋待機型・情報収集系の役職」であり、あえて怪しく見せているミスリード要員説が視聴者の間で濃厚。" },
                    { name: "西尾", room: "本館 205", role: "特殊役職？", roleColor: "text-yellow-500", roleBg: "border-yellow-600/50 bg-yellow-900/20", items: "手帳、青三色ペン、ライト、養生テープ？、巾着(水色レコーダー？)", desc: "金庫確認時、封筒が上。別館EV内で検証？館内に養生テープを貼る。養生テープを堂々と貼る行動から、視聴者考察では「鑑識」の役職でほぼ確定と見られている。独白から殺人鬼や協力者ではないと推測されている。" },
                    { name: "土井谷", room: "別館 401", role: "予言者？", roleColor: "text-gray-300", roleBg: "border-gray-600 bg-gray-800", items: "手帳、水色と黒のペン、ライト、時計、？？", desc: "凛殺害前に２F階段から廊下奥へ移動した謎の行動。夜、支配人の林太郎が土井谷の部屋を訪れた疑惑がある。佐々木を探し「バレたくない」と発言したことや、ボイラー室への出入りから、「予言者（占い師）」系の役職と推測される。また、林太郎と裏で繋がっている可能性が非常に高い。" },
                    { name: "須藤", room: "別館 502", role: "不明", roleColor: "text-gray-300", roleBg: "border-gray-600 bg-gray-800", items: "手帳、ペン、ライト、？？", desc: "金庫に「探偵みたいなの入ってる」と発言。渡り廊下の様子を伺う。独白から殺人鬼や協力者ではないと推測されている。第1、第2事件でアリバイが不透明かつ、相沢の最後の目撃者。白井と密談しており、100万円を盗んだ泥棒（共犯）の可能性が高い。殺人鬼の本命候補としても疑われている。" }
                ],
                hotel: [
                    { name: "黒崎 恒一", room: "別館 612", type: "オーナー", desc: "足が悪い。このホテル以外に2つホテルを持っている資産家。", isVictim: false },
                    { name: "黒崎 林太郎", room: "別館 601", type: "支配人 (入り婿)", desc: "由美子の夫。旧姓神谷。学歴・経歴を詐称して遺産を狙う戦略結婚。", isVictim: false },
                    { name: "黒崎 由美子", room: "別館 602", type: "長女 / スタッフ", desc: "掃除機の場所を知らなかった。林太郎の身辺調査を探偵に依頼。", isVictim: false },
                    { name: "黒崎 凛", room: "別館 611", type: "三女 / スタッフ", desc: "【第2の被害者】佐々木とパパ活。姉から計画を聞き遺産争いの渦中に。", isVictim: true },
                    { name: "田中 芳子", room: "別館 610", type: "清掃員", desc: "【第1の被害者】宿泊客のゴミを漁り、ホテルの裏事情を最もよく知る。", isVictim: true }
                ],
                guests: [
                    { name: "佐々木 清", room: "本館 201", type: "常連客", desc: "オーナーと仲が良い。凛と頻繁に会っていた（パパ活発覚）。【第3の被害者】", isVictim: true },
                    { name: "相沢 健二", room: "本館 306", type: "週刊誌ライター", desc: "小説家は偽り。ホテルに1ヶ月滞在。黒崎家の相続問題を追っている。【第4の被害者】", isVictim: true },
                    { name: "高橋 宏 / 中村 美咲", room: "本館 213", type: "不倫関係", desc: "新婚夫婦と偽る。会社が厳しいためカメラに映るのを極端に嫌がる。", isVictim: false },
                    { name: "悠斗", room: "別館 402", type: "スノーボーダー / 神谷家親戚", desc: "左利き。神谷家の親戚であることを隠して滞在。", isVictim: false },
                    { name: "リオ", room: "別館 405", type: "インフルエンサー / 神谷家親戚", desc: "神谷家の親戚であることを隠して滞在。常に動画を回している。", isVictim: false },
                    { name: "白井 玲司", room: "別館 501", type: "謎の男", desc: "自称東京出身。常に無言。由美子が雇った「探偵」説が有力。", isVictim: false }
                ]
            },
            incidents: [
                {
                    id: 1,
                    title: "第1の犠牲者：田中芳子",
                    summary: "別館のエレベーター内。死因：絞殺。第一発見者：飯野（15:50位）。殺害時刻：15:44過ぎ～15:50前？エレベーター内で掃除機（コードが目いっぱい出た状態）と一緒に発見。",
                    events: [
                        "15:43 渡り廊下で支配人、相沢とすれ違う。",
                        "15:44 別館EV前で田中と遭遇。田中がEVボタンを押す。",
                        "15:46 別館4F階段側で岩田、西尾と話す。",
                        "15:47 別館5Fで凛とすれ違う。",
                        "15:48 窓際で飯野と会話。飯野は6Fへ。",
                        "15:50 叫び声。6Fへ。飯野がEV前で死体発見。"
                    ],
                    alibis: [
                        { name: "リオ", status: "safe", desc: "カメラ動画の通り。犯行はほぼ不可能。" },
                        { name: "佐々木", status: "danger", desc: "15:40喫煙所。ロビーを通り自室201で仮眠。" },
                        { name: "高橋夫妻", status: "safe", desc: "ロビーでパンフレット。15:55に顔はめパネルで土井谷が撮影。" },
                        { name: "相沢", status: "safe", desc: "ロビーから3Fへ。食堂前で支配人と合流し1Fロビーへ。完璧なアリバイ。" },
                        { name: "林太郎", status: "safe", desc: "シーツ交換で田中と3Fで会話。相沢と合流しロビーへ(15:43カメラ)。" },
                        { name: "白井", status: "danger", desc: "ロビーに一瞬。階段に無言で立つ。喫煙所前の椅子に座る。" },
                        { name: "恒一(オーナー)", status: "danger", desc: "自室で休憩。由美子の叫び声で出る。" },
                        { name: "悠斗", status: "danger", desc: "死体発見時、別館5F廊下で目撃される。証言と行動の不一致。" },
                        { name: "飯野", status: "danger", desc: "別館探索。15:48 リオと会話後6Fへ。EVを呼んで死体発見（15:50）。" },
                        { name: "岩田", status: "danger", desc: "15:30 6Fへ。5Fで凛と会話。4Fでリオ、西尾と会話。3Fで飯野とすれ違う。死体発見時は2F？" },
                        { name: "西尾・須藤", status: "safe", desc: "死体発見時、須藤と一緒に喫煙所に。" }
                    ]
                },
                {
                    id: 2,
                    title: "第2の犠牲者：黒崎凛",
                    summary: "本館1Fスナック前の廊下。死因：絞殺（索状痕）。第一発見者：佐々木（18:25位）。殺害時刻：18:20頃？",
                    events: [
                        "17:30 佐々木清が夕食を早く切り上げて退席。その後別館6階へ行きすぐ戻る。",
                        "18:10位、凛が生きているのを目撃（白井、リオ、林太郎、須藤、西尾）。",
                        "18:10位、大浴場前。女性用大浴場の電気がついていなかった。（リオ、高橋、西尾）",
                        "18:15位 飯野が喫煙所の猫を見ている姿を目撃される。",
                        "18:20位～ 男湯にて高橋宏、飯野、西尾が一緒に入浴。",
                        "18:25位 佐々木がトイレに行こうとしたらスナック前で死体を発見。"
                    ],
                    alibis: [
                        { name: "佐々木", status: "danger", desc: "17:30に6Fへ。凛とEVで抱き合う？トイレへ向かい死体発見(18:25)。" },
                        { name: "恒一(オーナー)", status: "danger", desc: "夕食後、部屋でぼーっと。" },
                        { name: "白井", status: "danger", desc: "18:10凛生存目撃。喫煙所で猫を見る。岩田の気配を感じ逃げる。" },
                        { name: "相沢", status: "safe", desc: "自室306で土井谷と雑談。" },
                        { name: "大浴場組", status: "safe", desc: "リオ、宏、美咲、西尾。18:20〜大浴場内でアリバイ。" },
                        { name: "林太郎", status: "safe", desc: "18:10凛生存目撃。死体発見時は食堂に途中から加わる。" },
                        { name: "須藤・悠斗", status: "safe", desc: "30分前から食堂に同席。" },
                        { name: "土井谷", status: "safe", desc: "林太郎が部屋を訪れた？その後相沢と306で雑談。" },
                        { name: "飯野", status: "danger", desc: "18時後、2Fで凛と遭遇。18:20〜男湯。自室215で叫び声を聞く。" },
                        { name: "岩田", status: "danger", desc: "18時から食堂。6F〜4Fを見回り。3Fで佐々木の叫び声を聞き合流。" }
                    ]
                },
                {
                    id: 3,
                    title: "第3の犠牲者：佐々木清",
                    summary: "死因不明。最終目撃は21:15、遺体発見は翌朝11:15。",
                    events: [
                        "犯行可能時間が長すぎるため、アリバイ検証は困難。"
                    ],
                    alibis: []
                },
                {
                    id: 4,
                    title: "第4の犠牲者：相沢健二",
                    summary: "死因不明。殺害時刻は「14:30〜15:30」の間。",
                    events: [
                        "14:00に須藤が目撃し、14:30に林太郎が確認時は異常なし。",
                        "15:30に遺体発見。殺害時刻は「14:30〜15:30」の間。"
                    ],
                    alibis: [
                        { name: "土井谷", status: "danger", desc: "アリバイなし。" },
                        { name: "飯野", status: "danger", desc: "アリバイなし。" },
                        { name: "西尾", status: "danger", desc: "アリバイなし。" }
                    ]
                }
            ],
            clues: [
                { title: "犯人が使ったアリバイトリック", text: "田中芳子は発見時に本当に死んでいたのか？「首を絞められて死亡した」と発表したのは支配人。気絶していただけで、全員が大広間へ移動した後に殺害することも理論上は可能。このトリックを実行できるのは支配人・黒崎林太郎。" },
                { title: "支配人が401号室に入った理由", text: "夜のシーンでは支配人がどこかの部屋へ入っていく描写がありました。ホテルの見取り図を検証すると、その部屋は土井谷の401号室とのこと。なぜ入ったのかは不明ですが、今後の重要な伏線である可能性があります。" },
                { title: "黒崎凛は何を見てしまったのか", text: "殺害前、黒崎凛は庭園を見ていました。相沢は廊下で「回収されてたか」と呟いています。日中の庭園付近には白井がいました。「白井は何かを監視していた」「黒崎凛がそれを目撃した」「その結果、口封じされた」という流れが見えてきます。" },
                { title: "白井の正体は探偵？", text: "白井＝探偵説。由美子は夫である林太郎を疑い、探偵に調査を依頼していました。その探偵こそ白井ではないかと考えられます。もしそうなら白井の怪しい監視行動にも説明がつきます。" },
                { title: "大浴場の消灯は伏線なのか", text: "気になる描写として、女性側大浴場の電気が消えていたシーンがあります。黒崎凛が通過した後に電気が消えています。暗闇に紛れて犯行の準備をしていた可能性が考えられます。" },
                { title: "相沢が情報を操作している可能性", text: "現状では提供された情報はすべて正しいように見えますが、岩田が得ている情報の多くは相沢（ライター）からです。情報源が一人に集中している以上、岩田も視聴者も誘導されている可能性があります。不倫の情報を広めていたのも相沢です。" },
                { title: "飯野さんの不可解な行動", text: "飯野さんは視点映像がかなり少なく、行動が見えにくい人物です。特に気になったのは夜9時頃の2階での行動。エレベーター横付近で何かをしているシーンが映っていました。" },
                { title: "肝試しシーンの意味", text: "高橋がホテル内で肝試しをしている場面で、黒崎由美子と遭遇します。わざわざ映像で見せている以上、この出会いにも意味があるはずです。伏線として回収される可能性は高そうです。" },
                { title: "相沢のダイイングメッセージ", text: "台に椅子が2脚ある描写から「第2（だいに2）」つまり「西尾」を指しているという鋭い考察が存在する。公式でこのメッセージは「真実」と語られている。" },
                { title: "100万円盗難の真相", text: "だいにの誰かが鍵を見つけ、相沢に目撃させ、後に白井と協力して100万円を盗むシナリオが疑われている。須藤か土井谷が怪しい。" },
                { title: "隠し通路と車椅子の謎", text: "渡り廊下裏の「車椅子」が遺体運搬に使われた可能性や、「従業員専用の隠し通路」の存在が示唆されている。これが事実なら既存のアリバイはすべて覆る。" }
            ],
            references: [
                { title: "【だいにぐるーぷ リアル人狼】エピソード3 サツ人鬼は須藤＆伏線シーンまとめ。第3話ネタバレ感想＆伏線・ドラマ考察。雪山ホテルをカメラ60台で3日間記録した連続殺人ゲーム。", author: "んごミック 様", twitter: "@utaitengo0312", url: "https://note.com/utaitengo0312/n/n4444c7c3c862" },
                { title: "【リアル人狼】犯人が使ったアリバイトリック。第1話ネタバレ感想＆伏線・ドラマ考察。雪山ホテルをカメラ60台で3日間記録した連続殺人ゲーム。出演者：だいにぐるーぷ、他。", author: "んごミック 様", twitter: "@utaitengo0312", url: "https://note.com/utaitengo0312/n/n024031531e95" },
                { title: "【だいにぐるーぷ リアル人狼】エピソード2サツ人鬼の伏線・意味深シーンまとめ。第2話ネタバレ感想＆伏線・ドラマ考察。雪山ホテルをカメラ60台で3日間記録した連続殺人ゲーム。", author: "んごミック 様", twitter: "@utaitengo0312", url: "https://note.com/utaitengo0312/n/n563f2e758c96" },
                { title: "だいにぐるーぷ「殺人ゲーム」、Ep2で早くも個人の秘密が色々判明したのは意外。終盤はメンバー同士の争いが焦点になるのかも。とりあえずEp1,Ep2個人的まとめメモを公開。", author: "ヨン_kikyosan 様", twitter: "@yon_kikyosan", url: "https://fusetter.com/tw/RJXQX6ld" }
            ]
        };

        const SectionTitle = ({ title, subtitle }) => (
            <div className="text-center mb-12">
                <h2 className="text-3xl font-bold section-title tracking-widest">{title}</h2>
                <p className="text-gray-400 mt-2 text-sm tracking-widest">{subtitle}</p>
            </div>
        );

        const AppMain = () => {
            return (
                <React.Fragment>
                    {/* NEWS */}
                    <section id="news" className="py-12 bg-dark border-b border-gray-900">
                        <div className="max-w-4xl mx-auto px-4">
                            <div className="flex flex-col md:flex-row items-start md:items-center">
                                <h2 className="text-blood font-bold text-xl tracking-widest mr-8 mb-4 md:mb-0 shrink-0">NEWS</h2>
                                <ul className="space-y-3 w-full">
                                    {DATA.news.map((item, idx) => (
                                        <li key={idx} className="flex flex-col sm:flex-row sm:items-center border-b border-gray-800 pb-2">
                                            <span className="text-gray-500 text-sm w-32 shrink-0">{item.date}</span>
                                            <span className={`${item.color} font-bold mr-3 shrink-0`}><i className={`fa-solid ${item.icon}`}></i> {item.title}</span>
                                            <a href={item.link} className="hover:text-blood transition-colors line-clamp-1">{item.text}</a>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </section>

                    {/* INTRODUCTION */}
                    <section id="intro" className="py-20 bg-darker">
                        <div className="max-w-6xl mx-auto px-4 text-center">
                            <h2 className="text-3xl font-bold section-title tracking-widest">INTRODUCTION</h2>
                            <p className="text-gray-400 mb-12 text-sm tracking-widest">作品概要・ルール・ホテルの構造</p>
                            
                            <div className="bg-gray-900/50 border border-gray-800 p-8 rounded-lg text-left leading-relaxed space-y-6 mb-8">
                                <p className="text-gray-300">
                                    だいにぐるーぷのメンバーたちが長野県の雪山にあるホテルへ宿泊。しかし滞在中に殺人事件が発生します。吹雪によって警察が到着するのは2日後の朝。それまでに参加者たちはホテル内に潜む殺人鬼を見つけなければなりません。<br/>
                                    さらに、だいにぐるーぷのメンバーにはそれぞれ役職が与えられており、自分の役職を最も悟られなかった人物には賞金が与えられるというルール。視聴者は事件の真相と各メンバーの役職を推理しながら楽しむことができます。
                                </p>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
                                    <div className="bg-dark p-6 border-l-4 border-ice rounded-r">
                                        <h3 className="text-xl font-bold mb-4 flex items-center text-ice"><i className="fa-solid fa-building mr-2"></i> ホテルの構造データ</h3>
                                        <ul className="list-disc list-inside text-gray-400 space-y-2 text-sm">
                                            <li>本館1～3Fにエレベーター（使用禁止の貼り紙）、別館3～6Fにエレベーター稼働。</li>
                                            <li>両館は3Fの渡り廊下で繋がっている。渡り廊下の途中に喫煙所。</li>
                                            <li>別館はどの階も同じ構造。各階の奥には「非常時以外開放厳禁」の扉があり外へ出られる。</li>
                                            <li>6Fの客室はオーナー家族と従業員用。EV脇に白いポットと黒い電子レンジ。</li>
                                            <li>5FのEV脇に黒い電子レンジ。4FのEV脇に白い電子レンジとポット、廊下にソファー。</li>
                                            <li>3Fに大食堂と小食堂（別館EV前）。食事は小食堂で取る。</li>
                                            <li>2Fに男女大浴場とボイラー室。</li>
                                            <li>1Fにクラブアルカディア（19:00～21:00営業）。</li>
                                            <li>本館に非常用の裏階段あり（1〜3階の廊下端に接続）。</li>
                                        </ul>
                                    </div>
                                    <div className="bg-dark p-6 border-l-4 border-blood rounded-r">
                                        <h3 className="text-xl font-bold mb-4 flex items-center text-red-400"><i className="fa-solid fa-mask mr-2"></i> ホテルの不審な点・秘密</h3>
                                        <ul className="list-disc list-inside text-gray-400 space-y-2 text-sm">
                                            <li>女性側大浴場の電気が消えていた時間帯があった。</li>
                                            <li>別館エレベーター6F横の時計は一切動いていない。</li>
                                            <li>603号室の謎：夜ドアが少し開いて電気が点き、水と紙と何かが置いてある。</li>
                                            <li>第2回緊急会議後、食堂前で岩田と由美子がすれ違う（由美子はカレー所持）。岩田はその後空の皿を持っていた謎。</li>
                                            <li>支配人・林太郎はパリッとした恰好だが、娘姉妹はエプロン。由美子は掃除機の場所すら知らない。</li>
                                            <li>凛は「三女」。姉がもう一人いるはずだが、黒崎家の誰もそれに触れない。</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <p className="text-xs text-gray-600 text-right">【引用元：んごミック 様 / ヨン_kikyosan 様】</p>
                        </div>
                    </section>

                    {/* STORY */}
                    <section id="story" className="py-20 bg-dark">
                        <div className="max-w-5xl mx-auto px-4 text-center">
                            <h2 className="text-3xl font-bold section-title tracking-widest">STORY</h2>
                            <p className="text-gray-400 mb-12 text-sm tracking-widest">これまでの展開（100%正確な事実記録）</p>

                            <div className="space-y-8 text-left relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-700 before:to-transparent">
                                {DATA.story.map((item, idx) => (
                                    <div key={idx} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
                                        <div className={`flex items-center justify-center w-10 h-10 rounded-full border-4 border-dark ${item.isIncident ? 'bg-blood text-white' : 'bg-gray-800 text-gray-400'} font-bold shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow z-10`}>
                                            {item.isIncident ? <i className="fa-solid fa-skull"></i> : idx}
                                        </div>
                                        <div className={`w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-lg ${item.isIncident ? 'bg-red-950/10 border-blood/30 hover:border-blood/60' : 'bg-gray-900/80 border-gray-800 hover:border-gray-600'} border transition duration-300`}>
                                            <div className="flex items-center justify-between mb-1">
                                                <h3 className={`font-bold text-lg ${item.isIncident ? 'text-red-200' : 'text-white'}`}>{item.title}</h3>
                                                <span className={`text-xs ${item.isIncident ? 'text-red-400' : 'text-gray-500'} font-mono`}>{item.time}</span>
                                            </div>
                                            <p className={`${item.isIncident ? 'text-gray-300' : 'text-gray-400'} text-sm leading-relaxed`}>
                                                {item.text}
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </section>

                    {/* CAST */}
                    <section id="cast" className="py-20 bg-darker">
                        <div className="max-w-7xl mx-auto px-4 text-center">
                            <h2 className="text-3xl font-bold section-title tracking-widest">CAST & ROLES</h2>
                            <p className="text-gray-400 mb-12 text-sm tracking-widest">登場人物一覧・初期装備データ</p>

                            <h3 className="text-lg font-bold text-left border-l-4 border-gray-500 pl-3 mb-6 text-gray-300"><i className="fa-solid fa-users mr-2"></i>参加者 (だいにぐるーぷ)</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-12 text-left">
                                {DATA.characters.daini.map((c, i) => (
                                    <div key={i} className="bg-dark border border-gray-800 p-5 rounded">
                                        <h4 className="font-bold text-white text-lg mb-2">{c.name} ［{c.room}］</h4>
                                        <span className={`inline-block text-xs border ${c.roleBg} ${c.roleColor} px-2 py-1 rounded mb-3`}>役職: {c.role}</span>
                                        <p className="text-xs text-gray-400 mb-2"><strong>初期装備:</strong> {c.items}</p>
                                        <p className="text-sm text-gray-500 leading-relaxed">{c.desc}</p>
                                    </div>
                                ))}
                            </div>

                            <h3 className="text-lg font-bold text-left border-l-4 border-blood pl-3 mb-6 text-gray-300"><i className="fa-solid fa-bell-concierge mr-2"></i>ホテル関係者 (山幸閣・黒崎家)</h3>
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-12 text-left">
                                {DATA.characters.hotel.map((c, i) => (
                                    <div key={i} className={`${c.isVictim ? 'bg-red-950/20 border-blood/50' : 'bg-dark border-gray-800'} border p-4 rounded relative`}>
                                        {c.isVictim && <div className="absolute -top-2 -right-2 bg-blood text-white text-[10px] font-bold px-2 py-1 rounded rotate-12">被害者</div>}
                                        <h4 className={`font-bold ${c.isVictim ? 'text-red-300' : 'text-white'} mb-1`}>{c.name} ［{c.room}］</h4>
                                        <p className="text-xs text-red-400 mb-2">{c.type}</p>
                                        <p className={`text-xs ${c.isVictim ? 'text-gray-400' : 'text-gray-500'}`}>{c.desc}</p>
                                    </div>
                                ))}
                            </div>

                            <h3 className="text-lg font-bold text-left border-l-4 border-yellow-600 pl-3 mb-6 text-gray-300"><i className="fa-solid fa-suitcase mr-2"></i>宿泊客</h3>
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-left">
                                {DATA.characters.guests.map((c, i) => (
                                    <div key={i} className="bg-dark border border-gray-800 p-4 rounded">
                                        <h4 className="font-bold text-white mb-1">{c.name} ［{c.room}］</h4>
                                        <p className="text-xs text-yellow-500 mb-2">{c.type}</p>
                                        <p className="text-sm text-gray-500">{c.desc}</p>
                                    </div>
                                ))}
                            </div>
                            <p className="text-xs text-gray-600 text-right mt-4">【引用元：ヨン_kikyosan 様 / んごミック 様】</p>
                        </div>
                    </section>

                    {/* INCIDENTS */}
                    <section id="incidents" className="py-20 px-4 max-w-6xl mx-auto">
                        <SectionTitle title="INCIDENTS & ALIBI" subtitle="事件の詳細と全アリバイ証言" />
                        
                        <div className="space-y-12 text-left">
                            {DATA.incidents.map((incident, i) => (
                                <div key={i} className="bg-dark border border-blood/40 rounded-lg overflow-hidden shadow-2xl">
                                    <div className="bg-gradient-to-r from-red-950/40 to-transparent p-5 border-b border-red-900/40">
                                        <h3 className="text-xl font-bold text-red-200"><i className="fa-solid fa-skull text-red-600 mr-3"></i>{incident.title}</h3>
                                        <p className="text-sm text-gray-300 mt-2">{incident.summary}</p>
                                    </div>
                                    <div className="p-6">
                                        <div className="mb-6 bg-gray-900/50 p-4 rounded border border-gray-800">
                                            <h4 className="font-bold text-sm text-ice mb-3"><i className="fa-solid fa-clock mr-2"></i>直前の動向・時系列</h4>
                                            <ul className="space-y-1 text-sm text-gray-400 font-mono">
                                                {incident.events.map((ev, idx) => <li key={idx}>・{ev}</li>)}
                                            </ul>
                                        </div>
                                        
                                        {incident.alibis.length > 0 && (
                                            <React.Fragment>
                                                <h4 className="font-bold text-sm text-white mb-4"><i className="fa-solid fa-clipboard-check mr-2"></i>アリバイ状況一覧</h4>
                                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                                                    {incident.alibis.map((alibi, idx) => (
                                                        <div key={idx} className={`p-3 rounded border ${alibi.status === 'safe' ? 'bg-gray-900/30 border-gray-800' : 'bg-red-950/10 border-red-900/30'}`}>
                                                            <span className={`font-bold text-sm block mb-1 ${alibi.status === 'safe' ? 'text-gray-300' : 'text-red-400'}`}>{alibi.name}</span>
                                                            <p className="text-xs text-gray-400">{alibi.desc}</p>
                                                        </div>
                                                    ))}
                                                </div>
                                            </React.Fragment>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                        <p className="text-xs text-gray-600 text-right mt-4">【引用元：ヨン_kikyosan 様】</p>
                    </section>

                    {/* CLUES */}
                    <section id="clues" className="py-20 bg-darker border-t border-gray-900 px-4">
                        <div className="max-w-5xl mx-auto">
                            <SectionTitle title="CLUES & THEORY" subtitle="未回収の伏線・考察まとめ" />
                            <div className="space-y-4">
                                {DATA.clues.map((clue, i) => (
                                    <details key={i} className="bg-dark border border-gray-800 rounded group cursor-pointer">
                                        <summary className="font-bold p-4 flex justify-between items-center group-open:text-ice transition-colors">
                                            <span><i className="fa-solid fa-magnifying-glass mr-3 text-gray-600"></i>{clue.title}</span>
                                            <i className="fa-solid fa-chevron-down text-sm transition-transform group-open:rotate-180"></i>
                                        </summary>
                                        <div className="p-4 pt-0 text-sm text-gray-400 border-t border-gray-800 mt-2 leading-relaxed">
                                            {clue.text}
                                        </div>
                                    </details>
                                ))}
                            </div>
                            <p className="text-xs text-gray-600 text-right mt-4">【引用元：んごミック 様】</p>
                        </div>
                    </section>
                </React.Fragment>
            );
        };

        const AppRefs = () => {
            return (
                <section className="py-16 bg-dark border-t border-gray-900 px-4">
                    <div className="max-w-4xl mx-auto">
                        <h3 className="text-xs font-bold text-gray-500 mb-6 tracking-widest border-l-4 border-gray-700 pl-3">REFERENCES / 引用・参考元</h3>
                        <div className="space-y-4 text-xs">
                            {DATA.references.map((ref, i) => (
                                <div key={i} className="bg-gray-900/50 p-4 rounded border border-gray-800">
                                    <p className="text-gray-300 font-bold mb-1">{ref.title}</p>
                                    <p className="text-gray-500 mb-2">著者：{ref.author} ｜ X：<a href={`https://x.com/${ref.twitter.replace('@', '')}`} target="_blank" className="text-blue-400 hover:underline">{ref.twitter}</a></p>
                                    <a href={ref.url} target="_blank" className="text-gray-400 hover:text-white transition break-all"><i className="fa-solid fa-link mr-1"></i>{ref.url}</a>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>
            );
        };

        const rootMain = ReactDOM.createRoot(document.getElementById('react-root-main'));
        rootMain.render(<AppMain />);

        const rootRefs = ReactDOM.createRoot(document.getElementById('react-root-refs'));
        rootRefs.render(<AppRefs />);
    </script>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(head_part)
    f.write(react_root_main)
    f.write(vote_part)
    f.write(react_root_refs_and_script)
    f.write(footer_part)

print("Update completed successfully.")
