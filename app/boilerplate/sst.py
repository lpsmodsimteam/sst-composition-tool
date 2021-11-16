#!/usr/bin/env python
# -*- coding: utf-8 -*-


COMPONENT_INIT_TEMPL = """{name} = sst.Component("{name}", "{library}.{class_name}")"""
COMPONENT_PARAM_TEMPL = "{name}.addParams({params})"
COMPONENT_LINK_TEMPL = """sst.Link("{comp1}-{link1}").connect(
    ({comp1}, "{link1}", LINK_DELAY), ({comp2}, "{link2}", LINK_DELAY)
)"""
