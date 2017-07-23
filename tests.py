from unittest import TestCase

import xmltodict

from markdown import Markdown
from markdown.util import etree

from mdx_variables import VariablesExtension, VariablePattern, makeExtension


class XmlTestCaseMixin(object):
    """ Helper class for asserting that XML documents describe the same XML
        structures.
    """

    def mk_doc(self, s):
        return etree.fromstring(
            "<div>" + s.strip() + "</div>")

    def assert_xml_equal(self, a, b):
        self.assertEqual(
            xmltodict.parse(etree.tostring(a)),
            xmltodict.parse(etree.tostring(b)))

    def assert_xmltext_equal(self, a, b):
        self.assert_xml_equal(self.mk_doc(a), self.mk_doc(b))


class TestVariablesPattern(XmlTestCaseMixin, TestCase):
    """ Test VariablesPattern and handling of variables. """

    def mk_markdown(self, conf):
        md = Markdown()
        ext = VariablesExtension(conf)
        ext.extendMarkdown(md, {})
        return md

    def test_known_variable_function(self):
        def bar():
            return "bar"
        md = self.mk_markdown({'vars': {'foo': bar}})
        xml = md.convert("${foo}")
        self.assert_xmltext_equal(xml, "<p>bar</p>")

    def test_known_variable_string(self):
        md = self.mk_markdown({'vars': {'foo': "zoom"}})
        xml = md.convert("${foo}")
        self.assert_xmltext_equal(xml, "<p>zoom</p>")

    def test_known_variable_integer(self):
        md = self.mk_markdown({'vars': {'foo': 5}})
        xml = md.convert("${foo}")
        self.assert_xmltext_equal(xml, "<p>5</p>")

    def test_bad_variable(self):
        def err():
            raise RuntimeError("should be caught")
        md = self.mk_markdown({'vars': {'foo': err}})
        xml = md.convert("${foo}")
        self.assert_xmltext_equal(xml, "<p>BAD VARIABLE: foo</p>")

    def test_unknown_variable_without_default(self):
        md = self.mk_markdown({'vars': {}})
        xml = md.convert("${foo}")
        self.assert_xmltext_equal(xml, "<p>MISSING VARIABLE: foo</p>")

    def test_unknown_variable_with_default(self):
        def default(varname):
            return "got %s" % (varname,)
        md = self.mk_markdown({'vars': {'__getattr__': default}})
        xml = md.convert("${foo}")
        self.assert_xmltext_equal(xml, "<p>got foo</p>")

    def test_bad_default(self):
        def default_err(varname):
            raise RuntimeError("Should be caught")
        md = self.mk_markdown({'vars': {'__getattr__': default_err}})
        xml = md.convert("${foo}")
        self.assert_xmltext_equal(xml, "<p>BAD VARIABLE: foo</p>")


class TestVariablesExtension(TestCase):
    """ Test VariablesExtension class. """

    def mk_markdown(self):
        md = Markdown()
        md_globals = {}
        return md, md_globals

    def assert_registered(self, md, md_globals):
        pattern = md.inlinePatterns['variable']
        self.assertTrue(isinstance(pattern, VariablePattern))
        self.assertEqual(md_globals, {})

    def assert_not_registered(self, md, md_globals):
        self.assertFalse('variable' in md.inlinePatterns)
        self.assertEqual(md_globals, {})

    def text_create(self):
        ext = VariablesExtension({'a': 'b'})
        self.assertEqual(ext.conf, {'a': 'b'})

    def test_extend_markdown(self):
        md, md_globals = self.mk_markdown()
        ext = VariablesExtension({})
        self.assert_not_registered(md, md_globals)
        ext.extendMarkdown(md, md_globals)
        self.assert_registered(md, md_globals)


class TestExtensionRegistration(TestCase):
    """ Test registration of variables extension. """

    def test_make_extension(self):
        configs = {'a': 'b'}
        ext = makeExtension(configs)
        self.assertTrue(isinstance(ext, VariablesExtension))
        self.assertEqual(ext.conf, configs)
