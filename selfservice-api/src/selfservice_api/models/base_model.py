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
"""This manages Base Model functions."""

from .db import db


class BaseModel():
    """This class manages all of the base model functions."""

    @staticmethod
    def commit():
        """Commit the session."""
        db.session.commit()

    def save(self):
        """Save and commit."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Delete and commit."""
        db.session.delete(self)
        db.session.commit()

    def update_from_dict(self, columns: list, values: dict):
        """Update this model from a given dictionary.

        :params : columns, list of column name to update
        :values : dictionary contains key/value for the columns
        """
        for key in columns:
            exists = key in values
            if exists:
                val = getattr(self, key, '~skip~it~')
                if val != '~skip~it~':
                    setattr(self, key, values[key])
