
from flask import Blueprint, request, render_template, session
import matplotlib.pyplot as plt
import mpld3

from Document_Store import update_stabilizer_shape, get_stabilizer_shape

ssdc_blueprint = Blueprint('ssdc_handlers', __name__)

@ssdc_blueprint.route('/ssdc_configuration', methods=['POST'])
def ssdc_configuration():
        if request.method == 'POST':
                username = session['username']
                submit = request.form['submit']
                wingspan = float(request.form['wingspan'])
                root_chord = float(request.form['root_chord'])
                w = float(request.form['fuselage_width_inches'])
                l = float(request.form['elevator_length_inches'])
                L = float(request.form['L'])
                output_units = request.form['output_units']

                if username is not None:
                    if submit == "save":
                        wingspan = int(wingspan) if wingspan % 1 == 0 else wingspan
                        root_chord = int(root_chord) if root_chord % 1 == 0 else root_chord
                        w = int(w) if w % 1 == 0 else w
                        l = int(l) if l % 1 == 0 else l
                        L = int(L) if L % 1 == 0 else L
                        new_data = {
                            "Username": username,
                            "Format": "SS",
                            "Wingspan": wingspan,
                            "Root_Chord": root_chord,
                            "Fuselage_Width": w,
                            "Elevator_Length": l,
                            "L_greater_elevator_length": L,
                            "Output_Units": True if output_units == "in" else False  # False == mm True == in
                        }

                        data = [wingspan, root_chord, w, l, L, output_units]
                        update_stabilizer_shape(username, new_data)
                        return render_template("Stabilizer_shape_design_calculator.html", save=1, data=data)


                    elif submit == "load":
                        ss_data = get_stabilizer_shape(username)
                        stabilizer = aircraft_design_calculator(ss_data[2], ss_data[3], ss_data[4], ss_data[5], ss_data[6], "in" if ss_data[7] else "mm")
                        wingspan = int(ss_data[2]) if ss_data[2] % 1 == 0 else ss_data[2]
                        root_chord = int(ss_data[3]) if ss_data[3] % 1 == 0 else ss_data[3]
                        w = int(ss_data[4]) if ss_data[4] % 1 == 0 else ss_data[4]
                        l = int(ss_data[5]) if ss_data[5] % 1 == 0 else ss_data[5]
                        L = int(ss_data[6]) if ss_data[6] % 1 == 0 else ss_data[6]
                        data = [wingspan, root_chord, w, l, L, "in" if ss_data[7] else "mm"]
                        return render_template("Stabilizer_shape_design_calculator.html", submit=1, fig2_html=stabilizer[0],
                                               fig3_html=stabilizer[1], data=data)


                if submit == "submit":

                # Call MATLAB function
                    result = aircraft_design_calculator(float(wingspan), float(root_chord), w, l, L, output_units)
                    wingspan = int(wingspan) if wingspan %1 == 0 else wingspan
                    root_chord = int(root_chord) if root_chord %1 == 0 else root_chord
                    w = int(w) if w %1 == 0 else w
                    l = int(l) if l %1 == 0 else l
                    L = int(L) if L %1 == 0 else L
                    data = [wingspan, root_chord, w, l, L, output_units]
                    return render_template("Stabilizer_shape_design_calculator.html", submit=1, fig2_html=result[0],
                                       fig3_html=result[1], data=data)


        return render_template("Stabilizer_shape_design_calculator.html")


def dim_text(ax, x, y, label, value, is_vertical):
        ax.text(x, y, f"{label}{value}", fontsize=8, va='center' if is_vertical else 'top',
                ha='center' if not is_vertical else 'left')





def in2mm(inch):
        return inch * 25.4
