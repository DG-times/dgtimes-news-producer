from datetime import datetime
import json
import sys
from tqdm import tqdm

from model.news import News
from tool.JsonFileManager import JsonFileManager
from tool.RabbitmqContextManager import RabbitmqContextManager
import service.send_data_to_broker as send_data_to_broker
import service.make_dummy_data as make_dummy_data


if __name__ == '__main__':

    is_push_start = False
    sets = 1
    delay = 1

    for i, args in enumerate(sys.argv):

        if args == "--dummy":
            print("INFO : Making Dummy Data")
            make_dummy_data.run()
            print("INFO : Done")
            break

        if args == "--set":
            is_push_start = True
            sets = sys.argv[i+1]
        
        if args == "--delay":
            if not is_push_start:
                print("WARING : Before Setting Delay, Setting Sets First")
                break
            delay = sys.argv[i+1]
    
    if is_push_start:
        print(f"INFO : {int(sets) * 1000} Data And {delay}'s Delay ")

        """
        for i in tqdm(range(1)):
            news = JsonFileManager.read_data_from_local(f"data/{i}.json")
            send_data_to_broker.run(news, delay)
        """
