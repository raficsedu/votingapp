def get_formatted_menus(menus):
    items = []
    for menu in menus:
        items.append({
            'item': menu.item,
            'price': menu.price
        })
    return {'menus': items}