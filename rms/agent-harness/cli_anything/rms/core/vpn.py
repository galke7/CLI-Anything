"""VPN hub management for RMS API."""
from __future__ import annotations
from cli_anything.rms.utils.rms_backend import api_get


def list_hubs(token, company_id=None, enabled=None, tag_id=None, limit=25, offset=0, q=None):
    params = {"limit": limit, "offset": offset}
    if company_id is not None:
        params["company_id"] = company_id
    if enabled is not None:
        params["enabled"] = enabled
    if tag_id is not None:
        params["tag_id"] = tag_id
    if q is not None:
        params["q"] = q
    return api_get("/vpn/hubs", params=params, token=token)


def get_hub_info(token, hub_id):
    return api_get(f"/vpn/hubs/{hub_id}/info", token=token)


def list_hub_sessions(token, hub_id):
    return api_get(f"/vpn/hubs/{hub_id}/sessions", token=token)


def get_device_vpn_status(token, device_id=None):
    params = {}
    if device_id is not None:
        params["device_id"] = device_id
    return api_get("/devices/device-vpn-status", params=params, token=token)


def list_hub_logs(token, hub_id, start_date, end_date):
    return api_get(f"/vpn/hubs/{hub_id}/logs",
                   params={"start_date": start_date, "end_date": end_date}, token=token)
