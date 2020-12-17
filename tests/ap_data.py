# testdata format
# name, edges, facility_dict_in, facility_dict_out, exp_paths
testdata = [
    ("linear",
     [("Source", "Facility"), ("Facility", "Sink")],
     {"Source": [], "Facility": ["commodity"],
      "Sink": ["changedcommodity"]},
     {"Source": ["commodity"],
      "Facility": ["changedcommodity"], "Sink": []},
     {("Source", "Facility", "Sink")}
     ),
    ("multigraph",
     [("Source", "Sink"), ("Source", "Sink")],
     {"Source": [], "Sink": ["commodityA", "commodityB"]},
     {"Source": ["commodityA", "commodityB"], "Sink": []},
     {("Source", "Sink"), ("Source", "Sink")}
     ),
    ("multisourcesink",
     [("Source", "Facility"), ("Source1", "Facility"), ("Facility", "Sink"),
      ("Facility", "Sink1")],
     {"Source": [], "Source1": [], "Facility": ["commodityA", "commodityB"],
      "Sink": ["changedcommodity"], "Sink1": ["changedcommodity"]},
     {"Source": ["commodityA"], "Source1": ["commodityB"],
      "Facility": ["changedcommodity"], "Sink": [], "Sink1": []},
     {("Source", "Facility", "Sink"), ("Source", "Facility", "Sink1"),
      ("Source1", "Facility", "Sink"), ("Source1", "Facility", "Sink1")}
     ),
    ("bypass",
     [("Source", "Facility"), ("Source", "Sink"), ("Facility", "Sink")],
     {"Source": [], "Facility": ["commodity"],
      "Sink": ["commodity", "changedcommodity"]},
     {"Source": ["commodity"], "Facility": ["changedcommodity"], "Sink": []},
     {("Source", "Sink"), ("Source", "Facility", "Sink")}
     ),
    ("independent",
     [("Source", "Sink"), ("Source1", "Sink1")],
     {"Source": [], "Source1": [], "Sink": ["commodityA"],
      "Sink1": ["commodityB"]},
     {"Source": ["commodityA"], "Source1": ["commodityB"], "Sink": [],
      "Sink1": []},
     {("Source", "Sink"), ("Source1", "Sink1")}
     ),
    ("cycle",
     [("Source", "Facility"), ("Facility", "Recycle"), ("Recycle", "Facility"),
      ("Recycle", "Sink")],
     {"Source": [], "Facility": ["commodity", "recycledcommodity"],
      "Recycle": ["usedcommodity"], "Sink": ["waste"]},
     {"Source": ["commodity"], "Facility": ["usedcommodity"],
      "Recycle": ["recycledcommodity", "waste"], "Sink": []},
     {("Source", "Facility", "Recycle", "Sink")}
     ),
    ("selfcycle",
     [("Source", "Facility"), ("Facility", "Facility"), ("Facility", "Sink")],
     {"Source": [], "Facility": ["commodity", "changedcommodity"],
      "Sink": ["changedcommodity"]},
     {"Source": ["commodity"], "Facility": ["changedcommodity"], "Sink": []},
     {("Source", "Facility", "Sink")}
     )
]
