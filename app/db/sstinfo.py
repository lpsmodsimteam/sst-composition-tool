import subprocess
import xml.etree.ElementTree as ET


class SSTInfoXMLParser:
    def __init__(self, file_name: str = "SSTInfo.xml") -> None:

        return_code = subprocess.run(["sst-info", "-no", file_name])
        self.tree = (
            ET.parse(file_name).getroot() if return_code.returncode == 0 else None
        )
        self.parsed_data = []
        self.children_keys = {"Port", "Parameter"}

    def xml_to_dict(self) -> list:

        for element in self.tree.findall("Element"):
            element_data = {
                "Name": element.attrib["Name"],
                "Component": [],
            }
            for component in element.findall("Component"):
                component_data = {
                    "Name": component.attrib["Name"],
                }

                for child_item in self.children_keys:
                    component_data[child_item] = []

                    for child_data in component.findall(child_item):
                        component_data[child_item].append(child_data.attrib)

                element_data["Component"].append(component_data)

            self.parsed_data.append(element_data)

    def get_dict(self):

        return self.parsed_data


if __name__ == "__main__":

    obj = SSTInfoXMLParser()
    obj.xml_to_dict()

    from pprint import pprint

    pprint(obj.get_dict())
