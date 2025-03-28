import os

import image_article_comprehension.xhs.keyword_search as keyword_search
import json
import image_article_comprehension.agent.xuanti_flow_prompt as prompt
import image_article_comprehension.utils as utils
import concurrent.futures
import traceback


def generate_xuanti():
    xuanti_input_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/agent/result/input/xuanti/给猫咪cosplay哪吒.json"
    return json.load(open(xuanti_input_path))


def search(keyword):
    return keyword_search.key_word_search(keyword)


def search_analyse_filter(renshe_info, xuanti_result, search_result_dir_path, work_flow_base_dir):
    search_analyse_dir = os.path.join(work_flow_base_dir, "search_analyse")
    os.makedirs(search_analyse_dir, exist_ok=True)

    search_note_list = [json.load(open(os.path.join(search_result_dir_path, i), "r")) for i in
                        os.listdir(search_result_dir_path) if i.endswith(".json")]

    def process_search_note(search_note, renshe_info, xuanti_result, search_analyse_dir):
        try:
            analyse_result_save_path = os.path.join(search_analyse_dir, f"{search_note.get('channel_content_id')}.json")
            if os.path.exists(analyse_result_save_path):
                return

            ans = prompt.search_analyse_filter(renshe_info, xuanti_result, search_note)
            r = json.loads(ans)
            analyse_result = {
                "note_info": search_note,
                "search_analyse_filter": r,
            }
            utils.save(analyse_result, analyse_result_save_path)
        except Exception as e:
            print(f"process_search_note error {search_note.get('channel_content_id')} {str(e)}")
            traceback.print_exc()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_search_note, search_note, renshe_info, xuanti_result, search_analyse_dir) for
                   search_note in search_note_list]
        concurrent.futures.wait(futures)


if __name__ == "__main__":
    renshe_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/aigc_data/renshe_0305/account_李尾鱼_615657520000000002026e7c.json"
    renshe_info = json.load(open(renshe_path, "r"))

    xuanti_result = generate_xuanti()

    work_flow_base_dir = os.path.join(
        "/Users/nieqi/Documents/workspace/python/image_article_comprehension/agent/result/workflow",
        xuanti_result.get("选题结果").get("最终的选题"))
    os.makedirs(work_flow_base_dir, exist_ok=True)

    search_result_dir_path = search(xuanti_result.get("选题结果").get("最终的选题"))

    search_analyse_filter(renshe_info, xuanti_result, search_result_dir_path, work_flow_base_dir)
