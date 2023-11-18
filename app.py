from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
# 0 = puste 1 = kolko 2 = krzyzylk
plansza = [   
    [0,0,0],
    [0,0,0],
    [0,0,0],    ]
tie = False
znak = 2
bot = False

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/gra/human")
def grahuman():
    global bot
    empty()
    bot=False
    return render_template('gra.html',plansza=plansza,bot=bot, test=detectcrossing())

@app.route("/gra/bot")
def grabot():
    global bot
    empty()
    bot=True
    return render_template('gra.html',plansza=plansza,bot=bot, test=detectcrossing())
    
@app.route("/gra")
def gra():
    return render_template('gra.html',plansza=plansza,bot=bot, test=detectcrossing())

@app.route("/gra/reset")
def reset():
    global plansza
    empty()
    return redirect(url_for('index'))

def empty():
     global plansza,znak
     znak = 2
     for wiersz in range(0,3):
        for komorka in range(0,3):
            plansza[wiersz][komorka] = 0
@app.route("/ruch")
def ruch():
    global znak
    global bot
    wiersz = int(request.args["x"])
    komorka = int(request.args["y"])
    plansza[wiersz][komorka] = znak
    if checkforend():
        return redirect(url_for('wygrana'))
    if bot:
        changesymbol()
        if winningmove() !=(-1,-1):
                 plansza[winningmove()[0]][winningmove()[1]]=znak
                 if checkforend():
                    return redirect(url_for('wygrana'))
        if block() !=(-1,-1):
                 ruch = f"{block()[0]}{block()[1]}"
                 changesymbol()
                 return ruch
        if detectcrossing() !=(-1,-1):
                 ruch = f"{detectcrossing()[0]}{detectcrossing()[1]}"
                 changesymbol()
                 return ruch
        if basicmoves() !=(-1,-1):
                 ruch = f"{basicmoves()[0]}{basicmoves()[1]}"
                 changesymbol()
                 return ruch 
    changesymbol()
    return ""

@app.route("/gra/ruch")
def gra_ruch():
    global znak
    global bot
    wiersz = int(request.args["x"])
    komorka = int(request.args["y"])
    plansza[wiersz][komorka] = znak
    if checkforend():
        return redirect(url_for('wygrana'))
    if bot:
        changesymbol()
        if winningmove() !=(-1,-1):
                 plansza[winningmove()[0]][winningmove()[1]]=znak
                 if checkforend():
                    return redirect(url_for('wygrana'))
        if block() !=(-1,-1):
                 plansza[block()[0]][block()[1]]=znak
                 changesymbol()
                 return redirect(url_for('gra'))
        if detectcrossing() !=(-1,-1):
                 plansza[detectcrossing()[0]][detectcrossing()[1]]=znak
                 changesymbol()
                 return redirect(url_for('gra'))
        if basicmoves() !=(-1,-1):
                 plansza[basicmoves()[0]][basicmoves()[1]]=znak
                 changesymbol()
                 return redirect(url_for('gra'))  
    changesymbol()
    return redirect(url_for('gra'))

@app.route("/test_ajax")
def test_ajax():
     return 'Test'

def changesymbol():
     global znak
     if znak==2:
         znak = 1
     else:
        znak = 2

def winningmove():
    for i in range(3):
        if plansza[i][1] == plansza[i][2] == znak and plansza[i][0] == 0:
            return (i,0)
        if plansza[i][0] == plansza[i][2] == znak and plansza[i][1] == 0:
            return (i,1)
        if plansza[i][0] == plansza[i][1] == znak and plansza[i][2] == 0:
            return (i,2)
        if plansza[1][i] == plansza[2][i] == znak and plansza[0][i] == 0:
            return (0,i)
        if plansza[0][i] == plansza[2][i] == znak and plansza[1][i] == 0:
            return (1,i)
        if plansza[1][i] == plansza[0][i] == znak and plansza[2][i] == 0:
           return (2,i)
    if plansza[2][2] == plansza[1][1] == znak and plansza[0][0] == 0:
           return (0,0)
    if plansza[2][2] == plansza[0][0] == znak and plansza[1][1] == 0:
           return (1,1)
    if plansza[0][0] == plansza[1][1] == znak and plansza[2][2] == 0:
           return (2,2)
    if plansza[2][0] == plansza[1][1] == znak and plansza[0][2] == 0:
           return (0,2)
    if plansza[0][2] == plansza[2][0] == znak and plansza[1][1] == 0:
           return (1,1)
    if plansza[0][2] == plansza[1][1] == znak and plansza[2][0] == 0:
           return (2,0)
    return (-1,-1)

def block():
     enemy = znak
     if enemy==2:
        enemy = 1
     else:
        enemy = 2

     for i in range(3):
        if plansza[i][1] == plansza[i][2] == enemy and plansza[i][0] == 0:
            return (i,0)
        if plansza[i][0] == plansza[i][2] == enemy and plansza[i][1] == 0:
            return (i,1)
        if plansza[i][0] == plansza[i][1] == enemy and plansza[i][2] == 0:
            return (i,2)
        if plansza[1][i] == plansza[2][i] == enemy and plansza[0][i] == 0:
            return (0,i)
        if plansza[0][i] == plansza[2][i] == enemy and plansza[1][i] == 0:
            return (1,i)
        if plansza[1][i] == plansza[0][i] == enemy and plansza[2][i] == 0:
           return (2,i)
     if plansza[2][2] == plansza[1][1] == enemy and plansza[0][0] == 0:
           return (0,0)
     if plansza[2][2] == plansza[0][0] == enemy and plansza[1][1] == 0:
           return (1,1)
     if plansza[0][0] == plansza[1][1] == enemy and plansza[2][2] == 0:
           return (2,2)
     if plansza[2][0] == plansza[1][1] == enemy and plansza[0][2] == 0:
           return (0,2)
     if plansza[0][2] == plansza[2][0] == enemy and plansza[1][1] == 0:
           return (1,1)
     if plansza[0][2] == plansza[1][1] == enemy and plansza[2][0] == 0:
           return (2,0)
     return (-1,-1)

