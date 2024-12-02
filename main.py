import streamlit as st
import json
from utils import process_group_data

st.title('TT案作成サイト')

# 初期化
if "groups" not in st.session_state:
    st.session_state.groups = []  # グループを格納するリスト

def add_group():
    """新しいグループ（6つの入力）を追加"""
    st.session_state.groups.append([""] * 6)

# JSONファイルを読み込む関数
def load_json_file(file):
    """アップロードされたJSONファイルを読み込み、入力フォームに反映"""
    try:
        data = json.load(file)
        if isinstance(data, list) and all(isinstance(group, list) and len(group) == 6 for group in data):
            st.session_state.groups = data
            st.success("JSONファイルを正常に読み込みました！")
        else:
            st.error("JSONファイルの形式が正しくありません。")
    except Exception as e:
        st.error(f"ファイルの読み込みに失敗しました: {e}")

# JSONファイルのアップロード
uploaded_file = st.file_uploader("既存のJSONファイルをアップロード", type=["json"])
if uploaded_file is not None:
    load_json_file(uploaded_file)
# 初期状態で1つのグループを追加
if len(st.session_state.groups) == 0:
    add_group()

# 各グループの入力を横一列に並べて表示
for group_index, group in enumerate(st.session_state.groups):
    st.subheader(f"工程 {group_index + 1}")

    # 6つのカラムを作成
    cols = st.columns(6)

    all_filled = True  # 現在のグループが全て埋まっているかのフラグ

    for input_index, col in enumerate(cols):
        with col:
            key = f"group_{group_index}_input_{input_index}"
            match input_index:
                case 0:
                    sentence = "場所"
                case 1:
                    sentence = "情報"
                case 2:
                    sentence = "km"
                case 3:
                    sentence = "up"
                case 4:
                    sentence = "down"
                case 5:
                    sentence = "時間"
            user_input = st.text_input(
                f"{input_index + 1}.{sentence}",
                value=group[input_index],
                key=key
            )
            st.session_state.groups[group_index][input_index] = user_input

            # 空の入力欄がある場合、フラグをFalseにする
            if not user_input.strip():
                all_filled = False

    # 現在のグループが全て埋まっており、最後のグループなら新しいグループを追加
    if all_filled and group_index == len(st.session_state.groups) - 1:
        add_group()

if st.button("出力"):
    results = process_group_data(st.session_state.groups)
    st.write(results)
    st.write("TT案")
    st.write(results)

# 入力内容を確認
if st.button("入力内容を確認"):
    st.write("全グループの入力内容:")
    st.write(st.session_state.groups)

# ユーザーがダウンロード可能なJSONデータを作成
json_data = json.dumps(st.session_state.groups, ensure_ascii=False, indent=4)
st.download_button(
    label="JSONファイルをダウンロード",
    data=json_data,
    file_name="groups.json",
    mime="application/json"
)