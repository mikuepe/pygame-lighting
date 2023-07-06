import pygame

class NormalMap:
    def __init__(self, normal_map, normal_mask):
        self.__Normal_Img = normal_map
        self.__Mask_Img   = normal_mask

        self.__size = self.__Normal_Img.get_size()

        self.__img_up    = pygame.Surface(self.__size)
        self.__img_down  = pygame.Surface(self.__size)
        self.__img_left  = pygame.Surface(self.__size)
        self.__img_right = pygame.Surface(self.__size)

        self.__generate_normals()

    def __generate_normals(self):
        normal_array = pygame.PixelArray(self.__Normal_Img)

        array_up    = pygame.PixelArray(self.__img_up   )
        array_down  = pygame.PixelArray(self.__img_down )
        array_left  = pygame.PixelArray(self.__img_left )
        array_right = pygame.PixelArray(self.__img_right)

        print(normal_array[192,50])
        
        for x in range(self.__size[0]):
            for y in range(self.__size[1]):
                rawColor = normal_array[x,y]
                
                b = rawColor & 255
                g = rawColor >> 8 & 255
                r = rawColor >> 16 & 255

                array_right[x,y] = (r,r,r)
                r = 255 - r
                array_left[x,y]  = (r,r,r)

                array_up[x,y]    = (g,g,g)
                g = 255 - g
                array_down[x,y]  = (g,g,g)
                '''
                if r < 127:
                    r = 255 - r
                    array_left[x,y]  = (r,r,r)
                else:
                    array_right[x,y] = (r,r,r)

                if g < 127:
                    g = 255 - g
                    array_down[x,y]  = (g,g,g)
                else:
                    array_up[x,y]    = (g,g,g)
                '''

        normal_array.close()
        array_up.close()
        array_down.close()
        array_left.close()
        array_right.close()

        self.__img_up.blit(self.__Mask_Img, (0,0), special_flags=pygame.BLEND_MULT)
        self.__img_down.blit(self.__Mask_Img, (0,0), special_flags=pygame.BLEND_MULT)
        self.__img_left.blit(self.__Mask_Img, (0,0), special_flags=pygame.BLEND_MULT)
        self.__img_right.blit(self.__Mask_Img, (0,0), special_flags=pygame.BLEND_MULT)

    def render_directional(self, x, y):
        temp = pygame.Surface(self.__size)
        temp.fill((255,255,255))

        temp.blit(self.__img_up,   (0,0), special_flags=pygame.BLEND_ADD)
        temp.blit(self.__img_left, (0,0), special_flags=pygame.BLEND_ADD)

        return temp

    def multiply(self, surface):
        temp = pygame.transform.scale(surface, self.__size)
        self.__img_up.blit(temp, (0,0), special_flags=pygame.BLEND_MULT)
        self.__img_down.blit(temp, (0,0), special_flags=pygame.BLEND_MULT)
        self.__img_left.blit(temp, (0,0), special_flags=pygame.BLEND_MULT)
        self.__img_right.blit(temp, (0,0), special_flags=pygame.BLEND_MULT)

    def draw_up(self, surface, pos):
        surface.blit(self.__img_up, pos)

    def draw_down(self, surface, pos):
        surface.blit(self.__img_down, pos)

    def draw_left(self, surface, pos):
        surface.blit(self.__img_left, pos)

    def draw_right(self, surface, pos):
        surface.blit(self.__img_right, pos)

    @property
    def up(self):
        return self.__img_up

    @property
    def down(self):
        return self.__img_down

    @property
    def left(self):
        return self.__img_left

    @property
    def right(self):
        return self.__img_right

    @property
    def mask(self):
        return self.__Mask_Img
