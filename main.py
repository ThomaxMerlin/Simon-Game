import random
import sys
from typing import Literal, Callable

import pygame

from settings import COLORS, FLASH_COLORS, FPS, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))    
        
        pygame.display.set_caption("Simon Game")

        # sounds
        self.sounds = [pygame.mixer.Sound("./sounds/beep1.ogg"), pygame.mixer.Sound("./sounds/beep2.ogg"), pygame.mixer.Sound("./sounds/beep3.ogg"), pygame.mixer.Sound("./sounds/beep4.ogg")]

        self.sounds[2].set_volume(30) 
        self.sounds[3].set_volume(30) 
        self.gameover_sound = pygame.mixer.Sound("./sounds/gameover.mp3")

        self.font = pygame.font.Font("./font/Pixeltype.ttf", 50)
        self.clock = pygame.time.Clock()
        self.running = True

        self.game_state: Literal["running", "paused"] = "running"
       
        self.waiting_for_input = False

        self.colors: list[str] = ["red", "green", "blue", "yellow"]
        self.color_rects: dict[str,pygame.Rect] = {}
        self.pattern: list[str] = []

        self.score = 0
        self.high_scores: list[int] = [0]

        # next color index the player needs to click 
        self.next_color = 0

    def add_to_pattern(self):
        color = random.choice(self.colors)

        self.pattern.append(color)


    def handle_button_click(self, rect: pygame.Rect, action: Callable[[], None]):
        if rect.collidepoint(pygame.mouse.get_pos()):
            hand_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
            pygame.mouse.set_cursor(hand_cursor)
            if pygame.mouse.get_pressed()[0]:
                action()
        else:
            normal_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.mouse.set_cursor(normal_cursor)

    def animate_flash(self, color: str, animation_speed = 50):
        color_idx = self.colors.index(color)
        rect = self.color_rects[color]

        r,g,b = FLASH_COLORS[color_idx] 

        orig_surf = self.screen.copy()
        flash_surf = pygame.Surface((rect.width, rect.height))

        self.sounds[color_idx].play()

        for start, stop, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, stop, animation_speed * step):
                self.screen.blit(orig_surf, (0, 0))
                flash_surf.fill((r, g, b, alpha))
                self.screen.blit(flash_surf, (rect.x, rect.y))

                pygame.display.update()
        self.screen.blit(orig_surf, (0, 0))

    def check_input(self, clicked_color: str | None):
        if clicked_color and self.pattern[self.next_color] == clicked_color:
            self.animate_flash(clicked_color)
            self.next_color += 1
            if (self.next_color == len(self.pattern)):
                self.score += 1
                self.next_color = 0
                self.waiting_for_input = False
        elif clicked_color and self.pattern[self.next_color] != clicked_color: 
            self.game_over() 
        
    def get_rect_clicked(self, mouse_pos: tuple[int, int]):
        for color, rect in self.color_rects.items():
            if rect.collidepoint(mouse_pos):
                return color

        return None

    def draw_rects(self):
        width, height = 250, 250

        side_padding = 75 / 2
        rect_per_row = (WINDOW_WIDTH - (2 * side_padding)) // width

        gap = 25

        for i in range(len(self.colors)):
            rect_surface = pygame.Surface((width, height))
            rect_surface.fill(COLORS[i])

            x = (i % rect_per_row) * width + side_padding + ((i % rect_per_row) * gap)
            y = (i // rect_per_row) * height + ((i // rect_per_row) * gap) + 3 * gap

            rect = rect_surface.get_rect(topleft=(x, y))
            
            self.screen.blit(rect_surface, rect)

            self.color_rects[self.colors[i]] = rect

    def display_score(self):
        score_surf = self.font.render(f"Score: {self.score}", False, (255, 255, 255))
        score_rect = score_surf.get_rect(bottomright=(WINDOW_WIDTH - 50, WINDOW_HEIGHT - 150))

        highest_score_surf = self.font.render(f"Highest Score: {self.high_scores[0]}", False, (255, 255, 255))
        highest_score_rect = highest_score_surf.get_rect(bottomright=(WINDOW_WIDTH - 50, WINDOW_HEIGHT - 100))

        see_top_ten_surf = self.font.render("See top ten highest scores", False, (255, 255, 255))
        see_top_ten_rect = see_top_ten_surf.get_rect(bottomright=(WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50))
        
        self.screen.blit(score_surf, score_rect)
        self.screen.blit(highest_score_surf, highest_score_rect)
        self.screen.blit(see_top_ten_surf, see_top_ten_rect)
      
        def pause_game():
            self.game_state = "paused"

        self.handle_button_click(see_top_ten_rect, pause_game)
        if see_top_ten_rect.collidepoint(pygame.mouse.get_pos()):
            hand_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
            pygame.mouse.set_cursor(hand_cursor)
            if pygame.mouse.get_pressed()[0]:
                self.game_state = "paused"
        else:
            normal_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.mouse.set_cursor(normal_cursor)
    
    def diplay_top_10_high_scores(self):
        title_surf = self.font.render("Top 10 High Scores", False, (255, 255, 200))
        title_rect = title_surf.get_rect(midtop=(WINDOW_WIDTH / 2, 25))

        self.screen.blit(title_surf, title_rect)
        for index, score in enumerate(self.high_scores):
            number_surf = self.font.render(f"{index + 1}.", False, (255, 255, 255))
            number_rect = number_surf.get_rect(topleft=(75, 75 + (index * 75)))

            score_surf = self.font.render(f"{score}", False, (255, 255, 255))
            score_rect = score_surf.get_rect(topleft=(120, 75 + (index * 75)))

            self.screen.blit(score_surf, score_rect)
            self.screen.blit(number_surf, number_rect)

        back_btn_surf = self.font.render("Go Back", False, (255, 255, 200))
        back_btn_rect =back_btn_surf.get_rect(bottomleft=(50, WINDOW_HEIGHT - 25))

        def show_game():
            self.game_state = "running"

        self.handle_button_click(back_btn_rect, show_game)

        self.screen.blit(back_btn_surf, back_btn_rect)

    def update_highscore(self):
        if self.score not in self.high_scores:
            self.high_scores.append(self.score) 
            self.high_scores.sort(reverse=True)

            if (len(self.high_scores) > 10):
                self.high_scores.pop()

    def game_over(self):
        self.gameover_sound.play()
        self.waiting_for_input = False
        self.update_highscore()
        self.score = 0
        self.next_color = 0
        self.pattern.clear()
        pygame.time.wait(1000)


    def run(self):
        while self.running:
            clicked_button: str | None = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked_button = self.get_rect_clicked(event.pos)

            # bg
            self.screen.fill("black")
           
            match self.game_state:
                case "running":
                    self.draw_rects()
                    self.display_score()

                    if not self.waiting_for_input:
                        self.add_to_pattern()
                        pygame.display.update()
                        pygame.time.wait(1000)

                        for color in self.pattern:
                            self.animate_flash(color)
                            pygame.display.update()
                            pygame.time.wait(600)
                        
                        self.waiting_for_input = True
                    else:
                        self.check_input(clicked_button)
                case "paused":
                   self.diplay_top_10_high_scores()

            pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

