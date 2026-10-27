#!/usr/bin/env python3
"""
Estimate Reddit post creation date from the post ID prefix.
Reddit post IDs are sequential base36-encoded IDs. Calibrated using
known post dates (sknd9g = Feb 2022, 1bmz5ej = March 2024, 1rp5yuv = Feb 2025).
"""
def pid_to_approx_year_month(post_id):
    if not post_id:
        return "unknown"
    p = post_id.lower()
    # 7-char IDs starting with '1' — the second char maps roughly to the year
    if len(p) == 7 and p[0] == '1':
        c = p[1]
        # Calibration:
        #   '0' = late 2022
        #   '1','2','3' = 2023
        #   '4','5','6','7','8','9' = 2023-2024
        #   'a','b','c' = early 2024
        #   'd','e','f','g','h' = mid 2024
        #   'i','j','k','l' = late 2024
        #   'm','n','o','p','q','r' = 2025
        #   's','t','u','v','w','x','y','z' = late 2025-2026
        if c in ('0', '1', '2', '3'):
            return "2023 (est.)"
        if c in ('4', '5', '6', '7'):
            return "2023-Q4 (est.)"
        if c in ('8', '9'):
            return "2024-Q1 (est.)"
        if c in ('a', 'b', 'c'):
            return "2024-Q1/Q2 (est.)"
        if c in ('d', 'e', 'f', 'g', 'h'):
            return "2024-Q2/Q3 (est.)"
        if c in ('i', 'j', 'k', 'l'):
            return "2024-Q4 (est.)"
        if c in ('m', 'n', 'o', 'p', 'q', 'r'):
            return "2025-Q1/Q2 (est.)"
        if c in ('s', 't', 'u', 'v'):
            return "2025-Q3/Q4 (est.)"
        if c in ('w', 'x', 'y', 'z'):
            return "2026 (est.)"
    # 6-char IDs are older (pre-2022)
    if len(p) == 6:
        c0 = p[0]
        if c0 in ('s', 't'):
            return "2022 (est.)"
        if c0 in ('u', 'v', 'w', 'x'):
            return "2021 (est.)"
        if c0 in ('y', 'z'):
            return "2020 (est.)"
        return "pre-2022 (est.)"
    # 5-char or shorter = very old (2015-2020)
    if len(p) <= 5:
        return "pre-2022 (very old)"
    # Fallback
    return f"unknown ({p[:4]}...)"

if __name__ == "__main__":
    import sys
    for pid in sys.argv[1:]:
        print(f"{pid:12s} -> {pid_to_approx_year_month(pid)}")
