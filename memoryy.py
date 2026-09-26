import pygame
import random

pygame.init()

WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

ROWS, COLS = 4, 4
CARD_SIZE = 120
MARGIN = 10

# Load images (img1.png to img8.png)
card_images = []
for i in range(1, 9):
    img = pygame.image.load(f"img{i}.png")
    img = pygame.transform.scale(img, (CARD_SIZE, CARD_SIZE))
    card_images.append(img)

# values 0-7, each twice, shuffled
values = list(range(8)) * 2
random.shuffle(values)

cards = []
index = 0
for row in range(ROWS):
    for col in range(COLS):
        x = col * (CARD_SIZE + MARGIN) + MARGIN
        y = row * (CARD_SIZE + MARGIN) + MARGIN
        card = {
            "rect": pygame.Rect(x, y, CARD_SIZE, CARD_SIZE),
            "value": values[index],
            "flipped": False,
            "matched": False
        }
        cards.append(card)
        index += 1

flipped_cards = []      # holds the 1 or 2 cards currently flipped, waiting to be checked
wait_timer = 0           # counts down after a wrong match, before flipping back

def draw_grid():
    screen.fill((30, 30, 30))
    for card in cards:
        if card["flipped"] or card["matched"]:
            img = card_images[card["value"]]
            screen.blit(img, card["rect"])
        else:
            pygame.draw.rect(screen, (70, 130, 180), card["rect"], border_radius=8)

    if all(card["matched"] for card in cards):
        font = pygame.font.SysFont(None, 80)
        text = font.render("You Won!", True, (255, 215, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and wait_timer == 0:
            mouse_pos = event.pos
            for card in cards:
                if card["rect"].collidepoint(mouse_pos) and not card["flipped"] and not card["matched"] and len(flipped_cards) < 2:
                    card["flipped"] = True
                    flipped_cards.append(card)

    if len(flipped_cards) == 2:
        wait_timer += 1
        if wait_timer > 30:  # short pause so you can see both cards
            card1, card2 = flipped_cards
            if card1["value"] == card2["value"]:
                card1["matched"] = True
                card2["matched"] = True
            else:
                card1["flipped"] = False
                card2["flipped"] = False
            flipped_cards = []
            wait_timer = 0
            

    draw_grid()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
