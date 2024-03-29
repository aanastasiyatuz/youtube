from PIL import Image

def crop_img(url):
    pil_img = Image.open(url)
    img_width, img_height = pil_img.size
    if img_width == img_height:
        return
    crop_width, crop_height = min(pil_img.size), min(pil_img.size)
    pil_img.crop(((img_width - crop_width) // 2,
                  (img_height - crop_height) // 2,
                  (img_width + crop_width) // 2,
                  (img_height + crop_height) // 2)).save(url, quality=95)
