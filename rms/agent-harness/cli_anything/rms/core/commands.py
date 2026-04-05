"""Device command execution for RMS API."""
from __future__ import annotations
from cli_anything.rms.utils.rms_backend import api_post


def execute_command(token, device_id, data):
    return api_post(f"/devices/{device_id}/command", data=data, token=token)
