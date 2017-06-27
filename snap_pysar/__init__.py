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
            if name == 'CPU':
                values = self.output[name].values()[0]['all']
            else:
                values = self.output[name].values()[0]
            for parameter in values:
                metric = snap.Metric()
                metric.namespace.add_static_element('mfms')
                metric.namespace.add_static_element('sar')
                metric.namespace.add_static_element(name.lower())
                metric.namespace.add_static_element(parameter.lower())
                metrics.append(metric)

        return metrics

    def collect(self, config):
        metrics = []

        self.output = self._updatemetrics()

        for name in self.output:
            if name == 'CPU':
                values = self.output[name].values()[0]['all']
            else:
                values = self.output[name].values()[0]
            for valuename in values:
                metric = snap.Metric()
                metric.namespace.add_static_element('mfms')
                metric.namespace.add_static_element('sar')
                metric.namespace.add_static_element(name.lower())
                metric.namespace.add_static_element(valuename.lower())
                metric.data = values[valuename]
                metric.tags['host'] = self.hostname
                metrics.append(metric)

        return metrics

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
