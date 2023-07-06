import pygame
import NormalMap

pygame.init()


S_WIDTH = 800
S_HEIGHT = 600
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
clock = pygame.time.Clock()


print(pygame.display.set_gamma(5.0, 0.1, 1.0))

def clamp255(n):
    return min(max(0, n), 255)

def dist(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    x *= x
    y *= y
    return (x + y) ** 0.5


def generate_light(radius):
    diameter = radius * 2
    lightmap = pygame.Surface((diameter, diameter))

    for i in range(radius, max(0, radius - 255), -2):
        v = clamp255(radius - i)
        pygame.draw.circle(lightmap, (v,v,v), (radius, radius), i)

    return lightmap

def main():

    # Normal Map
    normal_img = pygame.image.load("Assets/Normal_MapTest.png").convert()
    mask_img = pygame.image.load("Assets/Normal_MapTest_Mask.png").convert()

    normal_img = pygame.transform.scale(normal_img, (256, 256))
    mask_img = pygame.transform.scale(mask_img, (256, 256))

    normalTest = NormalMap.NormalMap(normal_img, mask_img)

    normal_pos = (128, 128)


    # Light Settings
    light_normal_img1 = pygame.image.load("Assets/Light_Normal_Above.png").convert()
    light_normal_img2 = pygame.image.load("Assets/Light_Normal_GroundLevel.png").convert()
    light_mask_img = pygame.image.load("Assets/Light_Mask_Above.png").convert()

    light_normal1 = NormalMap.NormalMap(light_normal_img1, light_mask_img)
    light_normal2 = NormalMap.NormalMap(light_normal_img2, light_mask_img)

    light_normal = light_normal1

    light_radius = 128
    light_texture = generate_light(light_radius)
    
    light_normal1.multiply(light_texture)
    light_normal2.multiply(light_texture)

    light_normal1_preview = pygame.transform.scale(light_normal_img1, (128, 128))
    light_normal2_preview = pygame.transform.scale(light_normal_img2, (128, 128))


    # Lighting
    lightmap = pygame.Surface((S_WIDTH, S_HEIGHT))
    normal_render = pygame.Surface((S_WIDTH, S_HEIGHT))

    global_lighting_center = None
    
    while 1:
        mPos = pygame.mouse.get_pos()
        center = (mPos[0] - 128, mPos[1] - 128)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if light_normal == light_normal1:
                        light_normal = light_normal2
                    else:
                        light_normal = light_normal1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    global_lighting_center = mPos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    global_lighting_center = None

        

        # Reset Everything
        screen.fill((0,0,0))
        lightmap.fill((0,0,0))

        screen.blit(normalTest.mask, normal_pos)
        screen.blit(normalTest.mask, (512, 128))

        if global_lighting_center:
            global_lighting_normal = (min(max(mPos[0] - global_lighting_center[0], -128), 127) + 128,
                                      min(max(mPos[1] - global_lighting_center[1], -128), 127) + 128)
            global_lighting_end = (global_lighting_center[0] + global_lighting_normal[0] - 128,
                                   global_lighting_center[1] + global_lighting_normal[1] - 128)

            #length = dist(global_lighting_center, global_lighting_end)
            #if length > 0:
            #    global_lighting_normal = (global_lighting_normal[0] / length * 64,
            #                              global_lighting_normal[1] / length * 64)

            #normal_color = global_lighting_normal[0]
            normal_color = min(max(global_lighting_normal[0] * 2 - 255, 0), 255)
            normal_render.fill((normal_color, normal_color, normal_color))
            normal_render.blit(normalTest.left, normal_pos, special_flags=pygame.BLEND_MULT)
            lightmap.blit(normal_render, (0,0), special_flags=pygame.BLEND_ADD)

            #normal_color = 255 - global_lighting_normal[0]
            normal_color = min(max(255 - (global_lighting_normal[0] * 2), 0), 255)
            normal_render.fill((normal_color, normal_color, normal_color))
            normal_render.blit(normalTest.right, normal_pos, special_flags=pygame.BLEND_MULT)
            lightmap.blit(normal_render, (0,0), special_flags=pygame.BLEND_ADD)

            #normal_color = global_lighting_normal[1]
            normal_color = min(max(global_lighting_normal[1] * 2 - 255, 0), 255)
            normal_render.fill((normal_color, normal_color, normal_color))
            normal_render.blit(normalTest.up, normal_pos, special_flags=pygame.BLEND_MULT)
            lightmap.blit(normal_render, (0,0), special_flags=pygame.BLEND_ADD)

            #normal_color = 255 - global_lighting_normal[1]
            normal_color = min(max(255 - (global_lighting_normal[1] * 2), 0), 255)
            normal_render.fill((normal_color, normal_color, normal_color))
            normal_render.blit(normalTest.down, normal_pos, special_flags=pygame.BLEND_MULT)
            lightmap.blit(normal_render, (0,0), special_flags=pygame.BLEND_ADD)

            screen.blit(lightmap, (0,0), special_flags=pygame.BLEND_MULT)

            # Draw the normal color
            #z_asthetic_offset = abs(sum(global_lighting_normal) // 2)
            #screen.fill((global_lighting_normal[0] + 128, global_lighting_normal[1] + 128, 255 - z_asthetic_offset))
            
            pygame.draw.line(screen, 0xff0000, global_lighting_center, global_lighting_end, 2)

        '''
        # Draw the bottom normals
        normal_render.fill((0,0,0))
        normal_render.blit(light_normal.mask, center)
        normal_render.blit(normalTest.down, normal_pos, special_flags=pygame.BLEND_MULT)
        #normalTest.draw_down(normal_render, (256, 128))
        normal_render.blit(light_normal.up, center, special_flags=pygame.BLEND_MULT)
        lightmap.blit(normal_render, (0,0), special_flags=pygame.BLEND_ADD)

        # Draw the top normals
        normal_render.fill((0,0,0))
        normal_render.blit(light_normal.mask, center)
        normal_render.blit(normalTest.up, normal_pos, special_flags=pygame.BLEND_MULT)
        #normalTest.draw_up(normal_render, (256, 128))
        normal_render.blit(light_normal.down, center, special_flags=pygame.BLEND_MULT)
        lightmap.blit(normal_render, (0,0), special_flags=pygame.BLEND_ADD)

        # Draw the left normals
        normal_render.fill((0,0,0))
        normal_render.blit(light_normal.mask, center)
        normal_render.blit(normalTest.left, normal_pos, special_flags=pygame.BLEND_MULT)
        #normalTest.draw_left(normal_render, (256, 128))
        normal_render.blit(light_normal.right, center, special_flags=pygame.BLEND_MULT)
        lightmap.blit(normal_render, (0,0), special_flags=pygame.BLEND_ADD)

        # Draw the right normals
        normal_render.fill((0,0,0))
        normal_render.blit(light_normal.mask, center)
        normal_render.blit(normalTest.right, normal_pos, special_flags=pygame.BLEND_MULT)
        #normalTest.draw_right(normal_render, (256, 128))
        normal_render.blit(light_normal.left, center, special_flags=pygame.BLEND_MULT)
        lightmap.blit(normal_render, (0,0), special_flags=pygame.BLEND_ADD)

        # Draw the normal map
        screen.blit(normalTest.mask, normal_pos)
        screen.blit(normalTest.mask, (512, 128))
        #normalTest.draw_down(screen, (512, 128))
        #normalTest.draw_down(screen, normal_pos)

        # Draw 
        #lightmap.blit(down_light, (mPos[0] - light_radius, mPos[1] - light_radius), special_flags=pygame.BLEND_ADD)


        screen.blit(lightmap, (0,0), special_flags=pygame.BLEND_MULT)

        #normalTest.draw_up(   screen, (0,0)    )
        #normalTest.draw_down( screen, (0,256)  )
        #normalTest.draw_left( screen, (256,0)  )
        #normalTest.draw_right(screen, (256,256))
        

        if light_normal == light_normal1:
            screen.blit(light_normal1_preview, (0,0))
        else:
            screen.blit(light_normal2_preview, (0,0))
        '''

        milliseconds = max(clock.tick(),1)
        pygame.display.set_caption(f"Normal Mapping V1 | {milliseconds}ms | {1000//milliseconds}fps")
        pygame.display.update()

main()
