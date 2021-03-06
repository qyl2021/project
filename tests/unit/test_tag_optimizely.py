"""
Tests for the Optimizely template tags and filters.
"""

import pytest
from django.http import HttpRequest
from django.template import Context
from django.test.utils import override_settings
from utils import TagTestCase

from analytical.templatetags.optimizely import OptimizelyNode
from analytical.utils import AnalyticalException


@override_settings(OPTIMIZELY_ACCOUNT_NUMBER='1234567')
class OptimizelyTagTestCase(TagTestCase):
    """
    Tests for the ``optimizely`` template tag.
    """

    def test_tag(self):
        expected = '<script src="//cdn.optimizely.com/js/1234567.js"></script>'
        assert self.render_tag('optimizely', 'optimizely') == expected

    def test_node(self):
        expected = '<script src="//cdn.optimizely.com/js/1234567.js"></script>'
        assert OptimizelyNode().render(Context()) == expected

    @override_settings(OPTIMIZELY_ACCOUNT_NUMBER=None)
    def test_no_account_number(self):
        with pytest.raises(AnalyticalException):
            OptimizelyNode()

    @override_settings(OPTIMIZELY_ACCOUNT_NUMBER='123abc')
    def test_wrong_account_number(self):
        with pytest.raises(AnalyticalException):
            OptimizelyNode()

    @override_settings(ANALYTICAL_INTERNAL_IPS=['1.1.1.1'])
    def test_render_internal_ip(self):
        req = HttpRequest()
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        context = Context({'request': req})
        r = OptimizelyNode().render(context)
        assert r.startswith('<!-- Optimizely disabled on internal IP address')
        assert r.endswith('-->')
