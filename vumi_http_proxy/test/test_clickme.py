#!/usr/bin/env python
from click.testing import CliRunner
from vumi_http_proxy import clickme, http_proxy
from twisted.trial import unittest

# Testing segment


class TestClickMe(unittest.TestCase):
    def test_click(self):
        runner = CliRunner()
        self.patch(http_proxy.Initialize, 'main',
                   lambda x: x)
        result = runner.invoke(clickme.cli)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.splitlines(), [
           'Starting connection to 0.0.0.0:8080',
        ])
