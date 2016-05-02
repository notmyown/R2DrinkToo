from flask import Flask, render_template, request
import sqlite3 as lite
import barbot
import strings as s

app = Flask(__name__)

dbname = 'test.db'

global barbotInterface
   
@app.route('/barbot')
def index():
    return render_template('index.html')
    
@app.route('/barbot/status', methods=['GET', 'POST'])
def status():
    callback = request.args.get('callback')
    json = s.toString(callback) + "({"
    json += "})"
    return json

@app.route("/barbot/list_drinks") 
def list_drinks():
    callback = request.args.get('callback')
    con = lite.connect(dbname)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Drinks")
        rows = cur.fetchall()
        json = s.toString(callback) + '({"list":['
        for row in rows:
            json += '{"id" : ' + '"' + s.toString(row["ID"]) + '",'
            json += '"name" : ' + '"' + s.toString(row["NAME"]) + '",'
            json += '"image" : ' + '"' + s.toString(row["IMAGE"]) + '"},'
        json += "]})"
    return json

@app.route("/barbot/list_ingredients") 
def list_ingredients():
    callback = request.args.get('callback')
    con = lite.connect(dbname)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Ingredients ORDER BY NAME")
        rows = cur.fetchall()
        json = s.toString(callback) + '({"list":['
        for row in rows:
            json += '{"id" : ' + '"' + s.toString(row["ID"]) + '",'
            json += '"name" : ' + '"' + s.toString(row["NAME"]) + '",'
            json += '"image" : ' + '"' + s.toString(row["IMAGE"]) + '"},'
        json += "]})"
    return json
    
@app.route("/barbot/list_slots") 
def list_slots():
    callback = request.args.get('callback')
    con = lite.connect(dbname)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT Slot.ID, Ingredients.ID as INGREDIENT, Ingredients.NAME, Ingredients.IMAGE FROM Slot join Ingredients on Slot.INGREDIENT = Ingredients.ID")
        rows = cur.fetchall()
        json = s.toString(callback) + '({"list":['
        for row in rows:
            json += '{"id" : ' + '"' + s.toString(row["ID"]) + '",'
            json += '"ingredient" : ' + '"' + s.toString(row["INGREDIENT"]) + '",'
            json += '"name" : ' + '"' + s.toString(row["NAME"]) + '",'
            json += '"image" : ' + '"' + s.toString(row["IMAGE"]) + '"},'
        json += "]})"
    return json

@app.route("/barbot/add_ingredient") 
def add_ingredient():
    callback = request.args.get('callback')
    con = lite.connect(dbname)
    with con:
        name = request.args.get('name')
        image = request.args.get('image')
        s.debug(s.toString(name) + ' - ' + s.toString(image))
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute('INSERT INTO Ingredients (NAME, IMAGE) VALUES ("' + s.toString(name) + '", "' + s.toString(image) + '")')
        con.commit();
        json = s.toString(callback) + '({"list":['
        json += "]})"
    return json
    
@app.route("/barbot/add_cocktail") 
def add_cocktail():
    callback = request.args.get('callback')
    con = lite.connect(dbname)
    with con:
        name = request.args.get('name')
        image = request.args.get('image')
        ingredients = request.args.get('ingredients')
        
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute('INSERT INTO Drinks (NAME, IMAGE) VALUES ("' + s.toString(name) + '", "' + s.toString(image) + '")')
        splits = ingredients.split("-");
        drinkid = cur.lastrowid
        s.debug(s.toString(name) + ' - ' + s.toString(image) + " - " + s.toString(drinkid) + " - " + s.toString(splits))
        for splitme in splits:
            splits2 = splitme.split("_");
            if len(splits2) == 3:
                if splits2[2] == "on" or splits2[2] == "on-":
                    splits2[2] = s.toString(1)
                else:
                    splits2[2] = s.toString(0)
                cur.execute('INSERT INTO IngredientsToDrinks (DRINKID, INGREDIENT, AMOUNT, PROVIDED) VALUES ("' + s.toString(drinkid) + '", "' + s.toString(splits2[0]) + '","' + s.toString(splits2[1]) + '","' + s.toString(splits2[2]) + '")')
        con.commit();
        json = s.toString(callback) + '({"list":['
        json += "]})"
    return json

@app.route("/barbot/drink_info") 
def drink_info():
    callback = request.args.get('callback')
    con = lite.connect(dbname)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        drinkid = request.args.get('drinkid')
        sql = "select Drinks.NAME, Ingredients.NAME as INGREDIENT,  IngredientsToDrinks.AMOUNT, IngredientsToDrinks.PROVIDED, Drinks.IMAGE, Ingredients.IMAGE as INGREDIENTIMAGE, Slot.ID as SLOT "
        sql += "from Drinks join IngredientsToDrinks on Drinks.ID = IngredientsToDrinks.DRINKID join Ingredients on IngredientsToDrinks.INGREDIENT = Ingredients.ID left join Slot on Slot.INGREDIENT = Ingredients.ID "
        sql += "where Drinks.ID = " + s.toString(drinkid)
        cur.execute(sql)
        rows = cur.fetchall()
        json = s.toString(callback)
        if len(rows) > 0:
            json += '({ "name" : "' + rows[0]["NAME"] + '", '
            json += '"image" : "' + rows[0]["IMAGE"] + '", '
            json += '"drinkid" : "' + drinkid + '", '
            json += '"ingredients" : ['
            for row in rows:
                json += '{ "ingredient" : ' + '"' + s.toString(row["INGREDIENT"]) + '",'
                json += '"amount" : "' + s.toString(row["AMOUNT"]) + '",'
                json += '"slot" : "' + s.toString(row["SLOT"]) + '",'
                json += '"provided" : "' + s.toString(row["PROVIDED"]) + '",'
                json += '"image" : "' + s.toString(row["INGREDIENTIMAGE"]) + '"'
                json += '},'
            json += "]})"
        else:
            json += "({})"
    return json

@app.route("/barbot/order")
def order_drink():
    callback = request.args.get('callback')
    con = lite.connect(dbname)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        drinkid = request.args.get('drinkid')
        s.debug("Suche Drink mit ID " + s.toString(drinkid))
        sql = "select Drinks.NAME, Ingredients.NAME as INGREDIENT,  IngredientsToDrinks.AMOUNT, IngredientsToDrinks.PROVIDED, Slot.ID as SLOT "
        sql += "from Drinks join IngredientsToDrinks on Drinks.ID = IngredientsToDrinks.DRINKID join Ingredients on IngredientsToDrinks.INGREDIENT = Ingredients.ID left join Slot on Slot.INGREDIENT = Ingredients.ID "
        sql += "where Drinks.ID = " + s.toString(drinkid)
        cur.execute(sql)
        rows = cur.fetchall()
        f = [0] * barbotInterface.getPumpNum()
        s.debug(len(rows))
        
        for row in rows:
            slot = -1
            if not row["SLOT"] is None:
                slot = int(row["SLOT"])
            if slot > -1 and slot < barbotInterface.getPumpNum():
                f[slot-1] = int(row["AMOUNT"])
        s.debug("Ermittelte Pumpkonfiguration: " + s.toString(f))
        json = s.toString(callback) + '({"state": "' + barbotInterface.pumping(f) + '"})'
    return json

if __name__ == "__main__":
    barbotInterface = barbot.BarBot()
    s.defaultLevel = s.DEBUG
    try:
        app.run(host='0.0.0.0')
    finally:
        barbotInterface.shutdown()
        s.debug("Exit")