import os
import shutil
import numpy as np
from simassis.files import poscar_to, lammps_to
import scipy.constants as sc
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def getEnergy(path):
    ''' 
        Function that reads the energy from the log.lammps file that is in 
        the given directory. The function returns the energy in eV.
    '''
    lineWithLastStep = None
    with open(path) as inFile:
        linesOfTxt = inFile.readlines()

    for i in range(len(linesOfTxt)):
        if "Loop time" in linesOfTxt[i]:
            lineWithLastStep = i-1

    if lineWithLastStep == None:
        print("ERROR: ",end="")
        print(path)
        Energy = None
    else:
        lineSplited = linesOfTxt[lineWithLastStep].split()
        Energy = lineSplited[1]

    Energy = float(Energy)

    kcal_to_eV = 4184 / sc.Avogadro / sc.eV
    Energy = Energy * kcal_to_eV # kcal/mol to eV
    return Energy


def make_BM_simulation_and_get_data(
    amount_of_simulations,
    maxchange_x,
    maxchange_y,
    maxchange_z,
    path_to_simulations,
    path_lammps_src,
    path_in_changing_V,
    path_in_const_V,
    path_POSCAR,
    path_result,
    charges
):
    '''
        Function that automates the process of creating data for the 
        Birch-Murnaghan equation of state. The function creates a series of
        simulations with different volumes around relaxed volume and returns 
        the energies and volumes.
        Arguments:
        - amount_of_simulations: int, number of simulations
        - maxchange_x: float, maximum change of the cell in x direction
        - maxchange_y: float, maximum change of the cell in y direction
        - maxchange_z: float, maximum change of the cell in z direction
        - path_to_simulations: str, path to the directory where the simulations
          will be created
        - path_lammps_src: str, path to the directory with the source files for 
          simulations
        - path_in_changing_V: str, path to the input file for simulations with
          changing volume
        - path_in_const_V: str, path to the input file for simulations with
          constant volume
        - path_POSCAR: str, path to the POSCAR file that is structure one wants
          to simulate
        - path_result: str, path to the directory where the results will be saved
        - charges: list of floats, list of custom charges for each atom in 
          the structure
        Returns:
        - file BM_data.npz with two arrays: energies and volumes
    '''

    # Initial setup
    original_dir = os.getcwd()
    maxchange = np.array([maxchange_x, maxchange_y, maxchange_z])
    array_of_energies = np.zeros(amount_of_simulations)
    array_of_volumes = np.zeros(amount_of_simulations)
    change_dim = np.linspace(1-maxchange, 1+maxchange, amount_of_simulations)
    volumes_change = np.prod(change_dim, axis=1)
    # Needs update problem with simassis !!!
    custom_charges = [4, -2]

    # Create directory for simulations
    os.chdir(path_to_simulations)
    for directory in os.listdir():
        if directory == 'B-M_Simulations':
            shutil.rmtree('B-M_Simulations')

    os.mkdir('B-M_Simulations')
    os.chdir('B-M_Simulations')

    # Crete folder with source files
    os.mkdir('src')
    os.chdir('src')

    for file in os.listdir(path_lammps_src):
            source = os.path.join(path_lammps_src, file)
            shutil.copy2(source, os.getcwd())

    os.chdir('..')

    # Initial relaxation
    os.mkdir('Initial_Relaxation')
    os.chdir('Initial_Relaxation')
    shutil.copy(path_POSCAR, 'POSCAR.vasp')
    for file in os.listdir(path_lammps_src):
        source = os.path.join(path_lammps_src, file)
        shutil.copy2(source, os.getcwd())

    shutil.copy2(path_in_changing_V, 'in')
    sim_conf = poscar_to("POSCAR.vasp", ['charge', 'triclinic'])
    sim_conf.write(
            'lammps', 
            os.path.join(os.getcwd(), "data"), 
            ['charge', custom_charges])

    try:
            os.system("lmp -in in")
    except:
            print("Initial relaxation failed")

    path_initial_post_data = os.path.join(os.getcwd(), 'post.data')
    os.chdir('..')

    # Main Loop
    for idx_sim in range(amount_of_simulations):
        name = "{0:.5f}".format(volumes_change[idx_sim])
        os.mkdir(name)
        os.chdir(name)

        shutil.copy2(path_in_const_V, os.getcwd())
        shutil.copy2(path_initial_post_data, os.getcwd())

        sim_conf = lammps_to("post.data", ['charge', 'triclinic'])
        sim_conf.basex = sim_conf.basex * change_dim[idx_sim][0]
        sim_conf.basey = sim_conf.basey * change_dim[idx_sim][1]
        sim_conf.basez = sim_conf.basez * change_dim[idx_sim][2]
        array_of_volumes[idx_sim] = abs(np.linalg.det(np.array([sim_conf.basex, sim_conf.basey, sim_conf.basez])))

        positions_splited = []
        for i in range(len(sim_conf.positions_splited)):
            positions_splited.append(change_dim[idx_sim] * sim_conf.positions_splited[i])
        sim_conf.positions_splited = positions_splited

        # fix charges so thay can be custom
        sim_conf.write(
            'lammps', 
            os.path.join(os.getcwd(), "data"), 
            ['charge', custom_charges])
        # For visualisation (optional)
        sim_conf.write(
            'vasp', 
            os.path.join(os.getcwd(), "POSCAR.vasp"), 
            ['charge', custom_charges])
        
        try:
            os.system("lmp -in in")
        except:
            print("rip")

        array_of_energies[idx_sim] = getEnergy(os.path.join(os.getcwd(), 
                                                            "log.lammps"))
        
        os.chdir("..")
        print(str(volumes_change[idx_sim]) + " done") 

    os.chdir(original_dir)
    np.savez(path_result, energies=array_of_energies, volumes=array_of_volumes)


