from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/citynet'
app.config['SQLALCHEMY_ECHO']= True
db = SQLAlchemy(app)
app.secret_key = 'shhhh...iAmASecret!'

class Users(db.Model):

    __tablename__ = "users"

    login = db.Column(db.String(255))
    password = db.Column(db.String(255))
    id = db.Column(db.Integer, primary_key=True)

class Buxgalter(db.Model):

    __tablename__ = "buxgalter"

    login = db.Column(db.String(255))
    password = db.Column(db.String(255))
    id = db.Column(db.Integer, primary_key=True)

class Limite(db.Model):

    __tablename__="limite"

    name = db.Column(db.String(255))
    limits = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)

class Cards(db.Model):

    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    discount = db.Column(db.Integer)
class Cards2(db.Model):

    __tablename__ = "cards2"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    discount = db.Column(db.Integer)

class Cards3(db.Model):

    __tablename__ = "cards3"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    discount = db.Column(db.Integer)

class Cards4(db.Model):

    __tablename__ = "cards4"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    discount = db.Column(db.Integer)

class Workers(db.Model):

    __tablename__ = "workers"

    name = db.Column(db.String(255))
    year = db.Column(db.Integer)
    id = db.Column(db.String(255), primary_key=True)
    company = db.Column(db.String(255))
    limits = db.Column(db.Integer)

class Companies(db.Model):

    __tablename__ = "companies"

    company = db.Column(db.String(255))
    id = db.Column(db.Integer, primary_key=True)
    tier = db.Column(db.Integer)

class Report(db.Model):

    __tablename__ = "report"

    name = db.Column(db.String(255))
    buyer = db.Column(db.String(255))
    ydate = db.Column(db.Integer)
    mdate = db.Column(db.Integer)
    ddate = db.Column(db.Integer)
    hdate = db.Column(db.Integer)
    mindate = db.Column(db.Integer)
    buyerid = db.Column(db.String(255))
    seller = db.Column(db.String(255))
    sum = db.Column(db.String(255))
    discount = db.Column(db.String(255))
    id = db.Column(db.Integer, primary_key=True)

class Cardcontr(db.Model):

    __tablename__ = "cardcontr"

    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.String(255))
    food = db.Column(db.Integer)
    med = db.Column(db.Integer)
    edc = db.Column(db.Integer)
    drugoe = db.Column(db.Integer)

GlobUserId = 0
GlobSum = 0
GlobTier = ''
GlobDiscount = 0
GlobTotal = 0
GlobCard = ''
GlobDisc = 0
GlobName = ''
GlobUserComp = ''
GlobRepId = 0
GlobDate = ''
GlobDatet =''
GlobLogInUserId = 0;
GlobCardDiscount = 0;
GlobalLimit = 0;


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=["POST", "GET"])
def getvalue():
    name = request.form['name']
    password = request.form['password']
    companies = Companies.query.all()
    ErrorMessage = "Check your login and password!"
    global GlobLogInUserId
    if name != "" and password != "":
        getuser = Users.query.filter_by(login=name).first()
        checker = getuser is None
        if checker == True:
            getuser = Buxgalter.query.filter_by(login=name).first()
            checker = getuser is None
            if checker == True:
                return render_template('home.html', ErrorMessage=ErrorMessage )
            else:
                userlogin = getuser.login
                userPass = getuser.password
                GlobLogInUserId = getuser.id
                if userlogin == name and userPass == password:
                    return render_template('preReport.html', companies=companies)
                else:
                    return render_template('home.html', ErrorMessage=ErrorMessage )
        else:
            userlogin = getuser.login
            userPass = getuser.password
            userid = getuser.id
            if userid == 0 and password == userPass:
                return render_template('pass.html')
            elif userid == 999 and password == userPass:
                GlobLogInUserId = 999
                return render_template('preReport.html' , companies=companies)
            elif password == userPass and userlogin == name:
                GlobLogInUserId = getuser.id
                return render_template('search.html')
            else:
                return render_template('home.html', ErrorMessage=ErrorMessage )
    else:
        return render_template('home.html', ErrorMessage=ErrorMessage )


