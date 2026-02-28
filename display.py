import wireframe
import pygame

class ProjectionViewer:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("My Display2026")
        self.background=(10,10,50)
        
        self.wireframes={}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour =   (255,255,255)
        self.edgeColour =   (200,200,200)
        self.nodeRadius = 4
        
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
        
    def display(self):
        self.screen.fill(self.background)
        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)
                    
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)
    
    key_to_function = {
    pygame.K_LEFT: (lambda x: x.translateAll('x',-10)),
    pygame.K_RIGHT: (lambda x: x.translateAll('x',10)),
    pygame.K_DOWN:  (lambda x: x.translateAll('y',10)),
    pygame.K_UP:    (lambda x: x.translateAll('y',-10)),
    pygame.K_EQUALS:   (lambda x: x.scaleAll(1.25)),
    pygame.K_MINUS:     (lambda x: x.scaleAll(0.75))
    }
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                elif event.type == pygame.KEYDOWN:
                    if event.key in ProjectionViewer.key_to_function:
                        ProjectionViewer.key_to_function[event.key](self)
            self.display()
            pygame.display.flip()
            
    def translateAll(self, axis, d):
        for wireframe in self.wireframes.values():
            wireframe.translate(axis,d)
            
    def scaleAll(self,scale):
        center_x = self.width / 2
        center_y = self.height / 2
        center_xcenter_y=center_x, center_y
        for wireframe in self.wireframes.values():
            wireframe.scale(center_xcenter_y, scale)
            
            
            
if __name__ == '__main__':
        pv = ProjectionViewer(400,300)
        
        # το αντιγράφω από wireframe.pygame cube = Wireframe()
        cube = wireframe.Wireframe()
        cube_nodes = [(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)]
        cube.addNodes(cube_nodes)
        cube.outputNodes()
        cube.addEdges([(n,n+4) for n in range(0,4)])
        cube.addEdges([(n,n+1) for n in (0,2,4,6)])#range(0,8,2)
        cube.addEdges([(n,n+2) for n in (0,1,4,5)])
        #
        pv.addWireframe('cube', cube)
        pv.run()