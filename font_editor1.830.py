#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
フォントエディタ - 高解像度ビットマップフォント制作ツール
Version: 1.82.12
Last Updated: 2025-11-07

変更履歴:
- v1.82.12 (2025-11-07): ログエクスポート機能追加 📄
  * 偏旁抽出ツールのログをテキストファイルに保存可能
    - 「📄 ログを保存」ボタンを追加
    - タイムスタンプ付きファイル名で自動提案
    - UTF-8エンコーディングで保存
  * トラブルシューティングと記録保持が容易に
- v1.82.11 (2025-11-07): 動的境界検出の可視化対応 🔍
  * 動的境界検出の結果をログに表示
    - 固定ratioと検出ratioの比較を表示（例: [動的検出: 0.35 → 0.42]）
    - 検出値が固定値から0.01以上変わった場合のみ表示
  * カタログにused_ratioフィールドを追加
    - 実際に使用された分割比率を記録
    - 将来的な分析と最適化に活用可能
  * 偏旁抽出ツールのタイトルをv2.9に更新
    - 起動時に動的検出の設定状態を表示
    - 探索範囲とスキャンステップをログに出力
  * extract_single_part関数の戻り値にused_ratioを追加
- v1.82.10 (2025-11-06): 修正版 - 動的境界検出とクリップボード貼り付け 🔧
  * 動的境界検出をデフォルトで有効化（DYNAMIC_BOUNDARY_DETECTION = True）
  * PartTransformDialogの初期化バグを修正（current_transformedが未定義の問題）
  * クリップボード貼り付けのデバッグログを追加
- v1.82.9 (2025-11-06): 偏旁抽出ツールの大幅強化 🎯
  * 動的境界検出アルゴリズムを統合（オプション機能）
    - 画像解析で最適な分割位置を自動算出
    - 固定ratio値に加えて、文字ごとに最適化された値を提案
    - 「波」のような接触文字でも高精度な抽出が可能
    - 密度スキャン + エッジ検出による総合スコアリング
  * 文字存在チェックとフォールバック機能
    - フォントに文字が存在しない場合、自動的に代替文字を使用
    - 各偏旁に複数の代替サンプル文字を定義
    - 抽出失敗時の自動リトライで成功率向上
  * PARTS_CATALOGの拡張
    - 各エントリに代替サンプル文字リスト（alternatives）を追加
    - より多様なフォントに対応可能に
  * 偏旁抽出の成功率向上とログ改善
    - 詳細な抽出ログ（使用した文字、ratio値、動的検出結果）
    - フォールバック時の明示的な通知
  ※既存機能は完全に保持。動的検出はオプションとして追加。
  ※GUI操作は変更なし。内部的に自動で最適化。

- v1.82.8 (2025-11-06): 主要機能追加
  * TTCファイル（TrueType Collection）の読み込みに対応
    - fontToolsを使用してTTCから個別フォントを抽出
    - 複数フォントを含むTTCファイルから選択可能
  * 偏旁貼り付けプレビュー機能を実装
    - 貼り付け前に半透明でプレビュー表示
    - マウスドラッグで配置位置を自由に調整
    - クリックで確定、Escキーでキャンセル
    - リアルタイムで位置を確認しながら配置
  * 偏旁の変形機能を追加
    - 貼り付け時に拡大縮小スライダー (25%〜200%)
    - 縦横比の個別調整（幅・高さを独立して変更）
    - プレビューを見ながら調整可能
  * プロジェクト保存の最適化
    - 差分保存: 変更されたグリフのみ保存
    - 自動保存: 設定可能な間隔で自動保存（デフォルト5分）
    - バックアップ世代管理: 最大10世代まで保持
    - 保存時間の大幅短縮

- v1.82.7 (2025-11-06): テストフィードバックに基づく重要な修正
  * 偏旁パレット貼り付けの透過処理を修正
    - ImageChops.darkerを使用して黒い部分のみ貼り付け
    - 白い背景が透明として正しく扱われるように改善
    - 真っ黒な長方形が貼り付けられる問題を解決
  * プロジェクト保存のファイル名サニタイズを実装
    - ファイルシステムで使えない文字を自動的に置換
    - /<>:"\|?* などを _ に変換
    - safe_filenameをメタデータに記録
    - 保存エラーを防止し、詳細なログを出力
  * 偏旁抽出ツールの解像度を確認
    - render_char_to_bitmap は既に2048x2048を使用
    - 文字レンダリングと同じ高解像度を維持

- v1.82.6 (2025-11-06): バックグラウンド読み込み進捗表示の改善とバグ修正
  * バックグラウンド読み込み時にカテゴリ名と進捗を表示
    - 現在読み込み中のカテゴリ名を表示
    - カテゴリごとの進捗率と全体の進捗率を表示
    - 例: "読み込み中 [2/24] ひらがな (45%) - 全体 15%"
  * 偏旁パレットの「貼付」ボタンをクリップボード経由に変更
    - プロジェクトのクリップボードに偏旁画像をコピー
    - 文字編集ウィンドウで通常の貼り付け操作で使用可能
  * プロジェクト保存機能の検証と修正
    - partsデータの保存・読み込みが正しく動作することを確認
    - カテゴリ情報を含むメタデータの保存を確認

- v1.82.5 (2025-11-05): フォント読み込み方式の改善
  * 基本ラテン文字を先に読み込み、すぐに作業開始可能に
  * 残りの文字範囲はバックグラウンドで読み込み
  * 元のv1.81.pyの仕様に戻す
  * バックグラウンド読み込み中もステータスバーで進捗表示
  * スレッドベースの実装で、UI操作をブロックしない

- v1.82.4 (2025-11-05): 重要なバグ修正3点
  * 偏旁パレットの「貼付」ボタンを実装
    - _insert_part_to_active_editor関数を追加
    - 開いているGlyphEditorに偏旁を挿入
    - クリップボード経由ではなく直接貼り付け
  * プロジェクト保存時にparts_catalog.jsonを保存
    - metaフィールド（カテゴリ等）を含めて保存
    - プロジェクト再読み込み時にカテゴリ情報を維持

- v1.82.3 (2025-11-05): 偏旁パレットのカテゴリ分類機能追加
  * 偏旁パレットをタブUIに変更（偏・旁・冠・脚・繞・垂・構）
  * 各タブに該当する偏旁のみを表示
  * 偏旁抽出時にカテゴリ情報をcatalog.jsonに保存
  * 取り込み時にカテゴリ情報を正しく読み込み
  * 配置情報（左・右・上・下など）を表示
  * 視認性向上のため各偏旁アイテムに枠を追加

- v1.82.2 (2025-11-05): 偏旁取り込み機能の改善
  * 「本体へ取り込み」ボタンでフォルダ選択ダイアログを表示
  * 取り込み元フォルダをユーザーが選択できるように改善
  * .pngファイルの有無を確認して警告を表示
  * 取り込み完了メッセージにフォルダパスを表示

- v1.82.1 (2025-11-05): バグ修正
  * 偏旁抽出ツールの「本体へ取り込み」機能が動作しない問題を修正
  * 古い実装が新しい実装を上書きしていたバインディングを修正（4857-4858行目）
  * 取り込み完了時に件数を表示するメッセージが正しく表示されるように修正

- v1.82 (2025-11-05): コード整理とブラッシュアップ
  * 重複コード削除（9362行→6408行、31.5%削減）
  * Block構造明確化（本体BLOCK1-12、オプションOPTION1）
  * Block間隔を10行以上に統一
  * ハードコード値のConfig定数化
  * メインエントリポイント統合
  * 全機能維持（削減なし）
