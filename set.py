import torch
model1 = torch.load("runs/train/best.pt")
model2=torch.load("runs/train/exp123/weights/last.pt")
for name, param in model2.named_parameters():
    if name in model1 and model1[name].shape == param.shape:
        param.data = model1[name].data.clone()
torch.save(model2.state_dict(),"runs/train/exp123/best.pt")

