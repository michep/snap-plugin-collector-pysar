from . import SarCollector


def run():
    version = 1
    SarCollector("SarCollectorPlugin-py", int(version)).start_plugin()

if __name__ == "__main__":
    run()
