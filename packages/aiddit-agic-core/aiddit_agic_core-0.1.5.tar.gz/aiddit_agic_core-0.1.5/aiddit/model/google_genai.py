from google import genai as google_genai
from google.genai import types
import image_article_comprehension.aiddit.model.gemini_upload_file as gemini_upload_file
import image_article_comprehension.aiddit.utils as utils
from datetime import datetime, timezone
from tenacity import retry, stop_after_attempt, wait_fixed
import os
import json
from tqdm import tqdm
import concurrent.futures
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("google_genai_api_key")
cache_dir = os.getenv("google_genai_upload_file_cache_dir")
generate_image_save_dir_path = os.getenv("google_genai_generated_image_save_dir")


google_genai_client = google_genai.Client(api_key=api_key)


# google 升级的SDK https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn

class MaxTokenException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"MaxTokenException: {self.message}"


MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GEMINI_2_5_PRO_EXPT_0325 = "gemini-2.5-pro-exp-03-25"
MODEL_GEMINI_2_0_FLASH_EXP_IMAGE_GENERATION = "gemini-2.0-flash-exp-image-generation"


def google_genai(prompt, model_name=MODEL_GEMINI_2_0_FLASH, response_mime_type="application/json", images=None,
                 temperature=0, max_output_tokens=8192):
    contents = []
    if images is not None and len(images) > 0:
        seen = set()
        unique_image_urls = [url for url in images if not (url in seen or seen.add(url))]
        for image in tqdm(unique_image_urls):
            path = gemini_upload_file.handle_file_path(image)
            try:
                # image_content = Image.open(path)
                image_content = upload_file(image)
            except Exception as e:
                utils.delete_file(path)
                print(f"Image.open Error {image} , {path} error {str(e)}")
                raise e

            contents.append(image_content)

    contents.append(prompt)
    response = google_genai_client.models.generate_content(
        model=model_name,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type=response_mime_type,
            max_output_tokens=max_output_tokens,
            temperature=temperature
        )
    )

    if response.candidates[0].finish_reason == types.FinishReason.MAX_TOKENS:
        raise MaxTokenException(f"reached max tokens {max_output_tokens}")

    return response.text


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def upload_file(image_url):
    image_local_path = gemini_upload_file.handle_file_path(image_url)
    return __do_file_upload_and_cache(image_local_path)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def upload_file_from_local(image_local_path):
    return __do_file_upload_and_cache(image_local_path)



