import bin.logic.web
import bin.logic.filesystem
import bin.logic.geo
import bin.settings.settings as settings

import time
import random

def recursive_json_parse_for_key_value_fc(json_dc, key_str):
    """
    Recursively searches for a key in JSON data of any nesting level and returns its value.
    The search stops at the first occurrence of the key.

    Arguments:
    json_dc: JSON data as a Python dictionary or list.
    key_str: The key whose value to find (string).

    Returns:
    The value of the key, if the key is found, otherwise None.
    """

    if isinstance(json_dc, dict):
        if key_str in json_dc:
            return json_dc[key_str]
        for element in json_dc.values():
            res = recursive_json_parse_for_key_value_fc(element, key_str)
            if res is not None:
                return res
    elif isinstance(json_dc, list):
        for element in json_dc:
            res = recursive_json_parse_for_key_value_fc(element, key_str)
            if res is not None:
                return res
    return None # Key not found in current branch


class BaseParser:
    PLATFORMNAME_STR = None
    URL_START_STR = None
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    backuped_original_results_filename_str = ""

    def __init__(self, platformname_str, url_start_str):
        self.PLATFORMNAME_STR = platformname_str
        self.URL_START_STR = url_start_str
        self.database_filepath_str = bin.logic.filesystem.get_database_sqlite_filepath_fc(self.PLATFORMNAME_STR)
        self.results_filepath_str = bin.logic.filesystem.get_results_filepath_fc(self.PLATFORMNAME_STR, ".json")
        self.results_filename_str = bin.logic.filesystem.get_filenamefrompath(self.results_filepath_str)
        self.backuped_original_results_filename_str = self.results_filename_str
        self.current_timestamp_str = settings.get_timestamp_current_str_fc()

    def update_results_filepath_fc(self, pagenumber_int = None, filterslist_lst = None):
        suffix_str = ""
        if pagenumber_int:
            suffix_str += f"_{pagenumber_int}"
        if filterslist_lst:
            for i in filterslist_lst:
                if i:
                    suffix_str += f"_{i}"

        self.results_filename_str = bin.logic.filesystem.update_filename_with_suffix(self.backuped_original_results_filename_str, suffix_str)
        self.results_filepath_str = bin.logic.filesystem.update_filepath_with_suffix(self.results_filepath_str, suffix_str, self.backuped_original_results_filename_str)

    def _fetch_html(self, pagenumber_int = None) -> (str ,int):
        '''
        return: html_str, status_code_int
        '''
        if not pagenumber_int:
            return bin.logic.web.get_html_response_from_url(self.URL_START_STR, headers_dc=self.HEADERS)

        cookies = {

        }
        params = {
            'pn': f'{pagenumber_int}',
        }
        pause_seconds_int = random.randint(3, 7)
        print(f"OK: Technical pause between requests - {pause_seconds_int} seconds")
        time.sleep(pause_seconds_int)
        return bin.logic.web.get_html_response_from_url(self.URL_START_STR, headers_dc=self.HEADERS, params_dc=params, cookies_dc=cookies)

    def parse(self, pagenumber_int=0) -> None:
        '''dont return nothing, just write collected data into the database'''
        raise NotImplementedError("Subclasses must implement the 'parse' method")

    def update_coordinates(self) -> None:
        raise NotImplementedError("Subclasses must implement the 'update_coordinates' method")