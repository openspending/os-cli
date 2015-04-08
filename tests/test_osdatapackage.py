# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
from oscli import osdatapackage
from oscli import compat
from tests import base


class TestOpenSpendingDataPackage(base.BaseTestCase):

    def setUp(self):
        super(TestOpenSpendingDataPackage, self).setUp()
        self.valid = os.path.join(self.data_dir, 'descriptors', 'valid')
        self.invalid_no_openspending = os.path.join(self.data_dir, 'descriptors',
                                                    'invalid-no-openspending')
        self.invalid_no_openspending_descriptor = os.path.join(
            self.invalid_no_openspending, 'datapackage.json')
        self.invalid_no_owner = os.path.join(self.data_dir, 'descriptors',
                                                    'invalid-no-owner')
        self.invalid_no_owner_descriptor = os.path.join(
            self.invalid_no_owner, 'datapackage.json')

        self.invalid_no_mapping_id = os.path.join(self.data_dir, 'descriptors',
                                                  'invalid-no-mapping-id')
        self.invalid_no_mapping_id_descriptor = os.path.join(
            self.invalid_no_mapping_id, 'datapackage.json')
        self.invalid_no_mapping_amount = os.path.join(self.data_dir, 'descriptors',
                                                      'invalid-no-mapping-amount')
        self.invalid_no_mapping_amount_descriptor = os.path.join(
            self.invalid_no_mapping_amount, 'datapackage.json')

    def tearDown(self):
        super(TestOpenSpendingDataPackage, self).tearDown()

    def test_valid_descriptor_from_file(self):

        result = osdatapackage.OpenSpendingDataPackage(self.valid)
        self.assertTrue(result)

    def test_can_load_self_created_descriptor(self):
        pkg = osdatapackage.OpenSpendingDataPackage(self.valid)
        result = osdatapackage.OpenSpendingDataPackage(**pkg.as_dict())
        self.assertTrue(result)

    def test_invalid_descriptor_no_openspending_from_file(self):
        self.assertRaises(ValueError, osdatapackage.OpenSpendingDataPackage,
                          self.invalid_no_openspending)

    def test_invalid_descriptor_no_owner_from_file(self):
        self.assertRaises(ValueError, osdatapackage.OpenSpendingDataPackage,
                          self.invalid_no_owner)

    def test_invalid_descriptor_no_mapping_id_from_file(self):
        self.assertRaises(ValueError, osdatapackage.OpenSpendingDataPackage,
                          self.invalid_no_mapping_id)

    def test_invalid_descriptor_no_mapping_amount_from_file(self):
        self.assertRaises(ValueError, osdatapackage.OpenSpendingDataPackage,
                          self.invalid_no_mapping_amount)

    def test_invalid_descriptor_no_openspending_from_kwargs(self):
        with io.open(self.invalid_no_openspending_descriptor) as stream:
            kwargs = json.loads(stream.read())
        self.assertRaises(ValueError, osdatapackage.OpenSpendingDataPackage,
                          **kwargs)

    def test_invalid_descriptor_no_owner_from_kwargs(self):
        with io.open(self.invalid_no_owner_descriptor) as stream:
            kwargs = json.loads(stream.read())
        self.assertRaises(ValueError, osdatapackage.OpenSpendingDataPackage,
                          **kwargs)

    def test_invalid_descriptor_no_mapping_id_from_kwargs(self):
        with io.open(self.invalid_no_mapping_id_descriptor) as stream:
            kwargs = json.loads(stream.read())
        self.assertRaises(ValueError, osdatapackage.OpenSpendingDataPackage,
                          **kwargs)

    def test_invalid_descriptor_no_mapping_amount_from_kwargs(self):
        with io.open(self.invalid_no_mapping_amount_descriptor) as stream:
            kwargs = json.loads(stream.read())
        self.assertRaises(ValueError, osdatapackage.OpenSpendingDataPackage,
                          **kwargs)
