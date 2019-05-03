import csv

from requests_html import HTMLSession

session = HTMLSession()

URL = "http://vbpl.vn/TW/Pages/vanban.aspx?fromyear=01/01/2011&toyear=31/12/2020&dvid=13&Page="
MAX_PAGES = 875

with open("list.csv", mode="w", encoding="utf-8-sig", newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["sokyhieu", "trichyeu", "ngaybanhanh", "ngayhieuluc", "word"])

    for page in range(1, MAX_PAGES + 1):
        try:
            r = session.get(f"{URL}{page}")
        except Exception as e:
            r = None

        if r:
            items = r.html.find(".item")
            for item in items:
                try:
                    title = item.find(".title", first=True).text
                    description = item.find(".des", first=True).text
                    right_column = item.find(".green")
                    publish_date = right_column[0].text[-10:]
                    valid_date = right_column[1].text[-10:]
                    doc_file = item.find(".fileAttack a", first=True)

                    if doc_file:
                        doc_file = doc_file.attrs["href"].split(",")[-1]
                        doc_file = doc_file[1:-3]
                        doc_link = f"http://vbpl.vn/VBQPPL_UserControls/Publishing_22/pActiontkeFile.aspx?do=download&urlfile={doc_file}&filename={doc_file}"

                        # doc_content = requests.get(doc_link).content
                        # file_name = doc_file.split('/')[-1]
                        # doc_path = f'docs/{file_name}'
                        # with open(doc_path, mode='wb') as f:
                        #     f.write(doc_content)

                    print(title)
                    print(description)
                    print(publish_date)
                    print(valid_date)
                    print(doc_file)
                    print()

                    # csv_writer.writerow(
                    #     [title, description, publish_date, valid_date, doc_file]
                    # )

                except Exception as e:
                    print(e)
