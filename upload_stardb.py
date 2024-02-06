import manage_data
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cookie", help="set cookie", type=str)
args = parser.parse_args()
if args.cookie is not None:
    manage_data.set_cookie(args.cookie)
else:
    print("You need to specify the cookie with --cookie. Type 'python main.py --help' for more info.")
    exit()

L = manage_data.open_completed_list()
for chive_id in L:
    manage_data.check_chive(chive_id)
    time.sleep(0.05)
print("Finished checking chives.")
