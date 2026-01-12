# train_data_keywords.py
"""Physics keywords for generating the train data physics haikus.
Physics family names stored in train_families.
Physics keyword families stored in train_keyword_families. """

classical_mechanics_keywords = [
'force', 'momentum', 'acceleration', 'velocity', 'position',
'gravity', 'inertia', 'rigid body', 'moment', 'rotation',
'Lagrangian', 'Hamiltonian', 'motion', 'conservation', 'constant',
'friction', 'oscillator', 'spring', 'pendulum', 'rocket',
'frame', 'non-inertial', 'time', 'orbit', 'energy'
]

electromagnetism_keywords = [
'charge', 'Coulomb', 'Gauss', 'field', 'electric',
'magnet', 'pole', 'vector', 'Ampere', 'potential',
'Maxwell', 'voltage', 'circuit', 'resistor', 'current',
'capacitor', 'inductor', 'work', 'trajectory', 'cross product',
'radiation', 'antenna', 'waveguide', 'radio', 'Poynting'
]

quantum_mechanics_keywords = [
'quantize', 'wavefunction', 'Schrodinger', 'uncertainty', 'time-independent',
'superposition', 'operator', 'expectation value', 'Ehrenfest', 'measurement',
'observer', 'quanta', 'wave', 'particle', 'duality',
'conjugate variable', 'Copenhagen', 'many-worlds', 'entanglement', "Bell's Theorem",
'finite well', 'Dirac delta', 'tunneling', 'bound state', 'energy level'
]

thermo_statmech_keywords = [
'heat', 'entropy', 'second law', 'phase space', 'microstate',
'Boltzmann', 'distribution', 'Bose-Einstein', 'Fermi-Dirac', 'ideal gas',
'system', 'cycle', 'Carnot', 'engine', 'refrigerator',
'state variable', 'efficiency', 'pressure', 'volume', 'temperature',
'area', 'bath', 'partition function', 'ensemble', 'heat capacity'
]

mathematical_physics_keywords = [
'Lie algebra', 'spherical coordinates', 'gradient', 'divergence', 'curl',
'tensor', 'complex analysis', 'Cauchy integral', 'contour', 'Taylor series',
'residue', 'conformal map', 'Fourier transform', 'orthogonality', 'Laplace transform',
'first order', 'second order', 'Frobenius', 'quadrature', "Green's function",
'integral equation', 'steepest descent', 'group theory', 'variational calculus', 'representation'
]

advanced_lab_keywords = [
'oscilloscope', 'data analysis', 'diffraction', 'spectroscopy', 'Hall effect',
'photoelectric effect', 'error propagation', 'systematics', 'curve fitting', 'interference',
'optical pumping', 'Franck-Hertz', 'Zeeman effect', 'optical rotation', 'reflection',
'quantum optics', 'superconductor', 'chaos', 'non-linear system', 'lab report',
'multimeter', 'power supply', 'function generator', 'optical bench', 'laser'
]

condensed_matter_keywords = [
'Bravais lattice', 'unit cell', 'reciprocal lattice', 'Brillouin zone', 'phonon',
'Debye model', 'specific heat', 'thermal conductivity', 'Drude model', 'band gap',
"Bloch's theorem", 'metal', 'insulator', 'semiconductor', 'transistor',
'p-n junction', 'diamagnetism', 'paramagnetism', 'ferromagnetism', 'Meissner effect',
'BCS theory', 'phase transition', 'Berry phase', 'topological', 'polymer'
]

relativity_keywords = [
'spacetime', 'Minkowski', 'four-vector', 'invariance', 'proper time',
'metric', 'Christoffel symbols', 'connection', 'Einstein', 'simultaneity',
'length contraction', 'time dilation', 'event', 'Ricci tensor', 'stress-energy tensor',
'covariance', 'twin paradox', 'curvature', 'black hole', 'event horizon',
'diffeomorphism', 'equivalence principle', 'geodesic', 'free fall', 'gravitational wave' 
]

train_families = [
    'classical_mechanics',
    'electromagnetism',
    'quantum_mechanics',
    'thermo_statmech',
    'mathematical_physics',
    'advanced_lab',
    'condensed_matter',
    'relativity'
]

train_keyword_families = [
    classical_mechanics_keywords,
    electromagnetism_keywords,
    quantum_mechanics_keywords,
    thermo_statmech_keywords,
    mathematical_physics_keywords,
    advanced_lab_keywords,
    condensed_matter_keywords,
    relativity_keywords
]