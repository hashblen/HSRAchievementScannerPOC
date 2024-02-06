import win32gui

import input
import time
import manage_data
import scan_util

TAB_COUNT = 9
MAX_CHIVES_IN_CATEGORY = 400

debug = False
upload_while_scanning = True
do_uncheck_while_scanning = False

completed_list: list[int] = []


if __name__ == '__main__':
    input.debug = debug
    manage_data.download()
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
