import socket
import subprocess as sp
import snap_plugin.v1 as snap
from sar import parser


class SarCollector(snap.Collector):
    output = {}

    def __init__(self, *args, **kwargs):
        self.hostname = socket.gethostname().lower()
        super(SarCollector, self).__init__(*args, **kwargs)

    def update_catalog(self, config):
        metrics = []

        self.output = self._updatemetrics()

        for name in self.output:
            enums = self.output[name].values()[0]
            for enum in enums:
                values = enums[enum]
                for parameter in values:
                    metric = snap.Metric()
                    metric.namespace.add_static_element('mfms')
                    metric.namespace.add_static_element('sar')
                    metric.namespace.add_static_element(name.lower())
                    if name == 'CPU':
                        metric.namespace.add_dynamic_element("cpu_id", "CPU ID")
                    if name == 'IFACE':
                        metric.namespace.add_dynamic_element("iface_id", "IFACE ID")
                    metric.namespace.add_static_element(parameter.lower())
                    metrics.append(metric)
                break

        return metrics

    def collect(self, metrics):
        outmetrics = []

        self.output = self._updatemetrics()

        for name in self.output:
            enums = self.output[name].values()[0]
            for enum in enums:
                values = enums[enum]
                for parameter in values:
                    metric = snap.Metric()
                    metric.namespace.add_static_element('mfms')
                    metric.namespace.add_static_element('sar')
                    metric.namespace.add_static_element(name.lower())
                    if name == 'CPU':
                        metric.namespace.add_dynamic_element("cpu_id", "CPU ID")
                        metric.namespace[3].value = enum
                    if name == 'IFACE':
                        metric.namespace.add_dynamic_element("iface_id", "IFACE ID")
                        metric.namespace[3].value = enum
                    metric.namespace.add_static_element(parameter.lower())
                    metric.data = values[parameter]
                    metric.tags['host'] = self.hostname
                    outmetrics.append(metric)

        return outmetrics

    def get_config_policy(self):
        return snap.ConfigPolicy()

    def _updatemetrics(self):
        proc = sp.Popen(['sar', '-A', '1', '1'], stdout=sp.PIPE) #TODO: check 'sar' availability
        out = proc.stdout.read()
        stdout = out.encode('utf-8')

        sar = parser.Parser('')
        chunks = sar._split_file(stdout)
        output = sar._parse_file(chunks)
        return output


def namespace2str(ns, verb = False):
    st = ''
    for e in ns:
        if verb:
            st = (st + '/' + "[" + e.name + "]") if e.name else (st + '/' + e.value)
        else:
            st = st + '/' + e.value
    return st
