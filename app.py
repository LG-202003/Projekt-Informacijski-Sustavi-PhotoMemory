from flask import Flask, request, make_response, jsonify, render_template, redirect, url_for 
from pony import orm

DB = orm.Database()

app = Flask(__name__)

class Fotograf(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    ime_i_prezime = orm.Required(str)
    grad = orm.Required(str)
    broj_telefona = orm.Required(int)
    email = orm.Required(str)
    studio = orm.Required(str)
    cijena_po_satu = orm.Required(float)
    trenutna_dostupnost = orm.Required(bool)
    dogadaji = orm.Required(str)

DB.bind(provider="sqlite", filename="database_photographers.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)

def add_fotograf(json_request):
    try:
        ime_i_prezime = json_request["ime_i_prezime"]
        grad = json_request["grad"]
        broj_telefona = json_request["broj_telefona"]
        email = json_request["email"]
        studio = json_request["studio"]
        cijena_po_satu = json_request["cijena_po_satu"]
        trenutna_dostupnost = json_request["trenutna_dostupnost"]
        dogadaji = json_request["dogadaji"]

        with orm.db_session:
            Fotograf(ime_i_prezime=ime_i_prezime, grad=grad, broj_telefona=broj_telefona, email=email, studio=studio, cijena_po_satu=cijena_po_satu, trenutna_dostupnost=trenutna_dostupnost, dogadaji=dogadaji)
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}
    
def get_fotografe(filter_grad=None, filter_dostupan=None, max_cijena=None):
    try:
        with orm.db_session:
            query = orm.select(x for x in Fotograf)

            if filter_grad:
                query = query.filter(lambda x: x.grad.lower() == filter_grad.lower())

            if filter_dostupan is not None:
                query = query.filter(lambda x: x.trenutna_dostupnost == filter_dostupan)
            
            if max_cijena:
                max_cijena = float(max_cijena)
                query = query.filter(lambda x: x.cijena_po_satu <= max_cijena)

            result = [r.to_dict() for r in query]
            return {"response": "Success", "data": result}
        
    except Exception as e:
            return {"response": "Fail", "error": str(e)}
    
def get_fotograf_by_id(fotograf_id):
    try:
        with orm.db_session:
            result = Fotograf[fotograf_id].to_dict()
            response = {"response": "Success", "data": result}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}
    
def patch_fotograf(fotograf_id, json_request):
    try:
        with orm.db_session:
            to_update = Fotograf[fotograf_id]
            if 'ime_i_prezime' in json_request:
                to_update.ime_i_prezime = json_request['ime_i_prezime']
            if 'grad' in json_request:
                to_update.grad = json_request['grad']
            if 'broj_telefona' in json_request:
                to_update.broj_telefona = json_request['broj_telefona']
            if 'email' in json_request:
                to_update.email = json_request['email']
            if 'studio' in json_request:
                to_update.studio = json_request['studio']
            if 'cijena_po_satu' in json_request:
                to_update.cijena_po_satu = json_request['cijena_po_satu']
            if 'trenutna_dostupnost' in json_request:
                to_update.trenutna_dostupnost = json_request['trenutna_dostupnost']
            if 'dogadaji' in json_request:
                to_update.dogadaji = json_request['dogadaji']
            
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}
    
def delete_fotografa(fotograf_id):
    try:
        with orm.db_session:
            to_delete = Fotograf[fotograf_id]
            to_delete.delete()
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test_fotografi():
    with orm.db_session:
        svi = Fotograf.select()
        return "<br>".join([f"{f.id}: {f.ime_i_prezime}" for f in svi])

