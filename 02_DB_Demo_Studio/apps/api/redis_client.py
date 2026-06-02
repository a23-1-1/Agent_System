# apps/api/redis_client.py
# Redis 客户端 — 连接池 + 会话/消息缓存 + Pub/Sub

import json
import os
from typing import Optional
from datetime import datetime, timezone

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
TTL_SESSION = int(os.getenv("REDIS_TTL_SESSION", "86400"))       # 24h
TTL_LLM_CACHE = int(os.getenv("REDIS_TTL_LLM_CACHE", "3600"))    # 1h
MESSAGE_CACHE_SIZE = int(os.getenv("REDIS_MESSAGE_CACHE_SIZE", "50"))

_pool = None


def _get_redis():
    """Lazy-init Redis connection pool"""
    global _pool
    if _pool is None:
        import redis.asyncio as aioredis
        _pool = aioredis.ConnectionPool.from_url(
            REDIS_URL, decode_responses=True
        )
    return aioredis.Redis(connection_pool=_pool)


# ═══════════════════════════════════════════════
# 会话管理
# ═══════════════════════════════════════════════

async def set_active_session(teacher_id: str, conv_id: str, ws_conn_id: str):
    """记录活跃对话会话"""
    r = _get_redis()
    key = f"session:active:{conv_id}"
    await r.set(key, json.dumps({
        "teacherId": teacher_id,
        "wsConnectionId": ws_conn_id,
        "lastActivity": datetime.now(timezone.utc).isoformat(),
        "convId": conv_id,
    }))
    await r.expire(key, TTL_SESSION)


async def get_active_session(conv_id: str) -> Optional[dict]:
    """获取活跃会话状态"""
    r = _get_redis()
    data = await r.get(f"session:active:{conv_id}")
    if data:
        return json.loads(data)
    return None


async def remove_active_session(conv_id: str):
    """删除会话状态"""
    r = _get_redis()
    await r.delete(f"session:active:{conv_id}")


# ═══════════════════════════════════════════════
# 消息缓存
# ═══════════════════════════════════════════════

async def cache_message(conv_id: str, message: dict):
    """缓存最近消息到 Redis List，超出上限时裁剪"""
    r = _get_redis()
    key = f"conv:messages:{conv_id}"
    await r.lpush(key, json.dumps(message))
    await r.ltrim(key, 0, MESSAGE_CACHE_SIZE - 1)
    await r.expire(key, TTL_SESSION)


async def get_cached_messages(conv_id: str) -> list:
    """获取缓存的最近消息"""
    r = _get_redis()
    key = f"conv:messages:{conv_id}"
    data = await r.lrange(key, 0, -1)
    return [json.loads(d) for d in reversed(data)]


async def clear_message_cache(conv_id: str):
    """清除消息缓存"""
    r = _get_redis()
    await r.delete(f"conv:messages:{conv_id}")


# ═══════════════════════════════════════════════
# LLM 响应缓存
# ═══════════════════════════════════════════════

async def get_llm_cache(prompt_hash: str) -> Optional[str]:
    """获取 LLM 缓存"""
    r = _get_redis()
    return await r.get(f"llm:cache:{prompt_hash}")


async def set_llm_cache(prompt_hash: str, response: str):
    """设置 LLM 缓存"""
    r = _get_redis()
    await r.setex(f"llm:cache:{prompt_hash}", TTL_LLM_CACHE, response)


# ═══════════════════════════════════════════════
# 教师 Profile 缓存
# ═══════════════════════════════════════════════

async def cache_teacher_profile(teacher_id: str, profile: dict):
    """缓存教师风格配置"""
    r = _get_redis()
    await r.setex(
        f"teacher:profile:{teacher_id}",
        TTL_SESSION,
        json.dumps(profile),
    )


async def get_teacher_profile(teacher_id: str) -> Optional[dict]:
    """获取教师风格缓存"""
    r = _get_redis()
    data = await r.get(f"teacher:profile:{teacher_id}")
    if data:
        return json.loads(data)
    return None


# ═══════════════════════════════════════════════
# Pub/Sub 课堂广播
# ═══════════════════════════════════════════════

async def publish_room_event(conv_id: str, event: dict):
    """向课堂房间广播事件"""
    r = _get_redis()
    await r.publish(f"room:{conv_id}", json.dumps(event))


async def subscribe_room(conv_id: str):
    """订阅课堂房间（返回 async 订阅者）"""
    r = _get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(f"room:{conv_id}")
    return pubsub


# ═══════════════════════════════════════════════
# 健康检查
# ═══════════════════════════════════════════════

async def ping() -> bool:
    """检查 Redis 连接"""
    try:
        r = _get_redis()
        await r.ping()
        return True
    except Exception:
        return False
