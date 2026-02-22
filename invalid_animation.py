import pygame

class InvalidMoveAnimation:
    def __init__(self, square, duration=400):
        self.square = square
        self.duration = duration  # milliseconds
        self.start_time = pygame.time.get_ticks()
        self.finished = False

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.finished = True

    def draw(self, screen, square_size):
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = elapsed / self.duration

        if progress > 1:
            progress = 1

        # Fade in then fade out (triangle wave)
        if progress <= 0.5:
            alpha = int(255 * (progress * 2))
        else:
            alpha = int(255 * (1 - (progress - 0.5) * 2))

        overlay = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, alpha))

        row = self.square // 8
        col = self.square % 8

        screen.blit(overlay, (col * square_size, row * square_size))
