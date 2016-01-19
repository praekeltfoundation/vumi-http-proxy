#!/usr/bin/env python
from click.testing import CliRunner
from vumi_http_proxy import clickme
from twisted.trial import unittest

# Testing segment


class TestClickMe(unittest.TestCase):
    def test_click(self):
        runner = CliRunner()
        clickme.test = True
        result = runner.invoke(clickme.cli)
        assert 'Starting connection to 0.0.0.0:8080' in result.output
