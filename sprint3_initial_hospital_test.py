import random
import simpy# Import SimPy library using pip install simPy in CMD or Terminal

class Hospital:
    def __init__(self, env, num_staff):
        self.env = env
        self.staff = simpy.Resource(env, capacity=num_staff)
        self.wait_times = []

    def triage_patient(self, patient):
        with self.staff.request() as request:
            yield request
            wait_time = self.calculate_wait_time(len(self.staff.users))
            yield self.env.timeout(wait_time)
            self.wait_times.append(wait_time)

    def calculate_wait_time(self, num_staffed):
        base_wait_time = 500
        load_factor = max(1, num_staff - num_staffed)# Inverse proportionality: the more staff, the lower the load_factor
        return base_wait_time / load_factor
    
class Patient:
    def __init__(self, name, arrival_time):
        self.name = name
        self.arrival_time = arrival_time  # Record the arrival time of the patient

def patient_generator(env, hospital, num_patients, interarrival_time):
    for i in range(num_patients):
        patient = Patient(f'Patient-{i+1}', env.now)
        # Create a new patient with a unique name and arrival time
        env.process(hospital.triage_patient(patient))
        # Process the patient through triage
        yield env.timeout(interarrival_time)
        # Simulate interarrival time of patients

def run_simulation(num_patients, num_staff, interarrival_time, sim_duration):
    env = simpy.Environment()
    # Create a simulation environment
    hospital = Hospital(env, num_staff)
    # Initialize the hospital with the specified number of staff
    env.process(patient_generator(env, hospital, num_patients, interarrival_time))
    # Generate patients in the simulation
    env.run(until=sim_duration)
    # Run the simulation for the specified duration

    avg_wait_time = sum(hospital.wait_times) / len(hospital.wait_times) if hospital.wait_times else 0
    # Calculate average wait time
    print(f"Number of patients: {num_patients}")
    print(f"Number of hospital staff: {num_staff}")
    print(f"Average wait time: {avg_wait_time:.2f} time")
    # Print the average wait time at the end of the simulation

# Example simulation parameters
num_patients = 400  # Total number of patients to simulate
num_staff = 40# Number of hospital staff available
interarrival_time = 2  # Average time between patient arrivals (in minutes)
sim_duration = 100  # Duration of simulation (in minutes)

# Run the simulation with the specified parameters
run_simulation(num_patients, num_staff, interarrival_time, sim_duration)
