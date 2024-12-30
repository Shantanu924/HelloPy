import turtle as tr2

screen = tr.Screen()
screen.title("Tic-tac-toe")
screen.setup(width=600,height=600)

def draw_board():
    board_pen = tr.Turtle()
    board_pen.speed(0)
    board_pen.pensize(5)

    board_pen.penup()               #vertical lines
    board_pen.goto(-100,300)
    board_pen.pendown()
    board_pen.goto(-100,-300)

    board_pen.penup()
    board_pen.goto(100,300)
    board_pen.pendown()
    board_pen.goto(100,-300)

    board_pen.penup()              #horizontal lines
    board_pen.goto(-300,100)
    board_pen.pendown()
    board_pen.goto(300,100)

    board_pen.penup()
    board_pen.goto(-300,-100)
    board_pen.pendown()
    board_pen.goto(300,-100)

    board_pen.hideturtle()

def draw_x(x,y):
    pen = tr.Turtle()
    pen.color("blue")
    pen.pensize(5)
    pen.penup()
    pen.goto(x-50,y-50)
    pen.pendown()
    pen.goto(x+50,y+50)
    pen.penup()
    pen.goto(x-50,y+50)
    pen.pendown()
    pen.goto(x+50,y-50)
    
    pen.hideturtle()

def draw_o(x,y):
    pen = tr.Turtle()
    pen.color("red")
    pen.pensize(5)
    pen.penup()
    pen.goto(x,y-50)
    pen.pendown()
    pen.circle(50)

    pen.hideturtle()

positions = [
    (-200,200),(0,200),(200,200),
    (-200,0),(0,0),(200,0),
    (-200,-200),(0,-200),(200,-200)
]

grid = [""]*9
current_player = "X"
game_over= False

def check_winner():
    win_combine = [
        [0,1,2],[3,4,5],[6,7,8],  #row
        [0,3,6],[1,4,7],[2,5,8],  #column
        [0,4,8],[2,4,6]           #diagonal
    ]

    for combo in win_combine:
        if grid[combo[0]]==grid[combo[1]]==grid[combo[2]] and grid[combo[0]] !="":
            return grid[combo[0]]
    
    if "" not in grid:
        return "draw"
    
    return None

def click_handle(x,y):
    global current_player,game_over
    if game_over:
        return
    for i, pos in enumerate(positions):
        if pos[0]-100<x< pos[0]+100 and pos[1]-100<y<pos[1]+100:
            if grid[i]=="":
                grid[i]==current_player
                if current_player=="X":
                    draw_x(pos[0],pos[1])
                    current_player="O"
                else:
                    draw_o(pos[0],pos[1])
                    current_player="X"
                
                winner = check_winner()
                if winner:
                    game_over = True
                    if winner == "Draw":
                        screen.textinput("Game over, it's draw!")
                    else:
                        screen.textinput("Game over", f"{winner} wins! Press Enter to exit.")
                    screen.bye()
            break

draw_board()
screen.onclick(click_handle)
screen.mainloop()