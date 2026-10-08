# セット

# まず、Google ColabとGoogle Driveを接続します。以下のコードを使用します。
from google.colab import drive

drive.mount('/content/drive')

import os

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'

# フォルダが存在することを確認します
if os.path.exists(folder_path):
    files = os.listdir(folder_path)

    for file_name in files:
        print(file_name)
else:
    print(f"The folder does not exist: {folder_path}")

from PIL import Image
import numpy as np

# 画像を読み込む
img1 = Image.open('/content/drive/MyDrive/Colab Notebooks/test/2/17-KC.png')
img2 = Image.open('/content/drive/MyDrive/Colab Notebooks/test/2/18-FF.png')

# 画像をnumpy配列に変換
img1_arr = np.array(img1)
img2_arr = np.array(img2)

# 画像の差分を計算
diff_arr = img1_arr - img2_arr

# 差分がある箇所を抽出（差分が0より大きい場所）
diff_points = np.where(diff_arr > 0)

# 差分がある場所の数を表示
print(len(diff_points[0]))

import matplotlib.pyplot as plt

# 画像を読み込む
img1 = Image.open('/content/drive/MyDrive/Colab Notebooks/test/2/17-KC.png')
img2 = Image.open('/content/drive/MyDrive/Colab Notebooks/test/2/18-FF.png')

# 画像をnumpy配列に変換
img1_arr = np.array(img1)
img2_arr = np.array(img2)

# RGBAの各チャンネルの差分を計算
diff_arr = np.abs(img1_arr - img2_arr)

# 差分がある箇所を抽出（差分が0より大きい場所）
# 全てのチャンネルについて差分が0より大きい場所を抽出
diff_points = np.where(np.any(diff_arr > 0, axis=-1))

# 差分を視覚化するための空の画像を作成（透明度のためのアルファチャンネルも含む）
diff_img = np.zeros_like(img1_arr)

# 差分がある箇所を白色（255, 255, 255, 255）で塗りつぶす
diff_img[diff_points] = [255, 255, 255, 255]

# 差分画像を表示
plt.imshow(diff_img)
plt.show()

# 画像を読み込む
img1 = Image.open('/content/drive/MyDrive/Colab Notebooks/test/2/17-KC.png').convert('RGBA')
img2 = Image.open('/content/drive/MyDrive/Colab Notebooks/test/2/18-FF.png').convert('RGBA')

# 画像をnumpy配列に変換
img1_arr = np.array(img1)
img2_arr = np.array(img2)

# RGBAの各チャンネルの差分を計算
diff_arr = np.abs(img1_arr - img2_arr)

# 差分がある箇所を抽出（差分が0より大きい場所）
# 全てのチャンネルについて差分が0より大きい場所を抽出
diff_points = np.where(np.any(diff_arr > 0, axis=-1))

# 差分を視覚化するための空の画像を作成（透明度のためのアルファチャンネルも含む）
diff_img = np.zeros_like(img1_arr)

# 差分がある箇所を赤色（255, 0, 0, 255）で塗りつぶす
diff_img[diff_points] = [255, 0, 0, 255]

# 差分画像をPILのImageオブジェクトに変換
diff_img_pil = Image.fromarray(diff_img)

# 元の画像と差分画像を合成
composite = Image.alpha_composite(img1, diff_img_pil)

# 合成画像を表示
plt.imshow(composite)
plt.show()

def transparent_background(image, lower_green, upper_green):
    """
    画像の背景を透明にする関数

    Parameters
    ----------
    image: PIL.Image
        入力画像（RGBA）
    lower_green: array_like
        緑色の下限（[R, G, B]）
    upper_green: array_like
        緑色の上限（[R, G, B]）

    Returns
    -------
    image: PIL.Image
        背景が透明化された画像
    """
    # 画像をnumpy配列に変換
    img_arr = np.array(image)

    # RGBの各チャンネルの値が指定の緑色の範囲内（背景と判定）の箇所を抽出
    bg_points = np.where(((img_arr[:, :, :3] >= lower_green) & (img_arr[:, :, :3] <= upper_green)).all(axis=-1))

    # 背景と判定された箇所を透明（0, 0, 0, 0）にする
    img_arr[bg_points] = [0, 0, 0, 0]

    # numpy配列をPILのImageオブジェクトに戻す
    return Image.fromarray(img_arr)

# 画像を読み込みRGBAに変換
img1 = Image.open('/content/drive/MyDrive/Colab Notebooks/test/2/17-KC.png').convert('RGBA')
img2 = Image.open('/content/drive/MyDrive/Colab Notebooks/test/2/18-FF.png').convert('RGBA')

# 背景色の緑色の範囲を定義
lower_green = np.array([0, 120, 0])  # このRGB値以上を背景色と判定
upper_green = np.array([150, 255, 150])  # このRGB値以下を背景色と判定

