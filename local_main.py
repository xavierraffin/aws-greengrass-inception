import os
import sys
import load_model

exists=(os.path.isfile("Inception-BN-symbol.json") and os.path.isfile("Inception-BN-0000.params"))

def predict_cam():
    model_path = './'
    global_model = load_model.ImagenetModel(model_path + 'synset.txt', model_path + 'Inception-BN')
    while (True):
        predictions = global_model.predict_from_cam() 
        print(predictions)

if not exists:
    import urllib
    urllib.urlretrieve ("http://data.mxnet.io/models/imagenet/inception-bn/Inception-BN-symbol.json", "Inception-BN-symbol.json")
    urllib.urlretrieve ("http://data.mxnet.io/models/imagenet/inception-bn/Inception-BN-0126.params", "Inception-BN-0000.params")
    print("Models downloaded")

predict_cam()
