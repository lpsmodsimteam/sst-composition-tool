import subprocess
import xml.etree.ElementTree as ET


class SSTInfoXMLParser:
    def __init__(self, file_name: str = "SSTInfo.xml") -> None:

        return_code = subprocess.run(["sst-info", "-no", file_name])
        self.tree = (
            ET.parse(file_name).getroot() if return_code.returncode == 0 else None
        )
        self.parsed_data = []

    def get_names_list(self) -> list:

        for element in self.tree.findall("Element"):
            element_data = {
                "name": element.attrib["Name"],
            }
            component_data = {
                "name": None,
                "ports": [],
            }
            for component in element.findall("Component"):
                component_data["name"] = component.attrib["Name"]
                for item in component.findall("Port"):
                    component_data["components"].append(component.attrib["Name"])
            self.parsed_data.append(element_data)

        # return [item.attrib["Name"] for item in tree.findall("Element")]


obj = SSTInfoXMLParser()
print(obj.get_names_list())
