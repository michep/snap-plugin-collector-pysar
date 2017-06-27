from snap_pysar import SarCollector

col = SarCollector('collector', 1)
print(col.collect(None))