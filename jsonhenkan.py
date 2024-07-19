import json

class Tokuisaki:
    def __init__(self, a, b, c):
        self.tokuisaki_code = a
        self.folder_name = b
        self.kyaku = c

tokuisakies = [
	Tokuisaki('029007', "29007_粟井鋼商事㈱福岡営業所_____●", "粟井鋼商事㈱福岡営業所"),
	Tokuisaki('029267', "29267_協伸メタル㈱_____●", "協伸メタル㈱"),	
	Tokuisaki('029494', "29494_㈱鉄鋼社　長野営業所_____●", "㈱鉄鋼社　長野営業所"),
	Tokuisaki('029495', "29495_㈱鉄鋼社_____●", "㈱鉄鋼社"),
	Tokuisaki('029498', "29498_㈱鉄鋼社　北関東営業所_____●", "㈱鉄鋼社　北関東営業所"),
	Tokuisaki('029506', "29506_㈱鉄鋼社　東北営業所_____●", "㈱鉄鋼社　東北営業所"),
	Tokuisaki('029554', "29554_アイケーメタル㈱　狭山営業所___●", "アイケーメタル㈱　狭山営業所"),
    Tokuisaki('029612', "29612_南海モルディ㈱　名古屋事業所_____●", "南海モルディ㈱　名古屋事業所"),
	#Tokuisaki('029571', "29571_協同組合　島根県鐵工会　出雲営業所_____●", "協同組合　島根県鐵工会　出雲営業所"),
	Tokuisaki('029698', "29698_㈱林角本店　非鉄金属部___●", "㈱林角本店　非鉄金属部"),
	Tokuisaki('029806', "29806_富源商事㈱　上越支店____●", "富源商事㈱　上越支店"),
	#Tokuisaki('029879', "29879_萬世興業㈱　本社_____●", "萬世興業㈱　本社"),
	Tokuisaki('029886', "29886_萬世興業㈱　日光営業所_____●29879本社へ", "萬世興業㈱　日光営業所"),
	Tokuisaki('029896', "29896_保田特殊鋼㈱本社_____●", "保田特殊鋼㈱本社"),
    
]
# Chuyển các đối tượng Tokuisaki thành từ điển
tokuisaki_dicts = []
for tokuisaki in tokuisakies:
    tokuisaki_dict = {
        "tokuisaki_code": tokuisaki.tokuisaki_code,
        "folder_name": tokuisaki.folder_name,
        "kyaku": tokuisaki.kyaku
    }
    tokuisaki_dicts.append(tokuisaki_dict)

# Ghi vào tệp JSON
with open("tokuisakies.json", "w", encoding="utf-8") as json_file:
    json.dump(tokuisaki_dicts, json_file, indent=4, ensure_ascii=False)
