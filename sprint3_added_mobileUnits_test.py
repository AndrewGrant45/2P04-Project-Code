import simpy
import random

class Hospital:
    def __init__(self, env, num_staff, num_mobile_units):
        self.env = env
        self.staff = simpy.Resource(env, capacity=num_staff)
        self.mobile_units = simpy.Resource(env, capacity=num_mobile_units)
        self.wait_times = []  # List to store wait times of patients

    def triage_patient(self, patient):
        if random.random() < 0.6:
            # 60% chance of assigning patient to hospital staff
            with self.staff.request() as request:
                yield request
                wait_time = self.calculate_wait_time(len(self.staff.users))
                yield self.env.timeout(wait_time)
                self.wait_times.append(wait_time)
        else:  # 40% chance of assigning patient to mobile units
            with self.mobile_units.request() as request:
                yield request
                wait_time = self.calculate_wait_time(len(self.mobile_units.users)) * 0.1
                # Reduced wait time for mobile units
                yield self.env.timeout(wait_time)
                self.wait_times.append(wait_time)

    def calculate_wait_time(self, num_resources):
        base_wait_time = 500
        load_factor = max(1, num_staff - num_staff)
        return base_wait_time / load_factor

class Patient:
    def __init__(self, name, arrival_time):
        self.name = name
        self.arrival_time = arrival_time

def patient_generator(env, hospital, num_patients, interarrival_time):
    for i in range(num_patients):
        patient = Patient(f'Patient-{i+1}', env.now)
        env.process(hospital.triage_patient(patient))
        yield env.timeout(interarrival_time)

def run_simulation(num_patients, num_staff, num_mobile_units, interarrival_time, sim_duration):
    env = simpy.Environment()
    hospital = Hospital(env, num_staff, num_mobile_units)
    env.process(patient_generator(env, hospital, num_patients, interarrival_time))
    env.run(until=sim_duration)

    avg_wait_time = sum(hospital.wait_times) / len(hospital.wait_times) if hospital.wait_times else 0
    print(f"Number of patients: {num_patients}")
    print(f"Number of hospital staff: {num_staff}")
    print(f"Number of mobile health units: {num_mobile_units}")
    print(f"Average wait time: {avg_wait_time:.2f} time units")

# Example simulation parameters
num_patients = 400
num_staff = 7
num_mobile_units = 2  # Number of mobile health units available
interarrival_time = 2
sim_duration = 100

# Run the simulation with the specified parameters
run_simulation(num_patients, num_staff, num_mobile_units, interarrival_time, sim_duration)


#Patients have a 60% chance of being assigned to hospital staff and a 40% chance of being assigned to mobile units,
#simulating the allocation process based on probability.
#Wait times for patients assigned to mobile units are reduced by half (multiplied by 0.5) to reflect the
#benefits of immediate care and faster treatment provided by mobile health units.
#The number of mobile health units (num_mobile_units) is now a parameter in the simulation,
#allowing us to vary the impact of mobile units on patient wait times during the simulation.

