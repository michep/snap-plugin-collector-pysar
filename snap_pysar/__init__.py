import socket
import re
import time
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

        self.output = self.get_sar_output()

        for name in self.output:
            enums = self.output[name].values()[0]
            for enum in enums:
                values = enums[enum]
                for parameter in values:
                    metric = self.create_metric(name, parameter)
                    metrics.append(metric)
                break

        return metrics

    def collect(self, metrics):
        outmetrics = []
        retmetrics = []
        ts_now = time.time()

        self.output = self.get_sar_output()

        for name in self.output:
            enums = self.output[name].values()[0]
            for enum in enums:
                values = enums[enum]
                for parameter in values:
                    metric = self.create_metric(name, parameter)
                    if name == 'CPU' or name == 'IFACE' or name == 'DEV':
                        metric.namespace[3].value = enum
                    metric.data = values[parameter]
                    metric.tags['host'] = self.hostname
                    metric.timestamp = ts_now
                    outmetrics.append(metric)

        for mt in metrics:
            matching = self.lookup_metric_by_namespace(mt, outmetrics)
            if len(matching):
                retmetrics.extend(matching)

        return retmetrics

    def get_config_policy(self):
        return snap.ConfigPolicy()

    def get_sar_output(self):
        proc = sp.Popen(['sar', '-Ap', '1', '1'], stdout=sp.PIPE) #TODO: check 'sar' availability
        out = proc.stdout.read()
        stdout = out.encode('utf-8')

        sar = parser.Parser('')
        chunks = sar._split_file(stdout)
        output = sar._parse_file(chunks)
        return output

    def create_metric(self, name, parameter):
        metric = snap.Metric()
        metric.namespace.add_static_element('mfms')
        metric.namespace.add_static_element('sar')
        metric.namespace.add_static_element(name.lower())
        if name == 'CPU':
            metric.namespace.add_dynamic_element("cpu_id", "CPU ID")
        if name == 'IFACE':
            metric.namespace.add_dynamic_element("iface_id", "IFACE ID")
        if name == 'DEV':
            metric.namespace.add_dynamic_element("dev_id", "DEV ID")
        metric.namespace.add_static_element(parameter.lower())
        return metric

    def namespace2str(self, ns, verb = False):
        st = ''
        for e in ns:
            if verb:
                st = (st + '/' + "[" + e.name + "]") if e.name else (st + '/' + e.value)
            else:
                st = st + '/' + e.value
        return st


    def lookup_metric_by_namespace(self, lookupmetric, metrics):
        ret = []
        lookupns = self.namespace2str(lookupmetric.namespace)
        lookupns = lookupns.replace('/', '\/').replace('*', '.*') + '$'
        nsre = re.compile(lookupns)
        for met in metrics:
            ns = self.namespace2str(met.namespace)
            match = nsre.search(ns)
            if match:
                ret.append(met)
        return ret
