#!/usr/bin/env python

import click
from vumi_http_proxy import http_proxy


@click.command()
@click.option('--interface', default="0.0.0.0", help='eg 0.0.0.0')
@click.option('--port', default=8080, help='eg 80')
def cli(interface, port):
    """This script runs vumi-http-proxy on <interface>:<port>"""
    i = http_proxy.Initialize(["asdf.com"], str(interface), port)
    click.echo("Starting connection to %s:%d" % (str(interface), port))
    i.main()
