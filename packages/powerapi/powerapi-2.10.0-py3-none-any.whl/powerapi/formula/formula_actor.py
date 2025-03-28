# Copyright (c) 2022, INRIA
# Copyright (c) 2022, University of Lille
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

import logging
import re

from powerapi.actor import Actor, State
from powerapi.pusher import PusherActor


class FormulaState(State):
    """
    Initialize a new Formula actor state.
    :param actor: Actor linked to the state
    :param pushers: Pushers available for the actor
    :param metadata: Metadata related to the state
    """

    def __init__(self, actor, pushers, metadata):
        super().__init__(actor)
        self.pushers = pushers
        self.metadata = metadata


class FormulaActor(Actor):
    """
    Abstract actor class used to implement formula actor that compute power consumption of a device from Reports
    """

    def __init__(self, name, pushers: dict[str, PusherActor], level_logger=logging.WARNING, timeout=None):
        """
        Initialize a new Formula actor.
        :param name: Actor name
        :param pushers: Pusher actors
        :param level_logger: Level of the logger
        :param timeout: Time in millisecond to wait for a message before calling the timeout handler
        """
        Actor.__init__(self, name, level_logger, timeout)

        self.formula_metadata = self._extract_formula_metadata(name)
        self.state = FormulaState(self, pushers, self.formula_metadata)

    @staticmethod
    def _extract_formula_metadata(formula_name):
        metadata_str = re.findall(r'\'([\w_]*)\'', formula_name)

        metadata = {}

        if len(metadata_str) >= 2:
            metadata['sensor'] = metadata_str[1]

        if len(metadata_str) >= 3:
            metadata['socket'] = int(metadata_str[2])

        if len(metadata_str) >= 4:
            metadata['core'] = int(metadata_str[3])
        return metadata

    def setup(self):
        """
        Setup the Formula actor.
        """
        for _, pusher in self.state.pushers.items():
            pusher.connect_data()
