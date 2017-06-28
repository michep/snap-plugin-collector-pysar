from snap_pysar import SarCollector
from snap_pysar import namespace2str

col = SarCollector('collector', 1)
mts = col.update_catalog(None)