"""Unit tests for data-collect core module and CLI commands."""
from __future__ import annotations

import json
import os
from unittest.mock import patch

import pytest


# ── Core module tests ─────────────────────────────────────────────────


class TestDataCollectCore:
    """Tests for cli_anything.rms.core.data_collect functions."""

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_list_configs(self, mock_get):
        from cli_anything.rms.core.data_collect import list_configs

        mock_get.return_value = {"success": True, "data": [{"id": 1, "name": "cfg1"}]}
        result = list_configs("tok")

        assert result["success"] is True
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == "/data-collect/configs"

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_get_config(self, mock_get):
        from cli_anything.rms.core.data_collect import get_config

        mock_get.return_value = {"success": True, "data": {"id": 5, "name": "modbus"}}
        result = get_config("tok", "5")

        assert result["data"]["id"] == 5
        args, _ = mock_get.call_args
        assert args[0] == "/data-collect/configs/5"

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_list_assigned_configs(self, mock_get):
        from cli_anything.rms.core.data_collect import list_assigned_configs

        mock_get.return_value = {"success": True, "data": []}
        result = list_assigned_configs("tok", device_id=42)

        assert result["success"] is True
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["device_id"] == 42

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_list_assigned_configs_by_config(self, mock_get):
        from cli_anything.rms.core.data_collect import list_assigned_configs

        mock_get.return_value = {"success": True, "data": []}
        list_assigned_configs("tok", config_id=10)

        _, kwargs = mock_get.call_args
        assert kwargs["params"]["config_id"] == 10

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_list_config_logs(self, mock_get):
        from cli_anything.rms.core.data_collect import list_config_logs

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        result = list_config_logs("tok")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/data-collect/configs/logs"

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_get_custom_data(self, mock_get):
        from cli_anything.rms.core.data_collect import get_custom_data

        mock_get.return_value = {"success": True, "data": [{"ts": "2026-03-01", "temp": 42}]}
        result = get_custom_data("tok", "100", "2026-03-01 00:00:00", "2026-03-02 00:00:00")

        assert result["success"] is True
        args, kwargs = mock_get.call_args
        assert args[0] == "/devices/100/custom-data"
        assert kwargs["params"]["start_date"] == "2026-03-01 00:00:00"

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_get_custom_data_with_config(self, mock_get):
        from cli_anything.rms.core.data_collect import get_custom_data

        mock_get.return_value = {"success": True, "data": []}
        get_custom_data("tok", "100", "2026-03-01 00:00:00", "2026-03-02 00:00:00", config_id=5)

        _, kwargs = mock_get.call_args
        assert kwargs["params"]["config_id"] == 5

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_get_graph_data(self, mock_get):
        from cli_anything.rms.core.data_collect import get_graph_data

        mock_get.return_value = {"success": True, "data": []}
        result = get_graph_data("tok", "0:/modems/status:temperature")

        assert result["success"] is True
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["field"] == "0:/modems/status:temperature"

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_get_available_values(self, mock_get):
        from cli_anything.rms.core.data_collect import get_available_values

        mock_get.return_value = {"success": True, "data": ["val1", "val2"]}
        result = get_available_values("tok", "0:/modems/status:temperature")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/data-collect/data/values"

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_list_fields(self, mock_get):
        from cli_anything.rms.core.data_collect import list_fields

        mock_get.return_value = {"success": True, "data": [{"name": "temperature"}]}
        result = list_fields("tok")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/data/fields"


# ── CLI runner tests ──────────────────────────────────────────────────


class TestDataCollectCLI:
    """Click CliRunner tests for data-collect commands."""

    def setup_method(self):
        from click.testing import CliRunner
        self.runner = CliRunner()

    def test_data_collect_help(self):
        from cli_anything.rms.rms_cli import cli

        result = self.runner.invoke(cli, ["data-collect", "--help"])
        assert result.exit_code == 0
        assert "configs" in result.output
        assert "data" in result.output
        assert "fields" in result.output

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_configs_list_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "data-collect", "configs", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_data_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"temp": 42}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "--json", "data-collect", "data", "100",
                "--start", "2026-03-01 00:00:00",
                "--end", "2026-03-02 00:00:00",
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.data_collect.api_get")
    def test_fields_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"name": "temperature"}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "data-collect", "fields"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
