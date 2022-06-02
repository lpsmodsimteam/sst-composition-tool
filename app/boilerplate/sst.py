COMPONENT_INIT = """{name} = sst.Component("{name}", "{library}.{class_name}")"""
COMPONENT_PARAM = "{name}.addParams({params})"
COMPONENT_LINK = """sst.Link("{comp_out}-{link_out}").connect(
    ({comp_out}, "{link_out}"), ({comp_in}, "{link_in}")
)"""
