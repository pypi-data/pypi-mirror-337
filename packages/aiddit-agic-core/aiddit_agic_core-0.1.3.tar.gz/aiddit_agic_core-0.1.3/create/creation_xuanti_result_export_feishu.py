from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
data_dir = '/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/result/image_since_0113/手訫'
data = []

all_result = []
for i in [f for f in os.listdir(data_dir) if f.endswith('.json')]:
    try:
        all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))
    except Exception as e:
        print(f"{i} , {str(e)}")

for result in all_result:
    images = [f"\"{i}\"" for i in result.get('reference_note', {}).get('images', [])]

    xuanti_creation_by_note = result.get("xuanti_creation_by_note", {})
    depend_renshe = result.get("renshe", {})
    mj_images = [f"\"{i}\"" for i in xuanti_creation_by_note.get('midjourney_image', [])]

    for index, xuanti_creation in enumerate(result.get("xuanti_creation", [])):
        xuanti = xuanti_creation.get("xuanti_creation", {})
        mode = xuanti_creation.get("xuanti_mode", {})
        estimate = xuanti_creation.get("xuanti_estimate", {})
        row = {
            '个人主页链接': f"{os.path.basename(data_dir).split('_')[-1]} \n\n{depend_renshe.get('account_link', '')}",
            "创作灵魂": json.dumps(depend_renshe.get("renshe_xuanti_unique", {}).get("创作灵魂", ""),
                                   ensure_ascii=False, indent=4),
            "内容品类": json.dumps(depend_renshe.get("renshe_xuanti_unique", {}).get("内容品类", ""),
                                   ensure_ascii=False, indent=4),
            "选题必要点": json.dumps(depend_renshe.get("renshe_xuanti_unique", {}).get("选题必要点", ""),
                                     ensure_ascii=False, indent=4),
            "选题模式": json.dumps(depend_renshe.get("renshe_xuanti_mode", {}).get("modes", []), ensure_ascii=False,
                                   indent=4),

            '刺激源链接': result.get('reference_note', {}).get('link', '') if index >= 0 else "",
            '刺激源': f"[{','.join(images)}]" if index >= 0 else "",

            '参与创作的选题模式': mode.get("选题模式", ""),
            '参考源能否产生选题': xuanti.get("能否产生选题", ""),
            '不能产生选题的原因': xuanti.get("不能产生选题的原因", ""),
            '最终的选题': xuanti.get("最终的选题", ""),
            '选题的详细描述信息': xuanti.get("选题的详细描述信息", ""),
            "选题的参考来源": xuanti.get("选题的参考来源", ""),
            "选题依赖的关键信息": json.dumps(xuanti.get("选题依赖的关键信息", ""), ensure_ascii=False, indent=4),
            '选题符合是否要求': estimate.get("选题符合是否要求", ""),
            "选题解释": estimate.get("选题解释", ""),
            "选题描述符合是否要求": estimate.get("选题描述符合是否要求", ""),
            "选题描述解释": estimate.get("选题描述解释", ""),
        }
        data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = 'o9JdlE'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
