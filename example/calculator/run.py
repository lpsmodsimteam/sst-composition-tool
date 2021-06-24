#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sst

sst.setProgramOption("stopAtCycle", "10s")
CLOCK = "1Hz"
LINK_DELAY = "1ps"

calculator = sst.Component("Calculator driver", "calculator.calculator")
calculator.addParams({"clock": CLOCK})

add1 = sst.Component("Adder", "calculator.add")
add1.addParams({"clock": CLOCK})

sst.Link("add_opand1").connect(
    (add1, "add_opand1", LINK_DELAY), (calculator, "add_opand1", LINK_DELAY)
)
sst.Link("add_opand2").connect(
    (add1, "add_opand2", LINK_DELAY), (calculator, "add_opand2", LINK_DELAY)
)
sst.Link("sum_dout").connect((add1, "sum_dout", LINK_DELAY), (calculator, "sum_dout", LINK_DELAY))

sst.Link("add_of_dout").connect(
    (add1, "add_of_dout", LINK_DELAY), (calculator, "add_of_dout", LINK_DELAY)
)
