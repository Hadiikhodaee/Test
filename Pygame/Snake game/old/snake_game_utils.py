from turtle import Turtle
from random import randint


def move_snake(snake_head):
    if snake_head.direction == "up":
        snake_y_position = snake_head.ycor()
        snake_y_position += 20
        snake_head.sety(snake_y_position)
    if snake_head.direction == "down":
        snake_y_position = snake_head.ycor()
        snake_y_position -= 20
        snake_head.sety(snake_y_position)
    if snake_head.direction == "right":
        snake_x_position = snake_head.xcor()
        snake_x_position += 20
        snake_head.setx(snake_x_position)
    if snake_head.direction == "left":
        snake_x_position = snake_head.xcor()
        snake_x_position -= 20
        snake_head.setx(snake_x_position)


def make_turtle(turtle_shape, turtle_color, speed="fastest"):
    turtle_object = Turtle()
    turtle_object.shape(turtle_shape)
    turtle_object.color(turtle_color)
    turtle_object.speed(speed)
    turtle_object.penup()
    return turtle_object


def change_turtle_object_position_in_random_place(turtle_object):

    x = randint(-270, 270)
    y = randint(-270, 230)
    turtle_object.goto(x, y)


def reset(snake_head, snake_body):
    snake_head.goto(0, 0)
    snake_head.direction = ""
    for body in snake_body:
        body.ht()
    snake_body.clear()