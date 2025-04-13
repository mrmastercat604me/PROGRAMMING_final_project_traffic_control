import pygame
def draw_text(text:str,font,color:str,surface:'pygame.Surface',x:int,y:int,centerSurface=None,width:int=None,height:int=None):
		textobj = font.render(text, 1, color)
		textrect = textobj.get_rect()
		if width and height:
				textrect.width ,textrect.height = width, height
		if centerSurface:
			textrect.center = centerSurface.center
		else:
			textrect.topleft = (x,y)
		surface.blit(textobj,textrect)

def percent_of(percent:float,total:float) -> float:
		return (percent * total) / 100