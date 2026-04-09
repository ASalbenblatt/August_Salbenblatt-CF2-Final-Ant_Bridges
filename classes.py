from vectorMath import *

state = Literal["grabbing", "walking", "falling"]

class blorbs:
    def __init__ (self, initialPosition: vector) -> None:
        self.sate: state = "falling"
        self.velocity: vector = (0, 0)
        self.forces: vector = (0,0)
        self.position: vector = initialPosition
        self.attatchments: list[tuple[blorbs, float]] = [] #[blorb, angle(Right is 0, counterclockwise is positive)]

    def update (self, height: int, blorbList: list, frameRateCorection: float) -> None:
        self.velocity = add(self.velocity, scaleBy(self.forces, frameRateCorection/mass))
        self.position = add(scaleBy(self.velocity, frameRateCorection), self.position)
        if self.position[1] > height:
            blorbList.remove(self)

    def calcForces (self, blorbList: list) -> None:
        self.forces = (0, gravity*mass)

        for blorb in blorbList:
            if blorb != self:
                distance: float = distanceBetween(self.position, blorb.position)
                if distance < blorbRadius*2:
                    self.forces = add(self.forces, scaleBy(subtract(self.position, blorb.position), colideForce))

        if self.sate == "walking":
            pass

        
        if self.sate == "grabbing":
            pass

    def stateChange (self, blorbList: list) -> None:
        pass

    def draw(self) -> None:
        pygame.draw.circle(screen, [0, 0, 5], self.position, blorbRadius)