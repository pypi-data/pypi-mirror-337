# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['binary_cookies_parser']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=2.8.2,<3.0.0', 'pytest>=8.2.2,<9.0.0', 'typer>=0.12.3,<0.16.0']

entry_points = \
{'console_scripts': ['bcparser = binary_cookies_parser.__main__:main']}

setup_kwargs = {
    'name': 'binary-cookies-parser',
    'version': '1.0.0',
    'description': 'Parses binary cookies from a given .binarycookies file',
    'long_description': '[![Github Actions Status](https://github.com/dan1elt0m/binary-cookies-reader/workflows/test/badge.svg)](https://github.com/dan1elt0m/binary-cookies-reader/actions/workflows/test.yml)\n\n# Binary Cookies Reader\n\nThis project provides a CLI tool to read and interpret binary cookie files.\nThe project is based on the cookie reader written by Satishb3 \n\n## Requirements\n\n- Python 3.8 or higher\n\n## Installation\n```bash \npip install binary-cookies-parser\n```\nIf you want to use the parser as CLI, it\'s recommended to use pipx to install the package in an isolated environment.\n\n## Usage\nAfter installation, you can use the command-line interface to read a binary cookies file:\n\n```bash\nbcparser <path_to_binary_cookies_file>\n```\nReplace <path_to_binary_cookies_file> with the path to the binary cookie file you want to read.\n\nOr use it in Python:\n\n```python\nfrom binary_cookies_parser.parser import read_binary_cookies_file\n\ncookies = read_binary_cookies_file("path/to/cookies.binarycookies")\n```\n\n## Output Types\n\nThe `bcparser` CLI supports two output types: `json` (default) and `ascii`.\n\n### JSON Output\n\nThe `json` output type formats the cookies as a JSON array, making it easy to parse and manipulate programmatically.\n\nExample usage:\n```sh\nbcparser path/to/cookies.binarycookies --output json\n```\n\nexample output:\n```json\n[\n  {\n    "name": "session_id",\n    "value": "abc123",\n    "url": "https://example.com",\n    "path": "/",\n    "create_datetime": "2023-10-01T12:34:56+00:00",\n    "expiry_datetime": "2023-12-31T23:59:59+00:00",\n    "flag": "Secure"\n  },\n  {\n    "name": "user_token",\n    "value": "xyz789",\n    "url": "https://example.com",\n    "path": "/account",\n    "create_datetime": "2023-10-01T12:34:56+00:00",\n    "expiry_datetime": "2023-12-31T23:59:59+00:00",\n    "flag": "HttpOnly"\n  }\n]\n```\n\n### ASCII Output\nThe ascii output type formats the cookies in a simple, line-by-line text format, making it easy to read and pipe to other command-line tools.\n\nExample usage:\n```sh\nbcparser path/to/cookies.binarycookies --output ascii\n```\nExample output:\n```text\nName: session_id\nValue: abc123\nURL: https://example.com\nPath: /\nCreated: 2023-10-01T12:34:56+00:00\nExpires: 2023-12-31T23:59:59+00:00\nFlag: Secure\n----------------------------------------\nName: user_token\nValue: xyz789\nURL: https://example.com\nPath: /account\nCreated: 2023-10-01T12:34:56+00:00\nExpires: 2023-12-31T23:59:59+00:00\nFlag: HttpOnly\n----------------------------------------\n```\n',
    'author': 'Daniel Tom',
    'author_email': 'daniel.tom@xebia.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
