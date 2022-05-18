#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sst

sst.setProgramOption("stopAtCycle", "5s")

fulladder78144 = sst.Component("fulladder78144", "library_name.fulladder")
fulladder78144.addParams({'clock': '1MHz', 'link_speed': '1ps'})
fulladder78192 = sst.Component("fulladder78192", "library_name.fulladder")
fulladder78192.addParams({'clock': '1MHz', 'link_speed': '1ps'})
fulladder78240 = sst.Component("fulladder78240", "library_name.fulladder")
fulladder78240.addParams({'clock': '1MHz', 'link_speed': '1ps'})
fulladder78288 = sst.Component("fulladder78288", "library_name.fulladder")
fulladder78288.addParams({'clock': '1MHz', 'link_speed': '1ps'})
fulladder78432 = sst.Component("fulladder78432", "library_name.fulladder")
fulladder78432.addParams({'clock': '1MHz', 'link_speed': '1ps'})
fulladder78480 = sst.Component("fulladder78480", "library_name.fulladder")
fulladder78480.addParams({'clock': '1MHz', 'link_speed': '1ps'})
fulladder78528 = sst.Component("fulladder78528", "library_name.fulladder")
fulladder78528.addParams({'clock': '1MHz', 'link_speed': '1ps'})
fulladder78576 = sst.Component("fulladder78576", "library_name.fulladder")
fulladder78576.addParams({'clock': '1MHz', 'link_speed': '1ps'})

sst.Link("fulladder78144-cout").connect(
    (fulladder78144, "cout"), (fulladder78432, "cin")
)
sst.Link("fulladder78144-cout").connect(
    (fulladder78144, "cout"), (fulladder78240, "cin")
)
sst.Link("fulladder78144-cout").connect(
    (fulladder78144, "cout"), (fulladder78192, "cin")
)
sst.Link("fulladder78192-cout").connect(
    (fulladder78192, "cout"), (fulladder78480, "cin")
)
sst.Link("fulladder78192-cout").connect(
    (fulladder78192, "cout"), (fulladder78288, "cin")
)
sst.Link("fulladder78240-cout").connect(
    (fulladder78240, "cout"), (fulladder78528, "cin")
)
sst.Link("fulladder78240-cout").connect(
    (fulladder78240, "cout"), (fulladder78288, "cin")
)
sst.Link("fulladder78288-cout").connect(
    (fulladder78288, "cout"), (fulladder78432, "opand2")
)
sst.Link("fulladder78432-cout").connect(
    (fulladder78432, "cout"), (fulladder78528, "cin")
)
sst.Link("fulladder78432-cout").connect(
    (fulladder78432, "cout"), (fulladder78480, "cin")
)
sst.Link("fulladder78480-cout").connect(
    (fulladder78480, "cout"), (fulladder78576, "cin")
)
sst.Link("fulladder78528-cout").connect(
    (fulladder78528, "cout"), (fulladder78576, "cin")
)