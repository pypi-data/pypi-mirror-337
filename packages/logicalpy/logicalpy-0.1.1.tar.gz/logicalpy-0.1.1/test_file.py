from logicalpy import Formula, Proposition, Or, Implies
from logicalpy.resolution import ResolutionProver

premises = [Formula.from_string("A v B"), Formula.from_string("A -> C"), Formula.from_string("B -> C")]

conclusion = Formula.from_string("C")

test_prover = ResolutionProver(premises=premises, conclusion=conclusion)

refutation_found, proof_str = test_prover.prove()

print("Refutation found:", refutation_found)

print("\nProof:\n" + proof_str)
