#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sst

sst.setProgramOption("stopAtCycle", "5s")
CLOCK = "1Hz"
LINK_DELAY = "1ps"

ripplecarryadder = sst.Component("ripplecarryadder driver", "calculator.ripplecarryadder")
ripplecarryadder.addParams({"clock": CLOCK})

full_add_0 = sst.Component("Full Adder 0", "calculator.fulladder")
full_add_0.addParams({"clock": CLOCK})

full_add_1 = sst.Component("Full Adder 1", "calculator.fulladder")
full_add_1.addParams({"clock": CLOCK})

full_add_2 = sst.Component("Full Adder 2", "calculator.fulladder")
full_add_2.addParams({"clock": CLOCK})

full_add_3 = sst.Component("Full Adder 3", "calculator.fulladder")
full_add_3.addParams({"clock": CLOCK})

sst.Link("add_opand1_0").connect(
    (full_add_0, "opand1", LINK_DELAY), (ripplecarryadder, "add_opand1_0", LINK_DELAY)
)
sst.Link("add_opand2_0").connect(
    (full_add_0, "opand2", LINK_DELAY), (ripplecarryadder, "add_opand2_0", LINK_DELAY)
)
sst.Link("add_cin_0").connect(
    (full_add_0, "cin", LINK_DELAY), (ripplecarryadder, "add_cin_0", LINK_DELAY)
)
sst.Link("add_sum_0").connect(
    (full_add_0, "sum", LINK_DELAY), (ripplecarryadder, "add_sum_0", LINK_DELAY)
)
sst.Link("add_cout_0").connect(
    (full_add_0, "cout", LINK_DELAY), (ripplecarryadder, "add_cout_0", LINK_DELAY)
)

sst.Link("add_opand1_1").connect(
    (full_add_1, "opand1", LINK_DELAY), (ripplecarryadder, "add_opand1_1", LINK_DELAY)
)
sst.Link("add_opand2_1").connect(
    (full_add_1, "opand2", LINK_DELAY), (ripplecarryadder, "add_opand2_1", LINK_DELAY)
)
sst.Link("add_cin_1").connect(
    (full_add_1, "cin", LINK_DELAY), (ripplecarryadder, "add_cin_1", LINK_DELAY)
)
sst.Link("add_sum_1").connect(
    (full_add_1, "sum", LINK_DELAY), (ripplecarryadder, "add_sum_1", LINK_DELAY)
)
sst.Link("add_cout_1").connect(
    (full_add_1, "cout", LINK_DELAY), (ripplecarryadder, "add_cout_1", LINK_DELAY)
)

sst.Link("add_opand1_2").connect(
    (full_add_2, "opand1", LINK_DELAY), (ripplecarryadder, "add_opand1_2", LINK_DELAY)
)
sst.Link("add_opand2_2").connect(
    (full_add_2, "opand2", LINK_DELAY), (ripplecarryadder, "add_opand2_2", LINK_DELAY)
)
sst.Link("add_cin_2").connect(
    (full_add_2, "cin", LINK_DELAY), (ripplecarryadder, "add_cin_2", LINK_DELAY)
)
sst.Link("add_sum_2").connect(
    (full_add_2, "sum", LINK_DELAY), (ripplecarryadder, "add_sum_2", LINK_DELAY)
)
sst.Link("add_cout_2").connect(
    (full_add_2, "cout", LINK_DELAY), (ripplecarryadder, "add_cout_2", LINK_DELAY)
)

sst.Link("add_opand1_3").connect(
    (full_add_3, "opand1", LINK_DELAY), (ripplecarryadder, "add_opand1_3", LINK_DELAY)
)
sst.Link("add_opand2_3").connect(
    (full_add_3, "opand2", LINK_DELAY), (ripplecarryadder, "add_opand2_3", LINK_DELAY)
)
sst.Link("add_cin_3").connect(
    (full_add_3, "cin", LINK_DELAY), (ripplecarryadder, "add_cin_3", LINK_DELAY)
)
sst.Link("add_sum_3").connect(
    (full_add_3, "sum", LINK_DELAY), (ripplecarryadder, "add_sum_3", LINK_DELAY)
)
sst.Link("add_cout_3").connect(
    (full_add_3, "cout", LINK_DELAY), (ripplecarryadder, "add_cout_3", LINK_DELAY)
)
