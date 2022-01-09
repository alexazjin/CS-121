'''
Epidemic modelling
Ziqian (Alexa) Jin
Functions for running a simple epidemiological simulation
'''

import random
import sys

import click

# This seed should be used for debugging purposes only!  Do not refer
# to this variable in your code.
TEST_SEED = 20170217

def has_an_infected_neighbor(city, location):
    '''
    Determine whether a person at a specific location has an infected
    neighbor in a city modelled as a ring.
    Args:
        city (list of tuples): the state of all people in the simulation
          at the start of the day
        location (int): the location of the person to check
    Returns (boolean): True, if the person has an infected neighbor,
      False otherwise.
    '''
    # The location needs to be a valid index for the city list.
    assert 0 <= location < len(city)

    # This function should only be called when the person at location
    # is susceptible to infection.
    disease_state, _ = city[location]
    assert disease_state == "S"

    n = len(city) 
    if location == 0:
        return city[1][0] == 'I' or city[n-1][0] == 'I'

    elif location == n-1:
        return city[n-2][0] == 'I' or city[0][0] == 'I'
            
    else:
        return city[location - 1][0] == 'I' or city[location + 1][0] == 'I'
    


def advance_person_at_location(city, location, days_contagious):
    '''
    Compute the next state for the person at the specified location.
    Args:
        city (list): the state of all people in the simulation at the
          start of the day
        location (int): the location of the person to check
        days_contagious (int): the number of a days a person is infected
    Returns (string, int): the disease state and the number of days
      the person has been in that state after simulating one day.
      
    '''
    
    if city[location][0] == 'S':
        if has_an_infected_neighbor(city, location):
            new = ('I', 0)
        else: 
            new = ('S', city[location][1] + 1)
        
    elif city[location][0] == 'I':
        if city[location][1] in range(0, days_contagious - 1):
            new = ('I', city[location][1] + 1)
        else: 
            new = ('R', 0)
        
    else:
        new = (city[location][0], city[location][1] + 1)
    
    return new


def simulate_one_day(starting_city, days_contagious):
    '''
    Move the simulation forward a single day.
    Args:
        starting_city (list): the state of all people in the simulation at the
          start of the day
        days_contagious (int): the number of a days a person is infected
    Returns (list of tuples): the state of the city after one day
    '''
    updated_city = []
    for i, loc in enumerate(starting_city):
        updated_city.append(advance_person_at_location(starting_city,\
        i, days_contagious))
      
    return updated_city


def is_transmission_possible(city):
    """
    Is there at least one susceptible person who has an infected neighbor?
    Args:
        city (list): the current state of the city
    Returns (boolean): True if the city has at least one susceptible person
        with an infected neighbor, False otherwise.
    """
    output = False
    for i, loc in enumerate(city):
        if city[i][0] == 'S':
            if has_an_infected_neighbor(city, i):
                output = True
    
    return output


def run_simulation(starting_city, days_contagious):
    '''
    Run the entire simulation
    Args:
        starting_city (list): the state of all people in the city at the
          start of the simulation
        days_contagious (int): the number of a days a person is infected
    Returns tuple (list of tuples, int): the final state of the city
      and the number of days actually simulated.
    '''
    n = 0
    while is_transmission_possible(starting_city):
        starting_city = simulate_one_day(starting_city, days_contagious)
        n = n + 1

    return (starting_city, n)


def vaccinate_person(vax_tuple):
    '''
    Attempt to vaccinate a single person based on their current
    disease state and personal eagerness to be vaccinated.
    Args:
        vax_tuple (string, int, float): information about a person,
          including their eagerness to be vaccinated.
    Returns (string, int): a person tuple
    '''
    if vax_tuple[0] == 'S':
        x = random.random()
        if vax_tuple[2] > x:
            person_tuple = ('V', 0)
        else:
            person_tuple = (vax_tuple[0], vax_tuple[1])
 
    else:
        person_tuple = (vax_tuple[0], vax_tuple[1])
    
    return person_tuple


def vaccinate_city(city_vax_tuples, random_seed):
    '''
    Vaccinate the people in the city based on their current state and
    eagerness to be vaccinated.
    Args:
        city_vax_tuples (list of (string, int, float) triples):
          state of all people in the simulation at the start
          of the simulation, including their eagerness to be vaccinated.
        random_seed (int): seed for the random number generator
    Returns (list of (string, int) tuples): state of the people in the
      city after vaccination
    '''
    new_city = []
    random.seed(random_seed)
    for vax_tuple in city_vax_tuples:
        person_tuple = vaccinate_person(vax_tuple)
        new_city.append(person_tuple)

    return new_city


