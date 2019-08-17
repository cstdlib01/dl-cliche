from .image import *


def prepare_full_MNIST(data_folder):
    """
    Prepare dataset as images under:
        data_folder/images/('train' or 'valid')/(class)
    where filenames are:
        img(class)_(count index).png
    """
    train_ds = datasets.MNIST(data_folder, train=True, download=True,
                          transform=transforms.Compose([
                              transforms.Normalize((0.1307,), (0.3081,))
                          ]))
    valid_ds = datasets.MNIST(data_folder, train=False,
                              transform=transforms.Compose([
                                  transforms.Normalize((0.1307,), (0.3081,))
                              ]))

    def have_already_been_done():
        return (data_folder/'images').is_dir()
    def build_images_folder(data_root, X, labels, dest_folder):
        images = data_folder/'images'
        for i, (x, y) in tqdm.tqdm(enumerate(zip(X, labels))):
            folder = images/dest_folder/f'{y}'
            ensure_folder(folder)
            x = x.numpy()
            image = np.stack([x for ch in range(3)], axis=-1)
            PIL.Image.fromarray(image).save(folder/f'img{y}_{i:06d}.png')

    if not have_already_been_done():
        build_images_folder(data_root=DATA, X=train_ds.train_data,
                            labels=train_ds.train_labels, dest_folder='train')
        build_images_folder(data_root=DATA, X=valid_ds.test_data,
                            labels=valid_ds.test_labels, dest_folder='valid')