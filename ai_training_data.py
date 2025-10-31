"""
AI Chat Support Training Data for PCBulacan
Comprehensive Q&A pairs in English and Tagalog - 50+ Questions
"""

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
    {
        "question": "How much is the shipping fee?",
        "keywords": ["shipping fee", "delivery fee", "how much shipping"],
        "answer": "Shipping fees vary by location! During checkout:\n1. Enter your complete address\n2. Shipping fee will be calculated automatically\n3. Based on your province/city\n\nFees are competitive and transparent! 📦✨"
    },
    {
        "question": "Do you ship nationwide?",
        "keywords": ["nationwide", "ship nationwide", "deliver nationwide"],
        "answer": "Yes! We ship to all provinces in the Philippines! 🇵🇭\n\n📍 Luzon ✅\n📍 Visayas ✅\n📍 Mindanao ✅\n\nShipping fees calculated based on location. We use reliable courier services!"
    },
    {
        "question": "How long is the delivery time?",
        "keywords": ["delivery time", "how long delivery", "shipping time"],
        "answer": "Delivery time by location:\n📍 Metro Manila: 2-3 days\n📍 Luzon: 3-5 days\n📍 Visayas: 4-6 days\n📍 Mindanao: 5-7 days\n\nTracking information provided once shipped! 📦"
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
    {
        "question": "Magkano ang shipping fee?",
        "keywords": ["magkano shipping", "shipping fee", "delivery fee"],
        "answer": "Depende sa location ang shipping! Sa checkout:\n1. I-enter ang complete address\n2. Automatic na maca-calculate\n3. Based sa province/city\n\nCompetitive at transparent ang fees! 📦✨"
    },
    {
        "question": "Nag-ship ba kayo nationwide?",
        "keywords": ["nationwide", "buong pilipinas"],
        "answer": "Oo! Nag-ship kami sa buong Philippines! 🇵🇭\n\n📍 Luzon ✅\n📍 Visayas ✅\n📍 Mindanao ✅\n\nReliable courier services gamit namin!"
    },
    {
        "question": "Gaano katagal ang delivery?",
        "keywords": ["gaano katagal", "delivery time"],
        "answer": "Delivery time by location:\n📍 Metro Manila: 2-3 days\n📍 Luzon: 3-5 days\n📍 Visayas: 4-6 days\n📍 Mindanao: 5-7 days\n\nMay tracking info once shipped! 📦"
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
]


def get_ai_response(user_message):
    """
    Generate AI response based on training data
    Uses keyword matching to find best answer
    """
    user_message_lower = user_message.lower()
    
    # Find best matching Q&A pair based on keywords
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
    
    # Default response if no good match
    return """I'm here to help you with PCBulacan! 😊\n\nI can answer questions about:\n\n💻 **Products & Availability**\n• Graphics Cards, CPUs, RAM, Storage\n• Stock availability and prices\n• Product specifications\n\n🛒 **Ordering & Payment**\n• How to place orders\n• Payment methods (GCash, Bank Transfer)\n• Order cancellation\n\n📦 **Shipping & Delivery**\n• Shipping fees and delivery time\n• Order tracking\n• Nationwide shipping\n\n👤 **Account & Support**\n• Creating account\n• Password reset\n• Return policy and warranty\n\n🔧 **PC Building Help**\n• Component recommendations\n• Compatibility questions\n• Build suggestions\n\n**Ask me anything! I'm here 24/7!** 🚀\n\n---\n\nNandito ako para tumulong! 😊\n\nPwede ako magtanong tungkol sa:\n\n💻 **Mga Produkto**\n🛒 **Pag-order at Bayad**\n📦 **Shipping at Delivery**\n👤 **Account at Support**\n🔧 **PC Building Tulong**\n\n**Magtanong lang! Andito ako 24/7!** 🚀"""


# Export function for use in views
__all__ = ['get_ai_response', 'TRAINING_DATA']
