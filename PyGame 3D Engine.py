import sys, os, pygame, math
from xml.dom.minidom import parse, Document


# --- Init ------------------------------------------------------------------------------------------------------------------------------------------------

pygame.init()
font10 =  pygame.font.Font('C:\\Windows\\Fonts\\Arial.ttf', 10)
font30 =  pygame.font.Font('C:\\Windows\\Fonts\\Arial.ttf', 30)

# --- Classes ---------------------------------------------------------------------------------------------------------------------------------------------


class GroupItemClass():
    """ Container for each item in a group """

    def __init__(self, text, position, textColor=(0, 0, 0), backColor=(255, 255, 255)):
        """ Create the items of the group """
        self.text = text
        self.position = position
        self.textColor = textColor
        self.backColor = backColor


class GroupClass():
    """ Container for each group in a menu """

    def __init__(self, color, rectangle, name='Group'):
        """ Create the items of the group """
        self.color = color
        self.rectangle = rectangle
        self.items = []
        self.selectedItem = 0
        self.name = name

    def _addItem(self, item):
        self.items.append(item)


class MenuClass:
    """ A menu that can be rendered on screen, containing setting of options """

    def __init__(self, parent, width, height):
        """ Create the items of the menu """
        self.displayed = 0
        self.pWidth = width
        self.pHeight = height
        self.width = 1000
        self.height = 640
        self.selectedGroup = 0
        self.screen = parent.screen
        self.groups = [GroupClass([0, 0, 0], [110, 90, 90, 200], 'LoadSave'), GroupClass([0, 0, 0], [205, 90, 580, 200], 'Unused2'), GroupClass([0, 0, 0], [790, 90, 300, 620],'ObjectsGroup'), GroupClass([0, 0, 0], [110, 295, 675, 415], 'Unused 4')]

        # Adding Load/Save
        self.groups[0]._addItem(GroupItemClass('Load', [120, 132]))
        self.groups[0]._addItem(GroupItemClass('Save', [120, 194]))

        # Populating with objects loaded
        for nr, wf in enumerate(parent.wireframes):
            self.groups[2]._addItem(GroupItemClass(wf.name, (800, 95 + nr * 35)))
        self.groups[2]._addItem(GroupItemClass('All', (800, 95 + len(parent.wireframes) * 35)))
        self.groups[2].selectedItem = parent.selectedObject

        # Adding speed&scale-values
        self.groups[3]._addItem(GroupItemClass(str(parent.scaleFactor), (120, 400)))
        self.groups[3]._addItem(GroupItemClass(str(parent.moveSpeed), (120, 435)))
        self.groups[3]._addItem(GroupItemClass(str(parent.rotateSpeed), (120, 470)))







    def _menuCoords(self, Lx, Ly):
        """ Translates Menu-coordinates to Screen-coordinates. Supports negative coords, counting from right/lower of menu """

        if Lx < 0:
            xCoord = self.width + Lx + (self.pWidth - self.width) / 2
        else:
            xCoord = Lx + (self.pWidth - self.width) / 2

        if Ly < 0:
            yCoord = self.height + Ly + (self.pHeight - self.height) / 2
        else:
            yCoord = Ly + (self.pHeight - self.height) / 2

        return [xCoord, yCoord]


    def _screenCoords(self, Sx, Sy):
        """ Translates Screen-coordinates to Menu-coordinates. Never used, for demonstration only? """
        return (Sx - (self.pWidth - self.width) / 2,  Sy - (self.pHeight - self.height) / 2)


    def _showText(self, text, (xCoord, yCoord), cText=(0, 0, 0), cBG=(255, 255, 255)):
        textWidth = len(text) * 10
        textHeight = font30.get_height()    # for future support of multiple fonts
        textRect = pygame.Rect(xCoord, yCoord, textWidth, textHeight)
        test_message = font30.render(text, True, cText, cBG)
        self.screen.blit(test_message, textRect)
        

    def _switch(self):
        """ Switch display of menu on and off """
        if self.displayed:
            self.displayed = 0
        else:
            self.displayed = 1
        return 1


    def _moveGroupSelection(self, Up):
        """ Moves the selection to next item in list """
        if Up:
            self.selectedGroup += 1
        else:
            self.selectedGroup -= 1
        if self.selectedGroup > len(self.groups) - 1:
            self.selectedGroup = 0
        if self.selectedGroup < 0:
            self.selectedGroup = len(self.groups) - 1


    def _moveItemSelection(self, Up):
        """ Moves the selection to next item in list """
        if Up:
            self.groups[self.selectedGroup].selectedItem += 1
        else:
            self.groups[self.selectedGroup].selectedItem -= 1

            
        if self.groups[self.selectedGroup].selectedItem > len(self.groups[self.selectedGroup].items) - 1:
            self.groups[self.selectedGroup].selectedItem = 0
        if self.groups[self.selectedGroup].selectedItem < 0:
            self.groups[self.selectedGroup].selectedItem = len(self.groups[self.selectedGroup].items) - 1


    def _handleKeys(self, event):
        """ Registers which keys are held down and which are released, and acts accordingly. Must get event from main program! """
        if event.type == pygame.KEYDOWN:
            if event.key == 32:                                 # SPACE
                self.displayed = False
            elif event.key == 9:                                # TAB
                print 'TAB handled, but bound to nothing'
            elif event.key == 273:                              # Up
                self._moveItemSelection(0)
            elif event.key == 274:                              # Down
                self._moveItemSelection(1)
            elif event.key == 275:                              # Right
                self._moveGroupSelection(1)
            elif event.key == 276:                              # Left
                self._moveGroupSelection(0)


    def _display(self):
        """ Draw the menu """
        pygame.draw.rect(self.screen, (255,255,255), ((self.pWidth - self.width) / 2, (self.pHeight - self.height) / 2, self.width, self.height))
        pygame.draw.rect(self.screen, (0, 0, 0), (self._menuCoords(5, 5), (self.width - 10, self.height - 10)), 1)            # Outer-frame

        for nr, group in enumerate(self.groups):
            if nr == self.selectedGroup:
                pygame.draw.rect(self.screen, (255, 0, 0) , (group.rectangle), 3)
            else:
                pygame.draw.rect(self.screen, (group.color) , (group.rectangle), 1)
                
            for nr, item in enumerate(group.items):
                if nr == group.selectedItem:
                    self._showText(item.text, item.position, (255, 0, 0), item.backColor)
                else:
                    self._showText(item.text, item.position, item.textColor, item.backColor)



