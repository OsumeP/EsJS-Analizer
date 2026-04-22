from enum import Enum

class SintacticGenerator:
    productions: dict[str, list[list]]
    pred: dict[str, list[set]]

    def __init__(self, productions, pred):
        self.productions = productions
        self.pred = pred


    def build_condition(self, pred):
        conditions = []

        for t in pred:
            if isinstance(t, str):
                conditions.append(f"self.token().name == '{t}'")
            else:
                conditions.append(f"self.token().type == EnumToken.{t.name}")

        return " or ".join(conditions)


    def build_expected(self, preds):
        expected = []

        for p in preds:
            for t in p:
                if isinstance(t, str):
                    expected.append(f"'{t}'")
                else:
                    expected.append(f"EnumToken.{t.name}")

        return ", ".join(expected)


    def generate_parser(self, filename="parser.py"):
        with open(filename, "w", encoding="utf-8") as f:

            # Cabecera
            f.write("import sys\n")
            f.write("from LexicAnalizer import Lexer\n")
            f.write("from EnumTokenModule import EnumToken\n")
            f.write("from Token import Token\n\n")

            f.write("class Parser:\n")

            # constructor
            f.write("    def __init__(self, lexer):\n")
            f.write("        self.lexer = lexer\n")
            f.write("        self.lookahead = self.next_token()\n\n")

            # next token wrapper
            f.write("    def next_token(self):\n")
            f.write("        token = self.lexer.next_token()\n")
            f.write("        if token is None:\n")
            f.write("            return Token(EnumToken.END, 'EOF', -1, -1, None)\n")
            f.write("        return token\n\n")

            # token
            f.write("    def token(self):\n")
            f.write("        return self.lookahead\n\n")

            # match
            f.write("    def match(self, t):\n")
            f.write("        if isinstance(t, str):\n")
            f.write("            if self.lookahead.name == t:\n")
            f.write("                self.lookahead = self.next_token()\n")
            f.write("            else:\n")
            f.write("                self.syntax_error([t])\n")
            f.write("        else:\n")
            f.write("            if self.lookahead.type == t:\n")
            f.write("                self.lookahead = self.next_token()\n")
            f.write("            else:\n")
            f.write("                self.syntax_error([t])\n\n")

            # syntax error
            f.write("    def syntax_error(self, expected):\n")
            f.write("        if self.lookahead.type == EnumToken.END:\n")
            f.write("            found = 'final de archivo'\n")
            f.write("        else:\n")
            f.write("            found = self.lookahead.name\n\n")

            f.write("        expected_str = ', '.join(map(str, expected))\n\n")

            f.write('        print(f"<{self.lookahead.row}:{self.lookahead.col}> Error sintactico: se encontro: \"{found}\"; se esperaba: {expected_str}.)\n\n')

            # Generar funciones por no terminal
            for nonterminal in self.productions:

                f.write(f"    def {nonterminal}(self):\n")

                productions = self.productions[nonterminal]
                preds = self.pred[nonterminal]

                for i, production in enumerate(productions):

                    pred = preds[i]
                    condition = self.build_condition(pred)

                    if i == 0:
                        f.write(f"        if {condition}:\n")
                    else:
                        f.write(f"        elif {condition}:\n")

                    if production == ["ε"]:
                        f.write("            pass\n")
                    else:
                        for symbol in production:

                            if symbol in self.productions:
                                f.write(f"            self.{symbol}()\n")

                            elif symbol != "ε":

                                if isinstance(symbol, str):
                                    f.write(f"            self.match('{symbol}')\n")
                                else:
                                    f.write(
                                        f"            self.match(EnumToken.{symbol.name})\n"
                                    )

                # error
                expected = self.build_expected(preds)

                f.write("        else:\n")
                f.write(f"            self.syntax_error([{expected}])\n\n")