from django import template


register = template.Library()


# Return rating of item
@register.inclusion_tag(filename='restaurant/components/menu_engineering/row_cell.html')
def rate_item(obj, total_sold=0, profit_avg=0, percentage_share=0):
    sales_percentage = 0
    if total_sold:
        sales_percentage = (obj.number_sold / total_sold) * 100

    popularity_rate = 'H' if sales_percentage >= percentage_share else 'L'
    profit_rate = 'H' if obj.item_profit >= profit_avg else 'L'

    if profit_rate == 'H' and popularity_rate == 'H':
        return {'rate_result': '*****', 'rate_des': 'سود بالا، محبوبیت بالا'}
    elif profit_rate == 'L' and popularity_rate == 'H':
        return {'rate_result': '****', 'rate_des': 'سود پایین، محبوبیت بالا'}
    elif profit_rate == 'H' and popularity_rate == 'L':
        return {'rate_result': '***', 'rate_des': 'سود بالا، محبوبیت پایین'}
    else:
        return {'rate_result': '**', 'rate_des': 'سود پایین، محبوبیت پایین'}
