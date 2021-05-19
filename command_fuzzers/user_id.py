from katnip.model.low_level.radamsa import RadamsaField
from kitty.model.low_level.aliases import *
from kitty.model.low_level.container import *
from kitty.model.low_level.field import *
from katnip.legos.json import *

from command_fuzzers.base_command import BaseCommand
from encoders import *

import os

class SetUserID(BaseCommand):

    def __init__(self, model):
        super(SetUserID, self).__init__(model)

        self._target_template = None
        

    def case_1(self):
        self._target_template = Template(
            name="set_user_id",
            fields=[
                String(value='{"execute_command":{"session":"', fuzzable=False),
                Dynamic(key="session_id", default_value=""),
                String(
                    value='","command":"SET_USER_ID", "params":["user_id"],"values":[',
                    fuzzable=False,
                ),
                RadamsaField(value=b'"9687498355"', fuzz_count=5000, bin_path=self._radamsa_path),
                String(value="]}}", fuzzable=False),
            ],
            encoder=WEBSOCKET_BITS,
        )

    def case_2(self):
        self._target_template = Template(
            name="user_id_from_json",
            encoder=WEBSOCKET_BITS,
            fields=[
                str_to_json('{"execute_command":{"session":"')
            ]
        )
    def finalize(self):
        self._model.connect(self._ping, self._target_template)