@app.route('/search', methods=['POST', 'GET'])
def search():
    global GlobUserId
    global GlobUserId
    global GlobSum
    global GlobTier
    global GlobDiscount
    global GlobTotal
    global GlobCard
    global GlobDisc
    global GlobName
    global GlobUserComp
    global GlobLogInUserId
    global GlobalLimit


    if request.method == 'POST':
        submit = request.form['submit']
        if submit == 'Назад':
            return render_template('home.html')
        elif submit == 'Посчитать':
            userid = request.form['userid']
            getuser = Workers.query.filter_by(id=userid).first()
            usersum = request.form['sum']
            usersum = usersum.replace(" ","")
            usersum = int(usersum)

            selltiers = int(GlobLogInUserId)

            ErrorMessage = "Проверьте введенные данные!"
            if userid != "" and usersum > 0 and selltiers != 0 :
                getuser = Workers.query.filter_by(id=userid).first()
                checker = getuser is None

                if checker != True:
                    Uname = getuser.name
                    Uyear = getuser.year
                    Ucompany = getuser.company
                    userlim = getuser.limits

                    spliter = str(usersum)
                    dlina = len(spliter)
                    if dlina == 4:
                        spliter = spliter[:1] + ' ' + spliter[1:]
                    elif dlina == 5:
                        spliter = spliter[:2] + ' ' + spliter[2:]
                    elif dlina == 6:
                        spliter = spliter[:3] + ' ' + spliter[3:]
                    elif dlina == 7:
                        spliter = spliter[:1] + ' ' + spliter[1:4]+ ' ' + spliter[4:]
                    elif dlina == 8:
                        spliter = spliter[:2] + ' ' + spliter[2:5]+ ' ' + spliter[5:]
                    elif dlina == 9:
                        spliter = spliter[:3] + ' ' + spliter[3:6]+ ' ' + spliter[6:]
                    elif dlina == 10:
                        spliter = spliter[:1] + ' ' + spliter[1:4]+ ' ' + spliter[4:7]+ ' ' + spliter[7:]


                    usersum = int(usersum)
                    sellinfo = Companies.query.filter_by(id=selltiers).first()

                    tier = int(sellinfo.tier)

                    sellcomp = sellinfo.company
                    if tier == 1:
                        if Uyear >= 3 and Uyear < 5:
                            actives = Cardcontr.query.filter_by(id=1).first()
                            check = int(actives.food)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=1).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 5 and Uyear < 7:
                            actives = Cardcontr.query.filter_by(id=2).first()
                            check = int(actives.food)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=2).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 7 and Uyear < 10:
                            actives = Cardcontr.query.filter_by(id=3).first()
                            check = int(actives.food)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=3).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 10:
                            actives = Cardcontr.query.filter_by(id=4).first()
                            check = int(actives.food)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=4).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)


                    elif tier == 2:
                        if Uyear >= 3 and Uyear < 5:
                            actives = Cardcontr.query.filter_by(id=1).first()
                            check = int(actives.med)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=1).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 5 and Uyear < 7:
                            actives = Cardcontr.query.filter_by(id=2).first()
                            check = int(actives.med)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=2).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 7 and Uyear < 10:
                            actives = Cardcontr.query.filter_by(id=3).first()
                            check = int(actives.med)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=3).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 10:
                            actives = Cardcontr.query.filter_by(id=4).first()
                            check = int(actives.med)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=4).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)


                    elif tier == 3:
                        if Uyear >= 3 and Uyear < 5:
                            actives = Cardcontr.query.filter_by(id=1).first()
                            check = int(actives.edc)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=1).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 5 and Uyear < 7:
                            actives = Cardcontr.query.filter_by(id=2).first()
                            check = int(actives.edc)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=2).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 7 and Uyear < 10:
                            actives = Cardcontr.query.filter_by(id=3).first()
                            check = int(actives.edc)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=3).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 10:
                            actives = Cardcontr.query.filter_by(id=4).first()
                            check = int(actives.edc)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=4).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)


                    elif tier == 4:
                        if Uyear >= 3 and Uyear < 5:
                            actives = Cardcontr.query.filter_by(id=1).first()
                            check = int(actives.drugoe)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=1).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 5 and Uyear < 7:
                            actives = Cardcontr.query.filter_by(id=2).first()
                            check = int(actives.drugoe)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=2).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 7 and Uyear < 10:
                            actives = Cardcontr.query.filter_by(id=3).first()
                            check = int(actives.drugoe)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=3).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)
                        elif Uyear >= 10:
                            actives = Cardcontr.query.filter_by(id=4).first()
                            check = int(actives.drugoe)
                            if check == 1:
                                cardinfo = Cards.query.filter_by(id=4).first()
                                discount = int(cardinfo.discount)
                                card = cardinfo.name
                            elif check == 2:
                                ErrorMessage = "Статус карты не совпадает"
                                return render_template('search.html', ErrorMessage=ErrorMessage)


                    userlim = int(userlim)

                    if userlim == 0:
                        if Uyear >= 3 and Uyear < 5:
                            newlim = Limite.query.filter_by(id=1).first()
                            limit = int(newlim.limits)
                        elif Uyear >= 5 and Uyear < 7:
                            newlim = Limite.query.filter_by(id=2).first()
                            limit = int(newlim.limits)
                        elif Uyear >= 7 and Uyear < 10:
                            newlim = Limite.query.filter_by(id=3).first()
                            limit = int(newlim.limits)
                        elif Uyear >= 10:
                            newlim = Limite.query.filter_by(id=4).first()
                            limit = int(newlim.limits)

                        update = Workers.query.filter_by(id=userid).first()
                        update.limits = limit
                        db.session.commit()

                    discount = int(discount)
                    discsum = usersum * discount

                    discsum = discsum // 100 #discounted sum
                    limite = int(getuser.limits)
                    limite = limite - discsum

                    if limite > 0:
                        GlobalLimit = limite
                        totalpay = usersum - discsum #сумма оставшаящя для оплаты

                        discountspliter = str(discsum)
                        disdlina = len(discountspliter)
                        if disdlina == 4:
                            discountspliter = discountspliter[:1] + ' ' + discountspliter[1:]
                        elif disdlina == 5:
                            discountspliter = discountspliter[:2] + ' ' + discountspliter[2:]
                        elif disdlina == 6:
                            discountspliter = discountspliter[:3] + ' ' + discountspliter[3:]
                        elif disdlina == 7:
                            discountspliter = discountspliter[:1] + ' ' + discountspliter[1:4]+ ' ' + discountspliter[4:]
                        elif disdlina == 8:
                            discountspliter = discountspliter[:2] + ' ' + discountspliter[2:5]+ ' ' + discountspliter[5:]
                        elif disdlina == 9:
                            discountspliter = discountspliter[:3] + ' ' + discountspliter[3:6]+ ' ' + discountspliter[6:]
                        elif disdlina == 10:
                            discountspliter = discountspliter[:1] + ' ' + discountspliter[1:4]+ ' ' + discountspliter[4:7]+ ' ' + discountspliter[7:]


                        GlobDiscount = discountspliter
                        GlobTotal = totalpay
                        GlobCard = card
                        GlobDisc = discount
                        GlobName = Uname
                        GlobUserId = userid
                        GlobSum = spliter
                        GlobUserComp = Ucompany
                        GlobTier = sellcomp

                        totalpaysplit = str(totalpay)
                        totaldlina = len(totalpaysplit)
                        if totaldlina == 4:
                            totalpaysplit = totalpaysplit[:1] + ' ' + totalpaysplit[1:]
                        elif totaldlina == 5:
                            totalpaysplit = totalpaysplit[:2] + ' ' + totalpaysplit[2:]
                        elif totaldlina == 6:
                            totalpaysplit = totalpaysplit[:3] + ' ' + totalpaysplit[3:]
                        elif totaldlina == 7:
                            totalpaysplit = totalpaysplit[:1] + ' ' + totalpaysplit[1:4]+ ' ' + totalpaysplit[4:]
                        elif totaldlina == 8:
                            totalpaysplit = totalpaysplit[:2] + ' ' + totalpaysplit[2:5]+ ' ' + totalpaysplit[5:]
                        elif totaldlina == 9:
                            totalpaysplit = totalpaysplit[:3] + ' ' + totalpaysplit[3:6]+ ' ' + totalpaysplit[6:]
                        elif totaldlina == 10:
                            totalpaysplit = totalpaysplit[:1] + ' ' + totalpaysplit[1:4]+ ' ' + totalpaysplit[4:7]+ ' ' + totalpaysplit[7:]
                        return render_template('search2.html', Uname = Uname, discount = discount, usersum=spliter, Ucompany = Ucompany, discsum=discountspliter, totalpay=totalpaysplit, card=card, sellcomp=sellcomp, userid=userid)
                    else:
                        ErrorMessages = "Недостаток лимита! Остаток:"
                        nedostatok = Workers.query.filter_by(id=userid).first()
                        lime = nedostatok.limits
                        limespliter = str(lime)
                        disdlina = len(limespliter)
                        if disdlina == 4:
                            limespliter = limespliter[:1] + ' ' + limespliter[1:]
                        elif disdlina == 5:
                            limespliter = limespliter[:2] + ' ' + limespliter[2:]
                        elif disdlina == 6:
                            limespliter = limespliter[:3] + ' ' + limespliter[3:]
                        elif disdlina == 7:
                            limespliter = limespliter[:1] + ' ' + limespliter[1:4]+ ' ' + limespliter[4:]
                        elif disdlina == 8:
                            limespliter = limespliter[:2] + ' ' + limespliter[2:5]+ ' ' + limespliter[5:]
                        elif disdlina == 9:
                            limespliter = limespliter[:3] + ' ' + limespliter[3:6]+ ' ' + limespliter[6:]
                        elif disdlina == 10:
                            limespliter = limespliter[:1] + ' ' + limespliter[1:4]+ ' ' + limespliter[4:7]+ ' ' + limespliter[7:]
                        return render_template('search.html', ErrorMessage=ErrorMessages , lime=limespliter)
                else:
                    return render_template('search.html', ErrorMessage=ErrorMessage)
            else:
                return render_template('search.html', ErrorMessage=ErrorMessage)


