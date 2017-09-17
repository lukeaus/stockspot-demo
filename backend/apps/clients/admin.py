from django.contrib import admin
from django.urls import reverse
from .models import Client
from apps.securities.models import Security


class ClientAdmin(admin.ModelAdmin):
    search_fields = ('user__email', 'user__first_name', 'user__middle_name', 'user__last_name',
        'client_id', 'hin',)
    fields = ('user', 'client_id', 'hin', 'advisor', 'portfolio_', 'portfolio_market_value_display',
        'portfolio_profit_display',)
    readonly_fields = ('portfolio_', 'portfolio_market_value_display', 'portfolio_profit_display',)

    def portfolio_(self, obj):
        """Make the Client's portfolio more readable"""
        if obj:
            table_body = ''
            for key, val in obj.portfolio().items():
                security_admin_url = reverse(
                    'admin:%s_%s_change' % ('securities', 'security'),
                    args=(val['security_pk'],)
                )
                table_body += """
                    <tr>
                      <td><a href={security_admin_url}>{security_code}</a></td>
                      <td>{qty}</td>
                      <td>{price_latest}</td>
                      <td>{market_value_display}</td>
                    </tr>
                    """.format(security_code=val['code'],
                               security_admin_url=security_admin_url,
                               qty=val['qty'],
                               price_latest=val['price_latest_display'],
                               market_value_display=val['market_value_display'])

            html_table = """
                <table>
                <thead>
                  <th>Security</th>
                  <th>Qty</th>
                  <th>Price Latest</th>
                  <th>Market Value</th>
                </thead>
                <tbody>
                  {table_body}
                </tbody>
                </table>
                """.format(table_body=table_body)
            return html_table if obj.portfolio() else None

    portfolio_.allow_tags = True


admin.site.register(Client, ClientAdmin)
