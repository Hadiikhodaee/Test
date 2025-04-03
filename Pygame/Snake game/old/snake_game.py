from turtle import Screen
from time import sleep
from snake_game_utils import move_snake, make_turtle, change_turtle_object_position_in_random_place, reset

# TODO بقیه توابع را به ماژول کمکی منتقل

score = 0

try:
    with open("snake_result.txt", "r") as f:
        high_score = int(f.read())

except:

    high_score = 0


def go_up():
    if snake_head.direction != "down":
        snake_head.direction = "up"


def go_down():
    if snake_head.direction != "up":
        snake_head.direction = "down"


def go_right():
    if snake_head.direction != "left":
        snake_head.direction = "right"


def go_left():
    if snake_head.direction != "right":
        snake_head.direction = "left"


window = Screen()
window.title("Snake Game")
window.bgcolor("blue")
window.setup(width=600, height=600)
window.tracer(0)
snake_head = make_turtle("square", "black")
snake_head.direction = ""

food = make_turtle("circle", "red")
food.shapesize(0.4, 0.4)
change_turtle_object_position_in_random_place(food)

score_board = make_turtle("square", "white")
score_board.ht()
score_board.goto(0, 260)

snake_body = []

window.listen()
window.onkeypress(go_up, 'Up')
window.onkeypress(go_up, 'w')
window.onkeypress(go_down, 'Down')
window.onkeypress(go_down, 's')
window.onkeypress(go_right, 'Right')
window.onkeypress(go_right, 'd')
window.onkeypress(go_left, 'Left')
window.onkeypress(go_left, 'a')

def on_close():
    with open("snake_result.txt", "w") as f:
        f.write(str(high_score))
    global running
    running = False

root = window._root
root.protocol("WM_DELETE_WINDOW", on_close)

running = True
while running:
    window.update()
    score_board.clear()
    score_board.write(f"Score: {score}, HighScore: {high_score}", font=("Terminal", 22), align="center")
    if snake_head.distance(food) < 15:
        score += 1
        if score > high_score:
            high_score = score
        change_turtle_object_position_in_random_place(food)
        new_tail = make_turtle("square", "grey")
        snake_body.append(new_tail)
        
    if len(snake_body) < 3:
        new_tail = make_turtle("square", "grey")
        snake_body.append(new_tail)

    for i in range(len(snake_body) - 1, 0, -1):
        x_pos_of_prev_i = snake_body[i-1].xcor()
        y_pos_of_prev_i = snake_body[i-1].ycor()
        snake_body[i].goto(x_pos_of_prev_i, y_pos_of_prev_i)

    if len(snake_body) > 0:
        snake_last_head_x = snake_head.xcor()
        snake_last_head_y = snake_head.ycor()
        snake_body[0].goto(snake_last_head_x, snake_last_head_y)

    if snake_head.xcor() > 290 or snake_head.xcor() < -290 or snake_head.ycor() > 290 or snake_head.ycor() < -290:
        reset(snake_head, snake_body)
        score = 0

    move_snake(snake_head)

    for body_part in snake_body:
        if snake_head.distance(body_part) < 15:
            reset(snake_head, snake_body)
            score = 0
    sleep(0.1)