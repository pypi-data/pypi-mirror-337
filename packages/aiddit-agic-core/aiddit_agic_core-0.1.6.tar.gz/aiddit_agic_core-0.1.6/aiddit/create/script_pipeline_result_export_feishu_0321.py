from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
import image_article_comprehension.aiddit.utils as utils

# Directory containing the data files
data_dir = '/image_article_comprehension/aiddit/create/result/xuant_search/account_泡芙小姐美食日记_5b9a165c316ccf00013609ae'
data = []

all_result = []
for i in [f for f in os.listdir(data_dir)]:
    try:
        all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))
    except Exception as e:
        print(f"{i} , {str(e)}")

renshe_info_inserted  = False

for r_index, result in enumerate(all_result):

    generated_results = []

    renshe_info = json.load(open(result.get("renshe_path"), 'r'))
    account_link = renshe_info.get("account_info").get("account_link")

    for i in result.keys():
        if i.startswith("script_generate_result"):
            generated_results.append(result[i])
    xuanti_inserted = False

    for index, r in enumerate(generated_results):
        search_note = r.get("reference_note")
        search_note_images = [f"\"{i}\"" for i in utils.remove_duplicates(search_note.get('images', []))]

        history_note = r.get("history_note")

        history_note_detail = []
        for n in history_note:
            history_note_detail.append({
                "title_body_text": f"{n.get('title')}\n\n{n.get('body_text')}",
                "images": [f"\"{i}\"" for i in utils.remove_duplicates(n.get('images', []))]
            })

        script = r.get("script").get("创作的脚本")
        loop_count = max(len(script.get("图集描述")),len(history_note_detail))
        generated_image = r.get("generated_images")
        generated_image_without_materials = r.get("generated_images_without_materials")
        image_description = script.get('图集描述')
        merged_materials = r.get("merged_materials")

        for generated_index in range(loop_count):
            row = {
                "人设特点": (json.dumps(renshe_info.get("renshe_xuanti_unique"), indent=4, ensure_ascii=False) +"\n\n"+account_link) if  renshe_info_inserted is False else None,
                "人设脚本模式": json.dumps(renshe_info.get("script_mode"), indent=4, ensure_ascii=False) if  renshe_info_inserted is False else None,
                "选题": result.get("xuanti_creation").get("最终的选题") if  xuanti_inserted is False else None,
                "选题匹配历史帖子标题&正文": history_note_detail[generated_index].get("title_body_text") if generated_index in range(
                    len(history_note_detail)) else None,
                "选题匹配历史帖子图片": f"[{','.join(history_note_detail[generated_index].get('images'))}]" if generated_index in range(
                    len(history_note_detail)) else None,
                "搜索帖子标题&正文": search_note.get("title") + "\n\n" + search_note.get(
                    "body_text") if generated_index == 0 else None,
                "搜索帖子图片": f"[{','.join(search_note_images)}]" if generated_index == 0 else None,
                "生成脚本逻辑": script.get("图集构建逻辑") if generated_index == 0 else None,
                "结合说明": script.get("结合逻辑/理由") if generated_index == 0 else None,
                "脚本图片描述": image_description[generated_index] if generated_index in range(
                    len(image_description)) else None,
                "脚本图片生成": utils.get_file_uri(
                    generated_image[generated_index]) if generated_index in range(
                    len(generated_image)) else None,
            }

            xuanti_inserted = True
            renshe_info_inserted = True

            data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = '2qX1OL'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
