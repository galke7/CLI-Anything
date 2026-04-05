"""Data collection operations for RMS API."""
from __future__ import annotations
from cli_anything.rms.utils.rms_backend import api_get


def list_configs(token, limit=25, offset=0):
    return api_get("/data-collect/configs", params={"limit": limit, "offset": offset}, token=token)


def get_config(token, config_id):
    return api_get(f"/data-collect/configs/{config_id}", token=token)


def list_assigned_configs(token, device_id=None, config_id=None):
    params = {}
    if device_id is not None:
        params["device_id"] = device_id
    if config_id is not None:
        params["config_id"] = config_id
    return api_get("/data-collect/configs/assigned", params=params, token=token)


def list_config_logs(token, limit=25, offset=0):
    return api_get("/data-collect/configs/logs", params={"limit": limit, "offset": offset}, token=token)


def get_custom_data(token, device_id, start_date, end_date, config_id=None):
    params = {"start_date": start_date, "end_date": end_date}
    if config_id is not None:
        params["config_id"] = config_id
    return api_get(f"/devices/{device_id}/custom-data", params=params, token=token)


def get_graph_data(token, field):
    return api_get("/data-collect/data/graph", params={"field": field}, token=token)


def get_available_values(token, field):
    return api_get("/data-collect/data/values", params={"field": field}, token=token)


def list_fields(token):
    return api_get("/devices/data/fields", token=token)
