"""Unit tests for configurator core module and CLI commands."""
from __future__ import annotations

import json
import os
from unittest.mock import patch

import pytest


# ── Core module tests ─────────────────────────────────────────────────


class TestConfiguratorCore:
    """Tests for cli_anything.rms.core.configurator functions."""

    @patch("cli_anything.rms.core.configurator.api_get")
    def test_get_specification(self, mock_get):
        from cli_anything.rms.core.configurator import get_specification

        mock_get.return_value = {"success": True, "data": {"params": []}}
        result = get_specification("tok", "1,2,3")

        assert result["success"] is True
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["device_id"] == "1,2,3"

    @patch("cli_anything.rms.core.configurator.api_post")
    def test_get_configuration(self, mock_post):
        from cli_anything.rms.core.configurator import get_configuration

        mock_post.return_value = {"success": True, "data": {"values": {}}}
        payload = {"devices": [1, 2], "parameters": ["param1"]}
        result = get_configuration("tok", payload)

        assert result["success"] is True
        args, kwargs = mock_post.call_args
        assert args[0] == "/devices/configurator/configuration"
        assert kwargs["data"] == payload

    @patch("cli_anything.rms.core.configurator.api_get")
    def test_list_templates(self, mock_get):
        from cli_anything.rms.core.configurator import list_templates

        mock_get.return_value = {"success": True, "data": [{"id": 1, "name": "tmpl1"}]}
        result = list_templates("tok")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/configurator/templates"

    @patch("cli_anything.rms.core.configurator.api_get")
    def test_list_device_logs(self, mock_get):
        from cli_anything.rms.core.configurator import list_device_logs

        mock_get.return_value = {"success": True, "data": [{"action": "configure"}]}
        result = list_device_logs("tok", "2403606")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/2403606/configurator/logs"

    @patch("cli_anything.rms.core.configurator.api_get")
    def test_get_device_log(self, mock_get):
        from cli_anything.rms.core.configurator import get_device_log

        mock_get.return_value = {"success": True, "data": {"action": "configure"}}
        result = get_device_log("tok", "2403606", "12345")

        assert result["data"]["action"] == "configure"
        args, _ = mock_get.call_args
        assert args[0] == "/devices/2403606/configurator/logs/12345"


# ── CLI runner tests ──────────────────────────────────────────────────


class TestConfiguratorCLI:
    """Click CliRunner tests for configurator commands."""

    def setup_method(self):
        from click.testing import CliRunner
        self.runner = CliRunner()

    def test_configurator_help(self):
        from cli_anything.rms.rms_cli import cli

        result = self.runner.invoke(cli, ["configurator", "--help"])
        assert result.exit_code == 0
        assert "spec" in result.output
        assert "templates" in result.output

    @patch("cli_anything.rms.core.configurator.api_get")
    def test_configurator_spec_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": {"params": []}}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "configurator", "spec", "--device-id", "1,2,3"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.configurator.api_post")
    def test_configurator_config_json(self, mock_post):
        from cli_anything.rms.rms_cli import cli

        mock_post.return_value = {"success": True, "data": {}}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "--json", "configurator", "config",
                "--data", '{"devices": [1], "parameters": ["p1"]}',
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.configurator.api_get")
    def test_configurator_templates_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "configurator", "templates"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.configurator.api_get")
    def test_configurator_logs_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"action": "configure"}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "configurator", "logs", "2403606"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.configurator.api_get")
    def test_configurator_log_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": {"action": "configure"}}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "configurator", "log", "2403606", "12345"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
