from pathlib import Path; import sys; sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from lib.proc_init_utils import initialise_cpu; initialise_cpu()

from functools import partial
from transformers import LlamaTokenizer

from lib.dataloader import LlamaDataLoader
from lib.gsm_data import GSMDataset, train_collate_fn_factory

batch_size = 4
seed = 0
max_len = 512

def main() -> None:
    dataset = GSMDataset(split='train')
    tokenizer = LlamaTokenizer.from_pretrained('../llama-weights/7B')
    collate_fn = partial(train_collate_fn_factory, tokenizer, max_len)
    dataloader = LlamaDataLoader(dataset, collate_fn, batch_size, seed)

    for seq, seq_mask, labels, labels_mask in dataloader:
        print('seq', seq)
        print('seq_mask', seq_mask)
        print('labels', labels)
        print('labels_mask', labels_mask)

if __name__ == '__main__':
    main()