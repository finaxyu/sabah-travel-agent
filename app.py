import streamlit as st
import requests
import json
from groq import Groq

# =======================
# 100% FREE SETUP - FIXED MODEL!
# =======================
st.set_page_config(
    page_title="Sabah Tourism AI 🏝️",
    page_icon="🏝️",
    layout="wide"
)

# Get Groq API key (FREE!)
GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_KEY:
    st.error("⚠️ Please add Groq API key to .streamlit/secrets.toml")
    st.info("""
    Get your FREE API key at: https://console.groq.com
    
    Then create `.streamlit/secrets.toml`:
    ```
    GROQ_API_KEY = "gsk_your-key-here"
    ```
    """)
    st.stop()

# Initialize Groq (FREE & FAST!)
client = Groq(api_key=GROQ_KEY)

def ask_ai(prompt, max_tokens=1500):
    """Call Groq AI with UPDATED model (100% free!)"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ✅ UPDATED MODEL!
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"AI Error: {str(e)}")
        return f"Error: {str(e)}"

# =======================
# FREE GEOCODING
# =======================

@st.cache_data(ttl=3600)  # Cache for 1 hour to save API calls
def get_coordinates(location_name):
    """Get coordinates using FREE Nominatim"""
    try:
        query = f"{location_name}, Sabah, Malaysia"
        url = "https://nominatim.openstreetmap.org/search"
        params = {'q': query, 'format': 'json', 'limit': 1}
        headers = {'User-Agent': 'SabahTourismHackathon/1.0'}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]
            return {
                'lat': float(result['lat']),
                'lon': float(result['lon']),
                'display_name': result.get('display_name', location_name)
            }, None
        else:
            return None, f"Location not found. Try: Kota Kinabalu, Sandakan, or Tawau"
            
    except Exception as e:
        return None, f"Error: {str(e)}"

@st.cache_data(ttl=3600)  # Cache results
def search_places(lat, lon, search_type="tourism", radius_km=20):
    """Search places using FREE Overpass API"""
    try:
        url = "https://overpass-api.de/api/interpreter"
        offset = radius_km / 111.0
        
        # Define search filters
        if search_type == "restaurant":
            query_filter = 'amenity~"restaurant|cafe|food_court"'
        elif search_type == "accommodation":
            query_filter = 'tourism~"hotel|hostel|guest_house|apartment|chalet"'
        else:  # attractions
            query_filter = 'tourism~"attraction|viewpoint|museum|gallery|theme_park|zoo|aquarium"'
        
        # Overpass QL query
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node[{query_filter}]({lat-offset},{lon-offset},{lat+offset},{lon+offset});
          way[{query_filter}]({lat-offset},{lon-offset},{lat+offset},{lon+offset});
        );
        out body;
        """
        
        response = requests.post(url, data={'data': overpass_query}, timeout=30)
        data = response.json()
        
        places = []
        seen_names = set()  # Avoid duplicates
        
        for element in data.get('elements', []):
            if 'tags' in element:
                tags = element['tags']
                name = tags.get('name', '')
                
                # Skip unnamed or duplicate places
                if not name or name in seen_names:
                    continue
                
                seen_names.add(name)
                
                # Get coordinates
                if element['type'] == 'node':
                    place_lat = element.get('lat')
                    place_lon = element.get('lon')
                elif 'center' in element:
                    place_lat = element['center'].get('lat')
                    place_lon = element['center'].get('lon')
                else:
                    continue
                
                # Build place object
                place = {
                    'name': name,
                    'type': tags.get('tourism') or tags.get('amenity', 'place'),
                    'lat': place_lat,
                    'lon': place_lon,
                    'address': tags.get('addr:street', tags.get('addr:full', 'Sabah, Malaysia')),
                    'phone': tags.get('phone', tags.get('contact:phone', '')),
                    'website': tags.get('website', tags.get('contact:website', '')),
                    'cuisine': tags.get('cuisine', ''),
                    'description': tags.get('description', ''),
                    'link': f"https://www.google.com/maps/search/?api=1&query={place_lat},{place_lon}"
                }
                
                places.append(place)
        
        return places[:15]  # Return top 15
        
    except Exception as e:
        st.warning(f"Search error: {str(e)}")
        return []

# =======================
# MAIN AI LOGIC
# =======================

