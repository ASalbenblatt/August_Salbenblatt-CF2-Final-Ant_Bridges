from classes import *

blorbList: list[blorbs] = []
blockList: list[sideBlocks] = []

for n in range(nAttatchmentPoints):
    y = (1-(blockHeightPercent*((n+1)/nAttatchmentPoints)))*height
    blockList.append(sideBlocks("left", y))
    blockList.append(sideBlocks("right", y))
    blockList.append(sideBlocks("middleLeft", y))
    blockList.append(sideBlocks("middleRight", y))
frame: int = 0



while(True):
    delta = timer.tick(frameRate)
    frame += 1

    screen.fill([205, 225, 255])

    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    

    if frame % (secsPerSpawn*frameRate) == 0:
        blorbList.append(blorbs((xSpawn, (1-yPercentSpawn)*height)))

    furthestForward: float = sideBlockWidth
    for blorb in blorbList:
        if blorb.state == "grabbing" and blorb.position[0] > furthestForward:
            furthestForward = blorb.position[0]

    for blorb in blorbList:
        blorb.stateChange(blorbList, blockList, delta, furthestForward)

    for blorb in blorbList:
        blorb.calcForces(blorbList, blockList)

    for blorb in blorbList:
        blorb.update(blorbList, delta/10)

    for block in blockList:
        block.draw()
    for blorb in blorbList:
        blorb.draw()


    #-----------------Keep this section last-------------------------------------
    pygame.display.flip()  #updates the screen

    '''
    Keys:
    q - quit
    '''
    for event in events:

        
        #----------Keep this section last-------------------------
        if keys[pygame.K_q] or event.type == pygame.QUIT:
            pygame.display.quit()
            break
    else:
        continue  # Continue if the inner loop wasn't broken.
    break  # Inner loop was broken, break the outer.