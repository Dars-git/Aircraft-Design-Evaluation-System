from pymongo import MongoClient
from pymongo.server_api import ServerApi

#Connect to MongoDb 
client = MongoClient("mongodb+srv://lowen:sm2?P3pAb!FkJs@cluster0.6lo356o.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))

#initialize database
db = client['PresetsDataBase']

#Creates a presets table/collection
presets = db['presets']

def initialize_user(Username):
    #if the user does not exist in the database
    if  presets.count_documents({"Username": Username}) == 0:
    #Function to give a new user default parameters
        # Flying Wing Design default
        FW_data = {
            "Username": Username,
            "Format": "FW",
            "Wingspan": 28,
            "Tip_Chord": 6,
            "Root_Chord": 18,
            "Chassis_Width": 6,
            "Sweep_Angle": 30,
            "Output_Units": True  # False == mm True == in
        }
        presets.insert_one(FW_data)

        # Standard Wing Design default
        SW_data = {
            "Username": Username,
            "Format": "SW",
            "Wingspan": 78,
            "Root_Chord": 10.6,
            "Output_Units": True,
            "accurate_drawing": True,
            "bw_regions": False
        }
        presets.insert_one(SW_data)

        # Standard Fuselage Design default
        SF_data = {
            "Username": Username,
            "Format": "SF",
            "Wingspan": 78,
            "Root_Chord": 10.6,
            "Fuselage_Height": 3.75,
            "Fuselage_Width": 3.5,
            "Tail_End_Height": 3.75,
            "Angle_Of_Incidence": 0,
            "Output_Units": True,
            "accurate_drawing": False
        }
        presets.insert_one(SF_data)

        # Stabilizer Shape Design default
        SS_data = {
            "Username": Username,
            "Format": "SS",
            "Wingspan": 78,
            "Root_Chord": 10.6,
            "Fuselage_Width": 4,
            "Elevator_Length": 2,
            "L_greater_elevator_length": 6,
            "Output_Units": True
        }
        presets.insert_one(SS_data)
        return 0
    
    #If the user already exists
    else:
        print("Username already initialized")
        return 0


def get_flying_wing(Username):
    #Find the Flying Wing Design for a given user and extract all parameters
    find_user_FW = presets.find({"Username": Username, "Format":"FW"})

    Username = find_user_FW[0].get("Username")
    Format = find_user_FW[0].get("Format")
    Wingspan = find_user_FW[0].get("Wingspan")
    Tip_Chord = find_user_FW[0].get("Tip_Chord")
    Root_Chord = find_user_FW[0].get("Root_Chord")
    Chassis_Width = find_user_FW[0].get("Chassis_Width")
    Sweep_Angle = find_user_FW[0].get("Sweep_Angle")
    Output_Units = find_user_FW[0].get("Output_Units")

    return Username, Format, Wingspan, Tip_Chord, Root_Chord, Chassis_Width, Sweep_Angle, Output_Units

def get_standard_wing(Username):
    #Find the Standard Wing Design for a given user and extract all parameters
    find_user_SW = presets.find({"Username": Username, "Format":"SW"})

    Username_sw = find_user_SW[0].get("Username")
    Format_sw = find_user_SW[0].get("Format")
    Wingspan_sw = find_user_SW[0].get("Wingspan")
    Root_Chord_sw = find_user_SW[0].get("Root_Chord")
    Output_Units_sw = find_user_SW[0].get("Output_Units")
    accurate_drawing = find_user_SW[0].get("accurate_drawing")
    bw_regions = find_user_SW[0].get("bw_regions")

    return Username_sw, Format_sw, Wingspan_sw, Root_Chord_sw, Output_Units_sw, accurate_drawing, bw_regions

def get_standard_fuselage(Username):
    #Find the Standard Fuselage Design for a given user and extract all parameters
    find_user_SF = presets.find({"Username": Username, "Format":"SF"})

    Username_sf = find_user_SF[0].get("Username")
    Format_sf = find_user_SF[0].get("Format")
    Wingspan_sf = find_user_SF[0].get("Wingspan")
    Root_Chord_sf = find_user_SF[0].get("Root_Chord")
    Fuselage_Height_sf = find_user_SF[0].get("Fuselage_Height")
    Fuselage_Width_sf = find_user_SF[0].get("Fuselage_Width")
    Tail_End_Height_sf = find_user_SF[0].get("Tail_End_Height")
    Angle_Of_Incidence_sf = find_user_SF[0].get("Angle_Of_Incidence")
    Output_Units_sf = find_user_SF[0].get("Output_Units")
    accurate_drawing = find_user_SF[0].get("accurate_drawing")

    return Username_sf, Format_sf, Wingspan_sf, Root_Chord_sf, Fuselage_Height_sf, Fuselage_Width_sf, Tail_End_Height_sf, Angle_Of_Incidence_sf, Output_Units_sf, accurate_drawing

def get_stabilizer_shape(Username):
    #Find the Stabilizer Shape Design for a given user and extract all parameters
    find_user_SS = presets.find({"Username": Username, "Format":"SS"})

    Username_ss = find_user_SS[0].get("Username")
    Format_ss = find_user_SS[0].get("Format")
    Wingspan_ss = find_user_SS[0].get("Wingspan")
    Root_Chord_ss = find_user_SS[0].get("Root_Chord")
    Fuselage_Width_ss = find_user_SS[0].get("Fuselage_Width")
    Elevator_Length_ss = find_user_SS[0].get("Elevator_Length")
    L_greater_elevator_length_ss = find_user_SS[0].get("L_greater_elevator_length")
    Output_Units_ss = find_user_SS[0].get("Output_Units")

    return Username_ss, Format_ss, Wingspan_ss, Root_Chord_ss, Fuselage_Width_ss, Elevator_Length_ss, L_greater_elevator_length_ss, Output_Units_ss

def update_flying_wing(Username, new_data):
    # Update the Flying Wing Design parameters for a given user
    presets.update_one({"Username": Username, "Format": "FW"}, {"$set": new_data})

def update_stabilizer_shape(Username, new_data):
    # Update the Stabilizer Shape Design parameters for a given user
    presets.update_one({"Username": Username, "Format": "SS"}, {"$set": new_data})


def update_standard_fuselage(Username, new_data):
    # Update the Standard Fuselage Design parameters for a given user
    presets.update_one({"Username": Username, "Format": "SF"}, {"$set": new_data})

def update_standard_wing(Username, new_data):
    # Update the Standard Wing Design parameters for a given user
    presets.update_one({"Username": Username, "Format": "SW"}, {"$set": new_data})



#Save Preset/Overwrite Old Preset
#Delete Old Preset
def Overwrite(Preset):
    #Deletes the previous preset assigned to the user (A default one needs to be implemented)
    presets.delete_one({"Username": Preset["Username"], "Format": Preset["Format"]})

    #Insert New Preset
    presets.insert_one(Preset)

    return 0