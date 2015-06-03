# -*- coding: utf-8 -*-
import redis
import inspect
from bottle import __version__, PluginError


class RedisPlugin(object):
    name = 'redis'
    api = 2

    def __init__(self, keyword='rdb', *args, **kwargs):
      self.keyword = keyword
      self.redisdb = None
      self.args = args
      self.kwargs = kwargs

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, RedisPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another redis plugin with "\
                        "conflicting settings (non-unique keyword).")
        if self.redisdb is None:
            self.redisdb = redis.ConnectionPool(*self.args, **self.kwargs)

    def apply(self, callback, route):
        # hack to support bottle v0.9.x
        if __version__.startswith('0.9'):
            config = route['config']
            _callback = route['callback']
        else:
            config = route.config
            _callback = route.callback

        conf = config.get('redis') or {}
        args = inspect.getargspec(_callback)[0]
        keyword = conf.get('keyword', self.keyword)
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            kwargs[self.keyword] = redis.Redis(connection_pool=self.redisdb)
            rv = callback(*args, **kwargs)
            return rv
        return wrapper


Plugin = RedisPlugin
