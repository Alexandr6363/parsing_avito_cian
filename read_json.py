import json

link = "https://www.avito.ru//osinki/doma_dachi_kottedzhi/dom_648m_na_uchastke_14sot._2370421498"

link_object = {
    "link_of_house": link
}
with open('data.txt') as old_data_file:
    old_data= json.loads(old_data_file.read())["link"]
    
    if link_object not in old_data:
        print("no")
    elif link_object in old_data:
        print("yes")
    else:
        print("something wrong")