def create_travel_plan(user_input):
    """Main travel planning AI"""
    
    # Step 1: Extract location using AI
    extract_prompt = f"""Extract ONLY the location name from this query: "{user_input}"

Examples:
- "plan trip to Kinabatangan" → Kinabatangan
- "food in Kota Kinabalu" → Kota Kinabalu
- "show me Sandakan" → Sandakan
- "where to eat in KK" → Kota Kinabalu

Respond with ONLY the location name, nothing else.
Location:"""
    
    location = ask_ai(extract_prompt, max_tokens=50).strip()
    
    # Clean up AI response (sometimes adds extra text)
    if '\n' in location:
        location = location.split('\n')[0]
    
    # Step 2: Get coordinates
    coords, error = get_coordinates(location)
    if error:
        return {
            "text": f"❌ {error}\n\n**Try these popular destinations:**\n- Kota Kinabalu\n- Sandakan\n- Tawau\n- Kudat\n- Kinabatangan",
            "data": {}
        }
    
    # Step 3: Determine what user wants
    query_lower = user_input.lower()
    wants_food = any(w in query_lower for w in ['food', 'eat', 'restaurant', 'makan', 'dining', 'cafe'])
    wants_stay = any(w in query_lower for w in ['stay', 'hotel', 'homestay', 'accommodation', 'sleep'])
    
    # Step 4: Search for places
    results = {}
    
    # Search attractions (default)
    if not wants_food and not wants_stay:
        attractions = search_places(coords['lat'], coords['lon'], "attraction", 25)
        if attractions:
            results['attractions'] = attractions[:10]
    
    # Search restaurants
    if wants_food:
        restaurants = search_places(coords['lat'], coords['lon'], "restaurant", 15)
        if restaurants:
            results['restaurants'] = restaurants[:10]
    
    # Search accommodations
    if wants_stay:
        accommodations = search_places(coords['lat'], coords['lon'], "accommodation", 20)
        if accommodations:
            results['accommodations'] = accommodations[:10]
    
    # Step 5: Check if we found anything
    if not results or all(not v for v in results.values()):
        return {
            "text": f"🔍 No places found near **{location}** in OpenStreetMap.\n\n**Suggestions:**\n- Try larger towns (Kota Kinabalu, Sandakan)\n- Be more specific (e.g., 'restaurants in Kota Kinabalu')\n- Check if the location name is spelled correctly",
            "data": {}
        }
    
    # Step 6: Generate friendly response with AI
    summary_prompt = f"""Create a friendly travel guide for {location}, Sabah based on this data:

{json.dumps(results, indent=2)}

Format your response like this:

# 🏝️ Your {location} Adventure Guide

[Write 2-3 sentences introducing {location} - what makes it special, what to expect]

## 🎯 Places to Visit
[If attractions data exists, list them like this:]
- **[Place Name]** 📍 [address]
  🔗 [View on map](link)
  [Add 1 sentence about why it's worth visiting]

## 🍜 Where to Eat
[If restaurant data exists, list them]

## 🏡 Where to Stay
[If accommodation data exists, list them]

## 💡 Local Tips
[Provide 2-3 practical tips about visiting {location}]

Keep it helpful, friendly, and concise. Use emojis to make it engaging!"""
    
    response_text = ask_ai(summary_prompt, max_tokens=2000)
    
    return {
        "text": response_text,
        "data": results
    }

def translate_text(text, language):
    """Translate using AI"""
    if language == "English":
        return text
    
    prompt = f"""Translate the following text to {language}.
Keep all markdown formatting (headers, links, emojis) exactly the same.
Only translate the readable text content.

Text:
{text}

Translation:"""
    
    return ask_ai(prompt, max_tokens=2000)

def generate_listing(name, location, desc, biz_type):
    """Generate operator listing"""
    prompt = f"""Create a professional tourism business listing:

Business Name: {name}
Location: {location}, Sabah
Type: {biz_type}
Description: {desc}

Create a compelling listing with:

# {name}

## ✨ About Us
[3-4 sentences describing the business]

## 🎯 What We Offer
[5 key highlights as bullet points]

## 🌟 Activities & Experiences
[List 4-6 activities guests can enjoy]

## 📋 What to Bring
[List practical items guests should bring]

## 💰 Pricing Guide
[Suggest reasonable pricing for Sabah market]

## 📞 Contact & Booking
Location: {location}, Sabah
[Add placeholders for phone/email/website]

## ⭐ Why Choose Us
[2-3 unique selling points]

Use emojis and make it professional yet welcoming!"""
    
    return ask_ai(prompt, max_tokens=2000)

# =======================
# UI
# =======================

