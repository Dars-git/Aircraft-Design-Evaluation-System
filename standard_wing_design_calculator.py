import mpld3
import numpy as np
from flask import Blueprint, request, render_template, session
from pymongo import MongoClient
from matplotlib import pyplot as plt

from Document_Store import update_standard_wing, get_standard_wing

swdc_blueprint = Blueprint('swdc_handlers', __name__)

@swdc_blueprint.route('/swdc_configuration', methods=['POST'])
def swdc_configuration():
        if request.method == 'POST':

                username = session['username']
                submit = request.form['submit']
                wingspan = float(request.form['wingspan'])
                root_chord = float(request.form['root_chord'])
                output_units = request.form['output_units']
                accurate_drawing = request.form['accurate_drawing']
                BW_Regions = request.form['bw_regions']

                if username is not None:
                        if submit == "save":
                                wingspan = int(wingspan) if wingspan % 1 == 0 else wingspan
                                root_chord = int(root_chord) if root_chord % 1 == 0 else root_chord
                                new_data = {
                                        "Username": username,
                                        "Format": "SW",
                                        "Wingspan": wingspan,
                                        "Root_Chord": root_chord,
                                        "Output_Units": True if output_units == "in" else False,
                                        # False == mm True == in
                                        "accurate_drawing": True,
                                        "bw_regions": False
                                }
                                update_standard_wing(username, new_data)

                                data = [wingspan, root_chord, output_units, accurate_drawing, BW_Regions]
                                return render_template("standard_wing_design_calculator.html", save=1, data=data)


                        elif submit == "load":
                                sw_data = get_standard_wing(username)
                                wing = wing_design_calculator(sw_data[2], sw_data[3], "in" if sw_data[4] else "mm", sw_data[5], sw_data[6])
                                wingspan = int(sw_data[2]) if sw_data[2] % 1 == 0 else sw_data[2]
                                root_chord = int(sw_data[3]) if sw_data[3] % 1 == 0 else sw_data[3]
                                data = [wingspan, root_chord, "in" if sw_data[4] else "mm", sw_data[5], sw_data[6]]
                                return render_template("standard_wing_design_calculator.html", submit=1, fig1_html=wing[0], fig2_html=wing[1], data=data)


                if submit == "submit":

                        result = wing_design_calculator(wingspan, root_chord, output_units, accurate_drawing, BW_Regions)
                        wingspan = int(wingspan) if wingspan % 1 == 0 else wingspan
                        root_chord = int(root_chord) if root_chord % 1 == 0 else root_chord
                        data=[wingspan, root_chord, output_units, accurate_drawing, BW_Regions]
                        return render_template("standard_wing_design_calculator.html", submit=1, fig1_html=result[0], fig2_html=result[1], data=data)
        return render_template("standard_wing_design_calculator.html")

def dim_text(x, y, label, value, horizontal):
    plt.text(x, y, f"{label}{value}", fontsize=10, ha='center' if horizontal else 'right', va='center' if not horizontal else 'top')

def an_text(ax, x, y, text):
    ax.annotate(text, (x, y), fontsize=8, ha='center', va='center')



