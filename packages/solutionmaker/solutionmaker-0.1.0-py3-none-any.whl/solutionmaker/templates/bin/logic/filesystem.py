import json
import os
from bin.settings.settings import PROJECT_TITLE, RESULTS_DIR

def save_append_dictionary_into_json_file_fc(save_filepath_str, jobs_dc):
    if os.path.isfile(save_filepath_str):

        with open(save_filepath_str, "r", encoding="utf-8") as fr:
            try:
                data = json.load(fr)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append data to json
    data.append(jobs_dc)

    with open(save_filepath_str, "w", encoding="utf-8") as fw:
        json.dump(data, fw, ensure_ascii=False, indent=4)

def update_filename_with_suffix(filename_str, suffix_str):
    '''
    file1.txt -> file1_suffix1.txt
    '''
    if not suffix_str:
        return filename_str
    filename_base, filename_ext = os.path.splitext(filename_str)
    new_filename_str = f"{filename_base}{suffix_str}{filename_ext}"
    return new_filename_str


def update_filepath_with_suffix(filepath_str, suffix_str, to_update_old_filename_str = None):
    '''
    C:\folder1\file1.txt -> C:\folder1\file1_suffix1.txt
    '''
    if not suffix_str:
        if to_update_old_filename_str:
            # C:\folder1\file1.txt -> C:\folder1\newfilename1.txt
            return os.path.join(os.path.dirname(filepath_str), to_update_old_filename_str)
        else:
            # C:\folder1\file1.txt -> C:\folder1\file1.txt
            return filepath_str

    if not to_update_old_filename_str:
        # file1.txt -> newfilename1_suffix1.txt
        filename_str = os.path.basename(filepath_str)
        new_filename_str = update_filename_with_suffix(filename_str, suffix_str)
    else:
        # file1.txt -> file1_suffix1.txt
        new_filename_str = update_filename_with_suffix(to_update_old_filename_str, suffix_str)
    return os.path.join(os.path.dirname(filepath_str), new_filename_str)

def get_filenamefrompath_fc(path_str):
    return os.path.basename(path_str)

# functions for handling local filepaths
def make_filetitle_fc(somevalue_for_name = None):
    if not somevalue_for_name:
        return f"{PROJECT_TITLE}"
    return f"{PROJECT_TITLE}_{somevalue_for_name}"

def get_filename_fc(somevalue_for_name, extension_filename = ".sqlite"):
    if extension_filename.startswith("."):
        return make_filetitle_fc(somevalue_for_name) + extension_filename
    return f"{make_filetitle_fc(somevalue_for_name)}.{extension_filename}"

def get_results_filepath_fc(specifictitle_marker_str, extension_filename):
    return os.path.join(RESULTS_DIR, get_filename_fc(specifictitle_marker_str, extension_filename))


def get_database_sqlite_filename_fc(somevalue_for_name):
    return get_filename_fc(make_filetitle_fc(f"{somevalue_for_name}"), ".sqlite")

def get_results_html_filename_fc(somevalue_for_name):
    return get_filename_fc(make_filetitle_fc(f"{somevalue_for_name}"), ".html")

def get_database_sqlite_filepath_fc(specifictitle_marker_str):
    return os.path.join(RESULTS_DIR, get_database_sqlite_filename_fc(specifictitle_marker_str))

def get_results_html_filepath_fc(specifictitle_marker_str):
    return os.path.join(RESULTS_DIR, get_results_html_filename_fc(specifictitle_marker_str))