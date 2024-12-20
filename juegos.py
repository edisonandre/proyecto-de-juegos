import pygame
import random
import cv2

pygame.init()

# Dimensiones de la pantalla
display_width = 800
display_height = 600

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
dark_blue = (0, 0, 139)
bright_yellow = (255, 255, 0)
green = (0, 255, 0)
red = (255, 0, 0)
light_brown = (210, 180, 140)  # Color café claro

# Configuración de la pantalla
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Juegos MultiFun')

# Cargar imagen de fondo y carro
background = pygame.image.load('fondo.png')
car_img = pygame.image.load('carro.png')

# Cargar y escalar imágenes de obstáculos
tree_img = pygame.image.load('arbol.png')
tree_img = pygame.transform.scale(tree_img, (75, 75))
house_img = pygame.image.load('casa.png')
house_img = pygame.transform.scale(house_img, (75, 75))
puddle_img = pygame.image.load('charco.png')
puddle_img = pygame.transform.scale(puddle_img, (75, 75))

# Cargar imagen de fondo para la pantalla de inicio
intro_background = pygame.image.load('intro_fondo.png')

# Cargar video para la pantalla de selección de juegos
selection_video = cv2.VideoCapture('selection_fondo.mp4')

# Reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# Variables del carro
car_width = car_img.get_width()
car_height = car_img.get_height()
car_x = (display_width * 0.45)
car_y = (display_height * 0.8)
car_speed = 3

# Variables de los obstáculos
obstacle_speed = 5
obstacle_width = 75
obstacle_height = 75

# Variables de puntuación y nivel
score = 0
level = 1

# Función para mostrar el mensaje de "Perdiste"
def message_display(text):
    small_text = pygame.font.Font('freesansbold.ttf', 50)
    text_surface = small_text.render(text, True, dark_blue)
    text_rect = text_surface.get_rect()
    text_rect.center = ((display_width / 2), (display_height / 2))
    game_display.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

# Función para mostrar la puntuación y el nivel con sombras
def show_score_level(score, level):
    font = pygame.font.Font('freesansbold.ttf', 25)
    score_text = font.render(f"Puntuación: {score}", True, bright_yellow)
    score_shadow = font.render(f"Puntuación: {score}", True, black)
    level_text = font.render(f"Nivel: {level}", True, bright_yellow)
    level_shadow = font.render(f"Nivel: {level}", True, black)
    
    # Dibujar sombras
    game_display.blit(score_shadow, (12, 12))
    game_display.blit(level_shadow, (12, 42))
    
    # Dibujar texto principal
    game_display.blit(score_text, (10, 10))
    game_display.blit(level_text, (10, 40))

