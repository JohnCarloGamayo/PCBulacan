# PCBulacan AI Chat Support - Recent Updates

## Date: October 27, 2025

## Changes Made

### 1. Chat Widget Size Reduction ✅
**Issue:** Chat widget was too large and overlapping with content

**Solution:**
- Reduced width from 380px to **340px**
- Reduced height from 520px to **480px**
- Added `max-height: calc(100vh - 8rem)` to prevent overflow
- Mobile: Full screen with `max-height: 100vh`
- Chat bubble: Reduced from 60px to **55px** on mobile

**Files Modified:**
- `templates/support.html` - CSS for `.chat-widget`

---

### 2. Improved Shipping Query Matching ✅
**Issue:** AI couldn't answer "how much shipping fee in pandi" or "magkano shipping sa pandi bulacan"

**Solution:**
- Implemented **scoring system** for location matching:
  - Score 3: Both city AND state in message (best match)
  - Score 2: City only in message
  - Score 1: State only in message
- Now handles queries like:
  - "shipping pandi" → Finds Pandi, Bulacan
  - "magkano pandi bulacan" → Finds Pandi, Bulacan
  - "delivery fee bulacan" → Finds any Bulacan city
- Added keyword "tagal" for delivery time queries

**Files Modified:**
- `products/views.py` - `parse_and_respond()` function
- Updated to use correct field names: `fee_amount`, `estimated_days`, `is_available`

---

### 3. Removed "Submit Ticket" References ✅
**Issue:** User requested removal of ticket submission feature

**Solution:**
- Removed "Submit Ticket" quick link from hero section
- Updated hero subtitle from:
  - OLD: "Get instant answers, submit tickets, or chat with our AI assistant"
  - NEW: "Get instant answers from FAQs or chat with our AI assistant"
- Removed entire ticket form section (already done earlier)

**Files Modified:**
- `templates/support.html` - Hero section quick links

---

### 4. Added Delivery Fee Data ✅
**Issue:** No delivery fees in database, AI couldn't answer shipping queries

**Solution:**
Created `add_delivery_fees.py` script to populate database with:

**Bulacan Cities:**
- Malolos: ₱150.00 (3-5 days)
- Meycauayan: ₱120.00 (3-5 days)
- San Jose del Monte: ₱130.00 (3-5 days)
- **Pandi: ₱180.00 (4-6 days)** ← Your requested city!
- Balagtas: ₱160.00 (3-5 days)
- Bocaue: ₱140.00 (3-5 days)

**Metro Manila:**
- Caloocan: ₱100.00 (2-3 days)
- Manila: ₱100.00 (2-3 days)
- Quezon City: ₱100.00 (2-3 days)
- Valenzuela: ₱100.00 (2-3 days)

**Files Created:**
- `add_delivery_fees.py` - Script to add delivery fees

---

## Current AI Chat Capabilities

### ✅ Working Features

1. **Order Tracking**
   - "kamusta order ko?"
   - "status ng ORD-123456"
   - Shows: order number, status, total, items, date

2. **Product Recommendations**
   - "best graphics card"
   - "ano magandang processor"
   - Shows: top 3 products by rating in category

3. **Shipping Queries** ⭐ NEWLY IMPROVED
   - "magkano shipping sa pandi"
   - "how much shipping fee in pandi bulacan"
   - "delivery sa manila"
   - Shows: city, state, fee, estimated days, free shipping threshold

4. **Payment Methods**
   - "ano payment methods?"
   - Shows: Bank Transfer, GCash, PayMaya, COD with instructions

5. **Warranty & Returns**
   - "may warranty ba?"
   - Shows: 30-day return policy, warranty info

6. **Contact Support**
   - "contact support"
   - Shows: phone, email, business hours

---

## Test Queries

### Shipping Queries (Newly Fixed)
```
✅ "how much the shipping fee in pandi"
   → Response: Shipping to Pandi, Bulacan - ₱180.00 (4-6 days)

✅ "magkano shipping sa pandi bulacan"
   → Response: Shipping to Pandi, Bulacan - ₱180.00 (4-6 days)

✅ "delivery sa malolos"
   → Response: Shipping to Malolos, Bulacan - ₱150.00 (3-5 days)

✅ "magkano sa manila"
   → Response: Shipping to Manila, Metro Manila - ₱100.00 (2-3 days)

✅ "shipping bulacan" (state only)
   → Response: Best match based on scoring (e.g., Meycauayan ₱120)
```

