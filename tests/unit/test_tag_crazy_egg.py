"""
Tests for the Crazy Egg template tags and filters.
"""

import pytest
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.crazy_egg import CrazyEggNode
from analytical.utils import AnalyticalException


@override_settings(CRAZY_EGG_ACCOUNT_NUMBER='12345678')
class CrazyEggTagTestCase(TagTestCase):
    """
    Tests for the ``crazy_egg`` template tag.
    """

    def test_tag(self):
        r = self.render_tag('crazy_egg', 'crazy_egg')
        assert '/1234/5678.js' in r

    def test_node(self):
        r = CrazyEggNode().render(Context())
        assert '/1234/5678.js' in r

    @override_settings(CRAZY_EGG_ACCOUNT_NUMBER=None)
    def test_no_account_number(self):
        with pytest.raises(AnalyticalException):
            CrazyEggNode()

    @override_settings(CRAZY_EGG_ACCOUNT_NUMBER='123abc')
    def test_wrong_account_number(self):
        with pytest.raises(AnalyticalException):
            CrazyEggNode()

    def test_uservars(self):
        context = Context({'crazy_egg_var1': 'foo', 'crazy_egg_var2': 'bar'})
        r = CrazyEggNode().render(context)
        assert "CE2.set(1, 'foo');" in r
        assert "CE2.set(2, 'bar');" in r

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = CrazyEggNode().render(context)
        assert r.startswith('<!-- Crazy Egg disabled on internal IP address')
        assert r.endswith('-->')
