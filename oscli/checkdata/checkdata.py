# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import os
from goodtables import pipeline


GUIDEPATH = os.path.join(os.path.dirname(__file__), 'guide.md')


def print_guide():
    with io.open(GUIDEPATH, mode='r+t', encoding='utf-8') as stream:
        output = stream.read()
    return output

def display_report(reports):
    """Return an output string of text tables."""
    _reports = []
    _exclude = ['result_context', 'processor', 'row_name', 'result_category',
                'column_index', 'column_name', 'result_level']

    for report in reports:
        generated = report.generate('txt', exclude=_exclude)
        modified = generated.split('###')
        _reports.append(modified[1])
    return '\n\n'.join(_reports)


class Checker(object):

    """Check that data resources in a data package are valid."""

    def __init__(self, datapackage):
        self.pipeline_options = {'processors': ('schema',)}
        self.batch = pipeline.Batch(datapackage, source_type='datapackage',
                                    pipeline_options=self.pipeline_options,
                                    pipeline_post_task=self._collector)
        self.reports = []
        self.success = False

    def run(self):
        self.success = self.batch.run()
        return self.success

    def _collector(self, pipeline):
        """Collect reports."""
        self.reports.append(pipeline.report)
