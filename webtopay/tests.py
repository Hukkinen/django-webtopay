# -*- coding: UTF-8 -*-

import logging

from django.test import TestCase
from django.test.client import Client

from webtopay.forms import WebToPayResponseForm
from webtopay.signals import payment_was_successful, payment_was_flagged
from django.urls import reverse

# query string from libwebtopay tests
query = 'data=cHJvamVjdGlkPTExNDQyMyZvcmRlcmlkPXJlc2VydmF0aW9uLTgmYW1vdW50PTk4OSZwYXl0ZXh0PVUlQzUlQkVzYWt5bWFzK25yJTNBK' \
        '3Jlc2VydmF0aW9uLTgraHR0cCUzQSUyRiUyRmxvY2FsaG9zdCtwcm9qZWt0ZS4rJTI4UGFyZGF2JUM0JTk3amFzJTNBK1ZpZG1hbnRhcytaZW1' \
        'sZXJpcyUyOSZwX2ZpcnN0bmFtZT12aWRtYW50YXMmcF9sYXN0bmFtZT16ZW1sZXJpcyZwX2VtYWlsPXZpZG1hbnRhcy56ZW1sZXJpcyU0MGdtY' \
        'WlsLmNvbSZ0ZXN0PTEmbGFuZz1saXQmcGF5bWVudD1oYW56YSZjdXJyZW5jeT1FVVImY291bnRyeT1MVCZzdGF0dXM9MSZyZXF1ZXN0aWQ9MTc' \
        'zNzQzMDI5JnBheWFtb3VudD05ODkmcGF5Y3VycmVuY3k9RVVSJnZlcnNpb249MS42' \
        '&ss1=fd20a462c71de41ca0e8eca4ff2a7ee8' \
        '&ss2=V2BuLkejRhjvs03PDMYQdiMVEff6YDq2l3gI2g2bwtiJCfxPq1CuiZTiAi_ajQ5YfA6ixFNMGiI2wYl8ewXS0XkcCUEuCJqfkdb_LbNtNZQH4-z5fBpaqm2hTEO1-nrH4tHiah-ouQyEjuTty_dInY7ar2zW71sEaIzmKDDN55o%3D'

class TestVerifications(TestCase):
    def testSS1(self):
        form = WebToPayResponseForm(query)
        self.assertTrue(form.check_ss1())

    def testSS2(self):
        form = WebToPayResponseForm(query)
        self.assertTrue(form.check_ss2())

    def testSS1Fail(self):
        query2 = query.replace("fd20a462c71de41ca0e8eca4ff2a7ee8", "bad")
        form = WebToPayResponseForm(query2)
        self.assertFalse(form.check_ss1())

    def testSS2Fail(self):
        query2 = query.replace('V2BuLkejRhjvs', 'V2BuLkejRhjvs'.swapcase())
        form = WebToPayResponseForm(query2)
        self.assertFalse(form.check_ss2())

class TestSignals(TestCase):
    def setUp(self):
        self.client = Client()

    def testSuccess(self):
        self.got_signal = False
        def handle_signal(sender, **kargs):
            self.got_signal = True
            self.signal_obj = sender
        payment_was_successful.connect(handle_signal)
        resp = self.client.get(reverse('webtopay-makro') + "?" + query)
        self.assertTrue(self.got_signal)

    def testBadSS1(self):
        self.got_signal = False
        def handle_signal(sender, **kargs):
            self.got_signal = True
            self.signal_obj = sender
        payment_was_flagged.connect(handle_signal)
        query2 = query.replace("c72cffd0345f55fef6595a86e5c7caa6", "bad")
        resp = self.client.get(reverse('webtopay-makro') + "?" + query2)
        self.assertTrue(self.got_signal)

    def testBadSS2(self):
        self.got_signal = False
        def handle_signal(sender, **kargs):
            self.got_signal = True
            self.signal_obj = sender
        payment_was_flagged.connect(handle_signal)
        query2 = query.replace('FxVM5X7j2mg9w', 'FxVM5X7j2mg9w'.swapcase())
        resp = self.client.get(reverse('webtopay-makro') + "?" + query2)
        self.assertTrue(self.got_signal)

    def testBadProcessing(self):
        self.got_signal = False
        def handle_signal(sender, **kargs):
            raise Exception("broken signal handler")
        payment_was_successful.connect(handle_signal)

        logger = logging.getLogger('webtopay.views')
        old_level = logger.level
        logger.setLevel(100)
        resp = self.client.get(reverse('webtopay-makro') + "?" + query)
        logger.setLevel(old_level)
        self.assertEqual(str("OK"), str(resp.content.decode('utf-8')))
