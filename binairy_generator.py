from graphviz import Graph, nohtml
from enum import Enum, auto, Flag
from math import sqrt

class NodeType(Enum):
  START = auto()
  ROUTER = auto()
  END = auto()

class Direction(Flag):
  UPSTREAM = auto()
  DOWNSTREAM = auto()
  ROOT = UPSTREAM | DOWNSTREAM

class Node:
  __slots__ = ['nodeType', 'n', 'maxLevel', 'level', '_left', '_right']
  def __init__(self, nodeType, n, maxLevel, level = None):
    self.nodeType = nodeType
    self.n = n
    self.maxLevel = maxLevel
    self.level = level
    self._left = None
    self._right = None
  

  @property
  def left(self):
    return self._left

  @left.setter
  def left(self, value):
    self._left = value

  @property
  def right(self):
    return self._right

  @right.setter
  def right(self, value):
    self._right = value

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
    if not self.left is None:  
      g.edge(f"{self.NameBinary}:f1", f"{self.left.NameBinary}:f2")    
    if not self.right is None:
      g.edge(f"{self.NameBinary}:f1", f"{self.right.NameBinary}:f0")

class Start(Node):
  def __init__(self, n, maxLevel):
    super().__init__(NodeType.START, n, maxLevel, -1)

class End(Node):
  def __init__(self,n, maxLevel):
    super().__init__(NodeType.END, n, maxLevel, maxLevel+1)

class Router(Node):
  @staticmethod
  def generate(maxLevel):
    terminals = []
    upstream_routers = []
    downstream_routers = []
    nodes = []
    num_nodes = 2 ** maxLevel
    for x in range(0,num_nodes):
      terminals += [ \
        Start(x, maxLevel), \
        End(x, maxLevel) \
      ]
    upstream_nodes = [x for x in terminals if type(x) is Start]
    downstream_nodes = [x for x in terminals if type(x) is End]
    level_upstream = 0
    level_downstream =  maxLevel*2-2
    while(len(upstream_nodes) != 0 and len(downstream_nodes) != 0):
      nodes += upstream_nodes + downstream_nodes
      n = 0
      for start_nodes_pair in zip(upstream_nodes[::2], upstream_nodes[1::2]):
        router = Router(n, maxLevel, level_upstream)
        start_nodes_pair[0].right = router
        start_nodes_pair[1].left = router
        upstream_routers += [router]
        n = n + 1
      m = 0
      for end_nodes_pair in zip(downstream_nodes[::2], downstream_nodes[1::2]):
        router = Router(m, maxLevel,level_downstream)
        router.left = end_nodes_pair[0]
        router.right = end_nodes_pair[1]
        downstream_routers += [router]
        m = m + 1
      upstream_nodes = upstream_routers
      upstream_routers = []
      downstream_nodes = downstream_routers
      downstream_routers = []
      level_upstream = level_upstream + 1
      level_downstream = level_downstream - 1
    #root = Router(0,maxLevel,level_upstream,downstream_nodes[0], downstream_nodes[1])
    #upstream_nodes[0].left = root
    #upstream_nodes[1].right = root
    #nodes += upstream_nodes + downstream_nodes
    return nodes
  
  def __init__(self, n, maxLevel, level, left=None, right=None):
    super().__init__(NodeType.ROUTER, n, maxLevel, level)
    self._left = left
    self._right = right
maxLevel = 11
num_nodes = 2**maxLevel
nodes = Router.generate(maxLevel)
g = Graph(f"{num_nodes} binairy tree general", filename=f"{num_nodes} binairy tree general.gv",
            node_attr={"shape": "record", "height": ".1"},graph_attr={'rankdir':'LR'})

for node in nodes:
  node.Populate(g)

g.render(format="dot")