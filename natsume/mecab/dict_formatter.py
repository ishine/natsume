import os
import re
import csv

from tqdm import tqdm
from natsume.mecab import count_mora_size

_characters = r"[A-Za-z\d\u3005\u3040-\u30ff\u4e00-\u9faf\uff11-\uff19\uff21-\uff3a\uff41-\uff5a\uff66-\uff9d]"


def reformat_atype(atype):
    if atype == "*":
        atype = "0"
    else:
        atype = atype.split(",")[0]  # 选择最常用的type

    return atype

def reformat_lemma(lemma):
    """Reformat lemma
    Sometimes there are more info for lemma field, which uses comma as delimiter
    e.g. 濶端,15299,16092,9851,名詞,固有名詞,人名,一般,*,*,コデン,"コデン-Köden,Kūtān"
    """

    lemma = re.sub(r",", "%", lemma)

    return lemma


def reformat_fcontype(fcontype):
    """Reformat fConType
    This field is too complicated to know that it means...
    e.g. "B1S6SjShS,B1S6S8SjShS"
    """

    fcontype = re.sub(r",", "%", fcontype)

    return fcontype


def reformat_acontype(acontype):
    """Reformat aConType
    Some words use different chain rules depending on previous words
    e.g. "名詞%F2@1,動詞%F2@0,形容詞%F6@0,-2"
    """

    # use lookahead and lookbehind
    chain_rules = re.split(rf"(?<=\d),(?={_characters})", acontype)
    for i, chain_rule in enumerate(chain_rules):
        parts = re.split(r"[%@]", chain_rule)
        if len(parts) <= 1:
            break
        elif len(parts) == 2:
            pos, rule = parts
            chain_rules[i] = f"{pos}%{rule}"
        else:
            try:
                pos, rule, type = parts
            except:
                raise ValueError(chain_rule)
            type = re.split(",", type)[0]  # 选择常用的type
            chain_rules[i] = f"{pos}%{rule}@{type}"

    # 参照naist-jdic，以/分隔不同的chain rule
    acontype = "/".join(chain_rules)

    return acontype


def reformat_dict(input_path, output_path, config):
    """Reformat dictionary
    """

    num_cols = config["num_cols"]
    entry_cols = config["entry_cols"]
    fcontype_idx = entry_cols["fConType"]
    lemma_idx = entry_cols["lemma"]
    atype_idx = entry_cols["aType"]
    acontype_idx = entry_cols["aConType"]
    pron_idx = entry_cols["pron"]

    with open(input_path, "r", encoding="utf-8") as input, \
            open(output_path, "w", encoding="utf-8") as output:
        reader = csv.reader(input)
        writer = csv.writer(output)
        for row in reader:
            assert len(row) == num_cols
            # get cols that need to be reformatted
            lemma = row[lemma_idx]
            fcontype = row[fcontype_idx]
            atype = row[atype_idx]
            acontype = row[acontype_idx]

            # reformat
            lemma = reformat_lemma(lemma)
            fcontype = reformat_fcontype(fcontype)
            atype = reformat_atype(atype)
            acontype = reformat_acontype(acontype)

            # write back
            row[lemma_idx] = lemma
            row[fcontype_idx] = fcontype
            row[atype_idx] = atype
            row[acontype_idx] = acontype

            # NOTE: add mora_size
            pron = row[pron_idx]
            mora = count_mora_size(pron)
            row.insert(acontype_idx, mora)

            # write row
            writer.writerow(row)


def check_entries(input_path, num_cols=34):
    """Check entries of reformatted dictionary
    """

    with open(input_path, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.strip("\n")
            cols = line.split(",")
            if len(cols) != num_cols:
                print(line)


def run_demo():
    """A demo showing how to reformat a dictionary and double check the result
    """

    config = {
        "num_cols": 33,
        "entry_cols": {
            "surface": 0,
            "left_id": 1,
            "right_id": 2,
            "cost": 3,
            "pos1": 4,
            "pos2": 5,
            "pos3": 6,
            "pos4": 7,
            "cType": 8,
            "cForm": 9,
            "lForm": 10,
            "lemma": 11,
            "orth": 12,
            "pron": 13,
            "orthBase": 14,
            "pronBase": 15,
            "goshu": 16,
            "iType": 17,
            "iForm": 18,
            "fType": 19,
            "fForm": 20,
            "iConType": 21,
            "fConType": 22,
            "type": 23,
            "kana": 24,
            "kanaBase": 25,
            "form": 26,
            "formBase": 27,
            "aType": 28,
            "aConType": 29,
            "aModType": 30,
            "lid": 31,
            "lemma_id": 32
        }
    }

    input_path = "unidic-csj.csv"
    output_path = "unidic-csj_reformatted.csv"
    reformat_dict(input_path, output_path, config)
    check_entries(output_path)