# 背景を透明化
img1_trans = transparent_background(img1, lower_green, upper_green)
img2_trans = transparent_background(img2, lower_green, upper_green)

# （以降、img1_transとimg2_transを用いて差分の計算と表示を行う）

# 画像をnumpy配列に変換
img1_trans_arr = np.array(img1_trans)
img2_trans_arr = np.array(img2_trans)

# RGBAの各チャンネルの差分を計算
diff_trans_arr = np.abs(img1_trans_arr - img2_trans_arr)

# 差分がある箇所を抽出（差分が0より大きい場所）
# 全てのチャンネルについて差分が0より大きい場所を抽出
diff_points = np.where(np.any(diff_trans_arr > 0, axis=-1))

# 差分を視覚化するための空の画像を作成（透明度のためのアルファチャンネルも含む）
diff_img = np.zeros_like(img1_trans_arr)

# 差分がある箇所を赤色（255, 0, 0, 255）で塗りつぶす
diff_img[diff_points] = [255, 0, 0, 255]

# 差分画像をPILのImageオブジェクトに変換
diff_img_pil = Image.fromarray(diff_img)

# 元の画像（背景透明化済み）と差分画像を合成
composite = Image.alpha_composite(img1_trans, diff_img_pil)

# 合成画像を表示
plt.imshow(composite)
plt.show()

from PIL import ImageChops

# 画像の差分を取得
diff = ImageChops.difference(img1_trans, img2_trans)

# 差分画像をNumpy配列に変換
diff_arr = np.array(diff)

# RGBの各チャンネルで差の絶対値が一定のしきい値（ここでは250）を超えるピクセルを抽出
threshold = 250
extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))

# 強調したい箇所を赤色（255, 0, 0, 255）で塗りつぶす
highlight_img_arr = np.zeros_like(img1_trans_arr)
highlight_img_arr[extreme_points] = [255, 0, 0, 255]

# 強調画像をPILのImageオブジェクトに変換
highlight_img_pil = Image.fromarray(highlight_img_arr)

# 元の画像（背景透明化済み）と強調画像を合成
highlight_composite = Image.alpha_composite(img1_trans, highlight_img_pil)

# 合成画像を表示
plt.imshow(highlight_composite)
plt.show()

import matplotlib.patches as patches
from sklearn.cluster import KMeans

# クラスタの数（エリアの数）を設定
n_clusters = 5

# 差分が大きいピクセルの位置を取得
extreme_points_array = np.array(extreme_points).transpose()

# K-means クラスタリングを適用
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(extreme_points_array)

# 各クラスタの中心を取得
centers = kmeans.cluster_centers_

# 描画用の新しいfigとaxを作成
fig, ax = plt.subplots(1)

# 画像を表示
ax.imshow(highlight_composite)

extreme_radius = 20  # 半径を設定

# 各クラスタの中心に円を描画
for center in centers:
    circle = patches.Circle((center[1], center[0]), extreme_radius, edgecolor='blue', facecolor='none', linewidth=2)
    ax.add_patch(circle)

# 描画
plt.show()

# 描画用の新しいfigとaxを作成
fig, ax = plt.subplots(1)

# 画像を表示
ax.imshow(highlight_composite)

# 各クラスタの中心に小さな円を描画
circle_radius = 20  # 円の半径を20ピクセルに設定
for center in centers:
    circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
    ax.add_patch(circle)

# 描画
plt.show()

import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib import patches

def transparent_background(image, lower_green, upper_green):
    img = image.copy()
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] in list(range(lower_green[0], upper_green[0])) and item[1] in list(range(lower_green[1], upper_green[1])) and item[2] in list(range(lower_green[2], upper_green[2])):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'

# 緑色の範囲（RGB）を定義
lower_green = (0, 120, 0)
upper_green = (100, 255, 100)

# クラスタ数を定義（ここでは4とします）
n_clusters = 4

# 小さな円の半径を定義
circle_radius = 20

# フォルダ内のファイル名を取得
file_names = os.listdir(folder_path)

# 画像ファイルの拡張子
valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]

