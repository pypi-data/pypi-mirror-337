import random
from torch.utils.data import DataLoader, Dataset


class Maverick_Dataloader(DataLoader):
    def __init__(
        self,
        dataset: Dataset,
        shuffle=True,
        batch_size=1,
        num_workers=0,
        collate_fn=None,
    ):
        super().__init__(
            dataset,
            shuffle=shuffle,
            batch_size=batch_size,
            num_workers=num_workers,
        )
        data = list(dataset.set)
        self.batches = [collate_fn({k:[v] for k,v in b.items()}) for b in data]
        self.shuffle = shuffle

    def __iter__(self):
        if self.shuffle:
            random.shuffle(self.batches)
        for batch in self.batches:
            yield batch

    def __len__(self):
        return len(self.batches)
