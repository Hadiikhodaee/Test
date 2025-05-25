from configs import *

sprite_width, sprite_height = 98, 48
WIN_WIDTH, WIN_HEIGHT = sprite_width+500, sprite_height+400

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Dark knight animations")

main_frame_image = pygame.image.load(os.path.join(current_path, "assets", "dark_knigt.png"))
main_frame_image.set_colorkey((0, 255, 255))

animations = {
    "idle":(4, []),
    "long_attack":(6, []),
    "short_attack":(4, []),
    "dash":(5, []),
    "run":(12, []),
    "rest":(3, [])
    }

def get_each_frame(save_images=False, path=""):
    executed = False
    idx = 0
    for animation in animations:
        for col in range(animations[animation][0]):
            if col > 5:
                col -= 6
                if not executed:
                    idx += 1
                    executed = not executed
            frame = main_frame_image.subsurface(Rect(col*sprite_width, idx*sprite_height, sprite_width, sprite_height)).convert_alpha()
            frame = pygame.transform.scale(frame, (sprite_width*4, sprite_height*4))
            if save_images:
                pygame.image.save(frame, f"{path}{idx}{col}img.png")
            animations[animation][1].append(frame)
        idx += 1

def main():
    get_each_frame()
    frame_idx = 0
    time_frame = 1
    time_gap = 5
    starting_time_gap = time_gap
    starting_time_frame = time_frame
    animation_type_id = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key in (K_d, K_RIGHT):
                    animation_type_id = (animation_type_id + 1) % len(list(animations.keys()))
                    frame_idx = 0
                    time_frame = starting_time_frame
                elif event.key in (K_a, K_LEFT):
                    animation_type_id = (animation_type_id - 1) % len(list(animations.keys()))
                    frame_idx = 0
                    time_frame = starting_time_frame
                if event.key == K_q:
                    running = False

        WIN.fill((0, 0, 0))

        time_frame -= 0.1
        if frame_idx == list(animations.values())[animation_type_id][0]-1:
            time_frame += 5
            time_gap -= 0.1
            if time_gap <= 0:
               frame_idx = 0
               time_gap = starting_time_gap
               time_frame = starting_time_frame
        if time_frame <= 0:
            frame_idx += 1
            time_frame = starting_time_frame
        frame = animations[list(animations.keys())[animation_type_id]][1][frame_idx % len(animations[list(animations.keys())[animation_type_id]][1])]
        frame_rect = frame.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        WIN.blit(frame, frame_rect)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

main()