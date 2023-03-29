import requests
import sys
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup


url = "https://www.educationquizzes.com"
html = requests.get(url + sys.argv[1])
quizes = []
s = BeautifulSoup(html.content, 'html.parser')

results = s.find("table", class_="zebralist")

for a in results.find_all('a', href=True):
  link = url + a['href']
  quizes.append(link)

quizes = quizes[1:]

uuid = 1
labels = ["a","b","c","d"]
questionsArr = []

for quiz in quizes:
  html = requests.get(quiz)
  soup = BeautifulSoup(html.content, 'html.parser')
  
  for i in range(10):
    result = soup.find(id=f"q_and_a_{i+1}")
    question = result.find("div", class_="quiz__question__question").text
    optionTag = result.find_all("div",class_="quiz__question__answers__answer")
    optionList = []
    answer = ""
    index = ""
    labels = ["a","b","c","d"]
    for option in optionTag:
      optionList.append(option.text.strip())
      if option.get("data-iscorrect") == "true":
        index = option.get("data-i")
      
    # print(question)
    # for option in options:
    #   print(option)
    # print(index)
    # print()

    
    options = []

    for idx, x in enumerate(optionList):
      option = {}
      option["id"] = int(idx)+1
      option["label"] = labels[idx]
      option["text"] = x
      options.append(option)

    jsondata = {
      "id": uuid,
      "question": question,
      "options": options,
      "answer": labels[int(index)-1]
    }
    uuid += 1
    
    questionsArr.append(jsondata)

jd = {
  "id": 1,
  "name": "Physics",
  "imageUrl": "none",
  "questions": questionsArr
}

# Serializing json
json_object = json.dumps(jd, ensure_ascii=False, indent=2)
    
# Writing to sample.json
with open(sys.argv[2], "w") as outfile:
  outfile.write(json_object)




