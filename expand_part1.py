import os

base_dir = r"c:\Users\jorda\Documents\ANTIGRAVITY\STUDY13"

md_updates = {
    "01_Internet_Basics.md": r"""# 13.1.1: Web Basics (HTTP/HTTPS, TCP/IP, DNS)

### 1. 【エンジニアの定義】Professional Definition

> **1. HTTP/HTTPS**:
> クライアント（ブラウザ）とサーバー間でHTMLなどのデータを送受信するための通信プロトコル。HTTPSはTLS（Transport Layer Security）を用いて暗号化されており、改ざんや盗聴を防ぐ。
> 
> **2. TCP/IP**:
> インターネットの通信インフラを構成する基本プロトコル体系。IPが「目的地へのルート構築」を担い、TCPが「データの到着と順序の保証（信頼性）」を担保する。
> 
> **3. DNS (Domain Name System)**:
> 「google.com」のような人間が読めるドメイン名を、「142.250.190.46」といった機械が通信するためのIPアドレスに変換（名前解決）するシステム。インターネットの電話帳。

---

### 2. 【0ベース・深掘り解説】Gap Filling
※バックエンドエンジニアとしてシステムを設計するとき、ネットワークの基礎はトラブルシューティングの命綱になります。

#### 🌐 インターネットの裏側で何が起きているか？
APIサーバーを立ち上げ、ユーザーがそこにアクセスするとき、見えないところで3つのプロトコルがリレーしています。
*   **DNSが道案内をする**: ユーザーがURLを叩くと、まずDNSに「このAPIのIPアドレスは何？」と尋ねます。ここでDNSの設定（AレコードやCNAME）が間違っていると、どんなに良いコードを書いても一切アクセスが来ません。
*   **TCPが道をつくりデータを運ぶ**: IPアドレスがわかると、サーバーに対して「3ウェイ・ハンドシェイク（SYN -> SYN-ACK -> ACK）」を行い、信頼できる通信経路を確立します。
*   **HTTPSが注文書を暗号化して渡す**: 道ができたところで、ついに「このデータをください（GET）」というHTTPリクエストが暗号化された状態で送られます。

#### 💡 なぜこれを学ぶのか？
サーバーで「接続が切れる（Connection Timeout）」というエラーが出たとき、HTTPのレイヤー（アプリのエラー）なのか、TCPのレイヤー（NW機器による遮断）なのか、DNSのレイヤー（名前が引けない）なのかを切り分ける力が必要だからです。

---

### 3. 【通信の視覚化】Visual Guide

ブラウザからあなたのバックエンドAPIに到達するまでの流れです。

```mermaid
sequenceDiagram
    participant User as クライアント(ブラウザ)
    participant DNS as DNSサーバー
    participant Server as バックエンドサーバー
    
    Note over User, DNS: 1. DNS Resolution
    User->>DNS: "api.my-app.com" のIPは？
    DNS-->>User: "203.0.113.50" (IPアドレス)
    
    Note over User, Server: 2. TCP/IP 接続確立
    User->>Server: SYN (繋いでいい？)
    Server-->>User: SYN-ACK (いいよ！)
    User->>Server: ACK (了解！)
    
    Note over User, Server: 3. HTTP/HTTPS リクエスト
    User->>Server: GET /users (TLS暗号化)
    Server-->>User: 200 OK & JSONデータ
```

---

### 💡 この用語のまとめ (Key Takeaways)
*   **HTTP/HTTPS**: アプリケーション同士の「会話のルール」。暗号化(S)は現代の必須条件。
*   **TCP/IP**: 荷物を確実に届けるための「配送ネットワークと書留郵便」。
*   **DNS**: 名前から住所（IP）を引く「電話帳」。設定ミスはシステム全体のダウンに直結する。
""",

    "02_Realtime_Transmits.md": r"""# 13.1.2: Real-time Transmits (WebSockets, SSE)

### 1. 【エンジニアの定義】Professional Definition

> **14. WebSockets**:
> 1つのTCPコネクション上で、プレーンテキストやバイナリデータを**双方向**（サーバー⇔クライアント）に低遅延で通信し続けるプロトコル。HTTPのハンドシェイク後にアップグレードして通信を確立する。
> 
> **15. Server-Sent Events (SSE)**:
> サーバーからクライアントへ**単方向**でイベントデータをリアルタイムにプッシュ送信するためのHTTP標準規格。テキストデータの送信に特化している。

---

### 2. 【0ベース・深掘り解説】Gap Filling
※従来のHTTPは「クライアントからリクエストして、サーバーが返す」という一問一答形式です。しかし、チャットや株価のリアルタイム更新ではこのルールが限界を迎えます。

#### 🔄 ポーリングの限界と双方向通信
昔は、クライアントが数秒おきに「新しいメッセージある？」と尋ねる（ポーリング）方式を取っていました。これではサーバーに無駄な負荷がかかります。
*   **WebSocketsの登場**: 電話のように「一度繋いだら、お互い好きなタイミングでしゃべれる」仕組みです。チャットアプリや、対戦型のオンラインゲームなど、リアルタイムな双方向のやり取りが必須な場面で使われます。
*   **SSEの台頭**: WebSocketsは強力ですが、常時接続の維持管理（コネクション数やLBの制約）が面倒です。そこで、「サーバーからだけ一方的に送れればいい（例：通知システム、スポーツの速報、AIのストリーミング応答など）」場合、通常のHTTP上で動く軽量なSSEが適しています。

---

### 3. 【通信の視覚化】Visual Guide

HTTP(ポーリング) vs WebSockets vs SSE のアーキテクチャ比較。

```mermaid
sequenceDiagram
    participant C as クライアント
    participant S as サーバー
    
    Note over C, S: ■ WebSockets (双方向チャット)
    C->>S: HTTP Upgrade (WebSocketに切り替えて)
    S-->>C: 101 Switching Protocols (了解)
    C->>S: 「こんにちは！」
    S-->>C: 「いらっしゃい！」
    
    Note over C, S: ■ SSE (単方向の通知・AIストリーム)
    C->>S: GET /notifications (text/event-stream)
    S-->>C: 200 OK (Connection: keep-alive)
    S-->>C: data: "通知1"
    S-->>C: data: "通知2"
```

---

### 💡 この用語のまとめ (Key Takeaways)
*   **WebSockets**: 双方向。チャットやゲームなど、リアルタイムなやり取りが必要な場合に最適。
*   **SSE (Server-Sent Events)**: 単方向（サーバー→クライアント）。通知や、ChatGPTの文字ストリーミング描画などに最適で実装が楽。
""",

    "03_API_Paradigms.md": r"""# 13.2.1: API Paradigms (REST, GraphQL, gRPC, API Design)

### 1. 【エンジニアの定義】Professional Definition

> **4. REST APIs**:
> URLでリソース（名詞）を指定し、HTTPメソッド（GET, POST, PUT, DELETE）で操作（動詞）する設計原則。「/users/123」のような直感的な設計。
> 
> **5. GraphQL**:
> Facebookが開発したAPIクエリ言語。クライアントが「欲しいデータの構造」をJSON形式でリクエストし、過不足なくデータを1つのエンドポイント(`/graphql`)から取得できる。
> 
> **6. gRPC**:
> Googleが開発したRPC（Remote Procedure Call）。Protocol Buffersを用いてデータをバイナリシリアライズし、HTTP/2のストリームで超高速に通信する。主にマイクロサービス間の内部通信で使用。
> 
> **7. API Design**:
> 適切なバージョン管理（`/v1/`）、ページネーション、一貫したエラーレスポンス構造など、開発者が使いやすいAPIを設計するための原則とベストプラクティス。

---

### 2. 【0ベース・深掘り解説】Gap Filling

#### 🆚 3大パラダイムの使い分け戦略
「とりあえずRESTで作る」時代は終わり、用途に合わせてアーキテクチャを選ぶ必要があります。
*   **RESTの限界**: 画面Aでは「ユーザーの名前だけ」欲しいのに、画面Bでは「名前と会社名と所属リスト」が欲しい場合、RESTだと`/users/1`と`/users/1/companies`の2回通信するか、重いデータを1回で全部返すしかありませんでした（オーバーフェッチ・アンダーフェッチ問題）。
*   **GraphQLの解決策**: クライアント側で「名前と会社名だけください」とクエリを書けるため、モバイルアプリのように通信回数やデータ量を削りたいフロントエンド向けAPIで大活躍します。
*   **gRPCの闘技場**: ユーザーから見える表側のAPIではなく、バックエンド同士（決済サービス ⇔ 在庫サービス）が高速にやり取りする「裏側の通信」で猛威を振るいます。バイナリデータとHTTP/2により、RESTの10倍高速と言われます。

---

### 3. 【通信の視覚化】Visual Guide

適材適所でパラダイムを組み合わせる現代のアーキテクチャ。

```mermaid
graph TD
    Client[Web/Mobile App] -->|GraphQL<br>(柔軟なデータ取得)| Gateway[API Gateway / BFF]
    Client -->|REST<br>(ファイルアップロードや標準機能)| Gateway
    Gateway -->|gRPC<br>(超高速・バイナリ通信)| Auth[認証サービス]
    Gateway -->|gRPC| DB[ユーザー情報サービス]
```

---

### 💡 この用語のまとめ (Key Takeaways)
*   **REST**: 業界標準。シンプルでキャッシュしやすく、外部公開APIの王道。
*   **GraphQL**: 柔軟。フロントエンド（スマホアプリなど）の通信最適化に特化。
*   **gRPC**: 超高速。マイクロサービス内部のバックエンド間通信のデファクトスタンダード。
*   **API Design**: 使い勝手を決める「プロダクトの顔」。ドキュメントと一貫性が命。
""",

    "04_Data_Handling.md": r"""# 13.2.2: Data Handling (CRUD, Valid, SerDe)

### 1. 【エンジニアの定義】Professional Definition

> **8. CRUD Operations**:
> データ操作の基本4原則。Create (作成=POST), Read (読み取り=GET), Update (更新=PUT/PATCH), Delete (削除=DELETE)。大半のWebAPIはこの4つの操作にマッピングされる。
> 
> **41. Data Validation**:
> クライアントから送信されたデータが、要求する型、長さ、形式（メールアドレスなど）、ビジネスルールに合致しているかをサーバー側で検証すること。
> 
> **42. Serialization / 43. Deserialization**:
> 【シリアライズ】メモリ上のオブジェクトや構造体を、ネットワーク転送や保存可能なバイト列（JSON、XML、文字列）に変換すること。
> 【デシリアライズ】受信したバイト列を、アプリケーションで扱える元のオブジェクト構造に復元すること。

---

### 2. 【0ベース・深掘り解説】Gap Filling

#### 🛡️ なぜバリデーションが最も重要か？
「フロントエンド（HTML/JS）で入力チェックしているから、サーバー側ではチェックしなくていいよね？」は**初心者エンジニアが陥る最大の罠**です。
*   **セキュリティの壁**: 悪意のあるユーザーは、PostmanやcURLを使ってフロントエンドをバイパスし、直接APIに異常なデータを送り込んできます。バックエンドでのData Validationは「最後の砦」であり、ここを突破されるとSQLインジェクションやシステムクラッシュに直結します。
*   **早期リターン**: データベースの処理をする「前」に弾くことで、無駄なリソース消費を防ぎます。

#### 📦 データの箱詰め（SerDe）
プログラム言語（Pythonの辞書、Javaのクラス）の中身は、そのままではネットワークの線を通りません。
「段ボール（JSON）」にテキストとして綺麗に詰める作業が Serialization（シリアライズ）です。受け取った側で段ボールを開けて、自分の言語のクラスに組み立て直すのが Deserialization（デシリアライズ）です。ここで型エラーなどがよく発生します。

---

### 3. 【通信の視覚化】Visual Guide

データがリクエストされてからDBに保存されるまでのライフサイクル。

```mermaid
sequenceDiagram
    participant C as クライアント
    participant API as バックエンドAPI
    participant DB as データベース
    
    C->>API: HTTP POST JSON送信 (Serialization)
    Note over API: 1. Deserialization (JSON → Python Object)
    Note over API: 2. Data Validation (文字数、型チェック)
    alt Validation 失敗
        API-->>C: 400 Bad Request (エラーメッセージ)
    else Validation 成功
        Note over API: 3. CRUD (Create処理)
        API->>DB: INSERT INTO...
        DB-->>API: 成功
        Note over API: 4. Serialization (Object → JSON)
        API-->>C: 201 Created (JSONデータ)
    end
```

---

### 💡 この用語のまとめ (Key Takeaways)
*   **CRUD**: データ操作の基本。REST APIの設計と完全にリンクする。
*   **Data Validation**: バックエンドにおける絶対の防衛線。フロントのバリデーションは「ユーザー体験」のため、バックエンドのバリデーションは「セキュリティと一貫性」のため。
*   **SerDe**: 言語の壁を超えて通信するための「翻訳と箱詰め」作業。
""",

    "05_Identity_Management.md": r"""# 13.3.1: Identity Management (AuthN, AuthZ, JWT, OAuth)

### 1. 【エンジニアの定義】Professional Definition

> **9. Authentication (AuthN - 認証)**:
> 「あなたは誰か（Who you are）」を確認するプロセス。ID/パスワード、生体認証、多要素認証（MFA）など。
> 
> **10. Authorization (AuthZ - 認可)**:
> 「あなたは何ができるか（What you can do）」を制御するプロセス。「Admin」「User」のようなロール(RBAC)によってアクセスできるページやAPIを制限する。
> 
> **11. Sessions & Cookies** / **12. JWT (JSON Web Token)**:
> ログイン状態の保持方法。セッションは「サーバー側」で状態を記憶しCookieでIDだけ管理する。JWTは「クライアント側」に暗号署名された情報（トークン）を持たせ、サーバーは状態(ステート)を持たない。
> 
> **13. OAuth**:
> 「Googleアカウントでログイン」のように、パスワードを渡さずにサードパーティアプリケーションへ権限のみを委譲する標準プロトコル。

---

### 2. 【0ベース・深掘り解説】Gap Filling

#### 🔑 「認証」と「認可」は全くの別物
ホテルに例えましょう。
*   **認証 (Authentication)**: フロントで身分証を見せて、「確かにあなたは予約した田中さんですね」と本人確認を行うこと。
*   **認可 (Authorization)**: 田中さんに「301号室とジムのカードキー」を渡すこと。田中さんは「厨房」や「他の人の部屋」には入れません。

初心者はこれを混同しがちですが、コード上では「ログイン関数」と「権限チェック関数」として明確に分ける必要があります。

#### 🍪 セッション vs JWT の覇権争い
昔のWebシステムは、サーバーのメモリ上にすべてのログインユーザーのリスト（Session）を保持していました。しかし、ユーザーが1万人、100万人となりサーバーを複数台（ロードバランサー）に増やした時、「サーバーAにはログイン情報があるが、サーバーBには無い」という問題が発生しました。

これを解決したのが **JWT** です。JWTはパスポートのようなもので、「これは確かに私が署名した本物の証明書だ（改ざんされていない）」と自己完結で検証できるため、どのサーバーにアクセスしてもデータベースを引かずに認証でき、マイクロサービスと非常に相性が良いです。

---

### 3. 【通信の視覚化】Visual Guide

現代のデファクトスタンダードである JWT 認証のフロー。

```mermaid
sequenceDiagram
    participant C as クライアント
    participant S as 認証サーバー (Auth)
    participant API as API（リソースサーバー）
    
    Note over C, S: ■ 1. Authentication (認証)
    C->>S: POST /login (ID & Password)
    S->>S: DBとパスワード照合
    S-->>C: 200 OK + JWT (署名済みトークン)
    
    Note over C, API: ■ 2. Authorization (認可)
    C->>API: GET /admin/data<br/>Header: Authorization: Bearer <JWT>
    API->>API: 署名検証＆Roleチェック
    alt Admin権限あり
        API-->>C: 200 OK (機密データ)
    else Admin権限なし
        API-->>C: 403 Forbidden (アクセス拒否)
    end
```

---

### 💡 この用語のまとめ (Key Takeaways)
*   **AuthN (認証)と AuthZ (認可)**: ホテルのフロントとカードキー。分けて設計する。
*   **JWT**: ステートレスな現代APIのパスポート。データベース負荷を劇的に下げる。
*   **OAuth**: パスワードを預けずに、外部サービス間を安全に連携させるための鍵の貸し借り。
""",

    "06_Web_Security.md": r"""# 13.3.2: Web Security & OWASP

### 1. 【エンジニアの定義】Professional Definition

> **81. OWASP Top 10**:
> The Open Web Application Security Project が発表する、Webアプリの最も深刻な脆弱性ランキング。「インジェクション」「認証の不備」「暗号化の失敗」などが並ぶ。
> 
> **82. Input Sanitization / 85. XSS (Cross-Site Scripting)**:
> ユーザーが入力した悪意あるスクリプト(`<script>...</script>`)が、他のユーザーのブラウザ上で実行されてしまうXSS攻撃を防ぐため、特殊文字を安全な形式（エスケープ等）に無害化(Sanitization)すること。
> 
> **83. CSRF (Cross-Site Request Forgery)** / **84. CORS (Cross-Origin Resource Sharing)**:
> 偽サイトからバックグラウンドでリクエストを飛ばさせ、意図しない操作（送金など）を実行させるCSRF攻撃。それを防ぐ仕組みや、別のドメインからのAPI呼び出しを許可/拒否するブラウザ制御がCORS。
> 
> **76. Secrets Management / 78. Encryption / 80. Security Best Practices**:
> パスワードやAPIキーなどの機密（Secrets）はソースコード(Git)に書かず、Key Vaultや環境変数に保存する。データは保存時(at rest)と転送時(in transit: **79. HTTPS**)の両方で暗号化する。最小権限の原則を守る。

---

### 2. 【0ベース・深掘り解説】Gap Filling

#### ⚔️ ハッカーは「入力フォーム」からやってくる
バックエンドエンジニアが最も警戒すべきは「ユーザー入力は全て悪意がある」という前提(**Zero Trust**)に立つことです。
*   **XSS**: 掲示板の名前欄にJavaScriptを仕込み、それを見た管理者のセッションCookieを盗み出します。フレームワーク（Reactなど）が自動エスケープしてくれますが、油断は禁物です。
*   **コマンド/SQLインジェクション**: `admin' OR 1=1 --` のような文字列を入れることで、データベースのチェックをすり抜ける古典的かつ未だに最強の攻撃です。ORM（Django ORMやEntity Framework）やプレースホルダを使うことで防ぎます。

#### 🛡️ Secretsをコードに書くという大罪
GitにAWSのアカウントキーやデータベースへのパスワードを書いて`push`してしまった瞬間、数秒以内にボットがそれを検知して仮想マシンを数千台起動し、翌日に数百万円の請求が来ます（本当に起きます）。
Secrets Management（Azure Key Vault, AWS Secrets Manager, HashiCorp Vault）を使い、動的にキーを取得するアーキテクチャが必須です。

---

### 3. 【通信の視覚化】Visual Guide

CORSエラーとCSRF攻撃のメカニズム比較。

```mermaid
sequenceDiagram
    participant Hacker as 悪意のあるサイト (hacker.com)
    participant Browser as 被害者のブラウザ
    participant Bank as 銀行API (bank.com)
    
    Note over Hacker, Browser: ユーザーが悪意あるサイトを訪問
    Hacker->>Browser: 巧妙に隠された送金スクリプト
    
    Note over Browser, Bank: CSRF攻撃の試み
    Browser->>Bank: GET /transfer?to=Hacker&amount=1000<br/>(暗黙的に銀行のCookieが付与される)
    
    alt 脆弱なバックエンドの場合
        Bank-->>Browser: 200 OK (送金完了...)
    else CSRFトークン / CORS設定がある場合
        Note over Bank: Originがhacker.comである事を検知<br/>CSRFトークンも無し
        Bank-->>Browser: 403 Forbidden / CORS Block!
    end
```

---

### 💡 この用語のまとめ (Key Takeaways)
*   **OWASP Top 10**: バックエンドエンジニアの「交通ルール」。必ず目を通すこと。
*   **XSS / インジェクション**: ユーザーからの入力は全て疑い、検証（Validation）と無害化（Sanitization）を行う。
*   **Secrets Management**: 認証情報やAPIキーは絶対にコードにハードコードせず、Vaultなどの外部シークレットマネージャーから実行時に注入する。
""",

    "07_System_Architecture.md": r"""# 13.4.1: System Architecture Patterns

### 1. 【エンジニアの定義】Professional Definition

> **21. Monolith / 20. Microservices**:
> 【モノリス】UI、ビジネスロジック、DBアクセスが1つの巨大なコードベースとプロセスとして動く伝統的なシステム。
> 【マイクロサービス】「決済」「在庫」「ユーザー」など機能ごとにサーバーとDBを分割し、API(gRPCなど)で連携する設計。
> 
> **17. MVC / 18. Layered / 19. Clean Architecture**:
> アプリケーション「内部」のフォルダ分けやコードの責務分離パターン。依存関係を「ドメイン（ビジネスの中核）」に向けて一方向にすることで、変更に強いシステムを作る。
> 
> **22. Serverless / 46. Event-Driven**:
> サーバーのOS管理などをクラウド任せにし、イベント（ファイルアップロード、HTTPリクエスト）をトリガーに関数（AWS Lambda等）を実行する現代の疎結合アーキテクチャ。
>
> **16. Middleware**:
> リクエストがコントローラーに到達する前、またはレスポンスを返す前に処理を挟み込む層。ロギング、認証、CORS設定などを一元管理する。

---

### 2. 【0ベース・深掘り解説】Gap Filling

#### 🏢 モノリスは「悪」ではない
マイクロサービスはバズワードでしたが、スタートアップや中規模プロジェクトで最初から分割するのは**「分散モノリス（複雑なだけの負債）」**になる危険が高く、失敗の典型例です。
最初は「モジュラー・モノリス（1つのシステムだがフォルダ/クラスは綺麗に分離）」で構築し、ビジネスが急成長して組織が分かれるタイミングで、ボトルネック箇所のみをマイクロサービス化して切り出すのが現在最も賢い戦略とされています。

#### 🧅 なぜ Clean Architecture が注目されるのか？
システムで一番大事なのは「フレームワーク（Django, React）」でも「データベース（PostgreSQL）」でもなく、**「ビジネスのルール（カートの計算ロジック等）」**です。
Clean ArchitectureやLayered Architectureは、ビジネスロジックを「中心（Core）」に置き、データベースやWebフレームワークを「外側のプラグイン（いつでも付け替え可能）」として扱います。これにより「DBをMySQLからPostgreSQLに変えても、ビジネスルールのコードは1行も変更しなくて良い」という究極の保守性を実現します。

#### 🔄 Middlewareの力
リクエストごとに毎度「認証チェック」「ログ出力」のコードを書くのは冗長です。Middlewareはパイプラインの途中に立つ関所であり、これを設定するだけで全APIに一括で処理を適用できます。

---

### 3. 【通信の視覚化】Visual Guide

モノリス vs マイクロサービスのアーキテクチャの進化。

```mermaid
graph TD
    subgraph "Monolithic Architecture"
        WebM[Web App]
        logicM[User + Cart + Pay Logic]
        DBM[(Single DB)]
        WebM --> logicM
        logicM --> DBM
    end

    subgraph "Microservices Architecture"
        API_GW[API Gateway]
        ServiceU[User Service]
        ServiceC[Cart Service]
        ServiceP[Pay Service]
        DBU[(User DB)]
        DBC[(Cart DB)]
        DBP[(Pay DB)]
        
        API_GW --> ServiceU --> DBU
        API_GW --> ServiceC --> DBC
        API_GW --> ServiceP --> DBP
        ServiceC -.->|gRPC/Event| ServiceP
    end
```

---

### 💡 この用語のまとめ (Key Takeaways)
*   **モノリス vs マイクロサービス**: 最初からマイクロサービスに飛びつかず、まずは綺麗なモノリス（モジュラーモノリス）を目指す。
*   **Clean Architecture**: 「ドメイン（ビジネスロジック）」を中心に置き、フレームワークやDBと疎結合にする思想。
*   **Event-Driven / Serverless**: 非同期でスケーラブル。大量処理やスパイク（急なアクセス増）に非常に強い。
""",

    "08_Database_Core.md": r"""# 13.5.1: Database Core (RDBMS vs NoSQL & Optimization)

### 1. 【エンジニアの定義】Professional Definition

> **29. Database Design / 30. SQL / 31. NoSQL**:
> データの持ち方。「厳格な表形式(RDBMS)」か、「柔軟なドキュメント/KVS(NoSQL)」か。システム要件によって使い分ける（例：決済はSQL、ログやカタログはNoSQL）。
> 
> **32. Indexing / 33. Query Optimization**:
> 【インデックス】本の「索引」と同じ。データを全件走査（フルスキャン）せず、瞬時に該当行を見つけるためのB-Treeなどのデータ構造。
> 【クエリ最適化】オプティマイザが理解しやすいSQLを書く、または実行計画（EXPLAIN）を見てボトルネックを解消するプロセス。
> 
> **34. Transactions / 35. ACID**:
> 【トランザクション】「口座Aからお金を減らし、口座Bに増やす」といった一連の処理の塊。
> 【ACID特性】トランザクションが絶対に守るべき4原則。Atomicity（不可分性）、Consistency（一貫性）、Isolation（独立性）、Durability（永続性）。
> 
> **40. ORM (Object-Relational Mapping)**:
> SQLを直接書かず、PythonやJavaのオブジェクト（クラス）としてデータベースを操作するライブラリ（Hibernate, Entity Frameworkなど）。

---

### 2. 【0ベース・深掘り解説】Gap Filling

#### 🔍 データベースが遅い？ 9割は「インデックス」の欠如
バックエンドAPIのレスポンスが遅い原因の大部分は、データベースへの非効率なアクセスです。
ユーザー名で検索するAPIを作ったとき、数万件のデータだと問題ありませんが、レコードが数千万件になると突然システムが固まります。これは「フルスキャン」が発生しているからです。`CREATE INDEX` を一行実行してキーにインデックスを張るだけで、検索速度が1000倍速くなることも珍しくありません。バックエンドエンジニアに必須のチューニングスキルです。

#### ⚖️ ORMの光と闇（N+1問題）
ORMはコードを綺麗に保ち、SQLインジェクションを防いでくれる素晴らしいツールです。
しかし、「投稿一覧と、それぞれに関連するコメント」を取得しようとした時、裏側で「投稿を取得するSQL（1回） + 各投稿のコメントを取得するSQL（N回）」という合計 N+1 回のクエリが発行されてしまい、DBをパンクさせる**N+1問題**が頻発します。ORMに頼りきりにならず、裏でどんなSQLが発行されているか（Eager Loadingの使用等）を意識する必要があります。

#### 💳 ACID特性は銀行の命
トランザクション中にサーバーの電源が落ちても、「口座Aからお金は減ったが、口座Bに入金されていない」という中途半端な状態(**A**tomicity違反)になってはいけません（必ず全成功か、全ロールバックになる）。RDBMS（MySQL, PostgreSQL）はこれを強固に守るため、基幹システムに採用されます。

---

### 3. 【通信の視覚化】Visual Guide

インデックスを使わないフルスキャン vs インデックス検索の挙動比較。

```mermaid
graph LR
    subgraph "No Index (Full Table Scan)"
        Q1[SELECT * FROM users<br/>WHERE age = 28]
        DB1[(Database 10,000,000 rows)]
        Q1 -->|1千万行を1から順番にチェック<br>(O(N) - 激遅)| DB1
    end

    subgraph "With Index (B-Tree Seek)"
        Q2[SELECT * FROM users<br/>WHERE age = 28]
        IDX[Age Index Structure<br/>B-Tree]
        DB2[(Database Rows)]
        Q2 -->|すぐに場所を特定<br>(O(log N) - 爆速)| IDX
        IDX -->|ポインタで対象データのみ取得| DB2
    end
```

---

### 💡 この用語のまとめ (Key Takeaways)
*   **SQL vs NoSQL**: データの「関係性と厳格さ」が重要ならSQL。「拡張性と柔軟性」ならNoSQL（MongoDB等）。
*   **Indexing**: パフォーマンス改善の銀の弾丸。ただし無闇に張ると書き込み（INSERT/UPDATE）が遅くなるためトレードオフ。
*   **ACID**: 一貫性を保証するRDBMSの魂。
*   **ORMとN+1問題**: 便利なORMだが、裏側で発行されるクエリ数を常に警戒すること。
"""
}

for filename, content in md_updates.items():
    with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Expanded Part 1 ({len(md_updates)} files) successfully!")
