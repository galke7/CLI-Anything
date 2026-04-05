"""Unit tests for metrics core module and CLI commands."""
from __future__ import annotations

import json
import os
from unittest.mock import patch

import pytest


# ── Core module tests ─────────────────────────────────────────────────


class TestMetricsCore:
    """Tests for cli_anything.rms.core.metrics functions."""

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_graph_data(self, mock_get):
        from cli_anything.rms.core.metrics import get_graph_data

        mock_get.return_value = {"success": True, "data": [{"ts": "2026-03-01", "value": 42}]}
        result = get_graph_data("tok", "100", "dynamic", "2026-03-01 00:00:00", "2026-03-02 00:00:00")

        assert result["success"] is True
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == "/devices/100/information/dynamic"
        assert kwargs["params"]["start_date"] == "2026-03-01 00:00:00"
        assert kwargs["params"]["end_date"] == "2026-03-02 00:00:00"

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_information_history(self, mock_get):
        from cli_anything.rms.core.metrics import get_information_history

        mock_get.return_value = {"success": True, "data": {"firmware": "7.6.1"}}
        result = get_information_history("tok", "100", "2026-03-01 12:00:00")

        assert result["success"] is True
        args, kwargs = mock_get.call_args
        assert args[0] == "/devices/100/information-history"
        assert kwargs["params"]["datetime"] == "2026-03-01 12:00:00"

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_information_history_parameter(self, mock_get):
        from cli_anything.rms.core.metrics import get_information_history_parameter

        mock_get.return_value = {"success": True, "data": {"signal": -65}}
        result = get_information_history_parameter("tok", "100", "2026-03-01 12:00:00", "signal")

        assert result["success"] is True
        args, kwargs = mock_get.call_args
        assert args[0] == "/devices/100/information-history/parameter"
        assert kwargs["params"]["parameter"] == "signal"

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_available_datetimes(self, mock_get):
        from cli_anything.rms.core.metrics import get_available_datetimes

        mock_get.return_value = {"success": True, "data": ["2026-03-01 12:00:00"]}
        result = get_available_datetimes("tok", "100")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/100/information-history/datetimes"

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_data_usage(self, mock_get):
        from cli_anything.rms.core.metrics import get_data_usage

        mock_get.return_value = {"success": True, "data": {"sent": 1024, "received": 2048}}
        result = get_data_usage("tok", "100", "2026-03-01 00:00:00", "2026-03-02 00:00:00")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/100/data-usage"

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_tag_data(self, mock_get):
        from cli_anything.rms.core.metrics import get_tag_data

        mock_get.return_value = {"success": True, "data": [{"value": 55}]}
        result = get_tag_data("tok", "10", "temperature", "2026-03-01 00:00:00", "2026-03-02 00:00:00")

        assert result["success"] is True
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["parameter"] == "temperature"

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_tag_group_data(self, mock_get):
        from cli_anything.rms.core.metrics import get_tag_group_data

        mock_get.return_value = {"success": True, "data": [{"min": 20, "max": 60}]}
        result = get_tag_group_data("tok", "10", "signal", "2026-03-01 00:00:00", "2026-03-02 00:00:00")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/tags/10/group/data"

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_company_data(self, mock_get):
        from cli_anything.rms.core.metrics import get_company_data

        mock_get.return_value = {"success": True, "data": [{"value": 100}]}
        result = get_company_data("tok", "5", "sent", "2026-03-01 00:00:00", "2026-03-02 00:00:00")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/companies/5/data"

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_company_group_data(self, mock_get):
        from cli_anything.rms.core.metrics import get_company_group_data

        mock_get.return_value = {"success": True, "data": [{"min": 10, "max": 90}]}
        result = get_company_group_data("tok", "5", "received", "2026-03-01 00:00:00", "2026-03-02 00:00:00")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/companies/5/group/data"

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_fleet_statistics(self, mock_get):
        from cli_anything.rms.core.metrics import get_fleet_statistics

        mock_get.return_value = {"success": True, "data": {"model": {"RUT955": 10}}}
        result = get_fleet_statistics("tok", "model,status", model="RUT955")

        assert result["success"] is True
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["charts"] == "model,status"
        assert kwargs["params"]["model"] == "RUT955"

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_fleet_statistics_filters_none(self, mock_get):
        from cli_anything.rms.core.metrics import get_fleet_statistics

        mock_get.return_value = {"success": True, "data": {}}
        get_fleet_statistics("tok", "model", firmware=None, status=None)

        _, kwargs = mock_get.call_args
        assert "firmware" not in kwargs["params"]
        assert "status" not in kwargs["params"]

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_online_statistics(self, mock_get):
        from cli_anything.rms.core.metrics import get_online_statistics

        mock_get.return_value = {"success": True, "data": [{"date": "2026-03-01", "count": 42}]}
        result = get_online_statistics("tok", 1, "2026-03-01 00:00:00", "2026-03-02 00:00:00")

        assert result["success"] is True
        _, kwargs = mock_get.call_args
        assert "include_children" not in kwargs["params"]

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_get_online_statistics_with_children(self, mock_get):
        from cli_anything.rms.core.metrics import get_online_statistics

        mock_get.return_value = {"success": True, "data": []}
        get_online_statistics("tok", 1, "2026-03-01 00:00:00", "2026-03-02 00:00:00", include_children=True)

        _, kwargs = mock_get.call_args
        assert kwargs["params"]["include_children"] == 1


# ── CLI runner tests ──────────────────────────────────────────────────


class TestMetricsCLI:
    """Click CliRunner tests for metrics commands."""

    def setup_method(self):
        from click.testing import CliRunner
        self.runner = CliRunner()

    def test_metrics_help(self):
        from cli_anything.rms.rms_cli import cli

        result = self.runner.invoke(cli, ["metrics", "--help"])
        assert result.exit_code == 0
        assert "graph" in result.output
        assert "history" in result.output
        assert "data-usage" in result.output
        assert "statistics" in result.output

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_metrics_graph_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"ts": "2026-03-01", "temp": 45}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "--json", "metrics", "graph", "100",
                "--type", "dynamic",
                "--start", "2026-03-01 00:00:00",
                "--end", "2026-03-02 00:00:00",
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_metrics_datetimes_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": ["2026-03-01 12:00:00"]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "metrics", "datetimes", "100"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_metrics_statistics_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": {"model": {"RUT955": 10}}}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "--json", "metrics", "statistics", "--charts", "model,status",
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.metrics.api_get")
    def test_metrics_online_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"count": 42}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "--json", "metrics", "online",
                "--company-id", "1",
                "--start", "2026-03-01 00:00:00",
                "--end", "2026-03-02 00:00:00",
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    def test_metrics_graph_requires_type(self):
        from cli_anything.rms.rms_cli import cli

        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "metrics", "graph", "100",
                "--start", "2026-03-01 00:00:00",
                "--end", "2026-03-02 00:00:00",
            ])
        assert result.exit_code != 0
        assert "type" in result.output.lower() or "required" in result.output.lower()

    def test_metrics_graph_validates_type_enum(self):
        from cli_anything.rms.rms_cli import cli

        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "metrics", "graph", "100",
                "--type", "invalid",
                "--start", "2026-03-01 00:00:00",
                "--end", "2026-03-02 00:00:00",
            ])
        assert result.exit_code != 0
