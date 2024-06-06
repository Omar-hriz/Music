import pygame
from pymongo import MongoClient

# Initialisation de Pygame
pygame.init()

# Définition de quelques couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Définition de la taille de la fenêtre
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Configuration de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connexion")

# Initialisation de la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Music']
collection = db['Users']

# Font
font = pygame.font.Font(None, 32)

# Fonction pour afficher le texte à l'écran
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Fonction principale pour le programme
def main():
    clock = pygame.time.Clock()
    username = ""

    while True:
        screen.fill(WHITE)
        draw_text("Entrez votre nom d'utilisateur:", font, BLACK, screen, SCREEN_WIDTH // 2, 100)
        draw_text(username, font, BLACK, screen, SCREEN_WIDTH // 2, 150)

        # Dessine les boutons "Login" et "Créer un compte" avec de l'espace entre eux
        pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 150, 200, 100, 40))
        draw_text("Login", font, BLACK, screen, SCREEN_WIDTH // 2 - 100, 220)
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 + 50, 200, 150, 40))
        draw_text("Créer un compte", font, BLACK, screen, SCREEN_WIDTH // 2 + 125, 220)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifie si le clic est sur le bouton "Login"
                if SCREEN_WIDTH // 2 - 150 <= event.pos[0] <= SCREEN_WIDTH // 2 - 50 and 200 <= event.pos[1] <= 240:
                    login(username)
                # Vérifie si le clic est sur le bouton "Créer un compte"
                elif SCREEN_WIDTH // 2 + 50 <= event.pos[0] <= SCREEN_WIDTH // 2 + 200 and 200 <= event.pos[1] <= 240:
                    create_account(username)

        pygame.display.flip()
        clock.tick(30)

# Fonction pour afficher la nouvelle interface une fois l'utilisateur trouvé
def show_user_interface(username, preferences, potential_matches):
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption(f"Bienvenue {username}")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Vos musiques préférées:", font, BLACK, screen, 300, 50)
        # Afficher les préférences musicales
        for i, pref in enumerate(preferences):
            draw_text(f"{i+1}. {pref}", font, BLACK, screen, 300, 100 + i * 30)
        
        draw_text("Utilisateurs avec qui vous pourriez matcher:", font, BLACK, screen, 300, 250)
        # Afficher les utilisateurs avec qui l'utilisateur pourrait matcher
        for i, match in enumerate(potential_matches):
            draw_text(f"{i+1}. {match}", font, BLACK, screen, 300, 300 + i * 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)

# Fonction pour connecter l'utilisateur
def login(username):
    user_data = collection.find_one({"username": username})
    if user_data:
        preferences_ids = user_data.get('preferences', [])
        preferences_titles = []
        for song_id in preferences_ids:
            song_data = db['Songs'].find_one({"id": song_id})
            if song_data:
                preferences_titles.append(song_data['name'])
        potential_matches = [user['username'] for user in collection.find({"username": {"$ne": username}})]
        show_user_interface(username, preferences_titles, potential_matches)
    else:
        message = "Utilisateur non trouvé."
        draw_text(message, font, BLACK, screen, SCREEN_WIDTH // 2, 300)

# Fonction pour créer un nouveau compte utilisateur
def create_account(username):
    user_data = collection.find_one({"username": username})
    if user_data:
        message = "Ce nom d'utilisateur existe déjà."
    else:
        new_user = {"username": username, "preferences": []}
        collection.insert_one(new_user)
        message = "Compte créé avec succès!"
    draw_text(message, font, BLACK, screen, SCREEN_WIDTH // 2, 300)


if __name__ == "__main__":
    main()
