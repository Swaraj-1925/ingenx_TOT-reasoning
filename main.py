
from  tqdm import  tqdm
from config import Config
from omegaconf import OmegaConf
import argparse
import json
import  pandas as pd

from tot_reasoning.tot.tot_tree import TotTree


def load_ds(file: str):
    required_columns = {'question', 'answer'}
    if file.endswith(".jsonl"):
        data = []
        with open(file, "r") as f:
            lines = f.readlines()
        for line in lines:
            data.append(json.loads(line))
    elif file.endswith(".csv"):
        data =[]
        df = pd.read_csv(file)
        if not required_columns.issubset(df.columns):
            raise ValueError(f"df must contain columns {required_columns}")
        for row in df.iterrows():
            question = row["question"]
            answer = row["answer"]
            data.append({"question": question, "answer": answer})
    elif file.endswith(".parquet"):
        data = []
        df = pd.read_parquet(file)
        if not required_columns.issubset(df.columns):
            raise ValueError(f"df must contain columns {required_columns}")
        for row in df.iterrows():
            question = row["question"]
            answer = row["answer"]
            data.append({"question": question, "answer": answer})
    else:
        raise ValueError(f"Unrecognized file format: {file}")
    return data

def batch(iterable, n=-1):
    l = len(iterable)
    if n <= 0:
        n = l
    for ndx in range(0, l, n):
        yield iterable[ndx: min(ndx + n, l)]

def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--custom_cfg', type=str, default="config/sft_eval_mcts.yaml")
    args.add_argument("--ds", type=str, default="", help="quesuion and answer file")
    args.add_argument('--model_dir', type=str, default="")
    args.add_argument('--reward_model_dir', type=str, default="")
    args.add_argument('--save_in_model', type=str, default="")
    args = args.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    cfg = OmegaConf.structured(Config)
    if args.custom_cfg:
        custom_config = OmegaConf.load(args.custom_cfg)
        config = OmegaConf.merge(cfg, custom_config)
    cfg = OmegaConf.create(OmegaConf.to_yaml(cfg, resolve=True))
    if args.model_dir:
        cfg.model_dir = args.model_dir
    if args.reward_model_dir:
        cfg.reward_model_dir = args.reward_model_dir
    print("--------------------- configs ----------------------")
    print(cfg)
    print("----------------------------------------------------")

    data = load_ds(args.ds)
    agent = TotTree

    for cur_data in tqdm(batch(data,cfg.batch_size)):
        agents = [agent(config=cfg,question=d["question"],ground_truth=str(d["solution"]))
                  for d in cur_data]
