# db-engine — MySQL + PostgreSQL EXPLAIN 沙箱

## 目录结构

```
packages/db-engine/
├── docker-compose.yml       # MySQL 8 + PG 16 容器
├── mysql/init.sql           # MySQL 初始化（students + courses 表）
├── pg/init.sql              # PG 初始化（同上）
├── connector.py             # Python 统一连接器
└── .env.example             # 连接配置模板
```

## 启动

```powershell
# 启动容器
cd packages/db-engine
copy .env.example .env       # 可选：修改密码
docker-compose up -d

# 验证连接
python connector.py join
```

## 说明

- 学生表（students）3 行 + 课程表（courses）4 行
- JOIN 示例 SQL：取两表 INNER JOIN 结果
- LLM 约束：仅 DeepSeek
- `.env` 不进 git