def aircraft_design_calculator(wing_span_select, root_chord_select, w, l, L, output_units):

    SA = root_chord_select * wing_span_select
    horizontal_stabilizer_SA = SA * 0.25
    elevator_SA = horizontal_stabilizer_SA * 0.25
    vertical_stabilizer_SA = SA * 0.10
    rudder_SA = vertical_stabilizer_SA * 0.25

    gap = 0.15

    if output_units == "mm":
        w = in2mm(w)
        l = in2mm(l)
        L = in2mm(L)
        A_HS = in2mm(horizontal_stabilizer_SA ** 0.5) ** 2
        A_E = in2mm(elevator_SA ** 0.5) ** 2
        A_VS = in2mm(vertical_stabilizer_SA ** 0.5) ** 2
        A_R = in2mm(rudder_SA ** 0.5) ** 2
        gap = in2mm(gap)
    else:
        A_HS = horizontal_stabilizer_SA
        A_E = elevator_SA
        A_VS = vertical_stabilizer_SA
        A_R = rudder_SA

    b = 0.5 * (A_E / l - w)
    a = (A_HS - L * b + l * b) / (w + b)
    h = A_R / l
    c = (A_VS - A_R - l * h - 0.5 * h * (a - 2 * l)) / (0.5 * (a - 2 * l))

    # Figure 2
    fig2, ax2 = plt.subplots()

    boundary = plt.Polygon([(0, 0), (0, l), (w + 2 * b, l), (w + 2 * b, 0)], edgecolor='black',
                           facecolor='lightcoral')
    ax2.add_patch(boundary)
    dim_text(ax2, w / 2 + b, gap, "Width = ", w + 2 * b, False)

    plt.sca(ax2)  # Set the current Axes instance

    boundary = plt.Polygon(
        [(0, l), (0, L), (b, l + a), (w + b, l + a), (w + 2 * b, L), (w + 2 * b, l)],
        edgecolor='black', facecolor='lightblue')
    ax2.add_patch(boundary)

    plt.plot([gap * 2, gap * 2], [0, l], 'k--', color='purple')
    dim_text(ax2, gap, l / 2, "l_E = ", l, True)

    plt.plot([gap * 3, gap * 3], [0, L], 'k:', color='green')
    dim_text(ax2, gap * 2, L / 2, "l_hs = ", L, True)

    plt.plot([b, b + w], [l + a - gap * 2, l + a - gap * 2], 'k--', color='brown')
    dim_text(ax2, b + w / 2, a + l - gap, "w = ", w, False)

    plt.plot([w + b, w + b], [l, l + a], 'k:', color='pink')
    dim_text(ax2, w + b - gap, l + a / 2, "a = ", a, True)

    plt.plot([w + b, w + 2 * b], [l + gap, l + gap], 'k--', color='blue')
    dim_text(ax2, w + b + 0.5 * b, l + 2 * gap, "b = ", b, False)

    ax2.set_aspect('equal', adjustable='box')
    ax2.axis('off')

    h = A_R / l
    c = (A_VS - A_R - l * h - 0.5 * h * (a - 2 * l)) / (0.5 * (a - 2 * l))

    # Figure 3
    fig3, ax3 = plt.subplots()

    boundary = plt.Polygon([(0, 0), (l, 0), (l, h), (0, h)], edgecolor='black', facecolor='lightcoral')
    ax3.add_patch(boundary)

    plt.sca(ax3)  # Set the current Axes instance

    boundary = plt.Polygon([(l, 0), (a, 0), (a, c), (2 * l, h), (l, h)], edgecolor='black',
                           facecolor='lightblue')
    ax3.add_patch(boundary)

    plt.plot([0, l], [h - gap, h - gap], 'k:', color='orange')
    dim_text(ax3, l / 2, h - gap * 2, "l = ", l, False)

    plt.plot([2 * l, l], [h - gap, h - gap], 'k--', color='red')
    dim_text(ax3, l / 2 + l, h - gap * 2, "l = ", l, False)

    plt.plot([a - gap, a - gap], [0, c], 'k:', color='purple')
    dim_text(ax3, a - gap * 2, c / 2, "c = ", c, True)

    dim_text(ax3, a / 2, gap, "a = ", a, False)

    ax3.set_aspect('equal', adjustable='box')
    ax3.axis('off')

    fig2_html = mpld3.fig_to_html(fig2)
    fig3_html = mpld3.fig_to_html(fig3)

    return [fig2_html, fig3_html]