"""

# ========================================
# インポート（標準ライブラリ）
# ========================================
import os
import sys
import json
import threading
import tempfile
import shutil
import zipfile
import time
import datetime
from pathlib import Path
from types import MethodType
import numpy as np  # v1.82.9: 動的境界検出用

# ========================================
# インポート（サードパーティライブラリ）
# ========================================
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageTk
from typing import Optional, List, Tuple, Set, Dict, Any, Callable

# fontTools for TTC support (optional)
try:
    from fontTools.ttLib import TTCollection, TTFont
    FONTTOOLS_AVAILABLE = True
except ImportError:
    FONTTOOLS_AVAILABLE = False











# ################################################################################
# ■■■ 本体部分 - BLOCK 1-12 ■■■
# ################################################################################











# ===== [本体 BLOCK1-BEGIN] コンフィグ・定数定義 (2025-10-17: 高解像度対応・フォント制作最適化) =====

class Config:
    """エディタ設定"""
    
    # ===== 解像度設定 (2025-10-17: 高品質フォント制作用に2048px) =====
    CANVAS_SIZE = 2048  # 編集キャンバスサイズ (px) - 高品質フォント制作用
    GRID_THUMB_SIZE = 128  # グリッド表示時のサムネイルサイズ
    TARGET_DPI = 300  # 目標DPI
    
    # ===== フォントレンダリング設定 (2025-10-17: 2048px用に最適化) =====
    FONT_RENDER_SIZE = 2048  # 2048pxキャンバス用の最適フォントサイズ (約88%使用)
    MIN_BLACK_PIXELS = 50  # ブランクグリフ判定の最小黒ピクセル数
    
    # ===== PNG書き出し設定 (2025-10-17: デフォルト2048px) =====
    DEFAULT_PNG_EXPORT_SIZE = 2048  # PNG書き出し時のデフォルトサイズ
    
    # ===== TTF書き出し設定 =====
    ASCENT_RATIO = 0.8  # アセント比率
    DESCENT_RATIO = 0.2  # ディセント比率
    NOTDEF_MARGIN_RATIO = 0.1  # .notdefグリフの外枠マージン比率
    NOTDEF_INNER_MARGIN_RATIO = 0.15  # .notdefグリフの内枠マージン比率
    
    # ===== ウィンドウ設定 =====
    WINDOW_WIDTH = 1400  # メインウィンドウ幅
    WINDOW_HEIGHT = 900  # メインウィンドウ高さ
    
    # ===== グリッド表示設定 =====
    GRID_COLUMNS = 8  # グリッド表示の列数
    
    # ===== デフォルト設定 =====
    DEFAULT_RANGE = '基本ラテン文字 (ASCII)'  # デフォルト文字範囲
    
    # ===== 文字コード範囲プリセット =====
    CHAR_RANGES = {
        '基本ラテン文字 (ASCII)': (0x0020, 0x007F),  # 95文字
        'ラテン補助文字': (0x0080, 0x00FF),  # 128文字
        'ひらがな': (0x3040, 0x309F),  # 96文字
        'カタカナ': (0x30A0, 0x30FF),  # 96文字
        # 漢字を500文字単位に細分化
        '漢字 1/20 (一～乞)': (0x4E00, 0x4FFF),  # 512文字
        '漢字 2/20 (乢～你)': (0x5000, 0x51FF),  # 512文字
        '漢字 3/20 (倀～傿)': (0x5200, 0x53FF),  # 512文字
        '漢字 4/20 (僀～势)': (0x5400, 0x55FF),  # 512文字
        '漢字 5/20 (匀～呿)': (0x5600, 0x57FF),  # 512文字
        '漢字 6/20 (唀～哿)': (0x5800, 0x59FF),  # 512文字
        '漢字 7/20 (喀～嗿)': (0x5A00, 0x5BFF),  # 512文字
        '漢字 8/20 (嘀～囿)': (0x5C00, 0x5DFF),  # 512文字
        '漢字 9/20 (圀～夿)': (0x5E00, 0x5FFF),  # 512文字
        '漢字 10/20 (央～奿)': (0x6000, 0x61FF),  # 512文字
        '漢字 11/20 (妀～嫿)': (0x6200, 0x63FF),  # 512文字
        '漢字 12/20 (嬀～尿)': (0x6400, 0x65FF),  # 512文字
        '漢字 13/20 (局～峿)': (0x6600, 0x67FF),  # 512文字
        '漢字 14/20 (崀～帿)': (0x6800, 0x69FF),  # 512文字
        '漢字 15/20 (幀～廿)': (0x6A00, 0x6BFF),  # 512文字
        '漢字 16/20 (开～忿)': (0x6C00, 0x6DFF),  # 512文字
        '漢字 17/20 (怀～懿)': (0x6E00, 0x6FFF),  # 512文字
        '漢字 18/20 (戀～揿)': (0x7000, 0x71FF),  # 512文字
        '漢字 19/20 (搀～政)': (0x7200, 0x73FF),  # 512文字
        '漢字 20/20 (收～瓿)': (0x7400, 0x77FF),  # 1024文字
        'CJK統合漢字拡張A': (0x3400, 0x4DBF),  # 6,592文字
        '記号・約物': (0x2000, 0x206F),  # 112文字
        '全角記号': (0xFF00, 0xFFEF),  # 240文字
        '数学記号': (0x2200, 0x22FF),  # 256文字
        '矢印': (0x2190, 0x21FF),  # 112文字
        'ギリシャ文字': (0x0370, 0x03FF),  # 144文字
        'キリル文字': (0x0400, 0x04FF),  # 256文字
        '絵文字1': (0x1F300, 0x1F5FF),  # 768文字
        '絵文字2': (0x1F600, 0x1F64F),  # 80文字
    }
    
    # ===== UI設定 =====
    COLOR_BG = '#F0F0F0'  # 背景色
    COLOR_ACTIVE = '#ADD8E6'  # アクティブボタン色
    COLOR_CANVAS = '#FFFFFF'  # キャンバス背景色
    COLOR_EMPTY = '#FFE0E0'  # 空グリフ背景色
    
    # グリッド設定 (2025-10-17: 2048px用に調整)
    GRID_SPACING = 64  # グリッド線の間隔 (px) - 2048/32 = 64px間隔
    GRID_COLOR = '#E0E0E0'  # グリッド線の色
    GRID_CENTER_COLOR = '#FF0000'  # 中央線の色
    
    # ナビゲーション設定
    NAV_SIZE = 150  # ナビゲーションウィンドウのサイズ

    # [OPTIMIZATION] キャッシュ設定
    MAX_UNDO_STACK = 50  # アンドゥ履歴の最大数
    PROGRESS_UPDATE_INTERVAL = 10  # プログレスバー更新間隔（文字数）

    # ===== 自動保存・バックアップ設定 (2025-11-06) =====
    AUTO_SAVE_ENABLED = True  # 自動保存を有効にする
    AUTO_SAVE_INTERVAL = 300  # 自動保存間隔（秒）デフォルト5分
    MAX_BACKUP_GENERATIONS = 10  # 保持するバックアップ世代数
    DIFFERENTIAL_SAVE = True  # 差分保存を有効にする

    # ===== 偏旁抽出: 動的境界検出設定 (2025-11-06) =====
    DYNAMIC_BOUNDARY_DETECTION = True  # 動的境界検出を有効にする（実験的機能）
    BOUNDARY_SEARCH_RANGE_LR = (0.25, 0.75)  # 左右分割の探索範囲
    BOUNDARY_SEARCH_RANGE_TB = (0.25, 0.75)  # 上下分割の探索範囲
    BOUNDARY_SCAN_STEP = 0.02  # スキャンステップ（2%刻み）
    BINARY_THRESHOLD = 200  # 二値化閾値

# ===== [本体 BLOCK1-END] =====











# ===== [本体 BLOCK2-BEGIN] データモデル (2025-01-15: 異体字マッピング機能追加) =====

class GlyphData:
    """1文字分のグリフデータ"""
    
    def __init__(self, char_code: int, bitmap: Optional[Image.Image] = None, is_edited: bool = False):
        self.char_code = char_code
        self.bitmap = bitmap
        self.is_empty = bitmap is None
        self.is_edited = is_edited
        self.mapping_char = None  # [ADD] 2025-01-15: 読みマッピング
    
    def get_char(self) -> str:
        """文字コードから文字を取得"""
        # [ADD] 2025-01-15: マッピング文字があればそれを返す
        if self.mapping_char:
            return self.mapping_char
        try:
            return chr(self.char_code)
        except ValueError:
            return ''
    
    def get_code_label(self) -> str:
        """U+XXXX形式のラベル取得"""
        # [ADD] 2025-01-15: マッピング表示
        label = f'U+{self.char_code:04X}'
        if self.mapping_char:
            label += f' [{self.mapping_char}]'
        return label
    
    def set_mapping(self, char: str) -> None:
        """読みマッピングを設定 (2025-01-15: 新規追加)"""  # [ADD]
        self.mapping_char = char if char else None
    
    def get_mapping(self) -> Optional[str]:
        """読みマッピングを取得 (2025-01-15: 新規追加)"""  # [ADD]
        return self.mapping_char


class FontProject:
    """フォントプロジェクト管理"""
    
    def __init__(self):
        self.glyphs: Dict[int, GlyphData] = {}
        self.font_path: Optional[str] = None
        self.original_ttf_path: Optional[str] = None
        self.char_range: Tuple[int, int] = Config.CHAR_RANGES[Config.DEFAULT_RANGE]
        self.clipboard: Optional[Image.Image] = None
        self.loaded_ranges: Set[Tuple[int, int]] = set()
        self._lock = threading.Lock()
        self.glyph_mappings: Dict[int, str] = {}  # [ADD] 2025-01-15: 異体字マッピング

        # [ADD] 2025-10-23: 偏旁エディタ統合用のパーツ辞書。
        # キーは偏旁名、値は辞書 { 'image': Image.Image, 'meta': dict } を想定。
        self.parts: Dict[str, Dict[str, Any]] = {}

        # [ADD] 2025-11-06: 自動保存・差分保存用
        self.project_path: Optional[str] = None  # プロジェクトの保存先パス
        self.last_saved_time: Optional[float] = None  # 最後に保存した時刻
        self.saved_glyphs_hash: Dict[int, int] = {}  # 保存時のグリフハッシュ（差分検出用）

    @property
    def dirty(self) -> bool:
        """未保存判定"""
        try:
            return any(getattr(g, 'is_edited', False) for g in self.glyphs.values())
        except Exception:
            return False

    def create_backup(self, project_path: str) -> Optional[str]:
        """
        バックアップを作成

        Args:
            project_path: プロジェクトフォルダのパス

        Returns:
            バックアップファイルのパス、失敗時はNone
        """
        if not os.path.exists(project_path):
            return None

        try:
            # バックアップディレクトリを作成
            backup_dir = os.path.join(os.path.dirname(project_path), '.backups')
            os.makedirs(backup_dir, exist_ok=True)

            # タイムスタンプ付きバックアップ名
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            project_name = os.path.basename(project_path)
            backup_name = f'{project_name}_backup_{timestamp}'
            backup_path = os.path.join(backup_dir, backup_name)

            # プロジェクトをコピー
            shutil.copytree(project_path, backup_path)

            # 古いバックアップを削除（世代管理）
            self._cleanup_old_backups(backup_dir, project_name)

            return backup_path

        except Exception as e:
            print(f'バックアップ作成エラー: {e}')
            return None

    def _cleanup_old_backups(self, backup_dir: str, project_name: str):
        """古いバックアップを削除"""
        try:
            # バックアップファイル一覧を取得
            backups = []
            for name in os.listdir(backup_dir):
                if name.startswith(f'{project_name}_backup_'):
                    path = os.path.join(backup_dir, name)
                    if os.path.isdir(path):
                        mtime = os.path.getmtime(path)
                        backups.append((mtime, path))

            # 新しい順にソート
            backups.sort(reverse=True)

            # 古いものを削除
            for _, path in backups[Config.MAX_BACKUP_GENERATIONS:]:
                shutil.rmtree(path, ignore_errors=True)
                print(f'古いバックアップを削除: {os.path.basename(path)}')

        except Exception as e:
            print(f'バックアップクリーンアップエラー: {e}')

    def save_project(self, folder_path: str, differential: Optional[bool] = None):
        """プロジェクト保存（*.fproj）

        Args:
            folder_path: 保存先フォルダ
            differential: 差分保存するか（Noneの場合はConfig設定を使用）
        """
        import os, json
        import hashlib

        if differential is None:
            differential = Config.DIFFERENTIAL_SAVE

        os.makedirs(folder_path, exist_ok=True)
        os.makedirs(os.path.join(folder_path, 'glyphs'), exist_ok=True)

        # [ADD] 2025-01-15: マッピング情報を保存
        mappings = {}
        for code, glyph in self.glyphs.items():
            if hasattr(glyph, 'mapping_char') and glyph.mapping_char:
                mappings[code] = glyph.mapping_char

        meta = {
            'font_path': getattr(self, 'font_path', None),
            'original_ttf_path': getattr(self, 'original_ttf_path', None),
            'char_range': list(getattr(self, 'char_range', (0,0))),
            'edited_codes': [code for code, g in self.glyphs.items() if getattr(g, 'is_edited', False)],
            'glyph_mappings': mappings  # [ADD] 2025-01-15
        }
        with open(os.path.join(folder_path, 'metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        # [ADD] 2025-11-06: 差分保存対応
        saved_count = 0
        skipped_count = 0

        for code, g in self.glyphs.items():
            bmp = getattr(g, 'bitmap', None)
            if bmp is None:
                continue

            fn = os.path.join(folder_path, 'glyphs', f'U+{code:04X}.png')

            # 差分保存: 変更されたグリフのみ保存
            if differential and code in self.saved_glyphs_hash:
                # ハッシュを計算して比較
                img_hash = hashlib.md5(bmp.tobytes()).hexdigest()
                if img_hash == self.saved_glyphs_hash.get(code):
                    skipped_count += 1
                    continue  # 変更なし、スキップ

            bmp.save(fn, 'PNG')
            saved_count += 1

            # ハッシュを保存
            if differential:
                self.saved_glyphs_hash[code] = hashlib.md5(bmp.tobytes()).hexdigest()

        # 保存時刻を記録
        self.last_saved_time = time.time()
        self.project_path = folder_path

        if differential and skipped_count > 0:
            print(f'差分保存: {saved_count}個保存, {skipped_count}個スキップ')

        # [ADD] 2025-10-23: 偏旁エディタ用パーツデータを保存
        # [FIX] 2025-11-06: ファイル名サニタイズとエラーハンドリング改善
        if getattr(self, 'parts', None):
            parts_dir = os.path.join(folder_path, 'parts')
            os.makedirs(parts_dir, exist_ok=True)
            parts_meta = {}
            import re

            for name, info in self.parts.items():
                img = info.get('image')
                meta = info.get('meta', {})
                if img is None:
                    continue

                # ファイル名をサニタイズ（ファイルシステムで使えない文字を置換）
                # /<>:"\|?* などを _ に置換
                safe_name = re.sub(r'[/<>:\"\\|?*\x00-\x1f]', '_', name)
                # 連続するアンダースコアを1つに
                safe_name = re.sub(r'_+', '_', safe_name)
                # 先頭・末尾のアンダースコアを削除
                safe_name = safe_name.strip('_')
                # 空になった場合は代替名を使用
                if not safe_name:
                    safe_name = f'part_{hash(name) & 0xFFFFFFFF:08x}'

                part_fn = os.path.join(parts_dir, f'{safe_name}.png')
                try:
                    img.save(part_fn, 'PNG')
                    # メタデータには元の名前をキーとして保存
                    parts_meta[name] = {
                        **meta,
                        'safe_filename': safe_name  # 安全なファイル名も記録
                    }
                except Exception as e:
                    # 失敗した場合は詳細をログに記録
                    print(f'警告: パーツ "{name}" の保存に失敗: {e}')
                    continue

            # 偏旁のメタデータをJSONで保存
            if parts_meta:
                with open(os.path.join(parts_dir, 'metadata.json'), 'w', encoding='utf-8') as pf:
                    json.dump(parts_meta, pf, ensure_ascii=False, indent=2)

    def load_project(self, folder_path: str):
        """プロジェクト読込"""
        import os, json
        with open(os.path.join(folder_path, 'metadata.json'), 'r', encoding='utf-8') as f:
            meta = json.load(f)
        self.font_path = meta.get('font_path')
        self.original_ttf_path = meta.get('original_ttf_path')
        cr = meta.get('char_range')
        if isinstance(cr, list) and len(cr) == 2:
            self.char_range = (int(cr[0]), int(cr[1]))
        
        # [ADD] 2025-01-15: マッピング情報を読込
        self.glyph_mappings = {}
        mappings = meta.get('glyph_mappings', {})
        
        self.glyphs.clear()
        edited = set(meta.get('edited_codes', []))
        glyph_dir = os.path.join(folder_path, 'glyphs')
        if os.path.isdir(glyph_dir):
            for name in os.listdir(glyph_dir):
                if not name.lower().endswith('.png'):
                    continue
                try:
                    codepoint = int(name[2:6], 16)
                except Exception:
                    continue
                img = Image.open(os.path.join(glyph_dir, name)).convert('L')
                glyph = GlyphData(codepoint, img, is_edited=(codepoint in edited))
                
                # [ADD] 2025-01-15: マッピングを設定
                if str(codepoint) in mappings:
                    glyph.set_mapping(mappings[str(codepoint)])
                
                self.glyphs[codepoint] = glyph

        # [ADD] 2025-10-23: 偏旁エディタ用パーツデータを読み込む
        # [FIX] 2025-11-06: サニタイズされたファイル名に対応
        # 保存時に parts ディレクトリに保存されていれば読み出す
        self.parts = {}
        parts_dir = os.path.join(folder_path, 'parts')
        if os.path.isdir(parts_dir):
            # メタデータを読み込む
            meta_path = os.path.join(parts_dir, 'metadata.json')
            parts_meta = {}
            if os.path.isfile(meta_path):
                try:
                    with open(meta_path, 'r', encoding='utf-8') as pf:
                        parts_meta = json.load(pf)
                except Exception:
                    parts_meta = {}

            # メタデータから読み込む（safe_filenameを使用）
            if isinstance(parts_meta, dict) and parts_meta:
                for original_name, meta_info in parts_meta.items():
                    if not isinstance(meta_info, dict):
                        continue

                    # safe_filenameがあればそれを使用、なければ元の名前を使用
                    safe_name = meta_info.get('safe_filename', original_name)
                    img_path = os.path.join(parts_dir, f'{safe_name}.png')

                    if not os.path.exists(img_path):
                        continue

                    try:
                        img = Image.open(img_path).convert('L')
                        # 元の名前をキーとして保存
                        self.parts[original_name] = {'image': img, 'meta': meta_info}
                    except Exception as e:
                        print(f'警告: パーツ "{original_name}" の読み込みに失敗: {e}')
                        continue
            else:
                # 古い形式の場合はファイル名から直接読み込む
                for fname in os.listdir(parts_dir):
                    if not fname.lower().endswith('.png'):
                        continue
                    part_name = os.path.splitext(fname)[0]
                    img_path = os.path.join(parts_dir, fname)
                    try:
                        img = Image.open(img_path).convert('L')
                        self.parts[part_name] = {'image': img, 'meta': {}}
                    except Exception:
                        continue

    def set_range(self, range_name: str):
        """文字範囲を設定（表示フィルタのみ、データは保持）"""
        if range_name in Config.CHAR_RANGES:
            self.char_range = Config.CHAR_RANGES[range_name]
    
    def get_char_codes(self) -> list:
        """現在の範囲の文字コードリストを取得"""
        start, end = self.char_range
        return list(range(start, end + 1))
    
    def get_empty_count(self) -> int:
        """空白グリフ数をカウント（現在の範囲のみ）"""
        return sum(1 for code in self.get_char_codes() 
                  if code in self.glyphs and self.glyphs[code].is_empty)
    
    def set_glyph(self, char_code: int, bitmap: Image.Image, is_edited: bool = False):
        """グリフを設定"""
        glyph = GlyphData(char_code, bitmap, is_edited)
        # [ADD] 2025-01-15: 既存のマッピングを保持
        if char_code in self.glyphs and hasattr(self.glyphs[char_code], 'mapping_char'):
            glyph.set_mapping(self.glyphs[char_code].mapping_char)
        self.glyphs[char_code] = glyph
    
    def set_glyph_mapping(self, char_code: int, mapping_char: str):
        """グリフにマッピングを設定 (2025-01-15: 新規追加)"""  # [ADD]
        if char_code in self.glyphs:
            self.glyphs[char_code].set_mapping(mapping_char)
            self.glyph_mappings[char_code] = mapping_char
        else:
            # グリフが存在しない場合は空のグリフを作成
            glyph = GlyphData(char_code, None, False)
            glyph.set_mapping(mapping_char)
            self.glyphs[char_code] = glyph
            self.glyph_mappings[char_code] = mapping_char
    
    def mark_as_edited(self, char_code: int):
        """グリフを編集済みとしてマーク"""
        if char_code in self.glyphs:
            self.glyphs[char_code].is_edited = True
    
    def get_edited_glyphs(self) -> list:
        """編集済みグリフのリストを取得"""
        return [(code, glyph) for code, glyph in self.glyphs.items() 
                if not glyph.is_empty and glyph.is_edited]
    
    def is_range_loaded(self, range_tuple: Tuple[int, int]) -> bool:
        """指定範囲が読み込み済みか確認"""
        return range_tuple in self.loaded_ranges
    
    def mark_range_loaded(self, range_tuple: Tuple[int, int]):
        """範囲を読み込み済みとしてマーク"""
        self.loaded_ranges.add(range_tuple)

# ===== [本体 BLOCK2-END] =====











# ===== [本体 BLOCK3-BEGIN] フォント読み込み・レンダリング (2025-10-11: 型ヒント追加、定数使用) =====

# ===== TTC File Support Utilities (2025-11-06) =====

def extract_ttf_from_ttc(ttc_path: str, output_dir: Optional[str] = None) -> Optional[str]:
    """
    TTCファイルから最初のTTFを抽出

    Args:
        ttc_path: TTCファイルのパス
        output_dir: 出力先ディレクトリ（Noneの場合は一時ディレクトリ）

    Returns:
        抽出されたTTFファイルのパス、失敗時はNone
    """
    if not FONTTOOLS_AVAILABLE:
        messagebox.showerror(
            'エラー',
            'TTCファイルの読み込みには fontTools ライブラリが必要です。\n\n'
            'インストール方法:\n'
            'pip install fonttools'
        )
        return None

    try:
        ttc = TTCollection(ttc_path)

        # 複数フォントがある場合は選択ダイアログを表示
        if len(ttc.fonts) > 1:
            font_names = []
            for i, font in enumerate(ttc.fonts):
                try:
                    name = font['name'].getDebugName(4)  # Full font name
                    if not name:
                        name = f"Font {i+1}"
                except:
                    name = f"Font {i+1}"
                font_names.append(name)

            # 選択ダイアログ
            dialog = tk.Toplevel()
            dialog.title("フォントを選択")
            dialog.geometry("400x300")
            dialog.transient()
            dialog.grab_set()

            selected_index = tk.IntVar(value=0)

            tk.Label(dialog, text="TTCファイルに複数のフォントが含まれています。\n使用するフォントを選択してください:",
                    pady=10).pack()

            listbox = tk.Listbox(dialog, height=10)
            for name in font_names:
                listbox.insert(tk.END, name)
            listbox.select_set(0)
            listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            def on_ok():
                selection = listbox.curselection()
                if selection:
                    selected_index.set(selection[0])
                dialog.destroy()

            tk.Button(dialog, text="OK", command=on_ok, width=10).pack(pady=10)

            dialog.wait_window()
            font_index = selected_index.get()
        else:
            font_index = 0

        # TTFを抽出
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="ttc_extract_")

        output_path = os.path.join(output_dir, f"extracted_font_{font_index}.ttf")
        ttc.fonts[font_index].save(output_path)

        return output_path

    except Exception as e:
        messagebox.showerror('エラー', f'TTCファイルの読み込みに失敗しました:\n{e}')
        return None

class FontRenderer:
    """フォントレンダリング処理"""
    
    @staticmethod
    def load_font(
        font_path: str, 
        char_codes: List[int], 
        project: FontProject, 
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> bool:
        """フォントを読み込んで各文字をレンダリング (2025-10-11: 型ヒント追加)"""
        try:
            # PIL ImageFontでフォント読み込み (2025-10-11: 定数使用)
            pil_font = ImageFont.truetype(font_path, size=Config.FONT_RENDER_SIZE)
            
            # 元のTTFパスを保存（マージ用）
            if not project.original_ttf_path:
                project.original_ttf_path = font_path
            
            total = len(char_codes)
            
            for idx, code in enumerate(char_codes):
                # 既に手動編集されたグリフはスキップ (2025-10-03)
                if code in project.glyphs and not project.glyphs[code].is_empty:
                    # プログレス更新のみ
                    if progress_callback and idx % Config.PROGRESS_UPDATE_INTERVAL == 0:
                        progress_callback(idx + 1, total)
                    continue  # スキップ
                
                try:
                    char = chr(code)
                    
                    # 文字をレンダリング
                    bitmap = FontRenderer._render_char(char, pil_font)
                    
                    if bitmap:
                        project.set_glyph(code, bitmap, is_edited=False)  # 未編集としてマーク
                    else:
                        # 空グリフとして登録（既存がなければ）
                        with project._lock:  # (2025-10-11: スレッドセーフ化)
                            if code not in project.glyphs:
                                project.glyphs[code] = GlyphData(code, None, False)
                        
                except (ValueError, OSError):
                    # レンダリング失敗は空グリフ
                    with project._lock:  # (2025-10-11: スレッドセーフ化)
                        if code not in project.glyphs:
                            project.glyphs[code] = GlyphData(code, None, False)
                
                # プログレス更新 (2025-10-03: 10文字ごとに更新)
                if progress_callback and idx % Config.PROGRESS_UPDATE_INTERVAL == 0:
                    progress_callback(idx + 1, total)
                    
            # 最終プログレス
            if progress_callback:
                progress_callback(total, total)
            
            project.font_path = font_path
            return True
            
        except Exception as e:
            messagebox.showerror("読み込みエラー", f"フォント読み込み失敗:\n{e}")
            return False
    
    @staticmethod
    def _render_char(char: str, font: ImageFont.FreeTypeFont) -> Optional[Image.Image]:
        """1文字をビットマップ化 (2025-10-11: 定数使用)"""
        try:
            # バウンディングボックス取得
            bbox = font.getbbox(char)
            if bbox[2] - bbox[0] == 0 or bbox[3] - bbox[1] == 0:
                return None  # 空グリフ
            
            # 768x768キャンバス作成
            canvas = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
            draw = ImageDraw.Draw(canvas)
            
            # 中央配置計算
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x = (Config.CANVAS_SIZE - w) // 2 - bbox[0]
            y = (Config.CANVAS_SIZE - h) // 2 - bbox[1]
            
            # 描画
            draw.text((x, y), char, font=font, fill=0)
            
            # ブランクグリフ検出（枠だけで中身が空白の場合）
            pixels = canvas.load()
            black_pixels = sum(1 for py in range(Config.CANVAS_SIZE)
                             for px in range(Config.CANVAS_SIZE)
                             if pixels[px, py] < 128)
            
            # 黒ピクセルが少なすぎる場合はブランクグリフと判定 (2025-10-11: 定数使用)
            if black_pixels < Config.MIN_BLACK_PIXELS:
                return None
            
            return canvas
            
        except Exception:
            return None

# ===== [本体 BLOCK3-END] =====











# ===== [本体 BLOCK4-BEGIN] グリッドビューGUI (2025-01-15: マッピング機能追加、PhotoImage参照保持改善、型ヒント追加) =====

class GridView(tk.Frame):
    """グリッド一覧表示"""
    
    def __init__(
        self, 
        parent: tk.Widget, 
        project: FontProject, 
        on_click_callback: Callable[[int], None]
    ) -> None:
        super().__init__(parent, bg=Config.COLOR_BG)
        self.project: FontProject = project
        self.on_click: Callable[[int], None] = on_click_callback
        self.thumb_cache: Dict[int, ImageTk.PhotoImage] = {}  # サムネイルキャッシュ
        self._photo_refs: List[ImageTk.PhotoImage] = []  # (2025-10-11: GC対策で明示的リスト保持)
        
        # スクロール可能なキャンバス
        self.canvas = tk.Canvas(self, bg=Config.COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=Config.COLOR_BG)
        
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # マウスホイールスクロール対応 (2025-10-03: 修正)
        self.canvas.bind('<MouseWheel>', self._on_mousewheel)  # Windows/Mac
        self.canvas.bind('<Button-4>', self._on_mousewheel)  # Linux上スクロール
        self.canvas.bind('<Button-5>', self._on_mousewheel)  # Linux下スクロール
        self.scrollable_frame.bind('<MouseWheel>', self._on_mousewheel)
        self.scrollable_frame.bind('<Button-4>', self._on_mousewheel)
        self.scrollable_frame.bind('<Button-5>', self._on_mousewheel)
        
        self.filter: str = 'all'  # 初期フィルタ
    
    def _on_mousewheel(self, event: tk.Event) -> None:
        """マウスホイールでスクロール"""
        if event.num == 5 or event.delta < 0:
            # 下にスクロール
            self.canvas.yview_scroll(1, 'units')
        elif event.num == 4 or event.delta > 0:
            # 上にスクロール
            self.canvas.yview_scroll(-1, 'units')
    
    def set_filter(self, filter_type: str) -> None:
        """フィルタを設定して再描画"""
        self.filter = filter_type
        self.refresh()
    
    def refresh(self) -> None:
        """グリッド再描画 (2025-10-11: PhotoImage参照保持改善)"""
        # 既存ウィジェット削除
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.thumb_cache.clear()
        self._photo_refs.clear()  # (2025-10-11: 参照リストもクリア)
        
        # 固定列数を使用 (2025-10-04: 動的計算を削除)
        columns = Config.GRID_COLUMNS
        
        # グリッド生成
        char_codes = self.project.get_char_codes()
        
        # フィルタ適用
        filtered = []
        for code in char_codes:
            g = self.project.glyphs.get(code)
            if self.filter == 'all':
                filtered.append(code)
            elif self.filter == 'edited':
                if g and not g.is_empty and g.is_edited:
                    filtered.append(code)
            elif self.filter == 'unedited':
                if g and not g.is_empty and not g.is_edited:
                    filtered.append(code)
            elif self.filter == 'empty':
                if (g is None) or g.is_empty:
                    filtered.append(code)
            elif self.filter == 'defined':
                if g and not g.is_empty:
                    filtered.append(code)
        char_codes = filtered

        for idx, code in enumerate(char_codes):
            row = idx // columns
            col = idx % columns
            
            self._create_cell(code, row, col)
        
        # スクロール領域を更新
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def destroy(self) -> None:
        """ウィジェット破棄時の処理"""
        # 個別バインドは自動的に解除されるので、特別な処理不要
        super().destroy()
    
    def _create_cell(self, char_code: int, row: int, col: int) -> None:
        """1セル作成 (2025-01-15: マッピング表示対応)"""  # [ADD]
        frame = tk.Frame(
            self.scrollable_frame,
            bg=Config.COLOR_BG,
            relief='solid',
            borderwidth=1,
            padx=5,
            pady=5
        )
        frame.grid(row=row, column=col, padx=2, pady=2)
        
        # グリフデータ取得（存在しない場合は空グリフとして扱う）
        glyph = self.project.glyphs.get(char_code)
        
        if glyph and not glyph.is_empty:
            # サムネイル生成
            thumb = glyph.bitmap.resize(
                (Config.GRID_THUMB_SIZE, Config.GRID_THUMB_SIZE),
                Image.Resampling.LANCZOS
            )
            photo = ImageTk.PhotoImage(thumb)
            self.thumb_cache[char_code] = photo  # 辞書に保持
            self._photo_refs.append(photo)  # (2025-10-11: リストにも保持してGC防止)
            
            label = tk.Label(frame, image=photo, bg=Config.COLOR_BG)
            label.image = photo  # (2025-10-11: ラベル自体にも参照を持たせる)
        else:
            # 空グリフ (2025-10-03: 文字プレビュー追加)
            try:
                char_preview = chr(char_code)
                display_text = f'[空]\n{char_preview}'
            except ValueError:
                display_text = '[空]'
            
            label = tk.Label(
                frame,
                text=display_text,
                bg=Config.COLOR_EMPTY,
                width=10,
                height=5,
                font=('Arial', 20),
                relief='sunken'
            )
        
        label.pack()
        
        # 文字コードラベル + 文字表示 (2025-01-15: マッピング表示追加)  # [ADD]
        try:
            char_display = chr(char_code) if char_code < 0x10000 else ''
            label_text = f'U+{char_code:04X} {char_display}'
            
            # マッピングがある場合は表示
            if glyph and hasattr(glyph, 'mapping_char') and glyph.mapping_char:
                label_text += f'\n[{glyph.mapping_char}]'
                
        except ValueError:
            label_text = f'U+{char_code:04X}'
            if glyph and hasattr(glyph, 'mapping_char') and glyph.mapping_char:
                label_text += f'\n[{glyph.mapping_char}]'
        
        code_label = tk.Label(
            frame,
            text=label_text,
            bg=Config.COLOR_BG,
            font=('Arial', 8),
            fg='blue' if (glyph and hasattr(glyph, 'mapping_char') and glyph.mapping_char) else 'black'  # [ADD] マッピングがある場合は青色
        )
        code_label.pack()
        
        # クリックイベント
        frame.bind('<Button-1>', lambda e, c=char_code: self.on_click(c))
        label.bind('<Button-1>', lambda e, c=char_code: self.on_click(c))
        
        # 右クリックメニュー (2025-10-03)
        frame.bind('<Button-2>', lambda e, c=char_code: self._show_context_menu(e, c))
        label.bind('<Button-2>', lambda e, c=char_code: self._show_context_menu(e, c))
        # Windows/Mac用の右クリック
        frame.bind('<Button-3>', lambda e, c=char_code: self._show_context_menu(e, c))  # [ADD]
        label.bind('<Button-3>', lambda e, c=char_code: self._show_context_menu(e, c))  # [ADD]
    
    def _show_context_menu(self, event: tk.Event, char_code: int) -> None:
        """右クリックメニュー表示 (2025-01-15: マッピング機能追加)"""  # [ADD]
        menu = tk.Menu(self, tearoff=0)
        
        glyph = self.project.glyphs.get(char_code)
        
        if glyph and not glyph.is_empty:
            menu.add_command(
                label=f'U+{char_code:04X} をPNG保存',
                command=lambda: self._save_glyph_png(char_code)
            )
        
        menu.add_command(
            label='編集',
            command=lambda: self.on_click(char_code)
        )
        
        # [ADD] 2025-01-15: マッピング設定
        menu.add_separator()
        menu.add_command(
            label='読みマッピングを設定...',
            command=lambda: self._set_glyph_mapping(char_code)
        )
        
        if glyph and hasattr(glyph, 'mapping_char') and glyph.mapping_char:
            menu.add_command(
                label=f'マッピング解除 [{glyph.mapping_char}]',
                command=lambda: self._clear_glyph_mapping(char_code)
            )
        
        menu.tk_popup(event.x_root, event.y_root)
    
    def _save_glyph_png(self, char_code: int) -> None:
        """グリフをPNG保存"""
        glyph = self.project.glyphs.get(char_code)
        if glyph and not glyph.is_empty:
            default_name = f'U+{char_code:04X}.png'
            path = filedialog.asksaveasfilename(
                title='PNG保存',
                defaultextension='.png',
                initialfile=default_name,
                filetypes=[('PNG Image', '*.png'), ('All Files', '*.*')]
            )
            
            if path:
                glyph.bitmap.save(path)
                messagebox.showinfo('保存完了', f'保存しました:\n{path}')
    
    def _set_glyph_mapping(self, char_code: int) -> None:
        """グリフマッピングを設定 (2025-01-15: 新規追加)"""  # [ADD]
        dialog = tk.Toplevel(self)
        dialog.title('読みマッピング設定')
        dialog.geometry('300x150')
        dialog.transient(self)
        dialog.grab_set()  # モーダル化
        
        tk.Label(dialog, text=f'U+{char_code:04X} の読みを設定:', font=('Arial', 11)).pack(pady=10)
        
        # 現在の文字を表示
        try:
            current_char = chr(char_code)
            tk.Label(dialog, text=f'元の文字: {current_char}', font=('Arial', 10), fg='gray').pack()
        except ValueError:
            pass
        
        entry = tk.Entry(dialog, font=('Arial', 14), width=20)
        entry.pack(pady=10)
        
        # 既存のマッピングがあれば表示
        glyph = self.project.glyphs.get(char_code)
        if glyph and hasattr(glyph, 'mapping_char') and glyph.mapping_char:
            entry.insert(0, glyph.mapping_char)
        
        entry.focus()
        entry.select_range(0, tk.END)
        
        def apply():
            mapping = entry.get().strip()
            if mapping:
                self.project.set_glyph_mapping(char_code, mapping)
                self.refresh()
                dialog.destroy()
                messagebox.showinfo('設定完了', f'U+{char_code:04X} に「{mapping}」を設定しました')
            else:
                messagebox.showwarning('警告', '読みを入力してください')
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text='設定', command=apply, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text='キャンセル', command=dialog.destroy, width=10).pack(side='left', padx=5)
        
        entry.bind('<Return>', lambda e: apply())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    def _clear_glyph_mapping(self, char_code: int) -> None:
        """グリフマッピングをクリア (2025-01-15: 新規追加)"""  # [ADD]
        if messagebox.askyesno('確認', f'U+{char_code:04X} のマッピングを解除しますか？'):
            glyph = self.project.glyphs.get(char_code)
            if glyph:
                glyph.set_mapping(None)
                if char_code in self.project.glyph_mappings:
                    del self.project.glyph_mappings[char_code]
            self.refresh()
            messagebox.showinfo('解除完了', f'U+{char_code:04X} のマッピングを解除しました')

# ===== [本体 BLOCK4-END] =====











# ===== [本体 BLOCK5-BEGIN] 編集エディタGUI (2025-10-13: 基本部分) =====

class GlyphEditor(tk.Toplevel):
    """グリフ編集ウィンドウ(レイヤー方式テキスト挿入対応)"""
    
    def __init__(
        self, 
        parent: tk.Widget, 
        project: FontProject, 
        char_code: int, 
        on_save_callback: Callable[[], None]
    ) -> None:
        super().__init__(parent)
        self.project: FontProject = project
        self.char_code: int = char_code
        self.on_save: Callable[[], None] = on_save_callback
        self.glyph: Optional[GlyphData] = project.glyphs.get(char_code)
        
        # 編集用ビットマップ(作業用コピー) - ベースレイヤー
        if self.glyph and not self.glyph.is_empty:
            self.edit_bitmap: Image.Image = self.glyph.bitmap.copy()
        else:
            self.edit_bitmap: Image.Image = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
        
        # テキストレイヤー (2025-10-12: 新機能)
        self.text_layer: Optional[Image.Image] = None
        self.text_layer_pos: Tuple[int, int] = (0, 0)
        self.text_layer_original: Optional[Image.Image] = None  # リサイズ用の元画像
        self.is_text_mode: bool = False
        self.text_input_dialog: Optional[tk.Toplevel] = None

        # [ADD] 2025-10-22: グリッド表示フラグとエッジマスク
        # キャンバスの白・赤のグリッド線の表示を切り替えるためのフラグ。初期状態では非表示。
        self.grid_visible_var: tk.BooleanVar = tk.BooleanVar(value=False)
        # テキスト挿入時のエッジ領域をプレビューで表示するためのマスク画像。
        # エッジが存在しない場合やエッジ幅が0の場合はNoneとなる。
        self.text_edge_mask: Optional[Image.Image] = None

        # [ADD] コミット用のエッジマスク。エッジを透過に置き換える際に使用する。
        self.text_edge_mask_commit: Optional[Image.Image] = None

        # [ADD] 2025-10-23: エッジ形状設定 ('sharp' または 'round')
        self.edge_style_var: tk.StringVar = tk.StringVar(value='sharp')
        
        # アンドゥ・リドゥ用履歴
        self.undo_stack: List[Image.Image] = []
        self.redo_stack: List[Image.Image] = []
        self._save_to_undo()
        
        # 描画ツール状態
        self.current_tool: str = 'pen'
        self.brush_size: int = 5
        self.is_drawing: bool = False
        self.last_x: Optional[int] = None
        self.last_y: Optional[int] = None
        
        # 選択領域
        self.selection_start: Optional[Tuple[int, int]] = None
        self.selection_end: Optional[Tuple[int, int]] = None
        self.selection_rect: Optional[int] = None
        self.selected_image: Optional[Image.Image] = None

        # 移動操作用フラグと座標
        self.is_moving: bool = False
        self.move_start_offset: Optional[Tuple[int, int]] = None
        self.move_current_pos: Optional[Tuple[int, int]] = None

        # 拡大縮小操作用フラグと座標
        self.is_resizing: bool = False
        self.resize_origin: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        self.resize_handle: Optional[str] = None
        self.resize_start_point: Optional[Tuple[int, int]] = None
        self.resize_preview_rect: Optional[Tuple[int, int, int, int]] = None

        # 図形ツール用座標
        self.shape_start: Optional[Tuple[int, int]] = None
        self.shape_end: Optional[Tuple[int, int]] = None

        # ガイドライン保存
        self.guidelines: List[Tuple[str, int]] = []

        # ナビゲーション用キャンバスのPhotoImage保持
        self._move_photo: Optional[ImageTk.PhotoImage] = None
        self._resize_photo: Optional[ImageTk.PhotoImage] = None
        self._nav_photo: Optional[ImageTk.PhotoImage] = None
        self._text_layer_photo: Optional[ImageTk.PhotoImage] = None

        # 背景チェックパターンおよび表示用PhotoImage
        # パターンは遅延生成とする。_bg_patternはタイル用の小さなチェック柄、
        # _bg_fullはキャンバス全体サイズにタイル貼りした画像を保持する。
        self._bg_pattern: Optional[Image.Image] = None
        self._bg_full: Optional[Image.Image] = None
        self._bg_photo: Optional[ImageTk.PhotoImage] = None
        
        # ブラシカーソル
        self.brush_cursor: Optional[int] = None
        
        # ズーム機能
        self.zoom_level: float = 1.0
        self.zoom_levels: List[float] = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
        self.pan_offset: List[int] = [0, 0]
        self.is_panning: bool = False
        self.pan_start: Optional[Tuple[int, int]] = None
        
        # PhotoImage参照保持
        self.photo: Optional[ImageTk.PhotoImage] = None
        
        # ツールボタン管理
        self.tool_buttons: Dict[str, tk.Button] = {}
        
        # ドラッグ開始座標
        self.drag_start: Optional[Tuple[int, int]] = None
        
        # ハンドル描画用ID保存
        self.resize_handle_ids: List[int] = []
        
        self.title(f'編集: U+{char_code:04X}')
        self.geometry('1400x900')
        
        self._setup_ui()

        # 初期化時に背景パターンを生成
        # パターンサイズは8px単位で作成し、全体用のタイルも生成する
        # チェック柄のタイルサイズを大きくし、約30ピクセル四方の格子にする
        self._bg_pattern = self._create_bg_pattern(30)
        self._create_full_bg()

        # 初回プレビューを更新
        self._update_preview()

        # ウィンドウサイズに応じてズームレベルをフィットさせる
        # UI構築後に少し遅延させてキャンバスサイズが計算されてから調整する
        self.after(100, self._fit_zoom_to_window)
        
        # キーボードショートカット
        self.bind('<Control-s>', lambda e: self._save())
        self.bind('<Control-z>', lambda e: self._undo())
        self.bind('<Control-y>', lambda e: self._redo())
        self.bind('<Control-c>', lambda e: self._copy_selection())
        self.bind('<Control-x>', lambda e: self._cut_selection())
        self.bind('<Control-v>', lambda e: self._paste())
        self.bind('<Delete>', lambda e: self._delete_selection())
        self.bind('<Escape>', lambda e: self._clear_selection())
        self.bind('<KeyPress-space>', self._on_space_press)
        self.bind('<KeyRelease-space>', self._on_space_release)
        self.bind('<Control-0>', lambda e: self._reset_zoom())

        # 矢印キーによる1px単位移動
        self.bind('<Left>', lambda e: self._nudge(-1, 0))
        self.bind('<Right>', lambda e: self._nudge(1, 0))
        self.bind('<Up>', lambda e: self._nudge(0, -1))
        self.bind('<Down>', lambda e: self._nudge(0, 1))
    
    def _save_to_undo(self) -> None:
        """現在の状態をアンドゥスタックに保存"""
        self.undo_stack.append(self.edit_bitmap.copy())
        if len(self.undo_stack) > Config.MAX_UNDO_STACK:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    # ===== 背景チェックパターン関連 =====
    def _create_bg_pattern(self, tile_size: int = 30) -> Image.Image:
        """
        透過部分とキャンバス余白を見分けやすくするためのチェック柄を生成する。
        tile_sizeピクセル四方のタイルを2色で塗り分ける。
        少し濃淡の違うグレーを使用し、全体的に薄めのトーンにする。
        """
        # 2×2タイルを1つのパターンとして作成する
        pattern = Image.new('L', (tile_size * 2, tile_size * 2), 0)
        draw = ImageDraw.Draw(pattern)
        # 薄いグレーとやや濃いグレーを交互に塗り分ける
        light = 200
        dark = 180
        for by in range(2):
            for bx in range(2):
                color = light if (bx + by) % 2 == 0 else dark
                x0 = bx * tile_size
                y0 = by * tile_size
                x1 = x0 + tile_size
                y1 = y0 + tile_size
                draw.rectangle((x0, y0, x1 - 1, y1 - 1), fill=color)
        return pattern

    def _create_full_bg(self) -> None:
        """
        キャンバス全体サイズ(CANVAS_SIZE x CANVAS_SIZE)の背景パターン画像を生成する。
        すでに生成済みの場合は再生成しない。
        """
        if self._bg_pattern is None:
            # 後で生成される場合があるため、未設定なら何もしない
            return
        if self._bg_full is not None and self._bg_full.size == (Config.CANVAS_SIZE, Config.CANVAS_SIZE):
            return
        tile = self._bg_pattern
        w, h = Config.CANVAS_SIZE, Config.CANVAS_SIZE
        bg = Image.new('L', (w, h), 255)
        # タイルを繰り返し貼り付け
        for y in range(0, h, tile.height):
            for x in range(0, w, tile.width):
                bg.paste(tile, (x, y))
        self._bg_full = bg

    def _fit_zoom_to_window(self) -> None:
        """
        ウィンドウ内の表示領域に合わせてズームレベルを自動調整する。
        キャンバスがウィンドウからはみ出ないように、最適な倍率を選択する。
        """
        try:
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
        except Exception:
            return
        if canvas_width <= 1 or canvas_height <= 1:
            # ウィンドウ生成中は値がまだ取れないので再試行
            self.after(100, self._fit_zoom_to_window)
            return
        # キャンバスサイズに対するウィンドウサイズの比率を計算
        ratio_w = canvas_width / Config.CANVAS_SIZE
        ratio_h = canvas_height / Config.CANVAS_SIZE
        target_ratio = min(ratio_w, ratio_h)
        # 既存のズームレベルリストから最適な倍率を選択
        # 一番近いが小さめの倍率を選ぶことで余白を確保
        candidates = [z for z in self.zoom_levels if z <= target_ratio]
        if not candidates:
            # 全ての定義済み倍率よりも小さい場合は最小値を採用
            new_zoom = min(self.zoom_levels)
        else:
            new_zoom = max(candidates)
        if abs(self.zoom_level - new_zoom) > 1e-3:
            self.zoom_level = new_zoom
            self.zoom_label.config(text=f'{int(self.zoom_level * 100)}%')
            self._update_preview()
    
    def _setup_ui(self) -> None:
        """UI構築 (2025-10-12: テキスト挿入ツール追加)"""
        # ツールバー
        toolbar = tk.Frame(self, bg=Config.COLOR_BG)
        toolbar.pack(side='top', fill='x', padx=5, pady=5)
        
        tk.Button(toolbar, text='💾 保存', command=self._save).pack(side='left', padx=2)
        tk.Button(toolbar, text='📸 PNG保存', command=self._save_png).pack(side='left', padx=2)
        tk.Button(toolbar, text='📋 コピー', command=self._copy).pack(side='left', padx=2)
        tk.Button(toolbar, text='✂️ 切り取り', command=self._cut_selection).pack(side='left', padx=2)
        tk.Button(toolbar, text='📄 貼付', command=self._paste).pack(side='left', padx=2)
        tk.Button(toolbar, text='🗑️ クリア', command=self._clear).pack(side='left', padx=2)
        tk.Button(toolbar, text='⭕ 空白化', command=self._mark_as_empty).pack(side='left', padx=2)
        tk.Button(toolbar, text='🔥 他フォント読込', command=self._load_from_other_font).pack(side='left', padx=2)
        
        # ズームコントロール
        tk.Label(toolbar, text='🔍', bg=Config.COLOR_BG).pack(side='left', padx=(10, 0))
        tk.Button(toolbar, text='-', command=self._zoom_out, width=2).pack(side='left', padx=2)
        self.zoom_label = tk.Label(toolbar, text='100%', bg=Config.COLOR_BG, width=6)
        self.zoom_label.pack(side='left', padx=2)
        tk.Button(toolbar, text='+', command=self._zoom_in, width=2).pack(side='left', padx=2)
        tk.Button(toolbar, text='0', command=self._reset_zoom, width=2).pack(side='left', padx=2)
        
        # メインフレーム
        main_frame = tk.Frame(self, bg=Config.COLOR_BG)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # ===== 左側: ツールパネル（2列レイアウト） =====
        tool_panel_container = tk.Frame(main_frame, bg=Config.COLOR_BG)
        tool_panel_container.pack(side='left', fill='y', padx=(0, 10))
        
        tk.Label(tool_panel_container, text='ツール', bg=Config.COLOR_BG, font=('Arial', 12, 'bold')).pack(pady=5)
        
        # 2列レイアウト用フレーム
        tool_columns_frame = tk.Frame(tool_panel_container, bg=Config.COLOR_BG)
        tool_columns_frame.pack(fill='both', expand=True)
        
        # 左列: ツールボタン
        left_column = tk.Frame(tool_columns_frame, bg=Config.COLOR_BG, width=100)
        left_column.pack(side='left', fill='y', padx=(0, 5))
        
        # 右列: その他のコントロール
        right_column = tk.Frame(tool_columns_frame, bg=Config.COLOR_BG, width=200)
        right_column.pack(side='left', fill='both', expand=True)
        
        # ===== 左列: ツールボタン (2025-10-12: 文字挿入追加) =====
        tools = [
            ('✏️ ペン', 'pen'),
            ('📗 消しゴム', 'eraser'),
            ('🪣 塗りつぶし', 'fill'),
            ('選択', 'select'),
            ('✋ 移動', 'move'),
            ('🪜 拡大縮小', 'resize'),
            ('✒️ 文字挿入', 'text'),
            ('／ 直線', 'line'),
            ('□ 四角', 'rect'),
            ('○ 円', 'ellipse'),
            ('📐 ガイド', 'guide')
        ]

        for label, tool in tools:
            btn = tk.Button(
                left_column,
                text=label,
                command=lambda t=tool: self._set_tool(t),
                relief='sunken' if tool == 'pen' else 'raised',
                bg=Config.COLOR_ACTIVE if tool == 'pen' else Config.COLOR_BG,
                width=12
            )
            btn.pack(fill='x', padx=2, pady=2)
            self.tool_buttons[tool] = btn

        # ===== 右列: その他のコントロール =====
        
        # アンドゥ・リドゥボタン
        undo_redo_frame = tk.Frame(right_column, bg=Config.COLOR_BG)
        undo_redo_frame.pack(pady=(5, 0), fill='x')
        tk.Button(undo_redo_frame, text='↩️', command=self._undo, width=3).pack(side='left', padx=2)
        tk.Button(undo_redo_frame, text='↪️', command=self._redo, width=3).pack(side='left', padx=2)

        # 設定ボタン
        tk.Button(right_column, text='⚙ 設定', command=self._show_settings_dialog, width=10).pack(fill='x', padx=2, pady=(10, 2))

        # ナビゲーションウィンドウ
        nav_frame = tk.Frame(right_column, bg=Config.COLOR_BG)
        nav_frame.pack(pady=(10, 5))
        tk.Label(nav_frame, text='ナビ', bg=Config.COLOR_BG, font=('Arial', 10, 'bold')).pack()
        self.nav_canvas = tk.Canvas(nav_frame, width=Config.NAV_SIZE, height=Config.NAV_SIZE, bg='#F8F8F8', highlightthickness=1, highlightbackground='gray')
        self.nav_canvas.pack()
        # ナビゲーションクリックでスクロール移動を可能にする
        self.nav_canvas.bind('<Button-1>', self._on_nav_click)

        # [ADD] グリッド表示切り替え
        # 白線・赤線で構成されるグリッドのON/OFFを切り替えるチェックボックス。
        # 初期状態では非表示とし、チェック時にプレビューを更新する。
        grid_toggle = tk.Checkbutton(
            right_column,
            text='グリッド表示',
            variable=self.grid_visible_var,
            command=self._update_preview,
            bg=Config.COLOR_BG
        )
        grid_toggle.pack(anchor='w', padx=5, pady=(2, 5))
        
        # ブラシサイズ調整
        tk.Label(right_column, text='ブラシサイズ', bg=Config.COLOR_BG, font=('Arial', 10, 'bold')).pack(pady=(15, 5))
        
        self.brush_size_var = tk.IntVar(value=self.brush_size)
        brush_scale = tk.Scale(
            right_column,
            from_=1,
            to=50,
            orient='horizontal',
            variable=self.brush_size_var,
            command=self._on_brush_size_changed,
            length=150
        )
        brush_scale.pack(padx=5)
        
        self.brush_size_label = tk.Label(right_column, text=f'{self.brush_size}px', bg=Config.COLOR_BG)
        self.brush_size_label.pack()
        
        # 変形ツール
        tk.Label(right_column, text='変形', bg=Config.COLOR_BG, font=('Arial', 10, 'bold')).pack(pady=(15, 5))
        
        tk.Button(right_column, text='↔️ 左右反転', command=self._flip_horizontal, width=12).pack(fill='x', padx=5, pady=1)
        tk.Button(right_column, text='↕️ 上下反転', command=self._flip_vertical, width=12).pack(fill='x', padx=5, pady=1)
        tk.Button(right_column, text='🔄 90度回転', command=self._rotate_90, width=12).pack(fill='x', padx=5, pady=1)
        tk.Button(right_column, text='↔️ 左右中央', command=self._center_horizontal, width=12).pack(fill='x', padx=5, pady=1)
        tk.Button(right_column, text='↕️ 上下中央', command=self._center_vertical, width=12).pack(fill='x', padx=5, pady=1)
        tk.Button(right_column, text='🎯 上下左右', command=self._center_both, width=12).pack(fill='x', padx=5, pady=1)
        
        # ===== 右側: プレビューキャンバス =====
        preview_frame = tk.Frame(main_frame, bg=Config.COLOR_BG)
        preview_frame.pack(side='left', fill='both', expand=True)
        
        canvas_size = int(Config.CANVAS_SIZE * 1.2)

        canvas_container = tk.Frame(preview_frame, bg=Config.COLOR_BG)
        canvas_container.pack(fill='both', expand=True)

        self.preview_canvas = tk.Canvas(
            canvas_container,
            width=canvas_size,
            height=canvas_size,
            bg=Config.COLOR_CANVAS,
            highlightthickness=1,
            highlightbackground='gray'
        )
        h_scroll = ttk.Scrollbar(canvas_container, orient='horizontal', command=self._on_xscroll)
        v_scroll = ttk.Scrollbar(canvas_container, orient='vertical', command=self._on_yscroll)
        self.preview_canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        self.preview_canvas.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)

        self.preview_canvas.bind('<Button-1>', self._on_mouse_down)
        self.preview_canvas.bind('<B1-Motion>', self._on_mouse_drag)
        self.preview_canvas.bind('<ButtonRelease-1>', self._on_mouse_up)
        self.preview_canvas.bind('<Motion>', self._on_mouse_move)
    
    def _set_tool(self, tool: str) -> None:
        """ツール切り替え (2025-10-12: テキストツール追加)"""
        # テキストツール選択時
        if tool == 'text':
            self._start_text_input_mode()
            return
        
        self.current_tool = tool
        
        for t, btn in self.tool_buttons.items():
            if t == tool:
                btn.config(relief='sunken', bg=Config.COLOR_ACTIVE)
            else:
                btn.config(relief='raised', bg=Config.COLOR_BG)
    
    def _on_brush_size_changed(self, value: str) -> None:
        """ブラシサイズ変更"""
        self.brush_size = int(float(value))
        self.brush_size_label.config(text=f'{self.brush_size}px')

# ===== [本体 BLOCK5-END] =====







# ===== [本体 BLOCK5.5-BEGIN] 編集エディタGUI - テキスト挿入 (2025-10-17: 透過エッジ正しく実装) =====
# ===== GlyphEditorクラスの続き =====
    
    def _start_text_input_mode(self) -> None:
        """テキスト入力モード開始"""
        if self.text_input_dialog:
            self.text_input_dialog.lift()
            return
        
        self.is_text_mode = True
        
        self.text_layer_resized_size = None
        self.text_layer_resized_pos = None
        
        dialog = tk.Toplevel(self)
        dialog.title('文字挿入')
        dialog.geometry('450x550')
        dialog.transient(self)
        
        self.text_input_dialog = dialog
        
        tab_container = ttk.Notebook(dialog)
        tab_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ===== テキスト入力タブ =====
        text_tab = ttk.Frame(tab_container)
        tab_container.add(text_tab, text='テキスト入力')
        
        tk.Label(text_tab, text='挿入する文字を入力:', font=('Arial', 12, 'bold')).pack(pady=(10, 5))
        
        text_entry_frame = tk.Frame(text_tab)
        text_entry_frame.pack(fill='x', padx=20, pady=5)
        
        self.text_entry = tk.Entry(text_entry_frame, font=('Arial', 16), width=20)
        self.text_entry.pack(fill='x')
        self.text_entry.bind('<KeyRelease>', self._on_text_changed)
        self.text_entry.focus()
        
        # エッジ設定
        edge_frame = tk.Frame(text_tab)
        edge_frame.pack(fill='x', padx=20, pady=10)
        
        self.text_edge_var = tk.BooleanVar(value=False)
        edge_check = tk.Checkbutton(
            edge_frame, 
            text='白エッジを追加（透過領域を追加）', 
            variable=self.text_edge_var,
            command=self._on_text_changed,
            font=('Arial', 11)
        )
        edge_check.pack(anchor='w')
        
        tk.Label(edge_frame, text='エッジ幅:', font=('Arial', 10)).pack(anchor='w', pady=(10, 2))
        
        self.text_edge_width_var = tk.IntVar(value=3)
        # [MOD] エッジ幅のスライダを0〜100まで調整可能に拡大
        self.text_edge_scale = tk.Scale(
            edge_frame,
            from_=0,
            to=100,
            orient='horizontal',
            variable=self.text_edge_width_var,
            command=lambda v: self._on_text_changed() if self.text_edge_var.get() else None,
            length=200
        )
        self.text_edge_scale.pack(fill='x')

        # [ADD] エッジ幅の数値入力ボックス
        width_entry_frame = tk.Frame(edge_frame)
        width_entry_frame.pack(anchor='w', pady=(2, 2))
        tk.Label(width_entry_frame, text='幅入力:', font=('Arial', 9)).pack(side='left')
        self.text_edge_width_entry = tk.Entry(width_entry_frame, textvariable=self.text_edge_width_var, width=4)
        self.text_edge_width_entry.pack(side='left')
        # 値変更時にスライダと連動して更新
        def on_edge_width_entry_change(*args):
            try:
                val = int(self.text_edge_width_var.get())
            except Exception:
                return
            # 範囲を0-100に制限
            if val < 0:
                self.text_edge_width_var.set(0)
            elif val > 100:
                self.text_edge_width_var.set(100)
            if self.text_edge_var.get():
                self._on_text_changed()
        self.text_edge_width_var.trace_add('write', lambda *args: on_edge_width_entry_change())

        # [ADD] エッジ形状選択（角 or 丸）
        shape_frame = tk.Frame(edge_frame)
        shape_frame.pack(anchor='w', pady=(5, 0))
        tk.Label(shape_frame, text='エッジ形状:', font=('Arial', 9)).pack(side='left')
        sharp_rb = tk.Radiobutton(shape_frame, text='角', variable=self.edge_style_var, value='sharp', command=lambda: self._on_text_changed() if self.text_edge_var.get() else None, font=('Arial', 9))
        sharp_rb.pack(side='left', padx=(5, 0))
        round_rb = tk.Radiobutton(shape_frame, text='丸', variable=self.edge_style_var, value='round', command=lambda: self._on_text_changed() if self.text_edge_var.get() else None, font=('Arial', 9))
        round_rb.pack(side='left', padx=(5, 0))
        
        # ===== PNG読込タブ =====
        png_tab = ttk.Frame(tab_container)
        tab_container.add(png_tab, text='PNG読込')
        
        tk.Label(png_tab, text='PNG画像を読み込み:', font=('Arial', 12, 'bold')).pack(pady=(10, 5))
        
        png_btn_frame = tk.Frame(png_tab)
        png_btn_frame.pack(pady=10)
        
        tk.Button(
            png_btn_frame,
            text='📁 PNGファイルを選択',
            command=self._load_png_for_text,
            font=('Arial', 11),
            width=20
        ).pack()
        
        self.png_path_label = tk.Label(png_tab, text='ファイル未選択', font=('Arial', 9), fg='gray')
        self.png_path_label.pack(pady=5)
        
        tk.Label(png_tab, text='※ PNG画像は自動的にグレースケールに変換されます', 
                font=('Arial', 9), fg='gray').pack(pady=10)
        
        png_edge_frame = tk.Frame(png_tab)
        png_edge_frame.pack(fill='x', padx=20, pady=10)
        
        png_edge_check = tk.Checkbutton(
            png_edge_frame, 
            text='白エッジを追加（透過領域を追加）', 
            variable=self.text_edge_var,
            command=self._apply_edge_to_layer,
            font=('Arial', 11)
        )
        png_edge_check.pack(anchor='w')
        
        tk.Label(png_edge_frame, text='エッジ幅:', font=('Arial', 10)).pack(anchor='w', pady=(10, 2))
        
        # [MOD] PNG挿入時のエッジ幅スライダも0〜100まで選択可能にする
        self.png_edge_scale = tk.Scale(
            png_edge_frame,
            from_=0,
            to=100,
            orient='horizontal',
            variable=self.text_edge_width_var,
            command=lambda v: self._apply_edge_to_layer() if self.text_edge_var.get() else None,
            length=200
        )
        self.png_edge_scale.pack(fill='x')

        # [ADD] PNG用エッジ幅数値入力ボックス
        png_width_entry_frame = tk.Frame(png_edge_frame)
        png_width_entry_frame.pack(anchor='w', pady=(2, 2))
        tk.Label(png_width_entry_frame, text='幅入力:', font=('Arial', 9)).pack(side='left')
        self.png_edge_width_entry = tk.Entry(png_width_entry_frame, textvariable=self.text_edge_width_var, width=4)
        self.png_edge_width_entry.pack(side='left')
        # 値変更時にスライダと連動して更新
        def on_png_edge_width_entry_change(*args):
            try:
                val = int(self.text_edge_width_var.get())
            except Exception:
                return
            if val < 0:
                self.text_edge_width_var.set(0)
            elif val > 100:
                self.text_edge_width_var.set(100)
            if self.text_edge_var.get():
                self._apply_edge_to_layer()
        self.text_edge_width_var.trace_add('write', lambda *args: on_png_edge_width_entry_change())

        # [ADD] PNG用エッジ形状選択
        png_shape_frame = tk.Frame(png_edge_frame)
        png_shape_frame.pack(anchor='w', pady=(5, 0))
        tk.Label(png_shape_frame, text='エッジ形状:', font=('Arial', 9)).pack(side='left')
        sharp_png_rb = tk.Radiobutton(png_shape_frame, text='角', variable=self.edge_style_var, value='sharp', command=lambda: self._apply_edge_to_layer() if self.text_edge_var.get() else None, font=('Arial', 9))
        sharp_png_rb.pack(side='left', padx=(5, 0))
        round_png_rb = tk.Radiobutton(png_shape_frame, text='丸', variable=self.edge_style_var, value='round', command=lambda: self._apply_edge_to_layer() if self.text_edge_var.get() else None, font=('Arial', 9))
        round_png_rb.pack(side='left', padx=(5, 0))
        
        # ===== 共通ボタン =====
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(side='bottom', pady=10)
        
        tk.Button(btn_frame, text='✅ 決定', command=self._commit_text_layer, 
                 width=10, font=('Arial', 11, 'bold'), bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text='❌ キャンセル', command=self._cancel_text_input, 
                 width=10, font=('Arial', 11)).pack(side='left', padx=5)
        
        dialog.protocol('WM_DELETE_WINDOW', self._cancel_text_input)
    
    def _load_png_for_text(self) -> None:
        """PNG画像を読み込み"""
        path = filedialog.askopenfilename(
            title='PNG画像を選択',
            filetypes=[
                ('PNG Image', '*.png'),
                ('All Files', '*.*')
            ]
        )
        
        if not path:
            return
        
        try:
            img = Image.open(path)
            
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background.convert('L')
            elif img.mode != 'L':
                img = img.convert('L')
            
            max_size = Config.CANVAS_SIZE // 2
            if img.width > max_size or img.height > max_size:
                ratio = min(max_size / img.width, max_size / img.height)
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            self.text_layer = img
            self.text_layer_original = img.copy()
            
            x_pos = (Config.CANVAS_SIZE - img.width) // 2
            y_pos = (Config.CANVAS_SIZE - img.height) // 2
            self.text_layer_pos = (x_pos, y_pos)
            
            if self.text_edge_var.get():
                self._apply_edge_to_layer()
            
            self._update_preview()
            
            self.png_path_label.config(text=os.path.basename(path))
            
        except Exception as e:
            messagebox.showerror('エラー', f'PNG読み込みエラー:\n{e}')
    
    def _apply_edge_to_layer(self) -> None:
        """
        レイヤーにエッジを適用する。

        現在のテキストレイヤー (self.text_layer_original) を基にエッジ領域を算出し、
        エッジが有効な場合はその領域を preview で白色として表示し、決定時には透過となるよう
        自前のエッジマスク (self.text_edge_mask) と描画用レイヤー (self.text_layer) を生成する。
        エッジ幅が 0 またはエッジ表示が無効な場合はマスクを生成せず元画像を使用する。
        """
        # テキストレイヤーが存在しない場合は何もしない
        if not self.text_layer_original:
            return

        # エッジ機能が無効の場合はマスクをクリアして元画像をコピー
        if not self.text_edge_var.get():
            # エッジが無効な場合はマスクをクリア
            self.text_edge_mask = None
            self.text_edge_mask_commit = None
            self.text_layer = self.text_layer_original.copy()
            self._update_preview()
            return

        edge_width = self.text_edge_width_var.get()

        # エッジ幅が0の場合も同様にマスク無しで元画像をそのまま使用
        if edge_width == 0:
            # エッジ幅0の場合もマスクを生成しない
            self.text_edge_mask = None
            self.text_edge_mask_commit = None
            self.text_layer = self.text_layer_original.copy()
            self._update_preview()
            return


        # テキストレイヤーのコピー（グレースケール）
        base = self.text_layer_original.copy()
        width, height = base.size

        # 元の黒領域マスクを作成：文字部分は0、背景は255
        # 250未満のピクセルを文字とみなす（アンチエイリアス部分も含む）
        mask_original = base.point(lambda p: 0 if p < 250 else 255)

        # Edge style: 'sharp' or 'round'. For 'round', smooth the mask before dilation to round corners
        edge_style = getattr(self, 'edge_style_var', None).get() if hasattr(self, 'edge_style_var') else 'sharp'
        mask_to_dilate = mask_original
        if edge_style == 'round':
            # Apply a slight Gaussian blur to soften corners before dilation. The blur radius of 1
            # provides a smoother contour. Threshold back to binary after blurring.
            blurred = mask_original.filter(ImageFilter.GaussianBlur(1))
            mask_to_dilate = blurred.point(lambda p: 0 if p < 128 else 255)

        # 膨張処理：MinFilterを大きなカーネルで1回適用することで高速化する。
        # MinFilterは黒(0)を外側へ広げるので、サイズは2*edge_width+1とする。
        if edge_width > 0:
            kernel_size = edge_width * 2 + 1
            # pillow の MinFilter はカーネルサイズが奇数である必要がある
            # kernel_size が偶数の場合は次の奇数に調整
            if kernel_size % 2 == 0:
                kernel_size += 1
            dilated = mask_to_dilate.filter(ImageFilter.MinFilter(kernel_size))
        else:
            dilated = mask_to_dilate.copy()

        # 結果となるレイヤーとエッジマスクを初期化
        result = Image.new('L', base.size, 255)
        edge_mask_commit = Image.new('L', base.size, 0)  # コミット用
        edge_mask_preview = Image.new('L', base.size, 0)  # プレビュー用 (sharp=original, round=加工)

        orig_pixels = base.load()
        mask_pixels = mask_original.load()
        dil_pixels = dilated.load()
        res_pixels = result.load()
        edge_pixels_commit = edge_mask_commit.load()
        edge_pixels_preview = edge_mask_preview.load()

        # ピクセル単位で分類
        for y in range(height):
            for x in range(width):
                # 元の文字部分はそのまま（濃度を保持）
                if mask_pixels[x, y] == 0:
                    res_pixels[x, y] = orig_pixels[x, y]
                # 膨張した領域かつ元の文字ではない → エッジ領域
                elif dil_pixels[x, y] == 0 and mask_pixels[x, y] != 0:
                    # レイヤー上では透過（255）とする
                    res_pixels[x, y] = 255
                    # コミット用マスク：エッジ領域は255
                    edge_pixels_commit[x, y] = 255
                    # プレビュー用マスク: 初期状態はsharpと同様
                    edge_pixels_preview[x, y] = 255
                # それ以外は背景のまま

        # エッジ形状が丸の場合、プレビュー用マスクをぼかして角を丸める
        if edge_style == 'round' and edge_width > 0:
            try:
                # プレビュー用マスクをガウシアンブラーで滑らかにし、閾値をかけてバイナリ化
                blur_radius = max(1, int(edge_width / 2))
                blurred = edge_mask_preview.filter(ImageFilter.GaussianBlur(blur_radius))
                # 一旦二値化（少しでも白くなった部分をエッジとする）
                thresholded = blurred.point(lambda p: 255 if p > 0 else 0)
                # 内部侵食を防ぐため、元の文字部分(mask_pixels==0)ではマスクを0に設定する
                preview_pixels = thresholded.load()
                for yy in range(height):
                    for xx in range(width):
                        # mask_pixels[x,y]==0 は元の文字領域
                        if mask_pixels[xx, yy] == 0:
                            preview_pixels[xx, yy] = 0
                edge_mask_preview = thresholded
            except Exception:
                pass

        # テキストレイヤーとエッジマスクを保存
        self.text_layer = result
        # コミット用エッジマスク
        self.text_edge_mask_commit = edge_mask_commit
        # プレビュー用エッジマスク
        self.text_edge_mask = edge_mask_preview
        # プレビュー更新
        self._update_preview()
    
    def _on_text_changed(self, event=None) -> None:
        """テキスト入力変更時"""
        text = self.text_entry.get().strip()
        
        if not text:
            if not hasattr(self, 'text_layer_original') or self.text_layer_original is None:
                self.text_layer = None
                self.text_layer_resized_size = None
                self.text_layer_resized_pos = None
                self._update_preview()
            else:
                self._apply_edge_to_layer()
                self._update_preview()
            return
        
        if not self.project.font_path:
            messagebox.showwarning('警告', 'フォントが読み込まれていません')
            return
        
        try:
            target_size = self.text_layer_resized_size
            target_pos = self.text_layer_resized_pos
            
            font = ImageFont.truetype(self.project.font_path, size=Config.FONT_RENDER_SIZE)
            
            char_img = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
            draw = ImageDraw.Draw(char_img)
            
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            
            x = (Config.CANVAS_SIZE - w) / 2 - bbox[0]
            y = (Config.CANVAS_SIZE - h) / 2 - bbox[1]
            
            draw.text((x, y), text, fill=0, font=font)
            
            bbox = char_img.getbbox()
            if bbox:
                trimmed = char_img.crop(bbox)
                
                if target_size and target_pos:
                    target_w, target_h = target_size
                    self.text_layer_original = trimmed.resize((target_w, target_h), Image.LANCZOS)
                    self.text_layer_pos = target_pos
                else:
                    self.text_layer_original = trimmed
                    x_pos = (Config.CANVAS_SIZE - trimmed.width) // 2
                    y_pos = (Config.CANVAS_SIZE - trimmed.height) // 2
                    self.text_layer_pos = (x_pos, y_pos)
                
                if self.text_edge_var.get():
                    self._apply_edge_to_layer()
                else:
                    # エッジ無しの場合は元画像をそのまま使用し、エッジマスクをクリア
                    self.text_layer = self.text_layer_original.copy()
                    self.text_edge_mask = None
            else:
                self.text_layer = None
                self.text_layer_original = None
                self.text_layer_resized_size = None
                self.text_layer_resized_pos = None
            
            self._update_preview()
            
        except Exception as e:
            print(f'テキストレンダリングエラー: {e}')
            import traceback
            traceback.print_exc()
    
    def _commit_text_layer(self) -> None:
        """テキストレイヤーをベースに統合 (2025-10-17: 透過を正しく処理)"""  # [FIX]
        if not self.text_layer:
            messagebox.showwarning('警告', 'テキストが入力されていません')
            return
        
        # [FIX] 2025-10-17: 透過(255)はスキップ、黒はmin合成
        # レイヤーが存在しない場合は警告を出して終了
        if not self.text_layer:
            messagebox.showwarning('警告', 'テキストが入力されていません')
            return

        x_pos, y_pos = self.text_layer_pos
        # ラスタライズしたテキストレイヤーをキャンバスサイズの画像に展開
        layer_img = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
        layer_img.paste(self.text_layer, (x_pos, y_pos))

        # 合成処理：255より小さい領域のみ更新（255は透過および背景として扱う）
        mask = layer_img.point(lambda p: 255 if p < 255 else 0)
        # darker関数で元画像とレイヤーの暗い方を採用
        darker = ImageChops.darker(self.edit_bitmap, layer_img)
        # マスクに従ってペースト
        new_bitmap = self.edit_bitmap.copy()
        new_bitmap.paste(darker, mask=mask)

        # [ADD] 2025-10-22: エッジ領域を透過処理
        # テキストエッジマスクが存在する場合は、エッジ領域と重なっているベース画像を透過
        # （白＝255）に置き換える。これにより、決定後に白エッジが透明に変換される。
        # コミット用エッジマスクが存在する場合は、エッジ領域を白に置き換える
        if getattr(self, 'text_edge_mask_commit', None):
            try:
                edge_mask_full = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 0)
                x_pos, y_pos = self.text_layer_pos
                edge_mask_full.paste(self.text_edge_mask_commit, (x_pos, y_pos))
                white_layer = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
                new_bitmap = Image.composite(white_layer, new_bitmap, edge_mask_full)
            except Exception:
                pass
        # 更新
        self.edit_bitmap = new_bitmap

        # テキスト関連データのリセット
        self.text_layer = None
        self.text_layer_original = None
        self.text_layer_resized_size = None
        self.text_layer_resized_pos = None
        self.is_text_mode = False
        # エッジマスク類をリセット
        self.text_edge_mask = None
        self.text_edge_mask_commit = None
        if self.text_input_dialog:
            self.text_input_dialog.destroy()
            self.text_input_dialog = None

        self._save_to_undo()
        self._update_preview()
        messagebox.showinfo('完了', 'テキストを統合しました')
    
    def _cancel_text_input(self) -> None:
        """テキスト入力をキャンセル"""
        self.text_layer = None
        self.text_layer_original = None
        self.text_layer_resized_size = None
        self.text_layer_resized_pos = None
        self.is_text_mode = False
        
        if self.text_input_dialog:
            self.text_input_dialog.destroy()
            self.text_input_dialog = None
        
        self._update_preview()

# ===== [本体 BLOCK5.5-END] =====









# ===== [本体 BLOCK5.6-BEGIN] 編集エディタGUI - 描画メソッドとプレビュー更新 (2025-10-13: 新規作成) =====
# ===== GlyphEditorクラスの続き =====
    
    # ===== 描画メソッド (2025-10-13: 基本描画処理) =====
    
    def _draw_point(self, x: int, y: int) -> None:
        """点を描画"""
        if not (0 <= x < Config.CANVAS_SIZE and 0 <= y < Config.CANVAS_SIZE):
            return
        
        pixels = self.edit_bitmap.load()
        color = 0 if self.current_tool == 'pen' else 255  # ペン=黒、消しゴム=白
        
        # ブラシサイズに応じて円形で描画
        radius = self.brush_size // 2
        
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:  # 円形判定
                    px = x + dx
                    py = y + dy
                    
                    if 0 <= px < Config.CANVAS_SIZE and 0 <= py < Config.CANVAS_SIZE:
                        pixels[px, py] = color
    
    def _draw_line(self, x0: int, y0: int, x1: int, y1: int) -> None:
        """線を描画（ブレゼンハムアルゴリズム）"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        x, y = x0, y0
        
        while True:
            self._draw_point(x, y)
            
            if x == x1 and y == y1:
                break
            
            e2 = 2 * err
            
            if e2 > -dy:
                err -= dy
                x += sx
            
            if e2 < dx:
                err += dx
                y += sy
    
    def _flood_fill(self, x: int, y: int) -> None:
        """塗りつぶし（スタック使用）"""
        if not (0 <= x < Config.CANVAS_SIZE and 0 <= y < Config.CANVAS_SIZE):
            return
        
        pixels = self.edit_bitmap.load()
        target_color = pixels[x, y]
        fill_color = 0 if self.current_tool == 'pen' else 255
        
        if target_color == fill_color:
            return  # 既に同じ色
        
        # スタック使用（再帰ではなく）
        stack = [(x, y)]
        visited = set()
        
        while stack:
            cx, cy = stack.pop()
            
            if (cx, cy) in visited:
                continue
            
            if not (0 <= cx < Config.CANVAS_SIZE and 0 <= cy < Config.CANVAS_SIZE):
                continue
            
            if pixels[cx, cy] != target_color:
                continue
            
            pixels[cx, cy] = fill_color
            visited.add((cx, cy))
            
            # 4方向に拡張
            stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
        
        self._save_to_undo()
        self._update_preview()
    
    # ===== プレビュー更新 (2025-10-13: 通常版と高速版) =====
    
    def _update_preview(self) -> None:
        """プレビュー更新（通常版：グリッド・ハンドル含む）"""
        # ズーム適用
        new_width = int(Config.CANVAS_SIZE * self.zoom_level)
        new_height = int(Config.CANVAS_SIZE * self.zoom_level)

        # 背景パターンが未生成の場合は生成
        if self._bg_full is None or self._bg_full.size != (Config.CANVAS_SIZE, Config.CANVAS_SIZE):
            self._create_full_bg()

        # ベースレイヤーとテキストレイヤーを合成（ループを使わず高速化）
        if self.text_layer and not (self.is_moving or self.is_resizing):
            # テキストレイヤーが存在する場合はレイヤーをベース画像に貼り付けた画像を作成し、
            # ImageChops.darkerにより暗い方（0に近い方）を採用することで合成する
            layer_img = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
            x_pos, y_pos = self.text_layer_pos
            layer_img.paste(self.text_layer, (x_pos, y_pos))
            composite = ImageChops.darker(self.edit_bitmap, layer_img)
        else:
            composite = self.edit_bitmap

        # [ADD] 2025-10-22: テキストエッジのプレビュー表示
        # エッジマスクが存在する場合は、プレビュー上で白系の色を合成して視認性を高める
        if self.text_layer and self.text_edge_mask and not (self.is_moving or self.is_resizing):
            try:
                # エッジマスクをキャンバス全体に展開
                edge_full = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 0)
                x_pos, y_pos = self.text_layer_pos
                edge_full.paste(self.text_edge_mask, (x_pos, y_pos))
                # エッジ用の明るいレイヤー（白に近いグレー）
                # エッジを際立たせるため、背景より明るい値(254)で表示
                edge_color = 254
                edge_layer = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), edge_color)
                # マスクの非ゼロ領域にedge_layerを適用 (maskの値255→first image)
                composite = Image.composite(edge_layer, composite, edge_full)
            except Exception:
                # 念のためエラー時はそのまま表示
                pass

        # 背景パターンと合成
        # 255の場所（完全な白）は透過とみなし、背景パターンが表示される。
        # それ以外は黒や薄い灰色をそのまま前景として描画する。
        # まずマスク画像を生成: 255->0, その他->255
        mask = composite.point(lambda p: 0 if p == 255 else 255)
        merged = Image.composite(composite, self._bg_full, mask)

        # ズームリサイズ
        zoomed = merged.resize((new_width, new_height), Image.NEAREST if self.is_moving or self.is_resizing else Image.LANCZOS)

        # キャンバスに描画
        self.photo = ImageTk.PhotoImage(zoomed)
        self.preview_canvas.delete('all')
        self.preview_canvas.create_image(0, 0, anchor='nw', image=self.photo, tags='base')

        # グリッド線描画
        self._draw_grid()

        # 移動/リサイズ中の選択領域プレビュー
        if self.current_tool == 'move' and self.is_moving and self.move_current_pos:
            self._draw_moving_preview()
        if self.current_tool == 'resize' and self.is_resizing and self.resize_preview_rect:
            self._draw_resizing_preview()

        # 選択矩形描画
        if self.current_tool == 'select' and self.selection_start and self.selection_end:
            self._draw_selection_rect()

        # リサイズハンドル描画
        if self.current_tool == 'resize' and self.selection_start and self.selection_end:
            self._draw_resize_handles()

        # 図形プレビュー
        if self.shape_start and self.shape_end:
            self._draw_shape_preview()

        # テキストレイヤーの操作中プレビュー（移動/リサイズ中）
        if self.is_text_mode and self.text_layer:
            self._draw_text_layer_preview()
            if self.current_tool == 'resize':
                self._draw_text_layer_handles()

        # ガイドライン描画
        for guide_type, pos in self.guidelines:
            if guide_type == 'h':
                y_canvas = pos * self.zoom_level
                self.preview_canvas.create_line(0, y_canvas, new_width, y_canvas,
                                               fill='#FF00FF', dash=(5, 5), tags='guide')
            elif guide_type == 'v':
                x_canvas = pos * self.zoom_level
                self.preview_canvas.create_line(x_canvas, 0, x_canvas, new_height,
                                               fill='#FF00FF', dash=(5, 5), tags='guide')

        # ナビゲーション更新
        self._update_nav()

        # スクロール領域更新
        self.preview_canvas.configure(scrollregion=(0, 0, new_width, new_height))
    
    def _update_preview_fast(self) -> None:
        """高速プレビュー更新（ドラッグ中専用：グリッド・ハンドル省略）"""  # [ADD] 2025-10-13
        # ズーム適用
        new_width = int(Config.CANVAS_SIZE * self.zoom_level)
        new_height = int(Config.CANVAS_SIZE * self.zoom_level)

        # 背景パターン生成を確認
        if self._bg_full is None or self._bg_full.size != (Config.CANVAS_SIZE, Config.CANVAS_SIZE):
            self._create_full_bg()

        # グリッド線を削除（高速更新では描画しないため）
        self.preview_canvas.delete('grid')

        # 合成処理（高速バージョン）
        if self.text_layer:
            # レイヤーをベースに貼り付けて暗い方を採用
            layer_img = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
            x_pos, y_pos = self.text_layer_pos
            layer_img.paste(self.text_layer, (x_pos, y_pos))
            composite = ImageChops.darker(self.edit_bitmap, layer_img)
        else:
            composite = self.edit_bitmap

        # [ADD] 2025-10-22: 高速プレビューでもエッジを表示
        if self.text_layer and self.text_edge_mask:
            try:
                edge_full = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 0)
                x_pos, y_pos = self.text_layer_pos
                edge_full.paste(self.text_edge_mask, (x_pos, y_pos))
                # エッジを際立たせるため、背景より明るい値(254)で表示
                edge_color = 254
                edge_layer = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), edge_color)
                composite = Image.composite(edge_layer, composite, edge_full)
            except Exception:
                pass

        # 背景と合成
        mask = composite.point(lambda p: 0 if p == 255 else 255)
        merged = Image.composite(composite, self._bg_full, mask)

        zoomed = merged.resize((new_width, new_height), Image.NEAREST)

        self.photo = ImageTk.PhotoImage(zoomed)
        # ベース画像のみ更新（タグ指定で高速化）
        self.preview_canvas.delete('base')
        self.preview_canvas.create_image(0, 0, anchor='nw', image=self.photo, tags='base')
        
        # テキストレイヤーの枠のみ描画（簡易表示）
        if self.is_text_mode and self.text_layer:
            self.preview_canvas.delete('text_layer_rect')
            
            x_pos, y_pos = self.text_layer_pos
            x_end = x_pos + self.text_layer.width
            y_end = y_pos + self.text_layer.height
            
            cx1 = x_pos * self.zoom_level
            cy1 = y_pos * self.zoom_level
            cx2 = x_end * self.zoom_level
            cy2 = y_end * self.zoom_level
            
            self.preview_canvas.create_rectangle(cx1, cy1, cx2, cy2, 
                                                outline='#00FF00', width=2, 
                                                dash=(5, 5), tags='text_layer_rect')
        
        # ナビゲーション更新（軽量版）
        self._update_nav()
    
    # ===== 描画補助メソッド (2025-10-13: プレビュー用) =====
    
    def _draw_grid(self) -> None:
        """グリッド線を描画"""
        # グリッド表示がオフの場合は描画しない
        if not self.grid_visible_var.get():
            return

        new_width = int(Config.CANVAS_SIZE * self.zoom_level)
        new_height = int(Config.CANVAS_SIZE * self.zoom_level)

        # 縦線
        for x in range(0, Config.CANVAS_SIZE, Config.GRID_SPACING):
            x_canvas = x * self.zoom_level
            color = Config.GRID_CENTER_COLOR if x == Config.CANVAS_SIZE // 2 else Config.GRID_COLOR
            self.preview_canvas.create_line(x_canvas, 0, x_canvas, new_height,
                                           fill=color, tags='grid')

        # 横線
        for y in range(0, Config.CANVAS_SIZE, Config.GRID_SPACING):
            y_canvas = y * self.zoom_level
            color = Config.GRID_CENTER_COLOR if y == Config.CANVAS_SIZE // 2 else Config.GRID_COLOR
            self.preview_canvas.create_line(0, y_canvas, new_width, y_canvas,
                                           fill=color, tags='grid')
    
    def _draw_selection_rect(self) -> None:
        """選択矩形を描画"""
        if not (self.selection_start and self.selection_end):
            return
        
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        
        cx1 = x1 * self.zoom_level
        cy1 = y1 * self.zoom_level
        cx2 = x2 * self.zoom_level
        cy2 = y2 * self.zoom_level
        
        self.preview_canvas.create_rectangle(cx1, cy1, cx2, cy2, 
                                            outline='#0000FF', width=2, 
                                            dash=(5, 5), tags='selection')
    
    def _draw_resize_handles(self) -> None:
        """リサイズハンドルを描画"""
        if not (self.selection_start and self.selection_end):
            return
        
        self._normalize_selection()
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        
        cx1 = x1 * self.zoom_level
        cy1 = y1 * self.zoom_level
        cx2 = x2 * self.zoom_level
        cy2 = y2 * self.zoom_level
        
        cx_mid = (cx1 + cx2) / 2
        cy_mid = (cy1 + cy2) / 2
        
        handle_size = 6
        
        handles = [
            (cx1, cy1), (cx_mid, cy1), (cx2, cy1),
            (cx1, cy_mid), (cx2, cy_mid),
            (cx1, cy2), (cx_mid, cy2), (cx2, cy2)
        ]
        
        # 既存のハンドルを削除
        for hid in self.resize_handle_ids:
            self.preview_canvas.delete(hid)
        self.resize_handle_ids.clear()
        
        # 新しいハンドルを描画
        for hx, hy in handles:
            hid = self.preview_canvas.create_rectangle(
                hx - handle_size, hy - handle_size,
                hx + handle_size, hy + handle_size,
                fill='white', outline='blue', width=2, tags='handle'
            )
            self.resize_handle_ids.append(hid)
    
    def _draw_text_layer_handles(self) -> None:
        """テキストレイヤーのハンドルを描画"""
        if not self.text_layer:
            return
        
        x_pos, y_pos = self.text_layer_pos
        x_end = x_pos + self.text_layer.width
        y_end = y_pos + self.text_layer.height
        
        cx1 = x_pos * self.zoom_level
        cy1 = y_pos * self.zoom_level
        cx2 = x_end * self.zoom_level
        cy2 = y_end * self.zoom_level
        
        cx_mid = (cx1 + cx2) / 2
        cy_mid = (cy1 + cy2) / 2
        
        handle_size = 6
        
        handles = [
            (cx1, cy1), (cx_mid, cy1), (cx2, cy1),
            (cx1, cy_mid), (cx2, cy_mid),
            (cx1, cy2), (cx_mid, cy2), (cx2, cy2)
        ]
        
        # テキストレイヤーハンドルを描画
        for hx, hy in handles:
            self.preview_canvas.create_rectangle(
                hx - handle_size, hy - handle_size,
                hx + handle_size, hy + handle_size,
                fill='lime', outline='green', width=2, tags='text_handle'
            )
    
    def _draw_moving_preview(self) -> None:
        """移動中のプレビュー描画"""
        if not (self.selected_image and self.move_current_pos):
            return
        
        x, y = self.move_current_pos
        w = self.selected_image.width
        h = self.selected_image.height
        
        cx1 = x * self.zoom_level
        cy1 = y * self.zoom_level
        cx2 = (x + w) * self.zoom_level
        cy2 = (y + h) * self.zoom_level
        
        # 選択範囲の内容をプレビューに描画し、枠線を表示
        # 既存の移動画像を削除
        self.preview_canvas.delete('moving_img')
        # 描画内容を貼り付け
        try:
            # 拡大縮小された選択内容を作成
            preview_sel = self.selected_image.resize((int(w * self.zoom_level), int(h * self.zoom_level)), Image.NEAREST)
            self._move_photo = ImageTk.PhotoImage(preview_sel)
            self.preview_canvas.create_image(cx1, cy1, anchor='nw', image=self._move_photo, tags='moving_img')
        except Exception:
            pass
        # 枠線を描画
        self.preview_canvas.create_rectangle(cx1, cy1, cx2, cy2,
                                            outline='#00FF00', width=2,
                                            dash=(3, 3), tags='moving')
    
    def _draw_resizing_preview(self) -> None:
        """リサイズ中のプレビュー描画"""
        if not self.resize_preview_rect:
            return
        
        x1, y1, x2, y2 = self.resize_preview_rect
        
        cx1 = x1 * self.zoom_level
        cy1 = y1 * self.zoom_level
        cx2 = x2 * self.zoom_level
        cy2 = y2 * self.zoom_level
        
        self.preview_canvas.create_rectangle(cx1, cy1, cx2, cy2, 
                                            outline='#FF00FF', width=2, 
                                            dash=(3, 3), tags='resizing')
    
    def _draw_shape_preview(self) -> None:
        """図形プレビュー描画"""
        if not (self.shape_start and self.shape_end):
            return
        
        x1, y1 = self.shape_start
        x2, y2 = self.shape_end
        
        cx1 = x1 * self.zoom_level
        cy1 = y1 * self.zoom_level
        cx2 = x2 * self.zoom_level
        cy2 = y2 * self.zoom_level
        
        if self.current_tool == 'line':
            self.preview_canvas.create_line(cx1, cy1, cx2, cy2, 
                                           fill='red', width=2, tags='shape_preview')
        elif self.current_tool == 'rect':
            self.preview_canvas.create_rectangle(cx1, cy1, cx2, cy2, 
                                                outline='red', width=2, tags='shape_preview')
        elif self.current_tool == 'ellipse':
            self.preview_canvas.create_oval(cx1, cy1, cx2, cy2, 
                                           outline='red', width=2, tags='shape_preview')
    
    def _draw_text_layer_preview(self) -> None:
        """テキストレイヤーのプレビュー描画"""
        if not self.text_layer:
            return
        
        x_pos, y_pos = self.text_layer_pos
        x_end = x_pos + self.text_layer.width
        y_end = y_pos + self.text_layer.height
        
        cx1 = x_pos * self.zoom_level
        cy1 = y_pos * self.zoom_level
        cx2 = x_end * self.zoom_level
        cy2 = y_end * self.zoom_level
        
        # 緑色の枠で表示
        self.preview_canvas.create_rectangle(cx1, cy1, cx2, cy2, 
                                            outline='#00FF00', width=2, 
                                            dash=(5, 5), tags='text_layer')
    
    # ===== ナビゲーション更新 (2025-10-13) =====
    
    def _update_nav(self) -> None:
        """ナビゲーションウィンドウ更新"""
        # 現在の画像を縮小してナビゲーションに表示
        nav_img = self.edit_bitmap.resize((Config.NAV_SIZE, Config.NAV_SIZE), Image.NEAREST)
        self._nav_photo = ImageTk.PhotoImage(nav_img)
        
        self.nav_canvas.delete('all')
        self.nav_canvas.create_image(0, 0, anchor='nw', image=self._nav_photo)
        
        # 現在の表示範囲を赤枠で表示
        # visible_w/h: 画像上で表示されている幅・高さ
        visible_w = self.preview_canvas.winfo_width() / self.zoom_level
        visible_h = self.preview_canvas.winfo_height() / self.zoom_level
        ratio = Config.NAV_SIZE / Config.CANVAS_SIZE
        nav_w = visible_w * ratio
        nav_h = visible_h * ratio
        # 現在のオフセット（スクロール位置）を取得
        # canvasx/canvasyはズーム後の座標を返すのでズームレベルで割る
        try:
            x0_canvas = self.preview_canvas.canvasx(0)
            y0_canvas = self.preview_canvas.canvasy(0)
        except Exception:
            x0_canvas = 0
            y0_canvas = 0
        img_x0 = x0_canvas / self.zoom_level
        img_y0 = y0_canvas / self.zoom_level
        nav_x = img_x0 * ratio
        nav_y = img_y0 * ratio
        self.nav_canvas.create_rectangle(nav_x, nav_y, nav_x + nav_w, nav_y + nav_h,
                                        outline='red', width=2)

    def _on_nav_click(self, event: tk.Event) -> None:
        """
        ナビゲーションウィンドウのクリック位置に応じて、プレビューキャンバスの表示領域をスクロールする。
        クリックした位置がプレビューの中心になるように移動する。
        """
        # クリック座標を画像の座標系に変換
        ratio = Config.NAV_SIZE / Config.CANVAS_SIZE
        img_x = event.x / ratio
        img_y = event.y / ratio
        # 現在の表示領域のサイズ（画像座標）
        visible_w = self.preview_canvas.winfo_width() / self.zoom_level
        visible_h = self.preview_canvas.winfo_height() / self.zoom_level
        # 左上座標を計算（クリック位置を中心に）
        target_x = img_x - visible_w / 2
        target_y = img_y - visible_h / 2
        max_x = Config.CANVAS_SIZE - visible_w
        max_y = Config.CANVAS_SIZE - visible_h
        target_x = max(0, min(target_x, max_x))
        target_y = max(0, min(target_y, max_y))
        # キャンバス座標に変換
        target_canvas_x = target_x * self.zoom_level
        target_canvas_y = target_y * self.zoom_level
        total_width = Config.CANVAS_SIZE * self.zoom_level
        total_height = Config.CANVAS_SIZE * self.zoom_level
        denom_x = max(1, total_width - self.preview_canvas.winfo_width())
        denom_y = max(1, total_height - self.preview_canvas.winfo_height())
        # スクロール移動
        self.preview_canvas.xview_moveto(target_canvas_x / denom_x)
        self.preview_canvas.yview_moveto(target_canvas_y / denom_y)
        self._update_preview()
    
    # ===== スクロール処理 (2025-10-13) =====
    
    def _on_xscroll(self, *args) -> None:
        """横スクロール"""
        self.preview_canvas.xview(*args)
    
    def _on_yscroll(self, *args) -> None:
        """縦スクロール"""
        self.preview_canvas.yview(*args)

