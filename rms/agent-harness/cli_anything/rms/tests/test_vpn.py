"""Unit tests for VPN core module and CLI commands."""
from __future__ import annotations

import json
import os
from unittest.mock import patch

import pytest


# ── Core module tests ─────────────────────────────────────────────────


class TestVpnCore:
    """Tests for cli_anything.rms.core.vpn functions."""

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_list_hubs(self, mock_get):
        from cli_anything.rms.core.vpn import list_hubs

        mock_get.return_value = {"success": True, "data": [{"id": 1, "name": "hub1"}]}
        result = list_hubs("tok")

        assert result["success"] is True
        args, kwargs = mock_get.call_args
        assert args[0] == "/vpn/hubs"

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_list_hubs_with_filters(self, mock_get):
        from cli_anything.rms.core.vpn import list_hubs

        mock_get.return_value = {"success": True, "data": []}
        list_hubs("tok", company_id=5, enabled=1, limit=10, offset=5)

        _, kwargs = mock_get.call_args
        assert kwargs["params"]["company_id"] == 5
        assert kwargs["params"]["enabled"] == 1
        assert kwargs["params"]["limit"] == 10
        assert kwargs["params"]["offset"] == 5

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_get_hub_info(self, mock_get):
        from cli_anything.rms.core.vpn import get_hub_info

        mock_get.return_value = {"success": True, "data": {"id": 1, "name": "hub1"}}
        result = get_hub_info("tok", "1")

        assert result["data"]["id"] == 1
        args, _ = mock_get.call_args
        assert args[0] == "/vpn/hubs/1/info"

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_list_hub_sessions(self, mock_get):
        from cli_anything.rms.core.vpn import list_hub_sessions

        mock_get.return_value = {"success": True, "data": [{"device_id": 100}]}
        result = list_hub_sessions("tok", "1")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/vpn/hubs/1/sessions"

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_get_device_vpn_status(self, mock_get):
        from cli_anything.rms.core.vpn import get_device_vpn_status

        mock_get.return_value = {"success": True, "data": [{"device_id": 100, "status": "connected"}]}
        result = get_device_vpn_status("tok", device_id=100)

        assert result["success"] is True
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["device_id"] == 100

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_get_device_vpn_status_no_filter(self, mock_get):
        from cli_anything.rms.core.vpn import get_device_vpn_status

        mock_get.return_value = {"success": True, "data": []}
        get_device_vpn_status("tok")

        _, kwargs = mock_get.call_args
        assert kwargs["params"] == {}

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_list_hub_logs(self, mock_get):
        from cli_anything.rms.core.vpn import list_hub_logs

        mock_get.return_value = {"success": True, "data": [{"id": 1, "event": "connect"}]}
        result = list_hub_logs("tok", "1", "2026-03-01 00:00:00", "2026-03-30 23:59:59")

        assert result["success"] is True
        args, kwargs = mock_get.call_args
        assert args[0] == "/vpn/hubs/1/logs"
        assert kwargs["params"]["start_date"] == "2026-03-01 00:00:00"
        assert kwargs["params"]["end_date"] == "2026-03-30 23:59:59"


# ── CLI runner tests ──────────────────────────────────────────────────


class TestVpnCLI:
    """Click CliRunner tests for VPN commands."""

    def setup_method(self):
        from click.testing import CliRunner
        self.runner = CliRunner()

    def test_vpn_help(self):
        from cli_anything.rms.rms_cli import cli

        result = self.runner.invoke(cli, ["vpn", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output
        assert "get" in result.output

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_vpn_list_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "vpn", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_vpn_get_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": {"id": 1}}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "vpn", "get", "1"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["id"] == 1

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_vpn_sessions_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": []}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "vpn", "sessions", "1"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_vpn_device_status_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": []}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "vpn", "device-status"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.vpn.api_get")
    def test_vpn_logs_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "--json", "vpn", "logs", "1",
                "--start", "2026-03-01 00:00:00",
                "--end", "2026-03-30 23:59:59",
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
