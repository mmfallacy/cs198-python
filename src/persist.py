from numpy import asarray
import json

def load_simulated(target):
    # Note: SIMULATION_TPS_RUN should be set equal to the simulator's TPS parameter.
    # By default the simulator runs the simulations in 120 ticks per second.

    with open(target) as inp:
        data = json.load(inp)

    # Dexie.js format for exporting IndexedDB
    rows = data['data']['data'][0]['rows']

    X, Y = [], []
    Z = {
        "first_mttc": [],
        "ave_headway": [],
        "tick": [],
        "ave_vx": [],
    }

    for row in rows:
        # Skip colliding cases
        if (row["state_collision"] == True): continue
        # Skip impossible cases
        if (row["state_first_mttc"] <= 0): continue
        # Skip cases where FV average velocity went negative
        # if (row["state_FV_ave_vx"] < 0): continue
        
        Y.append(row["params_FV_vx"] - row["params_LV_vx"])
        X.append(row["params_FV_ax"] - row["params_LV_ax"])
        
        Z["first_mttc"].append(row["state_first_mttc"])
        Z["ave_headway"].append(row["state_ave_headway"])
        Z["tick"].append(row["state_tick"])
        Z["ave_vx"].append(row["state_FV_ave_vx"])
        
    return X, Y, Z
    
def save_points_csv(target, X, Y, Z):
    # Assertions:
    assert len(X) == len(Y) == len(Z)

    # Open with exclusive creation; fail if already exists
    with open(target, "x") as out:
        for i in range(0, len(X)):
            out.write(f"{X[i]},{Y[i]},{Z[i]}\n")
        
def load_points_csv(target):
    X, Y, Z = [], [], []
    with open(target) as inp:
        while line:=inp.readline().rstrip('\n'):
            x,y,z = line.split(',')
            X.append(x)
            Y.append(y)
            Z.append(z)
    
    return asarray(X, dtype=float), asarray(Y, dtype=float), asarray(Z, dtype=float)