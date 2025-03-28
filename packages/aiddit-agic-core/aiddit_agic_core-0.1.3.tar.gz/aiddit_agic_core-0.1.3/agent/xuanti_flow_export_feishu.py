from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
data_dir = '/Users/nieqi/Documents/workspace/python/image_article_comprehension/agent/result/input/xuanti'
data = []

all_result = []
for i in [f for f in os.listdir(data_dir) if f.endswith('.json')]:
    try:
        all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))
    except Exception as e:
        print(f"{i} , {str(e)}")

for r in all_result:

    xuanti = r.get("选题结果").get("最终的选题")
    path = f"/Users/nieqi/Documents/workspace/python/image_article_comprehension/agent/result/workflow/{xuanti}/search_analyse"

    list = [json.load(open(os.path.join(path, d), "r")) for d in os.listdir(path) if
                               d.endswith(".json")]
    for index, result in enumerate(list):
        images = [f"\"{i}\"" for i in result.get("note_info").get('images', [])]

        row = {
            "选题": r.get("选题结果").get("最终的选题") if index == 0 else None,
            "images": f"[{','.join(images)}]",
            "标题": result.get("note_info").get("title"),
            "正文": result.get("note_info").get("body_text"),
            "点赞数": result.get("note_info").get("like_count"),
            "收藏数": result.get("note_info").get("collect_count"),
            "是否相同选题": result.get("search_analyse_filter").get("是否相同选题"),
            "契合程度": result.get("search_analyse_filter").get("契合程度"),
            "契合理由": result.get("search_analyse_filter").get("契合理由"),
            "契合点": json.dumps(result.get("search_analyse_filter").get("契合点"), ensure_ascii=False, indent=4),
        }
        data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = 'v6uyHL'

write_data_to_sheet(data_with_header, sheet_token=sheet_token, sheetid=sheet_id)
