# Advent of Code 2019
My competitive advent of Code 2019 solutions, written in Python.

## Support Libraries

Some components were used in several different days, so I refactored them into standalone libraries. 

- [**coords.py**](https://github.com/kentonlam/aoc-2019/blob/master/coords.py): 2D coordinate system based on Python's complex numbers. Originall by [mb](http://github.com/MaxwellBo).
- [**intcode.py**](https://github.com/kentonlam/aoc-2019/blob/master/intcode.py): Virtual machine for the [Intcode](https://esolangs.org/wiki/Intcode) language. Supports input/output, various parameter modes and various calculation/comparison operations.
- [**san.py**](https://github.com/kentonlam/aoc-2019/blob/master/san.py): Chainable Python iterator functions like `.map(...).filter(...).collect()`.


## Personal Stats

I finished [85th worldwide](https://adventofcode.com/2019/leaderboard), with only 3 challenges uncompleted. 
Most notably, I finished 14th/32nd on day 7 and 17th/7th on day 23.

```
You have 853 points.

      -------Part 1--------   -------Part 2--------
Day       Time  Rank  Score       Time  Rank  Score
 24   00:12:59   142      0          -     -      -
 23   00:06:35    17     84   00:09:55     7     94
 22   00:16:28   198      0   08:08:07   638      0
 21   00:14:33    76     25       >24h  2832      0
 20       >24h  3303      0          -     -      -
 19   00:02:50    52     49   00:42:38   256      0
 18   00:50:40   103      0   01:14:54    36     65
 17   00:05:45    36     65       >24h  4072      0
 16   00:19:19   367      0   03:11:08   744      0
 15   06:42:37  2221      0   06:53:42  1915      0
 14   00:16:48    29     72   08:03:38  2130      0
 13   00:02:18    26     75   04:39:28  2707      0
 12   00:16:50   338      0   00:40:02   127      0
 11   00:09:41    67     34   00:12:58    54     47
 10   00:45:38   827      0   01:19:30   470      0
  9   00:13:57   101      0   00:14:19    96      5
  8   00:03:43    46     55   00:13:56   207      0
  7   00:05:09    14     87   00:21:51    32     69
  6   00:17:51   924      0   01:04:31  2038      0
  5   00:16:21   127      0   00:20:29    74     27
  4   00:06:07   613      0   00:11:03   390      0
  3   00:10:50   148      0   00:17:00   168      0
  2   00:07:49   198      0   00:19:17   580      0
  1   00:01:35   137      0   00:05:02   160      0
```
