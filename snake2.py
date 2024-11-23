import pygame
import random

# 初始化pygame
pygame.init()

# 设置屏幕尺寸
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 颜色定义
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# 初始设置
snake_size = 20  # 增大蛇的大小
snake_speed = 15

# 食物初始化
food_pos = [random.randrange(1, (SCREEN_WIDTH//snake_size)) * snake_size,
            random.randrange(1, (SCREEN_HEIGHT//snake_size)) * snake_size]
food_spawn = True

# 蛇初始化
snake_pos = [[random.randrange(1, (SCREEN_WIDTH//snake_size)) * snake_size,
              random.randrange(1, (SCREEN_HEIGHT//snake_size)) * snake_size]]
direction = 'RIGHT'

# 得分系统
score = 0
font = pygame.font.SysFont('Arial', 24)

# 游戏循环
running = True
clock = pygame.time.Clock()

# 增加游戏难度的变量
difficulty_level = 1
difficulty_increase_interval = 10  # 每10分增加难度
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)
while running:
    # 填充屏幕背景色为黑色
    window.fill(BLACK)

    # 绘制网格线
    for x in range(0, SCREEN_WIDTH, 20):  # 增大网格线间距
        pygame.draw.line(window, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, 20):
        pygame.draw.line(window, GRAY, (0, y), (SCREEN_WIDTH, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 检查键盘事件
        pygame.key.stop_text_input()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_SPACE:
                # 功能键逻辑
                pass
            elif event.key == pygame.K_w:
                snake_speed += 5
            elif event.key == pygame.K_s:
                if snake_speed > 5:  # 确保速度不会小于0
                    snake_speed -= 5
            else:
                # 处理其他按键事件
                print("Pressed an invalid key!")

    # 更新蛇的位置
    if direction == 'RIGHT':
        new_head = [snake_pos[0][0] + snake_size, snake_pos[0][1]]
    elif direction == 'LEFT':
        new_head = [snake_pos[0][0] - snake_size, snake_pos[0][1]]
    elif direction == 'UP':
        new_head = [snake_pos[0][0], snake_pos[0][1] - snake_size]
    elif direction == 'DOWN':
        new_head = [snake_pos[0][0], snake_pos[0][1] + snake_size]

    # 如果蛇头与食物位置相等，增加长度
    if new_head == food_pos:
        food_spawn = False
        score += 1
        # 增加游戏难度
        if score % difficulty_increase_interval == 0:
            difficulty_level += 1
            snake_speed += 1
    else:
        snake_pos.pop()  # 移除尾部

    snake_pos.insert(0, list(new_head))  # 在头部插入新位置

    # 检查蛇是否撞墙或自咬
    if (new_head[0] == SCREEN_WIDTH or
        new_head[0] < 0 or
        new_head[1] == SCREEN_HEIGHT or
        new_head[1] < 0):
        running = False

    for block in snake_pos[1:]:
        if new_head == block:
            running = False

    # 绘制食物
    if not food_spawn:
        while True:
            food_pos = [random.randrange(0, SCREEN_WIDTH - snake_size, snake_size),
                        random.randrange(0, SCREEN_HEIGHT - snake_size, snake_size)]
            if food_pos not in snake_pos:
                break
        food_spawn = True
    pygame.draw.rect(window, GREEN, pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))

    # 绘制蛇的身体
    for i, block in enumerate(snake_pos):
        if i == 0:
            pygame.draw.rect(window, BLUE, pygame.Rect(block[0], block[1], snake_size, snake_size))
        elif i == len(snake_pos) - 1:
            pygame.draw.rect(window, YELLOW, pygame.Rect(block[0], block[1], snake_size, snake_size))
        else:
            pygame.draw.rect(window, RED, pygame.Rect(block[0], block[1], snake_size, snake_size))

    # 显示得分
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))
    speed_text = font.render(f"Speed: {snake_speed}", True, WHITE)
    window.blit(speed_text, (10, 40))

    # 更新屏幕显示
    pygame.display.update()

    # 控制游戏速度
    clock.tick(snake_speed//2)

# 结束游戏
pygame.quit()
