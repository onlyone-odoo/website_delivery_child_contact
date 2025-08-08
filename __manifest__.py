{
    "name": "Website Delivery Child Contact",
    "version": "17.0.6.3.1",
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
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_delivery_child_contact/static/src/js/child_select.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
