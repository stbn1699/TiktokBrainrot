import pygame
import sys
import math
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur, hauteur = 800, 800
ecran = pygame.display.set_mode((largeur, hauteur))

# Horloge pour contrôler le taux de rafraîchissement
horloge = pygame.time.Clock()

# Paramètres du jeu
centre = (largeur // 2, hauteur // 2)  # Centre du cercle
rayon = 300  # Rayon du cercle
rayonBalle = 8  # Rayon des balles
gravite = 0.3  # Force de gravité appliquée aux balles
imagesParSeconde = 60  # Nombre d'images par seconde
positionHorizontaleBalle = 50  # Position initiale horizontale de la balle
positionVerticaleBalle = 150  # Position initiale verticale de la balle
vitesseTrou = 2  # Vitesse de rotation du trou
angleApparition = 180  # Angle de la zone d'apparition des nouvelles balles (en degrés)
sonCollision = pygame.mixer.Sound("collision.wav")  # Son joué lors d'une collision
plageAngleSortie = (250, 290)  # Plage angulaire du trou (en degrés)

# Couleurs utilisées dans le jeu
blanc = (255, 255, 255)  # Couleur blanche
noir = (0, 0, 0)  # Couleur noire

# Initialisation de la police pour afficher le compteur de balles
police = pygame.font.Font(None, 36)  # Taille de la police : 36


# Fonction pour dessiner le compteur de balles à l'écran
def dessinerCompteurBalles(surface, compteur):
    texte = police.render(f"Balls : {compteur}", True, blanc)  # Texte affiché
    surface.blit(texte, (largeur - 150, 20))  # Position du texte en haut à droite


# Classe représentant une balle
class Balle:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x  # Position horizontale de la balle
        self.y = y  # Position verticale de la balle
        self.vx = vx  # Vitesse horizontale de la balle
        self.vy = vy  # Vitesse verticale de la balle
        self.tombee = False  # Indique si la balle est tombée
        self.estSortie = False  # Indique si la balle est sortie par le trou
        # Couleur aléatoire attribuée à la balle
        self.couleur = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    # Met à jour la position et l'état de la balle
    def mettreAJour(self):
        # Applique la gravité à la vitesse verticale
        self.vy += gravite
        # Met à jour les positions en fonction des vitesses
        self.x += self.vx
        self.y += self.vy

        # Calcul de la distance entre la balle et le centre du cercle
        dx = self.x - centre[0]
        dy = self.y - centre[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Si la balle est trop loin du cercle, elle est supprimée
        if distance > 2 * rayon:
            return "supprimer"

        # Si la balle dépasse le bord du cercle
        if distance + rayonBalle > rayon:
            # Calcul de l'angle de la balle par rapport au centre
            angle = math.atan2(dy, dx)
            angleDeg = math.degrees(angle) % 360

            # Vérifie si la balle est dans la plage angulaire du trou
            if plageAngleSortie[0] <= angleDeg <= plageAngleSortie[1] or (
                    plageAngleSortie[0] > plageAngleSortie[1] and
                    (angleDeg >= plageAngleSortie[0] or angleDeg <= plageAngleSortie[1])
            ):
                # Si la balle passe par le trou, elle est marquée comme sortie
                if not self.estSortie:
                    self.estSortie = True
                    return "sortie"
            # Sinon, la balle rebondit sur le bord du cercle
            elif distance <= rayon + rayonBalle:
                sonCollision.play()  # Joue le son de collision
                # Calcul de la normale au point de collision
                normX = dx / distance
                normY = dy / distance
                # Calcul du produit scalaire pour ajuster les vitesses
                produitScalaire = self.vx * normX + self.vy * normY
                self.vx -= 2 * produitScalaire * normX
                self.vy -= 2 * produitScalaire * normY
                # Corrige le chevauchement entre la balle et le bord
                chevauchement = distance + rayonBalle - rayon
                self.x -= normX * chevauchement
                self.y -= normY * chevauchement
        return "ok"

    # Dessine la balle sur la surface donnée
    def dessiner(self, surface):
        pygame.draw.circle(surface, self.couleur, (int(self.x), int(self.y)), rayonBalle)


# Initialisation de la liste des balles avec une balle de départ
balles = [Balle(centre[0] + positionHorizontaleBalle, centre[0] - positionVerticaleBalle)]


# Fonction pour calculer les coordonnées d'apparition d'une balle à partir d'un angle
def obtenirPointApparition(angle):
    rad = math.radians(random.randint(0, angle) + -angle)  # Angle aléatoire dans la plage donnée
    x = centre[0] + rayon * math.cos(rad)  # Coordonnée X
    y = centre[1] + rayon * math.sin(rad)  # Coordonnée Y
    return x, y


# Boucle principale du jeu
while True:
    # Gestion des événements
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
            pygame.quit()
            sys.exit()

    # Remplit l'écran avec la couleur noire
    ecran.fill(noir)

    # Met à jour les angles du trou (rotation)
    plageAngleSortie = (
        (plageAngleSortie[0] + vitesseTrou) % 360,
        (plageAngleSortie[1] + vitesseTrou) % 360,
    )

    # Dessine le cercle avec le trou (arc de cercle non fermé)
    angle1 = math.radians(plageAngleSortie[0])
    angle2 = math.radians(plageAngleSortie[1])
    etapes = 100  # Nombre de segments pour dessiner le cercle
    for i in range(etapes):
        a1 = i / etapes * 2 * math.pi
        if plageAngleSortie[0] > plageAngleSortie[1]:
            if not (a1 >= angle1 or a1 <= angle2):
                x1 = centre[0] + rayon * math.cos(a1)
                y1 = centre[1] + rayon * math.sin(a1)
                x2 = centre[0] + rayon * math.cos(a1 + 2 * math.pi / etapes)
                y2 = centre[1] + rayon * math.sin(a1 + 2 * math.pi / etapes)
                pygame.draw.line(ecran, blanc, (x1, y1), (x2, y2), 2)
        else:
            if not (angle1 <= a1 <= angle2):
                x1 = centre[0] + rayon * math.cos(a1)
                y1 = centre[1] + rayon * math.sin(a1)
                x2 = centre[0] + rayon * math.cos(a1 + 2 * math.pi / etapes)
                y2 = centre[1] + rayon * math.sin(a1 + 2 * math.pi / etapes)
                pygame.draw.line(ecran, blanc, (x1, y1), (x2, y2), 2)

    # Gestion des balles
    nouvellesBalles = []  # Liste des nouvelles balles à ajouter
    ballesRestantes = []  # Liste des balles qui restent dans le jeu

    for balle in balles:
        resultat = balle.mettreAJour()  # Met à jour la balle
        if resultat == "ok" or resultat == "sortie":
            ballesRestantes.append(balle)  # Garde la balle si elle est encore active
            if resultat == "sortie":  # Si la balle sort par le trou
                spawnX, spawnY = obtenirPointApparition(angleApparition)
                for _ in range(2):  # Ajoute deux nouvelles balles
                    vx = random.uniform(-2, 2)  # Vitesse horizontale aléatoire
                    vy = random.uniform(-5, -2)  # Vitesse verticale aléatoire
                    nouvellesBalles.append(Balle(spawnX, spawnY, vx, vy))

    # Met à jour la liste des balles
    balles = ballesRestantes + nouvellesBalles

    # Dessine toutes les balles
    for balle in balles:
        balle.dessiner(ecran)

    # Affiche le compteur de balles
    dessinerCompteurBalles(ecran, len(balles))

    # Met à jour l'affichage
    pygame.display.flip()

    # Contrôle le taux de rafraîchissement
    horloge.tick(imagesParSeconde)