for file_name in file_names:
    # ファイル名が有効な拡張子を持っているかどうかを確認
    if not any(file_name.endswith(ext) for ext in valid_extensions):
        continue

    img_path = os.path.join(folder_path, file_name)


    # 画像読み込み
    img = Image.open(img_path).convert('RGBA')

    # 背景透明化
    img_trans = transparent_background(img, lower_green, upper_green)

    # 背景透明化された画像をNumpy配列に変換
    img_trans_arr = np.array(img_trans)

    # 前の画像との差分を取得
    diff = ImageChops.difference(img_trans, img_trans_prev) if 'img_trans_prev' in locals() else img_trans

    # 差分画像をNumpy配列に変換
    diff_arr = np.array(diff)

    # RGBの各チャンネルで差の絶対値が一定のしきい値（ここでは250）を超えるピクセルを抽出
    threshold = 250
    extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))

    # クラスタリングを適用
    extreme_points_array = np.array(extreme_points).transpose()

    if extreme_points_array.shape[0] > 0:  # 追加された条件チェック
        n_clusters_adj = min(n_clusters, extreme_points_array.shape[0])  # 調整されたn_clusters
        kmeans = KMeans(n_clusters=n_clusters_adj)
        kmeans.fit(extreme_points_array)
        centers = kmeans.cluster_centers_

        # 強調画像の作成
        highlight_img_arr = np.zeros_like(img_trans_arr)
        highlight_img_arr[extreme_points] = [255, 0, 0, 255]
        highlight_img_pil = Image.fromarray(highlight_img_arr)
        highlight_composite = Image.alpha_composite(img_trans, highlight_img_pil)

        # 描画用の新しいfigとaxを作成
        fig, ax = plt.subplots(1)

        # 画像を表示
        ax.imshow(highlight_composite)

        # 各クラスタの中心に小さな円を描画
        for center in centers:
            circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
            ax.add_patch(circle)

        # 描画
        plt.show()

    else:
        print(f"No significant difference found in image {file_name}. Skipping...")

    # 次回の差分計算のために現在の画像を保存
    img_trans_prev = img_trans

# k-means変更

import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib import patches

def transparent_background(image, lower_green, upper_green):
    img = image.copy()
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] in list(range(lower_green[0], upper_green[0])) and item[1] in list(range(lower_green[1], upper_green[1])) and item[2] in list(range(lower_green[2], upper_green[2])):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'

# 緑色の範囲（RGB）を定義
lower_green = (0, 120, 0)
upper_green = (100, 255, 100)

# クラスタ数を定義（ここでは4とします）
n_clusters = 4

# 小さな円の半径を定義
circle_radius = 20


# フォルダ内のファイル名を取得
file_names = os.listdir(folder_path)

# 画像ファイルの拡張子
valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]

for file_name in file_names:
    # ファイル名が有効な拡張子を持っているかどうかを確認
    if not any(file_name.endswith(ext) for ext in valid_extensions):
        continue

    img_path = os.path.join(folder_path, file_name)

    # 画像読み込み
    img = Image.open(img_path).convert('RGBA')


    # 背景透明化
    img_trans = transparent_background(img, lower_green, upper_green)

    # 背景透明化された画像をNumpy配列に変換
    img_trans_arr = np.array(img_trans)

    # 前の画像との差分を取得
    diff = ImageChops.difference(img_trans, img_trans_prev) if 'img_trans_prev' in locals() else img_trans

    # 差分画像をNumpy配列に変換
    diff_arr = np.array(diff)

    # RGBの各チャンネルで差の絶対値が一定のしきい値（ここでは250）を超えるピクセルを抽出
    threshold = 250
    extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))

    # クラスタリングを適用
    extreme_points_array = np.array(extreme_points).transpose()

    if extreme_points_array.shape[0] > 0:  # 追加された条件チェック
        n_clusters_adj = min(n_clusters, extreme_points_array.shape[0])  # 調整されたn_clusters
        kmeans = KMeans(n_clusters=n_clusters_adj, n_init=10)
        kmeans.fit(extreme_points_array)
        centers = kmeans.cluster_centers_

        # 強調画像の作成
        highlight_img_arr = np.zeros_like(img_trans_arr)
        highlight_img_arr[extreme_points] = [255, 0, 0, 255]
        highlight_img_pil = Image.fromarray(highlight_img_arr)
        highlight_composite = Image.alpha_composite(img_trans, highlight_img_pil)

        # 描画用の新しいfigとaxを作成
        fig, ax = plt.subplots(1)

        # 画像を表示
        ax.imshow(highlight_composite)

        # 各クラスタの中心に小さな円を描画
        for center in centers:
            circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
            ax.add_patch(circle)

        # 描画
        plt.show()

    else:
        print(f"No significant difference found in image {file_name}. Skipping...")

    # 次回の差分計算のために現在の画像を保存
    img_trans_prev = img_trans

# 各球種の最初のフレームとしてファストボール（FF）を選択し、その後の各球種との差異を確認します。

import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib import patches
from collections import defaultdict

def transparent_background(image, lower_green, upper_green):
    img = image.copy()
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] in list(range(lower_green[0], upper_green[0])) and item[1] in list(range(lower_green[1], upper_green[1])) and item[2] in list(range(lower_green[2], upper_green[2])):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'

# 緑色の範囲（RGB）を定義
lower_green = (0, 120, 0)
upper_green = (100, 255, 100)

# クラスタ数を定義（ここでは4とします）
n_clusters = 4

# 小さな円の半径を定義
circle_radius = 20

# フォルダ内のファイル名を取得
file_names = os.listdir(folder_path)

# ファーストボールのフレームを保存する辞書
first_frames = defaultdict(lambda: None)

# 画像ファイルの拡張子
valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]