def round_by_error(value, error):
    '''
        Function that rounds the value to the same decimal place as the error.
        Arguments:
        - value: float, value to be rounded
        - error: float, error of the value
        Returns:
        - string with the value and error in the format "value(error)"
    '''
    if error == 0:
        return f"{value}(0)"
    
    # Get the order of magnitude of the error
    order = math.floor(math.log10(abs(error)))
    
    # Round error to two significant figures
    rounded_error = round(error, -order + 1)
    
    # Ensure rounded_error is not zero
    if rounded_error == 0:
        rounded_error = 10 ** (order - 1)
    
    # Round value to the same decimal place as rounded_error
    rounded_value = round(value, -order + 1)
    
    return f"{rounded_value}({int(rounded_error*10**(-order+1))})"


def Birch_Murnaghan_internal_energy_of_V(V, E_0, V_0, B_0, B_0_prim):
    #https://en.wikipedia.org/wiki/Birch%E2%80%93Murnaghan_equation_of_state
    V_V0_to_2_3 = (V_0/V)**(2/3)
    E = E_0 + (9 * V_0 * B_0)/16 *(
        (V_V0_to_2_3 - 1 )**3 * B_0_prim
        + ( V_V0_to_2_3 -1)**2 * ( 6 - 4*V_V0_to_2_3 )
        )
    return E


def BM_plot(path_npz, path_POSCAR, mode = 'standard', output_name = 'B-M_Results.png'):
    '''
        Function that reads the data from the npz file and fits the Birch-Murnaghan
        equation of state to the data. The function saves the plot of the data and
        the fitted curve.
        Arguments:
        - path_npz: str, path to the npz file with the data
        - path_POSCAR: str, path to the POSCAR file with the structure
        - mode: str, 'standard' or 'density', determines if the x-axis of the plot
          is volume or density
        - output_name: str, name of the output file with the plot
    '''
    data = np.load(path_npz)
    energies = data['energies']
    volumes = data['volumes']

    # Loading attoms for density
    sim_conf = poscar_to(path_POSCAR, [])
    amount_of_atoms = np.sum(sim_conf.atoms_quantity)

    # Fitting B-M
    # Educated guess
    E0_guess = min(energies)# E0 = Ymin
    V0_guess = volumes[energies==E0_guess][0]# V0 = x in Ymin
    print("E0 guess: " + str(E0_guess) + " V0 guess: " + str(V0_guess))

    popt, pcov = curve_fit(Birch_Murnaghan_internal_energy_of_V, 
        volumes, 
        energies,
        p0 = [E0_guess, V0_guess, 1, 1])
    
    E0 = popt[0]
    V0 = popt[1]
    erorrs = np.sqrt(np.diag(pcov))
    print("E0 :" + round_by_error(E0/amount_of_atoms, 
                                  1/amount_of_atoms * erorrs[0]) + "eV/atoms" )
    print(f'rho:' + round_by_error( amount_of_atoms/V0, 
                                    amount_of_atoms/(V0**2) * erorrs[1]) 
         + 'atoms/A^3')

    # Plotting
    plus_start = (volumes[1] - volumes[0])/2
    plus_end = (volumes[-1] - volumes[-2])/2
    xs = np.linspace(volumes[0] - plus_start, volumes[-1] + plus_end, 100)

    fig, ax = plt.subplots()
    if mode == 'standard':
        ax.scatter(volumes, 
            energies/amount_of_atoms,
            c ="red")
        ax.plot(xs, Birch_Murnaghan_internal_energy_of_V(xs, *popt)/amount_of_atoms, 'r-')

        ax.set(xlabel='Volume($\\mathrm{\\AA^3}$)', ylabel='E (eV/atoms)',
        title='B-M')
    elif mode == 'density':
        ax.scatter(amount_of_atoms/volumes, 
            energies/amount_of_atoms,
            c ="red")
        ax.plot(amount_of_atoms/xs, Birch_Murnaghan_internal_energy_of_V(xs, *popt)/amount_of_atoms, 'r-')

        ax.set(xlabel='Density(atom/$\\mathrm{\\AA^3}$)', ylabel='E (eV/atoms)',
        title='B-M')
        
    ax.grid()
    fig.savefig(output_name)

    plt.show()