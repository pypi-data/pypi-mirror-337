import json
import os
import image_article_comprehension.aiddit.xhs.keyword_search as keyword_search
import image_article_comprehension.aiddit.model.google_genai as google_genai
from image_article_comprehension.aiddit.model import GenaiConversationMessage, GenaiMessagePart, MessageType
import image_article_comprehension.aiddit.utils as utils
from image_article_comprehension.aiddit.create.prompts.create_xuanti_search_prompt import (
    NOTE_PROVIDER_PROMPT,
    SAME_TOPIC_FIND_PROMPT,
    RENSHE_SCRIPT_MODE_AND_SEARCH_NOTE_SCRIPT_GENERATE_PROMPT,
    FIND_BEST_SCRIPT_NOTE_FROM_HISTORY_NOTE_PROMPT,
    NOTE_PROMPT,
    HISTORY_NOTE_AND_SEARCH_GENERATE_PROMPT,
    SCRIPT_ALIGN_MATERIALS_PROMPT
)
import image_article_comprehension.aiddit.comprehension.script0221.script_compehension as script_comprehension
import image_article_comprehension.aiddit.comprehension.script0221.script_prompt as script_prompt
import image_article_comprehension.aiddit.create.script_pipeline as script_pipeline


def _search_estimate(process_result, xuanti_result, renshe_info):
    result = {}

    final_xuanti = xuanti_result.get("最终的选题")

    keyword = final_xuanti
    keyword_search_result_dir = keyword_search.key_word_search(keyword)

    search_result_list = [json.load(open(os.path.join(keyword_search_result_dir, i), "r")) for i in
                          os.listdir(keyword_search_result_dir) if i.endswith(".json")]
    search_result_map = {note["channel_content_id"]: note for note in search_result_list}
    print(f"search {keyword} success, result count {len(search_result_list)}")

    ask_result = _ask_gemini(search_result_list, final_xuanti, renshe_info)

    ask_note_result_list = ask_result if type(ask_result) is list else ask_result.get("判断结果", [])
    print(f"_search_estimate input {len(search_result_list)} 个帖子， 模型判断了 {len(ask_note_result_list)} 个帖子")

    has_same_topic = any(note.get("same_topic") is True for note in ask_note_result_list)

    for i in ask_note_result_list:
        note = search_result_map.get(i.get("note_id"))
        if note is not None:
            note["same_topic"] = i.get("same_topic")
            note["score"] = i.get("score")
            note["explain"] = i.get("explain")

    result["搜索关键词"] = keyword
    result["是否有相同选题"] = has_same_topic
    result["搜索结果"] = search_result_map
    result["搜索是否完成"] = True

    # result["质量是否通过"] = _quality_estimate([note for note in search_result_list if note.get("same_topic") is True])
    result["质量是否通过"] = has_same_topic

    process_result.update(result)
    utils.save(process_result, process_result["save_path"])


def _same_topic_note_script_comprehension(process_result):
    """理解单帖脚本"""
    same_topic_notes = [note for note in process_result.get("搜索结果").values() if
                        note.get("same_topic") is True and note.get("script") is None]
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(script_comprehension.note_script, note) for note in same_topic_notes]
        for future, note in zip(concurrent.futures.as_completed(futures), same_topic_notes):
            note["script"] = future.result()

    utils.save(process_result, process_result["save_path"])


def _build_note_prompt(note_list, each_note_image_count=100):
    history_messages = []
    for index, note in enumerate(note_list):
        contents = []
        note_provider_prompt = NOTE_PROVIDER_PROMPT.format(index=index + 1,
                                                           channel_content_id=note.get("channel_content_id"),
                                                           title=note.get("title"),
                                                           body_text=note.get("body_text"))
        text_message = GenaiMessagePart(MessageType.TEXT, note_provider_prompt)
        contents.append(text_message)
        for image in utils.remove_duplicates(note.get("images"))[:each_note_image_count]:
            image_message = GenaiMessagePart(MessageType.URL_IMAGE, utils.oss_resize_image(image))
            contents.append(image_message)

        message = GenaiConversationMessage("user", contents)
        history_messages.append(message)

    return history_messages


def _find_material_image(note_list, note_id, image_index):
    note_map = {note.get("channel_content_id"): note for note in note_list}

    if image_index is None:
        return None

    target_note = note_map.get(note_id)
    if target_note is None:
        return None

    images = utils.remove_duplicates(target_note.get("images"))
    image_index_int = image_index if (type(image_index) is int) else int(image_index)
    real_index = image_index_int - 1
    if real_index in range(0, len(images)):
        return images[real_index]

    return None