# ===== [本体 BLOCK5.6-END] =====








# ===== [本体 BLOCK5.7-BEGIN] 編集エディタGUI - 選択・変形・操作メソッド (2025-10-17: マウスイベント追加) =====
# ===== GlyphEditorクラスの続き =====
    
    # ===== 選択領域メソッド (2025-10-13: 選択・移動・削除処理) =====
    
    def _finalize_selection(self) -> None:
        """選択範囲を確定"""
        if not (self.selection_start and self.selection_end):
            return
        
        self._normalize_selection()
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        
        # 選択領域が小さすぎる場合は無視
        if abs(x2 - x1) < 2 or abs(y2 - y1) < 2:
            self.selection_start = None
            self.selection_end = None
            self.selected_image = None
            return
        
        # 選択領域を切り取り
        try:
            self.selected_image = self.edit_bitmap.crop((x1, y1, x2, y2)).copy()
        except Exception as e:
            print(f'選択エラー: {e}')
            self.selection_start = None
            self.selection_end = None
            self.selected_image = None
    
    def _apply_translation(self) -> None:
        """移動を確定"""
        if not (self.selected_image and self.move_current_pos and self.selection_start):
            return
        
        # 元の領域を白で塗りつぶし
        draw = ImageDraw.Draw(self.edit_bitmap)
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        # 元の領域を白で塗りつぶす（排他的範囲）
        draw.rectangle((x1, y1, x2 - 1, y2 - 1), fill=255)
        # 新しい位置に貼り付け（透過部分は無視）
        dest_x, dest_y = self.move_current_pos
        mask = self.selected_image.point(lambda p: 255 if p < 255 else 0)
        self.edit_bitmap.paste(self.selected_image, (dest_x, dest_y), mask)
        # 選択状態を更新
        w = self.selected_image.width
        h = self.selected_image.height
        self.selection_start = (dest_x, dest_y)
        self.selection_end = (dest_x + w, dest_y + h)
        self._save_to_undo()
        self._update_preview()
    
    def _commit_shape(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """図形を確定して描画"""
        x1, y1 = start
        x2, y2 = end
        
        draw = ImageDraw.Draw(self.edit_bitmap)
        
        if self.current_tool == 'line':
            # 直線描画
            self._draw_line(x1, y1, x2, y2)
        elif self.current_tool == 'rect':
            # 矩形描画
            draw.rectangle((x1, y1, x2, y2), outline=0, width=self.brush_size)
        elif self.current_tool == 'ellipse':
            # 楕円描画
            draw.ellipse((x1, y1, x2, y2), outline=0, width=self.brush_size)
        
        self._save_to_undo()
        self._update_preview()
    
    def _nudge(self, dx: int, dy: int) -> None:
        """矢印キーで1px移動"""
        if self.is_text_mode and self.text_layer:
            # テキストレイヤーの移動
            x_pos, y_pos = self.text_layer_pos
            new_x = max(0, min(x_pos + dx, Config.CANVAS_SIZE - self.text_layer.width))
            new_y = max(0, min(y_pos + dy, Config.CANVAS_SIZE - self.text_layer.height))
            self.text_layer_pos = (new_x, new_y)
            self._update_preview()
        elif self.selected_image and self.selection_start and self.selection_end:
            # 選択領域の移動
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            new_x1 = max(0, min(x1 + dx, Config.CANVAS_SIZE - (x2 - x1)))
            new_y1 = max(0, min(y1 + dy, Config.CANVAS_SIZE - (y2 - y1)))
            # 元の領域を白で塗りつぶし
            draw = ImageDraw.Draw(self.edit_bitmap)
            # 元の領域を白で塗りつぶす（Pillowのrectangleは終点を含むため-1する）
            draw.rectangle((x1, y1, x2 - 1, y2 - 1), fill=255)
            # マスクを作成し、選択範囲の黒／灰色ピクセルのみを貼り付け
            # 250未満は描画すべき領域、その他は透過扱い
            # 非透過ピクセルをすべて移動対象とする
            mask = self.selected_image.point(lambda p: 255 if p < 255 else 0)
            self.edit_bitmap.paste(self.selected_image, (new_x1, new_y1), mask)
            # 選択状態を更新
            w = x2 - x1
            h = y2 - y1
            self.selection_start = (new_x1, new_y1)
            self.selection_end = (new_x1 + w, new_y1 + h)
            self._save_to_undo()
            self._update_preview()
    
    def _copy_selection(self) -> None:
        """選択領域をコピー"""
        if self.selected_image:
            self.project.clipboard = self.selected_image.copy()
            messagebox.showinfo('コピー', '選択領域をコピーしました')
    
    def _cut_selection(self) -> None:
        """選択領域を切り取り"""
        if self.selected_image and self.selection_start and self.selection_end:
            # クリップボードにコピー
            self.project.clipboard = self.selected_image.copy()
            
            # 選択領域を白で塗りつぶし
            draw = ImageDraw.Draw(self.edit_bitmap)
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            draw.rectangle((x1, y1, x2, y2), fill=255)
            
            # 選択解除
            self.selection_start = None
            self.selection_end = None
            self.selected_image = None
            
            self._save_to_undo()
            self._update_preview()
            
            messagebox.showinfo('切り取り', '選択領域を切り取りました')
    
    def _delete_selection(self) -> None:
        """選択領域を削除"""
        if self.selection_start and self.selection_end:
            draw = ImageDraw.Draw(self.edit_bitmap)
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            draw.rectangle((x1, y1, x2, y2), fill=255)
            
            self.selection_start = None
            self.selection_end = None
            self.selected_image = None
            
            self._save_to_undo()
            self._update_preview()
    
    def _clear_selection(self) -> None:
        """選択を解除"""
        self.selection_start = None
        self.selection_end = None
        self.selected_image = None
        self._update_preview()
    
    # ===== 変形メソッド (2025-10-13: 反転・回転・中央配置) =====
    
    def _flip_horizontal(self) -> None:
        """左右反転"""
        self.edit_bitmap = self.edit_bitmap.transpose(Image.FLIP_LEFT_RIGHT)
        self._save_to_undo()
        self._update_preview()
    
    def _flip_vertical(self) -> None:
        """上下反転"""
        self.edit_bitmap = self.edit_bitmap.transpose(Image.FLIP_TOP_BOTTOM)
        self._save_to_undo()
        self._update_preview()
    
    def _rotate_90(self) -> None:
        """90度回転（反時計回り）"""
        self.edit_bitmap = self.edit_bitmap.transpose(Image.ROTATE_90)
        self._save_to_undo()
        self._update_preview()
    
    def _center_horizontal(self) -> None:
        """左右中央配置。選択中は選択範囲をキャンバス中心に移動し、
        選択していない場合は描画部分全体を中央に配置する。"""
        # 選択領域があればその中心を計算して移動
        if self.selected_image and self.selection_start and self.selection_end:
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            sel_width = x2 - x1
            # キャンバス中心に合わせるターゲット位置
            target_x = (Config.CANVAS_SIZE - sel_width) // 2
            offset_x = target_x - x1
            if offset_x != 0:
                # 元の領域を白で塗りつぶし
                draw = ImageDraw.Draw(self.edit_bitmap)
                # 元の領域を白で塗りつぶす（終点を含まないよう -1）
                draw.rectangle((x1, y1, x2 - 1, y2 - 1), fill=255)
                # 新しい位置に貼り付け（透明部分を無視）
                new_x1 = max(0, min(target_x, Config.CANVAS_SIZE - sel_width))
                # 255未満のピクセルを全て貼り付け対象とする
                mask = self.selected_image.point(lambda p: 255 if p < 255 else 0)
                self.edit_bitmap.paste(self.selected_image, (new_x1, y1), mask)
                # 選択状態を更新
                self.selection_start = (new_x1, y1)
                self.selection_end = (new_x1 + sel_width, y2)
                self._save_to_undo()
                self._update_preview()
            return
        # 選択されていない場合はコンテンツ全体を対象
        bbox = self.edit_bitmap.getbbox()
        if not bbox:
            return
        x1, y1, x2, y2 = bbox
        content_width = x2 - x1
        target_x = (Config.CANVAS_SIZE - content_width) // 2
        offset_x = target_x - x1
        if offset_x == 0:
            return
        # 新しい画像を作成し中央配置
        new_img = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
        content = self.edit_bitmap.crop(bbox)
        new_img.paste(content, (target_x, y1))
        self.edit_bitmap = new_img
        self._save_to_undo()
        self._update_preview()
    
    def _center_vertical(self) -> None:
        """上下中央配置。選択範囲があればその中心をキャンバス中央に移動する。"""
        # 選択領域がある場合
        if self.selected_image and self.selection_start and self.selection_end:
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            sel_height = y2 - y1
            target_y = (Config.CANVAS_SIZE - sel_height) // 2
            offset_y = target_y - y1
            if offset_y != 0:
                draw = ImageDraw.Draw(self.edit_bitmap)
                draw.rectangle((x1, y1, x2 - 1, y2 - 1), fill=255)
                new_y1 = max(0, min(target_y, Config.CANVAS_SIZE - sel_height))
                # マスクを使用して透明部分を無視
                mask = self.selected_image.point(lambda p: 255 if p < 255 else 0)
                self.edit_bitmap.paste(self.selected_image, (x1, new_y1), mask)
                self.selection_start = (x1, new_y1)
                self.selection_end = (x2, new_y1 + sel_height)
                self._save_to_undo()
                self._update_preview()
            return
        # 選択が無い場合は全体を上下中央に配置
        bbox = self.edit_bitmap.getbbox()
        if not bbox:
            return
        x1, y1, x2, y2 = bbox
        content_height = y2 - y1
        target_y = (Config.CANVAS_SIZE - content_height) // 2
        offset_y = target_y - y1
        if offset_y == 0:
            return
        new_img = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
        content = self.edit_bitmap.crop(bbox)
        new_img.paste(content, (x1, target_y))
        self.edit_bitmap = new_img
        self._save_to_undo()
        self._update_preview()
    
    def _center_both(self) -> None:
        """上下左右中央配置。選択範囲があればその中心をキャンバス中央に移動する。"""
        # 選択範囲がある場合
        if self.selected_image and self.selection_start and self.selection_end:
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            sel_w = x2 - x1
            sel_h = y2 - y1
            target_x = (Config.CANVAS_SIZE - sel_w) // 2
            target_y = (Config.CANVAS_SIZE - sel_h) // 2
            # 塗りつぶして移動
            draw = ImageDraw.Draw(self.edit_bitmap)
            draw.rectangle((x1, y1, x2 - 1, y2 - 1), fill=255)
            new_x1 = max(0, min(target_x, Config.CANVAS_SIZE - sel_w))
            new_y1 = max(0, min(target_y, Config.CANVAS_SIZE - sel_h))
            # マスクを使用して黒い部分のみを貼り付け
            mask = self.selected_image.point(lambda p: 255 if p < 255 else 0)
            self.edit_bitmap.paste(self.selected_image, (new_x1, new_y1), mask)
            self.selection_start = (new_x1, new_y1)
            self.selection_end = (new_x1 + sel_w, new_y1 + sel_h)
            self._save_to_undo()
            self._update_preview()
            return
        # 選択が無ければ全体を中央に配置
        bbox = self.edit_bitmap.getbbox()
        if not bbox:
            return
        x1, y1, x2, y2 = bbox
        content_width = x2 - x1
        content_height = y2 - y1
        target_x = (Config.CANVAS_SIZE - content_width) // 2
        target_y = (Config.CANVAS_SIZE - content_height) // 2
        new_img = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
        content = self.edit_bitmap.crop(bbox)
        new_img.paste(content, (target_x, target_y))
        self.edit_bitmap = new_img
        self._save_to_undo()
        self._update_preview()
    
    # ===== 操作メソッド (2025-10-13: 元に戻す・保存・クリア等) =====
    
    def _undo(self) -> None:
        """元に戻す"""
        if len(self.undo_stack) > 1:
            # 現在の状態をリドゥスタックへ
            self.redo_stack.append(self.undo_stack.pop())
            # 1つ前の状態を復元
            self.edit_bitmap = self.undo_stack[-1].copy()
            self._update_preview()
    
    def _redo(self) -> None:
        """やり直し"""
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.undo_stack.append(state)
            self.edit_bitmap = state.copy()
            self._update_preview()
    
    def _copy(self) -> None:
        """全体をコピー"""
        self.project.clipboard = self.edit_bitmap.copy()
        messagebox.showinfo('コピー', 'グリフ全体をコピーしました')
    
    def _paste(self) -> None:
        """貼り付け (2025-11-06: プレビュー機能追加)"""
        # [DEBUG] 2025-11-06: クリップボード状態をログ出力
        print(f"[DEBUG] _paste called, clipboard: {self.project.clipboard}")
        if self.project.clipboard:
            print(f"[DEBUG] clipboard size: {self.project.clipboard.size}")

        if not self.project.clipboard:
            messagebox.showwarning('警告', 'クリップボードが空です')
            return

        # クリップボードのサイズがキャンバスと同じ場合は全体を置き換え
        if self.project.clipboard.size == (Config.CANVAS_SIZE, Config.CANVAS_SIZE):
            self.edit_bitmap = self.project.clipboard.copy()
        else:
            # [ADD] 2025-11-06: プレビューダイアログで位置調整
            preview_dialog = PastePreviewDialog(self, self.edit_bitmap, self.project.clipboard)
            self.wait_window(preview_dialog)

            if preview_dialog.result is None:
                return  # キャンセルされた

            paste_x, paste_y = preview_dialog.result
            w, h = self.project.clipboard.size

            # 透過処理付き貼り付け
            from PIL import ImageChops
            clipboard_copy = self.project.clipboard.copy()

            # 貼り付け先の領域を切り出し
            region = self.edit_bitmap.crop((paste_x, paste_y, paste_x + w, paste_y + h))

            # 合成: より黒い方を採用（白は透明として扱われる）
            result = ImageChops.darker(region, clipboard_copy)

            # 結果を貼り付け
            self.edit_bitmap.paste(result, (paste_x, paste_y))

        self._save_to_undo()
        self._update_preview()
    
    def _clear(self) -> None:
        """全消去"""
        if messagebox.askyesno('確認', '全て消去しますか？'):
            self.edit_bitmap = Image.new('L', (Config.CANVAS_SIZE, Config.CANVAS_SIZE), 255)
            self._save_to_undo()
            self._update_preview()
    
    def _save(self) -> None:
        """保存してプロジェクトに反映"""
        # グリフを更新
        self.project.set_glyph(self.char_code, self.edit_bitmap.copy(), is_edited=True)
        self.project.mark_as_edited(self.char_code)
        
        # コールバック実行
        if self.on_save:
            self.on_save()
        
        messagebox.showinfo('保存', '保存しました')
    
    def _save_png(self) -> None:
        """PNG保存"""
        default_name = f'U+{self.char_code:04X}.png'
        path = filedialog.asksaveasfilename(
            title='PNG保存',
            defaultextension='.png',
            initialfile=default_name,
            filetypes=[('PNG Image', '*.png'), ('All Files', '*.*')]
        )
        
        if path:
            # 透過PNG変換
            rgba_img = Image.new('RGBA', self.edit_bitmap.size, (255, 255, 255, 0))
            pixels_gray = self.edit_bitmap.load()
            pixels_rgba = rgba_img.load()
            
            for y in range(self.edit_bitmap.size[1]):
                for x in range(self.edit_bitmap.size[0]):
                    gray_value = pixels_gray[x, y]
                    alpha = 255 - gray_value
                    pixels_rgba[x, y] = (0, 0, 0, alpha)
            
            rgba_img.save(path, 'PNG')
            messagebox.showinfo('保存完了', f'保存しました:\n{path}')
    
    def _mark_as_empty(self) -> None:
        """空白グリフとしてマーク"""
        if messagebox.askyesno('確認', 'このグリフを空白としてマークしますか？'):
            # 空グリフとして登録
            self.project.glyphs[self.char_code] = GlyphData(self.char_code, None, is_edited=True)
            
            if self.on_save:
                self.on_save()
            
            self.destroy()
    
    def _load_from_other_font(self) -> None:
        """他のフォントから読み込み"""
        path = filedialog.askopenfilename(
            title='フォントファイルを選択',
            filetypes=[
                ('TrueType Font', '*.ttf'),
                ('OpenType Font', '*.otf'),
                ('All Files', '*.*')
            ]
        )
        
        if not path:
            return
        
        try:
            # 該当文字をレンダリング
            font = ImageFont.truetype(path, size=Config.FONT_RENDER_SIZE)
            char = chr(self.char_code)
            
            bitmap = FontRenderer._render_char(char, font)
            
            if bitmap:
                self.edit_bitmap = bitmap
                self._save_to_undo()
                self._update_preview()
                messagebox.showinfo('読込完了', f'フォントから読み込みました:\n{path}')
            else:
                messagebox.showwarning('警告', 'この文字はフォントに存在しません')
        
        except Exception as e:
            messagebox.showerror('エラー', f'フォント読み込み失敗:\n{e}')
    
    def _show_settings_dialog(self) -> None:
        """設定ダイアログ表示"""
        dialog = tk.Toplevel(self)
        dialog.title('設定')
        dialog.geometry('400x300')
        dialog.transient(self)
        
        tk.Label(dialog, text='エディタ設定', font=('Arial', 14, 'bold')).pack(pady=10)
        
        # グリッド表示設定
        tk.Label(dialog, text='グリッド間隔:').pack(pady=5)
        
        grid_var = tk.IntVar(value=Config.GRID_SPACING)
        tk.Scale(
            dialog,
            from_=16,
            to=128,
            orient='horizontal',
            variable=grid_var,
            length=300
        ).pack()
        
        # 適用ボタン
        def apply_settings():
            Config.GRID_SPACING = grid_var.get()
            self._update_preview()
            dialog.destroy()
        
        tk.Button(dialog, text='適用', command=apply_settings, width=10).pack(pady=20)
    
    # ===== [ADD] 2025-10-13: BLOCK10互換メソッド =====
    
    def _draw_rect(self, x0: int, y0: int, x1: int, y1: int, width: int = 1) -> None:
        """矩形描画（BLOCK10互換）"""
        draw = ImageDraw.Draw(self.edit_bitmap)
        draw.rectangle((x0, y0, x1, y1), outline=0, width=max(1, int(width)))
        self._update_preview()
    
    def _draw_ellipse(self, x0: int, y0: int, x1: int, y1: int, width: int = 1) -> None:
        """楕円描画（BLOCK10互換）"""
        draw = ImageDraw.Draw(self.edit_bitmap)
        draw.ellipse((x0, y0, x1, y1), outline=0, width=max(1, int(width)))
        self._update_preview()
    
    def _start_selection(self, x0: int, y0: int, x1: int, y1: int) -> None:
        """選択開始（BLOCK10互換）"""
        try:
            x0 = max(0, min(int(x0), Config.CANVAS_SIZE - 1))
            y0 = max(0, min(int(y0), Config.CANVAS_SIZE - 1))
            x1 = max(0, min(int(x1), Config.CANVAS_SIZE))
            y1 = max(0, min(int(y1), Config.CANVAS_SIZE))
            self.selection_start = (min(x0, x1), min(y0, y1))
            self.selection_end = (max(x0, x1), max(y0, y1))
            self.selected_image = self.edit_bitmap.crop((*self.selection_start, *self.selection_end)).copy()
            self._update_preview()
        except Exception:
            pass
    
    def _on_copy(self) -> None:
        """コピー（BLOCK10互換）"""
        self._copy()
    
    def _on_cut(self) -> None:
        """切り取り（BLOCK10互換）"""
        self._cut_selection()
    
    def _on_paste(self) -> None:
        """貼り付け（BLOCK10互換）"""
        self._paste()
    
    def commit_to_project_without_close(self) -> None:
        """エディタ内容をプロジェクトへ反映（BLOCK10互換）"""
        self.project.glyphs[self.char_code] = GlyphData(
            self.char_code, 
            self.edit_bitmap.copy(), 
            is_edited=True
        )
        self.project.dirty = True
        if self.on_save:
            self.on_save()
    
    def _save_from_editor(self, event: Optional[tk.Event] = None) -> None:
        """⌘S/Ctrl+S: 保存（BLOCK10互換）"""
        self.commit_to_project_without_close()
        if hasattr(self.master, '_save_project_dialog'):
            self.master._save_project_dialog()  # type: ignore
    
    # ===== [ADD] 2025-10-17: 座標変換・ハンドル取得メソッド =====
    
    def _normalize_selection(self) -> None:
        """選択範囲を正規化"""
        if self.selection_start and self.selection_end:
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            self.selection_start = (min(x1, x2), min(y1, y2))
            self.selection_end = (max(x1, x2), max(y1, y2))
    
    def _canvas_to_image_coords(self, canvas_x: float, canvas_y: float) -> Tuple[int, int]:
        """キャンバス座標を画像座標に変換"""
        c_x = self.preview_canvas.canvasx(canvas_x)
        c_y = self.preview_canvas.canvasy(canvas_y)
        img_x = int(c_x / self.zoom_level)
        img_y = int(c_y / self.zoom_level)
        img_x = max(0, min(img_x, Config.CANVAS_SIZE - 1))
        img_y = max(0, min(img_y, Config.CANVAS_SIZE - 1))
        return img_x, img_y
    
    def _get_handle_at(self, canvas_x: float, canvas_y: float) -> Optional[str]:
        """ハンドルを取得"""
        if not (self.selection_start and self.selection_end):
            return None
        
        self._normalize_selection()
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        
        cx1 = x1 * self.zoom_level
        cy1 = y1 * self.zoom_level
        cx2 = x2 * self.zoom_level
        cy2 = y2 * self.zoom_level
        
        cx_mid = (cx1 + cx2) / 2
        cy_mid = (cy1 + cy2) / 2
        
        threshold = 8
        
        handles = {
            'nw': (cx1, cy1),
            'n': (cx_mid, cy1),
            'ne': (cx2, cy1),
            'e': (cx2, cy_mid),
            'se': (cx2, cy2),
            's': (cx_mid, cy2),
            'sw': (cx1, cy2),
            'w': (cx1, cy_mid)
        }
        
        scroll_x = self.preview_canvas.canvasx(canvas_x)
        scroll_y = self.preview_canvas.canvasy(canvas_y)
        
        for handle, (hx, hy) in handles.items():
            if abs(scroll_x - hx) <= threshold and abs(scroll_y - hy) <= threshold:
                return handle
        
        return None
    
    def _get_text_layer_handle_at(self, canvas_x: float, canvas_y: float) -> Optional[str]:
        """テキストレイヤーのハンドルを取得"""
        if not self.text_layer:
            return None
        
        x_pos, y_pos = self.text_layer_pos
        x_end = x_pos + self.text_layer.width
        y_end = y_pos + self.text_layer.height
        
        cx1 = x_pos * self.zoom_level
        cy1 = y_pos * self.zoom_level
        cx2 = x_end * self.zoom_level
        cy2 = y_end * self.zoom_level
        
        cx_mid = (cx1 + cx2) / 2
        cy_mid = (cy1 + cy2) / 2
        
        threshold = 8
        
        handles = {
            'nw': (cx1, cy1),
            'n': (cx_mid, cy1),
            'ne': (cx2, cy1),
            'e': (cx2, cy_mid),
            'se': (cx2, cy2),
            's': (cx_mid, cy2),
            'sw': (cx1, cy2),
            'w': (cx1, cy_mid)
        }
        
        scroll_x = self.preview_canvas.canvasx(canvas_x)
        scroll_y = self.preview_canvas.canvasy(canvas_y)
        
        for handle, (hx, hy) in handles.items():
            if abs(scroll_x - hx) <= threshold and abs(scroll_y - hy) <= threshold:
                return handle
        
        return None
    
    def _resize_by_handle(self, x: int, y: int) -> None:
        """選択領域をハンドルでリサイズ"""
        if not (self.resize_origin and self.resize_handle):
            return
        
        (x1, y1), (x2, y2) = self.resize_origin
        handle = self.resize_handle
        
        new_x1, new_y1, new_x2, new_y2 = x1, y1, x2, y2
        
        if 'n' in handle:
            new_y1 = min(y, y2 - 1)
        if 's' in handle:
            new_y2 = max(y, y1 + 1)
        if 'w' in handle:
            new_x1 = min(x, x2 - 1)
        if 'e' in handle:
            new_x2 = max(x, x1 + 1)
        
        new_x1 = max(0, new_x1)
        new_y1 = max(0, new_y1)
        new_x2 = min(Config.CANVAS_SIZE, new_x2)
        new_y2 = min(Config.CANVAS_SIZE, new_y2)
        
        self.resize_preview_rect = (new_x1, new_y1, new_x2, new_y2)
    
    def _apply_resize_by_handle(self) -> None:
        """選択領域のリサイズを確定"""
        if not (self.selected_image and self.resize_preview_rect):
            return
        
        x1, y1, x2, y2 = self.resize_preview_rect
        new_w = x2 - x1
        new_h = y2 - y1
        
        if new_w <= 0 or new_h <= 0:
            return
        
        resized = self.selected_image.resize((new_w, new_h), Image.LANCZOS)
        
        draw = ImageDraw.Draw(self.edit_bitmap)
        old_x1, old_y1 = self.selection_start
        old_x2, old_y2 = self.selection_end
        draw.rectangle((old_x1, old_y1, old_x2, old_y2), fill=255)
        
        self.edit_bitmap.paste(resized, (x1, y1))
        
        self.selection_start = (x1, y1)
        self.selection_end = (x2, y2)
        self.selected_image = resized
        
        self._save_to_undo()
        self._update_preview()
    
    def _resize_text_layer_by_handle(self, x: int, y: int) -> None:
        """テキストレイヤーをハンドルでリサイズ"""
        if not (self.resize_origin and self.resize_handle):
            return
        
        (x1, y1), (x2, y2) = self.resize_origin
        handle = self.resize_handle
        
        new_x1, new_y1, new_x2, new_y2 = x1, y1, x2, y2
        
        if 'n' in handle:
            new_y1 = min(y, y2 - 1)
        if 's' in handle:
            new_y2 = max(y, y1 + 1)
        if 'w' in handle:
            new_x1 = min(x, x2 - 1)
        if 'e' in handle:
            new_x2 = max(x, x1 + 1)
        
        new_x1 = max(0, new_x1)
        new_y1 = max(0, new_y1)
        new_x2 = min(Config.CANVAS_SIZE, new_x2)
        new_y2 = min(Config.CANVAS_SIZE, new_y2)
        
        self.resize_preview_rect = (new_x1, new_y1, new_x2, new_y2)
    
    def _apply_text_layer_resize(self) -> None:
        """テキストレイヤーのリサイズを確定"""
        if not (self.text_layer and self.resize_preview_rect):
            return
        
        x1, y1, x2, y2 = self.resize_preview_rect
        new_w = x2 - x1
        new_h = y2 - y1
        
        if new_w <= 0 or new_h <= 0:
            return
        
        if self.text_layer_original:
            resized = self.text_layer_original.resize((new_w, new_h), Image.LANCZOS)
        else:
            resized = self.text_layer.resize((new_w, new_h), Image.LANCZOS)
        
        self.text_layer = resized
        self.text_layer_pos = (x1, y1)
        self.text_layer_resized_size = (new_w, new_h)
        self.text_layer_resized_pos = (x1, y1)

        # [ADD] 2025-10-23: テキストエッジマスクもリサイズに追従させる
        # 既存のエッジマスクが存在する場合、現在のサイズに合わせて拡大縮小する。
        # NEARESTを使うことでマスクのバイナリ性を保つ。
        try:
            if getattr(self, 'text_edge_mask', None):
                self.text_edge_mask = self.text_edge_mask.resize((new_w, new_h), Image.NEAREST)
            if getattr(self, 'text_edge_mask_commit', None):
                self.text_edge_mask_commit = self.text_edge_mask_commit.resize((new_w, new_h), Image.NEAREST)
        except Exception:
            pass
        
        self.resize_preview_rect = None
        self._update_preview()
    
    # ===== [ADD] 2025-10-17: ズーム機能 =====
    
    def _on_space_press(self, event: tk.Event) -> None:
        """スペースキー押下でパンモード"""
        if not self.is_panning:
            self.is_panning = True
            self.preview_canvas.config(cursor='hand2')
    
    def _on_space_release(self, event: tk.Event) -> None:
        """スペースキー解放でパンモード解除"""
        if self.is_panning:
            self.is_panning = False
            self.preview_canvas.config(cursor='')
    
    def _zoom_in(self) -> None:
        """ズームイン"""
        """
        ズームイン：現在の倍率より大きい最も近い倍率に切り替える。定義されている範囲よりも大きい場合は2倍にする。
        """
        # 既存レベルから次に大きい倍率を取得
        sorted_levels = sorted(set(self.zoom_levels + [self.zoom_level]))
        try:
            idx = sorted_levels.index(self.zoom_level)
        except ValueError:
            # 万が一現在の倍率がリストにない場合は標準倍率1.0として扱う
            idx = sorted_levels.index(1.0) if 1.0 in sorted_levels else 0
        # 次の倍率が存在すればそれを採用
        if idx < len(sorted_levels) - 1:
            new_zoom = sorted_levels[idx + 1]
        else:
            # 最大値より大きくする場合は倍にする
            new_zoom = self.zoom_level * 2
        self.zoom_level = new_zoom
        self.zoom_label.config(text=f'{int(self.zoom_level * 100)}%')
        self._update_preview()
    
    def _zoom_out(self) -> None:
        """ズームアウト"""
        """
        ズームアウト：現在の倍率より小さい最も近い倍率に切り替える。定義されている範囲よりも小さい場合は半分にする。
        """
        # 既存レベルから次に小さい倍率を取得
        sorted_levels = sorted(set(self.zoom_levels + [self.zoom_level]))
        try:
            idx = sorted_levels.index(self.zoom_level)
        except ValueError:
            idx = sorted_levels.index(1.0) if 1.0 in sorted_levels else 0
        if idx > 0:
            new_zoom = sorted_levels[idx - 1]
        else:
            new_zoom = max(self.zoom_level / 2, 0.01)
        self.zoom_level = new_zoom
        self.zoom_label.config(text=f'{int(self.zoom_level * 100)}%')
        self._update_preview()
    
    def _reset_zoom(self) -> None:
        """ズームリセット"""
        self.zoom_level = 1.0
        self.zoom_label.config(text='100%')
        self.pan_offset = [0, 0]
        self._update_preview()
    
    # ===== [ADD] 2025-10-17: マウスイベントハンドラ =====
    
    def _on_mouse_down(self, event: tk.Event) -> None:
        """マウスボタン押下"""
        self.drag_start = (event.x, event.y)
        if self.is_panning:
            self.preview_canvas.scan_mark(event.x, event.y)
            return
        
        x, y = self._canvas_to_image_coords(event.x, event.y)
        
        # テキストレイヤーのモード
        if self.is_text_mode and self.text_layer:
            if self.current_tool == 'move':
                x_pos, y_pos = self.text_layer_pos
                x_end = x_pos + self.text_layer.width
                y_end = y_pos + self.text_layer.height
                if x_pos <= x < x_end and y_pos <= y < y_end:
                    self.is_moving = True
                    self.move_start_offset = (x - x_pos, y - y_pos)
                    return
            elif self.current_tool == 'resize':
                handle = self._get_text_layer_handle_at(event.x, event.y)
                if handle:
                    self.is_resizing = True
                    self.resize_handle = handle
                    x_pos, y_pos = self.text_layer_pos
                    x_end = x_pos + self.text_layer.width
                    y_end = y_pos + self.text_layer.height
                    self.resize_origin = ((x_pos, y_pos), (x_end, y_end))
                    self.resize_start_point = (x, y)
                    return
        
        # 通常モード
        if self.current_tool == 'select':
            # [ADD] 2025-10-23: 選択モードでも既存選択の移動・リサイズを可能にする
            if self.selected_image and self.selection_start and self.selection_end:
                self._normalize_selection()
                # まずリサイズハンドルをクリックしているかチェック
                handle = self._get_handle_at(event.x, event.y)
                if handle:
                    # リサイズ開始
                    self.is_resizing = True
                    self.resize_handle = handle
                    self.resize_origin = (self.selection_start, self.selection_end)
                    self.resize_start_point = (x, y)
                    return
                # ハンドル以外で選択領域内をクリックした場合は移動
                x0, y0 = self.selection_start
                x1, y1 = self.selection_end
                if x0 <= x < x1 and y0 <= y < y1:
                    self.is_moving = True
                    self.move_start_offset = (x - x0, y - y0)
                    self.move_current_pos = (x0, y0)
                    return
            # 既存選択を無視して新規選択を開始
            self.selection_start = (x, y)
            self.selection_end = (x, y)
            self.selected_image = None
            self.is_moving = False
            self.is_resizing = False
            self.shape_start = None
            self.shape_end = None
        elif self.current_tool in ['pen', 'eraser']:
            if self.is_text_mode:
                messagebox.showinfo('情報', 'テキスト入力モード中は描画できません\n「決定」または「キャンセル」してください')
                return
            self.is_drawing = True
            self.last_x = x
            self.last_y = y
            self._draw_point(x, y)
        elif self.current_tool == 'fill':
            if self.is_text_mode:
                messagebox.showinfo('情報', 'テキスト入力モード中は塗りつぶしできません')
                return
            self._flood_fill(x, y)
        elif self.current_tool == 'move':
            if self.selected_image and self.selection_start and self.selection_end:
                self._normalize_selection()
                x0, y0 = self.selection_start
                x1, y1 = self.selection_end
                if x0 <= x < x1 and y0 <= y < y1:
                    self.is_moving = True
                    self.move_start_offset = (x - x0, y - y0)
                    self.move_current_pos = (x0, y0)
                    return
        elif self.current_tool == 'resize':
            if self.selected_image and self.selection_start and self.selection_end:
                self._normalize_selection()
                handle = self._get_handle_at(event.x, event.y)
                if handle:
                    self.is_resizing = True
                    self.resize_handle = handle
                    self.resize_origin = (self.selection_start, self.selection_end)
                    self.resize_start_point = (x, y)
                    return
        elif self.current_tool in ['line', 'rect', 'ellipse']:
            if self.is_text_mode:
                messagebox.showinfo('情報', 'テキスト入力モード中は図形描画できません')
                return
            self.shape_start = (x, y)
            self.shape_end = (x, y)
        elif self.current_tool == 'guide':
            self.guidelines.append(('h', y))
            self.guidelines.append(('v', x))
            self._update_preview()
    
    def _on_mouse_drag(self, event: tk.Event) -> None:
        """マウスドラッグ"""
        if self.is_panning:
            self.preview_canvas.scan_dragto(event.x, event.y, gain=1)
            self._update_preview()
            return
        
        x, y = self._canvas_to_image_coords(event.x, event.y)
        
        # テキストレイヤー移動
        if self.is_text_mode and self.is_moving and self.text_layer:
            if self.move_start_offset:
                offset_x, offset_y = self.move_start_offset
                dest_x = x - offset_x
                dest_y = y - offset_y
                
                w = self.text_layer.width
                h = self.text_layer.height
                dest_x = max(-w + 10, min(dest_x, Config.CANVAS_SIZE - 10))
                dest_y = max(-h + 10, min(dest_y, Config.CANVAS_SIZE - 10))
                
                self.text_layer_pos = (dest_x, dest_y)
                self._update_preview_fast()
            return
        
        # テキストレイヤーリサイズ
        if self.is_text_mode and self.is_resizing and self.text_layer:
            if self.resize_origin and self.resize_handle:
                self._resize_text_layer_by_handle(x, y)
                self._update_preview_fast()
            return
        
        # 通常の操作
        if self.current_tool == 'select':
            # [ADD] 2025-10-23: 選択モードでも移動・リサイズを可能にする
            if self.is_moving and self.move_start_offset and self.selected_image:
                offset_x, offset_y = self.move_start_offset
                dest_x = x - offset_x
                dest_y = y - offset_y
                w = self.selected_image.width
                h = self.selected_image.height
                dest_x = max(-w + 10, min(dest_x, Config.CANVAS_SIZE - 10))
                dest_y = max(-h + 10, min(dest_y, Config.CANVAS_SIZE - 10))
                self.move_current_pos = (dest_x, dest_y)
                self._update_preview_fast()
                return
            if self.is_resizing and self.selected_image and self.resize_origin and self.resize_handle:
                self._resize_by_handle(x, y)
                self._update_preview_fast()
                return
            # 移動・リサイズでない場合は通常の選択範囲更新
            self.selection_end = (x, y)
            self._update_preview()
        elif self.is_drawing and self.current_tool in ['pen', 'eraser']:
            if self.last_x is not None and self.last_y is not None:
                self._draw_line(self.last_x, self.last_y, x, y)
            self.last_x = x
            self.last_y = y
            self._update_preview()
        elif self.current_tool == 'move' and self.is_moving:
            if self.move_start_offset:
                offset_x, offset_y = self.move_start_offset
                dest_x = x - offset_x
                dest_y = y - offset_y
                w = self.selected_image.width if self.selected_image else 0
                h = self.selected_image.height if self.selected_image else 0
                dest_x = max(-w + 10, min(dest_x, Config.CANVAS_SIZE - 10))
                dest_y = max(-h + 10, min(dest_y, Config.CANVAS_SIZE - 10))
                self.move_current_pos = (dest_x, dest_y)
                self._update_preview()
        elif self.current_tool == 'resize' and self.is_resizing:
            if self.resize_origin and self.resize_handle:
                self._resize_by_handle(x, y)
                self._update_preview()
        elif self.current_tool in ['line', 'rect', 'ellipse'] and self.shape_start:
            self.shape_end = (x, y)
            self._update_preview()
    
    def _on_mouse_up(self, event: tk.Event) -> None:
        """マウスボタン解放"""
        if self.is_panning:
            self.is_panning = False
            self.pan_start = None
            return

        # テキストレイヤー移動終了
        if self.is_text_mode and self.is_moving:
            self.is_moving = False
            self.move_start_offset = None
            self.move_current_pos = None
            self._update_preview()
            return
        
        # テキストレイヤーリサイズ終了
        if self.is_text_mode and self.is_resizing:
            self.is_resizing = False
            self._apply_text_layer_resize()
            self.resize_origin = None
            self.resize_handle = None
            self.resize_start_point = None
            self.resize_preview_rect = None
            return

        x, y = self._canvas_to_image_coords(event.x, event.y)

        # ペン・消しゴム終了
        if self.is_drawing and self.current_tool in ['pen', 'eraser']:
            self.is_drawing = False
            self._save_to_undo()
            self._update_preview()
            return


        # 選択モードでの移動・リサイズ・選択確定
        if self.current_tool == 'select' and self.selection_start:
            # 移動確定
            if self.is_moving:
                self.is_moving = False
                self._apply_translation()
                self.move_start_offset = None
                self.move_current_pos = None
                return
            # リサイズ確定
            if self.is_resizing:
                self.is_resizing = False
                self._apply_resize_by_handle()
                self.resize_origin = None
                self.resize_handle = None
                self.resize_start_point = None
                self.resize_preview_rect = None
                return
            # 新規選択の確定
            self.selection_end = (x, y)
            self._finalize_selection()
            self._update_preview()
            return

        # 移動確定
        if self.current_tool == 'move' and self.is_moving:
            self.is_moving = False
            self._apply_translation()
            self.move_start_offset = None
            self.move_current_pos = None
            return

        # リサイズ確定
        if self.current_tool == 'resize' and self.is_resizing:
            self.is_resizing = False
            self._apply_resize_by_handle()
            self.resize_origin = None
            self.resize_handle = None
            self.resize_start_point = None
            self.resize_preview_rect = None
            return

        # 図形描画確定
        if self.current_tool in ['line', 'rect', 'ellipse'] and self.shape_start:
            self.shape_end = (x, y)
            self._commit_shape(self.shape_start, self.shape_end)
            self.shape_start = None
            self.shape_end = None
            return

        self._update_preview()
    
    def _on_mouse_move(self, event: tk.Event) -> None:
        """マウス移動"""
        # リサイズツール選択時、ハンドルにカーソルを合わせたらカーソル変更
        if self.current_tool == 'resize' and not self.is_resizing:
            if self.is_text_mode and self.text_layer:
                handle = self._get_text_layer_handle_at(event.x, event.y)
            else:
                handle = self._get_handle_at(event.x, event.y)
            
            if handle:
                cursor_map = {
                    'nw': 'size_nw_se', 'se': 'size_nw_se',
                    'ne': 'size_ne_sw', 'sw': 'size_ne_sw',
                    'n': 'size_ns', 's': 'size_ns',
                    'e': 'size_we', 'w': 'size_we'
                }
                self.preview_canvas.config(cursor=cursor_map.get(handle, ''))
            else:
                self.preview_canvas.config(cursor='')
        
        # ペン・消しゴムツール選択時、ブラシカーソル表示
        if self.current_tool in ['pen', 'eraser']:
            if self.brush_cursor:
                self.preview_canvas.delete(self.brush_cursor)
            
            radius = int(self.brush_size * self.zoom_level / 2)
            
            self.brush_cursor = self.preview_canvas.create_oval(
                event.x - radius, event.y - radius,
                event.x + radius, event.y + radius,
                outline='red' if self.current_tool == 'pen' else 'blue',
                width=1,
                dash=(2, 2)
            )

    # ===== [本体 BLOCK5.7-END] =====

    # [ADD] 2025-10-23: 偏旁パーツ貼り付けメソッド
    def insert_part_image(self, part_image: Image.Image, scale_hint: float = 1.0, offset_hint: Tuple[float, float] = (0.0, 0.0)) -> None:
        """
        偏旁パーツを編集キャンバスに貼り付ける。
        part_image: グレースケールImage（255は透過扱い）
        scale_hint: 貼り付け時の倍率（1.0=原寸）
        offset_hint: キャンバス中心からの相対オフセット (x,y)（-1.0〜1.0程度）
        """
        try:
            # 型チェック
            if not isinstance(part_image, PILImage.Image):
                raise ValueError('無効な画像')
            # グレースケールに変換
            if part_image.mode != 'L':
                part_image = part_image.convert('L')
            # 貼り付けサイズ計算
            orig_w, orig_h = part_image.size
            new_w = max(1, int(orig_w * scale_hint))
            new_h = max(1, int(orig_h * scale_hint))
            if (new_w, new_h) != (orig_w, orig_h):
                resized = part_image.resize((new_w, new_h), Image.Resampling.NEAREST)
            else:
                resized = part_image.copy()
            # オフセット計算 (キャンバス中心 + offset_hint * canvas_size)
            x = (Config.CANVAS_SIZE - new_w) // 2 + int(offset_hint[0] * Config.CANVAS_SIZE)
            y = (Config.CANVAS_SIZE - new_h) // 2 + int(offset_hint[1] * Config.CANVAS_SIZE)
            # 範囲内に収める
            x = max(0, min(x, Config.CANVAS_SIZE - new_w))
            y = max(0, min(y, Config.CANVAS_SIZE - new_h))
            # 透過用マスク: 255→0(透明), それ以外→255(不透明)
            mask = resized.point(lambda p: 0 if p == 255 else 255)
            # ビットマップに貼り付け
            self.edit_bitmap.paste(resized, (x, y), mask)
            # Undo履歴追加
            self._save_to_undo()
            # プレビュー更新
            self._update_preview()
            # ツールを移動モードに変更してすぐに調整できるようにする
            self._set_tool('move')
        except Exception as e:
            messagebox.showerror('エラー', f'パーツ貼り付けに失敗しました: {e}')

# ===== [本体 BLOCK5.7-END] =====











# ===== [本体 BLOCK6-BEGIN] メインアプリケーション (2025-10-11: 型ヒント追加、エラーハンドリング改善) =====

class FontEditorApp(tk.Tk):
    """メインアプリケーション"""
    
    def __init__(self) -> None:
        self._open_editors: List[GlyphEditor] = []  # 開いているエディタ追跡
        super().__init__()
        
        self.title('フォントエディタ - ハイブリッド方式(全機能版)')
        self.geometry(f'{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}')
        
        self.project: FontProject = FontProject()
        self.bg_loader: Optional['BackgroundLoader'] = None  # バックグラウンドローダー (2025-10-03)
        self.current_filter: str = 'all'  # 現在のフィルタ (2025-10-03)

        # [ADD] 2025-11-06: 自動保存用
        self.auto_save_enabled = Config.AUTO_SAVE_ENABLED
        self.auto_save_interval = Config.AUTO_SAVE_INTERVAL * 1000  # ミリ秒に変換

        self._setup_ui()

        # キーボードショートカット (2025-10-03)
        self.bind('<Control-z>', lambda e: self.grid_view.winfo_children() and None)
        self.bind('<Control-o>', lambda e: self._open_font())
        self.bind('<Control-f>', lambda e: self._show_filter_dialog())
        self.bind('<Control-p>', lambda e: self._show_text_preview())

        # バックグラウンド読み込み結果チェック用タイマー (2025-10-03)
        self.after(100, self._check_bg_loader)

        # [ADD] 2025-11-06: 自動保存タイマー
        if self.auto_save_enabled:
            self.after(self.auto_save_interval, self._auto_save_timer)
    
    def _setup_ui(self) -> None:
        """UI構築"""
        # メニューバー
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='ファイル', menu=file_menu)
        file_menu.add_command(label='フォントを開く...', command=self._open_font)
        file_menu.add_command(label='プロジェクトを保存...', command=self._save_project_dialog)
        file_menu.add_command(label='プロジェクトを開く...', command=self._open_project_dialog)
        file_menu.add_separator()
        file_menu.add_command(label='バックグラウンド読み込み停止', command=self._stop_bg_loading)
        file_menu.add_separator()
        file_menu.add_command(label='終了', command=self.quit)
        
        # 表示メニュー (2025-10-03)
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='表示', menu=view_menu)
        view_menu.add_command(label='グリフフィルタ...', command=self._show_filter_dialog)
        view_menu.add_command(label='テキストプレビュー...', command=self._show_text_preview)
        
        # エクスポートメニュー (2025-10-03)
        export_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='エクスポート', menu=export_menu)
        export_menu.add_command(label='BDF形式で保存...', command=self._export_bdf)
        export_menu.add_command(label='TTF形式で保存... (高品質アウトライン)', command=self._export_ttf)
        export_menu.add_separator()
        export_menu.add_command(label='PNG一括書き出し...', command=self._export_png_batch)
        
        # ツールバー
        toolbar = tk.Frame(self, bg=Config.COLOR_BG)
        toolbar.pack(side='top', fill='x', padx=5, pady=5)
        
        tk.Button(toolbar, text='📂 フォントを開く', command=self._open_font).pack(side='left', padx=2)
        tk.Button(toolbar, text='🔍 フィルタ', command=self._show_filter_dialog).pack(side='left', padx=2)
        tk.Button(toolbar, text='👁️ プレビュー', command=self._show_text_preview).pack(side='left', padx=2)
        # [ADD] 2025-10-23: 部首パレットを開くボタン
        tk.Button(toolbar, text='部首', command=self._open_parts_palette).pack(side='left', padx=2)
        tk.Button(toolbar, text='部首ツール', command=self._open_parts_editor).pack(side='left', padx=2)
        
        # 範囲選択ドロップダウン (2025-10-03)
        tk.Label(toolbar, text='文字範囲:', bg=Config.COLOR_BG).pack(side='left', padx=(20, 5))
        self.range_var = tk.StringVar(value=Config.DEFAULT_RANGE)
        range_combo = ttk.Combobox(
            toolbar,
            textvariable=self.range_var,
            values=list(Config.CHAR_RANGES.keys()),
            state='readonly',
            width=30
        )
        range_combo.pack(side='left', padx=5)
        range_combo.bind('<<ComboboxSelected>>', self._on_range_changed)
        
        # グリッドビュー
        self.grid_view = GridView(self, self.project, self._on_edit_char)
        self.grid_view.pack(fill='both', expand=True)
        
        # ステータスバー
        self.status_label = tk.Label(self, text='ファイル: なし', anchor='w', relief='sunken')
        self.status_label.pack(side='bottom', fill='x')
    
    def _open_font(self) -> None:
        """フォント読み込み (2025-11-06: TTC対応追加)"""
        path = filedialog.askopenfilename(
            title='フォントファイルを選択',
            filetypes=[
                ('TrueType Font', '*.ttf'),
                ('TrueType Collection', '*.ttc'),
                ('OpenType Font', '*.otf'),
                ('All Files', '*.*')
            ]
        )

        if not path:
            return

        # [ADD] 2025-11-06: TTCファイルの場合は抽出
        if path.lower().endswith('.ttc'):
            extracted_path = extract_ttf_from_ttc(path)
            if extracted_path is None:
                return  # 抽出失敗
            path = extracted_path

        # プロジェクト初期化
        self.project.font_path = path

        # [FIX v1.82.5] まず基本ラテン文字のみを読み込む（即座に作業開始可能に）
        basic_latin_range = Config.CHAR_RANGES.get('基本ラテン文字 (ASCII)', (0x0020, 0x007F))
        basic_char_codes = list(range(basic_latin_range[0], basic_latin_range[1] + 1))

        # プログレスウィンドウ作成
        progress_win = tk.Toplevel(self)
        progress_win.title('読み込み中...')
        progress_win.geometry('500x150')
        progress_win.transient(self)
        progress_win.grab_set()

        tk.Label(
            progress_win,
            text='基本ラテン文字を読み込んでいます...',
            font=('Arial', 12)
        ).pack(pady=10)

        progress_var = tk.IntVar(value=0)
        progress_bar = ttk.Progressbar(
            progress_win,
            maximum=len(basic_char_codes),
            variable=progress_var,
            length=400
        )
        progress_bar.pack(pady=10)

        progress_label = tk.Label(
            progress_win,
            text='0 / 0 文字',
            font=('Arial', 10)
        )
        progress_label.pack()

        # プログレスバー更新用コールバック
        def progress_callback(current: int, total: int) -> None:
            """プログレス更新"""
            progress_var.set(current)
            progress_label.config(text=f'{current} / {total} 文字')
            progress_win.update()

        # 基本ラテン文字を同期読み込み
        success = FontRenderer.load_font(
            path,
            basic_char_codes,
            self.project,
            progress_callback
        )

        if not success:
            progress_win.destroy()
            return

        # 基本ラテン文字範囲を読み込み済みとしてマーク
        self.project.mark_range_loaded(basic_latin_range)

        # プログレスウィンドウ閉じる
        progress_win.destroy()

        # グリッド表示更新
        self.grid_view.refresh()
        self._update_status()

        # 統計情報取得
        total = len(basic_char_codes)
        empty = self.project.get_empty_count()
        defined = total - empty
        
        # [FIX v1.82.5] 読み込み完了メッセージ
        messagebox.showinfo(
            '読込完了',
            f'基本ラテン文字の読み込みが完了しました\n\n'
            f'定義済み: {defined} / 空白: {empty}\n\n'
            f'残りの文字はバックグラウンドで読み込みます'
        )

        # [FIX v1.82.5] バックグラウンドで残りの範囲を読み込み
        self._start_background_loading_all_ranges(path, basic_latin_range)

    def _start_background_loading_all_ranges(self, font_path: str, skip_range: Tuple[int, int]) -> None:
        """[FIX v1.82.5] バックグラウンドで全ての範囲を読み込み"""
        # カテゴリごとに読み込みを行う（スキップ範囲以外）
        categories_to_load = []
        skip_codes = set(range(skip_range[0], skip_range[1] + 1))

        for range_name, (start, end) in Config.CHAR_RANGES.items():
            range_codes = set(range(start, end + 1))
            # スキップ範囲と重複していないカテゴリのみ追加
            if not range_codes.issubset(skip_codes):
                # 既に読み込まれていないコードのみを取得
                codes_to_load = sorted(range_codes - skip_codes)
                if codes_to_load:
                    categories_to_load.append((range_name, codes_to_load))

        if not categories_to_load:
            return

        # 総文字数を計算
        total_chars = sum(len(codes) for _, codes in categories_to_load)

        # バックグラウンドスレッドで読み込み
        def bg_load():
            try:
                loaded_chars = 0
                pil_font = ImageFont.truetype(font_path, size=Config.FONT_RENDER_SIZE)

                for cat_idx, (range_name, codes) in enumerate(categories_to_load):
                    cat_total = len(codes)

                    for idx, code in enumerate(codes):
                        # プロジェクトに読み込み
                        try:
                            char = chr(code)
                            bitmap = FontRenderer._render_char(char, pil_font)
                            if bitmap:
                                self.project.set_glyph(code, bitmap, is_edited=False)
                            else:
                                with self.project._lock:
                                    if code not in self.project.glyphs:
                                        self.project.glyphs[code] = GlyphData(code, None, False)
                        except Exception:
                            with self.project._lock:
                                if code not in self.project.glyphs:
                                    self.project.glyphs[code] = GlyphData(code, None, False)

                        loaded_chars += 1

                        # 50文字ごとまたはカテゴリの最後でステータス更新
                        if idx % 50 == 0 or idx == cat_total - 1:
                            progress = int(loaded_chars / total_chars * 100)
                            current_range = range_name
                            cat_progress = int((idx + 1) / cat_total * 100)
                            self.after(0, lambda p=progress, rn=current_range, cp=cat_progress, c=cat_idx+1, t=len(categories_to_load):
                                self.status_label.config(
                                    text=f'{Path(font_path).name} - 読み込み中 [{c}/{t}] {rn} ({cp}%) - 全体 {p}%'
                                ))

                # 全範囲を読み込み済みとしてマーク
                self.after(0, lambda: self._on_background_complete(font_path))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror('エラー', f'バックグラウンド読み込みエラー:\n{e}'))

        # スレッド開始
        thread = threading.Thread(target=bg_load, daemon=True)
        thread.start()

        # ステータス更新
        self.status_label.config(
            text=f'{Path(font_path).name} - バックグラウンド読み込み開始... ({len(categories_to_load)}カテゴリ, {total_chars}文字)'
        )

    def _on_background_complete(self, font_path: str) -> None:
        """[FIX v1.82.5] バックグラウンド読み込み完了"""
        # 全範囲を読み込み済みとしてマーク
        for range_name, char_range in Config.CHAR_RANGES.items():
            self.project.mark_range_loaded(char_range)

        # ステータス更新
        self.status_label.config(
            text=f'{Path(font_path).name} - バックグラウンド読み込み完了'
        )

        # グリッド表示更新
        self.grid_view.refresh()

    def _start_background_loading(self, font_path: str) -> None:
        """バックグラウンド読み込み開始"""
        # 既存のローダー停止
        if self.bg_loader:
            self.bg_loader.stop()
        
        # 新規ローダー作成
        self.bg_loader = BackgroundLoader(self.project, self._on_bg_status_update)
        self.bg_loader.start_background_load(font_path, self.project.char_range)
        
        # ステータス更新
        self.status_label.config(
            text=f'{Path(font_path).name} - バックグラウンド読み込み開始...'
        )
    
    def _check_bg_loader(self) -> None:
        """バックグラウンドローダーの結果チェック"""
        if self.bg_loader:
            self.bg_loader.check_results()
        
        # 定期的に実行
        self.after(100, self._check_bg_loader)
    
    def _on_bg_status_update(self, result: Dict[str, Any]) -> None:
        """バックグラウンド読み込みステータス更新"""
        result_type = result.get('type')
        message = result.get('message', '')
        
        if result_type == 'status':
            # 進行中
            if self.project.font_path:
                self.status_label.config(
                    text=f'{Path(self.project.font_path).name} - {message}'
                )
                
        elif result_type == 'complete':
            # 完了
            if self.project.font_path:
                self.status_label.config(
                    text=f'{Path(self.project.font_path).name} - バックグラウンド読み込み完了'
                )
                
        elif result_type == 'error':
            # エラー
            self.status_label.config(text=f'エラー: {message}')
            messagebox.showerror('エラー', message)
    
    def _on_range_changed(self, event: tk.Event) -> None:
        """文字範囲変更時の処理"""
        range_name = self.range_var.get()
        self.project.set_range(range_name)
        self.grid_view.refresh()
        self._update_status()
    
    def _on_edit_char(self, char_code: int) -> None:
        """文字編集ウィンドウを開く"""
        def on_save() -> None:
            self.grid_view.refresh()
            self._update_status()

        editor = GlyphEditor(self, self.project, char_code, on_save)
        self._open_editors.append(editor)

    def _insert_part_to_active_editor(self, part_image: Image.Image, part_name: str, offset: Tuple[float, float] = (0.0, 0.0)) -> None:
        """[FIX v1.82.8] 偏旁を変形してクリップボードに格納"""
        try:
            # 変形ダイアログを表示
            dialog = PartTransformDialog(self, part_image, part_name)
            self.wait_window(dialog)

            if dialog.result:
                # 変形された画像をクリップボードにコピー
                transformed_image = dialog.result
                self.project.clipboard = transformed_image
                # [DEBUG] 2025-11-06: クリップボード設定をログ出力
                print(f"[DEBUG] Clipboard set in _insert_part_to_active_editor: {self.project.clipboard}")
                print(f"[DEBUG] Clipboard size: {self.project.clipboard.size}")
                messagebox.showinfo("クリップボードにコピー",
                    f"偏旁「{part_name}」を変形してクリップボードにコピーしました。\n"
                    "文字編集ウィンドウで「📄 貼付」ボタンまたは Ctrl+V / ⌘V で貼り付けてください。")
        except Exception as e:
            messagebox.showerror("エラー", f"クリップボードへのコピーに失敗しました:\n{e}")

    def _update_status(self) -> None:
        """ステータス更新"""
        if self.project.font_path:
            total = len(self.project.get_char_codes())
            empty = self.project.get_empty_count()
            defined = total - empty
            
            range_name = self.range_var.get()
            
            self.status_label.config(
                text=f'{Path(self.project.font_path).name} | {range_name} | '
                     f'定義済み: {defined} / 空白: {empty}'
            )
        else:
            self.status_label.config(text='ファイル: なし')
    
    def _stop_bg_loading(self) -> None:
        """バックグラウンド読み込み停止"""
        if self.bg_loader:
            self.bg_loader.stop()
            self.status_label.config(text='バックグラウンド読み込み停止')
            messagebox.showinfo('停止', 'バックグラウンド読み込みを停止しました')

    def _auto_save_timer(self) -> None:
        """自動保存タイマー (2025-11-06)"""
        # プロジェクトが変更されており、保存先が設定されている場合のみ自動保存
        if self.project.dirty and self.project.project_path:
            try:
                # バックアップを作成
                self.project.create_backup(self.project.project_path)

                # 差分保存
                self.project.save_project(self.project.project_path, differential=True)

                # ステータス更新
                save_time = datetime.datetime.now().strftime('%H:%M:%S')
                print(f'自動保存完了: {save_time}')

            except Exception as e:
                print(f'自動保存エラー: {e}')

        # 次の自動保存をスケジュール
        if self.auto_save_enabled:
            self.after(self.auto_save_interval, self._auto_save_timer)

    def _show_filter_dialog(self) -> None:
        """フィルタダイアログを表示"""
        dialog = GlyphFilterDialog(self, self.project, self.current_filter)
        self.wait_window(dialog)
        
        if hasattr(dialog, 'result'):
            self.current_filter = dialog.result
            self.grid_view.set_filter(self.current_filter)
    
    def _show_text_preview(self) -> None:
        """テキストプレビューダイアログを表示"""
        if not self.project.glyphs:
            messagebox.showwarning('警告', 'フォントが読み込まれていません')
            return
        
        TextPreviewDialog(self, self.project)
    
    def _export_bdf(self) -> None:
        """BDF書き出し"""
        if not self.project.glyphs:
            messagebox.showwarning('警告', 'フォントが読み込まれていません')
            return
        
        path = filedialog.asksaveasfilename(
            title='BDF保存',
            defaultextension='.bdf',
            filetypes=[('BDF Font', '*.bdf'), ('All Files', '*.*')]
        )
        
        if path:
            if FontExporter.export_bdf(self.project, path):
                messagebox.showinfo('書き出し完了', f'BDF書き出し完了:\n{path}')
    
    def _export_ttf(self) -> None:
        """TTF書き出し"""
        if not self.project.glyphs:
            messagebox.showwarning('警告', 'フォントが読み込まれていません')
            return
        
        if not self.project.original_ttf_path:
            messagebox.showwarning('警告', '元のTTFファイルが必要です')
            return
        
        path = filedialog.asksaveasfilename(
            title='TTF保存',
            defaultextension='.ttf',
            filetypes=[('TrueType Font', '*.ttf'), ('All Files', '*.*')]
        )
        
        if path:
            if TTFExporter.export_ttf(self.project, path):
                messagebox.showinfo('書き出し完了', f'TTF書き出し完了:\n{path}')
    
    def _export_png_batch(self) -> None:
        """PNG一括書き出し"""
        if not self.project.glyphs:
            messagebox.showwarning('警告', 'フォントが読み込まれていません')
            return
        
        folder = filedialog.askdirectory(title='PNGを保存するフォルダを選択')
        
        if folder:
            count = FontExporter.export_png_batch(self.project, folder)
            messagebox.showinfo('書き出し完了', f'{count}個のPNGを書き出しました:\n{folder}')
