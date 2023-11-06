import json
import requests
from bs4 import BeautifulSoup


rubrics = {
    'pp-obed': 7,
    'pp-deserty': 2,
    'pp-zavtrak': 3,
    'lyogkii-ujin': 3
}


def get_receptions_from_pages() -> None:
    """
    Function which collect recipies from different urls from site: https://1000.menu/ and load them to a json file
    :return: None
    """
    for names, pages_quantities in rubrics.items():
        list_result_search_dicts = list()
        counter = 0
        for index in range(1, pages_quantities + 1):
            url = f"https://1000.menu/catalog/{names}/" + f"{index}"
            response = requests.get(url)
            src = response.text
            soup = BeautifulSoup(src, "lxml")
            find_all_hrefs_for_recipes = soup.find(class_="cooking-block").find_all(class_="cn-item")

            for item in find_all_hrefs_for_recipes:
                try:
                    counter += 1
                    id = counter
                    href = "https://1000.menu/" + item.find(class_="photo is-relative").find("a").get("href")
                    dish_name = item.find(class_="photo is-relative").find("a").find("img").get("alt")
                    calories = item.find(class_="info-preview")\
                        .find(class_="icons level is-mobile font-small my-0 pt-2").find(class_="level-left")\
                        .find("span").text
                    cooking_time = item.find(class_="info-preview")\
                        .find(class_="icons level is-mobile font-small my-0 pt-2").find(class_="level-right")\
                        .find("span").text
                    list_result_search_dicts.append({"id": id, "name": dish_name, "link": href,
                                                     "calories": calories, "cooking_time": cooking_time})
                except AttributeError:
                    counter -= 1
        with open(f"../telebot/database/results/result_{names}.json", "w") as file:
            json.dump(list_result_search_dicts, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print('start scraping...')
    get_receptions_from_pages()
    print('end scraping...')
