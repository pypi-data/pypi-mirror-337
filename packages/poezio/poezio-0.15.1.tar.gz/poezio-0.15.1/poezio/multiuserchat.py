# Copyright 2010-2011 Florent Le Coz <louiz@louiz.org>
#
# This file is part of Poezio.
#
# Poezio is free software: you can redistribute it and/or modify
# it under the terms of the GPL-3.0+ license. See the COPYING file.
"""
Implementation of the XEP-0045: Multi-User Chat.
Add some facilities that are not available on the XEP_0045
slix plugin
"""

from __future__ import annotations

import asyncio
from typing import (
    Optional,
    Union,
    TYPE_CHECKING,
)

from slixmpp import (
    JID,
    ClientXMPP,
    Presence,
)
from slixmpp.exceptions import IqError, IqTimeout

import logging
log = logging.getLogger(__name__)


if TYPE_CHECKING:
    from poezio.core.core import Core
    from poezio.tabs import MucTab


def change_show(
    xmpp: ClientXMPP,
    jid: JID,
    own_nick: str,
    show: str,
    status: Optional[str]
) -> None:
    """
    Change our 'Show'
    """
    jid = JID(jid)
    pres: Presence = xmpp.make_presence(pto='%s/%s' % (jid, own_nick))
    if show:  # if show is None, don't put a <show /> tag. It means "available"
        pres['type'] = show
    if status:
        pres['status'] = status
    pres.send()


def change_nick(
    core: Core,
    jid: Union[JID, str],
    nick: str,
    status: Optional[str] = None,
    show: Optional[str] = None
) -> None:
    """
    Change our own nick in a room
    """
    xmpp = core.xmpp
    pargs = {'pshow': show, 'pstatus': status}
    asyncio.create_task(xmpp.plugin['xep_0045'].set_self_nick(
        jid,
        nick,
        presence_options=pargs
    ))
    core.events.trigger('changing_nick', jid, nick)


def join_groupchat(
    core: Core,
    jid: JID,
    nick: str,
    passwd: str = '',
    status: Optional[str] = None,
    show: Optional[str] = None,
    seconds: Optional[int] = None,
    tab: Optional['MucTab'] = None
) -> None:
    xmpp = core.xmpp

    async def disco_and_join() -> None:
        has_mam = False
        try:
            iq = await xmpp.plugin['xep_0030'].get_info(jid=jid)
            has_mam = 'urn:xmpp:mam:2' in iq['disco_info'].get_features()
        except (IqError, IqTimeout):
            pass
        if has_mam or (tab and tab._text_buffer.last_message):
            secs = 0
        else:
            secs = seconds
        core.events.trigger('joining_muc', jid)
        pargs = {}
        if status:
            pargs['pstatus'] = status
        if show:
            pargs['pshow'] = show
        await xmpp.plugin['xep_0045'].join_muc_wait(
            room=jid,
            nick=nick,
            seconds=secs,
            password=passwd,
            presence_options=pargs
        )

    asyncio.create_task(disco_and_join())


def leave_groupchat(
    xmpp: ClientXMPP,
    jid: JID,
    own_nick: str,
    msg: str
) -> None:
    """
    Leave the groupchat
    """
    jid = JID(jid)
    try:
        xmpp.plugin['xep_0045'].leave_muc(jid, own_nick, msg)
    except KeyError:
        log.debug(
            "muc.leave_groupchat: could not leave the room %s",
            jid,
            exc_info=True)
