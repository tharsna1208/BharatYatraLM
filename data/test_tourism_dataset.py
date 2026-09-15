from torch.utils.data import DataLoader

from .tourism_dataset import TourismDataset


dataset = TourismDataset(
    "data/tourism_corpus.txt",
    "tokenizer/vocab_v2.json",
    context_length=128
)


dataloader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=True
)


print(
    "Vocabulary size:",
    len(dataset.tokenizer.token_to_id)
)

print(
    "Number of training sequences:",
    len(dataset)
)

print(
    "Number of batches:",
    len(dataloader)
)


input_batch, target_batch = next(
    iter(dataloader)
)


print(
    "Input batch shape:",
    input_batch.shape
)

print(
    "Target batch shape:",
    target_batch.shape
)


print("First sequence input:")
print(input_batch[0][:20])


print("First sequence target:")
print(target_batch[0][:20])