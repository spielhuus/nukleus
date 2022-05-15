from typing import Dict, List

from .AbstractParser import AbstractParser
from .ModelSchema import Symbol


class Bom(AbstractParser):

    def __init__(self, grouped: bool = True, child: AbstractParser | None = None) -> None:
        super().__init__(child)
        AbstractParser.__init__(self, child)
        self.grouped = grouped
        self.symbols: Dict[str, List[Symbol]] = {}

    @staticmethod
    def _number(number):
        numbers = ''
        for char in number:
            if char.isdigit():
                numbers += char
        assert len(numbers) > 0, f'no number found in {number}'
        return int(numbers)

    @staticmethod
    def _letter(letter):
        letters = ''
        for char in letter:
            if char.isalpha():
                letters += char
        return letters

    def bom(self):

        # search for power and gnd and replace netnames
        result_bom = []
        target_sorted = {}
        for ref, symbols in self.symbols.items():
            ref = symbols[0].property('Reference').value
            val = symbols[0].property('Value').value
            footprint = symbols[0].property('Footprint').value
            datasheet = ''
            for symbol in symbols:
                if symbol.has_property('Datasheet'):
                    datasheet = symbol.property('Datasheet').value
            description = ''
            for symbol in symbols:
                if symbol.has_property('Description'):
                    description = symbol.property('Description').value
            result_bom.append({'ref': ref, 'value': val, 'footprint': footprint,
                               'datasheet': datasheet, 'description': description})

            target_sorted[('%s%03d' % (Bom._letter(ref), Bom._number(ref)))] = {
                'ref': ref,
                'value': val,
                'datasheet': datasheet,
                'description': description,
                'footprint': footprint
            }

        if self.grouped:
            target_grouped = {}
            for key in sorted(target_sorted):
                element = target_sorted[key]
                if ('%s-%s' % (element['value'], element['footprint'])) in target_grouped:
                    target_grouped[('%s-%s' % (element['value'],
                                    element['footprint']))]['ref'].append(element['ref'])
                else:
                    target_grouped[('%s-%s' % (element['value'], element['footprint']))] = {
                        'ref': [element['ref']],
                        'value': element['value'],
                        'datasheet': element['datasheet'],
                        'description': element['description'],
                        'footprint': element['footprint']
                    }

            result_bom = []
            for key, element in target_grouped.items():
                result_bom.append({
                    'ref': element['ref'],
                    'value': element['value'],
                    'datasheet': element['datasheet'],
                    'description': element['description'],
                    'footprint': element['footprint']
                })

        return {'bom': result_bom}

    def visitSymbol(self, symbol: Symbol):
        assert symbol.library_symbol, 'symbol has no library symbol'
        if symbol.library_symbol.extends not in ['power']:
            if symbol.property('Reference').value in self.symbols:
                self.symbols[symbol.property('Reference').value].append(symbol)
            else:
                self.symbols[symbol.property('Reference').value] = [symbol]
        super().visitSymbol(symbol)
