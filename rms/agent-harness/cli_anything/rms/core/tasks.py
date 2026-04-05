"""Device tasks, firmware updates, and actions for RMS API."""
from __future__ import annotations
from cli_anything.rms.utils.rms_backend import api_get, api_post, api_put


def list_tasks(token, limit=25, offset=0):
    return api_get("/devices/tasks", params={"limit": limit, "offset": offset}, token=token)


def get_task(token, task_id):
    return api_get(f"/devices/tasks/{task_id}", token=token)


def list_task_logs(token, limit=25, offset=0):
    return api_get("/devices/tasks/logs", params={"limit": limit, "offset": offset}, token=token)


def get_task_log(token, log_id):
    return api_get(f"/devices/tasks/logs/{log_id}", token=token)


def list_task_groups(token, limit=25, offset=0):
    return api_get("/devices/tasks/groups", params={"limit": limit, "offset": offset}, token=token)


def get_task_group(token, group_id):
    return api_get(f"/devices/tasks/groups/{group_id}", token=token)


def list_task_group_logs(token, limit=25, offset=0):
    return api_get("/devices/tasks/groups/logs", params={"limit": limit, "offset": offset}, token=token)


# ── Firmware updates ──


def list_updates_pending(token, limit=25, offset=0):
    return api_get("/devices/updates/pending", params={"limit": limit, "offset": offset}, token=token)


def set_updates(token, data):
    return api_put("/devices/updates/set", data=data, token=token)


def cancel_updates(token, data):
    return api_put("/devices/updates/cancel", data=data, token=token)


# ── Device actions ──


def execute_action(token, data):
    return api_post("/devices/actions", data=data, token=token)


def cancel_actions(token, data):
    return api_post("/devices/actions/cancel", data=data, token=token)


def list_action_logs(token, device_id=None, tag_id=None):
    params = {}
    if device_id is not None:
        params["device_id"] = device_id
    if tag_id is not None:
        params["tag_id"] = tag_id
    return api_get("/devices/actions/logs", params=params, token=token)
