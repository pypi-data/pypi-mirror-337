# Copyright (c) 2021, INRIA
# Copyright (c) 2021, University of Lille
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
import logging
import os
from datetime import datetime

from powerapi.database.base_db import BaseDB, DBError, IterDB
from powerapi.report import Report


class FileBadDBError(DBError):
    """
    Error raised when hostname/port fail
    """

    def __init__(self, filename):
        DBError.__init__(self, "File error : " + filename + " not found")


class FileIterDB(IterDB):
    """
    FileIterDB class

    Class for iterating in a file
    """

    def __init__(self, db, report_type, stream_mode, filename):
        """ """
        IterDB.__init__(self, db, report_type, stream_mode)
        self.previousJson = ""
        self.__iter__()
        self.filename = filename

    def __iter__(self):
        """
        Create the iterator for get the data
        """
        return self

    def __next__(self) -> Report:
        """
        Allow to get the next data
        :raise: StopIteration in stream mode when no report was found.
        """

        with open(self.filename, encoding='utf-8') as file_object:
            json_str = file_object.read()

            if json_str is None:
                raise StopIteration()

            if json_str == self.previousJson:
                logging.error("Error : Report did not change since last read")
                raise StopIteration()

            self.previousJson = json_str

            return self.report_type.from_json(json.loads(json_str))


class FileDB(BaseDB):
    """
    FileDB class herited from BaseDB

    Allow to handle a FileDB database in reading or writing.
    """

    def __init__(self, report_type: type[Report], filename: str):
        """
        :param report_type:        Type of the report handled by this database
        :param filename:        Name of the file containing the report
        """

        BaseDB.__init__(self, report_type)

        self.filename = filename

    def connect(self):
        """
        Override from BaseDB.

        It check that the file exist
        """
        if not os.path.exists(self.filename):
            raise FileBadDBError(self.filename)

    def disconnect(self):
        """
        Disconnect from the file database.
        """

    def iter(self, stream_mode: bool = False) -> FileIterDB:
        """
        Create the iterator for get the data
        """
        return FileIterDB(self, self.report_type, stream_mode, self.filename)

    def save(self, report: Report):
        """
        Override from BaseDB

        :param report: Report to save
        """

        line = {
            "sensor": report.sensor,
            "target": report.target,
            "timestamp": int(datetime.timestamp(report.timestamp) * 1000),
            "power": report.power,
        }

        final_dict = {"PowerReport": [line]}

        with open(self.filename, 'w', encoding='utf-8') as file_object:
            file_object.write(str(final_dict))

    def save_many(self, reports: list[Report]):
        """
        Allow to save a batch of data

        :param reports: Batch of data.
        """
        for report in reports:
            self.save(report)