class Wireframe:
    """ Class to contain wireframes handled by viewer-class """
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.edges = []
        self.faces = []

    def addNodes(self, nodeList):
        for node in nodeList:
            self.nodes.append(node)


    def addEdges(self, edgeList):
        self.edges += edgeList


    def addFaces(self, faceList):
        self.faces += faceList


    def translate(self, axis, d):
        """ Add constant 'd' to the coordinate 'axis' of each node of a wireframe """
        for node in self.nodes:
            if axis == 'x':
                node[0] += d
            elif axis == 'y':
                node[1] += d
            elif axis == 'z':
                node[2] += d

    def scale(self, (centre_x, centre_y), scale):
        """ Scale the wireframe from the centre of the screen """
        for node in self.nodes:
            node[0] = centre_x + scale * (node[0] - centre_x)
            node[1] = centre_y + scale * (node[1] - centre_y)
            node[2] *= scale

    def findCentre(self):
        """ Find the centre of the wireframe. """
        num_nodes = len(self.nodes)
        meanX = sum([node[0] for node in self.nodes]) / num_nodes
        meanY = sum([node[1] for node in self.nodes]) / num_nodes
        meanZ = sum([node[2] for node in self.nodes]) / num_nodes
        return (meanX, meanY, meanZ)

    def rotateZ(self, (cx,cy,cz), radians):       
        for node in self.nodes:
            x      = node[0] - cx
            y      = node[1] - cy
            d      = math.hypot(y, x)
            theta  = math.atan2(y, x) + radians
            node[0] = cx + d * math.cos(theta)
            node[1] = cy + d * math.sin(theta)

    def rotateX(self, (cx,cy,cz), radians):
        for node in self.nodes:            
            y      = node[1] - cy
            z      = node[2] - cz
            d      = math.hypot(y, z)
            theta  = math.atan2(y, z) + radians
            node[2] = cz + d * math.cos(theta)
            node[1] = cy + d * math.sin(theta)
     
    def rotateY(self, (cx,cy,cz), radians):
        for node in self.nodes:
            x      = node[0] - cx
            z      = node[2] - cz
            d      = math.hypot(x, z)
            theta  = math.atan2(x, z) + radians
            node[2] = cz + d * math.cos(theta)
            node[0] = cx + d * math.sin(theta)



