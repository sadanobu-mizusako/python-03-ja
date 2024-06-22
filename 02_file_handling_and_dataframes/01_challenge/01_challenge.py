import os
import re
import json
import shutil
from pathlib import Path

CURRENT_DIRECTORY = os.getcwd()
FILE_DIRECTORY = CURRENT_DIRECTORY +"/data/text_files/"

def get_files(filetype):
    """
    filetype: "book" or "chapter"
    """
    files = os.listdir(FILE_DIRECTORY)
    if filetype=="book":
        files = [f for f in files if not re.match("Chapter_\d+.txt", f)]
    elif filetype=="chapter":
        files = [f for f in files if re.match("Chapter_\d+.txt", f)]
    else:
        raise Exception("filetype must be book or chapter!")
    
    return files

def script1():
    """
    書籍の名前が付いたすべてのファイルをPythonの辞書にインポートし、それを1つのテキストファイルに保存します。
    Chapter_x.txt という名前のファイルは含めない。
    """
    # ファイル一覧を取得 
    files_book = get_files("book")

    # bookファイルの読み込み
    res = {}
    for file in files_book:
        with open(FILE_DIRECTORY+file, "r") as f:
            text = f.read()
            res[file[:-4]] = text

    # テキストファイルに保存する
    with open(CURRENT_DIRECTORY +'/data/book.txt','w') as f:
        txt = json.dumps(res)
        f.write(txt)

def script2():
    # file一覧を取得
    files_chapter = get_files("chapter")

    # libraryフォルダを作成
    lib_dir = CURRENT_DIRECTORY +"/data/library/"
    if not os.path.exists(lib_dir):
        os.makedirs(lib_dir)
    # libraryフォルダにChapter_*.txtを保存
    for file in files_chapter:
        shutil.copy(FILE_DIRECTORY + file, lib_dir + file)
    # pathlib を使用してこのディレクトリに移動し、すべてのファイルとサイズを一覧表示
    for file in files_chapter:
        print(file ,":", Path(lib_dir + file).stat().st_size)

if __name__=="__main__":
    script1()
    script2()