# [INTEGRATED] removed misplaced _open_parts_editor (replaced by bound impl)
# [INTEGRATED] removed malformed helper block (replaced by bound impls)

# --- .fproj 保存：辞書スナップショットで安全保存 ---
def _save_project_dialog_impl(self: FontEditorApp) -> bool:
    """プロジェクト保存ダイアログ (2025-10-11: 型ヒント追加)"""
    try:
        if hasattr(self, '_stop_bg_loading'):
            self._stop_bg_loading()
    except Exception:
        pass
    try:
        if hasattr(self, '_commit_all_open_editors'):
            self._commit_all_open_editors()
    except Exception:
        pass

    path = filedialog.asksaveasfilename(
        title='プロジェクトを保存',
        defaultextension='.fproj',
        filetypes=[('Font Project', '*.fproj'), ('Single File Project', '*.fprojz')]
    )
    if not path:
        return False

    # --- 単一ファイル保存 ---
    if path.endswith('.fprojz'):
        return _export_project_singlefile_impl(self, path)

    # --- 通常フォルダ保存 ---
    if not path.endswith('.fproj'):
        path += '.fproj'

    try:
        with self.project._lock:  # (2025-10-11: スレッドセーフ化)
            orig_glyphs = self.project.glyphs
            snapshot = dict(orig_glyphs)
            self.project.glyphs = snapshot
        
        try:
            self.project.save_project(path)
            self.project.dirty = False
            messagebox.showinfo('保存完了', f'プロジェクトを保存しました:\n{path}')
            return True
        except OSError as e:
            messagebox.showerror('保存エラー', f'保存に失敗しました:\n{e}')
            return False
        except Exception as e:
            messagebox.showerror('保存エラー', f'予期しないエラー:\n{e}')
            return False
        finally:
            with self.project._lock:
                self.project.glyphs = orig_glyphs
    except Exception as e:
        messagebox.showerror('保存エラー', f'保存処理中にエラーが発生しました:\n{e}')
        return False


