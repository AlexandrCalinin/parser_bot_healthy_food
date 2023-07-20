import json
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

result_search = dict()


def get_receptions_from_pages():
    for i in range(1, 4):
        url = "https://1000.menu/catalog/pp-zavtrak/" + f"{i}"
        response = requests.get(url, headers=headers)
        src = response.text
        soup = BeautifulSoup(src, "lxml")
        find_all_hrefs_for_recipes = soup.find(class_="cooking-block").find_all(class_="cn-item")

        for item in find_all_hrefs_for_recipes:
            try:
                href = "https://1000.menu/" + item.find(class_="photo is-relative").find("a").get("href")
                dish_name = item.find(class_="photo is-relative").find("a").find("img").get("alt")
                result_search[dish_name] = href
            except AttributeError:
                print("Error...")
    with open(f"results/result_breakfast.json", "w") as file:
        json.dump(result_search, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    get_receptions_from_pages()
