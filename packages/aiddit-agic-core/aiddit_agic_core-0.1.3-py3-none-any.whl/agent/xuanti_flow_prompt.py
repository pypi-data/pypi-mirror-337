import json

import image_article_comprehension.model.google_genai as google_genai


def search_analyse_filter(renshe_info, xuanti_result, search_note_info):
    prompt = f"""
下面有一个小红书的帖子内容如下：
标题: 
{search_note_info.get("title")}
正文：
{search_note_info.get("body_text")}
还有图片内容。

现在我有一个选题：
{xuanti_result.get("选题结果").get("最终的选题")}

我的创作人设信息如下：
{json.dumps(renshe_info.get("renshe_xuanti_unique"), ensure_ascii=False, indent=4)}

请基于这个帖子帮我完成以下任务：
- 判断这个帖子的选题是否和我的选题一样：'是'、'否'：
- 判断这个帖子的主题/选题是否和我的选题、人设契合，给出一个契合程度的结果：'高'、'中'、'低'：
    - 请结合`创作人设信息`和`选题`来综合判断；
    - 契合程度越高指的是这个帖子越适合作为我的创作参考；
- 给出评分理由
- 如果和选题/人设相关，请给出契合点。
    - 契合的关键信息/亮点指的是能够在我的创作过程中，我能够借鉴或者参考；
    - 输入为关键信息/亮点的文本，格式为JSON，如：{{"契合点1": "契合点1的详细信息", "契合点2": "契合点2的详细信息"}}
    - 这将对我的创作非常有帮助；

要求：
- 选题的关键信息/亮点需要在帖子中有体现；
- 评分和理由需要有逻辑支撑。
- 契合程度越高，请给出充分的理由来证明你给出契合程度的原因。
- 按照以下格式输出为JSON，with keys：
    - 是否相同选题(enum['是'、'否'])
    - 契合程度(enum['高'、'中'、'低'])
    - 契合理由(str)
    - 契合点(dict)
"""

    ans = google_genai.google_genai(prompt, images=search_note_info.get("images"))

    return ans