@app.route('/search2', methods=['POST', 'GET'])
def search2():
    global GlobUserId
    global GlobSum
    global GlobTier
    global GlobDiscount
    global GlobTotal
    global GlobCard
    global GlobDisc
    global GlobName
    global GlobUserComp
    global GlobalLimit


    limite = int(GlobalLimit)


    checker = False
    idchecker = 1
    while checker != True:
        getuser = Report.query.filter_by(id=idchecker).first()
        idchecker += 1
        checker = getuser is None
        if checker == True:
            break

    idchecker -= 1
    time = datetime.now()
    tyear = time.year
    tmonth = time.month
    tday = time.day
    thour = time.hour
    tminute = time.minute
    userid = int(GlobUserId)

    if request.method == 'POST':
        submit = request.form['submit']
        if submit == 'Печать/Сохранить':
            update = Workers.query.filter_by(id=userid).first()
            update.limits = limite
            db.session.commit()

            reportinsert = Report(name=GlobName, buyer=GlobUserComp, ydate=tyear, mdate=tmonth, ddate=tday, hdate=thour, mindate=tminute, buyerid=GlobUserId, seller=GlobTier, sum=GlobSum, discount=GlobDiscount, id=idchecker)
            db.session.add(reportinsert)
            db.session.commit()
            return render_template('search.html')
        else:
            return render_template('search.html')


