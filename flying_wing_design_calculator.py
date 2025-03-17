# route_handlers.py

from flask import Blueprint, request, render_template, session

from Document_Store import update_flying_wing, get_flying_wing

fwdc_blueprint = Blueprint('fwdc_handlers', __name__)

@fwdc_blueprint.route('/fwdc_configuration', methods=['POST'])
def fwdc_configuration():
        if request.method == 'POST':
                username = session['username']
                submit = request.form['submit']
                wingspan = float(request.form['wingspan'])
                root_chord = float(request.form['root_chord'])
                tip_chord = float(request.form['tip_chord'])
                chassis_width = float(request.form['chassis_width'])
                sweep_angle = float(request.form['sweep_angle'])
                output_units = request.form['output_units']



                if username is not None:
                    if submit == "save":
                        wingspan = int(wingspan) if wingspan % 1 == 0 else wingspan
                        root_chord = int(root_chord) if root_chord % 1 == 0 else root_chord
                        tip_chord = int(tip_chord) if tip_chord % 1 == 0 else tip_chord
                        chassis_width = int(chassis_width) if chassis_width % 1 == 0 else chassis_width
                        sweep_angle = int(sweep_angle) if sweep_angle % 1 == 0 else sweep_angle

                        new_data = {
                            "Username": username,
                            "Format": "FW",
                            "Wingspan": wingspan,
                            "Tip_Chord": tip_chord,
                            "Root_Chord": root_chord,
                            "Chassis_Width": chassis_width,
                            "Sweep_Angle": sweep_angle,
                            "Output_Units": True if output_units == "in" else False  # False == mm True == in
                        }
                        update_flying_wing(username, new_data)
                        data = [wingspan, root_chord, tip_chord, chassis_width, sweep_angle, output_units]
                        return render_template("flying_wing_design_calculator.html", save=1, data=data)

                    elif submit == "load":

                        fw_data = get_flying_wing(username)
                        wing_length = round(flying_wing_design(fw_data[2], fw_data[4], fw_data[3], fw_data[5], fw_data[6],
                                                               "in" if fw_data[7] else "mm"), 2)
                        wingspan = int(fw_data[2]) if fw_data[2] % 1 == 0 else fw_data[2]
                        root_chord = int(fw_data[4]) if fw_data[4] % 1 == 0 else fw_data[4]
                        tip_chord = int(fw_data[3]) if fw_data[3] % 1 == 0 else fw_data[3]
                        chassis_width = int(fw_data[5]) if fw_data[5] % 1 == 0 else fw_data[5]
                        sweep_angle = int(fw_data[6]) if fw_data[6] % 1 == 0 else fw_data[6]
                        data = [wingspan, root_chord, tip_chord, chassis_width, sweep_angle, "in" if fw_data[7] else "mm", wing_length]
                        return render_template("flying_wing_design_calculator.html", submit=1, data=data)

                if submit == "submit":
                    # Call the MATLAB function
                    wing_length= round(flying_wing_design(wingspan, root_chord, tip_chord, chassis_width, sweep_angle, output_units),2)
                    wingspan = int(wingspan) if wingspan % 1 == 0 else wingspan
                    root_chord = int(root_chord) if root_chord % 1 == 0 else root_chord
                    tip_chord = int(tip_chord) if tip_chord % 1 == 0 else tip_chord
                    chassis_width = int(chassis_width) if chassis_width % 1 == 0 else chassis_width
                    sweep_angle = int(sweep_angle) if sweep_angle % 1 == 0 else sweep_angle


                    data =[wingspan, root_chord, tip_chord, chassis_width, sweep_angle, output_units, wing_length]
                    return render_template("flying_wing_design_calculator.html", submit=1, data=data)
        return render_template("flying_wing_design_calculator.html")


import numpy as np

def flying_wing_design(wingspan, root_chord, tip_chord, chassis_width, sweep_angle, output_units):
    # Adjustable parameters
    thickness = 3 / 16
    elevon_area = 1 / 8

    # Make graphs look pretty (optional)
    # These settings can be adjusted based on personal preferences
    # For simplicity, they are not translated directly from MATLAB
    # Use matplotlib or other libraries for more customization if needed


    # Convert units if necessary
    if output_units == "mm":
        wingspan = in2mm(wingspan)
        root_chord = in2mm(root_chord)
        chassis_width = in2mm(chassis_width)

    # Calculate parameters
    wing_span = wingspan / 2
    chassis_width = chassis_width / 2
    wing_length = wing_span / np.cos(np.radians(sweep_angle))

    # Calculate elevon dimensions
    elevon_area_total = elevon_area * root_chord * wing_span
    elevon_span = np.sqrt(elevon_area_total / elevon_area)  # square root to get span
    elevon_chord = elevon_area / elevon_span  # chord is area/span

    return wing_length

# Convert inch to mm. Accepts arrays.
def in2mm(inch):
    return inch * 25.4







