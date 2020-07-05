from graphviz import Graph, nohtml

g = Graph('strict', filename='2 binairy tree.gv',
            node_attr={'shape': 'record', 'height': '.1'},graph_attr={'rankdir':'LR'})

g.node('α0', nohtml('<f0> |<f1> α0|<f2>'))
g.node('α1', nohtml('<f0> |<f1> α1|<f2>'))
g.node('00', nohtml('<f0> |<f1> 00|<f2>'))
g.node('ω0', nohtml('<f0> |<f1> ω0|<f2>'))
g.node('ω1', nohtml('<f0> |<f1> ω1|<f2>'))


g.edge('α0:f2', '00:f1')
g.edge('α1:f0', '00:f1')
g.edge('00:f0', 'ω0:f1')
g.edge('00:f2', 'ω1:f1')

g.render(format="dot")