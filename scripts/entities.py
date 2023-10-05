import pygame


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        # reset collisions
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        # calculate movement
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )

        # apply x axis movement
        self.pos[0] += frame_movement[0]

        # correct for x axis collisions
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # if moving right into a collideable tile
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                # if moving left into a collideable tile
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = entity_rect.x

        # apply y axis movement
        self.pos[1] += frame_movement[1]

        # correct for y axis collisions
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # if moving down into a collideable tile
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                # if moving up into a collideable tile
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.pos[1] = entity_rect.y

        # apply gravity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # reset gravity based on collisions
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

    def render(self, surf):
        surf.blit(self.game.assets["player"], self.pos)
