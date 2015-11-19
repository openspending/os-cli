# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from goodtables import pipeline


class ValidateData(object):
    """Check that data resources in a data package are valid.

    Args:
        path (str): Path to the datapackage dir.
    """

    # Public

    def __init__(self, datapackage):
        self.pipeline_options = {'processors': ('schema',)}
        self.batch = pipeline.Batch(
            datapackage, source_type='datapackage',
            pipeline_options=self.pipeline_options,
            pipeline_post_task=self.__collect)
        self.reports = []
        self.success = False

    def run(self):
        """Run validation.
        """
        self.success = self.batch.run()
        return self.success

    @classmethod
    def display_report(cls, reports):
        """Return an output string of text tables.
        """

        # Prepare
        _reports = []
        _exclude = ['result_context', 'processor', 'row_name', 'result_category',
                    'column_index', 'column_name', 'result_level']

        # Iterate over reports
        for report in reports:
            generated = report.generate('txt', exclude=_exclude)
            modified = generated.split('###')
            _reports.append(modified[1])

        # Return joined reports
        return '\n\n'.join(_reports)

    # Private

    def __collect(self, pipeline):
        """Collect reports.
        """
        self.reports.append(pipeline.report)
