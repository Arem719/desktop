import sys, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/user/iremcnar/eyetutorial')
import eye as E
CW, CH = 16, 26
ROWS = 30
E.init(CW, CH, ROWS)
print(E.COLS, E.ROWS, E.W, E.H)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 22)
tiles = np.zeros((len(E.RAMP), CH, CW), np.float32)
for i, c in enumerate(E.RAMP):
    im = Image.new('L', (CW, CH), 0); d = ImageDraw.Draw(im)
    d.text((CW/2, CH/2), c, font=font, fill=255, anchor='mm')
    tiles[i] = np.asarray(im, np.float32)/255
dur = float(sys.argv[2]); fps = 30; out = sys.argv[1]
import subprocess
W, H = E.COLS*CW, E.ROWS*CH
p = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-vf','scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x010203',
    '-c:v','libx264','-pix_fmt','yuv420p','-crf','18', out], stdin=subprocess.PIPE)
bg = np.array([1,2,3], np.float32)
for f in range(int(dur*fps)):
    t = f/fps
    idx, q = E.render_cells(t, 1/fps)
    col = q.astype(np.float32)/(E.QL-1)*255
    g = tiles[idx]                      # R,C,ch,cw
    img = g[..., None]*col[:, :, None, None, :] + (1-g[..., None])*bg
    img = img.transpose(0,2,1,3,4).reshape(H, W, 3)
    frame = np.clip(img,0,255).astype(np.uint8)
    p.stdin.write(frame.tobytes())
    if f % 150 == 0: print('t', t, flush=True)
p.stdin.close(); p.wait()
