import sst

sst.setProgramOption("stopAtCycle", "5s")

{{components | join("\n")}}

{{links | join("\n")}}
