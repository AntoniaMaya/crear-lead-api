from flask import Flask, request, jsonify
import xmlrpc.client
import os

app = Flask(__name__)
CORS(app)

# Configuración de conexión a Odoo
odoo_url = "https://antoniamaya-zapier.odoo.com"
db = "antoniamaya-zapier-prod-20597647"
username = "antonia.maya@vanguardiaensistemas.com"
password = "123"

@app.route('/crear_lead', methods=['POST'])
def crear_lead():
    data = request.get_json()
    required_fields = ["name", "contact_name", "email_from", "phone"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        common = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/common")
        uid = common.authenticate(db, username, password, {})
        if not uid:
            return jsonify({"error": "Error de autenticación"}), 403

        models = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/object")
        lead_id = models.execute_kw(db, uid, password, 'crm.lead', 'create', [data])
        return jsonify({"mensaje": "Lead creado con éxito", "lead_id": lead_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
