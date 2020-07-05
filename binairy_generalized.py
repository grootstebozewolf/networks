from graphviz import Graph, nohtml
from enum import Enum, auto, Flag
from math import sqrt

nodes = 4
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
  """
  A 2x2 router (think factorio) which can pass items from α to ω
  has connections to a NodeType 
  """
  
  def __init__(self, nodeType, n, maxLevel, level = None):
    self.upstreamLeft: None
    self.upstreamRight: None
    self.downstreamLeft: None
    self.upstreamRight: None    
    super(Router, self).__init__(nodeType, n, maxLevel, level)
    
  def Populate(self, g):        
    if hasattr(self, "upstreamLeft") and not self.upstreamLeft is None:      
      g.edge(f"{self.NameBinary}:f0", self.upstreamLeft.NameBinary )
      self.upstreamLeft.Populate(g)
    if hasattr(self, "upstreamRight") and not self.upstreamRight is None:
      g.edge(f"{self.NameBinary}:f2", self.upstreamRight.NameBinary )
      self.upstreamRight.Populate(g)
    if hasattr(self, "downstreamLeft") and not self.downstreamLeft is None:    
      g.edge(self.downstreamLeft.NameBinary, f"{self.NameBinary}:f1")
      self.downstreamLeft.Populate(g)
    if hasattr(self, "downstreamRight") and not self.downstreamRight is None:
      g.edge(self.downstreamRight.NameBinary, f"{self.NameBinary}:f1")
      self.downstreamRight.Populate(g)
    super(Router,self).Populate(g)

        
terminals = []
maxLevel = round(sqrt(nodes))
for x in range(0,nodes):
  terminals += [ \
    Node(NodeType.START, x, maxLevel), \
    Node(NodeType.END, x, maxLevel) \
  ]

#for terminal in terminals:
#  terminal.Populate(g)

root = Router(NodeType.ROUTER, 0, maxLevel, maxLevel//2+1)

def recursiveRoot(terminals, node):
    """
    Build tree of nodes with 2 inputs and 2 outputs
    """
    if(len(terminals)==4):
        node.downstreamLeft = terminals[0] if not hasattr(node,"downstreamLeft") else node.downstreamLeft
        node.downstreamRight = terminals[2] if not hasattr(node,"downstreamRight") else node.downstreamRight
        node.upstreamLeft = terminals[1] if not hasattr(node,"upstreamRight")  else node.upstreamLeft
        node.upstreamRight = terminals[3] if not hasattr(node,"upstreamRight")  else node.upstreamRight
    else:
        node.upstreamLeft = Router(NodeType.ROUTER, node.n + 2, maxLevel, node.level+1)
        node.upstreamRight = Router(NodeType.ROUTER, node.n + 1, maxLevel, node.level+1)
        node.downstreamLeft = Router(NodeType.ROUTER, node.n - 2, maxLevel, node.level-1)
        node.downstreamRight = Router(NodeType.ROUTER, node.n - 1, maxLevel, node.level-1)
        
        recursiveRoot(terminals[:len(terminals)//2],node.upstreamLeft) 
        recursiveRoot(terminals[:len(terminals)//2],node.downstreamLeft)        
        recursiveRoot(terminals[len(terminals)//2:],node.upstreamLeft)        
        recursiveRoot(terminals[len(terminals)//2:],node.upstreamRight)
 

terminals = []
maxLevel = round(sqrt(nodes))
for x in range(0,nodes):
  terminals += [ \
    Node(NodeType.START, x, maxLevel), \
    Node(NodeType.END, x, maxLevel) \
  ]

root = Router(NodeType.ROUTER, 0, maxLevel, maxLevel//2+1)
recursiveRoot(terminals, root)

root.Populate(g)
g.render(format="dot")
