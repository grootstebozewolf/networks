from graphviz import Graph, nohtml
from enum import Enum, auto, Flag
from math import sqrt

nodes = 8
g = Graph(f"{nodes} binairy tree general", filename=f"{nodes} binairy tree general.gv",
            node_attr={"shape": "record", "height": ".1"})

class NodeType(Enum):
  START = auto()
  ROUTER = auto()
  END = auto()

class Direction(Flag):
  UPSTREAM = auto()
  DOWNSTREAM = auto()
  ROOT = UPSTREAM | DOWNSTREAM

  
class Node:
  def __init__(self, nodeType, n, maxLevel, level = None):
    self.nodeType = nodeType
    self.n = n
    self.maxLevel = maxLevel
    self.level = level
  
  @property
  def NameBinary(self):
    nameBinary = f"{self.n:b}".zfill(self.maxLevel)
    if(self.nodeType == NodeType.START):
      return f"α{nameBinary}"
    elif(self.nodeType == NodeType.END):
      return f"ω{nameBinary}"
    elif(self.nodeType == NodeType.ROUTER):
      return f"{self.level}{nameBinary}"

  def Populate(self, g):
    nameBinary = f"{self.n:b}".zfill(self.maxLevel)
    if(self.nodeType == NodeType.START):
      g.node(self.NameBinary, nohtml(f"<f0> |<f1> α{self.n}|<f2>"))
    elif(self.nodeType == NodeType.END):
      g.node(self.NameBinary, nohtml(f"<f0> |<f1> ω{self.n}|<f2>"))
    elif(self.nodeType == NodeType.ROUTER):
      g.node(self.NameBinary, nohtml(f"<f0> |<f1> {self.NameBinary}|<f2>"))

class Router(Node):
  def Wire(self, g, terminals, direction = Direction.ROOT, parent = None):
    if len(terminals) == 0:
      pass
    if len(terminals) == 4:        
      self.Populate(g)
      if Direction.DOWNSTREAM in direction:
        g.edge(terminals[0].NameBinary, f"{self.NameBinary}:f1")
        g.edge(terminals[2].NameBinary, f"{self.NameBinary}:f1")
      if Direction.UPSTREAM in direction:
        g.edge(f"{self.NameBinary}:f0", terminals[1].NameBinary)
        g.edge(f"{self.NameBinary}:f2", terminals[3].NameBinary)
    else:
      leftD = Router(NodeType.ROUTER, parent.n if not parent is None else 0,self.maxLevel, self.level-1)  
      rightD = Router(NodeType.ROUTER,parent.n+3 if not parent is None else 3,self.maxLevel, self.level-1)
      leftU = Router(NodeType.ROUTER, parent.n if not parent is None else 0,self.maxLevel, self.level+1)  
      rightU = Router(NodeType.ROUTER,parent.n+3 if not parent is None else 3,self.maxLevel, self.level+1)
        
      leftD.Wire(g, terminals[:len(terminals)//2],Direction.DOWNSTREAM,parent)
      rightD.Wire(g, terminals[len(terminals)//2:],Direction.DOWNSTREAM,parent)
      
      leftU.Wire(g, terminals[:len(terminals)//2],Direction.UPSTREAM,parent)
      rightU.Wire(g, terminals[len(terminals)//2:],Direction.UPSTREAM,parent)
      if parent is None:
        self.Wire(g, [leftD,leftU, rightD, rightU])

terminals = []
maxLevel = round(sqrt(nodes))
for x in range(0,nodes):
  terminals += [ \
    Node(NodeType.START, x, maxLevel), \
    Node(NodeType.END, x, maxLevel) \
  ]

for terminal in terminals:
  terminal.Populate(g)

root = Router(NodeType.ROUTER, 0, maxLevel, maxLevel//2+1)
root.Wire(g,terminals)
g.render(format="dot")
