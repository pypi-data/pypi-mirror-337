# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import os

from flask.helpers import send_from_directory
from werkzeug.exceptions import NotFound

from trytond.model import ModelSQL, fields
from trytond.pool import PoolMeta

from nereid import current_app, route

#: Get the default static folder. The content of this folder also
#: goes into the distribution package.
STATIC_FOLDER = os.path.join(
    os.path.abspath(
        os.path.dirname(__file__)
    ), 'static'
)


class Company(metaclass=PoolMeta):
    __name__ = "company.company"

    logo = fields.Many2One("nereid.static.file", "Logo")


class WebShop(ModelSQL):
    "Website"
    __name__ = "nereid.webshop"

    @classmethod
    @route("/static-webshop/<path:filename>", methods=["GET"])
    def send_static_file(self, filename):
        """Function used internally to send static files from the static
        folder to the browser.
        """
        try:
            return send_from_directory(current_app.static_folder, filename)
        except NotFound:
            return send_from_directory(STATIC_FOLDER, filename)


class BannerCategory(metaclass=PoolMeta):
    __name__ = 'nereid.cms.banner.category'

    @staticmethod
    def check_xml_record(records, values):
        return True


class Banner(metaclass=PoolMeta):
    __name__ = 'nereid.cms.banner'

    @staticmethod
    def check_xml_record(records, values):
        return True


class Article(metaclass=PoolMeta):
    __name__ = 'nereid.cms.article'

    @staticmethod
    def check_xml_record(records, values):
        """The webshop module creates a bunch of commonly used articles on
        webshops. Since tryton does not allow records created via XML to be
        edited, this method explicitly allows users to modify the articles
        created by the module.
        """
        return True


class ArticleCategory(metaclass=PoolMeta):
    __name__ = 'nereid.cms.article.category'

    @staticmethod
    def check_xml_record(records, values):
        """The webshop module creates a bunch of commonly used article category on
        webshops. Since tryton does not allow records created via XML to be
        edited, this method explicitly allows users to modify the article
        category created by the module.
        """
        return True


class MenuItem(metaclass=PoolMeta):
    __name__ = 'nereid.cms.menuitem'

    @staticmethod
    def check_xml_record(records, values):
        return True

    @classmethod
    def allowed_models(cls):
        res = super(MenuItem, cls).allowed_models()

        if ('product.tree_node', 'Tree Node') not in res:
            res.append(('product.tree_node', 'Tree Node'))
        if ('product.product', 'Product') not in res:
            res.append(('product.product', 'Product'))
        return res
