# testdata format
# name, short, long, semiconnect, hierarchy, edges, paths
testdata = [
    ("linear", 3, 3, True, 1.0,
     [("Source", "Facility"), ("Facility", "Sink")],
     {("Source", "Facility", "Sink")}),
    ("multigraph", 2, 2, True, 1.0,
     [("Source", "Sink"), ("Source", "Sink")],
     {("Source", "Sink"), ("Source", "Sink")}),
    ("multisourcesink", 3, 3, False, 1.0,
     [("SourceA", "Facility"), ("SourceB", "Facility"), ("Facility", "SinkA"),
      ("Facility", "SinkB")],
     {("SourceA", "Facility", "SinkA"), ("SourceA", "Facility", "SinkB"),
      ("SourceB", "Facility", "SinkA"), ("SourceB", "Facility", "SinkB")}),
    ("bypass", 2, 3, True, 1.0,
     [("Source", "Facility"), ("Source", "Sink"), ("Facility", "Sink")],
     {("Source", "Sink"), ("Source", "Facility", "Sink")}),
    ("independent", 2, 2, False, 1.0,
     [("SourceA", "SinkA"), ("SourceB", "SinkB")],
     {("SourceA", "SinkA"), ("SourceB", "SinkB")}),
    ("cycle", 4, 4, True, 0.5,
     [("Source", "Facility"), ("Facility", "Recycle"), ("Recycle", "Facility"),
      ("Recycle", "Sink")],
     {("Source", "Facility", "Recycle", "Sink")}),
    ("selfcycle", 3, 3, True, 0.666667,
     [("Source", "Facility"), ("Facility", "Facility"), ("Facility", "Sink")],
     {("Source", "Facility", "Sink")})
]
