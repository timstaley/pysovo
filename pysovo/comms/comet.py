# largely transplanted from comet-sendvo script:
# https://github.com/jdswinbank/Comet/blob/release-1.0/scripts/comet-sendvo
# Should track updates.

from __future__ import absolute_import
import logging

# Twisted
from twisted.python import usage
from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString

# VOEvent transport protocol
from comet.tcp.protocol import VOEventSenderFactory

# Encapsulation of event
from comet.log import log
from comet.utility.xml import xml_document
import lxml.etree as ElementTree

import voeparse

logger = logging.getLogger(__name__)


class OneShotSender(VOEventSenderFactory):
    """
    A factory that shuts down the reactor when we lose the connection to the
    remote host. That either means that our event has been sent or that we
    failed.
    """
    def clientConnectionLost(self, connector, reason):
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        logger.warning("Connection failed")
        reactor.stop()


def send_voevent(voevent, host='localhost', port=8098):
    voevent = xml_document(voeparse.dumps(voevent))

    try:
        factory = OneShotSender(voevent)
    except IOError:
        logger.warning("Reading XML document failed")
        reactor.callWhenRunning(reactor.stop)
    except ElementTree.Error:
        logger.warning("Could not parse event text")
        reactor.callWhenRunning(reactor.stop)
    else:
        reactor.connectTCP(host, port, factory)

    reactor.run()

    # If our factory didn't get an acknowledgement of receipt, we'll raise:
    if locals().has_key("factory") and factory.ack:
        return
    else:
        raise RuntimeError("send voevent failed")
