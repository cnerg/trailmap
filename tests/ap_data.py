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
     [("SourceA", "Facility"), ("SourceB", "Facility"), ("Facility", "SinkA"),
      ("Facility", "SinkB")],
     {"SourceA": [], "SourceB": [], "Facility": ["commodityA", "commodityB"],
      "SinkA": ["changedcommodity"], "SinkB": ["changedcommodity"]},
     {"SourceA": ["commodityA"], "SourceB": ["commodityB"],
      "Facility": ["changedcommodity"], "SinkA": [], "SinkB": []},
     {("SourceA", "Facility", "SinkA"), ("SourceA", "Facility", "SinkB"),
      ("SourceB", "Facility", "SinkA"), ("SourceB", "Facility", "SinkB")}
     ),
    ("bypass",
     [("Source", "Facility"), ("Source", "Sink"), ("Facility", "Sink")],
     {"Source": [], "Facility": ["commodity"],
      "Sink": ["commodity", "changedcommodity"]},
     {"Source": ["commodity"], "Facility": ["changedcommodity"], "Sink": []},
     {("Source", "Sink"), ("Source", "Facility", "Sink")}
     ),
    ("independent",
     [("SourceA", "SinkA"), ("SourceB", "SinkB")],
     {"SourceA": [], "SourceB": [], "SinkA": ["commodityA"],
      "SinkB": ["commodityB"]},
     {"SourceA": ["commodityA"], "SourceB": ["commodityB"], "SinkA": [],
      "SinkB": []},
     {("SourceA", "SinkA"), ("SourceB", "SinkB")}
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