for file_name in file_names:
    # ファイル名が有効な拡張子を持っているかどうかを確認
    if not any(file_name.endswith(ext) for ext in valid_extensions):
        continue

    img_path = os.path.join(folder_path, file_name)

    # 画像読み込み
    img = Image.open(img_path).convert('RGBA')

    # 背景透明化
    img_trans = transparent_background(img, lower_green, upper_green)

    # ファイル名から球種を取得
    pitch_type = file_name.split('-')[1].split('.')[0]

    if first_frames[pitch_type] is None:
        # この球種の最初のフレームを保存
        first_frames[pitch_type] = img_trans
    else:
        # 保存されているフレームと現在のフレームとの差分を計算
        diff = ImageChops.difference(img_trans, first_frames[pitch_type])

        # 差分画像をNumpy配列に変換
        diff_arr = np.array(diff)

        # RGBの各チャンネルで差の絶対値が一定のしきい値（ここでは250）を超えるピクセルを抽出
        threshold = 250
        extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))

        # クラスタリングを適用
        extreme_points_array = np.array(extreme_points).transpose()

        if extreme_points_array.shape[0] > 0:  # 追加された条件チェック
            n_clusters_adj = min(n_clusters, extreme_points_array.shape[0])  # 調整されたn_clusters
            kmeans = KMeans(n_clusters=n_clusters_adj, n_init=10)
            kmeans.fit(extreme_points_array)
            centers = kmeans.cluster_centers_

            # 強調画像の作成
            highlight_img_arr = np.zeros_like(img_trans_arr)
            highlight_img_arr[extreme_points] = [255, 0, 0, 255]
            highlight_img_pil = Image.fromarray(highlight_img_arr)
            highlight_composite = Image.alpha_composite(img_trans, highlight_img_pil)

            # 描画用の新しいfigとaxを作成
            fig, ax = plt.subplots(1)

            # 画像を表示
            ax.imshow(highlight_composite)

            # 各クラスタの中心に小さな円を描画
            for center in centers:
                circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
                ax.add_patch(circle)

            # 描画
            plt.show()

        else:
            print(f"No significant difference found in image {file_name}. Skipping...")

import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib import patches
from collections import defaultdict

def transparent_background(image, lower_green, upper_green):
    img = image.copy()
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] in list(range(lower_green[0], upper_green[0])) and item[1] in list(range(lower_green[1], upper_green[1])) and item[2] in list(range(lower_green[2], upper_green[2])):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'

# 緑色の範囲（RGB）を定義
lower_green = (0, 120, 0)
upper_green = (100, 255, 100)

# クラスタ数を定義（ここでは4とします）
n_clusters = 4

# 小さな円の半径を定義
circle_radius = 20

# フォルダ内のファイル名を取得
file_names = os.listdir(folder_path)

# ファーストボールのフレームを保存する辞書
first_frames = defaultdict(lambda: None)

for file_name in sorted(file_names):
    # Check if file is an image
    if not file_name.endswith(('.png', '.jpg', '.jpeg')):
        continue

    img_path = os.path.join(folder_path, file_name)

    # 画像読み込み
    img = Image.open(img_path).convert('RGBA')

    # 背景透明化
    img_trans = transparent_background(img, lower_green, upper_green)

    # ファイル名から球種を取得
    pitch_type = file_name.split('-')[1].split('.')[0]

    if first_frames[pitch_type] is None:
        # この球種の最初のフレームを保存
        first_frames[pitch_type] = img_trans
    else:
        # 保存されているフレームと現在のフレームとの差分を計算
        diff = ImageChops.difference(img_trans, first_frames[pitch_type])

        # 差分画像をNumpy配列に変換
        diff_arr = np.array(diff)

        # RGBの各チャンネルで差の絶対値が一定のしきい値（ここでは250）を超えるピクセルを抽出
        threshold = 250
        extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))

        # クラスタリングを適用
        extreme_points_array = np.array(extreme_points).transpose()

        if extreme_points_array.shape[0] > 0:  # 追加された条件チェック
            n_clusters_adj = min(n_clusters, extreme_points_array.shape[0])  # 調整されたn_clusters
            kmeans = KMeans(n_clusters=n_clusters_adj, n_init=10)
            kmeans.fit(extreme_points_array)
            centers = kmeans.cluster_centers_

            # 強調画像の作成
            highlight_img_arr = np.zeros_like(img_trans_arr)
            highlight_img_arr[extreme_points] = [255, 0, 0, 255]
            highlight_img_pil = Image.fromarray(highlight_img_arr)
            highlight_composite = Image.alpha_composite(img_trans, highlight_img_pil)

            # 描画用の新しいfigとaxを作成
            fig, ax = plt.subplots(1)

            # 画像のタイトルを追加
            plt.title(f"Image: {file_name}, Pitch type: {pitch_type}")

            # 画像を表示
            ax.imshow(highlight_composite)

            # 各クラスタの中心に小さな円を描画
            for center in centers:
                circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
                ax.add_patch(circle)

            # 描画
            plt.show()

        else:
            print(f"No significant difference found in image {file_name}. Skipping...")

