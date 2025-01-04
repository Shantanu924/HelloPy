import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
from PIL import Image
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def generate_synthetic_data(image_path, num_samples=100):
    dataset = []
    original = Image.open(image_path).convert("RGB").resize((128, 128))

    for _ in range(num_samples):
        transformed = transforms.ColorJitter(brightness=0.5, contrast=0.5)(original)
        dataset.append((original, transformed))

    return dataset

class ImageDataset(torch.utils.data.Dataset):
    def __init__(self, image_pairs, transform=None):
        self.image_pairs = image_pairs
        self.transform = transform

    def __len__(self):
        return len(self.image_pairs)

    def __getitem__(self, idx):
        img_a, img_b = self.image_pairs[idx]
        if self.transform:
            img_a = self.transform(img_a)
            img_b = self.transform(img_b)
        return img_a, img_b, (img_a + img_b) / 2 

class BlendingNet(nn.Module):
    def __init__(self):
        super(BlendingNet, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(6, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Conv2d(128, 3, kernel_size=3, stride=1, padding=1),
            nn.Sigmoid()
        )

    def forward(self, img_a, img_b):
        x = torch.cat((img_a, img_b), dim=1) 
        x = self.encoder(x)
        x = self.decoder(x)
        return x

def train_model(model, dataloader, num_epochs=10, lr=0.001):
    
    model = model.to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(num_epochs):
        epoch_loss = 0
        for img_a, img_b, target in dataloader:
            img_a, img_b, target = img_a.to(device), img_b.to(device), target.to(device)

            output = model(img_a, img_b)
            loss = criterion(output, target)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss/len(dataloader):.4f}")

def visualize_results(model, test_loader):
    model.eval()
    with torch.no_grad():
        for img_a, img_b, target in test_loader:
            img_a, img_b, target = img_a.to(device), img_b.to(device), target.to(device)
            output = model(img_a, img_b)

            # Convert tensors to images
            img_a = img_a[0].cpu().permute(1, 2, 0).numpy()
            img_b = img_b[0].cpu().permute(1, 2, 0).numpy()
            blended = output[0].cpu().permute(1, 2, 0).numpy()

            plt.figure(figsize=(12, 4))
            plt.subplot(1, 3, 1)
            plt.title("Image A")
            plt.imshow((img_a * 0.5 + 0.5).clip(0, 1)) # Denormalize
            plt.subplot(1, 3, 2)
            plt.title("Image B")
            plt.imshow((img_b * 0.5 + 0.5).clip(0, 1))
            plt.subplot(1, 3, 3)
            plt.title("Blended Image")
            plt.imshow((blended * 0.5 + 0.5).clip(0, 1))
            plt.show()
            break

# Main
if __name__ == "__main__":
    # 1. Generate synthetic data
    image_path = "./img/spiderman.jpg"
    synthetic_data = generate_synthetic_data(image_path, num_samples=100)

    # 2. Create DataLoader
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    dataset = ImageDataset(synthetic_data, transform=transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=16, shuffle=True)

    # 3. Initialize and train the model
    model = BlendingNet()
    train_model(model, dataloader, num_epochs=10, lr=0.001)

    # 4. Visualize results
    visualize_results(model, dataloader)