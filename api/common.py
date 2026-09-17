# -*- coding: utf-8 -*-
"""ابزارهای مشترک API — پاسخ JSON، احراز هویت، IP کلاینت، اجرای executor."""

import asyncio
import functools
import ipaddress
import json
import os

from aiohttp import web

from core import config as cfg
from core import database as db
from core.security import verify_token
from core.xray import xray
from core.router import router

_bg_tasks = set()

# پروکسی‌های مورد اعتماد (فقط این‌ها اجازه دارند XFF را تنظیم کنند)
# می‌توان با TRUSTED_PROXIES=10.0.0.0/8,172.16.0.0/12 تنظیم کرد
_TRUSTED_CIDRS = None


def _trusted_cidrs():
    global _TRUSTED_CIDRS
    if _TRUSTED_CIDRS is not None:
        return _TRUSTED_CIDRS
    raw = os.environ.get("TRUSTED_PROXIES", "").strip()
    nets = []
    if raw:
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                nets.append(ipaddress.ip_network(part, strict=False))
            except ValueError:
                pass
    # در حالت PaaS روتر محلی را همیشه اعتماد می‌کنیم
    if cfg.PAAS:
        nets.append(ipaddress.ip_network("127.0.0.0/8"))
        nets.append(ipaddress.ip_network("::1/128"))
    _TRUSTED_CIDRS = nets
    return nets


def _is_trusted(addr: str) -> bool:
    if not addr or addr == "?":
        return False
    try:
        ip = ipaddress.ip_address(addr)
    except ValueError:
        return False
    for net in _trusted_cidrs():
        if ip in net:
            return True
    return False


def _dumps(data) -> str:
    return json.dumps(data, ensure_ascii=False)


def json_ok(data, status: int = 200) -> web.Response:
    return web.json_response(data, status=status, dumps=_dumps)


def json_err(msg, status: int = 400) -> web.Response:
    return web.json_response({"error": msg}, status=status, dumps=_dumps)


async def body_json(request) -> dict:
    try:
        data = await request.json()
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def client_ip(request) -> str:
    """IP واقعی با اعتبارسنجی پروکسی (رفع SF-003).
    فقط اگر remote از پروکسی مورد اعتماد باشد، X-Forwarded-For را می‌پذیریم.
    """
    remote = request.remote or "?"
    xff = request.headers.get("X-Forwarded-For", "")
    if xff and _is_trusted(remote):
        # اولین آدرس سمت چپ معمولاً کلاینت اصلی است
        for part in xff.split(","):
            candidate = part.strip()
            if not candidate:
                continue
            try:
                ipaddress.ip_address(candidate)
                return candidate
            except ValueError:
                continue
    return remote


def bearer_token(request) -> str:
    h = request.headers.get("Authorization", "")
    if h.startswith("Bearer "):
        return h[7:].strip()
    return ""


def auth_required(fn):
    """احراز هویت + بررسی اینکه username هنوز مدیر فعال است (رفع SF-006)."""
    @functools.wraps(fn)
    async def wrapped(request):
        user = verify_token(bearer_token(request), db.get_setting("secret"))
        if not user:
            return json_err("نشست نامعتبر یا منقضی است.", 401)
        active = db.get_setting("admin_user")
        if not active or user != active:
            return json_err("نشست نامعتبر یا منقضی است.", 401)
        request["user"] = user
        return await fn(request)
    return wrapped


def path_int(request, key: str = "id"):
    try:
        return int(request.match_info[key])
    except (KeyError, ValueError):
        return None


async def run_ex(fn, *args, **kwargs):
    """اجرای تابع سنگین/همگام در thread pool تا event loop قفل نشود."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, functools.partial(fn, *args, **kwargs))


def spawn_bg(coro) -> None:
    """اجرای coroutine در پس‌زمینه بدون بلاک کردن پاسخ."""
    loop = asyncio.get_running_loop()
    t = loop.create_task(coro)
    _bg_tasks.add(t)
    t.add_done_callback(_bg_tasks.discard)


async def apply_config():
    """اعمال کانفیگ جدید روی هسته + رفرش مسیرهای روتر. → (ok, error)"""
    ok, err = await run_ex(xray.restart, "تغییر پیکربندی")
    router.refresh()
    return ok, err
