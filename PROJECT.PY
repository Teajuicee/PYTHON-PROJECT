"""
╔══════════════════════════════════════════════════════════════════╗
║          FASHION FIT — Clothing Size Converter                   ║
║          Converts sizes across 10 major fashion brands           ║
╚══════════════════════════════════════════════════════════════════╝

Requirements:  Python 3.7+  |  Only standard library (Tkinter)
Run:           python clothing_size_converter.py
"""

import tkinter as tk
from tkinter import ttk, font
import json

# ─────────────────────────────────────────────────────────────────
#  SIZE DATABASE
#  Each entry maps a brand+gender+category size label
#  to its real-world measurements (cm / EU size for shoes).
#  Measurements used per category:
#    Shirts / T-Shirts / Blazers / Suits → chest (cm)
#    Jeans                               → waist (cm)
#    Lowers (Joggers/Sweatpants)         → waist (cm)
#    Shoes                               → EU size (numeric)
# ─────────────────────────────────────────────────────────────────

SIZE_DB = {
    # ── MEN ──────────────────────────────────────────────────────
    "Men": {
        "Shirts": {
            "H&M":            {"XS": 84, "S": 88, "M": 96, "L": 104, "XL": 112, "XXL": 120},
            "Zara":           {"XS": 82, "S": 86, "M": 94, "L": 102, "XL": 110, "XXL": 118},
            "Nike":           {"XS": 83, "S": 88, "M": 96, "L": 104, "XL": 112, "XXL": 120},
            "Adidas":         {"XS": 82, "S": 87, "M": 95, "L": 103, "XL": 111, "XXL": 119},
            "Levi's":         {"XS": 84, "S": 89, "M": 97, "L": 105, "XL": 113, "XXL": 121},
            "Uniqlo":         {"XS": 80, "S": 84, "M": 92, "L": 100, "XL": 108, "XXL": 116},
            "Puma":           {"XS": 83, "S": 88, "M": 96, "L": 104, "XL": 112, "XXL": 120},
            "Tommy Hilfiger": {"XS": 85, "S": 90, "M": 98, "L": 106, "XL": 114, "XXL": 122},
            "Calvin Klein":   {"XS": 84, "S": 88, "M": 96, "L": 104, "XL": 112, "XXL": 120},
            "Ralph Lauren":   {"XS": 86, "S": 91, "M": 99, "L": 107, "XL": 115, "XXL": 123},
        },
        "T-Shirts": {
            "H&M":            {"XS": 82, "S": 88, "M": 96, "L": 104, "XL": 112, "XXL": 120},
            "Zara":           {"XS": 80, "S": 86, "M": 94, "L": 102, "XL": 110, "XXL": 118},
            "Nike":           {"XS": 83, "S": 88, "M": 96, "L": 104, "XL": 113, "XXL": 122},
            "Adidas":         {"XS": 82, "S": 87, "M": 95, "L": 103, "XL": 112, "XXL": 121},
            "Levi's":         {"XS": 84, "S": 89, "M": 97, "L": 105, "XL": 113, "XXL": 121},
            "Uniqlo":         {"XS": 80, "S": 84, "M": 92, "L": 100, "XL": 108, "XXL": 116},
            "Puma":           {"XS": 82, "S": 88, "M": 96, "L": 104, "XL": 112, "XXL": 120},
            "Tommy Hilfiger": {"XS": 84, "S": 90, "M": 98, "L": 106, "XL": 114, "XXL": 122},
            "Calvin Klein":   {"XS": 83, "S": 88, "M": 96, "L": 104, "XL": 112, "XXL": 120},
            "Ralph Lauren":   {"XS": 85, "S": 90, "M": 98, "L": 106, "XL": 114, "XXL": 122},
        },
        "Jeans": {
            "H&M":            {"28": 71, "30": 76, "32": 81, "34": 86, "36": 91, "38": 96},
            "Zara":           {"28": 72, "30": 77, "32": 82, "34": 87, "36": 92, "38": 97},
            "Nike":           {"28": 71, "30": 76, "32": 81, "34": 86, "36": 91, "38": 96},
            "Adidas":         {"28": 71, "30": 76, "32": 81, "34": 86, "36": 91, "38": 96},
            "Levi's":         {"28": 70, "30": 75, "32": 80, "34": 85, "36": 90, "38": 95},
            "Uniqlo":         {"28": 71, "30": 76, "32": 81, "34": 86, "36": 91, "38": 96},
            "Puma":           {"28": 71, "30": 76, "32": 81, "34": 86, "36": 91, "38": 96},
            "Tommy Hilfiger": {"28": 72, "30": 77, "32": 82, "34": 87, "36": 92, "38": 97},
            "Calvin Klein":   {"28": 71, "30": 76, "32": 81, "34": 86, "36": 91, "38": 96},
            "Ralph Lauren":   {"28": 73, "30": 78, "32": 83, "34": 88, "36": 93, "38": 98},
        },
        "Blazers": {
            "H&M":            {"46": 92, "48": 96, "50": 100, "52": 104, "54": 108, "56": 112},
            "Zara":           {"46": 90, "48": 94, "50": 98,  "52": 102, "54": 106, "56": 110},
            "Nike":           {"S": 90,  "M": 96,  "L": 102,  "XL": 108, "XXL": 114},
            "Adidas":         {"S": 90,  "M": 96,  "L": 102,  "XL": 108, "XXL": 114},
            "Levi's":         {"S": 91,  "M": 97,  "L": 103,  "XL": 109, "XXL": 115},
            "Uniqlo":         {"S": 88,  "M": 94,  "L": 100,  "XL": 106, "XXL": 112},
            "Puma":           {"S": 90,  "M": 96,  "L": 102,  "XL": 108, "XXL": 114},
            "Tommy Hilfiger": {"46": 92, "48": 96, "50": 100, "52": 104, "54": 108, "56": 112},
            "Calvin Klein":   {"46": 92, "48": 96, "50": 100, "52": 104, "54": 108, "56": 112},
            "Ralph Lauren":   {"46": 93, "48": 97, "50": 101, "52": 105, "54": 109, "56": 113},
        },
        "Suits": {
            "H&M":            {"46": 92, "48": 96, "50": 100, "52": 104, "54": 108, "56": 112},
            "Zara":           {"46": 91, "48": 95, "50": 99,  "52": 103, "54": 107, "56": 111},
            "Nike":           {"S": 90,  "M": 96,  "L": 102,  "XL": 108, "XXL": 114},
            "Adidas":         {"S": 90,  "M": 96,  "L": 102,  "XL": 108, "XXL": 114},
            "Levi's":         {"S": 91,  "M": 97,  "L": 103,  "XL": 109, "XXL": 115},
            "Uniqlo":         {"S": 88,  "M": 94,  "L": 100,  "XL": 106, "XXL": 112},
            "Puma":           {"S": 90,  "M": 96,  "L": 102,  "XL": 108, "XXL": 114},
            "Tommy Hilfiger": {"46": 92, "48": 96, "50": 100, "52": 104, "54": 108, "56": 112},
            "Calvin Klein":   {"46": 91, "48": 95, "50": 99,  "52": 103, "54": 107, "56": 111},
            "Ralph Lauren":   {"46": 93, "48": 97, "50": 101, "52": 105, "54": 109, "56": 113},
        },
        "Shoes": {
            # EU size → EU measurement value (used directly for comparison)
            "H&M":            {"40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46},
            "Zara":           {"40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46},
            "Nike":           {"40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46},
            "Adidas":         {"40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46},
            "Levi's":         {"40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46},
            "Uniqlo":         {"40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46},
            "Puma":           {"39": 39, "40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46},
            "Tommy Hilfiger": {"40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46},
            "Calvin Klein":   {"40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46},
            "Ralph Lauren":   {"40": 40, "41": 41, "42": 42, "43": 43, "44": 44, "45": 45, "46": 46},
        },
        "Lowers": {
            "H&M":            {"XS": 68, "S": 74, "M": 80, "L": 86, "XL": 94, "XXL": 102},
            "Zara":           {"XS": 67, "S": 73, "M": 79, "L": 85, "XL": 93, "XXL": 101},
            "Nike":           {"XS": 68, "S": 74, "M": 80, "L": 88, "XL": 96, "XXL": 104},
            "Adidas":         {"XS": 68, "S": 74, "M": 80, "L": 88, "XL": 96, "XXL": 104},
            "Levi's":         {"XS": 68, "S": 74, "M": 80, "L": 86, "XL": 94, "XXL": 102},
            "Uniqlo":         {"XS": 64, "S": 70, "M": 76, "L": 84, "XL": 92, "XXL": 100},
            "Puma":           {"XS": 68, "S": 74, "M": 80, "L": 88, "XL": 96, "XXL": 104},
            "Tommy Hilfiger": {"XS": 69, "S": 75, "M": 81, "L": 87, "XL": 95, "XXL": 103},
            "Calvin Klein":   {"XS": 68, "S": 74, "M": 80, "L": 86, "XL": 94, "XXL": 102},
            "Ralph Lauren":   {"XS": 70, "S": 76, "M": 82, "L": 88, "XL": 96, "XXL": 104},
        },
    },

    # ── WOMEN ────────────────────────────────────────────────────
    "Women": {
        "Shirts": {
            "H&M":            {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Zara":           {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Nike":           {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Adidas":         {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Levi's":         {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Uniqlo":         {"XS": 76, "S": 80, "M": 86, "L": 92,  "XL": 100, "XXL": 108},
            "Puma":           {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Tommy Hilfiger": {"XS": 81, "S": 85, "M": 91, "L": 97,  "XL": 105, "XXL": 113},
            "Calvin Klein":   {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Ralph Lauren":   {"XS": 82, "S": 86, "M": 92, "L": 98,  "XL": 106, "XXL": 114},
        },
        "T-Shirts": {
            "H&M":            {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Zara":           {"XS": 76, "S": 80, "M": 86, "L": 92,  "XL": 100, "XXL": 108},
            "Nike":           {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Adidas":         {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Levi's":         {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Uniqlo":         {"XS": 74, "S": 78, "M": 84, "L": 90,  "XL": 98,  "XXL": 106},
            "Puma":           {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Tommy Hilfiger": {"XS": 79, "S": 83, "M": 89, "L": 95,  "XL": 103, "XXL": 111},
            "Calvin Klein":   {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Ralph Lauren":   {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
        },
        "Jeans": {
            "H&M":            {"24": 60, "26": 64, "28": 70, "30": 76, "32": 82, "34": 88},
            "Zara":           {"24": 61, "26": 65, "28": 71, "30": 77, "32": 83, "34": 89},
            "Nike":           {"24": 60, "26": 64, "28": 70, "30": 76, "32": 82, "34": 88},
            "Adidas":         {"24": 60, "26": 64, "28": 70, "30": 76, "32": 82, "34": 88},
            "Levi's":         {"24": 59, "26": 63, "28": 69, "30": 75, "32": 81, "34": 87},
            "Uniqlo":         {"24": 60, "26": 64, "28": 70, "30": 76, "32": 82, "34": 88},
            "Puma":           {"24": 60, "26": 64, "28": 70, "30": 76, "32": 82, "34": 88},
            "Tommy Hilfiger": {"24": 61, "26": 65, "28": 71, "30": 77, "32": 83, "34": 89},
            "Calvin Klein":   {"24": 60, "26": 64, "28": 70, "30": 76, "32": 82, "34": 88},
            "Ralph Lauren":   {"24": 62, "26": 66, "28": 72, "30": 78, "32": 84, "34": 90},
        },
        "Blazers": {
            "H&M":            {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Zara":           {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Nike":           {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Adidas":         {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Levi's":         {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Uniqlo":         {"XS": 76, "S": 80, "M": 86, "L": 92,  "XL": 100, "XXL": 108},
            "Puma":           {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Tommy Hilfiger": {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Calvin Klein":   {"XS": 79, "S": 83, "M": 89, "L": 95,  "XL": 103, "XXL": 111},
            "Ralph Lauren":   {"XS": 81, "S": 85, "M": 91, "L": 97,  "XL": 105, "XXL": 113},
        },
        "Suits": {
            "H&M":            {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Zara":           {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Nike":           {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Adidas":         {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Levi's":         {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Uniqlo":         {"XS": 76, "S": 80, "M": 86, "L": 92,  "XL": 100, "XXL": 108},
            "Puma":           {"XS": 78, "S": 82, "M": 88, "L": 94,  "XL": 102, "XXL": 110},
            "Tommy Hilfiger": {"XS": 80, "S": 84, "M": 90, "L": 96,  "XL": 104, "XXL": 112},
            "Calvin Klein":   {"XS": 79, "S": 83, "M": 89, "L": 95,  "XL": 103, "XXL": 111},
            "Ralph Lauren":   {"XS": 81, "S": 85, "M": 91, "L": 97,  "XL": 105, "XXL": 113},
        },
        "Shoes": {
            "H&M":            {"36": 36, "37": 37, "38": 38, "39": 39, "40": 40, "41": 41, "42": 42},
            "Zara":           {"36": 36, "37": 37, "38": 38, "39": 39, "40": 40, "41": 41, "42": 42},
            "Nike":           {"36": 36, "37": 37, "38": 38, "38.5": 38.5, "39": 39, "40": 40, "41": 41},
            "Adidas":         {"36": 36, "37": 37, "38": 38, "39": 39, "40": 40, "41": 41, "42": 42},
            "Levi's":         {"36": 36, "37": 37, "38": 38, "39": 39, "40": 40, "41": 41, "42": 42},
            "Uniqlo":         {"36": 36, "37": 37, "38": 38, "39": 39, "40": 40, "41": 41},
            "Puma":           {"36": 36, "37": 37, "38": 38, "39": 39, "40": 40, "41": 41, "42": 42},
            "Tommy Hilfiger": {"36": 36, "37": 37, "38": 38, "39": 39, "40": 40, "41": 41, "42": 42},
            "Calvin Klein":   {"36": 36, "37": 37, "38": 38, "39": 39, "40": 40, "41": 41, "42": 42},
            "Ralph Lauren":   {"36": 36, "37": 37, "38": 38, "39": 39, "40": 40, "41": 41, "42": 42},
        },
        "Lowers": {
            "H&M":            {"XS": 58, "S": 64, "M": 70, "L": 78,  "XL": 86,  "XXL": 94},
            "Zara":           {"XS": 57, "S": 63, "M": 69, "L": 77,  "XL": 85,  "XXL": 93},
            "Nike":           {"XS": 58, "S": 64, "M": 70, "L": 78,  "XL": 86,  "XXL": 96},
            "Adidas":         {"XS": 58, "S": 64, "M": 70, "L": 78,  "XL": 86,  "XXL": 96},
            "Levi's":         {"XS": 58, "S": 64, "M": 70, "L": 78,  "XL": 86,  "XXL": 94},
            "Uniqlo":         {"XS": 54, "S": 60, "M": 66, "L": 74,  "XL": 82,  "XXL": 90},
            "Puma":           {"XS": 58, "S": 64, "M": 70, "L": 78,  "XL": 86,  "XXL": 96},
            "Tommy Hilfiger": {"XS": 59, "S": 65, "M": 71, "L": 79,  "XL": 87,  "XXL": 95},
            "Calvin Klein":   {"XS": 58, "S": 64, "M": 70, "L": 78,  "XL": 86,  "XXL": 94},
            "Ralph Lauren":   {"XS": 60, "S": 66, "M": 72, "L": 80,  "XL": 88,  "XXL": 96},
        },
    },

    # ── KIDS ─────────────────────────────────────────────────────
    "Kids": {
        "Shirts": {
            "H&M":            {"2Y": 54, "4Y": 58, "6Y": 62, "8Y": 68,  "10Y": 74, "12Y": 80},
            "Zara":           {"2Y": 53, "4Y": 57, "6Y": 61, "8Y": 67,  "10Y": 73, "12Y": 79},
            "Nike":           {"2Y": 54, "4Y": 58, "6Y": 62, "8Y": 68,  "10Y": 74, "12Y": 80},
            "Adidas":         {"2Y": 54, "4Y": 58, "6Y": 62, "8Y": 68,  "10Y": 74, "12Y": 80},
            "Levi's":         {"2Y": 54, "4Y": 58, "6Y": 62, "8Y": 68,  "10Y": 74, "12Y": 80},
            "Uniqlo":         {"2Y": 52, "4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78},
            "Puma":           {"2Y": 54, "4Y": 58, "6Y": 62, "8Y": 68,  "10Y": 74, "12Y": 80},
            "Tommy Hilfiger": {"2Y": 55, "4Y": 59, "6Y": 63, "8Y": 69,  "10Y": 75, "12Y": 81},
            "Calvin Klein":   {"2Y": 54, "4Y": 58, "6Y": 62, "8Y": 68,  "10Y": 74, "12Y": 80},
            "Ralph Lauren":   {"2Y": 55, "4Y": 59, "6Y": 63, "8Y": 69,  "10Y": 75, "12Y": 81},
        },
        "T-Shirts": {
            "H&M":            {"2Y": 52, "4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78},
            "Zara":           {"2Y": 51, "4Y": 55, "6Y": 59, "8Y": 65,  "10Y": 71, "12Y": 77},
            "Nike":           {"2Y": 52, "4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78},
            "Adidas":         {"2Y": 52, "4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78},
            "Levi's":         {"2Y": 52, "4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78},
            "Uniqlo":         {"2Y": 50, "4Y": 54, "6Y": 58, "8Y": 64,  "10Y": 70, "12Y": 76},
            "Puma":           {"2Y": 52, "4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78},
            "Tommy Hilfiger": {"2Y": 53, "4Y": 57, "6Y": 61, "8Y": 67,  "10Y": 73, "12Y": 79},
            "Calvin Klein":   {"2Y": 52, "4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78},
            "Ralph Lauren":   {"2Y": 53, "4Y": 57, "6Y": 61, "8Y": 67,  "10Y": 73, "12Y": 79},
        },
        "Jeans": {
            "H&M":            {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Zara":           {"2Y": 49, "4Y": 53, "6Y": 57, "8Y": 61,  "10Y": 67, "12Y": 73},
            "Nike":           {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Adidas":         {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Levi's":         {"2Y": 47, "4Y": 51, "6Y": 55, "8Y": 59,  "10Y": 65, "12Y": 71},
            "Uniqlo":         {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Puma":           {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Tommy Hilfiger": {"2Y": 49, "4Y": 53, "6Y": 57, "8Y": 61,  "10Y": 67, "12Y": 73},
            "Calvin Klein":   {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Ralph Lauren":   {"2Y": 50, "4Y": 54, "6Y": 58, "8Y": 62,  "10Y": 68, "12Y": 74},
        },
        "Blazers": {
            "H&M":            {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Zara":           {"4Y": 55, "6Y": 59, "8Y": 65,  "10Y": 71, "12Y": 77, "14Y": 83},
            "Nike":           {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Adidas":         {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Levi's":         {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Uniqlo":         {"4Y": 54, "6Y": 58, "8Y": 64,  "10Y": 70, "12Y": 76, "14Y": 82},
            "Puma":           {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Tommy Hilfiger": {"4Y": 57, "6Y": 61, "8Y": 67,  "10Y": 73, "12Y": 79, "14Y": 85},
            "Calvin Klein":   {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Ralph Lauren":   {"4Y": 57, "6Y": 61, "8Y": 67,  "10Y": 73, "12Y": 79, "14Y": 85},
        },
        "Suits": {
            "H&M":            {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Zara":           {"4Y": 55, "6Y": 59, "8Y": 65,  "10Y": 71, "12Y": 77, "14Y": 83},
            "Nike":           {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Adidas":         {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Levi's":         {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Uniqlo":         {"4Y": 54, "6Y": 58, "8Y": 64,  "10Y": 70, "12Y": 76, "14Y": 82},
            "Puma":           {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Tommy Hilfiger": {"4Y": 57, "6Y": 61, "8Y": 67,  "10Y": 73, "12Y": 79, "14Y": 85},
            "Calvin Klein":   {"4Y": 56, "6Y": 60, "8Y": 66,  "10Y": 72, "12Y": 78, "14Y": 84},
            "Ralph Lauren":   {"4Y": 57, "6Y": 61, "8Y": 67,  "10Y": 73, "12Y": 79, "14Y": 85},
        },
        "Shoes": {
            "H&M":            {"28": 28, "29": 29, "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35},
            "Zara":           {"28": 28, "29": 29, "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35},
            "Nike":           {"28": 28, "29": 29, "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35},
            "Adidas":         {"28": 28, "29": 29, "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35},
            "Levi's":         {"28": 28, "29": 29, "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35},
            "Uniqlo":         {"28": 28, "29": 29, "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35},
            "Puma":           {"27": 27, "28": 28, "29": 29, "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35},
            "Tommy Hilfiger": {"28": 28, "29": 29, "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35},
            "Calvin Klein":   {"28": 28, "29": 29, "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35},
            "Ralph Lauren":   {"28": 28, "29": 29, "30": 30, "31": 31, "32": 32, "33": 33, "34": 34, "35": 35},
        },
        "Lowers": {
            "H&M":            {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Zara":           {"2Y": 47, "4Y": 51, "6Y": 55, "8Y": 59,  "10Y": 65, "12Y": 71},
            "Nike":           {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Adidas":         {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Levi's":         {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Uniqlo":         {"2Y": 46, "4Y": 50, "6Y": 54, "8Y": 58,  "10Y": 64, "12Y": 70},
            "Puma":           {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Tommy Hilfiger": {"2Y": 49, "4Y": 53, "6Y": 57, "8Y": 61,  "10Y": 67, "12Y": 73},
            "Calvin Klein":   {"2Y": 48, "4Y": 52, "6Y": 56, "8Y": 60,  "10Y": 66, "12Y": 72},
            "Ralph Lauren":   {"2Y": 49, "4Y": 53, "6Y": 57, "8Y": 61,  "10Y": 67, "12Y": 73},
        },
    },
}

# ─────────────────────────────────────────────────────────────────
#  BRAND COLOUR PALETTE  (used to draw the logo placeholder)
# ─────────────────────────────────────────────────────────────────
BRAND_COLORS = {
    "H&M":            {"bg": "#E50010", "fg": "#FFFFFF"},   # Red
    "Zara":           {"bg": "#000000", "fg": "#FFFFFF"},   # Black
    "Nike":           {"bg": "#111111", "fg": "#FFFFFF"},   # Dark
    "Adidas":         {"bg": "#000000", "fg": "#FFFFFF"},   # Black
    "Levi's":         {"bg": "#C8102E", "fg": "#FFFFFF"},   # Red
    "Uniqlo":         {"bg": "#E60012", "fg": "#FFFFFF"},   # Red
    "Puma":           {"bg": "#D20A11", "fg": "#FFFFFF"},   # Red
    "Tommy Hilfiger": {"bg": "#C41230", "fg": "#FFFFFF"},   # Red/Navy
    "Calvin Klein":   {"bg": "#1A1A2E", "fg": "#FFFFFF"},   # Dark Navy
    "Ralph Lauren":   {"bg": "#002868", "fg": "#FFFFFF"},   # Navy Blue
}

ALL_BRANDS = list(BRAND_COLORS.keys())
CATEGORIES = ["Shirts", "T-Shirts", "Jeans", "Blazers", "Suits", "Shoes", "Lowers"]

# ─────────────────────────────────────────────────────────────────
#  CONVERSION LOGIC
# ─────────────────────────────────────────────────────────────────

def get_measurement(gender, category, brand, size_label):
    """Return the numeric measurement for a given brand/size or None."""
    try:
        return SIZE_DB[gender][category][brand][size_label]
    except KeyError:
        return None


def find_closest_size(target_measurement, brand_size_dict):
    """
    Given a target measurement and a {size_label: measurement} dict,
    return the size label whose measurement is closest to the target.
    Also return the delta (difference in cm / EU units).
    """
    best_label = None
    best_delta = float("inf")
    for label, meas in brand_size_dict.items():
        delta = abs(meas - target_measurement)
        if delta < best_delta:
            best_delta = delta
            best_label = label
    return best_label, best_delta


def convert_size(gender, category, source_brand, source_size):
    """
    Convert source_brand + source_size to equivalents in all other brands.
    Returns a list of dicts: [{brand, size, delta, fit_note}]
    """
    target_meas = get_measurement(gender, category, source_brand, source_size)
    if target_meas is None:
        return []

    results = []
    for brand in ALL_BRANDS:
        if brand == source_brand:
            continue
        brand_sizes = SIZE_DB.get(gender, {}).get(category, {}).get(brand)
        if not brand_sizes:
            continue
        closest, delta = find_closest_size(target_meas, brand_sizes)
        # Determine fit note based on delta
        if delta == 0:
            fit_note = "✅ Exact"
        elif delta <= 2:
            fit_note = "🟢 Very Close"
        elif delta <= 4:
            fit_note = "🟡 Close"
        else:
            fit_note = "🟠 Check fit"
        results.append({
            "brand":    brand,
            "size":     closest,
            "delta":    delta,
            "fit_note": fit_note,
        })
    return results


# ═════════════════════════════════════════════════════════════════
#  GUI APPLICATION
# ═════════════════════════════════════════════════════════════════

class FashionFitApp(tk.Tk):
    """Main application window for the Fashion Fit size converter."""

    # ── Colour palette ─────────────────────────────────────────
    DARK_BG     = "#0F0F1A"
    PANEL_BG    = "#1A1A2E"
    CARD_BG     = "#16213E"
    ACCENT      = "#E94560"
    ACCENT2     = "#0F3460"
    TEXT_LIGHT  = "#E0E0E0"
    TEXT_DIM    = "#888888"
    SUCCESS     = "#2ECC71"
    WARNING     = "#F39C12"
    DANGER      = "#E74C3C"

    def __init__(self):
        super().__init__()
        self.title("Fashion Fit — Clothing Size Converter")
        self.geometry("980x760")
        self.minsize(820, 680)
        self.configure(bg=self.DARK_BG)
        self.resizable(True, True)

        # Track current theme
        self.is_dark = True

        self._setup_styles()
        self._build_ui()

    # ── Style configuration ────────────────────────────────────
    def _setup_styles(self):
        """Configure ttk styles for dropdowns and other themed widgets."""
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TCombobox",
            fieldbackground=self.CARD_BG,
            background=self.CARD_BG,
            foreground=self.TEXT_LIGHT,
            selectbackground=self.ACCENT2,
            selectforeground=self.TEXT_LIGHT,
            borderwidth=0,
            relief="flat",
        )
        style.map("TCombobox",
            fieldbackground=[("readonly", self.CARD_BG)],
            foreground=[("readonly", self.TEXT_LIGHT)],
        )
        style.configure("Vertical.TScrollbar",
            background=self.PANEL_BG,
            troughcolor=self.DARK_BG,
            borderwidth=0,
        )

    # ── Main UI build ──────────────────────────────────────────
    def _build_ui(self):
        """Build all UI sections."""
        self._build_header()
        self._build_body()

    def _build_header(self):
        """Top header bar with title and theme toggle."""
        header = tk.Frame(self, bg=self.ACCENT, height=64)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # App icon / title
        tk.Label(
            header,
            text="👗  Fashion Fit",
            font=("Helvetica", 20, "bold"),
            bg=self.ACCENT,
            fg="#FFFFFF",
            padx=24,
        ).pack(side="left", pady=12)

        tk.Label(
            header,
            text="Smart Clothing Size Converter",
            font=("Helvetica", 11),
            bg=self.ACCENT,
            fg="#FFD0D8",
        ).pack(side="left", pady=12)

        # Theme toggle button
        self.theme_btn = tk.Button(
            header,
            text="☀  Light Mode",
            font=("Helvetica", 10),
            bg="#C0304D",
            fg="#FFFFFF",
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self._toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=20, pady=14)

    def _build_body(self):
        """Main body split into left (inputs) and right (results)."""
        body = tk.Frame(self, bg=self.DARK_BG)
        body.pack(fill="both", expand=True, padx=20, pady=16)

        # Left panel — input controls
        left = tk.Frame(body, bg=self.PANEL_BG, bd=0, relief="flat",
                        width=340)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)
        self._build_input_panel(left)

        # Right panel — results
        right = tk.Frame(body, bg=self.PANEL_BG, bd=0)
        right.pack(side="left", fill="both", expand=True)
        self._build_results_panel(right)

    # ── Left input panel ───────────────────────────────────────
    def _build_input_panel(self, parent):
        # Section title
        tk.Label(parent, text="⚙  Your Details",
                 font=("Helvetica", 13, "bold"),
                 bg=self.PANEL_BG, fg=self.ACCENT,
                 anchor="w").pack(fill="x", padx=18, pady=(18, 6))

        separator = tk.Frame(parent, bg=self.ACCENT, height=2)
        separator.pack(fill="x", padx=18, pady=(0, 14))

        # ── Gender ─────────────────────────────────────────────
        self._label(parent, "Gender")
        self.gender_var = tk.StringVar(value="Men")
        gender_frame = tk.Frame(parent, bg=self.PANEL_BG)
        gender_frame.pack(fill="x", padx=18, pady=(0, 12))
        for g in ("Men", "Women", "Kids"):
            btn = tk.Radiobutton(
                gender_frame,
                text=g,
                variable=self.gender_var,
                value=g,
                font=("Helvetica", 10),
                bg=self.PANEL_BG,
                fg=self.TEXT_LIGHT,
                selectcolor=self.ACCENT2,
                activebackground=self.PANEL_BG,
                activeforeground=self.TEXT_LIGHT,
                command=self._on_gender_change,
            )
            btn.pack(side="left", padx=(0, 10))

        # ── Source brand ───────────────────────────────────────
        self._label(parent, "Your Brand")
        self.brand_var = tk.StringVar(value=ALL_BRANDS[0])
        self.brand_combo = ttk.Combobox(
            parent,
            textvariable=self.brand_var,
            values=ALL_BRANDS,
            state="readonly",
            font=("Helvetica", 11),
        )
        self.brand_combo.pack(fill="x", padx=18, pady=(0, 14), ipady=6)
        self.brand_combo.bind("<<ComboboxSelected>>", self._on_brand_change)

        # ── Brand logo placeholder ─────────────────────────────
        self.logo_canvas = tk.Canvas(
            parent,
            bg=self.PANEL_BG,
            bd=0,
            highlightthickness=0,
            height=72,
        )
        self.logo_canvas.pack(fill="x", padx=18, pady=(0, 16))
        self._draw_logo(self.brand_var.get())

        # ── Category ───────────────────────────────────────────
        self._label(parent, "Category")
        self.cat_var = tk.StringVar(value=CATEGORIES[0])
        self.cat_combo = ttk.Combobox(
            parent,
            textvariable=self.cat_var,
            values=CATEGORIES,
            state="readonly",
            font=("Helvetica", 11),
        )
        self.cat_combo.pack(fill="x", padx=18, pady=(0, 14), ipady=6)
        self.cat_combo.bind("<<ComboboxSelected>>", self._update_size_options)

        # ── Size ───────────────────────────────────────────────
        self._label(parent, "Your Size")
        self.size_var = tk.StringVar()
        self.size_combo = ttk.Combobox(
            parent,
            textvariable=self.size_var,
            state="readonly",
            font=("Helvetica", 11),
        )
        self.size_combo.pack(fill="x", padx=18, pady=(0, 18), ipady=6)
        self._update_size_options()

        # ── Search/filter bar ──────────────────────────────────
        self._label(parent, "Filter Results by Brand")
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", self._apply_filter)
        filter_entry = tk.Entry(
            parent,
            textvariable=self.filter_var,
            font=("Helvetica", 11),
            bg=self.CARD_BG,
            fg=self.TEXT_LIGHT,
            insertbackground=self.TEXT_LIGHT,
            relief="flat",
            bd=6,
        )
        filter_entry.pack(fill="x", padx=18, pady=(0, 18), ipady=5)
        filter_entry.insert(0, "")

        # ── Convert button ─────────────────────────────────────
        convert_btn = tk.Button(
            parent,
            text="🔍  Convert Size",
            font=("Helvetica", 13, "bold"),
            bg=self.ACCENT,
            fg="#FFFFFF",
            activebackground="#C0304D",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=12,
            command=self._do_convert,
        )
        convert_btn.pack(fill="x", padx=18, pady=(0, 8))

        # ── Reset button ───────────────────────────────────────
        reset_btn = tk.Button(
            parent,
            text="↺  Reset",
            font=("Helvetica", 10),
            bg=self.CARD_BG,
            fg=self.TEXT_DIM,
            activebackground=self.PANEL_BG,
            activeforeground=self.TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self._reset,
        )
        reset_btn.pack(fill="x", padx=18, pady=(0, 18))

    # ── Right results panel ────────────────────────────────────
    def _build_results_panel(self, parent):
        # Panel title row
        title_row = tk.Frame(parent, bg=self.PANEL_BG)
        title_row.pack(fill="x", padx=18, pady=(18, 6))

        tk.Label(title_row, text="📊  Conversion Results",
                 font=("Helvetica", 13, "bold"),
                 bg=self.PANEL_BG, fg=self.ACCENT,
                 anchor="w").pack(side="left")

        self.result_count_lbl = tk.Label(
            title_row,
            text="",
            font=("Helvetica", 10),
            bg=self.PANEL_BG,
            fg=self.TEXT_DIM,
        )
        self.result_count_lbl.pack(side="right")

        separator = tk.Frame(parent, bg=self.ACCENT, height=2)
        separator.pack(fill="x", padx=18, pady=(0, 10))

        # ── Summary bar (shown after conversion) ───────────────
        self.summary_frame = tk.Frame(parent, bg=self.CARD_BG)
        self.summary_lbl = tk.Label(
            self.summary_frame,
            text="",
            font=("Helvetica", 11),
            bg=self.CARD_BG,
            fg=self.TEXT_LIGHT,
            anchor="w",
            padx=14,
            pady=10,
            wraplength=560,
            justify="left",
        )
        self.summary_lbl.pack(fill="x")

        # ── Scrollable results area ────────────────────────────
        results_outer = tk.Frame(parent, bg=self.PANEL_BG)
        results_outer.pack(fill="both", expand=True, padx=18, pady=(0, 14))

        # Canvas + scrollbar for scrollable list
        self.result_canvas = tk.Canvas(
            results_outer,
            bg=self.PANEL_BG,
            bd=0,
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            results_outer,
            orient="vertical",
            command=self.result_canvas.yview,
        )
        self.result_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.result_canvas.pack(side="left", fill="both", expand=True)

        # Inner frame inside canvas
        self.result_inner = tk.Frame(self.result_canvas, bg=self.PANEL_BG)
        self.result_canvas_window = self.result_canvas.create_window(
            (0, 0), window=self.result_inner, anchor="nw"
        )

        # Bind resizing
        self.result_inner.bind("<Configure>", self._on_frame_configure)
        self.result_canvas.bind("<Configure>", self._on_canvas_configure)

        # Mouse wheel scrolling
        self.result_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Placeholder text
        self._show_placeholder()

        # Store last results for filter
        self._last_results = []
        self._last_source_info = {}

    # ── Helpers ─────────────────────────────────────────────────
    def _label(self, parent, text):
        """Small section label."""
        tk.Label(
            parent,
            text=text.upper(),
            font=("Helvetica", 8, "bold"),
            bg=self.PANEL_BG,
            fg=self.TEXT_DIM,
            anchor="w",
        ).pack(fill="x", padx=18, pady=(0, 4))

    def _draw_logo(self, brand_name):
        """Draw a colourful brand logo placeholder on the canvas."""
        self.logo_canvas.delete("all")
        colors = BRAND_COLORS.get(brand_name, {"bg": "#444", "fg": "#FFF"})
        w = self.logo_canvas.winfo_reqwidth()
        if w < 10:
            w = 300   # fallback before window renders

        # Background pill
        self.logo_canvas.create_rectangle(
            0, 4, w, 68,
            fill=colors["bg"],
            outline="",
        )
        # Brand initials or short name
        short = brand_name if len(brand_name) <= 12 else brand_name[:10] + "…"
        self.logo_canvas.create_text(
            w // 2, 36,
            text=short,
            font=("Helvetica", 16, "bold"),
            fill=colors["fg"],
        )

    def _show_placeholder(self):
        """Show an instructional message before first conversion."""
        for w in self.result_inner.winfo_children():
            w.destroy()
        tk.Label(
            self.result_inner,
            text=(
                "\n\n"
                "👆  Select your brand, category,\n"
                "and size, then press\n\n"
                "🔍  Convert Size\n\n"
                "to see equivalent sizes\nacross all other brands."
            ),
            font=("Helvetica", 13),
            bg=self.PANEL_BG,
            fg=self.TEXT_DIM,
            justify="center",
        ).pack(pady=40, padx=20)

    def _update_size_options(self, event=None):
        """Refresh size dropdown based on selected gender/brand/category."""
        gender   = self.gender_var.get()
        brand    = self.brand_var.get()
        category = self.cat_var.get()
        sizes = list(
            SIZE_DB.get(gender, {}).get(category, {}).get(brand, {}).keys()
        )
        self.size_combo["values"] = sizes
        if sizes:
            self.size_var.set(sizes[0])
        else:
            self.size_var.set("")

    def _on_brand_change(self, event=None):
        self._draw_logo(self.brand_var.get())
        self._update_size_options()

    def _on_gender_change(self):
        self._update_size_options()

    # ── Conversion action ──────────────────────────────────────
    def _do_convert(self):
        gender   = self.gender_var.get()
        brand    = self.brand_var.get()
        category = self.cat_var.get()
        size     = self.size_var.get()

        if not size:
            self._show_error("Please select a valid size.")
            return

        results = convert_size(gender, category, brand, size)
        if not results:
            self._show_error("No conversion data found.")
            return

        self._last_results = results
        self._last_source_info = {
            "gender": gender, "brand": brand,
            "category": category, "size": size,
        }

        self._render_results(results, brand, size, gender, category)

    def _apply_filter(self, *args):
        """Re-render results filtered by brand search term."""
        if not self._last_results:
            return
        term = self.filter_var.get().strip().lower()
        filtered = [
            r for r in self._last_results
            if term in r["brand"].lower()
        ] if term else self._last_results
        self._render_results(
            filtered,
            self._last_source_info.get("brand", ""),
            self._last_source_info.get("size", ""),
            self._last_source_info.get("gender", ""),
            self._last_source_info.get("category", ""),
        )

    def _render_results(self, results, source_brand, source_size,
                        gender, category):
        """Render result cards into the scrollable area."""
        # Clear old content
        for w in self.result_inner.winfo_children():
            w.destroy()

        # Update count label
        self.result_count_lbl.config(
            text=f"{len(results)} brand(s) shown"
        )

        # Summary bar
        measure_val = get_measurement(gender, category, source_brand, source_size)
        measure_label = "EU" if category == "Shoes" else "cm"
        self.summary_frame.pack(fill="x", padx=18, pady=(0, 12))
        self.summary_lbl.config(
            text=(
                f"Source:  {gender} › {category}  |  "
                f"{source_brand}  ›  Size {source_size}"
                + (f"  (≈ {measure_val} {measure_label})" if measure_val else "")
            )
        )

        if not results:
            tk.Label(
                self.result_inner,
                text="No brands match your filter.",
                font=("Helvetica", 12),
                bg=self.PANEL_BG,
                fg=self.TEXT_DIM,
            ).pack(pady=30)
            return

        # Table header
        header_frame = tk.Frame(self.result_inner, bg=self.ACCENT2)
        header_frame.pack(fill="x", pady=(0, 2))
        for col_text, w in [
            ("Brand", 220), ("Size", 100), ("Fit", 140), ("Δ cm / EU", 100)
        ]:
            tk.Label(
                header_frame,
                text=col_text,
                font=("Helvetica", 9, "bold"),
                bg=self.ACCENT2,
                fg=self.TEXT_LIGHT,
                width=w // 9,
                anchor="w",
            ).pack(side="left", padx=10, pady=6)

        # Result rows
        for i, row in enumerate(results):
            self._result_row(row, i)

    def _result_row(self, row, index):
        """Render a single result row card."""
        bg = self.CARD_BG if index % 2 == 0 else self.PANEL_BG
        brand_color = BRAND_COLORS.get(row["brand"], {}).get("bg", "#333")

        row_frame = tk.Frame(self.result_inner, bg=bg)
        row_frame.pack(fill="x", pady=1)

        # Coloured brand stripe
        stripe = tk.Frame(row_frame, bg=brand_color, width=5)
        stripe.pack(side="left", fill="y")

        # Brand logo mini badge
        badge = tk.Canvas(row_frame, bg=brand_color,
                          width=40, height=38, bd=0,
                          highlightthickness=0)
        badge.pack(side="left", padx=(6, 0))
        initials = "".join(w[0] for w in row["brand"].split()[:2]).upper()
        badge.create_text(
            20, 19,
            text=initials,
            font=("Helvetica", 10, "bold"),
            fill=BRAND_COLORS.get(row["brand"], {}).get("fg", "#FFF"),
        )

        # Brand name
        tk.Label(
            row_frame,
            text=row["brand"],
            font=("Helvetica", 11, "bold"),
            bg=bg,
            fg=self.TEXT_LIGHT,
            width=16,
            anchor="w",
        ).pack(side="left", padx=(8, 0))

        # Size label
        tk.Label(
            row_frame,
            text=row["size"],
            font=("Helvetica", 14, "bold"),
            bg=bg,
            fg=self.ACCENT,
            width=6,
            anchor="center",
        ).pack(side="left", padx=8)

        # Fit note
        fit_colors = {
            "✅ Exact":       self.SUCCESS,
            "🟢 Very Close":  "#27AE60",
            "🟡 Close":       self.WARNING,
            "🟠 Check fit":   self.DANGER,
        }
        fit_color = fit_colors.get(row["fit_note"], self.TEXT_DIM)
        tk.Label(
            row_frame,
            text=row["fit_note"],
            font=("Helvetica", 10),
            bg=bg,
            fg=fit_color,
            width=14,
            anchor="w",
        ).pack(side="left", padx=4)

        # Delta
        delta_text = f"±{row['delta']} {'EU' if row['delta'] == int(row['delta']) else ''}"
        tk.Label(
            row_frame,
            text=f"±{row['delta']}",
            font=("Helvetica", 10),
            bg=bg,
            fg=self.TEXT_DIM,
        ).pack(side="left", padx=8)

    def _show_error(self, message):
        """Show an error message in the results area."""
        for w in self.result_inner.winfo_children():
            w.destroy()
        tk.Label(
            self.result_inner,
            text=f"⚠  {message}",
            font=("Helvetica", 12),
            bg=self.PANEL_BG,
            fg=self.DANGER,
            pady=20,
        ).pack()

    def _reset(self):
        """Reset all inputs and clear results."""
        self.gender_var.set("Men")
        self.brand_var.set(ALL_BRANDS[0])
        self.cat_var.set(CATEGORIES[0])
        self.filter_var.set("")
        self._update_size_options()
        self._draw_logo(ALL_BRANDS[0])
        self._last_results = []
        self._last_source_info = {}
        self.summary_frame.pack_forget()
        self.result_count_lbl.config(text="")
        self._show_placeholder()

    # ── Theme toggle ───────────────────────────────────────────
    def _toggle_theme(self):
        """Switch between dark and light colour schemes."""
        if self.is_dark:
            # Switch to light
            self.DARK_BG   = "#F5F5F5"
            self.PANEL_BG  = "#FFFFFF"
            self.CARD_BG   = "#F0F0F0"
            self.TEXT_LIGHT = "#1A1A1A"
            self.TEXT_DIM  = "#666666"
            self.theme_btn.config(text="🌙  Dark Mode", bg="#B0203D")
        else:
            # Switch to dark
            self.DARK_BG   = "#0F0F1A"
            self.PANEL_BG  = "#1A1A2E"
            self.CARD_BG   = "#16213E"
            self.TEXT_LIGHT = "#E0E0E0"
            self.TEXT_DIM  = "#888888"
            self.theme_btn.config(text="☀  Light Mode", bg="#C0304D")

        self.is_dark = not self.is_dark
        self.configure(bg=self.DARK_BG)

        # Rebuild to apply theme — simplest approach for Tkinter
        for widget in self.winfo_children():
            widget.destroy()
        self._setup_styles()
        self._build_ui()

    # ── Canvas / scroll helpers ────────────────────────────────
    def _on_frame_configure(self, event):
        self.result_canvas.configure(
            scrollregion=self.result_canvas.bbox("all")
        )

    def _on_canvas_configure(self, event):
        self.result_canvas.itemconfig(
            self.result_canvas_window, width=event.width
        )

    def _on_mousewheel(self, event):
        self.result_canvas.yview_scroll(-1 * (event.delta // 120), "units")


# ─────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = FashionFitApp()
    app.mainloop()