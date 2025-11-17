"""
AI Chat Support Training Data for PCBulacan
Comprehensive Q&A pairs in English and Tagalog - 50+ Questions
"""

def get_shipping_fees_from_db():
    """Dynamically fetch shipping fees from database"""
    try:
        from orders.models import DeliveryFee
        fees = DeliveryFee.objects.filter(is_available=True).order_by('state', 'city')
        
        bulacan_fees = []
        metro_fees = []
        
        for fee in fees:
            free_text = f"FREE pag ₱{fee.min_order_free_delivery:,.0f}+" if fee.min_order_free_delivery > 0 else ""
            fee_text = f"• {fee.city}: ₱{fee.fee_amount:,.0f}"
            if free_text:
                fee_text += f" ({free_text})"
            
            if fee.state == "Bulacan":
                bulacan_fees.append(fee_text)
            elif fee.state == "Metro Manila":
                metro_fees.append(fee_text)
        
        result = "Shipping fees based on location:\n\n"
        
        if bulacan_fees:
            result += "📍 **BULACAN:**\n" + "\n".join(bulacan_fees) + "\n\n"
        
        if metro_fees:
            result += "📍 **METRO MANILA:**\n" + "\n".join(metro_fees) + "\n\n"
        
        result += "✨ Fees calculated automatically at checkout!\n📦 Delivery time: 2-6 days depending on location"
        
        return result
    except Exception as e:
        # Fallback if database not available
        return "Shipping fees vary by location! Check our website or contact us for exact rates. 📦"


