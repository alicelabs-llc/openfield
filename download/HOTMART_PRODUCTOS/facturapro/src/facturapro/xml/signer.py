"""FacturaPro — XML digital signing (XAdES-EPES for SRI).

Note: full XAdES signing requires xmlsig + cryptography. This module
implements the XAdES envelope structure; the actual crypto signature
is computed via xmlsig.sign().
"""
from __future__ import annotations
from lxml import etree
from pathlib import Path

XADES_NS = "http://uri.etsi.org/01903/v1.3.2#"
DS_NS = "http://www.w3.org/2000/09/xmldsig#"


def wrap_with_xades_envelope(factura_xml: str, signature_id: str = "Sign") -> str:
    """Wrap a factura XML with the XAdES-EPES envelope expected by SRI.

    This produces the structure that gets signed. The actual <ds:SignatureValue>
    is filled by the signer (xmlsig or external service).
    """
    # Parse the original factura
    factura_tree = etree.fromstring(factura_xml.encode("utf-8"))

    # Create the outer comprobante container
    nsmap = {
        None: "http://www.gob.ec/sri/empleo/esquema/factura",
        "ds": DS_NS,
        "xades": XADES_NS,
    }
    outer = etree.Element("comprobante", nsmap=nsmap)
    outer.append(factura_tree)

    # Append ds:Signature placeholder with SignedInfo + KeyInfo + Object
    sig = etree.SubElement(outer, f"{{{DS_NS}}}Signature", attrib={"Id": signature_id})
    signed_info = etree.SubElement(sig, f"{{{DS_NS}}}SignedInfo")
    etree.SubElement(signed_info, f"{{{DS_NS}}}CanonicalizationMethod",
                     attrib={"Algorithm": "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"})
    etree.SubElement(signed_info, f"{{{DS_NS}}}SignatureMethod",
                     attrib={"Algorithm": "http://www.w3.org/2000/09/xmldsig#rsa-sha1"})
    ref = etree.SubElement(signed_info, f"{{{DS_NS}}}Reference", attrib={"URI": f"#{signature_id}-SignedProperties"})
    transforms = etree.SubElement(ref, f"{{{DS_NS}}}Transforms")
    etree.SubElement(transforms, f"{{{DS_NS}}}Transform",
                     attrib={"Algorithm": "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"})
    etree.SubElement(ref, f"{{{DS_NS}}}DigestMethod",
                     attrib={"Algorithm": "http://www.w3.org/2000/09/xmldsig#sha1"})
    etree.SubElement(ref, f"{{{DS_NS}}}DigestValue")

    etree.SubElement(sig, f"{{{DS_NS}}}SignatureValue")
    key_info = etree.SubElement(sig, f"{{{DS_NS}}}KeyInfo")
    x509_data = etree.SubElement(key_info, f"{{{DS_NS}}}X509Data")
    etree.SubElement(x509_data, f"{{{DS_NS}}}X509Certificate")

    # Object with xades:QualifyingProperties
    obj = etree.SubElement(sig, f"{{{DS_NS}}}Object")
    qprops = etree.SubElement(obj, f"{{{XADES_NS}}}QualifyingProperties", attrib={
        "Target": f"#{signature_id}",
    })
    qprops_props = etree.SubElement(qprops, f"{{{XADES_NS}}}SignedProperties",
                                    attrib={"Id": f"{signature_id}-SignedProperties"})
    sig_props = etree.SubElement(qprops_props, f"{{{XADES_NS}}}SignedSignatureProperties")
    etree.SubElement(sig_props, f"{{{XADES_NS}}}SigningTime")
    cert_props = etree.SubElement(sig_props, f"{{{XADES_NS}}}SigningCertificate")
    cert = etree.SubElement(cert_props, f"{{{XADES_NS}}}Cert")
    cert_digest = etree.SubElement(cert, f"{{{XADES_NS}}}CertDigest")
    etree.SubElement(cert_digest, f"{{{DS_NS}}}DigestMethod",
                     attrib={"Algorithm": "http://www.w3.org/2000/09/xmldsig#sha1"})
    etree.SubElement(cert_digest, f"{{{DS_NS}}}DigestValue")

    return etree.tostring(outer, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode("utf-8")


def sign_xml(xml_str: str, cert_path: str, cert_password: str) -> str:
    """Sign XML using xmlsig (real RSA-SHA1 with .p12 cert).

    In production, requires xmlsig + libxml2 + openssl. Falls back to a
    "development" envelope if xmlsig is not available (the XML is structurally
    valid but unsigned — only usable in ambiente=pruebas).
    """
    try:
        import xmlsig  # type: ignore
    except ImportError:
        # Dev mode: return the unsigned XML with a warning comment
        tree = etree.fromstring(xml_str.encode("utf-8"))
        comment = etree.Comment(" DEV MODE: not signed — install xmlsig for production signing ")
        tree.insert(0, comment)
        return etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode("utf-8")

    # Production signing path (requires xmlsig)
    cert_p = Path(cert_path).expanduser()
    if not cert_p.exists():
        raise FileNotFoundError(f"Certificate not found: {cert_path}")

    root = etree.fromstring(xml_str.encode("utf-8"))
    sig_node = xmlsig.template.create(
        c14n_method=xmlsig.constants.TransformInclC14N,
        sign_method=xmlsig.constants.TransformRsaSha1,
    )
    xmlsig.template.add_reference(
        sig_node,
        xmlsig.constants.TransformSha1,
        uri="",
        uri_type="",
    )
    xmlsig.template.add_x509_cert(sig_node)

    ctx = xmlsig.SignatureContext()
    key = xmlsig.KeysProvider().load_pkcs12(str(cert_p), cert_password)
    ctx.key = key
    ctx.sign(sig_node)
    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode("utf-8")
