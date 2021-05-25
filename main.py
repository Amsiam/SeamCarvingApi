from flask import Flask,jsonify,request

from PIL import Image
from io import BytesIO
from base64 import b64decode
import numpy as np
from PIL import Image
import seam_carving



app = Flask(__name__)

@app.route('/',methods=('POST',))
def image():

	json_data = request.get_json()
	img_data = json_data['image']

	im = Image.open(BytesIO(b64decode(img_data.split(',')[1])))
	outputfile = "output.jpg"
	rgb_im = im.convert('RGB')
	rgb_im.save(outputfile)
	src = np.array(Image.open(outputfile))
	src_h, src_w, _ = src.shape
	dst = seam_carving.resize(
		src, (src_w - 200, src_h),
		energy_mode='backward',   # Choose from {backward, forward}
		order='width-first',  # Choose from {width-first, height-first}
		keep_mask=None
	)
	Image.fromarray(dst).save("image.png")

	return "Hi"


if __name__ == "__main__":
	app.run(debug=True)