# --- .fproj 読込 ---
def _open_project_dialog_impl(self: FontEditorApp) -> None:
    """プロジェクト読込ダイアログ"""
    if not self._confirm_unsaved_changes():
        return
    folder = filedialog.askdirectory(title='プロジェクトを開く（*.fproj フォルダを選択）')
    if not folder:
        return
    try:
        self.project.load_project(folder)
        self.project.dirty = False
        if hasattr(self, 'grid_view'):
            self.grid_view.refresh()
        if hasattr(self, '_update_status'):
            self._update_status()
        messagebox.showinfo('読込完了', f'プロジェクトを読み込みました:\n{folder}')
    except OSError as e:
        messagebox.showerror('読込エラー', f'プロジェクト読込に失敗しました:\n{e}')
    except Exception as e:
        messagebox.showerror('読込エラー', f'予期しないエラー:\n{e}')


# --- .fprojz へ単一ファイル書出し ---
def _export_project_singlefile_impl(self: FontEditorApp, dest: Optional[str] = None) -> bool:
    """単一ファイル書出し (2025-10-11: 型ヒント追加、安全な一時ファイル管理)"""
    try:
        if hasattr(self, '_stop_bg_loading'):
            self._stop_bg_loading()
    except Exception:
        pass
    try:
        if hasattr(self, '_commit_all_open_editors'):
            self._commit_all_open_editors()
    except Exception:
        pass

    if not dest:
        dest = filedialog.asksaveasfilename(
            title='単一ファイルに書き出し',
            defaultextension='.fprojz',
            filetypes=[('Font Project (Single File)', '*.fprojz')]
        )
    if not dest:
        return False
    if not dest.endswith('.fprojz'):
        dest += '.fprojz'

    tmpdir = tempfile.mkdtemp(prefix='fproj_tmp_')
    try:
        with self.project._lock:  # (2025-10-11: スレッドセーフ化)
            orig_glyphs = self.project.glyphs
            snapshot = dict(orig_glyphs)
            self.project.glyphs = snapshot

        temp_folder = os.path.join(tmpdir, 'project.fproj')
        
        try:
            self.project.save_project(temp_folder)

            with zipfile.ZipFile(dest, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(temp_folder):
                    for name in files:
                        abspath = os.path.join(root, name)
                        arcname = os.path.relpath(abspath, start=tmpdir)
                        zf.write(abspath, arcname)

            self.project.dirty = False
            messagebox.showinfo('書き出し完了', f'単一ファイルへ書き出しました:\n{dest}')
            return True
        except OSError as e:
            messagebox.showerror('書き出しエラー', f'単一ファイル書き出しに失敗しました:\n{e}')
            return False
        except Exception as e:
            messagebox.showerror('書き出しエラー', f'予期しないエラー:\n{e}')
            return False
        finally:
            with self.project._lock:
                self.project.glyphs = orig_glyphs
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# --- .fprojz 読込 ---
def _open_project_singlefile_impl(self: FontEditorApp) -> None:
    """単一ファイルプロジェクト読込"""
    if not self._confirm_unsaved_changes():
        return
    src = filedialog.askopenfilename(
        title='単一ファイルのプロジェクトを開く',
        filetypes=[('Font Project (Single File)', '*.fprojz'), ('All Files', '*.*')]
    )
    if not src:
        return
    tmpdir = tempfile.mkdtemp(prefix='fproj_open_')
    try:
        with zipfile.ZipFile(src, 'r') as zf:
            zf.extractall(tmpdir)
        target = None
        for entry in os.listdir(tmpdir):
            p = os.path.join(tmpdir, entry)
            if os.path.isdir(p) and entry.endswith('.fproj'):
                target = p
                break
        if not target:
            raise RuntimeError('アーカイブ内に .fproj フォルダが見つかりません')

        self.project.load_project(target)
        self.project.dirty = False
        if hasattr(self, 'grid_view'):
            self.grid_view.refresh()
        if hasattr(self, '_update_status'):
            self._update_status()
        messagebox.showinfo('読込完了', f'単一ファイルのプロジェクトを読み込みました:\n{src}')
    except OSError as e:
        messagebox.showerror('読込エラー', f'単一ファイル読込に失敗しました:\n{e}')
    except Exception as e:
        messagebox.showerror('読込エラー', f'予期しないエラー:\n{e}')
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)



