from image_analyzer.utils.feshu import write_data_to_sheet
import pandas as pd
import os
import json
import image_article_comprehension.utils as utils

# Directory containing the data files
data_dir = '/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/result/xuant_search/account_泡芙小姐美食日记_5b9a165c316ccf00013609ae'
data = []

all_result = []
for i in [f for f in os.listdir(data_dir)]:
    try:
        all_result.append(json.load(open(os.path.join(data_dir, i), 'r')))
    except Exception as e:
        print(f"{i} , {str(e)}")

for result in all_result:
    reference_note_images = [f"\"{i}\"" for i in result.get('reference_note', {}).get('images', [])]

    renshe_info = json.load(open(result.get("renshe_path"),"r"))

    # search_m_names =  [i.get("materials_name") for i in result.get("script_materials")]
    # search_m_images = [f"\"{i.get('image')}\"" for i in result.get('script_materials', {})]
    #
    # use_m_names = [i.get("name") for i in result.get("image_detail").get("vision_materials")]
    # use_m_images = [f"\"{i.get('image')}\"" for i in result.get("image_detail").get("vision_materials")]

    search_summary_script = result.get("search_script_summary")

    renshe_script_summary = result.get("renshe_script_summary")

    match_script_summary = result.get("best_script_match")

    for index, search_note in enumerate(result.get("搜索结果").values()):
        search_note_images = [f"\"{i}\"" for i in utils.remove_duplicates(search_note.get('images', []))]

        row = {
            "选题":  result.get("xuanti_creation").get("最终的选题") if index == 0 else None,
            "刺激源标题&正文": result.get("reference_note").get("title") +"\n\n"+ result.get("reference_note").get("body_text") if index == 0 else None,
            "刺激源图片": f"[{','.join(reference_note_images)}]" if index == 0 else None,
            "搜索关键词" : result.get("搜索关键词") if index == 0 else None,
            "帖子id": search_note.get("channel_content_id"),
            "搜索帖子标题&正文": search_note.get("title") +"\n\n"+ search_note.get("body_text"),
            "搜索帖子图片": f"[{','.join(search_note_images)}]" ,
            "点赞数": str(search_note.get("like_count")),
            "收藏数": str(search_note.get("collect_count")),
            "是否相同选题": "是" if search_note.get("same_topic") else "否",
            "关联度得分": str(search_note.get("score")),
            "解释": search_note.get("explain"),
            "脚本": json.dumps(search_note.get("script") , indent=4,ensure_ascii=False) if search_note.get("script") is not  None else None,
            "搜索帖子的脚本总结": json.dumps(result.get("script_summary"),indent=4,ensure_ascii=False) if index ==0  and result.get("script_summary") is not None else None,
            "搜索脚本生成逻辑": search_summary_script.get("创作的脚本").get("图集构建逻辑") if index == 0 else None,
            "搜索脚本生成": search_summary_script.get("创作的脚本").get("图集描述")[index] if index < len(search_summary_script.get("创作的脚本").get("图集描述")) else None,
            "搜索脚本生成图片": utils.get_file_uri(search_summary_script.get("generated_images")[index]) if index < len(search_summary_script.get("generated_images")) else None,

            "人设脚本": json.dumps(renshe_info.get("script_mode"), indent=4,ensure_ascii=False) if index ==0 else None,
            "人设脚本生成逻辑": renshe_script_summary.get("创作的脚本").get("图集构建逻辑") if index == 0 else None,
            "人设脚本生成": renshe_script_summary.get("创作的脚本").get("图集描述")[index] if index < len(
                renshe_script_summary.get("创作的脚本").get("图集描述")) else None,
            "人设脚本生成图片": utils.get_file_uri(renshe_script_summary.get("generated_images")[index] ) if index < len(
                renshe_script_summary.get("generated_images")) else None,

            "匹配帖子id": match_script_summary.get("参考的帖子id") if index == 0 else None,
            "参考理由": match_script_summary.get("参考的理由") if index == 0 else None,
            "配本脚本生成逻辑": match_script_summary.get("创作的脚本").get("图集构建逻辑") if index == 0 else None,
            "匹配脚本生成": match_script_summary.get("创作的脚本").get("图集描述")[index] if index < len(
                match_script_summary.get("创作的脚本").get("图集描述")) else None,
            "匹配脚本生成图片": utils.get_file_uri(match_script_summary.get("generated_images")[index]) if index < len(
                match_script_summary.get("generated_images")) else None,
        }
        data.append(row)

# Convert DataFrame to list with header
df = pd.DataFrame(data)
header = df.columns.tolist()
data_rows = df.values.tolist()
data_with_header = [header] + data_rows

sheet_token = 'Ty2MsTOSih0B2KtSdAAczl5fnJe'
sheet_id = 'ufrDTM'

write_data_to_sheet(data_with_header, sheet_token=sheet_token,
                    sheetid=sheet_id, )
