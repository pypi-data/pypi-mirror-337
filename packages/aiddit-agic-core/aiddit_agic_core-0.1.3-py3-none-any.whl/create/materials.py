import json
import re
import image_article_comprehension.vector_database.pymilvus_client as pymilvus_client
import image_article_comprehension.utils as utils

create_script_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/打工人发现紧跟孙主席时间表的一周自律生活记录.json"

script = json.load(open(create_script_path, 'r'))

cover = script.get("step_result").get("封面").get('ans').get("图片描述")

print(cover)

images = [i.get("图片描述") for i in script.get("step_result").get("图集").get('ans').get("图片")]

print(images)

image_list = [cover] + images

image_material_result = []
for img in image_list:
    square_brackets = re.findall(r'\[([^\]]+)\]', img)
    angle_brackets = re.findall(r'<([^>]+)>', img)

    c = {}
    for i in square_brackets + angle_brackets:
        c[i] = ""
    r = {
        "description": img,
        "材料": c
    }

    image_material_result.append(r)

print(json.dumps(image_material_result, ensure_ascii=False, indent=4))

for e in image_material_result:
    for key in e["材料"].keys():
        res = pymilvus_client.query(key)
        filter = [{"材料名称": i.get("entity").get("name"), "材料描述": i.get("entity").get("description"),
                   "distance": i.get("distance")} for i in res
                  if i.get("distance") > 0.5]
        e["材料"][key] = filter[:3]

print(json.dumps(image_material_result, ensure_ascii=False, indent=4))

utils.save(image_material_result,
           "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/image_material_result.json")
