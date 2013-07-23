import sys, pygame, time, random
from pygame.locals import *

pygame.init()

class Cell(object):
	def __init__(self, position):
		if not len(position)==2 or type(position[0]) != int or type(position[1]) != int:
			raise Exception("Invalid position "+str(position))
		elif position[0] > size[0]-20 or position[1] > size[1] - 20:
			raise Exception("Position out of bounds: "+str(position))
		else:
			self.position = position

		self.alive = False
		self.next_step = False
		self.neighbors = []

	def rect(self):
		return pygame.Rect((self.position[0]*20, self.position[1]*20), (20, 20))
	def color(self):
		return white if self.alive else black
	def live_neighbors(self):
		return len([neighbor for neighbor in self.neighbors if neighbor.alive])
	def duplicate(self):
		new = Cell(self.position)
		new.alive = self.alive
		new.neighbors = self.neighbors
		return new
	def die(self):
		self.alive = False
	def live(self):
		self.alive = True
	def plan_next_step(self):
		self.next_step = self.alive
		if self.live_neighbors() < 2 or self.live_neighbors() > 3:
			self.next_step = False
		if (not self.alive) and self.live_neighbors() == 3:
			self.next_step = True
		# self.next_step = bool(random.getrandbits(2)>1)



size = width, height = 320,240
speed = [1, 1]
black = 0, 0, 0
green = 0, 255, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

# print pygame.image.tostring(ball, "RGB")

#Initialize cells
cells = []
for top in range(0, height/20):
	cellrow = []
	for left in range(0, width/20):
		cell = Cell((left, top))
		cell.alive = bool(random.randrange(100)>75) #randomize livelihood
		cellrow.append(cell)
	cells.append(cellrow)
#Add neighbors
for v in range(0, len(cells)-1):
	for h in range(0, len(cells[v])-1):
		cell = cells[v][h]
		if v > 0: 
			cell.neighbors.append(cells[v-1][h])
			if h > 0: cell.neighbors.append(cells[v-1][h-1])
			if h < len(cells[v])-1: cell.neighbors.append(cells[v-1][h+1])
		if v < len(cells)-1: 
			cell.neighbors.append(cells[v+1][h])
			if h > 0: cell.neighbors.append(cells[v+1][h-1])
			if h < len(cells[v])-1: cell.neighbors.append(cells[v+1][h+1])
		if h > 0: cell.neighbors.append(cells[v][h-1])
		if h < len(cells[v])-1: cell.neighbors.append(cells[v][h+1])


while True:
	for event in pygame.event.get():
		if event.type==pygame.QUIT: sys.exit()

	screen.fill(black)

	#Draw cells
	for row in cells:
		for cell in row:
			# print "pygame.draw.rect("+str(type(screen))+", "+str(type(cell.rect()))+", "+str(type(cell.color()))+")"
			# print "Drawing cell "+str(cell.color())
			pygame.draw.rect(screen, cell.color(), cell.rect())

	#Plan next steps
	for row in cells:
		for cell in row:
			cell.plan_next_step()
 	
 	#Execute next steps
 	for row in cells:
 		for cell in row:
 			cell.alive = cell.next_step

	pygame.display.flip()
	time.sleep(.5)