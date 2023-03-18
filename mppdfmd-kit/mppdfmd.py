# mppdfmd.py
# ver 1.0

import os
import glob
import shutil
import yaml
import io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')
sys.stderr = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')

# _MDフォルダの中にimagesというフォルダを作成する、既に存在している場合削除し作り直す。
MD_DIR = "_MD\\"
IMAGES_DIR = "images"
DEST_IMAGES_DIR = MD_DIR + IMAGES_DIR
if os.path.exists(DEST_IMAGES_DIR):
    shutil.rmtree(DEST_IMAGES_DIR)
os.mkdir(DEST_IMAGES_DIR)

CURRENT_DIR = os.getcwd()

# imagesフォルダのパスを再帰的に取得し、フォルダの中身を_MD/imagesフォルダにコピー
for folder in glob.glob("**/images", recursive=True):
    if (folder == DEST_IMAGES_DIR):
        continue
    list_file_name = os.listdir(folder)
    for i_file_name in list_file_name:
        join_name = os.path.join(CURRENT_DIR, folder, i_file_name)
        DEST_IMAGES_PATH = os.path.join(CURRENT_DIR, DEST_IMAGES_DIR)
        if os.path.isfile(join_name):
            shutil.copy(join_name, DEST_IMAGES_PATH)
        else:
            shutil.copytree(join_name, os.path.join(DEST_IMAGES_PATH, i_file_name))

# yamlファイルを読み込み、Markdownファイルの結合に必要な情報を取得
CONFIG_YAML = "mppdfmd-config.yaml"
with open(CONFIG_YAML, encoding="utf-8") as f:
    filenames = yaml.load(f, Loader=yaml.FullLoader)
md_files = filenames["md-files"]
merged_file_name = MD_DIR + filenames["merged-file-name"]


print("--- Selected Markdown files -----------------")
print(md_files)
print("\n")

# Markdownファイルの中身を順に結合する、その際ファイル間には改ページタグを挿入する
with open(merged_file_name, "w", encoding="utf-8") as merged_file:
    for mdfile in md_files:
        with open(mdfile, encoding="utf-8") as read_file:
            merged_file.write(read_file.read())
            if mdfile != md_files[-1]:
                merged_file.write("\n\n")
                merged_file.write("<div style=\"page-break-before: always;\"></div>")
                merged_file.write("\n\n")

print("--- Merged Markdown file ------------------")
print(merged_file_name)
print("\n")

# Markdownファイルの結合はここまで、これ以降は以下に掲示された順番に編集作業やコマンドの実行を行う
# 本プログラムでは、後続で実行するコマンドはコピペで実行可能なものが表示されるようにしている

# 結合したMarkdownファイルを開き、目次を生成する
# 方法：手動：VS Codeのプラグインの機能 「Markdown All in One:（目次）の作成」 を使用する
print("----------------------------------")
print("Generate Table of Contents by VS Code: Manual operation")
print("----------------------------------")
print("Please use the VS Code plugin 'Markdown All in One: create ToC' to add a table of contents.")
print("\n")

# MD to HTML に変換する
# 定数
HTML_DIR = "_HTML/"
translated_html = HTML_DIR + (filenames["merged-file-name"].rsplit(".",1))[0] + ".html"
# 方法：下記コマンドを実行（コピペ可能）
print("----------------------------------")
print("Markdown to HTML : use the follow command")
print("----------------------------------")
print("pandoc %s --to html5 --resource-path %s --embed-resources --standalone --css _HTML/github-markdown-light-custom4pdf.css --output %s" % (merged_file_name.replace('\\', '\\\\'), MD_DIR.replace('\\', '\\\\'), translated_html))
print("\n")

# 画面デザインを適用する<div class="markdown-body">の閉じタグを追加する
# 方法：下記コマンドを実行（コピペ可能）
print("----------------------------------")
print("Refactaring HTML : add close tag </div> before </body> : use the follow command")
print("----------------------------------")
print("sed -i -z 's/<\/body>\\n<\/html>/<\/div>\\n<\/body>\\n<\/html>/g' %s" % (translated_html))
print("\n")

# HTML to PDF に変換する
# 定数
PDF_DIR = "_PDF/"
translated_pdf = PDF_DIR + (filenames["merged-file-name"].rsplit(".",1))[0] + ".pdf"
copyright_text = filenames["copyright"]
# 方法：下記コマンドを実行（コピペ可能）
print("----------------------------------")
print("HTML to PDF : use the follow command")
print("----------------------------------")
print("wkhtmltopdf --footer-left '%s' --footer-right '[page]/[topage]' %s %s" % (copyright_text, translated_html, translated_pdf))
