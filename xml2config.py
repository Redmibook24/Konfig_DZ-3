import argparse
import xml.etree.ElementTree as ET
import sys

class ConfigParser:
    def __init__(self, xml_file):
        self.constants = {}
        self.parse_xml(xml_file)

    def parse_xml(self, xml_file):
        try:
            tree = ET.parse(xml_file)
            self.root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            sys.exit(1)

    def transform(self):
        output = []
        for element in self.root:
            if element.tag == 'var':
                output.append(self.parse_var(element))
            elif element.tag == 'array':
                output.append(self.parse_array(element))
            elif element.tag == 'dict':
                output.append(self.parse_dict(element))
            else:
                raise ValueError(f"Unknown tag: {element.tag}")
        return '\n'.join(output)

    def parse_var(self, element):
        name = element.attrib.get('name')
        value = element.text.strip() if element.text else ''
        return f"var {name} {value};"

    def parse_array(self, element):
        name = element.attrib.get('name')
        values = [value.text.strip() for value in element.findall('value')]
        return f"var {name} ( {', '.join(values)} );"

    def parse_dict(self, element):
        name = element.attrib.get('name')
        entries = []
        for entry in element.findall('entry'):
            key = entry.attrib.get('key')
            value = entry.text.strip() if entry.text else ''
            entries.append(f"{key} -> {value}.")
        return f"var {name} {{\n    " + "\n    ".join(entries) + "\n}}"

def main():
    parser = argparse.ArgumentParser(description="XML to Custom Config Language Converter")
    parser.add_argument('-i', '--input', required=True, help='Path to the input XML file')
    parser.add_argument('-o', '--output', required=True, help='Path to the output config file')
    
    args = parser.parse_args()
    
    # Парсим XML и конвертируем его
    try:
        config_parser = ConfigParser(args.input)
        result = config_parser.transform()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Сохраняем результат в файл
    with open(args.output, 'w') as f:
        f.write(result)
    
    print(f"Configuration has been successfully written to {args.output}")

if __name__ == '__main__':
    main()
