#!/usr/bin/env python3
"""
Comprehensive migration script for GitBook hint blocks and sc-knowledge terminology calibration.
"""

import os
import re
import sys
from pathlib import Path

STYLE_MAP = {
    "NOTE": "info",
    "TIP": "info",
    "IMPORTANT": "warning",
    "WARNING": "warning",
    "CAUTION": "danger",
}

def convert_hints(content: str) -> str:
    lines = content.split("\n")
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^\s*>\s*\\?\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\](.*)$", line, re.IGNORECASE)
        if m:
            alert_type = m.group(1).upper()
            style = STYLE_MAP[alert_type]
            inline = m.group(2).strip()
            block_content = []
            if inline:
                block_content.append(inline)
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith(">") and not re.match(r"^\s*>\s*\\?\[!", lines[j]):
                l = lines[j].strip()
                if l.startswith("> "):
                    block_content.append(l[2:])
                elif l.startswith(">"):
                    block_content.append(l[1:].strip())
                j += 1
            
            # Ensure preceding empty line if needed
            if new_lines and new_lines[-1].strip() != "":
                new_lines.append("")
            
            new_lines.append(f'{{% hint style="{style}" %}}')
            for bl in block_content:
                new_lines.append(bl)
            new_lines.append("{% endhint %}")
            
            # If next line is not empty and not end of file, ensure empty line
            if j < len(lines) and lines[j].strip() != "":
                new_lines.append("")
                
            i = j
        else:
            new_lines.append(line)
            i += 1
    return "\n".join(new_lines)


