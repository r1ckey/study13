import os

base_dir = r"c:\Users\jorda\Documents\ANTIGRAVITY\STUDY13"

md_updates = {
    "07_System_Architecture.md": """# System Architecture Patterns
## 16. Middleware
リクエストとレスポンスの間で処理を挟み込む層（ロギング、認証、エラーハンドリングなどに利用）。
## 17. MVC Architecture
Model-View-Controllerで責務を分離するUIパターンのクラシック。
## 18. Layered / 19. Clean Architecture
依存関係を内側に向かってのみ設定し、ドメインロジックを分離する設計。
## 20. Microservices / 21. Monolith
独立してデプロイ可能な小さなサービスの集合体か、単一の巨大なコードベースか。
## 22. Serverless
インフラの管理をクラウドプロバイダに任せ、コードの実行に集中するモデル。
## 46. Event-Driven Architecture
状態の変更（イベント）をトリガーとしてシステムを連携させるアーキテクチャ。
""",
    "06_Web_Security.md": """# Web Security
## 76. Secrets Management
パスワードやAPIキーなどの機密情報を安全に管理する仕組み。
## 78. Encryption / 79. HTTPS/TLS
データの暗号化とセキュアな通信経路の確保。
## 80. Security Best Practices
最小権限の原則など、システムレベルで取り入れるべきセキュア設計のアプローチ。
## 81. OWASP Top 10
Webアプリケーションの最も重大な10のセキュリティリスク。
## 82. Input Sanitization / 85. XSS (Cross-Site Scripting)
悪意のあるスクリプトの注入を防ぐための入力値の無害化。
## 83. CSRF / 84. CORS
クロスサイトリクエストフォージェリの防止と、オリジン間のリソース共有制御。
""",
    "15_DevOps_Containers.md": """# Testing, CI/CD & Deployment
## 64-67. Unit/Integration/E2E Testing
自動テストのピラミッド。個別ロジックからシステム全体までの品質保証。
## 68. CI/CD (Continuous Integration / Continuous Deployment)
コードの変更からテスト、本番環境へのデプロイまでを自動化するパイプライン。
## 69. Docker / 70. Kubernetes / 71. Containerization
アプリケーションとその依存関係をパッケージ化し、オーケストレーションで管理する技術。
## 72-75. Deployment Strategies (Blue-Green, Canary, Feature Flags)
ダウンタイムやリスクを最小限に抑えながら新機能をリリースする手法。
## 77. Environment Variables
設定をコードから分離し、環境ごとに異なる値（DB接続情報など）を安全に注入する仕組み。
""",
    "10_Infra_LoadBalancing.md": """# Infrastructure & Load Balancing
## 23. Load Balancing
トラフィックを複数のサーバーに分散させ、可用性とスループットを向上させる。
## 24. Reverse Proxy / 25. Nginx
クライアントとバックエンドサーバーの間に立ち、ルーティングやキャッシングを行う。
## 51. API Gateway
マイクロサービス群の入り口として機能し、認証、ルーティング、レート制限を担う。
## 52. Service Discovery
動的に変化するマイクロサービスのIPアドレスを自動的に見つける仕組み。
## 96. Scalability
システムの負荷増大に合わせてリソースを追加拡張（スケールアップ・スケールアウト）する能力。
## 97. High Availability
システムが単一障害点（SPOF）を持たず、長期間にわたって稼働し続ける（99.99%など）能力。
""",
    "11_Caching_Strategies.md": """# Caching Tactics
## 26. Caching
頻繁にアクセスされるデータを高速なストア（メモリ等）に保持する。
## 27. Redis / 28. Memcached
代表的なインメモリデータストア/キャッシングシステム。
## 86. Data Compression / 89. CDN Integration
静的アセットやエッジでのキャッシュを活用し、レスポンス速度を高速化。
## 98. Performance Optimization
アルゴリズムの改善やN+1問題の解決など、ソフトウェア・ハードウェアレベルの総合的なパフォーマンス向上。
"""
}

for filename, content in md_updates.items():
    with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Updated {len(md_updates)} files with the remaining missing concepts!")
