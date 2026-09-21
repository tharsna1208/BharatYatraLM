from data.tourism_dataset import TourismDataset


train_dataset = TourismDataset(
    "data/tourism_train.txt",
    "tokenizer/vocab_v3.json",
    context_length=128
)


validation_dataset = TourismDataset(
    "data/tourism_validation.txt",
    "tokenizer/vocab_v3.json",
    context_length=128
)


print(
    "Vocabulary size:",
    len(train_dataset.tokenizer.token_to_id)
)

print(
    "Training sequences:",
    len(train_dataset)
)

print(
    "Validation sequences:",
    len(validation_dataset)
)


print(
    "Training first input shape:",
    train_dataset[0][0].shape
)

print(
    "Validation first input shape:",
    validation_dataset[0][0].shape
)