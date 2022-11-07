import os
import time
from zipfile import BadZipFile, ZipFile

import requests
import tqdm

from awards import Contract, Grant

user_profile_path = os.environ["USERPROFILE"]

Contract.zipped_folder_location = Grant.zipped_folder_location = os.path.join(
    user_profile_path,
    r"E Glaser Ped AIDS Fdtn\ACIO - Power BI Datasets\Zipped Grant files",
)

subaward_data_folder = os.path.join(
    user_profile_path,
    r"E Glaser Ped AIDS Fdtn\ACIO - Power BI Datasets\Unzipped Grant files",
)

CDC = 7523
USAID = 7200
DOD = 1700

awards = [
    Grant("NU2GGH002178", CDC),
    Grant("NU2GGH002421", CDC),
    # Grant("NU2GGH002016", CDC),
    # Grant("N002441910011", DOD),
    # Grant("NU2HGH000084", CDC),
    Contract("72067421C00005", USAID),
    Grant("NU2GGH002211", CDC),
    # Grant("NU2GGH001948", CDC),
    Grant("NU2GGH002315", CDC),
    Grant("AID674A1600005", USAID),
    Grant("NU2GGH002301", CDC),
    Grant("NU2GGH002010", CDC),
    # Grant("NU2GGH002369", CDC),
    Grant("NU2GGH002425", CDC),
    Contract("72062122C00001", USAID),
    Grant("AID617A1500010", USAID),
]

bad_zips = []


def clear_previous_files(award_list):
    active_fains = [award.FAIN for award in award_list]
    for folder in (Grant.zipped_folder_location, subaward_data_folder):
        for fil in os.listdir(folder):
            if fil.split("_")[1] in active_fains:
                os.remove(os.path.join(folder, fil))


def download_zips(award_list):
    for award in tqdm.tqdm(award_list):
        endpoint = (
            "contract"
            if award.__class__.__name__.lower() == "contract"
            else "assistance"
        )
        response = requests.post(
            f"https://api.usaspending.gov/api/v2/download/{endpoint}/",
            json={"award_id": award.unique_id},
        )
        content = response.json()

        with open(
            os.path.join(award.zipped_folder_location, content["file_name"]), "wb"
        ) as zipped_file:
            for chunk in requests.get(content["file_url"]).iter_content():
                zipped_file.write(chunk)
        time.sleep(0.75)
    print()


def extract_csv():
    os.chdir(subaward_data_folder)
    for zipped_file in os.listdir(Grant.zipped_folder_location):
        zipped_path = os.path.join(Grant.zipped_folder_location, zipped_file)
        try:
            with ZipFile(zipped_path) as z:
                for fil in z.namelist():
                    if "Sub-Awards_1" in fil:
                        z.extract(fil)
        except BadZipFile:
            # print(f"{zipped_file} could not be extracted")
            bad_zips.extend(award for award in awards if award.FAIN in zipped_file)


def main():
    if not os.path.exists(Grant.zipped_folder_location):
        raise FileNotFoundError(f"{Grant.zipped_folder_location} could not be found")

    if not os.path.exists(Contract.zipped_folder_location):
        raise FileNotFoundError(f"{Contract.zipped_folder_location} could not be found")

    if not os.path.exists(subaward_data_folder):
        raise FileNotFoundError(f"{subaward_data_folder} could not be found")

    while True:
        downloads = bad_zips or awards
        clear_previous_files(downloads)
        download_zips(downloads)
        bad_zips.clear()
        extract_csv()
        if not bad_zips:
            break


if __name__ == "__main__":
    main()
