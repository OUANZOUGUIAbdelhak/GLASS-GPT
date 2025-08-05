from langflow.custom import Component
from langflow.io import Output, MessageTextInput
from langflow.schema import Data
import requests
import ast  # Pour convertir les chaînes de listes en vraies listes Python
import re

class EnvoyerDonneesVerreTableComponent(Component):
    display_name = "Envoyer Données Verre à la Table"
    description = "Envoyer la composition détaillée du verre et les informations de référence du document au serveur Flask."
    icon = "table"

    inputs = [
        MessageTextInput(
            name="texte_extrait",
            display_name="Texte Extrait",
            info=(
                "Texte extrait contenant la référence du document et les informations sur la composition du verre."
            ),
            value=(
                "1. Type du document : Article scientifique\n"
                "2. Titre du document : Can a simple topological-constraints-based model predict the initial dissolution rate of borosilicate and aluminosilicate glasses?\n"
                "3. Référence : npj Materials Degradation (2020) 4:6 ; https://doi.org/10.1038/s41529-020-0111-4\n"
                "4. Premier Auteur : Stéphane Gin\n"
                "5. Nombre de types de verres : 16\n"
                "6. Verre_type1 : NBS12/28\n"
                "7. Nombre de tests(Verre_type1) : 2\n"
                "8. Li(Verre_type1) : [0, 0]\n"
                "9. B(Verre_type1) : [39.83, 39.83]\n"
                "10. O(Verre_type1) : [0, 0]\n"
                "11. Na(Verre_type1) : [16.68, 16.68]\n"
                "12. Mg(Verre_type1) : [0, 0]\n"
                "13. Al(Verre_type1) : [0, 0]\n"
                "14. Si(Verre_type1) : [43.49, 43.49]\n"
                "15. P(Verre_type1) : [0, 0]\n"
                "16. K(Verre_type1) : [0, 0]\n"
                "17. Ca(Verre_type1) : [0, 0]\n"
                "18. Ti(Verre_type1) : [0, 0]\n"
                "19. V(Verre_type1) : [0, 0]\n"
                "20. Cr(Verre_type1) : [0, 0]\n"
                "21. Mn(Verre_type1) : [0, 0]\n"
                "22. Fe(Verre_type1) : [0, 0]\n"
                "23. Co(Verre_type1) : [0, 0]\n"
                "24. Ni(Verre_type1) : [0, 0]\n"
                "25. Cu(Verre_type1) : [0, 0]\n"
                "26. Zn(Verre_type1) : [0, 0]\n"
                "27. Ga(Verre_type1) : [0, 0]\n"
                "28. Ge(Verre_type1) : [0, 0]\n"
                "29. As(Verre_type1) : [0, 0]\n"
                "30. Se(Verre_type1) : [0, 0]\n"
                "31. Rb(Verre_type1) : [0, 0]\n"
                "32. Sr(Verre_type1) : [0, 0]\n"
                "33. Y(Verre_type1) : [0, 0]\n"
                "34. Zr(Verre_type1) : [0, 0]\n"
                "35. Nb(Verre_type1) : [0, 0]\n"
                "36. Mo(Verre_type1) : [0, 0]\n"
                "37. Tc(Verre_type1) : [0, 0]\n"
                "38. Ru(Verre_type1) : [0, 0]\n"
                "39. Rh(Verre_type1) : [0, 0]\n"
                "40. Pd(Verre_type1) : [0, 0]\n"
                "41. Ag(Verre_type1) : [0, 0]\n"
                "42. Cd(Verre_type1) : [0, 0]\n"
                "43. In(Verre_type1) : [0, 0]\n"
                "44. Sn(Verre_type1) : [0, 0]\n"
                "45. Sb(Verre_type1) : [0, 0]\n"
                "46. Te(Verre_type1) : [0, 0]\n"
                "47. I(Verre_type1) : [0, 0]\n"
                "48. Cs(Verre_type1) : [0, 0]\n"
                "49. Ba(Verre_type1) : [0, 0]\n"
                "50. La(Verre_type1) : [0, 0]\n"
                "51. Hf(Verre_type1) : [0, 0]\n"
                "52. Ta(Verre_type1) : [0, 0]\n"
                "53. W(Verre_type1) : [0, 0]\n"
                "54. Re(Verre_type1) : [0, 0]\n"
                "55. Os(Verre_type1) : [0, 0]\n"
                "56. Ir(Verre_type1) : [0, 0]\n"
                "57. Pt(Verre_type1) : [0, 0]\n"
                "58. Au(Verre_type1) : [0, 0]\n"
                "59. Hg(Verre_type1) : [0, 0]\n"
                "60. Tl(Verre_type1) : [0, 0]\n"
                "61. Pb(Verre_type1) : [0, 0]\n"
                "62. Bi(Verre_type1) : [0, 0]\n"
                "63. Po(Verre_type1) : [0, 0]\n"
                "64. At(Verre_type1) : [0, 0]\n"
                "65. Rn(Verre_type1) : [0, 0]\n"
                "66. Ce(Verre_type1) : [0, 0]\n"
                "67. Pr(Verre_type1) : [0, 0]\n"
                "68. Nd(Verre_type1) : [0, 0]\n"
                "69. S_autres_TR(Verre_type1) : [0, 0]\n"
                "70. Th(Verre_type1) : [0, 0]\n"
                "71. U(Verre_type1) : [0, 0]\n"
                "72. Pu(Verre_type1) : [0, 0]\n"
                "73. Np(Verre_type1) : [0, 0]\n"
                "74. Am(Verre_type1) : [0, 0]\n"
                "75. Cm(Verre_type1) : [0, 0]\n"
                "76. S_autres_An(Verre_type1) : [0, 0]\n"
                "77. Somme(Verre_type1) : [100.0, 100.0]\n"
                "78. Densité(Verre_type1) : [2.462, 2.462]\n"
                "79. Homogénéité(Verre_type1) : [Not available, Not available]\n"
                "80. % B(IV)(Verre_type1) : [43, 43]\n"
                "81. Irradié(Verre_type1) : [Not available, Not available]\n"
                "82. Caractéristiques si irradié(Verre_type1) : [Not available, Not available]\n"
                "83. Température(Verre_type1) : [90, 90]\n"
                "84. Statique/dynamique(Verre_type1) : [static, static]\n"
                "85. Plage granulométrique (si poudre)(Verre_type1) : [Not available, 40 –63]\n"
                "86. Surface spécifique géométrique (si poudre)(Verre_type1) : [Not available, 37.6]\n"
                "87. Surface spécifique BET (si poudre)(Verre_type1) : [Not available, Not available]\n"
                "88. Qualité de polissage (si monolithe)(Verre_type1) : [Not available, Not available]\n"
                "89. Masse du verre(Verre_type1) : [1.292, 0.080]\n"
                "90. Surface du verre (S)(Verre_type1) : [5.08, Not available]\n"
                "91. Volume de la solution (V)(Verre_type1) : [0.485, 0.999]\n"
                "92. Débit de la solution(Verre_type1) : [Not available, Not available]\n"
                "93. pH initial (T amb)(Verre_type1) : [Not available, Not available]\n"
                "94. pH initial (T essai)(Verre_type1) : [9, 9]\n"
                "95. Composition de la solution(Verre_type1) : [Not available, Not available]\n"
                "96. Durée de l'expérience(Verre_type1) : [2.4, 0.7]\n"
                "97. pH final (T amb)(Verre_type1) : [Not available, Not available]\n"
                "98. pH final (T essai)(Verre_type1) : [8.9, 9.0]\n"
                "99. Normalisation de la vitesse (Sgeo ou SBET)(Verre_type1) : [Not available, Not available]\n"
                "100. V₀(Si) ou r₀(Si)(Verre_type1) : [192, 202]\n"
                "101. r²(Si)(Verre_type1) : [1.000, 0.995]\n"
                "102. Ordonnée à l'origine (Si)(Verre_type1) : [0.4, 0.6]\n"
                "103. V₀(B) ou r₀(B)(Verre_type1) : [Not available, Not available]\n"
                "104. Ordonnée à l'origine (B)(Verre_type1) : [Not available, Not available]\n"
                "105. V₀(Na) ou r₀(Na)(Verre_type1) : [Not available, Not available]\n"
                "106. r²(Na)(Verre_type1) : [Not available, Not available]\n"
                "107. Ordonnée à l'origine (Na)(Verre_type1) : [Not available, Not available]\n"
                "108. V₀(ΔM) ou r₀(ΔM)(Verre_type1) : [223, Not available]\n"
                "109. Congruence(Verre_type1) : [1.1 ± 0.1, Not available]\n"
                "110. Verre_type2 : NBS36/21\n"
                "111. Nombre de tests(Verre_type2) : 1\n"
                "112. Li(Verre_type2) : [0]\n"
                "113. B(Verre_type2) : [26.37]\n"
                "114. O(Verre_type2) : [0]\n"
                "115. Na(Verre_type2) : [46.11]\n"
                "116. Mg(Verre_type2) : [0]\n"
                "117. Al(Verre_type2) : [0]\n"
                "118. Si(Verre_type2) : [27.52]\n"
                "119. P(Verre_type2) : [0]\n"
                "120. K(Verre_type2) : [0]\n"
                "121. Ca(Verre_type2) : [0]\n"
                "122. Ti(Verre_type2) : [0]\n"
                "123. V(Verre_type2) : [0]\n"
                "124. Cr(Verre_type2) : [0]\n"
                "125. Mn(Verre_type2) : [0]\n"
                "126. Fe(Verre_type2) : [0]\n"
                "127. Co(Verre_type2) : [0]\n"
                "128. Ni(Verre_type2) : [0]\n"
                "129. Cu(Verre_type2) : [0]\n"
                "130. Zn(Verre_type2) : [0]\n"
                "131. Ga(Verre_type2) : [0]\n"
                "132. Ge(Verre_type2) : [0]\n"
                "133. As(Verre_type2) : [0]\n"
                "134. Se(Verre_type2) : [0]\n"
                "135. Rb(Verre_type2) : [0]\n"
                "136. Sr(Verre_type2) : [0]\n"
                "137. Y(Verre_type2) : [0]\n"
                "138. Zr(Verre_type2) : [0]\n"
                "139. Nb(Verre_type2) : [0]\n"
                "140. Mo(Verre_type2) : [0]\n"
                "141. Tc(Verre_type2) : [0]\n"
                "142. Ru(Verre_type2) : [0]\n"
                "143. Rh(Verre_type2) : [0]\n"
                "144. Pd(Verre_type2) : [0]\n"
                "145. Ag(Verre_type2) : [0]\n"
                "146. Cd(Verre_type2) : [0]\n"
                "147. In(Verre_type2) : [0]\n"
                "148. Sn(Verre_type2) : [0]\n"
                "149. Sb(Verre_type2) : [0]\n"
                "150. Te(Verre_type2) : [0]\n"
                "151. I(Verre_type2) : [0]\n"
                "152. Cs(Verre_type2) : [0]\n"
                "153. Ba(Verre_type2) : [0]\n"
                "154. La(Verre_type2) : [0]\n"
                "155. Hf(Verre_type2) : [0]\n"
                "156. Ta(Verre_type2) : [0]\n"
                "157. W(Verre_type2) : [0]\n"
                "158. Re(Verre_type2) : [0]\n"
                "159. Os(Verre_type2) : [0]\n"
                "160. Ir(Verre_type2) : [0]\n"
                "161. Pt(Verre_type2) : [0]\n"
                "162. Au(Verre_type2) : [0]\n"
                "163. Hg(Verre_type2) : [0]\n"
                "164. Tl(Verre_type2) : [0]\n"
                "165. Pb(Verre_type2) : [0]\n"
                "166. Bi(Verre_type2) : [0]\n"
                "167. Po(Verre_type2) : [0]\n"
                "168. At(Verre_type2) : [0]\n"
                "169. Rn(Verre_type2) : [0]\n"
                "170. Ce(Verre_type2) : [0]\n"
                "171. Pr(Verre_type2) : [0]\n"
                "172. Nd(Verre_type2) : [0]\n"
                "173. S_autres_TR(Verre_type2) : [0]\n"
                "174. Th(Verre_type2) : [0]\n"
                "175. U(Verre_type2) : [0]\n"
                "176. Pu(Verre_type2) : [0]\n"
                "177. Np(Verre_type2) : [0]\n"
                "178. Am(Verre_type2) : [0]\n"
                "179. Cm(Verre_type2) : [0]\n"
                "180. S_autres_An(Verre_type2) : [0]\n"
                "181. Somme(Verre_type2) : [100.0]\n"
                "182. Densité(Verre_type2) : [2.537]\n"
                "183. Homogénéité(Verre_type2) : [Not available]\n"
                "184. % B(IV)(Verre_type2) : [63]\n"
                "185. Irradié(Verre_type2) : [Not available]\n"
                "186. Caractéristiques si irradié(Verre_type2) : [Not available]\n"
                "187. Température(Verre_type2) : [90]\n"
                "188. Statique/dynamique(Verre_type2) : [static]\n"
                "189. Plage granulométrique (si poudre)(Verre_type2) : [Not available]\n"
                "190. Surface spécifique géométrique (si poudre)(Verre_type2) : [Not available]\n"
                "191. Surface spécifique BET (si poudre)(Verre_type2) : [Not available]\n"
                "192. Qualité de polissage (si monolithe)(Verre_type2) : [Not available]\n"
                "193. Masse du verre(Verre_type2) : [1.986]\n"
                "194. Surface du verre (S)(Verre_type2) : [6.18]\n"
                "195. Volume de la solution (V)(Verre_type2) : [1.017]\n"
                "196. Débit de la solution(Verre_type2) : [Not available]\n"
                "197. pH initial (T amb)(Verre_type2) : [Not available]\n"
                "198. pH initial (T essai)(Verre_type2) : [9]\n"
                "199. Composition de la solution(Verre_type2) : [Not available]\n"
                "200. Durée de l'expérience(Verre_type2) : [0.4]\n"
                "201. pH final (T amb)(Verre_type2) : [Not available]\n"
                "202. pH final (T essai)(Verre_type2) : [9.5]\n"
                "203. Normalisation de la vitesse (Sgeo ou SBET)(Verre_type2) : [Not available]\n"
                "204. V₀(Si) ou r₀(Si)(Verre_type2) : [47370]\n"
                "205. r²(Si)(Verre_type2) : [0.986]\n"
                "206. Ordonnée à l'origine (Si)(Verre_type2) : [-31.2]\n"
                "207. V₀(B) ou r₀(B)(Verre_type2) : [Not available]\n"
                "208. Ordonnée à l'origine (B)(Verre_type2) : [Not available]\n"
                "209. V₀(Na) ou r₀(Na)(Verre_type2) : [Not available]\n"
                "210. r²(Na)(Verre_type2) : [Not available]\n"
                "211. Ordonnée à l'origine (Na)(Verre_type2) : [Not available]\n"
                "212. V₀(ΔM) ou r₀(ΔM)(Verre_type2) : [Not available]\n"
                "213. Congruence(Verre_type2) : [1.1 ± 0.1]\n"
            ),
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Réponse", name="sortie", method="construire_sortie"),
    ]

    def construire_sortie(self) -> Data:
        texte_extrait = self.texte_extrait
        print(f"Texte Extrait: {texte_extrait}")
    
        try:
            # Nettoyer et analyser le texte
            lignes = [ligne.strip() for ligne in texte_extrait.split("\n") if ligne.strip()]
    
            # Extraction des données générales
            type_doc = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("1. Type du document :")), None)
            titre = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("2. Titre du document :")), None)
            reference = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("3. Référence :")), None)
            premier_auteur = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("4. Premier Auteur :")), None)
            nombre_types_verres_str = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith("5. Nombre de types de verres :")), None)
            print(f"Nombre de types de verres (str): {nombre_types_verres_str}")
    
            # Convertir en entier avec vérification
            if nombre_types_verres_str is not None:
                nombre_types_verres = int(nombre_types_verres_str)
            else:
                raise ValueError("Le nombre de types de verres n'a pas été trouvé dans le texte.")
    
            # Liste pour stocker tous les verres (une entrée par test)
            donnees_verres = []
    
            # Liste complète des paramètres à extraire, correspondant exactement au Flask
            parametres = [
                "Li", "B", "O", "Na", "Mg", "Al", "Si", "P", "K", "Ca", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Cs", "Ba", "La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Ce", "Pr", "Nd", "S_autres_TR", "Th", "U", "Pu", "Np", "Am", "Cm", "S_autres_An", "Somme", "Densité", "Homogénéité", "% B(IV)", "Irradié", "Caractéristiques si irradié", "Température", "Statique/dynamique", "Plage granulométrique (si poudre)", "Surface spécifique géométrique (si poudre)", "Surface spécifique BET (si poudre)", "Qualité de polissage (si monolithe)", "Masse du verre", "Surface du_verre (S)", "Volume de la solution (V)", "Débit de la solution", "pH initial (T amb)", "pH initial (T essai)", "Composition de la solution", "Durée de l'expérience", "pH final (T amb)", "pH final (T essai)", "Normalisation de la vitesse (Sgeo ou SBET)", "V₀(Si) ou r₀(Si)", "r²(Si)", "Ordonnée à l'origine (Si)", "V₀(B) ou r₀(B)", "Ordonnée à l'origine (B)", "V₀(Na) ou r₀(Na)", "r²(Na)", "Ordonnée à l'origine (Na)", "V₀(ΔM) ou r₀(ΔM)", "Congruence"
            ]
    
            # Dictionnaire de correspondance entre paramètres d'entrée et clés Flask
            parametres_flask = {
                "Li": "Li",
                "B": "B",
                "O": "O",
                "Na": "Na",
                "Mg": "Mg",
                "Al": "Al",
                "Si": "Si",
                "P": "P",
                "K": "K",
                "Ca": "Ca",
                "Ti": "Ti",
                "V": "V",
                "Cr": "Cr",
                "Mn": "Mn",
                "Fe": "Fe",
                "Co": "Co",
                "Ni": "Ni",
                "Cu": "Cu",
                "Zn": "Zn",
                "Ga": "Ga",
                "Ge": "Ge",
                "As": "As",
                "Se": "Se",
                "Rb": "Rb",
                "Sr": "Sr",
                "Y": "Y",
                "Zr": "Zr",
                "Nb": "Nb",
                "Mo": "Mo",
                "Tc": "Tc",
                "Ru": "Ru",
                "Rh": "Rh",
                "Pd": "Pd",
                "Ag": "Ag",
                "Cd": "Cd",
                "In": "In",
                "Sn": "Sn",
                "Sb": "Sb",
                "Te": "Te",
                "I": "I",
                "Cs": "Cs",
                "Ba": "Ba",
                "La": "La",
                "Hf": "Hf",
                "Ta": "Ta",
                "W": "W",
                "Re": "Re",
                "Os": "Os",
                "Ir": "Ir",
                "Pt": "Pt",
                "Au": "Au",
                "Hg": "Hg",
                "Tl": "Tl",
                "Pb": "Pb",
                "Bi": "Bi",
                "Po": "Po",
                "At": "At",
                "Rn": "Rn",
                "Ce": "Ce",
                "Pr": "Pr",
                "Nd": "Nd",
                "S_autres_TR": "S_autres_TR",
                "Th": "Th",
                "U": "U",
                "Pu": "Pu",
                "Np": "Np",
                "Am": "Am",
                "Cm": "Cm",
                "S_autres_An": "S_autres_An",
                "Somme": "Somme",
                "Densité": "Densité",
                "Homogénéité": "Homogénéité",
                "% B(IV)": "B_IV",
                "Irradié": "Irradié",
                "Caractéristiques si irradié": "Caractéristiques_si_irradié",
                "Température": "Température",
                "Statique/dynamique": "Statique_dynamique",
                "Plage granulométrique (si poudre)": "Plage_granulométrique_si_poudre",
                "Surface spécifique géométrique (si poudre)": "Surface_spécifique_géométrique_si_poudre",
                "Surface spécifique BET (si poudre)": "Surface_spécifique_BET_si_poudre",
                "Qualité de polissage (si monolithe)": "Qualité_de_polissage_si_monolithe",
                "Masse du verre": "Masse_du_verre",
                "Surface du_verre (S)": "Surface_du_verre_S",
                "Volume de la solution (V)": "Volume_de_la_solution_V",
                "Débit de la solution": "Débit_de_la_solution",
                "pH initial (T amb)": "pH_initial_T_amb",
                "pH initial (T essai)": "pH_initial_T_essai",
                "Composition de la solution": "Composition_de_la_solution",
                "Durée de l'expérience": "Durée_de_l_expérience",
                "pH final (T amb)": "pH_final_T_amb",
                "pH final (T essai)": "pH_final_T_essai",
                "Normalisation de la vitesse (Sgeo ou SBET)": "Normalisation_de_la_vitesse_Sgeo_ou_SBET",
                "V₀(Si) ou r₀(Si)": "V₀(Si) ou r₀(Si)",
                "r²(Si)": "r²(Si)",
                "Ordonnée à l'origine (Si)": "Ordonnée_à_l'origine_Si",
                "V₀(B) ou r₀(B)": "V₀(B) ou r₀(B)",
                "Ordonnée à l'origine (B)": "Ordonnée_à_l'origine_B",
                "V₀(Na) ou r₀(Na)": "V₀(Na) ou r₀(Na)",
                "r²(Na)": "r²(Na)",
                "Ordonnée à l'origine (Na)": "Ordonnée_à_l'origine_Na",
                "V₀(ΔM) ou r₀(ΔM)": "V₀(ΔM) ou r₀(ΔM)",
                "Congruence": "Congruence"
            }
    
            for i in range(nombre_types_verres):
                verre_type_key = f"Verre_type{i+1}"
                type_verre = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{6 + i * 104}. {verre_type_key} :")), None)
                print(f"Type de verre {verre_type_key}: {type_verre}")
    
                # Extraction du nombre de tests avec gestion de None
                nombre_tests_str = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{7 + i * 104}. Nombre de tests({verre_type_key}) :")), None)
                print(f"Nombre de tests (str) pour {verre_type_key}: {nombre_tests_str}")
                if nombre_tests_str is not None:
                    nombre_tests = int(nombre_tests_str)
                else:
                    nombre_tests = 1
    
                # Extraction des listes pour chaque paramètre avec gestion des erreurs
                params = {}
                for idx, param in enumerate(parametres):
                    # Normaliser le nom du paramètre pour gérer les variantes
                    param_key = param.replace("_", " ").replace("S autres TR", "S(autres TR)").replace("S autres An", "S(autres An)")
                    param_value_str = next((ligne.split(":", 1)[1].strip() for ligne in lignes if ligne.startswith(f"{8 + i * 104 + idx}. {param_key}({verre_type_key}) :")), None)
                    print(f"Valeur extraite pour {param}({verre_type_key}): {param_value_str}")
                    if param_value_str:
                        # Nettoyer la chaîne
                        param_value_str = re.sub(r'–', '-', param_value_str)  # Remplacer les tirets par des signes moins
                        param_value_str = re.sub(r'\s+', ' ', param_value_str)  # Réduire les espaces multiples
                        try:
                            # Essayer de parser avec ast.literal_eval
                            params[param] = ast.literal_eval(param_value_str)
                        except (ValueError, SyntaxError):
                            # Si le parsing échoue, traiter comme une liste de chaînes
                            items = [item.strip() for item in param_value_str.strip("[]").split(",")]
                            cleaned_items = []
                            for item in items:
                                try:
                                    cleaned_items.append(float(item))  # Si c’est un nombre, le convertir
                                except ValueError:
                                    cleaned_items.append(item)  # Sinon, le laisser comme chaîne
                            params[param] = cleaned_items
                    else:
                        params[param] = None
    
                # Créer une entrée pour chaque test
                for j in range(nombre_tests):
                    verre_data = {
                        "type": f"{type_verre}_test{j+1}" if nombre_tests > 1 else type_verre,  # Nom unique pour chaque test
                    }
                    for param, flask_key in parametres_flask.items():
                        if params[param] and len(params[param]) > j:
                            verre_data[flask_key] = params[param][j]
                        else:
                            verre_data[flask_key] = "Not available"
                    donnees_verres.append(verre_data)
    
            # Préparer les données à envoyer
            url = 'http://127.0.0.1:5002/add_glass_data'
            donnees = {
                "type": type_doc,
                "titre": titre,
                "reference": reference,
                "premier_auteur": premier_auteur,
                "nombre_types_verres": len(donnees_verres),  # Nombre total d’entrées (une par test)
                "verres": donnees_verres
            }
            print(f"Envoi des données: {donnees}")
    
            reponse = requests.post(url, json=donnees)
    
            if reponse.status_code == 200:
                return Data(value="Données du verre ajoutées avec succès!")
            else:
                return Data(value=f"Erreur lors de l'ajout des données du verre. Code d'état: {reponse.status_code} - {reponse.text}")
    
        except Exception as e:
            return Data(value=f"Exception survenue: {str(e)}")
