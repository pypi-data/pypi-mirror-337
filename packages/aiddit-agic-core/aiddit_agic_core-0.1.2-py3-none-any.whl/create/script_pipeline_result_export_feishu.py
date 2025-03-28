from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
from itertools import groupby

# Directory containing the data files
result_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/从众效应：旅行选择中的心理陷阱.json"

result = json.load(open(result_path, 'r'))
data = []

data.append({
    "-1": "脚本模式",
    "1": json.dumps(result.get("script_mode"), ensure_ascii=False, indent=4),
    "2": None,
})

data.append({
    "-1": "选题",
    "1": json.dumps(result.get("xuanti_result"), ensure_ascii=False, indent=4),
    "2": None,
})

data.append({
    "-1": "模块生成顺序",
    "1": result.get("step_result").get("dispatch").get("ans"),
    "2": result.get("step_result").get("dispatch").get("reason"),
})

data.append({
    "-1": "标题",
    "1": result.get("step_result").get("标题").get("ans"),
    "2": result.get("step_result").get("标题").get("reason"),
})

data.append({
    "-1": "正文",
    "1": result.get("step_result").get("正文").get("ans"),
    "2": result.get("step_result").get("正文").get("reason"),
})

data.append({
    "-1": "视觉整体规划",
    "1": json.dumps(result.get("step_result").get("vision_prepare").get("ans"), ensure_ascii=False, indent=4),
    "2": result.get("step_result").get("vision_prepare").get("reason"),
})

data.append({
    "-1": "封面",
    "1": json.dumps(result.get("step_result").get("封面").get("ans"), ensure_ascii=False, indent=4),
    "2": result.get("step_result").get("封面").get("reason"),
})

data.append({
    "-1": "图集",
    "1": json.dumps(result.get("step_result").get("图集").get("ans"), ensure_ascii=False, indent=4),
    "2": result.get("step_result").get("图集").get("reason"),
})

for message in result.get("messages"):
    data.append({
        "-1": "对话",
        "1": message.get("role"),
        "2": message.get("content"),
    })

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = 'qnG671'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id)
