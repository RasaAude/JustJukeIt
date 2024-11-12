import drive_api
service = drive_api.get_drive_service()
'''unis = [
    "agw2135",
    "ahk2181",
    "al4574",
    "ab5927",
    "av3099",
    "akj2147",
    "bip2106",
    "bes2178",
    "dls2230",
    "egh2138",
    "ecb2215",
    "ekm2164",
    "ehl2158",
    "fer2121",
    "gc3082",
    "jrb2299",
    "jw4346",
    "jpd2208",
    "jem2349",
    "jhw2175",
    "mc5517",
    "nhk2130",
    "nsr2144",
    "ocb2111",
    "ona2107",
    "ocg2108",
    "pjw2145",
    "rmc2234",
    "sja2180",
    "spt2120",
    "smw2259",
    "scs2269",
    "suf2102",
    "wg2445"
]'''
#for uni in unis:
    #drive_api.create_workout_folder(service, uni)

drive_api.add_folder_to_all_subfolders(service, "10_Min")