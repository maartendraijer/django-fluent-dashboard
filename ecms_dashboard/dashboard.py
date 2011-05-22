"""
Custom dashboard for ECMS.

To activate the index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'ecms_dashboard.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'ecms_dashboard.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name  # needs 0.4.0

from ecms_dashboard.modules import CmsAppIconList, AppIconList


ADMINISTRATION_APPS = ('django.contrib.*', 'registration.*',)
DEVELOPER_APPS = ()
ALL_KNOWN_APPS = ADMINISTRATION_APPS + DEVELOPER_APPS


class EcmsIndexDashboard(Dashboard):
    """
    Custom index dashboard for ECMS
    """
    class Media:
        css = ("ecms_dashboard/dashboard.css",)

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        quick_links = modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        )

        apps = CmsAppIconList(
            _('CMS'),
            exclude=ALL_KNOWN_APPS,
            collapsible=False
        )

        administration = AppIconList(
            _('Administration'),
            models=ADMINISTRATION_APPS,
            collapsible=False
        )

        if DEVELOPER_APPS:
            development = AppIconList(
                _('Developer tools'),
                models=DEVELOPER_APPS,
                collapsible=True
            )

        recent_actions = modules.RecentActions(_('Recent Actions'), 5, enabled=False, collapsible=False)

        self.children.append(quick_links)
        self.children.append(apps)
        self.children.append(administration)
        if DEVELOPER_APPS:
            self.children.append(development)

        self.children.append(recent_actions)


class EcmsAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for ECMS
    """

    # disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        model_list = modules.ModelList(self.app_title, self.models)

        recent_actions = modules.RecentActions(
            _('Recent Actions'),
            include_list=self.get_app_content_types(),
            limit=5,
            enabled=False,
            collapsible=False
        )

        self.children += [model_list, recent_actions]


    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(EcmsAppIndexDashboard, self).init_with_context(context)