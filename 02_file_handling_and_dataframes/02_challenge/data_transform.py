import csv
import json
import os
import re

import logging
logging.basicConfig(level=logging.WARNING)

def read_csv(file_path):
    """
    CSVファイルを読み取り、その内容を辞書のリストで返す

    :引数 file_path: 文字列 - CSVファイルへのパス
    :戻り値: リスト - CSVの列を表す辞書のリスト
    """
    with open(file_path) as f:
        reader = csv.reader(f)
        reader = list(reader)
        header = reader[0]
        res = [{h:elm for h, elm in zip(header, row)} for row in reader[1:]]
        logging.info(f"open csv file: {res}")
        return res

def csv_to_json(csv_data):
    """
    CSVデータ (辞書のリスト) を受け取り、それをJSON形式 (文字列) に変換する

    :引数 csv_data: リスト - 辞書のリストで表したCSVデータ
    :戻り値: 文字列 - JSON形式で表したデータ
    """
    return json.dumps(csv_data)

def write_json(json_data, file_path):
    """
    JSONデータをファイルに書き込む

    :param json_data: 文字列 - 書き込むJSONデータ
    :param file_path: 文字列 - JSONファイルへのパス
    """
    with open(file_path, 'w') as f:
        json.dump(json_data, f, indent=3)

def read_json(file_path):
    """
    JSONファイルを読み取ってその内容を返す

    :引数 file_path: 文字列 - JSONファイルへのパス
    :戻り値: JSONファイルの内容 (リスト型)
    """
    with open(file_path, 'r') as f:
        json_data = json.load(f)
        # json_data = f.read()
        logging.info(f"open json file: {json_data}")
    
    return json_data

def json_to_csv(json_data):
    """
    JSONデータを受け取り (通常は辞書のリスト)、それをCSV形式 (文字列) に変換する

    :引数 json_data: JSONデータ
    :戻り値: 文字列 - CSV形式で表したデータ
    """
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    csv_data = ""
    count = 0
    for row in json_data:
        if count == 0:
            header = row.keys()
            csv_data += ", ".join(header)
            csv_data += "\n"
            count += 1
        row_value = row.values()
        row_value = [str(v) for v in row_value]
        csv_data += ", ".join(row_value)
        csv_data += "\n"
    return csv_data

def write_csv(csv_data, file_path):
    """
    CSVデータをファイルに書き込む

    :引数 csv_data: 文字列 - 書き込むCSVデータ
    :引数 file_path: 文字列 - CSVファイルへのパス
    """
    with open(file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

def validate_data(data, data_type):
    """
    データの整合性を確認する (例: CSVの列数に一貫性があること)

    :引数 data: 検証対象のデータ
    :引数 data_type: 文字列 - データ型 ('CSV' または 'JSON')
    :戻り値: bool - データが有効な場合はTrue、無効な場合はFalse
    """
    if data_type=="CSV":
        # 列数の一貫性
        # data_sep = data.split("\n")
        for i, row in enumerate(data):
            if i==0:
                # col_cnt_header = len(row.split(","))
                col_cnt_header = len(row)
            else:
                # col_cnt = len(row.split(","))
                col_cnt = len(row)
                if col_cnt_header!=col_cnt:
                    return False
                
    elif data_type=="JSON":
        # キーの一貫性
        if isinstance(data, str):
            data = json.loads(data)
        for i, row in enumerate(data):
            # print(row, type(row))
            if i==0:
                key = sorted(row.keys())
            else:
                if key!=sorted(row.keys()):
                    return False
    
    else:
        raise Exception("data_type must be CSV or JSON")
                    
    return True
def process_directory(directory_path):
    """
    指定されたディレクトリにあるすべてのCSVまたはJSONファイルを確認し、適切に変換する

    :引数 directory_path: 文字列 - 処理対象のディレクトリへのパス
    """
    files = os.listdir(directory_path)
    logging.info(f"found {len(files)} files: {files}")
    csv_files = [f for f in files if re.match("\w+.csv", f)]
    json_files = [f for f in files if re.match("\w+.json", f)]
    logging.info(f"csv file: {csv_files}")
    logging.info(f"json file: {json_files}")

    # csv処理 (csv -> json)
    for file in csv_files:
        csv_data = read_csv(directory_path+file)
        if not validate_data(csv_data, "CSV"):
            logging.warning(f"invalid data structure: {csv_data}")
        else:
            logging.info(f"valid csv data: {csv_data}")
        json_data = csv_to_json(csv_data)

        if not validate_data(json_data, "JSON"):
            logging.warning(f"invalid data structure {json_data}")
        else:
            logging.info(f"valid json data: {json_data}")

        logging.info("completed csv process")

    # json処理（json -> csv）
    for file in json_files:
        json_data = read_json(directory_path+file)
        # print(type(json_data))
        if not validate_data(json_data, "JSON"):
            logging.warning("invalid data structure")
        else:
            logging.info("valid data structure")

        csv_data = json_to_csv(json_data)
        logging.info(f"converted json to cev: {csv_data}")
        if not validate_data(csv_data, "CSV"):
            logging.warning("invalid data structure")
        else:
            logging.info("valid data structure")

# スクリプトを実行するmain関数
def main():
    # 使用例
    try:
        directory = os.getcwd() + "\\"
        process_directory(directory)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()