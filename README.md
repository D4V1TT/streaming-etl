C:\Users\user\.local\bin\uv.exe run C:/dev/streaming-etl/.venv/Scripts/python.exe C:\dev\streaming-etl\src\benchmarks\bench_memory.py 
      rows | approach           |   peak MB |  seconds |  file MB
--------------------------------------------------------------------
   100,000 | eager_whole_file   |      53.2 |     0.74 |      3.6
   100,000 | eager_rows_only    |      40.9 |     2.41 |      3.6
   100,000 | lazy               |       0.0 |     1.13 |      3.6
--------------------------------------------------------------------
   500,000 | eager_whole_file   |     268.8 |     7.38 |     18.8
   500,000 | eager_rows_only    |     205.4 |     7.13 |     18.8
   500,000 | lazy               |       0.0 |     6.86 |     18.8
--------------------------------------------------------------------
 2,000,000 | eager_whole_file   |    1083.7 |    28.67 |     77.6
 2,000,000 | eager_rows_only    |     824.5 |    31.97 |     77.6
 2,000,000 | lazy               |       0.0 |    26.09 |     77.6
--------------------------------------------------------------------

