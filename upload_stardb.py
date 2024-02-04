import manage_data
import time

L = manage_data.open_completed_list()
for chive_id in L:
    manage_data.check_chive(chive_id)
    time.sleep(0.05)
print("Finished checking chives.")
