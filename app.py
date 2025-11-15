from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def to_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        # Input Retrieval
        capacity = to_float(request.form.get("capacity"))
        recovery = to_float(request.form.get("recovery"))
        design_flux = to_float(request.form.get("design_flux"))
        membrane_area = to_float(request.form.get("membrane_area"))
        backwash_flux = to_float(request.form.get("backwash_flux"))
        CEB_flux = to_float(request.form.get("CEB_flux"))
        caustic_flux = to_float(request.form.get("caustic_flux"))
        caustic_dosing_conc = to_float(request.form.get("caustic_dosing_conc"))
        caustic_available_conc_in_percent = to_float(request.form.get("caustic_available_conc_in_percent"))
        hcl_dosing_conc = to_float(request.form.get("hcl_dosing_conc"))
        hcl_available_conc_in_percent = to_float(request.form.get("hcl_available_conc_in_percent"))
        naOCI_dosing_conc = to_float(request.form.get("naOCI_dosing_conc"))
        naOCI_available_conc_in_percent = to_float(request.form.get("naOCI_available_conc_in_percent"))
        cip_flux = to_float(request.form.get("cip_flux"))
        cip_pump_capacity = to_float(request.form.get("cip_pump_capacity"))

        

        # Results Calculation
        feed_flow = capacity / (recovery / 100)
        feed_pump_capacity = feed_flow / 0.9 if feed_flow else 0
        no_of_membranes = feed_flow * 1000 / (design_flux * membrane_area) if design_flux and membrane_area else 0
        no_of_membranes_in_ceil = math.ceil(no_of_membranes)
        backwash_pump_capacity = no_of_membranes_in_ceil * backwash_flux * membrane_area / 1000
        CEB_pump_flow_rate = no_of_membranes_in_ceil * CEB_flux * membrane_area / 1000 if membrane_area else 0
        caustic_dosing_pump_capacity = CEB_pump_flow_rate * caustic_dosing_conc * 1000 / (45 * 10000)
        hcl_dosing_pump_capacity = CEB_pump_flow_rate * hcl_dosing_conc * 1000 / (33 * 10000)
        naOCI_dosing_pump_capacity = CEB_pump_flow_rate * naOCI_dosing_conc * 1000 / (8 * 10000)
        cip_pump_capacity_skid = math.ceil(cip_pump_capacity)


        return jsonify({
            "status": "success",
            "results": {
                "feed_flow": feed_flow,
                "feed_pump_capacity": round(feed_pump_capacity, 4),
                "no_of_membranes": round(no_of_membranes, 4),
                "no_of_membranes_in_ceil": no_of_membranes_in_ceil,
                "backwash_pump_capacity": round(backwash_pump_capacity, 4),
                "CEB_pump_flow_rate": round(CEB_pump_flow_rate, 4),
                "caustic_dosing_pump_capacity": round(caustic_dosing_pump_capacity, 6),
                "hcl_dosing_pump_capacity": round(hcl_dosing_pump_capacity, 6),
                "naOCI_dosing_pump_capacity": round(naOCI_dosing_pump_capacity, 6),
                "cip_pump_capacity_skid": cip_pump_capacity_skid
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