# === [INTEGRATED] Parts editor openers (bound to FontEditorApp) ===
def _open_parts_editor_impl(self) -> None:
    if not getattr(self.project, 'font_path', None):
        messagebox.showwarning('警告', 'まずフォントを読み込んでください')
        return
    top = tk.Toplevel(self)
    top.title('偏旁エディタ')
    try:
        gui = IntegratedPartsExtractorGUI(top)
    except Exception as e:
        messagebox.showerror('起動エラー', f'偏旁エディタ起動に失敗しました:\n{e}')
        try:
            top.destroy()
        except Exception:
            pass
        return
    font_path = self.project.font_path
    out_dir = _get_parts_output_dir_impl(self)
    os.makedirs(out_dir, exist_ok=True)
    # pass context to GUI if supported
    if hasattr(gui, 'set_font_path'):
        gui.set_font_path(font_path)
    if hasattr(gui, 'set_output_dir'):
        gui.set_output_dir(out_dir)
    if hasattr(gui, 'set_copy_callback'):
        gui.set_copy_callback(lambda img, s, off: self._insert_part_to_active_editor(img, s, off))

    def _import_back() -> None:
        try:
            _import_parts_from_folder_impl(self, out_dir)
            _open_parts_palette_impl(self)
        except Exception as e:
            messagebox.showerror('取り込みエラー', f'偏旁の取り込みに失敗しました:\n{e}')

    tk.Button(top, text='本体へ取り込み', command=_import_back).pack(side='bottom', pady=6)

def _open_parts_palette_impl(self) -> None:
    try:
        if getattr(self, 'parts_palette', None) and self.parts_palette.winfo_exists():
            self.parts_palette.lift()
            return
    except Exception:
        pass
    if not getattr(self.project, 'parts', None):
        try:
            if messagebox.askyesno('偏旁エディタ', '偏旁パーツがありません。今すぐ抽出ツールを開きますか？'):
                _open_parts_editor_impl(self)
        except Exception as e:
            messagebox.showerror('起動エラー', f'偏旁エディタ起動に失敗しました:\n{e}')
        return
    self.parts_palette = PartsPalette(self, self.project, self._insert_part_to_active_editor)

# helper: resolve parts output dir inside current project
def _get_parts_output_dir_impl(self) -> str:
    base = None
    try:
        base = os.path.dirname(self.project.font_path) if self.project.font_path else os.getcwd()
    except Exception:
        base = os.getcwd()
    proj_dir = getattr(self.project, '_project_dir', None)
    if proj_dir and os.path.isdir(proj_dir):
        base = proj_dir
    out_dir = os.path.join(base, 'assets', 'parts')
    return out_dir

# helper: import parts (PNG + catalog) into project.parts
def _import_parts_from_folder_impl(self, folder: str) -> None:
    if not os.path.isdir(folder):
        raise FileNotFoundError(folder)
    catalog_path = os.path.join(folder, 'parts_catalog.json')
    catalog = {}
    if os.path.exists(catalog_path):
        import json
        with open(catalog_path, 'r', encoding='utf-8') as f:
            nested_catalog = json.load(f)
            # ネストされたカタログをフラット化
            for category, parts_in_cat in nested_catalog.items():
                if isinstance(parts_in_cat, dict):
                    for part_name, part_meta in parts_in_cat.items():
                        # ファイル名からキーを生成（category_partname_char形式）
                        if isinstance(part_meta, dict):
                            file_name = part_meta.get("file", "")
                            if file_name:
                                key = os.path.splitext(file_name)[0]
                                catalog[key] = part_meta
                                # カテゴリ情報を確実に含める
                                if "category" not in catalog[key]:
                                    catalog[key]["category"] = category
    parts = {}
    for name in os.listdir(folder):
        if not name.lower().endswith('.png'):
            continue
        path = os.path.join(folder, name)
        try:
            img = Image.open(path).convert('RGBA')
        except Exception:
            continue
        key = os.path.splitext(name)[0]
        meta = catalog.get(key, {})
        parts[key] = {'image': img, 'meta': meta, 'path': path}
    self.project.parts = parts
    # mark project dirty so save will include parts via our save hook
    try:
        self.project.dirty = True
    except Exception:
        pass

# --- FontEditorApp へバインド ---
def _wrap(f: Callable) -> Callable:
    """関数ラッパー"""
    f.__wrapped__ = f  # type: ignore
    return f

FontEditorApp._save_project_dialog = _wrap(_save_project_dialog_impl)  # type: ignore
FontEditorApp._open_project_dialog = _wrap(_open_project_dialog_impl)  # type: ignore
FontEditorApp._export_project_singlefile = _wrap(_export_project_singlefile_impl)  # type: ignore
FontEditorApp._open_project_singlefile = _wrap(_open_project_singlefile_impl)  # type: ignore


# =========================
# GlyphEditor 互換パッチ群
# =========================
# UI/レイアウトは一切変更せず、足りないAPIだけ後付け
#  - ⌘S/Ctrl+Sで「閉じずにプロジェクトへ反映→保存ダイアログ」
#  - _on_copy/_on_cut/_on_paste/_draw_rect/_draw_ellipse/_start_selection を補完

def _ge_commit(self: GlyphEditor) -> None:
    """エディタ内容をプロジェクトへ反映（BLOCK9互換）"""
    self.project.glyphs[self.char_code] = GlyphData(self.char_code, self.edit_bitmap.copy(), is_edited=True)
    self.project.dirty = True
    if callable(getattr(self, 'on_commit', None)):
        self.on_commit(self.char_code)  # type: ignore

def _ge_save_from_editor(self: GlyphEditor, event: Optional[tk.Event] = None) -> None:
    """⌘S/Ctrl+S: 保存（BLOCK9互換）"""
    if not hasattr(self, 'commit_to_project_without_close'):
        self.commit_to_project_without_close = MethodType(_ge_commit, self)  # type: ignore
    self.commit_to_project_without_close()  # type: ignore
    if hasattr(self.master, '_save_project_dialog'):
        self.master._save_project_dialog()  # type: ignore

def _ge_on_copy(self: GlyphEditor) -> None:
    """コピー（BLOCK9互換）"""
    if hasattr(self, '_copy'):
        self._copy()

def _ge_on_cut(self: GlyphEditor) -> None:
    """切り取り（BLOCK9互換）"""
    if hasattr(self, '_cut'):
        self._cut()

def _ge_on_paste(self: GlyphEditor) -> None:
    """貼り付け（BLOCK9互換）"""
    if hasattr(self, '_paste'):
        self._paste()

def _ge_start_selection(self: GlyphEditor, x0: int, y0: int, x1: int, y1: int) -> None:
    """選択開始（BLOCK9互換）"""
    try:
        x0 = max(0, min(int(x0), self.edit_bitmap.width - 1))
        y0 = max(0, min(int(y0), self.edit_bitmap.height - 1))
        x1 = max(0, min(int(x1), self.edit_bitmap.width))
        y1 = max(0, min(int(y1), self.edit_bitmap.height))
        self.selection_start = (min(x0, x1), min(y0, y1))
        self.selection_end = (max(x0, x1), max(y0, y1))
        self.selected_image = self.edit_bitmap.crop((*self.selection_start, *self.selection_end)).copy()
        if hasattr(self, '_update_preview'):
            self._update_preview()
    except Exception:
        pass

def _ge_draw_rect(self: GlyphEditor, x0: int, y0: int, x1: int, y1: int, width: int = 1) -> None:
    """矩形描画（BLOCK9互換）"""
    dr = ImageDraw.Draw(self.edit_bitmap)
    dr.rectangle((x0, y0, x1, y1), outline=0, width=max(1, int(width)))
    if hasattr(self, '_update_preview'):
        self._update_preview()

def _ge_draw_ellipse(self: GlyphEditor, x0: int, y0: int, x1: int, y1: int, width: int = 1) -> None:
    """楕円描画（BLOCK9互換）"""
    dr = ImageDraw.Draw(self.edit_bitmap)
    dr.ellipse((x0, y0, x1, y1), outline=0, width=max(1, int(width)))
    if hasattr(self, '_update_preview'):
        self._update_preview()

# __init__ をラップしてショートカット/メソッドを付与
try:
    _GE_init_orig = GlyphEditor.__init__
    def _GE_init_patched(self: GlyphEditor, *a: Any, **k: Any) -> None:
        _GE_init_orig(self, *a, **k)  # type: ignore
        if not hasattr(self, 'commit_to_project_without_close'):
            self.commit_to_project_without_close = MethodType(_ge_commit, self)  # type: ignore
        if not hasattr(self, '_save_from_editor'):
            self._save_from_editor = MethodType(_ge_save_from_editor, self)  # type: ignore
        for name, func in (
            ('_on_copy', _ge_on_copy),
            ('_on_cut', _ge_on_cut),
            ('_on_paste', _ge_on_paste),
            ('_start_selection', _ge_start_selection),
            ('_draw_rect', _ge_draw_rect),
            ('_draw_ellipse', _ge_draw_ellipse),
        ):
            if not hasattr(self, name):
                setattr(self, name, MethodType(func, self))  # type: ignore
        try:
            self.unbind_all('<Command-s>')
            self.unbind_all('<Control-s>')
        except Exception:
            pass
        try:
            self.bind_all('<Command-s>', self._save_from_editor)  # type: ignore
            self.bind_all('<Control-s>', self._save_from_editor)  # type: ignore
        except Exception:
            pass
    GlyphEditor.__init__ = _GE_init_patched  # type: ignore
except Exception:
    pass

# ===== [本体 BLOCK6-END] =====













# ===== 貼り付けプレビューダイアログ (2025-11-06) =====

class PastePreviewDialog(tk.Toplevel):
    """貼り付けプレビューダイアログ - 位置調整可能"""

    def __init__(self, parent, canvas_image: Image.Image, paste_image: Image.Image):
        super().__init__(parent)
        self.title("貼り付けプレビュー")
        self.geometry("650x700")
        self.transient(parent)
        self.grab_set()

        self.canvas_image = canvas_image.copy()
        self.paste_image = paste_image
        self.paste_x = (Config.CANVAS_SIZE - paste_image.size[0]) // 2
        self.paste_y = (Config.CANVAS_SIZE - paste_image.size[1]) // 2
        self.result = None

        self.drag_start = None

        self._setup_ui()
        self._update_preview()

        # キーバインド
        self.bind('<Escape>', lambda e: self._on_cancel())
        self.bind('<Return>', lambda e: self._on_ok())

    def _setup_ui(self):
        """UI構築"""
        # 説明
        tk.Label(
            self,
            text="ドラッグで位置を調整してください\nEnterで確定 / Escでキャンセル",
            font=("", 10)
        ).pack(pady=5)

        # プレビューキャンバス
        canvas_frame = tk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.preview_canvas = tk.Canvas(canvas_frame, width=600, height=600, bg='white')
        self.preview_canvas.pack()

        # マウスイベント
        self.preview_canvas.bind('<Button-1>', self._on_mouse_down)
        self.preview_canvas.bind('<B1-Motion>', self._on_mouse_drag)
        self.preview_canvas.bind('<ButtonRelease-1>', self._on_mouse_up)

        # ボタン
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(button_frame, text="OK (Enter)", command=self._on_ok, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="キャンセル (Esc)", command=self._on_cancel, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="中央に配置", command=self._center_paste).pack(side=tk.LEFT, padx=5)

    def _update_preview(self):
        """プレビュー更新"""
        try:
            # 合成画像を作成
            composite = self.canvas_image.copy()

            # 貼り付け画像を半透明で合成
            from PIL import ImageChops
            paste_region = composite.crop((
                self.paste_x,
                self.paste_y,
                self.paste_x + self.paste_image.size[0],
                self.paste_y + self.paste_image.size[1]
            ))

            # 暗い方を採用（透過合成）
            blended = ImageChops.darker(paste_region, self.paste_image)

            # 半透明効果（簡易版）
            from PIL import ImageEnhance
            blended = ImageEnhance.Brightness(blended).enhance(0.7)

            composite.paste(blended, (self.paste_x, self.paste_y))

            # 600x600に縮小表示
            display_size = 600
            scale = display_size / Config.CANVAS_SIZE
            display_w = display_h = display_size
            display_image = composite.resize((display_w, display_h), Image.Resampling.LANCZOS)

            # Tkinter用に変換
            photo = ImageTk.PhotoImage(display_image)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(300, 300, image=photo)
            self.preview_canvas.image = photo

        except Exception as e:
            print(f"プレビュー更新エラー: {e}")

    def _on_mouse_down(self, event):
        """マウスダウン"""
        self.drag_start = (event.x, event.y)

    def _on_mouse_drag(self, event):
        """マウスドラッグ"""
        if self.drag_start:
            # キャンバス座標からグリフ座標に変換
            scale = Config.CANVAS_SIZE / 600
            dx = int((event.x - self.drag_start[0]) * scale)
            dy = int((event.y - self.drag_start[1]) * scale)

            self.paste_x += dx
            self.paste_y += dy

            # 範囲制限
            self.paste_x = max(0, min(Config.CANVAS_SIZE - self.paste_image.size[0], self.paste_x))
            self.paste_y = max(0, min(Config.CANVAS_SIZE - self.paste_image.size[1], self.paste_y))

            self.drag_start = (event.x, event.y)
            self._update_preview()

    def _on_mouse_up(self, event):
        """マウスアップ"""
        self.drag_start = None

    def _center_paste(self):
        """中央に配置"""
        self.paste_x = (Config.CANVAS_SIZE - self.paste_image.size[0]) // 2
        self.paste_y = (Config.CANVAS_SIZE - self.paste_image.size[1]) // 2
        self._update_preview()

    def _on_ok(self):
        """OK"""
        self.result = (self.paste_x, self.paste_y)
        self.destroy()

    def _on_cancel(self):
        """キャンセル"""
        self.result = None
        self.destroy()


# ===== 偏旁変形ダイアログ (2025-11-06) =====

class PartTransformDialog(tk.Toplevel):
    """偏旁変形ダイアログ - スケール＆比率調整"""

    def __init__(self, parent, part_image: Image.Image, part_name: str):
        super().__init__(parent)
        self.title(f"偏旁変形 - {part_name}")
        self.geometry("600x700")
        self.transient(parent)
        self.grab_set()

        self.original_image = part_image
        self.part_name = part_name
        self.result = None
        self.current_transformed = part_image.copy()  # [FIX] 2025-11-06: 初期値を設定

        # 変形パラメータ
        self.scale_x = tk.DoubleVar(value=1.0)
        self.scale_y = tk.DoubleVar(value=1.0)
        self.uniform_scale = tk.DoubleVar(value=1.0)

        self._setup_ui()
        self._update_preview()

    def _setup_ui(self):
        """UI構築"""
        # プレビューエリア
        preview_frame = tk.Frame(self)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(preview_frame, text="プレビュー", font=("", 12, "bold")).pack()

        self.preview_canvas = tk.Canvas(preview_frame, width=400, height=400, bg='white')
        self.preview_canvas.pack()

        # コントロールパネル
        control_frame = tk.LabelFrame(self, text="変形設定", padx=10, pady=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # 統一スケール
        tk.Label(control_frame, text="統一スケール (25% - 200%):").grid(row=0, column=0, sticky='w', pady=5)
        scale_slider = tk.Scale(
            control_frame,
            from_=0.25, to=2.0, resolution=0.05,
            orient=tk.HORIZONTAL, length=300,
            variable=self.uniform_scale,
            command=lambda v: self._on_uniform_scale_change()
        )
        scale_slider.grid(row=0, column=1, columnspan=2, pady=5)

        # 幅スケール
        tk.Label(control_frame, text="幅 (25% - 200%):").grid(row=1, column=0, sticky='w', pady=5)
        width_slider = tk.Scale(
            control_frame,
            from_=0.25, to=2.0, resolution=0.05,
            orient=tk.HORIZONTAL, length=300,
            variable=self.scale_x,
            command=lambda v: self._update_preview()
        )
        width_slider.grid(row=1, column=1, columnspan=2, pady=5)

        # 高さスケール
        tk.Label(control_frame, text="高さ (25% - 200%):").grid(row=2, column=0, sticky='w', pady=5)
        height_slider = tk.Scale(
            control_frame,
            from_=0.25, to=2.0, resolution=0.05,
            orient=tk.HORIZONTAL, length=300,
            variable=self.scale_y,
            command=lambda v: self._update_preview()
        )
        height_slider.grid(row=2, column=1, columnspan=2, pady=5)

        # リセットボタン
        tk.Button(control_frame, text="リセット", command=self._reset).grid(row=3, column=0, pady=10)

        # ボタンエリア
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(button_frame, text="OK", command=self._on_ok, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="キャンセル", command=self._on_cancel, width=15).pack(side=tk.LEFT, padx=5)

    def _on_uniform_scale_change(self):
        """統一スケール変更時"""
        scale = self.uniform_scale.get()
        self.scale_x.set(scale)
        self.scale_y.set(scale)
        self._update_preview()

    def _update_preview(self):
        """プレビュー更新"""
        try:
            # スケールを適用
            scale_x = self.scale_x.get()
            scale_y = self.scale_y.get()

            orig_w, orig_h = self.original_image.size
            new_w = int(orig_w * scale_x)
            new_h = int(orig_h * scale_y)

            if new_w <= 0 or new_h <= 0:
                return

            # リサイズ
            scaled_image = self.original_image.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # プレビュー用に縮小（400x400に収める）
            preview_size = min(scaled_image.size)
            if preview_size > 400:
                ratio = 400 / preview_size
                display_w = int(scaled_image.size[0] * ratio)
                display_h = int(scaled_image.size[1] * ratio)
                display_image = scaled_image.resize((display_w, display_h), Image.Resampling.LANCZOS)
            else:
                display_image = scaled_image

            # Tkinter用に変換
            photo = ImageTk.PhotoImage(display_image)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(200, 200, image=photo)
            self.preview_canvas.image = photo  # 参照を保持

            # 現在の変形画像を保存
            self.current_transformed = scaled_image

        except Exception as e:
            print(f"プレビュー更新エラー: {e}")

    def _reset(self):
        """リセット"""
        self.uniform_scale.set(1.0)
        self.scale_x.set(1.0)
        self.scale_y.set(1.0)
        self._update_preview()

    def _on_ok(self):
        """OK"""
        self.result = self.current_transformed
        self.destroy()

    def _on_cancel(self):
        """キャンセル"""
        self.result = None
        self.destroy()


# ===== [本体 BLOCK11-BEGIN] グリフフィルタダイアログ (2025-10-11: 型ヒント追加) =====

class GlyphFilterDialog(tk.Toplevel):
    """グリフフィルタ選択ダイアログ"""
    
    def __init__(self, parent: tk.Widget, project: FontProject, current_filter: str) -> None:
        super().__init__(parent)
        self.project: FontProject = project
        self.result: str = current_filter
        
        self.title('グリフフィルタ')
        self.geometry('400x350')
        self.transient(parent)
        self.grab_set()
        
        # 説明ラベル
        tk.Label(
            self,
            text='表示するグリフの種類を選択してください',
            font=('Arial', 12, 'bold'),
            pady=10
        ).pack()
        
        # フィルタオプション
        self.filter_var = tk.StringVar(value=current_filter)
        
        filter_options = [
            ('all', 'すべて表示'),
            ('edited', '編集済みのみ'),
            ('unedited', '未編集のみ'),
            ('defined', '定義済みのみ'),
            ('empty', '空白のみ')
        ]
        
        for value, label in filter_options:
            tk.Radiobutton(
                self,
                text=label,
                variable=self.filter_var,
                value=value,
                font=('Arial', 11),
                anchor='w'
            ).pack(fill='x', padx=20, pady=5)
        
        # 統計情報表示 (2025-10-08)
        stats_frame = tk.Frame(self, relief='sunken', borderwidth=1)
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            stats_frame,
            text='現在の範囲の統計:',
            font=('Arial', 10, 'bold')
        ).pack(pady=5)
        
        # 統計計算 (2025-10-11: スレッドセーフ化)
        char_codes = project.get_char_codes()
        total = len(char_codes)
        
        with project._lock:
            edited = sum(1 for code in char_codes
                        if code in project.glyphs and not project.glyphs[code].is_empty and project.glyphs[code].is_edited)
            unedited = sum(1 for code in char_codes
                          if code in project.glyphs and not project.glyphs[code].is_empty and not project.glyphs[code].is_edited)
            empty = sum(1 for code in char_codes
                       if code not in project.glyphs or project.glyphs[code].is_empty)
        
        stats_text = f'全体: {total}  |  編集済み: {edited}  |  未編集: {unedited}  |  空白: {empty}'
        
        tk.Label(
            stats_frame,
            text=stats_text,
            font=('Arial', 9)
        ).pack(pady=5)
        
        # ボタンフレーム
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text='適用',
            command=self._apply,
            width=10
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text='キャンセル',
            command=self.destroy,
            width=10
        ).pack(side='left', padx=5)
        
        # Enterキーで適用
        self.bind('<Return>', lambda e: self._apply())
    
    def _apply(self) -> None:
        """適用ボタン押下"""
        self.result = self.filter_var.get()
        self.destroy()

