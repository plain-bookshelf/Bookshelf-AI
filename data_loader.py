import pandas as pd

def load_and_preprocess_data(csv_path="bookshelf_novels.csv"):
    data = pd.read_csv(csv_path)

    data['description'] = data['description'].fillna('')
    data['pubDate'] = data['pubDate'].fillna('')
    data['img'] = data['img'].fillna('')
    data['catgory'] = data['catgory'].fillna('')

    # 불필요 문자 제거
    data['description'] = data['description'].str.replace('[^가-힣a-zA-Z0-9 ]', '', regex=True)

    # 이미지 기준 중복 제거
    data = data.drop_duplicates(subset=['img']).reset_index(drop=True)

    return data


def extract_genres(data):
    genre_list = []
    for cat in data['catgory']:
        seen = set()
        split_genres = sum([g.split('>') for g in cat.split('/')], [])
        genre_list.append([g for g in split_genres if not (g in seen or seen.add(g))])
    return genre_list


def extract_authors(data):
    return [author.split() for author in data['writer'].to_list()]
