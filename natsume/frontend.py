from natsume.oj import OpenjtalkFrontend
from natsume.utils import (
    features_to_tokens, tokens_to_phonemes, convert_fonts
)

class Natsume(object):
    def __init__(self,
                 dict_name=None,
                 crf_model_path=None):
        self._oj = OpenjtalkFrontend(dict_name=dict_name, crf_model_path=crf_model_path)
        self._g2p_modes = ["romaji", "ipa"]
        self._token_modes = ["word", "phrase"]

    def tokenize(self, text, mode="word", use_crf=False):
        """Tokenize text into tokens
        """
        if mode not in self._token_modes:
            raise ValueError(
                "Invalid mode for tokenization. Expected {}, got {} instead."
                .format(", ".join(self._token_modes), mode)
            )
        
        features = self._oj.get_features(text, mode=mode, use_crf=use_crf)
        tokens = features_to_tokens(features, mode=mode)
        return tokens


    def g2p(self, text, phoneme_mode="romaji", token_mode="word", with_accent=False, use_crf=False):
        """Grapheme-to-phoneme conversion
        """
        if phoneme_mode not in self._g2p_modes:
            raise ValueError(
                "Invalid mode for g2p. Expected {}, got {} instead."
                .format(", ".join(self._g2p_modes), phoneme_mode)
            )
        
        tokens = self.tokenize(text, token_mode, use_crf=use_crf)
        phonemes = tokens_to_phonemes(tokens, phoneme_mode, with_accent=with_accent)

        return phonemes

    def convert_fonts(self, text, reverse=False):
        """Conversion between new fonts and old fonts
        """
        text = convert_fonts(text, reverse=reverse)

        return text
    
    def text2mecab(self, text):
        """Get raw MeCab features
        """
        mecab_features = self._oj.get_mecab_features(text)
        
        return mecab_features


    def text2njd(self, text):
        """Get raw NJD features
        """
        njd_features = self._oj.get_njd_features(text)

        return njd_features
    
    def get_njd_inter1(self, text):
        njd_features = self._oj.get_njd_features_inter1(text)

        return njd_features
    
    def put_njd_inter1(self, features):
        njd_features = self._oj.put_njd_features_inter1(features)

        return njd_features

    def set_dict_dir(self, dict_dir):
        # TODO: support mannualy setting dictionary directory
        pass


