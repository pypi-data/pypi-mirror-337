from unittest.mock import Mock

import bson
from pymongo.uri_parser import parse_uri
from twisted.internet import defer, reactor
from twisted.test import proto_helpers
from twisted.trial import unittest

from txmongo import MongoProtocol, Query
from txmongo.connection import ConnectionPool, _Connection
from txmongo.protocol import Reply


def _delay(time):
    d = defer.Deferred()
    reactor.callLater(time, d.callback, None)
    return d


class AssertCallbackNotCalled:
    """
    Context manager that assures Deferred's callback was not called
    after it was cancelled. So we can be sure that Deferred's canceller
    correctly removed it from waiting lists.
    """

    def __init__(self, deferred):
        self.deferred = deferred

    def __enter__(self):
        self.deferred.callback = Mock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deferred.callback.assert_not_called()


class TestCancelParts(unittest.TestCase):

    def test_protocol_query(self):
        tr = proto_helpers.StringTransport()
        proto = MongoProtocol()
        proto.makeConnection(tr)

        d = proto.send_query(Query(query=bson.encode({"x": 42})))
        d.cancel()

        with AssertCallbackNotCalled(d):
            reply = Reply(response_to=1, documents=[bson.encode({"x": 42})])
            proto.dataReceived(reply.encode(1))

        self.failureResultOf(d, defer.CancelledError)

    def test_protocol_connectionReady(self):
        proto = MongoProtocol()
        d1 = proto.connectionReady()
        d2 = proto.connectionReady()
        d1.cancel()

        with AssertCallbackNotCalled(d1):
            proto.makeConnection(proto_helpers.StringTransport())

        self.assertTrue(d2.called)
        self.failureResultOf(d1, defer.CancelledError)

    @defer.inlineCallbacks
    def test_connection_notifyReady(self):
        uri = parse_uri("mongodb://localhost:27017/")
        pool = Mock()
        pool._logical_session_timeout_minutes = 30
        pool.auth_creds = {}
        conn = _Connection(pool, uri, 0, 10, 10)
        d1 = conn.notifyReady()
        d2 = conn.notifyReady()
        d1.cancel()

        connector = reactor.connectTCP("localhost", 27017, conn)

        with AssertCallbackNotCalled(d1):
            yield d2

        self.failureResultOf(d1, defer.CancelledError)

        conn.stopTrying()
        conn.stopFactory()
        conn.instance.transport.loseConnection()
        connector.disconnect()


class TestCancelIntegrated(unittest.TestCase):

    def setUp(self):
        self.conn = ConnectionPool()
        self.db = self.conn.db
        self.coll = self.db.coll

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.coll.drop()
        yield self.conn.disconnect()

    @defer.inlineCallbacks
    def test_integration(self):
        # Our ConnectionPool is not actually connected yet, so on this
        # stage operations can be safely cancelled -- they won't be
        # sent to MongoDB at all. This test checks this.

        d1 = self.coll.insert_one({"x": 1})
        d2 = self.coll.insert_one({"x": 2})
        d3 = self.coll.insert_one({"x": 3})
        d4 = self.coll.insert_one({"x": 4})

        d1.cancel()
        d3.cancel()

        yield d4

        self.failureResultOf(d1, defer.CancelledError)
        self.assertTrue(d2.called)
        self.failureResultOf(d3, defer.CancelledError)

        docs = yield self.coll.distinct("x")
        self.assertEqual(set(docs), {2, 4})

    @defer.inlineCallbacks
    def test_remove(self):
        # Let's test cancellation of some dangerous operation for the peace
        # of mind. NB: remove can be cancelled only because ConnectionPool
        # is not connected yet.
        for i in range(10):
            self.coll.insert_one({"x": i})

        d1 = self.coll.delete_many({"x": {"$lt": 3}})
        d2 = self.coll.delete_many({"x": {"$gte": 3, "$lt": 6}})
        d3 = self.coll.delete_many({"x": {"$gte": 6, "$lt": 9}})

        d2.cancel()

        yield d3

        self.assertTrue(d1.called)
        self.failureResultOf(d2, defer.CancelledError)

        x = yield self.coll.distinct("x")
        self.assertEqual(set(x), {3, 4, 5, 9})

    @defer.inlineCallbacks
    def test_no_way(self):
        # If ConnectionPool picks already active connection, the query is sent
        # to MongoDB immediately and there is no way to cancel it

        yield self.coll.count_documents({})

        d = self.coll.insert_one({"x": 42})
        d.cancel()

        yield _delay(1)

        self.failureResultOf(d, defer.CancelledError)

        cnt = yield self.coll.count_documents({})
        self.assertEqual(cnt, 1)
