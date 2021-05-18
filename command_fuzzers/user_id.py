from katnip.model.low_level.radamsa import RadamsaField
from kitty.model.low_level.aliases import *
from kitty.model.low_level.container import *
from kitty.model.low_level.field import *

from command_fuzzers.base_command import BaseCommand
from encoders import *

class SetUserID(BaseCommand):

    def __init__(self, model):
        super(SetUserID, self).__init__(model)

        self._user_id_fuzz = Template(
            name="set_user_id",
            fields=[
                String(value='{"execute_command":{"session":"', fuzzable=False),
                Dynamic(key="session_id", default_value=""),
                String(
                    value='","command":"SET_USER_ID", "params":["user_id"],"values":[',
                    fuzzable=False,
                ),
                OneOf(fields=[
                    String(value='9687498355'),
                    Qword(value=9687498355),
                    RadamsaField(value='9687498355', fuzz_count=5000, bin_path=)
                ]),
                String(value=']}}', fuzzable=False),
            ],
            encoder=WEBSOCKET_BITS,
        )

        self._model.connect(self._init_handshake, self._user_id_fuzz, self.new_session_callback)

