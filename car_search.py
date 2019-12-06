from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'vehicles'

mysql = MySQL(app)

@app.route("/home", methods=["GET", "POST"])
def home():
    drives = []
    sizes = []
    if request.method == "POST":
        # Condition
        condition = request.form.get("cond-dropdown", None)
        all_conds = request.form.get("allconds")
        fuel = request.form.get("fuel-dropdown", None)
        all_fuels = request.form.get("allfuels")
        title = request.form.get("title-dropdown", None)
        all_title = request.form.get("alltitles")
        trans = request.form.get("trans-dropdown", None)
        all_trans = request.form.get("alltrans")
        brand = request.form.get("brand-dropdown", None)
        drive1 = request.form.get("drives1")
        drive2 = request.form.get("drives2")
        drive3 = request.form.get("drives3")

        for gets in (drive1, drive2, drive3):
            if gets != None:
                drives.append(gets)
        size1 = request.form.get("sizes1")
        size2 = request.form.get("sizes2")
        size3 = request.form.get("sizes3")
        size4 = request.form.get("sizes4")

        for size in (size1, size2, size3, size4):
            if size != None:
                sizes.append(size)
        amount = request.form["amount"]
        # Input sanitize amount
        # isinstance(), built in python function to check whether the given variable is the given data type.
        if not isinstance(amount, int) or (int(amount) < 1 and int(amount) > 50000):
            amount = 50

        # All-inventory
        if brand == "all":
            cur = mysql.connection.cursor()
            star_query1 = f"SELECT year, manufacturer, make, condition_, cylinders, fuel, price, odometer, title_status, transmission, drive, type, image_url, paint_color "
            star_query2 = f"FROM cars "   
            star_query3 = f"WHERE title_status LIKE '{title}' "
            star_query4 = f"AND transmission LIKE '{trans}' "
            star_query5 = f"LIMIT {amount}" 
            cur.execute(star_query1+star_query2+star_query3+star_query4+star_query5)
            r = cur.fetchall()
            if len(r) == 0:
                return render_template("empty_list.html")
            cur.close()
            return render_template("inventory_view.html", r=r)        
        if condition != None:
            cur = mysql.connection.cursor()
            full_query1 = f"SELECT year, manufacturer, make, condition_, cylinders, fuel, price, odometer, title_status, transmission, drive, type, image_url, paint_color "
            full_query2 = f"FROM cars "
            # All-conds not checked, so proceed forward, if checked.
            if all_conds != None:
                full_query3 = f"WHERE manufacturer LIKE '{brand}' AND title_status LIKE '{title}' "
            elif all_conds == None:
                full_query3 = f"WHERE manufacturer LIKE '{brand}' AND title_status LIKE '{title}' AND condition_ LIKE '{condition}' "

            if all_fuels != None:
                full_query4 = f" "
            elif all_fuels == None:
                full_query4 = f"AND fuel LIKE '{fuel}' "

            if all_title != None:
                full_query5 = f" "
            elif all_title == None:
                full_query5 = f"AND title_status LIKE '{title}' "

            if all_trans != None:
                full_query6 = f" "
            elif all_trans == None:
                full_query6 = f"AND transmission LIKE '{trans}' "
            
            amount_query = f"LIMIT {amount} "
            print(full_query1+full_query2+full_query3+full_query4+full_query5+full_query6+amount_query)
            cur.execute(full_query1+full_query2+full_query3+full_query4+full_query5+full_query6+amount_query)
            r = cur.fetchall()
            if len(r) == 0:
                return render_template("empty_list.html") 
            cur.close()
            return render_template("inventory_view.html", r=r)
    else:
        return render_template("otherHome.html")
'''
@app.route("/<condition>", methods=["GET", "POST"])
def condition(condition):
    return f"<h1>{condition}</h1>"
    '''

if __name__ == "__main__":
    app.run(debug=True)


