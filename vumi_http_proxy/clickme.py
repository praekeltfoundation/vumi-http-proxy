#!/usr/bin/env python

import click
from vumi_http_proxy import http_proxy


@click.command()
@click.option('--interface', default="0.0.0.0", help='eg 0.0.0.0')
@click.option('--port', default=8080, help='eg 80')
def cli(interface, port):
    cli.interface = str(interface)
    cli.port = port
    """This script runs vumi-http-proxy on <interface>:<port>"""
    click.echo("Starting connection to %s:%d" % (interface, port))
    i = http_proxy.Initialize(["asdf.com"], interface, port)
    i.main()


if __name__ == '__main__':
    cli()
