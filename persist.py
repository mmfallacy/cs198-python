from numpy import asarray

def save_calc_csv(target, X,Y,Z):
    
    # Assertions:
    # Note on matplotlib's contourf convention of X and Y axes.
    assert len(Y) == len(Z)
    assert len(X) == len(Z[0])
    
    # Fail if target exists.
    with open(target, 'x') as out:
        # Write X as comma separated
        out.write(",".join(str(i) for i in X))
        out.write("\n")
        # Write Y as comma separated
        out.write(",".join(str(i) for i in Y))
        out.write("\n")
        
        # Write Z for the remainder
        out.writelines(map(lambda el: ",".join(str(i) for i in el) + "\n" ,Z))

def load_calc_csv(target):

    with open(target) as inp:
        X = asarray(inp.readline().split(","), dtype=float)
        Y = asarray(inp.readline().split(","), dtype=float)
        
        Z = []

        while line := inp.readline():
            Z.append(asarray(line.split(","), dtype=float))
        
        return X, Y, Z