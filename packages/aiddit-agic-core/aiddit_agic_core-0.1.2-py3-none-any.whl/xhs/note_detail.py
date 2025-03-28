import os
import requests
import json
import traceback
from tqdm import tqdm
import time
import image_article_comprehension.utils as utils
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode


def get_note_detail(content_link):
    print(f"get note detail {content_link}")

    url = "http://crawler.aiddit.com/crawler/xiao_hong_shu/detail"

    payload = json.dumps({
        "content_link": content_link,
        "is_upload": True
    })
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.uU_4v9ukxon47prl6EEV2U5YqSIoJr8r6wS1SBnOJiA',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        note_detail_response = json.loads(response.text)
        if note_detail_response.get("code") != 0:
            raise Exception(
                f"Failed to get note detail {content_link} , code = {note_detail_response.get('code')} , {response.text}")

        return note_detail_response.get("data").get("data")
    else:
        raise Exception(f"Failed to get note detail {content_link} , http status code = {response.status_code}")


def batch_get_note_detail(note_dir):
    note_list = os.listdir(note_dir)

    success_cnt = 0
    cached_cnt = 0
    for note_filename in tqdm(note_list):
        with open(os.path.join(note_dir, note_filename), 'r') as f:
            note = json.load(f)
            if not note.get("images"):
                while True:
                    try:
                        note_detail = get_note_detail(note.get("link"))
                        print(f"get note detail success {note.get('link')}")

                        note["comment_count"] = note_detail.get("comment_count")

                        note["images"] = [i.get("cdn_url", i.get("image_url")) for i in
                                          note_detail.get("image_url_list", [])]
                        note["like_count"] = note_detail.get("like_count")
                        note["body_text"] = note_detail.get("body_text")
                        note["title"] = note_detail.get("title")
                        note["collect_count"] = note_detail.get("collect_count")
                        note["content_type"] = note_detail.get("content_type")
                        note["link"] = note_detail.get("content_link")

                        with open(os.path.join(note_dir, note_filename), 'w') as wf:
                            json.dump(note, wf, ensure_ascii=False, indent=4)
                            success_cnt += 1
                        break
                    except Exception as e:
                        error = traceback.format_exc()
                        print(error)
                        print(f"Failed to get note detail , {e}")
                        if "访问频次异常" in error:
                            print(f"访问频次异常 sleep 3s")
                            time.sleep(3)
                        else:
                            break
            else:
                cached_cnt += 1
                print(f"note {note.get('link')} already has detail data")

    print(f"cached count = {cached_cnt} , total count = {len(note_list)} success count = {success_cnt}")
    return cached_cnt, len(note_list), success_cnt


def single_detail(link, output_dir):
    note_id = link.split("?")[0].split("/")[-1]
    if os.path.exists(os.path.join(output_dir, f"{note_id}.json")):
        print(f"{note_id}.json already exists , skip , {link}")
        return

    note_detail = get_note_detail(link)
    print(note_detail)
    note = {}

    note["comment_count"] = note_detail.get("comment_count")
    note["images"] = [i.get("cdn_url", i.get("image_url")) for i in
                      note_detail.get("image_url_list", [])]
    note["like_count"] = note_detail.get("like_count")
    note["body_text"] = note_detail.get("body_text")
    note["title"] = note_detail.get("title")
    note["collect_count"] = note_detail.get("collect_count")
    note["link"] = note_detail.get("content_link")
    note["channel_content_id"] = note_detail.get("channel_content_id")
    note["content_type"] = note_detail.get("content_type")

    with open(os.path.join(output_dir, f"{note_detail.get('channel_content_id')}.json"), 'w') as wf:
        json.dump(note, wf, ensure_ascii=False, indent=4)


def refresh_detail_images():
    refresh_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note_keypoint/image_merge_0102_1230"
    total_count = len(os.listdir(refresh_dir))

    files = os.listdir(refresh_dir)
    files = ["67752b32000000000900c5cc.json"]

    success_cnt = 0
    for i in tqdm(files):
        try:
            note = json.load(open(os.path.join(refresh_dir, i), 'r'))

            if any("res.cybertogether.net" in images_url for images_url in note.get("note_info").get("images")):
                print(f"{json.dumps(note.get('note_info').get('images'))} has res.cybertogether.net , skip")
                continue

            note_detail = get_note_detail(note.get("note_info").get("link"))

            note["note_info"]["images"] = [i.get("cdn_url", i.get("image_url")) for i in
                                           note_detail.get("image_url_list", [])]

            utils.save(note, os.path.join(refresh_dir, i))
            success_cnt += 1
        except Exception as e:
            print("Failed to refresh detail images", i, str(e))

    print(f"success count = {success_cnt} / {total_count}")
    pass


