"""
This plugin allows sending message retractions in a room as a moderator.
It requires XEP-0425 to be available on the room.

Command
-------

.. glossary::

    /moderate
        **Usage in a MUC tab:** ``/moderate <message time> [reason]``
"""

from typing import Optional, Union

from slixmpp.exceptions import IqError, IqTimeout
from poezio.decorators import command_args_parser
from poezio.plugin import BasePlugin
from poezio.core.structs import Completion
from poezio.ui.types import Message
from poezio.tabs import MucTab


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


class Plugin(BasePlugin):
    """Message Moderation (XEP-0425) plugin"""

    def init(self):
        self.core.xmpp.register_plugin('xep_0425')

        self.api.add_tab_command(
            MucTab,
            name='moderate',
            handler=self.command_moderate,
            usage='<message time> [reason]',
            help='Moderate a message using its timestamp (using tab complete)',
            short='Moderate a message using its timestamp',
            completion=self.completion_moderate,
        )

    def find_message(self, time: str) -> Optional[Message]:
        """Find a message back from a timestamp"""
        messages = self.api.get_conversation_messages()[:-100:-1]
        if not messages:
            return None
        for message in messages:
            if isinstance(message, Message) and \
               message.time.strftime(DATETIME_FORMAT) == time:
                return message
        return None

    def completion_moderate(self, the_input) -> Union[bool, Completion]:
        """Datetime completion"""
        if the_input.get_argument_position() != 1:
            return False

        all_messages = self.api.get_conversation_messages()[:-100:-1]
        filtered_messages = filter(
            lambda m: isinstance(m, Message) and m.nickname and m.stanza_id,
            all_messages,
        )
        messages = list(map(lambda m: m.time.strftime(DATETIME_FORMAT), filtered_messages))

        if not messages:
            return False

        return Completion(the_input.auto_completion, messages, '')

    @command_args_parser.quoted(1, 1)
    async def command_moderate(self, args) -> None:
        """Moderate a message in a chatroom"""
        if not args:
            return
        time, *reason = args
        reason = ' '.join(reason)

        found_msg = self.find_message(time)
        if not found_msg:
            self.api.information(
                f'Moderated message with timestamp “{time}” not found.',
                'Error',
            )
            return

        id_ = found_msg.stanza_id
        if id_ is None:
            self.api.information(
                f'Moderated message with timestamp “{time}” '
                'found but contained no “{urn:xmpp:sid:0}stanza-id” identifier.',
                'Error',
            )
            return

        # For logging
        nickname = found_msg.nickname
        namespace = self.core.xmpp['xep_0425'].namespace

        tab = self.api.current_tab()
        jid = tab.jid
        try:
            await self.core.xmpp['xep_0425'].moderate(jid, id_, reason)
        except IqError as exn:
            if exn.iq['error']['text']:
                text = f"\n{exn.iq['error']['text']}"
            else:
                text = ''

            if exn.iq['error']['condition'] == 'service-unavailable':
                self.api.information(
                    f'Room “{jid}” doesn\'t support “{namespace}”.{text}',
                    'Error',
                )
            elif exn.iq['error']['condition'] == 'item-not-found':
                self.api.information(
                    f'Room “{jid}”: Message to moderate not found.{text}',
                    'Error',
                )
            elif exn.iq['error']['condition'] == 'forbidden':
                self.api.information(
                    f'Room “{jid}”: Message moderation forbidden.{text}',
                    'Error',
                )

            return
        except IqTimeout:
            self.api.information(f'Received no reply querying “{jid}”…', 'Error')
            return

        self.api.information(
            f'Room “{jid}”: message from: “{nickname}” at “{time}” successfully retracted.',
            'Info',
        )
