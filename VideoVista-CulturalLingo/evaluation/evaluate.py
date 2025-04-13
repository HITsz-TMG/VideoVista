# 根据中英文计算不同模型的得分

import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--origin_data", type=str, default="VideoVista-CulturalLingo.json", help="Path to the directory containing evaluation results")
parser.add_argument("--results_file", type=str, help="Path to the directory containing evaluation results")
args = parser.parse_args()

benchmark = json.load(open(args.origin_data, "r"))
eval_result = json.load(open(args.results_file, "r"))
qid2pred = {}
for line in eval_result:
    qid2pred[line["question_id"]] = line["pred"]

correct = 0

category2correct = {}
category2total = {}

subcategory2correct = {}
subcategory2total = {}
for line in benchmark:
    if line["question_id"] not in qid2pred:
        pred = "No Answer"
    else:
        pred = qid2pred[line["question_id"]][0]    
    
    if line["category"] not in category2total:
        category2total[line["category"]] = 0
        category2correct[line["category"]] = 0
    category2total[line["category"]] += 1
    if line["subcategory"] not in subcategory2total:
        subcategory2total[line["subcategory"]] = 0
        subcategory2correct[line["subcategory"]] = 0
    subcategory2total[line["subcategory"]] += 1
    
    if line["answer"] == pred:
        correct += 1
        category2correct[line["category"]] += 1
        subcategory2correct[line["subcategory"]] += 1
    
print(f"Overall: {correct/len(benchmark)} Len:{len(benchmark)}")
print("-----Category-----")
for k, v in category2total.items():
    print(f"{k}: {category2correct[k]/v} Len:{v}")
print("-----SubCategory-----")
for k, v in subcategory2total.items():
    print(f"{k}: {subcategory2correct[k]/v} Len:{v}")

        