class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, path, width, height, displayNodes=1, displayEdges=1, displayFaces=1, displayObj= 1):
        print('Program initiating...')
        self.width = width
        self.height = height
        self.centre = (width / 2, height / 2, 200)  # Center of 3D space
        self.screen = pygame.display.set_mode((width, height))
        pygame.font.init()
        pygame.display.set_caption('PyGame 3D Engine')
        self.font = pygame.font.SysFont(None, 15)
        self.background = (10,10,50)
        self.wireframes = []
        self.nodeColour = (0,255,255)
        self.edgeColour = (255,255,255)
        self.faceColour = (0,0,255)
        self.nodeRadius = 2
        self.scaleFactor = 0.0025
        self.moveSpeed = 1.0
        self.rotateSpeed = 0.01
        self.running = False
        self._keysHeld = []
        self._path = path
        self.displayNodes = displayNodes
        self.displayEdges = displayEdges
        self.displayFaces = displayFaces
        self.displayObjectList = displayObj
        self.readData()
        self.selectedObject = len(self.wireframes)
        self.optMenu = MenuClass(self, width, height)


    def readData(self):
        """ Reads an XML-file and builds wireframes """
        if not os.path.exists(self._path):
            sys.exit('File path does not exist!')
        print('Loading file "' + path + '"...')
        self.parser = parse(path)
        for obj in self.parser.childNodes[0].getElementsByTagName('object'):
            name = str(obj.getAttribute('id'))
            newWireframe = Wireframe(name)
            rawVertices = obj.getElementsByTagName('vertice')
            for x in rawVertices:
                vertice = []
                for count in [1,3,5]:
                    vertice.append(float(x.childNodes[count].firstChild.nodeValue))
                newWireframe.nodes.append(vertice)
            rawEdges = obj.getElementsByTagName('edge')
            for y in rawEdges:
                edge = []
                for count in [1,3]:
                    edge.append(int(y.childNodes[count].firstChild.nodeValue))
                newWireframe.edges.append(edge)
            rawFaces = obj.getElementsByTagName('face')
            for z in rawFaces:
                face = []
                for count in range(1, len(z.childNodes), 2):
                    face.append(int(z.childNodes[count].firstChild.nodeValue))
                newWireframe.faces.append(face)
            self._addWireframe(name, newWireframe)
        print('  Found ' + str(len(self.wireframes)) + ' objects in file:')
        for wf in self.wireframes:
            print '    "' + wf.name + '" with ' + str(len(wf.nodes)) + ' vertices'
        print '  Loading complete!'
        return 1


    def writeData(self):
        """ Writes each wireframe to a file """
        fh = open(self._path, 'w')
        xmlDoc = Document()
        topElement = xmlDoc.createElement("catalog")
        xmlDoc.appendChild(topElement)
        for name, obj in self.wireframes.iteritems():
            # create each object-element
            objectElement = xmlDoc.createElement("object")
            topElement.appendChild(objectElement)
            objectElement.setAttribute('id', obj.name)
            objectElement.setIdAttribute('id')
            # add vertices
            for vertice in obj.nodes:
                verticeElement = xmlDoc.createElement("vertice")
                objectElement.appendChild(verticeElement)
                xElement = xmlDoc.createElement("x")
                yElement = xmlDoc.createElement("y")
                zElement = xmlDoc.createElement("z")
                xElement.appendChild(xmlDoc.createTextNode(str(vertice[0])))
                yElement.appendChild(xmlDoc.createTextNode(str(vertice[1])))
                zElement.appendChild(xmlDoc.createTextNode(str(vertice[2])))
                verticeElement.appendChild(xElement)
                verticeElement.appendChild(yElement)
                verticeElement.appendChild(zElement)
            # add faces
            for face in obj.faces:
                faceElement = xmlDoc.createElement("face")
                objectElement.appendChild(faceElement)
                for nr, node in enumerate(face):
                    nodeElement = xmlDoc.createElement("node" + str(nr + 1))
                    nodeElement.appendChild(xmlDoc.createTextNode(str(node)))
                    faceElement.appendChild(nodeElement)
            # add edges
            for edge in obj.edges:
                edgeElement = xmlDoc.createElement("edge")
                objectElement.appendChild(edgeElement)
                xElement = xmlDoc.createElement("x")
                yElement = xmlDoc.createElement("y")
                xElement.appendChild(xmlDoc.createTextNode(str(edge[0])))
                yElement.appendChild(xmlDoc.createTextNode(str(edge[1])))
                edgeElement.appendChild(xElement)
                edgeElement.appendChild(yElement)
        fh.writelines(xmlDoc.toprettyxml())
        fh.close()
        print('Wrote file ok')


    def _addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """
        self.wireframes.append(wireframe)


    def _getKeys(self):
        """ Registers which keys are held down and which are released, then moves view accordingly """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.optMenu.displayed:
                    self.optMenu._handleKeys(event)
                else:
                    if event.key == pygame.K_ESCAPE:                    # Escape
                        self.running = False
                    elif event.key == 32:                               # SPACE
                        self.optMenu._switch()
                    else:
                        self._keysHeld.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self._keysHeld:
                    self._keysHeld.remove(event.key)

        # Process keys being held down...
        if 269 in self._keysHeld:   self._scaleObjects(1 - self.scaleFactor)        # Numpad -
        if 270 in self._keysHeld:   self._scaleObjects(1 + self.scaleFactor)        # Numpad +
        if 273 in self._keysHeld:   self._moveObjects('y', -self.moveSpeed)         # Up
        if 274 in self._keysHeld:   self._moveObjects('y',  self.moveSpeed)         # Down
        if 275 in self._keysHeld:   self._moveObjects('x',  self.moveSpeed)         # Right
        if 276 in self._keysHeld:   self._moveObjects('x', -self.moveSpeed)         # Left
        if 115 in self._keysHeld:   self._rotateObjects('X', -self.rotateSpeed)     # S
        if 119 in self._keysHeld:   self._rotateObjects('X',  self.rotateSpeed)     # W
        if 97  in self._keysHeld:   self._rotateObjects('Y',  self.rotateSpeed)     # A
        if 100 in self._keysHeld:   self._rotateObjects('Y', -self.rotateSpeed)     # D
        if 101 in self._keysHeld:   self._rotateObjects('Z',  self.rotateSpeed)     # E
        if 113 in self._keysHeld:   self._rotateObjects('Z', -self.rotateSpeed)     # Q

        
    def _display(self):
        """ Draw the wireframes on the screen. """
        self.screen.fill(self.background)
        for wireframe in self.wireframes:
            if self.displayEdges:
                for n1, n2 in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, wireframe.nodes[n1 - 1][:2], wireframe.nodes[n2 - 1][:2], 1)
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
            if self.displayFaces:
                for face in wireframe.faces:
                    nodeList = []
                    for node in face:
                        nodeList.append(wireframe.nodes[node - 1][:2])
                    pygame.draw.polygon(self.screen, self.faceColour, nodeList, 0)
            if self.optMenu.displayed:
                self.optMenu._display()
        pygame.display.flip()


    def _findCommonCentre(self):
        """ Go through each wireframe, add up coordinates for centres, and divide up """
        common = [0,0,0]
        for wireframe in self.wireframes:
            common[0] += wireframe.findCentre()[0]
            common[1] += wireframe.findCentre()[1]
            common[2] += wireframe.findCentre()[2]
        num_nodes = len(self.wireframes)
        return (common[0] / num_nodes, common[1] / num_nodes, common[2] /num_nodes)

    
    def _moveObjects(self, axis, d):
        """ Move all wireframes along a given axis by d units. """
        if self.selectedObject == len(self.wireframes) : # All objects are selected
            for wireframe in self.wireframes:
                wireframe.translate(axis, d)
        else:
            self.wireframes[self.selectedObject].translate(axis, d)


    def _scaleObjects(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """
        centre_x = self.width  / 2
        centre_y = self.height / 2
        if self.selectedObject == len(self.wireframes) : # All objects are selected
            for wireframe in self.wireframes:
                wireframe.scale((centre_x, centre_y), scale)
        else:
            self.wireframes[self.selectedObject].scale((centre_x, centre_y), scale)


    def _rotateObjects(self, axis, theta):
        """ Rotate one or all wireframe about their centre, along a given axis by a given angle. """
        if self.selectedObject == len(self.wireframes) : # All objects are selected
            for wireframe in self.wireframes:
                getattr(wireframe, 'rotate' + axis)(self.centre, theta)
        else:
            getattr(self.wireframes[self.selectedObject], 'rotate' + axis)(self.centre, theta)


    def unify(self):
        """ Build a list of all Edges / Nodes, convert to tuples and build lists of uniques """
        all_Edges = []
        all_Nodes = []
        unique_Edges_Mapped = []
        for wireframe in self.wireframes.itervalues():
            for edge in wireframe.edges:
                all_Edges.append((tuple(wireframe.nodes[edge[0]]), tuple(wireframe.nodes[edge[1]])))
            for node in wireframe.nodes:
                all_Nodes.append(tuple(node))
        # Generating unique tuples
        unique_Nodes = list(set(all_Nodes))
        unique_Edges = list(set(all_Edges))
        print '------------------------------------------------'
        print '  Found ' + str(len(all_Nodes)) + ' Nodes total, ' + str(len(unique_Nodes)) + ' of which are Unique '
        print '  Found ' + str(len(all_Edges)) + ' Edges total, ' + str(len(unique_Edges)) + ' of which are Unique'
        print '------------------------------------------------'
        # Mapping Edges
        for edge in unique_Edges:
            edge_coord = [0,0]
            for nr, node in enumerate(unique_Nodes):
                if node == edge[0]:
                    edge_coord[0] = nr 
                if node == edge[1]:
                    edge_coord[1] = nr
            unique_Edges_Mapped.append(edge_coord)
        # Converting nodes back to list
        for nr, x in enumerate(unique_Nodes):
            unique_Nodes[nr] = list(x)
        # Destroying wireframes
        self.wireframes.clear()
        # Building and adding new wireframe
        pangea = Wireframe()
        pangea.addNodes(unique_Nodes)
        pangea.addEdges(unique_Edges_Mapped)
        self._addWireframe('Pangea', pangea)


    def _extractData(self, data):
        """ Tager en fil som raa data og returnerer faces og vertices """
        global total_vertices
        obj_nr = 0
        objects = [[]]
        _split = data.split('\n')
        for nr, line in enumerate(_split):
            if line[0:2] == 'o ':
                    obj_nr += 1
                    objects.append([])
            objects[obj_nr].append(line)
        # First part is file info, which we discard
        objects.pop(0)
        objectsSorted = []
        for obj in objects:
            name = obj[0].split()[1]
            faces = []
            vertices = []
            for line in obj:
                if len(line) > 0:
                    if line[0] == 'v':
                        split = line.split()
                        vertices.append([float(split[1]), float(split[2]), float(split[3])])
                    if line[0] == 'f':
                        split = line.split()
                        split.pop(0)
                        for entry in split:
                            int_faces = []
                            for entry in split:
                                int_faces.append(int(entry) - total_vertices)
                            faces.append(int_faces)
            total_vertices += len(vertices)
            edges = self._facesToEdges(faces)
            objectsSorted.append(ImportedObjects(name, vertices, edges, faces))
        return objectsSorted


    def _facesToEdges(self, faces):
        """ Genmgaar faces og udregner edges """
        edges = []
        edges_sorted = []
        # Converting...
        for face in faces:
            for nr, x in enumerate(face):
                edges.append((face[nr - 1], face[nr]))
        # Sorting low->high
        for edge in edges:
            if edge[0] < edge[1]:
                    edges_sorted.append((edge[0], edge[1]))
            else:
                    edges_sorted.append((edge[1], edge[0]))
        # Returning uniqes
        return list(set(edges_sorted))


    def importObject(self, path):
        """ Import an .Obj-file and add it as a wireframe """
        global total_vertices
        total_vertices = 0
        if os.path.splitext(path)[1].upper() != '.OBJ':
            print 'Cannot import file, only .obj-files supported'
            return None
        # Importing obj.-file
        print 'Importing file "' + path + '"...'
        fh = open(path, 'r')
        fileData = fh.read()
        fh.close()
        _objects = self._extractData(fileData)
        print '\nFound ' + str(len(_objects)) + ' objects:'
        print '--------------------------------------'
        for _object in _objects:
            print 'The object "' + _object.name + '" contains ' + str(len(_object.vertices)) + ' vertices, ' + str(len(_object.faces)) + ' faces and ' + str(len(_object.edges)) + ' edges'
        # Create and add wireframes
        for _object in _objects:
            wf = Wireframe(_object.name)
            wf.addNodes(_object.vertices)
            wf.addEdges(_object.edges)
            wf.addFaces(_object.faces)
            self._addWireframe(_object.name, wf)
        # Scaling objects
        all_values = []
        for _object in _objects:
            for vertice in _objects[0].vertices:
                for coord in vertice:
                    all_values.append(coord)
        scale_factor = 1000 / abs(max(all_values) - min(all_values))
        self._scaleObjects(scale_factor)
        # Centering objects
        while self.wireframes.itervalues().next().nodes[0][0] < self.width / 2:
            self.__moveObjects('x', 10.0)
        while self.wireframes.itervalues().next().nodes[0][1] < self.height / 2:
            self._moveObjects('y', 10.0)
        while self.wireframes.itervalues().next().nodes[0][0] > self.width / 2:
            self._moveObjects('x', -10.0)
        while self.wireframes.itervalues().next().nodes[0][1] > self.height / 2:
            self._moveObjects('y', -10.0)
        return 1


    def run(self):
        """ Start the main loop from outside """
        print('Program running... press <ESC> to quit')
        self.commonCentre = self._findCommonCentre()
        self.running = True
        self._loop()

        
    def _loop(self):
        """ Main loop """
        while self.running:
            self._getKeys()
            self._display()
        print('\nDisplay closed...\n')
        pygame.quit()
            



# --- Main ---------------------------------------------------------------------------------------------------------------------------------------------

path = 'ConeAndCircle.xml'

if __name__ == '__main__':
    pv = ProjectionViewer(path, 1200, 800, 1, 1, 1, 1)



#    cube = Wireframe('cube1')
#    cube_nodes = [[x,y,z] for x in (50,250) for y in (50,250) for z in (50,250)]
#    cube.addNodes(list(cube_nodes))
#    cube.addEdges([(n,n+4) for n in range(0,4)])
#    cube.addEdges([(n,n+1) for n in range(0,8,2)])
#    cube.addEdges([(n,n+2) for n in (0,1,4,5)])
#    pv._addWireframe('cube1', cube)


  
    pv.run()



# --- Status ---------------------------------------------------------------------------------------------------------------------------------------------

#   - Faa knapperne i menuen til at goere noget
#   - Saet hastigheder i menuen
#   - Lave en label-type, til menu, dvs. text som ikke kan røres
#   - TAB to move selection, left/right to change values? Textfields?

















