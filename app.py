import streamlit as st
import pandas as pd
import os
from pathlib import Path
import json
from datetime import datetime
import random

# ページ設定
st.set_page_config(
    page_title="プロフェッショナリズム研修 クイズ",
    page_icon=":mortar_board:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# シンプルな白背景 + 青系カラー
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap');
    
    :root {
        --primary: #4f46e5;
        --primary-light: #e0e7ff;
        --primary-hover: #4338ca;
        --success: #3b82f6;
        --success-light: #dbeafe;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-300: #d1d5db;
        --gray-400: #9ca3af;
        --gray-500: #6b7280;
        --gray-700: #374151;
        --gray-900: #111827;
    }
    
    /* アニメーション */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .stApp {
        background: white;
        font-family: 'Noto Sans JP', sans-serif;
    }
    
    .main .block-container {
        padding: 1rem 1.5rem;
        max-width: 1000px;
        animation: fadeIn 0.4s ease-out;
    }
    
    /* Hide default elements */
    #MainMenu, footer, header, .stDeployButton {display: none;}
    
    /* サイドバー */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border-right: 1px solid var(--gray-200);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    
    /* ナビタイトル */
    .nav-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid var(--primary-light);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .nav-section {
        margin-bottom: 1.5rem;
    }
    
    .nav-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--gray-500);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    /* 問題ドット */
    .question-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 4px;
    }
    
    .q-dot {
        aspect-ratio: 1;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: default;
        background: var(--gray-100);
        color: var(--gray-500);
        border: 1px solid var(--gray-200);
    }
    
    .q-dot.current {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
        animation: pulse 2s infinite;
    }
    
    .q-dot.correct {
        background: #3b82f6;
        color: white;
        border-color: #3b82f6;
    }
    
    .q-dot.wrong {
        background: #94a3b8;
        color: white;
        border-color: #94a3b8;
    }
    
    /* 統計カード */
    .stat-card {
        background: var(--gray-50);
        border: 1px solid var(--gray-200);
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    
    .stat-card:hover {
        border-color: var(--primary-light);
        background: var(--primary-light);
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
    }
    
    .stat-label {
        font-size: 0.7rem;
        color: var(--gray-500);
        font-weight: 500;
    }
    
    /* 問題ヘッダー */
    .question-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
        animation: fadeIn 0.4s ease-out;
    }
    
    .question-num {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--gray-900);
    }
    
    .question-badge {
        background: var(--primary-light);
        color: var(--primary);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* 問題文ボックス */
    .question-container {
        background: var(--gray-50);
        border: 1px solid var(--gray-200);
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .question-text {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--gray-900);
        line-height: 1.6;
    }
    
    .category-label {
        display: inline-block;
        background: var(--gray-200);
        color: var(--gray-700);
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* セクションラベル */
    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--gray-500);
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* フィードバック */
    .feedback {
        padding: 1rem;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 1rem;
        animation: fadeIn 0.3s ease-out;
        line-height: 1.6;
    }
    
    .feedback.correct {
        background: #dcfce7;
        color: #166534;
        border-left: 4px solid #22c55e;
    }
    
    .feedback.wrong {
        background: #fce7f3;
        color: #9d174d;
        border-left: 4px solid #ec4899;
    }
    
    .feedback-title {
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* 回答後の選択肢表示 */
    .option-result {
        padding: 0.875rem 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.95rem;
        animation: fadeIn 0.3s ease-out;
    }
    
    .option-result.correct-option {
        background: #dcfce7;
        border: 2px solid #86efac;
        color: #166534;
    }
    
    .option-result.wrong-option {
        background: #fce7f3;
        border: 2px solid #f9a8d4;
        color: #9d174d;
    }
    
    .option-result.neutral {
        background: var(--gray-50);
        border: 2px solid var(--gray-200);
        color: var(--gray-500);
    }
    
    .option-letter-badge {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
        flex-shrink: 0;
    }
    
    .correct-option .option-letter-badge {
        background: #22c55e;
        color: white;
    }
    
    .wrong-option .option-letter-badge {
        background: #ec4899;
        color: white;
    }
    
    .neutral .option-letter-badge {
        background: var(--gray-200);
        color: var(--gray-500);
    }
    
    /* Streamlit overrides */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.25s ease !important;
        text-align: left !important;
        display: flex !important;
        justify-content: flex-start !important;
        height: auto !important;
        white-space: normal !important;
        line-height: 1.5 !important;
    }
    
    /* 選択肢ボタン専用スタイル */
    .stButton > button p {
        display: flex !important;
        align-items: center !important;
        gap: 0.75rem !important;
        margin: 0 !important;
        text-align: left !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    .stImage {
        border-radius: 10px;
        overflow: hidden;
        animation: fadeIn 0.4s ease-out;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# データ読み込み
@st.cache_data
def load_data():
    csv_path = Path(__file__).parent / "list.csv"
    # CSVの読み込み（エンコーディングはutf-8を想定、失敗したらcp932）
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding='cp932')
    return df

# 選択肢シャッフル
def get_shuffled_options(question_data, question_id):
    # 正解のテキストを取得
    correct_char = question_data['正解'] # A, B, C, D
    correct_text = question_data[f'選択肢{correct_char}']
    
    options_list = [
        question_data['選択肢A'],
        question_data['選択肢B'],
        question_data['選択肢C'],
        question_data['選択肢D']
    ]
    
    # NaNを除去（選択肢が3つの場合などに対応）
    options_list = [opt for opt in options_list if pd.notna(opt)]
    
    random.seed(question_id * 7)
    random.shuffle(options_list)
    
    shuffled = {}
    correct_key = None
    for idx, text in enumerate(options_list):
        key = chr(65 + idx) # A, B, C, D
        shuffled[key] = text
        if text == correct_text:
            correct_key = key
    
    return shuffled, correct_key

# セッション初期化
def init_session():
    defaults = {
        'current_question': 1,
        'answers': {},
        'shuffled_answers': {},
        'show_summary': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# 進捗保存
def save_progress():
    path = Path(__file__).parent / 'progress.json'
    data = {
        'current_question': st.session_state.current_question,
        'answers': st.session_state.answers,
        'shuffled_answers': st.session_state.shuffled_answers,
        'timestamp': datetime.now().isoformat()
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True

# 進捗読込
def load_progress():
    path = Path(__file__).parent / 'progress.json'
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for k in ['current_question', 'answers', 'shuffled_answers']:
                if k in data:
                    st.session_state[k] = data[k]
            return True
    return False

# スコア計算
def calc_score():
    correct = sum(1 for q, a in st.session_state.answers.items() 
                  if st.session_state.shuffled_answers.get(q) == a)
    return correct, len(st.session_state.answers)

# メイン
def main():
    init_session()
    df = load_data()
    total = len(df)
    
    # スコア計算
    correct_count, answered_count = calc_score()
    
    # 総括ページを表示
    if st.session_state.show_summary:
        show_summary_page(correct_count, answered_count, total)
        return
    
    # URLパラメータから問題番号を取得（クリックナビゲーション用）
    query_params = st.query_params
    if 'q' in query_params:
        try:
            q_num = int(query_params['q'])
            if 1 <= q_num <= total and q_num != st.session_state.current_question:
                st.session_state.current_question = q_num
                # パラメータをクリアしてリロード
                st.query_params.clear()
                st.rerun()
        except (ValueError, TypeError):
            pass
    
    current = st.session_state.current_question
    
    # IDでフィルタリング（No.カラムを使用）
    q_data = df[df['No.'] == current].iloc[0]
    
    # シャッフル
    options, correct_key = get_shuffled_options(q_data, current)
    
    if current not in st.session_state.shuffled_answers:
        st.session_state.shuffled_answers[current] = correct_key
    
    correct_answer = st.session_state.shuffled_answers[current]
    
    # スコア
    correct_count, answered_count = calc_score()
    
    # === サイドバー ===
    with st.sidebar:
        st.markdown('<div class="nav-title">🎓 プロフェッショナリズム研修</div>', unsafe_allow_html=True)
        
        # 統計
        if answered_count > 0:
            pct = (correct_count / answered_count * 100) if answered_count else 0
            st.markdown(f"""
            <div class="nav-section">
                <div class="nav-label">成績</div>
                <div class="stat-card">
                    <div class="stat-value">{pct:.0f}%</div>
                    <div class="stat-label">{correct_count}/{answered_count} 正解</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 問題一覧（クリックで直接移動可能）
        st.markdown('<div class="nav-label">問題一覧</div>', unsafe_allow_html=True)
        
        # JavaScriptでクリック時にURLパラメータを変更してリロード
        dots_html = '<div class="question-grid">'
        for i in range(1, total + 1):
            is_current = i == current
            is_answered = i in st.session_state.answers
            is_correct = st.session_state.answers.get(i) == st.session_state.shuffled_answers.get(i) if is_answered else False
            
            dot_class = "q-dot"
            if is_current:
                dot_class += " current"
            elif is_answered:
                dot_class += " correct" if is_correct else " wrong"
            
            # onclick でURLにパラメータを追加してページをリロード
            dots_html += f'<div class="{dot_class}" onclick="goToQuestion({i})">{i}</div>'
        dots_html += '</div>'
        
        # JavaScriptを追加（クリック時にURLパラメータを設定）
        dots_html += '''
        <script>
        function goToQuestion(num) {
            const url = new URL(window.location.href);
            url.searchParams.set('q', num);
            window.location.href = url.toString();
        }
        </script>
        '''
        st.markdown(dots_html, unsafe_allow_html=True)
        
        # 問題選択（ドロップダウンも残す）
        st.markdown("<br>", unsafe_allow_html=True)
        new_q = st.selectbox("移動", range(1, total + 1), index=current - 1, 
                            format_func=lambda x: f"問題 {x}", label_visibility="collapsed")
        if new_q != current:
            st.session_state.current_question = new_q
            st.rerun()
        
        st.markdown("<hr style='border:none;border-top:1px solid #e5e7eb;margin:1rem 0;'>", unsafe_allow_html=True)
        
        # 操作ボタン
        st.markdown('<div class="nav-label">操作</div>', unsafe_allow_html=True)
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("💾", use_container_width=True, help="保存"):
                if save_progress():
                    st.toast("保存しました", icon="✅")
        with col_s2:
            if st.button("📂", use_container_width=True, help="読込"):
                if load_progress():
                    st.toast("読み込みました", icon="✅")
                    st.rerun()
        
        if st.button("🔄 リセット", use_container_width=True):
            for k in ['current_question', 'answers', 'shuffled_answers']:
                st.session_state[k] = 1 if k == 'current_question' else {}
            st.rerun()
    
    # === メインコンテンツ ===
    
    # 問題ヘッダー
    st.markdown(f"""
    <div class="question-header">
        <span class="question-num">問題 {current}</span>
        <span class="question-badge">{current} / {total}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 問題文
    st.markdown(f"""
    <div class="question-container">
        <span class="category-label">{q_data['カテゴリ']}</span>
        <div class="question-text">{q_data['問題文（シチュエーション）']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # メインコンテンツ（2カラム）
    col_img, col_content = st.columns([1, 1])
    
    # 左: 画像
    with col_img:
        image_path = Path(__file__).parent / "IMAGES" / f"{current}.png"
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            # 画像がない場合のプレースホルダー（オプション）
            st.info("画像生成中...")
    
    # 右: 選択肢
    with col_content:
        is_answered = current in st.session_state.answers
        user_answer = st.session_state.answers.get(current)
        
        st.markdown('<div class="section-label">📝 選択肢</div>', unsafe_allow_html=True)
        
        if is_answered:
            # 回答後: 色付きHTML表示
            for key, value in options.items():
                is_correct_opt = key == correct_answer
                is_selected = key == user_answer
                
                if is_correct_opt:
                    opt_class = "correct-option"
                elif is_selected and not is_correct_opt:
                    opt_class = "wrong-option"
                else:
                    opt_class = "neutral"
                
                st.markdown(f"""
                <div class="option-result {opt_class}">
                    <span class="option-letter-badge">{key}</span>
                    <span>{value}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # フィードバックメッセージ
            if user_answer == correct_answer:
                st.markdown(f"""
                <div class="feedback correct">
                    <span class="feedback-title">🎉 正解です！</span>
                    {q_data['解説・根拠']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="feedback wrong">
                    <span class="feedback-title">😢 不正解</span>
                    {q_data['解説・根拠']}
                </div>
                """, unsafe_allow_html=True)
                
            # 次へボタン または 結果を見るボタン
            if current < total:
                if st.button("次の問題へ ➡", type="primary", use_container_width=True):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                # 最後の問題の場合、結果ページへのボタンを表示
                if st.button("📊 結果を見る", type="primary", use_container_width=True):
                    st.session_state.show_summary = True
                    st.rerun()
                    
        else:
            # 回答前: ボタン表示
            for key, value in options.items():
                if st.button(f"【{key}】 {value}", key=f"opt_{key}", use_container_width=True):
                    st.session_state.answers[current] = key
                    st.rerun()


def show_summary_page(correct_count, total_answered, total_questions):
    """総括ページ - ミニマルポートフォリオスタイル"""
    
    # スコア計算
    if total_answered > 0:
        percentage = (correct_count / total_answered) * 100
    else:
        percentage = 0
    
    # ミニマルスタイル用CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    .summary-container {
        background: #E9E9E9;
        min-height: 100vh;
        padding: 3rem 4rem;
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
    }
    
    .section-nav {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #333333;
        margin-bottom: 3rem;
    }
    
    .hero-section {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;
        margin-bottom: 4rem;
        padding-bottom: 3rem;
        border-bottom: 1px solid #000000;
    }
    
    .hero-left {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .hero-title {
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #333333;
        margin-bottom: 1rem;
    }
    
    .hero-score {
        font-size: 8rem;
        font-weight: 900;
        line-height: 0.9;
        color: #000000;
        letter-spacing: -5px;
    }
    
    .hero-score-sub {
        font-size: 1.5rem;
        font-weight: 300;
        color: #333333;
        margin-top: 1rem;
    }
    
    .hero-right {
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding-left: 2rem;
        border-left: 1px solid #333333;
    }
    
    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        padding: 1.5rem 0;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    
    .stat-row:last-child {
        border-bottom: none;
    }
    
    .stat-label-min {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #333333;
    }
    
    .stat-value-min {
        font-size: 2.5rem;
        font-weight: 800;
        color: #000000;
    }
    
    .content-section {
        margin-bottom: 4rem;
    }
    
    .content-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #000000;
    }
    
    .content-title {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #000000;
    }
    
    .content-subtitle {
        font-size: 0.6rem;
        font-weight: 400;
        letter-spacing: 1px;
        color: #666666;
    }
    
    .principle-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        margin-bottom: 3rem;
    }
    
    .principle-item {
        text-align: center;
        padding: 2rem 1rem;
        background: #FFFFFF;
    }
    
    .principle-num {
        font-size: 5rem;
        font-weight: 900;
        color: #000000;
        line-height: 1;
        margin-bottom: 1rem;
    }
    
    .principle-text {
        font-size: 0.85rem;
        font-weight: 500;
        color: #333333;
        letter-spacing: 1px;
    }
    
    .guideline-section {
        margin-bottom: 3rem;
    }
    
    .guideline-header {
        display: grid;
        grid-template-columns: 60px 1fr;
        gap: 2rem;
        align-items: start;
        padding: 2rem 0;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    
    .guideline-num {
        font-size: 2.5rem;
        font-weight: 900;
        color: #000000;
        line-height: 1;
    }
    
    .guideline-content {
        padding-top: 0.3rem;
    }
    
    .guideline-title {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #000000;
        margin-bottom: 1rem;
    }
    
    .guideline-text {
        font-size: 0.9rem;
        font-weight: 400;
        color: #333333;
        line-height: 1.8;
        letter-spacing: 0.5px;
    }
    
    .dark-section {
        background: #000000;
        color: #FFFFFF;
        padding: 4rem;
        margin: 3rem -4rem;
    }
    
    .dark-title {
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.6);
        margin-bottom: 2rem;
    }
    
    .dark-main {
        font-size: 2rem;
        font-weight: 300;
        line-height: 1.6;
        color: #FFFFFF;
        max-width: 800px;
    }
    
    .dark-main strong {
        font-weight: 700;
    }
    
    .formula-section {
        text-align: center;
        padding: 3rem 0;
        margin-bottom: 3rem;
    }
    
    .formula {
        font-size: 1.8rem;
        font-weight: 300;
        color: #000000;
        letter-spacing: 2px;
    }
    
    .formula strong {
        font-weight: 800;
    }
    
    .two-col {
        display: grid;
        grid-template-columns: 1fr 1px 1fr;
        gap: 3rem;
        padding: 2rem 0;
    }
    
    .col-divider {
        background: #000000;
        width: 2px;
    }
    
    .col-header {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }
    
    .col-header.wrong-col { color: #000000; }
    .col-header.correct-col { color: #000000; }
    
    .col-item {
        font-size: 0.95rem;
        color: #333333;
        padding: 0.5rem 0;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # セクションナビ
    st.markdown("""<div style="font-size: 0.75rem; font-weight: 600; letter-spacing: 1px; color: #4f46e5; margin-bottom: 1rem;">研修結果</div>""", unsafe_allow_html=True)
    
    # ヒーローセクション
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 2px solid #4f46e5;">
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 0.75rem; font-weight: 600; color: #6b7280; margin-bottom: 0.5rem;">あなたのスコア</div>
            <div style="font-size: 5rem; font-weight: 900; line-height: 1; color: #4f46e5;">{percentage:.0f}<span style="font-size: 2rem; font-weight: 400;">%</span></div>
            <div style="font-size: 1rem; font-weight: 400; color: #374151; margin-top: 0.5rem;">{total_answered}問中 {correct_count}問正解</div>
        </div>
        <div style="display: flex; flex-direction: column; justify-content: center; padding-left: 1.5rem; border-left: 1px solid #e5e7eb;">
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid #f3f4f6;">
                <span style="font-size: 0.85rem; color: #6b7280;">全問題数</span>
                <span style="font-size: 1.5rem; font-weight: 700; color: #111827;">{total_questions}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid #f3f4f6;">
                <span style="font-size: 0.85rem; color: #6b7280;">回答数</span>
                <span style="font-size: 1.5rem; font-weight: 700; color: #111827;">{total_answered}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0;">
                <span style="font-size: 0.85rem; color: #6b7280;">正解数</span>
                <span style="font-size: 1.5rem; font-weight: 700; color: #22c55e;">{correct_count}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 数式セクション
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; margin-bottom: 1.5rem; background: #f8fafc; border-radius: 8px;">
        <div style="font-size: 1.4rem; font-weight: 500; color: #111827;"><strong style="font-weight: 800; color: #4f46e5;">成果</strong> = 技術力 × <strong style="font-weight: 800; color: #4f46e5;">信頼・振る舞い</strong></div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3原則ヘッダー
    st.markdown("""
    <div style="margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid #4f46e5;">
        <span style="font-size: 0.9rem; font-weight: 700; color: #111827;">覚えておくべき3つの原則</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 3原則グリッド
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #eef2ff; border-radius: 8px;">
            <div style="font-size: 2.5rem; font-weight: 900; color: #4f46e5; line-height: 1; margin-bottom: 0.5rem;">01</div>
            <div style="font-size: 0.9rem; font-weight: 600; color: #1e1b4b;">嘘をつかない</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #eef2ff; border-radius: 8px;">
            <div style="font-size: 2.5rem; font-weight: 900; color: #4f46e5; line-height: 1; margin-bottom: 0.5rem;">02</div>
            <div style="font-size: 0.9rem; font-weight: 600; color: #1e1b4b;">隠さない</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #eef2ff; border-radius: 8px;">
            <div style="font-size: 2.5rem; font-weight: 900; color: #4f46e5; line-height: 1; margin-bottom: 0.5rem;">03</div>
            <div style="font-size: 0.9rem; font-weight: 600; color: #1e1b4b;">逃げない</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # ガイドラインヘッダー
    st.markdown("""
    <div style="margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid #4f46e5;">
        <span style="font-size: 0.9rem; font-weight: 700; color: #111827;">プロフェッショナル行動指針</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ガイドライン01
    st.markdown("""
    <div style="display: grid; grid-template-columns: 40px 1fr; gap: 1rem; align-items: start; padding: 1rem 0; border-bottom: 1px solid #e5e7eb;">
        <div style="font-size: 1.5rem; font-weight: 800; color: #4f46e5; line-height: 1;">01</div>
        <div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #111827; margin-bottom: 0.5rem;">現場入りの鉄則</div>
            <div style="font-size: 0.9rem; color: #374151; line-height: 1.7;">集合時間は「作業開始可能時間」。10〜15分前には到着し、トイレや着替えを済ませておく。スタッフは「黒子」として清潔感のある黒を基調に。1分でも遅れるなら必ず連絡を入れる。</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ガイドライン02
    st.markdown("""
    <div style="display: grid; grid-template-columns: 40px 1fr; gap: 1rem; align-items: start; padding: 1rem 0; border-bottom: 1px solid #e5e7eb;">
        <div style="font-size: 1.5rem; font-weight: 800; color: #4f46e5; line-height: 1;">02</div>
        <div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #111827; margin-bottom: 0.5rem;">技術・機材エリアでの規律</div>
            <div style="font-size: 0.9rem; color: #374151; line-height: 1.7;">壁のコンセントを無断で私用充電に使うのは「電気窃盗」のリスク。機材をぶつけた、ミスをしたといった「悪い報告」ほど最優先で伝える。隠蔽は取り返しのつかない事故につながる。</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ガイドライン03
    st.markdown("""
    <div style="display: grid; grid-template-columns: 40px 1fr; gap: 1rem; align-items: start; padding: 1rem 0; border-bottom: 1px solid #e5e7eb;">
        <div style="font-size: 1.5rem; font-weight: 800; color: #4f46e5; line-height: 1;">03</div>
        <div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #111827; margin-bottom: 0.5rem;">クライアント・ゲストへの敬意</div>
            <div style="font-size: 0.9rem; color: #374151; line-height: 1.7;">序列を理解する：ゲスト ＞ クライアント ＞ 上席者 ＞ スタッフ。現場の様子を個人SNSにアップすることは即刻契約解除になり得る重大な違反。</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ガイドライン04
    st.markdown("""
    <div style="display: grid; grid-template-columns: 40px 1fr; gap: 1rem; align-items: start; padding: 1rem 0; border-bottom: 1px solid #e5e7eb;">
        <div style="font-size: 1.5rem; font-weight: 800; color: #4f46e5; line-height: 1;">04</div>
        <div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #111827; margin-bottom: 0.5rem;">「見えない場所」での品格</div>
            <div style="font-size: 0.9rem; color: #374151; line-height: 1.7;">余ったお弁当は許可なく持ち帰らない。クライアントから見える場所でのスマホ操作、腕組み、居眠りは厳禁。「いつでも動ける姿勢」で待機することが安心感というサービスになる。</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # 言葉遣いヘッダー
    st.markdown("""
    <div style="margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid #4f46e5;">
        <span style="font-size: 0.9rem; font-weight: 700; color: #111827;">言葉遣い</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 言葉遣い対比
    col_avoid, col_use = st.columns(2)
    with col_avoid:
        st.markdown("""
        <div style="background: #fef2f2; padding: 1rem; border-radius: 8px; border-left: 4px solid #ef4444;">
            <div style="font-size: 0.8rem; font-weight: 700; margin-bottom: 0.75rem; color: #dc2626;">✕ 使わない</div>
            <div style="font-size: 0.95rem; color: #374151; padding: 0.3rem 0;">「わかりません」</div>
            <div style="font-size: 0.95rem; color: #374151; padding: 0.3rem 0;">「担当じゃないです」</div>
        </div>
        """, unsafe_allow_html=True)
    with col_use:
        st.markdown("""
        <div style="background: #ecfdf5; padding: 1rem; border-radius: 8px; border-left: 4px solid #22c55e;">
            <div style="font-size: 0.8rem; font-weight: 700; margin-bottom: 0.75rem; color: #16a34a;">○ 使う</div>
            <div style="font-size: 0.95rem; color: #374151; padding: 0.3rem 0;">「確認いたします」</div>
            <div style="font-size: 0.95rem; color: #374151; padding: 0.3rem 0;">「担当者にお繋ぎします」</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # ダークセクション（アクセントカラーに変更）
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); color: #FFFFFF; padding: 2rem; border-radius: 12px;">
        <div style="font-size: 0.8rem; font-weight: 600; color: rgba(255,255,255,0.8); margin-bottom: 1rem;">💡 最後に</div>
        <div style="font-size: 1.1rem; font-weight: 400; line-height: 1.7; color: #FFFFFF;">
            トラブルが起きた時、クライアントは「誰がミスをしたか」よりも「<strong style="font-weight: 700;">その後どう対応したか</strong>」を見ています。この3つを守り、誠実に行動することが、あなた自身を守り、次の仕事へと繋げる最大の武器になります。
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 操作ボタン
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 もう一度挑戦する", key="summary_retry", use_container_width=True):
            for k in ['current_question', 'answers', 'shuffled_answers', 'show_summary']:
                st.session_state[k] = 1 if k == 'current_question' else ({} if k in ['answers', 'shuffled_answers'] else False)
            st.rerun()
    with col2:
        if st.button("📋 問題を復習する", key="summary_review", use_container_width=True, type="primary"):
            st.session_state.show_summary = False
            st.rerun()


if __name__ == "__main__":
    main()
