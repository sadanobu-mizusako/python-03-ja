import requests
import json

API_URL = "https://jsonplaceholder.typicode.com"

def list_posts():
    res = requests.get(API_URL+"/posts")
    res.raise_for_status()
    return res.json()

def create_post():
    title = input("input title: ").strip()
    body = input("input body: ").strip()
    data = {"title": title, "body": body}
    # res = requests.post(API_URL+"/posts", json=json.dumps(data))
    res = requests.post(API_URL+"/posts", data=data)
    res.raise_for_status()
    return res.json()

def update_post():
    target_id = input("input target id: ").strip()
    title = input("input title: ").strip()
    body = input("input body: ").strip()

    data = {"title": title, "body": body}
    res = requests.put(API_URL+"/posts"+"/"+target_id, data=data)
    res.raise_for_status()
    return res.json()

def delete_post():
    target_id = input("input target id: ").strip()
    res = requests.delete(API_URL+"/posts"+"/"+target_id)
    res.raise_for_status()
    return res.json()

while True:
    command = input("select command: \n1: list_posts \n2: create_post \n3: update_post \n4: delete_post \n5: exit\n")
    if command=="1":
        try:
            res = list_posts()
        except Exception as e:
            print(e)
        else:
            for r in res:
                print(r)
    elif command=="2":
        try:
            res = create_post()
        except Exception as e:
            print(e)
        else:
            print("successfully created your post")
            print(res)
    elif command=="3":
        try:
            res = update_post()
        except Exception as e:
            print(e)
        else:
            print("successfully updated the target post")
            print(res)
    elif command=="4":
        try:
            res = delete_post()
        except Exception as e:
            print(e)
        else:
            print("successfully deleted the target post")
            print(res)
    elif command=="5":
        print("shut down the system. thank you!")
        break
    else:
        print("invalid input! input again.")