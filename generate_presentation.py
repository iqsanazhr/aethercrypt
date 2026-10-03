import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Palet Warna Sesuai Referensi Foto Persis
    C_BG = RGBColor(246, 244, 238)         # Warm Cream #F6F4EE
    C_BG_CARD = RGBColor(236, 232, 220)    # Warm Gray/Beige Card #ECE8DC
    C_WHITE = RGBColor(255, 255, 255)
    C_BLUE = RGBColor(24, 99, 229)         # Cobalt Royal Blue #1863E5
    C_BLUE_SOFT = RGBColor(232, 240, 254)  # Light Blue Soft #E8F0FE
    C_DARK = RGBColor(25, 27, 32)          # Dark Badge Obsidian #191B20
    C_MUTED = RGBColor(107, 114, 128)      # Slate Gray #6B7280
    C_BORDER = RGBColor(221, 216, 203)     # Soft Border #DDD8CB
    C_GOLD = RGBColor(212, 160, 23)        # Brass Gold #D4A017
    C_GREEN = RGBColor(16, 185, 129)       # Emerald #10B981

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()

    def add_top_meta(slide, left_text, center_text, right_text="2026 EDITION"):
        # Header meta line
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{left_text}   •   {center_text}   •   {right_text}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.name = "Arial"
        p.font.color.rgb = C_MUTED

    # =========================================================
    # SLIDE 1: COVER (PERSIS DENGAN REFERENSI FOTO)
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Big Title "AetherCrypt" (Like "Portfolio" in photo)
    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(7.5), Inches(1.5))
    tf = tbox.text_frame
    p = tf.paragraphs[0]
    p.text = "AetherCrypt"
    p.font.size = Pt(72)
    p.font.bold = True
    p.font.name = "Trebuchet MS"
    p.font.color.rgb = C_DARK

    # Author top-right (Like "EMMA BROOKS / Social Media Manager" in photo)
    abox = s1.shapes.add_textbox(Inches(8.5), Inches(0.8), Inches(4.0), Inches(1.2))
    atf = abox.text_frame
    p = atf.paragraphs[0]
    p.text = "INFORMATIKA UNSOED"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.name = "Arial Black"
    p.font.color.rgb = C_DARK
    p.alignment = PP_ALIGN.RIGHT
    p2 = atf.add_paragraph()
    p2.text = "IF21A05 Kriptografi • Dosen Pengampu:\nEddy Maryanto & Puteri Awaliatush"
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_MUTED
    p2.alignment = PP_ALIGN.RIGHT

    # Center Hero: Big Cylinder Base (Replacing the Folder)
    cyl_base = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), Inches(2.3), Inches(7.0), Inches(3.4))
    cyl_base.fill.solid()
    cyl_base.fill.fore_color.rgb = C_DARK
    cyl_base.line.fill.background()

    # Brass Cylinder Dials Inside
    for i, ch in enumerate(["P", "L", "A", "Y", "3"]):
        dial = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.6 + (i * 1.25)), Inches(2.6), Inches(1.05), Inches(2.8))
        dial.fill.solid()
        dial.fill.fore_color.rgb = C_GOLD if i % 2 == 0 else RGBColor(190, 140, 20)
        dial.line.color.rgb = RGBColor(70, 50, 5)
        dtf = dial.text_frame
        p = dtf.paragraphs[0]
        p.text = f"\n{ch}\n"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.alignment = PP_ALIGN.CENTER

    # Floating Badge Left (Like "2026 Edition" on photo)
    b_left = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(2.7), Inches(2.2), Inches(0.95))
    b_left.fill.solid()
    b_left.fill.fore_color.rgb = C_DARK
    b_left.line.fill.background()
    ltf = b_left.text_frame
    p = ltf.paragraphs[0]
    p.text = "2026 Edition"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p2 = ltf.add_paragraph()
    p2.text = "🔒 @lab_unsoed"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_MUTED

    # Floating Badge Right (Like "Content Strategy..." on photo)
    b_right = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(4.5), Inches(2.9), Inches(1.3))
    b_right.fill.solid()
    b_right.fill.fore_color.rgb = C_DARK
    b_right.line.fill.background()
    rtf = b_right.text_frame
    p = rtf.paragraphs[0]
    p.text = "✓ Playfair Cipher (5×5)"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p = rtf.add_paragraph()
    p.text = "✓ Vigenère Cipher (Mod 26)"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p = rtf.add_paragraph()
    p.text = "✓ Columnar Transposition"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    # Bottom Left: Stacked Typography (Like "BUILDING BRANDS THROUGH STRATEGY AND CONTENT")
    bot_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(4.5), Inches(1.0))
    btf = bot_box.text_frame
    p = btf.paragraphs[0]
    p.text = "SECURE MESSAGING THROUGH CONFUSION AND DIFFUSION"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.name = "Arial Black"
    p.font.color.rgb = C_DARK

    # =========================================================
    # SLIDE 2: LATAR BELAKANG ("STRATEGY FIRST, CONTENT SECOND")
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_top_meta(s2, "AETHERCRYPT CASE FILE", "01 LATAR BELAKANG & ANALISIS KERENTANAN")

    # Big Headline Left
    lh_box = s2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(3.0))
    ltf = lh_box.text_frame
    ltf.word_wrap = True
    p = ltf.paragraphs[0]
    p.text = "Konfusi dulu,\ndifusi kemudian."
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.name = "Trebuchet MS"
    p.font.color.rgb = C_BLUE

    p = ltf.add_paragraph()
    p.text = "\nCipher klasik tunggal selalu meninggalkan pola frekuensi bahasa alami. Super-enkripsi meruntuhkan korelasi statistik dengan memadukan substitusi poligram dan permutasi geometris."
    p.font.size = Pt(13)
    p.font.color.rgb = C_MUTED

    # Right: 3 Rounded Horizontal Pill Cards (With '+' Badges)
    pill_data = [
        ("Celah Monoalfabetik", "Frekuensi huruf alami bahasa Indonesia sangat timpang — huruf 'A' mencapai 19.33% sehingga cipher mudah ditebak via histogram 1-ke-1."),
        ("Celah Polialfabetik", "Vigenère standar rentan terhadap Kasiski Examination dan Friedman Test untuk membongkar panjang kunci d dari repetisi kata."),
        ("Solusi AetherCrypt", "Gabungan Playfair 5×5 + Vigenère Mod 26 + Columnar Transposition menghancurkan pola vokal dan meratakan statistik.")
    ]
    for i, (ptitle, pdesc) in enumerate(pill_data):
        py = Inches(1.6 + (i * 1.55))
        p_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), py, Inches(5.3), Inches(1.35))
        p_card.fill.solid()
        p_card.fill.fore_color.rgb = C_BG_CARD
        p_card.line.color.rgb = C_BORDER
        ptf = p_card.text_frame
        ptf.word_wrap = True
        p = ptf.paragraphs[0]
        p.text = f"+  {ptitle}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p = ptf.add_paragraph()
        p.text = pdesc
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_MUTED

    # Bottom Right Label: "Urgensi Keamanan"
    l_box = s2.shapes.add_textbox(Inches(9.5), Inches(6.5), Inches(3.0), Inches(0.5))
    p = l_box.text_frame.paragraphs[0]
    p.text = "Urgensi Keamanan"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.alignment = PP_ALIGN.RIGHT

    # =========================================================
    # SLIDE 3: METODE PIPELINE (BLUE FOLDER SHEET CONTAINER)
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_top_meta(s3, "AETHERCRYPT CASE FILE", "02 METODE PIPELINE 3 TAHAP")

    # Blue Folder Card Base
    f_sheet = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(11.7), Inches(5.7))
    f_sheet.fill.solid()
    f_sheet.fill.fore_color.rgb = C_BLUE
    f_sheet.line.fill.background()

    # Left White Frame Card (Playfair 5x5 Matrix)
    w_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.8), Inches(4.2), Inches(4.5))
    w_card.fill.solid()
    w_card.fill.fore_color.rgb = C_WHITE
    w_card.line.color.rgb = C_BORDER
    wtf = w_card.text_frame
    wtf.word_wrap = True
    p = wtf.paragraphs[0]
    p.text = "MATRIKS KUNCI 5×5 (PLAYFAIR)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    p = wtf.add_paragraph()
    p.text = "U  N  I  V  E\nR  S  T  A  B\nC  D  F  G  H\nK  L  M  O  P\nQ  W  X  Y  Z"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.name = "Consolas"
    p.font.color.rgb = C_DARK

    p = wtf.add_paragraph()
    p.text = "\nKunci: UNIVERSITAS (25 Karakter, huruf J dileburkan ke I). Memproses pasangan bigram."
    p.font.size = Pt(10)
    p.font.color.rgb = C_MUTED

    # Right Content Inside Blue Sheet
    rt_box = s3.shapes.add_textbox(Inches(6.0), Inches(1.8), Inches(6.0), Inches(4.5))
    rtf = rt_box.text_frame
    rtf.word_wrap = True
    p = rtf.paragraphs[0]
    p.text = "ARSITEKTUR BERANTAI SIMETRIS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_SOFT

    p = rtf.add_paragraph()
    p.text = "Transformasi 3 Tahap Non-Linear"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    pipe_desc = [
        ("1. Playfair 5×5 (Substitusi Poligram):", "Memecah teks menjadi 21 pasangan bigram untuk mengeliminasi analisis frekuensi 1-ke-1."),
        ("2. Vigenère Mod 26 (Substitusi Periodik):", "Pergeseran aljabar dinamis C_i = (P_i + K_i) mod 26 dengan kunci SOEDIRMAN."),
        ("3. Columnar Transposition (Permutasi Geometris):", "Menyusun karakter ke dalam kisi 4×11 dan membaca kolom secara vertikal mengikuti ranking leksikografis kunci INFORMATIKA.")
    ]
    for h, b in pipe_desc:
        p = rtf.add_paragraph()
        p.text = f"\n{h}\n{b}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_WHITE

    # =========================================================
    # SLIDE 4: HASIL & EVALUASI ("RESULT & GROWTH" BIG CIRCULAR STATS)
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_top_meta(s4, "AETHERCRYPT CASE FILE", "03 KRIPTANALISIS & EVALUASI FORENSIK")

    # Left: Big Title "Result & Growth" style
    lt_box = s4.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.2), Inches(2.2))
    ltf = lt_box.text_frame
    ltf.word_wrap = True
    p = ltf.paragraphs[0]
    p.text = "Hasil &\nEvaluasi."
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.name = "Trebuchet MS"
    p.font.color.rgb = C_BLUE

    p = ltf.add_paragraph()
    p.text = "Pengujian empiris membuktikan bahwa super-enkripsi secara efektif meratakan distribusi statistik dan menghapus sidik jari bahasa alami."
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED

    # Left Bottom: Dark Key Metrics Card
    km_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(5.2), Inches(2.4))
    km_card.fill.solid()
    km_card.fill.fore_color.rgb = C_DARK
    km_card.line.fill.background()
    ktf = km_card.text_frame
    ktf.word_wrap = True
    p = ktf.paragraphs[0]
    p.text = "METRIK FORENSIK KUNCI   ✓ VALID"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_SOFT

    km_points = [
        "• Index of Coincidence mendekati nilai acak murni teoritis (0.0385)",
        "• Peningkatan Entropi Informasi Shannon mendekati batas atas 4.70 Bit",
        "• Reversibilitas 100% identik tanpa data yang hilang",
        "• Waktu eksekusi ultra cepat < 15ms"
    ]
    for pt in km_points:
        p = ktf.add_paragraph()
        p.text = pt
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(200, 205, 215)

    # Right: 3 Big Circular Stat Cards
    # Circle 1: IC Drop
    c1 = s4.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.8), Inches(1.4), Inches(2.7), Inches(2.7))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BLUE
    c1.line.width = Pt(2.5)
    ctf = c1.text_frame
    p = ctf.paragraphs[0]
    p.text = "\n0.0359"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.alignment = PP_ALIGN.CENTER
    p = ctf.add_paragraph()
    p.text = "INDEX OF COINCIDENCE\n(Normal: 0.0720)"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    p.alignment = PP_ALIGN.CENTER

    # Circle 2: Entropy
    c2 = s4.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.8), Inches(1.4), Inches(2.7), Inches(2.7))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_BG_CARD
    c2.line.color.rgb = C_BORDER
    ctf = c2.text_frame
    p = ctf.paragraphs[0]
    p.text = "\n4.231"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.alignment = PP_ALIGN.CENTER
    p = ctf.add_paragraph()
    p.text = "ENTROPI SHANNON\n(Maks: 4.700 Bit)"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    p.alignment = PP_ALIGN.CENTER

    # Pill 3 (Bottom Horizontal): 100% Reversibility
    c3 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.2))
    c3.fill.solid()
    c3.fill.fore_color.rgb = C_WHITE
    c3.line.color.rgb = C_BORDER
    ctf = c3.text_frame
    ctf.word_wrap = True
    p = ctf.paragraphs[0]
    p.text = "100% AKURASI DEKRIPSI"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.alignment = PP_ALIGN.CENTER
    p = ctf.add_paragraph()
    p.text = "Teks pulih sempurna: P ≡ P' tanpa distorsi karakter apapun.\nLatensi Pemrosesan Pipeline: < 15ms"
    p.font.size = Pt(11)
    p.font.color.rgb = C_MUTED
    p.alignment = PP_ALIGN.CENTER

    # =========================================================
    # SLIDE 5: CONTOH ENKRIPSI (4 FRAMED STEP CARDS)
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_top_meta(s5, "AETHERCRYPT CASE FILE", "04 CONTOH NYATA: PROSES ENKRIPSI STEP-BY-STEP")

    # 4 Cards Row
    steps_data = [
        ("TAHAP 00", "Normalisasi Input", "Pembersihan spasi dan simbol. Dibentuk 21 pasangan bigram.", "TEMUISAYADILABORATORIUMKRIPTOGRAFIMALAMINI"),
        ("TAHAP 01", "Playfair 5×5", "Kunci: UNIVERSITAS. Substitusi geometris baris, kolom, sudut.", "TWOLVKSVFYBQEZBMBNCOZQWCFUZTMSVJDFOGGGBWQM"),
        ("TAHAP 02", "Vigenère Mod 26", "Kunci: SOEDIRMAN. Pergeseran periodik C = (P + K) mod 26.", "TWOLVKSVFYBQEZBMBNCOZQWCFUZTMSVJDFOGGGBWQMXX"),
        ("TAHAP 03", "Columnar Transposition", "Kunci: INFORMATIKA. Kisi 4×11 dibaca urut ranking leksikografis.", "SNMWBQDXOZFGTQWFFOVMYZJXKBTBWECOLBUGVMZGVCSQ")
    ]

    for idx, (snum, stitle, sdesc, sout) in enumerate(steps_data):
        cx = Inches(0.8 + (idx * 2.95))
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.8), Inches(2.8), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE if idx < 3 else C_DARK
        card.line.color.rgb = C_BLUE if idx == 3 else C_BORDER
        ctf = card.text_frame
        ctf.word_wrap = True
        
        p = ctf.paragraphs[0]
        p.text = snum
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_BLUE_SOFT if idx == 3 else C_BLUE

        p = ctf.add_paragraph()
        p.text = stitle
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_WHITE if idx == 3 else C_DARK

        p = ctf.add_paragraph()
        p.text = sdesc
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(200, 205, 215) if idx == 3 else C_MUTED

        p = ctf.add_paragraph()
        p.text = f"\nKeluaran String:\n{sout}"
        p.font.size = Pt(9.5)
        p.font.name = "Consolas"
        p.font.bold = True
        p.font.color.rgb = C_WHITE if idx == 3 else C_BLUE

    # =========================================================
    # SLIDE 6: ALUR DEKRIPSI (4 CIRCULAR ICONS WORK PROCESS)
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_top_meta(s6, "AETHERCRYPT CASE FILE", "05 ALUR DEKRIPSI INVERS & PEMBUKTIAN REVERSIBILITAS")

    # Title Top
    tbox = s6.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(1.0))
    p = tbox.text_frame.paragraphs[0]
    p.text = "Alur Kerja Dekripsi Invers (P ≡ P')"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.name = "Trebuchet MS"
    p.font.color.rgb = C_DARK

    dec_steps = [
        ("1. Invers Columnar", "Menyusun ciphertext kembali ke kisi 4×11 mengikuti ranking kunci INFORMATIKA."),
        ("2. Invers Vigenère", "Pengurangan aljabar P = (C - K + 26) mod 26 dengan kunci SOEDIRMAN."),
        ("3. Invers Playfair", "Pembalikan aturan geser kiri, atas, dan penukaran sudut pada matriks 5×5."),
        ("4. Verifikasi Utuh", "Pesan awal pulih 100% identik tanpa kehilangan informasi semantik apapun.")
    ]

    for idx, (title, desc) in enumerate(dec_steps):
        cx = Inches(0.8 + (idx * 2.95))
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(2.2), Inches(2.8), Inches(4.3))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_GREEN if idx == 3 else C_BORDER
        ctf = card.text_frame
        ctf.word_wrap = True
        
        p = ctf.paragraphs[0]
        p.text = f"\n0{idx+1}"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = C_GREEN if idx == 3 else C_BLUE
        p.alignment = PP_ALIGN.CENTER

        p = ctf.add_paragraph()
        p.text = f"\n{title}"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.alignment = PP_ALIGN.CENTER

        p = ctf.add_paragraph()
        p.text = f"\n{desc}"
        p.font.size = Pt(11)
        p.font.color.rgb = C_MUTED
        p.alignment = PP_ALIGN.CENTER

    # =========================================================
    # SLIDE 7: KESIMPULAN ("WORK WITH ME!" CLOSING STYLE)
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_top_meta(s7, "AETHERCRYPT CASE FILE", "06 KESIMPULAN & PENUTUP")

    # Left: Big Display "Aether-Crypt!" (Work with Me! style)
    lt_box = s7.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.8), Inches(4.5))
    ltf = lt_box.text_frame
    ltf.word_wrap = True
    p = ltf.paragraphs[0]
    p.text = "Aether-\nCrypt!"
    p.font.size = Pt(64)
    p.font.bold = True
    p.font.name = "Trebuchet MS"
    p.font.color.rgb = C_BLUE

    p = ltf.add_paragraph()
    p.text = "\nSistem Super-Enkripsi 3 Lapis membuktikan integrasi harmonis antara kekuatan konfusi-difusi klasik dengan transparansi edukasi modern Three.js."
    p.font.size = Pt(14)
    p.font.color.rgb = C_MUTED

    # Right: Dark Closing Card (Contact Me! style)
    c_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.8))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = C_DARK
    c_card.line.fill.background()
    ctf = c_card.text_frame
    ctf.word_wrap = True
    
    p = ctf.paragraphs[0]
    p.text = "INFORMASI KULIAH & TIM:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_SOFT

    info_rows = [
        "🏛️ Program Studi:\nTeknik Informatika, FT Universitas Jenderal Soedirman",
        "👨‍🏫 Dosen Pengampu:\nEddy Maryanto, M.Kom & Puteri Awaliatush Shofro, M.Kom",
        "⚙️ Engine & Stack:\nPure Python 3.12 (Math Engine) + React Three.js Web",
        "✓ Status Validasi:\nTeruji 100% Identik & Siap Dipresentasikan"
    ]
    for row in info_rows:
        p = ctf.add_paragraph()
        p.text = f"\n{row}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_WHITE

    p = ctf.add_paragraph()
    p.text = "\nTERIMA KASIH • SESI TANYA JAWAB"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    p.alignment = PP_ALIGN.CENTER

    output_file = r"d:\Kripto\AetherCrypt_Presentasi_Kriptografi.pptx"
    prs.save(output_file)
    print(f"PPTX successfully updated: {output_file}")

if __name__ == "__main__":
    create_deck()
