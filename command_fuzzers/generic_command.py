from katnip.model.low_level.radamsa import RadamsaField
from kitty.model.low_level.aliases import *
from kitty.model.low_level.container import *
from kitty.model.low_level.field import *
from katnip.legos.json import *
from kitty.model import ENC_BITS_DEFAULT

from command_fuzzers.base_command import BaseCommand
from encoders import *

import os

class GenericCommand(BaseCommand):

    def __init__(self, model):
        super(GenericCommand, self).__init__(model)

        self._target_template = None
        

    def case_1(self):
        self._target_template = Template(
            name="generic_command",
            fields=[
                String(value='{"execute_command":{"session":"', fuzzable=False),
                Dynamic(key="session_id", default_value="AAAA"),
                String(
                    value='","command":"',
                    fuzzable=False,
                ),
                OneOf(fields=[
                    String(value="SET_USER_ID", encoder=ENC_BITS_DEFAULT),
                ], encoder=ENC_BITS_DEFAULT),
                # SET_USER_ID", "params":["user_id"],"values":['
                # RadamsaField(value=b'9687498355', fuzz_count=5000, bin_path=self._radamsa_path),
                String(value="]}}", fuzzable=False),
            ],
            encoder=WEBSOCKET_BITS,
        )

    def finalize(self):
        self._model.connect(self._ping, self._target_template)
        #self._model.connect(self._init_websocket, self._target_template)