@app.route('/adminpage', methods=['POST', 'GET'])
def adminpage():
    companies = Companies.query.all()
    if request.method == 'POST':
        submit = request.form['submit']
        if submit == 'Компанию':
            return render_template('companiya.html')
            #return redirect(url_for('reports'))
        elif submit == 'Персонал':
            return render_template('registration.html', companies=companies)
        elif submit == 'Карту':
            return render_template('cardpass.html')
        elif submit == 'Назад':
            return render_template('home.html')


@app.route('/discountpass', methods=['POST', 'GET'])
def discountpass():
    if request.method == 'POST':
        submit = request.form['submit']
        if submit == 'Назад':
            return render_template('cardpass.html')
        else:
            global GlobCardDiscount
            option = int(request.form['compn'])
            GlobCardDiscount = option
            if option == 1:
                silver = Cards.query.filter_by(id=1).first()
                gold = Cards.query.filter_by(id=2).first()
                premium = Cards.query.filter_by(id=3).first()
                infinity = Cards.query.filter_by(id=4).first()
                return render_template('discount.html', silver = silver, gold = gold, premium = premium, infinity = infinity)
            elif option == 2:
                silver2 = Cards2.query.filter_by(id=1).first()
                gold2 = Cards2.query.filter_by(id=2).first()
                premium2 = Cards2.query.filter_by(id=3).first()
                infinity2 = Cards2.query.filter_by(id=4).first()
                return render_template('discount.html', silver = silver2, gold = gold2, premium = premium2, infinity = infinity2)
            elif option == 3:
                silver3 = Cards3.query.filter_by(id=1).first()
                gold3 = Cards3.query.filter_by(id=2).first()
                premium3 = Cards3.query.filter_by(id=3).first()
                infinity3 = Cards3.query.filter_by(id=4).first()
                return render_template('discount.html', silver = silver3, gold = gold3, premium = premium3, infinity = infinity3)
            elif option == 4:
                silver4 = Cards4.query.filter_by(id=1).first()
                gold4 = Cards4.query.filter_by(id=2).first()
                premium4 = Cards4.query.filter_by(id=3).first()
                infinity4 = Cards4.query.filter_by(id=4).first()
                return render_template('discount.html', silver = silver4, gold = gold4, premium = premium4, infinity = infinity4)



