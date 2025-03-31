# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linkml',
 'linkml.cli',
 'linkml.generators',
 'linkml.generators.common',
 'linkml.generators.legacy',
 'linkml.generators.pydanticgen',
 'linkml.generators.python',
 'linkml.generators.shacl',
 'linkml.generators.sqlalchemy',
 'linkml.linter',
 'linkml.linter.config.datamodel',
 'linkml.linter.formatters',
 'linkml.reporting',
 'linkml.transformers',
 'linkml.utils',
 'linkml.validator',
 'linkml.validator.loaders',
 'linkml.validator.plugins',
 'linkml.validators',
 'linkml.workspaces',
 'linkml.workspaces.datamodel']

package_data = \
{'': ['*'],
 'linkml.generators': ['docgen/*', 'javagen/*'],
 'linkml.generators.pydanticgen': ['templates/*'],
 'linkml.linter': ['config/*']}

install_requires = \
['antlr4-python3-runtime>=4.9.0,<4.10',
 'click>=7.0',
 'graphviz>=0.10.1',
 'hbreader',
 'isodate>=0.6.0',
 'jinja2>=3.1.0',
 'jsonasobj2>=1.0.3,<2.0.0',
 'jsonschema[format]>=4.0.0',
 'linkml-dataops',
 'linkml-runtime>=1.8.1,<2.0.0',
 'openpyxl',
 'parse',
 'prefixcommons>=0.1.7',
 'prefixmaps>=0.2.2',
 'pydantic>=1.0.0,<3.0.0',
 'pyjsg>=0.11.6',
 'pyshex>=0.7.20',
 'pyshexc>=0.8.3',
 'python-dateutil',
 'pyyaml',
 'rdflib>=6.0.0',
 'requests>=2.22',
 'sqlalchemy>=1.4.31',
 'watchdog>=0.9.0']

extras_require = \
{':python_version < "3.12"': ['typing-extensions>=4.6.0'],
 'black': ['black>=24.0.0'],
 'numpydantic:python_version >= "3.9"': ['numpydantic>=1.6.1'],
 'shacl': ['pyshacl>=0.25.0,<0.26.0'],
 'tests': ['pyshacl>=0.25.0,<0.26.0', 'black>=24.0.0'],
 'tests:python_version >= "3.9"': ['numpydantic>=1.6.1']}

entry_points = \
{'console_scripts': ['gen-csv = linkml.generators.csvgen:cli',
                     'gen-dbml = linkml.generators.dbmlgen:cli',
                     'gen-doc = linkml.generators.docgen:cli',
                     'gen-erdiagram = linkml.generators.erdiagramgen:cli',
                     'gen-excel = linkml.generators.excelgen:cli',
                     'gen-golang = linkml.generators.golanggen:cli',
                     'gen-golr-views = linkml.generators.golrgen:cli',
                     'gen-graphql = linkml.generators.graphqlgen:cli',
                     'gen-graphviz = linkml.generators.dotgen:cli',
                     'gen-java = linkml.generators.javagen:cli',
                     'gen-json-schema = linkml.generators.jsonschemagen:cli',
                     'gen-jsonld = linkml.generators.jsonldgen:cli',
                     'gen-jsonld-context = '
                     'linkml.generators.jsonldcontextgen:cli',
                     'gen-linkml = linkml.generators.linkmlgen:cli',
                     'gen-markdown = linkml.generators.markdowngen:cli',
                     'gen-mermaid-class-diagram = '
                     'linkml.generators.mermaidclassdiagramgen:cli',
                     'gen-namespaces = linkml.generators.namespacegen:cli',
                     'gen-owl = linkml.generators.owlgen:cli',
                     'gen-plantuml = linkml.generators.plantumlgen:cli',
                     'gen-prefix-map = linkml.generators.prefixmapgen:cli',
                     'gen-project = linkml.generators.projectgen:cli',
                     'gen-proto = linkml.generators.protogen:cli',
                     'gen-py-classes = linkml.generators.pythongen:cli',
                     'gen-pydantic = linkml.generators.pydanticgen:cli',
                     'gen-python = linkml.generators.pythongen:cli',
                     'gen-rdf = linkml.generators.rdfgen:cli',
                     'gen-shacl = linkml.generators.shaclgen:cli',
                     'gen-shex = linkml.generators.shexgen:cli',
                     'gen-sparql = linkml.generators.sparqlgen:cli',
                     'gen-sqla = linkml.generators.sqlalchemygen:cli',
                     'gen-sqlddl = linkml.generators.sqltablegen:cli',
                     'gen-sqltables = linkml.generators.sqltablegen:cli',
                     'gen-sssom = linkml.generators.sssomgen:cli',
                     'gen-summary = linkml.generators.summarygen:cli',
                     'gen-terminusdb = linkml.generators.terminusdbgen:cli',
                     'gen-typescript = linkml.generators.typescriptgen:cli',
                     'gen-yaml = linkml.generators.yamlgen:cli',
                     'gen-yuml = linkml.generators.yumlgen:cli',
                     'linkml = linkml.cli.main:linkml',
                     'linkml-convert = linkml.utils.converter:cli',
                     'linkml-jsonschema-validate = '
                     'linkml.validators.jsonschemavalidator:cli',
                     'linkml-lint = linkml.linter.cli:main',
                     'linkml-run-examples = '
                     'linkml.workspaces.example_runner:cli',
                     'linkml-schema-fixer = linkml.utils.schema_fixer:main',
                     'linkml-sparql-validate = '
                     'linkml.validators.sparqlvalidator:cli',
                     'linkml-sqldb = linkml.utils.sqlutils:main',
                     'linkml-validate = linkml.validator.cli:cli',
                     'run-tutorial = linkml.utils.execute_tutorial:cli']}

setup_kwargs = {
    'name': 'linkml',
    'version': '1.9.0rc1',
    'description': 'Linked Open Data Modeling Language',
    'long_description': '[![Pyversions](https://img.shields.io/pypi/pyversions/linkml.svg)](https://pypi.python.org/pypi/linkml)\n![](https://github.com/linkml/linkml/workflows/Build/badge.svg)\n[![PyPi](https://img.shields.io/pypi/v/linkml.svg)](https://pypi.python.org/pypi/linkml)\n[![badge](https://img.shields.io/badge/launch-binder-579ACA.svg)](https://mybinder.org/v2/gh/linkml/linkml/main?filepath=notebooks)\n[![DOI](https://zenodo.org/badge/13996/linkml/linkml.svg)](https://zenodo.org/badge/latestdoi/13996/linkml/linkml)\n[![PyPIDownloadsTotal](https://pepy.tech/badge/linkml)](https://pepy.tech/project/linkml)\n[![PyPIDownloadsMonth](https://img.shields.io/pypi/dm/linkml?logo=PyPI&color=blue)](https://pypi.org/project/linkml)\n[![codecov](https://codecov.io/gh/linkml/linkml/branch/main/graph/badge.svg?token=WNQNG986UN)](https://codecov.io/gh/linkml/linkml)\n\n\n# LinkML - Linked Data Modeling Language\n\nLinkML is a linked data modeling language following object-oriented and ontological principles. LinkML models are typically authored in YAML, and can be converted to other schema representation formats such as JSON or RDF.\n\nThis repo holds the tools for generating and working with LinkML. For the LinkML schema (metamodel), please see https://github.com/linkml/linkml-model\n\nThe complete documentation for LinkML can be found here:\n\n - [linkml.io/linkml](https://linkml.io/linkml)\n',
    'author': 'Chris Mungall',
    'author_email': 'cjmungall@lbl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://linkml.io/linkml/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
