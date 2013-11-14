#!/usr/bin/env python

import netlink.core as netlink
import netlink.route.link as link
import netlink.route.address as Address

sock = netlink.Socket()
sock.connect(netlink.NETLINK_ROUTE)

cache = link.LinkCache()
cache.refill(sock)
intf = cache['wlan0']

addr_cache = Address.AddressCache()
addr_cache.refill()

for addr in addr_cache:
    if addr.ifindex == intf.ifindex:
        print addr
