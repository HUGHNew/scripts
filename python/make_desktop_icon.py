"""
pip install typer[all] Pillow
"""

import typer
from PIL import Image

def fit_shorter_edge(image_file:str):
    image = Image.open(image_file)
    w, h = image.size
    w_t, h_t = 0, 0
    if w > h:
        w_t = (w-h)//2
        w = h
    else:
        h_t = (h-w)//2
        h = w
    return image.convert("RGBA").crop([w_t, h_t, w_t+w, h_t+h])

def trans_color_round(image_rf:str|Image.Image, mask_color:tuple[int, int, int], round:int=3):
    if isinstance(image_rf, str):
        image = Image.open(image_rf)
    elif isinstance(image_rf, Image.Image):
        image = image_rf
    else:
        raise RuntimeError(f"{image_rf} should be str or Image")
    def mask_color_with_range(color:tuple[int, int, int, int]):
        if sum(map(lambda x: abs(x[0]-x[1]) , zip(color[:3], mask_color))) < round * 3:
            return (*color[:3], 0)
        return color
    image.putdata([
        mask_color_with_range(point)
        for point in image.getdata()
    ])
    return image

def make_icon(image_ref:str, output:str,
              size:int=96, mask_color:tuple[int,int,int]=(255, 255, 255), color_around:int=3):
    image = fit_shorter_edge(image_ref)
    image = trans_color_round(image, mask_color, color_around)
    image = image.resize((size,size))
    image.save(output)

if __name__ == "__main__":
    typer.run(make_icon)