@app.route('/discount', methods=['POST', 'GET'])
def discount():
    global GlobCardDiscount
    Silver = int(request.form['SILVER'])
    Gold = int(request.form['GOLD'])
    Premium = int(request.form['PREMIUM'])
    Infinity = int(request.form['INFINITY'])
    if request.method == 'POST':
        submit = request.form['submit']
        if submit == 'Назад':
            return render_template('discountpass.html')
        else:
            tier = int(GlobCardDiscount)
            if tier == 1:
                if Silver != 0 and Gold != 0 and Premium != 0 and Infinity != 0:
                    update = Cards.query.filter_by(id=1).first()
                    update2 = Cards.query.filter_by(id=2).first()
                    update3 = Cards.query.filter_by(id=3).first()
                    update4 = Cards.query.filter_by(id=4).first()
                    update.discount = Silver
                    update2.discount = Gold
                    update3.discount = Premium
                    update4.discount = Infinity
                    db.session.commit()
                    return render_template('cardpass.html')

                elif Silver != 0:
                    if Gold != 0:
                        if Premium != 0:
                            update = Cards.query.filter_by(id=1).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update.discount = Silver
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update = Cards.query.filter_by(id=1).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update.discount = Silver
                            update2.discount = Gold
                            db.session.commit()
                            return render_template('cardpass.html')
                    else:
                        if Premium != 0:
                            if Infinity != 0:
                                update = Cards.query.filter_by(id=1).first()
                                update4 = Cards.query.filter_by(id=4).first()
                                update3 = Cards.query.filter_by(id=3).first()
                                update.discount = Silver
                                update4.discount = Infinity
                                update3.discount = Premium
                                db.session.commit()
                                return render_template('cardpass.html')
                            else:
                                update = Cards.query.filter_by(id=1).first()
                                update3 = Cards.query.filter_by(id=3).first()
                                update.discount = Silver
                                update3.discount = Premium
                                db.session.commit()
                                return render_template('cardpass.html')
                        else:
                            if Infinity != 0:
                                update = Cards.query.filter_by(id=1).first()
                                update.discount = Silver
                                update4 = Cards.query.filter_by(id=4).first()
                                update4.discount = Infinity
                                db.session.commit()
                                return render_template('cardpass.html')
                            else:
                                update = Cards.query.filter_by(id=1).first()
                                update.discount = Silver
                                db.session.commit()
                                return render_template('cardpass.html')
                elif Gold != 0:
                    if Premium != 0:
                        if Infinity != 0:
                            update4 = Cards.query.filter_by(id=4).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update4.discount = Infinity
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                    else:
                        if Infinity != 0:
                            update2 = Cards.query.filter_by(id=2).first()
                            update4 = Cards.query.filter_by(id=4).first()
                            update2.discount = Gold
                            update4.discount = Infinity
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update2 = Cards.query.filter_by(id=2).first()
                            update2.discount = Gold
                            db.session.commit()
                            return render_template('cardpass.html')
                elif Premium != 0:
                    if Infinity != 0:
                        update4 = Cards.query.filter_by(id=4).first()
                        update3 = Cards.query.filter_by(id=3).first()
                        update4.discount = Infinity
                        update3.discount = Premium
                        db.session.commit()
                        return render_template('cardpass.html')
                    else:
                        update3 = Cards.query.filter_by(id=3).first()
                        update3.discount = Premium
                        db.session.commit()
                        return render_template('cardpass.html')
                else:
                    update4 = Cards.query.filter_by(id=4).first()
                    update4.discount = Infinity
                    db.session.commit()
                    return render_template('cardpass.html')

            elif tier == 2:
                if Silver != 0 and Gold != 0 and Premium != 0 and Infinity != 0:
                    update = Cards2.query.filter_by(id=1).first()
                    update2 = Cards2.query.filter_by(id=2).first()
                    update3 = Cards2.query.filter_by(id=3).first()
                    update4 = Cards2.query.filter_by(id=4).first()
                    update.discount = Silver
                    update2.discount = Gold
                    update3.discount = Premium
                    update4.discount = Infinity
                    db.session.commit()
                    return render_template('cardpass.html')
                elif Silver != 0:
                    if Gold != 0:
                        if Premium != 0:
                            update = Cards.query.filter_by(id=1).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update.discount = Silver
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update = Cards.query.filter_by(id=1).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update.discount = Silver
                            update2.discount = Gold
                            db.session.commit()
                            return render_template('cardpass.html')
                    else:
                        if Premium != 0:
                            if Infinity != 0:
                                update = Cards.query.filter_by(id=1).first()
                                update4 = Cards.query.filter_by(id=4).first()
                                update3 = Cards.query.filter_by(id=3).first()
                                update.discount = Silver
                                update4.discount = Infinity
                                update3.discount = Premium
                                db.session.commit()
                                return render_template('cardpass.html')
                            else:
                                update = Cards.query.filter_by(id=1).first()
                                update3 = Cards.query.filter_by(id=3).first()
                                update.discount = Silver
                                update3.discount = Premium
                                db.session.commit()
                                return render_template('cardpass.html')
                        else:
                            if Infinity != 0:
                                update = Cards.query.filter_by(id=1).first()
                                update.discount = Silver
                                update4 = Cards.query.filter_by(id=4).first()
                                update4.discount = Infinity
                                db.session.commit()
                                return render_template('cardpass.html')
                            else:
                                update = Cards.query.filter_by(id=1).first()
                                update.discount = Silver
                                db.session.commit()
                                return render_template('cardpass.html')
                elif Gold != 0:
                    if Premium != 0:
                        if Infinity != 0:
                            update4 = Cards.query.filter_by(id=4).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update4.discount = Infinity
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                    else:
                        if Infinity != 0:
                            update2 = Cards.query.filter_by(id=2).first()
                            update4 = Cards.query.filter_by(id=4).first()
                            update2.discount = Gold
                            update4.discount = Infinity
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update2 = Cards.query.filter_by(id=2).first()
                            update2.discount = Gold
                            db.session.commit()
                            return render_template('cardpass.html')
                elif Premium != 0:
                    if Infinity != 0:
                        update4 = Cards.query.filter_by(id=4).first()
                        update3 = Cards.query.filter_by(id=3).first()
                        update4.discount = Infinity
                        update3.discount = Premium
                        db.session.commit()
                        return render_template('cardpass.html')
                    else:
                        update3 = Cards.query.filter_by(id=3).first()
                        update3.discount = Premium
                        db.session.commit()
                        return render_template('cardpass.html')
                else:
                    update4 = Cards.query.filter_by(id=4).first()
                    update4.discount = Infinity
                    db.session.commit()
                    return render_template('cardpass.html')

            elif tier == 3:
                if Silver != 0 and Gold != 0 and Premium != 0 and Infinity != 0:
                    update = Cards3.query.filter_by(id=1).first()
                    update2 = Cards3.query.filter_by(id=2).first()
                    update3 = Cards3.query.filter_by(id=3).first()
                    update4 = Cards3.query.filter_by(id=4).first()
                    update.discount = Silver
                    update2.discount = Gold
                    update3.discount = Premium
                    update4.discount = Infinity
                    db.session.commit()
                    return render_template('cardpass.html')
                elif Silver != 0:
                    if Gold != 0:
                        if Premium != 0:
                            update = Cards.query.filter_by(id=1).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update.discount = Silver
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update = Cards.query.filter_by(id=1).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update.discount = Silver
                            update2.discount = Gold
                            db.session.commit()
                            return render_template('cardpass.html')
                    else:
                        if Premium != 0:
                            if Infinity != 0:
                                update = Cards.query.filter_by(id=1).first()
                                update4 = Cards.query.filter_by(id=4).first()
                                update3 = Cards.query.filter_by(id=3).first()
                                update.discount = Silver
                                update4.discount = Infinity
                                update3.discount = Premium
                                db.session.commit()
                                return render_template('cardpass.html')
                            else:
                                update = Cards.query.filter_by(id=1).first()
                                update3 = Cards.query.filter_by(id=3).first()
                                update.discount = Silver
                                update3.discount = Premium
                                db.session.commit()
                                return render_template('cardpass.html')
                        else:
                            if Infinity != 0:
                                update = Cards.query.filter_by(id=1).first()
                                update.discount = Silver
                                update4 = Cards.query.filter_by(id=4).first()
                                update4.discount = Infinity
                                db.session.commit()
                                return render_template('cardpass.html')
                            else:
                                update = Cards.query.filter_by(id=1).first()
                                update.discount = Silver
                                db.session.commit()
                                return render_template('cardpass.html')
                elif Gold != 0:
                    if Premium != 0:
                        if Infinity != 0:
                            update4 = Cards.query.filter_by(id=4).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update4.discount = Infinity
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                    else:
                        if Infinity != 0:
                            update2 = Cards.query.filter_by(id=2).first()
                            update4 = Cards.query.filter_by(id=4).first()
                            update2.discount = Gold
                            update4.discount = Infinity
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update2 = Cards.query.filter_by(id=2).first()
                            update2.discount = Gold
                            db.session.commit()
                            return render_template('cardpass.html')
                elif Premium != 0:
                    if Infinity != 0:
                        update4 = Cards.query.filter_by(id=4).first()
                        update3 = Cards.query.filter_by(id=3).first()
                        update4.discount = Infinity
                        update3.discount = Premium
                        db.session.commit()
                        return render_template('cardpass.html')
                    else:
                        update3 = Cards.query.filter_by(id=3).first()
                        update3.discount = Premium
                        db.session.commit()
                        return render_template('cardpass.html')
                else:
                    update4 = Cards.query.filter_by(id=4).first()
                    update4.discount = Infinity
                    db.session.commit()
                    return render_template('cardpass.html')

            elif tier == 4:
                if Silver != 0 and Gold != 0 and Premium != 0 and Infinity != 0:
                    update = Cards4.query.filter_by(id=1).first()
                    update2 = Cards4.query.filter_by(id=2).first()
                    update3 = Cards4.query.filter_by(id=3).first()
                    update4 = Cards4.query.filter_by(id=4).first()
                    update.discount = Silver
                    update2.discount = Gold
                    update3.discount = Premium
                    update4.discount = Infinity
                    db.session.commit()
                    return render_template('cardpass.html')
                elif Silver != 0:
                    if Gold != 0:
                        if Premium != 0:
                            update = Cards.query.filter_by(id=1).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update.discount = Silver
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update = Cards.query.filter_by(id=1).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update.discount = Silver
                            update2.discount = Gold
                            db.session.commit()
                            return render_template('cardpass.html')
                    else:
                        if Premium != 0:
                            if Infinity != 0:
                                update = Cards.query.filter_by(id=1).first()
                                update4 = Cards.query.filter_by(id=4).first()
                                update3 = Cards.query.filter_by(id=3).first()
                                update.discount = Silver
                                update4.discount = Infinity
                                update3.discount = Premium
                                db.session.commit()
                                return render_template('cardpass.html')
                            else:
                                update = Cards.query.filter_by(id=1).first()
                                update3 = Cards.query.filter_by(id=3).first()
                                update.discount = Silver
                                update3.discount = Premium
                                db.session.commit()
                                return render_template('cardpass.html')
                        else:
                            if Infinity != 0:
                                update = Cards.query.filter_by(id=1).first()
                                update.discount = Silver
                                update4 = Cards.query.filter_by(id=4).first()
                                update4.discount = Infinity
                                db.session.commit()
                                return render_template('cardpass.html')
                            else:
                                update = Cards.query.filter_by(id=1).first()
                                update.discount = Silver
                                db.session.commit()
                                return render_template('cardpass.html')
                elif Gold != 0:
                    if Premium != 0:
                        if Infinity != 0:
                            update4 = Cards.query.filter_by(id=4).first()
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update4.discount = Infinity
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update2 = Cards.query.filter_by(id=2).first()
                            update3 = Cards.query.filter_by(id=3).first()
                            update2.discount = Gold
                            update3.discount = Premium
                            db.session.commit()
                            return render_template('cardpass.html')
                    else:
                        if Infinity != 0:
                            update2 = Cards.query.filter_by(id=2).first()
                            update4 = Cards.query.filter_by(id=4).first()
                            update2.discount = Gold
                            update4.discount = Infinity
                            db.session.commit()
                            return render_template('cardpass.html')
                        else:
                            update2 = Cards.query.filter_by(id=2).first()
                            update2.discount = Gold
                            db.session.commit()
                            return render_template('cardpass.html')
                elif Premium != 0:
                    if Infinity != 0:
                        update4 = Cards.query.filter_by(id=4).first()
                        update3 = Cards.query.filter_by(id=3).first()
                        update4.discount = Infinity
                        update3.discount = Premium
                        db.session.commit()
                        return render_template('cardpass.html')
                    else:
                        update3 = Cards.query.filter_by(id=3).first()
                        update3.discount = Premium
                        db.session.commit()
                        return render_template('cardpass.html')
                else:
                    update4 = Cards.query.filter_by(id=4).first()
                    update4.discount = Infinity
                    db.session.commit()
                    return render_template('cardpass.html')



