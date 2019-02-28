import datetime

from sqlalchemy import or_, and_

from App.models.cinema.hall_model import Hall
from App.models.cinema.paidang_model import PaiDang
from App.models.viewer.seat_order_model import SeatOrder, SEAT_ORDER_STATUS_PAYED, SEAT_ORDER_STATUS_NOT_PAY


def get_avaliable_seats(paidang_pk):
    seatorders = SeatOrder.query.filter(SeatOrder.s_paidang.__eq__(paidang_pk)) \
        .filter(or_(SeatOrder.s_status.__eq__(SEAT_ORDER_STATUS_PAYED)
                    , and_(SeatOrder.s_status.__eq__(SEAT_ORDER_STATUS_NOT_PAY), SeatOrder.s_expire.__ge__(datetime.datetime.now()))))

    sold_seats = set()

    paidang = PaiDang.query.get(paidang_pk)

    hall = Hall.query.get(paidang.p_hall)

    for seatorder in seatorders:
        seat_list = seatorder.s_seats.split("#")
        print("seat_list", seat_list)
        sold_seats |= set(seat_list)

    all_seats = set(hall.h_seats.split("#"))

    print(sold_seats)

    print(all_seats)

    avaliable_seats = all_seats - sold_seats

    print(avaliable_seats)

    return avaliable_seats