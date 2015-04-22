'''
This middleware extends the Items with two fields and stores the original URL of the request there. If the DEVEL flag is set then it also stores the body of the response.

Alternative to this middleware is either enforcing of these two fields in every items.py for every spider created, filling them manually in each spider and a custom item pipeline that throws out the body HTML if DEVEL is set.

Slightly better alternative is to subclass all items definition from FlexibleItem:

class FlexibleItem(scrapy.Item):
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super(FlexibleItem, self).__setitem__(key, value)

but that will still need filling of body HTML manually in each spider.
'''

from scrapy.http import Request
from scrapy.conf import settings
from scrapy import log, Field


class ItemsExtenderMiddleware(object):

    @staticmethod
    def extend_class(item):
        cls = item.__class__
        ext_name = "_Ext_" + cls.__name__
        new_fields = {
            '_original_html' : Field(),
            '_original_url' : Field()
            }
        ext_cls = type(ext_name, (cls,), new_fields)
        ei = ext_cls()
        ei.update(item)
        return ei

    def process_spider_output(self, response, result, spider):
        devel = settings.getbool('DEVEL','False')
        for x in result:
            if isinstance(x, Request):
                yield x
            else: # x is instance of Item
                x = self.extend_class(x)
                if not devel:
                    x['_original_html'] = None
                else:
                    x['_original_html'] = response.body
                x['_original_url'] = response.url
                yield x