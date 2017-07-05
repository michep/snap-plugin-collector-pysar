from snap_pysar import SarCollector


def run():
    version = 1
    SarCollector("sar-py", int(version)).start_plugin()

if __name__ == "__main__":
    run()