@app.route("/fotograf/dodaj", methods=["GET", "POST"])
def dodaj_fotografa():
    if request.method == "POST":
        ime_i_prezime = request.form.get("ime_i_prezime")
        grad = request.form.get("grad")
        broj_telefona = request.form.get("broj_telefona")
        email = request.form.get("email")
        studio = request.form.get("studio")
        cijena_po_satu = request.form.get("cijena_po_satu")
        trenutna_dostupnost = request.form.get("trenutna_dostupnost") == "on"
        dogadaji = request.form.get("dogadaji")

        json_request = {
            "ime_i_prezime": ime_i_prezime,
            "grad": grad,
            "broj_telefona": int(broj_telefona),
            "email": email,
            "studio": studio,
            "cijena_po_satu": float(cijena_po_satu),
            "trenutna_dostupnost": trenutna_dostupnost,
            "dogadaji": dogadaji
        }

        response = add_fotograf(json_request)

        if response["response"] == "Success":
            return redirect(url_for("vrati_fotografe_l"))
        else:
            return render_template("dodaj.html", error=response.get("error", "Nešto nije u redu"))
    return render_template("dodaj.html")

@app.route("/fotografi", methods=["GET"])
def vrati_fotografe():
    if request.args and 'id' in request.args:
        fotograf_id= int(request.args.get("id"))
        response = get_fotograf_by_id(fotograf_id)
        return make_response(jsonify(response), 200 if response["response"] == "Success" else 400)
    
    grad = request.args.get("grad")
    dostupan = request.args.get("dostupan")
    cijena = request.args.get("max_cijena")
    
    if dostupan is not None:
        dostupan = dostupan.lower() == "true"
    
    response = get_fotografe(filter_grad=grad, filter_dostupan=dostupan, max_cijena=cijena)
    return make_response(jsonify(response), 200 if response["response"] == "Success" else 400)

@app.route("/fotografi/stranica")
def vrati_fotografe_l():
    grad = request.args.get("grad")
    dostupan = request.args.get("dostupan")
    cijena = request.args.get("max_cijena")

    if dostupan is not None:
        dostupan = dostupan.lower() == "true"

    response = get_fotografe(filter_grad=grad, filter_dostupan=dostupan, max_cijena=cijena)
    if response["response"] == "Success":
        podaci = response["data"]
    else:
        podaci = []
    return render_template("vrati.html", data=podaci)

@app.route("/fotograf/<int:fotograf_id>", methods=["DELETE"])
def obrisi_fotografa(fotograf_id):
        response = delete_fotografa(fotograf_id)
        if response["response"] == "Success":
            return make_response(jsonify(response), 200)
        return make_response(jsonify(response), 400)

@app.route("/fotograf/<int:fotograf_id>/uredi", methods=["GET", "POST"])
def uredi_fotografa(fotograf_id):
    with orm.db_session:
        fotograf = Fotograf.get(id=fotograf_id)
        if not fotograf:
            return "Fotograf ne postoji", 404

        if request.method == "POST":
            fotograf.ime_i_prezime = request.form.get("ime_i_prezime")
            fotograf.grad = request.form.get("grad")
            fotograf.broj_telefona = int(request.form.get("broj_telefona"))
            fotograf.email = request.form.get("email")
            fotograf.studio = request.form.get("studio")
            fotograf.cijena_po_satu = float(request.form.get("cijena_po_satu"))
            fotograf.trenutna_dostupnost = request.form.get("trenutna_dostupnost") == "on"
            fotograf.dogadaji = request.form.get("dogadaji")

            return redirect(url_for("vrati_fotografe_l"))
    return render_template("uredi.html", fotograf=fotograf)

@app.route('/statistika/cijene')
def statistika_cijena():
    with orm.db_session:
        gradovi = orm.select(f.grad for f in Fotograf)[:]
        jedinstveni_gradovi = list(set(gradovi))

        x_axis = []
        y_axis = []

        for grad in jedinstveni_gradovi:
            fotografi_u_gradu = orm.select(f for f in Fotograf if f.grad == grad)[:]
            if fotografi_u_gradu:
                prosjecna = sum(f.cijena_po_satu for f in fotografi_u_gradu) / len(fotografi_u_gradu)
                x_axis.append(grad)
                y_axis.append(round(prosjecna, 2))

        return render_template("graf.html", x_axis=x_axis, y_axis=y_axis)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)