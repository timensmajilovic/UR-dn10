def unikati(num):
    uni = []
    for n in num:
        if n not in uni:
            uni.append(n)
    return uni

def avtor(tvit):
    i = tvit.index(":")
    return tvit[:i]

def vsi_avtorji(tviti):
    avtorji = []
    for tvit in tviti:
        i = tvit.index(":")
        ime = tvit[:i]
        if ime not in avtorji:
            avtorji.append(ime)
    return avtorji

def izloci_besedo(beseda):
    prvi_del = ""
    drugi_del = ""
    for l in beseda:
        if not l.isalnum():
            prvi_del += l
        else:
            break

    for l in beseda[::-1]:
        if not l.isalnum():
            drugi_del += l
        else:
            break

    beseda = beseda.strip(prvi_del)
    beseda = beseda.strip(drugi_del)
    return beseda

def se_zacne_z(tvit, c):
    words = []
    for word in tvit.split():
        if word[0] == c:
            words.append(izloci_besedo(word))
    return words

def zberi_se_zacne_z(tviti, c):
    words = []
    for tvit in tviti:
        for word in tvit.split():
            if word[0] == c:
                if izloci_besedo(word) not in words:
                    words.append(izloci_besedo(word))
    return words

def vse_afne(tviti):
    return zberi_se_zacne_z(tviti, "@")

def vsi_hashtagi(tviti):
    return zberi_se_zacne_z(tviti, "#")

def vse_osebe(tviti):
    avtorji = vsi_avtorji(tviti)
    omenjeni = vse_afne(tviti)

    vsi = avtorji + omenjeni

    return unikati(sorted(vsi))

def custva(tviti, hashtagi):
    avtorji = []
    for tvit in tviti:
        for hashtag in hashtagi:
            for h in se_zacne_z(tvit, "#"):
                if h == hashtag:
                    avtorji.append(avtor(tvit))
    return(unikati(sorted(avtorji)))

def se_poznata(tviti, oseba1, oseba2):
    avtorji = vsi_avtorji(tviti)
    for tvit in tviti:
        for omenjen in se_zacne_z(tvit, "@"):
            if (oseba1 == avtor(tvit) and oseba2 == omenjen) or (oseba2 == avtor(tvit) and oseba1 == omenjen):
                return True
    else:
        return False



import unittest


class TestTviti(unittest.TestCase):
    tviti = [
        "sandra: Spet ta dež. #dougcajt",
        "berta: @sandra Delaj domačo za #programiranje1",
        "sandra: @berta Ne maram #programiranje1 #krneki",
        "ana: kdo so te @berta, @cilka, @dani? #krneki",
        "cilka: jst sm pa #luft",
        "benjamin: pogrešam ano #zalosten",
        "ema: @benjamin @ana #split? po dvopičju, za začetek?",
    ]

    def test_01_unikat(self):
        self.assertEqual(unikati([1, 2, 1, 1, 3, 2]), [1, 2, 3])
        self.assertEqual(unikati([1, 3, 2, 1, 1, 3, 2]), [1, 3, 2])
        self.assertEqual(unikati([1, 5, 4, 3, 2]), [1, 5, 4, 3, 2])
        self.assertEqual(unikati([1, 1, 1, 1, 1]), [1])
        self.assertEqual(unikati([1]), [1])
        self.assertEqual(unikati([]), [])
        self.assertEqual(unikati(["Ana", "Berta", "Cilka", "Berta"]), ["Ana", "Berta", "Cilka"])

    def test_02_avtor(self):
        self.assertEqual(avtor("janez: pred dvopičjem avtor, potem besedilo"), "janez")
        self.assertEqual(avtor("ana: malo krajse ime"), "ana")
        self.assertEqual(avtor("benjamin: pomembne so tri stvari: prva, druga in tretja"), "benjamin")

    def test_03_vsi_avtorji(self):
        self.assertEqual(vsi_avtorji(self.tviti), ["sandra", "berta", "ana", "cilka", "benjamin", "ema"])
        self.assertEqual(vsi_avtorji(self.tviti[:3]), ["sandra", "berta"])

    def test_04_izloci_besedo(self):
        self.assertEqual(izloci_besedo("@ana"), "ana")
        self.assertEqual(izloci_besedo("@@ana!!!"), "ana")
        self.assertEqual(izloci_besedo("ana"), "ana")
        self.assertEqual(izloci_besedo("!#$%\"=%/%()/Ben-jamin'"), "Ben-jamin")

    def test_05_vse_na_crko(self):
        self.assertEqual(se_zacne_z("Benjamin $je $skocil! Visoko!", "$"), ["je", "skocil"])
        self.assertEqual(se_zacne_z("Benjamin $je $skocil! #Visoko!", "$"), ["je", "skocil"])
        self.assertEqual(se_zacne_z("ana: kdo so te @berta, @cilka, @dani? #krneki", "@"), ["berta", "cilka", "dani"])

    def test_06_zberi_na_crko(self):
        self.assertEqual(zberi_se_zacne_z(self.tviti, "@"), ['sandra', 'berta', 'cilka', 'dani', 'benjamin', 'ana'])
        self.assertEqual(zberi_se_zacne_z(self.tviti, "#"), ['dougcajt', 'programiranje1', 'krneki', 'luft', 'zalosten', 'split'])

    def test_07_vse_afne(self):
        self.assertEqual(vse_afne(self.tviti), ['sandra', 'berta', 'cilka', 'dani', 'benjamin', 'ana'])

    def test_08_vsi_hashtagi(self):
        self.assertEqual(vsi_hashtagi(self.tviti), ['dougcajt', 'programiranje1', 'krneki', 'luft', 'zalosten', 'split'])

    def test_09_vse_osebe(self):
        self.assertEqual(vse_osebe(self.tviti), ['ana', 'benjamin', 'berta', 'cilka', 'dani', 'ema', 'sandra'])

    def test_10_custva(self):
        self.assertEqual(custva(self.tviti, ["dougcajt", "krneki"]), ["ana", "sandra"])
        self.assertEqual(custva(self.tviti, ["luft"]), ["cilka"])
        self.assertEqual(custva(self.tviti, ["meh"]), [])

    def test_11_se_poznata(self):
        self.assertTrue(se_poznata(self.tviti, "ana", "berta"))
        self.assertTrue(se_poznata(self.tviti, "ema", "ana"))
        self.assertFalse(se_poznata(self.tviti, "sandra", "ana"))
        self.assertFalse(se_poznata(self.tviti, "cilka", "luft"))
        self.assertFalse(se_poznata(self.tviti, "cilka", "balon"))


if __name__ == "__main__":
    unittest.main()

