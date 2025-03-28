from dataclasses import dataclass
from io import BytesIO

import cv2
import tyro
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from skimage.metrics import structural_similarity as ssim
from tqdm import tqdm


@dataclass
class Args:
    """Extract frames from a video and summarize them as a PDF file."""

    input: str  # input video path
    output: str = "tmp.pdf"  # output path
    jump: int = 2  # jump seconds


def diff_frame(frame1, frame2):
    f1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    f2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    return ssim(f1, f2, data_range=255)


def save_frames(frames: list[cv2.typing.MatLike], output_path: str) -> None:
    c = canvas.Canvas(output_path)
    for f in frames:
        img_rgb = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        img_width, img_height = pil_img.size
        c.setPageSize((img_width, img_height))
        # wrap BytesIO using ImageReader
        with BytesIO() as img_buffer:
            pil_img.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            c.drawImage(
                ImageReader(img_buffer), 0, 0, width=img_width, height=img_height
            )
        c.showPage()
    c.save()


def video2frames(video_path: str, jump_seconds: int = 5) -> list[cv2.typing.MatLike]:
    """Extract frames from a video and save them as images. 2 second one frame"""
    # firstly, get video fps
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # secondly, collect frames
    frames = []
    t = 0
    while cap.isOpened():
        print(f"Extracting frame at {t} seconds")
        ret, frame = cap.read()
        if ret is False:
            break
        else:
            frames.append(frame)
            t += jump_seconds
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)

    # thirdly, filter frames
    wanted_frames = []
    for i, frame in enumerate(tqdm(frames)):
        if i == 0:
            preframe = frame
        diff = diff_frame(frame, preframe)
        if diff < 0.95:
            wanted_frames.append(frame)
        preframe = frame
    return wanted_frames


def main():
    args = tyro.cli(Args)
    frames = video2frames(args.input, args.jump)
    save_frames(frames, args.output)


if __name__ == "__main__":
    main()
