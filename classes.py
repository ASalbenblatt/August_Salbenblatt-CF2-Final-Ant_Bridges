from vectorMath import *

state = Literal["grabbing", "walking", "falling"]

class blorbs:
    def __init__ (self, initialPosition: vector) -> None:
        self.state: state = "falling"
        self.velocity: vector = (0, 0)
        self.forces: vector = (0,0)
        self.position: vector = initialPosition
        self.attatchments: dict[(blorbs | sideBlocks), float] = {} #{blorb or anchor: angle(Right is 0, counterclockwise is positive)}
        self.lastHit: int = 0

    def update (self, blorbList: list, frameRateCorection: float) -> None:
        self.velocity = add(self.velocity, scaleBy(self.forces, frameRateCorection/mass))
        self.position = add(scaleBy(self.velocity, frameRateCorection), self.position)
        if self.position[1] > height + blorbRadius+5 or self.position[0] > width + blorbRadius+5 or self.position[0] < 0 - (blorbRadius+5):
            blorbList.remove(self)
            for blorb in blorbList:
                if blorb.attatchments.__contains__(self):
                    blorb.attatchments.pop(self)

    def calcForces (self, blorbList: list, blockList: list) -> None:
        self.forces = (0, gravity*mass)

        if self.state == "grabbing":
            for attatchment in self.attatchments:
                pointToAttatchment: vector = subtract(attatchment.position, self.position)
                normalPointToAttatchment: vector = normalPoint(self.position, attatchment.position)
                distance: float = distanceBetween(self.position, attatchment.position)

                dampingForce: vector = scaleBy(normalPointToAttatchment, dot(normalPointToAttatchment, subtract(attatchment.velocity, self.velocity)) * dampingConstant)
                if attatchment.__class__ == blorbs:
                    springForce: vector = scaleBy(normalPointToAttatchment, springConstant*(distance-(2*blorbRadius))*(abs(distance-(2*blorbRadius))**(springExponent-1)))
                else: 
                    springForce: vector = scaleBy(normalPointToAttatchment, springConstant*(distance-(blorbRadius))*(abs(distance-(blorbRadius))**(springExponent-1)))

                self.forces = add(self.forces, add(dampingForce, springForce))

                pygame.draw.line(screen, [11, 13, 18], self.position, add(self.position, pointToAttatchment), width=20)
                # pygame.draw.line(screen, [0, 255, 0], self.position, add(self.position, scaleBy((-1*pointToAttatchment[1], pointToAttatchment[0]), angleForce*angleBetween*10)), width=10)
                
                
        
        for blorb in blorbList:
            if blorb != self and not (blorb.state == "grabbing" and self.state == "grabbing"):
                distance: float = distanceBetween(self.position, blorb.position)
                if distance < blorbRadius*2:
                    self.position = add(self.position, scaleBy(normalPoint(blorb.position, self.position), (blorbRadius*2) -distance))
                    if isclose(angleOf(projectOnto(self.velocity, normalPoint(blorb.position, self.position))), angleOf(normalPoint(self.position, blorb.position))):
                        self.velocity = subtract(self.velocity, projectOnto(self.velocity, normalPoint(blorb.position, self.position)))
                    if self.state != "grabbing" or blorb.state != "grabbing":
                        self.lastHit = pygame.time.get_ticks()

        for block in blockList:
            if ((self.position[0] < block.position [0] and block.side == "left") or (self.position[0] > block.position [0] and block.side == "right")or (self.position[0] > block.position [0] and self.position[0] < width/2 and block.side == "middleLeft")or (self.position[0] < block.position [0] and self.position[0] > width/2 and block.side == "middleRight")) and self.position[1] >= block.position[1]-blorbRadius:
                self.forces = add(self.forces, (0, -1*gravity*mass))
                self.position = (self.position[0], block.position[1]-blorbRadius)
                self.velocity = (self.velocity[0], 0)
                self.lastHit = pygame.time.get_ticks()
            if self.position[1] > block.position [1] and (block.side == "left" or (block.side == "middleRight" and self.position[0] > width/2)) and self.position[0] <= block.position[0] + blorbRadius:
                self.position = (block.position[0] + blorbRadius, self.position[1])
                self.velocity = (0, self.velocity[1])
                self.lastHit = pygame.time.get_ticks()
            if self.position[1] > block.position [1] and (block.side == "right" or (block.side == "middleLeft" and self.position[0] < width/2)) and self.position[0] >= block.position[0] - blorbRadius:
                self.position = (block.position[0] - blorbRadius, self.position[1])
                self.velocity = (0, self.velocity[1])
                self.lastHit = pygame.time.get_ticks()
                if self.state == "walking":
                    self.grip(blorbList, blockList)
            if distanceBetween(self.position, block.position) < blorbRadius and (block.side == "left" or block.side == "middleRight"):
                self.position = add(block.position, scaleBy(normalPoint(block.position, self.position), blorbRadius))
                if angleOf(self.velocity) < pi and angleOf(self.velocity) > pi/2:
                    self.velocity = add(self.velocity, scaleBy(projectOnto(self.velocity, normalPoint(block.position, self.position)), -1))
                self.lastHit = pygame.time.get_ticks()
                
            if distanceBetween(self.position, block.position) < blorbRadius and (block.side == "right" or block.side == "middleLeft"):
                self.position = add(block.position, scaleBy(normalPoint(block.position, self.position), blorbRadius))
                if angleOf(self.velocity) < pi/2 and angleOf(self.velocity) > 0:
                    self.velocity = add(self.velocity, scaleBy(projectOnto(self.velocity, normalPoint(block.position, self.position)), -1))
                self.lastHit = pygame.time.get_ticks()

        if self.state == "walking":
            self.forces = add(self.forces, ((speedGoal - self.velocity[0])*horizontalAccPercent,0))

    def stateChange (self, blorbList: list, blockList: list, deltaMils: float, furthestForward: float) -> None:
        if self.state == "grabbing" and self.position[1] < (1-blockHeightPercent)*height:
            self.ungrip()
        
        if self.state == "grabbing":
            toRemove = []
            for attatchment in self.attatchments:
                if distanceBetween(attatchment.position, self.position) >= (blorbRadius*2) + releaseGap:
                    toRemove.append(attatchment)
                    #attatchment.attatchments.pop(self)
            for remove in toRemove:
                self.attatchments.pop(remove)
            for blorb in blorbList:
                distance: float = distanceBetween(self.position, blorb.position)
                if distance < blorbRadius*2 and blorb.state == "grabbing" and not self.attatchments.__contains__(blorb) and blorb != self:
                    self.attatchments[blorb] = angleOf(subtract(blorb.position, self.position))
            for block in blockList:
                distance: float = distanceBetween(self.position, block.position)
                if distance < blorbRadius * 1.5 and not self.attatchments.__contains__(block):
                    self.attatchments[block] = angleOf(subtract(block.position, self.position))
                    block.attatchments[self] = angleOf(subtract(self.position, block.position))

        if self.state == "walking" and self.velocity[0] <= 0 and self.position[1] > (1-blockHeightPercent)*height:
            self.grip(blorbList, blockList)
        if self.position[0] >= furthestForward + frontGapTillGrip and self.state != "grabbing" and self.position[0] > sideBlockWidth+frontGapTillGrip and self.position[0] < width-(sideBlockWidth+frontGapTillGrip) and (self.position[0] > (width/2) + (middleBlockWidth/2) + frontGapTillGrip or self.position[0] < width/2) and (self.position[0] < (width/2) - ((middleBlockWidth/2) + frontGapTillGrip) or self.position[0] > width/2):
            self.grip(blorbList, blockList)
        if self.state == "falling" and self.position[1] > (1-blockHeightPercent)*height:
            for blorb in blorbList:
                if blorb != self and distanceBetween(blorb.position, self.position) <= (blorbRadius*2) + atatchGap and blorb.state=="grabbing":
                    self.grip(blorbList, blockList)
                    break
        if self.state == "grabbing" and len(self.attatchments) == 0:
            self.ungrip()
        if self.state == "falling" and self.lastHit + deltaMils >= pygame.time.get_ticks():
            self.state = "walking"
        elif self.state == "walking":
            if self.lastHit + secsUntilFalling*1000 < pygame.time.get_ticks() and self.velocity[1] > 0:
                self.state = "falling"
        
        

    def draw(self) -> None:
        if self.state == "walking":
            screen.blit(walkingImage, (self.position[0]-50, self.position[1]-50))
        elif self.state == "grabbing":
            screen.blit(grabbingImage, (self.position[0]-50, self.position[1]-50))
        else:
            screen.blit(fallingImage, (self.position[0]-50, self.position[1]-50))

    def grip(self, blorbList: list, blockList: list) -> None:
        for blorb in blorbList:
            if blorb != self and distanceBetween(blorb.position, self.position) <= (blorbRadius*2) + atatchGap and blorb.state=="grabbing":
                self.attatchments[blorb] = angleOf(subtract(blorb.position, self.position))
                blorb.attatchments[self] = angleOf(subtract(self.position, blorb.position))
        for block in blockList:
            if distanceBetween(block.position, self.position) < blorbRadius + atatchGap:
                self.attatchments[block] = angleOf(subtract(block.position, self.position))
                block.attatchments[self] = angleOf(subtract(self.position, block.position))
        self.state = "grabbing"

    def ungrip(self) -> None:
        for attatchment in self.attatchments:
            if attatchment.attatchments.__contains__(self):
                    attatchment.attatchments.pop(self)
        self.attatchments = {}
        self.state = "walking"

