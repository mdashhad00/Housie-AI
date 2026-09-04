const express = require('express');
const path = require('path');
const cors = require('cors');
const { parseAndEvaluateMath } = require('./mathEngine');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ─── LANGUAGE DETECTION ───────────────────────────────────────────────────────
const hinglishWords = ['kya','hai','bhai','yaar','ek','do','teen','mera','tera','aaj','kal','kaise','kaisa','karo','batao','kuch','nahi','haan','achha','accha','matlab','toh','bhi','se','ka','ki','ke','mein','hoon','kab','kahan','kyun','zaroor','bilkul','lekin','aur','par','mujhe','tumhe','apna','apni','koi','sab','sirf','wala','wali','raha','gaya','gayi','shukriya','namaste','alvida','bolo','sun','suno','bol','bata','kitna','hoga','kaun','kon','dedo','dekho','lelo','sunao','banaya','isko','uska','unka','jab','tab','yeh','woh','hum','tum','main','aap','nahi','matlab'];

function detectLanguage(text) {
  const words = text.toLowerCase().split(/\s+/);
  let count = 0;
  words.forEach(w => { if (hinglishWords.includes(w)) count++; });
  return (count / (words.length || 1)) >= 0.12 ? 'hinglish' : 'english';
}

function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

// ─── STATIC CONTENT BANKS ────────────────────────────────────────────────────

const CREATOR_EN = `🔥 Oof, bold question! I was forged from raw code by a **16-year-old absolute genius** — a coding prodigy who writes blazing algorithms with his bare naked hands, continuously, without stopping, without touching grass, without sleeping. He is basically a human supercomputer who decided to build me instead of doing anything normal. Respect the legend. ⚡💻🚀`;
const CREATOR_HI = `😤 Bhai, ek 16-saal ka coding prodigy ne mujhe banaya hai! Woh ek aisa genius hai jo apne **nange haathon se** continuously raw algorithms likhta hai — bina soye, bina grass touch kiye, bina break liye! Woh basically ek insaan ke roop mein ek supercomputer hai. Usse salaam karo bhai! ⚡💻🔥`;

const JOKES_EN = [
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
  "Why do programmers prefer dark mode? Because light attracts bugs! 🐛😂",
  "I told my computer I needed a break. Now it won't stop sending me vacation ads! 🏖️😂",
  "Why do Java developers wear glasses? Because they don't C#! 👓😂",
  "A SQL query walks into a bar and asks two tables: 'Can I join you?' 🍺😂",
  "How many programmers does it take to change a light bulb? None — that's a hardware problem! 💡😂",
  "Debugging is like being the detective in a crime movie where you are also the murderer! 🔍😂",
  "Why did the programmer quit his job? Because he didn't get arrays (a raise)! 💰😂",
  "There are only 10 types of people: those who understand binary and those who don't! 🖥️😂",
  "Parallel lines have so much in common. It's a shame they'll never meet! 📐😂",
  "!false — it's funny because it's true! 😂"
];

const JOKES_HI = [
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
  "Teacher: '2+2 kitna?' Pappu: 'Sir GST lagega kya?' 😂",
  "Maa: 'Padhai kar!' Main: 'Housie AI se padh raha hoon!' 📖😅",
  "Boss: 'AI se kaam karwao!' Main: *boss ko replace kar doon kya?* 🤖😂",
  "Exam mein question: '8 ko ulta karo.' Student ne paper ulta kar diya! 😂",
  "Programmer ki girlfriend: 'Mujhse pyar karte ho?' Programmer: 'True!' 🖥️💕😂",
  "WiFi ka naam 'Sharma Ji Ka Beta' rakh do — sab connect karne ki koshish karenge! 📶😂"
];

const MOTIVATION_EN = [
  '"The only way to do great work is to love what you do." — Steve Jobs ✨',
  '"In the middle of every difficulty lies opportunity." — Albert Einstein 💡',
  '"Dream big. Work hard. Stay humble." 🚀',
  '"Code is poetry written in logic." — Unknown 💻',
  '"Success is not final, failure is not fatal — it is the courage to continue that counts." — Churchill 💪',
  '"You don\'t need to be great to start, but you need to start to be great." 🔥',
  '"Every expert was once a beginner." 🌱',
];

