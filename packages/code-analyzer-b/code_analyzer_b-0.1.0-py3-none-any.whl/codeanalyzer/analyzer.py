from tqdm import tqdm
from .deepseek import DeepSeekClient
from .utils import read_file


class CodeAnalyzer:
    def __init__(self):
        self.client = DeepSeekClient()
        self.findings = []

    def analyze_file(self, file_path):
        try:
            code = read_file(file_path)
            result = self.client.analyze_code(code)
            if "no issues" not in result.lower():
                self.findings.append({
                    "file": file_path,
                    "result": result
                })
        except Exception as e:
            pass

    def analyze_project(self, file_list):
        with tqdm(
                total=len(file_list),
                desc="Analyzing Files",
                unit="file",
                bar_format="{l_bar}{bar:20}| {n_fmt}/{total_fmt} [{elapsed}]"
        ) as pbar:
            for file_path in file_list:
                self.analyze_file(file_path)
                pbar.update(1)

    def generate_report(self):
        findings_text = "\n\n".join(
            [f"File: {f['file']}\nFindings: {f['result']}" for f in self.findings]
        )

        print("\nGenerating Summary:")
        full_summary = []
        stream = self.client.generate_summary_streaming(findings_text)
        for chunk in stream:
            full_summary.append(chunk)
            print(chunk, end='', flush=True)
        print("\n")

        return {
            "summary": ''.join(full_summary),
            "detailed_findings": self.findings
        }