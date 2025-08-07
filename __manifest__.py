{
    "name": "Website Delivery Child Contact",
    "version": "17.0.3.2.0",
    "category": "Website/eCommerce",
    "summary": 'Permitir seleccionar contactos hijos tipo "contact" como direcciones de entrega en el checkout',
    "description": """
        Extiende el checkout del website para incluir contactos hijos de tipo 'contact' (individuos) como opciones de dirección de entrega,
        incluso si no son de tipo 'delivery'.
    """,
    "author": "Be OnlyOne",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "license": "AGPL-3",
    "depends": ["website_sale"],
    "data": [
        "views/templates.xml",  # Si decides agregar herencia de vistas
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
