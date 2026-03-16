"""
Script Generator Module
Generates scripts for Islamic/Halal content videos
"""
import random
from pathlib import Path

# Pre-built Islamic Stories Scripts
ISLAMIC_STORIES = {
    "sahaba": [
        {
            "title": "Hazrat Umar R.A Ka Qabool-e-Islam",
            "script": """
Kya aap jante hain ke woh shakhs jo Islam ka sabse bada dushman tha,
woh kaise Islam ka sabse mazboot sutoon ban gaya?

Yeh kahani hai Hazrat Umar ibn al-Khattab Razi Allah Anhu ki.

[EMOTIONAL MUSIC]

Hazrat Umar... woh shakhs jis ke naam se Quraysh kaampte the.
Unki taqat ka yeh aalam tha ke log unke saamne se guzarne se darte the.

Aur unhe Islam se itni nafrat thi ke unhone faisla kar liya...
ke woh Rasool Allah Sallallahu Alaihi Wasallam ko shaheed kar denge.

[PAUSE]

Talwar haath mein liye woh nikal pade.
Raaste mein unhe Nuaim ibn Abdullah mile.

Nuaim ne pucha: "Umar, kahan ja rahe ho is haalat mein?"
Umar ne kaha: "Muhammad ko khatam karne!"

Nuaim ne kaha: "Pehle apne ghar ka haal dekh lo.
Tumhari behan Fatima aur bahnoi Said ne Islam qabool kar liya hai."

[DRAMATIC PAUSE]

Umar ke qadmon ki taal badal gayi.
Ab woh apne ghar ki taraf mud gaye... ghusse se bhari hui aankhon ke saath.

Ghar pahunche toh andar se Quran ki tilawat ki awaaz aa rahi thi.
Surah Taha ki tilawat ho rahi thi.

Umar ne darwaza khola aur apni behan ko maara.
Khoon beh nikla Fatima R.A ke chehre se.

Lekin Fatima R.A ne kaha:
"Umar! Tum jo chahte ho karo, lekin hum Islam nahi chhodenge!"

[PAUSE]

Yeh alfaaz... yeh himmat... Umar ke dil mein kuch hilaya.
Unhone kaha: "Mujhe woh sahifa dikhao jo tum padh rahe the."

Fatima R.A ne kaha: "Pehle paak ho jao."
Umar ne ghusl kiya aur Quran haath mein liya.

Surah Taha ki ayaat padhi:
"Ta Ha. Hum ne Quran tum par is liye nazil nahi kiya ke tum mushkil mein paro.
Balke yeh unke liye naseehat hai jo Allah se darte hain."

[EMOTIONAL PEAK]

Umar ki aankhon se aansu beh nikle.
Wahi Umar jo kabhi nahi roye.
Wahi Umar jo Islam ke dushman the.

Unhone pucha: "Mujhe Muhammad ke paas le chalo."

Aur jab woh Rasool Allah SAW ke paas pahunche,
toh Nabi SAW ne farmaya: "Umar, ab bhi waqt hai."

Umar ne kaha: "Ya Rasool Allah, main gawahi deta hun
ke Allah ke siwa koi mabood nahi aur aap Allah ke Rasool hain."

[CONCLUSION]

Usi din se Islam mazboot ho gaya.
Sahaba ne pehli baar Kaaba mein khul kar namaz padhi.

Hazrat Umar R.A ka qabool-e-Islam hume sikhata hai:
Allah jise chahe hidayat de sakta hai.
Koi shakhs hidayat se door nahi.

Agar aapko yeh kahani pasand aayi toh subscribe karein.
Aur comment mein batayein ke aapko Sahaba ki kaun si kahani sunni hai.

Allah Hafiz.
"""
        },
        {
            "title": "Hazrat Bilal R.A Ki Azmaish",
            "script": """
Ek ghulam jo apne maalik ke zulm sahte hue sirf ek lafz bolta raha...
"Ahad... Ahad... Ek hai... Ek hai..."

Yeh kahani hai Hazrat Bilal ibn Rabah Razi Allah Anhu ki.

[EMOTIONAL MUSIC]

Hazrat Bilal... Habsha ke rehne wale.
Rang unka kaala tha, lekin dil unka chamakte sooraj se zyada roshan tha.

Woh Makkah ke ek zaaalim sardar Umayyah ibn Khalaf ke ghulam the.
Jab Bilal R.A ne Islam qabool kiya, unke maalik ko pata chala.

[DRAMATIC PAUSE]

Umayyah ne hukm diya ke Bilal ko dopahar ki dhoop mein le jaaya jaye.
Jalti ret par unhe litaya gaya.
Seene par bhaari patthar rakhe gaye.

Aur Umayyah cheekh kar bola:
"Lat aur Uzza ka naam lo! Muhammad ke deen ko chod do!"

[PAUSE]

Lekin Bilal R.A ke lab par sirf ek lafz tha...
"Ahad... Ahad..."
"Allah ek hai... Allah ek hai..."

Din ba din yahi zulm hota raha.
Kabhie kanton par ghaseetay jaate.
Kabhi bhookhe rakhay jaate.

Lekin Bilal R.A ka imaan ek pehad ki tarah mazboot tha.

[EMOTIONAL MOMENT]

Ek din Hazrat Abu Bakr Siddique R.A wahan se guzre.
Unhone Bilal R.A ki haalat dekhi aur dil tarrap utha.

Abu Bakr R.A ne Umayyah se kaha: "Is ghulam ki kya qeemat hai?"
Umayyah ne badtameezi se kaha: "Yeh tumhare kisi kaam ka nahi."

Abu Bakr R.A ne farmaya: "Main ise khareed raha hun."
Aur unhone Bilal R.A ko azad kar diya.

[TURNING POINT]

Rasool Allah Sallallahu Alaihi Wasallam ne Bilal R.A ko gale lagaya.
Aur farmaya: "Bilal hamare mein se hain."

Aur jab Madina mein pehli masjid bani...
Rasool Allah SAW ne farmaya: "Bilal! Azaan do."

Woh kaale rang ka ghulam...
Islam ki taareekh ka pehla moazzin bana.

[CONCLUSION]

Bilal R.A ki kahani hume sikhati hai:
Imaan ki taqat duniya ki har taqat se barh kar hai.
Rang, nasl, ya haisiyat... Allah ke nazdeek koi mayne nahi rakhti.

Allah ke nazdeek sabse izzat wala woh hai jo sabse zyada muttaqi hai.

Agar aapke dil ko yeh kahani choo gayi, toh subscribe karein.
Comment mein likhein: "Ahad"

Allah Hafiz.
"""
        },
        {
            "title": "Hazrat Khadija R.A Ka Wafa",
            "script": """
Woh pehli insaan jinhone Rasool Allah SAW ki baat maani...
Woh khatoon jinke baghair shayad Islam ki ibtida na hoti.

Yeh kahani hai Ummul Momineen Hazrat Khadija Razi Allah Anha ki.

[SOFT EMOTIONAL MUSIC]

Hazrat Khadija... Makkah ki ameer tareen khatoon.
Unki tijarat door door tak mashoor thi.
Arab ke badhe badhe sardar unse shadi ka paigham bhejte.

Lekin unhone sab ko mana kar diya.

[PAUSE]

Phir ek din unhe ek naujawan ki khabar mili.
Muhammad ibn Abdullah... jise log "Al-Ameen" kehte the.
Sadiq bhi... Ameen bhi.

Khadija R.A ne unhe apni tijarat saunpi.
Aur jab Muhammad SAW wapas aaye...
Maisara ne bataya ke kaisa imandaar aur mehnat kash hai yeh insaan.

Khadija R.A ke dil mein kuch jaga.
Aur unhone khud shaadi ka paigham bheja.

[EMOTIONAL MOMENT]

25 saal ki umar mein Muhammad SAW...
40 saal ki Khadija R.A se byahe.

Aur yeh rishta? Yeh rishta misaal ban gaya.
Pyaar, izzat, aur wafa ki misaal.

[TURNING POINT]

Phir woh din aaya jab Jibreel Alaihissalam Ghaar-e-Hira mein aaye.
Muhammad SAW kaampte hue ghar aaye aur farmaya:
"Mujhe chadar orhao... mujhe chadar orhao!"

Khadija R.A ne chadar orhai aur pucha kya hua.
Nabi SAW ne saara waqiya sunaya.

Kya Khadija R.A ne shak kiya? Nahi!
Unhone kaha:

"Allah ki qasam! Allah aapko kabhi ruswa nahi karega.
Aap rishtedaron se sila rehmi karte hain.
Aap kamzoron ka bojh uthate hain.
Aap mehman nawazi karte hain.
Aap haq ki madad karte hain."

[EMOTIONAL PEAK]

Yeh alfaaz suniye...
Jab poori duniya ne muh pher liya...
Jab apno ne saath chhod diya...
Khadija R.A har pal saath rahi.

Unhone apni saari daulat Islam ke liye de di.
Teen saal Shib-e-Abi Talib ki mushkilat sahi.
Bhook sahi, takleefein sahiein... lekin saath nahi chhoda.

[CONCLUSION]

Aur jab Khadija R.A ka inteqal hua...
Us saal ko "Aam ul Huzn" - Gham ka saal kaha gaya.

Rasool Allah SAW saari umar unhe yaad karte rahe.
Hazrat Ayesha R.A farmati hain:
"Mujhe kisi se rashk nahi hua jitna Khadija se...
halankeh maine unhe dekha bhi nahi tha."

Khadija R.A hume sikhati hain:
Sachcha pyaar wafa mein hai.
Sachcha saath mushkil mein diya jata hai.

Subscribe karein aur Ummahatul Momineen ki aur kahaniyan sunein.

Allah Hafiz.
"""
        },
    ],
    "prophets": [
        {
            "title": "Hazrat Yusuf A.S Ki Kahani",
            "script": """
Ek nabi jinhein unke apne bhaiyon ne kuan mein phenk diya...
Phir ghulam bana kar bech diya...
Phir jail bheja gaya...
Aur phir? Phir woh Misr ke Aziz ban gaye!

Yeh kahani hai Hazrat Yusuf Alaihissalam ki.
Quran ne jise "Ahsan ul Qasas" - sabse khoobsurat kahani kaha.

[BEAUTIFUL MUSIC]

Hazrat Yaqoob Alaihissalam ke barah bete the.
Lekin Yusuf A.S sabse zyada pyare the.

Bachpan mein Yusuf A.S ne ek khwab dekha:
Gyarah sitare, sooraj aur chand... sab unhe sajda kar rahe hain.

Yaqoob A.S ne farmaya: "Beta, yeh khwab bhaiyon ko mat batana."
Lekin bhaiyon ke dil mein hasad ki aag lag chuki thi.

[DRAMATIC TURN]

Ek din bhaiyon ne kaha: "Abba, Yusuf ko hamare saath jungle bhejein."
Yaqoob A.S ka dil gawahi de raha tha...
Lekin maan gaye.

Aur bhaiyon ne Yusuf A.S ko ek andhay kuan mein phenk diya.
Ghar aa kar jhoothi kahani sunai:
"Abba, Yusuf ko bheriya kha gaya."
Aur khoon lagi qamees dikhai.

[EMOTIONAL MOMENT]

Yaqoob A.S ne kaha: "Sabar... Sabar jameel."
Aur itna roye ke aankhein safed ho gayin.

Udhar kuan se ek qafla ne Yusuf A.S ko nikaala.
Aur Misr mein ghulam ki tarah bech diya.

Aziz-e-Misr ne khareed liya.
Yusuf A.S bade hue... aur itne khoobsurat ke Quran kehta hai:
"Unhe aadhi khoobsurti di gayi thi."

[TEST OF CHARACTER]

Aziz ki biwi Zulaikha ne Yusuf A.S ko bura raasta dikhana chaha.
Lekin Yusuf A.S ne kaha:
"Ma'az Allah! Yeh main kabhi nahi karunga."

Aur jail jaana qabool kiya, lekin gunah nahi kiya.

[TURNING POINT]

Jail mein Yusuf A.S ne khwabon ki tabeer batayi.
Ek din Misr ke badshah ne khwab dekha jo koi nahi samjha.
Yusuf A.S ko bulaya gaya.

Unhone tabeer batayi aur hal bhi.
Badshah ne unhe Misr ka wazir bana diya!

[EMOTIONAL REUNION]

Saalon baad qehet pada.
Wohi bhai jinhone kuan mein phenka tha...
Woh anaaj lene Misr aaye.

Yusuf A.S ne pehchaan liya, lekin unhone nahi pehchana.

Aur jab sach saamne aaya...
Yusuf A.S ne kya kaha?

"Aaj tumhare upar koi ilzaam nahi.
Allah tumhe maaf kare. Woh sabse zyada rehem karne wala hai."

[DREAM FULFILLED]

Yaqoob A.S Misr aaye.
Aur jab Yusuf A.S se mile...
Maan, baap, aur gyarah bhai... sab ne sajda kiya.

Yusuf A.S ne aasman ki taraf dekha aur kaha:
"Yeh hai mera wo khwab... Allah ne use sach kar diya."

[CONCLUSION]

Yusuf A.S ki kahani hume sikhati hai:
Mushkilein imtihaan hain.
Sabar ka phal hamesha meetha hota hai.
Allah ki planning se behtar koi planning nahi.

Subscribe karein aur Prophets ki mazeed kahaniyan sunein.

Allah Hafiz.
"""
        },
        {
            "title": "Hazrat Ibrahim A.S Aur Aag Ka Waqiya",
            "script": """
Jab ek nabi ko zinda aag mein phenk diya gaya...
Aur aag ne unhe chooa tak nahi!

Yeh kahani hai Hazrat Ibrahim Alaihissalam ki.
Jinhe "Khalil Allah" - Allah ka dost kaha jata hai.

[POWERFUL MUSIC]

Hazrat Ibrahim A.S ki qaum but parast thi.
Unke apne walid Azar but banate aur bechte the.

Bachpan se Ibrahim A.S sochte: "Yeh patthar bhala kisi ki madad kya karenge?"

[SEARCHING FOR TRUTH]

Raat ko aasman ki taraf dekha... sitara chamka.
Kaha: "Shayad yahi mera Rab hai."
Lekin sitara doob gaya.

Chand nikla... kaha: "Yeh bada hai, yahi Rab hoga."
Lekin chand bhi doob gaya.

Sooraj nikla... roshni se zameen jagmaga uthi.
Kaha: "Yeh sabse bada hai!"
Lekin sooraj bhi doob gaya.

Tab Ibrahim A.S ne kaha:
"Main in sab se bezaar hun.
Mera Rab woh hai jisne yeh sab banaya!"

[CONFRONTATION]

Ek din Ibrahim A.S ne faisla kiya.
Jab sab log jashn par gaye...
Ibrahim A.S but khane mein gaye.
Aur tamam buton ko tod diya!

Sirf ek bada but rakha... aur kulhada uske kandhe par rakh diya.

[DRAMATIC SCENE]

Log wapas aaye aur chilaye: "Yeh kisne kiya?!"
Kisi ne kaha: "Ek naujawan hai Ibrahim... woh bura kehta hai buton ko."

Ibrahim A.S ko bulaya gaya.
Pucha: "Kya tumne yeh kiya hamare khuadaon ke saath?"

Ibrahim A.S ne kaha: "Nahi, yeh bade but ne kiya. Issi se pucho!"

Log bole: "Tujhe pata hai yeh bol nahi sakta!"

Ibrahim A.S ne kaha:
"Phir tum aise ki ibadat karte ho jo bol nahi sakta,
sun nahi sakta, tumhe faida ya nuqsan nahi de sakta?"

[THE FIRE]

Qaum ghusse mein aa gayi.
Faisla hua: "Ibrahim ko aag mein jala do!"

Itni badi aag lagayi gayi ke paas koi nahi ja sakta tha.
Manjaneeq se Ibrahim A.S ko aag mein phenka gaya!

[MIRACULOUS MOMENT]

Jab Ibrahim A.S hawa mein the...
Jibreel A.S aaye aur pucha: "Koi madad chahiye?"

Ibrahim A.S ne kaha: "Tum se nahi. Allah kaafi hai."

Aur Allah ne aag ko hukm diya:
"Aay aag! Thandi ho ja aur salamati ban ja Ibrahim ke liye!"

Ibrahim A.S aag ke beech mein baithe rahe.
Aur aag unke liye baagh ban gayi.
Woh bila zeham baahar aa gaye!

[CONCLUSION]

Nimrod aur uski qaum dekh kar hairan reh gayi.
Lekin phir bhi imaan nahi laaye.

Ibrahim A.S ki zindagi mein aur bhi imtihaan aaye:
Beta qurbaan karne ka hukm...
Bibi aur bachay ko biyabaan mein chhodna...

Lekin har imtihaan mein woh khare utre.
Is liye unhe "Khalil Allah" kaha gaya.

Unki kahani hume sikhati hai:
Jab Allah saath ho toh aag bhi gul zaar ban jati hai.
Jab tawakkal ho toh koi mushkil badi nahi.

Subscribe karein. Comment mein likhein: "Khalil Allah"

Allah Hafiz.
"""
        },
    ],
    "quran_lessons": [
        {
            "title": "Surah Rahman Ka Paigham",
            "script": """
"Fa bi ayyi aalaa'i Rabbikuma tukazzibaan?"
"Tum apne Rab ki kaun kaun si naimaton ko jhutlaoge?"

Yeh ayat Surah Rahman mein 31 baar aayi hai.
Aaj hum samjhenge ke Allah hum se kya keh raha hai.

[BEAUTIFUL RECITATION CLIP]

Surah Rahman ko "Aroos ul Quran" kaha jata hai.
Quran ki dulhan.
Kyunke yeh sabse khoobsurat surahon mein se hai.

[STRUCTURE]

Allah ne is surah mein apni naimaton ka zikr kiya:

Pehle farmaya: "Ar-Rahman."
Allah ka naam... jo Rehmaan hai.
Jo beshak rehmat karta hai.

Phir farmaya: "Allam al-Quran."
Usne Quran sikhaya.

"Khalaq al-insaan."
Usne insaan ko paida kiya.

"Allamahul bayaan."
Usne use bolna sikhaya.

[REFLECTION]

Zara sochiye...
Aap bol sakte hain, yeh Allah ki nemat hai.
Aap sun sakte hain, yeh Allah ki nemat hai.
Aap sochte hain, yeh Allah ki nemat hai.

Phir aap in mein se kaun si nemat ko jhutlaoge?

[NATURE'S SIGNS]

Surah mein Allah ne farmaya:
Sooraj aur chand hisaab se chalte hain.
Sitare aur darakht sajda karte hain.
Aasman ko buland kiya aur mizaan rakhi.

Yeh sab Allah ki nishaniyan hain.
Kya hum ghour karte hain?

[TWO SEAS]

Allah ne farmaya:
"Usne do samundaron ko mila diya.
Woh aapas mein milte hain.
Lekin un ke darmiyan ek aad hai jis se woh tajawuz nahi karte."

Science ne yeh haal hi mein discover kiya.
Atlantic aur Mediterranean... milte hain lekin pani mix nahi hota.

Yeh Quran mein 1400 saal pehle tha.
Fa bi ayyi aalaa'i Rabbikuma tukazzibaan?

[PARADISE DESCRIPTION]

Surah ke aakhir mein jannat ka zikr hai:
Do baagh... jahan neechay se nehrain behti hain.
Har phal ke do qism.
Reshami bistar... phal qareeb.

Yeh un ke liye hai jo apne Rab ke saamne khade hone se dare.

[CONCLUSION]

Surah Rahman hume yaad dilati hai:
Har saans Allah ki nemat hai.
Har lamha shukr ka mauka hai.

Aaj se har nemat par Alhamdulillah kahein.
Har mushkil mein sabar karein.

Kyunke jitni naimatein hain... gin nahi sakte.

Subscribe karein Quran ki mazeed hikmat ke liye.

Allah Hafiz.
"""
        },
    ],
    "motivational": [
        {
            "title": "Mushkilon Ka Raaz",
            "script": """
Kya aap jaante hain?
Allah sabse zyada mushkilein unhe deta hai jinse sabse zyada pyar karta hai.

Aaj hum baat karenge mushkilon ke raaz ki.

[THOUGHTFUL MUSIC]

Sahih hadith mein hai:
"Jab Allah kisi bande se pyar karta hai, use mushkilon mein daalta hai."

Yeh sunne mein ajeeb lagta hai.
Lekin samajhne ki zaroorat hai.

[GOLD ANALOGY]

Sona kaise banta hai?
Kachay lohe ko aag mein daalte hain.
Baar baar garam karte hain.
Baar baar peetate hain.

Phir woh chamakta hua sona banta hai.

Aap bhi wohi sona hain.
Mushkilein woh aag hai jo aapko nikalti hai.

[PROPHET'S EXAMPLE]

Rasool Allah SAW ki zindagi dekhiye:
Bachpan mein yateem ho gaye.
Chacha ne saath chhoda.
Taif mein patthar maare gaye.
Apno ne muh pher liya.

Kya woh kamzor the? Nahi!
Woh toh sabse pyaare the Allah ke.

[SAHABA'S STRUGGLES]

Hazrat Bilal R.A ko jalti ret par tadpaya gaya.
Hazrat Sumayya R.A ko shaheed kiya gaya.
Hazrat Yasir R.A ko qatl kiya gaya.

Kya woh haar gaye? Nahi!
Unhi ke sabr se Islam phela.

[PERSPECTIVE SHIFT]

Allah Quran mein farmata hai:
"Yaqeenan har mushkil ke saath asaani hai.
Beshak har mushkil ke saath asaani hai."

Do baar farmaya!
Ek mushkil ke saath DO asaaniyan!

[PRACTICAL LESSON]

Jab mushkil aaye toh sochiye:
- Yeh mera imtihaan hai
- Yeh mujhe mazboot bana rahi hai
- Is mein bhi koi khair hai

Aur yeh dua karein:
"Ya Allah, mujhe sabr de.
Mujhe is mushkil mein jo khair hai woh dikha."

[CLOSING]

Yaad rakhein:
Dariya ke tez bahao mein hi machli mazboot hoti hai.
Tez hawaaon mein hi darakht ki jadein gehri hoti hain.

Aap haar nahi sakte jab Allah saath hai.

Mushkilein aati hain toh sirf is liye...
Ke Allah aapko agli level ke liye tayyar kar raha hai.

Subscribe karein aur apni mushkil comment mein share karein.
Hum aapke liye dua karenge.

Allah Hafiz.
"""
        },
    ],
    "hadith": [
        {
            "title": "Hadith: Muskurana Sadqa Hai",
            "script": """
Rasool Allah Sallallahu Alaihi Wasallam ne farmaya:
"Apne bhai ke saamne muskurana sadqa hai."

Aaj hum is khoobsurat hadith ko samjhenge.

[GENTLE MUSIC]

Yeh hadith Sunan al-Tirmizi mein hai.
Kitni simple baat hai... muskurana sadqa hai.

Lekin is mein kitni gehrai hai?

[UNDERSTANDING SADQA]

Sadqa ka matlab hai woh cheez jo Allah ki raza ke liye di jaye.
Hum sochte hain sadqa sirf paisa hai.

Lekin Nabi SAW ne bataya:
Muskurana bhi sadqa hai.
Achhi baat kehna bhi sadqa hai.
Raasta batana bhi sadqa hai.

[POWER OF SMILE]

Aap jab muskurate hain toh kya hota hai?

Aapke andar endorphins release hoti hain.
Saamne wale ko achha lagta hai.
Mahol khushgawar ho jata hai.

Science ne yeh recently bataya.
Nabi SAW ne 1400 saal pehle bata diya tha.

[SUNNAH OF SMILE]

Sahaba farmate hain:
"Rasool Allah SAW ka chehra hamesha muskurata rehta tha."

Itni mushkilein thin... phir bhi muskurate the.
Ghar ki pareshaniyan... muskurate the.
Munafiqon ki saazieshein... muskurate the.

Yeh thi sunnat.

[PRACTICAL APPLICATION]

Aaj se yeh karein:

1. Subah aaina mein khud ko dekh kar muskurayein
2. Ghar walon se muskura kar milein
3. Kaam par sabko smile dein
4. Zindagi ki choti choti khushiyon par muskurayein

[MULTIPLIED REWARD]

Jab aap muskurate hain:
- Aapko sawab milta hai
- Saamne wala khush hota hai
- Woh bhi muskurata hai
- Chain reaction!

Ek muskurahat se kitne logon tak khushi pahunchi!

[CLOSING]

Duniya mein gham bahut hai.
Pareshaniyan bahut hain.
Mushkilein bahut hain.

Lekin muskurana mat chhodiye.
Yeh sunnat bhi hai, sawab bhi hai, aur therapy bhi hai.

Agle video mein ek aur pyaari hadith samjhenge.
Subscribe karein.

Aur comment mein ek muskurati emoji bhejein
taake pata chale kitne logon ne yeh video dekhi.

Allah Hafiz.
"""
        },
    ],
}


