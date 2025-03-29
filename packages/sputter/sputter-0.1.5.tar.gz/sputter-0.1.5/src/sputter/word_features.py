"""A module for detecting interesting features of words.

Inspired by https://github.com/rdeits/Collective.jl.
"""

from collections import defaultdict
from dataclasses import dataclass
import json
import logging
import math
import os
import os.path
import platformdirs
from typing import Dict, List, Optional, Set

from sputter.fitness import WordStatistics


logger = logging.getLogger(__name__)


ALPHABET = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
VOWELS = set("AEIOU")
CONSONANTS = ALPHABET - VOWELS
CARDINAL_DIRECTIONS = set("NESW")
CHEMICAL_ELEMENT_SYMBOLS = [
    "H",
    "HE",
    "LI",
    "BE",
    "B",
    "C",
    "N",
    "O",
    "F",
    "NE",
    "NA",
    "MG",
    "AL",
    "SI",
    "P",
    "S",
    "CL",
    "AR",
    "K",
    "CA",
    "SC",
    "TI",
    "V",
    "CR",
    "MN",
    "FE",
    "CO",
    "NI",
    "CU",
    "ZN",
    "GA",
    "GE",
    "AS",
    "SE",
    "BR",
    "KR",
    "RB",
    "SR",
    "Y",
    "ZR",
    "NB",
    "MO",
    "TC",
    "RU",
    "RH",
    "PD",
    "AG",
    "CD",
    "IN",
    "SN",
    "SB",
    "TE",
    "I",
    "XE",
    "CS",
    "BA",
    "LA",
    "CE",
    "PR",
    "ND",
    "PM",
    "SM",
    "EU",
    "GD",
    "TB",
    "DY",
    "HO",
    "ER",
    "TM",
    "YB",
    "LU",
    "HF",
    "TA",
    "W",
    "RE",
    "OS",
    "IR",
    "PT",
    "AU",
    "HG",
    "TL",
    "PB",
    "BI",
    "PO",
    "AT",
    "RN",
    "FR",
    "RA",
    "AC",
    "TH",
    "PA",
    "U",
    "NP",
    "PU",
    "AM",
    "CM",
    "BK",
    "CF",
    "ES",
    "FM",
    "MD",
    "NO",
    "LR",
    "RF",
    "DB",
    "SG",
    "BH",
    "HS",
    "MT",
    "DS",
    "RG",
    "CN",
    "NH",
    "FL",
    "MC",
    "LV",
    "TS",
    "OG",
]
STATE_ABBREVIATIONS = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]


@dataclass
class WordFeaturePrecomputes:
    """Precomputes for word features."""

    __ORD_A = ord("A")

    word: str
    """The word itself."""

    word_letter_counts: List[int]
    """A list of letter counts in the word, where index 0 is A, 1 is B, etc."""

    letter_bank: Set[str]
    """The set of letters in the word."""

    def __init__(self, word: str):
        self.word = word
        self.word_letter_counts = [0] * 26
        for letter in word:
            self.word_letter_counts[ord(letter) - WordFeaturePrecomputes.__ORD_A] += 1
        self.letter_bank = set(word)

    def get_letter_count(self, letter: str):
        """Return the number of times the letter appears in the word."""
        return self.word_letter_counts[ord(letter) - WordFeaturePrecomputes.__ORD_A]


class WordFeature:
    """A base class for detecting an interesting feature of a word."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        """Return true iff the word has this feature."""
        raise NotImplementedError


@dataclass(frozen=True)
class LetterCountFeature(WordFeature):
    """Word features based on number of letter occurrences."""

    letter: str
    """The letter to count. Must be uppercase."""

    min_count: int
    """The minimum number of occurrences of the letter to satisfy this feature."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        return precomputes.get_letter_count(self.letter) >= self.min_count

    def __repr__(self) -> str:
        return f"at least {self.min_count} occurrences of {self.letter}"


