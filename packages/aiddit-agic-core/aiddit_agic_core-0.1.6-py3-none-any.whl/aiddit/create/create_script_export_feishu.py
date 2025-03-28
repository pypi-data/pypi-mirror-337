from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
resource = [
    "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/猫咪围巾温暖圣诞头像系列_detail.json",
    "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/猫咪戴红灯笼金流苏装扮迎新春_detail.json",
    "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/猫咪躺在床上假装接电话拒绝出门_detail.json",
    "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/猫咪时尚秀场走秀系列拍摄_detail.json",
    "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/猫咪第一次玩滑梯的惊喜瞬间_detail.json"
]
data = []
all_result = []
for i in resource:
    try:
        all_result.append(json.load(open(i, 'r')))
    except Exception as e:
        print(f"{i} , {str(e)}")

for xuanti_creation in all_result:

    xuanti = xuanti_creation.get("script_data").get("xuanti_result").get("最终的选题")
    xuanti_description = xuanti_creation.get("script_data").get("xuanti_result").get("选题的详细描述信息")
    title = xuanti_creation.get("script_data").get("step_result").get("标题").get("ans")
    body_text = xuanti_creation.get("script_data").get("step_result").get("正文").get("ans")

    vision_common = xuanti_creation.get("image_detail").get("通用信息")

    script_data = xuanti_creation.get("script_data")
    image_list = [script_data.get("step_result").get("封面").get("ans").get("图片描述")] \
                 + [v.get("图片描述") for v in script_data.get("step_result").get("图集").get("ans").get("图片")]

    for idx, image in enumerate(xuanti_creation.get("image_detail").get("图片描述")):
        mj_images = [f"\"{i}\"" for i in image.get('results', [])]

        row = {
            "选题": xuanti if idx == 0 else None,
            "选题描述": xuanti_description if idx == 0 else None,
            '标题': title if idx == 0 else None,
            "正文": body_text if idx == 0 else None,
            "视觉通用信息": json.dumps(vision_common, ensure_ascii=False, indent=4) if idx == 0 else None,

            "脚本描述": image_list[idx],
            "图片描述": image.get("图片描述"),
            "生成图片": f"[{','.join(mj_images)}]",
        }
        data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = '50nE7t'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