def get_categories():
    """Return available content categories"""
    return {
        "1": "Sahaba Stories",
        "2": "Prophet Stories",
        "3": "Quran Lessons",
        "4": "Motivational Islamic",
        "5": "Daily Hadith",
    }


def get_scripts_by_category(category_num: str):
    """Get available scripts for a category"""
    category_map = {
        "1": "sahaba",
        "2": "prophets",
        "3": "quran_lessons",
        "4": "motivational",
        "5": "hadith",
    }

    category_key = category_map.get(category_num)
    if category_key and category_key in ISLAMIC_STORIES:
        return ISLAMIC_STORIES[category_key]
    return []


def get_random_script(category_num: str = None):
    """Get a random script, optionally from a specific category"""
    if category_num:
        scripts = get_scripts_by_category(category_num)
        if scripts:
            return random.choice(scripts)

    # Get random from all
    all_scripts = []
    for category_scripts in ISLAMIC_STORIES.values():
        all_scripts.extend(category_scripts)

    return random.choice(all_scripts) if all_scripts else None


def generate_custom_prompt(topic: str, duration: int = 6) -> str:
    """Generate a prompt for custom topic (user can use with ChatGPT)"""
    return f"""
Tum ek expert Islamic storyteller ho YouTube ke liye.

Mujhe is topic pe {duration}-{duration+2} minute ka script likho: {topic}

Script format:
1. HOOK (pehle 10 seconds - shocking/emotional start)
2. Context/Background
3. Main story with details and emotions
4. Climax moment
5. Lesson/Moral
6. CTA (subscribe/comment reminder)

Style instructions:
- Roman Urdu mein likho
- Short sentences
- Emotional pauses indicate karo (...)
- Background music suggestions do [brackets mein]
- Har section ke beech [PAUSE] ya [EMOTIONAL MUSIC] likho

Topic: {topic}
"""


def save_script(title: str, script: str, output_dir: Path) -> Path:
    """Save script to file"""
    filename = title.lower().replace(" ", "_").replace(".", "") + ".txt"
    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"TITLE: {title}\n")
        f.write("=" * 50 + "\n\n")
        f.write(script.strip())

    return filepath