@app.route('/cardpass', methods=['POST', 'GET'])
def cardpass():
    silver = Limite.query.filter_by(id=1).first()
    gold = Limite.query.filter_by(id=2).first()
    premium = Limite.query.filter_by(id=3).first()
    infinity = Limite.query.filter_by(id=4).first()
    if request.method == 'POST':
        submit = request.form['submit']
        if submit == 'Скидки':
            return render_template('discountpass.html')
        elif submit == 'Лимит':
            return render_template('limit.html', silver= silver, gold=gold, premium= premium, infinity=infinity)
        elif submit == 'Взаимодействие':
            return render_template('spliter.html')
        elif submit == 'Назад':
            return render_template('pass.html')


@app.route('/spliter', methods=['POST', 'GET'])
def spliter():
    if request.method == 'POST':
        submit = request.form['submit']
        if submit == 'Изменения':
            return render_template('cardconnect.html')
        elif submit == 'Статус':
            return redirect(url_for('cardstatus'))
        elif submit == 'Назад':
            return render_template('cardpass.html')

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    ErrorMessage = "Заполните все поля"
    companies = Companies.query.all()
    newuser = request.form['name']
    newyear = request.form['year']
    newcomp = int(request.form['compn'])
    newuserid = request.form['userid']



    if newuser == "" or newyear == "" or newcomp == 0 or newuserid == "":
        return render_template('registration.html', ErrorMessage=ErrorMessage, companies=companies)

    newdata = int(newyear)
    newcompany = int(newcomp)

    newyear = int(newyear)
    if newyear >= 3 and newyear < 5:
        newlim = Limite.query.filter_by(id=1).first()
        limit = newlim.limits
    elif newyear >= 5 and newyear < 7:
        newlim = Limite.query.filter_by(id=2).first()
        limit = newlim.limits
    elif newyear >= 7 and newyear < 10:
        newlim = Limite.query.filter_by(id=3).first()
        limit = newlim.limits
    elif newyear >= 10:
        newlim = Limite.query.filter_by(id=4).first()
        limit = newlim.limits

    companew = Companies.query.filter_by(id=newcompany).first()
    sellcomp = companew.company

    addnewuser = Workers(name=newuser, year=newdata, id=newuserid, company=sellcomp, limits = limit)
    db.session.add(addnewuser)
    db.session.commit()

    return render_template('pass.html')

