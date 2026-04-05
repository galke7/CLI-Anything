"""Device multi-configuration management for RMS API."""
from __future__ import annotations
from cli_anything.rms.utils.rms_backend import api_get, api_post


def get_specification(token, device_id):
    return api_get("/devices/configurator/specification", params={"device_id": device_id}, token=token)


def get_configuration(token, data):
    return api_post("/devices/configurator/configuration", data=data, token=token)


def list_templates(token):
    return api_get("/devices/configurator/templates", token=token)


def list_device_logs(token, device_id):
    return api_get(f"/devices/{device_id}/configurator/logs", token=token)


def get_device_log(token, device_id, action_name):
    return api_get(f"/devices/{device_id}/configurator/logs/{action_name}", token=token)
