"""Device metrics and statistics operations for RMS API."""
from __future__ import annotations
from cli_anything.rms.utils.rms_backend import api_get


def get_graph_data(token, device_id, info_type, start_date, end_date):
    return api_get(
        f"/devices/{device_id}/information/{info_type}",
        params={"start_date": start_date, "end_date": end_date},
        token=token,
    )


def get_information_history(token, device_id, datetime_str):
    return api_get(
        f"/devices/{device_id}/information-history",
        params={"datetime": datetime_str},
        token=token,
    )


def get_information_history_parameter(token, device_id, datetime_str, parameter):
    return api_get(
        f"/devices/{device_id}/information-history/parameter",
        params={"datetime": datetime_str, "parameter": parameter},
        token=token,
    )


def get_available_datetimes(token, device_id):
    return api_get(f"/devices/{device_id}/information-history/datetimes", token=token)


def get_data_usage(token, device_id, start_date, end_date):
    return api_get(
        f"/devices/{device_id}/data-usage",
        params={"start_date": start_date, "end_date": end_date},
        token=token,
    )


def get_tag_data(token, tag_id, parameter, start_date, end_date):
    return api_get(
        f"/devices/tags/{tag_id}/data",
        params={"parameter": parameter, "start_date": start_date, "end_date": end_date},
        token=token,
    )


def get_tag_group_data(token, tag_id, parameter, start_date, end_date):
    return api_get(
        f"/devices/tags/{tag_id}/group/data",
        params={"parameter": parameter, "start_date": start_date, "end_date": end_date},
        token=token,
    )


def get_company_data(token, company_id, parameter, start_date, end_date):
    return api_get(
        f"/devices/companies/{company_id}/data",
        params={"parameter": parameter, "start_date": start_date, "end_date": end_date},
        token=token,
    )


def get_company_group_data(token, company_id, parameter, start_date, end_date):
    return api_get(
        f"/devices/companies/{company_id}/group/data",
        params={"parameter": parameter, "start_date": start_date, "end_date": end_date},
        token=token,
    )


def get_fleet_statistics(token, charts, **filters):
    params = {"charts": charts}
    params.update({k: v for k, v in filters.items() if v is not None})
    return api_get("/devices/statistics", params=params, token=token)


def get_online_statistics(token, company_id, start_date, end_date, include_children=False):
    params = {
        "company_id": company_id,
        "start_date": start_date,
        "end_date": end_date,
    }
    if include_children:
        params["include_children"] = 1
    return api_get("/statistics/devices/online", params=params, token=token)
