from vectorMath import *

state = Literal["grabbing", "walking", "falling"]

class blorbs:
    def __init__ (self, initialPosition: vector) -> None:
        self.sate: state = "falling"
        self.velocity: vector = (0, 0)
        self.forces: vector = (0,0)
        self.position: vector = initialPosition
        self.attatchments: dict[(blorbs | sideBlocks), float] = {} #{blorb or anchor: angle(Right is 0, counterclockwise is positive)}
        self.lastHit: int = 0

    def update (self, blorbList: list, frameRateCorection: float) -> None:
        self.velocity = add(self.velocity, scaleBy(self.forces, frameRateCorection/mass))
        self.position = add(scaleBy(self.velocity, frameRateCorection), self.position)
        if self.position[1] > height:
            blorbList.remove(self)

    def calcForces (self, blorbList: list, blockList: list) -> None:
        self.forces = (0, gravity*mass)

        for blorb in blorbList:
            if blorb != self:
                distance: float = distanceBetween(self.position, blorb.position)
                if distance < blorbRadius*2:
                    self.forces = add(self.forces, scaleBy(subtract(self.position, blorb.position), colideForce))
                    self.lastHit = pygame.time.get_ticks()

        for block in blockList:
            if ((self.position[0] < block.position [0] and block.side == "left") or (self.position[0] > block.position [0] and block.side == "right")) and self.position[1] >= block.position[1]-blorbRadius:
                self.forces = add(self.forces, (0, -1*gravity*mass))
                self.position = (self.position[0], block.position[1]-blorbRadius)
                self.velocity = (self.velocity[0], 0)
                self.lastHit = pygame.time.get_ticks()

        if self.sate == "walking":
            self.forces = add(self.forces, ((speedGoal - self.velocity[0])*horizontalAccPercent,0))
        elif self.sate == "grabbing":
            pass

    def stateChange (self, blorbList: list, deltaMils: float) -> None:
        if self.sate == "falling" and self.lastHit + deltaMils >= pygame.time.get_ticks():
            self.sate = "walking"
        elif self.sate == "walking":
            if self.lastHit + deltaMils*framesUntilFalling < pygame.time.get_ticks():
                self.sate = "falling"

    def draw(self) -> None:
        color = [0, 0, 60]
        if self.sate == "walking":
            color = [0, 60, 0]
        elif self.sate == "grabbing":
            color = [60, 0, 0]
        pygame.draw.circle(screen, color, self.position, blorbRadius)

    def grip(self, blorbList: list, blockList: list) -> None:
        for blorb in blorbList:
            if blorb != self and distanceBetween(blorb.position, self.position) <= (blorbRadius*2) + atatchGap and blorb.state=="gripping":
                self.attatchments[blorb] = angleOf(subtract(blorb.position, self.position))
                blorb.attatchments[self] = angleOf(subtract(self.position, blorb.position))
        for block in blockList:
            if distanceBetween(block.position, self.position) < blorbRadius + atatchGap:
                self.attatchments[block] = angleOf(subtract(block.position, self.position))
                block.attatchments[self] = angleOf(subtract(self.position, block.position))
        self.sate = "grabbing"

    def ungrip(self) -> None:
        for attatchment in self.attatchments:
            attatchment.attatchments.pop(self)
        self.attatchments = {}
        self.sate = "falling"

class sideBlocks:
    def __init__ (self, side: Literal["left", "right"]) -> None:
        if side == "left":
            self.position: vector = (blockWidth, (1-blockHeightPercent)*height)
        else:
            self.position: vector = (width - blockWidth, (1-blockHeightPercent)*height)
        self.attatchments: dict[(blorbs | sideBlocks), float] = {} #{blorb: angle(Right is 0, counterclockwise is positive)}
        self.side = side
    def draw (self) -> None:
        if self.side == "left":
            pygame.draw.rect(screen, blockColor, pygame.Rect(0, self.position[1], blockWidth, (blockHeightPercent)*height))
        else:
            pygame.draw.rect(screen, blockColor, pygame.Rect(self.position[0], self.position[1], blockWidth, (blockHeightPercent)*height))