import numpy as np 
#import cupy as np 
from rdkit import Chem
from rdkit.Chem import AllChem
from .util import one_of_k_encoding, one_of_k_encoding_unk, one_of_TF_encoding

def atom_features_from_ecfp(atom):
    return np.array(one_of_k_encoding_unk(atom.GetSymbol(),
                                      ['c', 'n', 'o', 's', 'f', 'si', 'p', 'cl', 'br', 'mg', 'na',
                                       'ca', 'fe', 'as', 'al', 'i', 'b', 'v', 'k', 'tl', 'yb',
                                       'sb', 'sn', 'ag', 'pd', 'co', 'se', 'ti', 'zn', 'h',    # h?
                                       'li', 'ge', 'cu', 'au', 'ni', 'cd', 'in', 'mn', 'zr',
                                       'cr', 'pt', 'hg', 'pb', 'unknown']) +
                    one_of_k_encoding(atom.GetDegree(), [0, 1, 2, 3, 4, 5]) +
                    one_of_k_encoding_unk(atom.GetTotalNumHs(), [0, 1, 2, 3, 4]) +
                    #one_of_k_encoding_unk(atom.GetImplicitValence(), [0, 1, 2, 3, 4, 5]) +
					one_of_TF_encoding(atom.GetIsAromatic())
					)

def atom_features_from_fcfp(mol):
	com = AllChem.RemoveHs(mol) 
	gl = AllChem.GetFeatureInvariants(com)
	def to_bin(x):
		f1 = format(x, 'b').zfill(6)
		f2 = map(int, list(f1))
		f3 = list(f2)
		def to_TF(f):
			arr = []
			for y in f:
				if y:
					arr += [1,0]
				else:
					arr += [0,1]
			return arr
		f4 = to_TF(f3)
		ff = list(f4) #FCFP has 6 features
		del ff[1:3]
		return ff
	gl = list(map(to_bin, gl))

	
	return np.array(gl)

def bond_features(bond):
    bt = bond.GetBondType()
    return np.array([bt == Chem.rdchem.BondType.SINGLE,
                     bt == Chem.rdchem.BondType.DOUBLE,
                     bt == Chem.rdchem.BondType.TRIPLE,
                     bt == Chem.rdchem.BondType.AROMATIC,
                     bond.GetIsConjugated(),
                     bond.IsInRing()])

def num_atom_features_from_ecfp():
	# Return length of feature vector using a very simple molecule.
	m = Chem.MolFromSmiles('CC')
	alist = m.GetAtoms()
	a = alist[0]
	return len(atom_features_from_ecfp(a))

def num_atom_features_from_fcfp():
	# Return length of feature vector using a very simple molecule.
	a = Chem.MolFromSmiles('CC')
	return len(atom_features_from_fcfp(a)[0])


def num_bond_features():
    # Return length of feature vector using a very simple molecule.
    simple_mol = Chem.MolFromSmiles('CC')
    Chem.SanitizeMol(simple_mol)
    return len(bond_features(simple_mol.GetBonds()[0]))

