import pandas as pd 
df = pd.read_csv('hotel_booking.csv')

print(df.head(7))

df = df.rename(columns={
    'is canceled':'is_canceled',
    'lead time' : 'lead_time',
    'arrival date year': 'arrival_date_year',
    'arrival date month' : 'arrival_date_month',
    'arrival date week number' : 'arrival_date_week_number ',
    'arrival date day of month' : 'arrival_date_day_of_month',
    'stays in weekend nights' : 'stays_in_weekend_nights',
    'stays in week nights' : 'stays_in_week_nights', 
    'market segment' : 'market_segment',
    'distribution channel' : 'distribution_channel',
    'is repeated guest' : 'is_repeated_guest',
    'previous cancellations' : 'previous_cancellations',
    'previous bookings not canceled' : 'previous_bookings_not_canceled',
    'reserved room type' : 'reserved_room_type',
    'assigned room type' : 'assigned_room_type',
    'booking changes' : 'booking_changes',
    'deposit type' : 'deposit_type',
    'days in waiting list' : 'days_in_waiting_list',
    'customer type' : 'customer_type',
    'required car parking spaces' : 'required_car_parking_spaces',
    'total of special requests' : 'total_of_special_requests',
    'reservation status' : 'reservation_status',
    'reservation status date' : 'reservation_status_date',
    'phone number' : 'phone_number',
    'credit card' : 'credit_card',
})

# Статистика по странам
secsess_customers_by_country = df.query('is_canceled == 0') \
    .groupby(['country'], as_index=False)\
    .aggregate({'is_canceled' : 'count'}, ascending=False) \
    .sort_values('is_canceled', ascending=False) \
    .head(5) \
    .rename(columns={'country' : 'Страна', 'is_canceled' : 'Количество успешных бронирований'})


# Статистика среднему количеству ночей
df['stays_total_night'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']

mean_stays_by_hotelType = df.query('is_canceled == 0') \
    .groupby('hotel', as_index=False) \
    .aggregate({'stays_total_night' : 'mean'}).round(2) \
    .sort_values('stays_total_night', ascending=False) \
    .rename(columns={'hotel' : 'Тип отеля', 'stays_total_night' : 'Среднее количество ночей в отеле'})

print(df.info())

# Статистика по сменненому типу номера в отеле
count_change_room_type = df.query('is_canceled == 0')\
    .query('reserved_room_type != assigned_room_type')\
    .aggregate({'is_canceled' : 'count'}) \
    

# Статистика по самому популярному месяцу бронирования в 2016
month_of_2016 = df.query('is_canceled == 0 & arrival_date_year == 2016') \
    .groupby('arrival_date_month', as_index=False) \
    .aggregate({'is_canceled' : 'count'}) \
    .sort_values('is_canceled', ascending=False) \
    .head(1)['arrival_date_month'].values[0]

# Статистика по самому популярному месяцу бронирования в 2017
month_of_2017 = df.query('is_canceled == 0 & arrival_date_year == 2017') \
    .groupby('arrival_date_month', as_index=False) \
    .aggregate({'is_canceled' : 'count'}) \
    .sort_values('is_canceled', ascending=False) \
    .head(1)['arrival_date_month'].values[0]

# Статистика по детям
df['total_kids'] = df['children'] + df['babies']

mean_kids_by_hotel = df.groupby('hotel', as_index=False) \
    .aggregate({'total_kids' : 'mean'}).round(2) \
    .sort_values('total_kids', ascending=False)

# Статистика оттока клиентов
df['has_kids'] = (df['total_kids'] > 0)
canceled_all = df.query('is_canceled == 1') \
    .aggregate({'is_canceled' : 'count'}) \
    .values[0]

canceled_with_kids = df.query('is_canceled == 1') \
    .groupby('has_kids') \
    .aggregate({'has_kids' : 'count'}) \
    .loc[True] \
    .values[0]


print('\n Статистика по странам')
print(secsess_customers_by_country)

print('\n Среднее количество ночей в отелях')
print(mean_stays_by_hotelType)

print('\n Количество сменненых типов номеров в отелях ')
print(count_change_room_type['is_canceled'])

print('\n Статистика по самому бронируемому месяцу в 2016')
print(month_of_2016)

print('\n Статистика по самому бронируемому месяцу в 2017')
print(month_of_2017)

print('\n Статистика по среднему количеству детей в отелях:')
print(mean_kids_by_hotel)

print("\n Статистика оттока клиентов с детьми к общему количеству оттока:")
print("{} %".format((canceled_with_kids / canceled_all * 100).round(2)) )