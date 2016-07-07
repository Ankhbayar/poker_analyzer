# coding: utf-8


class PokerHandAnalyzer(object):
    # Static VARIABLES
    SUIT_S = "S"
    SUIT_H = "H"
    SUIT_D = "D"
    SUIT_C = "C"

    CARD_SUIT_ORDER = [SUIT_S, SUIT_H, SUIT_D, SUIT_C]
    CARD_NUMBER_ORDER = [
        "01",  # A
        "13",  # K
        "12",  # Q
        "11",  # J
        "10",
        "09",
        "08",
        "07",
        "06",
        "05",
        "04",
        "03",
        "02",
    ]
    # "13" - K
    # "12" - Q
    # "12" - J
    # "11" - J
    CARD_NUMBER_ORDER_ROYAL_FLUSH = ["01", "13", "12", "11", "10"]

    HAND_TYPE_ROYAL_FLUSH = "royal_flush"
    HAND_TYPE_STRAIGHT_FLUSH = "straight_flush"
    HAND_TYPE_4_OFKIND = "4_of_kind"
    HAND_TYPE_FULL_HOUSE = "full_house"
    HAND_TYPE_FLUSH = "flush"
    HAND_TYPE_STRAIGHT = "straight"
    HAND_TYPE_3_OFKIND = "3_of_kind"
    HAND_TYPE_TWO_PAIR = "two_pair"
    HAND_TYPE_ONE_PAIR = "one_pair"
    HAND_TYPE_HIGH_CARD = "high_card"

    HAND_TYPE_SORT_ORDER = [
        HAND_TYPE_ROYAL_FLUSH,
        HAND_TYPE_STRAIGHT_FLUSH,
        HAND_TYPE_4_OFKIND,
        HAND_TYPE_FULL_HOUSE,
        HAND_TYPE_FLUSH,
        HAND_TYPE_STRAIGHT,
        HAND_TYPE_3_OFKIND,
        HAND_TYPE_TWO_PAIR,
        HAND_TYPE_ONE_PAIR,
        HAND_TYPE_HIGH_CARD,
    ]

    LABEL_TRANSLATE = {
        "en": {
            HAND_TYPE_ROYAL_FLUSH: "Royal Flush",
            HAND_TYPE_STRAIGHT_FLUSH: "Straight Flush",
            HAND_TYPE_4_OFKIND: "Four Of Kind",
            HAND_TYPE_FULL_HOUSE: "Full House",
            HAND_TYPE_FLUSH: "Flush",
            HAND_TYPE_STRAIGHT: "Straight",
            HAND_TYPE_3_OFKIND: "Tree Of Kind",
            HAND_TYPE_TWO_PAIR: "Two Pair",
            HAND_TYPE_ONE_PAIR: "One Pair",
            HAND_TYPE_HIGH_CARD: "High Card",
        },
        "jp": {
            HAND_TYPE_ROYAL_FLUSH: "ロイヤルフラッシュ",
            HAND_TYPE_STRAIGHT_FLUSH: "ストレートフラッシュ",
            HAND_TYPE_4_OFKIND: "フォー・オブ・ア・カインド",
            HAND_TYPE_FULL_HOUSE: "フルハウス",
            HAND_TYPE_FLUSH: "フラッシュ",
            HAND_TYPE_STRAIGHT: "ストレート",
            HAND_TYPE_3_OFKIND: "スリー・オブ・ア・カインド",
            HAND_TYPE_TWO_PAIR: "ツーペア",
            HAND_TYPE_ONE_PAIR: "ワンペア",
            HAND_TYPE_HIGH_CARD: "ハイカード",
        },
    }

    # Internal Variables
    cards = []
    hand_card_count = 0
    is_valid = None  # Unknown
    card_suits = []
    card_numbers = []
    hand_line = ""
    parse_error_msg = ""
    lang_code = "jp"

    def __init__(self, hand_line=None, lang_code=None):
        if hand_line and self.parse(hand_line) is False:
            raise Exception("Invalid CARD")
        if lang_code:
            self.lang_code = lang_code

    def reset(self):
        self.is_valid = None
        self.hand_card_count = 0
        self.hand_type = None
        self.parse_error_msg = ""
        if self.card_suits:
            del self.card_suits[:]
        if self.cards:
            del self.cards[:]
        if self.card_numbers:
            del self.card_numbers[:]

    def parse(self, hand_line):
        # Clear
        self.reset()

        self.cards.extend(hand_line.upper().split())
        self.hand_card_count = len(self.cards)

        for card in self.cards:
            card_suit, card_number = card[0], card[1:].zfill(2)
            if card_suit not in self.CARD_SUIT_ORDER:
                self.is_valid = False
                self.parse_error_msg = "Invalid Card Suit %s only %r " % (card_suit, self.CARD_SUIT_ORDER)
                return self.is_valid
            if card_number not in self.CARD_NUMBER_ORDER:
                self.is_valid = False
                self.parse_error_msg = "Invalid Card Number %s only %r " % (card_number, self.CARD_NUMBER_ORDER)
                return self.is_valid
            self.card_numbers.append(card_number)
            self.card_suits.append(card_suit)
        # Check Duplicate Card
        if len(set(self.cards)) != self.hand_card_count:
            self.is_valid = False
            self.parse_error_msg = "Card Duplicate Card Found!!!! %r " % (self.cards)
            return self.is_valid

        # Parse OK
        self.hand_line = hand_line
        self.hand_type = self.detect_hand_type()
        self.is_valid = True
        return self.is_valid

    def get_hand_type(self):
        lang_data = self.LABEL_TRANSLATE.get(self.lang_code)
        return lang_data.get(self.hand_type, self.hand_type)

    def get_hand_sort_order(self):
        index = self.HAND_TYPE_SORT_ORDER.index(self.hand_type)
        return index

    def is_valid(self, hand_line):
        return self.is_valid

    def detect_hand_type(self):
        if self.is_royal_flush() is True:
            return self.HAND_TYPE_ROYAL_FLUSH
        elif self.is_staight_flush() is True:
            return self.HAND_TYPE_STRAIGHT_FLUSH
        elif self.is_four_of_kind() is True:
            return self.HAND_TYPE_4_OFKIND
        elif self.is_fullhouse() is True:
            return self.HAND_TYPE_FULL_HOUSE
        elif self.is_flash() is True:
            return self.HAND_TYPE_FLUSH
        elif self.is_straight() is True:
            return self.HAND_TYPE_STRAIGHT
        elif self.is_tree_of_kind() is True:
            return self.HAND_TYPE_3_OFKIND
        elif self.is_two_pair() is True:
            return self.HAND_TYPE_TWO_PAIR
        elif self.is_one_pair() is True:
            return self.HAND_TYPE_ONE_PAIR
        return self.HAND_TYPE_HIGH_CARD

    def is_royal_flush(self):
        if self.hand_card_count != 5:
            return False
        if len(set(self.card_suits)) > 1:
            return False
        if self.card_numbers != self.CARD_NUMBER_ORDER_ROYAL_FLUSH:
            return False
        return True

    def is_staight_flush(self):
        if self.hand_card_count != 5:
            return False

        if len(set(self.card_suits)) > 1:
            return False

        # "020304050607080910111213"
        card_order_check_lst = "".join(["%02d" % x for x in range(2, 14)])

        card_index_lst = []
        for card_number in self.card_numbers:
            c_index = self.CARD_NUMBER_ORDER.index(card_number)
            card_index_lst.append("%02d" % c_index)
        card_index_lst.sort()
        card_result = "".join(card_index_lst)
        try:
            # Order Success
            card_order_check_lst.index(card_result)
            return True
        except ValueError:
            return False

    def is_four_of_kind(self):
        if self.hand_card_count < 4:
            return False

        diff_number_types = set(self.card_numbers)
        for card_number in diff_number_types:
            if self.card_numbers.count(card_number) == 4:
                return True
        return False

    def is_fullhouse(self):
        if self.hand_card_count != 5:
            return False

        diff_number_types = list(set(self.card_numbers))
        if len(diff_number_types) != 2:
            return False

        if self.card_numbers.count(diff_number_types[0]) not in [2, 3]:
            return False
        return True

    def is_flash(self):
        if self.hand_card_count != 5:
            return False

        diff_type_suites = set(self.card_suits)
        if len(diff_type_suites) != 1:
            return False

        return True

    def is_straight(self):
        if self.hand_card_count != 5:
            return False

        # "020304050607080910111213"
        card_sort_check_lst = "".join(["%02d" % x for x in range(2, 14)])

        card_index_lst = []
        for card_number in self.card_numbers:
            c_index = self.CARD_NUMBER_ORDER.index(card_number)
            card_index_lst.append("%02d" % c_index)
        card_index_lst.sort()
        card_result = "".join(card_index_lst)
        try:
            # Order Success
            card_sort_check_lst.index(card_result)
            return True
        except ValueError:
            return False

        return True

    def is_tree_of_kind(self):
        if self.hand_card_count != 5:
            return False

        diff_numbers = set(self.card_numbers)
        if len(diff_numbers) != 3:
            return False
        found_tree_num = False
        for diff_num in diff_numbers:
            if self.card_numbers.count(diff_num) == 3:
                found_tree_num = True
        return found_tree_num

    def is_two_pair(self):
        if self.hand_card_count != 5:
            return False

        diff_numbers = set(self.card_numbers)
        if len(diff_numbers) != 3:
            return False

        num_dups = []
        for diff_num in diff_numbers:
            num_dups.append(self.card_numbers.count(diff_num))
        if num_dups.count(2) != 2:
            return False
        return True

    def is_one_pair(self):
        if self.hand_card_count != 5:
            return False

        diff_numbers = set(self.card_numbers)
        num_dups = []
        for diff_num in diff_numbers:
            num_dups.append(self.card_numbers.count(diff_num))
        if num_dups.count(2) != 1:
            return False
        return True


