# Gkoutzas Nikos, 29-5-2021
# First, you have to install necessary dependencies such as tkinter and Image-ImageTk (tested on Ubuntu 20 / Python3)


# Have fun !


from tkinter import *
import tkinter.font as tkFont
from PIL import Image , ImageTk
from random import randrange , randint
import os

bombs_array = [(0 , 0)] * 30
root = Tk()
root.title("Snake game")
root.resizable(False , False)

image = PhotoImage(file = "app_icon.png")
root.iconphoto(False , image)

difficulty_mode = "easy"
SCORE = 0
GAME_SPEED = 105
GAME_SPEED_MSG = 1
EATEN_APPLES = 0
WIDTH_BOARD = 1400
HEIGHT_BOARD = 780
enable_food_ = True
Hearts = 3
CHOICE = ""
limit = 0
NEW_RECORD_IN_FILE = 0

canvas = Canvas(root , width = WIDTH_BOARD , height = HEIGHT_BOARD , bg = "black")
canvas.create_line(10 , 50 , 1390 , 50 , fill = "red" , width = 2)
canvas.create_line(10 , 50 , 10 , 770 , fill = "red" , width = 2)
canvas.create_line(1390 , 50 , 1390 , 770 , fill = "red" , width = 2)
canvas.create_line(10 , 770 , 1390 , 770 , fill = "red" , width = 2)

score_font = tkFont.Font(size = 17)

canvas.pack()

snake_icon = Image.open("snake.png")
snake_image = ImageTk.PhotoImage(snake_icon)


rocket_icon = Image.open("rocket.png")
rocket_image = ImageTk.PhotoImage(rocket_icon)

fire_of_rocket_icon = Image.open("fire_of_rocket.png")
fire_of_rocket_icon = fire_of_rocket_icon.resize( (40 , 40) , resample = 0)
fire_of_rocket_image = ImageTk.PhotoImage(fire_of_rocket_icon)

food_icon = Image.open("apple.png")
food_icon = food_icon.resize( (40 , 40) , resample = 0)
food_image = ImageTk.PhotoImage(food_icon)

bomb_icon = Image.open("images.png")
bomb_icon = bomb_icon.resize( (30 , 30) , resample = 0)
bomb_image = ImageTk.PhotoImage(bomb_icon)

arrow_keys_icon = Image.open("arrow_keys.png")
arrow_keys_icon = arrow_keys_icon.resize( (150 , 120) , resample = 0)
arrow_keys_image = ImageTk.PhotoImage(arrow_keys_icon)

hide_snake_icon = Image.open("hide_snake.jpg")
hide_snake_image = ImageTk.PhotoImage(hide_snake_icon)

heart_icon = Image.open("heart.png")
heart_icon = heart_icon.resize( (50 , 50) , resample = 0)
heart_image = ImageTk.PhotoImage(heart_icon)

space_bar_icon = Image.open("space_bar.png")
space_bar_icon = space_bar_icon.resize( (126 , 112) , resample = 0)
space_bar_image = ImageTk.PhotoImage(space_bar_icon)

heart_icon_corners = Image.open("Heart_Corners.png")
heart_icon_corners = heart_icon_corners.resize( (35 , 35) , resample = 0)
heart_image_corners = ImageTk.PhotoImage(heart_icon_corners)



positions_of_snake = [(700 , 460) , (680 , 460) , (660 , 460)]
X_axis_food = 2000
Y_axis_food = 2000
food = (X_axis_food , Y_axis_food)

X_axis_bomb = 2000
Y_axis_bomb = 2000
enable_bombs = True
DIFF_TIME = 5000
NUMBER_of_BOMBS = 0
LIMIT_X_distance = 100
LIMIT_Y_distance = 80
rocket_speed = 300
lose_heart_from_rocket_once = True
delete_heart_from_board = False
enable_hearts_corner_ONE = False
enable_hearts_corner_TWO = True
enable_hearts = False

Record = 0
axis_rand_4_corners = [(20,60) , (1380 , 60) , (20 , 760) , (1380 , 760)]

y_axis_rocket = randrange(60 , 760 , 20)
rocket_list = [(1420 , y_axis_rocket) , (1440 , y_axis_rocket) , (1460 , y_axis_rocket) , (1480 , y_axis_rocket) , (1500 , y_axis_rocket)]
cur_direction = "Right"

