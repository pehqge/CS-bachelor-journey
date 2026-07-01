import pygame

#button class
class Botao():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.__image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.__rect = self.__image.get_rect()
		self.__rect.topleft = (x, y)
		self.__clicked = False

	def draw(self, surface):
		#draw button on screen
		surface.blit(self.__image, (self.__rect.x, self.__rect.y))


	def clicado(self):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.__rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.__clicked == False:
				self.__clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.__clicked = False

		return action