import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib import patches
from collections import defaultdict

def transparent_background(image, lower_green, upper_green):
    img = image.copy()
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] in list(range(lower_green[0], upper_green[0])) and item[1] in list(range(lower_green[1], upper_green[1])) and item[2] in list(range(lower_green[2], upper_green[2])):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'

# 緑色の範囲（RGB）を定義
lower_green = (0, 120, 0)
upper_green = (100, 255, 100)

# クラスタ数を定義（ここでは4とします）
n_clusters = 4

# 小さな円の半径を定義
circle_radius = 20

# フォルダ内のファイル名を取得
file_names = os.listdir(folder_path)

# ファーストボールのフレームを保存する辞書
first_frames = defaultdict(lambda: None)

# 各ピッチタイプの画像を保存する辞書
images_per_pitch_type = defaultdict(list)

for file_name in sorted(file_names):
    # Check if file is an image
    if not file_name.endswith(('.png', '.jpg', '.jpeg')):
        continue

    img_path = os.path.join(folder_path, file_name)

    # 画像読み込み
    img = Image.open(img_path).convert('RGBA')

    # 背景透明化
    img_trans = transparent_background(img, lower_green, upper_green)

    # ファイル名から球種を取得
    pitch_type = file_name.split('-')[1].split('.')[0]

    if first_frames[pitch_type] is None:
        # この球種の最初のフレームを保存
        first_frames[pitch_type] = img_trans
    else:
        # 保存されているフレームと現在のフレームとの差分を計算
        diff = ImageChops.difference(img_trans, first_frames[pitch_type])

        # 差分画像をNumpy配列に変換
        diff_arr = np.array(diff)

        # RGBの各チャンネルで差の絶対値が一定のしきい値（ここでは250）を超えるピクセルを抽出
        threshold = 250
        extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))

        # クラスタリングを適用
        extreme_points_array = np.array(extreme_points).transpose()

        if extreme_points_array.shape[0] > 0:  # 追加された条件チェック
            n_clusters_adj = min(n_clusters, extreme_points_array.shape[0])  # 調整されたn_clusters
            kmeans = KMeans(n_clusters=n_clusters_adj, n_init=10)
            kmeans.fit(extreme_points_array)
            centers = kmeans.cluster_centers_

            # 強調画像の作成
            highlight_img_arr = np.zeros_like(img_trans_arr)
            highlight_img_arr[extreme_points] = [255, 0, 0, 255]
            highlight_img_pil = Image.fromarray(highlight_img_arr)
            highlight_composite = Image.alpha_composite(img_trans, highlight_img_pil)

            # ピッチタイプ毎に画像を保存
            images_per_pitch_type[pitch_type].append((highlight_composite, centers))

        else:
            print(f"No significant difference found in image {file_name}. Skipping...")

# 画像を表示
for pitch_type, images in images_per_pitch_type.items():
    fig, axs = plt.subplots(1, 4, figsize=(20, 5))
    fig.suptitle(f'Pitch type: {pitch_type}')

    for i, (highlight_composite, centers) in enumerate(images):
        if i < 4:  # 最初の4枚だけ表示
            axs[i].imshow(highlight_composite)

            # 各クラスタの中心に小さな円を描画
            for center in centers:
                circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
                axs[i].add_patch(circle)

import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib import patches
from collections import defaultdict

def transparent_background(image, lower_green, upper_green):
    img = image.copy()
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] in list(range(lower_green[0], upper_green[0])) and item[1] in list(range(lower_green[1], upper_green[1])) and item[2] in list(range(lower_green[2], upper_green[2])):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'
lower_green = (0, 120, 0)
upper_green = (100, 255, 100)
n_clusters = 4
circle_radius = 20
file_names = os.listdir(folder_path)
first_frames = defaultdict(lambda: None)
images_per_pitch_type = defaultdict(lambda: [])

for file_name in sorted(file_names):
    # Add this line to check file extension
    if not os.path.splitext(file_name)[1] in [".png", ".jpg", ".jpeg"]:
        continue

    img_path = os.path.join(folder_path, file_name)
    img = Image.open(img_path).convert('RGBA')

    img_trans = transparent_background(img, lower_green, upper_green)
    pitch_type = file_name.split('-')[1].split('.')[0]

    if first_frames[pitch_type] is None:
        first_frames[pitch_type] = img_trans
    else:
        diff = ImageChops.difference(img_trans, first_frames[pitch_type])
        diff_arr = np.array(diff)
        threshold = 250
        extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))

        extreme_points_array = np.array(extreme_points).transpose()

        if extreme_points_array.shape[0] > 0:
            n_clusters_adj = min(n_clusters, extreme_points_array.shape[0])
            kmeans = KMeans(n_clusters=n_clusters_adj, n_init=10)
            kmeans.fit(extreme_points_array)
            centers = kmeans.cluster_centers_

            highlight_img_arr = np.zeros_like(diff_arr)
            highlight_img_arr[extreme_points] = [255, 0, 0, 255]
            highlight_img_pil = Image.fromarray(highlight_img_arr)
            highlight_composite = Image.alpha_composite(img_trans, highlight_img_pil)

            images_per_pitch_type[pitch_type].append((highlight_composite, centers))