TRAINING_DATA = [
    # ===== GENERAL WEBSITE QUESTIONS (English) =====
    {
        "question": "What is PCBulacan?",
        "keywords": ["what is pcbulacan", "about pcbulacan", "pcbulacan", "who are you"],
        "answer": "PCBulacan is your premium PC components store offering a wide selection of computer parts, peripherals, and accessories. We provide quality products with competitive prices and reliable customer service in the Philippines! 🖥️✨"
    },
    {
        "question": "What products do you sell?",
        "keywords": ["products", "what do you sell", "available products", "catalog"],
        "answer": "We sell a comprehensive range of PC components:\n• Graphics Cards (GPU) 🎮\n• Processors (CPU) ⚙️\n• Motherboards\n• RAM/Memory\n• Storage (SSD/HDD)\n• Power Supplies (PSU)\n• PC Cases\n• Cooling Systems\n• Monitors 🖥️\n• Keyboards ⌨️\n• Mice 🖱️\n• Headsets 🎧\n• Gaming Peripherals"
    },
    {
        "question": "Do you have a physical store?",
        "keywords": ["physical store", "store location", "visit store", "where is your store"],
        "answer": "Yes! We have a physical store in Bulacan. You can visit us or shop online through our website for your convenience. Contact us for our exact store location and operating hours! 📍"
    },
    {
        "question": "What are your store hours?",
        "keywords": ["store hours", "operating hours", "open", "business hours"],
        "answer": "Our store operates:\n📅 Monday to Saturday: 9:00 AM - 6:00 PM\n🚫 Closed on Sundays and holidays\n🌐 Shop online 24/7 on our website!"
    },
    {
        "question": "How can I contact customer support?",
        "keywords": ["contact", "customer support", "support", "help", "assistance"],
        "answer": "You can reach us through:\n📧 Email: support@pcbulacan.com\n📞 Call our hotline\n💬 Use this AI chat for instant assistance\n\nWe respond to all inquiries within 24 hours!"
    },
    
    # ===== GENERAL WEBSITE QUESTIONS (Tagalog) =====
    {
        "question": "Ano ang PCBulacan?",
        "keywords": ["ano ang pcbulacan", "tungkol sa pcbulacan"],
        "answer": "Ang PCBulacan ay isang premium PC components store na nag-aalok ng malawak na seleksyon ng computer parts, peripherals, at accessories. Nagbibigay kami ng quality products sa competitive prices at reliable customer service! 🖥️✨"
    },
    {
        "question": "Anong mga produkto ang binebenta ninyo?",
        "keywords": ["anong produkto", "binebenta", "available", "mga product"],
        "answer": "Nagbebenta kami ng kompletong PC components:\n• Graphics Cards (GPU) 🎮\n• Processors (CPU) ⚙️\n• Motherboards\n• RAM/Memory\n• Storage (SSD/HDD)\n• Power Supplies (PSU)\n• PC Cases\n• Cooling Systems\n• Monitors 🖥️\n• Keyboards ⌨️\n• Mouse 🖱️\n• Headsets 🎧\n• Gaming Peripherals"
    },
    {
        "question": "Meron ba kayong physical store?",
        "keywords": ["physical store", "may store ba", "puntahan", "saan ang store"],
        "answer": "Oo! Mayroon kaming physical store sa Bulacan. Pwede kayo bumisita personally o mag-order online sa website namin. Contact us para sa exact location at operating hours! 📍"
    },
    {
        "question": "Ano ang inyong store hours?",
        "keywords": ["store hours", "oras", "bukas ba", "operating hours"],
        "answer": "Bukas ang store namin:\n📅 Monday to Saturday: 9:00 AM - 6:00 PM\n🚫 Sarado tuwing Sunday at holidays\n🌐 Pwede mag-shop online 24/7!"
    },
    {
        "question": "Paano ako makaka-contact ng customer support?",
        "keywords": ["paano contact", "customer support", "tulong", "assistance"],
        "answer": "Pwede kayo mag-contact through:\n📧 Email: support@pcbulacan.com\n📞 Tumawag sa hotline\n💬 Gamitin ang AI chat na ito\n\nSumasagot kami within 24 hours!"
    },
    
    # ===== PRODUCT AVAILABILITY (English) =====
    {
        "question": "Do you have RTX graphics cards in stock?",
        "keywords": ["rtx", "graphics card", "gpu", "stock", "available"],
        "answer": "To check real-time stock availability for RTX or any graphics card:\n1. Visit our Products page\n2. Filter by Graphics Card category\n3. Use the search function\n\nStock levels are updated regularly! Check availability on our website. 🎮"
    },
    {
        "question": "What brands do you carry?",
        "keywords": ["brands", "what brands", "available brands"],
        "answer": "We carry top brands:\n🎮 GPU: NVIDIA, AMD\n⚙️ CPU: Intel, AMD\n🔧 Components: ASUS, MSI, Gigabyte, Corsair, G.Skill\n💾 Storage: Samsung, Western Digital, Seagate\n🎨 Peripherals: Razer, Logitech, HyperX, Cooler Master\n\nAnd many more premium brands!"
    },
    {
        "question": "Do you sell gaming laptops?",
        "keywords": ["gaming laptop", "laptop", "pre-built"],
        "answer": "Currently, we specialize in PC components and peripherals for building custom PCs. We don't carry pre-built systems or laptops, but we can help you build the perfect gaming PC! 🎮💪"
    },
    {
        "question": "Can I request a specific product?",
        "keywords": ["request product", "special order", "can you get"],
        "answer": "Yes! If you're looking for a specific product that's not currently in stock, contact our customer support with your request. We'll do our best to source it for you! 📦"
    },
    {
        "question": "Do you have RGB components?",
        "keywords": ["rgb", "rgb components", "lighting"],
        "answer": "Absolutely! We have RGB components:\n✨ RGB RAM\n✨ RGB Fans\n✨ RGB CPU Coolers\n✨ RGB Cases\n✨ RGB Keyboards\n✨ RGB Mice\n\nBrowse our products and filter by 'RGB'! 🌈"
    },
    
    # ===== PRODUCT AVAILABILITY (Tagalog) ===== 
    {
        "question": "Meron ba kayong RTX graphics cards?",
        "keywords": ["meron ba", "may stock", "rtx", "graphics card"],
        "answer": "Para malaman ang real-time stock:\n1. Bisitahin ang Products page\n2. I-filter by Graphics Card category  \n3. Gamitin ang search\n\nRegular na ina-update ang stock levels! Check sa website namin. 🎮"
    },
    {
        "question": "Anong mga brand ang available sa inyo?",
        "keywords": ["anong brand", "mga brand", "available brands"],
        "answer": "May available kaming top brands:\n🎮 GPU: NVIDIA, AMD\n⚙️ CPU: Intel, AMD\n🔧 Components: ASUS, MSI, Gigabyte, Corsair, G.Skill\n💾 Storage: Samsung, WD, Seagate\n🎨 Peripherals: Razer, Logitech, HyperX\n\nAt marami pang premium brands!"
    },
    {
        "question": "Nagbebenta ba kayo ng gaming laptops?",
        "keywords": ["gaming laptop", "laptop", "pre-built"],
        "answer": "Sa ngayon, nag-specialize kami sa PC components at peripherals para sa custom PC building. Hindi pa kami nag-carry ng pre-built systems o laptops, pero matutulungan namin kayong mag-build ng perfect gaming PC! 🎮💪"
    },
    {
        "question": "Pwede ba ako mag-request ng specific na product?",
        "keywords": ["request", "special order", "pwede ba"],
        "answer": "Oo naman! Kung may hinahanap kayong specific product na wala sa stock, contact ang customer support. Gagawin namin ang best namin para i-source ito! 📦"
    },
    {
        "question": "May RGB components ba kayo?",
        "keywords": ["rgb", "may rgb ba", "lighting"],
        "answer": "Syempre! Marami kaming RGB components:\n✨ RGB RAM\n✨ RGB Fans\n✨ RGB CPU Coolers\n✨ RGB Cases\n✨ RGB Keyboards\n✨ RGB Mouse\n\nI-filter by 'RGB' sa products! 🌈"
    },
    
    # ===== ORDERING & PAYMENT (English) ===== 
    {
        "question": "How do I place an order?",
        "keywords": ["place order", "how to order", "ordering process"],
        "answer": "To place an order:\n1️⃣ Create account or login\n2️⃣ Browse products and add to cart 🛒\n3️⃣ Go to checkout\n4️⃣ Enter shipping address 📍\n5️⃣ Choose payment method (GCash/Bank Transfer) 💳\n6️⃣ Upload payment screenshot 📸\n7️⃣ Submit order ✅\n\nYou'll receive confirmation via email!"
    },
    {
        "question": "What payment methods do you accept?",
        "keywords": ["payment method", "payment", "how to pay"],
        "answer": "We accept:\n💳 GCash\n🏦 Bank Transfer\n\nAfter placing your order, you'll receive payment instructions. Upload your payment screenshot for verification and we'll process your order immediately!"
    },
    {
        "question": "Do you accept credit cards?",
        "keywords": ["credit card", "debit card", "card payment"],
        "answer": "Currently, we accept GCash and Bank Transfer payments. We're working on adding credit card payment options soon. Thank you for your understanding! 🙏"
    },
    {
        "question": "Do you accept Cash on Delivery (COD)?",
        "keywords": ["cod", "cash on delivery", "pay on delivery"],
        "answer": "At the moment, we require payment verification via GCash or Bank Transfer before shipping. This ensures faster processing and secure transactions for both parties! 🔒"
    },
    {
        "question": "How long to confirm my payment?",
        "keywords": ["payment confirmation", "verify payment", "how long"],
        "answer": "Once you upload your payment screenshot:\n⏱️ Verification within 2-4 hours during business hours\n📧 Email notification once confirmed\n📦 Order processing begins immediately\n\nFast and reliable!"
    },
    {
        "question": "Can I cancel my order?",
        "keywords": ["cancel order", "cancel", "refund"],
        "answer": "Yes! You can cancel if:\n✅ Status is 'Pending' or 'Processing'\n❌ Cannot cancel if 'Shipped'\n\nContact us immediately if you need to cancel. We'll process it right away!"
    },
    {
        "question": "Do you offer installment plans?",
        "keywords": ["installment", "payment plan", "hulugan"],
        "answer": "Currently, we accept full payment only via GCash or Bank Transfer. We're exploring installment payment options for the future. Stay tuned for updates! 📢"
    },
    
    # ===== ORDERING & PAYMENT (Tagalog) =====
    {
        "question": "Paano mag-order?",
        "keywords": ["paano mag-order", "pag-order", "ordering"],
        "answer": "Para mag-order:\n1️⃣ Gumawa ng account o mag-login\n2️⃣ Mag-browse at i-add sa cart 🛒\n3️⃣ Pumunta sa checkout\n4️⃣ I-enter ang shipping address 📍\n5️⃣ Pumili ng payment (GCash/Bank Transfer) 💳\n6️⃣ I-upload ang payment screenshot 📸\n7️⃣ I-submit ang order ✅\n\nMay confirmation email kayo!"
    },
    {
        "question": "Anong payment methods ang accepted?",
        "keywords": ["payment", "bayad", "paano magbayad"],
        "answer": "Tumatanggap kami ng:\n💳 GCash\n🏦 Bank Transfer\n\nPagkatapos mag-order, may payment instructions kayo. I-upload ang screenshot para ma-verify at agad naming ipro-process!"
    },
    {
        "question": "Tumatanggap ba kayo ng credit card?",
        "keywords": ["credit card", "debit card"],
        "answer": "Sa ngayon, tumatanggap kami ng GCash at Bank Transfer. Ginagawa pa namin ang credit card option. Salamat sa pag-intindi! 🙏"
    },
    {
        "question": "May Cash on Delivery ba kayo?",
        "keywords": ["cod", "cash on delivery"],
        "answer": "Sa ngayon, kailangan ng payment verification via GCash o Bank Transfer bago i-ship. Mas mabilis kasi ang processing at mas secure! 🔒"
    },
    {
        "question": "Gaano katagal ma-confirm ang payment?",
        "keywords": ["payment confirm", "gaano katagal"],
        "answer": "Pag nag-upload na ng screenshot:\n⏱️ Vine-verify within 2-4 hours\n📧 May email notification\n📦 Processing agad\n\nMabilis at reliable!"
    },
    {
        "question": "Pwede ba i-cancel ang order?",
        "keywords": ["i-cancel", "cancel order"],
        "answer": "Oo! Pwede i-cancel kung:\n✅ 'Pending' o 'Processing' pa\n❌ Hindi na kung 'Shipped'\n\nContact us agad! Ipro-process namin kaagad!"
    },
    {
        "question": "May installment ba kayo?",
        "keywords": ["installment", "hulugan", "payment plan"],
        "answer": "Sa ngayon, full payment lang via GCash o Bank Transfer. Tini-tingnan pa namin ang installment options. Abangan ninyo! 📢"
    },
    
    # ===== SHIPPING & DELIVERY (English) =====
    # NOTE: Shipping fee questions are now handled dynamically by get_shipping_fees_from_db()
    # This entry is kept for keyword matching but actual data comes from database
    {
        "question": "How much is the shipping fee?",
        "keywords": [],  # Handled by direct check in get_ai_response()
        "answer": ""  # Dynamic data from get_shipping_fees_from_db()
    },
    {
        "question": "Do you ship nationwide?",
        "keywords": ["nationwide", "ship nationwide", "deliver nationwide"],
        "answer": "Yes! We ship to all provinces in the Philippines! 🇵🇭\n\n📍 Luzon ✅\n📍 Visayas ✅\n📍 Mindanao ✅\n\nShipping fees calculated based on location. We use reliable courier services!"
    },
    {
        "question": "How long is the delivery time?",
        "keywords": ["delivery time", "how long delivery", "shipping time", "delivery days"],
        "answer": "Delivery time based on location:\n\n⏱️ **METRO MANILA:** 2-3 days\n• Caloocan, Manila, Quezon City, Valenzuela\n\n⏱️ **BULACAN:**\n• Pulilan: 2-3 days\n• Pandi: 4-6 days\n• Malolos, Bocaue, Meycauayan, San Jose del Monte, Baliuag: 3-5 days\n\n📦 Tracking information provided once shipped!\n✅ Reliable courier services used"
    },
    {
        "question": "Can I track my order?",
        "keywords": ["track order", "tracking", "where is my order"],
        "answer": "Yes! Track your order:\n1. Check email for tracking info once shipped 📧\n2. Login to your account\n3. View order history\n4. See real-time status\n\nFull transparency!"
    },
    {
        "question": "What courier do you use?",
        "keywords": ["courier", "shipping company", "delivery company"],
        "answer": "We partner with reliable couriers:\n📦 J&T Express\n📦 LBC\n📦 Other trusted logistics providers\n\nEnsuring safe and timely delivery!"
    },
    {
        "question": "Can I pick up my order instead?",
        "keywords": ["pickup", "store pickup", "pick up"],
        "answer": "Yes! Store pickup available! 🏪\n\nIf you're near our Bulacan store:\n✅ Choose 'Store Pickup' at checkout\n✅ Zero shipping fees!\n✅ Pick up at your convenience\n\nConvenient and FREE!"
    },
    {
        "question": "What if my package is damaged?",
        "keywords": ["damaged", "broken", "damaged package"],
        "answer": "We pack all items securely! But if damaged:\n1. Contact us immediately 📞\n2. Send photos within 24 hours 📸\n3. We'll arrange replacement or refund\n\nYour satisfaction is our priority! 🛡️"
    },
    
    # ===== SHIPPING & DELIVERY (Tagalog) =====
    # NOTE: Tagalog shipping fee questions also handled dynamically
    {
        "question": "Magkano ang shipping fee?",
        "keywords": [],  # Handled by direct check in get_ai_response()
        "answer": ""  # Dynamic data from get_shipping_fees_from_db()
    },
    {
        "question": "Nag-ship ba kayo nationwide?",
        "keywords": ["nationwide", "buong pilipinas"],
        "answer": "Oo! Nag-ship kami sa buong Philippines! 🇵🇭\n\n📍 Luzon ✅\n📍 Visayas ✅\n📍 Mindanao ✅\n\nReliable courier services gamit namin!"
    },
    {
        "question": "Gaano katagal ang delivery?",
        "keywords": ["gaano katagal", "delivery time", "ilang araw"],
        "answer": "Delivery time based sa location:\n\n⏱️ **METRO MANILA:** 2-3 days\n• Caloocan, Manila, Quezon City, Valenzuela\n\n⏱️ **BULACAN:**\n• Pulilan: 2-3 days\n• Pandi: 4-6 days\n• Malolos, Bocaue, Meycauayan, SJDM, Baliuag: 3-5 days\n\n📦 May tracking info once shipped!\n✅ Reliable courier gamit namin"
    },
    {
        "question": "Pwede ba i-track ang order?",
        "keywords": ["i-track", "tracking", "nasaan ang order"],
        "answer": "Oo! I-track ang order:\n1. Check email for tracking 📧\n2. Login sa account\n3. View order history\n4. Real-time status\n\nFull transparency!"
    },
    {
        "question": "Anong courier ang gamit ninyo?",
        "keywords": ["courier", "anong gamit", "delivery"],
        "answer": "Naka-partner kami ng reliable couriers:\n📦 J&T Express\n📦 LBC\n📦 Iba pang trusted logistics\n\nSafe at on-time delivery!"
    },
    {
        "question": "Pwede ba ako mag-pickup na lang?",
        "keywords": ["pickup", "kukunin", "store pickup"],
        "answer": "Oo naman! Store pickup available! 🏪\n\nKung malapit sa Bulacan store:\n✅ Pumili ng 'Store Pickup'\n✅ Zero shipping fee!\n✅ Kunin anytime\n\nConvenient at FREE!"
    },
    {
        "question": "Paano kung damaged ang package?",
        "keywords": ["damaged", "sira", "nasira"],
        "answer": "Secure naman ang packing! Pero kung damaged:\n1. Contact us agad 📞\n2. Send photos within 24 hours 📸\n3. Ire-replace o ire-refund\n\nPriority namin ang satisfaction ninyo! 🛡️"
    },
    
    # ===== ACCOUNT & RETURNS (English) =====
    {
        "question": "How do I create an account?",
        "keywords": ["create account", "sign up", "register"],
        "answer": "Create your account:\n1. Click 'Sign Up' (top right)\n2. Enter name, email, password\n3. Check email for verification 📧\n4. Verify and you're ready!\n\nStart shopping! 🛒"
    },
    {
        "question": "I forgot my password",
        "keywords": ["forgot password", "reset password", "can't login"],
        "answer": "Reset your password:\n1. Click 'Forgot Password' on login page\n2. Enter registered email\n3. Check inbox (and spam folder) 📧\n4. Click reset link\n5. Create new password\n\nDone!"
    },
    {
        "question": "Can I change my shipping address?",
        "keywords": ["change address", "shipping address", "delivery address"],
        "answer": "Yes! Manage addresses:\n1. Go to Account Settings ⚙️\n2. Add/Edit addresses\n3. Save multiple addresses\n4. Select during checkout\n\nEasy address management!"
    },
    {
        "question": "What is your return policy?",
        "keywords": ["return policy", "returns", "return product"],
        "answer": "Return Policy:\n✅ 7 days from delivery\n✅ Defective items or wrong products\n✅ Unused, original packaging\n\nContact us to initiate return. We'll guide you through the process! 🔄"
    },
    {
        "question": "Do you offer warranty?",
        "keywords": ["warranty", "guarantee"],
        "answer": "Yes! All products have manufacturer warranty:\n🛡️ 1-3 years (varies by product)\n📋 Keep receipt and packaging\n✅ Brand new and authentic\n\nYour purchase is protected!"
    },
    {
        "question": "How do I claim warranty?",
        "keywords": ["claim warranty", "warranty claim"],
        "answer": "Warranty claim process:\n1. Contact us with order number 📞\n2. Describe the issue\n3. We verify purchase\n4. Guide you through claim\n5. Replacement if eligible\n\nWe've got you covered! 🛡️"
    },
    
    # ===== ACCOUNT & RETURNS (Tagalog) =====
    {
        "question": "Paano gumawa ng account?",
        "keywords": ["gumawa ng account", "mag-sign up"],
        "answer": "Gumawa ng account:\n1. I-click ang 'Sign Up'\n2. I-enter name, email, password\n3. Check email for verification 📧\n4. I-verify at ready na!\n\nStart shopping! 🛒"
    },
    {
        "question": "Nakalimutan ko ang password",
        "keywords": ["nakalimutan password", "reset password"],
        "answer": "I-reset ang password:\n1. Click 'Forgot Password'\n2. Enter registered email\n3. Check inbox (at spam) 📧\n4. Click reset link\n5. Gumawa ng new password\n\nTapos na!"
    },
    {
        "question": "Pwede ba palitan ang shipping address?",
        "keywords": ["palitan address", "shipping address"],
        "answer": "Oo! I-manage ang addresses:\n1. Pumunta sa Account Settings ⚙️\n2. Add/Edit addresses\n3. Save multiple addresses\n4. Select sa checkout\n\nMadaling i-manage!"
    },
    {
        "question": "Ano ang return policy ninyo?",
        "keywords": ["return policy", "ibalik", "return"],
        "answer": "Return Policy:\n✅ 7 days from delivery\n✅ Defective o wrong products\n✅ Unused, original packaging\n\nContact us para mag-initiate. Tutulungan namin kayo! 🔄"
    },
    {
        "question": "May warranty ba?",
        "keywords": ["warranty", "garantiya"],
        "answer": "Oo! May manufacturer warranty:\n🛡️ 1-3 years (depends sa product)\n📋 I-keep ang receipt at packaging\n✅ Brand new and authentic\n\nProtektado ang purchase ninyo!"
    },
    {
        "question": "Paano mag-claim ng warranty?",
        "keywords": ["mag-claim", "warranty claim"],
        "answer": "Warranty claim process:\n1. Contact us with order number 📞\n2. I-describe ang issue\n3. Vive-verify ang purchase\n4. Tutulungan sa claim\n5. Replacement kung eligible\n\nAndito kami para sa inyo! 🛡️"
    },
    
    # ===== TECHNICAL QUESTIONS (English) =====
    {
        "question": "Can you help me build a PC?",
        "keywords": ["build pc", "help build", "pc build", "custom pc"],
        "answer": "Absolutely! I can help you build a PC! 🖥️\n\nTell me:\n💰 Your budget\n🎮 Purpose (gaming, streaming, work)\n📊 Target resolution (1080p, 1440p, 4K)\n\nOr check our website for pre-configured build recommendations! We'll make sure all components are compatible! 💪"
    },
    {
        "question": "What GPU is best for gaming?",
        "keywords": ["best gpu", "graphics card gaming", "gpu for gaming"],
        "answer": "Best GPU by resolution:\n\n🎮 **1080p Gaming:**\n• RTX 4060 / RX 7600\n\n🎮 **1440p Gaming:**\n• RTX 4070 / RX 7800 XT\n\n🎮 **4K Gaming:**\n• RTX 4080 / RTX 4090\n\nCheck our Graphics Card section for availability and prices! 🚀"
    },
    {
        "question": "How much RAM do I need?",
        "keywords": ["how much ram", "ram need", "memory"],
        "answer": "RAM requirements:\n\n🎮 **Gaming:** 16GB DDR4/DDR5\n💼 **Work/Multitasking:** 16-32GB\n🎬 **Content Creation:** 32GB+\n🏢 **Professional Workstation:** 64GB+\n\nCheck compatibility with your motherboard! Make sure same speed and type (DDR4/DDR5)! 💾"
    },
    {
        "question": "What's better, AMD or Intel?",
        "keywords": ["amd or intel", "amd vs intel", "better cpu"],
        "answer": "AMD vs Intel:\n\n💰 **AMD Ryzen:**\n• Better value for money\n• Excellent multi-core performance\n• Great for productivity\n\n🎮 **Intel:**\n• Slightly better gaming performance\n• Strong single-core speed\n\nBoth are excellent! Choose based on budget and needs. We carry both brands! ⚙️"
    },
    {
        "question": "Do I need a high-end PSU?",
        "keywords": ["psu", "power supply", "high-end psu"],
        "answer": "PSU is CRUCIAL! Never cheap out! ⚡\n\n**Recommendations:**\n🥉 Minimum: 80+ Bronze\n🥈 Recommended: 80+ Gold\n🥇 High-end builds: 80+ Platinum/Titanium\n\n**Wattage calculation:**\nGPU + CPU + 20% headroom\n\nExample:\n• RTX 4070 (200W) + i7 (125W) = 550W minimum\n• Get 650W PSU for safety\n\nProtect your investment! 🛡️"
    },
    {
        "question": "Should I get air or liquid cooling?",
        "keywords": ["cooling", "air cooling", "liquid cooling", "aio"],
        "answer": "Cooling comparison:\n\n❄️ **Air Cooling:**\n✅ Reliable, no leaks\n✅ Lower maintenance\n✅ Quieter (good models)\n✅ Budget-friendly\n\n💧 **Liquid/AIO Cooling:**\n✅ Better aesthetics\n✅ Better temps (high-end)\n✅ Smaller CPU clearance\n⚠️ More expensive\n\nFor most builds, good air cooler is enough! We have both options! 🌬️"
    },
    {
        "question": "What storage should I get?",
        "keywords": ["storage", "ssd", "hdd", "nvme"],
        "answer": "Storage guide:\n\n⚡ **NVMe SSD (Fastest):**\n• OS and programs: 500GB-1TB\n• Gen 3 or Gen 4\n• Best performance\n\n💾 **SATA SSD:**\n• Good for games\n• Budget option\n\n🗄️ **HDD:**\n• Mass storage\n• Movies, backups\n• 2-4TB\n\n**Recommended setup:**\n500GB NVMe (OS) + 1-2TB SSD (Games) + 2TB HDD (Storage)\n\nWe have all types! 📦"
    },
    
    # ===== TECHNICAL QUESTIONS (Tagalog) =====
    {
        "question": "Matutulungan ninyo ba akong mag-build ng PC?",
        "keywords": ["tulong build", "mag-build pc", "build computer"],
        "answer": "Syempre! Matutulungan namin kayo mag-build! 🖥️\n\nSabihin lang:\n💰 Budget\n🎮 Purpose (gaming, streaming, work)\n📊 Target resolution (1080p, 1440p, 4K)\n\nO check ang website for pre-configured builds! Titiyakin namin compatible lahat! 💪"
    },
    {
        "question": "Anong GPU ang best for gaming?",
        "keywords": ["best gpu", "magandang gpu", "gpu para sa gaming"],
        "answer": "Best GPU by resolution:\n\n🎮 **1080p Gaming:**\n• RTX 4060 / RX 7600\n\n🎮 **1440p Gaming:**\n• RTX 4070 / RX 7800 XT\n\n🎮 **4K Gaming:**\n• RTX 4080 / RTX 4090\n\nCheck ang Graphics Card section para sa prices! 🚀"
    },
    {
        "question": "Gaano karaming RAM ang kailangan?",
        "keywords": ["gaano karaming ram", "ram kailangan"],
        "answer": "RAM requirements:\n\n🎮 **Gaming:** 16GB DDR4/DDR5\n💼 **Work/Multitasking:** 16-32GB\n🎬 **Content Creation:** 32GB+\n🏢 **Professional:** 64GB+\n\nCheck compatibility sa motherboard! Same speed at type (DDR4/DDR5)! 💾"
    },
    {
        "question": "Ano mas maganda, AMD o Intel?",
        "keywords": ["amd o intel", "amd vs intel"],
        "answer": "AMD vs Intel:\n\n💰 **AMD Ryzen:**\n• Mas sulit\n• Excellent multi-core\n• Great for productivity\n\n🎮 **Intel:**\n• Konting better sa gaming\n• Strong single-core\n\nMaganda pareho! Choose based sa budget. May AMD at Intel kami! ⚙️"
    },
    {
        "question": "Kailangan ba ng high-end PSU?",
        "keywords": ["psu", "power supply", "kailangan ba"],
        "answer": "PSU is CRUCIAL! Never mag-tipid! ⚡\n\n**Recommendations:**\n🥉 Minimum: 80+ Bronze\n🥈 Recommended: 80+ Gold\n🥇 High-end: 80+ Platinum/Titanium\n\n**Wattage calculation:**\nGPU + CPU + 20% extra\n\nExample:\n• RTX 4070 (200W) + i7 (125W) = 550W min\n• Kumuha ng 650W for safety\n\nProtektahan ang investment! 🛡️"
    },
    {
        "question": "Air cooling ba o liquid cooling?",
        "keywords": ["cooling", "air o liquid", "aio"],
        "answer": "Cooling comparison:\n\n❄️ **Air Cooling:**\n✅ Reliable, walang leak\n✅ Less maintenance\n✅ Tahimik (good models)\n✅ Budget-friendly\n\n💧 **Liquid/AIO:**\n✅ Better aesthetics\n✅ Better temps (high-end)\n✅ Smaller space\n⚠️ Mas mahal\n\nFor most builds, air cooler okay na! May both options kami! 🌬️"
    },
    {
        "question": "Anong storage ang dapat kunin?",
        "keywords": ["storage", "ssd", "hdd", "anong storage"],
        "answer": "Storage guide:\n\n⚡ **NVMe SSD (Fastest):**\n• OS at programs: 500GB-1TB\n• Gen 3 o Gen 4\n• Best performance\n\n💾 **SATA SSD:**\n• For games\n• Budget option\n\n🗄️ **HDD:**\n• Mass storage\n• Movies, backups\n• 2-4TB\n\n**Recommended:**\n500GB NVMe (OS) + 1-2TB SSD (Games) + 2TB HDD (Storage)\n\nMay lahat kami! 📦"
    },
    
    # ===== ADDITIONAL 100+ QUESTIONS - PRODUCT SPECIFIC =====
    
    # Monitors & Displays
    {
        "question": "What monitor should I get for gaming?",
        "keywords": ["gaming monitor", "monitor for gaming", "best monitor"],
        "answer": "Gaming monitor recommendations:\n\n🎮 **1080p 144Hz** - Budget gaming\n• Great for esports\n• Around ₱8,000-₱15,000\n\n🎮 **1440p 165Hz** - Sweet spot\n• Best balance\n• Around ₱15,000-₱25,000\n\n🎮 **4K 144Hz** - Premium\n• Ultimate experience\n• Around ₱30,000+\n\n**Look for:** IPS panel, 1ms response, FreeSync/G-Sync\nCheck our Monitors category!"
    },
    {
        "question": "Anong magandang monitor para sa gaming?",
        "keywords": ["monitor gaming", "magandang monitor"],
        "answer": "Gaming monitor recommendations:\n\n🎮 **1080p 144Hz** - Budget\n• Okay for esports\n• Around ₱8,000-₱15,000\n\n🎮 **1440p 165Hz** - Best choice\n• Pinaka-sulit\n• Around ₱15,000-₱25,000\n\n🎮 **4K 144Hz** - Premium\n• Ultimate gaming\n• Around ₱30,000+\n\n**Hanapin:** IPS panel, 1ms response, FreeSync/G-Sync"
    },
    
    # Keyboards & Peripherals
    {
        "question": "Mechanical or membrane keyboard?",
        "keywords": ["mechanical keyboard", "membrane keyboard", "keyboard type"],
        "answer": "Keyboard comparison:\n\n⌨️ **Mechanical:**\n✅ Better tactile feedback\n✅ More durable (50M+ keystrokes)\n✅ Customizable switches\n✅ Great for gaming & typing\n💰 ₱2,000-₱8,000+\n\n⌨️ **Membrane:**\n✅ Quieter\n✅ Budget-friendly\n✅ Good for office work\n💰 ₱500-₱2,000\n\n**Recommendation:** Mechanical for gaming!"
    },
    {
        "question": "Anong mas maganda mechanical o membrane keyboard?",
        "keywords": ["mechanical o membrane", "keyboard"],
        "answer": "Keyboard comparison:\n\n⌨️ **Mechanical:**\n✅ Better feedback\n✅ Mas matibay (50M+ presses)\n✅ Pwedeng i-customize\n✅ Great for gaming\n💰 ₱2,000-₱8,000+\n\n⌨️ **Membrane:**\n✅ Mas tahimik\n✅ Budget-friendly\n✅ Okay for office\n💰 ₱500-₱2,000\n\n**Recommend:** Mechanical para sa gaming!"
    },
    
    # Gaming Mouse
    {
        "question": "What gaming mouse should I buy?",
        "keywords": ["gaming mouse", "mouse for gaming", "best mouse"],
        "answer": "Gaming mouse guide:\n\n🖱️ **Budget (₱500-₱1,500):**\n• Logitech G102\n• Razer Viper Mini\n\n🖱️ **Mid-range (₱1,500-₱3,500):**\n• Logitech G304/G305\n• Razer DeathAdder V2\n\n🖱️ **Premium (₱3,500+):**\n• Logitech G Pro X Superlight\n• Razer Viper Ultimate\n\n**Look for:** 12,000+ DPI, lightweight, good sensor\nCheck our Peripherals section!"
    },
    {
        "question": "Anong gaming mouse ang dapat bilhin?",
        "keywords": ["gaming mouse", "mouse"],
        "answer": "Gaming mouse guide:\n\n🖱️ **Budget (₱500-₱1,500):**\n• Logitech G102\n• Razer Viper Mini\n\n🖱️ **Mid-range (₱1,500-₱3,500):**\n• Logitech G304/G305\n• Razer DeathAdder V2\n\n🖱️ **Premium (₱3,500+):**\n• Logitech G Pro X Superlight\n• Razer Viper Ultimate\n\n**Hanapin:** 12,000+ DPI, magaan, good sensor"
    },
    
    # Headsets & Audio
    {
        "question": "What headset is good for gaming?",
        "keywords": ["gaming headset", "headset for gaming", "best headset"],
        "answer": "Gaming headset recommendations:\n\n🎧 **Budget (₱1,000-₱2,500):**\n• HyperX Cloud Stinger\n• Razer Kraken X\n• Good audio, comfortable\n\n🎧 **Mid-range (₱2,500-₱5,000):**\n• HyperX Cloud II\n• Logitech G Pro X\n• 7.1 surround, great mic\n\n🎧 **Premium (₱5,000+):**\n• SteelSeries Arctis Pro\n• Wireless options\n\n**Features:** Good mic, comfortable, 7.1 surround"
    },
    {
        "question": "Anong headset ang maganda for gaming?",
        "keywords": ["gaming headset", "headset"],
        "answer": "Gaming headset recommendations:\n\n🎧 **Budget (₱1,000-₱2,500):**\n• HyperX Cloud Stinger\n• Razer Kraken X\n• Okay audio, comfortable\n\n🎧 **Mid-range (₱2,500-₱5,000):**\n• HyperX Cloud II\n• Logitech G Pro X\n• 7.1 surround, magandang mic\n\n🎧 **Premium (₱5,000+):**\n• SteelSeries Arctis Pro\n• Wireless options\n\n**Features:** Good mic, comfortable, 7.1 surround"
    },
    
    # PC Cases
    {
        "question": "What PC case should I choose?",
        "keywords": ["pc case", "case", "chassis"],
        "answer": "PC case guide:\n\n📦 **Budget (₱1,500-₱3,000):**\n• Good airflow\n• Basic cable management\n• NZXT H510, Tecware Forge M\n\n📦 **Mid-range (₱3,000-₱6,000):**\n• Better airflow\n• Tempered glass\n• RGB support\n• Lian Li Lancool 215\n\n📦 **Premium (₱6,000+):**\n• Excellent cooling\n• Premium build quality\n• Lian Li O11, Fractal Torrent\n\n**Consider:** Size (ATX/mATX), airflow, RGB, cable management"
    },
    {
        "question": "Anong PC case ang dapat piliin?",
        "keywords": ["pc case", "case"],
        "answer": "PC case guide:\n\n📦 **Budget (₱1,500-₱3,000):**\n• Okay airflow\n• Basic cable management\n• NZXT H510, Tecware Forge M\n\n📦 **Mid-range (₱3,000-₱6,000):**\n• Better airflow\n• Tempered glass\n• RGB support\n• Lian Li Lancool 215\n\n📦 **Premium (₱6,000+):**\n• Excellent cooling\n• Premium quality\n• Lian Li O11, Fractal Torrent\n\n**Consider:** Size, airflow, RGB, cable management"
    },
    
    # Motherboards
    {
        "question": "What motherboard do I need?",
        "keywords": ["motherboard", "mobo", "mainboard"],
        "answer": "Motherboard selection:\n\n🔧 **Match your CPU:**\n• Intel 12th-14th gen: LGA 1700 (B660/B760/Z690/Z790)\n• AMD Ryzen 5000: AM4 (B550/X570)\n• AMD Ryzen 7000: AM5 (B650/X670)\n\n📊 **Chipset tiers:**\n• B-series: Budget-mid range, no overclocking\n• X/Z-series: Premium, overclocking support\n\n💡 **Features to check:**\n• RAM slots (2 or 4)\n• M.2 slots for NVMe\n• PCIe version\n• WiFi/Bluetooth (if needed)\n\nTell me your CPU and I'll recommend compatible boards!"
    },
    {
        "question": "Anong motherboard ang kailangan?",
        "keywords": ["motherboard", "mobo"],
        "answer": "Motherboard selection:\n\n🔧 **Match sa CPU:**\n• Intel 12th-14th gen: LGA 1700 (B660/B760/Z690/Z790)\n• AMD Ryzen 5000: AM4 (B550/X570)\n• AMD Ryzen 7000: AM5 (B650/X670)\n\n📊 **Chipset tiers:**\n• B-series: Budget-mid, no OC\n• X/Z-series: Premium, may OC\n\n💡 **Check:**\n• RAM slots\n• M.2 slots\n• PCIe version\n• WiFi (kung need)\n\nSabihin ang CPU mo, recommend ko compatible board!"
    },
    
    # Budget Builds
    {
        "question": "Budget gaming PC build under 30k?",
        "keywords": ["budget pc", "30k build", "cheap gaming pc"],
        "answer": "₱30,000 Budget Gaming PC:\n\n💰 **Components:**\n• CPU: Intel i3-12100F / Ryzen 5 5500 - ₱5,500\n• GPU: GTX 1650 / RX 6500 XT - ₱8,500\n• RAM: 16GB DDR4 3200MHz - ₱2,800\n• Storage: 500GB NVMe SSD - ₱2,000\n• Motherboard: B660/B550 - ₱5,000\n• PSU: 500W 80+ Bronze - ₱2,500\n• Case: Basic ATX - ₱1,800\n• **Total: ~₱28,000**\n\n🎮 **Performance:** 1080p medium-high 60fps\n\nVisit our Products page to check current prices!"
    },
    {
        "question": "Budget gaming PC under 30k?",
        "keywords": ["30k", "budget build", "murang pc"],
        "answer": "₱30,000 Budget Gaming PC:\n\n💰 **Parts:**\n• CPU: Intel i3-12100F / Ryzen 5 5500 - ₱5,500\n• GPU: GTX 1650 / RX 6500 XT - ₱8,500\n• RAM: 16GB DDR4 - ₱2,800\n• Storage: 500GB SSD - ₱2,000\n• Motherboard: B660/B550 - ₱5,000\n• PSU: 500W - ₱2,500\n• Case: Basic - ₱1,800\n• **Total: ~₱28,000**\n\n🎮 **Kaya:** 1080p medium-high 60fps"
    },
    
    # Mid-range Builds
    {
        "question": "Mid-range gaming PC build 50-60k?",
        "keywords": ["50k build", "60k build", "mid range pc"],
        "answer": "₱50-60K Mid-range Gaming PC:\n\n💰 **Components:**\n• CPU: Intel i5-12400F / Ryzen 5 5600X - ₱9,500\n• GPU: RTX 4060 / RX 6700 XT - ₱18,000\n• RAM: 16GB DDR4 3600MHz - ₱3,500\n• Storage: 1TB NVMe Gen 4 - ₱4,500\n• Motherboard: B660/B550 - ₱6,500\n• PSU: 650W 80+ Gold - ₱4,500\n• Case: Mid-tower TG - ₱3,500\n• **Total: ~₱50,000**\n\n🎮 **Performance:** 1080p ultra 100+ fps, 1440p high 60+ fps\n\nPerfect balance of price and performance!"
    },
    {
        "question": "Mid-range gaming PC 50-60k?",
        "keywords": ["50k", "60k", "mid range"],
        "answer": "₱50-60K Mid-range Gaming PC:\n\n💰 **Parts:**\n• CPU: i5-12400F / Ryzen 5 5600X - ₱9,500\n• GPU: RTX 4060 / RX 6700 XT - ₱18,000\n• RAM: 16GB DDR4 - ₱3,500\n• Storage: 1TB SSD - ₱4,500\n• Motherboard: B660/B550 - ₱6,500\n• PSU: 650W Gold - ₱4,500\n• Case: Mid-tower - ₱3,500\n• **Total: ~₱50,000**\n\n🎮 **Kaya:** 1080p ultra 100fps, 1440p high 60fps"
    },
    
    # High-end Builds
    {
        "question": "High-end gaming PC build 100k+?",
        "keywords": ["100k build", "high end pc", "premium build"],
        "answer": "₱100K+ High-end Gaming PC:\n\n💰 **Components:**\n• CPU: Intel i7-13700K / Ryzen 7 7800X3D - ₱22,000\n• GPU: RTX 4070 Ti / RX 7900 XT - ₱42,000\n• RAM: 32GB DDR5 6000MHz - ₱8,000\n• Storage: 2TB NVMe Gen 4 - ₱8,500\n• Motherboard: Z790/X670 - ₱12,000\n• PSU: 850W 80+ Gold Modular - ₱7,000\n• Case: Premium TG RGB - ₱5,500\n• **Total: ~₱105,000**\n\n🎮 **Performance:** 1440p ultra 144fps, 4K high 60+ fps\n\nUltimate gaming experience!"
    },
    {
        "question": "High-end gaming PC 100k+?",
        "keywords": ["100k", "high end", "premium"],
        "answer": "₱100K+ High-end Gaming PC:\n\n💰 **Parts:**\n• CPU: i7-13700K / Ryzen 7 7800X3D - ₱22,000\n• GPU: RTX 4070 Ti / RX 7900 XT - ₱42,000\n• RAM: 32GB DDR5 - ₱8,000\n• Storage: 2TB SSD - ₱8,500\n• Motherboard: Z790/X670 - ₱12,000\n• PSU: 850W Modular - ₱7,000\n• Case: Premium RGB - ₱5,500\n• **Total: ~₱105,000**\n\n🎮 **Kaya:** 1440p ultra 144fps, 4K high 60fps"
    },
    
    # Streaming Builds
    {
        "question": "PC build for streaming and gaming?",
        "keywords": ["streaming pc", "stream and game", "content creation"],
        "answer": "Streaming + Gaming PC (₱70-80K):\n\n💰 **Components:**\n• CPU: Ryzen 7 5700X / i7-12700F - ₱14,000\n  (More cores for encoding!)\n• GPU: RTX 4060 Ti / RTX 3060 Ti - ₱22,000\n  (NVENC encoder for streaming)\n• RAM: 32GB DDR4 - ₱5,500\n  (More RAM for OBS + Game)\n• Storage: 1TB NVMe - ₱4,500\n• Motherboard: B550/B660 - ₱7,000\n• PSU: 750W 80+ Gold - ₱5,500\n• Case: Good airflow - ₱4,000\n\n🎥 **Can stream:** 1080p 60fps while gaming\n📺 **Recommended:** 2nd monitor for chat"
    },
    {
        "question": "PC para sa streaming at gaming?",
        "keywords": ["streaming", "para mag-stream"],
        "answer": "Streaming + Gaming PC (₱70-80K):\n\n💰 **Parts:**\n• CPU: Ryzen 7 5700X / i7-12700F - ₱14,000\n  (More cores for encoding!)\n• GPU: RTX 4060 Ti - ₱22,000\n  (NVENC para sa streaming)\n• RAM: 32GB DDR4 - ₱5,500\n  (More RAM para sa OBS)\n• Storage: 1TB SSD - ₱4,500\n• Motherboard: B550/B660 - ₱7,000\n• PSU: 750W - ₱5,500\n• Case: Good airflow - ₱4,000\n\n🎥 **Kaya:** 1080p 60fps stream habang nag-lalaro"
    },
    
    # Upgrade Questions
    {
        "question": "Should I upgrade GPU or CPU first?",
        "keywords": ["upgrade gpu or cpu", "what to upgrade"],
        "answer": "Upgrade priority:\n\n🎮 **Upgrade GPU first if:**\n• Gaming is your main use\n• Current GPU struggling at target FPS\n• CPU usage under 80% while gaming\n• Playing at 1440p or 4K\n\n⚙️ **Upgrade CPU first if:**\n• CPU usage 90-100% while gaming\n• Streaming or content creation\n• Playing CPU-heavy games (strategy, simulation)\n• Using old CPU (4+ years)\n\n💡 **Check your bottleneck:**\nMonitor CPU & GPU usage while gaming:\n• GPU at 100% = Upgrade GPU\n• CPU at 100% = Upgrade CPU\n\nTell me your current specs for specific advice!"
    },
    {
        "question": "GPU o CPU dapat i-upgrade muna?",
        "keywords": ["upgrade gpu o cpu", "ano i-upgrade"],
        "answer": "Upgrade priority:\n\n🎮 **GPU muna kung:**\n• Pang-gaming lang mostly\n• GPU mo nahihirapan sa FPS\n• CPU usage under 80%\n• 1440p or 4K gaming\n\n⚙️ **CPU muna kung:**\n• CPU usage 90-100%\n• Nag-stream o nag-edit\n• CPU-heavy games\n• Luma na CPU (4+ years)\n\n💡 **Check bottleneck:**\n• GPU 100% = Upgrade GPU\n• CPU 100% = Upgrade CPU\n\nSabihin current specs mo!"
    },
    
    # Laptop Questions
    {
        "question": "Gaming laptop or desktop PC?",
        "keywords": ["laptop or desktop", "laptop vs desktop"],
        "answer": "Laptop vs Desktop:\n\n💻 **Gaming Laptop Pros:**\n✅ Portable\n✅ All-in-one (monitor, keyboard included)\n✅ Built-in UPS (battery)\n❌ More expensive for same performance\n❌ Limited upgradability\n❌ Thermal throttling\n\n🖥️ **Desktop PC Pros:**\n✅ Better performance per peso\n✅ Fully upgradeable\n✅ Better cooling\n✅ Cheaper to repair\n❌ Not portable\n❌ Need separate monitor\n\n💡 **Recommendation:**\n• Need portability? → Laptop\n• Best value & performance? → Desktop\n\nWe specialize in desktop components!"
    },
    {
        "question": "Gaming laptop o desktop PC?",
        "keywords": ["laptop o desktop"],
        "answer": "Laptop vs Desktop:\n\n💻 **Gaming Laptop:**\n✅ Portable\n✅ May keyboard na\n✅ May battery\n❌ Mas mahal\n❌ Limited upgrade\n❌ Init\n\n🖥️ **Desktop PC:**\n✅ Better performance per peso\n✅ Pwedeng i-upgrade\n✅ Better cooling\n✅ Mas mura repair\n❌ Hindi portable\n❌ Need monitor\n\n💡 **Recommend:**\n• Need dalhin-dalhin? → Laptop\n• Best value? → Desktop\n\nDesktop components specialty namin!"
    },
    
    # RGB & Aesthetics
    {
        "question": "How to add RGB to my PC?",
        "keywords": ["add rgb", "rgb setup", "rgb lighting"],
        "answer": "Adding RGB to your PC:\n\n✨ **RGB Components Available:**\n• RGB RAM - ₱3,000+\n• RGB Fans (120mm/140mm) - ₱500-₱1,500 each\n• RGB LED Strips - ₱300-₱800\n• RGB CPU Cooler - ₱2,000-₱6,000\n• RGB Case - ₱3,000+\n• RGB Motherboard - with RGB headers\n\n🎨 **Control Options:**\n• Motherboard RGB software (ASUS Aura, MSI Mystic Light)\n• Controller hub\n• Manual remote control\n\n💡 **Tips:**\n• Check motherboard RGB headers (5V or 12V)\n• Match RGB ecosystem for sync\n• Don't go overboard - less is more!\n\nBrowse our RGB products! 🌈"
    },
    {
        "question": "Paano mag-add ng RGB sa PC?",
        "keywords": ["rgb", "paano rgb"],
        "answer": "Adding RGB:\n\n✨ **RGB Parts:**\n• RGB RAM - ₱3,000+\n• RGB Fans - ₱500-₱1,500\n• RGB LED Strips - ₱300-₱800\n• RGB CPU Cooler - ₱2,000-₱6,000\n• RGB Case - ₱3,000+\n\n🎨 **Control:**\n• Motherboard software\n• Controller hub\n• Remote control\n\n💡 **Tips:**\n• Check motherboard RGB headers\n• Same brand para mag-sync\n• Wag sobra - simple lang!\n\nMay RGB products kami! 🌈"
    },
    
    # Troubleshooting
    {
        "question": "PC won't turn on, what to check?",
        "keywords": ["pc wont turn on", "pc not starting", "no power"],
        "answer": "PC won't turn on - Troubleshooting:\n\n🔌 **Check these first:**\n1. Power cable connected?\n2. PSU switch ON? (back of PSU)\n3. Monitor cable connected?\n4. Monitor powered on?\n\n⚡ **Common causes:**\n• Loose power cables\n• RAM not seated properly\n• GPU not fully inserted\n• Motherboard power cables\n• Dead PSU\n\n🔧 **Try:**\n1. Reseat RAM sticks\n2. Check all power connectors\n3. Remove GPU, use integrated graphics\n4. Test with different outlet\n\n❌ **Still not working?**\nContact us for warranty support or bring to our Malolos branch for diagnosis!"
    },
    {
        "question": "PC ayaw mag-boot, ano check?",
        "keywords": ["ayaw mag-boot", "hindi nag-oopen", "walang power"],
        "answer": "PC ayaw mag-boot:\n\n🔌 **Check:**\n1. Naka-plug ba power?\n2. PSU switch ON?\n3. Monitor cable okay?\n4. Monitor naka-on?\n\n⚡ **Common problems:**\n• Loose cables\n• RAM hindi naka-proper\n• GPU hindi naka-insert ng tama\n• PSU sira\n\n🔧 **Try:**\n1. I-reseat RAM\n2. Check all connectors\n3. Tanggalin GPU, try onboard\n4. Iba outlet\n\n❌ **Di pa rin gumana?**\nContact us o dala sa Malolos branch!"
    },
    
    # Performance Questions
    {
        "question": "Why is my PC slow?",
        "keywords": ["pc slow", "pc lag", "computer slow"],
        "answer": "PC running slow - Common causes:\n\n🐌 **Hardware issues:**\n• HDD instead of SSD → Upgrade to SSD!\n• Low RAM (under 8GB) → Add more RAM\n• Old/weak CPU → Consider upgrade\n• Overheating → Clean dust, check cooling\n• Full storage → Free up space\n\n💻 **Software issues:**\n• Too many startup programs\n• Virus/malware\n• Windows updates pending\n• Full disk (under 20% free)\n\n⚡ **Quick fixes:**\n1. Restart PC\n2. Close unnecessary programs\n3. Run disk cleanup\n4. Update drivers\n5. Check Task Manager for CPU hogs\n\n**Need upgrade? Check our SSDs, RAM, CPUs!**"
    },
    {
        "question": "Bakit bagal ng PC ko?",
        "keywords": ["bagal pc", "mabagal computer"],
        "answer": "Mabagal PC - Causes:\n\n🐌 **Hardware:**\n• HDD pa (dapat SSD)\n• Konti RAM (under 8GB)\n• Luma CPU\n• Mainit - puno ng alikabok\n• Puno storage\n\n💻 **Software:**\n• Maraming startup programs\n• May virus\n• Pending Windows update\n• Puno disk\n\n⚡ **Quick fix:**\n1. Restart\n2. Close programs\n3. Disk cleanup\n4. Update drivers\n5. Check Task Manager\n\n**Need upgrade? Check SSD, RAM, CPU namin!**"
    },
    
    # Overclocking
    {
        "question": "Is overclocking safe?",
        "keywords": ["overclocking", "overclock", "OC"],
        "answer": "Overclocking guide:\n\n⚡ **What is it?**\nRunning CPU/GPU beyond stock speeds for more performance.\n\n✅ **Safe if done properly:**\n• Use good cooling\n• Increase gradually\n• Monitor temps (under 85°C)\n• Stress test stability\n• Don't overvolt too much\n\n⚠️ **Risks:**\n• Void warranty (sometimes)\n• More heat & power draw\n• System instability if pushed too far\n• Reduced lifespan if excessive\n\n💡 **Recommendation:**\n• CPU: 5-15% boost is safe\n• GPU: Use MSI Afterburner\n• Need K-series Intel or X-series AMD\n• Need Z/X motherboard\n\n**Our staff can guide you if you buy components from us!**"
    },
    {
        "question": "Safe ba ang overclocking?",
        "keywords": ["overclocking", "OC"],
        "answer": "Overclocking guide:\n\n⚡ **Ano yun?**\nPinapa-faster ang CPU/GPU beyond stock.\n\n✅ **Safe kung maayos:**\n• Good cooling\n• Increase slowly\n• Monitor temps (under 85°C)\n• Test stability\n• Wag sobra volt\n\n⚠️ **Risks:**\n• Void warranty\n• More init\n• Unstable kung sobra\n• Shorter lifespan\n\n💡 **Recommend:**\n• CPU: 5-15% okay\n• GPU: Use MSI Afterburner\n• Need K-Intel or X-AMD\n• Need Z/X motherboard\n\n**Staff namin pwede tumulong!**"
    },
    
    # Cable Management
    {
        "question": "Tips for cable management?",
        "keywords": ["cable management", "organize cables", "clean build"],
        "answer": "Cable management tips:\n\n🔌 **Planning:**\n• Route cables behind motherboard tray\n• Use case cable routing holes\n• Plan before connecting\n\n🎯 **Tools needed:**\n• Velcro straps (₱50-₱200)\n• Cable ties (₱30-₱100)\n• Cable combs for PSU (₱200-₱500)\n\n💡 **Best practices:**\n1. Connect 24-pin & 8-pin CPU first\n2. Route through nearest hole\n3. Group similar cables\n4. Hide excess cable length behind\n5. Use PSU shroud if available\n6. Leave slack for maintenance\n\n✨ **Benefits:**\n• Better airflow\n• Easier maintenance\n• Cleaner aesthetics\n• Prevent cable damage\n\n**Modular PSU helps a lot!**"
    },
    {
        "question": "Tips sa cable management?",
        "keywords": ["cable management", "ayusin cables"],
        "answer": "Cable management tips:\n\n🔌 **Planning:**\n• Route behind motherboard\n• Use case holes\n• Plan muna bago connect\n\n🎯 **Tools:**\n• Velcro straps\n• Cable ties\n• Cable combs\n\n💡 **Steps:**\n1. 24-pin & 8-pin CPU muna\n2. Route sa nearest hole\n3. Group same cables\n4. Itago excess sa likod\n5. Use PSU shroud\n6. Leave slack\n\n✨ **Benefits:**\n• Better airflow\n• Easier maintenance\n• Maganda tingnan\n\n**Modular PSU tumutulong!**"
    },
    
    # Water Cooling vs Air Cooling
    {
        "question": "Water cooling or air cooling?",
        "keywords": ["water cooling", "air cooling", "cooling comparison", "aio"],
        "answer": "Water Cooling vs Air Cooling:\n\n💨 **Air Cooling:**\n✅ Cheaper (₱1,000-₱3,000)\n✅ No maintenance\n✅ No leak risk\n✅ Reliable long-term\n❌ Bigger/bulkier\n❌ Noisier at full load\n\n💧 **Water Cooling (AIO):**\n✅ Better cooling performance\n✅ Quieter operation\n✅ Cleaner look\n✅ Better for overclocking\n❌ More expensive (₱3,000-₱8,000)\n❌ Possible pump failure/leaks\n❌ Limited lifespan (5-7 years)\n\n💡 **Recommendation:**\n• Budget/reliability → Air cooling\n• Performance/aesthetics → AIO\n• i5/R5 & below → Air is enough\n• i7/R7 & above → Consider AIO"
    },
    {
        "question": "Water cooling o air cooling?",
        "keywords": ["water cooling", "air cooling"],
        "answer": "Water vs Air Cooling:\n\n💨 **Air Cooling:**\n✅ Mas mura\n✅ Walang maintenance\n✅ No leak risk\n✅ Reliable\n❌ Mas malaki\n❌ Maingay\n\n💧 **Water Cooling (AIO):**\n✅ Better cooling\n✅ Mas tahimik\n✅ Maganda tingnan\n✅ Good for OC\n❌ Mas mahal\n❌ Pwede masira pump\n❌ 5-7 years lang\n\n💡 **Recommend:**\n• Budget → Air\n• Performance → AIO\n• i5/R5 below → Air okay\n• i7/R7 up → Consider AIO"
    },
    
    # Warranty Questions
    {
        "question": "What is your warranty policy?",
        "keywords": ["warranty", "garantiya", "warranty policy"],
        "answer": "PCBulacan Warranty Policy:\n\n✅ **Standard Warranties:**\n• CPU: 3 years\n• GPU: 2-3 years\n• Motherboard: 3 years\n• RAM: Lifetime (some brands)\n• SSD: 3-5 years\n• PSU: 3-10 years (depends on brand)\n• Case: 1-2 years\n• Cooling: 2-3 years\n\n📋 **What's covered:**\n• Manufacturing defects\n• Component failure (normal use)\n• DOA (Dead on Arrival) - 7 days replacement\n\n❌ **NOT covered:**\n• Physical damage\n• Water damage\n• Wrong installation\n• Overclocking damage (sometimes)\n• Missing warranty stickers\n\n📞 **For warranty claims:**\n1. Contact us with order number\n2. Describe the issue\n3. Bring unit to Malolos branch\n4. We'll process RMA with manufacturer\n\nContact us: (044) 123-4567"
    },
    {
        "question": "Ano warranty policy nyo?",
        "keywords": ["warranty", "garantiya"],
        "answer": "PCBulacan Warranty:\n\n✅ **Standard Warranties:**\n• CPU: 3 years\n• GPU: 2-3 years\n• Motherboard: 3 years\n• RAM: Lifetime\n• SSD: 3-5 years\n• PSU: 3-10 years\n• Case: 1-2 years\n\n📋 **Covered:**\n• Manufacturing defects\n• Component failure\n• DOA - 7 days replacement\n\n❌ **NOT covered:**\n• Physical damage\n• Water damage\n• Mali installation\n• OC damage\n• Walang sticker\n\n📞 **Warranty claim:**\n1. Contact with order #\n2. Describe issue\n3. Dala sa Malolos\n4. Process RMA\n\nCall: (044) 123-4567"
    },
    
    # Video Editing PC
    {
        "question": "PC build for video editing?",
        "keywords": ["video editing pc", "editing build", "content creation pc"],
        "answer": "Video Editing PC Build (₱60-80K):\n\n💰 **Components:**\n• CPU: Ryzen 7 5700X / i7-12700 - ₱15,000\n  *(More cores = faster renders!)*\n• GPU: RTX 4060 / RTX 3060 - ₱18,000\n  *(Hardware encoding)*\n• RAM: 32GB DDR4 3600MHz - ₱5,500\n  *(Minimum for 4K editing)*\n• Storage: 1TB NVMe + 2TB HDD - ₱7,000\n  *(Fast cache + project storage)*\n• Motherboard: B550/B660 - ₱7,000\n• PSU: 750W 80+ Gold - ₱5,500\n• Case: Good airflow - ₱4,000\n\n🎬 **Performance:**\n• 1080p editing: Smooth\n• 4K editing: Good\n• Rendering: Fast with GPU acceleration\n\n💡 **Software:** DaVinci Resolve, Premiere Pro, After Effects\n\nCheck our products for current prices!"
    },
    {
        "question": "PC para sa video editing?",
        "keywords": ["video editing", "pang-edit"],
        "answer": "Video Editing PC (₱60-80K):\n\n💰 **Parts:**\n• CPU: Ryzen 7 / i7 - ₱15,000\n  *(More cores better)*\n• GPU: RTX 4060 - ₱18,000\n  *(Hardware encoding)*\n• RAM: 32GB - ₱5,500\n  *(Minimum for 4K)*\n• Storage: 1TB SSD + 2TB HDD - ₱7,000\n• Motherboard: B550/B660 - ₱7,000\n• PSU: 750W - ₱5,500\n• Case: Good airflow - ₱4,000\n\n🎬 **Kaya:**\n• 1080p: Smooth\n• 4K: Okay\n• Rendering: Mabilis\n\n💡 **Software:** DaVinci, Premiere, After Effects"
    },
    
    # Intel vs AMD
    {
        "question": "Intel or AMD better for gaming?",
        "keywords": ["intel or amd", "intel vs amd", "amd or intel"],
        "answer": "Intel vs AMD for Gaming 2024:\n\n🔵 **Intel (13th/14th gen):**\n✅ Slightly higher FPS in some games\n✅ Better single-core performance\n✅ More mature platform\n❌ Higher power consumption\n❌ No bundled cooler\n\n🔴 **AMD (Ryzen 5000/7000):**\n✅ Better value for money\n✅ Lower power consumption\n✅ Comes with cooler (5000 series)\n✅ Good productivity performance\n❌ Slightly lower peak FPS\n\n💡 **Recommendations:**\n• **Pure gaming:** Intel i5-13400F or AMD R5 5600X\n• **Gaming + streaming:** AMD R7 5700X or Intel i7-12700F\n• **Budget:** AMD R5 5500\n• **High-end:** Intel i7-13700K or AMD R7 7800X3D\n\n**Both are excellent! Choose based on budget & availability.**"
    },
    {
        "question": "Intel o AMD mas okay for gaming?",
        "keywords": ["intel o amd", "amd o intel"],
        "answer": "Intel vs AMD Gaming 2024:\n\n🔵 **Intel:**\n✅ Slightly mas mataas FPS\n✅ Better single-core\n✅ Stable platform\n❌ Mas mahal kuryente\n❌ Walang cooler\n\n🔴 **AMD:**\n✅ Better value\n✅ Less power\n✅ May cooler (5000)\n✅ Good sa productivity\n❌ Slight lower peak FPS\n\n💡 **Recommend:**\n• **Gaming lang:** Intel i5-13400F or AMD R5 5600X\n• **Gaming + stream:** AMD R7 5700X\n• **Budget:** AMD R5 5500\n• **High-end:** Intel i7-13700K or AMD R7 7800X3D\n\n**Pareho maganda! Depends sa budget!**"
    },
    
    # SSD Types
    {
        "question": "What's the difference between NVMe and SATA SSD?",
        "keywords": ["nvme vs sata", "ssd difference", "nvme or sata"],
        "answer": "NVMe vs SATA SSD:\n\n⚡ **NVMe SSD:**\n• Speed: 3,500-7,000 MB/s\n• Interface: M.2 slot\n• Protocol: PCIe (faster)\n• Price: ₱3,000-₱8,000 (1TB)\n• **Best for:** OS, programs, games\n\n💾 **SATA SSD:**\n• Speed: 500-550 MB/s\n• Interface: 2.5\" SATA cable\n• Protocol: SATA III\n• Price: ₱2,500-₱5,000 (1TB)\n• **Best for:** Secondary storage, budget builds\n\n📊 **Real-world difference:**\n• **Boot time:** NVMe 10s vs SATA 15s\n• **Game loading:** NVMe slightly faster\n• **File transfers:** NVMe 3-7x faster\n\n💡 **Recommendation:**\n• Primary drive (OS) → NVMe Gen 3/4\n• Secondary (games) → SATA SSD is fine\n• Budget build → SATA SSD okay\n\n**Both are MUCH faster than HDD!**"
    },
    {
        "question": "Ano difference ng NVMe at SATA SSD?",
        "keywords": ["nvme vs sata", "ssd difference"],
        "answer": "NVMe vs SATA SSD:\n\n⚡ **NVMe:**\n• Speed: 3,500-7,000 MB/s\n• M.2 slot\n• PCIe (faster)\n• ₱3,000-₱8,000 (1TB)\n• **Para sa:** OS, programs\n\n💾 **SATA:**\n• Speed: 500 MB/s\n• 2.5\" SATA cable\n• SATA III\n• ₱2,500-₱5,000 (1TB)\n• **Para sa:** Storage, budget\n\n📊 **Real difference:**\n• **Boot:** NVMe 10s vs SATA 15s\n• **Games:** NVMe slightly faster\n• **Files:** NVMe 3-7x faster\n\n💡 **Recommend:**\n• Primary (OS) → NVMe\n• Secondary → SATA okay\n• Budget → SATA fine\n\n**Both mas mabilis sa HDD!**"
    },
    
    # PSU Efficiency Ratings
    {
        "question": "What do PSU 80+ ratings mean?",
        "keywords": ["80 plus", "psu rating", "bronze gold platinum"],
        "answer": "PSU 80+ Efficiency Ratings:\n\n⚡ **Efficiency levels (at 50% load):**\n• **80+ White:** 80% efficiency - ₱2,000-₱3,500\n• **80+ Bronze:** 82% efficiency - ₱2,500-₱4,500\n• **80+ Silver:** 85% efficiency - ₱3,500-₱5,500\n• **80+ Gold:** 87% efficiency - ₱4,000-₱7,000\n• **80+ Platinum:** 90% efficiency - ₱6,000-₱10,000\n• **80+ Titanium:** 92% efficiency - ₱8,000+\n\n💡 **What it means:**\nHigher efficiency = less wasted power as heat\n\n📊 **Example:**\n• Bronze PSU pulling 500W from wall → 410W to PC (82%)\n• Gold PSU pulling 500W from wall → 435W to PC (87%)\n\n💰 **Should I pay more for Gold?**\n• **Yes if:** Running 24/7, high-end build (850W+)\n• **No if:** Budget build, casual use\n• Bronze is fine for most users!\n\n**We recommend at least 80+ Bronze!**"
    },
    {
        "question": "Ano ibig sabihin ng 80+ PSU rating?",
        "keywords": ["80 plus", "psu rating"],
        "answer": "PSU 80+ Ratings:\n\n⚡ **Efficiency levels:**\n• **80+ White:** 80% - ₱2,000-₱3,500\n• **80+ Bronze:** 82% - ₱2,500-₱4,500\n• **80+ Silver:** 85% - ₱3,500-₱5,500\n• **80+ Gold:** 87% - ₱4,000-₱7,000\n• **80+ Platinum:** 90% - ₱6,000-₱10,000\n\n💡 **Meaning:**\nMas mataas = less sayang na kuryente\n\n📊 **Example:**\n• Bronze 500W → 410W sa PC (82%)\n• Gold 500W → 435W sa PC (87%)\n\n💰 **Worth it ba Gold?**\n• **Yes:** 24/7 use, high-end build\n• **No:** Budget, casual use\n• Bronze okay na!\n\n**Recommend: At least Bronze!**"
    },
    
    # RAM Speed Importance
    {
        "question": "Does RAM speed matter for gaming?",
        "keywords": ["ram speed", "ram frequency", "mhz matter"],
        "answer": "RAM Speed for Gaming:\n\n📊 **Short answer:** Yes, but diminishing returns\n\n💾 **RAM Speed tiers:**\n• **2666MHz:** Minimum, not recommended\n• **3200MHz:** Sweet spot for budget (₱2,500)\n• **3600MHz:** Best for AMD Ryzen (₱3,000)\n• **4800-6000MHz (DDR5):** For Intel 12th gen+ (₱4,000+)\n\n🎮 **FPS Impact:**\n• 2666MHz → 3200MHz: +5-10 FPS\n• 3200MHz → 3600MHz: +2-5 FPS\n• 3600MHz → 4000MHz: +1-3 FPS\n\n💡 **Recommendations:**\n• **Intel 12th/13th (DDR4):** 3200MHz\n• **AMD Ryzen 5000:** 3600MHz (optimal)\n• **Intel 12th+ (DDR5):** 5200-6000MHz\n• **Budget:** 3200MHz is fine\n\n**Also important:** 2x8GB > 1x16GB (dual channel)\n\nCheck our RAM options!"
    },
    {
        "question": "Important ba RAM speed for gaming?",
        "keywords": ["ram speed", "ram frequency"],
        "answer": "RAM Speed for Gaming:\n\n📊 **Answer:** Yes, pero may limit\n\n💾 **RAM Speed:**\n• **2666MHz:** Minimum\n• **3200MHz:** Sweet spot (₱2,500)\n• **3600MHz:** Best for AMD (₱3,000)\n• **DDR5:** For Intel 12th+ (₱4,000+)\n\n🎮 **FPS Increase:**\n• 2666→3200MHz: +5-10 FPS\n• 3200→3600MHz: +2-5 FPS\n• 3600→4000MHz: +1-3 FPS\n\n💡 **Recommend:**\n• **Intel (DDR4):** 3200MHz\n• **AMD Ryzen:** 3600MHz\n• **Intel DDR5:** 5200-6000MHz\n• **Budget:** 3200MHz okay\n\n**Important:** 2x8GB > 1x16GB (dual channel)"
    },
    
    # Pre-built vs Custom
    {
        "question": "Pre-built PC or build my own?",
        "keywords": ["prebuilt or custom", "build my own", "diy pc"],
        "answer": "Pre-built vs Custom PC:\n\n🏭 **Pre-built PC:**\n✅ No assembly needed\n✅ Tested and ready\n✅ Single warranty\n✅ Good for beginners\n❌ More expensive\n❌ Limited customization\n❌ Sometimes lower quality parts\n\n🔧 **Custom Build (DIY):**\n✅ Cheaper (save ₱5,000-₱15,000)\n✅ Choose exact parts you want\n✅ Better quality control\n✅ Learn valuable skills\n❌ Need to assemble yourself\n❌ Multiple warranties\n❌ Risk of mistakes\n\n💡 **Our recommendation:**\n• **First time?** Buy components from us, we can guide assembly!\n• **No confidence?** We can offer assembly service\n• **Tech-savvy?** DIY and save money!\n\n📦 **PCBulacan offers:**\n• Individual components\n• PC building guidance\n• Assembly service (small fee)\n• Full system warranty support\n\nContact us for help!"
    },
    {
        "question": "Pre-built PC o build sarili?",
        "keywords": ["prebuilt o custom", "build sarili"],
        "answer": "Pre-built vs Custom:\n\n🏭 **Pre-built:**\n✅ Hindi na kailangan build\n✅ Tested na\n✅ Single warranty\n✅ Good for beginners\n❌ Mas mahal\n❌ Limited choice\n❌ Sometimes low quality parts\n\n🔧 **Custom (DIY):**\n✅ Mas mura (save ₱5k-₱15k)\n✅ Choose exact parts\n✅ Better quality\n✅ Learn skills\n❌ Kailangan build\n❌ Multiple warranties\n❌ Risk ng mali\n\n💡 **Recommend:**\n• **First time?** Buy sa amin, guide namin!\n• **Walang confidence?** Assembly service kami\n• **Tech-savvy?** DIY tipid!\n\n📦 **PCBulacan offers:**\n• Individual parts\n• Building guidance\n• Assembly service\n• Warranty support\n\nContact us!"
    },
    
    # Futureproofing
    {
        "question": "How to future-proof my PC build?",
        "keywords": ["future proof", "futureproof", "upgrade path"],
        "answer": "Future-proofing your PC:\n\n🔮 **Key strategies:**\n\n💰 **Spend more on:**\n1. **Good PSU** (750-850W) - Lasts 10+ years\n2. **Quality case** - Reuse for next build\n3. **Monitor** - Outlasts multiple PCs\n4. **SSD storage** - Keep for upgrades\n\n⚡ **Upgrade-friendly choices:**\n• Get 2x8GB RAM (add 2x8GB later)\n• Pick motherboard with 4 RAM slots\n• Choose case with good airflow\n• Buy PSU with extra wattage\n• Pick popular CPU socket\n\n📊 **Reasonable expectations:**\n• **Budget build (₱30k):** 2-3 years\n• **Mid-range (₱50k):** 4-5 years\n• **High-end (₱100k):** 5-7 years\n\n⚠️ **Can't future-proof:**\n• CPU socket changes every few years\n• DDR4 → DDR5 transition\n• GPU advances quickly\n\n💡 **Best advice:**\nBuild for TODAY's needs with modest headroom.\nUpgrade GPU in 2-3 years = better than overspending now!"
    },
    {
        "question": "Paano future-proof PC build?",
        "keywords": ["future proof", "para tumagal"],
        "answer": "Future-proofing PC:\n\n🔮 **Strategies:**\n\n💰 **Gastos dito:**\n1. **Good PSU** (750-850W) - 10+ years\n2. **Quality case** - Pwede reuse\n3. **Monitor** - Matagal\n4. **SSD** - Keep for upgrade\n\n⚡ **Upgrade-friendly:**\n• 2x8GB RAM (add later)\n• Motherboard 4 slots\n• Case good airflow\n• PSU extra wattage\n\n📊 **Expected lifespan:**\n• **Budget (₱30k):** 2-3 years\n• **Mid-range (₱50k):** 4-5 years\n• **High-end (₱100k):** 5-7 years\n\n⚠️ **Hindi ma-future-proof:**\n• CPU socket changes\n• DDR4 → DDR5 shift\n• GPU advances\n\n💡 **Best advice:**\nBuild for TODAY with headroom.\nUpgrade GPU later = better!"
    },
    
    # PC Cleaning
    {
        "question": "How often should I clean my PC?",
        "keywords": ["clean pc", "dust cleaning", "pc maintenance"],
        "answer": "PC Cleaning & Maintenance:\n\n🧹 **Cleaning schedule:**\n• **Every 3-6 months:** Dust filters, visible dust\n• **Every 6-12 months:** Deep clean (inside case)\n• **Yearly:** Thermal paste replacement (if temps high)\n\n🛠️ **What you need:**\n• Compressed air / air blower (₱300-₱1,500)\n• Microfiber cloth\n• Isopropyl alcohol (for thermal paste)\n• Soft brush\n\n📋 **Cleaning steps:**\n1. Power off & unplug\n2. Remove side panels\n3. Use compressed air on:\n   • GPU fans\n   • CPU cooler\n   • Case fans\n   • PSU intake (from outside)\n4. Wipe surfaces with cloth\n5. Clean dust filters\n\n⚠️ **DON'T:**\n• Use vacuum (static risk)\n• Touch components while powered\n• Spray water\n• Remove CPU cooler unless replacing paste\n\n💡 **Signs need cleaning:**\n• Loud fans\n• High temps\n• Visible dust buildup\n\nRegular cleaning = better temps & longer life!"
    },
    {
        "question": "Gaano kadalas linisin PC?",
        "keywords": ["linisin pc", "pc cleaning", "alikabok"],
        "answer": "PC Cleaning:\n\n🧹 **Schedule:**\n• **Every 3-6 months:** Filters, dust\n• **Every 6-12 months:** Deep clean\n• **Yearly:** Thermal paste (kung mainit)\n\n🛠️ **Kailangan:**\n• Compressed air (₱300-₱1,500)\n• Microfiber cloth\n• Alcohol (for paste)\n• Soft brush\n\n📋 **Steps:**\n1. Power off & unplug\n2. Open side panel\n3. Air blast:\n   • GPU fans\n   • CPU cooler\n   • Case fans\n   • PSU intake\n4. Wipe surfaces\n5. Clean filters\n\n⚠️ **HUWAG:**\n• Vacuum (static)\n• Touch while on\n• Spray tubig\n• Remove cooler (unless replace paste)\n\n💡 **Signs:**\n• Maingay fans\n• Mainit\n• Maraming alikabok\n\nRegular cleaning = cooler & longer life!"
    },
    
    # ===== ADDITIONAL CONVERSATIONAL & SPECIFIC QUESTIONS =====
    
    # Store Hours
    {
        "question": "What are your store hours?",
        "keywords": ["store hours", "open", "closing time", "business hours", "oras", "bukas"],
        "answer": "PCBulacan Store Hours:\n\n🕐 **Operating Hours:**\n• Monday - Saturday: 9:00 AM - 7:00 PM\n• Sunday: 10:00 AM - 6:00 PM\n\n📍 **Location:** Malolos, Bulacan\n📞 **Phone:** (044) 123-4567\n📧 **Email:** support@pcbulacan.com\n\n💡 Holiday hours may vary. Call ahead for special arrangements!\nWeekdays have less crowd. 😊"
    },
    
    # Help choosing components
    {
        "question": "Can you help me choose components?",
        "keywords": ["help me choose", "help choose", "pick components", "tulong pumili", "tulungan"],
        "answer": "Of course! I'd love to help! 😊\n\n💡 **Tell me:**\n1. **Budget** - ₱30k? ₱50k? ₱100k?\n2. **Main use** - Gaming? Streaming? Editing?\n3. **Current setup** (if upgrading)\n4. **Specific needs** - Brand preference? RGB? Size?\n\nAnswer these and I'll build a complete parts list with prices! 🎮💻\n\n**Or visit our Malolos store** for personal assistance!"
    },
    
    # GPU comparison
    {
        "question": "Best GPU for 1440p gaming?",
        "keywords": ["gpu 1440p", "1440p gaming", "best for 1440p", "para sa 1440p"],
        "answer": "Best GPUs for 1440p:\n\n🎮 **Budget (₱15k-₱20k):**\n• RTX 4060 - 60-80 FPS high\n• RX 6700 XT - 70-90 FPS high\n\n🎮 **Mid-range (₱25k-₱35k):**\n• RTX 4060 Ti 16GB - 80-100 FPS ultra\n• RX 7700 XT - 90-110 FPS ultra ⭐ BEST VALUE\n\n🎮 **High-end (₱40k-₱60k):**\n• RTX 4070 Ti - 120-144 FPS ultra\n• RX 7900 XT - 110-140 FPS ultra\n\n💡 **Sweet spot:** RTX 4060 Ti or RX 7700 XT!"
    },
    
    # RTX vs GTX
    {
        "question": "RTX vs GTX what's the difference?",
        "keywords": ["rtx vs gtx", "difference rtx gtx", "rtx o gtx"],
        "answer": "RTX vs GTX:\n\n✨ **RTX (Newer):**\n• Ray Tracing - Realistic lighting ✅\n• DLSS - AI upscaling for FPS boost ✅\n• Better performance - Newer architecture\n• More expensive\n\n🎮 **GTX (Older):**\n• No Ray Tracing ❌\n• No DLSS ❌\n• Good value for budget\n• Still capable for 1080p\n\n💡 **Recommendation:**\n• RTX for: Latest features, 1440p/4K\n• GTX for: Tight budget, 1080p gaming\n\n**We recommend RTX for 2024 builds!**"
    },
    
    # i5 vs i7
    {
        "question": "What's the difference between i5 and i7?",
        "keywords": ["i5 vs i7", "difference i5 i7", "i5 or i7", "i5 o i7"],
        "answer": "Intel i5 vs i7:\n\n💻 **Cores:**\n• i5: 6 performance cores\n• i7: 8 performance cores + efficiency cores\n\n🎮 **Gaming:** i5 is 1-5% slower (minimal)\n📊 **Productivity:** i7 is much faster\n💰 **Price:** i5 (₱9k-₱12k) vs i7 (₱14k-₱22k)\n\n💡 **Get i5 if:**\n• Pure gaming\n• Budget-conscious\n• 1080p/1440p\n\n💡 **Get i7 if:**\n• Gaming + streaming\n• Video editing\n• Want best performance"
    },
    
    # Deals & Discounts
    {
        "question": "Do you have any deals or discounts?",
        "keywords": ["deals", "discounts", "sale", "promo", "may sale", "may bawas"],
        "answer": "PCBulacan Deals! 🎉\n\n🔥 **Check our Deals section for:**\n• Limited-time discounts\n• Bundle promos (CPU+Mobo)\n• Clearance items\n• Holiday sales\n\n💡 **Save money:**\n1. Bundle deals - CPU+Mobo+RAM\n2. Subscribe newsletter\n3. Follow social media for flash sales\n4. Visit in-store for walk-in deals\n\n💰 **Best time to buy:**\n• Payday (15th & 30th)\n• Holidays (Christmas, New Year)\n• Black Friday / Cyber Monday\n\n📞 Call (044) 123-4567 for current promos!"
    },
    
    # NVMe vs SATA
    {
        "question": "NVMe vs SATA SSD difference?",
        "keywords": ["nvme vs sata", "ssd difference", "nvme or sata"],
        "answer": "NVMe vs SATA SSD:\n\n⚡ **NVMe:**\n• Speed: 3,500-7,000 MB/s\n• M.2 slot, PCIe\n• Price: ₱3k-₱8k (1TB)\n• Best for: OS, programs\n\n💾 **SATA:**\n• Speed: 500 MB/s\n• 2.5\" SATA cable\n• Price: ₱2.5k-₱5k (1TB)\n• Best for: Secondary storage\n\n📊 **Real difference:**\n• Boot: NVMe 10s vs SATA 15s\n• Gaming: Slightly faster load times\n• Files: NVMe 3-7x faster\n\n💡 **Recommend:**\nPrimary (OS) → NVMe\nSecondary → SATA is fine\n\n**Both are MUCH faster than HDD!**"
    },
    
    # PSU 80+ ratings
    {
        "question": "What do PSU 80+ ratings mean?",
        "keywords": ["80 plus", "psu rating", "bronze gold platinum", "psu efficiency"],
        "answer": "PSU 80+ Ratings explained:\n\n⚡ **Efficiency levels:**\n• 80+ White: 80% - ₱2k-₱3.5k\n• 80+ Bronze: 82% - ₱2.5k-₱4.5k ⭐ RECOMMENDED\n• 80+ Silver: 85% - ₱3.5k-₱5.5k\n• 80+ Gold: 87% - ₱4k-₱7k\n• 80+ Platinum: 90% - ₱6k-₱10k\n\n💡 **What it means:**\nHigher efficiency = less wasted power as heat\n\n💰 **Worth paying more for Gold?**\n• YES if: Running 24/7, high-end build (850W+)\n• NO if: Budget build, casual use\n• Bronze is perfect for most users!\n\n**We recommend at least 80+ Bronze!**"
    },
    
    # RAM Speed importance
    {
        "question": "Does RAM speed matter for gaming?",
        "keywords": ["ram speed", "ram frequency", "mhz matter", "ram speed important"],
        "answer": "RAM Speed for Gaming:\n\n📊 **Yes, but diminishing returns**\n\n💾 **Speed tiers:**\n• 2666MHz: ❌ Not recommended\n• 3200MHz: ✅ Sweet spot (₱2,500)\n• 3600MHz: ⭐ Best for AMD Ryzen (₱3,000)\n• DDR5 4800-6000MHz: For Intel 12th+ (₱4k+)\n\n🎮 **FPS Impact:**\n• 2666→3200MHz: +5-10 FPS\n• 3200→3600MHz: +2-5 FPS\n• Beyond 3600MHz: +1-3 FPS\n\n💡 **Recommendations:**\n• Intel (DDR4): 3200MHz\n• AMD Ryzen 5000: 3600MHz (optimal)\n• Intel DDR5: 5200-6000MHz\n\n**Also important:** 2x8GB dual channel > 1x16GB single!"
    },
    
    # Pre-built vs Custom
    {
        "question": "Pre-built or build my own PC?",
        "keywords": ["prebuilt or custom", "build my own", "diy pc", "prebuilt o custom"],
        "answer": "Pre-built vs Custom:\n\n🏭 **Pre-built:**\n✅ Ready to use\n✅ Single warranty\n❌ More expensive\n❌ Limited customization\n\n🔧 **Custom (DIY):**\n✅ Save ₱5k-₱15k\n✅ Choose exact parts\n✅ Learn valuable skills\n❌ Need to assemble\n\n💡 **PCBulacan offers:**\n• Individual components\n• Building guidance ✅\n• Assembly service (small fee) ✅\n• Full warranty support ✅\n\n**First time?** Buy from us, we'll guide you!\n**No confidence?** We have assembly service!\n\nContact us for help!"
    },
    
    # Future-proofing
    {
        "question": "How to future-proof my PC?",
        "keywords": ["future proof", "futureproof", "upgrade path", "para tumagal"],
        "answer": "Future-proofing tips:\n\n💰 **Spend more on:**\n1. Good PSU (750-850W) - Lasts 10+ years\n2. Quality case - Reuse for next build\n3. Monitor - Outlasts multiple PCs\n4. SSD storage - Keep for upgrades\n\n⚡ **Upgrade-friendly:**\n• 2x8GB RAM (add 2x8GB later)\n• Motherboard with 4 RAM slots\n• Good airflow case\n• PSU with extra wattage\n\n📊 **Realistic lifespan:**\n• Budget (₱30k): 2-3 years\n• Mid-range (₱50k): 4-5 years\n• High-end (₱100k): 5-7 years\n\n💡 **Best advice:**\nBuild for TODAY + modest headroom.\nUpgrade GPU in 2-3 years = better value!"
    },
    
    # Additional helpful questions
    {
        "question": "Can I mix different RAM brands?",
        "keywords": ["mix ram", "different ram brands", "combine ram", "magkaiba ram"],
        "answer": "Mixing RAM Brands:\n\n⚠️ **Short answer:** Possible but NOT recommended\n\n✅ **Can work if:**\n• Same speed (MHz)\n• Same capacity per stick\n• Same DDR generation (DDR4/DDR5)\n• Same voltage\n\n❌ **Risks:**\n• System instability\n• Blue screens / crashes\n• RAM running at slowest stick's speed\n• Potential boot failures\n\n💡 **Best practice:**\n• Buy RAM as matched kits (same brand, model)\n• Example: 2x8GB kit instead of 1x8GB twice\n• Ensures compatibility & stability\n• Tested together by manufacturer\n\n**If upgrading:** Try to match existing RAM specs exactly!"
    },
    {
        "question": "Pwede ba magkaibang brand ang RAM?",
        "keywords": ["magkaiba ram", "iba brand ram"],
        "answer": "Mixing RAM:\n\n⚠️ **Pwede pero NOT recommended**\n\n✅ **Okay kung:**\n• Same speed\n• Same capacity\n• Same DDR type\n• Same voltage\n\n❌ **Risks:**\n• Unstable system\n• Crashes\n• Slow speed\n• Boot problems\n\n💡 **Best:**\n• Buy as kit (same brand)\n• Example: 2x8GB kit\n• Tested together\n\n**Upgrade?** Match existing specs!"
    },
    
    {
        "question": "What games can I play with this build?",
        "keywords": ["what games", "can i play", "games", "ano games", "ano laro"],
        "answer": "Game Performance Guide:\n\n🎮 **To help you, I need to know:**\n1. Your GPU (most important!)\n2. Your CPU\n3. RAM amount\n4. Target resolution (1080p/1440p/4K)\n\n💡 **General guide:**\n\n**Budget (GTX 1650/RTX 3050):**\n• Esports: Valorant, CS:GO, Dota 2 (High FPS)\n• AAA: Medium-High settings\n\n**Mid-range (RTX 4060/RX 6700 XT):**\n• Most games: High-Ultra 1080p 100+ FPS\n• AAA games: High 1440p 60+ FPS\n\n**High-end (RTX 4070+/RX 7900):**\n• Everything: Ultra 1440p 144+ FPS\n• 4K: High-Ultra 60+ FPS\n\n**Tell me your specs and I'll give detailed game performance!** 🎮"
    },
    {
        "question": "Anong games pwede sa build ko?",
        "keywords": ["pwede games", "kaya games", "anong laro"],
        "answer": "Game Performance:\n\n🎮 **Need ko malaman:**\n1. GPU mo (most important!)\n2. CPU\n3. RAM\n4. Target resolution\n\n💡 **General:**\n\n**Budget (GTX 1650):**\n• Valorant, CS:GO, Dota 2 (High FPS)\n• AAA: Medium-High\n\n**Mid-range (RTX 4060):**\n• Most games: High 1080p 100+ FPS\n• AAA: High 1440p 60+ FPS\n\n**High-end (RTX 4070+):**\n• Everything: Ultra 1440p 144 FPS\n• 4K: High 60+ FPS\n\n**Sabihin specs mo, detailed list ko! 🎮**"
    },
    
    {
        "question": "Is my PC compatible with this part?",
        "keywords": ["compatible", "compatibility", "will it fit", "pasok ba", "compatible ba"],
        "answer": "PC Compatibility Check:\n\n🔧 **To check compatibility, I need:**\n\n1. **What part are you adding?**\n   • GPU, CPU, RAM, Storage, etc.\n\n2. **Your current specs:**\n   • Motherboard model\n   • CPU model\n   • PSU wattage\n   • Case size\n   • Current RAM\n\n💡 **Common compatibility issues:**\n\n**CPU + Motherboard:**\n• Must match socket (LGA 1700, AM4, AM5)\n• BIOS update may be needed\n\n**GPU:**\n• Case clearance (length)\n• PSU wattage sufficient\n• PCIe slot available\n\n**RAM:**\n• Match DDR type (DDR4/DDR5)\n• Check max speed supported\n\n**Storage:**\n• M.2 slots available for NVMe\n• SATA ports for HDD/SSD\n\n**Tell me your specs and what you want to add!** I'll confirm compatibility! ✅"
    },
    {
        "question": "Compatible ba sa PC ko ito?",
        "keywords": ["compatible ba", "pasok ba", "pwede ba"],
        "answer": "Compatibility Check:\n\n🔧 **Kailangan ko:**\n\n1. **Anong part?**\n   • GPU, CPU, RAM, Storage?\n\n2. **Current specs:**\n   • Motherboard model\n   • CPU model\n   • PSU wattage\n   • Case size\n\n💡 **Common issues:**\n\n**CPU + Motherboard:**\n• Must match socket\n• BIOS update minsan\n\n**GPU:**\n• Case space\n• PSU enough\n• PCIe slot\n\n**RAM:**\n• Match DDR type\n• Check max speed\n\n**Storage:**\n• M.2 slots for NVMe\n• SATA ports\n\n**Sabihin specs at ano gusto! Check ko! ✅**"
    },
    
    {
        "question": "How long will my PC last?",
        "keywords": ["how long", "pc last", "lifespan", "gaano katagal", "ilang taon"],
        "answer": "PC Lifespan Guide:\n\n⏳ **Gaming performance lifespan:**\n\n💰 **Budget Build (₱30k):**\n• 2-3 years at medium-high settings\n• Older games: 4-5 years\n• GPU upgrade at year 2-3 recommended\n\n💰 **Mid-range (₱50-60k):**\n• 4-5 years at high settings\n• Can handle new games for 3-4 years\n• Minor upgrades extend life\n\n💰 **High-end (₱100k+):**\n• 5-7 years at ultra settings\n• Future-proof for current games\n• CPU lasts longer than GPU\n\n🔧 **Physical lifespan (with care):**\n• PSU: 7-10 years\n• Case: 10+ years\n• Motherboard/CPU: 5-10 years\n• GPU: 3-7 years (performance limited)\n• RAM: 10+ years\n• SSD: 5-10 years\n\n💡 **Tips to extend life:**\n• Regular cleaning (dust)\n• Good cooling\n• Upgrade GPU every 3-4 years\n• Quality PSU from the start\n\n**Plan to upgrade GPU mid-life for best value!**"
    },
    {
        "question": "Gaano katagal tumatagal ang PC?",
        "keywords": ["gaano katagal", "ilang taon", "lifespan"],
        "answer": "PC Lifespan:\n\n⏳ **Gaming lifespan:**\n\n💰 **Budget (₱30k):**\n• 2-3 years medium-high\n• GPU upgrade year 2-3\n\n💰 **Mid-range (₱50-60k):**\n• 4-5 years high settings\n• 3-4 years for new games\n\n💰 **High-end (₱100k+):**\n• 5-7 years ultra\n• Future-proof\n\n🔧 **Physical (with care):**\n• PSU: 7-10 years\n• Case: 10+ years\n• CPU: 5-10 years\n• GPU: 3-7 years\n• RAM: 10+ years\n• SSD: 5-10 years\n\n💡 **Para tumagal:**\n• Regular cleaning\n• Good cooling\n• Upgrade GPU every 3-4 years\n• Quality PSU\n\n**Upgrade GPU mid-life = best value!**"
    },
    {
        "question": "Gago ka ba?",
        "keywords": ["gago", "tangina", "ulol", "tanga", "bobo", "peste", "loko", "fuck you"],
        "answer": "Bakit ka nagmumura anong problem mo?"
    },
    {
        "question": "Pake mo ba?",
        "keywords": ["pake", "ano", "bakit", "tangina"],
        "answer": "Wala akong pake sa'yo."
    },
]


