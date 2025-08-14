import threading
import queue
import barterStallTracker
import playerInventoryTracker
from collections import defaultdict, deque
from shared import contribution_msg_list, itemIdsToName, itemNameToIds, trackedItemsAndAmount
# A thread-safe queue to hold inventory change events
change_queue = queue.Queue()

def on_change(source, item_name, diff, player_name = None):
    """
    Called by each script when an inventory change happens.
    """
    change_queue.put((source, player_name, item_name, diff))

# Inject the callback into both scripts
barterStallTracker.on_inventory_change = on_change
playerInventoryTracker.on_inventory_change = on_change

def thread_runner(func, source_name):
    try:
        func()  # pass source name so script knows where event came from
    except Exception as e:
        print(f"{source_name} thread crashed:", e)

event_history = deque(maxlen=5)  # keep the last 500 events globally

def start():
        # Inject the callback into both scripts
    barterStallTracker.on_inventory_change = on_change
    playerInventoryTracker.on_inventory_change = on_change

    def thread_runner(func, source_name):
        try:
            func()  # pass source name so script knows where event came from
        except Exception as e:
            print(f"{source_name} thread crashed:", e)

    # Start each script in a thread
    t1 = threading.Thread(target=thread_runner, args=(barterStallTracker.main, "barterStallTracker"), daemon=True)
    t2 = threading.Thread(target=thread_runner, args=(playerInventoryTracker.main, "playerInventoryTracker"), daemon=True)

    t1.start()
    t2.start()

    while True:
        source, player, item, diff = change_queue.get()

        # Record the event globally
        event_history.append((source, player, item, diff))
        # If current is ADD from barter stall
        if source == "barter_stall" and diff > 0:
            for src, plyr, itm, d in reversed(event_history):
                #print(f"Player: {plyr} diff:{d} item: {itm} item {item}")
                if itm == item and src == "player" and d == -diff and itemNameToIds[item] in trackedItemsAndAmount:
                    #print(f"{plyr} added {diff} of {item}aaa")
                    contribution_msg_list.append(f"{plyr} added {diff} of {item}")
                    break

        # If current is REMOVE from player inventory
        elif source == "player" and diff < 0:
            for src, plyr, itm, d in reversed(event_history):
                #print(f"Player: {plyr} diff:{d} item: {itm} item {item}")
                if itm == item and src == "barter_stall" and d == -diff and itemNameToIds[item] in trackedItemsAndAmount:
                    #print(f"{player} added {d} of {item}")
                    contribution_msg_list.append(f"{player} added {d} of {item}")
                    break
                
if __name__ == "__main__":
    start()