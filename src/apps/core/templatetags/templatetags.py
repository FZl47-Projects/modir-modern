from django import template
from persian_tools.digits import add_separator

register = template.Library()


# Return rating of item
@register.inclusion_tag(filename='restaurant/components/menu_engineering/row_cell.html')
def rate_item(obj, total_sold=0, total_profit=0, percentage_share=0):
    sales_percentage = 0
    profit_avg = 0
    if total_sold:
        sales_percentage = (obj.number_sold / total_sold) * 100
        profit_avg = int(total_profit / total_sold)

    popularity_rate = 'H' if sales_percentage and percentage_share and sales_percentage >= percentage_share else 'L'
    profit_rate = 'H' if obj.item_profit and profit_avg and obj.item_profit >= profit_avg else 'L'

    if profit_rate == 'H' and popularity_rate == 'H':
        return {'rate_result': '*****', 'rate_des': 'سود بالا، محبوبیت بالا'}
    elif profit_rate == 'L' and popularity_rate == 'H':
        return {'rate_result': '****', 'rate_des': 'سود پایین، محبوبیت بالا'}
    elif profit_rate == 'H' and popularity_rate == 'L':
        return {'rate_result': '***', 'rate_des': 'سود بالا، محبوبیت پایین'}
    else:
        return {'rate_result': '**', 'rate_des': 'سود پایین، محبوبیت پایین'}


# Return average of food costs
@register.simple_tag
def avg_food_costs(total_food_costs=0, obj_counts=0):
    if obj_counts:
        return int(total_food_costs / obj_counts)
    return 0


# Return each_item_profit_avg
@register.simple_tag
def each_item_profit_avg(total_total_profit=0, total_number_sold=0):
    if total_number_sold:
        return add_separator(int(total_total_profit / total_number_sold))
    return 0
