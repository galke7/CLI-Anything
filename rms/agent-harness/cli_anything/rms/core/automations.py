"""Automations management for RMS API."""
from __future__ import annotations
from cli_anything.rms.utils.rms_backend import api_get


def list_automations(token, company_id=None, limit=25, offset=0, sort=None, q=None):
    params = {"limit": limit, "offset": offset}
    if company_id is not None:
        params["company_id"] = company_id
    if sort is not None:
        params["sort"] = sort
    if q is not None:
        params["q"] = q
    return api_get("/automations", params=params, token=token)


def get_automation(token, automation_id):
    return api_get(f"/automations/{automation_id}", token=token)


def get_device_automations(token, device_id, limit=25, offset=0, sort=None):
    params = {"limit": limit, "offset": offset}
    if sort is not None:
        params["sort"] = sort
    return api_get(f"/devices/{device_id}/automations", params=params, token=token)


def list_automation_logs(token, automation_id, start_date=None, end_date=None):
    params = {}
    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date
    return api_get(f"/automations/{automation_id}/logs", params=params, token=token)
