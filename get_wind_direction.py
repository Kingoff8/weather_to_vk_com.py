def get_wind_direction(deg):
    l = ['северный,', 'северо-восточный,', 'восточный,', 'юго-восточный,', 'южный,', 'юго-западный,', 'западный,',
         'северо-западный,']
    for i in range(0, 8):
        step = 45.
        min = i * step - 45 / 2.
        max = i * step + 45 / 2.
        if i == 0 and deg > 360 - 45 / 2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res