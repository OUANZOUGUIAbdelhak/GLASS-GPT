from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message
import re

class GlassCompositionConverter(Component):
    display_name = "Glass Composition Converter"
    description = "Converts glass composition from any unit to mol% element, preserving existing mol% element values."
    documentation = "https://docs.langflow.org/components-custom-components"
    icon = "code"
    name = "GlassCompositionConverter"

    inputs = [
        MessageTextInput(
            name="input_text",
            display_name="Input Text",
            info="Text containing glass composition data from the LLM (e.g., wt% oxide, wt% element, mol% oxide, or mol% element).",
        ),
    ]

    outputs = [
        Output(display_name="Converted Data", name="converted_data", method="process_input"),
    ]

    def process_input(self) -> Message:
        """Process the input text, extract data, and convert all units to mol% element."""
        text = self.input_text
        lines = text.split('\n')
        current_glass = None
        data_by_glass = {}

        # Parse each line
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect the start of a new glass (English header: "Glass X:")
            if line.startswith("Glass"):
                current_glass = line.split(":")[0].strip()
                data_by_glass[current_glass] = []
                continue

            # Parse composition data (lines starting with a number followed by ".")
            if current_glass and re.match(r'\d+\.', line):
                data = self.parse_line(line)
                if data:
                    data_by_glass[current_glass].append(data)

        # Perform conversions
        self.convert_compositions(data_by_glass)

        # Generate output text and convert to Message
        output_text = self.format_output(data_by_glass)
        message = Message(text=output_text)
        self.status = message.text  # Update status with the message text
        return message

    def parse_line(self, line):
        """Parse a line to extract oxide, element, and values."""
        match = re.match(r'\d+\. \[(\w+)\]\[(\w+)\] :', line)
        if not match:
            return None
        oxide, element = match.groups()

        data = {'oxide': oxide, 'element': element}
        parts = line.split(':')[1].strip().split(';')
        for part in parts:
            part = part.strip()
            if part:
                match = re.search(r'\[([\d.]+)\]\[(\w+%)\]\[(\w+)\]', part)
                if match:
                    value, unit, type_ = match.groups()
                    key = f"{unit}_{type_}"
                    data[key] = float(value) if value else 0
                else:
                    raise ValueError(f"Invalid part format: {part}")
        return data

    def get_stoichiometric_coefficient(self, oxide, element):
        """Return the stoichiometric coefficient of the element in the oxide."""
        match = re.match(rf'^{element}(\d*)', oxide)
        if match:
            coeff_str = match.group(1)
            return int(coeff_str) if coeff_str else 1
        return 1  # Default to 1 if not found

    def get_oxygen_coefficient(self, oxide):
        """Retourne le nombre d'atomes d'oxygène dans la formule oxide.
        Exemples :
        - 'SiO2' retourne 2
        - 'B2O3' retourne 3
        """
        match = re.search(r'O(\d+)', oxide)
        if match:
            return int(match.group(1))
        else:
            # Si la formule ne comporte pas de chiffre après 'O', on suppose 1.
            return 1

    def convert_compositions(self, data_by_glass):
        """Convert all units (wt% oxide, wt% element, mol% oxide) to mol% element, preserving existing mol% element."""
        molar_masses = {
            'SiO2': 60.08, 'Si': 28.09,
            'B2O3': 69.62, 'B': 10.81,
            'P2O5': 141.94, 'P': 30.97,
            'TeO2': 159.60, 'Te': 127.60,
            'GeO2': 104.64, 'Ge': 72.64,
            'As2O3': 197.84, 'As': 74.92,
            'Sb2O3': 291.52, 'Sb': 121.76,
            'Bi2O3': 465.96, 'Bi': 208.98,
            'V2O5': 181.88, 'V': 50.94,
            'WO3': 231.84, 'W': 183.84,
            'Na2O': 61.98, 'Na': 22.99,
            'K2O': 94.20, 'K': 39.10,
            'Li2O': 29.88, 'Li': 6.94,
            'CaO': 56.08, 'Ca': 40.08,
            'MgO': 40.31, 'Mg': 24.31,
            'BaO': 153.33, 'Ba': 137.33,
            'SrO': 103.62, 'Sr': 87.62,
            'Cs2O': 281.81, 'Cs': 132.91,
            'Rb2O': 186.94, 'Rb': 85.47,
            'PbO': 223.20, 'Pb': 207.20,
            'ZnO': 81.38, 'Zn': 65.38,
            'CdO': 128.41, 'Cd': 112.41,
            'Ag2O': 231.74, 'Ag': 107.87,
            'Tl2O': 424.76, 'Tl': 204.38,
            'Al2O3': 101.96, 'Al': 26.98,
            'Fe2O3': 159.69, 'Fe': 55.85,
            'TiO2': 79.87, 'Ti': 47.87,
            'ZrO2': 123.22, 'Zr': 91.22,
            'CeO2': 172.12, 'Ce': 140.12,
            'La2O3': 325.81, 'La': 138.91,
            'Nd2O3': 336.48, 'Nd': 144.24,
            'HfO2': 210.49, 'Hf': 178.49,
            'SnO2': 150.71, 'Sn': 118.71,
            'NiO': 74.69, 'Ni': 58.69,
            'Cr2O3': 152.00, 'Cr': 52.00,
            'MnO2': 86.94, 'Mn': 54.94,
            'Y2O3': 225.81, 'Y': 88.91,
            'Pr2O3': 329.81, 'Pr': 140.91,
            'Sm2O3': 348.72, 'Sm': 150.36,
            'Eu2O3': 351.92, 'Eu': 151.96,
            'Gd2O3': 362.50, 'Gd': 157.25,
            'Nb2O5': 265.81, 'Nb': 92.91,
            'Ta2O5': 441.89, 'Ta': 180.95,
            'ThO2': 264.04, 'Th': 232.04,
            'Ga2O3': 187.44, 'Ga': 69.72,
            'In2O3': 277.64, 'In': 114.82,
            'Tb2O3': 365.85, 'Tb': 158.93,
            'Dy2O3': 373.00, 'Dy': 162.50,
            'Er2O3': 382.52, 'Er': 167.26,
            'Yb2O3': 394.10, 'Yb': 173.05,
            'Sc2O3': 137.91, 'Sc': 44.96,
            'Ho2O3': 377.86, 'Ho': 164.93,
            'Tm2O3': 385.86, 'Tm': 168.93,
            'Lu2O3': 397.94, 'Lu': 174.97,
            'UO2': 270.03, 'U': 238.03,
            'UO3': 286.03, 'U': 238.03,
            'PuO2': 276.06, 'Pu': 244.06,
            'NpO2': 269.05, 'Np': 237.05,
            'Am2O3': 534.12, 'Am': 243.06,
            'Cm2O3': 542.14, 'Cm': 247.07,
            'MoO3': 143.95, 'Mo': 95.95,
            'RuO2': 133.07, 'Ru': 101.07,
            'SeO2': 110.97, 'Se': 78.97,
            'CoO': 74.93, 'Co': 58.93,
            'CuO': 79.55, 'Cu': 63.55,
            'Au2O3': 441.94, 'Au': 196.97,
        }

        for glass, compositions in data_by_glass.items():
            if not compositions:
                continue

            # Dictionnaire pour agréger les moles par espèce pour chaque verre.
            aggregated_moles = {}
            has_convertible_data = False

            # Parcourir les données pour chaque composant
            for data in compositions:
                oxide = data['oxide']
                element = data['element']

                mole_value = None

                # Prioriser mol% oxide
                if data.get('mol%_oxide', 0) > 0:
                    mole_value = data['mol%_oxide'] / 100
                    has_convertible_data = True
                # Sinon, essayer wt% oxide
                elif data.get('wt%_oxide', 0) > 0:
                    if oxide in molar_masses:
                        mole_value = data['wt%_oxide'] / molar_masses[oxide]
                        has_convertible_data = True
                # Sinon, wt% element (attention, cette méthode ne donne pas la part d'oxygène)
                elif data.get('wt%_element', 0) > 0:
                    if element in molar_masses:
                        mole_value = data['wt%_element'] / molar_masses[element]
                        has_convertible_data = True

                if mole_value is None:
                    continue

                # Calculer les moles de cation et d’oxygène pour cet oxyde
                stoich_cation = self.get_stoichiometric_coefficient(oxide, element)
                stoich_oxygen = self.get_oxygen_coefficient(oxide)

                moles_cation = mole_value * stoich_cation
                moles_oxygen = mole_value * stoich_oxygen

                # Ajouter aux agrégations
                aggregated_moles[element] = aggregated_moles.get(element, 0) + moles_cation
                aggregated_moles['O'] = aggregated_moles.get('O', 0) + moles_oxygen

            # Si on a des données convertibles, calculer la mol%
            if has_convertible_data:
                total_moles = sum(aggregated_moles.values())
                # On ajoute les mol% dans aggregated_moles sous forme de pourcentage
                for species, moles in aggregated_moles.items():
                    aggregated_moles[species] = round((moles / total_moles) * 100, 2)

                # Remplacer le contenu de data_by_glass avec les résultats agrégés
                # Nous créons une liste de dictionnaires pour conserver le même format de sortie
                data_by_glass[glass] = [{'element': species, 'mol%_element': aggregated_moles[species]} for species in aggregated_moles]


    def format_output(self, data_by_glass):
        """Format the converted data into readable text."""
        output = []
        for glass, compositions in data_by_glass.items():
            if compositions:  # Only if data exists
                output.append(f"{glass.lower()}:")
                for data in compositions:
                    element = data['element']
                    mol_percent = data.get('mol%_element', 0)
                    if mol_percent > 0:
                        output.append(f"mol% {element} = {mol_percent}")
        return "\n".join(output)