@app.route('/reports', methods=['POST', 'GET'])
def reports():
    global GlobRepId
    global GlobUserId
    global GlobDate
    global GlobDatet
    check = int(GlobRepId)
    a,b,c = (int(x) for x in GlobDate.split('-'))
    e,f,g = (int(x) for x in GlobDatet.split('-'))
    if check == 999:
        reportdata = Report.query.filter(Report.ydate.between(a,e),Report.mdate.between(b,f)).all()
        checker = reportdata is None
        if checker != True:
            return render_template('reports.html', reportdata=reportdata)
        else:
            return render_template('reports.html')
    else:
        getuser = Companies.query.filter_by(id=check).first()
        getcomp = getuser.company
        reportdata = Report.query.filter(Report.seller==getcomp,Report.ydate.between(a,e),Report.mdate.between(b,f)).all()

        checker = reportdata is None
        if checker != True:
            return render_template('reports.html', reportdata=reportdata)
        else:
            return render_template('reports.html')

@app.route('/companiya', methods=['POST', 'GET'])
def companiya():
    checker = False
    idchecker = 1
    while checker != True:
        getuser = Companies.query.filter_by(id=idchecker).first()
        idchecker += 1
        checker = getuser is None

    newcompany = request.form['newcompany']
    newcompanyid = int(request.form['compn'])
    newulogin = request.form['cashierlogin']
    newblogin = request.form['buxlogin']
    newpass = request.form['passcashier']
    newbuxpass = request.form['passbux']
    idchecker -= 1

    addnewuser = Companies(company=newcompany, id=idchecker, tier=newcompanyid)
    db.session.add(addnewuser)
    db.session.commit()

    addcashierlogin = Users(login = newulogin, password = newpass, id = newcompanyid)
    db.session.add(addcashierlogin)
    db.session.commit()

    addbuxgalterlogin = Buxgalter(login = newblogin, password = newbuxpass, id = newcompanyid)
    db.session.add(addbuxgalterlogin)
    db.session.commit()


    return render_template('pass.html')

