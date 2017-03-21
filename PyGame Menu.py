import sys, os, pygame
from pygame import KMOD_SHIFT, KMOD_ALT

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

    def __init__(self, color, rectangle):
        """ Create the items of the group """
        self.color = color
        self.rectangle = rectangle
        self.items = []

    def _addItem(self, item):
        self.items.append(item)




class MenuClass:
    """ A menu that can be rendered on screen, containing setting of options """

    def __init__(self, screen, width, height):
        """ Create the items of the menu """
        self.displayed = 0
        self.pWidth = width
        self.pHeight = height
        self.width = 1000
        self.height = 640
        self.selectedGroup = 0
        self.selectedItem = 0
        self.screen = screen
        self.groups = [GroupClass([0, 0, 0], [110, 90, 90, 200]), GroupClass([0, 0, 0], [205, 90, 580, 200]), GroupClass([0, 0, 0], [790, 90, 300, 620]), GroupClass([0, 0, 0], [110, 295, 675, 415])]
        self.groups[0]._addItem(GroupItemClass('Load', [120, 132]))
        self.groups[0]._addItem(GroupItemClass('Save', [120, 194]))

 


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


    def _switch(self):
        """ Switch display of menu on and off """
        if self.displayed:
            self.displayed = 0
        else:
            self.displayed = 1


    def _showText(self, text, (xCoord, yCoord), cText=(0, 0, 0), cBG=(255, 255, 255)):
        textWidth = len(text) * 10
        textHeight = font30.get_height()    # for future support of multiple fonts
        textRect = pygame.Rect(xCoord, yCoord, textWidth, textHeight)
        test_message = font30.render(text, True, cText, cBG)
        self.screen.blit(test_message, textRect)


    def _moveGroupSelection(self):
        """ Moves the selection to next item in list """
        self.selectedGroup += 1
        if self.selectedGroup > len(self.groups) - 1:
            self.selectedGroup = 0


    def _moveItemSelection(self):
        """ Moves the selection to next item in list """
        self.selectedItem += 1
        if self.selectedItem > len(self.groups[self.selectedGroup].items) - 1:
            self.selectedItem = 0



# --- SETUP -----------------------------------------------------------------------------------------------------

    # Call this, instead of _handleKeys while setting up menu!!!
    def _handleKeysSetup(self, event):
        """ Only used for setting up Menu. Can be deleted when done. Replace with _handleKeys while setup """
        
        # Set modification-value
        if pygame.key.get_mods() & KMOD_SHIFT:
            value = 10
        else:
            value = 1

        if event.type == pygame.KEYDOWN:
            if event.key == 9:                                              # TAB
                if pygame.key.get_mods() & KMOD_SHIFT:
                    self._moveItemSelection()
                else:
                    self._moveGroupSelection()
            elif event.key == 32 or event.key == pygame.K_ESCAPE:           # SPACE or ESCAPE = Exit and dump data to std_out
                self.displayed = False
                parent.running = False
                print 'Dumping data for groups....'
                print 100 * '-'
                for g in self.groups:
                    print g.color, g.rectangle
                    for i in g.items:
                        print '   "' + i.text + '" :', i.position
                print 100 * '-'
            elif event.key == 273:                                          # Up
                if pygame.key.get_mods() & KMOD_ALT:
                    self.groups[self.selectedGroup].rectangle[3] -= value
                else:
                    self.groups[self.selectedGroup].rectangle[1] -= value
                    self.groups[self.selectedGroup].rectangle[3] -= value
                    for item in self.groups[self.selectedGroup].items:
                        item.position[1] -= value
            elif event.key == 274:                                          # Down
                if pygame.key.get_mods() & KMOD_ALT:
                    self.groups[self.selectedGroup].rectangle[3] += value
                else:
                    self.groups[self.selectedGroup].rectangle[1] += value
                    self.groups[self.selectedGroup].rectangle[3] += value
                    for item in self.groups[self.selectedGroup].items:
                        item.position[1] += value
            elif event.key == 275:                                          # Right
                if pygame.key.get_mods() & KMOD_ALT:
                    self.groups[self.selectedGroup].rectangle[2] += value
                else:
                    self.groups[self.selectedGroup].rectangle[0] += value
                    self.groups[self.selectedGroup].rectangle[2] += value
                    for item in self.groups[self.selectedGroup].items:
                        item.position[0] += value
            elif event.key == 276:                                          # Left
                if pygame.key.get_mods() & KMOD_ALT:
                    self.groups[self.selectedGroup].rectangle[2] -= value
                else:
                    self.groups[self.selectedGroup].rectangle[0] -= value
                    self.groups[self.selectedGroup].rectangle[2] -= value
                    for item in self.groups[self.selectedGroup].items:
                        item.position[0] -= value
            elif event.key == 119:                                          # W
                self.groups[self.selectedGroup].items[self.selectedItem].position[1] -= value
            elif event.key == 97:                                           # A
                self.groups[self.selectedGroup].items[self.selectedItem].position[0] -= value
            elif event.key == 115:                                          # S
                self.groups[self.selectedGroup].items[self.selectedItem].position[1] += value
            elif event.key == 100:                                          # D
                self.groups[self.selectedGroup].items[self.selectedItem].position[0] += value
            elif event.key == 127:                                          # Delete
                self.groups[self.selectedGroup].items.pop(self.selectedItem)





                

