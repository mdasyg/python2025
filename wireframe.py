import math

class Node:
    def __init__(self,coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        
        
class Edge:
    def __init__(self,start,stop):
        self.start = start
        self.stop = stop 
 
class Wireframe:
    def __init__(self):
        self.nodes = []
        self.edges = []
        
    def addNodes(self, nodeList):
        for node in nodeList:
            self.nodes.append(Node(node))
            
    def addEdges(self, edgeList):
        for (start,stop) in edgeList:
            self.edges.append(Edge(self.nodes[start],self.nodes[stop]))
            
    def outputNodes(self):
         print("\n -- Nodes -- ")
         for i,node in enumerate(self.nodes):
             print("%d: (%.2f, %.2f, %.2f)" % (i, node.x, node.y, node.z))
             
    def outputEdges(self):
        print("\n -- Edges -- ")
        for i,edge in enumerate(self.edges):
            print("%d: (%.2f, %.2f, %.2f)" % (i, edge.start.x, edge.start.y, edge.start.z))
            print("----> (%.2f, %.2f, %.2f)" % (edge.stop.x, edge.stop.y, edge.stop.z))
         
    def translate(self,axis,d):
        if axis in ['x','y', 'z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node,axis)+d) #node.axis=node.axis+d
                
    def scale(self, center_xcenter_y, scale):
        center_x,center_y=center_xcenter_y
        for node in self.nodes:
            node.x = center_x + scale* ( node.x - center_x)
            node.y = center_y + scale * ( node.y - center_y)
            node.z *= scale
            
            
    def findCenter(self):
        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes
        return (meanX, meanY, meanZ)
        
    def rotateX(self, cxcycz,radians):
        cx,cy,cz = cxcycz
        for node in self.nodes:
            y = node.y - cy
            z = node.z - cz
            node.y = cy + y*math.cos(radians) - z*math.sin(radians)
            node.z = cz + y*math.sin(radians) + z*math.cos(radians)   

    def rotateY(self, cxcycz,radians):
        cx,cy,cz = cxcycz
        for node in self.nodes:
            x = node.x - cx
            z = node.z - cz
            node.x = cx + x*math.cos(radians) + z*math.sin(radians)
            node.z = cz - x*math.sin(radians) + z*math.cos(radians)  

    def rotateZ(self, cxcycz,radians):
        cx,cy,cz = cxcycz
        for node in self.nodes:
            x = node.x - cx
            y = node.y - cy
            node.x = cx + x*math.cos(radians) - y*math.sin(radians)
            node.y = cy + x*math.sin(radians) + y*math.cos(radians) 
  
# myobject = Wireframe()
# myobject.addNodes([ (0,0,0), (1,2,3), (3,2,1)])
# myobject.addEdges([(1,2)])  
# myobject.outputNodes()
# myobject.outputEdges()

if __name__ == "__main__":
    cube_nodes = [(x,y,z) for x in (0,1) for y in (0,1) for z in (0,1)]
    cube = Wireframe()
    cube.addNodes(cube_nodes)
    cube.outputNodes()
    cube.addEdges([(n,n+4) for n in range(0,4)])
    cube.addEdges([(n,n+1) for n in (0,2,4,6)])#range(0,8,2)
    cube.addEdges([(n,n+2) for n in (0,1,4,5)])
    cube.outputEdges()
