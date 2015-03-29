# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from goodtables import pipeline


def display_report(reports):
    """Return an output string of text tables."""
    _reports = []
    for report in reports:
        _reports.append(report.generate('txt'))
    return '\n\n'.join(_reports)


class Ensure(object):

    """Ensure that a data package is valid.

    So, ensure that each resource in a data package are valid.

    """

    def __init__(self, datapackage):
        self.pipeline_options = {'fail_fast': True, 'processors': ('schema',),
                                 'post_task': self._collector}
        self.batch = pipeline.Batch(datapackage, source_type='dp',
                                    pipeline_options=self.pipeline_options)
        self.reports = []
        self.success = True

    def run(self):
        self.batch.run()
        if any([report.count for report in self.reports]):
            self.success = False
        return self.success

    def _collector(self, pipeline):
        """Collect reports."""
        self.reports.append(pipeline.generated_report)
