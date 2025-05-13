import pygame
import sys
import math
import random

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Paramètres
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 300
BALL_RADIUS = 8
GRAVITY = 0.3
FPS = 60
positionHorizontaleBalle = 20
positionVerticaleBalle = 150
EXIT_ANGLE_RANGE = (250, 290)  # Le "trou" en bas du cercle (en degrés)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Balle
class Ball:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

        # Vérifie collision avec le bord du cercle
        dx = self.x - CENTER[0]
        dy = self.y - CENTER[1]
        dist = math.sqrt(dx**2 + dy**2)

        if dist + BALL_RADIUS > RADIUS:
            angle = math.atan2(dy, dx)
            if not (EXIT_ANGLE_RANGE[0] <= math.degrees(angle) % 360 <= EXIT_ANGLE_RANGE[1]):
                # Rebond
                norm_x = dx / dist
                norm_y = dy / dist
                dot = self.vx * norm_x + self.vy * norm_y
                self.vx -= 2 * dot * norm_x
                self.vy -= 2 * dot * norm_y
                # Repositionne juste à l'intérieur
                overlap = dist + BALL_RADIUS - RADIUS
                self.x -= norm_x * overlap
                self.y -= norm_y * overlap
            else:
                return "exit"
        return "ok"

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), BALL_RADIUS)

# Initialisation des balles
balls = [Ball(CENTER[0] + positionHorizontaleBalle, CENTER[0] - positionVerticaleBalle)]

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Cercle + trou
    pygame.draw.circle(screen, WHITE, CENTER, RADIUS, 2)
    # Dessine le trou comme une ligne absente
    angle1 = math.radians(EXIT_ANGLE_RANGE[0])
    angle2 = math.radians(EXIT_ANGLE_RANGE[1])
    steps = 100
    for i in range(steps):
        a1 = i / steps * 2 * math.pi
        if not (angle1 <= a1 <= angle2):
            x1 = CENTER[0] + RADIUS * math.cos(a1)
            y1 = CENTER[1] + RADIUS * math.sin(a1)
            x2 = CENTER[0] + RADIUS * math.cos(a1 + 2 * math.pi / steps)
            y2 = CENTER[1] + RADIUS * math.sin(a1 + 2 * math.pi / steps)
            pygame.draw.line(screen, WHITE, (x1, y1), (x2, y2), 2)

    new_balls = []
    remaining_balls = []

    for ball in balls:
        result = ball.update()
        if result == "ok":
            remaining_balls.append(ball)
        else:
            # Ajoute deux nouvelles balles aléatoires
            for _ in range(2):
                vx = random.uniform(-2, 2)
                vy = random.uniform(-5, -2)
                new_balls.append(Ball(ball.x, ball.y, vx, vy))

    balls = remaining_balls + new_balls

    # Affiche les balles
    for ball in balls:
        ball.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