def detectcrossing():
    # middle is always full because it is first move for bot if player didnt took it
    if plansza[2][0] == plansza[0][2] == znak:
         if plansza [0][1]==plansza[0][0]==plansza[1][0]==0:
              return(0,0)
         if plansza [2][1]==plansza[2][2]==plansza[1][2]==0:
              return(2,2)
    if plansza[0][0] == plansza[2][2] == znak:
         if plansza [0][2]==plansza[1][2]==plansza[0][1]==0:
              return(0,2)
         if plansza [2][0]==plansza[2][1]==plansza[1][0]==0:
              return(2,0)
    if plansza[0][0]==plansza[1][1]==znak:
         if plansza[2][1]==plansza[0][1]==plansza[0][2]==0:
              return(0,1)
         if plansza[1][2]==plansza[1][0]==plansza[2][0]==0:
              return(1,0)
         if plansza[2][2]==plansza[2][0]==plansza[0][2]==0:
              return(0,2)
    if plansza[0][2]==plansza[1][1]==znak:
        if plansza[0][0]==plansza[0][1]==plansza[2][1]==0:
             return(0,1)
        if plansza[0][0]==plansza[1][0]==plansza[1][2]==0:
             return(1,0)
        if plansza[0][0]==plansza[2][0]==plansza[2][2]==0:
            return(0,0)
    if plansza[2][2] == plansza[1][1] == znak:
         if plansza [2][0]==plansza[0][1]==plansza[2][1]==0:
              return(2,1)
         if plansza [0][2]==plansza[1][0]==plansza[1][2]==0:
              return(1,2)
         if plansza [2][0]==plansza[0][2]==plansza[0][0]==0:
              return(0,2)
    if plansza[2][0] == plansza[1][1] == znak:
         if plansza [2][2]==plansza[0][1]==plansza[2][1]==0:
              return(2,1)
         if plansza [2][2]==plansza[1][0]==plansza[1][2]==0:
              return(1,2)
         if plansza [2][2]==plansza[0][2]==plansza[0][0]==0:
              return(0,0)
    return (-1,-1)

def basicmoves():
     enemy = znak
     if enemy==2:
        enemy = 1
     else:
        enemy = 2
    #middle
     if plansza[1][1] == 0:
          return (1,1)
     #corners
     if plansza[0][0] == enemy and plansza[2][2] == 0:
          return (2,2)
     if plansza[2][2] == enemy and plansza[0][0] == 0:
          return (0,0)
     if plansza[0][2] == enemy and plansza[2][0] == 0:
          return (2,0)
     if plansza[2][0] == enemy and plansza[0][2] == 0:
          return (0,2)

    #sides
     if plansza[0][0] == 0:
          return (0,0)
     if plansza[2][2] == 0:
          return (2,2)
     if plansza[0][2] == 0:
          return (0,2)
     if plansza[2][0] == 0:
          return (2,0)
     
     if plansza[0][1] == 0:
          return (0,1)
     if plansza[1][0] == 0:
          return (1,0)
     if plansza[1][2] == 0:
          return (1,2)
     if plansza[2][1] == 0:
          return (2,1)

     return (-1,-1)

def checkforend():
    global tie
    if \
    plansza[0][0] == plansza[0][1] == plansza[0][2] and plansza[0][0] !=0 or\
    plansza[1][0] == plansza[1][1] == plansza[1][2] and plansza[1][0] !=0 or\
    plansza[2][0] == plansza[2][1] == plansza[2][2] and plansza[2][0] !=0 or\
    plansza[0][0] == plansza[1][0] == plansza[2][0] and plansza[0][0] !=0 or\
    plansza[0][1] == plansza[1][1] == plansza[2][1] and plansza[0][1] !=0 or\
    plansza[0][2] == plansza[1][2] == plansza[2][2] and plansza[0][2] !=0 or\
    plansza[0][0] == plansza[1][1] == plansza[2][2] and plansza[0][0] !=0 or\
    plansza[0][2] == plansza[1][1] == plansza[2][0] and plansza[0][2] !=0 :
        tie = False
        return True
    if \
    plansza[0][0] != 0 and\
    plansza[0][1] != 0 and\
    plansza[0][2] != 0 and\
    plansza[1][0] != 0 and\
    plansza[1][1] != 0 and\
    plansza[1][2] != 0 and\
    plansza[2][0] != 0 and\
    plansza[2][1] != 0 and\
    plansza[2][2] != 0 :
        tie = True
        return True
    return False


@app.route("/gra/wygrana")
def wygrana():
    global tie
    if tie:
        return render_template('wygrana.html',znak = 0)
    return render_template('wygrana.html',znak = znak)