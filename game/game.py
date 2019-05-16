from random import randint
from math import sqrt
from controller import Controller
import pygame


class Obstacle:
    def __init__(self, surface_width, x=-1):
        if x == -1:
            self.x = randint(0, surface_width)
        else:
            self.x = x
        self.y = randint(-500, -50)
        if randint(1, 15) == 1:
            self.speed = 2
        else:
            self.speed = 1
        self.radius = randint(10, 50)


class Player:
    def __init__(self, default_x, default_y):
        self.x = default_x
        self.y = default_y
        self.radius = 10
        self.speed = 1

    def move_right(self, surface_width):
        if self.x < surface_width:
            self.x = self.x + self.speed

    def move_left(self):
        if self.x > 0:
            self.x = self.x - self.speed


def main():
    controller = Controller()

    running = True
    surface_width = 1000
    surface_height = 600
    player = Player(surface_width // 2, surface_height - 20)
    obstacles = []
    max_obstacles = 60
    score = 0
    best_score = 0

    pygame.init()

    pygame.display.set_caption("The best game ever")
    score_font = pygame.font.SysFont("arial", 32)
    fail_font = pygame.font.SysFont("arial", 100)

    surface = pygame.display.set_mode((surface_width, surface_height), pygame.HWSURFACE)
    player_avatar = pygame.image.load("player_avatar.png").convert()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     player.move_left()
        # if keys[pygame.K_RIGHT]:
        #     player.move_right(surface_width)
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_SPACE]:
            controller.display_charts()
        if keys[pygame.K_r]:
            score = 0
            obstacles = []
            player.x = surface_width // 2

        if score > best_score:
            best_score = score

        sorted_obstacles = \
            sorted(obstacles,
                   key=lambda o: sqrt((o.x - player.x) ** 2 + (o.y - player.y) ** 2) - o.radius - player.radius)

        if len(sorted_obstacles) == 0:
            fail = False
            first_closest_x_distance = 980
            second_closest_x_distance = 980

        elif len(sorted_obstacles) == 1:
            fail = sqrt((sorted_obstacles[0].x - player.x) ** 2 + (sorted_obstacles[0].y - player.y) ** 2) < \
                   sorted_obstacles[0].radius + player.radius

            if sorted_obstacles[0].x - player.x < 0:
                first_closest_x_distance = min(-1, (
                        sorted_obstacles[0].x - player.x + sorted_obstacles[0].radius + player.radius))
            else:
                first_closest_x_distance = max(0, (
                        sorted_obstacles[0].x - player.x - sorted_obstacles[0].radius - player.radius))

            second_closest_x_distance = first_closest_x_distance

        else:
            fail = sqrt((sorted_obstacles[0].x - player.x) ** 2 + (sorted_obstacles[0].y - player.y) ** 2) < \
                   sorted_obstacles[0].radius + player.radius

            if sorted_obstacles[0].x - player.x < 0:
                first_closest_x_distance = min(-1, (
                        sorted_obstacles[0].x - player.x + sorted_obstacles[0].radius + player.radius))
            else:
                first_closest_x_distance = max(0, (
                        sorted_obstacles[0].x - player.x - sorted_obstacles[0].radius - player.radius))

            if sorted_obstacles[1].x - player.x < 0:
                second_closest_x_distance = min(-1, (
                        sorted_obstacles[1].x - player.x + sorted_obstacles[1].radius + player.radius))
            else:
                second_closest_x_distance = max(0, (
                        sorted_obstacles[1].x - player.x - sorted_obstacles[1].radius - player.radius))

        if player.x < surface_width // 2:
            closest_wall_distance = -1 * player.x - 1
        else:
            closest_wall_distance = surface_width - player.x

        move = controller.calculate_move(first_closest_x_distance, second_closest_x_distance, closest_wall_distance)
        # print("First: " + str(first_closest_x_distance) + " Second: " + str(second_closest_x_distance) + " Wall: " + str(closest_wall_distance))
        # print(move)

        # if move < -0.6:
        #     player.move_left()
        #     player.move_left()
        # elif move > -0.6 and move < -0.2:
        #     player.move_left()
        # elif move > 0.2 and move < 0.6:
        #     player.move_right(surface_width)
        # elif move > 0.6:
        #     player.move_right(surface_width)
        #     player.move_right(surface_width)

        if move < -0.2:
            player.move_left()
        elif move > 0.2:
            player.move_right(surface_width)

        for i, obstacle in enumerate(obstacles):
            obstacle.y += obstacle.speed
            if obstacle.y > surface_height + obstacle.radius:
                obstacles.pop(i)
                score += 1

        if len(obstacles) < max_obstacles:
            if randint(1, 15) == 1:
                obstacles.append(Obstacle(surface_width))
            elif randint(1, 250) == 1:
                obstacles.append(Obstacle(surface_width, randint(0, 20)))
            elif randint(1, 250) == 1:
                obstacles.append(Obstacle(surface_width, randint(surface_width - 20, surface_width)))

        # render
        surface.fill((0, 0, 0))
        # pygame.draw.circle(surface, (255, 0, 0), (player.x, player.y), player.radius)
        surface.blit(player_avatar, (player.x - player.radius, player.y - player.radius))
        for obstacle in obstacles:
            pygame.draw.circle(surface, (0, 0, 255), (obstacle.x, obstacle.y), obstacle.radius)
        score_text = score_font.render("Score: " + str(score), False, (192, 192, 192))
        best_score_text = score_font.render("Best score: " + str(best_score), False, (192, 192, 192))
        surface.blit(score_text, (0, 0))
        surface.blit(best_score_text, (0, score_text.get_height()))

        if fail:
            score = 0
            fail_text = fail_font.render("Fail", False, (255, 0, 0))
            surface.blit(fail_text, (surface_width // 2 - fail_text.get_width() // 2,
                                     surface_height // 2 - fail_text.get_height() // 2))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
