from pathlib import Path
from PIL import Image,ImageDraw
import pdfplumber,json
root=Path(__file__).resolve().parent
issues=[]
with pdfplumber.open(root/'output-d3/review.pdf') as doc:
 for i,p in enumerate(doc.pages):
  for w in p.extract_words():
   if w['x0']<20 or w['x1']>p.width-20 or w['top']<15 or w['bottom']>p.height-15:issues.append((i+1,w['text']))
print('Text outside safe page margins:',issues)
assert not issues
files=sorted(Path('/private/tmp').glob('d3-review-*.png'))
assert len(files)==len(doc.pages)
for start in range(0,len(files),12):
 board=Image.new('RGB',(1600,930),'#ccd0d0');draw=ImageDraw.Draw(board)
 for j,path in enumerate(files[start:start+12]):
  im=Image.open(path);im.thumbnail((390,275));x=j%4*400;y=j//4*310
  board.paste(im,(x,y+22));draw.text((x+5,y+4),path.stem,fill='black')
 board.save(f'/private/tmp/d3-qa-{start//12+1}.png')
