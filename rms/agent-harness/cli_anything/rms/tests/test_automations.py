"""Unit tests for automations core module and CLI commands."""
from __future__ import annotations

import json
import os
from unittest.mock import patch

import pytest


# ── Core module tests ─────────────────────────────────────────────────


class TestAutomationsCore:
    """Tests for cli_anything.rms.core.automations functions."""

    @patch("cli_anything.rms.core.automations.api_get")
    def test_list_automations(self, mock_get):
        from cli_anything.rms.core.automations import list_automations

        mock_get.return_value = {"success": True, "data": [{"id": 1, "name": "auto1"}]}
        result = list_automations("tok")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/automations"

    @patch("cli_anything.rms.core.automations.api_get")
    def test_list_automations_with_filters(self, mock_get):
        from cli_anything.rms.core.automations import list_automations

        mock_get.return_value = {"success": True, "data": []}
        list_automations("tok", company_id=5, limit=10, offset=5, sort="-name")

        _, kwargs = mock_get.call_args
        assert kwargs["params"]["company_id"] == 5
        assert kwargs["params"]["limit"] == 10
        assert kwargs["params"]["offset"] == 5
        assert kwargs["params"]["sort"] == "-name"

    @patch("cli_anything.rms.core.automations.api_get")
    def test_get_automation(self, mock_get):
        from cli_anything.rms.core.automations import get_automation

        mock_get.return_value = {"success": True, "data": {"id": 42, "name": "auto1"}}
        result = get_automation("tok", "42")

        assert result["data"]["id"] == 42
        args, _ = mock_get.call_args
        assert args[0] == "/automations/42"

    @patch("cli_anything.rms.core.automations.api_get")
    def test_get_device_automations(self, mock_get):
        from cli_anything.rms.core.automations import get_device_automations

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        result = get_device_automations("tok", "2403606")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/2403606/automations"

    @patch("cli_anything.rms.core.automations.api_get")
    def test_get_device_automations_with_pagination(self, mock_get):
        from cli_anything.rms.core.automations import get_device_automations

        mock_get.return_value = {"success": True, "data": []}
        get_device_automations("tok", "2403606", limit=10, offset=5)

        _, kwargs = mock_get.call_args
        assert kwargs["params"]["limit"] == 10
        assert kwargs["params"]["offset"] == 5

    @patch("cli_anything.rms.core.automations.api_get")
    def test_list_automation_logs(self, mock_get):
        from cli_anything.rms.core.automations import list_automation_logs

        mock_get.return_value = {"success": True, "data": [{"id": 1, "status": "ok"}]}
        result = list_automation_logs("tok", "42")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/automations/42/logs"


# ── CLI runner tests ──────────────────────────────────────────────────


class TestAutomationsCLI:
    """Click CliRunner tests for automations commands."""

    def setup_method(self):
        from click.testing import CliRunner
        self.runner = CliRunner()

    def test_automations_help(self):
        from cli_anything.rms.rms_cli import cli

        result = self.runner.invoke(cli, ["automations", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output
        assert "get" in result.output

    @patch("cli_anything.rms.core.automations.api_get")
    def test_automations_list_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "automations", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.automations.api_get")
    def test_automations_get_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": {"id": 42}}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "automations", "get", "42"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["id"] == 42

    @patch("cli_anything.rms.core.automations.api_get")
    def test_automations_device_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "automations", "device", "2403606"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.automations.api_get")
    def test_automations_logs_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "automations", "logs", "42"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
