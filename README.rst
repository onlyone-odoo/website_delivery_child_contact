===========
Module Name: website_delivery_child_contact
===========
.. |badge1| image:: https://img.shields.io/badge/maturity-Stable-brightgreen
    :target: https://odoo-community.org/page/development-status
    :alt: Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://onlyone.odoo.com/web/image/website/1/logo/OnlyOne%20Soft?unique=dccda5b
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
|badge1| |badge2| |badge3|

This module extends the functionality of the Odoo website_sale module to support the selection of child contacts (type "contact") as delivery addresses during the checkout process and to allow users to choose a specific child contact from the shopping cart page.

**Table of contents**
.. contents::
   :local:

Install
=======
To install this module, follow the standard Odoo module installation process:
1. Clone or copy the module into your Odoo addons directory.
2. Restart the Odoo server.
3. Go to Apps menu, search for "website_delivery_child_contact", and click "Install".

Configure
=========
No specific configuration is required before using this module. It automatically integrates with the existing website_sale flow. However, ensure that:
- Parent contacts (e.g., parents) have child contacts of type "contact" defined under their partner record.
- The child contacts are marked as active.

Usage
=====
1. Go to the Odoo website and navigate to the shop page.
2. Add products to the cart.
3. Proceed to the cart page (/shop/cart), where a dropdown labeled "Comprando para:" will appear if the logged-in user has child contacts of type "contact".
4. Select the desired child contact from the dropdown.
5. The selected child contact will be set as the delivery address for the order. Verify the change in the backend under Sales > Quotations.

Known issues / Roadmap
======================
* Ensure all child contacts have a valid name to avoid display issues in the dropdown.
* Roadmap: Add support for dynamic updates without page reload in a future release.

Bug Tracker
===========
* For bugs or issues, contact support at `support@onlyone.odoo.com <mailto:support@onlyone.odoo.com>`_.

Credits
=======
Authors
~~~~~~~
* Be OnlyOne

Contributors
~~~~~~~~~~~~
* `Be OnlyOne. <https://onlyone.odoo.com/>`_
 
  * Matías Bressanello

Maintainers
~~~~~~~~~~~
This module is maintained by Be OnlyOne