def apply_terminology(text: str) -> str:
    # Preserving HTML comments
    comment_pattern = re.compile(r"(<!--.*?-->)", re.DOTALL)
    parts = comment_pattern.split(text)
    for idx in range(0, len(parts), 2):
        s = parts[idx]
        
        # 1. Drake
        s = s.replace("德拉克工業", "德雷克星際")
        s = re.sub(r"德拉克(?!沃斯)", "德雷克星際", s)
        
        # 2. RSI
        s = s.replace("羅伯茨太空工業", "羅伯茲太空工業")
        
        # 3. StarEngine
        s = s.replace("星辰引擎", "星際引擎")
        
        # 4. Starchitect
        s = s.replace("星辰建築師", "星際建築系統")
        
        # 5. Ruin Station
        s = s.replace("毀滅空間站", "廢墟太空站")
        
        # 6. Aaron Halo
        s = s.replace("阿隆光環", "亞倫環")
        
        # 7. United Wayfarers Club
        s = s.replace("聯合開路者公會", "旅者聯合俱樂部")
        s = s.replace("聯合開路者俱樂部", "旅者聯合俱樂部")
        
        # 8. Klescher
        s = s.replace("克萊雪自動化改造監獄", "克萊舍爾勞教所")
        s = s.replace("克萊雪監獄", "克萊舍爾勞教所")
        s = s.replace("克萊雪", "克萊舍爾")
        
        # 9. Stanton
        s = s.replace("史丹頓", "斯坦頓")
        
        # 10. Vulture
        s = s.replace("禿鷹 (Vulture)", "禿鷲 (Vulture)")
        s = s.replace("Drake Vulture (禿鷹)", "Drake Vulture (禿鷲)")
        
        # 11. Cambio-SRT
        s = s.replace("修復配件 (Cambio-SRT)", "坎比奧 打撈修復工具 (Cambio-SRT)")
        s = s.replace("Cambio-SRT 修復配件", "坎比奧 打撈修復工具 (Cambio-SRT)")
        
        # 12. Railen
        s = s.replace("蓋圖 瑞靈 (Railen)", "蓋圖 瑞倫 (Railen)")
        s = s.replace("瑞靈 (Railen)", "瑞倫 (Railen)")
        
        # 13. Command Module
        s = s.replace("指令模組 (Command Module)", "指揮模組 (Command Module)")
        s = s.replace("### 指令模組", "### 指揮模組")
        
        # 14. MedGel
        s = s.replace("醫療生物凝膠", "醫療凝膠")
        s = s.replace("MedGel 生物凝膠", "MedGel 醫療凝膠")
        
        # 15. Life Support
        s = s.replace("生命維持系統 (Life Support)", "維生系統 (Life Support)")
        s = s.replace("生命維持系統", "維生系統")
        
        # 16. Foundation Festival
        s = s.replace("基礎節 (Foundation Festival)", "奠基節 (Foundation Festival)")
        s = s.replace("基礎節", "奠基節")
        
        # 17. Coramor
        s = s.replace("寇拉莫 (Coramor)", "科拉情人節 (Coramor)")
        s = s.replace("寇拉莫", "科拉情人節")
        
        # 18. Luminalia
        s = s.replace("光明節", "光燈節")
        
        # 19. InterSec
        s = s.replace("互安防務", "互安防衛")
        
        # 20. Northrock
        s = s.replace("北岩服務集團", "北境之巖服務團隊")
        
        # 21. Eckhart
        s = s.replace("埃克哈特保安", "埃克哈特保全")
        
        # 22. ASD
        s = s.replace("聯合科學與發展公司 (Associates Science & Development, ASD)", "聯科發 (Associates Science & Development, ASD)")
        s = s.replace("聯合科學與發展公司 (ASD)", "聯科發 (ASD)")
        s = s.replace("聯合科學發展部 (ASD)", "聯科發 (ASD)")
        s = s.replace("先進系統部 (ASD)", "聯科發 (ASD)")
        s = s.replace("先進系統部", "聯科發")
        s = s.replace("聯合科學與發展公司", "聯科發")
        s = s.replace("聯合科學發展部", "聯科發")
        
        # 23. Covalex
        s = s.replace("科瓦萊什物流", "科瓦萊什貨運")
        s = s.replace("科瓦萊什 (Covalex Shipping)", "科瓦萊什貨運 (Covalex Shipping)")
        
        # 24. Keeger Belt
        s = s.replace("基格帶 (Keeger Belt)", "基格小行星帶 (Keeger Belt)")
        s = s.replace("基格帶", "基格小行星帶")
        
        # 25. QV Breaker Station
        s = s.replace("QV 拆解站", "QV 碎岩站")
        s = s.replace("QV拆解站", "QV 碎岩站")
        
        # 26. Master Modes
        s = s.replace("SCM (戰鬥機動)", "SCM (戰鬥操控模式)")
        s = s.replace("NAV (極速導航)", "NAV (巡航導航模式)")
        s = s.replace("SCM 戰鬥模式 (Speed Combat Maneuvers)", "SCM 戰鬥操控模式 (Standard Control Mode)")
        s = s.replace("NAV 導航模式 (Navigation Mode)", "NAV 巡航導航模式 (Navigation Mode)")
        
        # 27. XenoThreat
        s = re.sub(r"(?<!異種威脅\s)(?<!異種威脅\()(?<!異種威脅)XenoThreat(?!\))", "異種威脅 (XenoThreat)", s)
        
        parts[idx] = s
        
    return "".join(parts)


def main():
    dry_run = "--dry-run" in sys.argv
    repo_root = Path(__file__).resolve().parent.parent
    
    md_files = [p for p in repo_root.glob("**/*.md") if ".git" not in p.parts]
    modified_count = 0
    total_hints = 0
    
    for p in sorted(md_files):
        orig = p.read_text(encoding="utf-8")
        step1 = convert_hints(orig)
        step2 = apply_terminology(step1)
        
        hints_in_file = step2.count('{% hint')
        total_hints += hints_in_file
        
        if step2 != orig:
            modified_count += 1
            if not dry_run:
                p.write_text(step2, encoding="utf-8")
                print(f"Updated: {p.relative_to(repo_root)}")
            else:
                print(f"[DRY-RUN] Would update: {p.relative_to(repo_root)}")
                
    print(f"\nDone! Processed {len(md_files)} files. Modified {modified_count} files. Total hints: {total_hints}.")

if __name__ == "__main__":
    main()
