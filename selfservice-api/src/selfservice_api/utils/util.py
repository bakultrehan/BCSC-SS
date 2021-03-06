# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Common utils.

* CORS pre-flight decorator. A simple decorator to add the options method to a Request Class.
* Verify jwks uri
"""

import json

from six.moves.urllib.request import urlopen


def cors_preflight(methods: str = 'GET'):
    """Render an option method on the class."""
    def wrapper(f):  # pylint: disable=invalid-name
        def options(self, *args, **kwargs):  # pylint: disable=unused-argument
            return {'Allow': 'GET'}, 200, \
                   {'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': methods,
                    'Access-Control-Allow-Headers': 'Authorization, Content-Type'}

        setattr(f, 'options', options)
        return f
    return wrapper


def verify_jwks_uri(jwks_uri: str):  # pragma: no cover
    """Make sure the `jwks_uri` exist and in a valid format."""
    try:
        jsonurl = urlopen(jwks_uri)
        jwks = json.loads(jsonurl.read().decode('utf-8'))

        for key in jwks['keys']:
            if 'kty' in key and 'kid' in key and 'use' in key and 'n' in key and 'e' in key:
                return True
    finally:
        pass

    return False
