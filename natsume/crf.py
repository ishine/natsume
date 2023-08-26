import unicodedata

import CRFPP

def letters_full_to_half(text):
    converted_text = ""
    offset =  0xFF00 - 0x0020
    for char in text:
        if ord(char) >= 0x0041 and ord(char) <=  0x005a:
            converted_char = chr(ord(char) - offset)
        elif ord(char) >= 0x0061 and ord(char) <= 0x007a:
            converted_char = chr(ord(char) - offset)
        else:
            converted_char = char
        converted_text += converted_char
    return converted_text

def letters_half_to_full(text):
    converted_text = ""
    offset =  0xFF00 - 0x0020
    for char in text:
        if ord(char) >= 0x0041 and ord(char) <= 0x005a:
            converted_char = chr(ord(char) + offset)
        elif ord(char) >= 0x0061 and ord(char) <= 0x007a:
            converted_char = chr(ord(char) + offset)
        else:
            converted_char = char
        converted_text += converted_char
    return converted_text


# Reference: https://github.com/rockingdingo/deepnlp/blob/master/deepnlp/segmenter.py
class CRFPredictor(object):
    def __init__(self, model_path=None):
        self._model_path = model_path
        self._tagger = None
        self._initialize()
 
    def _initialize(self):
        if not self._model_path:
            pass
        try:
            self._tagger = CRFPP.Tagger("-m" + self._model_path)
        except:
            raise ValueError("Failed to load CRF predictor. Model path is invalid.")
            
    def predict(self, njd_features):
        """Make njd features fit the format of CRF
        """
        # default is chaining
        for i in range(len(njd_features)):
            njd_features[i]["chain_flag"] = 1

        # chain flag of the first word of a sentence is set to -1
        njd_features[0]["chain_flag"] = -1
        self._tagger.clear()
        for njd_feature in njd_features:
            # get fields
            surface = njd_feature["string"]
            pos = njd_feature["pos"]
            pos_group1 = njd_feature["pos_group1"]
            pos_group2 = njd_feature["pos_group2"]
            pos_group3 = njd_feature["pos_group3"]
            acc = njd_feature["acc"]
            mora_size = njd_feature["mora_size"]

            feature_string = f"{surface}\t{pos}\t{pos_group1}\t{pos_group2}\t{pos_group3}\t{acc}\t{mora_size}"
            self._tagger.add(feature_string)

        self._tagger.parse()
        size = self._tagger.size()
        xsize = self._tagger.xsize()

        for i in range(0, size):
            for j in range(0, xsize):
                surface = self._tagger.x(i, j) # surface
                chain_flag = self._tagger.y2(i)    # chain flag
                # assign predicted chain flag
                njd_features[i]["chain_flag"] = int(chain_flag) # chain flag is an integer

        return njd_features