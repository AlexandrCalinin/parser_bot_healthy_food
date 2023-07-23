import json
import time
import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


rubrics = {
    'pp-obed': 7,
    'pp-deserty': 2,
    'pp-zavtrak': 4,
    'lyogkii-ujin': 2
}


def get_receptions_from_pages() -> None:
    """
    Function which collect recipies from different urls from site: https://1000.menu/ and load them to a json file
    :return: None
    """
    for names, pages_quantities in rubrics.items():
        list_result_search_dicts = list()
        for index in range(1, pages_quantities):
            url = f"https://1000.menu/catalog/{names}/" + f"{index}"
            response = requests.get(url, headers=headers)
            src = response.text
            soup = BeautifulSoup(src, "lxml")
            find_all_hrefs_for_recipes = soup.find(class_="cooking-block").find_all(class_="cn-item")

            for item in find_all_hrefs_for_recipes:
                try:
                    href = "https://1000.menu/" + item.find(class_="photo is-relative").find("a").get("href")
                    dish_name = item.find(class_="photo is-relative").find("a").find("img").get("alt")
                    resp = requests.get(url=href, headers=headers)
                    src = resp.text
                    soup = BeautifulSoup(src, "lxml")
                    image_url = "https:" + soup.find(class_="foto_gallery bl clrl link-no-style").find("img").get("src")
                    calories = item.find(class_="info-preview")\
                        .find(class_="icons level is-mobile font-small my-0 pt-2").find(class_="level-left")\
                        .find("span").text
                    cooking_time = item.find(class_="info-preview")\
                        .find(class_="icons level is-mobile font-small my-0 pt-2").find(class_="level-right")\
                        .find("span").text
                    list_result_search_dicts.append({"name": dish_name, "link": href, "image": image_url,
                                                     "calories": calories, "cooking_time": cooking_time})
                except AttributeError:
                    continue
            print(index)
        print(names)
        with open(f"results/result_{names}.json", "w") as file:
            json.dump(list_result_search_dicts, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    start = time.time()
    get_receptions_from_pages()
    end = time.time() - start
    print(end)
