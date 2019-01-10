import json
# import math

hospitals = {}
dc = 0

filted = ['医院概况', '概况', '基本概况', '历史概况', '一、概况']

skiped = 0

with open('hospital.json') as f:
    json_obj = json.load(f)
    for page in json_obj:
        for title in page:
            if title in filted:
                skiped += 1
                continue
            if title not in hospitals:
                hospitals[title] = page[title]
            else:
                skiped += 1
print(f'Skip {skiped} records because of duplicated or filted.')

titles = sorted(hospitals.keys())

writed = 0
with open('hospital_all.md', 'w') as f:
    for title in titles:
        f.write(f'# {title}\n')
        f.write(f'{hospitals[title]}\n\n')
        writed += 1

# for i in range(math.ceil(len(titles) / 800)):
#     with open(f'hospital_{i+1}.md', 'w') as f:
#         lb = i * 800
#         hb = (i + 1) * 800
#         hb = hb if hb < len(titles) else len(titles)
#         for ki in range(lb, hb):
#             title = titles[ki]
#             content = hospitals[title]
#             f.write(f'# {title}\n')
#             f.write(f'{content}\n\n')

print(f'Read {len(titles)} hospitals, write {writed} hospitals.')
