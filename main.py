from classes import *

blorbList: list[blorbs] = []
frame: int = 0

while(True):
    delta = timer.tick(frameRate) / 10       #Sets the framerate
    frame += 1

    screen.fill([205, 225, 255])

    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    width:int = screen.get_width()
    height:int = screen.get_height()

    if frame % (secsPerSpawn*frameRate) == 0:
        blorbList.append(blorbs((xSpawn, yPercentSpawn*height)))



    for blorb in blorbList:
        blorb.stateChange(blorbList)

    for blorb in blorbList:
        blorb.calcForces(blorbList)

    for blorb in blorbList:
        blorb.update(height, blorbList, delta)

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