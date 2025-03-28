import dashvector
from dashvector import Doc
from openai import OpenAI
import json
from tqdm import tqdm
import time
import traceback
import os

openai_client = OpenAI()
dashvector_client = dashvector.Client(
    api_key='sk-cYd0GOY48TsL3pqU2rWuD53waLcFGD1748AB7B13A11EFAFF56E6DD62AB664',
    endpoint='vrs-cn-jmp4139hk0002u.image_article_comprehension.cn-hangzhou.aliyuncs.com'
)

collection = dashvector_client.get(name='xuanti1205')

# 修改变量start
xuanti_result_dir = "xuanti_result_v3"
# 修改变量end


def get_embedding(text):
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=text,
        encoding_format="float"
    )
    return response.data[0].embedding


def insert_doc(vector, fields):
    ret = collection.insert(
        Doc(
            vector=vector,
            fields=fields
        )
    )

    return ret


def query_doc(vector, topk=5):
    ret = collection.query(
        vector=vector,
        topk=topk,
        # filter="type = '选题描述'",
        # output_fields=["doc_value", "doc_type"]
    )
    return ret


def insert_doc_xt(doc_value, doc_type, note_info, comprehension_version, xt_result):
    fields = {
        "doc_type": doc_type,
        "doc_value": doc_value,
        "note_id": note_info["channel_content_id"],
        "like_cnt": note_info["like_count"],
        "collect_cnt": note_info["collect_count"],
        "comprehension_version": comprehension_version,
        "xt_result": json.dumps(xt_result, ensure_ascii=False),
        "note_info": json.dumps(note_info, ensure_ascii=False),
        "create_time": int(time.time()),
        "update_time": int(time.time())
    }
    return insert_doc(get_embedding(doc_value), fields), fields


def batch_insert_dashvector():
    path = f'../comprehension/{xuanti_result_dir}'
    files = os.listdir(path)
    insert_cnt = 0
    target_cnt = 0
    for file in tqdm(files):
        try:
            with open(os.path.join(path, file), 'r') as f:
                data = json.load(f)

                xt_result = data["xuanti_result"]
                note_info = data["note_info"]

                doc_type = ["选题描述", "选题思路"]

                if data.get("insert1205") is True:
                    print(f"note_id = {note_info['channel_content_id']} vector already inserted")
                    continue

                vector_data = []

                for dt in doc_type:
                    ret = collection.query(
                        topk=1,
                        filter=f"doc_type = '{dt}' and note_id = '{note_info['channel_content_id']}' and comprehension_version = '{data['comprehension_version']}'",
                        output_fields=["doc_value", "doc_type"]
                    )

                    if ret.response.output:
                        print(f"doc_type = {dt} note_id = {note_info['channel_content_id']} vector already exists")
                        continue

                    target_cnt += 1
                    insert_ret, fields = insert_doc_xt(xt_result[dt], dt, note_info, data["comprehension_version"],
                                                       xt_result)

                    if insert_ret.code == 0:
                        insert_cnt += 1
                        vector_data.append({
                            "id": insert_ret.output[0].id,
                            "fields": fields
                        })
                        print(f"insert {file} success total insert cnt = {insert_cnt}/{target_cnt}")
                    else:
                        print(
                            f"insert {file} fail ,  {insert_cnt}/{target_cnt} ,  {dt} response code = {ret.code} , message = {ret.message} ")

                data["insert1205"] = True
                data["vector_data"] = vector_data

                with open(os.path.join(path, file), 'w') as wf:
                    json.dump(data, wf, ensure_ascii=False, indent=4)
        except Exception as e:
            error = traceback.format_exc()
            print(error)
            print(f"{file} error {str(e)}")


batch_insert_dashvector()

# r = query_doc(get_embedding("创意雨衣"), topk=10)
# r.response.output.sort(key=lambda x: x.score, reverse=False)
# for r in r.response.output:
#     print(r)
