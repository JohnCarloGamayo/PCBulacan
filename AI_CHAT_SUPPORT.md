# AI Chat Support System Documentation

## 🎯 Quick Summary
**✅ 74 Comprehensive Q&A Pairs** - Covers all aspects of PCBulacan operations  
**🌐 Bilingual Support** - English & Tagalog  
**🤖 Smart Keyword Matching** - Intelligent intent detection  
**📦 Database Integration** - Real-time product, order, and shipping data  
**⚡ Instant Responses** - 24/7 availability  

---

## Overview
The AI Chat Support system provides intelligent, database-connected customer support through natural language processing of user queries.

## Features

### 1. Order Tracking 📦
**User Queries:**
- "Kamusta yung order ko?"
- "What's the status of my order ORD-ABC123?"
- "Track my order"

**What it does:**
- Extracts order number from message (supports formats: ORD-123, ORD123, 123456)
- Queries `Order` model in database
- Retrieves order status, total amount, items, shipping info
- Shows recent orders if no order number specified (for logged-in users)

**Response includes:**
- Order number
- Current status (in Filipino/English)
- Total amount
- Order date
- List of items
- Shipping location

### 2. Product Recommendations 🛍️
**User Queries:**
- "Ano best graphics card?"
- "Recommend processor"
- "Maganda ba yung RTX?"
- "Best products sa processors"

**What it does:**
- Detects category keywords in message
- Queries `Product` model filtered by category
- Returns top 3 products ordered by rating
- Shows discount information if available

**Response includes:**
- Top 3 products in requested category
- Product names and prices
- Discount percentages
- Featured products if no category specified

### 3. Shipping Information 🚚
**User Queries:**
- "Magkano shipping sa Manila?"
- "How much is delivery to Bulacan?"
- "Gaano katagal delivery?"

**What it does:**
- Extracts city/state name from message
- Queries `DeliveryFee` model for location
- Calculates shipping costs based on base fee

**Response includes:**
- Base shipping fee for location
- Per-kilometer rate
- Estimated delivery time (3-5 days Metro Manila, 5-7 days provincial)
- General shipping info if location not found

### 4. Payment Methods 💳
**User Queries:**
- "Ano payment methods?"
- "Pwede ba GCash?"
- "How to pay?"

**Response includes:**
- Bank Transfer (BDO, BPI, Metrobank, UnionBank)
- GCash (with screenshot upload)
- PayMaya (with screenshot upload)
- Cash on Delivery (select locations)

### 5. Warranty & Returns 🛡️
**User Queries:**
- "Ano return policy?"
- "May warranty ba?"
- "Can I return this?"

**Response includes:**
- 30-day return policy
- Product condition requirements
- Manufacturer warranty (1-3 years)
- Authentic and brand new guarantee

### 6. Contact Support 📞
**User Queries:**
- "How to contact support?"
- "Phone number?"
- "Email address?"

**Response includes:**
- Phone: (044) 123-4567
- Email: support@pcbulacan.com
- Business hours: Mon-Sat, 9AM-6PM

## Technical Details

### API Endpoint
- **URL:** `/api/chat/`
- **Method:** POST
- **Request Body:** `{ "message": "user question" }`
- **Response:** `{ "response": "AI answer", "data": {...} }`

### Database Models Used
1. **Order** - order_number, status, total, items, user
2. **OrderItem** - product details, quantity, price
3. **Product** - name, price, category, rating, discount
4. **Category** - product categories
5. **DeliveryFee** - city, state, base_fee, per_km_rate

### Intent Detection
The system uses keyword matching to detect user intent:
- **ORDER_QUERY:** order, orders, tracking, kamusta, status
- **PRODUCT_QUERY:** product, recommend, best, maganda, suggest, bili
- **SHIPPING_QUERY:** shipping, delivery, ship, deliver, paano, magkano, fee
- **PAYMENT_QUERY:** payment, pay, bayad, method, gcash, cod, bank
- **WARRANTY_QUERY:** warranty, return, refund, guarantee, ibalik
- **CONTACT_QUERY:** contact, support, help, tulong, email, phone
- **GREETING:** hi, hello, kumusta, hey

### Entity Extraction
- **Order Numbers:** Regex pattern `(ord[-\s]?\w+|\b\w{10}\b)`
- **Categories:** Matches against database Category names
- **Locations:** Matches against DeliveryFee cities/states

### Response Formatting
- Uses markdown-style formatting (`**text**` for bold)
- Converts to HTML in frontend (`<strong>text</strong>`)
- Line breaks converted to `<br>` tags
- Emojis used for visual appeal

## Frontend Integration

