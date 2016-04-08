from flask import Flask, render_template, request
import sqlite3 as lite

app = Flask(__name__)

dbname = 'test.db'
   
@app.route('/barbot')
def index():
    return render_template('index.html')
    
@app.route('/barbot/status', methods=['GET', 'POST'])
def status():
    callback = request.args.get('callback')
    json = str(callback) + "({"
    json += "})"
    return json

@app.route("/barbot/list_drinks") 
def list_drinks():
    con = lite.connect(dbname)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Drinks")
        rows = cur.fetchall()
        callback = request.args.get('callback')
        json = str(callback) + '({"list":['
        for row in rows:
            json += '{"id" : ' + '"' + str(row["ID"]) + '",'
            json += '"name" : ' + '"' + str(row["NAME"]) + '",'
            json += '"image" : ' + '"' + str(row["IMAGE"]) + '"},'
        json += "]})"
    return json
    
@app.route("/barbot/list_ingredients") 
def list_ingredients():
    con = lite.connect(dbname)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Ingredients ORDER BY NAME")
        rows = cur.fetchall()
        callback = request.args.get('callback')
        json = str(callback) + '({"list":['
        for row in rows:
            json += '{"id" : ' + '"' + str(row["ID"]) + '",'
            json += '"name" : ' + '"' + str(row["NAME"]) + '",'
            json += '"image" : ' + '"' + str(row["IMAGE"]) + '"},'
        json += "]})"
    return json
    
@app.route("/barbot/list_slots") 
def list_slots():
    con = lite.connect(dbname)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT Slot.ID, Ingredients.ID as INGREDIENT, Ingredients.NAME, Ingredients.IMAGE FROM Slot join Ingredients on Slot.INGREDIENT = Ingredients.ID")
        rows = cur.fetchall()
        callback = request.args.get('callback')
        json = str(callback) + '({"list":['
        for row in rows:
            json += '{"id" : ' + '"' + str(row["ID"]) + '",'
            json += '"ingredient" : ' + '"' + str(row["INGREDIENT"]) + '",'
            json += '"name" : ' + '"' + str(row["NAME"]) + '",'
            json += '"image" : ' + '"' + str(row["IMAGE"]) + '"},'
        json += "]})"
    return json

@app.route("/barbot/add_ingredient") 
def add_ingredient():
    con = lite.connect(dbname)
    with con:
        callback = request.args.get('callback')
        name = request.args.get('name')
        image = request.args.get('image')
        print(str(name) + ' - ' + str(image))
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute('INSERT INTO Ingredients (NAME, IMAGE) VALUES ("' + str(name) + '", "' + str(image) + '")')
        con.commit();
        json = str(callback) + '({"list":['
        json += "]})"
    return json

@app.route("/barbot/drink_info") 
def drink_info():
    con = lite.connect(dbname)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        drinkid = request.args.get('drinkid')
        callback = request.args.get('callback')
        sql = "select Drinks.NAME, Ingredients.NAME as INGREDIENT,  IngredientsToDrinks.AMOUNT, IngredientsToDrinks.PROVIDED, Drinks.IMAGE, Ingredients.IMAGE as INGREDIENTIMAGE, Slot.ID as SLOT "
        sql += "from Drinks join IngredientsToDrinks on Drinks.ID = IngredientsToDrinks.DRINKID join Ingredients on IngredientsToDrinks.INGREDIENT = Ingredients.ID left join Slot on Slot.INGREDIENT = Ingredients.ID "
        sql += "where Drinks.ID = " + str(drinkid)
        cur.execute(sql)
        rows = cur.fetchall()
        json = str(callback)
        if len(rows) > 0:
            json += '({ "name" : "' + rows[0]["NAME"] + '", '
            json += '"image" : "' + rows[0]["IMAGE"] + '", '
            json += '"ingredients" : ['
            for row in rows:
                json += '{ "ingredient" : ' + '"' + str(row["INGREDIENT"]) + '",'
                json += '"amout" : "' + str(row["AMOUNT"]) + '",'
                json += '"slot" : "' + str(row["SLOT"]) + '",'
                json += '"provided" : "' + str(row["PROVIDED"]) + '",'
                json += '"image" : "' + str(row["INGREDIENTIMAGE"]) + '"'
                json += '},'
            json += "]})"
        else:
            json += "({})"
    return json

@app.route("/barbot/order")
def order_drink():
    con = lite.connect(dbname)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        drinkid = request.args.get('drinkid')
        cur.execute("SELECT * FROM Drinks WHERE ID = " + str(drinkid))
        rows = cur.fetchone()
        print(len(rows))
        callback = request.args.get('callback')
        json = str(callback) + "({"
        for row in rows:
            json += '"id" : ' + '"' + str(row["ID"]) + '",'
            json += '"name" : ' + '"' + str(row["NAME"]) + '",'
            json += '"image" : ' + '"' + str(row["IMAGE"]) + '",'
            json += '"ingredients" : ' + '[' + str(row["INGREDIENTS"]) + ']'
        json += "})"
    return json

if __name__ == "__main__":
    app.run(host='0.0.0.0')