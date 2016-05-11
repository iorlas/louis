# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

try:
    from lxml import etree

    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree

        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree

            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree

                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree

                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")

from .base import Backend as BaseBackend


class Backend(BaseBackend):
    @classmethod
    def parse(cls, raw_data):
        return cls(etree.fromstring(raw_data))

    def get(self, query, many=False):
        if self.data is None:
            raise LookupError("Cannot look up for '{}' since current data is None".format(query))
        found = self.data.xpath(query)

        # to return one node
        if many:
            return [Backend(f) for f in found]
        return Backend(found[0] if found else None)