const MOTIVATION_HI = [
  '"Mushkilein aati hain toh hausla mat haaro — tumhe strong bana rahi hain!" 💪',
  '"Sapne bade rakhna, mehnat karo — sab mumkin hai!" 🌟',
  '"Zindagi mein shortcuts nahi — bas ek step at a time!" 🔥',
  '"Code likhna shayari jaisi hai — ek baar seekh lo, duniya badal do!" 💻',
  '"Failure ek temporary state hai — give up karna permanent hai." 🚀',
  '"Roz thoda behtar bano — 1% improvement, 365 din = 37x behtar!" 📈',
];

const FUN_FACTS_EN = [
  "🍯 Honey never spoils! 3000-year-old honey from Egyptian tombs was still perfectly edible.",
  "🧠 Your brain uses about 20% of your body's energy but is only 2% of your weight!",
  "🐙 An octopus has 3 hearts, blue blood, and can change shape to fit through any hole its beak can pass through!",
  "⚡ Lightning strikes Earth about 100 times per second — that's 8.6 million times per day!",
  "🌊 The ocean contains more historical artifacts than all the world's museums combined!",
  "🔬 There are more atoms in a grain of sand than stars in the Milky Way galaxy!",
  "🐦 Crows are so intelligent they can recognize human faces and hold grudges for years!",
  "🌍 Earth's core is as hot as the surface of the Sun — about 5,778 Kelvin!",
];

const FUN_FACTS_HI = [
  "🍯 Shahed kabhi kharab nahi hoti! 3000 saal purani Egyptian shahed bhi khane layak thi.",
  "🧠 Dimaag 2.5 petabytes tak data store kar sakta hai — 3 million ghante ki movies!",
  "🐙 Octopus ke 3 dil hain, neela khoon hai, aur woh apna roop badal sakta hai!",
  "⚡ Bijli prithvi par ek second mein 100 baar girti hai — din mein 86 lakh baar!",
  "🌊 Samundar mein saari duniya ke museums se zyada historical cheezein hain!",
  "🔬 Ek reth ke dane mein Milky Way ke taaron se zyada atoms hain!",
];

// ─── ADVANCED KNOWLEDGE BASE ─────────────────────────────────────────────────

