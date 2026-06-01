#!/usr/bin/env python3
"""
DB Demo Studio — db-engine 统一连接器

双引擎（MySQL + PostgreSQL）连接与 EXPLAIN 工具。
支持：
  - 连接 MySQL 8 / PG 16
  - 执行 SQL 查询
  - EXPLAIN ANALYZE / EXPLAIN (FORMAT JSON)
  - JOIN 演示默认 SQL
"""

import os
import json
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ── 默认 JOIN SQL（对齐 examples/join-query.json）─────────────
JOIN_SQL = (
    "SELECT s.name, c.course_name "
    "FROM students s "
    "INNER JOIN courses c ON s.id = c.student_id"
)

# ── MySQL 连接器 ──────────────────────────────────────────────


class MySQLConnector:
    """通过 pymysql 连接 MySQL 8"""
    def __init__(self):
        self.conn = None
        self.host = os.getenv("MYSQL_HOST", "127.0.0.1")
        self.port = int(os.getenv("MYSQL_PORT", "3308"))
        self.user = os.getenv("MYSQL_USER", "demo")
        self.password = os.getenv("MYSQL_PASSWORD", "demo_pass")
        self.database = os.getenv("MYSQL_DATABASE", "db_demo")

    def connect(self):
        import pymysql
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        return self.conn

    def query(self, sql: str) -> list[dict]:
        if not self.conn:
            self.connect()
        import pymysql
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def explain(self, sql: str) -> dict:
        """返回 EXPLAIN FORMAT=JSON"""
        if not self.conn:
            self.connect()
        import pymysql
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(f"EXPLAIN FORMAT=JSON {sql}")
        row = cursor.fetchone()
        cursor.close()
        return row

    def close(self):
        if self.conn:
            self.conn.close()

# ── PostgreSQL 连接器 ──────────────────────────────────────────


class PGConnector:
    """通过 psycopg2 连接 PostgreSQL 16"""
    def __init__(self):
        self.conn = None
        self.host = os.getenv("PG_HOST", "127.0.0.1")
        self.port = int(os.getenv("PG_PORT", "5433"))
        self.user = os.getenv("PG_USER", "demo")
        self.password = os.getenv("PG_PASSWORD", "demo_pass")
        self.database = os.getenv("PG_DATABASE", "db_demo")

    def connect(self):
        import psycopg2
        import psycopg2.extras
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.database,
        )
        return self.conn

    def query(self, sql: str) -> list[dict]:
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        return [dict(r) for r in rows]

    def explain(self, sql: str) -> dict:
        """返回 EXPLAIN (FORMAT JSON)"""
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(f"EXPLAIN (FORMAT JSON) {sql}")
        row = cursor.fetchone()
        cursor.close()
        return {"QUERY PLAN": row[0]} if row else {}

    def close(self):
        if self.conn:
            self.conn.close()

# ── 工厂函数 ────────────────────────────────────────────


def get_mysql() -> MySQLConnector:
    return MySQLConnector()


def get_pg() -> PGConnector:
    return PGConnector()


def explain_both(sql: str = JOIN_SQL) -> dict:
    """同时对 MySQL + PG 执行 EXPLAIN，返回对照结果"""
    result = {"mysql": None, "postgres": None, "error": None}
    try:
        mysql = get_mysql()
        mysql.connect()
        result["mysql"] = mysql.explain(sql)
        mysql.close()
    except Exception as e:
        result["mysql"] = {"error": str(e)}

    try:
        pg = get_pg()
        pg.connect()
        result["postgres"] = pg.explain(sql)
        pg.close()
    except Exception as e:
        result["postgres"] = {"error": str(e)}

    return result


# ── CLI ────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "join"
    engine = sys.argv[2] if len(sys.argv) > 2 else "both"

    if cmd == "join":
        print(f"\nSQL: {JOIN_SQL}\n")

        if engine in ("both", "mysql"):
            try:
                m = get_mysql()
                m.connect()
                rows = m.query(JOIN_SQL)
                print(f"[MySQL] 结果: {len(rows)} 行")
                for r in rows:
                    print(f"  {r}")
                print(f"[MySQL] EXPLAIN: {json.dumps(m.explain(JOIN_SQL), indent=2, ensure_ascii=False)}")
                m.close()
            except Exception as e:
                print(f"[MySQL] 错误: {e}")

        if engine in ("both", "postgres"):
            try:
                p = get_pg()
                p.connect()
                rows = p.query(JOIN_SQL)
                print(f"\n[PostgreSQL] 结果: {len(rows)} 行")
                for r in rows:
                    print(f"  {r}")
                print(f"[PostgreSQL] EXPLAIN: {json.dumps(p.explain(JOIN_SQL), indent=2, ensure_ascii=False)}")
                p.close()
            except Exception as e:
                print(f"[PostgreSQL] 错误: {e}")

    elif cmd == "explain":
        sql = sys.argv[2] if len(sys.argv) > 2 else JOIN_SQL
        result = explain_both(sql)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print("用法: python connector.py [join|explain] [mysql|postgres|both]")
