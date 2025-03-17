# route_handlers.py

from flask import Blueprint, request, render_template, session
from Sensitivity import *
import numpy as np
route_handlers_blueprint = Blueprint('route_handlers', __name__)

@route_handlers_blueprint.route('/handle_configuration', methods=['POST'])
def handle_configuration():
    if request.method == 'POST':
            # Capture the values of the range inputs
            W_ideal = int(request.form['range1'])
            T_ideal = int(request.form['range2'])
            n_l_ideal = int(request.form['range3'])
            T_GM_ideal = int(request.form['range4'])
            E_ideal =   int(request.form['range5'])
           
            
        #     W_ideal = 2
        #     T_ideal = 120
        #     n_l_ideal = 10
        #     T_GM_ideal = 45
        #     E_ideal = 50

            x = np.arange(.25, 1.76, 0.01)


            w = [value * W_ideal for value in x]
            t = [value * T_ideal for value in x]
            n_l = [value * n_l_ideal for value in x]
            e = [value * E_ideal for value in x]
            t_gm = [value * W_ideal for value in x]

        
            Score_W = (scoreU(w, T_ideal, n_l_ideal, E_ideal, T_GM_ideal, W_ideal, T_ideal, n_l_ideal, E_ideal,
                              T_GM_ideal) / 7 - 1) * 100
            Score_T = (scoreU(W_ideal, t, n_l_ideal, E_ideal, T_GM_ideal, W_ideal, T_ideal, n_l_ideal, E_ideal,
                              T_GM_ideal) / 7 - 1) * 100
            Score_N_L = (scoreU(W_ideal, T_ideal, n_l, E_ideal, T_GM_ideal, W_ideal, T_ideal, n_l_ideal, E_ideal,
                                T_GM_ideal) / 7 - 1) * 100
            Score_E = (scoreU(W_ideal, T_ideal, n_l_ideal, e, T_GM_ideal, W_ideal, T_ideal, n_l_ideal, E_ideal,
                              T_GM_ideal) / 7 - 1) * 100
            Score_T_GM = (scoreU(W_ideal, T_ideal, n_l_ideal, E_ideal, t_gm, W_ideal, T_ideal, n_l_ideal, E_ideal,
                                 T_GM_ideal) / 7 - 1) * 100
            

            # For now, let's print the values as an example
            print("W_ideal:", W_ideal)
            print("T_ideal:", T_ideal)
            print("n_l_ideal:", n_l_ideal)
            print("T_GM_ideal:", T_GM_ideal)
            print("E_ideal:", E_ideal)
            data=[W_ideal,T_ideal,n_l_ideal,T_GM_ideal,E_ideal]

        #     graph_W=[]
        #     for i in range(1,70):
        #             graph_W.append(int(100*((Score_W[i]-Score_W[i-1])/[Score_W[i-1]])))
        #     graph_T = []
        #     for i in range(1, 70):
        #             graph_T.append(int(100*((Score_T[i] - Score_T[i - 1]) / [Score_T[i - 1]])))
        #     graph_N_L = []
        #     for i in range(1, 70):
        #             if (Score_N_L[i] - Score_N_L[i - 1]) == 0:
        #                 graph_N_L.append(0)
        #             elif Score_N_L[i - 1] == 0:
        #                     graph_N_L.append(int(100*Score_N_L[i]))
        #             else:
        #                 graph_N_L.append(int(100*((Score_N_L[i] - Score_N_L[i - 1]) / [Score_N_L[i - 1]])))
        #     graph_T_GM = []
        #     for i in range(1, 70):
        #             graph_T_GM.append(int(100*((Score_T_GM[i] - Score_T_GM[i - 1]) / [Score_T_GM[i - 1]])))
        #     graph_E = []
        #     for i in range(1, 70):
        #             graph_E.append(int(100*((Score_E[i] - Score_E[i - 1]) / [Score_E[i - 1]])))
            graph_W=[]
            for i in range(1,149):
                    graph_W.append(int(Score_W[i]))
            graph_T = []
            for i in range(1, 149):
                    graph_T.append(int(Score_T[i]))
            graph_N_L = []
            for i in range(1, 149):
                    graph_N_L.append(int(Score_N_L[i]))
            graph_T_GM = []
            for i in range(1, 149):
                    graph_T_GM.append(int(Score_T_GM[i]))
            graph_E = []
            for i in range(1, 149):
                    graph_E.append(int(Score_E[i]))

            graph_x=[]
            for i in range(-74,75):
                    graph_x.append(i)
            t=graph_W.index(max(graph_W))
            print(graph_W[t-1], graph_W[t], graph_W[t+1])



            data.append(graph_W)

            data.append(graph_T)
            data.append(graph_N_L)
            data.append(graph_T_GM)
            data.append(graph_E)
            data.append(graph_x)
            print(data)


    return render_template("home.html", submit=1, data=data)





