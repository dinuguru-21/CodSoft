from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests

# Load pretrained model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load an image (example from the web)
img_url = "https://tse1.mm.bing.net/th/id/OIP.799jKm0kFXaF_hXqpWcRYwHaFj?rs=1&pid=ImgDetMain&o=7&rm=3"
image = Image.open(requests.get(img_url, stream=True).raw)

# Generate caption
inputs = processor(images=image, return_tensors="pt")
out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))
