#!/usr/bin/env python
from click.testing import CliRunner
from vumi_http_proxy import clickme, http_proxy
from twisted.trial import unittest

# Testing segment


class TestClickMe(unittest.TestCase):
    def test_click(self):
        runner = CliRunner()
        self.initializers = []
        self.patch(http_proxy.Initialize, 'main',
                   lambda x: self.initializers.append(x))
        result = runner.invoke(clickme.cli)
        [initializer] = self.initializers
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.splitlines(), [
           'Starting connection to 0.0.0.0:8080',
        ])
        self.assertEquals(type(initializer), http_proxy.Initialize)
        self.assertEquals(initializer.port, 8080)
        self.assertEquals(initializer.ip, "0.0.0.0")
