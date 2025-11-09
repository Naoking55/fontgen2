#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
偏旁抽出ツール - 完全版 GUI v2.8 (2025-10-10)
消しゴム補間機能追加
"""

import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageTk
import threading
import math  # [ADD] 2025-10-10: 補間計算用

# macOS対策
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# ============================================================
# [BLOCK1-BEGIN] 偏旁カタログ (2025-10-10)
# ============================================================
"""
■ サンプル文字の修正方法

PARTS_CATALOG の各エントリの "sample" を変更してください。

例：
"ひへん": {"char": "火", "sample": "灯", "split": "left", "ratio": 0.35},
                                    ↑ ここを変更

修正が必要な例：
- 偏が明確でない文字（例：「炎」→「灯」に変更済み）
- 旁が明確でない文字
- 抽出結果が不適切な文字

修正後、再度「抽出開始」を実行すると、新しいサンプル文字で抽出されます。
"""

PARTS_CATALOG = {
    # ===== 偏（へん）: 左側配置のみ - 40種類 =====
    "hen": {
        # 人に関する偏
        "にんべん": {"char": "亻", "sample": "仁", "split": "left", "ratio": 0.35},
        "ぎょうにんべん": {"char": "彳", "sample": "行", "split": "left", "ratio": 0.3},
        "りっしんべん": {"char": "忄", "sample": "情", "split": "left", "ratio": 0.3},
        
        # 手・動作に関する偏
        "てへん": {"char": "扌", "sample": "持", "split": "left", "ratio": 0.35},
        "さんずい": {"char": "氵", "sample": "海", "split": "left", "ratio": 0.3},
        
        # 言葉に関する偏
        "ごんべん": {"char": "訁", "sample": "語", "split": "left", "ratio": 0.4},
        "くちへん": {"char": "口", "sample": "呼", "split": "left", "ratio": 0.4},
        
        # 木・植物に関する偏
        "きへん": {"char": "木", "sample": "林", "split": "left", "ratio": 0.4},
        "のぎへん": {"char": "禾", "sample": "秋", "split": "left", "ratio": 0.4},
        
        # 金属・鉱物に関する偏
        "かねへん": {"char": "金", "sample": "鉄", "split": "left", "ratio": 0.45},
        "いしへん": {"char": "石", "sample": "砂", "split": "left", "ratio": 0.4},
        
        # 糸・衣に関する偏
        "いとへん": {"char": "糸", "sample": "結", "split": "left", "ratio": 0.45},
        "ころもへん": {"char": "衤", "sample": "被", "split": "left", "ratio": 0.35},
        
        # 食べ物に関する偏
        "しょくへん": {"char": "飠", "sample": "館", "split": "left", "ratio": 0.4},
        
        # 動物に関する偏
        "けものへん": {"char": "犭", "sample": "狼", "split": "left", "ratio": 0.35},
        "うおへん": {"char": "魚", "sample": "鮮", "split": "left", "ratio": 0.5},
        "むしへん": {"char": "虫", "sample": "蛇", "split": "left", "ratio": 0.4},
        
        # 土・自然に関する偏
        "つちへん": {"char": "土", "sample": "城", "split": "left", "ratio": 0.35},
        "やまへん": {"char": "山", "sample": "峰", "split": "left", "ratio": 0.4},
        
        # 火・水に関する偏
        "ひへん": {"char": "火", "sample": "灯", "split": "left", "ratio": 0.35},
        "にすい": {"char": "冫", "sample": "冷", "split": "left", "ratio": 0.25},
        
        # 体の部位に関する偏
        "にくづき": {"char": "月", "sample": "胸", "split": "left", "ratio": 0.4},
        "ほねへん": {"char": "骨", "sample": "骸", "split": "left", "ratio": 0.5},
        "めへん": {"char": "目", "sample": "眼", "split": "left", "ratio": 0.4},
        "みみへん": {"char": "耳", "sample": "聴", "split": "left", "ratio": 0.4},
        "みへん": {"char": "身", "sample": "躯", "split": "left", "ratio": 0.4},
        
        # その他の重要な偏
        "やまいだれへん": {"char": "疒", "sample": "病", "split": "left", "ratio": 0.3},
        "おんなへん": {"char": "女", "sample": "妹", "split": "left", "ratio": 0.4},
        "こざとへん": {"char": "阝", "sample": "防", "split": "left", "ratio": 0.3},
        "しめすへん": {"char": "礻", "sample": "祈", "split": "left", "ratio": 0.35},
        
        # マイナーな偏
        "ゆみへん": {"char": "弓", "sample": "張", "split": "left", "ratio": 0.35},
        "かわへん": {"char": "革", "sample": "靴", "split": "left", "ratio": 0.45},
        "かいへん": {"char": "貝", "sample": "販", "split": "left", "ratio": 0.4},
        "あしへん": {"char": "足", "sample": "跡", "split": "left", "ratio": 0.45},
        "くるまへん": {"char": "車", "sample": "輪", "split": "left", "ratio": 0.45},
        "さけのとり": {"char": "酉", "sample": "配", "split": "left", "ratio": 0.4},
        "うしへん": {"char": "牛", "sample": "牡", "split": "left", "ratio": 0.4},
        "ちからへん": {"char": "力", "sample": "加", "split": "left", "ratio": 0.35},
        "まめへん": {"char": "豆", "sample": "豉", "split": "left", "ratio": 0.4},
        "ぶたへん": {"char": "豕", "sample": "豚", "split": "left", "ratio": 0.4},
    },
    
    # ===== 旁（つくり）: 右側配置のみ - 35種類 =====
    "tsukuri": {
        # 基本的な旁
        "おおざと": {"char": "阝", "sample": "部", "split": "right", "ratio": 0.7},
        "りっとう": {"char": "刂", "sample": "則", "split": "right", "ratio": 0.7},
        "ちから": {"char": "力", "sample": "助", "split": "right", "ratio": 0.65},
        "おおがい": {"char": "頁", "sample": "順", "split": "right", "ratio": 0.55},
        "ぼくづくり": {"char": "攵", "sample": "政", "split": "right", "ratio": 0.65},
        
        # 鳥・動物系
        "ふるとり": {"char": "隹", "sample": "雑", "split": "right", "ratio": 0.6},
        "とり": {"char": "鳥", "sample": "鳩", "split": "right", "ratio": 0.55},
        "うま": {"char": "馬", "sample": "駅", "split": "right", "ratio": 0.55},
        "しか": {"char": "鹿", "sample": "麗", "split": "right", "ratio": 0.55},
        
        # 武器・道具系
        "きづくり": {"char": "斤", "sample": "新", "split": "right", "ratio": 0.65},
        "ほこづくり": {"char": "戈", "sample": "成", "split": "right", "ratio": 0.6},
        "おのづくり": {"char": "斤", "sample": "所", "split": "right", "ratio": 0.65},
        "かたな": {"char": "刀", "sample": "切", "split": "right", "ratio": 0.65},
        "ほこ": {"char": "殳", "sample": "殴", "split": "right", "ratio": 0.6},
        
        # 文字・記号系
        "ふでづくり": {"char": "聿", "sample": "律", "split": "right", "ratio": 0.6},
        "ぼく": {"char": "攴", "sample": "牧", "split": "right", "ratio": 0.65},
        "おおざと右": {"char": "邑", "sample": "郎", "split": "right", "ratio": 0.6},
        
        # 自然・天体系
        "おうへん": {"char": "王", "sample": "珠", "split": "right", "ratio": 0.6},
        "つき": {"char": "月", "sample": "朝", "split": "right", "ratio": 0.6},
        "ひ": {"char": "日", "sample": "旧", "split": "right", "ratio": 0.6},
        "かぜ": {"char": "風", "sample": "颯", "split": "right", "ratio": 0.55},
        
        # 体・感覚系
        "みる": {"char": "見", "sample": "規", "split": "right", "ratio": 0.6},
        "きく": {"char": "音", "sample": "韻", "split": "right", "ratio": 0.55},
        "あくび": {"char": "欠", "sample": "歌", "split": "right", "ratio": 0.65},
        
        # 食物・植物系
        "むぎ": {"char": "麦", "sample": "麺", "split": "right", "ratio": 0.55},
        "まめ": {"char": "豆", "sample": "豊", "split": "right", "ratio": 0.6},
        
        # その他
        "おおがい頁": {"char": "頁", "sample": "頭", "split": "right", "ratio": 0.55},
        "おに": {"char": "鬼", "sample": "魅", "split": "right", "ratio": 0.55},
        "かい右": {"char": "貝", "sample": "頁", "split": "right", "ratio": 0.6},
        "ふ": {"char": "阜", "sample": "陸", "split": "right", "ratio": 0.6},
        
        # 複合系
        "けん": {"char": "見", "sample": "視", "split": "right", "ratio": 0.6},
        "せい": {"char": "斉", "sample": "済", "split": "right", "ratio": 0.6},
        "き": {"char": "气", "sample": "気", "split": "right", "ratio": 0.6},
        "しゅう": {"char": "隹", "sample": "集", "split": "right", "ratio": 0.6},
        "よう": {"char": "羊", "sample": "養", "split": "right", "ratio": 0.6},
    },
    
    # ===== 冠（かんむり）: 上側配置 - 28種類 =====
    "kanmuri": {
        # 植物に関する冠
        "くさかんむり": {"char": "艹", "sample": "花", "split": "top", "ratio": 0.3},
        "たけかんむり": {"char": "⺮", "sample": "笑", "split": "top", "ratio": 0.35},
        
        # 自然・天候に関する冠
        "あめかんむり": {"char": "雨", "sample": "雷", "split": "top", "ratio": 0.4},
        "やまかんむり": {"char": "山", "sample": "崩", "split": "top", "ratio": 0.35},
        
        # 建物・覆うものに関する冠
        "うかんむり": {"char": "宀", "sample": "宇", "split": "top", "ratio": 0.25},
        "あなかんむり": {"char": "穴", "sample": "空", "split": "top", "ratio": 0.35},
        "わかんむり": {"char": "冖", "sample": "冠", "split": "top", "ratio": 0.25},
        
        # 網・枠に関する冠
        "あみがしら": {"char": "罒", "sample": "買", "split": "top", "ratio": 0.3},
        "よこめ": {"char": "⺫", "sample": "置", "split": "top", "ratio": 0.3},
        
        # 形・記号的な冠
        "なべぶた": {"char": "亠", "sample": "市", "split": "top", "ratio": 0.2},
        "はちがしら": {"char": "八", "sample": "公", "split": "top", "ratio": 0.25},
        "ひとやね": {"char": "𠆢", "sample": "会", "split": "top", "ratio": 0.2},
        "つめかんむり": {"char": "爫", "sample": "受", "split": "top", "ratio": 0.3},
        "てんてん": {"char": "⺀", "sample": "当", "split": "top", "ratio": 0.25},
        
        # その他の冠
        "しょうがしら": {"char": "⺌", "sample": "尚", "split": "top", "ratio": 0.25},
        "だいかんむり": {"char": "大", "sample": "奇", "split": "top", "ratio": 0.3},
        "ひとがしら": {"char": "人", "sample": "介", "split": "top", "ratio": 0.25},
        "けいがしら": {"char": "⺕", "sample": "前", "split": "top", "ratio": 0.3},
        "おいがしら": {"char": "老", "sample": "考", "split": "top", "ratio": 0.35},
        "ちいさい": {"char": "小", "sample": "尖", "split": "top", "ratio": 0.3},
        "そうにょう": {"char": "⺍", "sample": "学", "split": "top", "ratio": 0.25},
        "なつあし上": {"char": "夂", "sample": "条", "split": "top", "ratio": 0.3},
        "かぜがまえ": {"char": "風", "sample": "風", "split": "top", "ratio": 0.4},
        "おおいかんむり": {"char": "覀", "sample": "要", "split": "top", "ratio": 0.35},
        "あめ": {"char": "雨", "sample": "雪", "split": "top", "ratio": 0.4},
        "くち上": {"char": "口", "sample": "吉", "split": "top", "ratio": 0.3},
        "つち上": {"char": "土", "sample": "吉", "split": "top", "ratio": 0.3},
        "くさ": {"char": "艸", "sample": "草", "split": "top", "ratio": 0.3},
    },
    
    # ===== 脚（あし）: 下側配置 - 12種類 =====
    "ashi": {
        "こころ": {"char": "心", "sample": "念", "split": "bottom", "ratio": 0.65},
        "れっか": {"char": "灬", "sample": "熱", "split": "bottom", "ratio": 0.75},
        "ひとあし": {"char": "儿", "sample": "児", "split": "bottom", "ratio": 0.7},
        "したごころ": {"char": "心", "sample": "恋", "split": "bottom", "ratio": 0.7},
        "したみず": {"char": "水", "sample": "泰", "split": "bottom", "ratio": 0.7},
        "さら": {"char": "皿", "sample": "盛", "split": "bottom", "ratio": 0.7},
        "こうあし": {"char": "儿", "sample": "兄", "split": "bottom", "ratio": 0.7},
        "したひ": {"char": "灬", "sample": "煮", "split": "bottom", "ratio": 0.75},
        "かい": {"char": "貝", "sample": "買", "split": "bottom", "ratio": 0.65},
        "こころあし": {"char": "心", "sample": "慕", "split": "bottom", "ratio": 0.7},
        "したしたごころ": {"char": "灬", "sample": "点", "split": "bottom", "ratio": 0.75},
        "れんが": {"char": "灬", "sample": "煎", "split": "bottom", "ratio": 0.75},
    },
    
    # ===== 繞（にょう）: 左下を囲む - 5種類 =====
    "nyou": {
        "しんにょう": {"char": "辶", "sample": "近", "split": "left_bottom", "ratio": 0.6},
        "えんにょう": {"char": "廴", "sample": "延", "split": "left_bottom", "ratio": 0.55},
        "そうにょう走": {"char": "走", "sample": "起", "split": "left_bottom", "ratio": 0.65},
        "えんにょう廴": {"char": "廴", "sample": "建", "split": "left_bottom", "ratio": 0.55},
        "かんにょう": {"char": "⻎", "sample": "道", "split": "left_bottom", "ratio": 0.65},
    },
    
    # ===== 垂（たれ）: 上から左へ垂れる - 10種類 =====
    "tare": {
        "がんだれ": {"char": "厂", "sample": "原", "split": "top_left", "ratio": 0.5},
        "まだれ": {"char": "广", "sample": "広", "split": "top_left", "ratio": 0.45},
        "やまいだれ": {"char": "疒", "sample": "痛", "split": "top_left", "ratio": 0.45},
        "とだれ": {"char": "戶", "sample": "戻", "split": "top_left", "ratio": 0.5},
        "しかばねだれ": {"char": "尸", "sample": "局", "split": "top_left", "ratio": 0.45},
        "かばねだれ": {"char": "尸", "sample": "屋", "split": "top_left", "ratio": 0.45},
        "とびがしら": {"char": "飛", "sample": "飛", "split": "top_left", "ratio": 0.5},
        "いわだれ": {"char": "厂", "sample": "厚", "split": "top_left", "ratio": 0.45},
        "たれ": {"char": "广", "sample": "店", "split": "top_left", "ratio": 0.45},
        "がんだれ厂": {"char": "厂", "sample": "雁", "split": "top_left", "ratio": 0.5},
    },
    
    # ===== 構（かまえ）: 周りを囲む - 14種類 =====
    "kamae": {
        "もんがまえ": {"char": "門", "sample": "間", "split": "frame", "ratio": 0.5},
        "くにがまえ": {"char": "囗", "sample": "国", "split": "frame", "ratio": 0.5},
        "どうがまえ": {"char": "行", "sample": "衛", "split": "frame", "ratio": 0.5},
        "かくしがまえ": {"char": "匸", "sample": "匹", "split": "frame", "ratio": 0.5},
        "はこがまえ": {"char": "匚", "sample": "匠", "split": "frame", "ratio": 0.45},
        "けいがまえ": {"char": "冂", "sample": "円", "split": "frame", "ratio": 0.45},
        "もんがまえ門": {"char": "門", "sample": "門", "split": "frame", "ratio": 0.5},
        "とうがまえ": {"char": "鬨", "sample": "鬥", "split": "frame", "ratio": 0.5},
        "くがまえ": {"char": "句", "sample": "句", "split": "frame", "ratio": 0.45},
        "とかまえ": {"char": "戸", "sample": "房", "split": "frame", "ratio": 0.5},
        "むじなへん": {"char": "鬼", "sample": "魂", "split": "frame", "ratio": 0.55},
        "しきがまえ": {"char": "式", "sample": "式", "split": "frame", "ratio": 0.5},
        "かぜがまえ": {"char": "風", "sample": "凪", "split": "frame", "ratio": 0.5},
        "とがまえ": {"char": "戸", "sample": "扉", "split": "frame", "ratio": 0.5},
    },
}

# ============================================================
# [BLOCK1-END]
# ============================================================











# ============================================================
# [BLOCK2-BEGIN] 画像処理ユーティリティ (2025-10-10)
# ============================================================

def render_char_to_bitmap(char, font_path, size=1024):
    """文字をビットマップにレンダリング"""
    try:
        font = ImageFont.truetype(font_path, size)
        img = Image.new("L", (size, size), 255)
        draw = ImageDraw.Draw(img)
        
        bbox = draw.textbbox((0, 0), char, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        
        x = (size - w) / 2 - bbox[0]
        y = (size - h) / 2 - bbox[1]
        
        draw.text((x, y), char, fill=0, font=font)
        return img
    except:
        return None


def find_split_position(img, direction="vertical", ratio=0.5):
    """画像の分割位置を検出（ratio指定対応）"""
    w, h = img.size
    
    if direction == "vertical":
        return int(w * ratio)
    else:
        return int(h * ratio)


def split_glyph(img, split_type, ratio=0.5):
    """グリフを分割してパーツを抽出（比率指定対応）"""
    if img is None:
        return None
    
    w, h = img.size
    
    if split_type == "left":
        split_x = find_split_position(img, "vertical", ratio)
        return img.crop((0, 0, split_x, h))
    elif split_type == "right":
        split_x = find_split_position(img, "vertical", ratio)
        return img.crop((split_x, 0, w, h))
    elif split_type == "top":
        split_y = find_split_position(img, "horizontal", ratio)
        return img.crop((0, 0, w, split_y))
    elif split_type == "bottom":
        split_y = find_split_position(img, "horizontal", ratio)
        return img.crop((0, split_y, w, h))
    elif split_type == "left_bottom":
        split_x = int(w * ratio)
        split_y = int(h * 0.7)
        
        result = Image.new("L", (w, h), 255)
        result.paste(img.crop((0, 0, split_x, h)), (0, 0))
        result.paste(img.crop((0, split_y, w, h)), (0, split_y))
        
        return result
    elif split_type == "top_left":
        split_x = int(w * ratio)
        split_y = int(h * 0.4)
        
        result = Image.new("L", (w, h), 255)
        result.paste(img.crop((0, 0, w, split_y)), (0, 0))
        result.paste(img.crop((0, 0, split_x, h)), (0, 0))
        
        return result
    elif split_type == "top_right":
        split_x = int(w * (1.0 - ratio))
        split_y = int(h * 0.4)
        
        result = Image.new("L", (w, h), 255)
        result.paste(img.crop((0, 0, w, split_y)), (0, 0))
        result.paste(img.crop((split_x, 0, w, h)), (split_x, 0))
        
        return result
    elif split_type == "right_bottom":
        split_x = int(w * (1.0 - ratio))
        split_y = int(h * 0.7)
        
        result = Image.new("L", (w, h), 255)
        result.paste(img.crop((split_x, 0, w, h)), (split_x, 0))
        result.paste(img.crop((0, split_y, w, h)), (0, split_y))
        
        return result
    elif split_type == "frame":
        return img
    else:
        return img


def remove_noise(img, min_size=50):
    """ノイズ除去（孤立した小さなピクセル塊を削除）"""
    if img is None:
        return None
    
    pixels = img.load()
    w, h = img.size
    visited = set()
    
    def flood_fill_count(start_x, start_y):
        """連結成分のサイズをカウント"""
        stack = [(start_x, start_y)]
        count = 0
        coords = []
        
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            if not (0 <= x < w and 0 <= y < h):
                continue
            if pixels[x, y] >= 128:
                continue
            
            visited.add((x, y))
            coords.append((x, y))
            count += 1
            
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
        
        return count, coords
    
    result = img.copy()
    result_pixels = result.load()
    
    for y in range(h):
        for x in range(w):
            if (x, y) not in visited and pixels[x, y] < 128:
                size, coords = flood_fill_count(x, y)
                if size < min_size:
                    for cx, cy in coords:
                        result_pixels[cx, cy] = 255
    
    return result


def trim_whitespace(img):
    """余白を削除"""
    if img is None:
        return None
    bbox = img.getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def save_as_transparent_png(img, output_path):
    """グレースケール画像を透過PNGとして保存"""
    if img is None:
        return False
    
    try:
        rgba = Image.new("RGBA", img.size, (0, 0, 0, 0))
        pixels = img.load()
        rgba_pixels = rgba.load()
        
        for y in range(img.height):
            for x in range(img.width):
                gray = pixels[x, y]
                alpha = 255 - gray
                rgba_pixels[x, y] = (0, 0, 0, alpha)
        
        rgba.save(output_path, "PNG")
        return True
    except:
        return False

# ============================================================
# [BLOCK2-END]
# ============================================================











# ============================================================
# [BLOCK3-BEGIN] パーツ抽出コア処理 (2025-10-10)
# ============================================================

def extract_single_part(font_path, part_name, part_info, output_path, noise_removal=True):
    """単一パーツを抽出"""
    try:
        sample_char = part_info["sample"]
        split_type = part_info["split"]
        ratio = part_info.get("ratio", 0.5)
        
        img = render_char_to_bitmap(sample_char, font_path)
        if img is None:
            return False, None, "レンダリング失敗"
        
        part_img = split_glyph(img, split_type, ratio)
        if part_img is None:
            return False, None, "分割失敗"
        
        if noise_removal:
            part_img = remove_noise(part_img)
        
        part_img = trim_whitespace(part_img)
        
        if save_as_transparent_png(part_img, output_path):
            return True, part_img, None
        else:
            return False, None, "保存失敗"
            
    except Exception as e:
        return False, None, str(e)


def extract_all_parts(font_path, output_dir, progress_callback=None, log_callback=None):
    """フォントから全パーツを抽出"""
    
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)
    
    os.makedirs(output_dir, exist_ok=True)
    
    stats = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "by_category": {}
    }
    
    catalog_json = {}
    
    log("=" * 70)
    log("偏旁抽出ツール")
    log("=" * 70)
    log(f"フォント: {font_path}")
    log(f"出力先: {output_dir}")
    log("=" * 70)
    log("")
    
    total_parts = sum(len(parts) for parts in PARTS_CATALOG.values())
    current_idx = 0
    
    for category, parts in PARTS_CATALOG.items():
        category_name = {
            "hen": "偏（へん）",
            "tsukuri": "旁（つくり）",
            "kanmuri": "冠（かんむり）",
            "ashi": "脚（あし）",
            "nyou": "繞（にょう）",
            "tare": "垂（たれ）",
            "kamae": "構（かまえ）"
        }.get(category, category)
        
        log(f"\n【{category_name}】")
        log("-" * 70)
        
        category_stats = {"success": 0, "failed": 0}
        catalog_json[category] = {}
        
        for part_name, part_info in parts.items():
            current_idx += 1
            stats["total"] += 1
            
            filename = f"{category}_{part_name}_{part_info['char']}.png"
            output_path = os.path.join(output_dir, filename)
            
            msg = f"  {part_name} ({part_info['char']}) [例: {part_info['sample']}]"
            
            if progress_callback:
                progress_callback(current_idx, total_parts, f"{part_name} 処理中...")
            
            success, img, error = extract_single_part(font_path, part_name, part_info, output_path)
            
            if success:
                log(f"{msg} ... ✅ 保存完了")
                stats["success"] += 1
                category_stats["success"] += 1
                
                catalog_json[category][part_name] = {
                    "char": part_info["char"],
                    "sample": part_info["sample"],
                    "file": filename,
                    "split": part_info["split"],
                    "ratio": part_info.get("ratio", 0.5)
                }
            else:
                log(f"{msg} ... ❌ {error}")
                stats["failed"] += 1
                category_stats["failed"] += 1
        
        stats["by_category"][category] = category_stats
    
    catalog_path = os.path.join(output_dir, "parts_catalog.json")
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog_json, f, ensure_ascii=False, indent=2)
    
    log("\n" + "=" * 70)
    log("抽出完了")
    log("=" * 70)
    log(f"✅ 成功: {stats['success']}")
    log(f"❌ 失敗: {stats['failed']}")
    log(f"📊 合計: {stats['total']}")
    log("\nカテゴリ別:")
    for cat, cat_stats in stats["by_category"].items():
        log(f"  {cat:10s}: 成功 {cat_stats['success']:2d} / 失敗 {cat_stats['failed']:2d}")
    log(f"\n📁 保存先: {os.path.abspath(output_dir)}")
    log(f"📋 カタログ: {catalog_path}")
    log("=" * 70)
    
    return stats

# ============================================================
# [BLOCK3-END]
# ============================================================











# ============================================================
# [BLOCK4-BEGIN] パーツプレビュー・編集GUI (2025-10-10: 補間描画追加)
# ============================================================

class PartsPreviewWindow(tk.Toplevel):
    """パーツプレビュー・編集ウィンドウ"""
    
    def __init__(self, parent, parts_dir, font_path):
        super().__init__(parent)
        self.title("パーツプレビュー・編集")
        self.geometry("1500x850")
        
        self.parts_dir = parts_dir
        self.font_path = font_path
        self.catalog = self._load_catalog()
        self.current_category = None
        self.current_part = None
        self.photo_cache = {}
        
        self.eraser_mode = False
        self.eraser_size = 20
        self.eraser_shape = 'circle'
        self.current_image = None
        self.modified = False
        
        self.undo_stack = []
        self.redo_stack = []
        
        self.zoom_level = 1.0
        self.zoom_levels = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]
        self.preview_scale = 1.0
        
        self.eraser_cursor_id = None
        
        # [ADD] 2025-10-10: 補間描画用
        self.last_erase_pos = None
        
        self._setup_ui()
        self._load_preview()
    
    def _load_catalog(self):
        """カタログJSON読み込み"""
        catalog_path = os.path.join(self.parts_dir, "parts_catalog.json")
        if os.path.exists(catalog_path):
            with open(catalog_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _setup_ui(self):
        """UI構築"""
        # 左側: カテゴリリスト
        left_frame = ttk.Frame(self, width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(left_frame, text="カテゴリ", font=("", 12, "bold")).pack(pady=5)
        
        self.category_listbox = tk.Listbox(left_frame, font=("", 22))
        self.category_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.category_listbox.bind('<<ListboxSelect>>', self._on_category_select)
        
        for category in ["hen", "tsukuri", "kanmuri", "ashi", "nyou", "tare", "kamae"]:
            display_name = {
                "hen": "偏（へん）",
                "tsukuri": "旁（つくり）",
                "kanmuri": "冠（かんむり）",
                "ashi": "脚（あし）",
                "nyou": "繞（にょう）",
                "tare": "垂（たれ）",
                "kamae": "構（かまえ）"
            }.get(category, category)
            self.category_listbox.insert(tk.END, display_name)
        
        # 中央: パーツ一覧
        center_frame = ttk.Frame(self)
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(center_frame, text="パーツ一覧", font=("", 12, "bold")).pack(pady=5)
        
        canvas_frame = ttk.Frame(center_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.parts_canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.parts_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.parts_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.parts_canvas.configure(scrollregion=self.parts_canvas.bbox("all"))
        )
        
        self.parts_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.parts_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.parts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右側: 詳細編集パネル
        right_frame = ttk.Frame(self, width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        
        ttk.Label(right_frame, text="パーツ編集", font=("", 12, "bold")).pack(pady=5)
        
        # パーツ情報
        info_frame = ttk.LabelFrame(right_frame, text="情報", padding=5)
        info_frame.pack(fill=tk.X, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="パーツを選択してください", wraplength=450)
        self.info_label.pack()
        
        # プレビュー
        preview_frame = ttk.LabelFrame(right_frame, text="プレビュー", padding=5)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # ズームコントロール
        zoom_control_frame = ttk.Frame(preview_frame)
        zoom_control_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(zoom_control_frame, text="ズーム:").pack(side=tk.LEFT, padx=2)
        ttk.Button(zoom_control_frame, text="-", command=self._zoom_out, width=3).pack(side=tk.LEFT, padx=1)
        self.zoom_label = ttk.Label(zoom_control_frame, text="100%", width=6)
        self.zoom_label.pack(side=tk.LEFT, padx=1)
        ttk.Button(zoom_control_frame, text="+", command=self._zoom_in, width=3).pack(side=tk.LEFT, padx=1)
        ttk.Button(zoom_control_frame, text="リセット", command=self._zoom_reset, width=6).pack(side=tk.LEFT, padx=1)
        
        ttk.Button(zoom_control_frame, text="↶元に戻す", command=self._undo, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_control_frame, text="↷やり直し", command=self._redo, width=10).pack(side=tk.LEFT, padx=1)
        
        # プレビューキャンバス
        self.preview_canvas = tk.Canvas(preview_frame, width=400, height=350, bg="white", relief="sunken", borderwidth=2)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        self.preview_canvas.bind('<Button-1>', self._on_canvas_click)
        self.preview_canvas.bind('<B1-Motion>', self._on_canvas_drag)
        self.preview_canvas.bind('<ButtonRelease-1>', self._on_canvas_release)  # [ADD] 2025-10-10
        self.preview_canvas.bind('<Motion>', self._on_canvas_motion)
        
        # 編集ツール
        tools_frame = ttk.LabelFrame(right_frame, text="編集ツール", padding=5)
        tools_frame.pack(fill=tk.X, pady=5)
        
        # サンプル文字 + 分割タイプ
        row0_frame = ttk.Frame(tools_frame)
        row0_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(row0_frame, text="サンプル:").pack(side=tk.LEFT)
        self.sample_entry = ttk.Entry(row0_frame, width=4)
        self.sample_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(row0_frame, text="分割:").pack(side=tk.LEFT, padx=(10, 2))
        self.split_type_var = tk.StringVar(value='left')
        split_combo = ttk.Combobox(row0_frame, textvariable=self.split_type_var, width=12, state='readonly')
        split_combo['values'] = [
            '左 (←)',
            '右 (→)',
            '上 (↑)',
            '下 (↓)',
            'L字 (└)',
            '逆L (┐)',
            '┌字',
            '┘字',
            '囲み'
        ]
        split_combo.pack(side=tk.LEFT, padx=2)
        split_combo.bind('<<ComboboxSelected>>', self._on_split_type_change)
        
        # 分割比率
        row1_frame = ttk.Frame(tools_frame)
        row1_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(row1_frame, text="分割比率:").pack(side=tk.LEFT)
        self.ratio_var = tk.DoubleVar(value=0.5)
        ratio_scale = ttk.Scale(row1_frame, from_=0.0, to=1.0, variable=self.ratio_var, orient=tk.HORIZONTAL)
        ratio_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.ratio_label = ttk.Label(row1_frame, text="50%", width=5)
        self.ratio_label.pack(side=tk.LEFT)
        self.ratio_var.trace_add('write', lambda *args: self.ratio_label.config(text=f"{int(self.ratio_var.get()*100)}%"))
        
        # ノイズ除去
        self.noise_removal_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(tools_frame, text="ノイズ自動除去", variable=self.noise_removal_var).pack(anchor=tk.W, pady=2)
        
        # 消しゴム
        self.eraser_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(tools_frame, text="消しゴムモード", variable=self.eraser_var, command=self._toggle_eraser).pack(anchor=tk.W, pady=2)
        
        # 消しゴム形状 + サイズ
        row2_frame = ttk.Frame(tools_frame)
        row2_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(row2_frame, text="形状:").pack(side=tk.LEFT)
        self.eraser_shape_var = tk.StringVar(value='circle')
        ttk.Radiobutton(row2_frame, text="●", variable=self.eraser_shape_var, value='circle', command=self._on_shape_change, width=3).pack(side=tk.LEFT)
        ttk.Radiobutton(row2_frame, text="■", variable=self.eraser_shape_var, value='square', command=self._on_shape_change, width=3).pack(side=tk.LEFT)
        ttk.Radiobutton(row2_frame, text="◆", variable=self.eraser_shape_var, value='diamond', command=self._on_shape_change, width=3).pack(side=tk.LEFT)
        
        ttk.Label(row2_frame, text="サイズ:").pack(side=tk.LEFT, padx=(10, 2))
        self.eraser_size_var = tk.IntVar(value=20)
        eraser_scale = ttk.Scale(row2_frame, from_=5, to=50, variable=self.eraser_size_var, orient=tk.HORIZONTAL, length=100)
        eraser_scale.pack(side=tk.LEFT, padx=2)
        self.eraser_size_var.trace_add('write', lambda *args: self._update_eraser_cursor())
        
        # ボタン
        button_frame = ttk.Frame(tools_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="再抽出", command=self._re_extract, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="保存", command=self._save_current, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="削除", command=self._delete_current, width=10).pack(side=tk.LEFT, padx=2)
        
        # キーボードショートカット
        self.bind('<Control-z>', lambda e: self._undo())
        self.bind('<Control-y>', lambda e: self._redo())
        self.bind('<Control-Shift-Z>', lambda e: self._redo())
    
    def _load_preview(self):
        pass
    
    def _on_split_type_change(self, event):
        """分割タイプ変更時"""
        selected = self.split_type_var.get()
        split_type_map = {
            '左 (←)': 'left',
            '右 (→)': 'right',
            '上 (↑)': 'top',
            '下 (↓)': 'bottom',
            'L字 (└)': 'left_bottom',
            '逆L (┐)': 'top_left',
            '┌字': 'top_right',
            '┘字': 'right_bottom',
            '囲み': 'frame'
        }
        self.current_split_type = split_type_map.get(selected, 'left')
    
    def _on_category_select(self, event):
        """カテゴリ選択時"""
        selection = self.category_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        categories = ["hen", "tsukuri", "kanmuri", "ashi", "nyou", "tare", "kamae"]
        self.current_category = categories[idx]
        
        self._display_parts_grid()
    
    def _display_parts_grid(self):
        """パーツ一覧表示"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.photo_cache.clear()
        
        if self.current_category not in self.catalog:
            ttk.Label(self.scrollable_frame, text="パーツがありません").pack(pady=20)
            return
        
        parts = self.catalog[self.current_category]
        
        col_count = 0
        row_count = 0
        max_cols = 7
        
        for part_name, part_data in parts.items():
            filename = part_data["file"]
            filepath = os.path.join(self.parts_dir, filename)
            
            if not os.path.exists(filepath):
                continue
            
            try:
                img = Image.open(filepath).convert('RGBA')
                
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                
                bg.thumbnail((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(bg)
                self.photo_cache[part_name] = photo
                
                frame = ttk.Frame(self.scrollable_frame, relief="solid", borderwidth=1, padding=5)
                frame.grid(row=row_count, column=col_count, padx=5, pady=5)
                
                label = tk.Label(frame, image=photo, bg="white", cursor="hand2")
                label.pack()
                label.bind('<Button-1>', lambda e, p=part_name: self._select_part(p))
                
                name_label = ttk.Label(frame, text=part_name, font=("", 9))
                name_label.pack()
                
                col_count += 1
                if col_count >= max_cols:
                    col_count = 0
                    row_count += 1
                    
            except Exception as e:
                print(f"[ERROR] サムネイル作成失敗: {part_name} - {e}")
    
    def _select_part(self, part_name):
        """パーツ選択"""
        self.current_part = part_name
        part_data = self.catalog[self.current_category][part_name]
        
        info_text = f"名前: {part_name}\n"
        info_text += f"文字: {part_data['char']}\n"
        info_text += f"サンプル: {part_data['sample']}\n"
        info_text += f"分割: {part_data['split']}\n"
        info_text += f"比率: {part_data['ratio']}"
        self.info_label.config(text=info_text)
        
        self.sample_entry.delete(0, tk.END)
        self.sample_entry.insert(0, part_data['sample'])
        self.ratio_var.set(part_data['ratio'])
        
        # 分割タイプを設定
        split_type_reverse_map = {
            'left': '左 (←)',
            'right': '右 (→)',
            'top': '上 (↑)',
            'bottom': '下 (↓)',
            'left_bottom': 'L字 (└)',
            'top_left': '逆L (┐)',
            'top_right': '┌字',
            'right_bottom': '┘字',
            'frame': '囲み'
        }
        display_split = split_type_reverse_map.get(part_data['split'], '左 (←)')
        self.split_type_var.set(display_split)
        self.current_split_type = part_data['split']
        
        filepath = os.path.join(self.parts_dir, part_data['file'])
        if os.path.exists(filepath):
            img = Image.open(filepath).convert('RGBA')
            
            bg = Image.new('L', img.size, 255)
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b, a = img.getpixel((x, y))
                    if a > 0:
                        bg.putpixel((x, y), 0)
                    else:
                        bg.putpixel((x, y), 255)
            
            self.current_image = bg
            self.zoom_level = 1.0
            
            self.undo_stack = [self.current_image.copy()]
            self.redo_stack = []
            
            self._update_preview()
    
    def _save_to_undo(self):
        """現在の状態をアンドゥスタックに保存"""
        if self.current_image:
            self.undo_stack.append(self.current_image.copy())
            if len(self.undo_stack) > 50:
                self.undo_stack.pop(0)
            self.redo_stack.clear()
    
    def _undo(self):
        """元に戻す"""
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.current_image = self.undo_stack[-1].copy()
            self._update_preview()
    
    def _redo(self):
        """やり直し"""
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.undo_stack.append(state)
            self.current_image = state.copy()
            self._update_preview()
    
    def _zoom_in(self):
        """ズームイン"""
        current_idx = self.zoom_levels.index(self.zoom_level) if self.zoom_level in self.zoom_levels else 2
        if current_idx < len(self.zoom_levels) - 1:
            self.zoom_level = self.zoom_levels[current_idx + 1]
            self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
            self._update_preview()
    
    def _zoom_out(self):
        """ズームアウト"""
        current_idx = self.zoom_levels.index(self.zoom_level) if self.zoom_level in self.zoom_levels else 2
        if current_idx > 0:
            self.zoom_level = self.zoom_levels[current_idx - 1]
            self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")
            self._update_preview()
    
    def _zoom_reset(self):
        """ズームリセット"""
        self.zoom_level = 1.0
        self.zoom_label.config(text="100%")
        self._update_preview()
    
    def _update_preview(self):
        """プレビュー更新"""
        if self.current_image is None:
            return
        
        canvas_w = 400
        canvas_h = 350
        
        orig_w = self.current_image.width
        orig_h = self.current_image.height
        
        scale_w = canvas_w / orig_w if orig_w > 0 else 1.0
        scale_h = canvas_h / orig_h if orig_h > 0 else 1.0
        fit_scale = min(scale_w, scale_h, 1.0)
        
        final_scale = fit_scale * self.zoom_level
        
        new_w = int(orig_w * final_scale)
        new_h = int(orig_h * final_scale)
        
        display_img = self.current_image.resize((new_w, new_h), Image.Resampling.NEAREST)
        
        bg = Image.new('L', (canvas_w, canvas_h), 255)
        x_offset = (canvas_w - new_w) // 2
        y_offset = (canvas_h - new_h) // 2
        
        if x_offset >= 0 and y_offset >= 0:
            bg.paste(display_img, (x_offset, y_offset))
        else:
            paste_x = max(0, x_offset)
            paste_y = max(0, y_offset)
            
            crop_x = max(0, -x_offset)
            crop_y = max(0, -y_offset)
            crop_w = min(new_w - crop_x, canvas_w)
            crop_h = min(new_h - crop_y, canvas_h)
            
            cropped = display_img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
            bg.paste(cropped, (paste_x, paste_y))
        
        self.preview_photo = ImageTk.PhotoImage(bg)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(canvas_w//2, canvas_h//2, image=self.preview_photo)
        
        self.preview_scale = final_scale
    
    def _toggle_eraser(self):
        """消しゴムモード切り替え"""
        self.eraser_mode = self.eraser_var.get()
        if self.eraser_mode:
            self.preview_canvas.config(cursor="none")
        else:
            self.preview_canvas.config(cursor="")
            if self.eraser_cursor_id:
                self.preview_canvas.delete(self.eraser_cursor_id)
                self.eraser_cursor_id = None
    
    def _on_shape_change(self):
        """消しゴム形状変更"""
        self.eraser_shape = self.eraser_shape_var.get()
        self._update_eraser_cursor()
    
    def _on_canvas_motion(self, event):
        """マウス移動時の処理"""
        if self.eraser_mode:
            self._update_eraser_cursor_position(event.x, event.y)
    
    def _update_eraser_cursor(self):
        """消しゴムカーソルの形状を更新"""
        pass
    
    def _update_eraser_cursor_position(self, x, y):
        """消しゴムカーソル位置更新"""
        if self.eraser_cursor_id:
            self.preview_canvas.delete(self.eraser_cursor_id)
        
        if not self.eraser_mode:
            return
        
        radius = int(self.eraser_size_var.get() * self.preview_scale)
        
        if self.eraser_shape == 'circle':
            self.eraser_cursor_id = self.preview_canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                outline='red', width=2, dash=(3, 3)
            )
        elif self.eraser_shape == 'square':
            self.eraser_cursor_id = self.preview_canvas.create_rectangle(
                x - radius, y - radius, x + radius, y + radius,
                outline='red', width=2, dash=(3, 3)
            )
        elif self.eraser_shape == 'diamond':
            points = [
                x, y - radius,
                x + radius, y,
                x, y + radius,
                x - radius, y
            ]
            self.eraser_cursor_id = self.preview_canvas.create_polygon(
                points, outline='red', width=2, dash=(3, 3), fill=''
            )
    
    def _on_canvas_click(self, event):
        """キャンバスクリック"""
        if self.eraser_mode and self.current_image:
            self._save_to_undo()
            img_x, img_y = self._canvas_to_image_coords(event.x, event.y)
            self.last_erase_pos = (img_x, img_y)  # [ADD] 2025-10-10
            self._erase_at_image(img_x, img_y)
    
    def _on_canvas_drag(self, event):
        """キャンバスドラッグ"""  # [FIX] 2025-10-10: 補間描画追加
        if self.eraser_mode and self.current_image:
            img_x, img_y = self._canvas_to_image_coords(event.x, event.y)
            
            if self.last_erase_pos:
                # 前回の位置から現在の位置まで補間
                self._interpolate_erase(self.last_erase_pos[0], self.last_erase_pos[1], img_x, img_y)
            else:
                self._erase_at_image(img_x, img_y)
            
            self.last_erase_pos = (img_x, img_y)
    
    def _on_canvas_release(self, event):
        """マウスボタン解放"""  # [ADD] 2025-10-10
        self.last_erase_pos = None
    
    def _canvas_to_image_coords(self, canvas_x, canvas_y):
        """キャンバス座標を画像座標に変換"""  # [ADD] 2025-10-10
        img_x = int((canvas_x - 200) / self.preview_scale + self.current_image.width / 2)
        img_y = int((canvas_y - 175) / self.preview_scale + self.current_image.height / 2)
        
        img_x = max(0, min(img_x, self.current_image.width - 1))
        img_y = max(0, min(img_y, self.current_image.height - 1))
        
        return img_x, img_y
    
    def _interpolate_erase(self, x1, y1, x2, y2):
        """2点間を補間して消去（デコボコ軽減）"""  # [ADD] 2025-10-10
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        steps = max(int(distance / 2), 1)  # ブラシサイズの半分ごとに補間
        
        for i in range(steps + 1):
            t = i / steps
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            self._erase_at_image(x, y)
        
        self._update_preview()
        self._update_eraser_cursor_position(
            int(200 + (x2 - self.current_image.width / 2) * self.preview_scale),
            int(175 + (y2 - self.current_image.height / 2) * self.preview_scale)
        )
    
    def _erase_at_image(self, img_x, img_y):
        """画像座標で消去"""  # [RENAME] 2025-10-10: _erase_atから名称変更
        if self.current_image is None:
            return
        
        if not (0 <= img_x < self.current_image.width and 0 <= img_y < self.current_image.height):
            return
        
        draw = ImageDraw.Draw(self.current_image)
        radius = int(self.eraser_size_var.get())
        
        if self.eraser_shape == 'circle':
            draw.ellipse([img_x-radius, img_y-radius, img_x+radius, img_y+radius], fill=255)
        elif self.eraser_shape == 'square':
            draw.rectangle([img_x-radius, img_y-radius, img_x+radius, img_y+radius], fill=255)
        elif self.eraser_shape == 'diamond':
            points = [
                (img_x, img_y - radius),
                (img_x + radius, img_y),
                (img_x, img_y + radius),
                (img_x - radius, img_y)
            ]
            draw.polygon(points, fill=255)
        
        self.modified = True
    
    def _re_extract(self):
        """再抽出"""
        if not self.current_part:
            messagebox.showwarning("警告", "パーツを選択してください")
            return
        
        sample_char = self.sample_entry.get()
        if not sample_char:
            messagebox.showwarning("警告", "サンプル文字を入力してください")
            return
        
        part_data = self.catalog[self.current_category][self.current_part]
        part_info = {
            "sample": sample_char,
            "split": self.current_split_type,
            "ratio": self.ratio_var.get(),
            "char": part_data["char"]
        }
        
        filename = part_data["file"]
        output_path = os.path.join(self.parts_dir, filename)
        
        success, img, error = extract_single_part(
            self.font_path,
            self.current_part,
            part_info,
            output_path,
            noise_removal=self.noise_removal_var.get()
        )
        
        if success:
            img_rgba = Image.open(output_path).convert('RGBA')
            bg = Image.new('L', img_rgba.size, 255)
            for y in range(img_rgba.height):
                for x in range(img_rgba.width):
                    r, g, b, a = img_rgba.getpixel((x, y))
                    if a > 0:
                        bg.putpixel((x, y), 0)
            
            self.current_image = bg
            self.zoom_level = 1.0
            
            self.undo_stack = [self.current_image.copy()]
            self.redo_stack = []
            
            self._update_preview()
            messagebox.showinfo("成功", "再抽出しました")
            
            self.catalog[self.current_category][self.current_part]["sample"] = sample_char
            self.catalog[self.current_category][self.current_part]["split"] = self.current_split_type
            self.catalog[self.current_category][self.current_part]["ratio"] = self.ratio_var.get()
            self._save_catalog()
            
            self._display_parts_grid()
        else:
            messagebox.showerror("エラー", f"再抽出失敗: {error}")
    
    def _save_current(self):
        """現在の編集を保存"""
        if not self.current_part or not self.current_image or not self.modified:
            return
        
        part_data = self.catalog[self.current_category][self.current_part]
        filepath = os.path.join(self.parts_dir, part_data['file'])
        
        if save_as_transparent_png(self.current_image, filepath):
            self.modified = False
            messagebox.showinfo("保存", "保存しました")
            self._display_parts_grid()
        else:
            messagebox.showerror("エラー", "保存失敗")
    
    def _delete_current(self):
        """現在のパーツを削除"""
        if not self.current_part:
            return
        
        if not messagebox.askyesno("確認", f"{self.current_part} を削除しますか？"):
            return
        
        part_data = self.catalog[self.current_category][self.current_part]
        filepath = os.path.join(self.parts_dir, part_data['file'])
        
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            del self.catalog[self.current_category][self.current_part]
            self._save_catalog()
            self._display_parts_grid()
            self.current_part = None
            self.current_image = None
            messagebox.showinfo("削除", "削除しました")
        except Exception as e:
            messagebox.showerror("エラー", f"削除失敗: {e}")
    
    def _save_catalog(self):
        """カタログJSON保存"""
        catalog_path = os.path.join(self.parts_dir, "parts_catalog.json")
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(self.catalog, f, ensure_ascii=False, indent=2)

# ============================================================
# [BLOCK4-END]
# ============================================================











# ============================================================
# [BLOCK5-BEGIN] メインGUI (2025-10-10)
# ============================================================

class PartsExtractorGUI:
    """偏旁抽出ツールGUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("偏旁抽出ツール v2.8 (2025-10-10) - 補間描画対応")
        
        self.font_path = None
        self.output_dir = "assets/parts"
        self.is_running = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UI構築"""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        file_frame = ttk.LabelFrame(main_frame, text="入力設定", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(file_frame, text="フォントファイル:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.font_label = ttk.Label(file_frame, text="未選択", foreground="gray")
        self.font_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(file_frame, text="参照...", command=self._select_font, width=10).grid(row=0, column=2, padx=5)
        
        ttk.Label(file_frame, text="出力ディレクトリ:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_label = ttk.Label(file_frame, text=self.output_dir)
        self.output_label.grid(row=1, column=1, sticky=tk.W, padx=5)
        ttk.Button(file_frame, text="変更...", command=self._select_output, width=10).grid(row=1, column=2, padx=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.extract_button = ttk.Button(button_frame, text="抽出開始", command=self._start_extraction)
        self.extract_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="プレビュー・編集", command=self._open_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="出力先を開く", command=self._open_output).pack(side=tk.LEFT, padx=5)
        
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="準備完了")
        self.progress_label.pack()
        
        log_frame = ttk.LabelFrame(main_frame, text="処理ログ", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            wrap=tk.WORD,
            font=("Monaco", 10) if sys.platform == "darwin" else ("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self._log("偏旁抽出ツール v2.8 - 補間描画対応")
        self._log("=" * 70)
        self._log("【更新内容】")
        self._log("  ✅ 消しゴム補間描画: デコボコを大幅軽減")
        self._log("  ✅ 滑らかな消去が可能に")
        self._log("=" * 70)
    
    def _select_font(self):
        path = filedialog.askopenfilename(
            title="フォントファイルを選択",
            filetypes=[("フォントファイル", "*.ttf *.otf"), ("すべてのファイル", "*.*")]
        )
        if path:
            self.font_path = path
            self.font_label.config(text=os.path.basename(path), foreground="black")
            self._log(f"\n✅ フォント選択: {path}")
    
    def _select_output(self):
        path = filedialog.askdirectory(title="出力ディレクトリを選択")
        if path:
            self.output_dir = path
            self.output_label.config(text=path)
            self._log(f"\n📁 出力先変更: {path}")
    
    def _open_output(self):
        if os.path.exists(self.output_dir):
            if sys.platform == "darwin":
                os.system(f'open "{self.output_dir}"')
            elif sys.platform == "win32":
                os.startfile(self.output_dir)
            else:
                os.system(f'xdg-open "{self.output_dir}"')
        else:
            messagebox.showwarning("警告", "出力ディレクトリが存在しません")
    
    def _open_preview(self):
        if not os.path.exists(self.output_dir):
            messagebox.showwarning("警告", "まず抽出を実行してください")
            return
        if not self.font_path:
            messagebox.showwarning("警告", "フォントファイルを選択してください")
            return
        PartsPreviewWindow(self.root, self.output_dir, self.font_path)
    
    def _log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def _update_progress(self, current, total, message):
        self.progress_bar['maximum'] = total
        self.progress_bar['value'] = current
        self.progress_label.config(text=f"{message} ({current}/{total})")
        self.root.update()
    
    def _start_extraction(self):
        if self.is_running:
            return
        if not self.font_path:
            messagebox.showwarning("警告", "フォントファイルを選択してください")
            return
        
        self.is_running = True
        self.extract_button.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        
        self._log("\n" + "=" * 70)
        self._log("抽出開始...")
        self._log("=" * 70)
        
        thread = threading.Thread(target=self._run_extraction, daemon=True)
        thread.start()
    
    def _run_extraction(self):
        try:
            stats = extract_all_parts(
                self.font_path,
                self.output_dir,
                progress_callback=self._update_progress,
                log_callback=self._log
            )
            
            self.root.after(0, lambda: messagebox.showinfo(
                "完了",
                f"抽出完了\n\n✅ 成功: {stats['success']}\n❌ 失敗: {stats['failed']}\n\n保存先: {self.output_dir}"
            ))
        except Exception as e:
            self._log(f"\n❌ エラー: {e}")
            import traceback
            self._log(traceback.format_exc())
            self.root.after(0, lambda: messagebox.showerror("エラー", f"抽出中にエラーが発生しました:\n{e}"))
        finally:
            self.is_running = False
            self.root.after(0, lambda: self.extract_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.progress_label.config(text="完了"))

# ============================================================
# [BLOCK5-END]
# ============================================================











# ============================================================
# [BLOCK6-BEGIN] メインエントリポイント (2025-10-10)
# ============================================================

def main():
    try:
        root = tk.Tk()
        root.geometry("900x750")
        
        app = PartsExtractorGUI(root)
        
        if sys.platform == "darwin":
            root.createcommand("tk::mac::Quit", root.quit)
        
        root.mainloop()
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

# ============================================================
# [BLOCK6-END]
# ============================================================