@dataclass(frozen=True)
class RepeatedLetterFeature(WordFeature):
    """Word features based on number of repeated letter occurrences."""

    min_letter_count: int
    """The number of letters that must be repeated to satisfy this feature."""

    min_repeat_count: int
    """The number of letter repetitions needed to satisfy this feature."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        return (
            sum(c >= self.min_repeat_count for c in precomputes.word_letter_counts)
            >= self.min_letter_count
        )

    def __repr__(self) -> str:
        return f"at least {self.min_letter_count} letters repeated at least {self.min_repeat_count} times each"


@dataclass(frozen=True)
class UniqueLetterCountFeature(WordFeature):
    """Word features based on number of unique letter occurrences."""

    count: int
    """The number of unique letters to satisfy this feature."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        return len(precomputes.letter_bank) == self.count

    def __repr__(self) -> str:
        return f"exactly {self.count} unique letters"


@dataclass(frozen=True)
class UniqueVowelCountFeature(WordFeature):
    """Word features based on number of unique vowel occurrences."""

    count: int
    """The number of unique vowels to satisfy this feature."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        return len(precomputes.letter_bank & VOWELS) == self.count

    def __repr__(self) -> str:
        return f"exactly {self.count} unique vowels"


@dataclass(frozen=True)
class UniqueConsonantCountFeature(WordFeature):
    """Word features based on number of unique consonant occurrences."""

    count: int
    """The number of unique consonants to satisfy this feature."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        return len(precomputes.letter_bank & CONSONANTS) == self.count

    def __repr__(self) -> str:
        return f"exactly {self.count} unique consonants"


@dataclass(frozen=True)
class AlternatesVowelConsonantFeature(WordFeature):
    """Word features based on alternating vowel and consonant occurrences."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        last_was_vowel = precomputes.word[0] in VOWELS
        for c in precomputes.word[1:]:
            if c in VOWELS:
                if last_was_vowel:
                    return False
            elif not last_was_vowel:
                return False
            last_was_vowel = c in VOWELS
        return True

    def __repr__(self) -> str:
        return "alternates between vowels and consonants"


@dataclass(frozen=True)
class DoubleLettersFeature(WordFeature):
    """Word features based on number of occurrences of double letters."""

    count: int
    """The number of double letters to satisfy this feature."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        return (
            sum(
                1
                for i in range(len(precomputes.word) - 1)
                if precomputes.word[i] == precomputes.word[i + 1]
            )
            == self.count
        )

    def __repr__(self) -> str:
        return f"exactly {self.count} pairs of double letters"


@dataclass(frozen=True)
class CardinalDirectionsCountFeature(WordFeature):
    """Word features based on number of cardinal direction letters."""

    min_count: int
    """The minimum number of cardinal direction letters to satisfy this feature."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        return (
            sum(precomputes.get_letter_count(c) for c in CARDINAL_DIRECTIONS)
            >= self.min_count
        )

    def __repr__(self) -> str:
        return f"at least {self.min_count} cardinal directions"


@dataclass(frozen=True)
class ChemicalElementSymbolCountFeature(WordFeature):
    """Word features based on number of chemical element symbols."""

    min_count: int
    """The minimum number of chemical element symbols to satisfy this feature."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        count = 0
        for s in CHEMICAL_ELEMENT_SYMBOLS:
            if s in precomputes.word:
                count += 1
        return count >= self.min_count

    def __repr__(self) -> str:
        return f"at least {self.min_count} unique chemical element symbols"


@dataclass(frozen=True)
class StateAbbreviationCountFeature(WordFeature):
    """Word features based on number of US state abbreviations."""

    min_count: int
    """The minimum number of US state abbreviations to satisfy this feature."""

    def evaluate(
        self,
        precomputes: WordFeaturePrecomputes,
    ) -> bool:
        count = 0
        for s in STATE_ABBREVIATIONS:
            if s in precomputes.word:
                count += 1
        return count >= self.min_count

    def __repr__(self) -> str:
        return f"at least {self.min_count} unique US state abbreviations"