@app.route('/preReport', methods=['POST', 'GET'])
def preReport():
    global GlobRepId
    global GlobDate
    global GlobDatet
    global GlobLogInUserId

    reportid = GlobLogInUserId
    fromdate = request.form['from']
    todate = request.form['to']
    GlobRepId = reportid
    GlobDate = fromdate
    GlobDatet = todate
    return redirect(url_for('reports'))

@app.route('/limit', methods=['POST','GET'])
def limit():
    silver = Limite.query.filter_by(id=1).first()
    gold = Limite.query.filter_by(id=2).first()
    premium = Limite.query.filter_by(id=3).first()
    infinity = Limite.query.filter_by(id=4).first()
    if request.method == 'POST':
        submit = request.form['submit']
        if submit == 'Назад':
            return render_template('cardpass.html')
        else:
            tip = int(request.form['compn'])
            if tip == 2:
                limitsum = request.form['limits2']
            elif tip == 3:
                limitsum = request.form['limits3']
            elif tip == 4:
                limitsum = request.form['limits4']
            elif tip == 1:
                limitsum = request.form['limits']
            limitsum = limitsum.replace(" ","")
            limitsum=int(limitsum)
            update = Limite.query.filter_by(id=tip).first()
            update.limits = limitsum
            db.session.commit()
            return render_template('limit.html', silver= silver, gold=gold, premium= premium, infinity=infinity)

@app.route('/cardstatus', methods=['POST','GET'])
def cardstatus():
    getstatus = Cardcontr.query.filter_by(id=1).first()
    getstatus2 = Cardcontr.query.filter_by(id=2).first()
    getstatus3 = Cardcontr.query.filter_by(id=3).first()
    getstatus4 = Cardcontr.query.filter_by(id=4).first()

    return render_template('status.html', getstatus=getstatus, getstatus2=getstatus2, getstatus3=getstatus3, getstatus4=getstatus4)

@app.route('/cardcontrol', methods=['POST','GET'])
def cardcontrol():
    if request.method == 'POST':
        submit = request.form['submit']
        if submit == 'Назад':
            return render_template('cardpass.html')
        elif submit == 'Изменить':
            #общепит контроль карт
            goldinfo = int(request.form['gold'])
            if goldinfo != 0:
                update = Cardcontr.query.filter_by(id=1).first()
                update.food = goldinfo

            silverinfo = int(request.form['silver'])
            if silverinfo != 0:
                update = Cardcontr.query.filter_by(id=2).first()
                update.food = silverinfo

            premiuminfo = int(request.form['premium'])
            if premiuminfo != 0:
                update = Cardcontr.query.filter_by(id=3).first()
                update.food = premiuminfo

            infinityinfo = int(request.form['infinity'])
            if infinityinfo != 0:
                update = Cardcontr.query.filter_by(id=4).first()
                update.food = infinityinfo

            #Медицина контроль карт
            goldinfo2 = int(request.form['gold2'])
            if goldinfo2 != 0:
                update = Cardcontr.query.filter_by(id=1).first()
                update.med = goldinfo2

            silverinfo2 = int(request.form['silver2'])
            if silverinfo2 != 0:
                update = Cardcontr.query.filter_by(id=2).first()
                update.med = silverinfo2

            premiuminfo2 = int(request.form['premium2'])
            if premiuminfo2 != 0:
                update = Cardcontr.query.filter_by(id=3).first()
                update.med = premiuminfo2

            infinityinfo2 = int(request.form['infinity2'])
            if infinityinfo2 != 0:
                update = Cardcontr.query.filter_by(id=4).first()
                update.med = infinityinfo2

            #Образование контроль карт
            goldinfo3 = int(request.form['gold3'])
            if goldinfo3 != 0:
                update = Cardcontr.query.filter_by(id=1).first()
                update.edc = goldinfo3

            silverinfo3 = int(request.form['silver3'])
            if silverinfo3 != 0:
                update = Cardcontr.query.filter_by(id=2).first()
                update.edc = silverinfo3

            premiuminfo3 = int(request.form['premium3'])
            if premiuminfo3 != 0:
                update = Cardcontr.query.filter_by(id=3).first()
                update.edc = premiuminfo3

            infinityinfo3 = int(request.form['infinity3'])
            if infinityinfo3 != 0:
                update = Cardcontr.query.filter_by(id=4).first()
                update.edc = infinityinfo3

            #Прочие контроль карт
            goldinfo4 = int(request.form['gold4'])
            if goldinfo4 != 0:
                update = Cardcontr.query.filter_by(id=1).first()
                update.drugoe = goldinfo4

            silverinfo4 = int(request.form['silver4'])
            if silverinfo4 != 0:
                update = Cardcontr.query.filter_by(id=2).first()
                update.drugoe = silverinfo4

            premiuminfo4 = int(request.form['premium4'])
            if premiuminfo4 != 0:
                update = Cardcontr.query.filter_by(id=3).first()
                update.drugoe = premiuminfo4

            infinityinfo4 = int(request.form['infinity4'])
            if infinityinfo4 != 0:
                update = Cardcontr.query.filter_by(id=4).first()
                update.drugoe = infinityinfo4

            db.session.commit()
            return render_template('cardpass.html')



if __name__=="__main__":
    app.run(debug=True)