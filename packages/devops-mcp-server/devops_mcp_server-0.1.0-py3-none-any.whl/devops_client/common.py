import datetime
import hashlib
import math
import os
import time
from datetime import datetime as dt
from typing import Any

import httpx

PROJECT_ID = "1309452422001967104"
TENANT_CODE = "22"
global_ticket = os.environ.get("DEVOPS_TICKET")
global_userId = os.environ.get("DEVOPS_USERID")
global_user_acct = os.environ.get("DEVOPS_USERNAME")
global_user_pwd = os.environ.get("DEVOPS_PASSWORD")


async def _get_ticket():
    global global_ticket
    if not global_ticket or not await _is_valid_ticket(global_ticket):
        token = await _get_token()
        if not token:
            raise Exception("获取token失败，请检查用户名和密码是否正确")
        global_ticket = token_to_ticket(token)
    return global_ticket


async def _is_valid_ticket(ticket):
    url = "http://devops.yusys.com.cn/devops-api/agile/workflow/isOpenWorkflow"
    headers = await _get_headers(ticket)
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url=url, headers=headers, timeout=30)
            r.raise_for_status()
            json = r.json()
            if json["code"] == "200":
                return True
            else:
                print(f"票据失效，错误信息：{json}")
                return False
        except Exception as e:
            print(f"请求失败，错误信息：{e}")
            return False


async def _get_token():
    global global_user_acct
    global global_user_pwd
    if not global_user_acct or not global_user_pwd:
        raise Exception("请设置环境变量DEVOPS_USERNAME和DEVOPS_PASSWORD")
    if len(global_user_pwd) < 32:
        global_user_pwd = hashlib.md5(global_user_pwd.encode()).hexdigest().lower()
    url = "http://devops.yusys.com.cn/devops-api/facade/user/login"
    data = {
        "loginType": 1,
        "userAcct": global_user_acct,
        "userPwd": global_user_pwd,
    }
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(url=url, json=data, timeout=30)
            r.raise_for_status()
            json = r.json()
            if json["code"] == "200":
                global global_userId
                global_userId = json["data"]["userId"]
                return json["data"]["token"].replace("-", "")
            else:
                print(f"登录失败，错误信息：{json}")
                return None
        except Exception as e:
            print(f"请求失败，错误信息：{e}")
            return None


async def token_to_ticket(token):
    pass


async def _get_headers(ticket: str = None):
    ticket = ticket or await _get_ticket()
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://devops.yusys.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
        "currentTime": str(math.floor(time.time() * 1000)),
        "language": "zh",
        "projectId": PROJECT_ID,
        "tenantCode": TENANT_CODE,
        "ticket": ticket,
    }


def date_to_timestamp(date: datetime.date):
    dt1 = dt.combine(date, dt.min.time())
    return int(dt1.timestamp() * 1000)


def calc_work_hours_between_days(start_date: datetime.date, end_date: datetime.date):
    """计算两个工作日之间的工时，不包括周末，如果是同一天返回8小时"""
    if start_date == end_date:
        return 8
    work_hours = 0
    while start_date < end_date:
        if start_date.weekday() < 5:
            work_hours += 8
        start_date += datetime.timedelta(days=1)
    return work_hours


async def do_get(url, url_param) -> dict[str, Any] | None:
    headers = await _get_headers()
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url=url, headers=headers, params=url_param, timeout=30)
            r.raise_for_status()
            json = r.json()
            if json["code"] == "200":
                return json
            else:
                print(f"服务器报错，错误信息：{json}")
                return None
        except Exception as e:
            print(f"请求失败，错误信息：{e}")
            return None


async def do_post(url, body_json) -> dict[str, Any] | None:
    headers = await _get_headers()
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(url=url, headers=headers, json=body_json, timeout=30)
            r.raise_for_status()
            json = r.json()
            if json["code"] == "200":
                return json
            else:
                print(f"服务器报错，错误信息：{json}")
                return None
        except Exception as e:
            print(f"请求失败，错误信息：{e}")
            return None