# ===== [本体 BLOCK11-END] =====











# ===== [本体 BLOCK12-BEGIN] テキストプレビューダイアログ (2025-10-11: 型ヒント追加、PhotoImage参照保持改善) =====

class TextPreviewDialog(tk.Toplevel):
    """テキストプレビューダイアログ"""
    
    def __init__(self, parent: tk.Widget, project: FontProject) -> None:
        super().__init__(parent)
        self.project: FontProject = project
        
        self.title('テキストプレビュー')
        self.geometry('800x600')
        self.transient(parent)
        
        # PhotoImage参照保持 (2025-10-11: GC対策)
        self.preview_photo: Optional[ImageTk.PhotoImage] = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """UI構築"""
        # ツールバー
        toolbar = tk.Frame(self)
        toolbar.pack(side='top', fill='x', padx=5, pady=5)
        
        tk.Label(toolbar, text='サイズ:').pack(side='left', padx=5)
        
        self.size_var = tk.IntVar(value=48)
        size_scale = tk.Scale(
            toolbar,
            from_=12,
            to=200,
            orient='horizontal',
            variable=self.size_var,
            command=lambda v: self._update_preview()
        )
        size_scale.pack(side='left', padx=5)
        
        tk.Button(
            toolbar,
            text='PNG保存',
            command=self._save_png
        ).pack(side='left', padx=5)
        
        # 入力エリア
        input_frame = tk.Frame(self)
        input_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(input_frame, text='プレビューテキスト:').pack(anchor='w')
        
        self.text_entry = tk.Entry(input_frame, font=('Arial', 12))
        self.text_entry.pack(fill='x', pady=5)
        self.text_entry.insert(0, 'ABCDEFGあいうえお')
        self.text_entry.bind('<KeyRelease>', lambda e: self._update_preview())
        
        # プレビューキャンバス
        preview_frame = tk.Frame(self, relief='sunken', borderwidth=1)
        preview_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # スクロール対応
        self.preview_canvas = tk.Canvas(preview_frame, bg='white')
        v_scroll = ttk.Scrollbar(preview_frame, orient='vertical', command=self.preview_canvas.yview)
        h_scroll = ttk.Scrollbar(preview_frame, orient='horizontal', command=self.preview_canvas.xview)
        
        self.preview_canvas.configure(
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set
        )
        
        self.preview_canvas.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        # 初期プレビュー
        self._update_preview()
    
    def _update_preview(self) -> None:
        """プレビュー更新 (2025-10-11: スレッドセーフ化、PhotoImage参照保持改善)"""
        text = self.text_entry.get()
        size = self.size_var.get()
        
        if not text:
            return
        
        # 各文字のビットマップを取得して並べる
        char_images: List[Image.Image] = []
        
        with self.project._lock:  # (2025-10-11: スレッドセーフ化)
            for char in text:
                try:
                    code = ord(char)
                    glyph = self.project.glyphs.get(code)
                    
                    if glyph and not glyph.is_empty and glyph.bitmap:
                        # グリフをリサイズ
                        resized = glyph.bitmap.resize((size, size), Image.Resampling.LANCZOS)
                        char_images.append(resized)
                    else:
                        # 空白グリフは空白スペース
                        blank = Image.new('L', (size, size), 255)
                        char_images.append(blank)
                        
                except (ValueError, KeyError):
                    # エラー時は空白
                    blank = Image.new('L', (size, size), 255)
                    char_images.append(blank)
        
        if not char_images:
            return
        
        # 横に並べて1枚の画像を作成
        total_width = sum(img.width for img in char_images)
        max_height = max(img.height for img in char_images)
        
        combined = Image.new('L', (total_width, max_height), 255)
        
        x_offset = 0
        for img in char_images:
            combined.paste(img, (x_offset, 0))
            x_offset += img.width
        
        # キャンバスに表示 (2025-10-11: PhotoImage参照保持改善)
        self.preview_photo = ImageTk.PhotoImage(combined)
        self.preview_canvas.delete('all')
        self.preview_canvas.create_image(0, 0, anchor='nw', image=self.preview_photo)
        
        # スクロール領域更新
        self.preview_canvas.configure(scrollregion=(0, 0, total_width, max_height))
    
    def _save_png(self) -> None:
        """プレビュー画像をPNG保存 (2025-10-11: スレッドセーフ化)"""
        text = self.text_entry.get()
        size = self.size_var.get()
        
        if not text:
            messagebox.showwarning('警告', 'テキストを入力してください')
            return
        
        path = filedialog.asksaveasfilename(
            title='プレビュー画像を保存',
            defaultextension='.png',
            filetypes=[('PNG Image', '*.png'), ('All Files', '*.*')]
        )
        
        if not path:
            return
        
        # 画像を再生成して保存
        char_images: List[Image.Image] = []
        
        with self.project._lock:  # (2025-10-11: スレッドセーフ化)
            for char in text:
                try:
                    code = ord(char)
                    glyph = self.project.glyphs.get(code)
                    
                    if glyph and not glyph.is_empty and glyph.bitmap:
                        resized = glyph.bitmap.resize((size, size), Image.Resampling.LANCZOS)
                        char_images.append(resized)
                    else:
                        blank = Image.new('L', (size, size), 255)
                        char_images.append(blank)
                except (ValueError, KeyError):
                    blank = Image.new('L', (size, size), 255)
                    char_images.append(blank)
        
        if not char_images:
            messagebox.showwarning('警告', '画像を生成できませんでした')
            return
        
        total_width = sum(img.width for img in char_images)
        max_height = max(img.height for img in char_images)
        
        combined = Image.new('L', (total_width, max_height), 255)
        
        x_offset = 0
        for img in char_images:
            combined.paste(img, (x_offset, 0))
            x_offset += img.width
        
        # 透過PNG変換
        rgba_img = Image.new('RGBA', combined.size, (255, 255, 255, 0))
        pixels_gray = combined.load()
        pixels_rgba = rgba_img.load()
        
        for y in range(combined.size[1]):
            for x in range(combined.size[0]):
                gray_value = pixels_gray[x, y]
                alpha = 255 - gray_value
                pixels_rgba[x, y] = (0, 0, 0, alpha)
        
        try:
            rgba_img.save(path, 'PNG')
            messagebox.showinfo('保存完了', f'保存しました:\n{path}')
        except OSError as e:
            messagebox.showerror('保存エラー', f'保存に失敗しました:\n{e}')

# ===== [本体 BLOCK12-END] =====











# ################################################################################
# ■■■ オプション機能 - 偏旁（部首）ツール ■■■
# ################################################################################











# ===== [オプション OPTION1-BEGIN] 偏旁エディタ - 状態管理とヘルパー関数 =====

def _collect_editor_state(gui) -> Dict[str, Any]:
    cand = ["output_dir","font_path","erase_radius","smooth_sigma","threshold","zoom","last_selected_key","current_tool","ui_theme","preview_scale"]
    st = {}
    for k in cand:
        if hasattr(gui, k):
            try: st[k] = getattr(gui, k)
            except Exception: pass
    if hasattr(gui, "get_output_dir"):
        try: st["output_dir"] = gui.get_output_dir()
        except Exception: pass
    return st

def _apply_editor_state(gui, st: Dict[str, Any]):
    if not isinstance(st, dict): return
    if "output_dir" in st and hasattr(gui, "set_output_dir"):
        try: gui.set_output_dir(st["output_dir"])
        except Exception: pass
    if "font_path" in st and hasattr(gui, "set_font_path"):
        try: gui.set_font_path(st["font_path"])
        except Exception: pass
    for k, v in st.items():
        if k in ("output_dir","font_path"): continue
        if hasattr(gui, k):
            try: setattr(gui, k, v)
            except Exception: pass

def _ensure_editor_slots(self):
    if not hasattr(self, "_parts_editor_top"): self._parts_editor_top = None
    if not hasattr(self, "_parts_editor_gui"): self._parts_editor_gui = None
    if not hasattr(self, "_editor_state"): self._editor_state = {}

def _save_editor_state_from_gui(self):
    _ensure_editor_slots(self)
    gui = getattr(self, "_parts_editor_gui", None)
    if gui is None: return
    try: self._editor_state = _collect_editor_state(gui)
    except Exception: self._editor_state = {}

def _apply_editor_state_to_gui(self, gui):
    _ensure_editor_slots(self)
    st = getattr(self, "_editor_state", {}) or {}
    try: _apply_editor_state(gui, st)
    except Exception: pass

def _import_parts_from_folder(self, folder: str) -> int:
    if not os.path.isdir(folder):
        raise FileNotFoundError(folder)

    # カタログ読み込み
    catalog = {}
    catalog_path = os.path.join(folder, "parts_catalog.json")
    if os.path.exists(catalog_path):
        try:
            with open(catalog_path, 'r', encoding='utf-8') as f:
                nested_catalog = json.load(f)
                # ネストされたカタログをフラット化
                for category, parts_in_cat in nested_catalog.items():
                    if isinstance(parts_in_cat, dict):
                        for part_name, part_meta in parts_in_cat.items():
                            if isinstance(part_meta, dict):
                                file_name = part_meta.get("file", "")
                                if file_name:
                                    key = os.path.splitext(file_name)[0]
                                    catalog[key] = part_meta
                                    # カテゴリ情報を確実に含める
                                    if "category" not in catalog[key]:
                                        catalog[key]["category"] = category
        except Exception:
            pass

    picked: Dict[str, Dict] = {}
    for root, _, files in os.walk(folder):
        for name in files:
            if not name.lower().endswith(".png"): continue
            path = os.path.join(root, name)
            key  = os.path.splitext(os.path.relpath(path, folder))[0]
            try: img = Image.open(path).convert("RGBA")
            except Exception: continue
            # カタログからメタデータを取得
            meta = catalog.get(key, {})
            picked[key] = {"image": img, "path": path, "w": img.width, "h": img.height, "meta": meta}
    if not hasattr(self.project, "parts") or self.project.parts is None:
        self.project.parts = {}
    self.project.parts.update(picked)
    self.project.parts_order = list(self.project.parts.keys())
    try: self.project.dirty = True
    except Exception: pass
    return len(picked)

