from meilisearch import Client

# اتصال به کلاینت MeiliSearch
client = Client('http://127.0.0.1:7700')

# انتخاب اندیس مورد نظر
index = client.index('words')

# تنظیمات پیش‌فرض
default_settings = {
    "displayedAttributes": ["*"],
    "searchableAttributes": ["word"],
    "filterableAttributes": [],
    "sortableAttributes": [],
    "rankingRules": [
        "typo",
        "words",
        "proximity",
        "attribute",
        "sort",
        "exactness"
    ],
    "stopWords": [],
    "synonyms": {},
    "distinctAttribute": None,
    # "proximityPrecision": 1,
    "typoTolerance": {
        "enabled": True,
        "minWordSizeForTypos": {
            "oneTypo": 4,
            "twoTypos": 8
        },
        "disableOnWords": [],
        "disableOnAttributes": []
    },
    "faceting": {
        "maxValuesPerFacet": 100,
        # "sortFacetValuesBy": "count"
    },
    "pagination": {
        "maxTotalHits": 1000
    },
    "searchCutoffMs": None,
    "localizedAttributes": None,
    "facetSearch": False,
    # "prefixSearch": False
}

my_settings = {
    "displayedAttributes": ["*"],
    "searchableAttributes": ["word"],
    "filterableAttributes": ["word"],
    "sortableAttributes": [],
    "rankingRules": [
        "typo",
        "words",

        "proximity",
        "attribute",
        "sort",
        "exactness"
    ],
    "stopWords": [],
    "synonyms": {
    },
    "distinctAttribute": None,
    # "proximityPrecision": 1,
    "typoTolerance": {
        "enabled": True,
        "minWordSizeForTypos": {
            "oneTypo": 4,
            "twoTypos": 8
        },
        "disableOnWords": [],
        "disableOnAttributes": []
    },
    "faceting": {
        "maxValuesPerFacet": 100,
        # "sortFacetValuesBy": "count"
    },
    "pagination": {
        "maxTotalHits": 1000
    },
    "searchCutoffMs": None,
    "localizedAttributes": None,
    "facetSearch": False,
    # "prefixSearch": False
}

# به‌روزرسانی تنظیمات اندیس
response = index.update_settings(my_settings)
print("success")



