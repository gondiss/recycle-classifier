import torch
from PIL import Image
from torchvision import transforms
import time

def classify():
    torch.backends.quantized.engine = "qnnpack"
    
    filename = "image.jpeg"
    model_name = "resnet-recycle-classifier_q.ptl"
    
    tokens = ["metal","plastic","glass","trash", "plastic", "cardboard"]
    
    start_time = time.time()
    input_image = Image.open(filename)
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model
    duration_time = time.time() - start_time
    print("Image load time (seconds): {0:.3f}".format(duration_time))
    
    start_time = time.time()
    model = torch.jit.load(model_name)
    duration_time = time.time() - start_time
    print("Model load time (seconds): {0:.3f}".format(duration_time))
    
    start_time = time.time()
    output = model(input_batch)
    # probabilities = torch.nn.functional.softmax(output[0], dim=0)
    # print(probabilities)
    duration_time = time.time() - start_time
    print("Inference time (seconds): {0:.3f}".format(duration_time))
    print(output[0])
    
    start_time = time.time()
    _ , pred = torch.max(output,dim=1)
    duration_time = time.time() - start_time
    print("torch maxtime (seconds): {0:.3f}".format(duration_time))

    print(tokens[pred[0].item()])
    return tokens[pred[0].item()]

#print(classify())