for pitch_type, images in images_per_pitch_type.items():
    n_rows = -(-len(images) // 4)

    for row in range(n_rows):
        fig, axs = plt.subplots(1, 4, figsize=(20, 5))
        fig.suptitle(f'Pitch type: {pitch_type}, Row: {row + 1}')

        for i in range(4):
            index = row * 4 + i
            if index < len(images):
                highlight_composite, centers = images[index]
                axs[i].imshow(highlight_composite)

                for center in centers:
                    circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
                    axs[i].add_patch(circle)
            else:
                axs[i].axis('off')

# 題名を追加

import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib import patches
from collections import defaultdict

def transparent_background(image, lower_green, upper_green):
    img = image.copy()
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] in list(range(lower_green[0], upper_green[0])) and item[1] in list(range(lower_green[1], upper_green[1])) and item[2] in list(range(lower_green[2], upper_green[2])):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'
lower_green = (0, 120, 0)
upper_green = (100, 255, 100)
n_clusters = 4
circle_radius = 20
file_names = os.listdir(folder_path)
first_frames = defaultdict(lambda: None)
images_per_pitch_type = defaultdict(lambda: [])

for file_name in sorted(file_names):
    if not os.path.splitext(file_name)[1] in [".png", ".jpg", ".jpeg"]:
        continue

    img_path = os.path.join(folder_path, file_name)
    img = Image.open(img_path).convert('RGBA')

    img_trans = transparent_background(img, lower_green, upper_green)
    pitch_type = file_name.split('-')[1].split('.')[0]

    if first_frames[pitch_type] is None:
        first_frames[pitch_type] = img_trans
    else:
        diff = ImageChops.difference(img_trans, first_frames[pitch_type])
        diff_arr = np.array(diff)
        threshold = 250
        extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))

        extreme_points_array = np.array(extreme_points).transpose()

        if extreme_points_array.shape[0] > 0:
            n_clusters_adj = min(n_clusters, extreme_points_array.shape[0])
            kmeans = KMeans(n_clusters=n_clusters_adj, n_init=10)
            kmeans.fit(extreme_points_array)
            centers = kmeans.cluster_centers_

            highlight_img_arr = np.zeros_like(diff_arr)
            highlight_img_arr[extreme_points] = [255, 0, 0, 255]
            highlight_img_pil = Image.fromarray(highlight_img_arr)
            highlight_composite = Image.alpha_composite(img_trans, highlight_img_pil)

            images_per_pitch_type[pitch_type].append((file_name, highlight_composite, centers))

for pitch_type, images in images_per_pitch_type.items():
    n_rows = -(-len(images) // 4)

    for row in range(n_rows):
        fig, axs = plt.subplots(1, 4, figsize=(20, 5))
        fig.suptitle(f'Pitch type: {pitch_type}, Row: {row + 1}')

        for i in range(4):
            index = row * 4 + i
            if index < len(images):
                file_name, highlight_composite, centers = images[index]
                axs[i].imshow(highlight_composite)
                axs[i].set_title(file_name)

                for center in centers:
                    circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
                    axs[i].add_patch(circle)
            else:
                axs[i].axis('off')

import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib import patches
from collections import defaultdict

def transparent_background(image, lower_green, upper_green):
    img = image.copy()
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] in list(range(lower_green[0], upper_green[0])) and item[1] in list(range(lower_green[1], upper_green[1])) and item[2] in list(range(lower_green[2], upper_green[2])):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'
lower_green = (0, 120, 0)
upper_green = (100, 255, 100)
n_clusters = 4
circle_radius = 20
file_names = os.listdir(folder_path)

# Open the reference image
reference_image_name = '18-FF.png'
reference_image_path = os.path.join(folder_path, reference_image_name)
reference_img = Image.open(reference_image_path).convert('RGBA')
reference_img_trans = transparent_background(reference_img, lower_green, upper_green)

images_per_pitch_type = defaultdict(lambda: [])

