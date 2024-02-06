import win32gui

import input
import time
import manage_data
import scan_util
import argparse

TAB_COUNT = 9
MAX_CHIVES_IN_CATEGORY = 400

parser = argparse.ArgumentParser()
parser.add_argument("--cookie", help="set cookie", type=str)
parser.add_argument("-c", "--check", help="check items on stardb (needs --cookie \"COOKIE\")", action="store_true")
parser.add_argument("-u", "--uncheck", help="(NOT RECOMMENDED) uncheck items on stardb (needs --cookie \"COOKIE\"); "
                                            "unchecks only the visible achievements", action="store_true")
parser.add_argument("-fd", "--forcedownload", help="(RECOMMENDED ON FIRST USE) Force redownload of the achievements "
                                                   "list", action="store_true")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

debug = False if args.verbose is None else args.verbose
upload_while_scanning = False if args.check is None else args.check
do_uncheck_while_scanning = False if args.uncheck is None else args.uncheck
if args.cookie is not None:
    manage_data.set_cookie(args.cookie)
elif upload_while_scanning or do_uncheck_while_scanning:
    print("You need to specify the cookie with --cookie. Type 'python main.py --help' for more info.")
    exit()
force_download = False if args.forcedownload is None else args.forcedownload

completed_list: list[int] = []


if __name__ == '__main__':
    input.debug = debug
    manage_data.download(force=force_download)
    manage_data.process()
    hwnd = win32gui.FindWindow("UnityWndClass", "Honkai: Star Rail")
    if not hwnd:
        print("Honkai: Star Rail window not found. Is it running?")
        exit()
    win32gui.ShowWindow(hwnd, 5)
    win32gui.SetForegroundWindow(hwnd)

    input.load_gamepad()
    input.wake_up()
    time.sleep(0.3)
    scan_util.load_data()
    last_chive_id = -1
    current_tab = 1
    index = 0
    last_completed = 0
    completed_count = 0
    while index < MAX_CHIVES_IN_CATEGORY:
        if win32gui.GetForegroundWindow() != win32gui.FindWindow("UnityWndClass", "Honkai: Star Rail"):
            print("Stopping...")
            break
        is_chive_completed = scan_util.get_completed_status(index)
        if not is_chive_completed:
            if debug:
                chive_name, chive_id = scan_util.get_closest_name_match(index)
                print("Not completed", chive_id, chive_name)
            if not do_uncheck_while_scanning:
                print("Skipped uncompleted achievement")
                input.go_down()
                index += 1
                continue
        chive_name, chive_id = scan_util.get_closest_name_match(index)
        if chive_id == last_chive_id:
            if debug:
                print("Debug:", chive_id, chive_name)
            print(completed_count - last_completed, "completed achievements in this category")
            last_completed = completed_count
            if current_tab == TAB_COUNT:
                print("Scanned all achievements.")
                break
            print("Hit the bottom of the page. Switching tabs.")
            index = 0
            input.change_tab()
            current_tab += 1
            time.sleep(0.3)
            continue
        if is_chive_completed:
            print("Achievement:", chive_name, "| with id:", chive_id, "is completed.")
            completed_list.append(chive_id)
            if upload_while_scanning:
                manage_data.check_chive(chive_id)
            completed_count += 1
        elif do_uncheck_while_scanning:
            manage_data.uncheck_chive(chive_id)
        last_chive_id = chive_id
        input.go_down()
        index += 1
    manage_data.save_completed_list(completed_list)
    print("Completed:", completed_count)