class sideBlocks:
    def __init__ (self, side: Literal["left", "right", "middleLeft", "middleRight"], y: float) -> None:
        if side == "left":
            self.position: vector = (sideBlockWidth, y)
        elif side == "right":
            self.position: vector = (width - sideBlockWidth, y)
        elif side == "middleLeft":
            self.position: vector = ((width/2) - (middleBlockWidth/2), y)
        else:
            self.position: vector = ((width/2) + (middleBlockWidth/2), y)
        self.attatchments: dict[(blorbs | sideBlocks), float] = {} #{blorb: angle(Right is 0, counterclockwise is positive)}
        self.side: Literal["left", "right", "middleLeft", "middleRight"] = side
        self.velocity: vector = (0, 0)
    def draw (self) -> None:
        if self.side == "left":
            pygame.draw.rect(screen, blockColor, pygame.Rect(0, self.position[1], sideBlockWidth, (blockHeightPercent)*height))
        elif self.side == "right":
            pygame.draw.rect(screen, blockColor, pygame.Rect(self.position[0], self.position[1], sideBlockWidth, (blockHeightPercent)*height))
        elif self.side == "middleLeft":
            pygame.draw.rect(screen, blockColor, pygame.Rect(self.position[0], self.position[1], middleBlockWidth/2, (blockHeightPercent)*height))
        elif self.side == "middleRight":
            pygame.draw.rect(screen, blockColor, pygame.Rect(width/2, self.position[1], middleBlockWidth/2, (blockHeightPercent)*height))
