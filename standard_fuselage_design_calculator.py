import mpld3
import numpy as np
from flask import Blueprint, request, render_template, session

from matplotlib import pyplot as plt
from matplotlib.patches import Polygon

from Document_Store import update_standard_fuselage, get_standard_fuselage

sfdc_blueprint = Blueprint('sfdc_handlers', __name__)

@sfdc_blueprint.route('/sfdc_configuration', methods=['POST'])
def sfdc_configuration():
        if request.method == 'POST':
                username = session['username']
                submit = request.form['submit']
                wingspan = float(request.form['wingspan'])
                root_chord = float(request.form['root_chord'])
                height = float(request.form['height'])
                width = float(request.form['width'])
                incidence = float(request.form['incidence'])
                tail_end_height = float(request.form['tail_end_height'])
                output_units = request.form['output_units']
                accurate_drawing = request.form['accurate_drawing']
                if username is not None:
                    if submit == "save":
                        wingspan = int(wingspan) if wingspan % 1 == 0 else wingspan
                        root_chord = int(root_chord) if root_chord % 1 == 0 else root_chord
                        height = int(height) if height % 1 == 0 else height
                        width = int(width) if width % 1 == 0 else width
                        incidence = int(incidence) if incidence % 1 == 0 else incidence
                        tail_end_height = int(tail_end_height) if tail_end_height % 1 == 0 else tail_end_height
                        new_data = {
                            "Username": username,
                            "Format": "SF",
                            "Wingspan": wingspan,
                            "Root_Chord": root_chord,
                            "Fuselage_Height": height,
                            "Fuselage_Width": width,
                            "Tail_End_Height": tail_end_height,
                            "Angle_Of_Incidence": incidence,
                            "Output_Units": True if output_units == "in" else False,  # False == mm True == in
                            "accurate_drawing": False
                        }
                        update_standard_fuselage(username, new_data)
                        data = [wingspan, root_chord, height, width, incidence, tail_end_height, output_units,
                                accurate_drawing]
                        return render_template("standard_fuselage_design_calculator.html", save=1,data=data)

                    elif submit == "load":
                        sf_data = get_standard_fuselage(username)
                        fuselage = fuselage_design_calculator(sf_data[2], sf_data[3], sf_data[4], sf_data[5], sf_data[7],
                                                              sf_data[6], "in" if sf_data[8] else "mm", sf_data[9])
                        wingspan = int(sf_data[2]) if sf_data[2] % 1 == 0 else sf_data[2]
                        root_chord = int(sf_data[3]) if sf_data[3] % 1 == 0 else sf_data[3]
                        height = int(sf_data[4]) if sf_data[4] % 1 == 0 else sf_data[4]
                        width = int(sf_data[5]) if sf_data[5] % 1 == 0 else sf_data[5]
                        tail_end_height = int(sf_data[6]) if sf_data[6] % 1 == 0 else sf_data[6]
                        incidence = int(sf_data[7]) if sf_data[7] % 1 == 0 else sf_data[7]
                        data = [wingspan, root_chord, height, width, incidence, tail_end_height, "in" if sf_data[8] else "mm", sf_data[9]]
                        return render_template("standard_fuselage_design_calculator.html", submit=1, fig1_html=fuselage,data=data)

                if submit == "submit":
                    result = fuselage_design_calculator(wingspan, root_chord,  height, width, incidence, tail_end_height, output_units, accurate_drawing)

                    wingspan = int(wingspan) if wingspan % 1 == 0 else wingspan
                    root_chord = int(root_chord) if root_chord % 1 == 0 else root_chord
                    height = int(height) if height %1 == 0 else height
                    width = int(width) if width %1 == 0 else width
                    incidence= int(incidence) if incidence %1 == 0 else incidence
                    tail_end_height= int(tail_end_height) if tail_end_height %1 == 0 else tail_end_height



                    data =[wingspan, root_chord, height, width, incidence,tail_end_height, output_units,accurate_drawing ]
                    return render_template("standard_fuselage_design_calculator.html", submit=1, fig1_html=result, data=data)
        return render_template("standard_fuselage_design_calculator.html")


def text_for_dimension(x, y, desc, val, is_vert, output_units):
        text = f"{desc}{val}"
        if output_units:
                text += f" {output_units}"

        if is_vert:
                rotation = 'vertical'
                ha, va = 'center', 'center'
        else:
                rotation = 'horizontal'
                ha, va = 'center', 'bottom' if y < 0 else 'top'

        plt.text(x, y, text, rotation=rotation, ha=ha, va=va)





