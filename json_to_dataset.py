import json
import re
import base64
import os
from PIL import Image
from io import BytesIO
from absl import app, flags
from absl.flags import FLAGS
import tqdm

flags.DEFINE_string('json', './data/dataset.json', 'path to json file')
flags.DEFINE_string('output_dir', './data/imageset/', 'jgp and txt output dir')

def main(_argv):
	if not os.path.exists(FLAGS.output_dir):
		os.makedirs(FLAGS.output_dir)

	f = open(FLAGS.json)
	data = json.load(f)

	for i in tqdm.tqdm(range(len(data))):
		d = data[i]
		s = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", d['image'], re.DOTALL).groupdict().get("data")
		b = base64.urlsafe_b64decode(s + '=' * (-len(s) % 4))
		b = BytesIO(b)
		im = Image.open(b)
		im = im.convert('RGB')
		im.save(os.path.join(FLAGS.output_dir, str(i+162).zfill(5)+'.jpg'))
		info = open(os.path.join(FLAGS.output_dir, str(i).zfill(5)+'.txt'), "w+")
		for b in d['bbox']:
			if b['class']=='pcbBoardC' or b['class']=='UPlt':
				info.write("%s %f %f %f %f\n" % (b['xmin'], b['ymin'], b['xmax'], b['ymax'], b['class']))
		info.close()
	f.close()
if __name__ == '__main__':
	app.run(main)