pa = PokerHandAnalyzer()


TEST_CASES = [
    {
        "hand_type": PokerHandAnalyzer.HAND_TYPE_ROYAL_FLUSH,
        "hand_line": "H1 h13 h12 h11 h10",
    },
    {
        "hand_type": PokerHandAnalyzer.HAND_TYPE_FLUSH,
        "hand_line": "C1 C6 C5 C4 C3",
    },
    {
        "is_valid": False,
        "error_msg": "Duplicate",
        "hand_line": "C4 C6 C5 C4 C3",
    },
    {
        "is_valid": False,
        "error_msg": "Invalid Card Suit",
        "hand_line": "J4 C6 C5 C4 C3",
    },
    {
        "hand_type": PokerHandAnalyzer.HAND_TYPE_FLUSH,
        "hand_line": "H10 H11 H5 H4 H3",
    },
    {
        "hand_type": PokerHandAnalyzer.HAND_TYPE_FLUSH,
        "hand_line": "H10 H11 H5 H4 H3",
    },
]

for test_data in TEST_CASES:
    is_valid = test_data.get("is_valid", True)
    hand_type = test_data.get("hand_type", None)
    hand_type = test_data.get("hand_type", None)
    error_msg = test_data.get("error_msg", None)
    assert pa.parse(test_data.get("hand_line")) == is_valid, "IS Valid %r" % test_data
    assert pa.hand_type == hand_type, "Hand Type Must '%s' result %s TD %r" % (hand_type, pa.hand_type, test_data)
    assert pa.hand_type == hand_type, "Hand Type Must '%s' result %s TD %r" % (hand_type, pa.hand_type, test_data)
    if error_msg:
        assert error_msg in pa.parse_error_msg, "Parse Error msg contains '%s' error_msg %s TD %r" % (error_msg, pa.parse_error_msg, test_data)


# print "STRAIGHT_FLUSH", pa.parse("C7 C6 C5 C4 C3"), pa.hand_type, pa.parse_error_msg
# print "Flush", pa.parse("C1 C6 C5 C4 C3"), pa.hand_type, pa.parse_error_msg
# print "DUPLICATE", pa.parse("C4 C6 C5 C4 C3"), pa.hand_type, pa.parse_error_msg
# print "INVALID SUIT", pa.parse("J4 C6 C5 C4 C3"), pa.hand_type, pa.parse_error_msg
# print "INVALID NUMBER", pa.parse("C40 C6 C5 C4 C3"), pa.hand_type, pa.parse_error_msg
# print "Flush", pa.parse("H10 H11 H5 H4 H3"), pa.hand_type, pa.parse_error_msg
# print pa.parse("H1 h10 h12 h11 h13"), pa.hand_type, pa.parse_error_msg
# print pa.parse("H1 h13 h12 h11 h10"), pa.hand_type, pa.parse_error_msg
