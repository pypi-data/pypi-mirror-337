# coding: utf-8
# Copyright 2010 Mark L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from contextlib import asynccontextmanager, contextmanager

from pymongo.errors import OperationFailure
from twisted.internet import defer
from twisted.trial import unittest

import txmongo
import txmongo.filter as qf

mongo_host = "localhost"
mongo_port = 27017


class TestMongoFilters(unittest.TestCase):

    @defer.inlineCallbacks
    def setUp(self):
        self.conn = txmongo.MongoConnection(mongo_host, mongo_port)
        self.db = self.conn.mydb
        self.coll = self.db.mycol
        yield self.coll.insert_one({"x": 42})

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.coll.drop()
        yield self.db.system.profile.drop()
        yield self.conn.disconnect()

    @asynccontextmanager
    async def _assert_single_command_with_option(self, optionname, optionvalue):
        # Checking that `optionname` appears in profiler log with specified value

        await self.db.command("profile", 2)
        yield
        await self.db.command("profile", 0)

        profile_filter = {"command." + optionname: optionvalue}
        cnt = await self.db.system.profile.count_documents(profile_filter)
        await self.db.system.profile.drop()
        self.assertEqual(cnt, 1)

    async def test_Hint(self):
        # find() should fail with 'bad hint' if hint specifier works correctly
        self.assertFailure(
            self.coll.find({}, sort=qf.hint([("x", 1)])), OperationFailure
        )
        self.assertFailure(self.coll.find().hint({"x": 1}), OperationFailure)

        # create index and test it is honoured
        await self.coll.create_index(qf.sort(qf.ASCENDING("x")), name="test_index")
        forms = [
            [("x", 1)],
            {"x": 1},
            qf.ASCENDING("x"),
        ]
        for form in forms:
            async with self._assert_single_command_with_option("hint", {"x": 1}):
                await self.coll.find({}, sort=qf.hint(form))
            async with self._assert_single_command_with_option("hint", {"x": 1}):
                await self.coll.find().hint(form)

        async with self._assert_single_command_with_option("hint", "test_index"):
            await self.coll.find({}, sort=qf.hint("test_index"))
        async with self._assert_single_command_with_option("hint", "test_index"):
            await self.coll.find().hint("test_index")

        # find() should fail with 'bad hint' if hint specifier works correctly
        self.assertFailure(
            self.coll.find({}, sort=qf.hint(["test_index", 1])), OperationFailure
        )
        self.assertFailure(
            self.coll.find({}, sort=qf.hint(qf.ASCENDING("test_index"))),
            OperationFailure,
        )

    def test_SortAscendingMultipleFields(self):
        self.assertEqual(
            qf.sort(qf.ASCENDING(["x", "y"])),
            qf.sort(qf.ASCENDING("x") + qf.ASCENDING("y")),
        )
        self.assertEqual(
            qf.sort(qf.ASCENDING(["x", "y"])),
            qf.sort({"x": 1, "y": 1}),
        )

    def test_SortOneLevelList(self):
        self.assertEqual(qf.sort([("x", 1)]), qf.sort(("x", 1)))

    def test_SortInvalidKey(self):
        self.assertRaises(TypeError, qf.sort, [(1, 2)])
        self.assertRaises(TypeError, qf.sort, [("x", 3)])
        self.assertRaises(TypeError, qf.sort, {"x": 3})

    def test_SortGeoIndexes(self):
        self.assertEqual(qf.sort(qf.GEO2D("x")), qf.sort([("x", "2d")]))
        self.assertEqual(qf.sort(qf.GEO2DSPHERE("x")), qf.sort([("x", "2dsphere")]))
        self.assertEqual(qf.sort(qf.GEOHAYSTACK("x")), qf.sort([("x", "geoHaystack")]))

    def test_TextIndex(self):
        self.assertEqual(qf.sort(qf.TEXT("title")), qf.sort([("title", "text")]))

    async def test_SortProfile(self):
        forms = [
            qf.DESCENDING("x"),
            {"x": -1},
            [("x", -1)],
            ("x", -1),
        ]
        for form in forms:
            async with self._assert_single_command_with_option("sort.x", -1):
                await self.coll.find({}, sort=qf.sort(form))
            async with self._assert_single_command_with_option("sort.x", -1):
                await self.coll.find().sort(form)

    async def test_Comment(self):
        comment = "hello world"

        async with self._assert_single_command_with_option("comment", comment):
            await self.coll.find({}, sort=qf.comment(comment))
        async with self._assert_single_command_with_option("comment", comment):
            await self.coll.find().comment(comment)

    @defer.inlineCallbacks
    def test_Explain(self):
        result = yield self.coll.find({}, sort=qf.explain())
        self.assertTrue("executionStats" in result[0] or "nscanned" in result[0])
        result = yield self.coll.find().explain()
        self.assertTrue("executionStats" in result[0] or "nscanned" in result[0])

    @defer.inlineCallbacks
    def test_FilterMerge(self):
        self.assertEqual(
            qf.sort(qf.ASCENDING("x") + qf.DESCENDING("y")),
            qf.sort(qf.ASCENDING("x")) + qf.sort(qf.DESCENDING("y")),
        )

        comment = "hello world"

        yield self.db.command("profile", 2)
        yield self.coll.find({}, sort=qf.sort(qf.ASCENDING("x")) + qf.comment(comment))
        yield self.db.command("profile", 0)

        profile_filter = {"command.sort.x": 1, "command.comment": comment}
        cnt = yield self.db.system.profile.count_documents(profile_filter)
        self.assertEqual(cnt, 1)

    def test_Repr(self):
        self.assertEqual(
            repr(qf.sort(qf.ASCENDING("x"))),
            "<mongodb QueryFilter: {'orderby': (('x', 1),)}>",
        )
