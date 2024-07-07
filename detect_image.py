import subprocess
from os.path import exists
from pathlib import Path
def test():
  subprocess.run("python DOTA_devkit/SplitOnlyImage.py", shell=True)
  folder_dir = 'test/op'
  images = Path(folder_dir).glob('*.png')
  for image in images:
    image=str(image)
    result = subprocess.run("python detect.py  --name exp_im --weights runs/train/exp14/weights/best.pt --source {im} --imgsz 1024 --conf-thres 0.2 --device 0".format(im=image), shell=True , capture_output=True, text=True)
    print(result.stdout)
    

test()

