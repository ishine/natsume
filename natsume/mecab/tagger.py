import re
import fugashi



class MecabTagger(object):
    def __init__(self, dicdir=None):
        if dicdir is None:
            try:
                import unidic
                dicdir = unidic.DICDIR
            except BaseException:
                raise ImportError("Unidic is not installed. See {} for more information."
                                  .format("https://github.com/polm/unidic-py"))
        
        self.tagger = fugashi.GenericTagger("-d {}".format(dicdir))

    def parse(self, text):
        """Parse text
        """
        features_list = self.parse_nbest(text, num=1)

        return features_list[0]

    def parse_nbest(self, text, num=1):
        """Parse text and return the best n results
        """
        features_list = []
        results_list = self.tagger.nbestToNodeList(text, num=num)
        for results in results_list:
            # for every lattice  
            features = []
            for result in results:
                # results in every lattice
                # based on unidic，which has 29 fields
                # References: https://github.com/polm/unidic-py
                feature = {
                    "surface": result.surface,
                    "pos1": result.feature[0],
                    "pos2": result.feature[1],
                    "pos3": result.feature[2],
                    "pos4": result.feature[3],
                    "cType": result.feature[4],
                    "cForm": result.feature[5],
                    "lForm": result.feature[6],
                    "lemma": result.feature[7],
                    "orth": result.feature[8],
                    "pron": result.feature[9],
                    "orthBase": result.feature[10],
                    "pronBase": result.feature[11],
                    "goshu": result.feature[12],
                    "iType": result.feature[13],
                    "iForm": result.feature[14],
                    "fType": result.feature[15],
                    "fForm": result.feature[16],
                    "iConType": result.feature[17],
                    "fContype": result.feature[18],
                    "type": result.feature[19],
                    "kana": result.feature[20],
                    "kanaBase": result.feature[21],
                    "form": result.feature[22],
                    "formBase": result.feature[23],
                    "aType": result.feature[24],
                    "aConType": result.feature[25],
                    "aModType": result.feature[26],
                    "lid": result.feature[27],
                    "lemma_id": result.feature[28]
                }
                print(feature.keys())
                features.append(feature)

            features_list.append(features)

        return features_list

text = "すら"
tagger = MecabTagger()
features = tagger.parse(text)

for feature in features:
    print(len(feature.keys()))
    print(feature)