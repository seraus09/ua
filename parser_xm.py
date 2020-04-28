import xml.etree.ElementTree as ET

def reg():
    tree = ET.parse('1.xml')#Open the file
    root = tree.getroot()
    lis = []
    for  i in root[3][0][0][2]:#Xml tree, index navigation
        name = i.attrib#get name
        price = i[0].attrib# get price
        cost = price.get('YourAdditonalCost')
        if cost is None:
            g = str(cost).replace('None', '0')
            res = (f"Цена {name.get('Name')}: REG Период - {price.get('DurationType')}, Цена - {float(price.get('YourPrice') + g)}")
            lis.append(res)
        else:
            res = (f"Цена {name.get('Name')}: REG Период - {price.get('DurationType')}, Цена - {float(price.get('YourPrice')) + float(price.get('YourAdditonalCost'))}")
            lis.append(res)

        result = '\n'.join(lis)
    return result

print(reg())