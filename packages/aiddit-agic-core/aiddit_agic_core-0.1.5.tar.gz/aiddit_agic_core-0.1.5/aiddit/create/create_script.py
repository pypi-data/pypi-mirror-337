import os
import json
from script_create_prompt import prompt_create_script, prompt_create_script_0214
import image_article_comprehension.aiddit.utils as utils


def batch_create_script():
    xuanti_result_dir = "/image_article_comprehension/aiddit/create/result/image_since_0113/20250109_每天一点心理学"

    output_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/result/script/" + \
                 os.path.basename(xuanti_result_dir).split(".")[0]

    xuan_result_list = [json.load(open(os.path.join(xuanti_result_dir, f), "r")) for f in os.listdir(xuanti_result_dir)
                        if
                        f.endswith('.json')]

    generate(xuan_result_list, output_dir, top_n=100)


def generate(xt_list, output_dir, top_n=1):
    available_xuanti_result = []

    for x in xt_list:
        if x.get("xuanti_creation") is not None:
            for xuanti_creation in x.get("xuanti_creation"):
                if xuanti_creation.get("xuanti_creation", {}).get("能否产生选题") == "是" \
                        and xuanti_creation.get("xuanti_estimate", {}).get("选题符合是否要求") == "是" \
                        and xuanti_creation.get("xuanti_estimate", {}).get("选题描述符合是否要求") == "是":
                    available_xuanti_result.append({
                        "renshe": x.get("renshe"),
                        "xuanti": xuanti_creation
                    })

    # print(json.dumps(available_xuanti_result, ensure_ascii=False, indent=4))
    print(f"available_xuanti_result count: {len(available_xuanti_result)}")

    for xt in available_xuanti_result[:top_n]:
        xuanti_mode_name = xt.get("xuanti").get("xuanti_mode")

        renshe_xuanti_unique = xt.get("renshe").get("renshe_xuanti_unique")
        xuanti_mode = next((
            item for item in xt.get("renshe").get("renshe_xuanti_mode", {}).get("modes", []) \
            if item.get("选题模式") == xuanti_mode_name), None)

        xuanti_result = xt.get("xuanti").get("xuanti_creation")

        def execute_script():
            answer = prompt_create_script(renshe_xuanti_unique, xuanti_mode, xuanti_result)
            print(answer)
            return answer

        if output_dir is None:
            execute_script()
        else:
            xuanti_md5 = utils.md5_str(json.dumps(xuanti_result, ensure_ascii=False))
            output_file_name = os.path.join(output_dir, xuanti_md5 + ".json")

            if os.path.exists(output_file_name):
                print(f" {xuanti_result} , file exists")
                continue

            ans = execute_script()

            output = {
                "xuanti": xt,
                "generated_script": json.loads(ans)
            }

            utils.save(output, os.path.join(output_dir, output_file_name))


if __name__ == '__main__':
    # batch_create_script()

    # xuanti_result_list = [json.load(open(
    #     "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/result/image_since_0113/20250110_摸鱼阿希_claude35/675e726200000000060399a4.json",
    #     "r"))]
    # generate(xuanti_result_list,
    #          "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/result/script/20250110_摸鱼阿希_claude35",
    #          top_n=3)

    # renshe_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/result/20250110_摸鱼阿希_claude35.json"
    # renshe = json.load(open(renshe_path, "r"))
    #
    # script_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/result/renshe_script_0213/20250110_摸鱼阿希_claude35.json"
    # script = json.load(open(script_path, "r"))
    #
    xuanti_result = {
        "能否产生选题": "是",
        "不能产生选题的原因": "",
        "最终的选题": "办公室里假装听懂会议内容的表情变化记录",
        "选题的详细描述信息": "通过连续的表情包记录打工人在会议中从自信到迷茫的状态变化：先是白色狗狗一脸自信地说'慢着，我感觉不对劲'，到杰瑞老鼠举手说'放心交给我吧'，再到一脸迷惑的猫咪戴着汉堡头套，最后变成熊猫用酒瓶靠近耳朵说'没听清，麻烦再说一遍'的过程。整个过程展现打工人在会议中从开始自以为听懂到最后完全跟不上的真实心理变化。",
        "选题的参考来源": "参考内容中展示了多张表情包，包含了动物的各种表情变化，特别是白色狗狗、猫咪等动物表情的夸张化表现",
        "选题依赖的关键信息": {
            "场景设定": "办公室会议现场",
            "表情变化": "从自信到迷茫的连续性表情记录",
            "身份设定": "参会的职场打工人",
            "情节发展": "听不懂会议内容却要假装理解的过程",
            "表现形式": "通过连续的动物表情包展现心理变化"
        }
    }

    renshe_path = "/image_article_comprehension/aiddit/comprehension/renshe/result/result_0221/20250109_每天一点心理学.json"
    renshe = json.load(open(renshe_path, "r"))

    # script_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/result/renshe_script_0213/20250109_脆肚火锅噗噜噗噜.json"
    # script = json.load(open(script_path, "r"))

    # xuanti_result =  {
    #     "能否产生选题": "是",
    #     "不能产生选题的原因": None,
    #     "最终的选题": "从众效应：旅行选择中的心理陷阱",
    #     "选题的详细描述信息": "本选题旨在探讨旅行选择中常见的从众效应。首先，解释从众效应的定义，即个体在群体压力下改变自身行为或信念的现象。其次，结合旅行场景，分析游客如何受到他人推荐、社交媒体热度等因素的影响，盲目选择热门景点或旅行方式，而忽略自身兴趣和需求。最后，提供应对从众效应的实用建议，如独立思考、理性评估、制定个性化旅行计划等，帮助读者避免旅行选择中的心理陷阱，提升旅行体验。",
    #     "选题的参考来源": "参考内容中提到的小红书种草、热门景点推荐等现象，引发了我对从众效应在旅行选择中作用的思考。",
    #     "选题依赖的关键信息": {
    #         "心理学效应": "从众效应",
    #         "生活实例": "旅行选择、热门景点推荐",
    #         "实用建议": "独立思考、理性评估、制定个性化旅行计划"
    #     }
    # }

    ans = prompt_create_script_0214(renshe.get("renshe_xuanti_unique"), renshe.get("script_mode"), xuanti_result)
    print(ans)
    pass