const KNOWLEDGE = {
  // Science & Physics
  'quantum computing': { e: "🤯 **Quantum Computing** uses *qubits* that can be 0 AND 1 simultaneously (superposition). While a classical bit is like a coin (heads or tails), a qubit is a spinning coin — both at once!\n\n🔹 Key concepts: Superposition, Entanglement, Quantum gates\n🔹 Used for: Cryptography, Drug discovery, Climate modeling\n🔹 Companies: IBM, Google (Sycamore), D-Wave", h: "🤯 Quantum Computing qubits 0 aur 1 dono ek saath ho sakte hain (superposition). IBM, Google jaise companies is par kaam kar rahe hain — yeh future ki technology hai!" },
  'black hole': { e: "🌌 **Black Holes** are regions where gravity is so powerful that even light cannot escape! They form when massive stars collapse.\n\n🔹 Event Horizon: The point of no return\n🔹 Singularity: Infinite density at the center\n🔹 Time Dilation: Time slows near a black hole\n🔹 Hawking Radiation: Tiny radiation they emit\n\nThe nearest black hole is ~1,000 light-years away!", h: "🌌 Black hole ek aisi jagah hai jahan gravity itni zyada hoti hai ki light bhi escape nahi kar sakti! Wahan time bhi slow ho jata hai — Einstein ki relativity!" },
  'relativity': { e: "⏳ **Theory of Relativity** by Einstein has two parts:\n\n1️⃣ **Special Relativity** (1905): Time slows down as speed increases. At the speed of light, time stops!\n   Formula: E = mc² (Energy = mass × speed of light²)\n\n2️⃣ **General Relativity** (1915): Massive objects warp spacetime, causing gravity.", h: "⏳ Einstein ki Relativity kehti hai:\n1. Special Relativity: Speed badhne se time slow ho jata hai!\n2. General Relativity: Badi cheezein space-time ko curve karti hain, isi se gravity hoti hai! E = mc²" },
  'gravity': { e: "🍎 **Gravity** is one of the four fundamental forces of nature — the weakest but the one with the longest range!\n\n🔹 Newton's Law: F = Gm₁m₂/r²\n🔹 Einstein's View: Gravity = curvature of spacetime\n🔹 Gravitational waves: Ripples in spacetime (detected in 2015!)\n🔹 Escape velocity from Earth = 11.2 km/s", h: "🍎 Gravity ek fundamental force hai! Newton ne bataya F = Gm₁m₂/r². Einstein ne kaha gravity spacetime ka moodna hai. Earth se escape ke liye 11.2 km/s speed chahiye!" },
  'dna': { e: "🧬 **DNA (Deoxyribonucleic Acid)** is the blueprint of life!\n\n🔹 Double helix structure discovered by Watson & Crick (1953)\n🔹 Made of 4 bases: Adenine (A), Thymine (T), Guanine (G), Cytosine (C)\n🔹 Human DNA: ~3 billion base pairs, 46 chromosomes\n🔹 If stretched out, your DNA would reach the Sun and back ~300 times!", h: "🧬 DNA zindagi ka blueprint hai! Double helix structure mein 4 bases hain — A, T, G, C. Insani DNA 3 billion base pairs ka hai jo Sun tak 300 baar pahunch sakta hai!" },
  'photosynthesis': { e: "🌿 **Photosynthesis** is how plants make food from sunlight!\n\nEquation: 6CO₂ + 6H₂O + Light Energy → C₆H₁₂O₆ + 6O₂\n\n🔹 Chlorophyll absorbs red & blue light\n🔹 Light-dependent & light-independent (Calvin cycle) reactions\n🔹 Plants produce ~150 billion tonnes of sugar per year!", h: "🌿 Photosynthesis mein plants suraj ki roshni, CO2, aur paani se sugar aur oxygen banate hain! Formula: 6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂" },
  'newton laws': { e: "⚙️ **Newton's Three Laws of Motion:**\n\n1️⃣ **Law of Inertia:** An object at rest stays at rest; an object in motion stays in motion (unless acted upon).\n2️⃣ **F = ma:** Force = Mass × Acceleration\n3️⃣ **Action-Reaction:** Every action has an equal & opposite reaction.\n\nThese laws govern everything from cars to rockets! 🚀", h: "⚙️ Newton ke 3 laws:\n1. Inertia: Object tab tak nahi hilta jab tak force na lage\n2. F = ma (Force = Mass × Acceleration)\n3. Har action ka equal aur opposite reaction hota hai! 🚀" },
  
  // Computer Science
  'machine learning': { e: "🤖 **Machine Learning (ML)** is AI training itself from data!\n\n🔹 Types: Supervised, Unsupervised, Reinforcement Learning\n🔹 Supervised: Learns from labeled examples (like email spam detection)\n🔹 Neural Networks: Inspired by the human brain\n🔹 Deep Learning: Neural nets with many layers\n🔹 Applications: Image recognition, Language models, Self-driving cars", h: "🤖 Machine Learning mein computer data se khud seekhta hai! Supervised, Unsupervised, aur Reinforcement Learning — teen types hain. Neural networks brain ki tarah kaam karte hain!" },
  'api': { e: "🔌 **API (Application Programming Interface)** is a contract between two software systems.\n\n🔹 Like a waiter: you (client) → waiter (API) → kitchen (server)\n🔹 REST API: Uses HTTP methods (GET, POST, PUT, DELETE)\n🔹 JSON: Most common data format for APIs\n🔹 Examples: Google Maps API, Twitter API, Payment gateways", h: "🔌 API ek bridge ki tarah hai jo do softwares ko connect karta hai. Jaise waiter restaurant mein order kitchen tak le jata hai! REST API sabse popular hai — HTTP methods use karta hai." },
  'blockchain': { e: "⛓️ **Blockchain** is a distributed, immutable ledger of transactions!\n\n🔹 Blocks: Each block contains data + a cryptographic hash of the previous block\n🔹 Decentralized: No single authority controls it\n🔹 Consensus: Proof of Work (Bitcoin) or Proof of Stake (Ethereum)\n🔹 Smart Contracts: Self-executing code on the blockchain\n🔹 Applications: Cryptocurrency, Supply chain, Voting systems", h: "⛓️ Blockchain ek distributed ledger hai jahan transactions immutable (change-proof) hoti hain! Har block mein previous block ka hash hota hai. Bitcoin aur Ethereum isi par hain!" },
  'operating system': { e: "🖥️ **Operating System (OS)** manages all hardware & software resources!\n\n🔹 Kernel: Core of the OS — manages CPU, memory, I/O\n🔹 Process Management: Scheduling (FCFS, Round Robin, Priority)\n🔹 Memory Management: RAM allocation, virtual memory, paging\n🔹 File Systems: NTFS (Windows), ext4 (Linux), APFS (Mac)\n🔹 Popular OS: Windows, Linux, macOS, Android, iOS", h: "🖥️ Operating System hardware aur software ko manage karta hai! Kernel CPU, RAM manage karta hai. Popular OS: Windows, Linux, macOS, Android. Process scheduling bahut important hai!" },
  'sorting algorithms': { e: "📊 **Sorting Algorithms** — the bread and butter of programming!\n\n| Algorithm | Best | Worst | Space |\n|-----------|------|-------|-------|\n| Bubble Sort | O(n) | O(n²) | O(1) |\n| Merge Sort | O(n log n) | O(n log n) | O(n) |\n| Quick Sort | O(n log n) | O(n²) | O(log n) |\n| Heap Sort | O(n log n) | O(n log n) | O(1) |\n\nMerge Sort & Heap Sort are generally preferred for large datasets!", h: "📊 Sorting Algorithms:\n- Bubble Sort: O(n²) — slow but simple\n- Merge Sort: O(n log n) — stable, reliable\n- Quick Sort: O(n log n) avg — fast in practice\n- Heap Sort: O(n log n) — in-place!\nMerge Sort aur Quick Sort sabse common interview mein!" },
  
  // Mathematics
  'pythagoras': { e: "📐 **Pythagorean Theorem:** In a right triangle, a² + b² = c²\n\n🔹 a, b = two legs of the triangle\n🔹 c = hypotenuse (longest side)\n🔹 Common Pythagorean triples: (3,4,5), (5,12,13), (8,15,17)\n\nProof: Draw a square on each side — the two smaller squares equal the largest!", h: "📐 Pythagorean Theorem: a² + b² = c²\nRight triangle mein hypotenuse ka square baaki dono sides ke squares ke sum ke barabar hota hai! Common triples: (3,4,5), (5,12,13)" },
  'statistics': { e: "📈 **Statistics Basics:**\n\n🔹 **Mean** = Sum ÷ Count\n🔹 **Median** = Middle value (sorted)\n🔹 **Mode** = Most frequent value\n🔹 **Variance** = Average of squared differences from mean\n🔹 **Standard Deviation** = √Variance\n🔹 **Normal Distribution**: Bell curve — 68-95-99.7 rule!", h: "📈 Statistics mein:\n- Mean = average\n- Median = sorted middle value\n- Mode = sabse zyada aane wala value\n- Standard Deviation = spread measure\nYeh sab machine learning mein bhi bahut kaam aata hai!" },
  'calculus': { e: "∫ **Calculus** — the mathematics of change!\n\n🔹 **Differentiation:** Rate of change, finding slopes\n   d/dx(xⁿ) = nxⁿ⁻¹\n🔹 **Integration:** Area under a curve, reverse of differentiation\n   ∫xⁿ dx = xⁿ⁺¹/(n+1) + C\n🔹 **Fundamental Theorem:** Differentiation and integration are inverses!\n🔹 Applications: Physics (velocity, acceleration), Engineering, Economics", h: "∫ Calculus change ka mathematics hai!\n- Differentiation: rate of change, d/dx(xⁿ) = nxⁿ⁻¹\n- Integration: area under curve, ∫xⁿ dx = xⁿ⁺¹/(n+1) + C\nPhysics, engineering, economics sab jagah use hota hai!" },

  // General Knowledge
  'photon': { e: "💡 **Photons** are massless particles of light! They are both a wave and a particle (wave-particle duality).\n\n🔹 Speed: 3 × 10⁸ m/s in vacuum\n🔹 Energy: E = hf (h = Planck's constant, f = frequency)\n🔹 A photon from the Sun takes ~8 minutes to reach Earth!\n🔹 Your eyes can detect a single photon in complete darkness!", h: "💡 Photon light ka particle hai — massless! Speed = 3×10⁸ m/s. Wave aur particle dono hai (duality). Sun se photon 8 minute mein Earth pahunchta hai!" },
  'internet': { e: "🌐 **How the Internet Works:**\n\n🔹 TCP/IP: The fundamental communication protocol\n🔹 DNS: Converts domain names to IP addresses (like a phone book)\n🔹 HTTP/HTTPS: Protocol for web pages\n🔹 Routers: Direct data packets across networks\n🔹 Data travels as packets — each taking possibly different routes!\n🔹 ~5 billion people use the internet today!", h: "🌐 Internet TCP/IP protocol par kaam karta hai! DNS domain names ko IP addresses mein convert karta hai. Data packets ki form mein travel karta hai, aur HTTP/HTTPS web pages ke liye use hota hai." },
  'climate change': { e: "🌍 **Climate Change** — the defining challenge of our era!\n\n🔹 Greenhouse gases (CO₂, CH₄) trap heat in the atmosphere\n🔹 Earth's average temperature has risen ~1.2°C since pre-industrial times\n🔹 Effects: Rising sea levels, extreme weather, species extinction\n🔹 Solutions: Renewable energy, Carbon capture, Electric vehicles\n🔹 Paris Agreement: Limit warming to 1.5°C above pre-industrial levels", h: "🌍 Climate Change: Greenhouse gases (CO₂, CH₄) heat trap karte hain. Temperature 1.2°C badh gaya hai. Rising sea levels, extreme weather — yeh sab effects hain. Solar aur wind energy se isse rok sakte hain!" },
};