def wing_design_calculator(wing_span_select, root_chord_select, output_units, accurate_drawing, bw_regions):


        # Calculate wing thickness
        ratio_wing_thick = [0.12, 0.14]
        wing_thick = [root_chord_select * ratio for ratio in ratio_wing_thick]
        wing_thick_avg = sum(wing_thick) / len(wing_thick)

        # Calculate aileron surface area
        SA = root_chord_select * wing_span_select
        ratio_aileron_SA = [0.10, 0.12]
        aileron_SA = [SA * ratio for ratio in ratio_aileron_SA]

        def in2mm(inch):
                return inch * 25.4


        thickness = 3 / 16  # foam board thickness, inches

        # Convert units
        if output_units == "mm":
            t = in2mm(thickness)
            h = in2mm(wing_thick_avg)
            r = in2mm(root_chord_select)
            A = [in2mm(sa ** 0.5) ** 2 for sa in aileron_SA]
            w = in2mm(wing_span_select)
            l_ea = in2mm(1)
        else:
            t = thickness
            h = wing_thick_avg
            r = root_chord_select
            A = aileron_SA
            w = wing_span_select
            l_ea = 1

        cog = [0.20 * r, 0.30 * r]
        l_3 = max(cog) - min(cog)
        cog_avg = sum(cog) / len(cog)
        l_12 = ((h ** 2) + (cog_avg ** 2)) ** 0.5  # Pythagoras Theorem
        l_4 = ((h ** 2) + ((r - cog_avg - l_3) ** 2)) ** 0.5
        l_a = 0.25 * w  # length of aileron (one only)
        l_5 = round((min(A) * 0.5) / l_a, 1)
        l_5 = l_5 - l_5 % 0.25 + 0.25
        l_a = int(l_a)
        if (l_a * l_5 * 2) > max(A):
            l_5 = l_5 - 0.25

        l = r + l_12 + l_3 + l_4 + l_5
        l = l - l % 0.25 + 0.25
        l_1 = l_12 / 2 + t
        l_2 = l_12 - l_1
        l_1 = round(l_1 + t / 2, 2)
        l_2 = round(l_2 - t / 2, 2)
        l_3 = round(l_3, 2)
        l_4 = round(l_4, 2)
        cog_avg = round(cog_avg, 2)

        w = round(w, 2)
        l = round(l, 2)
        t = round(t, 2)
        r = round(r, 2)
        l_5 = round(l_5, 2)
        l_ea = round(l_ea, 2)
        l_a = round(l_a, 2)
        h = round(h, 2)

        # Figure 1
        fig1, ax1 = plt.subplots()

        boundary = plt.Polygon([[0, 0], [0, l], [w, l], [w, 0]], closed=True,
                               edgecolor='black' if bw_regions else None,
                               facecolor='white' if bw_regions else 'none')

        ax1.add_patch(boundary)

        pos_x = t * 2
        ax1.plot([pos_x, pos_x], [0, l], "k:")
        dim_text(pos_x, l / 2, "l= ", l, True)

        ax1.plot([0, w], [t * 3, t * 3], "k:")
        dim_text(w / 2, t * 4, "w= ", w, False)

        an_text(ax1, w / 2, t,
                "This (below) edge should be sanded to allow " + "upper surface to be flush with this")

        ax1.plot([0, w], [r, r], "k--")
        an_text(ax1, w / 2, r - t, "Bevel cut >45^\circ both sides")

        pos_x = t * 2 + pos_x
        ax1.plot([pos_x, pos_x], [0, r], "k:")
        pos_x = pos_x + t
        dim_text(pos_x, r / 2, "r= ", r, True)

        # Score 1
        pos_y = r + l_1
        ax1.plot([0, w], [pos_y, pos_y], "k--")
        an_text(ax1, w / 2, pos_y - t, "Crease")

        pos_x = pos_x + 2 * t
        ax1.plot([pos_x, pos_x], [r, pos_y], "k:")
        pos_x = pos_x + t
        dim_text(pos_x, (pos_y + r) / 2, "l_1=", l_1, True)

        # Score 2
        pos_y_prev = pos_y
        pos_y = pos_y + l_2
        ax1.plot([0, w], [pos_y, pos_y], "k--")
        an_text(ax1, w / 2, pos_y - t, "Crease")

        pos_x = pos_x + 2 * t
        ax1.plot([pos_x, pos_x], [pos_y_prev, pos_y], "k:")
        pos_x = pos_x + t
        dim_text(pos_x, (pos_y + pos_y_prev) / 2, "l_2=", l_2, True)

        # Score 3
        pos_y_prev = pos_y
        pos_y = pos_y + l_3
        ax1.plot([0, w], [pos_y, pos_y], "k--")
        an_text(ax1, w / 2, pos_y - t,
                "Crease, place spar of height approx" + str(round((h - 2 * t), 2)) + " in")

        pos_x = pos_x + 2 * t
        ax1.plot([pos_x, pos_x], [pos_y_prev, pos_y], "k:")
        pos_x = pos_x + t
        dim_text(pos_x, (pos_y + pos_y_prev) / 2, "l_3=", l_3, True)

        # Cut/half cut 4
        pos_y_prev = pos_y
        pos_y = pos_y + l_4
        ax1.plot([0, w], [pos_y, pos_y], "k--")
        an_text(ax1, w / 2, pos_y - t, "Angled cut ailerons; rest is your preference")

        pos_x = pos_x + 2 * t
        ax1.plot([pos_x, pos_x], [pos_y_prev, pos_y], "k:")
        pos_x = pos_x + t
        dim_text(pos_x, (pos_y + pos_y_prev) / 2, "l_4=", l_4, True)

        # Aileron left
        pos_y_prev = pos_y
        pos_y = pos_y + l_5
        boundary = plt.Polygon(
                np.array([[l_ea, l_ea + l_a, l_ea + l_a, l_ea],
                          [pos_y_prev, pos_y_prev, pos_y, pos_y]]).T,
                closed=True, edgecolor='black' if bw_regions else 'none',
                facecolor='white' if bw_regions else 'none')

        ax1.add_patch(boundary)

        pos_x = pos_x + 2 * t
        ax1.plot([pos_x, pos_x], [pos_y_prev, pos_y], "k:")
        pos_x = pos_x + t
        dim_text(pos_x, (pos_y + pos_y_prev) / 2, "l_5=", l_5, True)

        # Aileron right
        boundary = plt.Polygon(
                [[w - l_ea, pos_y_prev], [w - l_ea - l_a, pos_y_prev], [w - l_ea - l_a, pos_y],
                 [w - l_ea, pos_y]], closed=True, edgecolor='black' if bw_regions else 'none',
                facecolor='white' if bw_regions else 'none')

        ax1.add_patch(boundary)

        pos_y = (pos_y + pos_y_prev) / 2 - t
        pos_x = (w - l_ea - l_a + w - l_ea) / 2
        ax1.plot([w - l_ea - l_a, w - l_ea], [pos_y, pos_y], "k:")
        dim_text(pos_x, pos_y - t, "l_a=", l_a, False)

        # Distance between two
        pos_y = pos_y + t
        ax1.plot([l_a + l_ea, w - l_a - l_ea], [pos_y, pos_y], "k:")
        dim_text(w / 2, pos_y - t, "\Delta a=", (w - 2 * l_a - 2 * l_ea), False)

        # Figure 2
        fig2, ax2 = plt.subplots()

        # Root
        ax2.plot([0, r], [0, 0], "k", linewidth=2)
        dim_text(r / 2, t / 3, "r= ", r, False)

        # Upper horizontal surface
        ax2.plot([cog_avg, cog_avg + l_3], [h, h], "k", linewidth=2)
        dim_text((cog_avg * 2 + l_3) / 2, h - t / 3, "l_3= ", l_3, False)
        ax2.plot([0, cog_avg], [h / 2, h / 2], "k:")
        dim_text(cog_avg / 2, h / 2 - t / 3, "Leading edge to top edge = ", cog_avg, False)

        # Height
        ax2.plot([cog_avg, cog_avg], [0, h], "k:")
        dim_text(cog_avg + t / 3, h / 2, "h=", h, True)

        # Back side
        ax2.plot([cog_avg + l_3, r], [h, 0], "k", linewidth=2)
        dim_text((cog_avg + l_3 + r) / 2, h / 2, "l_4= ", l_4, False)

        an_text(ax2, r / 2, h / 2, "Outer surfaces of wing (except " + "l_1, l_2)")

        if accurate_drawing:
                ax2.set_aspect('equal', adjustable='box')
        ax2.set_position([0, 0, 1, 1])
        ax2.axis('off')

        fig1_html = mpld3.fig_to_html(fig1)
        fig2_html = mpld3.fig_to_html(fig2)

        return [fig1_html,fig2_html]









