import os
import json
import re

base_dir = r"c:\Users\jorda\Documents\ANTIGRAVITY\STUDY13"

replacements = {
    "03_API_Paradigms.md": [
        (
"""```mermaid
graph TD
    Client[Web/Mobile App] -->|GraphQL<br>(柔軟なデータ取得)| Gateway[API Gateway / BFF]
    Client -->|REST<br>(ファイルアップロードや標準機能)| Gateway
    Gateway -->|gRPC<br>(超高速・バイナリ通信)| Auth[認証サービス]
    Gateway -->|gRPC| DB[ユーザー情報サービス]
```""",
"""```mermaid
graph TD
    Client["Web/Mobile App"] -->|"GraphQL<br>(柔軟なデータ取得)"| Gateway["API Gateway / BFF"]
    Client -->|"REST<br>(ファイルアップロードや標準機能)"| Gateway
    Gateway -->|"gRPC<br>(超高速・バイナリ通信)"| Auth["認証サービス"]
    Gateway -->|gRPC| DB["ユーザー情報サービス"]
```"""
        )
    ],
    "05_Identity_Management.md": [
        (
"""```mermaid
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
```""",
"""```mermaid
sequenceDiagram
    participant C as クライアント
    participant S as 認証サーバー (Auth)
    participant API as API（リソースサーバー）
    
    Note over C, S: 1. Authentication (認証)
    C->>S: POST /login (ID & Password)
    S->>S: DBとパスワード照合
    S-->>C: 200 OK + JWT (署名済みトークン)
    
    Note over C, API: 2. Authorization (認可)
    C->>API: GET /admin/data<br/>Header: Authorization: Bearer (JWT)
    API->>API: 署名検証＆Roleチェック
    alt Admin権限あり
        API-->>C: 200 OK (機密データ)
    else Admin権限なし
        API-->>C: 403 Forbidden (アクセス拒否)
    end
```"""
        )
    ],
    "08_Database_Core.md": [
        (
"""```mermaid
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
```""",
"""```mermaid
graph LR
    subgraph "No Index (Full Table Scan)"
        Q1["SELECT * FROM users<br/>WHERE age = 28"]
        DB1[("Database 10,000,000 rows")]
        Q1 -->|"1千万行を1から順番にチェック<br>(O(N) - 激遅)"| DB1
    end

    subgraph "With Index (B-Tree Seek)"
        Q2["SELECT * FROM users<br/>WHERE age = 28"]
        IDX["Age Index Structure<br/>B-Tree"]
        DB2[("Database Rows")]
        Q2 -->|"すぐに場所を特定<br>(O(log N) - 爆速)"| IDX
        IDX -->|ポインタで対象データのみ取得| DB2
    end
```"""
        )
    ],
    "10_Infra_LoadBalancing.md": [
        (
"""```mermaid
graph TD
    Client[Users / Browsers] -->|HTTPS| Proxy[Reverse Proxy / LB<br>(e.g. Nginx / AWS ALB)]
    
    subgraph "Backend Servers (Scalability/HA)"
        Proxy -->|HTTP| App1[Web Server 1]
        Proxy -->|HTTP| App2[Web Server 2]
        Proxy -.->|Health Check: Fail!| App3[Web Server 3<br>(Down)]
    end
```""",
"""```mermaid
graph TD
    Client["Users / Browsers"] -->|HTTPS| Proxy["Reverse Proxy / LB<br>(e.g. Nginx / AWS ALB)"]
    
    subgraph "Backend Servers (Scalability/HA)"
        Proxy -->|HTTP| App1["Web Server 1"]
        Proxy -->|HTTP| App2["Web Server 2"]
        Proxy -.->|"Health Check: Fail!"| App3["Web Server 3<br>(Down)"]
    end
```"""
        )
    ],
    "13_Fault_Tolerance.md": [
        (
"""```mermaid
stateDiagram-v2
    [*] --> Closed: 通常状態 (通信OK)
    Closed --> Open: エラー連続 (例: 5回失敗)
    Note over Open: 外部通信を遮断し、<br/>即座にエラーを返す
    Open --> HalfOpen: 一定時間経過<br/>(テスト通信へ)
    HalfOpen --> Closed: テスト通信成功！
    HalfOpen --> Open: テスト通信失敗...
```""",
"""```mermaid
stateDiagram-v2
    [*] --> Closed : 通常状態(通信OK)
    Closed --> Open : エラー連続
    note right of Open: 外部通信を遮断し即エラーを返す
    Open --> HalfOpen : テスト通信へ
    HalfOpen --> Closed : テスト通信成功!
    HalfOpen --> Open : テスト通信失敗...
```"""
        )
    ],
    "14_Observability.md": [
        (
"""```mermaid
graph TD
    System[Distributed System]
    
    System -->|1. テキスト記録| Logs[Log Management<br>(Elasticsearch, Splunk)]
    System -->|2. 数値集計| Metrics[Metrics Dashboards<br>(Prometheus, Grafana)]
    System -->|3. 通信経路追跡| Trace[Distributed Tracing<br>(Jaeger, Datadog)]
    
    Logs -.->|相関分析| Observ[Observability<br>"なぜシステムが遅いか？"を特定]
    Metrics -.->|相関分析| Observ
    Trace -.->|相関分析| Observ
```""",
"""```mermaid
graph TD
    System["Distributed System"]
    
    System -->|"1. テキスト記録"| Logs["Log Management<br>(Elasticsearch, Splunk)"]
    System -->|"2. 数値集計"| Metrics["Metrics Dashboards<br>(Prometheus, Grafana)"]
    System -->|"3. 通信経路追跡"| Trace["Distributed Tracing<br>(Jaeger, Datadog)"]
    
    Logs -.->|相関分析| Observ["Observability<br>なぜシステムが遅いかを特定"]
    Metrics -.->|相関分析| Observ
    Trace -.->|相関分析| Observ
```"""
        )
    ],
    "16_Data_Pipelines.md": [
        (
"""```mermaid
graph LR
    subgraph "Backend System (App)"
        API[App API] --> DB[(Primary SQL DB)]
        API -->|1. 行動イベント発火| Kafka[Message Queue<br>Pub/Sub]
    end

    subgraph "Data Engineering Pipeline"
        Kafka -->|2. Stream (秒単位)| Flink[Stream Processing]
        DB -.->|3. Batch ETL (毎晩)| Spark[Batch Processing / Spark]
        
        Flink --> S3[(Object Storage<br>Data Lake)]
        Spark --> S3
        
        S3 --> DWH[(Data Warehouse<br>例えば Databricks)]
    end
```""",
"""```mermaid
graph LR
    subgraph "Backend System (App)"
        API["App API"] --> DB[("Primary SQL DB")]
        API -->|"1. 行動イベント発火"| Kafka["Message Queue<br>Pub/Sub"]
    end

    subgraph "Data Engineering Pipeline"
        Kafka -->|"2. Stream (秒単位)"| Flink["Stream Processing"]
        DB -.->|"3. Batch ETL (毎晩)"| Spark["Batch Processing / Spark"]
        
        Flink --> S3[("Object Storage<br>Data Lake")]
        Spark --> S3
        
        S3 --> DWH[("Data Warehouse<br>例えば Databricks")]
    end
```"""
        )
    ]
}

for filename, rules in replacements.items():
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        for old_t, new_t in rules:
            content = content.replace(old_t, new_t)
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed mermaid in {filename}")

# Run fix_bundle.py to update dashboard_data.js
os.system(f"python {os.path.join(base_dir, 'fix_bundle.py')}")

print("Fixed local diagrams and updated the bundle!")
