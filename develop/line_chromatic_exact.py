"""
Determine whether Gamma_6 minus the isometry-normalized 6-class
C = {1, 3, 5, 9, 17, 33} is 11-colorable.

If yes, chi(Gamma_6) = 12. If no, chi(Gamma_6) = 13.

The class C is the unique (up to isometry) independent set of size 6
in Gamma_6, by Lemma 3.1 of the paper.
"""
from pysat.formula import CNF
from pysat.solvers import Solver


def dot(u, v):
    return (u & v).bit_count() % 2


def build_graph():
    edges = []
    for u in range(1, 64):
        for v in range(u + 1, 64):
            if dot(u, v) == 0:
                edges.append((u, v))
    return edges


def main():
    C = {1, 3, 5, 9, 17, 33}
    all_edges = build_graph()
    vertices = [v for v in range(1, 64) if v not in C]
    n = len(vertices)
    k = 11
    idx = {v: i for i, v in enumerate(vertices)}

    def var(v, c):
        return idx[v] * k + c + 1

    cnf = CNF()

    # At least one color per vertex
    for v in vertices:
        cnf.append([var(v, c) for c in range(k)])

    # At most one color per vertex
    for v in vertices:
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(v, c1), -var(v, c2)])

    # Adjacent vertices have different colors
    for u, v in all_edges:
        if u in C or v in C:
            continue
        for c in range(k):
            cnf.append([-var(u, c), -var(v, c)])

    print(f"Variables: {cnf.nv}, Clauses: {len(cnf.clauses)}")
    print(f"Vertices: {n}, Edges in H: "
          f"{sum(1 for u, v in all_edges if u not in C and v not in C)}")

    with Solver(name='g4', bootstrap_with=cnf.clauses, with_proof=True) as solver:
        result = solver.solve()
        if result:
            print("Status: SAT")
            print("Conclusion: chi(Gamma_6) = 12")
        else:
            proof = solver.get_proof()
            print("Status: UNSAT")
            print("Conclusion: chi(Gamma_6) = 13")
            print(f"Proof lines: {len(proof)}")


if __name__ == '__main__':
    main()
