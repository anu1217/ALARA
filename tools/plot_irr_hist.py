import numpy as np
import matplotlib.pyplot as plt

def read_out(output_path):
    with open(output_path, "r") as output_file:
        out_lines = output_file.readlines()
    return out_lines    

def read_type_schedule(out_lines):
    sub_sched_dict = {}
    for line_idx, line in enumerate(out_lines):
        if line.strip().startswith("schedule"): # ignore the top_schedule line
            sub_sched_dict[line.strip().split()[1]] = {"sub_pulse_history" : line.strip().split()[3],
                                                       "sub_delay_dur" : line.strip().split()[5],
                                                       "sub_delay_units" : line.strip().split()[6]
                                                      }                                        
    return sub_sched_dict          

def 


def read_pulse_histories(out_lines):    
    pulse_dict = {}
    for line_idx, line in enumerate(out_lines):
        if line.strip().startswith("pulse_history"):
            pulse_dict[line.split()[1].strip("':")] = {"num_pulses_per_level": out_lines[line_idx+2].split(":")[1], 
                                                   "delay_seconds_per_level": out_lines[line_idx+3].split(":")[1]
                                                  }                                                                                          
    return pulse_dict   

def read_schedule_helper(out_lines, start_idx):
    # assume for now there is only one schedule and that it's the top one
    sch_dict = {}
    counter = 1
    for line_idx, line in enumerate(out_lines, start=start_idx+1):
        if line.strip()startswith("pulse_entry"):
            sch_dict[f"top_sched_entry_{counter}"] = {"entry_dur": line.split()[1], 
                                            "entry_dur_units": line.split()[2], 
                                            "corr_ph_name": line.split()[4],
                                            "delay_dur": line.split()[6],
                                            "delay_dur_units": line.split()[7]}
            counter += 1   
        if line.strip()startswith("pulse_entry") == False:
            break                              
    return sch_dict

def read_schedule(out_lines):
    # assume for now there is only one schedule and that it's the top one
    sch_dict = {}
    counter = 1
    for line_idx, line in enumerate(out_lines):
        if line.startswith("\tpulse_entry") == True:
            sch_dict[f"top_sched_entry_{counter}"] = {"entry_dur": line.split()[1], 
                                            "entry_dur_units": line.split()[2], 
                                            "corr_ph_name": line.split()[4],
                                            "delay_dur": line.split()[6],
                                            "delay_dur_units": line.split()[7]}
            counter += 1                             
    return sch_dict

def convert_sch_seconds(sch_dict, sub_sched_dict):
    unit_multiples = {
    'c' : 60 * 60 * 24 * 365 * 100,
    'y' : 60 * 60 * 24 * 365,
    'w' : 60 * 60 * 24 * 7,
    'd' : 60 * 60 * 24,
    'h' : 60 * 60,
    'm' : 60,
    's' : 1
                     }
    for value in sch_dict.values():      
        entry_dur_unit = value["entry_dur_units"]
        delay_dur_unit = value["delay_dur_units"]
        value["entry_dur"] = float(value["entry_dur"]) * unit_multiples[entry_dur_unit]    
        value["delay_dur"] = float(value["delay_dur"]) * unit_multiples[delay_dur_unit]   
        value["entry_dur_units"] = value["delay_dur_units"] = 's'
    
    for value in sub_sched_dict.values():      
        sub_delay_unit = value["sub_delay_units"] 
        value["sub_delay_dur"] = float(value["sub_delay_dur"]) * unit_multiples[sub_delay_unit]   
        value["sub_delay_units"] = value["sub_delay_units"] = 's'    
    return sch_dict, sub_sched_dict     

def store_irr_times(pulse_dict, sch_dict):
    irr_times = []
    dummy_heights = []
    t = 0
    for value in sch_dict.values():
        entry_dur = value["entry_dur"]
        delay_dur = value["delay_dur"]
        num_pulses_per_level = eval(pulse_dict[value["corr_ph_name"]]["num_pulses_per_level"])
        delay_seconds_per_level = eval(pulse_dict[value["corr_ph_name"]]["delay_seconds_per_level"])

        for num_pulse_id, num_pulse in enumerate(num_pulses_per_level):
            for pulse in range(num_pulse):
                t += entry_dur
                irr_times.append(t)
                dummy_heights.append(1)
                #make this more pythonic...
                if pulse != num_pulse - 1:
                    t += delay_seconds_per_level[num_pulse_id]
                    irr_times.append(t)
                    dummy_heights.append(0)  
                elif value != list(sch_dict.values())[-1]: #leave out any nonzero delay times in last schedule level entry
                        t += delay_dur 
                        irr_times.append(t)   
                        dummy_heights.append(0)
    return irr_times, dummy_heights            

def plot_irr_hist(irr_times, dummy_heights):  
    #figure out the scaling here...
    irr_times_norm = [irr_time / irr_times[-1] for irr_time in irr_times]
    plt.bar(irr_times_norm, dummy_heights)
    #modify x-limits and y-limits
    plt.savefig('ex.png')
    plt.show()       


def main():
    output_path = '../../../test_dir/final_test_out'

    out_lines = read_out(output_path)
    sub_sched_dict = read_type_schedule(out_lines)

    # sch_dict = read_schedule(out_lines)
    #sch_dict, sub_sched_dict = convert_sch_seconds(sch_dict, sub_sched_dict)
    pulse_dict = read_pulse_histories(out_lines)
    sch_dict = read_schedule_helper(out_lines, start_idx)
    #irr_times, dummy_heights = store_irr_times(pulse_dict, sch_dict)
    #plot_irr_hist(irr_times, dummy_heights)

if __name__ == '__main__':
    main()        

