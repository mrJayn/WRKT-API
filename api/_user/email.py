from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core import mail

from django.template.context import make_context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode, ExtendsNode
from django.views.generic.base import ContextMixin


from api._user import utils
from api._user.conf import settings


class BaseEmail(mail.EmailMultiAlternatives, ContextMixin):
    """
    Source:
    https://github.com/sunscrapers/django-templated-mail/blob/master/templated_mail/mail.py
    """

    template_name = None
    _node_map = {
        "subject": "subject",
        "text_body": "body",
        "html_body": "html",
    }

    def __init__(self, request=None, context=None, template_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.context = {} if context is None else context
        self.html = None

        if template_name is not None:
            self.template_name = template_name
            filename = str(self.template_name).split("/")[-1]
            filename = filename.removesuffix(".html")
            self.__class__.__name__ = filename

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        context = dict(ctx, **self.context)
        user = context.get("user", (None if not self.request else self.request.user))
        context.update(
            {
                "domain": settings.EMAIL_FRONTEND_DOMAIN,
                "protocol": settings.EMAIL_FRONTEND_PROTOCOL,
                "site_name": settings.EMAIL_FRONTEND_SITE_NAME,
                "user": user,
            }
        )
        return context

    def render(self):
        context = make_context(self.get_context_data(), request=self.request)
        template = get_template(self.template_name)
        with context.bind_template(template.template):
            blocks = self._get_blocks(template.template.nodelist, context)
            for block_node in blocks.values():
                self._process_block(block_node, context)
        self._attach_body()

    def send(self, to, *args, **kwargs):
        self.render()
        self.to = to
        self.cc = kwargs.pop("cc", [])
        self.bcc = kwargs.pop("bcc", [])
        self.reply_to = kwargs.pop("reply_to", [])
        self.from_email = kwargs.pop("from_email", settings.DEFAULT_FROM_EMAIL)
        super().send(*args, **kwargs)

    def _process_block(self, block_node, context):
        attr = self._node_map.get(block_node.name)
        if attr is not None:
            setattr(self, attr, block_node.render(context).strip())

    def _get_blocks(self, nodelist, context):
        blocks = {}
        for node in nodelist:
            if isinstance(node, ExtendsNode):
                parent = node.get_parent(context)
                blocks.update(self._get_blocks(parent.nodelist, context))
        blocks.update(
            {node.name: node for node in nodelist.get_nodes_by_type(BlockNode)}
        )
        return blocks

    def _attach_body(self):
        if self.body and self.html:
            self.attach_alternative(self.html, "text/html")
        elif self.html:
            self.body = self.html
            self.content_subtype = "html"


class AuthEmail(BaseEmail):
    url = None

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = self.url.format(**context)
        return context


class ActivationEmail(AuthEmail):
    template_name = "email/activation.html"
    url = settings.ACTIVATION_URL


class ConfirmationEmail(BaseEmail):
    template_name = "email/confirmation.html"


class PasswordResetEmail(AuthEmail):
    template_name = "email/password_reset.html"
    url = settings.PASSWORD_RESET_CONFIRM_URL


class PasswordChangedConfirmationEmail(BaseEmail):
    template_name = "email/password_changed_confirmation.html"


class UsernameChangedConfirmationEmail(BaseEmail):
    template_name = "email/username_changed_confirmation.html"


class UsernameResetEmail(AuthEmail):
    template_name = "email/username_reset.html"
    url = settings.USERNAME_RESET_CONFIRM_URL