list_of_files = ["easy.txt" , "normal.txt" , "hard.txt" , "very_hard.txt"]
# =====================================================================================================================================================




def food_not_in_bombs():
    global NUMBER_of_BOMBS , food , bombs_array
    for i in range(NUMBER_of_BOMBS):
        if(food == bombs_array[i]):
            return False
    return True





def random_pos_food():
    global X_axis_food , Y_axis_food
    while(True):
        X_axis_food = randrange(20 , 1380 , 20)
        Y_axis_food = randrange(60 , 760 , 20)
        food = (X_axis_food , Y_axis_food)
        FOOD_not_in_BOMBS = food_not_in_bombs()
        if(food not in positions_of_snake and FOOD_not_in_BOMBS):
            canvas.create_image(X_axis_food , Y_axis_food , image = food_image , tag = "food")
            break




        
def rocket():
    global rocket_list , rocket_speed , GAME_SPEED , positions_of_snake , lose_heart_from_rocket_once , limit , CHOICE
    if(not CHOICE == "1"):
        if(rocket_list[4][0] < 0):

            if(positions_of_snake[0][0] <= (WIDTH_BOARD // 2) + limit):
                #print("Rocket started")
                lose_heart_from_rocket_once = True
                y_axis_rocket = randrange(60 , 760 , 20)
                rocket_list = [(1420 , y_axis_rocket) , (1440 , y_axis_rocket) , (1460 , y_axis_rocket) , (1480 , y_axis_rocket) , (1500 , y_axis_rocket)]
                #print(rocket_list[0])

        else:
            rocket_nose = [ (rocket_list[0][0] - 20 , rocket_list[0][1]) ]
            rocket_list = rocket_nose + rocket_list[:-1]
                    
            for cur_position , new_rocket_pos in zip(canvas.find_withtag("rocket") , rocket_list):
                canvas.coords(cur_position , new_rocket_pos) # move snake from CURRENT position to the NEXT one
            for cur_position , new_rocket_pos in zip(canvas.find_withtag("fire_of_rocket") , rocket_list[3:]):
                canvas.coords(cur_position , new_rocket_pos) # move snake from CURRENT position to the NEXT one
        
        root.after(rocket_speed , rocket)
        rocket_speed = rocket_speed + 250 + GAME_SPEED







def create_elements():
    global rocket_list
    for x_coord , y_coord in positions_of_snake:
        canvas.create_image(x_coord , y_coord , image = snake_image , tag = "snake")
    canvas.create_image(X_axis_food , Y_axis_food , image = food_image , tag = "food")
    for X_rocket , Y_rocket in rocket_list[:-2]:
        canvas.create_image(X_rocket , Y_rocket , image = rocket_image , tag = "rocket")
    for X_rocket , Y_rocket in rocket_list[3:]:
        canvas.create_image(rocket_list[3][0] , rocket_list[3][1] , image = fire_of_rocket_image , tag = "fire_of_rocket")






def __enable_bombs__():
    global enable_bombs
    canvas.delete("bomb")
    enable_bombs = True








def put_hearts_in_corners():
    global Hearts , CHOICE , heart_icon , EATEN_APPLES , axis_rand_4_corners , positions_of_snake , enable_hearts_corner_TWO , enable_hearts_corner_ONE , enable_hearts
    
    #print("HEARTS: " + str(Hearts) + "     ,     " + "enable_hearts_corner_TWO:  " + str(enable_hearts_corner_TWO) + "     ,     " + "enable_hearts_corner_ONE:  "\
    #+ str(enable_hearts_corner_ONE))
    
    #print(enable_hearts)
    if(CHOICE == "2"):
        if(EATEN_APPLES % 5 == 0):
            if(Hearts == 2 and enable_hearts_corner_TWO):
                for i in range(4):
                    canvas.create_image(axis_rand_4_corners[i][0] , axis_rand_4_corners[i][1] , image = heart_image_corners , tag = "heart_corner")    
                enable_hearts_corner_TWO = False
                enable_hearts_corner_ONE = True
                enable_hearts = True

            elif(Hearts == 1 and enable_hearts_corner_ONE):
                for i in range(4):
                    canvas.create_image(axis_rand_4_corners[i][0] , axis_rand_4_corners[i][1] , image = heart_image_corners , tag = "heart_corner")    
                enable_hearts_corner_ONE = False
                enable_hearts_corner_TWO = True
                enable_hearts = True
                    
        else:
            enable_hearts = False
            canvas.delete("heart_corner")
            if(Hearts == 1):
                enable_hearts_corner_TWO = False
                enable_hearts_corner_ONE = True
            if(Hearts == 2):
                enable_hearts_corner_ONE = False
                enable_hearts_corner_TWO = True




    elif(CHOICE == "3"):
        if(EATEN_APPLES % 10 == 0):
            if(Hearts == 2 and enable_hearts_corner_TWO):
                for i in range(4):
                    canvas.create_image(axis_rand_4_corners[i][0] , axis_rand_4_corners[i][1] , image = heart_image_corners , tag = "heart_corner")    
                enable_hearts_corner_TWO = False
                enable_hearts_corner_ONE = True
                enable_hearts = True

            elif(Hearts == 1 and enable_hearts_corner_ONE):
                for i in range(4):
                    canvas.create_image(axis_rand_4_corners[i][0] , axis_rand_4_corners[i][1] , image = heart_image_corners , tag = "heart_corner")    
                enable_hearts_corner_ONE = False
                enable_hearts_corner_TWO = True
                enable_hearts = True
                    
        else:
            enable_hearts = False
            canvas.delete("heart_corner")
            if(Hearts == 1):
                enable_hearts_corner_TWO = False
                enable_hearts_corner_ONE = True
            if(Hearts == 2):
                enable_hearts_corner_ONE = False
                enable_hearts_corner_TWO = True




    elif(CHOICE == "4"):
        if(EATEN_APPLES % 15 == 0):
            if(Hearts == 2 and enable_hearts_corner_TWO):
                for i in range(4):
                    canvas.create_image(axis_rand_4_corners[i][0] , axis_rand_4_corners[i][1] , image = heart_image_corners , tag = "heart_corner")    
                enable_hearts_corner_TWO = False
                enable_hearts_corner_ONE = True
                enable_hearts = True

            elif(Hearts == 1 and enable_hearts_corner_ONE):
                for i in range(4):
                    canvas.create_image(axis_rand_4_corners[i][0] , axis_rand_4_corners[i][1] , image = heart_image_corners , tag = "heart_corner")    
                enable_hearts_corner_ONE = False
                enable_hearts_corner_TWO = True
                enable_hearts = True
                    
        else:
            enable_hearts = False
            canvas.delete("heart_corner")
            if(Hearts == 1):
                enable_hearts_corner_TWO = False
                enable_hearts_corner_ONE = True
            if(Hearts == 2):
                enable_hearts_corner_ONE = False
                enable_hearts_corner_TWO = True







def snake_get_life():
    global positions_of_snake , axis_rand_4_corners , Hearts , delete_heart_from_board , CHOICE , EATEN_APPLES , enable_hearts_corner_TWO , enable_hearts_corner_ONE\
           , enable_hearts

    if(positions_of_snake[0] in axis_rand_4_corners and Hearts < 3 and enable_hearts):
        delete_heart_from_board = False
        if(Hearts == 2):
            enable_hearts_corner_TWO = True
            enable_hearts_corner_ONE = False
            enable_hearts = False
        if(Hearts == 1):
            enable_hearts_corner_TWO = False
            enable_hearts_corner_ONE = True
            enable_hearts = False
            
        canvas.delete("heart_corner")

        if(not delete_heart_from_board):
            if(Hearts == 2):
                canvas.create_image(1340 , 25 , image = heart_image , tag = "heart_right")
            elif(Hearts == 1):
                canvas.create_image(1300 , 25 , image = heart_image , tag = "heart_middle")
        Hearts = Hearts + 1





def play_game():
    global SCORE , Record

    if ( not limits() ):
        canvas.bind_all("<Key>" , control_snake)
        move_snake()
        snake_catches_food()
        turn_on_bombs()
        rocket()
        hearts()
        put_hearts_in_corners()
        snake_get_life()
        root.after(GAME_SPEED , play_game)
    else:
        canvas.delete("fire_of_rocket")
        canvas.delete("rocket")
        canvas.delete("heart_corner")
        canvas.delete("food")
        canvas.delete("bomb")
        canvas.delete("snake")

        if(SCORE >= Record):
            You_won()

        else:
            game_over()
    





def write_record_to_file(fileName):
    global CHOICE , SCORE
    _file_ = open(fileName , "r+")
    _file_.seek(0)
    _file_.write(str(SCORE))
    _file_.close()







def read_record_from_file(fileName):
    global CHOICE , SCORE , NEW_RECORD_IN_FILE , Record
    _file_ = open(fileName , "r+")
    _file_.seek(0)
    NEW_RECORD_IN_FILE = int(_file_.read() )
    _file_.close()
    return NEW_RECORD_IN_FILE
        







def You_won():
    global SCORE , list_of_files , CHOICE
    
    canvas.delete("fire_of_rocket")
    canvas.delete("rocket")
    canvas.delete("heart_corner")
    canvas.delete("snake")
    canvas.delete("bomb")
    win_font = tkFont.Font(size = 70)
    Label_win = Label(root , text = "YOU WON !!!" , bg = "black" , fg = "green" , font = win_font)
    Label_win.place(x = 410 , y = 250)
    
    new_record_font = tkFont.Font(size = 40)
    Label_new_record = Label(root , text = "NEW RECORD: " + str(SCORE) , bg = "black" , fg = "green" , font = new_record_font)
    if(SCORE > NEW_RECORD_IN_FILE):    
        Label_new_record.place(x = 494, y = 450)
        write_record_to_file( list_of_files[int(CHOICE) - 1] )

        root.after(3500 , restart_game , False , None , None , None ,  Label_win , Label_new_record)
    else:
        root.after(3500 , restart_game , False , None , None , None ,  Label_win , Label_new_record)





def turn_on_bombs():
    global CHOICE , EATEN_APPLES , enable_bombs
    bomb()


    

def distance_between_snake_bomb():
    global X_axis_bomb , Y_axis_bomb , positions_of_snake , LIMIT_X_distance , LIMIT_Y_distance
    
    return abs(positions_of_snake[0][0] - X_axis_bomb) >= LIMIT_X_distance and abs(positions_of_snake[0][1] - Y_axis_bomb) >= LIMIT_Y_distance
    




def bomb():
    global EATEN_APPLES , X_axis_bomb , Y_axis_bomb , enable_bombs , DIFF_TIME , NUMBER_of_BOMBS , bombs_array , LIMIT_X_distance , LIMIT_Y_distance , CHOICE
    
    if(not CHOICE == "1"):
        if(CHOICE == "2"):
            if(EATEN_APPLES >= 34 and EATEN_APPLES <= 46):
                LIMIT_X_distance = 100
                LIMIT_Y_distance = 80
                NUMBER_of_BOMBS = 4
            elif(EATEN_APPLES > 46):
                NUMBER_of_BOMBS = 0
                LIMIT_X_distance = 120
                LIMIT_Y_distance = 100
                NUMBER_of_BOMBS = 1
        elif(CHOICE == "3"):
            if(EATEN_APPLES >= 39 and EATEN_APPLES < 50):
                LIMIT_X_distance = 90
                LIMIT_Y_distance = 70
                NUMBER_of_BOMBS = 5
            elif(EATEN_APPLES >= 50):
                NUMBER_of_BOMBS = 3
                LIMIT_X_distance = 110
                LIMIT_Y_distance = 90
                NUMBER_of_BOMBS = 2
        elif(CHOICE == "4"):
            if(EATEN_APPLES >= 45 and EATEN_APPLES <= 60):
                LIMIT_X_distance = 60
                LIMIT_Y_distance = 40
                NUMBER_of_BOMBS = 5
            elif(EATEN_APPLES > 60):
                NUMBER_of_BOMBS = 5
                LIMIT_X_distance = 80
                LIMIT_Y_distance = 60
                NUMBER_of_BOMBS = 3
        if(enable_bombs):
            for i in range(NUMBER_of_BOMBS):
                while(True):
                    X_axis_bomb = randrange(20 , 1380 , 20)
                    Y_axis_bomb = randrange(60 , 760 , 20)
                    bomb_XY = (X_axis_bomb , Y_axis_bomb)
                    bombs_array[i] = bomb_XY
                        
                    if(bomb_XY not in positions_of_snake and not bomb_XY == food and distance_between_snake_bomb() ):
                        canvas.create_image(X_axis_bomb , Y_axis_bomb , image = bomb_image , tag = "bomb")
                        break
            enable_bombs = False
            root.after(DIFF_TIME, __enable_bombs__ )






def hit_any_bomb():
    global positions_of_snake , bombs_array
    for i in range(NUMBER_of_BOMBS):
        #print(bombs_array[i])
        if(positions_of_snake[0] == bombs_array[i] ):
            return 1






def hearts():
    global Hearts , SCORE , X_axis_bomb , Y_axis_bomb , NUMBER_of_BOMBS , bombs_array , rocket_list , positions_of_snake , lose_heart_from_rocket_once ,\
           delete_heart_from_board , EATEN_APPLES , CHOICE , NEW_RECORD_IN_FILE

       
    hit_bomb = hit_any_bomb()

    
    
    if(hit_bomb == 1):
        delete_heart_from_board = True
        canvas.delete("bomb")
        X_axis_bomb = 20
        Y_axis_bomb = 60
        bomb_XY = (X_axis_bomb  , Y_axis_bomb)
        for i in range(NUMBER_of_BOMBS):    
            bombs_array[i] = bomb_XY
        
        
            
        if(Hearts == 3 and delete_heart_from_board):
            canvas.delete("heart_right")
        elif(Hearts == 2 and delete_heart_from_board): 
            canvas.delete("heart_middle")
        elif(Hearts == 1 and delete_heart_from_board):
            canvas.delete("heart_left")
        Hearts = Hearts - 1

        if(SCORE >= 1):
            SCORE = SCORE - 1
            score_text = Label(root , text = "Difficulty: " + difficulty_mode + "     " + "Score: " + str(SCORE)  + "/" + str(Record) + \
            "     Game speed: " + str(GAME_SPEED_MSG)\
            + "     Eaten apples: " + \
            str(EATEN_APPLES) + "     Bombs: " +  str(NUMBER_of_BOMBS) + "     " + "Record: " + str(NEW_RECORD_IN_FILE) + "    " , bg = "black" , \
            font = score_font , fg = "orange")
            score_text.place(x = 50 , y = 5)


    if(positions_of_snake[0] in rocket_list and lose_heart_from_rocket_once):
        delete_heart_from_board = True
        #print("HIT A ROCKET")
        lose_heart_from_rocket_once = False
        if(Hearts == 3 and delete_heart_from_board):
            canvas.delete("heart_right")
        elif(Hearts == 2 and delete_heart_from_board):
            canvas.delete("heart_middle")
        elif(Hearts == 1 and delete_heart_from_board):
            canvas.delete("heart_left")
        Hearts = Hearts - 1

        if(SCORE >= 1):
            SCORE = SCORE - 1
            score_text = Label(root , text = "Difficulty: " + difficulty_mode + "     " + "Score: " + str(SCORE)  + "/" + str(Record) + \
            "     Game speed: " + str(GAME_SPEED_MSG)\
            + "     Eaten apples: " + \
            str(EATEN_APPLES) + "     Bombs: " +  str(NUMBER_of_BOMBS) + "     " + "Record: " + str(NEW_RECORD_IN_FILE) + "    " , bg = "black" , \
            font = score_font , fg = "orange")
            score_text.place(x = 50 , y = 5)

        




def press_space_bar():
    canvas.create_image(600 , 380 , image = hide_snake_image)
    canvas.create_image(700 , 600 , image = arrow_keys_image)
    msg_font =  tkFont.Font(size = 11)
    label_msg = Label(root , text = "Use arrow keys to control snake" , bg = "black" , fg = "sky blue" , font = msg_font)
    label_msg.place(x = 580 , y = 680)
    start_font =  tkFont.Font(size = 25)
    press_label = Label(root , text = "PRESS" , bg = "black" , fg = "white" , font = start_font)
    press_label.place(x = 510 , y = 230)
    canvas.create_image(675 , 250 , image = space_bar_image , tag = "space_bar")
    to_start_label = Label(root , text = "TO START" , bg = "black" , fg = "white" , font = start_font)
    to_start_label.place(x = 725 , y = 230)
    root.bind_all("<space>" , lambda c: [root.unbind_all("<space>") , press_label.destroy() , to_start_label.destroy() , canvas.delete("space_bar") ,\
    hide_snake_image.__del__() , arrow_keys_image.__del__() , label_msg.destroy() , play_game()] )
    
    



def snake_catches_food():
    global enable_food_ , SCORE , EATEN_APPLES , CHOICE , NUMBER_of_BOMBS
    food = (X_axis_food , Y_axis_food)

    if(enable_food_):
        random_pos_food()
        enable_food_ = False

    if(positions_of_snake[0] == food):
        canvas.delete("food")
        
        EATEN_APPLES = EATEN_APPLES + 1
        SCORE = SCORE + 1
        increase_speed()
        score_text = Label(root , text = "Difficulty: " + difficulty_mode + "     " + "Score: " + str(SCORE)  + "/" + str(Record) + \
        "     Game speed: " + str(GAME_SPEED_MSG)\
        + "     Eaten apples: " + \
        str(EATEN_APPLES) + "     Bombs: " +  str(NUMBER_of_BOMBS) + "     " + "Record: " + str(NEW_RECORD_IN_FILE) + "    " , bg = "black" , \
        font = score_font , fg = "orange")
        score_text.place(x = 50 , y = 5)
        positions_of_snake.append(positions_of_snake[-1])
        canvas.create_image(positions_of_snake[-1] , image = snake_image , tag = "snake")
        #print(positions_of_snake)
        
        enable_food_ = True
    #print(enable_food_)






def increase_speed():
    global SCORE , GAME_SPEED , GAME_SPEED_MSG , NUMBER_of_BOMBS , Record
    if(SCORE % 5 == 0 and GAME_SPEED >= 35):
        GAME_SPEED = GAME_SPEED - 5
        GAME_SPEED_MSG = GAME_SPEED_MSG + 1
        score_text = Label(root , text = "Difficulty: " + difficulty_mode + "     " + "Score: " + str(SCORE)  + "/" + str(Record) + \
        "     Game speed: " + str(GAME_SPEED_MSG)\
        + "     Eaten apples: " + \
        str(EATEN_APPLES) + "     Bombs: " +  str(NUMBER_of_BOMBS) + "     " + "Record: " + str(NEW_RECORD_IN_FILE) + "    " , bg = "black" , \
        font = score_font , fg = "orange")
        score_text.place(x = 50 , y = 5)







def difficulty_level(entry , choice):
    global GAME_SPEED , difficulty_mode , snake_image , score_font , GAME_SPEED_MSG , CHOICE , NUMBER_of_BOMBS , LIMIT_X_distance , LIMIT_Y_distance , limit\
           , Record , list_of_files , NEW_RECORD_IN_FILE

    if(choice == "1"):
        CHOICE = choice
        NEW_RECORD_IN_FILE = read_record_from_file("easy.txt")
        difficulty_mode = "Easy"
        Record = 50
        GAME_SPEED_MSG = 1
        GAME_SPEED = 105
        for child in root.winfo_children(): # forget all places
            child.place_forget()
        press_space_bar()
        score_text = Label(root , text = "Difficulty: " + difficulty_mode + "     " + "Score: " + str(SCORE)  + "/" + str(Record) + \
        "     Game speed: " + str(GAME_SPEED_MSG)\
        + "     Eaten apples: " + \
        str(EATEN_APPLES) + "     Bombs: " +  str(NUMBER_of_BOMBS) + "     " + "Record: " + str(NEW_RECORD_IN_FILE) + "    " , bg = "black" , \
        font = score_font , fg = "orange")
        score_text.place(x = 50 , y = 5)
    elif(choice == "2"):
        CHOICE = choice
        NEW_RECORD_IN_FILE = read_record_from_file("normal.txt")
        difficulty_mode = "Normal"
        Record = 60
        limit = 0
        LIMIT_X_distance = 100
        LIMIT_Y_distance = 80
        NUMBER_of_BOMBS = 6
        GAME_SPEED_MSG = 3
        GAME_SPEED = 95
        for child in root.winfo_children(): # forget all places
            child.place_forget()
        press_space_bar()
        score_text = Label(root , text = "Difficulty: " + difficulty_mode + "     " + "Score: " + str(SCORE)  + "/" + str(Record) + \
        "     Game speed: " + str(GAME_SPEED_MSG)\
        + "     Eaten apples: " + \
        str(EATEN_APPLES) + "     Bombs: " +  str(NUMBER_of_BOMBS) + "     " + "Record: " + str(NEW_RECORD_IN_FILE) + "    " , bg = "black" , \
        font = score_font , fg = "orange")
        score_text.place(x = 50 , y = 5)
        canvas.create_image(1260 , 25 , image = heart_image , tag = "heart_left")
        canvas.create_image(1300 , 25 , image = heart_image , tag = "heart_middle")
        canvas.create_image(1340 , 25 , image = heart_image , tag = "heart_right")
    elif(choice == "3"):
        CHOICE = choice
        NEW_RECORD_IN_FILE = read_record_from_file("hard.txt")
        difficulty_mode = "Hard"
        Record = 70
        limit = 100
        LIMIT_X_distance = 70
        LIMIT_Y_distance = 50
        NUMBER_of_BOMBS = 8
        GAME_SPEED_MSG = 4
        GAME_SPEED = 90
        for child in root.winfo_children(): # forget all places
            child.place_forget()
        press_space_bar()
        score_text = Label(root , text = "Difficulty: " + difficulty_mode + "     " + "Score: " + str(SCORE)  + "/" + str(Record) + \
        "     Game speed: " + str(GAME_SPEED_MSG)\
        + "     Eaten apples: " + \
        str(EATEN_APPLES) + "     Bombs: " +  str(NUMBER_of_BOMBS) + "     " + "Record: " + str(NEW_RECORD_IN_FILE) + "    " , bg = "black" , \
        font = score_font , fg = "orange")
        score_text.place(x = 50 , y = 5)
        canvas.create_image(1260 , 25 , image = heart_image , tag = "heart_left")
        canvas.create_image(1300 , 25 , image = heart_image , tag = "heart_middle")
        canvas.create_image(1340 , 25 , image = heart_image , tag = "heart_right")
    elif(choice == "4"):
        CHOICE = choice
        NEW_RECORD_IN_FILE = read_record_from_file("very_hard.txt")
        difficulty_mode = "Very hard"
        Record = 85
        limit = 250
        LIMIT_X_distance = 50
        LIMIT_Y_distance = 30
        NUMBER_of_BOMBS = 10
        GAME_SPEED_MSG = 4
        GAME_SPEED = 90
        for child in root.winfo_children(): # forget all places
            child.place_forget()
        press_space_bar()

        score_text = Label(root , text = "Difficulty: " + difficulty_mode + "     " + "Score: " + str(SCORE)  + "/" + str(Record) + \
        "     Game speed: " + str(GAME_SPEED_MSG)\
        + "     Eaten apples: " + \
        str(EATEN_APPLES) + "     Bombs: " +  str(NUMBER_of_BOMBS) + "     " + "Record: " + str(NEW_RECORD_IN_FILE) + "    " , bg = "black" , \
        font = score_font , fg = "orange")
        score_text.place(x = 50 , y = 5)
        canvas.create_image(1260 , 25 , image = heart_image , tag = "heart_left")
        canvas.create_image(1300 , 25 , image = heart_image , tag = "heart_middle")
        canvas.create_image(1340 , 25 , image = heart_image , tag = "heart_right")
    else:
        entry.delete(0 , END)
        select_difficulty()
    





def select_difficulty():
    diff_font = tkFont.Font(size = 15)
    diff_font_2 = tkFont.Font(size = 20)
    use_msg_font = tkFont.Font(size = 11)

    label_msg = Label(root , text = "Difficulty Settings" , bg = "black" , fg = "green2" ,  font = diff_font_2)
    
    easy_label = Label(root , text = "1                            Give Me A Taste" , bg = "black" , fg = "white" , font = diff_font)
    medium_label = Label(root , text = "2              Give Me A Balanced Experience" , bg = "black" , fg = "white" , font = diff_font)   
    pro_label = Label(root , text = "3                        Give Me A Challenge" , bg = "black" , fg = "white" , font = diff_font)      
    titan_label = Label(root , text = "4                         Give Me Everything" , bg = "black" , fg = "white" , font = diff_font) 
    enter_msg = Label(root , text = " Type a number 1-4 and press Enter" , bg = "black" , fg = "DarkSeaGreen3" , font = use_msg_font)
    
    entry = Entry(root , width = 13 , bg = "gray76")
    entry.focus_set()
    entry.place(x = 650 , y = 450 , height = 30)

    label_msg.place(x = 586 , y = 180)
    easy_label.place(x = 440 , y = 250)
    medium_label.place(x = 440 , y = 280)
    pro_label.place(x = 440 , y = 310)
    titan_label.place(x = 440 , y = 340)
    enter_msg.place(x = 566 , y = 500)
    
    entry.bind_all("<Return>" , lambda c: [entry.unbind_all("<Return>") , difficulty_level(entry ,entry.get() ) ] )






def destroy_all():
    global positions_of_snake
    for child in root.winfo_children(): # forget all places
        child.place_forget()
    os.execv(sys.executable, ["python3"] + sys.argv)





def restart_game(enable , label_msg , Label_endOFgame , score_msg_label , label_won , label_new_record):
    global SCORE , Record
    if(enable):
        snake_image.__del__()
        food_image.__del__()
        label_msg.destroy()
        Label_endOFgame.destroy()
        score_msg_label.destroy()
    if(not enable):
        label_won.destroy()
        label_new_record.destroy()
    restart_font = tkFont.Font(size = 20)
    
    restart_label = Label(root , text = "Do you want to play again ? [y/n]" , bg = "black" , fg = "light coral" , font = restart_font)
    restart_label.place(x = 480 , y = 340)

    if(SCORE < Record):
        lost_font = tkFont.Font(size = 15)
        lost_label = Label(root , text = "Practice More, Be Better" , bg = "black" , fg = "gold" , font = lost_font)
        lost_label.place(x = 585 , y = 650)
    else:
        won_font = tkFont.Font(size = 15)
        won_label = Label(root , text = "You're very good" , bg = "black" , fg = "gold" , font = won_font)
        won_label.place(x = 620 , y = 650)
    restart_label.bind_all("<y>" , lambda c: destroy_all()  )
    restart_label.bind_all("<n>" , lambda c: exit(1) )





def game_over():
    global SCORE
    game_over_font = tkFont.Font(size = 60)
    Label_endOFgame = Label(root , text = "GAME OVER !" , bg = "black" , fg = "red" , font = game_over_font )
    Label_endOFgame.place(x = 420 , y = 350)
    score_font = tkFont.Font(size = 25)
    score_msg_label = Label(root , text = "You scored " + str(SCORE) , bg = "black" , fg = "green" , font = score_font)
    score_msg_label.place(x = 585 , y = 450)

    if(positions_of_snake[0] in positions_of_snake[1:] ):
        game_over_msg_font = tkFont.Font(size = 20)
        label_msg = Label(root , text = "Snake ate itself" , bg = "black" , fg = "white" , font = game_over_msg_font)
        label_msg.place(x = 595, y = 100)
    elif(Hearts == 0):
        game_over_msg_font = tkFont.Font(size = 20)
        label_msg = Label(root , text = "Snake ran out of life" , bg = "black" , fg = "white" , font = game_over_msg_font)
        label_msg.place(x = 570, y = 100)
    else:
        game_over_msg_font = tkFont.Font(size = 20)
        label_msg = Label(root , text = "Snake hit a wall" , bg = "black" , fg = "white" , font = game_over_msg_font)
        label_msg.place(x = 595, y = 100)

    root.after(3500 , restart_game , True , label_msg , Label_endOFgame , score_msg_label , None , None)
    




def limits():
    global Hearts
    return \
        positions_of_snake[0][0] == WIDTH_BOARD or positions_of_snake[0][0] == 0 or positions_of_snake[0][1] == 40 or positions_of_snake[0][1] == HEIGHT_BOARD\
        or positions_of_snake[0] in positions_of_snake[1:] or Hearts == 0
    



def control_snake(e):
    global cur_direction
    new_direction = e.keysym     
    if( new_direction == "Up" or new_direction == "Down" or new_direction == "Right" or new_direction == "Left"):   
        # Useful in order to NOT allow you to push other keys. 
        cur_direction = new_direction
    



def move_snake():
    global positions_of_snake
    if(cur_direction == "Right"):
        head = [ (positions_of_snake[0][0] + 20 , positions_of_snake[0][1] )]
    if(cur_direction == "Left"):
        head = [ (positions_of_snake[0][0] - 20 , positions_of_snake[0][1] )]
    if(cur_direction == "Down"):
        head = [ (positions_of_snake[0][0] , positions_of_snake[0][1] + 20)]
    if(cur_direction == "Up"):
        head = [ (positions_of_snake[0][0] , positions_of_snake[0][1] - 20)]
        
    positions_of_snake = head + positions_of_snake[:-1]
        
    for cur_position , new_snake_pos in zip(canvas.find_withtag("snake") , positions_of_snake):
        canvas.coords(cur_position , new_snake_pos) # move snake from CURRENT position to the NEXT one



select_difficulty()    
create_elements()

root.mainloop()