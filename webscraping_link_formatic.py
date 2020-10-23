from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup

#Requests Headers found with the browser’s Developer Tools
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.formatic-centre.fr",
    "referer": "https://www.formatic-centre.fr/formation/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.99 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


#raw string found with the browser’s Developer Tools
#raw_string = "action=swlabscore&module%5B%5D=top.Top_Controller&module%5B%5D=ajax_get_course_pagination&params%5B0%5D%5Bpage%5D=2&params%5B0%5D%5Batts%5D%5Blayout%5D=course&params%5B0%5D%5Batts%5D%5Blimit_post%5D=&params%5B0%5D%5Batts%5D%5Boffset_post%5D=0&params%5B0%5D%5Batts%5D%5Bsort_by%5D=&params%5B0%5D%5Batts%5D%5Bpagination%5D=yes&params%5B0%5D%5Batts%5D%5Blocation_slug%5D=&params%5B0%5D%5Batts%5D%5Bcolumns%5D=2&params%5B0%5D%5Batts%5D%5Bpaged%5D=&params%5B0%5D%5Batts%5D%5Bcur_limit%5D=&params%5B0%5D%5Batts%5D%5Brows%5D=0&params%5B0%5D%5Batts%5D%5Bbtn_content%5D=En+savoir+plus&params%5B0%5D%5Batts%5D%5Buniq_id%5D=block-13759488265f916bca45c89&params%5B0%5D%5Batts%5D%5Bthumb-size%5D%5Blarge%5D=swedugate-thumb-300x225&params%5B0%5D%5Batts%5D%5Bthumb-size%5D%5Bno-image%5D=thumb-300x225.gif&params%5B0%5D%5Batts%5D%5Bthumb-size%5D%5Bsmall%5D=swedugate-thumb-300x225&params%5B0%5D%5Blayout_course%5D=style-grid&ZmfUNQ=63y[Jt&PmhpIuZ_cTnUxqg=7v@IahmJNMplbCu&cZWVDbSPzTXRe=n9oa2k5u4GHWm&eOBITfdGRuriQ=hBPN5nObe.ktH"


#formdata found with the browser’s Developer Tools
payloadd = [
    ('action', 'swlabscore'),
    ('module[]', 'top.Top_Controller'),
    ('module[]', 'ajax_get_course_pagination'),
    ('params[0][page]', '1'),
    ('params[0][atts][layout]', 'course'),
    ('params[0][atts][offset_post]', '0'),
    ('params[0][atts][pagination]', 'yes'),
    ('params[0][atts][columns]', '2'),
    ('params[0][atts][rows]', '0'),
    ('params[0][atts][btn_content]', 'En savoir plus'),
    ('params[0][atts][uniq_id]', 'block-13759488265f916bca45c89'),
    ('params[0][atts][thumb-size][large]', 'swedugate-thumb-300x225'),
    ('params[0][atts][thumb-size][no-image]', 'thumb-300x225.gif'),
    ('params[0][atts][thumb-size][small]', 'swedugate-thumb-300x225'),
    ('params[0][layout_course]', 'style-grid'),
    ('ZmfUNQ', '63y[Jt'),
    ('PmhpIuZ_cTnUxqg', '7v@IahmJNMplbCu'),
    ('cZWVDbSPzTXRe', 'n9oa2k5u4GHWm'),
    ('eOBITfdGRuriQ', 'hBPN5nObe.ktH'),
]


all_links = []
for page in range(1, 10):
    payloadd.pop(3)
    payloadd.insert(3, ('params[0][page]', str(page)))
    response = requests.post(
        "https://www.formatic-centre.fr/wp-admin/admin-ajax.php?",
        headers=headers,
        data=urlencode(payloadd)
    )
    print(f"Getting links from page {page}...")
    soup = BeautifulSoup(response.text, "html.parser").find_all("a", class_="btn btn-green")
    links = [i["href"] for i in soup]
    print('\n'.join(links))
    all_links.extend(links)


with open("formation_links.txt", "w") as f:
    f.writelines("\n".join(all_links) + "\n")