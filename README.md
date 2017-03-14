# tcping

一个类似于 ping 的系统工具，
检测在连接 tcp 时候的延迟，
比较正确是反应出网络的延迟情况，比较 tcp 用途比较广。

虽然和 icmp 的 ping 原理不同，ping 命令也能很大程度上反映出网络的延迟，
但是该矫情还是要矫情一把的。

## Usage

```
➜ ~ tcping.py api.github.com
Connected to api.github.com[:80]: seq=1 time=617.20 ms
Connected to api.github.com[:80]: seq=2 time out!
Connected to api.github.com[:80]: seq=3 time=458.86 ms
Connected to api.github.com[:80]: seq=4 time=406.92 ms
Connected to api.github.com[:80]: seq=5 time=390.55 ms
Connected to api.github.com[:80]: seq=6 time=411.27 ms
Connected to api.github.com[:80]: seq=7 time=403.41 ms
Connected to api.github.com[:80]: seq=8 time=422.26 ms
Connected to api.github.com[:80]: seq=9 time out!
Connected to api.github.com[:80]: seq=10 time=411.50 ms

--- api.github.com[:80] tcping statistics ---
10 connections, 8 successed, 2 failed, 80.00% success rate
```

呵呵，GFW，66666
 
```
➜ ~ tcping.py --help
Usage: tcping.py [OPTIONS] HOST

Options:
  -p, --port INTEGER      tcp port
  -c, --count INTEGER     try connections counts
  -t, --timeout FLOAT     timeout seconds
  --report / --no-report  show report to replace statistics
  --help                  Show this message and exit.
```

其中这个 `--report` 可以生成一个 ascii 的 table，好看一点吧。。。

## END 

其实写这个主要是为了测试搭建翻墙 VPS 的 tcp 延迟。。。