def __do_file_upload_and_cache(local_image_path):
    cache_file_path = os.path.join(cache_dir, utils.md5_str(local_image_path) + ".json")

    if os.path.exists(cache_file_path):
        with open(cache_file_path, 'r') as file:
            file_ref_dict = json.load(file)
            file_ref = types.File()
            file_ref.name = file_ref_dict.get("name")
            file_ref.mime_type = file_ref_dict.get("mime_type")
            file_ref.size_bytes = file_ref_dict.get("size_bytes")
            file_ref.create_time = datetime.strptime(file_ref_dict.get("create_time"), '%Y-%m-%dT%H:%M:%S.%fZ').replace(
                tzinfo=timezone.utc)
            file_ref.expiration_time = datetime.strptime(file_ref_dict.get("expiration_time"),
                                                         '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
            file_ref.update_time = file_ref_dict.get("update_time")
            file_ref.sha256_hash = file_ref_dict.get("sha256_hash")
            file_ref.uri = file_ref_dict.get("uri")
            file_ref.state = file_ref_dict.get("state")
            file_ref.source = file_ref_dict.get("source")

            current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
            if current_time < file_ref.expiration_time:
                # print("cache hint")
                return file_ref

    file_ref = google_genai_client.files.upload(file=local_image_path)
    # print(f"real uploading to google {local_image_path}")
    with open(cache_file_path, 'w') as file:
        json.dump(file_ref.to_json_dict(), file)
    return file_ref


def google_genai_conversation(history_messages, prompt, response_mime_type=None):
    history = []
    for message in history_messages:
        # role  Must be either 'user' or  'model'
        part = types.Part.from_text(text=message.get("content", ""))
        # 创建一个 Content 实例
        content = types.Content(parts=[part], role="user" if message.get("role") == "user" else "model", )
        history.append(content)

    chat = google_genai_client.chats.create(model=MODEL_GEMINI_2_0_FLASH, history=history)
    response = chat.send_message(prompt, config=types.GenerateContentConfig(
        max_output_tokens=1000 * 20,
        temperature=0,
        response_mime_type=response_mime_type
    ))

    return response.text


from enum import Enum


class MessageType(Enum):
    TEXT = "text"
    LOCAL_IMAGE = "local_image"
    URL_IMAGE = "url_image"


class GenaiMessagePart:
    def __init__(self, message_type: MessageType, value: str):
        self.message_type = message_type
        self.value = value

    def __str__(self):
        return f"message_type: {self.message_type}, value: {self.value}"

    @staticmethod
    def image(image_url):
        message_type = MessageType.URL_IMAGE if image_url.startswith("http") else MessageType.LOCAL_IMAGE
        return GenaiMessagePart(message_type, image_url)


class GenaiConversationMessage:
    def __init__(self, role, content: list[GenaiMessagePart]):
        self.role = role
        self.content = content

    def __str__(self):
        break_line = "\n"
        return f"role: {self.role}, content: [\n{break_line.join(str(part) for part in self.content)}]"

    @staticmethod
    def one(role, value, message_type=MessageType.TEXT):
        return GenaiConversationMessage(role, [GenaiMessagePart(message_type, value)])

    @staticmethod
    def text_and_images(text, images):
        content = [GenaiMessagePart(MessageType.TEXT, text)]
        if images is not None:
            for image in images:
                content.append(GenaiMessagePart.image(image))
        return GenaiConversationMessage("user", content)


def save_binary_file(file_name, data):
    if os.path.exists(generate_image_save_dir_path) is False:
        os.makedirs(generate_image_save_dir_path)

    save_path = os.path.join(generate_image_save_dir_path, file_name)
    f = open(save_path, "wb")
    f.write(data)
    f.close()
    return save_path


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def _prepare_message_for_request(index, conversation_message):
    parts = []
    for gemini_message_part in conversation_message.content:
        if gemini_message_part.message_type == MessageType.TEXT:
            parts.append(types.Part.from_text(text=gemini_message_part.value))
        elif gemini_message_part.message_type == MessageType.URL_IMAGE:
            f = upload_file(gemini_message_part.value)
            parts.append(types.Part.from_uri(file_uri=f.uri, mime_type=f.mime_type))
        elif gemini_message_part.message_type == MessageType.LOCAL_IMAGE:
            f = upload_file_from_local(gemini_message_part.value)
            parts.append(types.Part.from_uri(file_uri=f.uri, mime_type=f.mime_type))

    if len(parts) == 0:
        raise Exception(f"parts is empty：{str(conversation_message)}")

    return index, types.Content(parts=parts,
                                role=conversation_message.role if conversation_message.role == "user" else "model", )


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def google_genai_output_images_and_text(new_message: GenaiConversationMessage,
                                        model=MODEL_GEMINI_2_0_FLASH_EXP_IMAGE_GENERATION,
                                        history_messages: list[GenaiConversationMessage] | None = None,
                                        response_mime_type="text/plain",
                                        max_output_tokens: int = 8192,
                                        temperature: float = 1,
                                        print_messages: bool = True) -> GenaiConversationMessage:
    global chunk
    if print_messages:
        if history_messages is not None:
            for hm in history_messages:
                print(hm)
        print(new_message)

    prepared_message = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(_prepare_message_for_request, index, message) for index, message in
                   enumerate((history_messages or []) + [new_message])]
        for future in concurrent.futures.as_completed(futures):
            try:
                idx, result = future.result()
                prepared_message.append({
                    "index": idx,
                    "content": result
                })
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"prepare message failed, {str(e)}")

    prepared_message.sort(key=lambda x: x["index"])
    contents = [item["content"] for item in prepared_message]

    response_modalities = ["image", "text"] if model == MODEL_GEMINI_2_0_FLASH_EXP_IMAGE_GENERATION else None

    generate_content_config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=0.95,
        top_k=40,
        max_output_tokens=max_output_tokens,
        response_modalities=response_modalities,
        response_mime_type=response_mime_type,
    )

    response_content: list[GenaiMessagePart] = []

    print("\n-------conversation prepared , waiting response ----------\n")

    text_response_content = ""
    for chunk in google_genai_client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        if chunk.candidates[0].content.parts[0].inline_data:
            file_name = f"{utils.generate_uuid_datetime()}.png"
            image_save_path = save_binary_file(
                file_name, chunk.candidates[0].content.parts[0].inline_data.data
            )
            print(
                "File of mime type"
                f" {chunk.candidates[0].content.parts[0].inline_data.mime_type} saved"
                f"to: {image_save_path}"
            )
            response_content.append(GenaiMessagePart(MessageType.LOCAL_IMAGE, image_save_path))
        else:
            text_response_content += chunk.text
            print(chunk.text)

    if chunk and chunk.candidates and chunk.candidates[0].finish_reason:
        if chunk.candidates[0].finish_reason != types.FinishReason.STOP:
            raise Exception("Unexpected Finish Reason: " + chunk.candidates[0].finish_reason)

    if text_response_content is not None and len(text_response_content) > 0:
        response_content.append(GenaiMessagePart(MessageType.TEXT, text_response_content))

    return GenaiConversationMessage("model", response_content)


