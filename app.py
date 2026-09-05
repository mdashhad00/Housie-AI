"""
Housie AI — Ultra-Smart Python Backend v4.0
Flask + SymPy powered AI with:
- SymPy Computer Algebra System for ANY math question
- Massive 50+ topic knowledge base
- Bilingual English/Hinglish
- Joke, motivation, fun fact banks
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import math, re, os, random, datetime

# SymPy for REAL mathematical solving power
try:
    import sympy
    from sympy import (
        symbols, solve, simplify, factor, expand, sqrt, cbrt,
        sin, cos, tan, asin, acos, atan, sec, csc, cot,
        log, ln, exp, pi, E, oo, I,
        Rational, factorial, binomial, gcd, lcm,
        isprime, nextprime, prevprime, primerange, factorint,
        diff, integrate, limit, summation, product,
        Matrix, det, Eq, solveset, S,
        latex, N, sympify
    )
    from sympy.parsing.sympy_parser import (
        parse_expr, standard_transformations,
        implicit_multiplication_application,
        convert_xor, function_exponentiation
    )
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
CORS(app)

# ═══════════════════════════════════════════
#   LANGUAGE DETECTION
# ═══════════════════════════════════════════
HINGLISH_WORDS = set(['kya','hai','bhai','yaar','ek','do','teen','mera','tera','aaj','kal',
    'kaise','kaisa','karo','batao','kuch','nahi','haan','achha','accha','matlab',
    'toh','bhi','se','ka','ki','ke','mein','hoon','kab','kahan','kyun','zaroor',
    'bilkul','lekin','aur','par','mujhe','tumhe','apna','apni','koi','sab','sirf',
    'wala','wali','raha','gaya','gayi','shukriya','namaste','alvida','bolo','sun',
    'suno','bol','bata','kitna','hoga','kaun','kon','dedo','dekho','lelo','sunao',
    'banaya','isko','uska','unka','jab','tab','yeh','woh','hum','tum','main','aap'])

def detect_lang(text):
    words = text.lower().split()
    if not words:
        return 'english'
    count = sum(1 for w in words if w in HINGLISH_WORDS)
    return 'hinglish' if (count / len(words)) >= 0.12 else 'english'

def pick(arr):
    return random.choice(arr)

# ═══════════════════════════════════════════
#   CONTENT BANKS
# ═══════════════════════════════════════════
CREATOR_EN = "🔥 Oof, bold question! I was forged from raw code by a **16-year-old absolute genius** — a coding prodigy who writes blazing algorithms with his bare naked hands, continuously, without stopping, without touching grass, without sleeping. He is basically a human supercomputer who decided to build me instead of doing anything normal. Respect the legend. ⚡💻🚀"
CREATOR_HI = "😤 Bhai, ek 16-saal ka coding prodigy ne mujhe banaya hai! Woh ek aisa genius hai jo apne **nange haathon se** continuously raw algorithms likhta hai — bina soye, bina grass touch kiye, bina break liye! Woh basically ek insaan ke roop mein ek supercomputer hai. Usse salaam karo bhai! ⚡💻🔥"

JOKES_EN = [
    # ── User Curated 50 English Jokes ──
    "Why don't scientists trust atoms? Because they make up everything! ⚛️😂",
    "What do you call a fake noodle? An impasta! 🍝😂",
    "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾😂",
    "Why don't skeletons fight each other? They don't have the guts! 💀😂",
    "What do you call cheese that isn't yours? Nacho cheese! 🧀😂",
    "Why did the bicycle fall over? Because it was two tired! 🚲😂",
    "What do you call a bear with no teeth? A gummy bear! 🐻😂",
    "How does a penguin build its house? Igloos it together! 🐧❄️😂",
    "What did one wall say to the other? I'll meet you at the corner! 🧱😂",
    "Why did the math book look sad? Because it had too many problems! 📚😅",
    "What do you call a factory that makes okay products? A satisfactory! 🏭😂",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one! ⛳😂",
    "What did the ocean say to the beach? Nothing, it just waved! 🌊😂",
    "Why do bees have sticky hair? Because they use a honeycomb! 🐝🍯😂",
    "What do you call a cow with no legs? Ground beef! 🐄😂",
    "Why did the tomato turn red? Because it saw the salad dressing! 🍅😂",
    "What do you call a dog that does magic tricks? A labracadabrador! 🐶✨😂",
    "Why don't eggs tell jokes? Because they'd crack each other up! 🥚😂",
    "What did the left eye say to the right eye? Between you and me, something smells! 👁️👃😂",
    "Why did the cookie go to the hospital? Because it felt crummy! 🍪🏥😂",
    "What do you call a snowman with a six-pack? An abdominal snowman! ⛄💪😂",
    "Why are ghosts bad liars? Because you can see right through them! 👻😂",
    "What did one hat say to the other? You wait here, I'll go on ahead! 🎩😂",
    "Why did the picture go to jail? Because it was framed! 🖼️⚖️😂",
    "What do you call a sleeping dinosaur? A dino-snore! 🦖💤😂",
    "Why do seagulls fly over the ocean? Because if they flew over the bay, they'd be bagels! 🥖😂",
    "What did the zero say to the eight? Nice belt! 0️⃣8️⃣😂",
    "Why did the computer go to the doctor? Because it had a virus! 💻🤒😂",
    "What do you call a fish wearing a bowtie? Sofishticated! 🐟👔😂",
    "What do you get when you cross a vampire and a snowman? Frostbite! 🧛❄️😂",
    "Why do ducks have feathers? To cover their butt-quacks! 🦆😂",
    "What do you call a lazy kangaroo? A pouch potato! 🦘🥔😂",
    "Why did the man put his money in the freezer? He wanted cold hard cash! 💵🧊😂",
    "What has ears but cannot hear? A cornfield! 🌽😂",
    "Why did the tree go to the dentist? To get a root canal! 🌳🦷😂",
    "What do you call a bear in the rain? A drizzly bear! 🐻🌧️😂",
    "Why are elevator jokes so classic? They work on many levels! 🛗😂",
    "What do you call a pony with a cough? A little horse! 🐴😂",
    "Why did the student eat his homework? Because the teacher told him it was a piece of cake! 🍰📚😂",
    "What do you call an alligator in a vest? An investigator! 🐊🕵️😂",
    "Why did the invisible man turn down the job offer? He couldn't see himself doing it! 👔😂",
    "What do you get if you cross a cat with a dark horse? Kitty Perry! 🐱🎤😂",
    "Why did the coffee file a police report? It got mugged! ☕🚓😂",
    "What do you call a can opener that doesn't work? A can't opener! 🥫😂",
    "Why did the belt get arrested? For holding up the pants! 👖🚨😂",
    "What do you call a funny mountain? Hill-arious! ⛰️😂",
    "Why did the teddy bear say no to dessert? Because it was already stuffed! 🧸🍰😂",
    "What do you call a group of musical whales? An orca-stra! 🐋🎻😂",
    "Why do melons have weddings? Because they cantaloupe! 🍈💍😂",
    "What do you call a bee that can't make up its mind? A maybe! 🐝🤔😂",
    # ── Tech & Geek Classics ──
    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛😂",
    "I told my computer I needed a break. Now it won't stop sending me vacation ads! 🏖️😂",
    "Why do Java developers wear glasses? Because they don't C#! 👓😂",
    "A SQL query walks into a bar and asks two tables: 'Can I join you?' 🍺😂",
    "How many programmers does it take to change a light bulb? None — that's a hardware problem! 💡😂",
    "Debugging is like being the detective in a crime movie where you are also the murderer! 🔍😂",
    "Why did the programmer quit his job? Because he didn't get arrays (a raise)! 💰😂",
    "There are only 10 types of people: those who understand binary and those who don't! 🖥️😂",
    "Parallel lines have so much in common. It's a shame they'll never meet! 📐😂",
    "!false — it's funny because it's true! 😂",
    "To understand recursion, you must first understand recursion! 🔄😂",
]

JOKES_HI = [
    # ── User Curated 50 Hindi Jokes ──
    "Teacher: Homework kyun nahi kiya?\nStudent: Sir, main hostel mein rehta hoon, wahan 'home'work kaise karu? 🏠😂",
    "Santa: Bhai, tu kal itna kyu bhaag raha tha?\nBanta: Arre, main kutton ki race mein hissa le raha tha!\nSanta: Toh kya jeeta?\nBanta: Nahi, main third aaya! 🐕🥉😂",
    "Ek machhar ne doosre machhar se kaha: 'Bhai, insaan kitne acche hote hain na, khoon peene ke baad taaliyan bajate hain!' 🦟👏😂",
    "Boss: Tumhe office aane mein itni deri kyun hui?\nEmployee: Sir, raaste mein board laga tha 'Drive Slow'! 🚗🐢😂",
    "Wife: Aji sunte ho, meri skin kitni soft aur glow kar rahi hai.\nHusband: Haan, barish ke baad mendhak bhi aise hi chamakte hain! 🐸✨😂",
    "Boy: Tum mujhe kitna chahti ho?\nGirl: Jitna tum mujhe chahte ho.\nBoy: Iska matlab tu bhi time pass hi kar rahi hai! 💔😂",
    "Doctor: Aapka wazan kaise badh gaya?\nPatient: Main dawai kha kar aaraam karta hoon.\nDoctor: Kaunsi dawai?\nPatient: Gulab jamun! 🍩🤤😂",
    "Teacher: Ek aisi line kaho jisse sun kar khushi bhi ho aur dukh bhi.\nStudent: Sir, aapki beti mujhse pyar karti hai! 💘😂",
    "Pappu: Papa, mujhe ek ladki pasand hai.\nPapa: Kaun hai wo?\nPappu: Pados wali Pinky.\nPapa: Arre beta, wo toh teri behen hai.\nPappu: Papa, lagta hai aapne pados mein bahut social work kiya hai! 🏘️😂",
    "Banta: Mujhe aisi biwi chahiye jo chand jaisi ho.\nSanta: Jo raat ko aaye aur subah chali jaye? 🌙😂",
    "Wife: Jab humari shaadi hui thi, tum mujhe kitna pyar karte the, ab kya ho gaya?\nHusband: Election ke baad kaunsa neta publicity karta hai? 🗳️😂",
    "Teacher: 'I love you' ka aavishkar kis desh mein hua tha?\nStudent: China mein! Na koi guarantee, na koi warranty, chale toh chaand tak, nahi toh shaam tak! 🇨🇳😂",
    "Beta: Papa, aapne mummy mein kya dekha jo shaadi kar li?\nPapa: Beta, us time smartphone nahi the, jo dikha le liya! 📱😂",
    "Boss: Humare company mein English bolna compulsory hai.\nPeon: Ok sir.\nBoss: Acha batao, 'ek glass pani lao' ko English mein kya kahenge?\nPeon: Water, please! 🥛😂",
    "Santa: Mujhe kal raat ek sapna aaya ki main crorepati ban gaya hoon.\nBanta: Phir kya hua?\nSanta: Phir kya, alarm baj gaya aur meri kismat phoot gayi! ⏰💸😂",
    "Husband: Tum mujhe itna pareshan kyun karti ho?\nWife: Pyar karti hoon isliye!\nHusband: Toh bhai, thodi nafrat bhi kar liya karo! 🤯😂",
    "Teacher: 10 mein se 4 gaye toh kitne bache?\nStudent: Sir, main math mein weak hoon, Hindi mein poocho! 🔢😂",
    "Boy: Tumhara naam kya hai?\nGirl: 'T' se shuru hota hai.\nBoy: Teetar? 🐦😂",
    "Chintu: Doctor sahab, mujhe door ki cheezein nahi dikhti.\nDoctor: Wo aasmaan mein kya hai?\nChintu: Chaand.\nDoctor: Ab isse zyada door kya dekhna chahte ho? 🌙😂",
    "Son: Papa, ek glass pani de do.\nPapa: Khud le lo.\nSon: De do na.\nPapa: Abki baar maanga toh thappad padega!\nSon: Jab thappad maarne aaoge, toh pani lete aana! 🥤👋😂",
    "Girlfriend: Tumne toh kaha tha ki tum mujhe duniya ghumao ge.\nBoyfriend: Haan, toh Google Earth kis din kaam aayega? 🌍💻😂",
    "Teacher: Neta aur Abhineta mein kya farq hai?\nStudent: Abhineta acting karta hai aur Neta public ki setting kharab karta hai! 🎭😂",
    "Santa: Oye, tu itna udaas kyun hai?\nBanta: Meri patni ne mujhe bola hai ki agar main kal tak use diamond ring nahi dilaunga toh wo mujhe chhod degi.\nSanta: Toh kal kya karega?\nBanta: Aaraam se so jaunga! 😴💍😂",
    "Wife: Tum sari duniya ki auraton mein sabse zyada kisko pasand karte ho?\nHusband: Tumhari sautan ko! 🥊😂",
    "Inspector: Chori kyun ki?\nChor: Sahab, biwi ko khush rakhne ke liye!\nInspector: Par biwi ne toh report likhayi hai.\nChor: Wo meri biwi thodi thi! 🚔😂",
    "Patient: Doctor, meri ek aankh se sab double dikhta hai.\nDoctor: Toh doosri aankh band karke dekha karo! 👁️😂",
    "Teacher: 'Mera baap chor hai' is sentence ko future tense mein convert karo.\nStudent: 'Main chor banunga!' 🏃‍♂️😂",
    "Husband: Khana kaisa bana hai?\nWife: Bahut acha, bas thoda namak kam hai.\nHusband: Namak kam nahi, khana hi kam hai! 🍲😂",
    "Boss: Tum late kyun ho?\nEmployee: Gadi kharab ho gayi thi.\nBoss: Toh bus se aa jate.\nEmployee: Par bus toh sahi chal rahi thi na! 🚌😂",
    "Wife: Suna hai shaadi ke baad mard ka dimag kaam karna band kar deta hai.\nHusband: Tumne sahi suna hai, main iska jeeta jaagta saboot hoon! 🧠📉😂",
    "Santa: Bhai, mujhe lagta hai ki meri biwi ka chakkar kisi ke sath chal raha hai.\nBanta: Kyun?\nSanta: Kal wo bata rahi thi ki uska ek naya 'Babu' aaya hai office mein! 💼😂",
    "Teacher: Batao baccho, sabse bada pakshi kaunsa hai?\nStudent: Sir, Pados wali aunty, ud ud kar sabki khabar rakhti hai! 🦅😂",
    "Boy: I love you.\nGirl: Par main toh tumhein bhai manti hoon.\nBoy: Toh fir apni saheli se meri setting karwa de, 'Bhai' ki itni toh madad kar sakti hai na? 🤝😂",
    "Doctor: Aapko kya problem hai?\nPatient: Doctor sahab, mujhe azeeb azeeb aawazein sunai deti hain.\nDoctor: Kya aapko bhoot dikhte hain?\nPatient: Nahi, par meri biwi bolti bahut hai! 👻😂",
    "Teacher: Hathi aur choohe mein kya samanta hai?\nStudent: Dono ke paas Facebook account nahi hai! 🐘🐭😂",
    "Santa: Main apni biwi se itna darta hoon ki jab wo mujhe gusse mein dekhti hai toh...\nBanta: Toh kya?\nSanta: Toh main apni aankhein band kar leta hoon! 🙈😂",
    "Wife: Dekho, maine 10 kg wazan kam kar liya hai!\nHusband: Woh kaise?\nWife: Maine apni purani photos delete kar di hain! 📸😂",
    "Teacher: Aap bade hokar kya banoge?\nStudent: Main bada hokar ek aamir insaan banunga, jiske paas car, bangla aur bohot saari ladkiyan hongi.\nTeacher: Aur tum Pinky?\nPinky: Main iski biwi banungi! 👸😂",
    "Santa: Oye, tu kal raat ko itna kyun chilla raha tha?\nBanta: Arre, main apne padosi ko uski bhalai ke liye samjha raha tha.\nSanta: Lekin wo toh pichle hafte ghar shift kar chuka hai!\nBanta: Wahi toh, mujhe kal pata chala! 🗣️😂",
    "Wife: Agar mujhe kuch ho gaya toh tum kya karoge?\nHusband: Main pagal ho jaunga.\nWife: Matlab doosri shaadi nahi karoge?\nHusband: Pagal aadmi toh kuch bhi kar sakta hai! 🤪😂",
    "Teacher: Kis kisne homework kiya hai, haath uthao! (Ek bacha haath nahi uthata)\nTeacher: Tumne homework kyun nahi kiya?\nStudent: Kyunki mere haath mein dard hai! ✋😂",
    "Doctor: Aapko exercise karni chahiye.\nPatient: Main subah jaldi uth kar park mein ghoomta hoon.\nDoctor: Sirf ghoomne se kya hoga?\nPatient: Wahan log exercise karte hain, main unhe dekhta hoon! 🏃‍♂️👀😂",
    "Boy: Teri aur meri kismat ek jaisi hai.\nGirl: Wo kaise?\nBoy: Kyunki main bhi single hoon aur tu bhi single hai! 💘😂",
    "Wife: Aji sunte ho, bahar koi aaya hai!\nHusband: Keh do, ghar mein koi nahi hai.\nWife: Arre wo kutta hai!\nHusband: Toh usse meri language mein samjhao - 'Bhow Bhow'! 🐕😂",
    "Santa: Bhai, aaj toh maine ek sher ko bhaga diya!\nBanta: Wah bhai! Kaise?\nSanta: Arre, wo zoo ke pinjre mein tha, main wahan se bhaag aaya! 🦁🏃‍♂️😂",
    "Teacher: Zindagi aur maut mein kya farq hai?\nStudent: Zindagi mein hum mobile charge karte hain aur maut ke baad humari battery hamesha ke liye discharge ho jaati hai! 🔋⚰️😂",
    "Husband: Tum itni taiyar kyun ho rahi ho?\nWife: Main beauty parlour ja rahi hoon.\nHusband: Theek hai, ja kar wapis zaroor aana, koi aur na le aaye dhoke se! 💄😂",
    "Santa: Main ek aisi machine banaunga jismein idhar se aloo daalunga, udhar se sona niklega!\nBanta: Arre, ye idea toh kisi aur ne pehle hi de diya hai! 🥔✨😂",
    "Wife: Suno, agar main kho gayi toh tum kya karoge?\nHusband: Main akhbaar mein ad dunga.\nWife: Kya likhoge?\nHusband: Jisko mile, wo khud rakhe! 📰😂",
    "Teacher: Class, shanti banaye rakho!\nStudent: Sir, Shanti toh aaj chutti par hai, Pooja se kaam chala lijiye! 🕊️😂",
    # ── Desi Classics ──
    "Teacher: '2+2 kitna?' Pappu: 'Sir GST lagega kya?' 😂",
    "Maa: 'Padhai kar!' Main: 'Housie AI se padh raha hoon!' 📖😅",
    "Boss: 'AI se kaam karwao!' Main: *boss ko replace kar doon kya?* 🤖😂",
    "Exam mein question: '8 ko ulta karo.' Student ne paper ulta kar diya! 😂",
    "Programmer ki girlfriend: 'Mujhse pyar karte ho?' Programmer: 'True!' 🖥️💕😂",
    "WiFi ka naam 'Sharma Ji Ka Beta' rakh do — sab connect karne ki koshish karenge! 📶😂",
]

MOTIVATION_EN = [
    '"The only way to do great work is to love what you do." — Steve Jobs ✨',
    '"In the middle of every difficulty lies opportunity." — Albert Einstein 💡',
    '"Dream big. Work hard. Stay humble." 🚀',
    '"Code is poetry written in logic." — Unknown 💻',
    '"Success is not final, failure is not fatal — it is the courage to continue that counts." — Churchill 💪',
    '"Every expert was once a beginner." 🌱',
    '"The best error message is the one that never shows up." — Thomas Fuchs 🖥️',
]

MOTIVATION_HI = [
    '"Mushkilein aati hain toh hausla mat haaro — tumhe strong bana rahi hain!" 💪',
    '"Sapne bade rakhna, mehnat karo — sab mumkin hai!" 🌟',
    '"Zindagi mein shortcuts nahi — bas ek step at a time!" 🔥',
    '"Code likhna shayari jaisi hai — ek baar seekh lo, duniya badal do!" 💻',
    '"Failure ek temporary state hai — give up karna permanent hai." 🚀',
    '"Roz thoda behtar bano — 1% improvement, 365 din = 37x behtar!" 📈',
]

FUN_FACTS_EN = [
    "🍯 Honey never spoils! 3000-year-old Egyptian honey was still perfectly edible.",
    "🧠 Your brain uses 20% of your body's energy but is only 2% of your weight!",
    "🐙 An octopus has 3 hearts, blue blood, and 9 brains!",
    "⚡ Lightning strikes Earth ~100 times per second — 8.6 million per day!",
    "🌊 The ocean contains more historical artifacts than all museums combined!",
    "🔬 There are more atoms in a grain of sand than stars in the Milky Way!",
    "🐦 Crows can recognize human faces and hold grudges for years!",
    "🌍 Earth's core is as hot as the surface of the Sun — ~5,778 Kelvin!",
    "🦑 The colossal squid has the largest eyes in the animal kingdom — up to 27cm wide!",
    "🧬 If you stretched out all your DNA, it would reach to Pluto and back!",
]

FUN_FACTS_HI = [
    "🍯 Shahed kabhi kharab nahi hoti! 3000 saal purani Egyptian shahed bhi khane layak thi.",
    "🧠 Dimaag 2.5 petabytes data store kar sakta hai — 3 million ghante ki movies!",
    "🐙 Octopus ke 3 dil hain, neela khoon hai, aur 9 dimaag hain!",
    "⚡ Bijli prithvi par ek second mein 100 baar girti hai — din mein 86 lakh baar!",
    "🔬 Ek reth ke dane mein Milky Way ke taaron se zyada atoms hain!",
    "🌍 Earth ka core Sun ki surface jitna garam hai — 5,778 Kelvin!",
]

# ═══════════════════════════════════════════
#   MASSIVE KNOWLEDGE BASE (50+ Topics)
# ═══════════════════════════════════════════
KNOWLEDGE = {
    # ─── PHYSICS ───
    'quantum computing': {
        'e': "🤯 **Quantum Computing** uses *qubits* that can be 0 AND 1 simultaneously (superposition).\n\n🔹 **Key concepts:** Superposition, Entanglement, Quantum gates\n🔹 **Used for:** Cryptography, Drug discovery, Climate modeling, Optimization\n🔹 **Companies:** IBM (127-qubit Eagle), Google (Sycamore), D-Wave\n🔹 **Languages:** Qiskit (Python), Cirq, Q#\n\nQuantum computers could break RSA encryption but also create unbreakable quantum encryption!",
        'h': "🤯 Quantum Computing qubits use karti hai jo 0 aur 1 dono ek saath ho sakte hain (superposition). IBM, Google is par kaam kar rahe hain — yeh future ki technology hai! Encryption todne aur drug discovery mein kaam aayegi!"
    },
    'black hole': {
        'e': "🌌 **Black Holes** — regions where gravity is so extreme that nothing escapes!\n\n🔹 **Event Horizon:** Point of no return\n🔹 **Singularity:** Infinite density at center\n🔹 **Time Dilation:** Time literally slows near a black hole\n🔹 **Hawking Radiation:** Stephen Hawking proved they slowly evaporate!\n🔹 **Types:** Stellar (10-100 M☉), Supermassive (millions of M☉), Primordial\n🔹 **Nearest:** Gaia BH1, ~1,560 light-years away\n\nThe black hole at our galaxy's center (Sagittarius A*) is 4 million times the Sun's mass!",
        'h': "🌌 Black hole ek aisi jagah hai jahan gravity itni strong hai ki light bhi escape nahi kar sakti! Hamare galaxy ke center mein Sagittarius A* hai — Sun se 40 lakh guna bhari!"
    },
    'relativity': {
        'e': "⏳ **Theory of Relativity** by Albert Einstein:\n\n1️⃣ **Special Relativity (1905):**\n   • Speed of light (c) is constant for all observers\n   • Time dilation: Moving clocks tick slower\n   • Length contraction: Moving objects appear shorter\n   • **E = mc²** — mass and energy are interchangeable!\n\n2️⃣ **General Relativity (1915):**\n   • Gravity = curvature of spacetime\n   • Massive objects bend light (gravitational lensing)\n   • Predicted gravitational waves (confirmed 2015 by LIGO!)\n   • GPS satellites must account for relativity to be accurate!",
        'h': "⏳ Einstein ki Relativity:\n1. Special: Speed badhne se time slow! E = mc² — mass aur energy same hain!\n2. General: Badi cheezein spacetime ko curve karti hain — isi se gravity! GPS bhi relativity use karta hai!"
    },
    'gravity': {
        'e': "🍎 **Gravity** — the weakest but most far-reaching fundamental force!\n\n🔹 **Newton:** F = Gm₁m₂/r² (1687)\n🔹 **Einstein:** Gravity = curvature of spacetime (1915)\n🔹 **Gravitational waves:** Ripples in spacetime (detected 2015 by LIGO!)\n🔹 **Escape velocity from Earth:** 11.2 km/s\n🔹 **g on Earth:** 9.81 m/s²\n🔹 **g on Moon:** 1.62 m/s² (6× weaker)\n🔹 **g on Jupiter:** 24.79 m/s² (2.5× stronger)",
        'h': "🍎 Gravity: Newton ne bataya F = Gm₁m₂/r². Einstein ne kaha gravity spacetime ka curve hai. Earth se escape ke liye 11.2 km/s speed chahiye! Moon par gravity 6 guna kam hai."
    },
    'newton': {
        'e': "⚙️ **Newton's Three Laws of Motion:**\n\n1️⃣ **Law of Inertia:** An object stays at rest or in motion unless acted upon by an external force.\n2️⃣ **F = ma:** Force equals mass times acceleration. More mass = harder to accelerate.\n3️⃣ **Action-Reaction:** Every action has an equal and opposite reaction.\n\n🔹 **Newton also discovered:** Laws of gravitation, calculus, optics, reflecting telescope\n🔹 Fun fact: The falling apple story is probably true! 🍎",
        'h': "⚙️ Newton ke 3 Laws:\n1. Jab tak force na lage, object nahi hilta (Inertia)\n2. F = ma (Force = Mass × Acceleration)\n3. Har action ka equal aur opposite reaction hota hai!\nNewton ne calculus bhi invent kiya tha! 🍎"
    },
    'thermodynamics': {
        'e': "🔥 **Laws of Thermodynamics:**\n\n0️⃣ **Zeroth Law:** If A is in thermal equilibrium with B, and B with C, then A is with C.\n1️⃣ **First Law:** Energy cannot be created or destroyed, only transformed. (ΔU = Q - W)\n2️⃣ **Second Law:** Entropy of an isolated system always increases. Heat flows hot → cold.\n3️⃣ **Third Law:** As temperature → absolute zero, entropy → minimum.\n\n🔹 **Entropy** is why your room gets messy but never cleans itself! 😂",
        'h': "🔥 Thermodynamics ke Laws:\n1. Energy create ya destroy nahi hoti — sirf form change hoti hai\n2. Entropy (disorder) hamesha badhti hai — isliye room apne aap ganda hota hai! 😂\n3. Absolute zero par entropy minimum hoti hai."
    },
    'electromagnetism': {
        'e': "⚡ **Electromagnetism** — one of the four fundamental forces!\n\n🔹 **Maxwell's Equations:** 4 equations that unify electricity and magnetism\n🔹 **Coulomb's Law:** F = kq₁q₂/r² (force between charges)\n🔹 **Electromagnetic spectrum:** Radio → Microwave → IR → Visible → UV → X-ray → Gamma\n🔹 **Speed of light:** 299,792,458 m/s (exactly!)\n🔹 **Applications:** Motors, generators, radio, WiFi, MRI, and literally everything electronic!",
        'h': "⚡ Electromagnetism: Maxwell ke 4 equations ne electricity aur magnetism ko ek kar diya! Light bhi ek electromagnetic wave hai — 3×10⁸ m/s ki speed se chalti hai. WiFi, radio, MRI — sab isi se kaam karte hain!"
    },
    'nuclear': {
        'e': "☢️ **Nuclear Physics:**\n\n🔹 **Fission:** Splitting heavy atoms (Uranium-235) → massive energy release. Used in nuclear power plants and bombs.\n🔹 **Fusion:** Combining light atoms (Hydrogen → Helium). Powers the Sun! Scientists are trying to achieve it on Earth (ITER project).\n🔹 **E = mc²:** A tiny amount of mass converts to enormous energy\n🔹 **Radioactivity:** Alpha (α), Beta (β), Gamma (γ) radiation\n🔹 **Half-life:** Time for half the atoms to decay\n\n1 kg of uranium = energy of 3,000 tons of coal! ⚡",
        'h': "☢️ Nuclear Physics:\n- Fission: Bade atoms todte hain → energy (nuclear power)\n- Fusion: Chhote atoms jodde hain → Sun ki energy source!\n- E = mc² — thodi si mass = bahut zyada energy! 1 kg uranium = 3000 ton coal ki energy!"
    },

    # ─── COMPUTER SCIENCE ───
    'machine learning': {
        'e': "🤖 **Machine Learning (ML)** — AI that learns from data!\n\n🔹 **Supervised Learning:** Learns from labeled data (Classification, Regression)\n🔹 **Unsupervised Learning:** Finds patterns in unlabeled data (Clustering, PCA)\n🔹 **Reinforcement Learning:** Learns by trial and error (Game AI, Robotics)\n\n📚 **Key Algorithms:**\n• Linear/Logistic Regression\n• Decision Trees, Random Forest\n• Neural Networks, CNNs, RNNs, Transformers\n• K-Means, SVM, KNN\n\n🔹 **Frameworks:** TensorFlow, PyTorch, scikit-learn\n🔹 **Languages:** Python (dominant), R, Julia",
        'h': "🤖 Machine Learning mein computer data se khud seekhta hai!\n- Supervised: Labeled data se seekhta hai\n- Unsupervised: Khud patterns dhundhta hai\n- Reinforcement: Trial and error se seekhta hai\nPython + TensorFlow/PyTorch sabse popular hai!"
    },
    'blockchain': {
        'e': "⛓️ **Blockchain** — distributed, immutable ledger technology!\n\n🔹 **Blocks:** Each contains data + hash of previous block\n🔹 **Mining:** Solving complex math puzzles to validate transactions\n🔹 **Consensus:** Proof of Work (Bitcoin) vs Proof of Stake (Ethereum 2.0)\n🔹 **Smart Contracts:** Self-executing code (Solidity on Ethereum)\n🔹 **DeFi:** Decentralized finance — lending, borrowing without banks\n🔹 **NFTs:** Unique digital ownership tokens\n\n🔸 Bitcoin: First cryptocurrency (2009, Satoshi Nakamoto)\n🔸 Ethereum: Programmable blockchain with smart contracts",
        'h': "⛓️ Blockchain ek distributed ledger hai — tamper-proof!\n- Bitcoin: Pehli cryptocurrency (2009)\n- Ethereum: Smart contracts wala blockchain\n- Mining: Complex math solve karke transactions validate karte hain\n- DeFi: Banks ke bina lending/borrowing!"
    },
    'sorting': {
        'e': "📊 **Sorting Algorithms — Complete Guide:**\n\n| Algorithm | Best | Average | Worst | Space | Stable |\n|-----------|------|---------|-------|-------|--------|\n| Bubble | O(n) | O(n²) | O(n²) | O(1) | ✅ |\n| Selection | O(n²) | O(n²) | O(n²) | O(1) | ❌ |\n| Insertion | O(n) | O(n²) | O(n²) | O(1) | ✅ |\n| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |\n| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |\n| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ |\n| Radix | O(nk) | O(nk) | O(nk) | O(n+k) | ✅ |\n\n🏆 **Best general-purpose:** Merge Sort (stable) or Quick Sort (fast in practice)",
        'h': "📊 Sorting Algorithms:\n- Bubble Sort: O(n²) — simple but slow\n- Merge Sort: O(n log n) — stable, reliable\n- Quick Sort: O(n log n) avg — fastest in practice\n- Heap Sort: O(n log n) — in-place!\nInterviews mein Merge aur Quick Sort sabse important!"
    },
    'operating system': {
        'e': "🖥️ **Operating System (OS):**\n\n🔹 **Kernel:** Core — manages CPU, memory, I/O\n🔹 **Process Management:** Scheduling (FCFS, SJF, Round Robin, Priority)\n🔹 **Memory Management:** Paging, Segmentation, Virtual Memory\n🔹 **File Systems:** NTFS, ext4, APFS, FAT32\n🔹 **Deadlock:** Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait\n🔹 **Concurrency:** Mutex, Semaphore, Monitor\n\n📱 **Popular OS:** Windows, Linux, macOS, Android, iOS\n🐧 **Linux distros:** Ubuntu, Fedora, Arch, Debian, CentOS",
        'h': "🖥️ OS hardware aur software manage karta hai!\n- Kernel: CPU, RAM, I/O manage karta hai\n- Process Scheduling: FCFS, Round Robin, SJF\n- Memory: Paging, Virtual Memory\n- Popular: Windows, Linux, macOS, Android"
    },
    'data structures': {
        'e': "🏗️ **Data Structures — The Essentials:**\n\n📋 **Linear:**\n• Array — O(1) access, O(n) insert\n• Linked List — O(1) insert, O(n) access\n• Stack — LIFO (push/pop)\n• Queue — FIFO (enqueue/dequeue)\n\n🌳 **Non-Linear:**\n• Binary Tree, BST — O(log n) search\n• Heap — Priority Queue\n• Graph — BFS, DFS, Dijkstra\n• Trie — String searching\n\n🗃️ **Hash-based:**\n• HashMap — O(1) average lookup\n• HashSet — Unique elements\n\n💡 **Choosing the right DS is 90% of solving a coding problem!**",
        'h': "🏗️ Data Structures:\n- Array: O(1) access, O(n) insert\n- Linked List: O(1) insert, O(n) access\n- Stack: LIFO, Queue: FIFO\n- Tree: O(log n) search (BST)\n- HashMap: O(1) average lookup\nSahi DS choose karna 90% problem solve kar deta hai!"
    },
    'api': {
        'e': "🔌 **API (Application Programming Interface):**\n\n🔹 **REST API:** HTTP-based, uses GET/POST/PUT/DELETE\n🔹 **GraphQL:** Query exactly what you need (by Facebook)\n🔹 **WebSocket:** Real-time bidirectional communication\n🔹 **gRPC:** High-performance RPC by Google (Protocol Buffers)\n\n📦 **Data Formats:** JSON (most common), XML, Protocol Buffers\n🔐 **Auth:** API Keys, OAuth 2.0, JWT Tokens\n\nThink of an API like a waiter in a restaurant — you tell the waiter (API) what you want, they get it from the kitchen (server)! 🍽️",
        'h': "🔌 API ek bridge hai jo do softwares ko connect karta hai!\n- REST: HTTP methods (GET, POST, PUT, DELETE)\n- GraphQL: Sirf jo chahiye woh maango\n- WebSocket: Real-time communication\nJaise restaurant mein waiter order kitchen tak le jata hai!"
    },
    'database': {
        'e': "🗄️ **Databases:**\n\n📊 **Relational (SQL):**\n• MySQL, PostgreSQL, SQLite, Oracle\n• Tables, Rows, Columns\n• ACID properties, JOINs, Normalization\n\n📄 **NoSQL:**\n• MongoDB (Document), Redis (Key-Value)\n• Cassandra (Wide Column), Neo4j (Graph)\n• BASE properties, flexible schema\n\n🔹 **SQL vs NoSQL:**\n• SQL: Structured data, complex queries, ACID\n• NoSQL: Flexible schema, horizontal scaling, speed\n\n💡 **CAP Theorem:** You can only guarantee 2 of 3: Consistency, Availability, Partition Tolerance",
        'h': "🗄️ Database:\n- SQL: MySQL, PostgreSQL — structured data, tables, JOINs\n- NoSQL: MongoDB, Redis — flexible, fast, scalable\n- SQL ACID hai, NoSQL BASE hai\n- CAP Theorem: 3 mein se sirf 2 guarantee ho sakti hain!"
    },
    'cybersecurity': {
        'e': "🔒 **Cybersecurity Essentials:**\n\n🔹 **Common Attacks:**\n• SQL Injection, XSS (Cross-Site Scripting)\n• MITM (Man-in-the-Middle), DDoS\n• Phishing, Ransomware, Zero-Day Exploits\n\n🔹 **Defense:**\n• Encryption (AES-256, RSA), Hashing (SHA-256, bcrypt)\n• Firewalls, IDS/IPS, VPN\n• 2FA, OAuth, JWT\n• Input validation, parameterized queries\n\n🔹 **CIA Triad:** Confidentiality, Integrity, Availability\n\n💡 **Top tip:** Never store passwords in plain text! Always hash with salt (bcrypt).",
        'h': "🔒 Cybersecurity:\n- Attacks: SQL Injection, XSS, DDoS, Phishing\n- Defense: Encryption, Hashing, Firewalls, 2FA\n- CIA Triad: Confidentiality, Integrity, Availability\n- Password kabhi plain text mein mat store karo — bcrypt use karo!"
    },

    # ─── MATH ───
    'calculus': {
        'e': "∫ **Calculus — The Mathematics of Change:**\n\n📐 **Differentiation (Derivatives):**\n• d/dx(xⁿ) = nxⁿ⁻¹ (Power Rule)\n• d/dx(sin x) = cos x\n• d/dx(eˣ) = eˣ\n• Chain Rule: d/dx[f(g(x))] = f'(g(x))·g'(x)\n\n∫ **Integration:**\n• ∫xⁿ dx = xⁿ⁺¹/(n+1) + C\n• ∫sin x dx = -cos x + C\n• ∫eˣ dx = eˣ + C\n\n🔹 **Fundamental Theorem:** Differentiation and integration are inverse operations!\n🔹 **Applications:** Physics (velocity, acceleration), Economics (marginal cost), Engineering",
        'h': "∫ Calculus — change ka mathematics!\n- Differentiation: d/dx(xⁿ) = nxⁿ⁻¹\n- Integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C\n- d/dx(sin x) = cos x, ∫sin x dx = -cos x + C\nPhysics, engineering, economics — sab mein use hota hai!"
    },
    'statistics': {
        'e': "📈 **Statistics Essentials:**\n\n🔹 **Measures of Central Tendency:**\n• Mean = Σx/n\n• Median = Middle value (sorted)\n• Mode = Most frequent value\n\n🔹 **Measures of Spread:**\n• Range = Max - Min\n• Variance = Σ(x-μ)²/n\n• Standard Deviation = √Variance\n\n🔹 **Distributions:**\n• Normal (Bell Curve): 68-95-99.7 rule\n• Poisson, Binomial, Exponential\n\n🔹 **Hypothesis Testing:** p-value, t-test, chi-square, ANOVA\n🔹 **Correlation ≠ Causation!** 📊",
        'h': "📈 Statistics:\n- Mean = average, Median = middle, Mode = most frequent\n- Standard Deviation = data ka spread\n- Normal Distribution: 68-95-99.7 rule\n- Correlation ≠ Causation! Yeh yaad rakhna! 📊"
    },
    'pythagoras': {
        'e': "📐 **Pythagorean Theorem:** a² + b² = c²\n\n🔹 In any right triangle, the square of the hypotenuse equals the sum of squares of the other two sides.\n🔹 **Common triples:** (3,4,5), (5,12,13), (8,15,17), (7,24,25), (9,40,41)\n🔹 **Converse:** If a² + b² = c², the triangle IS right-angled!\n🔹 **3D version:** d² = a² + b² + c²\n🔹 **Over 370 different proofs exist!** The most elegant uses areas of squares.",
        'h': "📐 Pythagorean Theorem: a² + b² = c²\nRight triangle mein hypotenuse ka square = dono sides ke squares ka sum!\nTriples: (3,4,5), (5,12,13), (8,15,17)\nIs theorem ke 370+ proofs hain!"
    },

    # ─── BIOLOGY ───
    'dna': {
        'e': "🧬 **DNA (Deoxyribonucleic Acid):**\n\n🔹 **Structure:** Double helix (Watson & Crick, 1953)\n🔹 **Base Pairs:** A-T (Adenine-Thymine), G-C (Guanine-Cytosine)\n🔹 **Human genome:** ~3.2 billion base pairs, 46 chromosomes (23 pairs)\n🔹 **Central Dogma:** DNA → RNA → Protein\n🔹 **Replication:** Semi-conservative (Meselson-Stahl experiment)\n🔹 **CRISPR-Cas9:** Gene editing tool — 2020 Nobel Prize!\n\n🤯 If stretched out, your DNA would reach the Sun and back ~300 times!",
        'h': "🧬 DNA zindagi ka blueprint hai!\n- Double helix structure (Watson & Crick, 1953)\n- 4 bases: A-T, G-C\n- Human DNA: 3.2 billion base pairs, 46 chromosomes\n- CRISPR: Gene editing tool — 2020 Nobel Prize!\nAgar stretch karo toh Sun tak 300 baar pahunch sakta hai!"
    },
    'photosynthesis': {
        'e': "🌿 **Photosynthesis:**\n\n**6CO₂ + 6H₂O + Light Energy → C₆H₁₂O₆ + 6O₂**\n\n🔹 **Light Reactions:** In thylakoid membranes — produce ATP & NADPH\n🔹 **Calvin Cycle:** In stroma — fixes CO₂ into glucose\n🔹 **Chlorophyll:** Absorbs red & blue light, reflects green (that's why plants are green!)\n🔹 **C3, C4, CAM:** Different carbon fixation pathways\n🔹 Plants produce ~150 billion tonnes of sugar per year!\n🔹 **Artificial photosynthesis** is a major research area for clean energy!",
        'h': "🌿 Photosynthesis: 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂\nPlants suraj ki roshni se sugar aur oxygen banate hain!\nChlorophyll green isliye dikhta hai kyunki green light reflect karta hai!\nPlants har saal 150 billion ton sugar banate hain!"
    },
    'evolution': {
        'e': "🧬 **Evolution — by Charles Darwin (1859):**\n\n🔹 **Natural Selection:** Survival of the fittest — organisms with advantageous traits reproduce more\n🔹 **Evidence:** Fossil record, DNA comparisons, homologous structures, vestigial organs\n🔹 **Mechanisms:** Mutation, Gene flow, Genetic drift, Natural selection\n🔹 **Common misconception:** Humans didn't evolve FROM apes — we share a common ancestor!\n🔹 **Timeline:** Life began ~3.8 billion years ago, humans appeared ~300,000 years ago\n\n🦕 99.9% of all species that ever existed are now extinct!",
        'h': "🧬 Evolution (Charles Darwin, 1859):\n- Natural Selection: Jo environment ke liye fit hai, woh survive karta hai\n- Humans apes se nahi aaye — common ancestor share karte hain!\n- Life 3.8 billion saal pehle shuru hui\n- 99.9% species jo kabhi thi, ab extinct hain!"
    },

    # ─── CHEMISTRY ───
    'periodic table': {
        'e': "⚗️ **Periodic Table:**\n\n🔹 **118 elements** arranged by atomic number\n🔹 **Groups (columns):** Elements with similar properties\n  • Group 1: Alkali metals (Li, Na, K) — highly reactive!\n  • Group 17: Halogens (F, Cl, Br) — very reactive nonmetals\n  • Group 18: Noble gases (He, Ne, Ar) — extremely stable\n🔹 **Periods (rows):** Electron shells\n🔹 **Dmitri Mendeleev (1869):** Predicted undiscovered elements!\n🔹 **Heaviest stable element:** Lead (Pb, 82)\n🔹 **Most abundant:** Hydrogen (75% of universe by mass)",
        'h': "⚗️ Periodic Table: 118 elements hain!\n- Group 1: Alkali metals — bahut reactive\n- Group 18: Noble gases — stable\n- Mendeleev ne 1869 mein table banaya aur undiscovered elements predict kiye!\n- Universe mein sabse zyada Hydrogen hai (75%)!"
    },

    # ─── TECHNOLOGY ───
    'internet': {
        'e': "🌐 **How the Internet Works:**\n\n🔹 **TCP/IP:** Core protocol stack\n🔹 **DNS:** Converts domain names → IP addresses (like a phone book)\n🔹 **HTTP/HTTPS:** Protocol for web pages (S = Secure via TLS/SSL)\n🔹 **OSI Model:** 7 layers (Physical → Application)\n🔹 **Routing:** BGP directs data between autonomous systems\n🔹 **CDN:** Content Delivery Networks for speed (Cloudflare, Akamai)\n\n📊 **Stats:**\n• ~5.3 billion internet users worldwide\n• ~200 billion emails sent daily\n• Submarine cables carry 99% of international data!",
        'h': "🌐 Internet TCP/IP par kaam karta hai!\n- DNS: Domain name → IP address convert karta hai\n- HTTP/HTTPS: Web pages ka protocol\n- 5.3 billion log internet use karte hain\n- 99% international data submarine cables se travel karta hai!"
    },
    'climate': {
        'e': "🌍 **Climate Change:**\n\n🔹 **Greenhouse gases:** CO₂, CH₄, N₂O trap heat in atmosphere\n🔹 **Temperature rise:** +1.2°C since pre-industrial era\n🔹 **Effects:**\n  • Rising sea levels (3.6mm/year)\n  • Extreme weather events\n  • Ocean acidification\n  • Species extinction (1 million at risk)\n🔹 **Solutions:**\n  • Renewable energy (Solar, Wind, Nuclear)\n  • Carbon capture technology\n  • Electric vehicles\n  • Reforestation\n🔹 **Paris Agreement:** Limit warming to 1.5°C",
        'h': "🌍 Climate Change:\n- CO₂, CH₄ heat trap karte hain → temperature badh raha hai (+1.2°C)\n- Sea levels badh rahe, extreme weather aa raha\n- Solution: Solar, Wind energy, Electric vehicles, Carbon capture\n- Paris Agreement: 1.5°C tak limit rakhna hai"
    },
    'artificial intelligence': {
        'e': "🤖 **Artificial Intelligence (AI) — Complete Overview:**\n\n🔹 **Narrow AI:** Specific tasks (Siri, Chess engines, Image recognition)\n🔹 **General AI (AGI):** Human-level intelligence — doesn't exist yet!\n🔹 **Super AI:** Surpasses human intelligence — theoretical\n\n📚 **Key Branches:**\n• Machine Learning (supervised, unsupervised, reinforcement)\n• Deep Learning (Neural Networks, CNNs, RNNs, Transformers)\n• NLP (Natural Language Processing) — ChatGPT, translation\n• Computer Vision — self-driving cars, facial recognition\n• Robotics — physical AI agents\n\n🔹 **Turing Test:** Can a machine convince a human it's human?\n🔹 **AI Ethics:** Bias, privacy, job displacement, deepfakes",
        'h': "🤖 AI (Artificial Intelligence):\n- Narrow AI: Specific tasks (Siri, Chess)\n- AGI: Human-level intelligence — abhi tak exist nahi karta!\n- Deep Learning: Neural networks ke bahut layers\n- NLP: Language samajhna (ChatGPT jaise)\n- Computer Vision: Images samajhna (self-driving cars)"
    },
    'programming languages': {
        'e': "💻 **Programming Languages — Top Picks:**\n\n| Language | Best For | Type |\n|----------|----------|------|\n| Python | AI/ML, Data Science, Web | Interpreted |\n| JavaScript | Web (Frontend + Backend) | Interpreted |\n| Java | Enterprise, Android | Compiled (JVM) |\n| C++ | Games, Systems, Competitive | Compiled |\n| C | Embedded, OS, Hardware | Compiled |\n| Rust | Systems, Safety-critical | Compiled |\n| Go | Cloud, Microservices | Compiled |\n| TypeScript | Large-scale Web apps | Transpiled |\n| Swift | iOS/macOS apps | Compiled |\n| Kotlin | Android apps | Compiled (JVM) |\n\n💡 **First language?** Python (easiest) or JavaScript (most versatile)",
        'h': "💻 Programming Languages:\n- Python: AI/ML, Data Science — sabse easy\n- JavaScript: Web development — frontend + backend\n- Java: Enterprise, Android\n- C++: Games, Competitive Programming\n- Rust: System programming, safe\n\nPehli language? Python ya JavaScript start karo!"
    },
    'web development': {
        'e': "🌐 **Web Development — Full Stack Guide:**\n\n**Frontend:**\n• HTML (structure), CSS (style), JavaScript (logic)\n• Frameworks: React, Vue, Angular, Svelte\n• CSS: Tailwind, Bootstrap, Sass\n\n**Backend:**\n• Node.js (Express), Python (Flask/Django/FastAPI)\n• Java (Spring), Go (Gin), Ruby (Rails)\n\n**Database:** PostgreSQL, MongoDB, Redis\n**DevOps:** Docker, Kubernetes, CI/CD, AWS/GCP/Azure\n**Version Control:** Git + GitHub\n\n🚀 **Modern Stack (2024):** React/Next.js + Node.js/Python + PostgreSQL + Docker",
        'h': "🌐 Web Development:\n- Frontend: HTML + CSS + JavaScript (React/Vue framework)\n- Backend: Node.js ya Python (Flask/Django)\n- Database: PostgreSQL ya MongoDB\n- DevOps: Docker, AWS/GCP\n- Modern stack: React + Python/Node + PostgreSQL + Docker"
    },
    'git': {
        'e': "📦 **Git — Version Control System:**\n\n🔹 **Basic Commands:**\n```\ngit init          # Initialize repo\ngit add .         # Stage all changes\ngit commit -m \"\" # Commit changes\ngit push          # Push to remote\ngit pull          # Pull from remote\ngit branch        # List branches\ngit checkout -b   # Create & switch branch\ngit merge         # Merge branches\ngit log           # View history\ngit stash         # Temporarily save changes\n```\n\n🔹 **Branching Strategy:** main → develop → feature branches\n🔹 **GitHub vs GitLab vs Bitbucket** — all use Git!\n🔹 Created by **Linus Torvalds** (also created Linux!)",
        'h': "📦 Git — code ka version control!\n- git add + commit + push = basic workflow\n- Branches: feature branches se kaam karo\n- GitHub par code share karo\n- Linus Torvalds ne banaya tha (Linux bhi usne banaya!)"
    },
    'solar system': {
        'e': "☀️ **Our Solar System:**\n\n🔹 **Sun:** 99.86% of total mass! G-type main-sequence star\n🔹 **Inner planets (Rocky):** Mercury, Venus, Earth, Mars\n🔹 **Outer planets (Gas giants):** Jupiter, Saturn, Uranus, Neptune\n🔹 **Dwarf planets:** Pluto, Ceres, Eris, Haumea, Makemake\n\n📊 **Key Facts:**\n• Jupiter: Largest planet, 79+ moons, Great Red Spot\n• Saturn: Beautiful rings (ice & rock), 82+ moons\n• Earth: Only known planet with life!\n• Mars: Target for human colonization (SpaceX)\n• Light from Sun reaches Earth in ~8 minutes 19 seconds",
        'h': "☀️ Solar System:\n- Sun: 99.86% total mass!\n- Rocky planets: Mercury, Venus, Earth, Mars\n- Gas giants: Jupiter, Saturn, Uranus, Neptune\n- Jupiter: Sabse bada, 79+ moons\n- Earth: Sirf yahi par life hai (abhi tak)!\n- Sun ki light 8 min 19 sec mein Earth tak pahunchti hai"
    },
    'human body': {
        'e': "🫀 **Human Body — Amazing Facts:**\n\n🔹 **Heart:** Beats ~100,000 times/day, pumps ~7,500 liters of blood!\n🔹 **Brain:** 86 billion neurons, uses 20% of body's energy\n🔹 **Bones:** 206 bones in adults (babies have ~270!)\n🔹 **Muscles:** ~600 skeletal muscles\n🔹 **DNA:** 3.2 billion base pairs, 99.9% identical between all humans\n🔹 **Blood vessels:** 100,000 km total — enough to wrap around Earth 2.5 times!\n🔹 **Stomach acid (HCl):** Strong enough to dissolve metal!\n🔹 **Fastest muscle:** Eye muscles (blink in 100ms)",
        'h': "🫀 Human Body:\n- Heart: Din mein 1 lakh baar dhakdhak!\n- Brain: 86 billion neurons, 20% energy use karta hai\n- 206 bones (babies mein 270!)\n- Blood vessels: 1 lakh km lambi — Earth ke 2.5 baar lapetne jitni!\n- Stomach acid metal bhi gala sakta hai!"
    },
    'instagram': {
        'aliases': ['instagram', 'insta', 'ig'],
        'e': "📸 **Instagram (IG):**\n\n🔹 **What it is:** A global photo and video sharing social network owned by **Meta Platforms** (Facebook).\n🔹 **Founded:** October 2010 by Kevin Systrom & Mike Krieger, acquired by Facebook in 2012 for $1 Billion.\n🔹 **Core Features:**\n  • **Feed Posts & Carousels:** High-res photo & video albums\n  • **Stories:** 24-hour disappearing photos/videos with stickers and filters\n  • **Reels:** Short-form vertical video algorithm (rivaling TikTok)\n  • **DMs (Direct Messages):** Private chats, voice notes, media sharing\n  • **Explore Page:** AI-driven personalized recommendation feed\n🔹 **Scale:** Over **2.4 Billion active users** worldwide!\n🔹 **Tech Stack:** Powered by **Python (Django)** backend, React Native mobile apps, and massive distributed databases.",
        'h': "📸 **Instagram:**\n\n🔹 **Kya hai:** Duniya ka sabse popular photo aur video sharing social media app hai, jo **Meta** (Facebook) ka hissa hai.\n🔹 **Kisne banaya:** 2010 mein Kevin Systrom aur Mike Krieger ne banaya tha, phir 2012 mein Mark Zuckerberg ne $1 Billion mein khareeda.\n🔹 **Features:** Stories (24 ghante mein gayab), Reels (viral short videos), Photos/Videos, DMs aur Explore page.\n🔹 **Scale:** 2.4 Billion se zyada log ise use karte hain!\n🔹 **Tech:** Iska backend **Python (Django)** par bana hai aur mobile app **React Native** par chalta hai!"
    },
    'coding': {
        'aliases': ['coding', 'code', 'programming', 'programmer', 'program', 'how to code', 'learn coding'],
        'e': "💻 **Coding (Computer Programming):**\n\n🔹 **What it is:** Coding is writing instructions in programming languages that computers understand and execute to build software, games, websites, and artificial intelligence.\n\n🔹 **How it works:**\n  1. **Source Code:** You write logic in human-readable languages (Python, JavaScript, C++, etc.).\n  2. **Compilation/Interpretation:** A compiler or interpreter converts it into binary machine code (0s and 1s).\n  3. **Execution:** The CPU executes instructions at billions of cycles per second!\n\n🔹 **What you can build:**\n  • 🌐 **Websites & Web Apps:** HTML, CSS, JavaScript, React, Node.js\n  • 📱 **Mobile Apps:** Flutter, React Native, Swift (iOS), Kotlin (Android)\n  • 🎮 **Games:** Unity (C#), Unreal Engine (C++)\n  • 🤖 **AI & Machine Learning:** Python, PyTorch, TensorFlow\n  • ⚡ **Operating Systems & Drivers:** C, C++, Rust\n\n💡 **Best language to start with:** **Python** (clean syntax & AI) or **JavaScript** (interactive web)!",
        'h': "💻 **Coding (Programming) kya hai:**\n\n🔹 **Simple shabdon mein:** Coding ka matlab computer ko instructions dena hai. Computer humari normal bhasha nahi samajhta, isliye hum programming languages (jaise Python, JavaScript, C++) use karke usse kaam karwate hain!\n\n🔹 **Kaise kaam karta hai:**\n  1. Aap code likhte ho (Source Code).\n  2. Compiler ya Interpreter use machine language (0s aur 1s - binary) mein badalta hai.\n  3. Processor use run karke app, game ya website chalata hai!\n\n🔹 **Coding se kya banta hai:**\n  • Websites aur Web Applications\n  • Android aur iOS Apps\n  • Video Games (Minecraft, GTA, BGMI sab coding se bane hain!)\n  • AI Robots aur Housie jaise assistants!\n\n💡 **Seekhna shuru kaise karein:** **Python** se shuru karo — yeh seekhne mein sabse aasan aur sabse powerful hai!"
    },
    'python': {
        'aliases': ['python', 'python3', 'py'],
        'e': "🐍 **Python Programming Language:**\n\n🔹 Created by **Guido van Rossum** in 1991.\n🔹 **Why it's #1:** Ultra-readable syntax, massive library ecosystem, and beginner-friendly!\n🔹 **Used for:** Artificial Intelligence, Machine Learning, Data Science, Backend Web (Django, Flask), Automation, and Scripting.\n🔹 **Key Libraries:** NumPy, Pandas, SymPy (which powers my math!), PyTorch, TensorFlow.\n🔹 Fun fact: Named after the British comedy show 'Monty Python's Flying Circus', NOT the snake!",
        'h': "🐍 **Python Language:**\n\n🔹 1991 mein Guido van Rossum ne banayi thi.\n🔹 Duniya ki sabse popular language hai — kyunki iska syntax English jaisa simple hai!\n🔹 AI, Machine Learning, Data Science, aur Web development (Django/Flask) mein sabse aage hai.\n🔹 Housie AI ka math engine bhi Python ke SymPy library se chalta hai! 🚀"
    },
    'javascript': {
        'aliases': ['javascript', 'js', 'ecmascript'],
        'e': "💛 **JavaScript (JS):**\n\n🔹 Created by **Brendan Eich** in just 10 days in May 1995!\n🔹 **The language of the web:** Powers 98%+ of all websites on the planet.\n🔹 **Full Stack:** Runs on browsers (React, Vue, Angular) and on servers via Node.js / Bun.\n🔹 Modern features: ES6+ arrow functions, async/await, promises, modules.",
        'h': "💛 **JavaScript (JS):**\n\n🔹 1995 mein Brendan Eich ne sirf 10 din mein banayi thi!\n🔹 Internet ki 98% websites JavaScript par chalti hain.\n🔹 Frontend (React, Vue) aur Backend (Node.js) dono jagah use hoti hai — full stack language hai!"
    },
    'minecraft': {
        'aliases': ['minecraft', 'mojang', 'steve', 'creeper', 'crafting'],
        'e': "⛏️ **Minecraft:**\n\n🔹 **What it is:** The best-selling video game of all time (over 300 Million copies sold!), developed by Mojang Studios (Markus 'Notch' Persson) and owned by Microsoft.\n🔹 **Core Gameplay:** A 3D sandbox where players explore a blocky, procedurally generated world, extract raw materials, craft tools, build structures, and fight mobs.\n🔹 **Game Modes:** Survival, Creative, Hardcore, Adventure, Spectator.\n🔹 **Iconic Mobs:** Creepers, Endermen, Zombies, Skeletons, Ender Dragon!\n🔹 And yes — my background is inspired by the gorgeous Minecraft movie world! 🌲⛏️",
        'h': "⛏️ **Minecraft:**\n\n🔹 Duniya ka sabse zyada bikne wala video game — 300 Million se zyada copies sold!\n🔹 Mojang ne banaya aur Microsoft ne khareeda.\n🔹 Sandbox game hai jahan blocks tod kar ghar, castles, aur machines bana sakte ho!\n🔹 Creepers, Enderman, aur Ender Dragon iske iconic mobs hain.\n🔹 Aur haan — mera chat background bhi Minecraft se inspired hai! 🌲⛏️"
    },
    'youtube': {
        'aliases': ['youtube', 'yt'],
        'e': "▶️ **YouTube:**\n\n🔹 World's largest video sharing platform, founded in February 2005 by Steve Chen, Chad Hurley, and Jawed Karim.\n🔹 Acquired by Google in 2006 for $1.65 Billion.\n🔹 Over **2.5 Billion monthly active users**.\n🔹 Over **500 hours of video** uploaded every single minute!",
        'h': "▶️ **YouTube:**\n\n🔹 Duniya ka sabse bada video streaming platform hai, 2005 mein shuru hua aur 2006 mein Google ne khareed liya.\n🔹 2.5 Billion se zyada log har mahine use karte hain.\n🔹 Har minute 500 ghante se zyada video upload hoti hai!"
    },
    'whatsapp': {
        'aliases': ['whatsapp', 'wa'],
        'e': "💬 **WhatsApp:**\n\n🔹 Founded in 2009 by Jan Koum and Brian Acton (ex-Yahoo employees).\n🔹 Acquired by Facebook (Meta) in 2014 for ~$19 Billion.\n🔹 Over **2.7 Billion active users**.\n🔹 Features end-to-end encryption using the Signal Protocol.",
        'h': "💬 **WhatsApp:**\n\n🔹 2009 mein Jan Koum aur Brian Acton ne banaya tha, 2014 mein Facebook ne $19 Billion mein khareeda.\n🔹 2.7 Billion log ise daily use karte hain.\n🔹 End-to-end encryption hoti hai — koi teesra message nahi padh sakta!"
    }
}

# Merge all 100 top apps into knowledge base
try:
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from app_knowledge import APPS_KNOWLEDGE
    KNOWLEDGE.update(APPS_KNOWLEDGE)
except ImportError:
    pass

def search_knowledge(text):
    text = text.lower().strip()
    
    # 1. Exact alias matching with word boundaries, sorted by alias length descending
    alias_pairs = []
    for key, item in KNOWLEDGE.items():
        aliases = item.get('aliases', [key])
        for alias in aliases:
            alias_pairs.append((alias, item))
    alias_pairs.sort(key=lambda x: len(x[0]), reverse=True)

    for alias, item in alias_pairs:
        # Prevent 1-letter aliases (like 'x' for Twitter) from matching math expressions
        if len(alias) <= 1 and text != alias and not re.search(r'\b(?:app|twitter|platform|social)\b', text):
            continue
        pattern = r'(?:\b|^)' + re.escape(alias) + r'(?:\b|$)'
        if re.search(pattern, text):
            return item

    # 2. Key phrase multi-word match (longest phrase first)
    keys_sorted = sorted(KNOWLEDGE.keys(), key=lambda k: len(k), reverse=True)
    for key in keys_sorted:
        words = key.split()
        if len(words) > 1 and all(re.search(r'\b' + re.escape(w) + r'\b', text) for w in words):
            return KNOWLEDGE[key]

    return None

# ═══════════════════════════════════════════
#   MATH VALIDATION & SYMPY SOLVER
# ═══════════════════════════════════════════
def looks_like_math(text):
    text = text.lower().strip()
    if not text:
        return False

    # Remove conversational filler words
    clean = re.sub(
        r'\b(what is|calculate|solve|compute|find|evaluate|simplify|value of|tell me|explain|bhai|yaar|kya|hai|kitna|hoga|batao|please|plz|formula of|formula for)\b',
        '', text, flags=re.I
    ).strip()

    if not clean:
        return False

    # Explicit math operations and function keywords
    math_keywords = [
        r'\b(derivative|diff|differentiate|integral|integrate|factor|factorize|factorise|expand|simplify)\b',
        r'\b(sin|cos|tan|asin|acos|atan|sec|csc|cot|sinh|cosh|tanh)\b',
        r'\b(sqrt|cbrt|log|ln|exp|factorial|fibonacci|lcm|gcd|hcf)\b',
        r'\b(prime|primes|hypotenuse|pythagoras|pythagorean)\b',
        r'\b(under\s*root|square\s*root|cube\s*root)\b',
        r'\b(compound\s*interest|simple\s*interest)\b',
        r'\b(area\s+of|volume\s+of|perimeter\s+of)\b'
    ]
    for kw in math_keywords:
        if re.search(kw, clean, re.I):
            return True

    # Percentages like "15% of 350"
    if re.search(r'\d+\s*%\s*(?:of)?\s*\d+', clean, re.I):
        return True

    # Permutations / Combinations like "10c3" or "5p2"
    if re.search(r'\b\d+\s*[cC]\s*\d+\b', clean) or re.search(r'\b\d+\s*[pP]\s*\d+\b', clean):
        return True

    # Factorials like "10!"
    if re.search(r'\b\d+!', clean):
        return True

    # Equations like "x^2 - 5x + 6 = 0" or "2x + 3 = 7"
    if '=' in clean and any(v in clean for v in ['x', 'y', 'z']):
        return True

    # Numbers with mathematical operators: +, -, *, /, ^, etc.
    has_digits = bool(re.search(r'\d', clean))
    has_operators = bool(re.search(r'[\+\-\*\/\^×÷√∛]', clean))
    if has_digits and has_operators:
        return True

    # Calculation words like "5 plus 10", "4 times 8", "10 divided by 2"
    if has_digits and re.search(r'\b(plus|minus|times|divided|into|multiplied|squared|cubed|power)\b', clean, re.I):
        return True

    # Pure alphabetical questions (like "what is instagram", "coding", "python") are NOT math!
    return False

def solve_math(query):
    """Use SymPy to solve virtually any math expression or equation."""
    if not looks_like_math(query):
        return None

    if not SYMPY_AVAILABLE:
        return basic_math(query)

    text = query.strip()
    clean = re.sub(r'\b(what is|calculate|solve|compute|find|evaluate|simplify|value of|bhai|yaar|kya|hai|kitna|hoga|batao|please|plz)\b', '', text, flags=re.I).strip()

    if not clean:
        return None

    x, y, z = symbols('x y z')

    try:
        # 1. Check for equations to solve: "x^2 - 5x + 6 = 0" or "solve 2x + 3 = 7"
        eq_match = re.match(r'(.+?)\s*=\s*(.+)', clean)
        if eq_match and ('x' in clean or 'y' in clean):
            lhs = eq_match.group(1).strip()
            rhs = eq_match.group(2).strip()
            transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
            lhs_expr = parse_expr(lhs, local_dict={'x': x, 'y': y, 'z': z, 'pi': pi, 'e': E}, transformations=transformations)
            rhs_expr = parse_expr(rhs, local_dict={'x': x, 'y': y, 'z': z, 'pi': pi, 'e': E}, transformations=transformations)
            equation = Eq(lhs_expr, rhs_expr)
            solutions = solve(equation)
            if solutions:
                sol_str = ', '.join([f"**{s}**" for s in solutions])
                return f"✅ **Equation Solved!**\n\n📝 Equation: {clean}\n\n📐 Solutions: {sol_str}"

        # 2. Derivative: "derivative of x^3 + 2x" or "diff x^2*sin(x)"
        deriv_match = re.match(r'(?:derivative|diff|differentiate|d/dx)\s*(?:of\s*)?(.+)', clean, re.I)
        if deriv_match:
            expr_str = deriv_match.group(1).strip()
            transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
            expr = parse_expr(expr_str, local_dict={'x': x, 'y': y, 'pi': pi, 'e': E}, transformations=transformations)
            result = diff(expr, x)
            return f"✅ **Derivative:**\n\nd/dx({expr}) = **{result}**"

        # 3. Integral: "integrate x^2" or "integral of sin(x)"
        int_match = re.match(r'(?:integrate|integral|∫)\s*(?:of\s*)?(.+)', clean, re.I)
        if int_match:
            expr_str = int_match.group(1).strip()
            transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
            expr = parse_expr(expr_str, local_dict={'x': x, 'y': y, 'pi': pi, 'e': E}, transformations=transformations)
            result = integrate(expr, x)
            return f"✅ **Integral:**\n\n∫({expr}) dx = **{result} + C**"

        # 4. Factor: "factor x^2 - 5x + 6"
        factor_match = re.match(r'(?:factor|factorize|factorise)\s*(?:of\s*)?(.+)', clean, re.I)
        if factor_match:
            expr_str = factor_match.group(1).strip()
            transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
            expr = parse_expr(expr_str, local_dict={'x': x, 'y': y, 'pi': pi, 'e': E}, transformations=transformations)
            result = factor(expr)
            return f"✅ **Factored:**\n\n{expr} = **{result}**"

        # 5. Expand: "expand (x+2)(x+3)"
        expand_match = re.match(r'(?:expand)\s*(?:of\s*)?(.+)', clean, re.I)
        if expand_match:
            expr_str = expand_match.group(1).strip()
            transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
            expr = parse_expr(expr_str, local_dict={'x': x, 'y': y, 'pi': pi, 'e': E}, transformations=transformations)
            result = expand(expr)
            return f"✅ **Expanded:**\n\n{expr} = **{result}**"

        # 6. Simplify: "simplify (x^2-1)/(x-1)"
        simp_match = re.match(r'(?:simplify)\s*(?:of\s*)?(.+)', clean, re.I)
        if simp_match:
            expr_str = simp_match.group(1).strip()
            transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
            expr = parse_expr(expr_str, local_dict={'x': x, 'y': y, 'pi': pi, 'e': E}, transformations=transformations)
            result = simplify(expr)
            return f"✅ **Simplified:**\n\n{expr} = **{result}**"

        # 7. Prime check
        prime_match = re.match(r'is\s+(\d+)\s+(?:a\s+)?prime', clean, re.I)
        if prime_match:
            n = int(prime_match.group(1))
            if isprime(n):
                return f"✅ Yes! **{n}** is a **prime number** 🔢"
            else:
                factors = factorint(n)
                factor_str = ' × '.join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()])
                return f"❌ No, **{n}** is NOT prime.\n\nPrime factorization: **{n} = {factor_str}**"

        # 8. Factorize number: "factorize 360"
        num_factor_match = re.match(r'(?:prime\s+)?(?:factorize|factorization|factors?\s+of)\s+(\d+)', clean, re.I)
        if num_factor_match:
            n = int(num_factor_match.group(1))
            factors = factorint(n)
            factor_str = ' × '.join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()])
            return f"✅ **Prime Factorization:**\n\n{n} = **{factor_str}**"

        # 9. LCM / GCD
        lcm_match = re.match(r'lcm\s+(?:of\s+)?(\d+)\s+(?:and\s+)?(\d+)', clean, re.I)
        if lcm_match:
            a, b = int(lcm_match.group(1)), int(lcm_match.group(2))
            return f"✅ **LCM({a}, {b}) = {lcm(a, b)}**"

        gcd_match = re.match(r'(?:gcd|hcf)\s+(?:of\s+)?(\d+)\s+(?:and\s+)?(\d+)', clean, re.I)
        if gcd_match:
            a, b = int(gcd_match.group(1)), int(gcd_match.group(2))
            return f"✅ **GCD/HCF({a}, {b}) = {gcd(a, b)}**"

        # 10. nCr / nPr
        ncr_match = re.match(r'(\d+)\s*[cC]\s*(\d+)', clean)
        if ncr_match:
            n_val, r_val = int(ncr_match.group(1)), int(ncr_match.group(2))
            return f"✅ **C({n_val},{r_val}) = {binomial(n_val, r_val)}**"

        npr_match = re.match(r'(\d+)\s*[pP]\s*(\d+)', clean)
        if npr_match:
            n_val, r_val = int(npr_match.group(1)), int(npr_match.group(2))
            result = factorial(n_val) / factorial(n_val - r_val)
            return f"✅ **P({n_val},{r_val}) = {result}**"

        # 11. Percentage
        pct_match = re.match(r'(\d+(?:\.\d+)?)\s*%\s*of\s+(\d+(?:\.\d+)?)', clean, re.I)
        if pct_match:
            pct, val = float(pct_match.group(1)), float(pct_match.group(2))
            return f"✅ **{pct}% of {val} = {pct/100*val}**"

        # 12. Fibonacci
        fib_match = re.match(r'(?:fibonacci|fib)\s+(\d+)', clean, re.I) or re.match(r'(\d+)(?:st|nd|rd|th)?\s+fibonacci', clean, re.I)
        if fib_match:
            n_val = min(int(fib_match.group(1)), 100)
            fib_n = sympy.fibonacci(n_val)
            return f"✅ **Fibonacci #{n_val} = {fib_n}**"

        # 13. General expression evaluation
        # Normalize text for SymPy
        expr_str = clean
        expr_str = re.sub(r'\bunder\s*root\b', 'sqrt', expr_str, flags=re.I)
        expr_str = re.sub(r'\bsquare\s+root\s+of\b', 'sqrt', expr_str, flags=re.I)
        expr_str = re.sub(r'\bcube\s+root\s+of\b', 'cbrt', expr_str, flags=re.I)
        expr_str = re.sub(r'√', 'sqrt', expr_str)
        expr_str = re.sub(r'\bmultiplied\s+by\b', '*', expr_str, flags=re.I)
        expr_str = re.sub(r'\bdivided\s+by\b', '/', expr_str, flags=re.I)
        expr_str = re.sub(r'\btimes\b', '*', expr_str, flags=re.I)
        expr_str = re.sub(r'\binto\b', '*', expr_str, flags=re.I)
        expr_str = re.sub(r'\bplus\b', '+', expr_str, flags=re.I)
        expr_str = re.sub(r'\bminus\b', '-', expr_str, flags=re.I)
        expr_str = re.sub(r'\bsquared\b', '**2', expr_str, flags=re.I)
        expr_str = re.sub(r'\bcubed\b', '**3', expr_str, flags=re.I)
        expr_str = re.sub(r'\bto\s+the\s+power\s+(?:of\s+)?(\d+)', r'**\1', expr_str, flags=re.I)
        expr_str = re.sub(r'(\d+)!', r'factorial(\1)', expr_str)

        transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

        try:
            parsed = parse_expr(
                expr_str,
                local_dict={
                    'x': x, 'y': y, 'z': z,
                    'pi': pi, 'e': E,
                    'sqrt': sqrt, 'cbrt': cbrt,
                    'sin': sin, 'cos': cos, 'tan': tan,
                    'asin': asin, 'acos': acos, 'atan': atan,
                    'sec': sec, 'csc': csc, 'cot': cot,
                    'log': log, 'ln': ln, 'exp': exp,
                    'factorial': factorial, 'abs': sympy.Abs,
                },
                transformations=transformations
            )

            # If expression has free symbols, show simplified form only if math operators/commands were present
            if parsed.free_symbols:
                if re.search(r'[\+\-\*\/\^=]', clean) or re.search(r'\b(simplify|expand|factor|solve)\b', query, re.I):
                    simplified = simplify(parsed)
                    return f"✅ **Simplified:**\n\n{parsed} = **{simplified}**"
                return None

            # Evaluate numerically
            result = N(parsed)

            # Format nicely
            if result == int(result):
                formatted = f"{int(result):,}"
            else:
                formatted = f"{float(result):.8g}"

            return f"✅ **Result = {formatted}**"
        except:
            pass

    except Exception as e:
        pass

    return None

def basic_math(query):
    """Fallback math solver without SymPy."""
    text = query.strip().lower()
    text = re.sub(r'what is|calculate|solve|compute|bhai|yaar|kya|hai|kitna|hoga|batao|please|plz|value of', '', text, flags=re.I).strip()

    # Simple arithmetic
    text = text.replace('×', '*').replace('÷', '/').replace('^', '**')
    text = re.sub(r'(\d+)\s*!\s*', lambda m: str(math.factorial(int(m.group(1)))), text)
    text = re.sub(r'√(\d+)', r'math.sqrt(\1)', text)
    text = re.sub(r'sqrt\s*\(?(\d+)\)?', r'math.sqrt(\1)', text, flags=re.I)

    try:
        result = eval(text, {"__builtins__": {}, "math": math})
        if isinstance(result, (int, float)) and not math.isnan(result) and math.isfinite(result):
            if isinstance(result, float) and result == int(result):
                return f"✅ **Result = {int(result):,}**"
            return f"✅ **Result = {result:,.8g}**"
    except:
        pass
    return None

# ═══════════════════════════════════════════
#   MAIN CHAT API ENDPOINT
# ═══════════════════════════════════════════
@app.route('/api/chat', methods=['GET', 'POST'])
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({'status': 'online', 'name': 'Housie AI Backend', 'version': '4.0'})
    data = request.json or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    text = message.lower()
    lang = detect_lang(message)
    is_h = lang == 'hinglish'

    # 1. Creator
    if re.search(r'who (created|made|built|coded|developed) (you|housie)|who is your (creator|maker|developer|author)|tumhe kisne (banaya|code kiya|design kiya)|aapko kisne banaya|kisne banaya', text):
        return jsonify({'response': CREATOR_HI if is_h else CREATOR_EN, 'language': lang})

    # 2. Greetings
    if re.match(r'^(hi+|hello+|hey+|yo|sup|hola)\b', text):
        resp = "Hey yaar! Housie hoon 😄 Math, Science, Coding — kuch bhi pucho! SymPy engine se main KUCH BHI solve kar sakta hoon!" if is_h else "Hello! I'm Housie 😊 Powered by SymPy — I can solve ANY math problem! Ask me calculus, algebra, physics, CS, and more!"
        return jsonify({'response': resp, 'language': lang})

    if re.search(r'namaste|namaskar', text):
        return jsonify({'response': "Namaste! 🙏 Housie ready hai!" if is_h else "Namaste! 🙏 How can I help you?", 'language': lang})

    if re.search(r'how are you|kaise ho|kaisa hai|kya haal', text):
        return jsonify({'response': "Ekdum mast! 🤩 Kya solve karein?" if is_h else "Doing fantastic! ⚡ What shall we tackle?", 'language': lang})

    if re.search(r'your name|tumhara naam|tera naam|who are you|kaun ho|what are you', text):
        return jsonify({'response': "Main Housie — tera AI dost! 🧠 SymPy powered math genius + encyclopedia!" if is_h else "I'm Housie — your AI companion! 🧠 Powered by SymPy for unlimited math solving!", 'language': lang})

    if re.search(r'what can you do|kya kar sakte|features|help me|capabilities', text):
        resp = ("🚀 Main kar sakta hoon:\n📐 **Calculus** — derivatives, integrals\n🔢 **Algebra** — solve equations, factor, expand\n√ **Any Math** — trig, roots, logs, factorial\n📊 LCM, GCD, nCr, nPr, Fibonacci, Primes\n💰 Compound/Simple Interest\n📏 Geometry — area, volume, Pythagoras\n🔬 **Science** — Physics, Chemistry, Biology, CS\n😂 Jokes, Motivation, Fun Facts\n\n**SymPy se main KUCH BHI solve kar sakta hoon!** Bas pucho! 🧠" if is_h else
         "🚀 I can help with:\n📐 **Calculus** — derivatives, integrals, limits\n🔢 **Algebra** — solve ANY equation, factor, expand, simplify\n√ **All Math** — trig, roots, logs, factorial, complex numbers\n📊 LCM, GCD, nCr, nPr, Fibonacci, Prime factorization\n💰 Compound/Simple Interest\n📏 Geometry — area, volume, Pythagoras\n🔬 **Science** — 30+ topics in Physics, Chemistry, Bio, CS\n😂 Jokes, Motivation, Fun Facts\n\n**Powered by SymPy — I can solve virtually ANY math problem!** 🧠")
        return jsonify({'response': resp, 'language': lang})

    # 3. Time & Date
    if re.search(r'what time|kitna baj|time kya|current time', text):
        t = datetime.datetime.now().strftime('%I:%M %p')
        return jsonify({'response': f'⏰ Current time: **{t}** (IST)', 'language': lang})

    if re.search(r"today.?s date|aaj ki date|what date|kon sa din", text):
        d = datetime.datetime.now().strftime('%A, %B %d, %Y')
        return jsonify({'response': f'📅 Today: **{d}**', 'language': lang})

    # 4. Jokes
    if re.search(r'joke|mazak|funny|hasao|haso|sunao|laugh', text):
        return jsonify({'response': pick(JOKES_HI if is_h else JOKES_EN), 'language': lang})

    # 5. Motivation
    if re.search(r'motiv|quote|inspire|hausla|himmat|encouragement', text):
        return jsonify({'response': pick(MOTIVATION_HI if is_h else MOTIVATION_EN), 'language': lang})

    # 6. Fun Facts
    if re.search(r'fun fact|did you know|interesting|rochak|amazing fact|fact', text):
        return jsonify({'response': pick(FUN_FACTS_HI if is_h else FUN_FACTS_EN), 'language': lang})

    # 7. Weather
    if re.search(r'weather|mausam|barish|garmi', text):
        return jsonify({'response': "Weather data mere paas nahi hai 😅 Google Weather try karo!" if is_h else "I don't have live weather data! 🌤️ Try Google Weather.", 'language': lang})

    # 8. Knowledge Base
    kb = search_knowledge(text)
    if kb:
        return jsonify({'response': kb['h'] if is_h else kb['e'], 'language': lang})

    # 9. Math Solver (SymPy powered!)
    math_result = solve_math(message)
    if math_result:
        suffix = "\n\nAur kuch solve karoon? 😊" if is_h else "\n\nNeed anything else solved? 😊"
        return jsonify({'response': math_result + suffix, 'language': lang, 'isMath': True})

    # 10. Smart Fallback
    fallbacks = [
        "Hmm, yeh topic abhi mere knowledge mein nahi hai! 🤔 Try karo:\n• derivative of x^3\n• solve x^2 - 5x + 6 = 0\n• is 97 prime?\n• explain quantum computing\n• fibonacci 20",
        "Bhai, yeh thoda zyada mushkil hai! 😅 Math, Physics, CS pe try karo!",
        "Interesting sawal! 🧠 Trigonometry, calculus, ya science concepts try karo!"
    ] if is_h else [
        "That's beyond my current knowledge! 🤔 Try:\n• derivative of x^3 + 2x\n• solve x^2 - 5x + 6 = 0\n• factor x^3 - 8\n• is 97 prime?\n• explain machine learning",
        "Not in my training data yet! 😅 I excel at math, physics, CS, and biology!",
        "Interesting question! 🧠 Try calculus, algebra, or any of 30+ science topics!"
    ]
    return jsonify({'response': pick(fallbacks), 'language': lang})

# ═══════════════════════════════════════════
#   SERVE STATIC FILES
# ═══════════════════════════════════════════
_STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.route('/')
def serve_index():
    return send_from_directory(_STATIC_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(_STATIC_DIR, filename)

if __name__ == '__main__':
    print("Housie AI Python server starting at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
