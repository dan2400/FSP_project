import requests
import fitz

#import catalog.models

#import dotenv

#dotenv.load_dotenv()

def check_new_block(s):
    try:
        if int(s) and s.startswith('2') and len(s)==16:
            return True
    except ValueError:
        return False


def extract_text(page_, result, index):
    text_ = page_.extract_text()
    result[index] = text_


def download_pdf_with_headers(url, save_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "application/pdf",
        "Referer": "https://google.com",
    }

    try:
        response = requests.get(url, headers=headers, stream=True,
                                verify="etc/ssl/website.crt")
        response.raise_for_status()

        with open(save_path, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)

        print(f"PDF downloaded successfully and saved to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download PDF: {e}")


pdf_url = "https://storage.minsport.gov.ru/cms-uploads/cms/II_chast_EKP_2024_14_11_24_65c6deea36.pdf"
save_location = "static_dev/files/II_chast_EKP_2024_with_certificate.pdf"

download_pdf_with_headers(pdf_url, save_location)

pdf_path = save_location

doc = fitz.open(pdf_path)
text = ''
for page in doc:
    text += page.get_text() + '\n'

arr = text.split('\n\n')

split_arr = []
for el in arr:
    split_arr+=el.split('\n')

new_arr = []
stack = []
database = dict()
sport_name = split_arr[19]
database[sport_name]=[]
new_sport = False

for el in split_arr:
    if el.startswith("Стр. ") or el.startswith("Основной состав") or el.startswith("Молодежный (резервный) состав"):
        continue
    if check_new_block(el):
        if stack and stack[0]!='':
            new_arr.append(stack)
        stack = []
    stack.append(el)

if stack:
    new_arr.append(stack)
new_arr = new_arr[1:]
del new_arr[-1][-1]

for block in new_arr:
    json_res = dict()
    json_res['id']=block[0]
    json_res['sport_name']=[]
    json_res['disciplines']=[]
    json_res['date'] = []
    i = 1
    while block[i].isupper():
        json_res['sport_name'].append(block[i])
        i+=1
    json_res['gen_age_block']=block[i]
    i+=1
    while block[i][0].isupper():
        json_res['disciplines'].append(block[i])
        i+=1
    while block[i][0].isnumeric():
        json_res['date'].append(block[i])
        i+=1
    if not block[-1].isnumeric():
        new_sport = True
        next_sport_name = block[-1]
        del block[-1]
    json_res['location']=block[i:-1]
    json_res['participants']=block[-1]
    database[sport_name].append(json_res)
    if new_sport:
        database[next_sport_name]=[]
        new_sport=False
        sport_name = str(next_sport_name)

print(database)

#def loc(id, lis):
#    if len(lis) == 2:
#        catalog.models.Items.objects.get_or_create(country__name=lis[0], subject__name=lis[1], town__name=lis[1], id=id)
#    else:
#        catalog.models.Items.objects.get_or_create(country__name=lis[0], subject__name=lis[1], town__name=lis[2], id=id)

#for item in database:
#    i, created_id = catalog.models.Items.objects.get_or_create(id=item['id'])
#    num, created_num = catalog.models.Items.objects.get_or_create(number=item['participants'], id=i)
#    for sport in item['sport_name']:
#        catalog.models.Items.objects.get_or_create(sport__name=sport, id=i)
#    for discipline in item['discipline']:
#        catalog.models.Items.objects.get_or_create(sport__name=discipline, id=i)
#    if item['date'][0] and item['date'][1]:
#        catalog.models.Items.objects.get_or_create(time__start=item['date'][0], time__end=item['date'][1], id=i)
#    loc(i, item['location'])
#    bl = item['gen_age_block']
#    ak = bl.split()[-2]
#    if '-' in ak:
#        ak = ak.split('-')
#    elif 'от' in ak.lower():
#        ak = (ak, 200)
#    elif 'до' in ak.lower():
#        ak = (0, ak)
#    bl = ' '.join(ak[:-2])
#    for genage in bl.split(', '):
#        catalog.models.Items.objects.get_or_create(genage__name=genage, id=i)
#    catalog.models.Items.objects.get_or_create(genage__age__low=ak[0], genage__age__hight=ak[1], id=i)

