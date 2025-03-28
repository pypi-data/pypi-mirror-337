import json
from pymilvus import MilvusClient
from pymilvus import connections, db
from image_article_comprehension.vector_database.openai_embedding import get_embedding

conn = connections.connect(host="192.168.100.20", port=19530)

print(db.list_database())

client = MilvusClient(
    uri="http://192.168.100.20:19530",
    token="root:Milvus"
)


def import_xhs_data():
    data = json.load(
        open("/Users/nieqi/Documents/workspace/python/image_article_comprehension/vector_database/data.json", 'r'))
    for index, key in enumerate(data.keys()):
        if index == 0:
            continue
        print(key)
        note_data = data.get(key)
        list = note_data.get("素材列表")
        for item in list:
            child_value(None, item, 0, key)


def child_value(parent, child, level=0, note_id=""):
    print("\t" * level + child.get("素材名称"))
    child_list = child.get("子素材列表")
    # insert_vector(child, note_id)
    if child_list is not None and len(child_list) > 0:
        for c in child_list:
            child_value(child, c, level + 1, note_id)


def insert_vector(child, note_id):
    res = client.insert(
        collection_name="materials",
        data={
            "name_vector": get_embedding(child.get("素材名称")),
            "description_vector": get_embedding(child.get("素材描述")),
            "modal": child.get("素材模态"),
            "type": child.get("素材类型"),
            "name": child.get("素材名称"),
            "description": child.get("素材描述"),
            "usage": child.get("素材作用"),
            "note_id": note_id
        }
    )

    print(res)

    pass


def query(name):
    res = client.search(
        collection_name="materials",  # Collection name
        anns_field="name_vector",  # Field name of the vector for search
        data=[get_embedding(name)],  # Replace with your query vector
        output_fields=["id", "modal", "type", "name", "description", "usage", "note_id"],
        limit=15,  # Max. number of search results to return
    )

    return res[0]


if __name__ == "__main__":
    import_xhs_data()
