""" Variables extension for Python Markdown.
"""

from markdown import Extension
from markdown.inlinepatterns import Pattern


class VariablePattern(Pattern):
    """ Handle matches to the variable pattern (i.e. ${...}). """

    VARIABLE_PATTERN = r'\$\{(\w+)\}'
    CONF_DEFAULTS = {
        'vars': None,
    }

    def __init__(self, conf):
        super(VariablePattern, self).__init__(self.VARIABLE_PATTERN)
        conf_vars = self.CONF_DEFAULTS.copy()
        conf_vars.update(conf or {})
        self.getters = conf_vars['vars'] or {}
        self.missing_getter = self.getters.pop(
            '__getattr__', self._default_missing)

    def _default_missing(self, var_name):
        return "MISSING VARIABLE: %s" % (var_name,)

    def _default_error(self, var_name):
        return "BAD VARIABLE: %s" % (var_name,)

    def _catch_error(self, var_name, f, *args):
        try:
            return f(*args)
        except Exception:
            pass
        return self._default_error(var_name)

    def _get_value(self, var_name):
        if var_name not in self.getters:
            return self._catch_error(var_name, self.missing_getter, var_name)
        value = self.getters[var_name]
        if callable(value):
            value = self._catch_error(var_name, value)
        return self._catch_error(var_name, str, value)

    def handleMatch(self, m):
        var_name = m.group(2)
        return self._get_value(var_name)


class VariablesExtension(Extension):
    """ The variables markdown extension. """

    def __init__(self, configs):
        self.conf = configs

    def extendMarkdown(self, md, md_globals):
        """ Initializes markdown extension components. """
        md.inlinePatterns.register(
            VariablePattern(self.conf), 'variable',
            75)  # add after the not_strong pattern


def makeExtension(**kwargs):
    """ Initialize the variables extension. """
    return VariablesExtension(configs=kwargs)
