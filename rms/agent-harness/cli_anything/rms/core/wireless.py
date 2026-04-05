"""Wireless access point management for RMS API."""
from __future__ import annotations
from cli_anything.rms.utils.rms_backend import api_get


def list_wireless(token, wireless_id, limit=25, offset=0, q=None):
    params = {"wireless_id": wireless_id, "limit": limit, "offset": offset}
    if q is not None:
        params["q"] = q
    return api_get("/wireless", params=params, token=token)


def get_device_wireless(token, device_id):
    return api_get(f"/devices/{device_id}/wireless", token=token)


def get_wireless_graph(token, device_id, wlan, start_date, end_date):
    return api_get(f"/devices/{device_id}/wireless/graph",
                   params={"wlan": wlan, "start_date": start_date, "end_date": end_date},
                   token=token)