def fuselage_design_calculator(wing_span_select, root_chord_select, height, width, incidence, tail_end_height, output_units, accurate_drawing):




    # Calculate fuselage length
    ratio_fuselage_length = np.array([0.7, 0.75])
    fuselage_length = wing_span_select * ratio_fuselage_length
    fuselage_length_avg = np.mean(fuselage_length)

    # Calculate distances
    distance_LE2_prop = wing_span_select * 0.15
    distance_LE2_stabilizer = root_chord_select * 3


    # Outputs for Standard_Fuselage_Design_Calculator.m
    nose_to_wing_tip = distance_LE2_prop
    root_chord = root_chord_select
    wing_tip_to_stab = distance_LE2_stabilizer
    fuselage_length = fuselage_length_avg

    thickness = 3 / 16  # foam board thickness

    # Convert first
    if output_units == "mm":
        # Convert all relevant parameters to mm
        thickness = in2mm(thickness)
        height = in2mm(height)
        width = in2mm(width)
        tail_end_height = in2mm(tail_end_height)
        nose_to_wing_tip = in2mm(nose_to_wing_tip)
        root_chord = in2mm(root_chord)
        wing_tip_to_stab = in2mm(wing_tip_to_stab)
        fuselage_length = in2mm(fuselage_length)

    wing_mount_length = root_chord * np.cos(np.radians(incidence))
    wing_mount_depth = root_chord * np.sin(np.radians(incidence))
    foam_cutout_width = 2 * height + 2 * width + 3 * thickness
    vert_stab_edge_distance = (width - thickness) / 2
    hor_stab_top_distance = (height - tail_end_height - thickness) / 2
    taper_begin_length = nose_to_wing_tip + wing_mount_length
    taper_end_length = fuselage_length - taper_begin_length
    taper_end_foam_length = np.linalg.norm([taper_end_length, height - tail_end_height])

    fig1, ax1 = plt.subplots(figsize=(15, 8))

    foam_cutout_width = round(foam_cutout_width, 2)
    taper_end_length = round(taper_end_length, 2)
    taper_end_foam_length = round(taper_end_foam_length, 2)
    fuselage_length = round(fuselage_length, 2)
    thickness = round(thickness, 2)
    width = round(width, 2)
    height = round(height, 2)
    tail_end_height = round(tail_end_height, 2)
    taper_begin_length = round(taper_begin_length, 2)
    nose_to_wing_tip = round(nose_to_wing_tip, 2)
    root_chord = round(root_chord, 2)
    incidence = round(incidence, 2)
    wing_tip_to_stab = round(wing_tip_to_stab, 2)


    # Boundary
    boundary = Polygon([[0, taper_end_length - taper_end_foam_length],
                        [foam_cutout_width, taper_end_length - taper_end_foam_length],
                        [foam_cutout_width, fuselage_length],
                        [0, fuselage_length]], edgecolor='black', facecolor='lightblue')
    ax1.add_patch(boundary)

    # Dimension text for foam board width
    text_for_dimension(foam_cutout_width / 2, fuselage_length + thickness,
                       "Foam board width = ", foam_cutout_width, False, None)

    # Dimension text for foam board height
    text_for_dimension(-thickness, fuselage_length / 2,
                       "Foam board height = ", taper_begin_length + taper_end_foam_length, True,
                       None)

    # Fuselage sides
    # Top side
    top_side = Polygon([[0, 0], [width, 0], [width, fuselage_length], [0, fuselage_length]],
                       edgecolor='black', facecolor='lightgray')
    ax1.add_patch(top_side)

    # Dimension text for top/bottom
    text_for_dimension(width / 2, fuselage_length - thickness, "Top/bot = ", width, False, None)

    # Dimension text for top length
    text_for_dimension(thickness, fuselage_length / 2, "Top length = ", fuselage_length, True,
                       output_units)

    # Left side
    shift = width + thickness

    left_side = Polygon([[shift, shift], [shift + tail_end_height, 0],
                         [shift + height, 0], [shift + height, fuselage_length],
                         [shift, fuselage_length]], edgecolor='black', facecolor='lightcoral')
    ax1.add_patch(left_side)

    # Dimension text for l/r
    text_for_dimension(shift + height / 2, fuselage_length - thickness, "L/r = ", height, False,
                       None)

    # Dimension text for tail
    text_for_dimension(shift + tail_end_height / 2, thickness, "Tail = ", tail_end_height, False,
                       output_units)

    # Dimension text for untapered length
    text_for_dimension(shift + height - thickness, (fuselage_length + taper_begin_length) / 2,
                       "Untapered length = ", taper_begin_length, True, output_units)

    # Bottom side
    shift = shift + height + thickness
    bottom_side = Polygon(
        [[shift, shift], [shift + width, taper_end_length - taper_end_foam_length],
         [shift + width, fuselage_length], [shift, fuselage_length]],
        edgecolor='black', facecolor='lightyellow')
    ax1.add_patch(bottom_side)

    # Dimension text for bottom length
    text_for_dimension(shift + thickness, fuselage_length / 2,
                       "Bottom length = ", taper_begin_length + taper_end_foam_length, True,
                       output_units)

    shift = shift + width + thickness
    right_side = Polygon([[shift + height - tail_end_height, shift + height],
                          [shift + height, fuselage_length],
                          [shift, fuselage_length], [shift, shift + tail_end_height]],
                         edgecolor='black')
    ax1.add_patch(right_side)

    # Cutouts
    mount_back = fuselage_length - nose_to_wing_tip - root_chord * incidence

    # Wing mount
    wing_mount_vertices = [[0, width, width, 0],
                           [mount_back, mount_back + root_chord, mount_back + root_chord,
                            mount_back]]
    wing_mount = Polygon(np.array(wing_mount_vertices).T, closed=True, facecolor='white',
                         edgecolor='black')
    ax1.add_patch(wing_mount)

    # Dimension text for nose to wing
    text_for_dimension(width - thickness, fuselage_length - nose_to_wing_tip / 2,
                       "Nose to wing = ", nose_to_wing_tip, True, None)

    # Dimension text for wing chord
    text_for_dimension(width - thickness, mount_back + root_chord / 2,
                       "Wing chord = ", root_chord, True, output_units)

    # Shift for the next set of wing mounts
    shift = width + thickness

    # Wing mount at the shifted position
    wing_mount_vertices = [[shift, shift + root_chord * incidence, shift],
                           [mount_back, mount_back, mount_back + root_chord * incidence]]
    wing_mount = Polygon(np.array(wing_mount_vertices).T, facecolor='white', edgecolor='black')
    ax1.add_patch(wing_mount)

    # Dimension text for depth
    text_for_dimension(shift + thickness, mount_back - thickness,
                       "Depth = ", root_chord * incidence, False, None)

    # Shift for the next set of wing mounts
    shift = shift + 2 * thickness + 2 * height + width

    # Wing mount at the shifted position
    wing_mount_vertices = [[shift - root_chord * incidence, shift, shift],
                           [mount_back, mount_back, mount_back + root_chord * incidence]]
    wing_mount = Polygon(np.array(wing_mount_vertices).T, facecolor='white', edgecolor='black')
    ax1.add_patch(wing_mount)

    # Dimension text for depth
    text_for_dimension(shift - thickness, mount_back - thickness,
                       "Depth = ", root_chord * incidence, False, None)

    # Stabilizers
    plt.plot([0, foam_cutout_width], [fuselage_length - wing_tip_to_stab - nose_to_wing_tip,
                                      fuselage_length - wing_tip_to_stab - nose_to_wing_tip],
             color="black", linestyle=":")

    text_for_dimension(foam_cutout_width / 2,
                       fuselage_length - wing_tip_to_stab + thickness - nose_to_wing_tip,
                       "Stabilizers (distance from wing tip) = ", wing_tip_to_stab, False,
                       output_units)

    # Drawing adjustments
    ax1.set_xlim([0, foam_cutout_width])
    ax1.set_ylim([taper_end_length - taper_end_foam_length, fuselage_length])

    if accurate_drawing:
        ax1.set_aspect('equal', 'box')

    ax1.set_position([0, 0, 1, 1])
    ax1.set_xlim([0, foam_cutout_width])
    ax1.set_ylim([taper_end_length - taper_end_foam_length, fuselage_length])
    ax1.axis('off')
    plt.tight_layout()

    fig1_html = mpld3.fig_to_html(fig1)

    return fig1_html



# Helper function to convert inches to millimeters
def in2mm(inches):
    return inches * 25.4









