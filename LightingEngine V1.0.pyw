import pygame
import math

pygame.init()


S_WIDTH = 800
S_HEIGHT = 600
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
clock = pygame.time.Clock()

def clamp255(n):
    return min(max(0, n), 255)


def generate_light(radius):
    diameter = radius * 2
    lightmap = pygame.Surface((diameter, diameter))

    for i in range(radius, max(0, radius - 255), -2):
        v = clamp255(radius - i)
        pygame.draw.circle(lightmap, (v,v,v), (radius, radius), i)

    '''
    for x in range(diameter):
        for y in range(diameter):
            value = clamp255(radius - math.dist((x,y), (radius,radius)))
            pygame.draw.rect(lightmap, (value, value//2, value//5), (x,y,1,1))
    '''

    return lightmap


def main():

    radius = 200
    light = generate_light(radius)

    lightmap = pygame.Surface((S_WIDTH, S_HEIGHT))
    img = pygame.image.load("Assets/brick.png").convert()
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    radius += 10
                    light = generate_light(radius)
                elif event.key == pygame.K_DOWN:
                    radius -= 10
                    radius = max(10, radius)
                    light = generate_light(radius)

        mPos = pygame.mouse.get_pos()


        screen.fill((0,0,0))


        for x in range(7):
            for y in range(5):
                screen.blit(img, (128*x, 128*y))

        lightmap.fill((0,0,0))
        lightmap.blit(light, (mPos[0] - radius, mPos[1] - radius), special_flags = pygame.BLEND_ADD)
        
        screen.blit(lightmap, (0,0), special_flags = pygame.BLEND_MULT)


        pygame.display.set_caption(f"Lighting V1  |  {clock.tick()}ms")
        pygame.display.update()

main()
