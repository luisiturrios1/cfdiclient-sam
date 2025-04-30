import xml.etree.ElementTree as ET

CFDI = 'http://www.sat.gob.mx/cfd/4'
TIMBRE = 'http://www.sat.gob.mx/TimbreFiscalDigital'


def parser40(root):
    campos_cfdi = {}
    campos_cfdi['Version'] = root.attrib.get('Version')
    campos_cfdi['Serie'] = root.attrib.get('Serie', '')
    campos_cfdi['Folio'] = root.attrib.get('Folio', '')
    campos_cfdi['Fecha'] = root.attrib.get('Fecha', '')
    campos_cfdi['RfcEmisor'] = root.find(
        f'.//{{{CFDI}}}Emisor').attrib.get('Rfc', '')
    campos_cfdi['NombreEmisor'] = root.find(
        f'.//{{{CFDI}}}Emisor').attrib.get('Nombre', '')
    campos_cfdi['RfcReceptor'] = root.find(
        f'.//{{{CFDI}}}Receptor').attrib.get('Rfc', '')
    campos_cfdi['NombreReceptor'] = root.find(
        f'.//{{{CFDI}}}Receptor').attrib.get('Nombre', '')
    campos_cfdi['DomicilioFiscalReceptor'] = root.find(
        f'.//{{{CFDI}}}Receptor').attrib.get('DomicilioFiscalReceptor', '')
    campos_cfdi['RegimenFiscalReceptor'] = root.find(
        f'.//{{{CFDI}}}Receptor').attrib.get('RegimenFiscalReceptor', '')
    campos_cfdi['UsoCFDI'] = root.find(
        f'.//{{{CFDI}}}Receptor').attrib.get('UsoCFDI', '')
    campos_cfdi['CondicionesDePago'] = root.attrib.get('CondicionesDePago', '')
    campos_cfdi['SubTotal'] = root.attrib.get('SubTotal', '')
    campos_cfdi['Moneda'] = root.attrib.get('Moneda', '')
    campos_cfdi['TipoCambio'] = root.attrib.get('TipoCambio', '')
    campos_cfdi['Total'] = root.attrib.get('Total', '')
    campos_cfdi['TipoDeComprobante'] = root.attrib.get('TipoDeComprobante', '')
    campos_cfdi['Exportacion'] = root.attrib.get('Exportacion', '')
    campos_cfdi['MetodoPago'] = root.attrib.get('MetodoPago', '')
    campos_cfdi['LugarExpedicion'] = root.attrib.get('LugarExpedicion', '')

    impuestos_node = root.findall(f'.//{{{CFDI}}}Impuestos')
    if len(impuestos_node) > 0:
        impuestos_node = impuestos_node[-1]
        campos_cfdi['TotalImpuestosTrasladados'] = impuestos_node.attrib.get(
            'TotalImpuestosTrasladados', '')
        campos_cfdi['TotalImpuestosRetenidos'] = impuestos_node.attrib.get(
            'TotalImpuestosRetenidos', '')

    campos_cfdi['UUID'] = root.find(
        f'.//{{{TIMBRE}}}TimbreFiscalDigital').attrib.get('UUID', '')
    campos_cfdi['FechaTimbrado'] = root.find(
        f'.//{{{TIMBRE}}}TimbreFiscalDigital').attrib.get('FechaTimbrado', '')

    return campos_cfdi


if __name__ == '__main__':
    root = None
    with open('f90a1157-52a4-4bbc-bffb-69b4777db9ae.xml', 'rb') as fs:
        root = ET.fromstring(fs.read())
    print(parser40(root))
