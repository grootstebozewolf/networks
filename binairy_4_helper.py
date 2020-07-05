from graphviz import Graph, nohtml

g = Graph("strict", filename="4 binairy tree.gv",
            node_attr={"shape": "record", "height": ".1"},graph_attr={"rankdir":"LR"})



g.node("α00", nohtml("<f0> |<f1> α0|<f2>"))
g.node("α01", nohtml("<f0> |<f1> α1|<f2>"))
g.node("ω00", nohtml("<f0> |<f1> ω0|<f2>"))
g.node("ω01", nohtml("<f0> |<f1> ω1|<f2>"))
g.node("α10", nohtml("<f0> |<f1> α2|<f2>"))
g.node("α11", nohtml("<f0> |<f1> α3|<f2>"))
g.node("ω10", nohtml("<f0> |<f1> ω2|<f2>"))
g.node("ω11", nohtml("<f0> |<f1> ω3|<f2>"))
g.node("000", nohtml("<f0> |<f1> 000|<f2>"))
g.node("010", nohtml("<f0> |<f1> 010|<f2>"))
g.node("100", nohtml("<f0> |<f1> 100|<f2>"))
g.node("200", nohtml("<f0> |<f1> 200|<f2>"))
g.node("210", nohtml("<f0> |<f1> 210|<f2>"))


g.edge("α00:f2", "000:f1")
g.edge("α01:f0", "000:f1")
g.edge("200:f0", "ω00:f1")
g.edge("200:f2", "ω01:f1")
g.edge("α10:f2", "010:f1")
g.edge("α11:f0", "010:f1")
g.edge("210:f0", "ω10:f1")
g.edge("210:f2", "ω11:f1")

g.edge("000:f2", "100:f1")
g.edge("010:f0", "100:f1")
g.edge("100:f0", "200:f1")
g.edge("100:f2", "210:f1")


g.render(format="dot")