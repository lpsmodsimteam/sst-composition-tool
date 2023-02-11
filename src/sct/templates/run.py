#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sst

sst.setProgramOption("stopAtCycle", "5s")

{{components | join("\n")}}

{{links | join("\n")}}