def refresh_crawler_detail_images():
    refresh_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/note_data/account_猫小司_6430bea30000000012011f2d"
    total_count = len(os.listdir(refresh_dir))

    files = os.listdir(refresh_dir)

    success_cnt = 0
    for i in tqdm(files):
        try:
            note = json.load(open(os.path.join(refresh_dir, i), 'r'))

            if any("res.cybertogether.net" in images_url for images_url in note.get("images")):
                print(f"{json.dumps(note.get('images'))} has res.cybertogether.net , skip")
                continue

            note_detail = get_note_detail(note.get("link").split("?")[0])

            print(f"{json.dumps(note_detail, ensure_ascii=False, indent=4)}")

            note["images"] = [i.get("cdn_url", i.get("image_url")) for i in
                              note_detail.get("image_url_list", [])]

            utils.save(note, os.path.join(refresh_dir, i))
            success_cnt += 1
        except Exception as e:
            print("Failed to refresh detail images", i, str(e))

    print(f"success count = {success_cnt} / {total_count}")
    pass


def simplify_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # 保留需要的参数
    simplified_query_params = {
        'xsec_token': query_params.get('xsec_token', [''])[0]
    }

    # 构建新的URL
    simplified_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        urlencode(simplified_query_params),
        parsed_url.fragment
    ))

    return simplified_url


if __name__ == "__main__":
    # refresh_detail_images()

    # refresh_crawler_detail_images()

    # batch_get_note_detail(
    #     '/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/note_data/account_20250110_春哥边走边画_62ad8bd7000000001b0267af')

    single_detail("https://www.xiaohongshu.com/explore/67b1af84000000001801a8d2",
                  "/Users/nieqi/Documents/workspace/python/image_article_comprehension/xhs/result/")


    # links = [
    #     'https://www.xiaohongshu.com/explore/676f75e30000000013001a59?xsec_token=ABETZg_LjTTHOHNnDY1nIhcRuD2-Bcsl9G8HJk1SwqBDk=&xsec_source=pc_feed',
    #     'https://www.xiaohongshu.com/explore/67752b32000000000900c5cc?xsec_token=ABRuzPFHmtnzesd35TlOpBSRRzB9pmw2ToMMEMR5T17d8=&xsec_source=pc_feed',
    #     'https://www.xiaohongshu.com/explore/676d6d71000000000b01528e?xsec_token=ABuXC7SAxzq2_Xp2NIIpqJdH00_7vzJDinhXS9ZiIc5HM=&xsec_source=pc_cfeed',
    #     'https://www.xiaohongshu.com/explore/675ee173000000000102801b?xsec_token=ABfODZC9pNE0j18eT6jduEJ37nT9OOA4gcfXpfBBc42pA=&xsec_source=pc_cfeed',
    #     'https://www.xiaohongshu.com/explore/676974d6000000000b0150b3?xsec_token=ABtyAgoJTK0hwuIvgfRz2YaY_83Hsws2LRYWuRJ5_gqTc=&xsec_source=pc_cfeed',
    #     'https://www.xiaohongshu.com/explore/6773d64e0000000013009114?xsec_token=ABmPNQE9IUkDRny609zo28a0WitMxM5zZrysDRg73YYsE=&xsec_source=pc_cfeed',
    #     'https://www.xiaohongshu.com/explore/676bf2b1000000000800c288?xsec_token=ABdSVhgBTvK47Lxde9ZzUwM-SxTyR9WavVk4wN1WmAGEg=&xsec_source=pc_cfeed',
    #     'https://www.xiaohongshu.com/explore/675781f7000000000603e33e?xsec_token=ABFVh_7bl3GW_LKYoqIHqIoUcEPkHF8mgeitPXa4p6Cc8=&xsec_source=pc_cfeed',
    #     'https://www.xiaohongshu.com/explore/676ffe8d000000001300efb3?xsec_token=ABETZg_LjTTHOHNnDY1nIhcV4JQprRtYokwCWf3klcAuM=&xsec_source=pc_cfeed',
    #     'https://www.xiaohongshu.com/explore/675ff5df000000000900e71f?xsec_token=ABAc0ZOx3jaP5RJDKWU8_4Yw4JcenJLQ9RRjWbsXw62zI=&xsec_source=pc_cfeed',
    #     'https://www.xiaohongshu.com/explore/67582b2f00000000070098db?xsec_token=AB-nrfqaH9lik15CKIqun8JZKT0QwCa9R-9_Z_4dv4xM0=&xsec_source=pc_cfeed',
    #     'https://www.xiaohongshu.com/explore/675ce18b00000000020162b0?xsec_token=ABAugq_w5_tNIQKUCmUowOMUSLO8pzQ5KzKnVsbeHrsa8=&xsec_source=pc_cfeed',
    # ]
    #

    # dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/create/reference_note/image_0109"
    #
    # for i in os.listdir(dir):
    #     print(i)
    #     note = json.load(open(os.path.join(dir, i), 'r'))
    #     link = note.get("link")
    #     note["original_link"] = link
    #     note["link"] = simplify_url(link)
    #     utils.save(note, os.path.join(dir, i))



    pass