def _quality_estimate(same_topic_notes: list):
    """质量评估"""
    quality_pass = False
    for note in same_topic_notes:
        if note.get("like_count") > 100 or note.get("collect_count") > 100:
            quality_pass = True
            break

    return quality_pass


def _ask_gemini(search_result_list, final_xuanti: str, renshe_info):
    """从搜索的结果中找同题的帖子"""
    history_messages = _build_note_prompt(search_result_list, each_note_image_count=3)

    ask_prompt = SAME_TOPIC_FIND_PROMPT.format(note_count=len(search_result_list), final_xuanti=final_xuanti,
                                               create_features=json.dumps({
                                                   "创作灵魂": renshe_info.get("renshe_xuanti_unique").get("创作灵魂"),
                                                   "内容品类": renshe_info.get("renshe_xuanti_unique").get("内容品类"),
                                                   "人设特点": renshe_info.get("renshe_xuanti_unique").get("人设必要信息"),
                                               }, indent=4, ensure_ascii=False))
    ask_message = GenaiConversationMessage("user", [GenaiMessagePart(MessageType.TEXT, ask_prompt)])
    gemini_result = google_genai.google_genai_output_images_and_text(ask_message, model=google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325,
                                                                     history_messages=history_messages,
                                                                     response_mime_type="application/json")
    response_content = gemini_result.content[0].value
    print(response_content)
    return json.loads(response_content)


def _process(xuanti_result, renshe_info, renshe_path):
    xuanti_creation = xuanti_result.get("xuanti_creation")
    final_xuanti = xuanti_creation.get("最终的选题")
    final_xuanti_description = xuanti_creation.get("选题的详细描述信息")
    log_file_name = final_xuanti + ".json"
    save_path = os.path.join(log_file_dir, log_file_name)

    process_result = json.load(open(save_path, "r")) if os.path.exists(save_path) else {
        "xuanti_creation": xuanti_creation,
        "reference_note": xuanti_result.get("reference_note"),
        "renshe_path": renshe_path,
        "save_path": save_path
    }

    # 选题关键词搜索
    if process_result.get("搜索是否完成", False) is False:
        _search_estimate(process_result, xuanti_creation, renshe_info)

    # 参考历史帖子的脚本 生成新脚本
    _generate_script_by_history_note(process_result, renshe_info, final_xuanti)

    #
    # if process_result.get("是否有相同选题", False) is False:
    #     print(f"没有相同选题，跳过")
    #     return
    #
    # # 搜索结果帖子脚本理解
    # _same_topic_note_script_comprehension(process_result)
    #
    # _generate_script_by_search_note_id(process_result, renshe_info, final_xuanti, final_xuanti_description)


def find_best_script_note_from_history_note(final_xuanti, renshe_info):
    comprehension_note_dir_path = renshe_info.get("comprehension_note_path")
    history_note_list = [json.load(open(os.path.join(comprehension_note_dir_path, i), "r")).get("note_info") for i in
                         os.listdir(comprehension_note_dir_path) if i.endswith(".json")]

    history_messages = _build_note_prompt(history_note_list)
    find_best_script_note_from_history_note_prompt = FIND_BEST_SCRIPT_NOTE_FROM_HISTORY_NOTE_PROMPT.format(
        final_xuanti=final_xuanti, note_count=len(history_note_list))
    gemini_result = google_genai.google_genai_output_images_and_text(
        GenaiConversationMessage.one("user", find_best_script_note_from_history_note_prompt), model="gemini-2.0-flash",
        history_messages=history_messages,
        response_mime_type="application/json")
    response_content = gemini_result.content[0].value
    print(response_content)

    note_ans = json.loads(response_content)
    history_reference_note_list = [i.get("帖子id","") for i in note_ans.get("参考帖子", [])]
    find_notes = []
    for note in history_note_list:
        if note.get("channel_content_id") in history_reference_note_list:
            find_notes.append(note)

    return find_notes