for file_name in sorted(file_names):
    if not os.path.splitext(file_name)[1] in [".png", ".jpg", ".jpeg"]:
        continue

    img_path = os.path.join(folder_path, file_name)
    img = Image.open(img_path).convert('RGBA')

    img_trans = transparent_background(img, lower_green, upper_green)
    pitch_type = file_name.split('-')[1].split('.')[0]

    # Compute the difference with the reference image
    diff = ImageChops.difference(img_trans, reference_img_trans)
    diff_arr = np.array(diff)
    threshold = 250
    extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))

    extreme_points_array = np.array(extreme_points).transpose()

    if extreme_points_array.shape[0] > 0:
        n_clusters_adj = min(n_clusters, extreme_points_array.shape[0])
        kmeans = KMeans(n_clusters=n_clusters_adj, n_init=10)
        kmeans.fit(extreme_points_array)
        centers = kmeans.cluster_centers_

        highlight_img_arr = np.zeros_like(diff_arr)
        highlight_img_arr[extreme_points] = [255, 0, 0, 255]
        highlight_img_pil = Image.fromarray(highlight_img_arr)
        highlight_composite = Image.alpha_composite(img_trans, highlight_img_pil)

        images_per_pitch_type[pitch_type].append((file_name, highlight_composite, centers))

for pitch_type, images in images_per_pitch_type.items():
    n_rows = -(-len(images) // 4)

    for row in range(n_rows):
        fig, axs = plt.subplots(1, 4, figsize=(20, 5))
        fig.suptitle(f'Pitch type: {pitch_type}, Row: {row + 1}')

        for i in range(4):
            index = row * 4 + i
            if index < len(images):
                file_name, highlight_composite, centers = images[index]
                axs[i].imshow(highlight_composite)
                axs[i].set_title(file_name)

                for center in centers:
                    circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
                    axs[i].add_patch(circle)
            else:
                axs[i].axis('off')


import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib import patches
from collections import defaultdict

def transparent_background(image, lower_green, upper_green):
    img = image.copy()
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] in list(range(lower_green[0], upper_green[0])) and item[1] in list(range(lower_green[1], upper_green[1])) and item[2] in list(range(lower_green[2], upper_green[2])):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'
lower_green = (0, 120, 0)
upper_green = (100, 255, 100)
n_clusters = 4
circle_radius = 20
file_names = os.listdir(folder_path)

# Open the reference image
reference_image_name = '18-FF.png'
reference_image_path = os.path.join(folder_path, reference_image_name)
reference_img = Image.open(reference_image_path).convert('RGBA')
reference_img_trans = transparent_background(reference_img, lower_green, upper_green)

# Initialize a list to store the difference arrays for FF pitch type
ff_diffs = []

for file_name in sorted(file_names):
    if not os.path.splitext(file_name)[1] in [".png", ".jpg", ".jpeg"]:
        continue

    img_path = os.path.join(folder_path, file_name)
    img = Image.open(img_path).convert('RGBA')
    img_trans = transparent_background(img, lower_green, upper_green)
    pitch_type = file_name.split('-')[1].split('.')[0]

    # Compute the difference with the reference image
    diff = ImageChops.difference(img_trans, reference_img_trans)
    diff_arr = np.array(diff)

    # Store the difference array for FF pitch type
    if pitch_type == 'FF':
        ff_diffs.append(diff_arr)

# Compute the mean and standard deviation of the differences for FF pitch type
ff_diffs_arr = np.array(ff_diffs)
mean_ff_diff = np.mean(ff_diffs_arr)
std_ff_diff = np.std(ff_diffs_arr)

images_per_pitch_type = defaultdict(lambda: [])

for file_name in sorted(file_names):
    if not os.path.splitext(file_name)[1] in [".png", ".jpg", ".jpeg"]:
        continue

    img_path = os.path.join(folder_path, file_name)
    img = Image.open(img_path).convert('RGBA')
    img_trans = transparent_background(img, lower_green, upper_green)
    pitch_type = file_name.split('-')[1].split('.')[0]

    # Compute the difference with the reference image
    diff = ImageChops.difference(img_trans, reference_img_trans)
    diff_arr = np.array(diff)

    # Adjust the differences for FF pitch type considering the 'error'
    if pitch_type == 'FF':
        diff_arr = np.where((mean_ff_diff - std_ff_diff <= diff_arr) & (diff_arr <= mean_ff_diff + std_ff_diff), 0, diff_arr)

    threshold = 250
    extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))
    extreme_points_array = np.array(extreme_points).transpose()

    if extreme_points_array.shape[0] > 0:
        n_clusters_adj = min(n_clusters, extreme_points_array.shape[0])
        kmeans = KMeans(n_clusters=n_clusters_adj, n_init=10)
        kmeans.fit(extreme_points_array)
        centers = kmeans.cluster_centers_

        highlight_img_arr = np.zeros_like(diff_arr)
        highlight_img_arr[extreme_points] = [255, 0, 0, 255]
        highlight_img_pil = Image.fromarray(highlight_img_arr)
        highlight_composite = Image.alpha_composite(img_trans, highlight_img_pil)

        images_per_pitch_type[pitch_type].append((file_name, highlight_composite, centers))

