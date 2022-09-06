from tqdm import tqdm

from tool.JsonFileManager import JsonFileManager
from model.news import News


def run():

    print("INFO : Loading To Get Source Data")
    source_data = JsonFileManager.read_data_from_local("data/source_data/source_data.json")

    print("INFO : Start To Make Dummy Data")
    count = 0
    news_list = []
    for i in tqdm(range(len(source_data))):

        news = source_data[i]["news"]
        news_list.append(News(news["title"], news["content"], source_data[i]["keyword"]).toJSON())

        if (i+1) % 1000 == 0 or i+1 == len(source_data):
            JsonFileManager.save_data_in_local(f"data/{count}.json",news_list)
            count += 1
            news_list = []
