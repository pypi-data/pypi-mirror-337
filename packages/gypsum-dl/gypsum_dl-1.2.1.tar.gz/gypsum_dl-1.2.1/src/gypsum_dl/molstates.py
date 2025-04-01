from collections import OrderedDict
from typing import Iterator, Union

from gypsum_dl.MolContainer import MolContainer
from gypsum_dl.Steps.SMILES.PrepareSmiles import prepare_smiles
from gypsum_dl.Parallelizer import Parallelizer

from rdkit import Chem


class MolStates:
    gypsum_dl_params = OrderedDict({
        "source": "",
        "output_folder": "./",
        "separate_output_files": False,
        "add_pdb_output": False,
        "add_html_output": False,
        "num_processors": 1,
        "start_time": 0,
        "end_time": 0,
        "run_time": 0,
        "min_ph": 6.4,
        "max_ph": 8.4,
        "pka_precision": 1.0, # pKa precision factor (number of standard devations, default: 1.0)
        "thoroughness": 3, # How many molecules to generate per variant
        "max_variants_per_compound": 5,
        "second_embed": False,
        "2d_output_only": False,
        "skip_optimize_geometry": False,
        "skip_alternate_ring_conformations": False,
        "skip_adding_hydrogen": False,
        "skip_making_tautomers": False,
        "skip_enumerate_chiral_mol": False,
        "skip_enumerate_double_bonds": False,
        "let_tautomers_change_chirality": False,
        "use_durrant_lab_filters": True,
        "job_manager": "serial",
        "cache_prerun": False,
        "test": False,
        "Parallelizer" : Parallelizer('serial', 1, True),
        })
    

    def __init__(self, smiles:str):
        self.smiles = smiles
        assert self.is_valid(), "Invalid SMILES: " + smiles
        self.states = self.run_gypsum_dl()
    

    def is_valid(self) -> bool:
        try:
            mol = Chem.MolFromSmiles(self.smiles, sanitize=False)
            assert mol, "cannot create rdmol object."
            for bond in mol.GetBonds():
                assert bond.GetBondTypeAsDouble() > 0.5, "molecule has an unassigned bond"
                # returns our bondType as a double (e.g. SINGLE->1.0, AROMATIC->1.5, etc.)
            return True
        except:
            return False
        
    
    def count(self) -> int:
        return len(self.states)
    

    def __iter__(self) -> Iterator:
        return iter(self.states)


    def __next__(self) -> str:
        return next(self.states)


    def __getitem__(self, index:Union[int, slice]) -> str:
        if self.count() == 0:
            raise ValueError(f"no state")
        try:
            return self.states[index]
        except:
            raise ValueError(f"index should be 0..{self.count()-1}")
        

    # requires python 3.9 and later
    def run_gypsum_dl(self) -> list[str]:
        name = "untitled"
        idx_counter = 0
        props = {}
        containers = [MolContainer(self.smiles, name, idx_counter, props)]
        # Remove None types from failed conversion
        containers = [x for x in containers if x.orig_smi_canonical != None]

        # In multiprocessing mode, Gypsum-DL parallelizes each small-molecule
        # preparation step separately. But this scheme is inefficient in MPI mode
        # because it increases the amount of communication required between nodes.
        # So for MPI mode, we will run all the preparation steps for a given
        # molecule container on a single thread.
        # Non-MPI (e.g., multiprocessing)
        # Start creating the models.

        # Prepare the smiles. Desalt, consider alternate ionization, tautometeric,
        # stereoisomeric forms, etc.
        prepare_smiles(containers, MolStates.gypsum_dl_params)
        return containers[0].all_can_noh_smiles()