ALL_FEATURES: List[WordFeature] = [
    AlternatesVowelConsonantFeature(),
]
ALL_FEATURES.extend(
    [LetterCountFeature(letter, count) for letter in ALPHABET for count in range(1, 5)]
)
ALL_FEATURES.extend(
    [
        RepeatedLetterFeature(min_letter_count, min_repeat_count)
        for min_letter_count in range(1, 6)
        for min_repeat_count in range(2, 5)
    ]
)
ALL_FEATURES.extend([UniqueLetterCountFeature(count) for count in range(1, 27)])
ALL_FEATURES.extend(
    [UniqueVowelCountFeature(count) for count in range(1, len(VOWELS) + 1)]
)
ALL_FEATURES.extend(
    [UniqueConsonantCountFeature(count) for count in range(1, len(CONSONANTS) + 1)]
)
ALL_FEATURES.extend([DoubleLettersFeature(count) for count in range(1, 4)])
ALL_FEATURES.extend([CardinalDirectionsCountFeature(count) for count in range(1, 6)])
ALL_FEATURES.extend([ChemicalElementSymbolCountFeature(count) for count in range(1, 6)])
ALL_FEATURES.extend([StateAbbreviationCountFeature(count) for count in range(1, 6)])


@dataclass
class WordFeatureResult:
    """The result of evaluating a word feature on a set of words."""

    feature: WordFeature
    """The word feature that was evaluated."""

    words: List[str]
    """The set of words that satisfied this feature."""

    log_prob: float
    """The log probability of the feature evaluating true for the set of words."""


class WordFeatureStatistics:
    """A class for computing statistics about word features."""

    def __init__(self, ws: Optional[WordStatistics] = None):
        """Initialize a set of word feature statistics based on word frequencies.

        :param ws: The WordStatistics to use. If None, a new WordStatistics will be
            created.
        """
        self._ws = ws or WordStatistics()

        feature_log_prob_json_path = os.path.join(
            platformdirs.user_cache_dir(appname="sputter"),
            "word_feature_log_prob.json",
        )
        try:
            if os.path.exists(feature_log_prob_json_path):
                with open(feature_log_prob_json_path, "r") as f:
                    feature_log_prob_json = json.load(f)
                if {repr(ft) for ft in ALL_FEATURES} == set(
                    feature_log_prob_json.keys()
                ):
                    self._feature_log_prob = {}
                    for ft in ALL_FEATURES:
                        self._feature_log_prob[ft] = feature_log_prob_json[repr(ft)]
                    return
        except Exception as e:
            logger.warning(f"Failed to read feature log probabilities cache: {e}")

        logger.info("Computing word feature log probabilities...")

        feature_count: Dict[WordFeature, int] = defaultdict(int)

        for word, freq in self._ws.word_frequencies().items():
            precomputes = WordFeaturePrecomputes(word)
            for feature in ALL_FEATURES:
                if feature.evaluate(precomputes):
                    feature_count[feature] += freq

        word_frequency_total = self._ws.word_frequency_total()
        self._feature_log_prob = {
            feature: math.log(feature_count.get(feature, 0.01) / word_frequency_total)
            for feature in ALL_FEATURES
        }

        try:
            os.makedirs(os.path.dirname(feature_log_prob_json_path), exist_ok=True)
            with open(feature_log_prob_json_path, "w") as f:
                json.dump(
                    {repr(ft): lp for ft, lp in self._feature_log_prob.items()}, f
                )
        except Exception as e:
            logger.warning(f"Failed to cache feature log probabilities: {e}")

    def evaluate_words(
        self, words: List[str], top_n: Optional[int] = 10
    ) -> List[WordFeatureResult]:
        """Evaluate a set of words against all word features.

        :param words: The words to evaluate.
        :param top_n: The number of top results to return. If None, all results will be
            returned.

        :return: A list of WordFeatureResults, one for each word feature. The list is
            sorted by log probability, from least likely to most likely.
        """
        precomputes = [WordFeaturePrecomputes(word) for word in words]
        results = []
        for feature, feature_log_prob in self._feature_log_prob.items():
            evals = [feature.evaluate(precompute) for precompute in precomputes]
            if any(evals):
                satisfied_words = [
                    word for word, e in zip(words, evals, strict=True) if e
                ]
                results.append(
                    WordFeatureResult(
                        feature,
                        satisfied_words,
                        feature_log_prob * len(satisfied_words),
                    )
                )
        results.sort(key=lambda result: result.log_prob)
        if top_n is not None:
            results = results[:top_n]
        return results