for pitch_type, images in images_per_pitch_type.items():
    n_rows = -(-len(images) // 4)

    for row in range(n_rows):
        fig, axs = plt.subplots(1, 4, figsize=(20, 5))
        fig.suptitle(f'Pitch type: {pitch_type}, Row: {row + 1}')

        for i in range(4):
            index = row * 4 + i
            if index < len(images):
                file_name, highlight_composite, centers = images[index]
                axs[i].imshow(highlight_composite)
                axs[i].set_title(file_name)

                for center in centers:
                    circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
                    axs[i].add_patch(circle)
            else:
                axs[i].axis('off')


import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib import patches
from collections import defaultdict

def transparent_background(image, lower_green, upper_green):
    img = image.copy()
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] in list(range(lower_green[0], upper_green[0])) and item[1] in list(range(lower_green[1], upper_green[1])) and item[2] in list(range(lower_green[2], upper_green[2])):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

folder_path = '/content/drive/MyDrive/Colab Notebooks/test/2'
lower_green = (0, 120, 0)
upper_green = (100, 255, 100)
n_clusters = 4
circle_radius = 20
file_names = os.listdir(folder_path)

# Open the reference image
reference_image_name = '18-FF.png'
reference_image_path = os.path.join(folder_path, reference_image_name)
reference_img = Image.open(reference_image_path).convert('RGBA')
reference_img_trans = transparent_background(reference_img, lower_green, upper_green)

# Initialize a list to store the difference arrays for FF pitch type
ff_diffs = []

for file_name in sorted(file_names):
    if not os.path.splitext(file_name)[1] in [".png", ".jpg", ".jpeg"]:
        continue

    img_path = os.path.join(folder_path, file_name)
    img = Image.open(img_path).convert('RGBA')
    img_trans = transparent_background(img, lower_green, upper_green)
    pitch_type = file_name.split('-')[1].split('.')[0]

    # Compute the difference with the reference image
    diff = ImageChops.difference(img_trans, reference_img_trans)
    diff_arr = np.array(diff)

    # Store the difference array for FF pitch type
    if pitch_type == 'FF':
        ff_diffs.append(diff_arr)

# Compute the mean and standard deviation of the differences for FF pitch type
ff_diffs_arr = np.array(ff_diffs)
mean_ff_diff = np.mean(ff_diffs_arr)
std_ff_diff = np.std(ff_diffs_arr)

images_per_pitch_type = defaultdict(lambda: [])

for file_name in sorted(file_names):
    if not os.path.splitext(file_name)[1] in [".png", ".jpg", ".jpeg"]:
        continue

    img_path = os.path.join(folder_path, file_name)
    img = Image.open(img_path).convert('RGBA')
    img_trans = transparent_background(img, lower_green, upper_green)
    pitch_type = file_name.split('-')[1].split('.')[0]

    # Compute the difference with the reference image
    diff = ImageChops.difference(img_trans, reference_img_trans)
    diff_arr = np.array(diff)


    # Adjust the differences for FF pitch type considering the 'error'
    # Let's say you want to adjust to mean ± 2SD instead of mean ± 1SD
    if pitch_type == 'FF':
      diff_arr = np.where((mean_ff_diff - 2*std_ff_diff <= diff_arr) & (diff_arr <= mean_ff_diff + 2*std_ff_diff), 0, diff_arr)


    threshold = 250
    extreme_points = np.where(np.any(diff_arr[:, :, :3] > threshold, axis=-1))
    extreme_points_array = np.array(extreme_points).transpose()

    if extreme_points_array.shape[0] > 0:
        n_clusters_adj = min(n_clusters, extreme_points_array.shape[0])
        kmeans = KMeans(n_clusters=n_clusters_adj, n_init=10)
        kmeans.fit(extreme_points_array)
        centers = kmeans.cluster_centers_

        highlight_img_arr = np.zeros_like(diff_arr)
        highlight_img_arr[extreme_points] = [255, 0, 0, 255]
        highlight_img_pil = Image.fromarray(highlight_img_arr)
        highlight_composite = Image.alpha_composite(img_trans, highlight_img_pil)

        images_per_pitch_type[pitch_type].append((file_name, highlight_composite, centers))

for pitch_type, images in images_per_pitch_type.items():
    n_rows = -(-len(images) // 4)

    for row in range(n_rows):
        fig, axs = plt.subplots(1, 4, figsize=(20, 5))
        fig.suptitle(f'Pitch type: {pitch_type}, Row: {row + 1}')

        for i in range(4):
            index = row * 4 + i
            if index < len(images):
                file_name, highlight_composite, centers = images[index]
                axs[i].imshow(highlight_composite)
                axs[i].set_title(file_name)

                for center in centers:
                    circle = patches.Circle((center[1], center[0]), circle_radius, edgecolor='blue', facecolor='none', linewidth=2)
                    axs[i].add_patch(circle)
            else:
                axs[i].axis('off')


