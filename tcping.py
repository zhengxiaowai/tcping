#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Use tcp ping host
"""

import sys
import socket
import time
import click
import os
import json

from timeit import default_timer as timer
from prettytable import PrettyTable

USER_HOME = os.path.expanduser('~')
HOST_SET_CONFIG = os.path.join(USER_HOME, '.ipset.json')


def avg(x):
    return sum(x) / float(len(x))


def load_host_set(conf_path):
    hostset = {}
    with open(conf_path) as f:
        hostset = json.load(f)

    return hostset


def create_host_set(conf_path):
    hostset = {}
    linode_host_list = [
        'speedtest.newark.linode.com',
        'speedtest.atlanta.linode.com',
        'speedtest.dallas.linode.com',
        'speedtest.fremont.linode.com',
        'speedtest.frankfurt.linode.com',
        'speedtest.london.linode.com',
        'speedtest.singapore.linode.com',
        'speedtest.tokyo.linode.com',
        'speedtest.tokyo2.linode.com']

    vultr_host_list = [
        'hnd-jp-ping.vultr.com',
        'syd-au-ping.vultr.com',
        'fra-de-ping.vultr.com',
        'ams-nl-ping.vultr.com',
        'lon-gb-ping.vultr.com',
        'par-fr-ping.vultr.com',
        'wa-us-ping.vultr.com',
        'sjo-ca-us-ping.vultr.com',
        'lax-ca-us-ping.vultr.com',
        'il-us-ping.vultr.com',
        'tx-us-ping.vultr.com',
        'nj-us-ping.vultr.com',
        'ga-us-ping.vultr.com',
        'fl-us-ping.vultr.com']

    hostset['linode'] = map(lambda host: (host, 80), linode_host_list)
    hostset['vultr'] = map(lambda host: (host, 80), vultr_host_list)

    if not os.path.exists(conf_path):
        with open(conf_path, 'wb') as f:
            json.dump(hostset, f, indent=4)


class Socket(object):
    def __init__(self, family, type_, timeout):
        s = socket.socket(family, type_)
        s.settimeout(timeout)
        self._s = s

    def connect(self, host, port=80):
        self._s.connect((host, int(port)))

    def shutdown(self):
        self._s.shutdown(socket.SHUT_RD)

    def close(self):
        self._s.close()


class Ping(object):
    def __init__(self, host, port=80, timeout=1):
        self._successed = 0
        self._failed = 0
        self._conn_times = []
        self._host = host
        self._port = port
        self._timeout = timeout
        self._report = []

    def _create_socket(self, family, type_):
        return Socket(family, type_, self._timeout)

    def _success_rate(self):
        count = self._successed + self._failed
        try:
            rate = (float(self._successed) / count) * 100
            rate = '{0:.2f}'.format(rate)
        except ZeroDivisionError:
            rate = '0.00'
        return rate
    
    @property
    def report(self):
        x = PrettyTable()     
        x.field_names = ['Host', 'Port', 'Successed', 'Failed', 'Success Rate', 'Minimum', 'Maximum', 'Average']
        for r in self._report:
            x.add_row(r)

        return x.get_string()

    def statistics(self, n):
        conn_times = self._conn_times if self._conn_times != [] else [0]
        minimum = '{0:.2f}ms'.format(min(conn_times))
        maximum = '{0:.2f}ms'.format(max(conn_times))
        average = '{0:.2f}ms'.format(avg(conn_times))
        success_rate = self._success_rate()
        self._report.append([
            self._host,
            self._port,
            self._successed,
            self._failed,
            success_rate,
            minimum,
            maximum,
            average]) 

        print(
            '\n--- {}[:{}] tcping statistics ---'.format(self._host, self._port))
        print('{} connections, {} successed, {} failed, {}% success rate'.format(
            n, self._successed, self._failed, success_rate))
        print('minimum = {}, maximum = {}, average = {}'.format(
            minimum, maximum, average))
        
    def ping(self, count=10):

        for n in range(1, count + 1):
            s = self._create_socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                time.sleep(1)

                s_start = timer()
                s.connect(self._host, self._port)
                s.shutdown()
                s_stop = timer()

                s_runtime = 1000 * (s_stop - s_start)
                print("Connected to %s[:%s]: seq=%d time=%.2f ms" % (
                    self._host, self._port, n, s_runtime))
                self._conn_times.append(s_runtime)
            except socket.timeout:
                print("Connected to %s[:%s]: seq=%d time out!" % (
                    self._host, self._port, n))
                self._failed += 1

            except KeyboardInterrupt:
                self.statistics(n - 1)
                sys.exit(1)

            else:
                self._successed += 1

            finally:
                s.close()

        self.statistics(n)

    create_host_set(HOST_SET_CONFIG)
    hostlist = load_host_set(HOST_SET_CONFIG)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--port', '-p', default=80, type=click.INT, help='tcp port')
@click.option('--count', '-c', default=10, type=click.INT, help='try connections counts')
@click.option('--timeout', '-t', default=1, type=click.FLOAT, help='timeout seconds')
@click.argument('host')
def tcp(host, port, count, timeout):
    ping = Ping(host, port, timeout)
    ping.ping(count)
    print('\n')
    print(ping.report)


@cli.command()
@click.option('--port', '-p', default=80, type=click.INT, help='tcp port')
@click.option('--count', '-c', default=3, type=click.INT, help='try connections counts')
@click.option('--timeout', '-t', default=1, type=click.FLOAT, help='timeout seconds')
@click.argument('hostset')
def tcphosts(hostset, port, count, timeout):
    create_host_set(HOST_SET_CONFIG)
    hostlist = load_host_set(HOST_SET_CONFIG)
    hosts = hostlist[hostset]
    for host, port in hosts:
        ping = Ping(host, port, timeout)
        ping.ping(count)
        print('\n')


@cli.command()
def clean():
    click.echo('The .ipset.json file was successfully deleted')
    os.remove(HOST_SET_CONFIG)


if __name__ == '__main__':
    cli()

