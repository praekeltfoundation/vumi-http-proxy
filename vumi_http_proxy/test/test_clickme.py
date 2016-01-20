#!/usr/bin/env python
# from click.testing import CliRunner
from vumi_http_proxy import clickme
from twisted.trial import unittest
from twisted.trial.unittest import SynchronousTestCase

# Testing segment


class TestClickMe(unittest.TestCase):
    def test_click(self):
        # runner = CliRunner()
        # import pdb; pdb.set_trace()
        result = SynchronousTestCase.patch(
                                           clickme.cli, clickme.cli.port, 8000)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(str(result.output).splitlines()[0], (
                         'Starting connection to 0.0.0.0:8080'))