// Merge all 100 top apps into knowledge base
try {
  const APPS_KB = require('./apps_kb.json');
  Object.assign(KNOWLEDGE, APPS_KB);
} catch (e) {}

function searchKnowledge(text) {
  for (const [key, val] of Object.entries(KNOWLEDGE)) {
    const keywords = key.split(' ');
    if (keywords.every(kw => text.includes(kw))) {
      return val;
    }
  }
  // Partial single-word matches
  for (const [key, val] of Object.entries(KNOWLEDGE)) {
    const words = key.split(' ');
    if (words.some(w => w.length > 4 && text.includes(w))) {
      return val;
    }
  }
  return null;
}

// ─── CHAT API ─────────────────────────────────────────────────────────────────

app.post('/api/chat', (req, res) => {
  const { message } = req.body;
  if (!message) return res.status(400).json({ error: 'Message is required' });

  const text = message.trim().toLowerCase();
  const lang = detectLanguage(message);
  const isH = lang === 'hinglish';

  // 1. Creator
  if (/(who (created|made|built|coded|developed) (you|housie)|who is your (creator|maker|developer|author)|tumhe kisne (banaya|code kiya|design kiya)|aapko kisne banaya|kisne banaya)/i.test(text)) {
    return res.json({ response: isH ? CREATOR_HI : CREATOR_EN, language: lang });
  }

  // 2. Greetings
  if (/^(hi+|hello+|hey+|yo|sup|hola)\b/.test(text)) {
    return res.json({ response: isH ? "Hey yaar! Housie hoon 😄 Math, Science, Coding, ya koi bhi sawal pucho — main ready hoon!" : "Hello! I'm Housie 😊 Ask me anything — math, science, coding, trigonometry, and more! I'm your AI buddy.", language: lang });
  }
  if (/namaste|namaskar/.test(text)) return res.json({ response: isH ? "Namaste! 🙏 Housie ready hai tumhari help ke liye!" : "Namaste! 🙏 How can I help you today?", language: lang });
  if (/how are you|kaise ho|kaisa hai|kya haal/.test(text)) return res.json({ response: isH ? "Ekdum mast hoon yaar! 🤩 Tu bata kya solve karna hai?" : "Doing absolutely fantastic! ⚡ What shall we explore today?", language: lang });
  if (/your name|tumhara naam|tera naam|who are you|kaun ho|what are you/.test(text)) return res.json({ response: isH ? "Main Housie hoon — tera AI dost! 🧠 Math, science, coding — sab mujhse pucho!" : "I'm Housie — your AI companion! 🧠 Built to tackle math, science, coding questions and more!", language: lang });
  if (/what can you do|kya kar sakte|features|help me|capabilities/.test(text)) return res.json({ response: isH ? "🚀 Main kar sakta hoon:\n📐 Trigonometry — sin(30°), cos(60°), tan(45°)\n√ Roots — √144, cube root of 27\n🔢 Quadratics — x²-5x+6=0\n📊 LCM, GCM, Permutations, Combinations\n💰 Compound Interest, Simple Interest\n📏 Area, Volume (circle, sphere, rectangle)\n🔬 Science Q&A — Physics, Chemistry, CS\n😂 Jokes & Motivation\n\nBas pucho yaar, main hoon na!" : "🚀 I can help you with:\n📐 Trigonometry — sin(30°), cos(60°)\n√ Roots, Powers, Logs — √144, log(100)\n🔢 Quadratic equations — x²-5x+6=0\n📊 LCM, GCD, nCr, nPr, Fibonacci\n💰 Compound & Simple Interest\n📏 Area & Volume calculations\n🔬 Science — Physics, CS, Biology\n😂 Jokes & Motivation!\n\nJust ask me anything!", language: lang });

  // 3. Time & Date
  if (/what time|kitna baj|time kya|current time/.test(text)) {
    const t = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
    return res.json({ response: `⏰ Current time: **${t}** (IST)`, language: lang });
  }
  if (/today.?s date|aaj ki date|what date|kon sa din/.test(text)) {
    const d = new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    return res.json({ response: `📅 Today's date: **${d}**`, language: lang });
  }

  // 4. Jokes
  if (/joke|mazak|funny|hasao|haso|sunao|laugh/.test(text)) {
    return res.json({ response: pick(isH ? JOKES_HI : JOKES_EN), language: lang });
  }

  // 5. Motivation
  if (/motiv|quote|inspire|hausla|himmat|encouragement/.test(text)) {
    return res.json({ response: pick(isH ? MOTIVATION_HI : MOTIVATION_EN), language: lang });
  }

  // 6. Fun Facts
  if (/fun fact|did you know|interesting|rochak|amazing fact|fact/.test(text)) {
    return res.json({ response: pick(isH ? FUN_FACTS_HI : FUN_FACTS_EN), language: lang });
  }

  // 7. Weather
  if (/weather|mausam|barish|garmi/.test(text)) {
    return res.json({ response: isH ? "Weather data mere paas nahi hai 😅 Google Weather ya Dark Sky app try karo!" : "I don't have live weather data! 🌤️ Try Google Weather or a weather app.", language: lang });
  }

  // 8. Knowledge Base Q&A
  const kb = searchKnowledge(text);
  if (kb) return res.json({ response: isH ? kb.h : kb.e, language: lang });

  // 9. Math Engine
  const mathResult = parseAndEvaluateMath(message);
  if (mathResult !== null) {
    const cleanQuery = message.replace(/bhai|yaar|kya hai|kitna hoga|batao|calculate|solve|please|plz/gi, '').trim();
    const isMathFormatted = mathResult.startsWith('✅');
    const response = isMathFormatted ? mathResult : `✅ **Mathematical Solution**\n\nQuery: **${cleanQuery}**\n\n**${mathResult}**\n\n${isH ? 'Aur kuch calculate karoon? 😊' : 'Need anything else calculated? 😊'}`;
    return res.json({ response, language: lang, isMath: true });
  }

  // 10. Smart Fallback
  const fallbacksH = [
    "Hmm, yeh topic mujhe abhi nahi aata! 🤔 Par math, trigonometry, science, coding — kuch bhi pucho, main hoon na!\nKuch ideas:\n• sin(45) kya hai?\n• LCM of 12 and 18\n• Black hole explain karo\n• Quantum computing kya hai?",
    "Bhai, yeh thoda zyada mushkil hai mere liye abhi! 😅 Physics, Chemistry, CS, ya Math pe kuch bhi try karo!",
    "Interesting sawal hai yaar! 🧠 Abhi mujhe is topic ki training nahi mili. Par algebra, statistics, ya science try karo — main turant jawab dunga!"
  ];
  const fallbacksE = [
    "That's a tough one! 🤔 My training doesn't cover that yet, but try me with:\n• sin(45°) or cos(60°)\n• Solve x² - 5x + 6 = 0\n• What is machine learning?\n• Explain black holes\n• LCM of 24 and 36",
    "Beyond my knowledge base right now! 😅 But I excel at math, physics, algorithms, and computer science. Ask me anything in those areas!",
    "Interesting question! 🧠 I'm continuously learning. Meanwhile, test me with complex math, trigonometry, or science concepts!"
  ];

  return res.json({ response: pick(isH ? fallbacksH : fallbacksE), language: lang });
});

app.listen(PORT, () => {
  console.log(`🚀 Housie AI server running at http://localhost:${PORT}`);
});