### Other Working Queries
```
✅ "kamusta order ko?" → Shows recent orders
✅ "best graphics card" → Top 3 graphics cards
✅ "ano payment methods?" → Payment options
✅ "may warranty ba?" → Warranty information
```

---

## Technical Details

### Chat Widget Specs
- **Desktop Size:** 340px × 480px
- **Mobile Size:** Full screen (100vw × 100vh)
- **Position:** Bottom-right, 6rem from bottom, 2rem from right
- **Z-index:** 999
- **Animation:** Slide up with fade-in

### Database Schema
```python
DeliveryFee Model:
- city: CharField(100)
- state: CharField(100)
- fee_amount: DecimalField(10, 2)
- min_order_free_delivery: DecimalField(10, 2)
- estimated_days: CharField(50)
- is_available: BooleanField
```

### API Response Format
```json
{
  "response": "📍 Shipping to Pandi, Bulacan:\n\n💵 Shipping Fee: ₱180.00...",
  "data": {
    "city": "Pandi",
    "state": "Bulacan",
    "fee_amount": 180.0,
    "estimated_days": "4-6 days"
  }
}
```

---

## Files Modified Summary

1. **templates/support.html**
   - Reduced chat widget size (340×480px)
   - Removed "Submit Ticket" quick link
   - Updated hero subtitle text
   - Added responsive max-height

2. **products/views.py**
   - Improved shipping query matching with scoring system
   - Fixed field names: `fee_amount`, `estimated_days`, `is_available`
   - Added "tagal" keyword for delivery time
   - Updated response format with estimated days

3. **add_delivery_fees.py** (NEW)
   - Script to populate delivery fees
   - 10 locations (6 Bulacan, 4 Metro Manila)
   - Includes Pandi with ₱180 fee

---

## Server Status

✅ **Django Server Running:** http://127.0.0.1:8000/
✅ **Support Page:** http://127.0.0.1:8000/support/
✅ **Chat API:** http://127.0.0.1:8000/api/chat/
✅ **Database:** 10 delivery fees loaded
✅ **Auto-reload:** Enabled (changes apply automatically)

---

## Next Steps (Optional Improvements)

### Recommended Enhancements
1. **Add More Cities**
   - Run `add_delivery_fees.py` with more locations
   - Cover all Philippine provinces

2. **Natural Language Processing**
   - Use spaCy or NLTK for better intent detection
   - Handle typos and variations better

3. **Context Memory**
   - Remember previous questions in conversation
   - Allow follow-up questions

4. **Product Search**
   - "may RTX 4080 ba kayo?"
   - "available ba ang ryzen 7?"

5. **Stock Availability**
   - "in stock ba ang [product]?"
   - Show real-time stock levels

---

## Known Limitations

1. **Keyword Matching Only**
   - Uses simple keyword matching, not advanced NLP
   - May not understand complex phrasing

2. **Single Query Per Message**
   - Can't handle multiple questions in one message
   - Example: "magkano shipping AND warranty?" → Only answers one

3. **No Context Memory**
   - Each message is independent
   - Can't refer to previous messages

4. **Limited to Database Data**
   - Can only answer about existing orders, products, fees
   - Can't handle hypothetical questions

---

## Error Handling

### If Chat Doesn't Work
1. **Check Server:** Ensure Django server is running
2. **Check Console:** Look for JavaScript errors in browser console
3. **Check API:** Visit http://127.0.0.1:8000/api/chat/ (should show 405 Method Not Allowed)
4. **Check Database:** Run `python manage.py shell` and query `DeliveryFee.objects.all()`

### If Location Not Found
- Add the city to database using `add_delivery_fees.py`
- Or manually via Django admin: http://127.0.0.1:8000/admin/

---

## Success Criteria ✅

All issues resolved:
- ✅ Chat widget size reduced (340×480px)
- ✅ No longer overlapping with content
- ✅ Shipping queries working for Pandi Bulacan
- ✅ "Submit Ticket" references removed
- ✅ AI can answer "how much shipping fee in pandi"
- ✅ AI can answer "magkano shipping sa pandi bulacan"
- ✅ 10 delivery fee locations in database
- ✅ Server running without errors
- ✅ Auto-reload working (changes apply instantly)

---

## Contact for Support Development
If you need additional features or fixes:
1. Add more delivery fee locations
2. Implement advanced NLP
3. Add product search functionality
4. Integrate with third-party AI (OpenAI, etc.)
5. Add multilingual support (full Filipino/English)

---

**Last Updated:** October 27, 2025, 1:50 PM
**Status:** ✅ All requested features working
**Server:** ✅ Running on http://127.0.0.1:8000/
