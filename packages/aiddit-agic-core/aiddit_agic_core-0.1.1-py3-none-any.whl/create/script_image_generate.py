import os
import json
from image_article_comprehension.tools.whish_generate_image import text_to_image
from image_article_comprehension.model.gemini_model_chat import translate_to_english, translate_to_mj_prompt
from image_article_comprehension.tools.midjourney_generate_image import generate_midjourney_image
from image_article_comprehension.model.chat import gemini
import traceback
from tqdm import tqdm
import image_article_comprehension.utils as utils


def image_generate(xuanti_result_dir):
    for i in tqdm(os.listdir(xuanti_result_dir)):
        print(f"process image generate {i}")
        r = json.load(open(os.path.join(xuanti_result_dir, i), 'r'))

        image = r.get("generated_script", {}).get("图片")
        cover = image.get("封面图")
        if cover.get("mid_journey") is None:
            cover["mid_journey"] = generate_midjourney_image_by_prompt(cover.get("用于图片生成的prompt"))
            utils.save(r, os.path.join(xuanti_result_dir, i))
        if cover.get("whisk_images") is None:
            cover["whisk_images"] = generate_whisk_image_by_prompt(cover.get("用于图片生成的prompt"))
            utils.save(r, os.path.join(xuanti_result_dir, i))

        for img in image.get("图集"):
            if img.get("mid_journey") is None:
                img["mid_journey"] = generate_midjourney_image_by_prompt(img.get("用于图片生成的prompt"))
                utils.save(r, os.path.join(xuanti_result_dir, i))
            if img.get("whisk_images") is None:
                img["whisk_images"] = generate_whisk_image_by_prompt(img.get("用于图片生成的prompt"))
                utils.save(r, os.path.join(xuanti_result_dir, i))


def generate_midjourney_image_by_prompt(prompt):
    try:
        images = generate_midjourney_image(prompt)
        print(f"generate_midjourney_image_by_prompt {prompt} {images}")
        return images
    except Exception as e:
        traceback.print_exc()
        if "banned_prompt_detected" in str(e):
            return ['banned_prompt_detected']
        return str(e)


def generate_whisk_image_by_prompt(prompt):
    try:
        images = text_to_image(prompt)
        result = json.loads(images).get("data")
        print(f"generate_whisk_image_by_prompt {prompt} {result}")
        return result
    except Exception as e:
        traceback.print_exc()
        return str(e)


if __name__ == "__main__":
    xuanti_result_dir = "/image_article_comprehension/create/result/script/20250110_摸鱼阿希_0125"
    image_generate(xuanti_result_dir)

    pass
