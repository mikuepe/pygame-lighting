import pygame

if pygame.display.get_surface() == None:
    raise Exception("A pygame display must be set to use Lighting Tools")


def generate_light(radius):
    diameter = radius * 2
    lightmap = pygame.Surface((diameter, diameter))

    for i in range(radius, max(0, radius - 255), -2):
        v = clamp255(radius - i)
        pygame.draw.circle(lightmap, (v,v,v), (radius, radius), i)

    return lightmap
    

def light_normal(normal_buffer, normal1, normal2, pos1=(0,0), pos2=(0,0)):
    # Reset the normal buffer surface
    normal_buffer.fill(0)

    # Blit the first normal
    normal_buffer.blit(normal_positive, pos1)

    # Multiply by the second normal
    normal_buffer.blit(normal_negative, pos2, special_flags=pygame.BLEND_RGB_MULT)


def light_normal_offset(normal_buffer, normal1, normal2, buffer_pos, pos1=(0,0), pos2=(0,0)):
    # Reset the normal buffer surface
    normal_buffer.fill(0)

    # Blit the first normal
    normal_buffer.blit(normal_positive,
                       (pos1[0] - buffer_pos[0], pos1[1] - buffer_pos[1]))

    # Multiply by the second normal
    normal_buffer.blit(normal_negative,
                       (pos2[0] - buffer_pos[0], pos2[1] - buffer_pos[1]),
                       special_flags=pygame.BLEND_RGB_MULT)


def light_normal_mask(normal_buffer, normal1, normal2, mask, pos1=(0,0), pos2=(0,0)):
    # Reset the normal buffer surface
    normal_buffer.fill(0)

    # Blit the mask
    normal_buffer.blit(mask, pos2)

    # Multiply the mask by the normals
    normal_buffer.blit(normal_positive, pos1, special_flags=pygame.BLEND_RGB_MULT)
    normal_buffer.blit(normal_negative, pos2, special_flags=pygame.BLEND_RGB_MULT)


def light_normal_offset_mask(normal_buffer, normal1, normal2, mask, buffer_pos, pos1=(0,0), pos2=(0,0)):
    # Reset the normal buffer surface
    normal_buffer.fill(0)

    # Precalculate the second position for effecieincy
    p2 = (pos2[0] - buffer_pos[0], pos2[1] - buffer_pos[1])

    # Blit the mask
    normal_buffer.blit(mask, p2)

    # Multiply the mask by the normals
    normal_buffer.blit(normal_positive,
                       (pos1[0] - buffer_pos[0], pos1[1] - buffer_pos[1]),
                       special_flags=pygame.BLEND_RGB_MULT)
    normal_buffer.blit(normal_negative, p2,
                       special_flags=pygame.BLEND_RGB_MULT)
