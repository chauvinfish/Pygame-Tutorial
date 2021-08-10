import pygame
screen = pygame.display.set_mode([480,640])


class SimpleGameRes:
    def __init__(self):
        resPath = ".//res//hockey2.png"
        resImg = pygame.image.load(resPath).convert_alpha()
        print(type(resImg))
        self.hockeyR = resImg.subsurface(pygame.Rect(0,0,40,40))
        self.hockeyB = resImg.subsurface(pygame.Rect(40,0,40,40))
        self.theBall = resImg.subsurface(pygame.Rect(80,0,40,40))
        self.buttonA = resImg.subsurface(pygame.Rect(120,0,40,40))
        self.buttonB = resImg.subsurface(pygame.Rect(160,0,40,40))


class Circle:
    def __init__(self,*args,**kwargs):
        pass

class ButtonOnRelease:
    def __init__(self,clickArea):
        assert hasattr(clickArea,'collidepoint'), 'clickArea must have the method "collidepoint"'
        self.clickArea = clickArea
        self.alreadyButtonDown = False
        self.listeningType = [pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP]

    def effect_on_release(self,event):
        pass

    def listening(self,event:pygame.event.EventType) -> None:
        if event.type in self.listeningType:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.clickArea.collidepoint(event.pos):
                    self.alreadyButtonDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.alreadyButtonDown == True:
                    self.alreadyButtonDown = False
                    if self.clickArea.collidepoint(event.pos):
                        self.effect_on_release(event)


class ButtonDraggable:
    def __init__(self, clickArea):
        assert hasattr(clickArea,'collidepoint'), 'clickArea must have the method "collidepoint"'
        self.clickArea = clickArea
        self.dragging = False

    def effect_when_dragging(self,event):
        pass

    def listening(self,event):
        if event.type==pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type==pygame.MOUSEBUTTONDOWN and self.clickArea.collidepoint(event.pos):
            self.dragging = True
            print("dragging")
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.effect_when_dragging(event)
            print(event)


class HockeyButton(ButtonDraggable):
    def __init__(self,img, clickArea,pos=(0,0)):
        super().__init__(clickArea)
        self.img = img
        self.pos = pos

    def effect_when_dragging(self,event):
        self.pos = event.pos

    def draw(self,targetSurface,pos=None):
        if pos == None:
            pos = self.pos
        targetSurface.blit(self.img,pos)


class ActivableImageButton(ButtonOnRelease):
    def __init__(self,img,clickArea,activedImg,pos=(0,0)):
        super().__init__(clickArea)
        self.img = img
        self.activedImg = activedImg
        self.actived = False
        self.pos = pos

    def effect_on_release(self,event):
        if self.actived:
            self.actived = False
        else:
            self.actived = True

    def draw(self,targetSurface,pos=None):
        if pos==None:
            pos = self.pos
        if self.actived:
            targetSurface.blit(self.activedImg,pos)
        else:
            targetSurface.blit(self.img,pos)


res = SimpleGameRes()
controlModeButton = ActivableImageButton(res.buttonA,pygame.Rect(0,0,40,40),res.buttonB)
hockeyR = HockeyButton(res.hockeyR,pygame.Rect(0,0,40,40),[200,40])
hockeyB = HockeyButton(res.hockeyB,pygame.Rect(0,0,40,40),[200,570])

while(1):
    screen.fill((200,255,255))

    screen.blit(res.theBall,[200,280])
    hockeyR.draw(screen)
    hockeyB.draw(screen)
    controlModeButton.draw(screen,(0,0))
    for event in pygame.event.get():
        #print(event)
        controlModeButton.listening(event)
        hockeyR.listening(event)
        hockeyB.listening(event)
    pygame.display.update()