# Sidebar
with st.sidebar:
    st.header("🌍 Language")
    language = st.selectbox(
        "Choose language:",
        ["English", "Bahasa Malaysia", "中文 (Chinese)", "日本語 (Japanese)"],
        key="language_selector"
    )
    
    st.markdown("---")
    
    st.header("🏢 For Tourism Operators")
    st.markdown("*Run a homestay or tour business?*")
    if st.button("📝 Create Professional Listing"):
        st.session_state.show_form = True
    
    st.markdown("---")
    
    st.header("ℹ️ About This Platform")
    st.markdown("""
    We help you discover:
    - 🏡 Local homestays & lodges
    - 🍜 Traditional restaurants
    - 🎭 Cultural experiences
    - 🌴 Nature attractions
    
    **100% Free to use!**
    Powered by community data.
    """)
    
    st.markdown("---")
    
    # Stats
    st.metric("Platform Cost", "RM 0.00", "100% Free")
    st.metric("Data Source", "OpenStreetMap", "Community-driven")
    
    st.markdown("---")
    st.caption("🏆 Hackathon Project 2025")
    st.caption("Built with ❤️ for Sabah")

# Main area
st.title("🏝️ Sabah Tourism AI Planner")
st.markdown("*Connecting travelers with authentic kampung experiences*")

# Info banner
st.success("💚 **Zero Cost Platform** - Using free AI (Groq) + free maps (OpenStreetMap)")

# =======================
# OPERATOR LISTING FORM
# =======================

if st.session_state.get('show_form', False):
    st.markdown("---")
    st.header("📝 Create Your Tourism Listing")
    st.markdown("*Generate a professional listing in 30 seconds!*")
    
    with st.form("listing_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            biz_name = st.text_input(
                "Business Name *", 
                placeholder="e.g., Kampung Penampang Homestay"
            )
            location = st.text_input(
                "Location *", 
                placeholder="e.g., Penampang, Sabah"
            )
        
        with col2:
            biz_type = st.selectbox(
                "Business Type *",
                ["Homestay", "Tour Operator", "Cultural Experience", "Nature Lodge", "Restaurant", "Craft Workshop"]
            )
        
        description = st.text_area(
            "Tell us about your business *",
            placeholder="Describe what makes your business special, what activities you offer, unique features...",
            height=120
        )
        
        submitted = st.form_submit_button("✨ Generate Professional Listing", use_container_width=True)
        
        if submitted:
            if biz_name and location and description:
                with st.spinner("🎨 Creating your professional listing..."):
                    listing = generate_listing(biz_name, location, description, biz_type)
                    
                    st.success("✅ Your listing is ready!")
                    st.markdown("---")
                    st.markdown(listing)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Listing (Markdown)",
                        data=listing,
                        file_name=f"{biz_name.replace(' ', '_')}_listing.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
            else:
                st.error("⚠️ Please fill in all required fields!")
    
    if st.button("← Back to Travel Planner"):
        st.session_state.show_form = False
        st.rerun()
    
    st.stop()

# =======================
# CHAT INTERFACE
# =======================

st.markdown("### 💬 Ask Me About Sabah")
st.markdown("*Try: 'Show me attractions in Kota Kinabalu' or 'Where to eat in Sandakan'*")

# Initialize chat history
if "messages" not in st.session_state:
    welcome = "👋 **Selamat datang!** Welcome to Sabah Tourism AI!\n\nI can help you discover amazing places in Sabah. Where would you like to explore?"
    if language != "English":
        welcome = translate_text(welcome, language)
    st.session_state.messages = [{"role": "assistant", "content": welcome}]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
placeholder = "Type your question... (e.g., 'attractions in Kota Kinabalu')"
if language != "English":
    placeholder = translate_text(placeholder, language)

if prompt := st.chat_input(placeholder):
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching Sabah's best spots..."):
            try:
                result = create_travel_plan(prompt)
                
                # Translate if needed
                text = result["text"]
                if language != "English":
                    with st.spinner("🌍 Translating..."):
                        text = translate_text(text, language)
                
                st.markdown(text)
                
                # Show raw data if available
                if result["data"]:
                    with st.expander("📊 View Detailed Data (JSON)"):
                        st.json(result["data"])
                
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": text
                })
                
            except Exception as e:
                error_msg = f"❌ Oops! Something went wrong: {str(e)}\n\nPlease try again or try a different location."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Quick action buttons
st.markdown("---")
st.markdown("**🚀 Quick Start - Try These Popular Destinations:**")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏙️ Kota Kinabalu", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Show me attractions in Kota Kinabalu"
        })
        st.rerun()

with col2:
    if st.button("🦧 Kinabatangan", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Wildlife and nature in Kinabatangan"
        })
        st.rerun()

with col3:
    if st.button("🏝️ Sandakan", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "What to see in Sandakan"
        })
        st.rerun()

with col4:
    if st.button("🍜 Local Food", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Find restaurants in Kota Kinabalu"
        })
        st.rerun()

# Footer
st.markdown("---")
st.caption("🗺️ Map Data: © OpenStreetMap contributors | 🤖 AI: Groq (Llama 3.3) | 💚 100% Free & Open Source")
st.caption("Made with ❤️ for Sabah's kampung tourism operators")