"""Unit tests for wireless core module and CLI commands."""
from __future__ import annotations

import json
import os
from unittest.mock import patch

import pytest


# ── Core module tests ─────────────────────────────────────────────────


class TestWirelessCore:
    """Tests for cli_anything.rms.core.wireless functions."""

    @patch("cli_anything.rms.core.wireless.api_get")
    def test_list_wireless(self, mock_get):
        from cli_anything.rms.core.wireless import list_wireless

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        result = list_wireless("tok", wireless_id=1)

        assert result["success"] is True
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["wireless_id"] == 1

    @patch("cli_anything.rms.core.wireless.api_get")
    def test_list_wireless_with_pagination(self, mock_get):
        from cli_anything.rms.core.wireless import list_wireless

        mock_get.return_value = {"success": True, "data": []}
        list_wireless("tok", wireless_id=1, limit=10, offset=5)

        _, kwargs = mock_get.call_args
        assert kwargs["params"]["limit"] == 10
        assert kwargs["params"]["offset"] == 5

    @patch("cli_anything.rms.core.wireless.api_get")
    def test_get_device_wireless(self, mock_get):
        from cli_anything.rms.core.wireless import get_device_wireless

        mock_get.return_value = {"success": True, "data": {"ssid": "MyAP"}}
        result = get_device_wireless("tok", "2403606")

        assert result["data"]["ssid"] == "MyAP"
        args, _ = mock_get.call_args
        assert args[0] == "/devices/2403606/wireless"

    @patch("cli_anything.rms.core.wireless.api_get")
    def test_get_wireless_graph(self, mock_get):
        from cli_anything.rms.core.wireless import get_wireless_graph

        mock_get.return_value = {"success": True, "data": {"graph": []}}
        result = get_wireless_graph("tok", "2403606", wlan="1,2",
                                     start_date="2026-03-01 00:00:00",
                                     end_date="2026-03-30 23:59:59")

        assert result["success"] is True
        args, kwargs = mock_get.call_args
        assert args[0] == "/devices/2403606/wireless/graph"
        assert kwargs["params"]["wlan"] == "1,2"
        assert kwargs["params"]["start_date"] == "2026-03-01 00:00:00"


# ── CLI runner tests ──────────────────────────────────────────────────


class TestWirelessCLI:
    """Click CliRunner tests for wireless commands."""

    def setup_method(self):
        from click.testing import CliRunner
        self.runner = CliRunner()

    def test_wireless_help(self):
        from cli_anything.rms.rms_cli import cli

        result = self.runner.invoke(cli, ["wireless", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output
        assert "get" in result.output

    @patch("cli_anything.rms.core.wireless.api_get")
    def test_wireless_list_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "wireless", "list", "--wireless-id", "1"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.wireless.api_get")
    def test_wireless_get_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": {"ssid": "MyAP"}}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "wireless", "get", "2403606"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["ssid"] == "MyAP"

    @patch("cli_anything.rms.core.wireless.api_get")
    def test_wireless_graph_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": {"graph": []}}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "--json", "wireless", "graph", "2403606", "--wlan", "1,2",
                "--start", "2026-03-01 00:00:00", "--end", "2026-03-30 23:59:59",
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