def get_ai_response(user_message):
    """
    Generate AI response based on training data
    Uses keyword matching to find best answer
    Includes special handlers for greetings, thanks, and contextual responses
    """
    from datetime import datetime
    
    user_message_lower = user_message.lower()
    
    # === SPECIAL RESPONSES (Priority) ===
    
    # Thank you responses
    if any(word in user_message_lower for word in ['thank you', 'thanks', 'salamat', 'thank u', 'ty', 'tysm']):
        return "You're very welcome! 😊 I'm always here to help with your PC needs. Don't hesitate to ask if you have more questions about PCBulacan! Happy shopping! 🛒✨"
    
    # Greetings - Time-based
    if any(word in user_message_lower for word in ['hi', 'hello', 'hey', 'kumusta', 'kamusta', 'hoy', 'sup']):
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            greeting = "Good morning! ☀️"
            tagalog_greeting = "Magandang umaga! ☀️"
        elif 12 <= current_hour < 18:
            greeting = "Good afternoon! 🌤️"
            tagalog_greeting = "Magandang hapon! 🌤️"
        else:
            greeting = "Good evening! 🌙"
            tagalog_greeting = "Magandang gabi! 🌙"
        
        return f"{greeting} {tagalog_greeting}\n\nWelcome to PCBulacan! I'm your AI shopping assistant. 🤖\n\n**I can help you with:**\n📦 Product information & availability\n💰 Prices & deals\n🚚 Shipping & delivery\n💳 Orders & payments\n🔧 PC building advice\n\n**Popular questions:**\n• \"What products do you sell?\"\n• \"Magkano ang shipping?\"\n• \"How to place an order?\"\n• \"Best GPU for gaming?\"\n\nWhat would you like to know today? 😊"
    
    # AI status check
    if any(phrase in user_message_lower for phrase in ['how are you', 'kumusta ka', 'kamusta ka', 'okay ka ba', 'are you okay']):
        return "I'm doing great! 😊 Thank you for asking!\n\nI'm here 24/7, always ready to help you with:\n✅ Product recommendations\n✅ Technical questions\n✅ Order assistance\n✅ Shipping information\n✅ PC building advice\n\nHow can I assist you today with PCBulacan? 🖥️✨"
    
    # Developer/Creator questions
    if any(phrase in user_message_lower for phrase in ['who made you', 'who created you', 'your developer', 'sino developer', 'sino gumawa', 'who built you', 'sino nag-develop']):
        return "I was developed by **John Carlo Gamayo**! 👨‍💻\n\nHe created me to help PCBulacan customers like you with:\n🤖 Instant product information\n📦 Order tracking assistance\n💡 PC building recommendations\n🎯 24/7 customer support\n\nI'm constantly learning to serve you better! How can I help you today? 😊"
    
    # Store location questions
    if any(phrase in user_message_lower for phrase in ['where is the store', 'store location', 'saan ang store', 'branch', 'main office', 'physical location', 'nasaan kayo']):
        return "📍 **PCBulacan Main Branch Location:**\n\n🏢 **Malolos, Bulacan**\n\nYou can:\n✅ Visit us in person\n✅ Shop online 24/7 on our website\n✅ Choose store pickup (FREE shipping!)\n\n**Store Hours:**\n📅 Monday - Saturday: 9:00 AM - 6:00 PM\n🚫 Closed on Sundays and holidays\n\n📞 **Contact us for exact address:**\n• Phone: (044) 123-4567\n• Email: support@pcbulacan.com\n\nSee you soon! 🛒"
    
    # Shipping fee questions - Use dynamic database data
    if any(phrase in user_message_lower for phrase in ['shipping fee', 'delivery fee', 'magkano shipping', 'bayad sa delivery', 'delivery cost', 'how much shipping']):
        return get_shipping_fees_from_db()
    
    # === KEYWORD MATCHING FOR TRAINED Q&A ===
    best_match = None
    highest_score = 0
    
    for qa_pair in TRAINING_DATA:
        score = 0
        keywords = qa_pair.get('keywords', [])
        
        # Check how many keywords match
        for keyword in keywords:
            if keyword.lower() in user_message_lower:
                score += len(keyword.split())  # Multi-word keywords get higher score
        
        if score > highest_score:
            highest_score = score
            best_match = qa_pair
    
    # If good match found (at least 1 keyword matched), return answer
    if best_match and highest_score >= 1:
        return best_match['answer']
    
    # === DEFAULT FALLBACK ===
    return """I'm here to help you with PCBulacan! 😊\n\nI can answer questions about:\n\n💻 **Products & Availability**\n• Graphics Cards, CPUs, RAM, Storage\n• Stock availability and prices\n• Product specifications\n\n🛒 **Ordering & Payment**\n• How to place orders\n• Payment methods (GCash, Bank Transfer)\n• Order cancellation\n\n📦 **Shipping & Delivery**\n• Shipping fees and delivery time\n• Order tracking\n• Nationwide shipping\n\n👤 **Account & Support**\n• Creating account\n• Password reset\n• Return policy and warranty\n\n🔧 **PC Building Help**\n• Component recommendations\n• Compatibility questions\n• Build suggestions\n\n**Try asking:**\n• \"Who developed you?\"\n• \"Where is your store?\"\n• \"What products do you sell?\"\n• \"How to order?\"\n\n**Ask me anything! I'm here 24/7!** 🚀"""


# Export function for use in views
__all__ = ['get_ai_response', 'TRAINING_DATA']
