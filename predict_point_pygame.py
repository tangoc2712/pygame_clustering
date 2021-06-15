import pygame
from random import randint
import math
from sklearn.cluster import KMeans

pygame.init()

# calculate distance from 2 points
def d(p1, p2):
	return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("Aloha")

running = True

clock = pygame.time.Clock()

# constant variable
BACKGROUND = (213, 114, 114)
GREY = (0,0,113)
BG_PANEL = (214,214,214)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

COLORS = [RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]
# font family
font_small = pygame.font.SysFont('sans', 15)
font = pygame.font.SysFont('sans', 40)
text_plus = font.render('+', True, WHITE)
text_minus = font.render('-', True, WHITE)
text_run = font.render("Run", True, WHITE)
text_random = font.render("Random", True, WHITE)
text_algorithm = font.render("Algorithm", True, WHITE)
text_reset = font.render("Reset", True, WHITE)

# variable
K = 0
error = 0
count = 0
t = 0
# 
points = []
clusters = []
labels = []

while running:	
	screen.fill(BACKGROUND)
	if count == 1: 
		t += 1
	# draw interface
	# draw panel

	pygame.draw.rect(screen, GREY, (50,50,700,500))
	pygame.draw.rect(screen, BG_PANEL, (55,55,690,490))
	
	# K button + 
	pygame.draw.rect(screen, GREY, (850,50,50,50))
	screen.blit(text_plus, (860,50))

	# K button -
	pygame.draw.rect(screen, GREY, (950,50,50,50))
	screen.blit(text_minus, (960,50))

	# K value
	text_k = font.render("K = " + str(K), True, GREY)
	screen.blit(text_k, (1050,50))

	# run button
	pygame.draw.rect(screen, GREY, (850,150,150,50))
	screen.blit(text_run, (900,150))

	# random button
	pygame.draw.rect(screen, GREY, (850,250,150,50))
	screen.blit(text_random, (850,250))

	# Reset button
	pygame.draw.rect(screen, GREY, (850,550,150,50))
	screen.blit(text_reset, (850,550))	

	# Algorithm button
	pygame.draw.rect(screen, GREY, (850,450,150,50))
	screen.blit(text_algorithm, (850,450))	

	mouse_x, mouse_y = pygame.mouse.get_pos()

	# draw mouse position
	if 55 <= mouse_x <= 755 and 55 <= mouse_y <= 555:
		text_point = font_small.render("("+ str(mouse_x-55) + "," + str(mouse_y-55) +")", True, GREY)
		screen.blit(text_point, (mouse_x+5, mouse_y+5)) 
	
	# draw point is checked in panel area
	for i in range(len(points)):
		pygame.draw.circle(screen, GREY, (points[i][0] + 50, points[i][1] + 50), 6)
		if labels == []:
			pygame.draw.circle(screen, WHITE, (points[i][0] + 50, points[i][1] + 50), 4)
		else:
			pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 50, points[i][1] + 50), 4)
	# draw clusters
	for i in range(len(clusters)):
		pygame.draw.circle(screen, COLORS[i], (clusters[i][0]+50, clusters[i][1]+50), 8)
	
	# draw error number
	error = 0
	if clusters != [] and labels != []:
		for i in range(len(points)):
			error += d(points[i], clusters[labels[i]])
	text_error = font.render("Error = " + str(int(error)), True, GREY)
	screen.blit(text_error, (850,350))

	# draw error
	
	if t < 120 and t > 0:
		text_bug = font.render("You should click random", True, GREY)
		screen.blit(text_bug, (350,250))
		
	

	# End draw interface
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Check point in panel area
			if 55 <= mouse_x <= 755 and 55 <= mouse_y <= 555:
				labels = []
				point = [mouse_x-50,mouse_y-50]
				if point not in points:
					points.append(point)
				print(points)

			# Change K button +
			if 850 < mouse_x < 900 and 50 < mouse_y < 100:
				if K < 8:
					K+=1
				print("Press K +")
				print(K)
			
			# Change K button -
			if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
				if K > 0:
					K -= 1
				print("Press K -")

			# Run button
			if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
				labels = []
				# check k = 0
	
				if clusters == []:
					count = 1
					continue

				# assign points to nearest cluster
				for p in points:
					distances_to_cluster = []
					for c in clusters:
						dis = d(p,c)
						distances_to_cluster.append(dis)

					min_dis = min(distances_to_cluster) # find min distance from all clusters for each point
					label = distances_to_cluster.index(min_dis) # labeling for this point
					labels.append(label) 
				
				# update clusters
				for i in range(K):
					sum_x = 0
					sum_y = 0
					count = 0
					for j in range(len(points)):
						if labels[j] == i:
							sum_x += points[j][0]
							sum_y += points[j][1]
							count +=1 
					if count != 0:
						new_cluster_x = sum_x / count
						new_cluster_y = sum_y / count
						clusters[i] = [new_cluster_x, new_cluster_y]
				print(labels)
				print("run pressed")

			# Random button
			if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
				labels = []
				clusters = []
				for i in range(K):
					random_point = [randint(0,680), randint(0,480)]
					clusters.append(random_point)
				print("random pressed")

			# Reset button
			if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
				K = 0
				error = 0
				points = []
				clusters = []
				labels = []
				print("reset button pressed")

			# Algorithm 
			if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
				kmeans = KMeans(n_clusters = K).fit(points)
				labels =  kmeans.predict(points)

				clusters = kmeans.cluster_centers_
				print("Algorithm button pressed")

	pygame.display.flip()
	clock.tick(60)
pygame.quit()