def vaccinate_and_simulate(city_vax_tuples, days_contagious, random_seed):
    """
    Vaccinate the city and then simulate the infection spread
    Args:
        city_vax_tuples (list): a list with the state of the people in the city,
            including their eagerness to be vaccinated.
        days_contagious (int): the number of days a person is infected
        random_seed (int): the seed for the random number generator
    Returns (list of tuples, int): the state of the city at the end of the
      simulation and the number of days simulated.
    """    
    updated_city = vaccinate_city(city_vax_tuples, random_seed)
    new = run_simulation(updated_city, days_contagious)
    
    return new  


################ Do not change the code below this line #######################

def run_trials(vax_city, days_contagious, random_seed, num_trials):
    """
    Run multiple trials of vaccinate_and_simulate and compute the median
    result for the number of days until infection transmission stops.
    Args:
        vax_city (list of (string, int, float) triples): a list with vax
            tuples for the people in the city
        days_contagious (int): the number of days a person is infected
        random_seed (int): the seed for the random number generator
        num_trials (int): the number of trial simulations to run
    Returns:
        (int) the median number of days until infection transmission stops
    """

    days = []
    for i in range(num_trials):
        if random_seed:
            _, num_days_simulated = vaccinate_and_simulate(vax_city,
                                                           days_contagious,
                                                           random_seed+i)
        else:
            _, num_days_simulated = vaccinate_and_simulate(vax_city,
                                                           days_contagious,
                                                           random_seed)
        days.append(num_days_simulated)

    # quick way to compute the median
    return sorted(days)[num_trials // 2]


def parse_city_file(filename, is_vax_tuple):
    """
    Read a city represented as person tuples or vax tuples from
    a file.
    Args:
        filename (string): the name of the file
        is_vax_tuple (boolean): True if the file is expected to contain
          (string, int) pairs.  False if the file is expected to contain
          (string, int, float) triples.
    Returns: list of tuples or None, if the file does not exist or
      cannot be parsed.
    """

    try:
        with open(filename) as f:
            residents = [line.split() for line in f]
    except IOError:
        print("Could not open:", filename, file=sys.stderr)
        return None

    ds_types = ('S', 'I', 'R', 'V')

    rv = []
    if is_vax_tuple:
        try:
            for i, res in enumerate(residents):
                ds, nd, ve = res
                num_days = int(nd)
                vax_eagerness = float(ve)
                if ds not in ds_types or num_days < 0 or \
                   vax_eagerness < 0 or vax_eagerness > 1.0:
                    raise ValueError()
                rv.append((ds, num_days, vax_eagerness))
        except ValueError:
            emsg = ("Error in line {}: vax tuples are represented "
                    "with a disease state {}"
                    "a non-negative integer, and a floating point value "
                    "between 0 and 1.0.")
            print(emsg.format(i, ds_types), file=sys.stderr)
            return None
    else:
        try:
            for i, res in enumerate(residents):
                ds, nd = res
                num_days = int(nd)
                if ds not in ds_types or num_days < 0:
                    raise ValueError()
                rv.append((ds, num_days))
        except ValueError:
            emsg = ("Error in line {}: persons are represented "
                    "with a disease state {} and a non-negative integer.")
            print(emsg.format(i, ds_types), file=sys.stderr)
            return None
    return rv


@click.command()
@click.argument("filename", type=str)
@click.option("--days-contagious", default=2, type=int)
@click.option("--task-type", default="no_vax",
              type=click.Choice(['no_vax', 'vax']))
@click.option("--random-seed", default=None, type=int)
@click.option("--num-trials", default=1, type=int)
def cmd(filename, days_contagious, task_type, random_seed, num_trials):
    '''
    Process the command-line arguments and do the work.
    '''
    city = parse_city_file(filename, task_type == "vax")
    if not city:
        return -1

    if task_type == "no_vax":
        print("Running simulation ...")
        final_city, num_days_simulated = run_simulation(
            city, days_contagious)
        print("Final city:", final_city)
        print("Days simulated:", num_days_simulated)
    elif num_trials == 1:
        print("Running one vax clinic and simulation ...")
        final_city, num_days_simulated = vaccinate_and_simulate(
            city, days_contagious, random_seed)
        print("Final city:", final_city)
        print("Days simulated:", num_days_simulated)
    else:
        print("Running multiple trials of the vax clinic and simulation ...")
        median_num_days = run_trials(city, days_contagious,
                                     random_seed, num_trials)
        print("Median number of days until infection transmission stops:",
              median_num_days)
    return 0


if __name__ == "__main__":
    cmd()  # pylint: disable=no-value-for-parameter
