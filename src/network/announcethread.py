"""
Announce myself (node address)
"""
import time

try:
    import state
    from bmconfigparser import BMConfigParser
    from network.assemble import assemble_addr
    from network.connectionpool import BMConnectionPool
    from network.udp import UDPSocket
    from network.node import Peer
    from network.threads import StoppableThread

except ModuleNotFoundError:
    from .. import state
    from ..bmconfigparser import BMConfigParser
    from .assemble import assemble_addr
    from .connectionpool import BMConnectionPool
    from .udp import UDPSocket
    from .node import Peer
    from .threads import StoppableThread


class AnnounceThread(StoppableThread):
    """A thread to manage regular announcing of this node"""
    name = "Announcer"

    def run(self):
        lastSelfAnnounced = 0
        while not self._stopped and state.shutdown == 0:
            processed = 0
            if lastSelfAnnounced < time.time() - UDPSocket.announceInterval:
                self.announceSelf()
                lastSelfAnnounced = time.time()
            if processed == 0:
                self.stop.wait(10)

    @staticmethod
    def announceSelf():
        """Announce our presence"""
        for connection in [udpSockets for udpSockets in BMConnectionPool().udpSockets.values()]:
            if not connection.announcing:
                continue
            for stream in state.streamsInWhichIAmParticipating:
                addr = (
                    stream,
                    #     state.Peer('127.0.0.1',int( BMConfigParser().safeGet("bitmessagesettings", "port"))),
                    #     int(time.time()))
                    # connection.append_write_buf(BMProto.assembleAddr([addr]))
                    Peer(
                        '127.0.0.1',
                        BMConfigParser().safeGetInt(
                            'bitmessagesettings', 'port')),
                    time.time())
                connection.append_write_buf(assemble_addr([addr]))
