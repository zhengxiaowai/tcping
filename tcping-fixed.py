#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Use tcp ping host, just like ping comppand , forked form hengxiaowai/tcping
"""

import socket
import time
import click
import sys

from collections import namedtuple
from functools import partial
from six.moves import zip_longest
from six import print_
from timeit import default_timer as timer
from prettytable import PrettyTable

__version__ = "0.2-brach"

Statistics = namedtuple(
    "Statistics",
    [
        "host",
        "resolvedIP",
        "port",
        "successed",
        "failed",
        "success_rate",
        "minimum",
        "maximum",
        "average",
    ],
)

iprint = partial(print_, flush=True)


def avg(x):
    return sum(x) / float(len(x))


class Socket(object):
    def __init__(self, family, type_, timeout):
        s = socket.socket(family, type_)
        s.settimeout(timeout)
        self._s = s

    def connect(self, host, port=80):
        if ":" in host:  # Check if it's an IPv6 address
            addrinfo = socket.getaddrinfo(
                host, port, socket.AF_INET6, socket.SOCK_STREAM
            )
            self._s.connect(addrinfo[0][4])
        else:
            self._s.connect((host, int(port)))

    def shutdown(self):
        self._s.shutdown(socket.SHUT_RD)

    def close(self):
        self._s.close()


class Print(object):
    def __init__(self):
        self.table_field_names = []
        self.rows = []

    @property
    def raw(self):
        statistics_group = []
        for row in self.rows:
            total = row.successed + row.failed
            statistics_header = "\n--- {}({})[:{}] tcping statistics ---".format(
                row.host, row.resolvedIP, row.port
            )
            statistics_body = (
                "\n{} connections, {} successed, {} failed, {} success rate".format(
                    total, row.successed, row.failed, row.success_rate
                )
            )
            statistics_footer = "\nminimum = {}, maximum = {}, average = {}".format(
                row.minimum, row.maximum, row.average
            )

            statistics = statistics_header + statistics_body + statistics_footer
            statistics_group.append(statistics)

        return "".join(statistics_group)

    @property
    def table(self):
        x = PrettyTable()
        x.field_names = self.table_field_names

        for row in self.rows:
            x.add_row(row)

        return "\n" + x.get_string()

    def set_table_field_names(self, field_names):
        self.table_field_names = field_names

    def add_statistics(self, row):
        self.rows.append(row)


class Timer(object):
    def __init__(self):
        self._start = 0
        self._stop = 0

    def start(self):
        self._start = timer()

    def stop(self):
        self._stop = timer()

    def cost(self, funcs, args):
        self.start()
        for func, arg in zip_longest(funcs, args):
            if arg:
                func(*arg)
            else:
                func()

        self.stop()
        return self._stop - self._start


class Ping(object):
    def __init__(self, host, host_type, port=80, timeout=1):
        self.print_ = Print()
        self.timer = Timer()
        self._successed = 0
        self._failed = 0
        self._conn_times = []
        self._host = host
        self._port = port
        self._timeout = timeout
        self.host_type = host_type

        self.print_.set_table_field_names(
            [
                "Host",
                "Resolved IP",
                "Port",
                "Successed",
                "Failed",
                "Success Rate",
                "Minimum",
                "Maximum",
                "Average",
            ]
        )

        # Resolve IP address and store it
        self._resolved_ip = self.resolve_ip(self.host_type)

    def resolve_ip(self, host_type):
        ip = "N/A"  # Default value
        try:
            if host_type == 2:
                ip = socket.getaddrinfo(self._host, None, socket.AF_INET6)[0][4][0]
            else:
                ip = socket.getaddrinfo(self._host, None, socket.AF_INET)[0][4][0]
        except socket.gaierror:
            print(f"Error: Unable to resolve IP address for host '{self._host}', Maybe try '-6' ?")
            sys.exit(1)  # Exit the script with an error code

        return ip

    def _create_socket(self, family, type_):
        return Socket(family, type_, self._timeout)

    def _success_rate(self):
        count = self._successed + self._failed
        try:
            rate = (float(self._successed) / count) * 100
            rate = "{0:.2f}".format(rate)
        except ZeroDivisionError:
            rate = "0.00"
        return rate

    def statistics(self, n):
        conn_times = self._conn_times if self._conn_times else [0]

        if conn_times:
            minimum = "{0:.2f}ms".format(min(conn_times))
            maximum = "{0:.2f}ms".format(max(conn_times))
            average = "{0:.2f}ms".format(avg(conn_times))
        else:
            minimum = maximum = average = "N/A"

        success_rate = self._success_rate() + "%"

        self.print_.add_statistics(
            Statistics(
                self._host,
                self._resolved_ip,
                self._port,
                self._successed,
                self._failed,
                success_rate,
                minimum,
                maximum,
                average,
            )
        )

    @property
    def result(self):
        return self.print_

    @property
    def status(self):
        return self._successed == 0

    def ping(self, count=10, ipv6=False):
        for n in range(1, count + 1):
            af = socket.AF_INET if self.host_type == 1 else socket.AF_INET6
            s = self._create_socket(af, socket.SOCK_STREAM)
            try:
                time.sleep(1)
                cost_time = self.timer.cost(
                    (s.connect, s.shutdown), ((self._host, self._port), None)
                )
                s_runtime = 1000 * (cost_time)

                iprint(
                    "Connected to {} ({}:{}): tcp_seq={} time={:.2f} ms".format(
                        self._host, self._resolved_ip, self._port, n, s_runtime
                    )
                )

                self._conn_times.append(s_runtime)
            except socket.timeout:
                iprint(
                    "Connected to {} ({}:{}): tcp_seq={} time out!".format(
                        self._host, self._resolved_ip, self._port, n
                    )
                )
                self._failed += 1

            except KeyboardInterrupt:
                self.statistics(n - 1)
                raise KeyboardInterrupt()

            else:
                self._successed += 1

            finally:
                s.close()

        self.statistics(n)


@click.command()
@click.option("--port", "-p", default=80, type=click.INT, help="Tcp port")
@click.option(
    "--count", "-c", default=10, type=click.INT, help="Try connections counts"
)
@click.option("--timeout", "-t", default=1, type=click.FLOAT, help="Timeout seconds")
@click.option(
    "--report/--no-report", default=False, help="Show report to replace statistics"
)
@click.option("--ipv4", "-4", is_flag=True, help="Use IPv4")
@click.option("--ipv6", "-6", is_flag=True, help="Use IPv6")
@click.argument("host")
def cli(host, port, count, timeout, report, ipv4, ipv6):
    # If we got a bare IP
    try:
        socket.inet_pton(socket.AF_INET, host)
        # Got a valid IPv4, force the use of IPv4
        (ipv4, ipv6) = (True, False)
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, host)
            # Got a valid IPv6, force the use of IPv6
            (ipv6, ipv4) = (True, False)
        except:
            # Possibly hostname
            pass

    if ipv4 and ipv6:  # Invalid
        iprint("Cannot use IPv4 and IPv6 at the same time. ")
        sys.exit(1)
    elif ipv6:
        host_type = 2
    else:  # Defaults to IPv4 for backward compatibility
        host_type = 1

    ping = Ping(host, host_type, port, timeout)

    try:
        ping.ping(count)
    except KeyboardInterrupt:
        pass

    if report:
        iprint(ping.result.table)
    else:
        iprint(ping.result.raw)
    sys.exit(ping.status)


if __name__ == "__main__":
    cli()