def get_generated_images(all_messages):
    generated_images = []

    for msg in all_messages:
        if msg.role == "model":
            for gemini_message_part in msg.content:
                if gemini_message_part.message_type == MessageType.LOCAL_IMAGE:
                    generated_images.append(gemini_message_part.value)

    return generated_images


if __name__ == "__main__":
    # google_genai_conversation()

    #     prompt_list = ["""你将要帮我生成一组图片，下面是图片中的通用信息：
    # {
    # "阿希": "年轻男性，身穿休闲办公服装，发型简单利落的短发，体型中等。表情生动丰富，能展现出从兴奋到生无可恋的多种状态。坐姿自然随意，符合年轻打工人特征。",
    # "办公室工位": "标准的开放式办公工位，配备灰色办公桌和黑色办公椅，桌面上有显示器、键盘、鼠标等基础办公设备。工位四周有矮隔板，背景是其他同事的工位。",
    # "打工人/生活用品": "办公桌面上摆放着工牌、便利贴、水杯、手机、计算器等办公必需品，以及外卖盒、零食包装等生活用品，呈现出真实的办公环境。",
    # "搞怪表情": "夸张的面部表情，包括瞪大眼睛、嘴角上扬的兴奋表情，以及眼神空洞、面无表情的呆滞状态，体现出强烈的情绪反差。",
    # "摸鱼状态": "瘫坐在办公椅上，身体前倾或后仰，双手无力下垂，眼神放空，整个人呈现出精神涣散的状态。"
    # }
    # 如果你听明白了，请回复 好的。""",
    #                    "在标准的开放式办公工位上，年轻男性阿希身穿休闲办公服装，看到手机补贴新闻，兴奋地举起手机，脸上露出夸张的瞪眼笑容，背景是摆满办公用品和生活物品的工位。",
    #                    "年轻男性阿希在开放式办公工位上，打开计算器，认真计算工资，桌面上整齐摆放着工牌、便利贴等办公用品，表情严肃认真",
    #                    "年轻男性阿希在办公工位上，掰着手指头，计算各项支出，嘴里念念有词，眉头紧锁，似乎在为钱发愁",
    #                    "年轻男性阿希在办公工位上，看着计算器上的余额，表情逐渐凝固，眼神空洞呆滞，面部表情夸张地显示出震惊，似乎发现了什么可怕的事情",
    #                    "年轻男性阿希瘫坐在办公工位的椅子上，身体无力下垂，眼神放空，桌面上散落着办公用品和生活物品，整个人呈现出生无可恋的状态"]
    prompt_list = ["解释马太效应，越详细越好"]

    hms = []

    for prompt in prompt_list:
        ml: list[GenaiMessagePart] = []
        ml.append(GenaiMessagePart(MessageType.TEXT, prompt))
        mess = GenaiConversationMessage("user", ml)

        res = google_genai_output_images_and_text(mess, history_messages=hms, max_output_tokens=200)
        hms.append(mess)
        hms.append(res)
        print(res)

    pass
