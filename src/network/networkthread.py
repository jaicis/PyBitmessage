"""
A thread to handle network concerns
"""
try:
    import network.asyncore_pollchoose as asyncore
    import state
    from network.connectionpool import BMConnectionPool
    from queues import excQueue
    from network.threads import StoppableThread
except ModuleNotFoundError:
    from pybitmessage.network import asyncore_pollchoose as asyncore
    from pybitmessage import state
    from pybitmessage.network.connectionpool import BMConnectionPool
    from pybitmessage.queues import excQueue
    from pybitmessage.network.threads import StoppableThread

class BMNetworkThread(StoppableThread):
    """Main network thread"""
    name = "Asyncore"

    def run(self):
        try:
            while not self._stopped and state.shutdown == 0:
                BMConnectionPool().loop()
        except Exception as e:
            excQueue.put((self.name, e))
            raise

    def stopThread(self):
        super(BMNetworkThread, self).stopThread()
        for i in [listeningSockets for listeningSockets in BMConnectionPool().listeningSockets.values()]:
            try:
                i.close()
            except:
                pass
        for i in [outboundConnections for outboundConnections in BMConnectionPool().outboundConnections.values()]:
            try:
                i.close()
            except:
                pass
        for i in [inboundConnections for inboundConnections in BMConnectionPool().inboundConnections.values()]:
            try:
                i.close()
            except:
                pass

        # just in case
        asyncore.close_all()
