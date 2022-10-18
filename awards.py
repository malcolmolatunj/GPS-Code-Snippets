import os


class SubAward:
    zipped_folder_location = None

    def __init__(self, FAIN, agency_id):
        self.FAIN = FAIN
        self.agency_id = agency_id

    def is_downloaded_to(self, folder):
        downloaded_zips = os.listdir(folder)
        downloaded_fains = [name.split("_")[1] for name in downloaded_zips]
        return self.FAIN in downloaded_fains


class Grant(SubAward):
    header_text = "Grant Summary"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.usaspending.gov/award/ASST_NON_"
        self.unique_id = f"ASST_NON_{self.FAIN}_{self.agency_id}"

    @property
    def download_url(self):
        unique_url = f"{self.FAIN}_{self.agency_id}"
        return self.base_url + unique_url


class Contract(SubAward):
    header_text = "Contract Summary"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://www.usaspending.gov/award/CONT_AWD_"
        self.unique_id = f"CONT_AWD_{self.FAIN}_{self.agency_id}_-NONE-_-NONE-"

    @property
    def download_url(self):
        unique_url = f"{self.FAIN}_{self.agency_id}_-NONE-_-NONE-"
        return self.base_url + unique_url