# --------------------------------------------------------------------------------------------------------

    def _handleKeys(self, event):
        """ Registers which keys are held down and which are released, and acts accordingly. Must get event from main program! """
        if event.type == pygame.KEYDOWN:
            if event.key == 32:                                 # SPACE
                self.displayed = False
            elif event.key == 9:                                # TAB
                self._moveSelection()
            elif event.key == 273:                              # Up
                print 'UP was pressed and handled by Menuclass!!'
            elif event.key == 274:                              # Down
                print 'DOWN was pressed and handled by Menuclass!!'
            elif event.key == 275:                              # Right
                print 'RIGHT was pressed and handled by Menuclass!!'
            elif event.key == 276:                              # Left
                print 'LEFT was pressed and handled by Menuclass!!'


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
                if nr == self.selectedItem:
                    self._showText(item.text, item.position, (255, 0, 0), item.backColor)
                else:
                    self._showText(item.text, item.position, item.textColor, item.backColor)


















class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height, displayNodes=1, displayEdges=1, displayFaces=1, displayObj= 1):
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
        self.nodeColor = (0,255,255)
        self.edgeColor = (255,255,255)
        self.faceColor = (0,0,255)
        self.nodeRadius = 2
        self.running = False
        self._keysHeld = []
        self.displayNodes = displayNodes
        self.displayEdges = displayEdges
        self.displayFaces = displayFaces
        self.displayObjectList = displayObj
        self.optMenu = MenuClass(self.screen, width, height)


    def _getKeys(self):
        """ Registers which keys are held down and which are released, then moves view accordingly """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.optMenu.displayed:
                    self.optMenu._handleKeysSetup(event)
                else:
                    if event.key == pygame.K_ESCAPE:                    # Escape
                        self.running = False
                    elif event.key == 9:                                # TAB
                        self._menu.moveSelection(0)
                    elif event.key == 32:                               # SPACE
                        self.optMenu._switch()
                    else:
                        self._keysHeld.append(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self._keysHeld:
                    self._keysHeld.remove(event.key)




        
    def _display(self):
        """ Draw the wireframes on the screen. """
        self.screen.fill(self.background)
        if self.optMenu.displayed:
            self.optMenu._display()
        pygame.display.flip()


    def run(self):
        """ Start the main loop from outside """
        print('Program running... press <ESC> to quit')
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


if __name__ == '__main__':
    parent = ProjectionViewer(1200, 800, 1, 1, 1, 1)



  
    parent.run()



# --- Status ---------------------------------------------------------------------------------------------------------------------------------------------

#   - Menu til at loade/save?


















