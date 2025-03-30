import datetime
from typing import Any

from . import common


async def query_sub_type():
    url = "http://devops.yusys.com.cn/devops-api/agile/project/issue/querySubType"
    url_param = {
        "pageNum": 1,
        "subTypeName": "",
        "pageSize": 10000,
        "issueType": 2,  # 任务管理
        "projectId": common.PROJECT_ID,
    }
    json = await common.do_get(url, url_param)
    return json


async def sprint_list():
    url = "http://devops.yusys.com.cn/devops-api/agile/sprint/list"
    data = {
        "pageNum": 1,
        "pageSize": 5,
        "sprintName": "",
    }
    return await common.do_post(url, data)


async def create_task(title: str,
                      description: str,
                      sub_type_id: str,
                      sprint_id: str,
                      plan_begin_date: datetime.date,
                      plan_end_date: datetime.date,
                      man_hours: int = None) -> dict[str, Any] | None:
    url = "http://devops.yusys.com.cn/devops-api/agile/createTask"
    attachment_list = []
    custom_field_list = [{"fieldName": "产品条线", "fieldId": "100437", "fieldCode": "code100437", "fieldValue": "1732506112826"}]
    default_field_list = [
        {"fieldName": "标题", "fieldId": "1", "fieldCode": "title", "fieldValue": title},
        {"fieldName": "类型", "fieldId": "2", "fieldCode": "subTypeId", "fieldValue": sub_type_id},
        {"fieldName": "当前处理人", "fieldId": "3", "fieldCode": "handler", "fieldValue": common.global_userId},
        {"fieldName": "迭代", "fieldId": "8", "fieldCode": "sprintId", "fieldValue": sprint_id},
        {"fieldName": "计划开始日期", "fieldId": "4", "fieldCode": "beginDate", "fieldValue": common.date_to_timestamp(plan_begin_date)},
        {"fieldName": "计划结束日期", "fieldId": "5", "fieldCode": "endDate", "fieldValue": common.date_to_timestamp(plan_end_date)},
        {"fieldName": "预计工时(小时)", "fieldId": "11", "fieldCode": "planWorkload", "fieldValue": man_hours if man_hours else common.calc_work_hours_between_days(plan_begin_date, plan_end_date)},
    ]
    description = description
    html_description = f"""<p>{description}</p>"""
    tag_list = []
    data = {
        "attachmentList": attachment_list,
        "customFieldList": custom_field_list,
        "defaultFieldList": default_field_list,
        "description": description,
        "htmlDescription": html_description,
        "tagList": tag_list,
    }
    print(data)
    return await common.do_post(url, data)


async def insert_hour(task_id, work_date, work_content, really_workload):
    url = "http://devops.yusys.com.cn/devops-api/agile/hour/insertHour"
    data = {
        "issueType": 2,
        "issueId": task_id,
        "projectId": common.PROJECT_ID,
        "createUid": common.global_userId,
        "workDate": common.date_to_timestamp(work_date),
        "workContent": work_content,
        "reallyWorkload": really_workload,
    }
    return await common.do_post(url, data)