def _generate_script_by_history_note(process_result, renshe_info, final_xuanti):
    # 搜索帖子补充材料
    same_topic_notes = [note for note in process_result.get("搜索结果").values() if note.get("same_topic") is True]
    # same_topic_notes 同题排序
    same_topic_notes = sorted(same_topic_notes, key=lambda x: x.get("score"), reverse=True)

    #  gemini-2.0-flash
    model = google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325

    for same_topic_note in same_topic_notes[:1]:
        generated_key = f"script_generate_result_{same_topic_note.get('channel_content_id')}"
        if process_result.get(generated_key) is not None:
            generate_script_result = process_result.get(generated_key)
        else :
            generate_script_result = {
                "reference_note": same_topic_note
            }

        if generate_script_result.get("history_note") is None:
            # 参考历史帖子中的 脚本 & 风格
            history_notes = find_best_script_note_from_history_note(final_xuanti, renshe_info)
            generate_script_result["history_note"] = history_notes
            if len(history_notes) is None:
                print("没有找到历史帖子")
                continue
        else:
            history_notes = generate_script_result.get("history_note")

        history_message = []

        for index , h_note in enumerate(history_notes):
            # 历史参考帖子
            h_note_images = utils.remove_duplicates(h_note.get("images"))
            history_note_prompt = NOTE_PROMPT.format(note_description=f"【历史创作帖子{index+1}】", channel_content_id= h_note.get("channel_content_id") ,title=h_note.get("title"), body_text=h_note.get("body_text"), image_count=len(h_note_images))
            history_note_conversation_message = google_genai.GenaiConversationMessage.text_and_images(history_note_prompt, h_note_images)
            history_message.append(history_note_conversation_message)

        # 搜索同题帖子
        same_topic_note_prompt = NOTE_PROMPT.format(note_description="【参考的同选题帖子】",channel_content_id= same_topic_note.get("channel_content_id"), title=same_topic_note.get("title"), body_text=same_topic_note.get("body_text"), image_count=len(same_topic_note.get("images")))
        same_topic_note_conversation_message = google_genai.GenaiConversationMessage.text_and_images(same_topic_note_prompt, utils.remove_duplicates(same_topic_note.get("images")))
        history_message.append(same_topic_note_conversation_message)

        history_note_and_search_generate_prompt = HISTORY_NOTE_AND_SEARCH_GENERATE_PROMPT.format(final_xuanti=final_xuanti)

        if generate_script_result.get("script") is  None:
            # 生成脚本
            script_ans_conversation_message = google_genai.google_genai_output_images_and_text(
                GenaiConversationMessage.one("user", history_note_and_search_generate_prompt),
                model=model,
                history_messages=history_message,
                response_mime_type="application/json")
            history_message.append(script_ans_conversation_message)
            script_ans_content = script_ans_conversation_message.content[0].value
            print(script_ans_content)
            script_ans = json.loads(script_ans_content)

            generate_script_result["script"] = script_ans
        else :
            script_ans = generate_script_result.get("script")
            history_message.append(google_genai.GenaiConversationMessage.one("model", json.dumps(script_ans, ensure_ascii=False, indent=4)))

        # 材料构建
        if generate_script_result.get("script_with_materials") is None:
            script_align_materials_prompt_message = google_genai.google_genai_output_images_and_text(
                GenaiConversationMessage.one("user", SCRIPT_ALIGN_MATERIALS_PROMPT),
                model=model,
                history_messages=history_message,
                response_mime_type="application/json")
            script_align_materials_content = script_align_materials_prompt_message.content[0].value
            print(script_align_materials_content)
            script_with_materials = json.loads(script_align_materials_content)
            for materials in script_with_materials.get("带材料的脚本").get("材料", []):
                target_notes = history_notes + [same_topic_note]
                image = _find_material_image(target_notes, materials.get("note_id"), materials.get("image_index"))
                materials["image"] = image

            generate_script_result["script_with_materials"] = script_with_materials

        if generate_script_result.get("generated_images") is None:
            script_image_description_list = script_ans.get("创作的脚本", []).get("图集描述", [])
            """根据脚本描述生成图片"""
            for i in script_image_description_list:
                # 图片生成
                image_generate_conversation= GenaiConversationMessage.one("user", f"参考【历史创作帖子】以及历史生成结果，保持风格的一致性，请根据下述图片描述完成图片生成：\n\n{i}")
                image_generation_conversation_message = google_genai.google_genai_output_images_and_text(
                    image_generate_conversation,
                    model=google_genai.MODEL_GEMINI_2_0_FLASH_EXP_IMAGE_GENERATION,
                    history_messages=history_message)
                history_message.append(image_generate_conversation)
                history_message.append(image_generation_conversation_message)
            generated_images = google_genai.get_generated_images(history_message)
            print(generated_images)
            generate_script_result["generated_images"] = generated_images


        """保存结果"""
        process_result[generated_key] = generate_script_result
        utils.save(process_result, process_result["save_path"])

        print(f"{final_xuanti} 生成脚本完成")