class _InternalPartsPalette(tk.Toplevel):
    def __init__(self, master, project, insert_cb):
        super().__init__(master); self.title("偏旁パレット")
        self.project = project; self.insert_cb = insert_cb
        self.geometry("480x600")

        # カテゴリ名のマッピング
        self.category_names = {
            "hen": "偏（へん）",
            "tsukuri": "旁（つくり）",
            "kanmuri": "冠（かんむり）",
            "ashi": "脚（あし）",
            "nyou": "繞（にょう）",
            "tare": "垂（たれ）",
            "kamae": "構（かまえ）",
            "other": "その他"
        }

        # タブUIの作成
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=4, pady=4)

        # 各カテゴリ用のフレームとキャンバスを保持
        self.tab_frames = {}
        self.tab_canvases = {}
        self.tab_inner_frames = {}

        self._tkimgs = {}
        self.refresh()

    def refresh(self):
        # 既存のタブをクリア
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        self._tkimgs.clear()
        self.tab_frames.clear()
        self.tab_canvases.clear()
        self.tab_inner_frames.clear()

        parts = getattr(self.project, "parts", None) or {}
        order = getattr(self.project, "parts_order", None) or list(parts.keys())

        if not order:
            empty_frame = tk.Frame(self.notebook)
            self.notebook.add(empty_frame, text="空")
            tk.Label(empty_frame, text="（偏旁が読み込まれていません）").pack(pady=12)
            return

        # カテゴリごとに偏旁を分類
        categorized = {cat: [] for cat in self.category_names.keys()}

        for key in order:
            data = parts.get(key) or {}
            img = data.get("image")
            if img is None: continue

            # メタデータからカテゴリを取得
            meta = data.get("meta", {})
            category = meta.get("category", "other")

            # カテゴリが存在しない場合は「その他」へ
            if category not in categorized:
                category = "other"

            categorized[category].append((key, img, meta))

        # 各カテゴリのタブを作成
        for cat_id, cat_name in self.category_names.items():
            items = categorized.get(cat_id, [])
            if not items:
                continue  # 空のカテゴリはスキップ

            # タブフレーム作成
            tab_frame = tk.Frame(self.notebook)
            self.tab_frames[cat_id] = tab_frame
            self.notebook.add(tab_frame, text=f"{cat_name} ({len(items)})")

            # スクロール可能なキャンバス作成
            canvas = tk.Canvas(tab_frame, highlightthickness=0)
            scrollbar = tk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
            inner = tk.Frame(canvas)

            inner.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
            canvas.create_window((0, 0), window=inner, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            self.tab_canvases[cat_id] = canvas
            self.tab_inner_frames[cat_id] = inner

            # 偏旁を配置
            for i, (key, img, meta) in enumerate(items):
                scale = max(img.width, img.height) or 1
                tw = max(1, int(img.width * (120.0 / scale)))
                th = max(1, int(img.height * (120.0 / scale)))
                tkimg = ImageTk.PhotoImage(img.resize((tw, th)))
                self._tkimgs[key] = tkimg

                row = tk.Frame(inner, padx=4, pady=4, relief="ridge", borderwidth=1)
                row.grid(row=i, column=0, sticky="ew", padx=4, pady=2)

                # 画像
                tk.Label(row, image=tkimg).grid(row=0, column=0, rowspan=2, padx=6)

                # 名前とメタ情報
                name_label = tk.Label(row, text=key, font=("", 10, "bold"))
                name_label.grid(row=0, column=1, sticky="w")

                # split情報があれば表示
                split_info = meta.get("split", "")
                if split_info:
                    split_text = {"left": "左", "right": "右", "top": "上", "bottom": "下",
                                 "left_bottom": "左下", "top_left": "左上", "frame": "囲み"}.get(split_info, split_info)
                    info_label = tk.Label(row, text=f"配置: {split_text}", font=("", 8), fg="gray")
                    info_label.grid(row=1, column=1, sticky="w")

                # 貼付ボタン
                def _do_insert(k=key, im=img):
                    return lambda: self.insert_cb(im, k, (0, 0))
                btn = tk.Button(row, text="貼付", command=_do_insert())
                btn.grid(row=0, column=2, rowspan=2, padx=6)

def _open_parts_palette_nospawn(self):
    pal_cls = globals().get("PartsPalette") or _InternalPartsPalette
    try:
        if getattr(self, "parts_palette", None) and self.parts_palette.winfo_exists():
            if hasattr(self.parts_palette, "refresh"):
                try: self.parts_palette.refresh()
                except Exception: pass
            self.parts_palette.lift(); return
        self.parts_palette = pal_cls(self, self.project, getattr(self, "_insert_part_to_active_editor", lambda *a, **k: None))
        if hasattr(self.parts_palette, "refresh"):
            try: self.parts_palette.refresh()
            except Exception: pass
        self.parts_palette.lift()
    except Exception as e:
        messagebox.showinfo("情報", f"パレットを開けませんでした。\\n{e}")

def _fe_open_parts_editor_safe(self) -> None:
    _ensure_editor_slots(self)
    if not getattr(self, "project", None) or not getattr(self.project, "font_path", None):
        messagebox.showwarning("警告", "まずフォントを読み込んでください"); return
    # reuse existing editor
    top = getattr(self, "_parts_editor_top", None)
    if top is not None:
        try:
            if top.winfo_exists(): top.lift(); return
        except Exception: pass
    top = tk.Toplevel(self); top.title("偏旁エディタ"); self._parts_editor_top = top
    # resolve GUI class
    cls = globals().get("IntegratedPartsExtractorGUI") or globals().get("PartsExtractorGUI")
    if not cls:
        try:
            import importlib
            mod = importlib.import_module("font_parts_extractor_full07")
            cls = getattr(mod, "IntegratedPartsExtractorGUI", None) or getattr(mod, "PartsExtractorGUI", None)
            if cls: globals()["PartsExtractorGUI"] = cls; globals()["IntegratedPartsExtractorGUI"] = cls
        except Exception: pass
    if not cls:
        messagebox.showerror("起動エラー", "偏旁エディタの統合ブロックが見つかりません。")
        try: top.destroy()
        except Exception: pass
        self._parts_editor_top = None; return
    gui = cls(top); self._parts_editor_gui = gui
    # initial sync
    default_out = os.path.join(getattr(self.project, "_project_dir", os.path.dirname(self.project.font_path)), "assets", "parts")
    try: os.makedirs(default_out, exist_ok=True)
    except Exception: pass
    if hasattr(gui, "set_font_path"):  gui.set_font_path(self.project.font_path)
    if hasattr(gui, "set_output_dir"): gui.set_output_dir(default_out)
    _apply_editor_state_to_gui(self, gui)
    if hasattr(gui, "set_copy_callback"):
        gui.set_copy_callback(lambda img, s, off: self._insert_part_to_active_editor(img, s, off))
    def _import_back():
        if getattr(self, "_is_importing_parts", False): return
        self._is_importing_parts = True
        try:
            # 推奨フォルダを取得
            suggested_dir = None
            if hasattr(gui, "get_output_dir"):
                try: suggested_dir = gui.get_output_dir()
                except Exception: pass
            if not suggested_dir: suggested_dir = default_out

            # ユーザーにフォルダを選択してもらう
            out_dir = filedialog.askdirectory(
                title="偏旁ファイルが保存されているフォルダを選択",
                initialdir=suggested_dir if os.path.isdir(suggested_dir) else os.path.dirname(self.project.font_path)
            )

            if not out_dir:  # キャンセルされた場合
                self._is_importing_parts = False
                return

            # 選択されたフォルダに.pngファイルがあるか確認
            png_files = [f for f in os.listdir(out_dir) if f.lower().endswith('.png')]
            if not png_files:
                if not messagebox.askyesno("確認", f"選択されたフォルダに.pngファイルが見つかりません。\n\nフォルダ: {out_dir}\n\nそれでも続行しますか？"):
                    self._is_importing_parts = False
                    return

            count = self._import_parts_from_folder(out_dir) if hasattr(self, "_import_parts_from_folder") else 0
            _save_editor_state_from_gui(self)
            if hasattr(self, "_open_parts_palette_nospawn"): self._open_parts_palette_nospawn()
            messagebox.showinfo("取り込み完了", f"偏旁を {count} 件 取り込みました\n\nフォルダ: {out_dir}")
        except Exception as e:
            messagebox.showerror("取り込みエラー", f"偏旁の取り込みに失敗しました。\n{e}")
        finally:
            self._is_importing_parts = False
    tk.Button(top, text="本体へ取り込み", command=_import_back).pack(side="bottom", pady=6)

try:
    FontEditorApp._open_parts_editor  = _fe_open_parts_editor_safe   # type: ignore
    FontEditorApp._open_parts_palette = _open_parts_palette_nospawn  # type: ignore
    FontEditorApp._import_parts_from_folder = _import_parts_from_folder  # [FIX] ensure final binding
    FontEditorApp._save_editor_state_from_gui = _save_editor_state_from_gui  # type: ignore
    FontEditorApp._apply_editor_state_to_gui = _apply_editor_state_to_gui    # type: ignore
    FontEditorApp._ensure_editor_slots = _ensure_editor_slots                # type: ignore
except Exception:
    pass
# ===== /PATCH-A =====


# ===== PATCH-B: project bundle (.fep) with parts & editor state + progress UI =====
import json, zipfile, tempfile, shutil, time
from tkinter import ttk
import os

class _SaveProgress(tk.Toplevel):
    def __init__(self, master, title="保存中…"):
        super().__init__(master)
        self.title(title); self.resizable(False, False); self.geometry("420x120")
        self._var_msg = tk.StringVar(value="準備中…"); self._var_pct = tk.StringVar(value="0%")
        ttk.Label(self, textvariable=self._var_msg).pack(anchor="w", padx=12, pady=(12,6))
        self._bar = ttk.Progressbar(self, mode="determinate", length=380, maximum=100); self._bar.pack(padx=12, pady=6)
        ttk.Label(self, textvariable=self._var_pct).pack(anchor="e", padx=12)
        try: self.grab_set()
        except Exception: pass
        self.update_idletasks()
    def set(self, msg, pct=None):
        self._var_msg.set(msg)
        if pct is not None:
            try: self._bar["value"] = max(0, min(100, pct)); self._var_pct.set(f"{int(pct)}%")
            except Exception: pass
        self.update_idletasks()
    def close(self):
        try: self.grab_release()
        except Exception: pass
        self.destroy()

def _save_project_bundle_internal(self, bundle_path: str, embed_font: bool = False):
    proj_dir = getattr(self.project, "_project_dir", None) or os.path.dirname(getattr(self.project, "font_path", "") or os.getcwd())
    tmp = tempfile.mkdtemp(prefix="fep_")
    try:
        assets_parts = os.path.join(tmp, "assets", "parts"); os.makedirs(assets_parts, exist_ok=True)
        # 1) parts write
        parts = getattr(self.project, "parts", {}) or {}
        items = list(parts.items()); total = max(1, len(items))
        catalog_data = {}  # [FIX v1.82.4] カタログデータを保存
        for i, (key, rec) in enumerate(items, 1):
            img, pth = rec.get("image"), rec.get("path")
            meta = rec.get("meta", {})  # [FIX v1.82.4] メタデータを取得
            rel = f"{key}.png"; dst = os.path.join(assets_parts, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if img is not None: img.save(dst, "PNG")
            elif pth and os.path.isfile(pth): shutil.copy2(pth, dst)
            # [FIX v1.82.4] メタデータをカタログに追加
            if meta:
                catalog_data[key] = dict(meta)  # コピーして保存
                catalog_data[key]["file"] = rel
            pct = 10 + int(50 * i / total); self._progress_cb("偏旁を書き出し中…", pct)
        # [FIX v1.82.4] カタログJSONを保存
        if catalog_data:
            catalog_path = os.path.join(assets_parts, "parts_catalog.json")
            with open(catalog_path, "w", encoding="utf-8") as f:
                json.dump(catalog_data, f, ensure_ascii=False, indent=2)
        # 2) editor_state write
        if hasattr(self, "_save_editor_state_from_gui"): self._save_editor_state_from_gui()
        ed_state = getattr(self, "_editor_state", {}) or {}
        with open(os.path.join(tmp, "editor_state.json"), "w", encoding="utf-8") as f:
            json.dump(ed_state, f, ensure_ascii=False, indent=2)
        self._progress_cb("エディタ状態を書き出し中…", 65)
        # 3) manifest
        manifest = {"version": 2, "saved_at": time.time(), "font_path": self.project.font_path, "project_dir": proj_dir, "embed_font": bool(embed_font), "parts_count": len(parts)}
        with open(os.path.join(tmp, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        self._progress_cb("メタデータを書き出し中…", 70)
        # 4) font optional
        if embed_font and self.project.font_path and os.path.isfile(self.project.font_path):
            fonts_dir = os.path.join(tmp, "fonts"); os.makedirs(fonts_dir, exist_ok=True)
            shutil.copy2(self.project.font_path, os.path.join(fonts_dir, os.path.basename(self.project.font_path)))
        self._progress_cb("フォントを同梱中…", 75)
        # 5) zip
        with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
            files = []
            for root, _, fs in os.walk(tmp):
                for name in fs:
                    abs = os.path.join(root, name); rel = os.path.relpath(abs, tmp); files.append((abs, rel))
            total_zip = max(1, len(files))
            for i, (abs, rel) in enumerate(files, 1):
                z.write(abs, rel)
                pct = 75 + int(25 * i / total_zip); self._progress_cb("アーカイブ中…", pct)
        self._progress_cb("完了", 100)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def save_project_bundle_ui(self, embed_font: bool = False):
    from tkinter import filedialog
    path = filedialog.asksaveasfilename(title="プロジェクトを保存 (.fep)", defaultextension=".fep", filetypes=[("Font Editor Project","*.fep"),("Zip","*.zip"),("All","*.*")])
    if not path: return
    dlg = _SaveProgress(self, title="プロジェクト保存")
    def _cb(msg, pct=None):
        try: dlg.set(msg, pct)
        except Exception: pass
    self._progress_cb = _cb
    def _run():
        try:
            _cb("準備中…", 5)
            _save_project_bundle_internal(self, path, embed_font=embed_font)
            self.after(0, lambda: (dlg.set("保存が完了しました", 100), dlg.close(), messagebox.showinfo("保存", "保存が完了しました")))
        except Exception as e:
            self.after(0, lambda: (dlg.close(), messagebox.showerror("保存エラー", f"保存に失敗しました。\\n{e}")))
    threading.Thread(target=_run, daemon=True).start()

def load_project_bundle(self, bundle_path: str, extract_to: str = None):
    if extract_to is None:
        stem = os.path.splitext(os.path.basename(bundle_path))[0]
        extract_to = os.path.join(os.path.dirname(bundle_path), f"{stem}_proj")
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(bundle_path, "r") as z: z.extractall(extract_to)
    # manifest
    manifest_path = os.path.join(extract_to, "manifest.json")
    try:
        with open(manifest_path, "r", encoding="utf-8") as f: manifest = json.load(f)
    except Exception: manifest = {}
    # font
    fonts_dir = os.path.join(extract_to, "fonts")
    if os.path.isdir(fonts_dir):
        for n in os.listdir(fonts_dir):
            if n.lower().endswith((".ttf",".otf",".ttc")):
                self.project.font_path = os.path.join(fonts_dir, n); break
    else:
        if manifest.get("font_path"): self.project.font_path = manifest["font_path"]
    # project dir
    self.project._project_dir = extract_to
    # parts
    parts_dir = os.path.join(extract_to, "assets", "parts")
    if hasattr(self, "_import_parts_from_folder") and os.path.isdir(parts_dir):
        self._import_parts_from_folder(parts_dir)
    # editor_state
    ed_path = os.path.join(extract_to, "editor_state.json")
    if os.path.isfile(ed_path):
        try:
            with open(ed_path, "r", encoding="utf-8") as f: self._editor_state = json.load(f) or {}
        except Exception: self._editor_state = {}
    # palette refresh
    try:
        if hasattr(self, "_open_parts_palette_nospawn"): self._open_parts_palette_nospawn()
    except Exception: pass

try:
    FontEditorApp.save_project_bundle_ui = save_project_bundle_ui  # type: ignore
    FontEditorApp.load_project_bundle    = load_project_bundle     # type: ignore
except Exception:
    pass
# ===== /PATCH-B =====


if __name__ == '__main__':
    app = FontEditorApp()
    app.mainloop()

# ===== [INTEGRATED-PARTS-CATALOG] =====



# ===== [INTEGRATED-PARTS-UTILS] =====



# ===== [INTEGRATED-PARTS-CORE] =====



# ===== [INTEGRATED-PARTS-GUI] =====



# === [INTEGRATED] bind methods to FontEditorApp ===
# [FIX v1.82.1] Commented out old bindings - use new implementations from PATCH-A (line 4691-4693)
# FontEditorApp._open_parts_editor = _wrap(_open_parts_editor_impl)  # type: ignore
# FontEditorApp._open_parts_palette = _wrap(_open_parts_palette_impl)  # type: ignore
# expose helpers (not UI)
FontEditorApp._get_parts_output_dir = _get_parts_output_dir_impl  # type: ignore
# FontEditorApp._import_parts_from_folder = _import_parts_from_folder  # type: ignore  # [FIX] prefer counting importer (already bound at line 4693)


# ===== [INTEGRATED-PARTS] BEGIN =====

# ============================================================
# [DYNAMIC-BOUNDARY] 動的境界検出アルゴリズム (v1.82.9)
# ============================================================

class DynamicBoundaryDetector:
    """動的境界検出器 - 画像解析で最適な分割位置を自動検出（v1.82.9）"""

    def __init__(self, binary_threshold: int = 200):
        self.binary_threshold = binary_threshold

    def find_optimal_split(self, img: Image.Image, direction: str = "vertical",
                          search_range: Tuple[float, float] = (0.3, 0.7),
                          num_candidates: int = 3) -> List[Tuple[float, float, Dict]]:
        """
        最適な分割位置を検出

        Args:
            img: 入力画像
            direction: "vertical" (左右分割) or "horizontal" (上下分割)
            search_range: 探索範囲 (min_ratio, max_ratio)
            num_candidates: 返す候補数

        Returns:
            [(ratio, score, info), ...] のリスト
            - ratio: 分割比率（0.0～1.0）
            - score: スコア（低いほど境界らしい）
            - info: 詳細情報
        """
        w, h = img.size
        img_array = np.array(img)
        binary = img_array < self.binary_threshold

        candidates = []

        if direction == "vertical":
            # 縦方向に走査（左右分割）
            for ratio in np.arange(search_range[0], search_range[1], Config.BOUNDARY_SCAN_STEP):
                x = int(w * ratio)
                if x <= 0 or x >= w:
                    continue

                # この位置での垂直線上の黒ピクセル密度
                line = binary[:, x]
                density = np.sum(line) / h

                # 周辺の密度変化も考慮（境界っぽさを強調）
                edge_score = self._calculate_edge_score(binary, x, "vertical")

                # 総合スコア（密度が低く、エッジが強いほど良い）
                score = density * 0.7 + (1.0 - edge_score) * 0.3

                candidates.append((ratio, score, {
                    'density': density,
                    'edge_score': edge_score,
                    'position': x
                }))
        else:
            # 横方向に走査（上下分割）
            for ratio in np.arange(search_range[0], search_range[1], Config.BOUNDARY_SCAN_STEP):
                y = int(h * ratio)
                if y <= 0 or y >= h:
                    continue

                line = binary[y, :]
                density = np.sum(line) / w

                edge_score = self._calculate_edge_score(binary, y, "horizontal")

                score = density * 0.7 + (1.0 - edge_score) * 0.3

                candidates.append((ratio, score, {
                    'density': density,
                    'edge_score': edge_score,
                    'position': y
                }))

        # スコアが低い順（境界らしい順）にソート
        candidates.sort(key=lambda x: x[1])

        # トップN候補を返す
        return candidates[:num_candidates]

    def _calculate_edge_score(self, binary: np.ndarray, position: int, direction: str) -> float:
        """エッジスコアを計算（境界の強さ）"""
        h, w = binary.shape

        if direction == "vertical":
            if position <= 2 or position >= w - 3:
                return 0.0

            # 左右の密度差
            left_region = binary[:, max(0, position - 5):position]
            right_region = binary[:, position:min(w, position + 5)]

            left_density = np.sum(left_region) / (left_region.size + 1e-8)
            right_density = np.sum(right_region) / (right_region.size + 1e-8)

            # 密度差が大きいほど境界らしい
            edge_strength = abs(left_density - right_density)

            return edge_strength
        else:
            if position <= 2 or position >= h - 3:
                return 0.0

            top_region = binary[max(0, position - 5):position, :]
            bottom_region = binary[position:min(h, position + 5), :]

            top_density = np.sum(top_region) / (top_region.size + 1e-8)
            bottom_density = np.sum(bottom_region) / (bottom_region.size + 1e-8)

            edge_strength = abs(top_density - bottom_density)

            return edge_strength


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
        "にんべん": {"char": "亻", "sample": "仁", "split": "left", "ratio": 0.35, "alternatives": ["人", "他", "住", "作", "使"]},
        "ぎょうにんべん": {"char": "彳", "sample": "行", "split": "left", "ratio": 0.3, "alternatives": ["往", "待", "役"]},
        "りっしんべん": {"char": "忄", "sample": "情", "split": "left", "ratio": 0.3, "alternatives": ["性", "怖", "悩", "快"]},

        # 手・動作に関する偏
        "てへん": {"char": "扌", "sample": "持", "split": "left", "ratio": 0.35, "alternatives": ["手", "打", "投", "押", "拾"]},
        "さんずい": {"char": "氵", "sample": "海", "split": "left", "ratio": 0.3, "alternatives": ["江", "河", "波", "池", "湖"]},

        # 言葉に関する偏
        "ごんべん": {"char": "訁", "sample": "語", "split": "left", "ratio": 0.4, "alternatives": ["話", "説", "訳", "記", "論"]},
        "くちへん": {"char": "口", "sample": "呼", "split": "left", "ratio": 0.4, "alternatives": ["味", "吸", "鳴", "唱"]},

        # 木・植物に関する偏
        "きへん": {"char": "木", "sample": "林", "split": "left", "ratio": 0.4, "alternatives": ["村", "森", "木", "桜", "松"]},
        "のぎへん": {"char": "禾", "sample": "秋", "split": "left", "ratio": 0.4, "alternatives": ["和", "私", "秀"]},
        
        # 金属・鉱物に関する偏
        "かねへん": {"char": "金", "sample": "鉄", "split": "left", "ratio": 0.45, "alternatives": ["銅", "銀", "鋼", "鉱", "鋭"]},
        "いしへん": {"char": "石", "sample": "砂", "split": "left", "ratio": 0.4, "alternatives": ["岩", "研", "硬", "確"]},

        # 糸・衣に関する偏
        "いとへん": {"char": "糸", "sample": "結", "split": "left", "ratio": 0.45, "alternatives": ["糸", "線", "紙", "級", "紅"]},
        "ころもへん": {"char": "衤", "sample": "被", "split": "left", "ratio": 0.35, "alternatives": ["袖", "裕", "補"]},

        # 食べ物に関する偏
        "しょくへん": {"char": "飠", "sample": "館", "split": "left", "ratio": 0.4, "alternatives": ["飯", "飲", "飾"]},

        # 動物に関する偏
        "けものへん": {"char": "犭", "sample": "狼", "split": "left", "ratio": 0.35, "alternatives": ["犬", "猫", "狐", "狩", "猟"]},
        "うおへん": {"char": "魚", "sample": "鮮", "split": "left", "ratio": 0.5, "alternatives": ["鯨", "鮭", "鯛"]},
        "むしへん": {"char": "虫", "sample": "蛇", "split": "left", "ratio": 0.4, "alternatives": ["虫", "蚊", "蝶", "蜂"]},

        # 土・自然に関する偏
        "つちへん": {"char": "土", "sample": "城", "split": "left", "ratio": 0.35, "alternatives": ["土", "地", "場", "坂", "型"]},
        "やまへん": {"char": "山", "sample": "峰", "split": "left", "ratio": 0.4, "alternatives": ["山", "岳", "崎", "峠"]},

        # 火・水に関する偏
        "ひへん": {"char": "火", "sample": "灯", "split": "left", "ratio": 0.35, "alternatives": ["火", "炎", "焼", "煙"]},
        "にすい": {"char": "冫", "sample": "冷", "split": "left", "ratio": 0.25, "alternatives": ["冬", "凍", "冴"]},

        # 体の部位に関する偏
        "にくづき": {"char": "月", "sample": "胸", "split": "left", "ratio": 0.4, "alternatives": ["肉", "腕", "脳", "腹", "胃"]},
        "ほねへん": {"char": "骨", "sample": "骸", "split": "left", "ratio": 0.5, "alternatives": ["骨", "髄"]},
        "めへん": {"char": "目", "sample": "眼", "split": "left", "ratio": 0.4, "alternatives": ["目", "眠", "睡", "瞬"]},
        "みみへん": {"char": "耳", "sample": "聴", "split": "left", "ratio": 0.4, "alternatives": ["耳", "聞", "聖"]},
        "みへん": {"char": "身", "sample": "躯", "split": "left", "ratio": 0.4, "alternatives": ["身", "躰"]},

        # その他の重要な偏
        "やまいだれへん": {"char": "疒", "sample": "病", "split": "left", "ratio": 0.3, "alternatives": ["痛", "症", "疲", "癒"]},
        "おんなへん": {"char": "女", "sample": "妹", "split": "left", "ratio": 0.4, "alternatives": ["女", "姉", "妻", "好", "娘"]},
        "こざとへん": {"char": "阝", "sample": "防", "split": "left", "ratio": 0.3, "alternatives": ["陽", "阪", "陸", "院"]},
        "しめすへん": {"char": "礻", "sample": "祈", "split": "left", "ratio": 0.35, "alternatives": ["神", "社", "福", "祝"]},

        # マイナーな偏
        "ゆみへん": {"char": "弓", "sample": "張", "split": "left", "ratio": 0.35, "alternatives": ["引", "弱", "弦"]},
        "かわへん": {"char": "革", "sample": "靴", "split": "left", "ratio": 0.45, "alternatives": ["革"]},
        "かいへん": {"char": "貝", "sample": "販", "split": "left", "ratio": 0.4, "alternatives": ["貝", "買", "貨", "貧"]},
        "あしへん": {"char": "足", "sample": "跡", "split": "left", "ratio": 0.45, "alternatives": ["足", "跳", "路", "踊"]},
        "くるまへん": {"char": "車", "sample": "輪", "split": "left", "ratio": 0.45, "alternatives": ["車", "軽", "転", "軸"]},
        "さけのとり": {"char": "酉", "sample": "配", "split": "left", "ratio": 0.4, "alternatives": ["酒", "酔", "酸"]},
        "うしへん": {"char": "牛", "sample": "牡", "split": "left", "ratio": 0.4, "alternatives": ["牛", "物", "特"]},
        "ちからへん": {"char": "力", "sample": "加", "split": "left", "ratio": 0.35, "alternatives": ["力", "努", "動"]},
        "まめへん": {"char": "豆", "sample": "豉", "split": "left", "ratio": 0.4, "alternatives": ["豆", "豊"]},
        "ぶたへん": {"char": "豕", "sample": "豚", "split": "left", "ratio": 0.4, "alternatives": ["豚", "豪"]},
    },
    
    # ===== 旁（つくり）: 右側配置のみ - 35種類 =====
    "tsukuri": {
        # 基本的な旁
        "おおざと": {"char": "阝", "sample": "部", "split": "right", "ratio": 0.7, "alternatives": ["都", "郡", "郵", "那"]},
        "りっとう": {"char": "刂", "sample": "則", "split": "right", "ratio": 0.7, "alternatives": ["刻", "削", "制", "割", "列"]},
        "ちから": {"char": "力", "sample": "助", "split": "right", "ratio": 0.65, "alternatives": ["力", "功", "勉", "務"]},
        "おおがい": {"char": "頁", "sample": "順", "split": "right", "ratio": 0.55, "alternatives": ["頭", "顔", "題", "領"]},
        "ぼくづくり": {"char": "攵", "sample": "政", "split": "right", "ratio": 0.65, "alternatives": ["教", "救", "故", "敗"]},

        # 鳥・動物系
        "ふるとり": {"char": "隹", "sample": "雑", "split": "right", "ratio": 0.6, "alternatives": ["準", "雄", "離"]},
        "とり": {"char": "鳥", "sample": "鳩", "split": "right", "ratio": 0.55, "alternatives": ["鳥", "鶏", "鳴"]},
        "うま": {"char": "馬", "sample": "駅", "split": "right", "ratio": 0.55, "alternatives": ["馬", "駐", "騎", "験"]},
        "しか": {"char": "鹿", "sample": "麗", "split": "right", "ratio": 0.55, "alternatives": ["鹿", "麓"]},

        # 武器・道具系
        "きづくり": {"char": "斤", "sample": "新", "split": "right", "ratio": 0.65, "alternatives": ["近", "斬", "析"]},
        "ほこづくり": {"char": "戈", "sample": "成", "split": "right", "ratio": 0.6, "alternatives": ["戦", "戯", "戒"]},
        "おのづくり": {"char": "斤", "sample": "所", "split": "right", "ratio": 0.65, "alternatives": ["断", "斬", "斯"]},
        "かたな": {"char": "刀", "sample": "切", "split": "right", "ratio": 0.65, "alternatives": ["刀", "分", "刃"]},
        "ほこ": {"char": "殳", "sample": "殴", "split": "right", "ratio": 0.6, "alternatives": ["殺", "殻"]},

        # 文字・記号系
        "ふでづくり": {"char": "聿", "sample": "律", "split": "right", "ratio": 0.6, "alternatives": ["建", "筆", "書"]},
        "ぼく": {"char": "攴", "sample": "牧", "split": "right", "ratio": 0.65, "alternatives": ["枚", "収", "放"]},
        "おおざと右": {"char": "邑", "sample": "郎", "split": "right", "ratio": 0.6, "alternatives": ["郷", "都", "郭"]},

        # 自然・天体系
        "おうへん": {"char": "王", "sample": "珠", "split": "right", "ratio": 0.6, "alternatives": ["理", "球", "現"]},
        "つき": {"char": "月", "sample": "朝", "split": "right", "ratio": 0.6, "alternatives": ["期", "明", "服"]},
        "ひ": {"char": "日", "sample": "旧", "split": "right", "ratio": 0.6, "alternatives": ["日", "明", "時", "昭"]},
        "かぜ": {"char": "風", "sample": "颯", "split": "right", "ratio": 0.55, "alternatives": ["風", "嵐"]},

        # 体・感覚系
        "みる": {"char": "見", "sample": "規", "split": "right", "ratio": 0.6, "alternatives": ["見", "視", "親", "観"]},
        "きく": {"char": "音", "sample": "韻", "split": "right", "ratio": 0.55, "alternatives": ["音", "章", "竟"]},
        "あくび": {"char": "欠", "sample": "歌", "split": "right", "ratio": 0.65, "alternatives": ["欠", "欧", "次"]},

        # 食物・植物系
        "むぎ": {"char": "麦", "sample": "麺", "split": "right", "ratio": 0.55, "alternatives": ["麦", "麹"]},
        "まめ": {"char": "豆", "sample": "豊", "split": "right", "ratio": 0.6, "alternatives": ["豆", "豊", "登"]},

        # その他
        "おおがい頁": {"char": "頁", "sample": "頭", "split": "right", "ratio": 0.55, "alternatives": ["頂", "順", "預", "願"]},
        "おに": {"char": "鬼", "sample": "魅", "split": "right", "ratio": 0.55, "alternatives": ["鬼", "魂", "魔"]},
        "かい右": {"char": "貝", "sample": "頁", "split": "right", "ratio": 0.6, "alternatives": ["貝", "財", "貿"]},
        "ふ": {"char": "阜", "sample": "陸", "split": "right", "ratio": 0.6, "alternatives": ["院", "陰", "隊"]},

        # 複合系
        "けん": {"char": "見", "sample": "視", "split": "right", "ratio": 0.6, "alternatives": ["覧", "覚", "観"]},
        "せい": {"char": "斉", "sample": "済", "split": "right", "ratio": 0.6, "alternatives": ["斉", "剤"]},
        "き": {"char": "气", "sample": "気", "split": "right", "ratio": 0.6, "alternatives": ["気", "汽"]},
        "しゅう": {"char": "隹", "sample": "集", "split": "right", "ratio": 0.6, "alternatives": ["集", "進", "焦"]},
        "よう": {"char": "羊", "sample": "養", "split": "right", "ratio": 0.6, "alternatives": ["羊", "洋", "様", "美"]},
    },
    
    # ===== 冠（かんむり）: 上側配置 - 28種類 =====
    "kanmuri": {
        # 植物に関する冠
        "くさかんむり": {"char": "艹", "sample": "花", "split": "top", "ratio": 0.3, "alternatives": ["草", "茶", "英", "菜", "若"]},
        "たけかんむり": {"char": "⺮", "sample": "笑", "split": "top", "ratio": 0.35, "alternatives": ["竹", "筆", "箱", "第"]},

        # 自然・天候に関する冠
        "あめかんむり": {"char": "雨", "sample": "雷", "split": "top", "ratio": 0.4, "alternatives": ["雪", "雲", "電", "需"]},
        "やまかんむり": {"char": "山", "sample": "崩", "split": "top", "ratio": 0.35, "alternatives": ["岩", "岡"]},

        # 建物・覆うものに関する冠
        "うかんむり": {"char": "宀", "sample": "宇", "split": "top", "ratio": 0.25, "alternatives": ["家", "室", "安", "定", "宗"]},
        "あなかんむり": {"char": "穴", "sample": "空", "split": "top", "ratio": 0.35, "alternatives": ["究", "窓", "窮"]},
        "わかんむり": {"char": "冖", "sample": "冠", "split": "top", "ratio": 0.25, "alternatives": ["軍", "冗"]},
        
        # 網・枠に関する冠
        "あみがしら": {"char": "罒", "sample": "買", "split": "top", "ratio": 0.3, "alternatives": ["罪", "置", "署"]},
        "よこめ": {"char": "⺫", "sample": "置", "split": "top", "ratio": 0.3, "alternatives": ["眞", "県", "真"]},

        # 形・記号的な冠
        "なべぶた": {"char": "亠", "sample": "市", "split": "top", "ratio": 0.2, "alternatives": ["亡", "交", "京", "亭"]},
        "はちがしら": {"char": "八", "sample": "公", "split": "top", "ratio": 0.25, "alternatives": ["八", "六", "共", "兵"]},
        "ひとやね": {"char": "𠆢", "sample": "会", "split": "top", "ratio": 0.2, "alternatives": ["今", "会", "合"]},
        "つめかんむり": {"char": "爫", "sample": "受", "split": "top", "ratio": 0.3, "alternatives": ["采", "爵", "妥"]},
        "てんてん": {"char": "⺀", "sample": "当", "split": "top", "ratio": 0.25, "alternatives": ["尚", "当", "党"]},

        # その他の冠
        "しょうがしら": {"char": "⺌", "sample": "尚", "split": "top", "ratio": 0.25, "alternatives": ["常", "堂", "党"]},
        "だいかんむり": {"char": "大", "sample": "奇", "split": "top", "ratio": 0.3, "alternatives": ["大", "奈", "套", "奔"]},
        "ひとがしら": {"char": "人", "sample": "介", "split": "top", "ratio": 0.25, "alternatives": ["人", "令", "企", "全"]},
        "けいがしら": {"char": "⺕", "sample": "前", "split": "top", "ratio": 0.3, "alternatives": ["首", "道", "俞"]},
        "おいがしら": {"char": "老", "sample": "考", "split": "top", "ratio": 0.35, "alternatives": ["者", "老", "孝"]},
        "ちいさい": {"char": "小", "sample": "尖", "split": "top", "ratio": 0.3, "alternatives": ["小", "少", "尚"]},
        "そうにょう": {"char": "⺍", "sample": "学", "split": "top", "ratio": 0.25, "alternatives": ["学", "覚"]},
        "なつあし上": {"char": "夂", "sample": "条", "split": "top", "ratio": 0.3, "alternatives": ["夏", "冬", "各"]},
        "かぜがまえ": {"char": "風", "sample": "風", "split": "top", "ratio": 0.4, "alternatives": ["風", "凧"]},
        "おおいかんむり": {"char": "覀", "sample": "要", "split": "top", "ratio": 0.35, "alternatives": ["要", "覆"]},
        "あめ": {"char": "雨", "sample": "雪", "split": "top", "ratio": 0.4, "alternatives": ["雨", "雷", "零"]},
        "くち上": {"char": "口", "sample": "吉", "split": "top", "ratio": 0.3, "alternatives": ["口", "古", "只"]},
        "つち上": {"char": "土", "sample": "吉", "split": "top", "ratio": 0.3, "alternatives": ["土", "去", "圭"]},
        "くさ": {"char": "艸", "sample": "草", "split": "top", "ratio": 0.3, "alternatives": ["草", "荘", "蒼"]},
    },
    
    # ===== 脚（あし）: 下側配置 - 12種類 =====
    "ashi": {
        "こころ": {"char": "心", "sample": "念", "split": "bottom", "ratio": 0.65, "alternatives": ["心", "思", "忍", "志"]},
        "れっか": {"char": "灬", "sample": "熱", "split": "bottom", "ratio": 0.75, "alternatives": ["点", "照", "然", "煮"]},
        "ひとあし": {"char": "儿", "sample": "児", "split": "bottom", "ratio": 0.7, "alternatives": ["見", "元", "光", "兄"]},
        "したごころ": {"char": "心", "sample": "恋", "split": "bottom", "ratio": 0.7, "alternatives": ["愛", "意", "想", "態"]},
        "したみず": {"char": "水", "sample": "泰", "split": "bottom", "ratio": 0.7, "alternatives": ["水"]},
        "さら": {"char": "皿", "sample": "盛", "split": "bottom", "ratio": 0.7, "alternatives": ["盟", "盆", "益"]},
        "こうあし": {"char": "儿", "sample": "兄", "split": "bottom", "ratio": 0.7, "alternatives": ["先", "充", "克"]},
        "したひ": {"char": "灬", "sample": "煮", "split": "bottom", "ratio": 0.75, "alternatives": ["蒸", "烈", "焦"]},
        "かい": {"char": "貝", "sample": "買", "split": "bottom", "ratio": 0.65, "alternatives": ["貝", "資", "賞", "賀"]},
        "こころあし": {"char": "心", "sample": "慕", "split": "bottom", "ratio": 0.7, "alternatives": ["忠", "恵", "慰"]},
        "したしたごころ": {"char": "灬", "sample": "点", "split": "bottom", "ratio": 0.75, "alternatives": ["黒", "魚", "無"]},
        "れんが": {"char": "灬", "sample": "煎", "split": "bottom", "ratio": 0.75, "alternatives": ["煎", "煮", "熟"]},
    },
    
    # ===== 繞（にょう）: 左下を囲む - 5種類 =====
    "nyou": {
        "しんにょう": {"char": "辶", "sample": "近", "split": "left_bottom", "ratio": 0.6, "alternatives": ["道", "通", "送", "進", "遠"]},
        "えんにょう": {"char": "廴", "sample": "延", "split": "left_bottom", "ratio": 0.55, "alternatives": ["廷", "建", "延"]},
        "そうにょう走": {"char": "走", "sample": "起", "split": "left_bottom", "ratio": 0.65, "alternatives": ["走", "赴", "超"]},
        "えんにょう廴": {"char": "廴", "sample": "建", "split": "left_bottom", "ratio": 0.55, "alternatives": ["延", "廷", "廻"]},
        "かんにょう": {"char": "⻎", "sample": "道", "split": "left_bottom", "ratio": 0.65, "alternatives": ["辿", "辺", "迅"]},
    },
    
    # ===== 垂（たれ）: 上から左へ垂れる - 10種類 =====
    "tare": {
        "がんだれ": {"char": "厂", "sample": "原", "split": "top_left", "ratio": 0.5, "alternatives": ["厚", "厳", "圧", "雁"]},
        "まだれ": {"char": "广", "sample": "広", "split": "top_left", "ratio": 0.45, "alternatives": ["店", "庭", "度", "座", "庫"]},
        "やまいだれ": {"char": "疒", "sample": "痛", "split": "top_left", "ratio": 0.45, "alternatives": ["病", "疲", "痩", "症", "療"]},
        "とだれ": {"char": "戸", "sample": "戻", "split": "top_left", "ratio": 0.5, "alternatives": ["戸", "所", "扉"]},
        "しかばねだれ": {"char": "尸", "sample": "局", "split": "top_left", "ratio": 0.45, "alternatives": ["尻", "尾", "層", "屋"]},
        "かばねだれ": {"char": "尸", "sample": "屋", "split": "top_left", "ratio": 0.45, "alternatives": ["屈", "展", "屠", "属"]},
        "とびがしら": {"char": "飛", "sample": "飛", "split": "top_left", "ratio": 0.5, "alternatives": ["飛"]},
        "いわだれ": {"char": "厂", "sample": "厚", "split": "top_left", "ratio": 0.45, "alternatives": ["原", "厨", "厩"]},
        "たれ": {"char": "广", "sample": "店", "split": "top_left", "ratio": 0.45, "alternatives": ["広", "庄", "床", "序"]},
        "がんだれ厂": {"char": "厂", "sample": "雁", "split": "top_left", "ratio": 0.5, "alternatives": ["厄", "厘", "厳"]},
    },
    
    # ===== 構（かまえ）: 周りを囲む - 14種類 =====
    "kamae": {
        "もんがまえ": {"char": "門", "sample": "間", "split": "frame", "ratio": 0.5, "alternatives": ["門", "開", "閉", "閣", "関"]},
        "くにがまえ": {"char": "囗", "sample": "国", "split": "frame", "ratio": 0.5, "alternatives": ["四", "回", "囲", "因", "団"]},
        "どうがまえ": {"char": "行", "sample": "衛", "split": "frame", "ratio": 0.5, "alternatives": ["街", "術", "衝"]},
        "かくしがまえ": {"char": "匸", "sample": "匹", "split": "frame", "ratio": 0.5, "alternatives": ["区", "医", "匿"]},
        "はこがまえ": {"char": "匚", "sample": "匠", "split": "frame", "ratio": 0.45, "alternatives": ["匠", "匡", "匿"]},
        "けいがまえ": {"char": "冂", "sample": "円", "split": "frame", "ratio": 0.45, "alternatives": ["冊", "再", "周", "内"]},
        "もんがまえ門": {"char": "門", "sample": "門", "split": "frame", "ratio": 0.5, "alternatives": ["問", "聞", "閥"]},
        "とうがまえ": {"char": "鬨", "sample": "鬥", "split": "frame", "ratio": 0.5, "alternatives": ["闘", "鬥"]},
        "くがまえ": {"char": "句", "sample": "句", "split": "frame", "ratio": 0.45, "alternatives": ["句", "拘", "勾"]},
        "とかまえ": {"char": "戸", "sample": "房", "split": "frame", "ratio": 0.5, "alternatives": ["戸", "扇", "戻"]},
        "むじなへん": {"char": "鬼", "sample": "魂", "split": "frame", "ratio": 0.55, "alternatives": ["鬼", "魅", "魔"]},
        "しきがまえ": {"char": "式", "sample": "式", "split": "frame", "ratio": 0.5, "alternatives": ["式", "試"]},
        "かぜがまえ": {"char": "風", "sample": "凪", "split": "frame", "ratio": 0.5, "alternatives": ["風", "嵐"]},
        "とがまえ": {"char": "戸", "sample": "扉", "split": "frame", "ratio": 0.5, "alternatives": ["戸", "所", "扇"]},
    },
}

# ============================================================
# [BLOCK1-END]
# ============================================================











# ============================================================
# [BLOCK2-BEGIN] 画像処理ユーティリティ (2025-10-10)
# ============================================================

def render_char_to_bitmap(char, font_path, size=2048):
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
    """単一パーツを抽出（フォールバック機能 + 動的境界検出対応）"""
    try:
        split_type = part_info["split"]
        ratio = part_info.get("ratio", 0.5)

        # 試行する文字のリスト（プライマリ + 代替文字）
        candidates = [part_info["sample"]]
        if "alternatives" in part_info:
            candidates.extend(part_info["alternatives"])

        # 各候補でレンダリングを試行
        img = None
        used_char = None
        for candidate_char in candidates:
            img = render_char_to_bitmap(candidate_char, font_path)
            if img is not None:
                used_char = candidate_char
                break

        # 全ての候補で失敗した場合
        if img is None:
            return False, None, "レンダリング失敗（全ての代替文字でも失敗）", None

        # 動的境界検出（オプション機能）
        used_ratio = ratio
        if Config.DYNAMIC_BOUNDARY_DETECTION:
            try:
                detector = DynamicBoundaryDetector(binary_threshold=Config.BINARY_THRESHOLD)

                # split_typeから方向を決定
                if split_type in ["left", "right"]:
                    direction = "vertical"
                    search_range = Config.BOUNDARY_SEARCH_RANGE_LR
                elif split_type in ["top", "bottom"]:
                    direction = "horizontal"
                    search_range = Config.BOUNDARY_SEARCH_RANGE_TB
                else:
                    # frame, left_bottom, top_left は動的検出非対応（固定ratioを使用）
                    direction = None

                if direction:
                    # 最適な分割位置を検出
                    candidates_dynamic = detector.find_optimal_split(img, direction, search_range, num_candidates=1)
                    if candidates_dynamic:
                        used_ratio = candidates_dynamic[0][0]  # トップ候補のratio
            except Exception as e:
                # 動的検出に失敗した場合は固定ratioを使用（無視して続行）
                pass

        # 分割処理
        part_img = split_glyph(img, split_type, used_ratio)
        if part_img is None:
            return False, None, "分割失敗", used_char

        # ノイズ除去
        if noise_removal:
            part_img = remove_noise(part_img)

        # 余白トリミング
        part_img = trim_whitespace(part_img)

        # 保存
        if save_as_transparent_png(part_img, output_path):
            return True, part_img, None, used_char, used_ratio
        else:
            return False, None, "保存失敗", used_char, used_ratio

    except Exception as e:
        return False, None, str(e), None, ratio


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
    log("偏旁抽出ツール v2.9 (動的境界検出対応)")
    log("=" * 70)
    log(f"フォント: {font_path}")
    log(f"出力先: {output_dir}")
    log(f"動的境界検出: {'有効' if Config.DYNAMIC_BOUNDARY_DETECTION else '無効'}")
    if Config.DYNAMIC_BOUNDARY_DETECTION:
        log(f"  探索範囲(左右): {Config.BOUNDARY_SEARCH_RANGE_LR}")
        log(f"  探索範囲(上下): {Config.BOUNDARY_SEARCH_RANGE_TB}")
        log(f"  スキャンステップ: {Config.BOUNDARY_SCAN_STEP}")
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

            success, img, error, used_char, used_ratio = extract_single_part(font_path, part_name, part_info, output_path)

            if success:
                # ログメッセージの構築
                log_parts = [msg, " ... ✅ 保存完了"]

                # 使用文字が異なる場合
                if used_char != part_info["sample"]:
                    log_parts.append(f" (使用文字: {used_char})")

                # 動的境界検出が使用された場合
                original_ratio = part_info.get("ratio", 0.5)
                if Config.DYNAMIC_BOUNDARY_DETECTION and abs(used_ratio - original_ratio) > 0.01:
                    log_parts.append(f" [動的検出: {original_ratio:.2f} → {used_ratio:.2f}]")

                log("".join(log_parts))
                stats["success"] += 1
                category_stats["success"] += 1

                catalog_json[category][part_name] = {
                    "char": part_info["char"],
                    "sample": used_char if used_char else part_info["sample"],  # 実際に使用した文字を記録
                    "file": filename,
                    "split": part_info["split"],
                    "ratio": part_info.get("ratio", 0.5),
                    "used_ratio": used_ratio,  # 実際に使用されたratio
                    "category": category  # カテゴリ情報を追加
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
            if len(self.undo_stack) > Config.MAX_UNDO_STACK:
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
        self.root.title("偏旁抽出ツール v2.9 (2025-11-06) - 動的境界検出対応")

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
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # ログエクスポートボタン
        log_button_frame = ttk.Frame(log_frame)
        log_button_frame.pack(fill=tk.X)
        ttk.Button(log_button_frame, text="📄 ログを保存", command=self._export_log).pack(side=tk.RIGHT)

        self._log("偏旁抽出ツール v2.9 - 動的境界検出対応")
        self._log("=" * 70)
        self._log("【更新内容】")
        self._log("  ✅ 動的境界検出: 画像解析で最適な分割位置を自動検出")
        self._log("  ✅ 高精度抽出: 接触文字でも境界を正確に判定")
        self._log("  ✅ 詳細ログ: 使用された検出値をリアルタイム表示")
        self._log(f"  ⚙️ 設定: 動的検出 {'有効' if Config.DYNAMIC_BOUNDARY_DETECTION else '無効'}")
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

    def _export_log(self):
        """ログをテキストファイルにエクスポート"""
        # ログの内容を取得
        log_content = self.log_text.get("1.0", tk.END)

        if not log_content.strip():
            messagebox.showwarning("警告", "ログが空です")
            return

        # デフォルトファイル名（タイムスタンプ付き）
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"parts_extraction_log_{timestamp}.txt"

        # 保存先を選択
        filepath = filedialog.asksaveasfilename(
            title="ログを保存",
            initialfile=default_filename,
            defaultextension=".txt",
            filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")]
        )

        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                messagebox.showinfo("保存完了", f"ログを保存しました:\n{filepath}")
                self._log(f"\n📄 ログを保存: {filepath}")
            except Exception as e:
                messagebox.showerror("エラー", f"ログの保存に失敗しました:\n{e}")

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


# ===== [オプション OPTION1-END] =====











# ################################################################################
# ■■■ メインエントリポイント ■■■
# ################################################################################











# ===== [MAIN-BEGIN] メインエントリポイント =====

def main_font_editor():
    """フォントエディタのメインアプリケーションを起動"""
    try:
        app = FontEditorApp()
        app.mainloop()
    except Exception as e:
        print(f"[FATAL ERROR in Font Editor] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main_parts_tool():
    """偏旁抽出ツールを起動"""
    try:
        root = tk.Tk()
        root.geometry("900x750")
        app = PartsExtractorGUI(root)
        if sys.platform == "darwin":
            root.createcommand("tk::mac::Quit", root.quit)
        root.mainloop()
    except Exception as e:
        print(f"[FATAL ERROR in Parts Tool] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# エイリアス（後方互換性のため）
main = main_font_editor
IntegratedPartsExtractorGUI = PartsExtractorGUI


if __name__ == '__main__':
    # デフォルトではフォントエディタを起動
    # オプションで偏旁ツールも起動可能: python font_editor1.81.py --parts-tool
    if len(sys.argv) > 1 and sys.argv[1] == '--parts-tool':
        main_parts_tool()
    else:
        main_font_editor()

# ===== [MAIN-END] =====




