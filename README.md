# Tcping

[中文](README-zh.md)

The Tcping is a network tool.
which is similar with ping.

We often use the network is based on tcp, So use tcping more accurately.

## Usage

```
pip install tcping
```

```
➜  ~ tcping api.github.com
Connected to api.github.com[:80]: seq=1 time=236.44 ms
Connected to api.github.com[:80]: seq=2 time=237.99 ms
Connected to api.github.com[:80]: seq=3 time=248.88 ms
Connected to api.github.com[:80]: seq=4 time=233.51 ms
Connected to api.github.com[:80]: seq=5 time=249.23 ms
Connected to api.github.com[:80]: seq=6 time=249.77 ms
Connected to api.github.com[:80]: seq=7 time=235.82 ms
Connected to api.github.com[:80]: seq=8 time=242.30 ms
Connected to api.github.com[:80]: seq=9 time=248.26 ms
Connected to api.github.com[:80]: seq=10 time=251.77 ms

--- api.github.com[:80] tcping statistics ---
10 connections, 10 successed, 0 failed, 100.00% success rate
minimum = 233.51ms, maximum = 251.77ms, average = 243.40ms
```

GFW Fucking.
 
```
➜  ~ tcping --help
Usage: tcping [OPTIONS] HOST

Options:
  -p, --port INTEGER      Tcp port
  -c, --count INTEGER     Try connections counts
  -t, --timeout FLOAT     Timeout seconds
  --report / --no-report  Show report to replace statistics
  --help  
```

the result is ascii table by using `--report`.

```
➜  ~ tcping api.github.com -c 3 --report
Connected to api.github.com[:80]: seq=1 time=237.79 ms
Connected to api.github.com[:80]: seq=2 time=237.72 ms
Connected to api.github.com[:80]: seq=3 time=258.53 ms

+----------------+------+-----------+--------+--------------+----------+----------+----------+
|      Host      | Port | Successed | Failed | Success Rate | Minimum  | Maximum  | Average  |
+----------------+------+-----------+--------+--------------+----------+----------+----------+
| api.github.com |  80  |     3     |   0    |   100.00%    | 237.72ms | 258.53ms | 244.68ms |
+----------------+------+-----------+--------+--------------+----------+----------+----------+
```

The return code can be catch by some real-time test tools. Following is an example:

```python
import subprocess as sp

# Print the return code (status=0 mean ping success)
status = sp.call(['tcping', '-c', '1', '-t', '1', 'github.com'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
print(status)

# OR print the full message
status = sp.run(['tcping', '-c', '1', '-t', '1', 'github.com'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
print(status)
```

## END 

Huh, I just want to check my VPS's network status.

