import argparse
import sys
import os
import shutil
import configparser
from .utils import download_repo, scan_files
from .analyzer import CodeAnalyzer


def setup_command(args):
    print("Initializing code analyzer setup...")
    api_key = input("Please enter your DeepSeek API key: ").strip()
    if not api_key:
        print("Error: API key cannot be empty.")
        sys.exit(1)

    config_dir = os.path.expanduser("~/.code_analyzer")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.ini")

    config = configparser.ConfigParser()
    config["DEEPSEEK"] = {"API_KEY": api_key}

    with open(config_path, "w") as f:
        config.write(f)

    print(f"Setup complete. API key saved to {config_path}")


def analyze_command(args):
    print(f"\n🔍 Starting analysis of {args.github_url}")
    repo_path = None
    try:
        repo_path = download_repo(args.github_url)
        files = scan_files(repo_path)
        print(f"📁 Found {len(files)} files to analyze")

        analyzer = CodeAnalyzer()
        analyzer.analyze_project(files)
        report = analyzer.generate_report()

        print("\n📝 Final Summary:")
        print("=" * 80)
        print(report['summary'])

        if report['detailed_findings']:
            print("\n🔍 Detailed Findings:")
            for finding in report['detailed_findings']:
                print(f"\nFile: {finding['file']}")
                print("-" * 80)
                print(finding['result'])
        else:
            print("\n✅ No significant issues found")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    finally:
        if repo_path and os.path.exists(os.path.dirname(repo_path)):
            shutil.rmtree(os.path.dirname(repo_path))


def main():
    parser = argparse.ArgumentParser(prog="code_analyzer")
    subparsers = parser.add_subparsers()

    setup_parser = subparsers.add_parser('setup', help='Initial setup')
    setup_parser.set_defaults(func=setup_command)

    analyze_parser = subparsers.add_parser('analyze', help='Analyze a repository')
    analyze_parser.add_argument('github_url', help='GitHub repository URL')
    analyze_parser.set_defaults(func=analyze_command)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()