# Función para detectar colisiones
def is_collision(car_x, car_y, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
    if car_y < obstacle_y + obstacle_height and car_y + car_height > obstacle_y:
        if car_x > obstacle_x and car_x < obstacle_x + obstacle_width or car_x + car_width > obstacle_x and car_x + car_width < obstacle_x + obstacle_width:
            return True
    return False

# Función para crear botones
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(game_display, ic, (x, y, w, h))

    small_text = pygame.font.Font('freesansbold.ttf', 20)
    text_surface = small_text.render(msg, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(text_surface, text_rect)

# Función para la pantalla de inicio
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.blit(intro_background, (0, 0))
        large_text = pygame.font.Font('freesansbold.ttf', 75)
        text_surface = large_text.render("Juegos MultiFun", True, bright_yellow)
        text_shadow = large_text.render("Juegos MultiFun", True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = ((display_width / 2), (display_height / 2))
        shadow_rect = text_shadow.get_rect()
        shadow_rect.center = (text_rect.center[0] + 2, text_rect.center[1] + 2)
        
        game_display.blit(text_shadow, shadow_rect)
        game_display.blit(text_surface, text_rect)

        button("INICIAR", 350, 450, 100, 50, green, bright_yellow, game_selection)

        pygame.display.update()
        clock.tick(15)

# Función para la pantalla de selección de juegos
def game_selection():
    selection = True
    while selection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        ret, frame = selection_video.read()
        if not ret:
            selection_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = selection_video.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (display_width, display_height))  # Redimensionar el video al tamaño de la pantalla
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        game_display.blit(frame, (0, 0))

        large_text = pygame.font.Font('freesansbold.ttf', 75)
        text_surface = large_text.render("Selecciona un Juego", True, bright_yellow)
        text_shadow = large_text.render("Selecciona un Juego", True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = ((display_width / 2), (display_height / 2 - 200))
        shadow_rect = text_shadow.get_rect()
        shadow_rect.center = (text_rect.center[0] + 2, text_rect.center[1] + 2)
        
        game_display.blit(text_shadow, shadow_rect)
        game_display.blit(text_surface, text_rect)

        # Botones en dos columnas, 3 en cada columna
        button("1 Juego", 150, 150, 200, 50, green, bright_yellow, game_loop)
        button("2 Juego", 150, 220, 200, 50, green, bright_yellow, snake_game)
        button("3 Juego", 150, 290, 200, 50, green, bright_yellow, another_game)
        button("4 Juego", 450, 150, 200, 50, green, bright_yellow, another_game)
        button("5 Juego", 450, 220, 200, 50, green, bright_yellow, another_game)
        button("6 Juego", 450, 290, 200, 50, green, bright_yellow, another_game)

        pygame.display.update()
        clock.tick(24)

# Bucle principal del juego de carros
def game_loop():
    global car_x, car_y, x_change, y_change, score, level, obstacle_speed

    # Iniciar la música del juego
    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.play(-1)

    car_x = (display_width * 0.45)
    car_y = (display_height * 0.8)
    x_change = 0
    y_change = 0
    score = 0
    level = 1
    obstacle_speed = 5

    # Lista de obstáculos
    obstacles = [
        {'img': tree_img, 'x': random.randrange(0, display_width - obstacle_width), 'y': -600},
        {'img': house_img, 'x': random.randrange(0, display_width - obstacle_width), 'y': -1600},
        {'img': puddle_img, 'x': random.randrange(0, display_width - obstacle_width), 'y': -2600}
    ]

    game_exit = False
    game_close = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -car_speed
                elif event.key == pygame.K_RIGHT:
                    x_change = car_speed
                elif event.key == pygame.K_UP:
                    y_change = -car_speed
                elif event.key == pygame.K_DOWN:
                    y_change = car_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        car_x += x_change
        car_y += y_change

        # Dibujar el fondo
        game_display.blit(background, (0, 0))

        # Dibujar los obstáculos
        for obstacle in obstacles:
            game_display.blit(obstacle['img'], (obstacle['x'], obstacle['y']))
            obstacle['y'] += obstacle_speed

            if obstacle['y'] > display_height:
                obstacle['y'] = -obstacle_height
                obstacle['x'] = random.randrange(0, display_width - obstacle_width)
                score += 1
                if score % 6 == 0:
                    level += 1
                    obstacle_speed += 1

            # Detectar colisiones con obstáculos
            if is_collision(car_x, car_y, obstacle['x'], obstacle['y'], obstacle_width, obstacle_height):
                game_close = True

        # Dibujar el carro
        game_display.blit(car_img, (car_x, car_y))

        # Dibujar el borde
        pygame.draw.rect(game_display, dark_blue, (0, 0, display_width, display_height), 5)

        # Mostrar la puntuación y el nivel
        show_score_level(score, level)

        # Detectar colisiones con los bordes
        if car_x < 0 or car_x > display_width - car_width or car_y < 0 or car_y > display_height - car_height:
            game_close = True

        pygame.display.update()
        clock.tick(60)  # Controlar la velocidad del juego

        while game_close:
            game_display.fill(light_brown)
            message("Perdiste", red)
            button("Reiniciar", display_width / 2 - 50, display_height / 2 + 50, 100, 50, green, bright_yellow, game_loop)
            button("Inicio", display_width / 2 - 50, display_height / 2 + 110, 100, 50, green, bright_yellow, game_intro)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_close = False

    pygame.quit()
    quit()

# Función para otro juego (ejemplo)
def another_game():
    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 75)
        text_surface = large_text.render("Otro Juego", True, bright_yellow)
        text_rect = text_surface.get_rect()
        text_rect.center = ((display_width / 2), (display_height / 2))
        game_display.blit(text_surface, text_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

# Función para el juego de la serpiente
def snake_game():
    snake_block = 30  # Tamaño más grande para la serpiente y la fruta
    snake_speed = 10  # Velocidad más lenta

    x1 = display_width / 2
    y1 = display_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(100, display_width - 100 - snake_block) / 30.0) * 30.0
    foody = round(random.randrange(100, display_height - 100 - snake_block) / 30.0) * 30.0

    game_over = False
    game_close = False

    # Cargar y redimensionar imágenes de la cabeza de la serpiente y la fruta
    snake_head_img = pygame.image.load('snake_head.png')
    snake_head_img = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
    fruit_img = pygame.image.load('fruit.png')
    fruit_img = pygame.transform.scale(fruit_img, (snake_block, snake_block))

    def our_snake(snake_block, snake_List):
        for x in snake_List[:-1]:
            pygame.draw.rect(game_display, green, [x[0], x[1], snake_block, snake_block])
        game_display.blit(snake_head_img, (snake_List[-1][0], snake_List[-1][1]))

    def message(msg, color):
        large_text = pygame.font.Font('freesansbold.ttf', 75)
        text_surface = large_text.render(msg, True, color)
        text_shadow = large_text.render(msg, True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = ((display_width / 2), (display_height / 2))
        shadow_rect = text_shadow.get_rect()
        shadow_rect.center = (text_rect.center[0] + 2, text_rect.center[1] + 2)
        game_display.blit(text_shadow, shadow_rect)
        game_display.blit(text_surface, text_rect)

    def show_score(score):
        font = pygame.font.SysFont(None, 35)
        value = font.render("Puntuación: " + str(score), True, black)
        game_display.blit(value, [display_width / 2 - 50, display_height - 50])

    while not game_over:

        while game_close == True:
            game_display.fill(light_brown)
            message("Perdiste", red)
            button("Reiniciar", display_width / 2 - 50, display_height / 2 + 50, 100, 50, green, bright_yellow, snake_game)
            game_display.blit(snake_head_img, (display_width / 2 - 75, display_height - 75))
            show_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        snake_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= display_width - 100 or x1 < 100 or y1 >= display_height - 100 or y1 < 100:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        game_display.fill(light_brown)
        pygame.draw.rect(game_display, black, [100, 100, display_width - 200, display_height - 200], 10)  # Dibujar el límite
        game_display.blit(fruit_img, (foodx, foody))
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_score(Length_of_snake - 1)

        pygame.display.update()

        # Detectar colisión con la fruta
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(100, display_width - 100 - snake_block) / 30.0) * 30.0
            foody = round(random.randrange(100, display_height - 100 - snake_block) / 30.0) * 30.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_intro()