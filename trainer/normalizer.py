import re

# Spoken digit words to numeric values
digit_replacements = {
    "ZERO": "0", "ONE": "1", "TWO": "2", "THREE": "3",
    "FOUR": "4", "FIVE": "5", "SIX": "6", "SEVEN": "7",
    "EIGHT": "8", "NINE": "9", "TEN": "10", "ELEVEN": "11",
    "TWELVE": "12", "THIRTEEN": "13", "FOURTEEN": "14",
    "FIFTEEN": "15", "SIXTEEN": "16", "SEVENTEEN": "17",
    "EIGHTEEN": "18", "NINETEEN": "19", "TWENTY": "20",
    "TWENTY ONE": "21", "TWENTY TWO": "22", "TWENTY THREE": "23",
    "TWENTY FOUR": "24", "TWENTY FIVE": "25", "TWENTY SIX": "26",
    "TWENTY SEVEN": "27", "TWENTY EIGHT": "28", "TWENTY NINE": "29",
    "THIRTY": "30", "THIRTY ONE": "31", "THIRTY TWO": "32",
    "THIRTY THREE": "33", "THIRTY FOUR": "34", "THIRTY FIVE": "35",
    "THIRTY SIX": "36", "THIRTY SEVEN": "37", "THIRTY EIGHT": "38",
    "THIRTY NINE": "39", "FORTY": "40", "FORTY ONE": "41",
    "FORTY TWO": "42", "FORTY THREE": "43", "FORTY FOUR": "44",
    "FORTY FIVE": "45", "FORTY SIX": "46", "FORTY SEVEN": "47",
    "FORTY EIGHT": "48", "FORTY NINE": "49", "FIFTY": "50",
    "FIFTY ONE": "51", "FIFTY TWO": "52", "FIFTY THREE": "53",
    "FIFTY FOUR": "54", "FIFTY FIVE": "55", "FIFTY SIX": "56",
    "FIFTY SEVEN": "57", "FIFTY EIGHT": "58", "FIFTY NINE": "59",
    "SIXTY": "60", "SIXTY ONE": "61", "SIXTY TWO": "62",
    "SIXTY THREE": "63", "SIXTY FOUR": "64", "SIXTY FIVE": "65",
    "SIXTY SIX": "66", "SIXTY SEVEN": "67", "SIXTY EIGHT": "68",
    "SIXTY NINE": "69", "SEVENTY": "70", "SEVENTY ONE": "71",
    "SEVENTY TWO": "72", "SEVENTY THREE": "73", "SEVENTY FOUR": "74",
    "SEVENTY FIVE": "75", "SEVENTY SIX": "76", "SEVENTY SEVEN": "77",
    "SEVENTY EIGHT": "78", "SEVENTY NINE": "79", "EIGHTY": "80",
    "EIGHTY ONE": "81", "EIGHTY TWO": "82", "EIGHTY THREE": "83",
    "EIGHTY FOUR": "84", "EIGHTY FIVE": "85", "EIGHTY SIX": "86",
    "EIGHTY SEVEN": "87", "EIGHTY EIGHT": "88", "EIGHTY NINE": "89",
    "NINETY": "90", "NINETY ONE": "91", "NINETY TWO": "92",
    "NINETY THREE": "93", "NINETY FOUR": "94", "NINETY FIVE": "95",
    "NINETY SIX": "96", "NINETY SEVEN": "97", "NINETY EIGHT": "98",
    "NINETY NINE": "99"
}

# Common variations of letter sounds and spoken digits
synonym_replacements = {
    "OH": "0", "O": "0",
    "TOO": "2", "TO": "2",
    "FOR": "4", "FUR": "4",
    "ATE": "8",
    "FIFE": "5",  # sometimes misheard for five

    # Phonetic letters
    "AY": "A", "BEE": "B", "CEE": "C", "DEE": "D", "EE": "E",
    "EFF": "F", "GEE": "G", "AYCH": "H", "EYE": "I", "JAY": "J",
    "KAY": "K", "EL": "L", "EM": "M", "EN": "N", "PEE": "P",
    "QUEUE": "Q", "ARE": "R", "ESS": "S", "TEE": "T", "YOU": "U",
    "VEE": "V", "DOUBLEYOU": "W", "EX": "X", "WHY": "Y", "ZEE": "Z", "ZED": "Z",
}

# Handle formats like 6TY → 60, 6TEEN → 16
pattern_xty = re.compile(r"\b([0-9])TY\b")
pattern_xteen = re.compile(r"\b([0-9])TEEN\b")

def normalize(text: str) -> str:
    text = text.upper()

    for word, digit in digit_replacements.items():
        text = text.replace(word, digit)

    for word, replacement in synonym_replacements.items():
        text = text.replace(word, replacement)

    text = pattern_xty.sub(lambda m: str(int(m.group(1)) * 10), text)
    text = pattern_xteen.sub(lambda m: m.group(1) + "6", text)

    text = re.sub(r"[^A-Z0-9]", "", text)
    return text
