import os
import pkg_resources
import six
import json

if six.PY2:
    from urllib import urlretrieve
else:
    from urllib.request import urlretrieve

import tarfile

from natsume.openjtalk import OpenJTalk
from natsume.utils import MecabFeature, NJDFeature

GLOBAL_CONFIG = {
    "dict_urls": {
        "naist-jdic": "https://github.com/r9y9/open_jtalk/releases/download/v1.11.1/open_jtalk_dic_utf_8-1.11.tar.gz",
        "naist-jdic-tdmelodic": "https://github.com/Francis-Komizu/natsume/releases/download/naist-jdic-tdmelodic/naist-jdic-tdmelodic.tar.gz"}, 
    "dict_pkgs": {
        "naist-jdic": "open_jtalk_dic_utf_8-1.11",
        "naist-jdic-tdmelodic": "naist-jdic-tdmelodic"},
}

class OpenjtalkFrontend(object):
    def __init__(self, dict_name=None, crf_model_path=None):
        self._dict_name = dict_name
        self._crf_model_path = crf_model_path
        self._oj = None  # openjtalk
        self._crf = None # crf predictor
        self._dm = None  # dictionary manager

        self._initialize()

    def _initialize(self):
        self._dm = DictManager()
        if self._crf_model_path:
            try:
                from natsume.crf import CRFPredictor
                self._crf = CRFPredictor(self._crf_model_path)
            except:
                raise ImportError("CRF++ is not installed! Please see {} for more information."
                                  .format("https://taku910.github.io/crfpp/"))
            
        dict_dir = self._dm.get_dict_dir(self._dict_name)
        self._oj = OpenJTalk(dn_mecab=dict_dir)

    def set_dict_dir(self, dict_dir):
        self._dict_dir = dict_dir
        self._initialize()

    def set_crf_model_path(self, crf_model_path):
        self._crf_model_path = crf_model_path
        self._initialize()

    def get_features(self, text, mode="word", use_crf=False):
        features = []
        if mode == "word":
            raw_features = self.get_mecab_features(text)
            for raw_feature in raw_features:
                feature = MecabFeature(raw_feature)
                features.append(feature)
        elif mode == "phrase":
            if use_crf:
                # oj -> crf -> oj
                if self._crf:
                    raw_features = self.get_njd_features_inter1(text)
                    raw_features = self._crf.predict(raw_features) 
                    raw_features = self.put_njd_features_inter1(raw_features)
                else:
                    raise ValueError("CRF++ is not installed or CRF model is not loaded.")
            else:
                raw_features = self.get_njd_features(text)

            for raw_feature in raw_features:
                feature = NJDFeature(raw_feature)
                features.append(feature)

        return features

    def get_mecab_features(self, text):
        features = self._oj.get_mecab_features(text)

        return features
    
    def get_njd_features(self, text):
        features = self._oj.get_njd_features(text)

        return features

    def get_njd_features_inter1(self, text):
        features = self._oj.get_njd_features_inter1(text)

        return features
    
    def put_njd_features_inter1(self, features):
        features = self._oj.put_njd_features_inter1(features)

        return features


# Reference: https://github.com/r9y9/pyopenjtalk/blob/master/pyopenjtalk/__init__.py    
class DictManager(object):
    def __init__(self):
        self._config_path = pkg_resources.resource_filename(__name__, "config.json")   # hardcode
        self._config = self.load_config()
        self._dict_dir = self._config["dict_dir"]

    def get_dict_dir(self, dict_name=None):
        if dict_name is None:
            # use most recently used dict download a default dict
            if self.check_dict_dir(self._dict_dir):
                # most recently used dict is availabel
                return self._dict_dir.encode("utf-8")
            elif dict_name is None:
                # download naist-jdic as default dictionary
                print("No dictionary available, download {}.".format(list(self._config["dict_urls"].keys())[0]))
                dict_name = "naist-jdic"
                dict_dir = self.download_dict(dict_name)
        
        else:
            if dict_name not in GLOBAL_CONFIG["dict_urls"].keys():
                raise ValueError("No such dictionary available. Expected {}."
                                .format(", ".join(list(GLOBAL_CONFIG["dict_urls"].keys()))))

            dict_pkg = GLOBAL_CONFIG["dict_pkgs"][dict_name]
            dict_dir = pkg_resources.resource_filename(__name__, dict_pkg)
            if self.check_dict_dir(dict_dir):
                # dict is available
                pass
            else:
                # not available, download one
                print("{} is not available, download one.".format(dict_name))
                self.download_dict(dict_name)

        return dict_dir.encode("utf-8")

    @staticmethod
    def check_dict_dir(dict_dir):
        if os.path.exists(dict_dir) and os.path.isdir(dict_dir):
            return True
        return False
    
    def download_dict(self, dict_name):
        if dict_name not in GLOBAL_CONFIG["dict_urls"].keys():
            raise ValueError("No such dictionary available. Expected {}."
                            .format(", ".join(list(GLOBAL_CONFIG["dict_urls"].keys()))))
        
        dict_url = GLOBAL_CONFIG["dict_urls"][dict_name]
        dict_pkg = GLOBAL_CONFIG["dict_pkgs"][dict_name]
        self._config["dict_name"] = dict_name

        filename = pkg_resources.resource_filename(__name__, "dic.tar.gz")
        print("Downloading dictionary from {}...".format(dict_url))
        urlretrieve(dict_url, filename)

        print("Extracting tar file {}...".format(filename))
        with tarfile.open(filename, mode="r|gz") as f:
            f.extractall(path=pkg_resources.resource_filename(__name__, ""))

        dict_dir = pkg_resources.resource_filename(__name__, dict_pkg)
        self._config["dict_dir"] = dict_dir
        self.save_config()
        os.remove(filename)
        print("Successfully downloaded {} to {}.".format(dict_name, dict_dir))

        return dict_dir
    
    def create_config(self):
        config = {
            "dict_name": "",
            "dict_dir": ""
        }
        with open(self._config_path, "w", encoding="utf-8") as f:
            json.dump(config, f)

        return config

    def load_config(self):
        if not os.path.exists(self._config_path):
            config = self.create_config()
        else:
            with open(self._config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

        return config
    
    def save_config(self):
        with open(self._config_path, "w", encoding="utf-8") as f:
            json.dump(self._config, f)
