# tcping

一个类似于 ping 的系统工具，
检测在连接 tcp 时候的延迟，
比较正确是反应出网络的延迟情况，毕竟 tcp 用途比较广。

虽然和 icmp 的 ping 原理不同，ping 命令也能很大程度上反映出网络的延迟，
但是该矫情还是要矫情一把的。

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

呵呵，GFW，66666
 
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

其中这个 `--report` 可以生成一个 ascii 的 table，好看一点吧。。。

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
## END 

其实写这个主要是为了测试搭建翻墙 VPS 的 tcp 延迟。。。
