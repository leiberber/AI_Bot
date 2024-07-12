import torch


class autoencoder(torch.nn.Module):
    def __init__(self):
        super(autoencoder,self).__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(28 * 28, 256),
            torch.nn.ReLU(inplace=True),
            torch.nn.Linear(256, 64),
            torch.nn.ReLU(inplace=True),
            torch.nn.Linear(64, 16),
            torch.nn.ReLU(inplace=True),
            torch.nn.Linear(16, 3),
        )
        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(3, 16),
            torch.nn.ReLU(inplace=True),
            torch.nn.Linear(16, 64),
            torch.nn.ReLU(inplace=True),
            torch.nn.Linear(64, 256),
            torch.nn.ReLU(inplace=True),
            torch.nn.Linear(256, 28 * 28),
            torch.nn.Sigmoid()
        )

    def forward(self, x):
        y_encoder = self.encoder(x)
        y_decoder = self.decoder(y_encoder)
        return y_encoder, y_decoder


import torchvision


net = autoencoder()
transforms = torchvision.transforms.Compose([torchvision.transforms.ToTensor])
train_dataset = torchvision.datasets.MNIST("./mnist_dataset", transform=transforms, download=True)

train_databatch = torch.utils.data.DataLoader(train_dataset, batch_size=1000, shuffle=True)
f_loss = torch.nn.MSELoss(reduction="mean")
optimizer = torch.optim.Adam(net.parameters(), lr=0.001)
import os
n_epoch = 2
n_interval = 60
out_dir = "out_train"

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

is_cuda = torch.cuda.is_available()
net = net.cuda() if is_cuda else net

n_epoch = 100
n_interval = 10
for n_iter in range(1, n_epoch + 1):
    # 小技巧：不去处理自动求导的关闭
    def closure():
        global v_loss, x, y_
        optimizer.zero_grad()
        x = x.view(x.shape[0], -1)     # [N  C  H  W]
        _, y_ = net(x)
        v_loss = f_loss(y_, x)
        v_loss.backward()
        return v_loss

    for x, _ in train_databatch:
        x = x.cuda() if  is_cuda else x
        optimizer.step(closure)

    if n_iter % n_interval == 0:
        # 保存模型，或者输出数据
        print(f_loss.detach().cpu().numpy())
        torch.save(net.state_dict(), "out_train/result2.pt")

torch.save(net.state_dict(), "out_train/result2.pt")
net2 = autoencoder()
net2.load_state_dict(torch.load("out_train/result2.pt"))
is_cuda = torch.cuda.is_available()
net2 = net2.cuda() if is_cuda else net2
torch.seed()

encode = torch.FloatTensor(100, 3).uniform_(-15, 15)
encode = encode.cuda() if is_cuda else encode

decode = net2.decoder(encode)
t100_img = decode.view(-1, 1, 28, 28)
torchvision.utils.save_image(t100_img, "decode.png")

from IPython.display import display, Image
display(Image("decode.png"))

