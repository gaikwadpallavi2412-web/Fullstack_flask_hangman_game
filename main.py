from flask import Flask,render_template,request,session
import random
app=Flask(__name__)
app.secret_key="fgheiurjk"

def choose_random_word(Hint=""):
    guess_list = {
                    "Programming Language": ["PYTHON", "RECURSION", "ALGORITHM", "INHERITANCE", "COMPILER"],
                    "AI Tools": ["MIDJOURNEY", "GEMINI", "CANVA", "GITHUBCOPILOT", "PERPLEXITY"],
                    "Roles": ["TESTER", "SUPPORT", "DEVELOPER", "ARCHITECTURE", "ANALYST"]
                 }

    hint_list=list(guess_list.keys())
    if len(Hint)==0:
        Hint=0
        random.shuffle(hint_list)
        return hint_list[0]
    else:
        random.shuffle(guess_list[Hint])
        return guess_list[Hint][0]

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/home',methods=['POST','GET'])
def home():
    session['Hint']=choose_random_word()
    session['s_word']=choose_random_word(Hint=session.get('Hint')) #to select the secrete word  #s_word=choose_random_word(guess_list,Hint=Hint) #to select the secrete word
    session['incorrect_guess']=[]
    session['num_of_wrong_guess']=6
    session['b_list']=["-" for i in range(len(session.get('s_word')))]
    session['score']=0
    return render_template("home.html",Hint=session['Hint'],score=session['score'],b_list=session['b_list'],lives=session['num_of_wrong_guess'],incorrect_guess=session["incorrect_guess"])

@app.route('/update',methods=["POST"])
def update():
    guess=request.form.get('action')
    score=session.get('score')
    num_of_wrong_guess=session.get('num_of_wrong_guess')
    s_word=session.get('s_word')
    b_list=session.get('b_list')
    
    incorrect_guess=session.get('incorrect_guess')
    if (request.method=="POST"):
        if(num_of_wrong_guess>0 and b_list.count("-")!=0):
            if(guess in s_word):            #If the letter predicted by user is in secrete word
                    
                    num_of_wrong_guess=num_of_wrong_guess
                    if(s_word.count(guess)>1):          #to check if s_word has many occurances of guess'ed letter
                        for j in range(len(s_word)):
                            if(guess==s_word[j]):
                                b_list[j]=guess
                    else:                                       #else s_word has 1 occurances of guess'ed letter
                        b_list[s_word.find(guess)]=guess
                        
            else:                                   #If the letter predicted by user is not in secrete word
                num_of_wrong_guess=num_of_wrong_guess-1  #reduce the no.of lives count by 
                #if (score>0):
                #    score=score-10
                #else:
                #    score=score
                incorrect_guess.append(guess)  
        session['incorrect_guess']=incorrect_guess
        session['num_of_wrong_guess']=num_of_wrong_guess
        session['b_list']=b_list
        session['score']=score
        
    return render_template("home.html",Hint=session['Hint'],score=session['score'],b_list=session['b_list'],lives=session['num_of_wrong_guess'],incorrect_guess=session["incorrect_guess"])




if __name__=="__main__":
    app.run(debug=True)