### JavaScript (support.html)
```javascript
fetch('/api/chat/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: message })
})
.then(response => response.json())
.then(data => {
    // Format and display response
    let formattedResponse = data.response;
    formattedResponse = formattedResponse.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedResponse = formattedResponse.replace(/\n/g, '<br>');
    addMessage(formattedResponse, 'bot');
})
```

### Chat Widget Features
- 380x520px size
- Floating bubble with pulse animation
- Typing indicator with 3 animated dots
- Timestamp on each message
- Auto-scroll to latest message
- Enter key to send message

## Example Conversations

### Example 1: Order Tracking
**User:** "Kamusta order ko ORD-ABC1234567?"

**AI Response:**
```
Nakita ko ang order mo **ORD-ABC1234567**!

📦 **Status:** Processing (preparing your order)
💰 **Total:** ₱25,450.00
📅 **Ordered:** October 25, 2025
🛍️ **Items:** 1x RTX 4070, 1x AMD Ryzen 7 5800X
🚚 **Shipping:** Manila, Metro Manila

Need more help? Just ask!
```

### Example 2: Product Recommendation
**User:** "Ano best graphics card?"

**AI Response:**
```
Here are my top Graphics Cards recommendations:

1. **NVIDIA RTX 4090** - ₱89,999.00
2. **NVIDIA RTX 4080** - ₱64,999.00
3. **AMD RX 7900 XTX** - ₱54,999.00

All products are authentic and brand new! Visit our shop to see more Graphics Cards.
```

### Example 3: Shipping Query
**User:** "Magkano shipping sa Malolos?"

**AI Response:**
```
📍 **Shipping to Malolos, Bulacan:**

💵 **Base Fee:** ₱150.00
📦 **Per km rate:** ₱15.00/km
⏱️ **Delivery Time:** 3-5 business days

Standard shipping within Metro Manila takes 3-5 days. Other areas may take 5-7 days.
```

### Example 4: Payment Methods
**User:** "Ano payment methods?"

**AI Response:**
```
💳 **Available Payment Methods:**

1. **Bank Transfer** 🏦
   - BDO, BPI, Metrobank, UnionBank
   - Upload payment screenshot after ordering

2. **GCash** 📱
   - Upload screenshot after payment

3. **PayMaya** 💰
   - Upload screenshot after payment

4. **Cash on Delivery (COD)** 💵
   - Available for select locations only
   - Pay when you receive your order

All payments are secure and verified!
```

## Error Handling

### Order Not Found
```
Sorry, hindi ko mahanap ang order **ORD-123456**. 
Please check the order number or log in to view your orders.
```

### No Products in Category
```
Sorry, wala kaming available na [Category] products right now. 
Try another category!
```

### Location Not Found
```
Tell me your city/province and I'll give you the exact shipping cost!
⏱️ Delivery: 3-5 days Metro Manila, 5-7 days provincial
```

### API Error
```
Sorry, may problema sa connection. Please try again.
```

## Security

### Authentication
- Order queries respect user authentication
- Users can only view their own orders
- Unauthenticated users can get general info (products, shipping, payment)

### CSRF Protection
- Uses `@csrf_exempt` decorator (for API endpoint)
- In production, implement proper CSRF token handling

## Future Enhancements

### Planned Features
1. **Natural Language Processing:** Use NLP library (spaCy, NLTK) for better intent detection
2. **Context Memory:** Remember previous messages in conversation
3. **User Preferences:** Learn user preferences for better recommendations
4. **Multilingual Support:** Full Filipino and English language support
5. **Order Updates:** Proactive notifications about order status changes
6. **Product Comparison:** Compare multiple products side-by-side
7. **Stock Availability:** Check real-time product stock
8. **Estimated Arrival:** Calculate exact delivery dates based on location

### Technical Improvements
1. **Rate Limiting:** Prevent API abuse
2. **Caching:** Cache frequent queries for better performance
3. **Analytics:** Track common questions and improve responses
4. **Machine Learning:** Train model on customer conversations
5. **Sentiment Analysis:** Detect frustrated users and escalate to human support

## Testing

### Test Queries
Run these queries to test all features:

```
1. "Hi" - Test greeting
2. "Kamusta order ko?" - Test order listing
3. "Status ng ORD-123" - Test specific order
4. "Best graphics card" - Test product recommendation
5. "Magkano shipping sa Manila?" - Test shipping query
6. "Ano payment methods?" - Test payment info
7. "May warranty ba?" - Test warranty info
8. "Contact support" - Test contact info
9. "Random question" - Test default response
```

## Support Page URL
- **Customer Support:** http://127.0.0.1:8000/support/
- **Chat API:** http://127.0.0.1:8000/api/chat/

## Notes
- The AI chat uses keyword matching, not advanced NLP
- Responses are pre-formatted for consistency
- All data is pulled from live database
- Chat works for both logged-in and anonymous users
- Order details only shown to authenticated users who own the order
