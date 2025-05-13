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
positionHorizontaleBalle = 50
positionVerticaleBalle = 150
vitesseTrou = 2
angleDApparition = 180 # Angle de la zone d'apparition des nouvelles balles (en degrés)
EXIT_ANGLE_RANGE = (250, 290)  # Le "trou" en bas du cercle (en degrés)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialisation de la police
font = pygame.font.Font(None, 36)  # Taille de la police : 36

def draw_ball_counter(surface, count):
    text = font.render(f"Balls: {count}", True, WHITE)
    surface.blit(text, (WIDTH - 150, 20))  # Position en haut à droite

# Balle
class Ball:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.falling = False
        # couleur random a chaque apparition
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Couleur aléatoire

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
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

# Initialisation des balles
balls = [Ball(CENTER[0] + positionHorizontaleBalle, CENTER[0] - positionVerticaleBalle)]

# Fonction pour calculer les coordonnées à partir d'un angle
def get_spawn_point(angle):
    rad = math.radians(random.randint(0, angle) + -angle) # Angle aléatoire dans la zone d'apparition entre 0 et angle, mois l'angle pour que ce soit au centre en haut
    x = CENTER[0] + RADIUS * math.cos(rad)
    y = CENTER[1] + RADIUS * math.sin(rad)
    return x, y

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Met à jour les angles du trou
    EXIT_ANGLE_RANGE = (
        (EXIT_ANGLE_RANGE[0] + vitesseTrou) % 360,
        (EXIT_ANGLE_RANGE[1] + vitesseTrou) % 360,
    )

    # Cercle + trou (juste un arc de cercle qui n'est pas terminé)
    angle1 = math.radians(EXIT_ANGLE_RANGE[0])
    angle2 = math.radians(EXIT_ANGLE_RANGE[1])
    steps = 100
    for i in range(steps):
        a1 = i / steps * 2 * math.pi
        # Cas où le trou traverse 0°, sinon il disparait
        if EXIT_ANGLE_RANGE[0] > EXIT_ANGLE_RANGE[1]:
            if not (a1 >= angle1 or a1 <= angle2):
                x1 = CENTER[0] + RADIUS * math.cos(a1)
                y1 = CENTER[1] + RADIUS * math.sin(a1)
                x2 = CENTER[0] + RADIUS * math.cos(a1 + 2 * math.pi / steps)
                y2 = CENTER[1] + RADIUS * math.sin(a1 + 2 * math.pi / steps)
                pygame.draw.line(screen, WHITE, (x1, y1), (x2, y2), 2)
        else:
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
            # Coordonnées fixes pour l'apparition des nouvelles balles
            spawn_x, spawn_y = get_spawn_point(angleDApparition)
            for _ in range(2):
                vx = random.uniform(-2, 2)
                vy = random.uniform(-5, -2)
                new_balls.append(Ball(spawn_x, spawn_y, vx, vy))

    balls = remaining_balls + new_balls

    # Affiche les balles
    for ball in balls:
        ball.draw(screen)

    draw_ball_counter(screen, len(balls))
    pygame.display.flip()
    clock.tick(FPS)
