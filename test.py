#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
import sys
import bottle
from bottle.ext import redis as redis_plugin
import redis

py = sys.version_info
py3k = py >= (3, 0, 0)


class RedisTest(unittest.TestCase):
    def setUp(self):
        self.app = bottle.Bottle(catchall=False)

    def test_with_keyword(self):
        self.plugin = self.app.install(redis_plugin.Plugin())

        @self.app.get('/')
        def test(rdb):
            self.assertEqual(type(rdb), type(redis.client.Redis()))
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET'}, lambda x, y: None)

    def test_without_keyword(self):
        self.plugin = self.app.install(redis_plugin.Plugin())

        @self.app.get('/')
        def test():
            pass
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET'}, lambda x, y: None)

        @self.app.get('/2')
        def test_kw(**kw):
            self.assertFalse('rdb' in kw)
        self.app({'PATH_INFO':'/2', 'REQUEST_METHOD':'GET'}, lambda x, y: None)
    
    def test_optional_args(self):
        self.plugin = self.app.install(redis_plugin.Plugin(db=1,
                                                           decode_responses=True))

        @self.app.get('/db/1')
        def test_db_arg(rdb):
            self.assertTrue(rdb.connection_pool.connection_kwargs['db'] == 1)
            self.assertTrue(rdb.connection_pool.connection_kwargs['decode_responses'] == True)
            rdb.set('test', 'bottle')
            if py3k:
                self.assertEqual(rdb.get('test'), b'bottle')
            else:
                self.assertEqual(rdb.get('test'), 'bottle')
        self.app({'PATH_INFO':'/db/1', 'REQUEST_METHOD':'GET'},
                 lambda x,y: None)
        

    def test_save(self):
        self.plugin = self.app.install(redis_plugin.Plugin())

        @self.app.get('/')
        def test(rdb):
            rdb.set('test', 'bottle')
            r = redis.Redis()
            if py3k:
                self.assertEqual(rdb.get('test'), b'bottle')
            else:
                self.assertEqual(rdb.get('test'), 'bottle')
            self.assertEqual(rdb.get('test'), r.get('test'))
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET'}, lambda x,y: None)
 

if __name__ == '__main__':
    unittest.main()
