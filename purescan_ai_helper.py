import streamlit as st
import json
from google import genai
from google.genai import types
import pydantic
from PIL import Image

# =====================================================================
# 🎨 Streamlit 行動端優化網頁設定
# =====================================================================
st.set_page_config(
    page_title="PureScan AI Helper 🍱",
    page_icon="🔮",
    layout="centered", # 集中排版，最適合手機垂直螢幕閱讀
    initial_sidebar_state="collapsed"
)

# 套用全域馬卡龍多巴胺配色與字型自定義 (內聯 CSS)
st.markdown("""
    <style>
    .reportview-container { background-color: #C69FD5; }
    h1, h2, h3 { color: #4A2E80 !important; font-family: 'Segoe UI', sans-serif; }
    .stButton>button {
        background-color: #4A2E80 !important; color: #FDFDC9 !important;
        font-weight: bold; width: 100%; border-radius: 8px; height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 PureScan AI 評估鏡")
st.write("海外藥妝、保健食品成分一秒翻譯與安全警示防線！")

# 初始化 Gemini 客戶端
@st.cache_resource
def get_ai_client():
    try:
        return genai.Client(api_key="")
    except:
        return None

ai_client = get_ai_client()

# =====================================================================
# 🤖 定義絕對不會出錯的 AI 結構化輸出 Schema
# =====================================================================
class IngredientAnalysisSchema(pydantic.BaseModel):
    商品名稱翻譯: str
    主要功效說明: str
    安全等級: str # 必須為 "安全 (綠色)", "注意 (黃色)", "警告 (紅色)" 其中之一
    成分翻譯對照表: list[str] # 格式如 ["成分A (日/英文) -> 中文翻譯", "成分B..."]
    特定體質與過敏警語: str

# =====================================================================
# 📸 手機拍照與相簿上傳功能區
# =====================================================================
uploaded_file = st.file_uploader(
    "📸 請拍攝或上傳商品背面「成分表」照片", 
    type=["png", "jpg", "jpeg", "webp"],
    help="支援日文、英文、韓文等多國包裝成分表直接辨識"
)

if uploaded_file is not None:
    # 讀取並顯示圖片（縮小顯示以符合手機螢幕）
    img = Image.open(uploaded_file)
    st.image(img, caption="已成功載入成分相片", use_container_width=True)
    
    btn_analyze = st.button("🚀 啟動 AI 智能成分分析")
    
    if btn_analyze:
        if not ai_client:
            st.error("❌ Gemini API 初始失敗，請檢查系統環境變數中的 GEMINI_API_KEY。")
        else:
            with st.spinner("AI 正在開啟多模態光學魔鏡辨識中... ⏳"):
                try:
                    # 💡 呼叫支援視覺辨識的最高性價比模型 gemini-2.5-flash
                    response = ai_client.models.generate_content(
                        model='gemini-2.5-flash',
                        # 將文字 Prompt 與 PIL Image 圖片對象直接包裹發送給 AI
                        contents=[
                            """你是一位精通多國藥妝與化學成分的醫學專家。請仔細辨識這張圖片中的外包裝成分表文字（無論是日文、英文或韓文），將其翻譯並評估其安全性與功效。
                            請注意：如果成分中含有高刺激性、台灣禁用、或常見強烈過敏原，請將安全等級評為 '警告 (紅色)' 或 '注意 (黃色)'。
                            必須一律使用繁體中文回傳結果。""",
                            img
                        ],
                        config=types.GenerateContentConfig(
                            # ✨ 核心魔法：強迫 Gemini 視覺辨識後，只能吐出嚴格的 JSON 字典結構
                            response_mime_type="application/json",
                            response_schema=IngredientAnalysisSchema,
                            temperature=0.1
                        )
                    )
                    
                    # 解析 AI 的視覺戰果
                    result = json.loads(response.text)
                    
                    st.success("分析完成！🎉")
                    st.divider()
                    
                    # =====================================================================
                    # 🎨 視覺渲染：紅黃綠大字卡面板
                    # =====================================================================
                    st.subheader(f"🏷️ 商品名稱：{result.get('商品名稱翻譯', '未明外國商品')}")
                    
                    # 依據 AI 判定的安全等級，渲染對應的高亮通知卡片
                    safety_level = result.get("安全等級", "注意 (黃色)")
                    if "綠色" in safety_level or "安全" in safety_level:
                        st.success(f"🟢 **成分安全評級：{safety_level}**")
                    elif "黃色" in safety_level or "注意" in safety_level:
                        st.warning(f"🟡 **成分安全評級：{safety_level}**")
                    else:
                        st.error(f"🔴 **成分安全評級：{safety_level}**")
                        
                    # 核心功效與警語卡片
                    st.markdown(f"### ✨ 核心功效說明\n{result.get('主要功效說明', '無')}")
                    
                    with st.expander("⚠️ 特定體質與過敏警語 (特定人群必看)", expanded=True):
                        st.write(result.get("特定體質與過敏警語", "暫無特殊警語，若有不適請立即停用。"))
                        
                    # 成分翻譯對照牆
                    st.markdown("### 📋 完整成分中文對照表")
                    for ing in result.get("成分翻譯對照表", []):
                        st.markdown(f"- {ing}")
                        
                except Exception as e:
                    st.error(f"💥 視覺解析過程中發生意外錯誤：{str(e)}")
else:
    # 初始歡迎導覽
    st.info("💡 小提示：在手機上打開此網頁時，點擊 Browse files 可以直接觸發手機相機拍照功能！")