def _generate_script_by_search_note_id(process_result, renshe_info, final_xuanti, final_xuanti_description):
    same_topic_notes = [note for note in process_result.get("搜索结果").values() if note.get("same_topic") is True]
    # same_topic_notes 根据点赞量排序
    same_topic_notes = sorted(same_topic_notes, key=lambda x: x.get("like_count"), reverse=True)

    #  gemini-2.0-flash
    model = google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325

    for note in same_topic_notes[:6]:
        generated_key = f"script_generate_result_{note.get('channel_content_id')}"
        # if process_result.get(generated_key) is not None:
        #     continue

        history_message, ask_script_message = script_prompt.build_note_script_message(note)
        history_message.append(ask_script_message)

        ask_script_response_message = GenaiConversationMessage("model", [
            GenaiMessagePart(MessageType.TEXT, json.dumps(note["script"], ensure_ascii=False, indent=4))])
        history_message.append(ask_script_response_message)

        history_message.append(GenaiConversationMessage.one("user",
                                                            "以上就是我给你的参考帖子，下面你需要帮我一个创作任务。准备好了，请回复ok"))
        history_message.append(GenaiConversationMessage.one("model", "ok"))

        script_mode = renshe_info.get("script_mode")
        script_mode = utils.remove_key_from_dict(script_mode, "来源帖子id")

        script_generate_prompt = RENSHE_SCRIPT_MODE_AND_SEARCH_NOTE_SCRIPT_GENERATE_PROMPT.format(
            final_xuanti=final_xuanti,
            final_xuanti_description=final_xuanti_description,
            script_mode=json.dumps(script_mode, indent=4, ensure_ascii=False),
            renshe_xuanti_unique=json.dumps(renshe_info.get("renshe_xuanti_unique"),
                                            indent=4, ensure_ascii=False))
        script_generate_message = GenaiConversationMessage.one("user", script_generate_prompt)
        script_generate_result = google_genai.google_genai_output_images_and_text(script_generate_message,
                                                                                  model=model,
                                                                                  history_messages=history_message,
                                                                                  temperature=0,
                                                                                  response_mime_type="application/json")

        script_result = json.loads(script_generate_result.content[0].value)
        result = {
            "script": script_result,
            "reference_note": note
        }

        materials = script_result.get("创作的脚本", {}).get("视觉材料", [])
        find_materials_map = {}
        for m in materials:
            image = _find_material_image(same_topic_notes, note.get("channel_content_id"), m.get("image_index"))
            if image is not None:
                m["image"] = image
                if find_materials_map.get(image) is not None:
                    find_materials_map[image].append(m.get("materials_name"))
                else:
                    find_materials_map[image] = [m.get("materials_name")]

        vision_materials: list[script_pipeline.VisionMaterial] = []
        for image, names in find_materials_map.items():
            vision_materials.append(script_pipeline.VisionMaterial.build(names, image))

        result["merged_materials"] = [{"name": "、".join(i.name), "image": i.image} for i in vision_materials]
        generated_images = script_pipeline.generate_image_by_gemini(script_result.get("创作的脚本", {}).get("图集描述"),
                                                                    vision_materials)

        result["generated_images"] = generated_images
        process_result[generated_key] = result
        utils.save(process_result, process_result["save_path"])

        # 不用搜索帖子中的材料生成
        generated_images_without_materials = script_pipeline.generate_image_by_gemini(
            script_result.get("创作的脚本", {}).get("图集描述"), [])
        result["generated_images_without_materials"] = generated_images_without_materials
        utils.save(process_result, process_result["save_path"])
    pass


if __name__ == "__main__":
    # 替换 start account_LING_5687a2645e87e702df7b5304 account_山木木简笔画_649da24b000000002b0081a1
    filter_xuanti_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/xuanti_result_0218/account_摸鱼阿希_617a100c000000001f03f0b9/filter_xuanti.json"
    renshe_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/renshe_0314/account_摸鱼阿希_617a100c000000001f03f0b9.json"
    # 替换 end

    filter_xuanti_result = json.load(open(filter_xuanti_path, "r"))

    result_save_base_dir_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/create/result/xuant_search"
    log_file_dir = os.path.join(result_save_base_dir_path, filter_xuanti_path.split("/")[-2])

    renshe_info_data = json.load(open(renshe_path, "r"))

    for result in filter_xuanti_result:
        #  办公室确诊“摸鱼大师”人格 领导PUA与摸鱼的反差 15分钟搞定家常版蒜蓉西兰花 日落时分城市建筑光影与紫藤花交织
        if result.get("xuanti_creation").get("最终的选题") == "办公室确诊“摸鱼大师”人格":
            _process(result, renshe_info_data, renshe_path)
            break

    pass
