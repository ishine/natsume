# Natsume/棗

[![PyPI](https://img.shields.io/pypi/v/natsume.svg)](https://pypi.python.org/pypi/natsume)
[![GPL](https://img.shields.io/github/license/Francis-Komizu/natsume.svg)](https://github.com/Francis-Komizu/natsume/blob/master/LICENSE)

## Introduction

Natsume is a toolkit for Japanese text frontend processing. It's based on the open source project [OpenJTalk](http://open-jtalk.sp.nitech.ac.jp/) and its python wrapper [pyopenjalk](https://github.com/r9y9/pyopenjtalk).

Natsume has the following main features:
- Doesn't use [full context labels](http://hts.sp.nitech.ac.jp/archives/2.3/HTS-demo_NIT-ATR503-M001.tar.bz2): The NJD features in OpenJTalk are already enough for determining the boundary and accent nucleus of an accent phrase. In addition, JPCoomon could sometimes bring redundant boundaries.

- Apply more rules: On top of the rules provided in OpenJTalk, we have derived some additional rules based on literature and case studies. Also, few original rules have been modified. Please see [njd_set_accent_phrase](libs/open_jtalk/src/njd_set_accent_phrase) for more information.

- Support CRF-based accent phrase boundary estimation

- Support morphological analysis using [tdmelodic](https://github.com/PKSHATechnology-Research/tdmelodic)

## Updates
- 2023/08/27: Support accent sandhi estimation using [marine](https://github.com/6gsn/marine).
- 2023/08/26: Support accent phrase boundary estimation based on CRF (model is not publicly available yet).

## Build Requirements

- C/C++ compilers
- cmake 
- cython

## Platforms

- Mac OSX

- Linux

## Installation

```bash
pip install natsume
```

If you're having problems installing, please refer to [common problems](docs/common_problems.md)

## Usage

### Grapheme-to-Phoneme

```python
from natsume import Natsume

frontend = Natsume()

text = "天気がいいから、散歩しましょう。"
```

**Romaji**

Convert text to Romaji.

```python
phonemes = frontend.g2p(text, phoneme_mode="romaji", token_mode="phrase")
print(" ".join(phonemes))
```

```bash
teNkiga iikara , saNpo shimasho: .
```

**IPA**

Convert text to IPA (broad transcription).

```python
phonemes = frontend.g2p(text, phoneme_mode="ipa", token_mode="phrase")
print(" ".join(phonemes))
```

```bash
teNkiga iikaɾa , saNpo ɕimaɕo: .
```

**With Accent**

Convert text to phonemes with accent.

```python
phonemes = frontend.g2p(text, phoneme_mode="romaji", token_mode="phrase", with_accent=True)
print(" ".join(phonemes))
```

```bash
teꜜNkiga iꜜikara , saꜛNpo shiꜛmashoꜜ: .
```

## Tokenization

```python
from natsume import Natsume

frontend = Natsume()

text = "何の話をしているのかまったくわからない。"
```

**Word**

Tokenize text in word level.

```python
tokens = frontend.tokenize(text, mode="word")
print(" ".join([token.surface() for token in tokens]))
```

```bash
何 の 話 を し て いる の か まったく わから ない 。
```

**Phrase**

Tokenize text in (accent) phrase level.

```python
tokens = frontend.tokenize(text, mode="phrase")
print(" ".join([token.surface() for token in tokens]))
```

```bash
何の 話を して いるのか まったく わからない 。
```

## Using ML/DL models

Specify `mode` argument to use corresponding models. Currently, the following models are supported.

- `rule`: Default rule-based methoed.
- `crf`: Use CRF to estimate the accent phrase boundary, which is more accurate and reasonable compared to rule-based method.
- `marine`: Use [marine](https://github.com/6gsn/marine), a DNN-based accent sandhi predictor, to predict accent phrase boundary and accent nucleus simultaneouly. It's better than CRF but relatively slow.

```python
from natsume import Natsume

frontend = Natsume(dict_name="naist-jdic",
                   crf_model_path="natsume/crf_model")

text = "今度機会があれば飲んでみてください。"

tokens = frontend.tokenize(text, mode="phrase", model="rule")
tokens = frontend.tokenize(text, mode="phrase", model="crf")
tokens = frontend.tokenize(text, mode="phrase", model="marine")
```

```bash
# ground truth
今度 機会が あれば 飲んでみてください 。

# rule-based
今度 機会が あれば 飲んで みて ください 。

# CRF
今度 機会が あれば 飲んでみてください 。

# marine
今度 機会が あれば 飲んでみて ください。
```

### MeCab Features

Get intermediate [MeCab](https://taku910.github.io/mecab/) features.

```python
from natsume import Natsume

frontend = Natsume()

text = "人間は「食べて寝て」を繰り返すと牛になる。"

mecab_features = frontend.text2mecab(text)

for mecab_feature in mecab_features:
    surface = mecab_feature["surface"]
    feature_string = ",".join(list(mecab_feature.values())[1:])
    print("{}\t{}".format(surface, feature_string))
```

```bash
人間	名詞,一般,*,*,*,*,人間,ニンゲン,ニンゲン,0/4,C2
は	助詞,係助詞,*,*,*,*,は,ハ,ワ,0/1,名詞%F1/動詞%F2@0/形容詞%F2@0
「	記号,括弧開,*,*,*,*,「,「,「,*/*,*
食べ	動詞,自立,*,*,一段,連用形,食べる,タベ,タベ,2/2,*
て	助詞,接続助詞,*,*,*,*,て,テ,テ,0/1,動詞%F1/形容詞%F1/名詞%F5
寝	動詞,自立,*,*,一段,連用形,寝る,ネ,ネ,1/1,*
て	助詞,接続助詞,*,*,*,*,て,テ,テ,0/1,動詞%F1/形容詞%F1/名詞%F5
」	記号,括弧閉,*,*,*,*,」,」,」,*/*,*
を	助詞,格助詞,一般,*,*,*,を,ヲ,ヲ,0/1,動詞%F5/名詞%F1
繰り返す	動詞,自立,*,*,五段・サ行,基本形,繰り返す,クリカエス,クリカエス,3/5,*
と	助詞,接続助詞,*,*,*,*,と,ト,ト,0/1,形容詞%F1/動詞%F1
牛	名詞,一般,*,*,*,*,牛,ウシ,ウシ,0/2,C3
に	助詞,格助詞,一般,*,*,*,に,ニ,ニ,0/1,動詞%F5/形容詞%F1/名詞%F1
なる	動詞,自立,*,*,五段・ラ行,基本形,なる,ナル,ナル,1/2,*
。	記号,句点,*,*,*,*,。,。,。,*/*,*
```

### Font Conversion

Convert new fonts to old fonts and vice versa. 

Please note that 「弁」 has several old fonts. Now, for simplicity, Natsume converts it to 「辯」. 

```python
from natsume import Natsume

frontend = Natsume()

new = "桜、桜、うたかたに。"

old = frontend.convert_fonts(new, reverse=False)
print(old)
```
```bash
櫻、櫻、うたかたに。
```

## Dictionary

By default, Natsume uses [naist-jdic](http://naist-jdic.osdn.jp/). If you would like to use [tdmelodic](https://github.com/PKSHATechnology-Research/tdmelodic), specify `dict_name` argument.

```python
from natsume import Natsume

frontend = Natsume(dict_name="naist-jdic-tdmelodic")
```

Here's a example showing how tdmelodic is robust to neologisms.

```python
text = "龍野町に住んでいます。"

mecab_features = frontend.text2mecab(text)

for mecab_feature in mecab_features:
    surface = mecab_feature["surface"]
    feature_string = ",".join(list(mecab_feature.values())[1:])
    print("{}\t{}".format(surface, feature_string))
```

**without tdmelodic**

```bash
龍野	名詞,固有名詞,地域,一般,*,*,龍野,タツノ,タツノ,0/3,C2
町	名詞,接尾,地域,*,*,*,町,マチ,マチ,2/2,C3
に	助詞,格助詞,一般,*,*,*,に,ニ,ニ,0/1,動詞%F5/形容詞%F1/名詞%F1
住ん	動詞,自立,*,*,五段・マ行,連用タ接続,住む,スン,スン,1/2,*
で	助詞,接続助詞,*,*,*,*,で,デ,デ,1/1,動詞%F1
い	動詞,非自立,*,*,一段,連用形,いる,イ,イ,0/1,*
ます	助動詞,*,*,*,特殊・マス,基本形,ます,マス,マス’,1/2,動詞%F4@1/助詞%F2@1
。	記号,句点,*,*,*,*,。,。,。,*/*,*
```

**with tdmelodic**

```bash
龍野町	名詞,固有名詞,一般,*,*,*,龍野町,タツノチョウ,タツノチョー,3/5,*
に	助詞,格助詞,一般,*,*,*,に,ニ,ニ,0/1,動詞%F5/形容詞%F1/名詞%F1
住ん	動詞,自立,*,*,五段・マ行,連用タ接続,住む,スン,スン,1/2,*
で	助詞,接続助詞,*,*,*,*,で,デ,デ,1/1,動詞%F1
い	動詞,非自立,*,*,一段,連用形,いる,イ,イ,0/1,*
ます	助動詞,*,*,*,特殊・マス,基本形,ます,マス,マス’,1/2,動詞%F4@1/助詞%F2@1
。	記号,句点,*,*,*,*,。,。,。,*/*,*
```


## LICENCE

- Natsume: GPL license ([LICENSE](licenses/LICENSE))
- pyopenjtalk: MIT license ([LICENSE.md](https://github.com/r9y9/pyopenjtalk/LICENSE.md))
- OpenJTalk: Modified BSD license ([COPYING](https://github.com/r9y9/open_jtalk/blob/1.10/src/COPYING))
- marine: Apache 2.0 license([LICENSE](https://github.com/6gsn/marine/LICENSE))

## References

- [OpenJTalk](https://open-jtalk.sourceforge.net/)
- [pyopenjtalk](https://github.com/r9y9/pyopenjtalk)
- [tdmelodic](https://github.com/PKSHATechnology-Research/tdmelodic)
- [tdmelodic_openjtalk](https://github.com/sarulab-speech/tdmelodic_openjtalk)
- [単語の追加方法](https://github.com/sarulab-speech/tdmelodic_openjtalk)
- [CRF++: Yet Another CRF toolkit](https://taku910.github.io/crfpp/)
- [marine](https://github.com/6gsn/marine)
- [OpenJTalkの解析資料](https://www.negi.moe/negitalk/openjtalk.html)
- [Wikipedia: Hiragana](https://en.wikipedia.org/wiki/Hiragana)
- [新旧字体対照表](https://hagitaka.work/wp-content/uploads/2021/07/%E6%96%B0%E6%97%A7%E5%AD%97%E4%BD%93%E5%AF%BE%E7%85%A7%E8%A1%A8-1.pdf)

