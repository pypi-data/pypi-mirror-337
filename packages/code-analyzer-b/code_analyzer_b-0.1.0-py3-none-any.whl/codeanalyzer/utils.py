import os
import tempfile
import zipfile
import io
import requests
from tqdm import tqdm
from codeanalyzer.config import Config


def download_repo(github_url):
    temp_dir = tempfile.mkdtemp(prefix="code_analyzer_")

    # Try both main and master branches
    branches = ['main', 'master']
    for branch in branches:
        zip_url = f"{github_url}/archive/refs/heads/{branch}.zip"
        response = requests.get(zip_url, stream=True)
        if response.status_code == 200:
            break
    else:
        raise ValueError("Failed to download repository: branch not found")

    total_size = int(response.headers.get('content-length', 0))

    with tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            desc="Downloading Repository",
            bar_format="{desc}: {percentage:3.0f}%|{bar:20}| {n_fmt}/{total_fmt}",
            ascii="->="
    ) as progress_bar:
        zip_content = io.BytesIO()
        for data in response.iter_content(chunk_size=1024):
            zip_content.write(data)
            progress_bar.update(len(data))

    with zipfile.ZipFile(zip_content) as zip_ref:
        zip_ref.extractall(temp_dir)

    extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
    return extracted_dir


def scan_files(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) > Config.MAX_FILE_SIZE:
                continue
            ext = os.path.splitext(file_path)[1]
            if ext.lower() in Config.SUPPORTED_EXTENSIONS:
                file_list.append(file_path)
    return file_list


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()